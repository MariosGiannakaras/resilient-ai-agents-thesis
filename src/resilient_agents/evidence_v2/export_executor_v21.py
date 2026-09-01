"""Protocol-aware export executor for the DEC-060 evidence package."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from ..run_bundle import sha256_file
from ..study.model import ArtifactRole, EvidenceClass, StudyArtifact, StudyJobSpec, StudyStage
from ..study.ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome
from ..study.store import StudyStore
from .export_executor import StudyExportExecutor, _V1_EXPORTS, _V2_ADDITIONAL_EXPORTS, _mapping, _read_json, _relative
from .exports_v21 import StudyExportEngineV21


class StudyExportExecutorV21:
    """Persist deterministic v2.1 recovery/comparison tables and provenance."""

    job_type = "study-export"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if context.recipe.protocol_version != "protocol-v2.1":
            raise ValueError("v2.1 export executor requires protocol-v2.1 recipe")
        if job.stage is not StudyStage.EXPORT:
            raise ValueError("study-export executor requires an EXPORT job")
        specification = _mapping(job.payload.get("specification"), field="study-export specification")
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
            raise RuntimeError("study export requires exactly one derived analysis-package artifact")
        analysis_artifact = analyses[0]
        analysis_path = context.writable_root / analysis_artifact.relative_path
        if sha256_file(analysis_path) != analysis_artifact.sha256:
            raise RuntimeError("analysis-package artifact content hash mismatch")
        package = _read_json(analysis_path, field="analysis package")

        output_dir = context.study_dir / "derived" / "export"
        exported = StudyExportEngineV21().export(
            analysis_package=package,
            specification=specification,
            output_dir=output_dir,
            source_analysis_artifact_id=analysis_artifact.artifact_id,
            source_analysis_sha256=analysis_artifact.sha256,
        )
        by_filename = {item["filename"]: item for item in exported["files"]}
        expected = {**_V1_EXPORTS, **_V2_ADDITIONAL_EXPORTS}
        if exported["manifest"].get("package") != "protocol-v2-evidence-handoff-v2":
            raise RuntimeError("v2.1 requires the version-2 evidence handoff package")
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
                        "protocol_extension": "v2.1-recovery-comparisons",
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
                "analysis_recipe": exported["manifest"]["analysis_recipe"],
                "figure_rendering_status": exported["manifest"]["figure_rendering_status"],
            },
        )
        return StudyJobOutcome(
            kind=JobOutcomeKind.COMPLETED,
            artifacts=(*artifacts, manifest_artifact),
            measurements={
                "exported_files": len(artifacts) + 1,
                "result_count": int(by_filename["result-index.json"]["row_count"]),
                "phase_a_summary_rows": int(by_filename["phase-a-method-summary.csv"]["row_count"]),
                "phase_b_summary_rows": int(by_filename["phase-b-method-condition-summary.csv"]["row_count"]),
                "recovery_summary_rows": int(by_filename["recovery-method-condition-summary.csv"]["row_count"]),
            },
        )


class StudyExportExecutorRouter:
    """Route v2.1 exports without changing historical export behavior."""

    job_type = "study-export"

    def __init__(self) -> None:
        self._legacy = StudyExportExecutor()
        self._v21 = StudyExportExecutorV21()

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if context.recipe.protocol_version == "protocol-v2.1":
            return self._v21.execute(job, context=context)
        return self._legacy.execute(job, context=context)
