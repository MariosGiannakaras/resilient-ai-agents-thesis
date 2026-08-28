"""Concrete protocol-v2 scientific executors for study-materialized jobs.

The study layer owns orchestration and durable lineage; algorithm internals stay
inside the already-validated protocol-v2 drivers/adapters.  This module is the
explicit bridge between those two layers.  It intentionally contains no UI
logic and no hidden final-study parameter defaults.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from ..agents import TabularQLearningAgent, TabularQLearningConfig
from ..contracts import ChangeEvent, InformationPolicy, ScenarioSpec
from ..dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig
from ..environment import EnvironmentSeeds
from ..evidence_v2.records import PhaseAAnalysisRecord, ProbeMeasurement
from ..gridworld import ACTION_NAMES, GridWorldEnvironment
from ..protocol_v2 import (
    ProtocolV2TaskSemantics,
    TabularQScientificStateAdapter,
    dyna_q_plus_state_adapter,
    sarsa_state_adapter,
)
from ..protocol_v2_executor import execute_phase_a
from ..protocol_v2_runtime import (
    NoLearningProbePlan,
    PhaseARequest,
    ProbeResult,
    ProtocolV2MethodConfig,
    ProtocolV2RootIdentity,
)
from ..protocol_v2_sb3 import dqn_state_adapter, ppo_state_adapter
from ..protocol_v2_sb3_driver import SB3PhaseADriver, SB3_IMPLEMENTATION_ID
from ..protocol_v2_sb3_gridworld import ExplicitSeededGridWorldEnv
from ..protocol_v2_sb3_seeding import reseed_sb3_behavior_rng
from ..protocol_v2_tabular_driver import (
    PROJECT_IMPLEMENTATION_ID,
    ProjectTabularNoLearningProbeEvaluator,
    ProjectTabularPhaseADriver,
)
from ..randomness import derive_scoped_seed
from ..run_bundle import FINALIZATION_MARKER, RunBundle, sha256_file
from ..sarsa import SarsaAgent, SarsaConfig
from .model import ArtifactRole, StudyArtifact, StudyJobSpec, StudyStage
from .ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome

_CORE_METHODS = {"q_learning", "sarsa", "dqn", "ppo", "dyna_q_plus"}
_ROOT_SEED_FIELDS = (
    "initialization_seed",
    "exploration_seed",
    "scenario_seed",
    "environment_seed",
    "action_disturbance_seed",
    "observation_disturbance_seed",
)


def _mapping(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return dict(value)


def _positive_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{field} must be an integer > 0")
    return value


def _nonnegative_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be an integer >= 0")
    return value


def _root_identity(value: Mapping[str, Any]) -> ProtocolV2RootIdentity:
    root_id = value.get("root_id")
    if not isinstance(root_id, str) or not root_id.strip():
        raise ValueError("root.root_id must be non-empty")
    missing = [field for field in _ROOT_SEED_FIELDS if field not in value]
    if missing:
        raise ValueError(f"root is missing explicit protocol-v2 seed fields: {missing}")
    kwargs = {field: _nonnegative_int(value[field], field=f"root.{field}") for field in _ROOT_SEED_FIELDS}
    return ProtocolV2RootIdentity(root_id=root_id, **kwargs)


def _information_policy(value: Any) -> InformationPolicy:
    payload = _mapping(value, field="scenario.information_policy")
    expected = {
        "expose_executed_action",
        "expose_disturbance_flags",
        "expose_change_indicator",
        "expose_regime_id",
        "expose_true_state",
    }
    if set(payload) != expected or not all(isinstance(payload[key], bool) for key in expected):
        raise ValueError("scenario.information_policy must explicitly define the five boolean visibility flags")
    return InformationPolicy(**payload)


def _change_events(value: Any) -> tuple[ChangeEvent, ...]:
    if not isinstance(value, list):
        raise ValueError("scenario.change_events must be a list")
    result: list[ChangeEvent] = []
    for index, item in enumerate(value):
        payload = _mapping(item, field=f"scenario.change_events[{index}]")
        result.append(ChangeEvent(**payload))
    return tuple(result)


def _scenario_from_layout(layout: Mapping[str, Any]) -> ScenarioSpec:
    layout_id = layout.get("layout_id")
    if not isinstance(layout_id, str) or not layout_id.strip():
        raise ValueError("layout.layout_id must be non-empty")
    scenario = _mapping(layout.get("scenario"), field="layout.scenario")
    expected = {
        "scenario_id",
        "environment_id",
        "max_steps",
        "reward_spec",
        "initial_state_spec",
        "dynamics_spec",
        "observation_spec",
        "action_disturbance_spec",
        "observation_disturbance_spec",
        "change_events",
        "information_policy",
    }
    if set(scenario) != expected:
        raise ValueError("layout.scenario keys mismatch")
    if scenario["scenario_id"] != layout_id:
        raise ValueError("layout.scenario.scenario_id must match layout_id")
    return ScenarioSpec(
        scenario_id=scenario["scenario_id"],
        environment_id=scenario["environment_id"],
        max_steps=_positive_int(scenario["max_steps"], field="scenario.max_steps"),
        reward_spec=_mapping(scenario["reward_spec"], field="scenario.reward_spec"),
        initial_state_spec=_mapping(
            scenario["initial_state_spec"], field="scenario.initial_state_spec"
        ),
        dynamics_spec=_mapping(scenario["dynamics_spec"], field="scenario.dynamics_spec"),
        observation_spec=_mapping(
            scenario["observation_spec"], field="scenario.observation_spec"
        ),
        action_disturbance_spec=_mapping(
            scenario["action_disturbance_spec"],
            field="scenario.action_disturbance_spec",
        ),
        observation_disturbance_spec=_mapping(
            scenario["observation_disturbance_spec"],
            field="scenario.observation_disturbance_spec",
        ),
        change_events=_change_events(scenario["change_events"]),
        information_policy=_information_policy(scenario["information_policy"]),
    )


def _episode_seeds(
    root: ProtocolV2RootIdentity,
    *,
    scope: str,
    count: int,
) -> tuple[EnvironmentSeeds, ...]:
    return tuple(
        EnvironmentSeeds(
            scenario=derive_scoped_seed(root.scenario_seed, f"{scope}:episode:{index}"),
            environment=derive_scoped_seed(root.environment_seed, f"{scope}:episode:{index}"),
            action_disturbance=derive_scoped_seed(
                root.action_disturbance_seed, f"{scope}:episode:{index}"
            ),
            observation_disturbance=derive_scoped_seed(
                root.observation_disturbance_seed, f"{scope}:episode:{index}"
            ),
        )
        for index in range(count)
    )


class _SB3ProjectProbeEvaluator:
    """Deterministic no-learning neural probe using project GridWorld semantics."""

    def __init__(
        self,
        *,
        scenario: ScenarioSpec,
        seeds: Sequence[EnvironmentSeeds],
    ) -> None:
        self.scenario = scenario
        self.seeds = tuple(seeds)
        if not self.seeds:
            raise ValueError("probe seeds must be explicit")

    def __call__(
        self,
        adapter: Any,
        *,
        training_interaction_index: int,
        episodes: int,
    ) -> ProbeResult:
        if episodes <= 0 or episodes > len(self.seeds):
            raise ValueError("invalid probe episode count")
        returns: list[float] = []
        lengths: list[int] = []
        terminated = 0
        truncated = 0
        interactions = 0
        for seeds in self.seeds[:episodes]:
            env = GridWorldEnvironment(self.scenario)
            try:
                observation = env.reset(seeds=seeds)
                total = 0.0
                length = 0
                while True:
                    action = adapter.predict(observation, deterministic=True)
                    if hasattr(action, "item"):
                        action = action.item()
                    truth = env.step(int(action))
                    total += float(truth.reward)
                    length += 1
                    interactions += 1
                    observation = truth.delivered_observation
                    if truth.terminated or truth.truncated:
                        terminated += int(truth.terminated)
                        truncated += int(truth.truncated)
                        break
                returns.append(total)
                lengths.append(length)
            finally:
                env.close()
        return ProbeResult(
            training_interaction_index=training_interaction_index,
            probe_environment_interactions=interactions,
            episodes=episodes,
            metrics={
                "return_mean": sum(returns) / len(returns),
                "episode_length_mean": sum(lengths) / len(lengths),
                "terminated_rate": terminated / episodes,
                "truncated_rate": truncated / episodes,
            },
        )


def _project_driver(
    *,
    method_id: str,
    parameters: Mapping[str, Any],
    scenario: ScenarioSpec,
    root: ProtocolV2RootIdentity,
) -> ProjectTabularPhaseADriver:
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
            TabularQLearningConfig(
                agent_id="study-q-learning",
                learning_enabled=True,
                **common,
            ),
            checkpoint=None,
        )
        adapter = TabularQScientificStateAdapter(agent)
    elif method_id == "sarsa":
        agent = SarsaAgent(
            SarsaConfig(agent_id="study-sarsa", **common),
            checkpoint=None,
        )
        adapter = sarsa_state_adapter(agent)
    elif method_id == "dyna_q_plus":
        agent = DynaQPlusAgent(
            DynaQPlusConfig(
                agent_id="study-dyna-q-plus",
                planning_steps=int(parameters["planning_steps"]),
                kappa=float(parameters["kappa"]),
                **common,
            ),
            checkpoint=None,
        )
        adapter = dyna_q_plus_state_adapter(agent)
    else:
        raise ValueError(f"unsupported project Phase-A method: {method_id}")
    return ProjectTabularPhaseADriver(adapter=adapter, scenario=scenario, root=root)


def _sb3_driver(
    *,
    method_id: str,
    parameters: Mapping[str, Any],
    scenario: ScenarioSpec,
    root: ProtocolV2RootIdentity,
    training_budget: int,
) -> SB3PhaseADriver:
    try:
        from stable_baselines3 import DQN, PPO
    except ImportError as exc:  # pragma: no cover - dependency-group environment path.
        raise RuntimeError("DQN/PPO Study execution requires the protocol-v2-pilot dependency group") from exc

    schedule = _episode_seeds(
        root,
        scope="protocol-v2-study-phase-a",
        count=training_budget + 1,
    )

    def environment_factory() -> ExplicitSeededGridWorldEnv:
        return ExplicitSeededGridWorldEnv(
            scenario=scenario,
            episode_seeds=schedule,
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
        raise ValueError(f"unsupported SB3 Phase-A method: {method_id}")
    reseed_sb3_behavior_rng(adapter, exploration_seed=root.exploration_seed)
    return SB3PhaseADriver(adapter)


def _relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _artifact(
    *,
    artifact_id: str,
    role: ArtifactRole,
    path: Path,
    context: StudyJobContext,
    job_id: str,
    source_artifact_ids: tuple[str, ...] = (),
    metadata: Mapping[str, Any] | None = None,
) -> StudyArtifact:
    return StudyArtifact(
        artifact_id=artifact_id,
        role=role,
        evidence_class=context.recipe.evidence_class,
        relative_path=_relative(path, context.writable_root),
        sha256=sha256_file(path),
        source_job_ids=(job_id,),
        source_artifact_ids=source_artifact_ids,
        metadata=dict(metadata or {}),
    )


class ProtocolV2PhaseAStudyExecutor:
    """Execute one recipe-materialized protocol-v2 nominal-learning job."""

    job_type = "phase-a-training"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if job.stage is not StudyStage.PHASE_A:
            raise ValueError("phase-a-training executor requires a PHASE_A job")
        execution = _mapping(job.payload.get("execution"), field="job.execution")
        method = _mapping(job.payload.get("method"), field="job.method")
        root_payload = _mapping(job.payload.get("root"), field="job.root")
        layout = _mapping(job.payload.get("layout"), field="job.layout")
        method_id = method.get("method_id")
        if method_id not in _CORE_METHODS:
            raise ValueError(f"unsupported protocol-v2 Study method: {method_id!r}")
        parameters = _mapping(method.get("parameters"), field="job.method.parameters")
        implementation_id = method.get("implementation_id")
        if not isinstance(implementation_id, str) or not implementation_id.strip():
            raise ValueError("job.method.implementation_id must be explicit")

        root = _root_identity(root_payload)
        scenario = _scenario_from_layout(layout)
        task_payload = _mapping(execution.get("task"), field="job.execution.task")
        task = ProtocolV2TaskSemantics(
            gamma=float(task_payload["gamma"]),
            reward_contract=_mapping(
                task_payload["reward_contract"], field="job.execution.task.reward_contract"
            ),
            administrative_truncation=bool(task_payload["administrative_truncation"]),
            bootstrap_on_truncation=bool(task_payload["bootstrap_on_truncation"]),
        )
        budget = _positive_int(
            execution.get("training_interaction_budget"),
            field="job.execution.training_interaction_budget",
        )
        probe_indices_payload = execution.get("probe_interaction_indices")
        if not isinstance(probe_indices_payload, list):
            raise ValueError("job.execution.probe_interaction_indices must be a list")
        probe_indices = tuple(
            _nonnegative_int(item, field="probe interaction index")
            for item in probe_indices_payload
        )
        probe_episodes = _positive_int(
            execution.get("episodes_per_probe"),
            field="job.execution.episodes_per_probe",
        )
        probe_plan = NoLearningProbePlan(
            interaction_indices=probe_indices,
            episodes_per_probe=probe_episodes,
        )
        probe_plan.validate_against_training_budget(budget)

        request = PhaseARequest(
            protocol_version=context.recipe.protocol_version,
            experiment_id=job.job_id,
            layout_id=str(layout["layout_id"]),
            root=root,
            task=task,
            method=ProtocolV2MethodConfig(
                method_id=str(method_id),
                implementation_id=implementation_id,
                parameters=parameters,
            ),
            training_interaction_budget=budget,
            probe_plan=probe_plan,
        )

        if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
            if implementation_id != PROJECT_IMPLEMENTATION_ID:
                raise ValueError("project Study method implementation_id mismatch")
            driver = _project_driver(
                method_id=str(method_id),
                parameters=parameters,
                scenario=scenario,
                root=root,
            )
            evaluator = ProjectTabularNoLearningProbeEvaluator(
                scenario=scenario,
                environment_seeds=_episode_seeds(
                    root,
                    scope=f"protocol-v2-study-probe:{context.study_id}:{layout['layout_id']}",
                    count=probe_episodes,
                ),
            )
        else:
            if implementation_id != SB3_IMPLEMENTATION_ID:
                raise ValueError("SB3 Study method implementation_id mismatch")
            driver = _sb3_driver(
                method_id=str(method_id),
                parameters=parameters,
                scenario=scenario,
                root=root,
                training_budget=budget,
            )
            evaluator = _SB3ProjectProbeEvaluator(
                scenario=scenario,
                seeds=_episode_seeds(
                    root,
                    scope=f"protocol-v2-study-probe:{context.study_id}:{layout['layout_id']}",
                    count=probe_episodes,
                ),
            )

        resolved_config = {
            "entrypoint": "resilient_agents.study.protocol_v2_executors.phase-a.v1",
            "study_id": context.study_id,
            "recipe_sha256": context.recipe_sha256,
            "job_id": job.job_id,
            "job_payload": dict(job.payload),
        }
        run_id = f"{context.study_id}--{job.job_id}"
        run_dir = context.writable_root / "results" / "runs" / run_id
        if run_dir.is_dir() and not (run_dir / FINALIZATION_MARKER).exists():
            bundle = RunBundle.resume(
                repo_root=context.repo_root,
                writable_root=context.writable_root,
                run_id=run_id,
                resolved_config=resolved_config,
                protocol_version=context.recipe.protocol_version,
                stage=context.recipe.evidence_class.value,
                retention_policy="study-v2-scientific",
            )
        else:
            bundle = RunBundle(
                repo_root=context.repo_root,
                writable_root=context.writable_root,
                run_id=run_id,
                resolved_config=resolved_config,
                protocol_version=context.recipe.protocol_version,
                stage=context.recipe.evidence_class.value,
                retention_policy="study-v2-scientific",
            )

        wall_start = time.perf_counter()
        cpu_start = time.process_time()
        try:
            execution_result = execute_phase_a(
                request,
                driver=driver,
                probe_evaluator=evaluator,
                checkpoint_provenance={
                    "study_id": context.study_id,
                    "recipe_sha256": context.recipe_sha256,
                    "job_id": job.job_id,
                    "configuration_id": method.get("configuration_id"),
                },
            )
        finally:
            close = getattr(driver, "close", None)
            if callable(close):
                close()
        wall_seconds = time.perf_counter() - wall_start
        cpu_seconds = time.process_time() - cpu_start

        checkpoint_path = bundle.write_json_artifact(
            "scientific-checkpoint.json",
            execution_result.result.final_checkpoint.to_mapping(),
        )
        analysis_record = PhaseAAnalysisRecord(
            study_id=context.study_id,
            job_id=job.job_id,
            method_id=str(method_id),
            root_id=root.root_id,
            layout_id=str(layout["layout_id"]),
            probes=tuple(
                ProbeMeasurement(
                    interaction_index=probe.training_interaction_index,
                    metrics=probe.metrics,
                )
                for probe in execution_result.result.probes
            ),
            resource_metrics={
                "training_environment_interactions": float(
                    execution_result.result.ledger.training_interactions
                ),
                "probe_environment_interactions": float(
                    execution_result.result.ledger.probe_interactions
                ),
                "wall_seconds": float(wall_seconds),
                "process_cpu_seconds": float(cpu_seconds),
            },
        )
        analysis_path = bundle.write_json_artifact(
            "analysis-data.json", analysis_record.to_dict()
        )
        summary = {
            "status": "completed",
            "study_id": context.study_id,
            "job_id": job.job_id,
            "method_id": method_id,
            "root_id": root.root_id,
            "layout_id": layout["layout_id"],
            "training_environment_interactions": execution_result.result.ledger.training_interactions,
            "probe_environment_interactions": execution_result.result.ledger.probe_interactions,
            "probe_count": len(execution_result.result.probes),
            "checkpoint_sha256": execution_result.result.final_checkpoint.sha256,
            "wall_seconds": wall_seconds,
            "process_cpu_seconds": cpu_seconds,
        }
        finalized_dir = bundle.finalize(status="completed", summary=summary)
        manifest_path = finalized_dir / "manifest.json"

        run_artifact_id = f"run__{job.job_id}"
        checkpoint_artifact_id = f"checkpoint__{job.job_id}"
        run_artifact = _artifact(
            artifact_id=run_artifact_id,
            role=ArtifactRole.RUN_BUNDLE,
            path=manifest_path,
            context=context,
            job_id=job.job_id,
            metadata={"run_id": run_id, "bundle_dir": _relative(finalized_dir, context.writable_root)},
        )
        checkpoint_artifact = _artifact(
            artifact_id=checkpoint_artifact_id,
            role=ArtifactRole.SCIENTIFIC_CHECKPOINT,
            path=checkpoint_path,
            context=context,
            job_id=job.job_id,
            source_artifact_ids=(run_artifact_id,),
            metadata={
                "scientific_checkpoint_sha256": execution_result.result.final_checkpoint.sha256,
                "training_interaction_index": budget,
            },
        )
        analysis_artifact = _artifact(
            artifact_id=f"analysis-data__{job.job_id}",
            role=ArtifactRole.ANALYSIS_DATA,
            path=analysis_path,
            context=context,
            job_id=job.job_id,
            source_artifact_ids=(run_artifact_id, checkpoint_artifact_id),
            metadata={"record_type": "phase-a"},
        )
        return StudyJobOutcome(
            kind=JobOutcomeKind.COMPLETED,
            artifacts=(run_artifact, checkpoint_artifact, analysis_artifact),
            measurements={
                "training_interactions": budget,
                "probe_interactions": execution_result.result.ledger.probe_interactions,
                "wall_seconds": wall_seconds,
                "process_cpu_seconds": cpu_seconds,
            },
        )
