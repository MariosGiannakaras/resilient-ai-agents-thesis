"""Study-scheduler executor for deterministic protocol-v2 evidence handoff."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from ..run_bundle import sha256_file
from ..study.model import ArtifactRole, EvidenceClass, StudyArtifact, StudyJobSpec, StudyStage
from ..study.ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome
from ..study.store import StudyStore
from .exports import StudyExportEngine


def _mapping(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return dict(value)


def _read_json(path: Path, *, field: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{field} is unreadable: {path}") from exc
    if not isinstance(payload, Mapping):
        raise RuntimeError(f"{field} must be a JSON object")
    return dict(payload)


def _relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


_V1_EXPORTS: Mapping[str, tuple[str, ArtifactRole]] = {
    "phase-a-method-summary.csv": (
        "thesis-table-phase-a-method-summary",
        ArtifactRole.THESIS_TABLE,
    ),
    "phase-b-method-condition-summary.csv": (
        "thesis-table-phase-b-method-condition-summary",
        ArtifactRole.THESIS_TABLE,
    ),
    "phase-a-root-records.csv": (
        "analysis-table-phase-a-root-records",
        ArtifactRole.ANALYSIS_TABLE,
    ),
    "phase-b-root-records.csv": (
        "analysis-table-phase-b-root-records",
        ArtifactRole.ANALYSIS_TABLE,
    ),
    "result-index.json": ("result-index", ArtifactRole.PROVENANCE),
}

_V2_ADDITIONAL_EXPORTS: Mapping[str, tuple[str, ArtifactRole]] = {
    "phase-a-method-contrasts.csv": (
        "thesis-table-phase-a-method-contrasts",
        ArtifactRole.THESIS_TABLE,
    ),
    "phase-b-method-contrasts.csv": (
        "thesis-table-phase-b-method-contrasts",
        ArtifactRole.THESIS_TABLE,
    ),
    "recovery-root-records.csv": (
        "analysis-table-recovery-root-records",
        ArtifactRole.ANALYSIS_TABLE,
    ),
    "recovery-trajectory-records.csv": (
        "analysis-table-recovery-trajectories",
        ArtifactRole.ANALYSIS_TABLE,
    ),
    "recovery-method-condition-summary.csv": (
        "thesis-table-recovery-method-condition-summary",
        ArtifactRole.THESIS_TABLE,
    ),
    "recovery-method-contrasts.csv": (
        "thesis-table-recovery-method-contrasts",
        ArtifactRole.THESIS_TABLE,
    ),
    "recovery-sensitivity-root-records.csv": (
        "analysis-table-recovery-sensitivity",
        ArtifactRole.ANALYSIS_TABLE,
    ),
}


class StudyExportExecutor:
    """Export stable evidence tables/indexes from one validated analysis package."""

    job_type = "study-export"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if job.stage is not StudyStage.EXPORT:
            raise ValueError("study-export executor requires an EXPORT job")
        specification = _mapping(
            job.payload.get("specification"),
            field="study-export specification",
        )
        store = StudyStore.load(
            repo_root=context.repo_root,
            writable_root=context.writable_root,
            study_id=context.study_id,
        )
        analyses = [
            artifact
            for artifact in store.artifacts()
            if artifact.artifact_id == "analysis-package"
            and artifact.role is ArtifactRole.ANALYSIS_DATA
            and artifact.evidence_class is EvidenceClass.DERIVED
        ]
        if len(analyses) != 1:
            raise RuntimeError(
                "study export requires exactly one derived analysis-package artifact"
            )
        analysis_artifact = analyses[0]
        analysis_path = context.writable_root / analysis_artifact.relative_path
        if sha256_file(analysis_path) != analysis_artifact.sha256:
            raise RuntimeError("analysis-package artifact content hash mismatch")
        package = _read_json(analysis_path, field="analysis package")

        output_dir = context.study_dir / "derived" / "export"
        exported = StudyExportEngine().export(
            analysis_package=package,
            specification=specification,
            output_dir=output_dir,
            source_analysis_artifact_id=analysis_artifact.artifact_id,
            source_analysis_sha256=analysis_artifact.sha256,
        )
        by_filename = {item["filename"]: item for item in exported["files"]}
        package_id = exported["manifest"]["package"]
        if package_id == "protocol-v2-evidence-handoff-v1":
            expected = dict(_V1_EXPORTS)
        elif package_id == "protocol-v2-evidence-handoff-v2":
            expected = {**_V1_EXPORTS, **_V2_ADDITIONAL_EXPORTS}
        else:
            raise RuntimeError("export engine returned an unsupported handoff package")
        if set(by_filename) != set(expected):
            raise RuntimeError("export engine returned an unexpected handoff file set")

        artifacts: list[StudyArtifact] = []
        for filename in sorted(expected):
            artifact_id, role = expected[filename]
            metadata = by_filename[filename]
            path = output_dir / filename
            actual_sha = sha256_file(path)
            if actual_sha != metadata["sha256"]:
                raise RuntimeError(f"exported file hash mismatch: {filename}")
            artifacts.append(
                StudyArtifact(
                    artifact_id=artifact_id,
                    role=role,
                    evidence_class=EvidenceClass.DERIVED,
                    relative_path=_relative(path, context.writable_root),
                    sha256=actual_sha,
                    source_job_ids=(job.job_id,),
                    source_artifact_ids=(analysis_artifact.artifact_id,),
                    metadata={
                        "row_count": int(metadata["row_count"]),
                        "recipe_sha256": context.recipe_sha256,
                    },
                )
            )

        manifest_path = Path(exported["manifest_path"])
        manifest_sha = sha256_file(manifest_path)
        if manifest_sha != exported["manifest_sha256"]:
            raise RuntimeError("evidence-handoff manifest hash mismatch")
        manifest_artifact = StudyArtifact(
            artifact_id="evidence-handoff-package",
            role=ArtifactRole.EVIDENCE_PACKAGE,
            evidence_class=EvidenceClass.DERIVED,
            relative_path=_relative(manifest_path, context.writable_root),
            sha256=manifest_sha,
            source_job_ids=(job.job_id,),
            source_artifact_ids=(
                analysis_artifact.artifact_id,
                *(artifact.artifact_id for artifact in artifacts),
            ),
            metadata={
                "package": exported["manifest"]["package"],
                "recipe_sha256": context.recipe_sha256,
                "figure_rendering_status": exported["manifest"][
                    "figure_rendering_status"
                ],
            },
        )
        return StudyJobOutcome(
            kind=JobOutcomeKind.COMPLETED,
            artifacts=(*artifacts, manifest_artifact),
            measurements={
                "exported_files": len(artifacts) + 1,
                "result_count": int(by_filename["result-index.json"]["row_count"]),
                "phase_a_summary_rows": int(
                    by_filename["phase-a-method-summary.csv"]["row_count"]
                ),
                "phase_b_summary_rows": int(
                    by_filename["phase-b-method-condition-summary.csv"]["row_count"]
                ),
                "recovery_summary_rows": int(
                    by_filename.get("recovery-method-condition-summary.csv", {}).get(
                        "row_count", 0
                    )
                ),
            },
        )
