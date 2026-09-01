"""Study executor for protocol-v2.1 temporal Phase-B matched sets.

The implementation reuses the validated legacy checkpoint/prefix/scenario
helpers but dispatches branch execution only through protocol-v2.1 drivers.  It
therefore adds deterministic temporal evidence without changing historical
protocol-v2 source files or reinterpreting legacy analysis records.
"""
from __future__ import annotations

import time
from pathlib import Path

from ..evidence_v2.records import PHASE_B_TEMPORAL_SCHEMA_VERSION, PhaseBAnalysisRecord
from ..protocol_v2 import ProtocolV2Branch
from ..protocol_v2_1_execution import execute_phase_b_v21
from ..protocol_v2_1_sb3_phase_b import SB3PhaseBBranchDriverV21
from ..protocol_v2_1_tabular_phase_b import ProjectTabularPhaseBBranchDriverV21
from ..protocol_v2_prefix import prepare_shared_no_learning_prefix
from ..run_bundle import FINALIZATION_MARKER, RunBundle
from .model import ArtifactRole, StudyJobSpec, StudyStage
from .ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome
from .protocol_v2_executors import (
    _artifact,
    _episode_seeds,
    _mapping,
    _positive_int,
    _relative,
    _root_identity,
    _scenario_from_layout,
)
from .protocol_v2_phase_b_executor import (
    _EXPECTED_BRANCHES,
    _disturbed_spec,
    _load_phase_a_checkpoint,
    _require_nominal,
    _restore_learner,
)

_PROTOCOL_VERSION = "protocol-v2.1"
_TEMPORAL_EVIDENCE_ID = "dec-060-fixed-reward-windows-v1"
_RESET_POLICY_ID = "dec-055-persistent-multi-episode-deployment-v1"


class ProtocolV21PhaseBStudyExecutor:
    """Execute one v2.1 matched FN/FD/AN/AD unit with fixed reward windows."""

    job_type = "phase-b-matched-set"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if context.recipe.protocol_version != _PROTOCOL_VERSION:
            raise ValueError("protocol-v2.1 executor requires protocol_version=protocol-v2.1")
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
        expected_execution = {
            "prefix_interactions",
            "interaction_budget_per_branch",
            "episode_reset_policy_id",
            "subsequent_episode_seed_count",
            "temporal_evidence_id",
            "temporal_window_size",
        }
        if set(execution) != expected_execution:
            raise ValueError(
                "protocol-v2.1 Phase-B execution keys mismatch; "
                f"missing={sorted(expected_execution - set(execution))}, "
                f"unknown={sorted(set(execution) - expected_execution)}"
            )
        if execution["temporal_evidence_id"] != _TEMPORAL_EVIDENCE_ID:
            raise ValueError("unsupported protocol-v2.1 temporal evidence contract")
        if execution["temporal_window_size"] != 32:
            raise ValueError("protocol-v2.1 temporal window size is frozen at 32")

        prefix_interactions = _positive_int(
            execution["prefix_interactions"], field="job.execution.prefix_interactions"
        )
        branch_budget = _positive_int(
            execution["interaction_budget_per_branch"],
            field="job.execution.interaction_budget_per_branch",
        )
        if branch_budget != 256:
            raise ValueError("protocol-v2.1 Phase-B horizon is frozen at 256")
        if execution["episode_reset_policy_id"] != _RESET_POLICY_ID:
            raise ValueError("unsupported protocol-v2.1 Phase-B episode reset policy")
        subsequent_episode_seed_count = _positive_int(
            execution["subsequent_episode_seed_count"],
            field="job.execution.subsequent_episode_seed_count",
        )
        if subsequent_episode_seed_count < branch_budget:
            raise ValueError("multi-episode seed count must cover the fail-closed worst case")

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
        if learner.state_sha256() != checkpoint.state.get(
            "state_sha256", learner.state_sha256()
        ):
            if method_id in {"dqn", "ppo"}:
                raise RuntimeError(
                    "restored SB3 learner fingerprint differs from Phase-A checkpoint"
                )

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
        subsequent_episode_seeds = _episode_seeds(
            root,
            scope=(
                "protocol-v2-study-phase-b-episodes:"
                f"{layout['layout_id']}:{condition['condition_id']}"
            ),
            count=subsequent_episode_seed_count,
        )

        resolved_config = {
            "entrypoint": "resilient_agents.study.protocol_v2_1_phase_b_executor.matched-set.v1",
            "study_id": context.study_id,
            "recipe_sha256": context.recipe_sha256,
            "job_id": job.job_id,
            "phase_a_job_id": phase_a_job_id,
            "phase_a_checkpoint_relative_path": _relative(
                checkpoint_path, context.writable_root
            ),
            "phase_a_checkpoint_sha256": checkpoint.sha256,
            "temporal_evidence_id": _TEMPORAL_EVIDENCE_ID,
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
                    ProjectTabularPhaseBBranchDriverV21(
                        branch=branch,
                        adaptive=adaptive,
                        learner=branch_learner,
                        environment=environment,
                        subsequent_episode_seeds=subsequent_episode_seeds,
                    )
                )
            elif method_id in {"dqn", "ppo"}:
                factory = lambda branch, adaptive, branch_learner, environment: (
                    SB3PhaseBBranchDriverV21(
                        branch=branch,
                        adaptive=adaptive,
                        learner=branch_learner,
                        environment=environment,
                        deterministic_inference=False,
                        subsequent_episode_seeds=subsequent_episode_seeds,
                    )
                )
            else:  # pragma: no cover
                raise AssertionError("unreachable Phase-B method")

            matched = execute_phase_b_v21(
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
            "schema_version": PHASE_B_TEMPORAL_SCHEMA_VERSION,
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
            "episode_reset_policy_id": _RESET_POLICY_ID,
            "temporal_evidence_id": _TEMPORAL_EVIDENCE_ID,
            "temporal_window_size": 32,
            "branch_point_learner_sha256": matched.branch_point_learner_sha256,
            "branch_point_environment_sha256": matched.branch_point_environment_sha256,
            "branches": [
                {
                    "branch": item.branch.value,
                    "interactions": item.interactions,
                    "metrics": dict(item.metrics),
                    "reward_windows": [window.to_dict() for window in item.reward_windows],
                    "final_learner_state_sha256": item.final_learner_state_sha256,
                    "final_environment_state_sha256": item.final_environment_state_sha256,
                }
                for item in matched.results
            ],
        }
        matched_path = bundle.write_json_artifact("matched-set.json", matched_payload)

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
                reward_windows=result.reward_windows,
                schema_version=PHASE_B_TEMPORAL_SCHEMA_VERSION,
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
            "temporal_evidence_id": _TEMPORAL_EVIDENCE_ID,
            "temporal_reward_window_size": 32,
            "temporal_reward_window_count_per_branch": branch_budget // 32,
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
                "protocol_extension": "v2.1-temporal",
            },
        )
        matched_artifact = _artifact(
            artifact_id=f"analysis-data__{job.job_id}__matched-set",
            role=ArtifactRole.ANALYSIS_DATA,
            path=matched_path,
            context=context,
            job_id=job.job_id,
            source_artifact_ids=(run_artifact_id, checkpoint_artifact_id),
            metadata={
                "record_type": "phase-b-matched-set",
                "schema_version": PHASE_B_TEMPORAL_SCHEMA_VERSION,
            },
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
                    "schema_version": PHASE_B_TEMPORAL_SCHEMA_VERSION,
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
                "temporal_reward_windows_per_branch": branch_budget // 32,
                "wall_seconds": wall_seconds,
                "process_cpu_seconds": cpu_seconds,
            },
        )
