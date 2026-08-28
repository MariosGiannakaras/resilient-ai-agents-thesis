"""Explicit non-ranked Phase-A reference executors for Study recipes.

References are supporting calibration evidence, not trainable methods.  This
module intentionally implements only reference identities whose semantics are
fully explicit. Unknown reference IDs fail closed instead of acquiring hidden
oracle behavior.
"""
from __future__ import annotations

import random
import statistics
from typing import Any

from ..gridworld import GridWorldEnvironment
from ..randomness import derive_scoped_seed
from ..run_bundle import FINALIZATION_MARKER, RunBundle
from .model import ArtifactRole, StudyJobSpec, StudyStage
from .ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome
from .protocol_v2_executors import (
    _artifact,
    _episode_seeds,
    _mapping,
    _nonnegative_int,
    _positive_int,
    _relative,
    _root_identity,
    _scenario_from_layout,
)


class ProtocolV2PhaseAReferenceExecutor:
    """Execute an explicitly declared supporting Phase-A reference policy."""

    job_type = "phase-a-reference"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if job.stage is not StudyStage.PHASE_A:
            raise ValueError("phase-a-reference executor requires a PHASE_A job")
        execution = _mapping(job.payload.get("execution"), field="job.execution")
        reference = _mapping(job.payload.get("reference"), field="job.reference")
        root = _root_identity(_mapping(job.payload.get("root"), field="job.root"))
        layout = _mapping(job.payload.get("layout"), field="job.layout")
        scenario = _scenario_from_layout(layout)

        reference_id = reference.get("reference_id")
        if reference_id != "random":
            raise ValueError(
                f"unsupported Phase-A reference_id {reference_id!r}; only 'random' is explicit"
            )
        probe_indices_payload = execution.get("probe_interaction_indices")
        if not isinstance(probe_indices_payload, list) or not probe_indices_payload:
            raise ValueError("reference probe_interaction_indices must be a non-empty list")
        probe_indices = tuple(
            _nonnegative_int(item, field="reference probe interaction index")
            for item in probe_indices_payload
        )
        if tuple(sorted(set(probe_indices))) != probe_indices:
            raise ValueError("reference probe_interaction_indices must be unique/increasing")
        episodes = _positive_int(
            execution.get("episodes_per_probe"),
            field="job.execution.episodes_per_probe",
        )
        environment_seeds = _episode_seeds(
            root,
            scope=f"protocol-v2-study-probe:{context.study_id}:{layout['layout_id']}",
            count=episodes,
        )

        probes: list[dict[str, Any]] = []
        total_environment_interactions = 0
        for probe_index in probe_indices:
            returns: list[float] = []
            lengths: list[int] = []
            terminated_count = 0
            truncated_count = 0
            for episode_index, seeds in enumerate(environment_seeds):
                action_rng = random.Random(
                    derive_scoped_seed(
                        root.exploration_seed,
                        (
                            f"protocol-v2-reference:{reference_id}:"
                            f"{layout['layout_id']}:probe:{probe_index}:episode:{episode_index}"
                        ),
                    )
                )
                env = GridWorldEnvironment(scenario)
                try:
                    _ = env.reset(seeds=seeds)
                    episode_return = 0.0
                    episode_length = 0
                    while True:
                        truth = env.step(action_rng.randrange(env.gym_env.action_space.n))
                        episode_return += float(truth.reward)
                        episode_length += 1
                        total_environment_interactions += 1
                        if truth.terminated or truth.truncated:
                            terminated_count += int(truth.terminated)
                            truncated_count += int(truth.truncated)
                            break
                    returns.append(episode_return)
                    lengths.append(episode_length)
                finally:
                    env.close()
            probes.append(
                {
                    "interaction_index": probe_index,
                    "metrics": {
                        "return_mean": float(statistics.fmean(returns)),
                        "episode_length_mean": float(statistics.fmean(lengths)),
                        "terminated_rate": terminated_count / episodes,
                        "truncated_rate": truncated_count / episodes,
                    },
                }
            )

        resolved_config = {
            "entrypoint": "resilient_agents.study.reference_executors.random-reference.v1",
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
                retention_policy="study-v2-reference",
            )
        else:
            bundle = RunBundle(
                repo_root=context.repo_root,
                writable_root=context.writable_root,
                run_id=run_id,
                resolved_config=resolved_config,
                protocol_version=context.recipe.protocol_version,
                stage=context.recipe.evidence_class.value,
                retention_policy="study-v2-reference",
            )

        record = {
            "schema_version": 1,
            "record_type": "phase-a-reference",
            "study_id": context.study_id,
            "job_id": job.job_id,
            "reference_id": reference_id,
            "root_id": root.root_id,
            "layout_id": layout["layout_id"],
            "role": reference.get("role"),
            "probes": probes,
            "resource_metrics": {
                "probe_environment_interactions": total_environment_interactions,
            },
        }
        analysis_path = bundle.write_json_artifact("analysis-data.json", record)
        finalized_dir = bundle.finalize(
            status="completed",
            summary={
                "status": "completed",
                "study_id": context.study_id,
                "job_id": job.job_id,
                "reference_id": reference_id,
                "root_id": root.root_id,
                "layout_id": layout["layout_id"],
                "probe_count": len(probes),
                "probe_environment_interactions": total_environment_interactions,
            },
        )
        run_artifact_id = f"run__{job.job_id}"
        run_artifact = _artifact(
            artifact_id=run_artifact_id,
            role=ArtifactRole.RUN_BUNDLE,
            path=finalized_dir / "manifest.json",
            context=context,
            job_id=job.job_id,
            metadata={
                "run_id": run_id,
                "bundle_dir": _relative(finalized_dir, context.writable_root),
                "record_type": "phase-a-reference",
            },
        )
        analysis_artifact = _artifact(
            artifact_id=f"analysis-data__{job.job_id}",
            role=ArtifactRole.ANALYSIS_DATA,
            path=analysis_path,
            context=context,
            job_id=job.job_id,
            source_artifact_ids=(run_artifact_id,),
            metadata={
                "record_type": "phase-a-reference",
                "reference_id": reference_id,
            },
        )
        return StudyJobOutcome(
            kind=JobOutcomeKind.COMPLETED,
            artifacts=(run_artifact, analysis_artifact),
            measurements={
                "probe_count": len(probes),
                "probe_environment_interactions": total_environment_interactions,
            },
        )
