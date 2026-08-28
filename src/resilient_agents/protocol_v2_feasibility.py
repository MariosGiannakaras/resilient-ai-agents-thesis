"""Physical-machine T-526 protocol-v2 Phase-A feasibility/discrimination runner.

This module consumes the predeclared non-final feasibility plan and writes only
bounded pilot evidence under ``results/pilots``. It never reads final-reserve
configuration/results and never selects an environment from preferred method
rankings.

The first T-526 physical gate covers ordered GridWorld discrimination plus core
method/runtime/checkpoint feasibility. Phase-B severity calibration remains a
subsequent T-526 step after the selected level is known; its candidate set is
already predeclared in the same plan.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from .agents import TabularQLearningAgent, TabularQLearningConfig
from .contracts import InformationPolicy, ScenarioSpec
from .dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig
from .environment import EnvironmentSeeds
from .gridworld import ACTION_NAMES, GridWorldEnvironment
from .protocol_v2 import (
    ProtocolV2TaskSemantics,
    TabularQScientificStateAdapter,
    dyna_q_plus_state_adapter,
    sarsa_state_adapter,
)
from .protocol_v2_executor import execute_phase_a
from .protocol_v2_runtime import (
    NoLearningProbePlan,
    PhaseARequest,
    ProbeResult,
    ProtocolV2MethodConfig,
    ProtocolV2RootIdentity,
)
from .protocol_v2_sb3 import dqn_state_adapter, ppo_state_adapter
from .protocol_v2_sb3_driver import SB3PhaseADriver, SB3_IMPLEMENTATION_ID
from .protocol_v2_sb3_gridworld import ExplicitSeededGridWorldEnv
from .protocol_v2_sb3_seeding import reseed_sb3_behavior_rng
from .protocol_v2_tabular_driver import (
    PROJECT_IMPLEMENTATION_ID,
    ProjectTabularNoLearningProbeEvaluator,
    ProjectTabularPhaseADriver,
)
from .randomness import derive_scoped_seed
from .sarsa import SarsaAgent, SarsaConfig

PLAN_SCHEMA_VERSION = 1
CORE_METHOD_IDS = ("q_learning", "sarsa", "dqn", "ppo", "dyna_q_plus")
STRICT_POLICY = InformationPolicy(False, False, False, False, False)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def load_plan(path: Path) -> Mapping[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("feasibility plan must be a JSON object")
    required = {
        "schema_version",
        "pilot_id",
        "scientific_status",
        "purpose",
        "final_reserve_access",
        "required_host",
        "task",
        "phase_a",
        "roots",
        "provisional_method_configs",
        "ordered_gridworld_ladder",
        "level_selection_rule",
        "runtime_guardrails",
        "phase_b_calibration_candidates_after_level_selection",
        "output",
    }
    if set(payload) != required:
        raise ValueError("feasibility plan keys mismatch")
    if payload["schema_version"] != PLAN_SCHEMA_VERSION:
        raise ValueError("unsupported feasibility plan schema_version")
    if payload["scientific_status"] != "non-final-feasibility-only":
        raise ValueError("T-526 plan must be marked non-final feasibility only")
    if payload["final_reserve_access"] is not False:
        raise ValueError("T-526 feasibility plan must forbid final-reserve access")
    methods = payload["provisional_method_configs"]
    if not isinstance(methods, Mapping) or tuple(sorted(methods)) != tuple(sorted(CORE_METHOD_IDS)):
        raise ValueError("feasibility plan must configure exactly the five core methods")
    phase_a = payload["phase_a"]
    budget = int(phase_a["training_interaction_budget"])
    indices = tuple(int(item) for item in phase_a["probe_interaction_indices"])
    if budget <= 0 or not indices or indices[-1] != budget or indices[0] != 0:
        raise ValueError("Phase-A probe grid must start at 0 and end at the exact budget")
    ppo_quantum = int(methods["ppo"]["n_steps"])
    if any(index % ppo_quantum != 0 for index in indices):
        raise ValueError("all T-526 probe indices must align with the PPO rollout quantum")
    roots = payload["roots"]
    if not isinstance(roots, list) or len(roots) < 2:
        raise ValueError("T-526 requires multiple explicit roots")
    level_orders = [int(item["selection_order"]) for item in payload["ordered_gridworld_ladder"]]
    if level_orders != list(range(1, len(level_orders) + 1)):
        raise ValueError("GridWorld ladder selection_order must be contiguous from 1")
    return payload


def _root(value: Mapping[str, Any]) -> ProtocolV2RootIdentity:
    return ProtocolV2RootIdentity(**dict(value))


def _scenario(plan: Mapping[str, Any], layout: Mapping[str, Any]) -> ScenarioSpec:
    task = plan["task"]
    return ScenarioSpec(
        scenario_id=str(layout["layout_id"]),
        environment_id=str(task["environment_id"]),
        max_steps=int(layout["max_steps"]),
        reward_spec=dict(task["reward_spec"]),
        initial_state_spec={
            "grid": {
                "width": int(layout["width"]),
                "height": int(layout["height"]),
                "start": list(layout["start"]),
                "goal": list(layout["goal"]),
                "obstacles": [list(item) for item in layout["obstacles"]],
            }
        },
        dynamics_spec={
            "action_vectors": {
                "up": [0, -1],
                "right": [1, 0],
                "down": [0, 1],
                "left": [-1, 0],
            }
        },
        observation_spec={
            "type": "position",
            "coordinate_order": "x-y",
            "reset_observation": "true-state",
        },
        action_disturbance_spec={
            "type": "no-op-failure",
            "failure_probability": 0.0,
        },
        observation_disturbance_spec={
            "type": "position-mislocalization",
            "mislocalization_probability": 0.0,
        },
        change_events=(),
        information_policy=STRICT_POLICY,
    )


def _episode_seeds(
    root: ProtocolV2RootIdentity,
    *,
    scope: str,
    count: int,
) -> tuple[EnvironmentSeeds, ...]:
    result: list[EnvironmentSeeds] = []
    for index in range(count):
        child = f"{scope}:episode:{index}"
        result.append(
            EnvironmentSeeds(
                scenario=derive_scoped_seed(root.scenario_seed, child),
                environment=derive_scoped_seed(root.environment_seed, child),
                action_disturbance=derive_scoped_seed(root.action_disturbance_seed, child),
                observation_disturbance=derive_scoped_seed(
                    root.observation_disturbance_seed, child
                ),
            )
        )
    return tuple(result)


class SB3ProjectGridWorldProbeEvaluator:
    """Deterministic no-learning SB3 probe on explicit project GridWorld seeds."""

    def __init__(self, *, scenario: ScenarioSpec, seeds: Sequence[EnvironmentSeeds]) -> None:
        self.scenario = scenario
        self.seeds = tuple(seeds)
        if not self.seeds:
            raise ValueError("probe seeds must be non-empty")

    def __call__(self, adapter, *, training_interaction_index: int, episodes: int) -> ProbeResult:
        if episodes <= 0 or episodes > len(self.seeds):
            raise ValueError("invalid probe episode count")
        returns: list[float] = []
        lengths: list[int] = []
        successes = 0
        truncations = 0
        interactions = 0
        for seeds in self.seeds[:episodes]:
            environment = GridWorldEnvironment(self.scenario)
            try:
                observation = environment.reset(seeds=seeds)
                total = 0.0
                length = 0
                while True:
                    action = adapter.predict(observation, deterministic=True)
                    if hasattr(action, "item"):
                        action = action.item()
                    truth = environment.step(int(action))
                    total += float(truth.reward)
                    length += 1
                    interactions += 1
                    observation = truth.delivered_observation
                    if truth.terminated or truth.truncated:
                        successes += int(truth.terminated)
                        truncations += int(truth.truncated)
                        break
                returns.append(total)
                lengths.append(length)
            finally:
                environment.close()
        return ProbeResult(
            training_interaction_index=training_interaction_index,
            probe_environment_interactions=interactions,
            episodes=episodes,
            metrics={
                "return_mean": float(statistics.fmean(returns)),
                "episode_length_mean": float(statistics.fmean(lengths)),
                "terminated_rate": successes / episodes,
                "truncated_rate": truncations / episodes,
            },
        )


def _project_driver(method_id: str, parameters: Mapping[str, Any], scenario: ScenarioSpec, root: ProtocolV2RootIdentity):
    common = dict(
        actions=ACTION_NAMES,
        learning_rate=float(parameters["learning_rate"]),
        discount_factor=float(parameters["discount_factor"]),
        exploration_epsilon=float(parameters["exploration_epsilon"]),
        bootstrap_on_truncation=bool(parameters["bootstrap_on_truncation"]),
        initial_q_value=float(parameters["initial_q_value"]),
    )
    if method_id == "q_learning":
        agent = TabularQLearningAgent(
            TabularQLearningConfig(agent_id="q-learning-t526", learning_enabled=True, **common),
            checkpoint=None,
        )
        adapter = TabularQScientificStateAdapter(agent)
    elif method_id == "sarsa":
        agent = SarsaAgent(SarsaConfig(agent_id="sarsa-t526", **common), checkpoint=None)
        adapter = sarsa_state_adapter(agent)
    elif method_id == "dyna_q_plus":
        agent = DynaQPlusAgent(
            DynaQPlusConfig(
                agent_id="dyna-q-plus-t526",
                planning_steps=int(parameters["planning_steps"]),
                kappa=float(parameters["kappa"]),
                **common,
            ),
            checkpoint=None,
        )
        adapter = dyna_q_plus_state_adapter(agent)
    else:
        raise ValueError(f"unsupported project method: {method_id}")
    return ProjectTabularPhaseADriver(adapter=adapter, scenario=scenario, root=root)


def _sb3_driver(method_id: str, parameters: Mapping[str, Any], scenario: ScenarioSpec, root: ProtocolV2RootIdentity, budget: int):
    try:
        from stable_baselines3 import DQN, PPO
    except ImportError as exc:
        raise RuntimeError("T-526 requires the protocol-v2-pilot dependency group") from exc

    training_seed_schedule = _episode_seeds(
        root,
        scope="protocol-v2-phase-a",
        count=budget + 1,
    )

    def environment_factory():
        return ExplicitSeededGridWorldEnv(
            scenario=scenario,
            episode_seeds=training_seed_schedule,
        )

    seed = int(root.initialization_seed % (2**32))
    if method_id == "dqn":
        model = DQN(
            "MlpPolicy",
            environment_factory(),
            learning_rate=float(parameters["learning_rate"]),
            buffer_size=int(parameters["buffer_size"]),
            learning_starts=int(parameters["learning_starts"]),
            batch_size=int(parameters["batch_size"]),
            gamma=float(parameters["discount_factor"]),
            train_freq=int(parameters["train_freq"]),
            gradient_steps=int(parameters["gradient_steps"]),
            target_update_interval=int(parameters["target_update_interval"]),
            exploration_fraction=float(parameters["exploration_fraction"]),
            exploration_initial_eps=float(parameters["exploration_initial_eps"]),
            exploration_final_eps=float(parameters["exploration_final_eps"]),
            policy_kwargs={"net_arch": list(parameters["net_arch"])},
            seed=seed,
            device="cpu",
            verbose=0,
        )
        adapter = dqn_state_adapter(
            model,
            configuration=dict(parameters),
            environment_factory=environment_factory,
        )
    elif method_id == "ppo":
        model = PPO(
            "MlpPolicy",
            environment_factory(),
            learning_rate=float(parameters["learning_rate"]),
            n_steps=int(parameters["n_steps"]),
            batch_size=int(parameters["batch_size"]),
            n_epochs=int(parameters["n_epochs"]),
            gamma=float(parameters["discount_factor"]),
            gae_lambda=float(parameters["gae_lambda"]),
            clip_range=float(parameters["clip_range"]),
            ent_coef=float(parameters["ent_coef"]),
            vf_coef=float(parameters["vf_coef"]),
            max_grad_norm=float(parameters["max_grad_norm"]),
            policy_kwargs={"net_arch": dict(parameters["net_arch"])},
            seed=seed,
            device="cpu",
            verbose=0,
        )
        adapter = ppo_state_adapter(
            model,
            configuration=dict(parameters),
            environment_factory=environment_factory,
        )
    else:
        raise ValueError(f"unsupported SB3 method: {method_id}")
    reseed_sb3_behavior_rng(adapter, exploration_seed=root.exploration_seed)
    return SB3PhaseADriver(adapter)


def _phase_a_request(plan: Mapping[str, Any], *, method_id: str, parameters: Mapping[str, Any], root: ProtocolV2RootIdentity, layout_id: str) -> PhaseARequest:
    phase_a = plan["phase_a"]
    task = plan["task"]
    return PhaseARequest(
        protocol_version="protocol-v2.0-feasibility-v0.1",
        experiment_id=f"t526-{layout_id}-{root.root_id}-{method_id}",
        layout_id=layout_id,
        root=root,
        task=ProtocolV2TaskSemantics(
            gamma=float(task["gamma"]),
            reward_contract=dict(task["reward_spec"]),
            administrative_truncation=True,
            bootstrap_on_truncation=True,
        ),
        method=ProtocolV2MethodConfig(
            method_id=method_id,
            implementation_id=str(parameters["implementation_id"]),
            parameters=dict(parameters),
        ),
        training_interaction_budget=int(phase_a["training_interaction_budget"]),
        probe_plan=NoLearningProbePlan(
            interaction_indices=tuple(phase_a["probe_interaction_indices"]),
            episodes_per_probe=int(phase_a["episodes_per_probe"]),
        ),
    )


def run_unit(plan: Mapping[str, Any], *, level_id: str, layout: Mapping[str, Any], root_data: Mapping[str, Any], method_id: str) -> Mapping[str, Any]:
    root = _root(root_data)
    parameters = dict(plan["provisional_method_configs"][method_id])
    scenario = _scenario(plan, layout)
    budget = int(plan["phase_a"]["training_interaction_budget"])
    probe_count = int(plan["phase_a"]["episodes_per_probe"])
    probe_seeds = _episode_seeds(
        root,
        scope=f"protocol-v2-phase-a-probe:{layout['layout_id']}",
        count=probe_count,
    )

    if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
        driver = _project_driver(method_id, parameters, scenario, root)
        evaluator = ProjectTabularNoLearningProbeEvaluator(
            scenario=scenario,
            environment_seeds=probe_seeds,
        )
    else:
        driver = _sb3_driver(method_id, parameters, scenario, root, budget)
        evaluator = SB3ProjectGridWorldProbeEvaluator(
            scenario=scenario,
            seeds=probe_seeds,
        )

    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    try:
        execution = execute_phase_a(
            _phase_a_request(
                plan,
                method_id=method_id,
                parameters=parameters,
                root=root,
                layout_id=str(layout["layout_id"]),
            ),
            driver=driver,
            probe_evaluator=evaluator,
            checkpoint_provenance={
                "pilot_id": plan["pilot_id"],
                "level_id": level_id,
                "scientific_status": "non-final-feasibility-only",
            },
        )
        wall_seconds = time.perf_counter() - wall_start
        cpu_seconds = time.process_time() - cpu_start
        checkpoint_payload = execution.result.final_checkpoint.to_mapping()
        checkpoint_bytes = len(_canonical_json(checkpoint_payload).encode("utf-8"))
        return {
            "status": "completed",
            "level_id": level_id,
            "layout_id": layout["layout_id"],
            "root_id": root.root_id,
            "method_id": method_id,
            "implementation_id": parameters["implementation_id"],
            "training_interactions": execution.result.ledger.training_interactions,
            "probe_interactions": execution.result.ledger.probe_interactions,
            "wall_seconds": wall_seconds,
            "process_cpu_seconds": cpu_seconds,
            "checkpoint_bytes": checkpoint_bytes,
            "checkpoint_sha256": execution.result.final_checkpoint.sha256,
            "learner_state_sha256": execution.final_adapter.state_sha256(),
            "probes": [
                {
                    "interaction_index": item.training_interaction_index,
                    "environment_interactions": item.probe_environment_interactions,
                    "episodes": item.episodes,
                    "metrics": dict(item.metrics),
                }
                for item in execution.result.probes
            ],
        }
    finally:
        close = getattr(driver, "close", None)
        if callable(close):
            close()
        adapter = getattr(driver, "state_adapter", None)
        model = getattr(adapter, "model", None)
        env = model.get_env() if model is not None else None
        if env is not None:
            env.close()


def summarize_level(plan: Mapping[str, Any], level_id: str, records: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    completed = [item for item in records if item.get("status") == "completed"]
    expected = len(plan["roots"]) * len(next(item for item in plan["ordered_gridworld_ladder"] if item["level_id"] == level_id)["layouts"]) * len(CORE_METHOD_IDS)
    if len(completed) != expected:
        return {
            "level_id": level_id,
            "status": "incomplete-review-required",
            "expected_units": expected,
            "completed_units": len(completed),
            "selected": False,
        }

    early_index = int(plan["phase_a"]["probe_interaction_indices"][1])
    final_index = int(plan["phase_a"]["training_interaction_budget"])
    method_summary: dict[str, Any] = {}
    for method_id in CORE_METHOD_IDS:
        rows = [item for item in completed if item["method_id"] == method_id]
        early = []
        final = []
        walls = []
        cpus = []
        checkpoint_sizes = []
        for row in rows:
            by_index = {probe["interaction_index"]: probe for probe in row["probes"]}
            early.append(float(by_index[early_index]["metrics"]["terminated_rate"]))
            final.append(float(by_index[final_index]["metrics"]["terminated_rate"]))
            walls.append(float(row["wall_seconds"]))
            cpus.append(float(row["process_cpu_seconds"]))
            checkpoint_sizes.append(int(row["checkpoint_bytes"]))
        method_summary[method_id] = {
            "early_success_median": float(statistics.median(early)),
            "final_success_median": float(statistics.median(final)),
            "wall_seconds_median": float(statistics.median(walls)),
            "process_cpu_seconds_median": float(statistics.median(cpus)),
            "checkpoint_bytes_max": max(checkpoint_sizes),
        }

    universal_floor = all(
        item["final_success_median"] <= 0.10 for item in method_summary.values()
    )
    universal_early_ceiling = all(
        item["early_success_median"] >= 0.90 for item in method_summary.values()
    )
    acceptable = not universal_floor and not universal_early_ceiling
    return {
        "level_id": level_id,
        "status": "acceptable" if acceptable else "rejected-by-predeclared-discrimination-rule",
        "selected": acceptable,
        "universal_floor": universal_floor,
        "universal_early_ceiling": universal_early_ceiling,
        "method_summary": method_summary,
    }


def _validate_host(plan: Mapping[str, Any]) -> Mapping[str, Any]:
    snapshot = {
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "python_executable_basename": Path(sys.executable).name,
        "cpu_count": os.cpu_count(),
    }
    if snapshot["platform_system"] != "Windows":
        raise RuntimeError("T-526 must execute on the validated physical Windows thesis machine")
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError("T-526 requires CPython 3.12")
    return snapshot


def _git_commit(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(_canonical_json(value) + "\n")


def run_physical_phase_a_gate(*, repo_root: Path, plan_path: Path) -> Path:
    plan = load_plan(plan_path)
    host = _validate_host(plan)
    output_dir = repo_root / str(plan["output"]["directory"])
    if output_dir.exists() and any(output_dir.iterdir()):
        raise RuntimeError(
            f"pilot output directory already exists and is non-empty: {output_dir}"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    runs_path = output_dir / "phase-a-runs.jsonl"
    failures_path = output_dir / "failures.jsonl"
    runs_path.write_text("", encoding="utf-8")
    failures_path.write_text("", encoding="utf-8")

    accepted_capability = repo_root / "docs" / "context" / "system-capability.accepted.json"
    if not accepted_capability.exists():
        raise RuntimeError("accepted target-machine capability snapshot is missing")
    (output_dir / "system-capability.json").write_text(
        accepted_capability.read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "pilot_id": plan["pilot_id"],
        "scientific_status": plan["scientific_status"],
        "final_reserve_access": False,
        "plan_sha256": _sha256(plan),
        "git_commit": _git_commit(repo_root),
        "started_unix_seconds": time.time(),
        "host": host,
    }
    (output_dir / "manifest.json").write_text(
        _canonical_json(manifest) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    level_summaries: list[Mapping[str, Any]] = []
    selected_level: str | None = None
    hard_limit = float(plan["runtime_guardrails"]["hard_abort_seconds_per_method_root_layout"])

    for level in plan["ordered_gridworld_ladder"]:
        level_records: list[Mapping[str, Any]] = []
        stop_for_runtime = False
        for layout in level["layouts"]:
            for root_data in plan["roots"]:
                for method_id in CORE_METHOD_IDS:
                    try:
                        record = run_unit(
                            plan,
                            level_id=str(level["level_id"]),
                            layout=layout,
                            root_data=root_data,
                            method_id=method_id,
                        )
                        _append_jsonl(runs_path, record)
                        level_records.append(record)
                        if float(record["wall_seconds"]) > hard_limit:
                            _append_jsonl(
                                failures_path,
                                {
                                    "kind": "runtime-guardrail",
                                    "message": "completed unit exceeded hard runtime limit; pilot stops after retaining the unit",
                                    "level_id": level["level_id"],
                                    "layout_id": layout["layout_id"],
                                    "root_id": root_data["root_id"],
                                    "method_id": method_id,
                                    "wall_seconds": record["wall_seconds"],
                                    "hard_limit_seconds": hard_limit,
                                },
                            )
                            stop_for_runtime = True
                            break
                    except Exception as exc:  # retained feasibility outcome
                        failure = {
                            "kind": "scientific-or-feasibility-failure",
                            "level_id": level["level_id"],
                            "layout_id": layout["layout_id"],
                            "root_id": root_data["root_id"],
                            "method_id": method_id,
                            "exception_type": type(exc).__name__,
                            "message": str(exc),
                        }
                        _append_jsonl(failures_path, failure)
                        level_records.append({"status": "failed", **failure})
                if stop_for_runtime:
                    break
            if stop_for_runtime:
                break

        summary = summarize_level(plan, str(level["level_id"]), level_records)
        if stop_for_runtime:
            summary = {**summary, "status": "runtime-review-required", "selected": False}
        level_summaries.append(summary)
        if summary.get("selected") is True:
            selected_level = str(level["level_id"])
            break
        if summary["status"] in {"incomplete-review-required", "runtime-review-required"}:
            break

    level_summary = {
        "pilot_id": plan["pilot_id"],
        "selection_rule": dict(plan["level_selection_rule"]),
        "selected_level": selected_level,
        "levels": level_summaries,
        "next_gate": (
            "phase-b-severity-calibration"
            if selected_level is not None
            else "manual-review-before-protocol-amendment"
        ),
    }
    (output_dir / "level-summary.json").write_text(
        _canonical_json(level_summary) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return output_dir


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Run the predeclared T-526 protocol-v2 physical Windows Phase-A feasibility gate."
    )
    parser.add_argument(
        "--plan",
        default="configs/protocols/protocol-v2-feasibility-v0.1.json",
    )
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    output = run_physical_phase_a_gate(
        repo_root=repo_root,
        plan_path=(repo_root / args.plan).resolve(),
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
