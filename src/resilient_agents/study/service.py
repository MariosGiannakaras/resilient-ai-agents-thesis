"""Framework-neutral application facade for study-first backend control/read APIs."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .model import StudyArtifact
from .planner import StudyPlanPreview, StudyPlanner
from .recipe import StudyRecipe
from .scheduler import ScheduledJobResult, StudyExecutorRegistry, StudyScheduler
from .store import STUDY_FINALIZATION_MARKER, StudyStore


@dataclass(frozen=True)
class StudyStatus:
    study_id: str
    protocol_version: str
    evidence_class: str
    frozen_recipe: bool
    recipe_sha256: str
    status: str
    current_stage: str | None
    progress: dict[str, int]
    ready_job_ids: tuple[str, ...]
    finalized: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "study_id": self.study_id,
            "protocol_version": self.protocol_version,
            "evidence_class": self.evidence_class,
            "frozen_recipe": self.frozen_recipe,
            "recipe_sha256": self.recipe_sha256,
            "status": self.status,
            "current_stage": self.current_stage,
            "progress": dict(self.progress),
            "ready_job_ids": list(self.ready_job_ids),
            "finalized": self.finalized,
        }


@dataclass(frozen=True)
class StudyPlanSummary:
    study_id: str
    protocol_version: str
    evidence_class: str
    frozen_recipe: bool
    recipe_sha256: str
    preview: StudyPlanPreview

    def to_dict(self) -> dict[str, Any]:
        return {
            "study_id": self.study_id,
            "protocol_version": self.protocol_version,
            "evidence_class": self.evidence_class,
            "frozen_recipe": self.frozen_recipe,
            "recipe_sha256": self.recipe_sha256,
            "preview": self.preview.to_dict(),
        }


class StudyService:
    """Single backend facade intended for the later replacement frontend.

    The facade owns no UI session state. Durable filesystem study evidence is
    always reloaded before control/read operations, so application restart does
    not alter scientific identity or progress.
    """

    def __init__(
        self,
        *,
        repo_root: Path,
        writable_root: Path | None = None,
        executors: StudyExecutorRegistry | None = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.writable_root = (
            Path(writable_root).resolve() if writable_root else self.repo_root
        )
        self.executors = executors or StudyExecutorRegistry()

    def preview(self, recipe: StudyRecipe) -> StudyPlanSummary:
        planner = StudyPlanner(recipe)
        return StudyPlanSummary(
            study_id=recipe.recipe_id,
            protocol_version=recipe.protocol_version,
            evidence_class=recipe.evidence_class.value,
            frozen_recipe=recipe.frozen,
            recipe_sha256=recipe.sha256(),
            preview=planner.preview(),
        )

    def create(self, recipe: StudyRecipe) -> StudyStatus:
        planner = StudyPlanner(recipe)
        store = StudyStore.create(
            repo_root=self.repo_root,
            writable_root=self.writable_root,
            recipe=recipe,
            plan=planner.materialize(),
        )
        return self._status(store)

    def status(self, study_id: str) -> StudyStatus:
        return self._status(self._load(study_id))

    def list_studies(self) -> tuple[StudyStatus, ...]:
        root = self.writable_root / "results" / "studies"
        if not root.is_dir():
            return ()
        statuses: list[StudyStatus] = []
        for path in sorted(item for item in root.iterdir() if item.is_dir()):
            statuses.append(self.status(path.name))
        return tuple(statuses)

    def artifacts(self, study_id: str) -> tuple[StudyArtifact, ...]:
        return self._load(study_id).artifacts()

    def run_ready(
        self,
        study_id: str,
        *,
        max_jobs: int | None = None,
        stop_on_infrastructure_failure: bool = True,
    ) -> tuple[ScheduledJobResult, ...]:
        store = self._load(study_id)
        scheduler = StudyScheduler(store=store, executors=self.executors)
        return scheduler.run_ready(
            max_jobs=max_jobs,
            stop_on_infrastructure_failure=stop_on_infrastructure_failure,
        )

    def run_job(self, study_id: str, job_id: str) -> ScheduledJobResult:
        store = self._load(study_id)
        return StudyScheduler(store=store, executors=self.executors).run_job(job_id)

    def retry_infrastructure_failure(self, study_id: str, job_id: str) -> StudyStatus:
        store = self._load(study_id)
        store.retry_job(job_id)
        return self._status(store)

    def finalize(self, study_id: str) -> StudyStatus:
        store = self._load(study_id)
        store.finalize()
        return self.status(study_id)

    def _load(self, study_id: str) -> StudyStore:
        return StudyStore.load(
            repo_root=self.repo_root,
            writable_root=self.writable_root,
            study_id=study_id,
        )

    @staticmethod
    def _status(store: StudyStore) -> StudyStatus:
        current_stage = store.lifecycle.current_stage
        return StudyStatus(
            study_id=store.plan.study_id,
            protocol_version=store.recipe.protocol_version,
            evidence_class=store.recipe.evidence_class.value,
            frozen_recipe=store.recipe.frozen,
            recipe_sha256=store.recipe.sha256(),
            status=str(store.manifest["status"]),
            current_stage=current_stage.value if current_stage is not None else None,
            progress=store.lifecycle.progress(),
            ready_job_ids=tuple(job.job_id for job in store.lifecycle.ready_jobs()),
            finalized=(store.study_dir / STUDY_FINALIZATION_MARKER).is_file(),
        )
