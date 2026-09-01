"""Structural/integrity validation for protocol-v2 study evidence."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

from ..protocol_v2 import ProtocolV2Branch
from ..study import ArtifactRole, JobState, StudyArtifact, StudyStore
from .records import PHASE_B_TEMPORAL_SCHEMA_VERSION, PhaseBAnalysisRecord


@dataclass(frozen=True)
class EvidenceValidationFinding:
    code: str
    severity: str
    message: str
    job_id: str | None = None
    artifact_id: str | None = None

    def __post_init__(self) -> None:
        if self.severity not in {"error", "warning", "info"}:
            raise ValueError("unsupported validation finding severity")
        if not self.code or not self.message:
            raise ValueError("validation finding code/message must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "job_id": self.job_id,
            "artifact_id": self.artifact_id,
        }


@dataclass(frozen=True)
class StudyEvidenceValidationReport:
    study_id: str
    recipe_sha256: str
    planned_scientific_jobs: int
    completed_scientific_jobs: int
    scientific_failures: int
    skipped_scientific_jobs: int
    checkpoint_count: int
    run_bundle_count: int
    failure_record_count: int
    findings: tuple[EvidenceValidationFinding, ...]

    @property
    def valid(self) -> bool:
        return not any(item.severity == "error" for item in self.findings)

    @property
    def ready_for_analysis(self) -> bool:
        return self.valid

    def to_dict(self) -> dict[str, Any]:
        return {
            "study_id": self.study_id,
            "recipe_sha256": self.recipe_sha256,
            "valid": self.valid,
            "ready_for_analysis": self.ready_for_analysis,
            "planned_scientific_jobs": self.planned_scientific_jobs,
            "completed_scientific_jobs": self.completed_scientific_jobs,
            "scientific_failures": self.scientific_failures,
            "skipped_scientific_jobs": self.skipped_scientific_jobs,
            "checkpoint_count": self.checkpoint_count,
            "run_bundle_count": self.run_bundle_count,
            "failure_record_count": self.failure_record_count,
            "findings": [item.to_dict() for item in self.findings],
        }


class StudyEvidenceValidator:
    """Validate planned-vs-produced scientific evidence before analysis.

    Scientific failures are valid outcomes when explicitly recorded. Missing or
    ambiguous evidence, broken Phase-A -> matched-Phase-B checkpoint lineage and
    unclassified/infrastructure-incomplete units are validation errors.

    Protocol-v2.1 additionally requires complete fixed-window Phase-B evidence
    for every completed matched set. The validator checks stored records only;
    it never derives recovery outcomes or reads final-reserve results.
    """

    _SCIENTIFIC_JOB_TYPES = {
        "phase-a-training",
        "phase-a-reference",
        "phase-b-matched-set",
    }

    def validate(self, store: StudyStore) -> StudyEvidenceValidationReport:
        if not isinstance(store, StudyStore):
            raise ValueError("store must be StudyStore")
        jobs = store.plan.by_id()
        artifacts = store.artifacts()
        artifacts_by_id = {item.artifact_id: item for item in artifacts}
        by_job: dict[str, list[StudyArtifact]] = {job_id: [] for job_id in jobs}
        for artifact in artifacts:
            for job_id in artifact.source_job_ids:
                if job_id in by_job:
                    by_job[job_id].append(artifact)

        findings: list[EvidenceValidationFinding] = []
        scientific_jobs = [
            job
            for job in store.plan.jobs
            if job.payload.get("job_type") in self._SCIENTIFIC_JOB_TYPES
        ]
        completed = 0
        scientific_failures = 0
        skipped = 0

        for job in scientific_jobs:
            state = store.lifecycle.state_for(job.job_id)
            produced = by_job[job.job_id]
            job_type = str(job.payload.get("job_type"))
            roles = [item.role for item in produced]

            if state is JobState.COMPLETED:
                completed += 1
                self._validate_completed_job(
                    store=store,
                    job=job,
                    job_type=job_type,
                    produced=produced,
                    roles=roles,
                    artifacts_by_id=artifacts_by_id,
                    findings=findings,
                )
            elif state is JobState.SCIENTIFIC_FAILED:
                scientific_failures += 1
                if ArtifactRole.FAILURE_RECORD not in roles:
                    findings.append(
                        EvidenceValidationFinding(
                            code="SCIENTIFIC_FAILURE_RECORD_MISSING",
                            severity="error",
                            message="Scientific failure has no retained failure-record artifact.",
                            job_id=job.job_id,
                        )
                    )
            elif state is JobState.SKIPPED:
                skipped += 1
                if job_type != "phase-b-matched-set":
                    findings.append(
                        EvidenceValidationFinding(
                            code="UNEXPECTED_SCIENTIFIC_SKIP",
                            severity="error",
                            message="Only a dependent Phase-B matched set may be scientifically skipped.",
                            job_id=job.job_id,
                        )
                    )
                else:
                    dependency_states = [
                        store.lifecycle.state_for(item) for item in job.dependencies
                    ]
                    if not any(
                        item in {JobState.SCIENTIFIC_FAILED, JobState.SKIPPED}
                        for item in dependency_states
                    ):
                        findings.append(
                            EvidenceValidationFinding(
                                code="SKIP_WITHOUT_FAILED_DEPENDENCY",
                                severity="error",
                                message="Skipped Phase-B matched set is not explained by an upstream scientific failure.",
                                job_id=job.job_id,
                            )
                        )
            else:
                findings.append(
                    EvidenceValidationFinding(
                        code="SCIENTIFIC_JOB_UNRESOLVED",
                        severity="error",
                        message=f"Scientific job remains {state.value}; evidence is not frozen for analysis.",
                        job_id=job.job_id,
                    )
                )

        checkpoints = [
            item for item in artifacts if item.role is ArtifactRole.SCIENTIFIC_CHECKPOINT
        ]
        run_bundles = [item for item in artifacts if item.role is ArtifactRole.RUN_BUNDLE]
        failure_records = [
            item for item in artifacts if item.role is ArtifactRole.FAILURE_RECORD
        ]
        return StudyEvidenceValidationReport(
            study_id=store.plan.study_id,
            recipe_sha256=store.recipe.sha256(),
            planned_scientific_jobs=len(scientific_jobs),
            completed_scientific_jobs=completed,
            scientific_failures=scientific_failures,
            skipped_scientific_jobs=skipped,
            checkpoint_count=len(checkpoints),
            run_bundle_count=len(run_bundles),
            failure_record_count=len(failure_records),
            findings=tuple(findings),
        )

    def _validate_completed_job(
        self,
        *,
        store: StudyStore,
        job: Any,
        job_type: str,
        produced: list[StudyArtifact],
        roles: list[ArtifactRole],
        artifacts_by_id: Mapping[str, StudyArtifact],
        findings: list[EvidenceValidationFinding],
    ) -> None:
        if job_type == "phase-a-training":
            required_roles = {
                ArtifactRole.RUN_BUNDLE,
                ArtifactRole.SCIENTIFIC_CHECKPOINT,
                ArtifactRole.ANALYSIS_DATA,
            }
        elif job_type in {"phase-a-reference", "phase-b-matched-set"}:
            required_roles = {ArtifactRole.RUN_BUNDLE, ArtifactRole.ANALYSIS_DATA}
        else:  # pragma: no cover - filtered by caller.
            return
        for role in required_roles:
            if role not in roles:
                findings.append(
                    EvidenceValidationFinding(
                        code="REQUIRED_ARTIFACT_MISSING",
                        severity="error",
                        message=f"Completed {job_type} job lacks required {role.value} artifact.",
                        job_id=job.job_id,
                    )
                )

        if job_type == "phase-a-training":
            checkpoints = [
                item for item in produced if item.role is ArtifactRole.SCIENTIFIC_CHECKPOINT
            ]
            if len(checkpoints) != 1:
                findings.append(
                    EvidenceValidationFinding(
                        code="PHASE_A_CHECKPOINT_AMBIGUOUS",
                        severity="error",
                        message=(
                            "Completed Phase-A training must expose exactly one final scientific checkpoint; "
                            f"found {len(checkpoints)}."
                        ),
                        job_id=job.job_id,
                    )
                )
            return

        if job_type != "phase-b-matched-set":
            return
        if len(job.dependencies) != 1:
            findings.append(
                EvidenceValidationFinding(
                    code="PHASE_B_ORIGIN_DEPENDENCY_INVALID",
                    severity="error",
                    message="Phase-B matched set must depend on exactly one matching Phase-A producer.",
                    job_id=job.job_id,
                )
            )
            return
        phase_a_job_id = job.dependencies[0]
        expected_checkpoints = [
            artifact
            for artifact in artifacts_by_id.values()
            if artifact.role is ArtifactRole.SCIENTIFIC_CHECKPOINT
            and phase_a_job_id in artifact.source_job_ids
        ]
        if len(expected_checkpoints) != 1:
            findings.append(
                EvidenceValidationFinding(
                    code="PHASE_B_ORIGIN_CHECKPOINT_MISSING",
                    severity="error",
                    message=(
                        "Phase-B matched set cannot resolve one exact scientific checkpoint from its Phase-A dependency."
                    ),
                    job_id=job.job_id,
                )
            )
            return
        checkpoint_id = expected_checkpoints[0].artifact_id
        lineage_artifacts = [
            item
            for item in produced
            if item.role in {ArtifactRole.RUN_BUNDLE, ArtifactRole.ANALYSIS_DATA}
        ]
        for artifact in lineage_artifacts:
            if checkpoint_id not in artifact.source_artifact_ids:
                findings.append(
                    EvidenceValidationFinding(
                        code="PHASE_B_CHECKPOINT_LINEAGE_MISSING",
                        severity="error",
                        message=(
                            "Phase-B evidence artifact does not trace to the exact Phase-A checkpoint."
                        ),
                        job_id=job.job_id,
                        artifact_id=artifact.artifact_id,
                    )
                )

        if str(store.recipe.protocol_version).startswith("protocol-v2.1"):
            self._validate_temporal_phase_b(
                store=store,
                job=job,
                produced=produced,
                findings=findings,
            )

    def _validate_temporal_phase_b(
        self,
        *,
        store: StudyStore,
        job: Any,
        produced: list[StudyArtifact],
        findings: list[EvidenceValidationFinding],
    ) -> None:
        execution = job.payload.get("execution")
        if not isinstance(execution, Mapping):
            findings.append(
                EvidenceValidationFinding(
                    code="PHASE_B_TEMPORAL_EXECUTION_SPEC_MISSING",
                    severity="error",
                    message="Protocol-v2.1 Phase-B job lacks an execution specification.",
                    job_id=job.job_id,
                )
            )
            return
        budget = execution.get("interaction_budget_per_branch")
        if not isinstance(budget, int) or isinstance(budget, bool) or budget <= 0:
            findings.append(
                EvidenceValidationFinding(
                    code="PHASE_B_TEMPORAL_BUDGET_INVALID",
                    severity="error",
                    message="Protocol-v2.1 Phase-B interaction budget is invalid.",
                    job_id=job.job_id,
                )
            )
            return
        if budget % 32:
            findings.append(
                EvidenceValidationFinding(
                    code="PHASE_B_TEMPORAL_BUDGET_NOT_WINDOW_ALIGNED",
                    severity="error",
                    message="Protocol-v2.1 Phase-B budget must be divisible by the frozen 32-interaction window.",
                    job_id=job.job_id,
                )
            )
            return

        branch_artifacts = [
            artifact
            for artifact in produced
            if artifact.role is ArtifactRole.ANALYSIS_DATA
            and artifact.metadata.get("record_type") == "phase-b"
        ]
        if len(branch_artifacts) != 4:
            findings.append(
                EvidenceValidationFinding(
                    code="PHASE_B_TEMPORAL_BRANCH_RECORD_COUNT_INVALID",
                    severity="error",
                    message=(
                        "Protocol-v2.1 matched set must retain exactly four branch analysis records."
                    ),
                    job_id=job.job_id,
                )
            )
            return
        expected_branches = set(ProtocolV2Branch)
        observed_branches: set[ProtocolV2Branch] = set()
        expected_endpoints = tuple(range(32, budget + 1, 32))
        for artifact in branch_artifacts:
            path = store.writable_root / artifact.relative_path
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                record = PhaseBAnalysisRecord.from_dict(raw)
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
                findings.append(
                    EvidenceValidationFinding(
                        code="PHASE_B_TEMPORAL_RECORD_INVALID",
                        severity="error",
                        message=f"Protocol-v2.1 Phase-B record is unreadable or invalid: {exc}",
                        job_id=job.job_id,
                        artifact_id=artifact.artifact_id,
                    )
                )
                continue
            observed_branches.add(record.branch)
            if record.schema_version != PHASE_B_TEMPORAL_SCHEMA_VERSION:
                findings.append(
                    EvidenceValidationFinding(
                        code="PHASE_B_TEMPORAL_SCHEMA_REQUIRED",
                        severity="error",
                        message="Protocol-v2.1 Phase-B analysis requires temporal schema v2.",
                        job_id=job.job_id,
                        artifact_id=artifact.artifact_id,
                    )
                )
                continue
            endpoints = tuple(window.end_interaction for window in record.reward_windows)
            if endpoints != expected_endpoints or any(
                window.interaction_count != 32 for window in record.reward_windows
            ):
                findings.append(
                    EvidenceValidationFinding(
                        code="PHASE_B_TEMPORAL_WINDOWS_INCOMPLETE",
                        severity="error",
                        message=(
                            "Protocol-v2.1 Phase-B temporal evidence does not contain the exact fixed-window grid."
                        ),
                        job_id=job.job_id,
                        artifact_id=artifact.artifact_id,
                    )
                )
        if observed_branches != expected_branches:
            findings.append(
                EvidenceValidationFinding(
                    code="PHASE_B_TEMPORAL_BRANCH_SET_INVALID",
                    severity="error",
                    message="Protocol-v2.1 Phase-B temporal records do not cover exact FN/FD/AN/AD branches.",
                    job_id=job.job_id,
                )
            )
