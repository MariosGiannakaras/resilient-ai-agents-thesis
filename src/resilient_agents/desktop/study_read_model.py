"""Read-only desktop projection over durable framework-neutral Study state."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..study.scheduler import StudyExecutorRegistry
from ..study.service import StudyService


@dataclass(frozen=True)
class StudyListItem:
    study_id: str
    protocol_version: str
    evidence_class: str
    status: str
    current_stage: str | None
    total_jobs: int
    resolved_jobs: int
    completed_jobs: int
    running_jobs: int
    scientific_failures: int
    infrastructure_failures: int
    finalized: bool

    @property
    def progress_fraction(self) -> float:
        if self.total_jobs <= 0:
            return 0.0
        return min(1.0, max(0.0, self.resolved_jobs / self.total_jobs))

    @property
    def stage_label(self) -> str:
        labels = {
            "phase-a": "Nominal learning",
            "phase-b": "Resilience test",
            "validation": "Validation",
            "analysis": "Analysis",
            "export": "Export",
            "feasibility": "Feasibility",
            "tuning-freeze": "Tuning / freeze",
        }
        if self.current_stage is None:
            return "Complete" if self.finalized else "Resolved"
        return labels.get(self.current_stage, self.current_stage)


@dataclass(frozen=True)
class ArtifactListItem:
    artifact_id: str
    role: str
    evidence_class: str
    relative_path: str
    sha256: str
    source_job_ids: tuple[str, ...]
    source_artifact_ids: tuple[str, ...]

    @property
    def source_job_count(self) -> int:
        return len(self.source_job_ids)

    @property
    def source_artifact_count(self) -> int:
        return len(self.source_artifact_ids)


class DesktopStudyReadModel:
    """Safe read facade for the Qt application.

    An empty executor registry is supplied intentionally. Listing/status/artifact
    operations cannot execute jobs, and the UI therefore does not import or own
    scientific executors merely to render durable state.
    """

    def __init__(self, *, repo_root: Path, writable_root: Path | None = None) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.writable_root = (
            Path(writable_root).resolve() if writable_root else self.repo_root
        )
        self._service = StudyService(
            repo_root=self.repo_root,
            writable_root=self.writable_root,
            executors=StudyExecutorRegistry(),
        )

    def studies(self) -> tuple[StudyListItem, ...]:
        items: list[StudyListItem] = []
        for status in self._service.list_studies():
            progress = status.progress
            items.append(
                StudyListItem(
                    study_id=status.study_id,
                    protocol_version=status.protocol_version,
                    evidence_class=status.evidence_class,
                    status=status.status,
                    current_stage=status.current_stage,
                    total_jobs=int(progress.get("total", 0)),
                    resolved_jobs=int(progress.get("resolved", 0)),
                    completed_jobs=int(progress.get("completed", 0)),
                    running_jobs=int(progress.get("running", 0)),
                    scientific_failures=int(progress.get("scientific_failed", 0)),
                    infrastructure_failures=int(progress.get("infrastructure_failed", 0)),
                    finalized=status.finalized,
                )
            )
        return tuple(items)

    def artifacts(self, study_id: str) -> tuple[ArtifactListItem, ...]:
        return tuple(
            ArtifactListItem(
                artifact_id=artifact.artifact_id,
                role=artifact.role.value,
                evidence_class=artifact.evidence_class.value,
                relative_path=artifact.relative_path,
                sha256=artifact.sha256,
                source_job_ids=tuple(artifact.source_job_ids),
                source_artifact_ids=tuple(artifact.source_artifact_ids),
            )
            for artifact in self._service.artifacts(study_id)
        )
