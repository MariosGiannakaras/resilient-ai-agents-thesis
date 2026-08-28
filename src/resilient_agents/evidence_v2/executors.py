"""Study-scheduler executors for protocol-v2 evidence processing."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from ..study.model import ArtifactRole, EvidenceClass, StudyArtifact, StudyJobSpec, StudyStage
from ..study.ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome
from ..study.store import StudyStore
from .analysis import StudyAnalysisEngine
from .denominators import build_scientific_denominators
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


def _mapping(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return dict(value)


class StudyValidationExecutor:
    job_type = "study-validation"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if job.stage is not StudyStage.VALIDATION:
            raise ValueError("study-validation executor requires a VALIDATION job")
        store = StudyStore.load(
            repo_root=context.repo_root,
            writable_root=context.writable_root,
            study_id=context.study_id,
        )
        report = StudyEvidenceValidator().validate(store)
        path = context.study_dir / "derived" / "validation" / "report.json"
        digest = _write_json_atomic(path, report.to_dict())
        relative = path.resolve().relative_to(context.writable_root.resolve()).as_posix()
        source_ids = tuple(
            sorted(
                artifact.artifact_id
                for artifact in store.artifacts()
                if artifact.role
                in {
                    ArtifactRole.RUN_BUNDLE,
                    ArtifactRole.SCIENTIFIC_CHECKPOINT,
                    ArtifactRole.FAILURE_RECORD,
                    ArtifactRole.ANALYSIS_DATA,
                }
            )
        )
        artifact = StudyArtifact(
            artifact_id="validation-report",
            role=ArtifactRole.VALIDATION_REPORT,
            evidence_class=EvidenceClass.DERIVED,
            relative_path=relative,
            sha256=digest,
            source_job_ids=(job.job_id,),
            source_artifact_ids=source_ids,
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
            measurements={
                "error_count": sum(
                    item.severity == "error" for item in report.findings
                )
            },
        )


class StudyAnalysisExecutor:
    """Build the deterministic root-level protocol-v2 analysis package."""

    job_type = "study-analysis"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if job.stage is not StudyStage.ANALYSIS:
            raise ValueError("study-analysis executor requires an ANALYSIS job")
        specification = _mapping(
            job.payload.get("specification"),
            field="study-analysis specification",
        )
        store = StudyStore.load(
            repo_root=context.repo_root,
            writable_root=context.writable_root,
            study_id=context.study_id,
        )
        validation_reports = [
            artifact
            for artifact in store.artifacts()
            if artifact.role is ArtifactRole.VALIDATION_REPORT
        ]
        if len(validation_reports) != 1:
            raise RuntimeError(
                "study analysis requires exactly one completed validation-report artifact"
            )

        package = StudyAnalysisEngine().analyze(
            store,
            specification=specification,
        )
        package["scientific_denominators"] = build_scientific_denominators(store)
        path = context.study_dir / "derived" / "analysis" / "analysis-package.json"
        digest = _write_json_atomic(path, package)
        relative = path.resolve().relative_to(context.writable_root.resolve()).as_posix()
        source_ids = tuple(
            sorted(
                {
                    validation_reports[0].artifact_id,
                    *(
                        artifact.artifact_id
                        for artifact in store.artifacts()
                        if artifact.role is ArtifactRole.ANALYSIS_DATA
                        and artifact.evidence_class is not EvidenceClass.DERIVED
                    ),
                }
            )
        )
        artifact = StudyArtifact(
            artifact_id="analysis-package",
            role=ArtifactRole.ANALYSIS_DATA,
            evidence_class=EvidenceClass.DERIVED,
            relative_path=relative,
            sha256=digest,
            source_job_ids=(job.job_id,),
            source_artifact_ids=source_ids,
            metadata={
                "record_type": "protocol-v2-analysis-package",
                "analysis_recipe": package["analysis_recipe"],
                "recipe_sha256": context.recipe_sha256,
            },
        )
        denominators = package["scientific_denominators"]
        scientific_failures = sum(
            int(row["scientific_failed"])
            for section in denominators.values()
            for row in section
        )
        return StudyJobOutcome(
            kind=JobOutcomeKind.COMPLETED,
            artifacts=(artifact,),
            measurements={
                "phase_a_unit_records": len(package["phase_a"]["unit_records"]),
                "phase_a_root_records": len(package["phase_a"]["root_records"]),
                "phase_b_unit_records": len(package["phase_b"]["unit_records"]),
                "phase_b_root_records": len(package["phase_b"]["root_records"]),
                "scientific_failures": scientific_failures,
            },
        )
