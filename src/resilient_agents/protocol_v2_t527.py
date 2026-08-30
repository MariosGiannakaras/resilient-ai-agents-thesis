"""DEC-055 fair tuning, multi-episode sizing, and evidence validation.

The module has three deliberately separate roles:

* derive a deterministic diagnostic package from immutable T-526 evidence;
* execute the one reviewed native-Windows non-final tuning/sizing program;
* validate the generated packages without reading any final-reserve path.

No final layout or final root is materialized here.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import statistics
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .evidence_v2.statistics import trapezoidal_time_average
from .protocol_v2 import ProtocolV2Branch, fork_four_branches
from .protocol_v2_boundary_settlement import settle_phase_a_interaction_boundary
from .protocol_v2_executor import execute_phase_a
from .protocol_v2_feasibility import (
    CORE_METHOD_IDS,
    SB3ProjectGridWorldProbeEvaluator,
    _episode_seeds,
    _project_driver,
    _root,
    _sb3_driver,
    _scenario,
)
from .protocol_v2_prefix import prepare_shared_no_learning_prefix
from .protocol_v2_runtime import (
    NoLearningProbePlan,
    PhaseARequest,
    ProtocolV2MethodConfig,
    ProtocolV2TaskSemantics,
)
from .protocol_v2_sb3_phase_b import SB3PhaseBBranchDriver
from .protocol_v2_t526_boundary_phase_b_v03 import (
    validate_phase_b_v03_attempt,
    validate_settlement_evidence,
)
from .protocol_v2_t526_recovery import verify_original_bundle
from .protocol_v2_t526_recovery_v02 import (
    load_amendment as load_dec053_amendment,
)
from .protocol_v2_t526_recovery_v02 import (
    validate_phase_b_attempt_evidence as validate_dec053_phase_b,
)
from .protocol_v2_t526_recovery_v02 import (
    validate_recovery_attempt_evidence as validate_dec053_recovery,
)
from .protocol_v2_t526_recovery_v02 import (
    verify_prior_failed_recovery,
)
from .protocol_v2_tabular_driver import ProjectTabularNoLearningProbeEvaluator
from .protocol_v2_tabular_phase_b import ProjectTabularPhaseBBranchDriver
from .study.protocol_v2_phase_b_executor import _disturbed_spec

PLAN_SCHEMA_VERSION = 1
BRANCHES = tuple(ProtocolV2Branch)
TUNING_FILES = (
    "manifest.json",
    "tuning-runs.jsonl",
    "selection.json",
    "failures.jsonl",
    "integrity.json",
)
SIZING_FILES = (
    "manifest.json",
    "phase-a-sizing.jsonl",
    "phase-b-sizing.jsonl",
    "selection.json",
    "failures.jsonl",
    "integrity.json",
)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256_value(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(_canonical_json(value) + "\n", encoding="utf-8", newline="\n")


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(_canonical_json(value) + "\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, Mapping):
                raise ValueError(f"JSONL row must be an object: {path}")
            rows.append(dict(value))
    return rows


def _git_commit(repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
    ).strip()


def _host() -> Mapping[str, Any]:
    result = {
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "python_executable_basename": Path(sys.executable).name,
        "cpu_count": os.cpu_count(),
    }
    if result["platform_system"] != "Windows" or sys.version_info[:2] != (3, 12):
        raise RuntimeError("DEC-055 physical tuning/sizing requires native Windows CPython 3.12")
    return result


def load_plan(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("DEC-055 plan must be an object")
    required = {
        "schema_version",
        "decision_id",
        "study_id",
        "scientific_status",
        "purpose",
        "final_reserve_access",
        "required_host",
        "immutable_inputs",
        "task",
        "development_layouts",
        "tuning",
        "candidate_configs",
        "sizing",
        "phase_b_lifecycle",
        "outputs",
    }
    if set(value) != required or value["schema_version"] != PLAN_SCHEMA_VERSION:
        raise ValueError("DEC-055 plan schema/keys mismatch")
    if value["decision_id"] != "DEC-055" or value["final_reserve_access"] is not False:
        raise ValueError("DEC-055 identity/final-reserve firewall mismatch")
    if tuple(sorted(value["candidate_configs"])) != tuple(sorted(CORE_METHOD_IDS)):
        raise ValueError("DEC-055 must start exactly the five core methods")
    expected = int(value["tuning"]["configuration_count_per_method"])
    for method_id in CORE_METHOD_IDS:
        configs = value["candidate_configs"][method_id]
        if len(configs) != expected or len({item["config_id"] for item in configs}) != expected:
            raise ValueError(f"{method_id} must have exactly {expected} unique candidates")
    probes = tuple(int(item) for item in value["tuning"]["probe_interaction_indices"])
    budget = int(value["tuning"]["training_interaction_budget"])
    if probes != (0, 512, 1024, 2048, 4096, 8192) or budget != 8192:
        raise ValueError("DEC-055 common tuning budget/probe grid changed")
    if any(index % 128 for index in probes):
        raise ValueError("DEC-055 probes must preserve the PPO update boundary")
    if tuple(value["sizing"]["root_count_candidates"]) != (12, 16, 20, 24):
        raise ValueError("DEC-055 root-count candidates changed")
    if tuple(value["sizing"]["phase_b_horizon_candidates"]) != (256, 512):
        raise ValueError("DEC-055 horizon candidates changed")
    lifecycle = value["phase_b_lifecycle"]
    required_true = {
        "learner_persists_across_episode_resets",
        "actual_interaction_clock_persists",
        "disturbed_regime_persists_across_episode_resets",
        "nominal_and_disturbed_branches_use_common_episode_seed_schedules_where_valid",
        "administrative_truncation_bootstraps",
    }
    if any(lifecycle.get(key) is not True for key in required_true):
        raise ValueError("DEC-055 multi-episode persistence contract changed")
    if lifecycle["learning_state_reset_on_episode_boundary"] is not False:
        raise ValueError("DEC-055 forbids learning-state reset at episode boundaries")
    for output_path in value["outputs"].values():
        if "final" in str(output_path).lower() or "reserve" in str(output_path).lower():
            raise ValueError("DEC-055 output path violates final-reserve firewall")
    return value


def verify_immutable_inputs(*, repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Any]:
    dec053_path = repo_root / "configs/protocols/protocol-v2-t526-recovery-phase-b-v0.2.json"
    dec053 = load_dec053_amendment(dec053_path)
    original = verify_original_bundle(repo_root=repo_root, amendment=dec053)
    dec052 = verify_prior_failed_recovery(repo_root=repo_root, amendment=dec053)
    recovery = validate_dec053_recovery(repo_root=repo_root, amendment=dec053)
    failed_phase_b = validate_dec053_phase_b(repo_root=repo_root, amendment=dec053)
    dec054_path = repo_root / "configs/protocols/protocol-v2-t526-boundary-settlement-phase-b-v0.3.json"
    dec054 = json.loads(dec054_path.read_text(encoding="utf-8"))
    settlement = validate_settlement_evidence(repo_root=repo_root, config=dec054)
    phase_b = validate_phase_b_v03_attempt(repo_root=repo_root, config=dec054)
    if recovery["status"] != "valid-complete":
        raise RuntimeError("DEC-053 recovery input is not valid-complete")
    if failed_phase_b["status"] != "valid-failed":
        raise RuntimeError("DEC-053 failed Phase-B history is not valid-failed")
    if settlement["status"] != "valid-complete" or phase_b["status"] != "valid-complete":
        raise RuntimeError("DEC-054 retained evidence is not valid-complete")
    for declared in plan["immutable_inputs"].values():
        if not (repo_root / str(declared)).is_dir():
            raise RuntimeError(f"declared immutable input is missing: {declared}")
    return {
        "original_phase_a_files": original,
        "dec052_files": dec052,
        "dec053_recovery": recovery,
        "dec053_failed_phase_b": failed_phase_b,
        "dec054_settlement": settlement,
        "dec054_phase_b": phase_b,
    }


def write_input_diagnostics(*, repo_root: Path, plan: Mapping[str, Any]) -> Path:
    validation = verify_immutable_inputs(repo_root=repo_root, plan=plan)
    output = repo_root / str(plan["outputs"]["input_diagnostics"])
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"input diagnostic output already exists: {output}")
    output.mkdir(parents=True, exist_ok=True)
    phase_a_rows = _read_jsonl(
        repo_root / str(plan["immutable_inputs"]["phase_a"]) / "phase-a-runs.jsonl"
    )
    phase_b_rows = _read_jsonl(
        repo_root / str(plan["immutable_inputs"]["dec054_phase_b"]) / "matched-sets.jsonl"
    )
    method_diagnostics: dict[str, Any] = {}
    for method_id in CORE_METHOD_IDS:
        rows = [item for item in phase_a_rows if item["method_id"] == method_id]
        by_index: dict[str, Any] = {}
        for index in (0, 512, 1024, 2048):
            success = []
            returns = []
            for row in rows:
                probe = next(item for item in row["probes"] if item["interaction_index"] == index)
                success.append(float(probe["metrics"]["terminated_rate"]))
                returns.append(float(probe["metrics"]["return_mean"]))
            by_index[str(index)] = {
                "terminated_rate_mean": statistics.fmean(success),
                "terminated_rate_standard_deviation": statistics.stdev(success),
                "return_mean": statistics.fmean(returns),
            }
        method_diagnostics[method_id] = {
            "units": len(rows),
            "probes": by_index,
            "wall_seconds_sum": sum(float(item["wall_seconds"]) for item in rows),
            "process_cpu_seconds_sum": sum(float(item["process_cpu_seconds"]) for item in rows),
            "checkpoint_bytes_sum": sum(int(item["checkpoint_bytes"]) for item in rows),
            "failures": 0,
        }
    condition_diagnostics: dict[str, Any] = {}
    for condition_id in sorted({item["condition_id"] for item in phase_b_rows}):
        rows = [item for item in phase_b_rows if item["condition_id"] == condition_id]
        frozen_losses = []
        adaptive_losses = []
        benefits = []
        for row in rows:
            values = {item["branch"]: float(item["metrics"]["return_sum"]) for item in row["branches"]}
            frozen = values["FN"] - values["FD"]
            adaptive = values["AN"] - values["AD"]
            frozen_losses.append(frozen)
            adaptive_losses.append(adaptive)
            benefits.append(frozen - adaptive)
        condition_diagnostics[condition_id] = {
            "matched_sets": len(rows),
            "frozen_loss_mean": statistics.fmean(frozen_losses),
            "adaptive_loss_mean": statistics.fmean(adaptive_losses),
            "adaptation_benefit_mean": statistics.fmean(benefits),
            "adaptation_benefit_standard_deviation": statistics.stdev(benefits),
        }
    diagnostics = {
        "schema_version": 1,
        "decision_id": "DEC-055",
        "scientific_status": "non-final-input-diagnostics-only",
        "final_reserve_access": False,
        "source_phase_a_units": len(phase_a_rows),
        "source_phase_b_matched_sets": len(phase_b_rows),
        "method_diagnostics": method_diagnostics,
        "condition_diagnostics": condition_diagnostics,
        "interpretation_boundary": "descriptive immutable T-526 inputs only; candidate tuning rules were frozen independently",
    }
    _write_json(output / "diagnostics.json", diagnostics)
    manifest = {
        "schema_version": 1,
        "decision_id": "DEC-055",
        "scientific_status": "non-final-input-diagnostics-only",
        "final_reserve_access": False,
        "plan_sha256": _sha256_value(plan),
        "immutable_input_validation_sha256": _sha256_value(validation),
        "diagnostics_sha256": _sha256_file(output / "diagnostics.json"),
    }
    _write_json(output / "manifest.json", manifest)
    _write_integrity(output)
    return output


def _phase_a_request(
    plan: Mapping[str, Any],
    *,
    method_id: str,
    parameters: Mapping[str, Any],
    root: Any,
    layout_id: str,
    budget: int,
    probes: Sequence[int],
    protocol_version: str = "protocol-v2.0-t527-development-v0.1",
) -> PhaseARequest:
    return PhaseARequest(
        protocol_version=protocol_version,
        experiment_id=f"t527-{layout_id}-{root.root_id}-{method_id}-{parameters['config_id']}",
        layout_id=layout_id,
        root=root,
        task=ProtocolV2TaskSemantics(
            gamma=float(plan["task"]["gamma"]),
            reward_contract=dict(plan["task"]["reward_spec"]),
            administrative_truncation=True,
            bootstrap_on_truncation=True,
        ),
        method=ProtocolV2MethodConfig(
            method_id=method_id,
            implementation_id=str(parameters["implementation_id"]),
            parameters={key: value for key, value in parameters.items() if key != "config_id"},
        ),
        training_interaction_budget=budget,
        probe_plan=NoLearningProbePlan(
            interaction_indices=tuple(int(item) for item in probes),
            episodes_per_probe=int(plan["tuning"]["episodes_per_probe"]),
        ),
    )


def _run_phase_a_unit(
    *,
    plan: Mapping[str, Any],
    method_id: str,
    parameters: Mapping[str, Any],
    root_data: Mapping[str, Any],
    layout: Mapping[str, Any],
    budget: int,
    probes: Sequence[int],
    decision_id: str = "DEC-055",
    protocol_version: str = "protocol-v2.0-t527-development-v0.1",
) -> tuple[Mapping[str, Any], Any, Any]:
    root = _root(root_data)
    scenario_plan = {
        "task": plan["task"],
    }
    scenario = _scenario(scenario_plan, layout)
    clean_parameters = {key: value for key, value in parameters.items() if key != "config_id"}
    probe_seeds = _episode_seeds(
        root,
        scope=f"protocol-v2-t527-phase-a-probe:{layout['layout_id']}",
        count=int(plan["tuning"]["episodes_per_probe"]),
    )
    if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
        driver = _project_driver(method_id, clean_parameters, scenario, root)
        evaluator = ProjectTabularNoLearningProbeEvaluator(
            scenario=scenario,
            environment_seeds=probe_seeds,
        )
    else:
        driver = _sb3_driver(method_id, clean_parameters, scenario, root, budget)
        evaluator = SB3ProjectGridWorldProbeEvaluator(scenario=scenario, seeds=probe_seeds)
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    execution = execute_phase_a(
        _phase_a_request(
            plan,
            method_id=method_id,
            parameters=parameters,
            root=root,
            layout_id=str(layout["layout_id"]),
            budget=budget,
            probes=probes,
            protocol_version=protocol_version,
        ),
        driver=driver,
        probe_evaluator=evaluator,
        checkpoint_provenance={
            "decision_id": decision_id,
            "scientific_status": "non-final-development-only",
            "config_id": parameters["config_id"],
        },
    )
    payload = execution.result.final_checkpoint.to_mapping()
    row = {
        "status": "completed",
        "method_id": method_id,
        "config_id": parameters["config_id"],
        "root_id": root.root_id,
        "layout_id": layout["layout_id"],
        "training_interactions": budget,
        "probe_interactions": execution.result.ledger.probe_interactions,
        "wall_seconds": time.perf_counter() - wall_start,
        "process_cpu_seconds": time.process_time() - cpu_start,
        "checkpoint_bytes": len(_canonical_json(payload).encode("utf-8")),
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
    return row, execution, driver


def _close_phase_a(driver: Any) -> None:
    close = getattr(driver, "close", None)
    if callable(close):
        close()
    adapter = getattr(driver, "state_adapter", None)
    model = getattr(adapter, "model", None)
    env = model.get_env() if model is not None else None
    if env is not None:
        env.close()


def _probe_value(row: Mapping[str, Any], index: int, metric: str) -> float:
    probe = next(item for item in row["probes"] if int(item["interaction_index"]) == index)
    return float(probe["metrics"][metric])


def _curve_auc(row: Mapping[str, Any], metric: str) -> float:
    return trapezoidal_time_average(
        [(int(item["interaction_index"]), float(item["metrics"][metric])) for item in row["probes"]]
    )


def _select_configs(plan: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    selected: dict[str, Any] = {}
    rankings: dict[str, Any] = {}
    budget = int(plan["tuning"]["training_interaction_budget"])
    for method_id in CORE_METHOD_IDS:
        candidates = []
        for config in plan["candidate_configs"][method_id]:
            subset = [row for row in rows if row["method_id"] == method_id and row["config_id"] == config["config_id"]]
            expected = len(plan["tuning"]["roots"]) * len(plan["development_layouts"])
            if len(subset) != expected:
                raise RuntimeError(f"incomplete tuning candidate: {method_id}/{config['config_id']}")
            score = {
                "config_id": config["config_id"],
                "auc_terminated_rate": statistics.fmean(_curve_auc(row, "terminated_rate") for row in subset),
                "final_terminated_rate": statistics.fmean(_probe_value(row, budget, "terminated_rate") for row in subset),
                "auc_return_mean": statistics.fmean(_curve_auc(row, "return_mean") for row in subset),
                "wall_seconds_sum": sum(float(row["wall_seconds"]) for row in subset),
            }
            candidates.append(score)
        candidates.sort(
            key=lambda item: (
                -item["auc_terminated_rate"],
                -item["final_terminated_rate"],
                -item["auc_return_mean"],
                item["config_id"],
            )
        )
        winner_id = candidates[0]["config_id"]
        selected[method_id] = next(
            dict(item) for item in plan["candidate_configs"][method_id] if item["config_id"] == winner_id
        )
        rankings[method_id] = candidates

    use_4096 = True
    budget_evidence: dict[str, Any] = {}
    for method_id in CORE_METHOD_IDS:
        winner = selected[method_id]["config_id"]
        subset = [row for row in rows if row["method_id"] == method_id and row["config_id"] == winner]
        success_gain = statistics.fmean(
            _probe_value(row, 8192, "terminated_rate") - _probe_value(row, 4096, "terminated_rate")
            for row in subset
        )
        return_gain = statistics.fmean(
            _probe_value(row, 8192, "return_mean") - _probe_value(row, 4096, "return_mean")
            for row in subset
        )
        budget_evidence[method_id] = {
            "terminated_rate_gain_4096_to_8192": success_gain,
            "return_mean_gain_4096_to_8192": return_gain,
        }
        use_4096 = use_4096 and success_gain <= 0.05 and return_gain <= 0.25
    return {
        "schema_version": 1,
        "decision_id": "DEC-055",
        "selected_configs": selected,
        "rankings": rankings,
        "phase_a_budget_evidence": budget_evidence,
        "selected_phase_a_budget": 4096 if use_4096 else 8192,
        "selection_rule": dict(plan["tuning"]["selection_rule"]),
    }


def _sizing_root(index: int) -> Mapping[str, Any]:
    return {
        "root_id": f"t527-size-r{index:02d}",
        "initialization_seed": 31000 + index,
        "exploration_seed": 32000 + index,
        "scenario_seed": 33000 + index,
        "environment_seed": 34000 + index,
        "action_disturbance_seed": 35000 + index,
        "observation_disturbance_seed": 36000 + index,
    }


def _valid_observations(layout: Mapping[str, Any]) -> set[tuple[int, int]]:
    blocked = {tuple(item) for item in layout["obstacles"]}
    return {
        (x, y)
        for x in range(int(layout["width"]))
        for y in range(int(layout["height"]))
        if (x, y) not in blocked
    }


def _run_sizing_phase_b(
    *,
    plan: Mapping[str, Any],
    method_id: str,
    parameters: Mapping[str, Any],
    root_data: Mapping[str, Any],
    layout: Mapping[str, Any],
    learner: Any,
    condition: Mapping[str, Any],
) -> Mapping[str, Any]:
    root = _root(root_data)
    nominal = _scenario({"task": plan["task"]}, layout)
    prefix_seed = _episode_seeds(
        root,
        scope=f"protocol-v2-t527-phase-b-prefix:{layout['layout_id']}:{condition['condition_id']}",
        count=1,
    )[0]
    prefix = prepare_shared_no_learning_prefix(
        learner=learner,
        nominal_spec=nominal,
        environment_seeds=prefix_seed,
        interactions=int(plan["sizing"]["common_nominal_no_learning_prefix_interactions"]),
    )
    disturbed = _disturbed_spec(
        nominal=nominal,
        condition=condition,
        onset_step=prefix.environment.environment.gym_env._step,
    )
    branch_point_learner = prefix.learner.state_sha256()
    branch_point_environment = prefix.environment.state_sha256()
    learner_branches = fork_four_branches(prefix.learner)
    episode_seeds = _episode_seeds(
        root,
        scope=f"protocol-v2-t527-phase-b-episodes:{layout['layout_id']}:{condition['condition_id']}",
        count=513,
    )
    snapshots: dict[str, Any] = {"256": [], "512": []}
    plans = {
        ProtocolV2Branch.FROZEN_NOMINAL: (False, False),
        ProtocolV2Branch.FROZEN_DISTURBED: (False, True),
        ProtocolV2Branch.ADAPTIVE_NOMINAL: (True, False),
        ProtocolV2Branch.ADAPTIVE_DISTURBED: (True, True),
    }
    environments = []
    try:
        for branch in BRANCHES:
            adaptive, is_disturbed = plans[branch]
            environment = prefix.environment.fork_into(disturbed if is_disturbed else nominal)
            environments.append(environment)
            branch_learner = learner_branches[branch]
            if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
                driver = ProjectTabularPhaseBBranchDriver(
                    branch=branch,
                    adaptive=adaptive,
                    learner=branch_learner,
                    environment=environment,
                    subsequent_episode_seeds=episode_seeds,
                )
            else:
                driver = SB3PhaseBBranchDriver(
                    branch=branch,
                    adaptive=adaptive,
                    learner=branch_learner,
                    environment=environment,
                    deterministic_inference=False,
                    subsequent_episode_seeds=episode_seeds,
                )
            for horizon in (256, 512):
                metrics = dict(driver.run_to_interaction(horizon))
                snapshots[str(horizon)].append(
                    {
                        "branch": branch.value,
                        "interactions": horizon,
                        "metrics": metrics,
                        "learner_state_sha256": branch_learner.state_sha256(),
                        "environment_state_sha256": environment.state_sha256(),
                    }
                )
    finally:
        prefix.environment.environment.close()
        for environment in environments:
            environment.environment.close()
    return {
        "status": "completed",
        "method_id": method_id,
        "config_id": parameters["config_id"],
        "root_id": root.root_id,
        "layout_id": layout["layout_id"],
        "condition_id": condition["condition_id"],
        "condition_family": condition["family"],
        "prefix_interactions": 1,
        "branch_point_learner_sha256": branch_point_learner,
        "branch_point_environment_sha256": branch_point_environment,
        "horizons": snapshots,
    }


def _half_width(values: Sequence[float], critical: float) -> float:
    return critical * statistics.stdev(values) / math.sqrt(len(values))


def _horizon_256_rule_passes(phase_b_rows: Sequence[Mapping[str, Any]]) -> bool:
    for row in phase_b_rows:
        for branch in row["horizons"]["256"]:
            if branch["branch"] in {"AN", "AD"}:
                metrics = branch["metrics"]
                if (
                    float(metrics["episodes_completed"]) < 2
                    or float(metrics["native_update_opportunities_completed"]) < 2
                ):
                    return False
    return True


def _sizing_selection(
    *,
    plan: Mapping[str, Any],
    phase_a_rows: Sequence[Mapping[str, Any]],
    phase_b_rows: Sequence[Mapping[str, Any]],
    decision_id: str = "DEC-055",
) -> Mapping[str, Any]:
    horizon_256_valid = _horizon_256_rule_passes(phase_b_rows)
    selected_horizon = 256 if horizon_256_valid else 512
    criticals = plan["sizing"]["precision_rule"]["student_t_critical_values"]
    target = float(plan["sizing"]["precision_rule"]["target_half_width"])
    precision: dict[str, Any] = {}
    selected_roots = 24
    for count in plan["sizing"]["root_count_candidates"]:
        count = int(count)
        method_values: dict[str, Any] = {}
        maximum = 0.0
        for method_id in CORE_METHOD_IDS:
            phase_a_root_values = []
            phase_b_root_values = []
            for index in range(1, count + 1):
                root_id = f"t527-size-r{index:02d}"
                a_rows = [row for row in phase_a_rows if row["method_id"] == method_id and row["root_id"] == root_id]
                phase_a_root_values.append(statistics.fmean(_curve_auc(row, "terminated_rate") for row in a_rows))
                b_rows = [row for row in phase_b_rows if row["method_id"] == method_id and row["root_id"] == root_id]
                effects = []
                for row in b_rows:
                    values = {
                        item["branch"]: float(item["metrics"]["return_sum"])
                        for item in row["horizons"][str(selected_horizon)]
                    }
                    effects.append(((values["FN"] - values["FD"]) - (values["AN"] - values["AD"])) / selected_horizon)
                phase_b_root_values.append(statistics.fmean(effects))
            critical = float(criticals[str(count)])
            a_half = _half_width(phase_a_root_values, critical)
            b_half = _half_width(phase_b_root_values, critical)
            maximum = max(maximum, a_half, b_half)
            method_values[method_id] = {
                "phase_a_auc_half_width": a_half,
                "phase_b_adaptation_benefit_per_interaction_half_width": b_half,
            }
        precision[str(count)] = {"maximum_half_width": maximum, "by_method": method_values}
        if maximum <= target and selected_roots == 24:
            selected_roots = count
    return {
        "schema_version": 1,
        "decision_id": decision_id,
        "selected_phase_b_horizon": selected_horizon,
        "horizon_256_rule_passed": horizon_256_valid,
        "selected_root_count": selected_roots,
        "precision_target_half_width": target,
        "precision_target_met": precision[str(selected_roots)]["maximum_half_width"] <= target,
        "precision_by_candidate_count": precision,
        "root_is_independent": True,
        "layouts_equal_weighted_within_root": True,
    }


def _write_integrity(directory: Path) -> Mapping[str, Any]:
    files = {
        str(path.relative_to(directory)).replace("\\", "/"): {
            "sha256": _sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(directory.rglob("*"))
        if path.is_file() and path.name != "integrity.json"
    }
    value = {"schema_version": 1, "files": files}
    _write_json(directory / "integrity.json", value)
    return value


def _new_output(repo_root: Path, relative: str) -> Path:
    output = repo_root / relative
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"retained output already exists: {output}")
    output.mkdir(parents=True, exist_ok=True)
    return output


def run_physical_tuning_and_sizing(*, repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Path]:
    host = _host()
    inputs = verify_immutable_inputs(repo_root=repo_root, plan=plan)
    tuning = _new_output(repo_root, str(plan["outputs"]["tuning"]))
    sizing = _new_output(repo_root, str(plan["outputs"]["sizing"]))
    for directory, filename in ((tuning, "tuning-runs.jsonl"), (tuning, "failures.jsonl"), (sizing, "phase-a-sizing.jsonl"), (sizing, "phase-b-sizing.jsonl"), (sizing, "failures.jsonl")):
        (directory / filename).write_text("", encoding="utf-8")
    base_manifest = {
        "schema_version": 1,
        "decision_id": "DEC-055",
        "scientific_status": plan["scientific_status"],
        "final_reserve_access": False,
        "plan_sha256": _sha256_value(plan),
        "execution_commit": _git_commit(repo_root),
        "host": host,
        "immutable_input_validation_sha256": _sha256_value(inputs),
        "started_unix_seconds": time.time(),
    }
    _write_json(tuning / "manifest.json", {**base_manifest, "stage": "fair-tuning", "expected_units": 180, "status": "in-progress"})
    tuning_rows: list[Mapping[str, Any]] = []
    for method_id in CORE_METHOD_IDS:
        for parameters in plan["candidate_configs"][method_id]:
            for root_data in plan["tuning"]["roots"]:
                for layout in plan["development_layouts"]:
                    driver = None
                    try:
                        row, _execution, driver = _run_phase_a_unit(
                            plan=plan,
                            method_id=method_id,
                            parameters=parameters,
                            root_data=root_data,
                            layout=layout,
                            budget=8192,
                            probes=plan["tuning"]["probe_interaction_indices"],
                        )
                        tuning_rows.append(row)
                        _append_jsonl(tuning / "tuning-runs.jsonl", row)
                    except Exception as exc:
                        failure = {
                            "stage": "tuning",
                            "method_id": method_id,
                            "config_id": parameters["config_id"],
                            "root_id": root_data["root_id"],
                            "layout_id": layout["layout_id"],
                            "exception_type": type(exc).__name__,
                            "message": str(exc),
                        }
                        _append_jsonl(tuning / "failures.jsonl", failure)
                        _write_json(tuning / "manifest.json", {**base_manifest, "stage": "fair-tuning", "status": "failed", "completed_units": len(tuning_rows), "failure": failure})
                        _write_integrity(tuning)
                        raise
                    finally:
                        if driver is not None:
                            _close_phase_a(driver)
    selection = _select_configs(plan, tuning_rows)
    _write_json(tuning / "selection.json", selection)
    _write_json(tuning / "manifest.json", {**base_manifest, "stage": "fair-tuning", "status": "complete", "expected_units": 180, "completed_units": len(tuning_rows), "completed_unix_seconds": time.time()})
    _write_integrity(tuning)

    sizing_manifest = {**base_manifest, "stage": "precision-runtime-sizing", "expected_phase_a_units": 240, "expected_phase_b_matched_sets": 480, "status": "in-progress"}
    _write_json(sizing / "manifest.json", sizing_manifest)
    phase_a_rows: list[Mapping[str, Any]] = []
    phase_b_rows: list[Mapping[str, Any]] = []
    budget = int(selection["selected_phase_a_budget"])
    probes = [index for index in plan["tuning"]["probe_interaction_indices"] if int(index) <= budget]
    for method_id in CORE_METHOD_IDS:
        parameters = selection["selected_configs"][method_id]
        for index in range(1, 25):
            root_data = _sizing_root(index)
            for layout in plan["development_layouts"]:
                driver = None
                try:
                    row, execution, driver = _run_phase_a_unit(
                        plan=plan,
                        method_id=method_id,
                        parameters=parameters,
                        root_data=root_data,
                        layout=layout,
                        budget=budget,
                        probes=probes,
                    )
                    learner = execution.final_adapter
                    settlement = settle_phase_a_interaction_boundary(
                        learner,
                        expected_source_learner_sha256=learner.state_sha256(),
                        expected_interactions=budget,
                        valid_observations=_valid_observations(layout),
                    )
                    checkpoint = execution.result.final_checkpoint.to_mapping()
                    checkpoint["state"] = learner.export_state()
                    checkpoint["provenance"] = {
                        **dict(checkpoint["provenance"]),
                        "boundary_settlement": settlement.to_mapping(),
                        "deployment_start_learner_sha256": learner.state_sha256(),
                    }
                    relative = Path("deployment-start-checkpoints") / method_id / root_data["root_id"] / f"{layout['layout_id']}.json"
                    target = sizing / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    _write_json(target, checkpoint)
                    row = {
                        **dict(row),
                        "settlement": settlement.to_mapping(),
                        "deployment_start_checkpoint_path": str(relative).replace("\\", "/"),
                        "deployment_start_checkpoint_file_sha256": _sha256_file(target),
                    }
                    phase_a_rows.append(row)
                    _append_jsonl(sizing / "phase-a-sizing.jsonl", row)
                    for condition in plan["sizing"]["conditions"]:
                        wall_start = time.perf_counter()
                        phase_b = _run_sizing_phase_b(
                            plan=plan,
                            method_id=method_id,
                            parameters=parameters,
                            root_data=root_data,
                            layout=layout,
                            learner=learner.clone(),
                            condition=condition,
                        )
                        phase_b = {**dict(phase_b), "wall_seconds": time.perf_counter() - wall_start}
                        phase_b_rows.append(phase_b)
                        _append_jsonl(sizing / "phase-b-sizing.jsonl", phase_b)
                except Exception as exc:
                    failure = {
                        "stage": "sizing",
                        "method_id": method_id,
                        "root_id": root_data["root_id"],
                        "layout_id": layout["layout_id"],
                        "exception_type": type(exc).__name__,
                        "message": str(exc),
                    }
                    _append_jsonl(sizing / "failures.jsonl", failure)
                    _write_json(sizing / "manifest.json", {**sizing_manifest, "status": "failed", "completed_phase_a_units": len(phase_a_rows), "completed_phase_b_matched_sets": len(phase_b_rows), "failure": failure})
                    _write_integrity(sizing)
                    raise
                finally:
                    if driver is not None:
                        _close_phase_a(driver)
    sizing_selection = _sizing_selection(plan=plan, phase_a_rows=phase_a_rows, phase_b_rows=phase_b_rows)
    _write_json(sizing / "selection.json", sizing_selection)
    _write_json(sizing / "manifest.json", {**sizing_manifest, "status": "complete", "completed_phase_a_units": len(phase_a_rows), "completed_phase_b_matched_sets": len(phase_b_rows), "completed_branch_horizon_evaluations": len(phase_b_rows) * 4 * 2, "completed_unix_seconds": time.time()})
    _write_integrity(sizing)
    return {"tuning": tuning, "sizing": sizing}


def validate_attempt(*, repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Any]:
    result: dict[str, Any] = {}
    for key, files in (("tuning", TUNING_FILES), ("sizing", SIZING_FILES)):
        directory = repo_root / str(plan["outputs"][key])
        if not directory.is_dir() or any(not (directory / name).is_file() for name in files):
            raise RuntimeError(f"DEC-055 {key} evidence is incomplete")
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        integrity = json.loads((directory / "integrity.json").read_text(encoding="utf-8"))
        if manifest["status"] != "complete" or manifest["final_reserve_access"] is not False:
            raise RuntimeError(f"DEC-055 {key} manifest is not complete/non-final")
        for relative, expected in integrity["files"].items():
            path = directory / relative
            if _sha256_file(path) != expected["sha256"] or path.stat().st_size != expected["bytes"]:
                raise RuntimeError(f"DEC-055 {key} integrity mismatch: {relative}")
        failures = _read_jsonl(directory / "failures.jsonl")
        if failures:
            raise RuntimeError(f"DEC-055 {key} contains retained failures")
        result[key] = {
            "status": "valid-complete",
            "files": len(integrity["files"]),
            "bytes": sum(int(item["bytes"]) for item in integrity["files"].values()),
        }
    tuning_rows = _read_jsonl(repo_root / str(plan["outputs"]["tuning"]) / "tuning-runs.jsonl")
    phase_a = _read_jsonl(repo_root / str(plan["outputs"]["sizing"]) / "phase-a-sizing.jsonl")
    phase_b = _read_jsonl(repo_root / str(plan["outputs"]["sizing"]) / "phase-b-sizing.jsonl")
    if len(tuning_rows) != 180 or len(phase_a) != 240 or len(phase_b) != 480:
        raise RuntimeError("DEC-055 finite evidence denominator mismatch")
    if any(len(row["horizons"]["256"]) != 4 or len(row["horizons"]["512"]) != 4 for row in phase_b):
        raise RuntimeError("DEC-055 Phase-B horizon/branch matrix mismatch")
    result.update({"tuning_units": 180, "sizing_phase_a_units": 240, "sizing_phase_b_matched_sets": 480, "branch_horizon_evaluations": 3840})
    return result


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="DEC-055 T-527 fair tuning and sizing")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default="configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json")
    parser.add_argument("--write-input-diagnostics", action="store_true")
    parser.add_argument("--validate-inputs-only", action="store_true")
    parser.add_argument("--validate-attempt-only", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    plan = load_plan((repo_root / args.config).resolve())
    if args.write_input_diagnostics:
        print(write_input_diagnostics(repo_root=repo_root, plan=plan))
    elif args.validate_inputs_only:
        print(_canonical_json(verify_immutable_inputs(repo_root=repo_root, plan=plan)))
    elif args.validate_attempt_only:
        print(_canonical_json(validate_attempt(repo_root=repo_root, plan=plan)))
    else:
        print(_canonical_json({key: str(value) for key, value in run_physical_tuning_and_sizing(repo_root=repo_root, plan=plan).items()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
