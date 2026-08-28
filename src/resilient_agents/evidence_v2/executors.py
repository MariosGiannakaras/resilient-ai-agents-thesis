"""Study-scheduler executors for protocol-v2 evidence processing."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..study import (
    ArtifactRole,
    EvidenceClass,
    JobOutcomeKind,
    StudyArtifact,
    StudyJobContext,
    StudyJobOutcome,
    StudyJobSpec,
    StudyStore,
)
from .validation import StudyEvidenceValidator


def _write_json_atomic(path: Path, payload: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    data = (
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    temporary.write_bytes(data)
    temporary.replace(path)
    return hashlib.sha256(data).hexdigest()


class StudyValidationExecutor:
    job_type = "study-validation"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        store = StudyStore.load(
            repo_root=context.repo_root,
            writable_root=context.writable_root,
            study_id=context.study_id,
        )
        report = StudyEvidenceValidator().validate(store)
        path = context.study_dir / "derived" / "validation" / "report.json"
        digest = _write_json_atomic(path, report.to_dict())
        relative = path.resolve().relative_to(context.writable_root.resolve()).as_posix()
        artifact = StudyArtifact(
            artifact_id="validation-report",
            role=ArtifactRole.VALIDATION_REPORT,
            evidence_class=EvidenceClass.DERIVED,
            relative_path=relative,
            sha256=digest,
            source_job_ids=(job.job_id,),
            metadata={
                "recipe_sha256": context.recipe_sha256,
                "planned_scientific_jobs": report.planned_scientific_jobs,
                "scientific_failures": report.scientific_failures,
                "skipped_scientific_jobs": report.skipped_scientific_jobs,
            },
        )
        if report.valid:
            return StudyJobOutcome(
                kind=JobOutcomeKind.COMPLETED,
                artifacts=(artifact,),
                measurements={
                    "planned_scientific_jobs": report.planned_scientific_jobs,
                    "completed_scientific_jobs": report.completed_scientific_jobs,
                    "scientific_failures": report.scientific_failures,
                    "skipped_scientific_jobs": report.skipped_scientific_jobs,
                },
            )
        return StudyJobOutcome(
            kind=JobOutcomeKind.INFRASTRUCTURE_FAILURE,
            message="protocol-v2 study evidence failed structural/integrity validation",
            artifacts=(artifact,),
            measurements={"error_count": sum(item.severity == "error" for item in report.findings)},
        )
