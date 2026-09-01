"""Study executor for one atomic protocol-v2 Phase-B matched set.

A Phase-B Study job is one method/root/layout/condition unit.  It restores the
exact Phase-A scientific checkpoint, advances one common nominal no-learning
prefix, then delegates FN/FD/AN/AD creation and execution atomically to the
validated protocol-v2 executor.

No multi-episode reset semantics are invented here.  The shared prefix and each
post-boundary branch must fit inside one exact GridWorld segment; otherwise the
existing protocol-v2 drivers fail closed until T-526/T-527 freezes a lifecycle
amendment.
"""
from __future__ import annotations

import json
import time
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any

from ..contracts import ChangeEvent, ScenarioSpec
from ..evidence_v2.records import PhaseBAnalysisRecord
from ..gridworld import ACTION_NAMES, gridworld_scenario_to_dict
from ..protocol_v2 import (
    ProtocolV2Branch,
    ProtocolV2Phase,
    ScientificCheckpoint,
)
from ..protocol_v2_executor import execute_phase_b
from ..protocol_v2_prefix import prepare_shared_no_learning_prefix
from ..protocol_v2_sb3_phase_b import SB3PhaseBBranchDriver
from ..protocol_v2_tabular_phase_b import ProjectTabularPhaseBBranchDriver
from ..run_bundle import FINALIZATION_MARKER, RunBundle, sha256_file
from .model import ArtifactRole, StudyJobSpec, StudyStage
from .ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome
from .protocol_v2_executors import (
    PROJECT_IMPLEMENTATION_ID,
    SB3_IMPLEMENTATION_ID,
    _artifact,
    _episode_seeds,
    _mapping,
    _positive_int,
    _project_driver,
    _relative,
    _root_identity,
    _sb3_driver,
    _scenario_from_layout,
)

_ACTION_REMAP_CATALOG: Mapping[str, Mapping[str, str]] = {
    "swap-right-down": {
        "up": "up",
        "right": "down",
        "down": "right",
        "left": "left",
    },
    "cycle-clockwise": {
        "up": "right",
        "right": "down",
        "down": "left",
        "left": "up",
    },
}
_EXPECTED_BRANCHES = tuple(branch.value for branch in ProtocolV2Branch)


def _read_json(path: Path, *, field: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{field} is unreadable: {path}") from exc
    if not isinstance(value, Mapping):
        raise RuntimeError(f"{field} must be a JSON object")
    return dict(value)


def _load_phase_a_checkpoint(
    *,
    context: StudyJobContext,
    phase_a_job_id: str,
    method_id: str,
    root_id: str,
    layout_id: str,
) -> tuple[ScientificCheckpoint, Path]:
    run_id = f"{context.study_id}--{phase_a_job_id}"
    run_dir = context.writable_root / "results" / "runs" / run_id
    if not (run_dir / FINALIZATION_MARKER).is_file():
        raise RuntimeError("Phase-B origin Phase-A run is not finalized")

    manifest = _read_json(run_dir / "manifest.json", field="Phase-A manifest")
    if manifest.get("status") != "completed":
        raise RuntimeError("Phase-B origin Phase-A run is not completed")
    files = manifest.get("files")
    if not isinstance(files, Mapping):
        raise RuntimeError("Phase-A manifest files section is invalid")

    checkpoint_path = run_dir / "scientific-checkpoint.json"
    checkpoint_file = files.get("scientific-checkpoint.json")
    if not isinstance(checkpoint_file, Mapping):
        raise RuntimeError("Phase-A manifest does not retain scientific-checkpoint.json")
    actual_file_sha = sha256_file(checkpoint_path)
    if checkpoint_file.get("sha256") != actual_file_sha:
        raise RuntimeError("Phase-A scientific checkpoint file hash mismatch")

    payload = _read_json(checkpoint_path, field="Phase-A scientific checkpoint")
    expected = {
        "schema_version",
        "method_id",
        "root_id",
        "layout_id",
        "phase",
        "training_interaction_index",
        "state",
        "provenance",
    }
    if set(payload) != expected:
        raise RuntimeError("Phase-A scientific checkpoint keys mismatch")
    try:
        phase = ProtocolV2Phase(str(payload["phase"]))
    except ValueError as exc:
        raise RuntimeError("Phase-A scientific checkpoint has unknown phase") from exc
    checkpoint = ScientificCheckpoint(
        schema_version=payload["schema_version"],
        method_id=payload["method_id"],
        root_id=payload["root_id"],
        layout_id=payload["layout_id"],
        phase=phase,
        training_interaction_index=payload["training_interaction_index"],
        state=payload["state"],
        provenance=payload["provenance"],
    )
    if checkpoint.phase is not ProtocolV2Phase.NOMINAL_TRAINING:
        raise RuntimeError("Phase-B origin checkpoint must be a Phase-A nominal-training state")
    if checkpoint.method_id != method_id:
        raise RuntimeError("Phase-B method does not match Phase-A checkpoint")
    if checkpoint.root_id != root_id or checkpoint.layout_id != layout_id:
        raise RuntimeError("Phase-B root/layout does not match Phase-A checkpoint")

    summary = _read_json(run_dir / "summary.json", field="Phase-A summary")
    if summary.get("checkpoint_sha256") != checkpoint.sha256:
        raise RuntimeError("Phase-A checkpoint scientific digest does not match finalized summary")
    return checkpoint, checkpoint_path


def _require_nominal(spec: ScenarioSpec) -> None:
    if tuple(spec.change_events):
        raise ValueError("Phase-B source layout must be nominal before condition application")
    action = _mapping(spec.action_disturbance_spec, field="nominal action disturbance")
    observation = _mapping(
        spec.observation_disturbance_spec,
        field="nominal observation disturbance",
    )
    if float(action.get("failure_probability", -1.0)) != 0.0:
        raise ValueError("Phase-B source layout must have zero nominal action failure")
    if float(observation.get("mislocalization_probability", -1.0)) != 0.0:
        raise ValueError("Phase-B source layout must have zero nominal observation corruption")


def _action_mapping(specification: Mapping[str, Any]) -> Mapping[str, str]:
    if "mapping" in specification:
        raw = specification["mapping"]
        if not isinstance(raw, Mapping):
            raise ValueError("action-remap specification.mapping must be an object")
        mapping = {str(key): str(value) for key, value in raw.items()}
    else:
        mapping_id = specification.get("mapping_id")
        if not isinstance(mapping_id, str) or mapping_id not in _ACTION_REMAP_CATALOG:
            raise ValueError("action-remap requires an explicit known mapping_id or mapping")
        mapping = dict(_ACTION_REMAP_CATALOG[mapping_id])
    if set(mapping) != set(ACTION_NAMES) or set(mapping.values()) != set(ACTION_NAMES):
        raise ValueError("action-remap mapping must be a permutation of GridWorld actions")
    return mapping


def _probability(specification: Mapping[str, Any], *, field: str) -> float:
    value = specification.get("probability")
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field}.probability must be numeric")
    result = float(value)
    if not 0.0 < result <= 1.0:
        raise ValueError(f"{field}.probability must be in (0, 1]")
    return result


def _disturbed_spec(
    *,
    nominal: ScenarioSpec,
    condition: Mapping[str, Any],
    onset_step: int,
) -> ScenarioSpec:
    condition_id = condition.get("condition_id")
    family = condition.get("family")
    if not isinstance(condition_id, str) or not condition_id.strip():
        raise ValueError("Phase-B condition_id must be explicit")
    if not isinstance(family, str) or not family.strip():
        raise ValueError("Phase-B condition family must be explicit")
    specification = _mapping(
        condition.get("specification"),
        field="job.condition.specification",
    )
    disturbed_id = f"{nominal.scenario_id}--{condition_id}--disturbed"

    if family == "action-remap":
        mapping = _action_mapping(specification)
        identity = {name: name for name in ACTION_NAMES}
        remapped = sum(identity[name] != mapping[name] for name in ACTION_NAMES)
        if remapped <= 0:
            raise ValueError("action-remap condition must change at least one action")
        event = ChangeEvent(
            event_id=f"{condition_id}-onset",
            change_type="action-remap",
            onset_step=onset_step,
            persistent=True,
            affected_mechanism="transition",
            severity={"remapped_actions": remapped},
            pre_change={"action_remap": identity},
            post_change={"action_remap": dict(mapping)},
        )
        disturbed = replace(
            nominal,
            scenario_id=disturbed_id,
            change_events=(event,),
        )
    elif family == "action-failure":
        disturbed = replace(
            nominal,
            scenario_id=disturbed_id,
            action_disturbance_spec={
                "type": "no-op-failure",
                "failure_probability": _probability(
                    specification,
                    field="action-failure",
                ),
            },
        )
    elif family == "observation-corruption":
        support = specification.get("support")
        if support not in {
            None,
            "uniform-valid-non-obstacle-excluding-true-state",
        }:
            raise ValueError("unsupported observation-corruption support")
        disturbed = replace(
            nominal,
            scenario_id=disturbed_id,
            observation_disturbance_spec={
                "type": "position-mislocalization",
                "mislocalization_probability": _probability(
                    specification,
                    field="observation-corruption",
                ),
            },
        )
    else:
        raise ValueError(f"unsupported Phase-B condition family: {family!r}")

    # Validate the complete concrete GridWorld scenario before any execution.
    gridworld_scenario_to_dict(disturbed)
    return disturbed


def _restore_learner(
    *,
    method_id: str,
    implementation_id: str,
    parameters: Mapping[str, Any],
    scenario: ScenarioSpec,
    root: Any,
    checkpoint: ScientificCheckpoint,
):
    if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
        if implementation_id != PROJECT_IMPLEMENTATION_ID:
            raise ValueError("project Phase-B implementation_id mismatch")
        driver = _project_driver(
            method_id=method_id,
            parameters=parameters,
            scenario=scenario,
            root=root,
        )
        adapter = driver.state_adapter
        adapter.restore_state(checkpoint.state)
        return adapter

    if method_id in {"dqn", "ppo"}:
        if implementation_id != SB3_IMPLEMENTATION_ID:
            raise ValueError("SB3 Phase-B implementation_id mismatch")
        # The temporary Phase-A driver supplies the exact algorithm/configuration
        # factory. restore_state replaces its initialized model with the serialized
        # Phase-A learner and leaves the restored model detached from any env.
        driver = _sb3_driver(
            method_id=method_id,
            parameters=parameters,
            scenario=scenario,
            root=root,
            training_budget=max(1, checkpoint.training_interaction_index),
        )
        adapter = driver.state_adapter
        adapter.restore_state(checkpoint.state)
        return adapter

    raise ValueError(f"unsupported Phase-B method: {method_id!r}")


class ProtocolV2PhaseBStudyExecutor:
    """Execute one matched FN/FD/AN/AD Study unit from one exact Phase-A state."""

    job_type = "phase-b-matched-set"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if job.stage is not StudyStage.PHASE_B:
            raise ValueError("phase-b-matched-set executor requires a PHASE_B job")
        if tuple(job.payload.get("branches", ())) != _EXPECTED_BRANCHES:
            raise ValueError("Phase-B matched set must declare exact FN/FD/AN/AD branch order")
        if len(job.dependencies) != 1:
            raise ValueError("Phase-B matched set requires exactly one Phase-A dependency")

        phase_a_job_id = job.payload.get("phase_a_job_id")
        if phase_a_job_id != job.dependencies[0]:
            raise ValueError("Phase-B phase_a_job_id must match its exact dependency")
        if not isinstance(phase_a_job_id, str) or not phase_a_job_id:
            raise ValueError("Phase-B phase_a_job_id must be explicit")

        execution = _mapping(job.payload.get("execution"), field="job.execution")
        prefix_interactions = _positive_int(
            execution.get("prefix_interactions"),
            field="job.execution.prefix_interactions",
        )
        branch_budget = _positive_int(
            execution.get("interaction_budget_per_branch"),
            field="job.execution.interaction_budget_per_branch",
        )
        reset_policy = execution.get("episode_reset_policy_id")
        subsequent_episode_seed_count = execution.get("subsequent_episode_seed_count")
        unknown_execution = set(execution) - {
            "prefix_interactions",
            "interaction_budget_per_branch",
            "episode_reset_policy_id",
            "subsequent_episode_seed_count",
        }
        if unknown_execution:
            raise ValueError(
                f"unsupported Phase-B execution fields: {sorted(unknown_execution)}"
            )
        if reset_policy is None and subsequent_episode_seed_count is not None:
            raise ValueError("subsequent episode seeds require an explicit reset policy")
        if reset_policy is not None:
            if reset_policy != "dec-055-persistent-multi-episode-deployment-v1":
                raise ValueError("unsupported Phase-B episode reset policy")
            subsequent_episode_seed_count = _positive_int(
                subsequent_episode_seed_count,
                field="job.execution.subsequent_episode_seed_count",
            )
            if subsequent_episode_seed_count < branch_budget:
                raise ValueError(
                    "multi-episode seed count must cover the fail-closed worst case"
                )

        method = _mapping(job.payload.get("method"), field="job.method")
        root_payload = _mapping(job.payload.get("root"), field="job.root")
        layout = _mapping(job.payload.get("layout"), field="job.layout")
        condition = _mapping(job.payload.get("condition"), field="job.condition")
        method_id = method.get("method_id")
        implementation_id = method.get("implementation_id")
        if not isinstance(method_id, str) or not method_id:
            raise ValueError("Phase-B method_id must be explicit")
        if not isinstance(implementation_id, str) or not implementation_id:
            raise ValueError("Phase-B implementation_id must be explicit")
        parameters = _mapping(method.get("parameters"), field="job.method.parameters")
        root = _root_identity(root_payload)
        nominal_spec = _scenario_from_layout(layout)
        _require_nominal(nominal_spec)

        checkpoint, checkpoint_path = _load_phase_a_checkpoint(
            context=context,
            phase_a_job_id=phase_a_job_id,
            method_id=method_id,
            root_id=root.root_id,
            layout_id=str(layout["layout_id"]),
        )
        learner = _restore_learner(
            method_id=method_id,
            implementation_id=implementation_id,
            parameters=parameters,
            scenario=nominal_spec,
            root=root,
            checkpoint=checkpoint,
        )
        if learner.state_sha256() != checkpoint.state.get("state_sha256", learner.state_sha256()):
            # SB3 embeds its own exact fingerprint. Project adapters are validated
            # by restore_state and ScientificCheckpoint.sha256 instead.
            if method_id in {"dqn", "ppo"}:
                raise RuntimeError("restored SB3 learner fingerprint differs from Phase-A checkpoint")

        prefix_seed = _episode_seeds(
            root,
            scope=(
                "protocol-v2-study-phase-b-prefix:"
                f"{layout['layout_id']}:{condition['condition_id']}"
            ),
            count=1,
        )[0]
        prefix = prepare_shared_no_learning_prefix(
            learner=learner,
            nominal_spec=nominal_spec,
            environment_seeds=prefix_seed,
            interactions=prefix_interactions,
        )
        disturbed_spec = _disturbed_spec(
            nominal=nominal_spec,
            condition=condition,
            onset_step=prefix.environment.environment.gym_env._step,
        )
        subsequent_episode_seeds = (
            ()
            if reset_policy is None
            else _episode_seeds(
                root,
                scope=(
                    "protocol-v2-study-phase-b-episodes:"
                    f"{layout['layout_id']}:{condition['condition_id']}"
                ),
                count=int(subsequent_episode_seed_count),
            )
        )

        resolved_config = {
            "entrypoint": "resilient_agents.study.protocol_v2_phase_b_executor.matched-set.v1",
            "study_id": context.study_id,
            "recipe_sha256": context.recipe_sha256,
            "job_id": job.job_id,
            "phase_a_job_id": phase_a_job_id,
            "phase_a_checkpoint_relative_path": _relative(
                checkpoint_path,
                context.writable_root,
            ),
            "phase_a_checkpoint_sha256": checkpoint.sha256,
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
            if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
                factory = lambda branch, adaptive, branch_learner, environment: (
                    ProjectTabularPhaseBBranchDriver(
                        branch=branch,
                        adaptive=adaptive,
                        learner=branch_learner,
                        environment=environment,
                        subsequent_episode_seeds=subsequent_episode_seeds,
                    )
                )
            elif method_id in {"dqn", "ppo"}:
                factory = lambda branch, adaptive, branch_learner, environment: (
                    SB3PhaseBBranchDriver(
                        branch=branch,
                        adaptive=adaptive,
                        learner=branch_learner,
                        environment=environment,
                        deterministic_inference=False,
                        subsequent_episode_seeds=subsequent_episode_seeds,
                    )
                )
            else:  # pragma: no cover - guarded by restore path.
                raise AssertionError("unreachable Phase-B method")

            matched = execute_phase_b(
                learner=prefix.learner,
                shared_environment=prefix.environment,
                nominal_spec=nominal_spec,
                disturbed_spec=disturbed_spec,
                interaction_budget_per_branch=branch_budget,
                driver_factory=factory,
            )
        finally:
            prefix.environment.environment.close()
        wall_seconds = time.perf_counter() - wall_start
        cpu_seconds = time.process_time() - cpu_start

        checkpoint_artifact_id = f"checkpoint__{phase_a_job_id}"
        matched_payload = {
            "schema_version": 1,
            "record_type": "phase-b-matched-set",
            "study_id": context.study_id,
            "job_id": job.job_id,
            "method_id": method_id,
            "root_id": root.root_id,
            "layout_id": layout["layout_id"],
            "condition_id": condition["condition_id"],
            "phase_a_checkpoint_artifact_id": checkpoint_artifact_id,
            "phase_a_checkpoint_sha256": checkpoint.sha256,
            "prefix_interactions": prefix_interactions,
            "episode_reset_policy_id": reset_policy,
            "branch_point_learner_sha256": matched.branch_point_learner_sha256,
            "branch_point_environment_sha256": matched.branch_point_environment_sha256,
            "branches": [
                {
                    "branch": item.branch.value,
                    "interactions": item.interactions,
                    "metrics": dict(item.metrics),
                    "final_learner_state_sha256": item.final_learner_state_sha256,
                    "final_environment_state_sha256": item.final_environment_state_sha256,
                }
                for item in matched.results
            ],
        }
        matched_path = bundle.write_json_artifact(
            "matched-set.json",
            matched_payload,
        )

        analysis_paths: list[tuple[ProtocolV2Branch, Path]] = []
        for result in matched.results:
            record = PhaseBAnalysisRecord(
                study_id=context.study_id,
                job_id=job.job_id,
                method_id=method_id,
                root_id=root.root_id,
                layout_id=str(layout["layout_id"]),
                condition_id=str(condition["condition_id"]),
                branch=result.branch,
                checkpoint_artifact_id=checkpoint_artifact_id,
                metrics=result.metrics,
                resource_metrics={
                    "environment_interactions": float(result.interactions),
                },
            )
            filename = f"analysis-data-{result.branch.value.lower()}.json"
            analysis_paths.append(
                (result.branch, bundle.write_json_artifact(filename, record.to_dict()))
            )

        summary = {
            "status": "completed",
            "study_id": context.study_id,
            "job_id": job.job_id,
            "method_id": method_id,
            "root_id": root.root_id,
            "layout_id": layout["layout_id"],
            "condition_id": condition["condition_id"],
            "phase_a_checkpoint_sha256": checkpoint.sha256,
            "prefix_interactions": prefix_interactions,
            "interaction_budget_per_branch": branch_budget,
            "total_post_boundary_interactions": branch_budget * 4,
            "branch_point_learner_sha256": matched.branch_point_learner_sha256,
            "branch_point_environment_sha256": matched.branch_point_environment_sha256,
            "wall_seconds": wall_seconds,
            "process_cpu_seconds": cpu_seconds,
        }
        finalized_dir = bundle.finalize(status="completed", summary=summary)
        manifest_path = finalized_dir / "manifest.json"

        run_artifact_id = f"run__{job.job_id}"
        source_checkpoint = (checkpoint_artifact_id,)
        run_artifact = _artifact(
            artifact_id=run_artifact_id,
            role=ArtifactRole.RUN_BUNDLE,
            path=manifest_path,
            context=context,
            job_id=job.job_id,
            source_artifact_ids=source_checkpoint,
            metadata={
                "run_id": run_id,
                "bundle_dir": _relative(finalized_dir, context.writable_root),
                "record_type": "phase-b-matched-set",
            },
        )
        matched_artifact = _artifact(
            artifact_id=f"analysis-data__{job.job_id}__matched-set",
            role=ArtifactRole.ANALYSIS_DATA,
            path=matched_path,
            context=context,
            job_id=job.job_id,
            source_artifact_ids=(run_artifact_id, checkpoint_artifact_id),
            metadata={"record_type": "phase-b-matched-set"},
        )
        branch_artifacts = tuple(
            _artifact(
                artifact_id=f"analysis-data__{job.job_id}__{branch.value.lower()}",
                role=ArtifactRole.ANALYSIS_DATA,
                path=path,
                context=context,
                job_id=job.job_id,
                source_artifact_ids=(run_artifact_id, checkpoint_artifact_id),
                metadata={
                    "record_type": "phase-b",
                    "branch": branch.value,
                },
            )
            for branch, path in analysis_paths
        )
        return StudyJobOutcome(
            kind=JobOutcomeKind.COMPLETED,
            artifacts=(run_artifact, matched_artifact, *branch_artifacts),
            measurements={
                "prefix_interactions": prefix_interactions,
                "interaction_budget_per_branch": branch_budget,
                "post_boundary_interactions": branch_budget * 4,
                "wall_seconds": wall_seconds,
                "process_cpu_seconds": cpu_seconds,
            },
        )
