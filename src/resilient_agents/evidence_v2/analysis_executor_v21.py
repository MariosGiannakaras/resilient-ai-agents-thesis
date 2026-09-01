"""Protocol-aware Study analysis dispatch for the DEC-060 amendment."""
from __future__ import annotations

from ..study.model import ArtifactRole, EvidenceClass, StudyArtifact, StudyJobSpec, StudyStage
from ..study.ports import JobOutcomeKind, StudyJobContext, StudyJobOutcome
from ..study.store import StudyStore
from .analysis_v21 import StudyAnalysisEngineV21
from .denominators import build_scientific_denominators
from .executors import StudyAnalysisExecutor, _mapping, _write_json_atomic


class StudyAnalysisExecutorV21:
    """Persist protocol-v2.1 root-level analysis with actual-root-df intervals."""

    job_type = "study-analysis"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if context.recipe.protocol_version != "protocol-v2.1":
            raise ValueError("v2.1 analysis executor requires protocol-v2.1 recipe")
        if job.stage is not StudyStage.ANALYSIS:
            raise ValueError("study-analysis executor requires an ANALYSIS job")
        specification = _mapping(
            job.payload.get("specification"), field="study-analysis specification"
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

        package = StudyAnalysisEngineV21().analyze(store, specification=specification)
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
                "protocol_extension": "v2.1-recovery-comparisons",
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


class StudyAnalysisExecutorRouter:
    """Keep legacy analysis unchanged and route only explicit v2.1 recipes."""

    job_type = "study-analysis"

    def __init__(self) -> None:
        self._legacy = StudyAnalysisExecutor()
        self._v21 = StudyAnalysisExecutorV21()

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if context.recipe.protocol_version == "protocol-v2.1":
            return self._v21.execute(job, context=context)
        return self._legacy.execute(job, context=context)
