"""Deterministic fail-closed scheduler for study job DAGs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .model import StudyJobSpec
from .ports import (
    JobOutcomeKind,
    StudyJobContext,
    StudyJobExecutor,
    StudyJobOutcome,
)
from .store import StudyStore


class StudyExecutorCrashed(RuntimeError):
    """Unexpected executor exception recorded as infrastructure failure."""


class StudyExecutorRegistry:
    """Explicit job-type registry; no dynamic UI/import reflection."""

    def __init__(self, executors: Iterable[StudyJobExecutor] = ()) -> None:
        self._executors: dict[str, StudyJobExecutor] = {}
        for executor in executors:
            self.register(executor)

    def register(self, executor: StudyJobExecutor) -> None:
        if not isinstance(executor, StudyJobExecutor):
            raise ValueError("executor must satisfy StudyJobExecutor")
        job_type = executor.job_type
        if not isinstance(job_type, str) or not job_type.strip():
            raise ValueError("executor job_type must be non-empty")
        if job_type in self._executors:
            raise ValueError(f"duplicate study executor for job_type: {job_type}")
        self._executors[job_type] = executor

    def resolve(self, job: StudyJobSpec) -> StudyJobExecutor:
        job_type = job.payload.get("job_type")
        if not isinstance(job_type, str) or not job_type:
            raise ValueError(f"study job {job.job_id} has no explicit job_type")
        try:
            return self._executors[job_type]
        except KeyError as exc:
            raise RuntimeError(
                f"no study executor registered for job_type {job_type!r}"
            ) from exc

    def job_types(self) -> tuple[str, ...]:
        return tuple(sorted(self._executors))


@dataclass(frozen=True)
class ScheduledJobResult:
    job_id: str
    outcome: StudyJobOutcome


class StudyScheduler:
    """Execute only recipe-materialized ready jobs in deterministic plan order.

    This first scheduler is intentionally sequential. Parallelism is a later
    resource-policy optimization and must not change stage/dependency semantics,
    scientific identities, RNG streams or output interpretation.
    """

    def __init__(
        self,
        *,
        store: StudyStore,
        executors: StudyExecutorRegistry,
    ) -> None:
        if not isinstance(store, StudyStore):
            raise ValueError("store must be StudyStore")
        if not isinstance(executors, StudyExecutorRegistry):
            raise ValueError("executors must be StudyExecutorRegistry")
        self.store = store
        self.executors = executors

    def run_job(self, job_id: str) -> ScheduledJobResult:
        ready = {job.job_id: job for job in self.store.lifecycle.ready_jobs()}
        job = ready.get(job_id)
        if job is None:
            raise RuntimeError(f"study job is not ready: {job_id}")
        executor = self.executors.resolve(job)
        self.store.start_job(job_id)
        context = StudyJobContext(
            study_id=self.store.execution_id,
            recipe=self.store.recipe,
            recipe_sha256=self.store.recipe.sha256(),
            repo_root=self.store.repo_root,
            writable_root=self.store.writable_root,
            study_dir=self.store.study_dir,
            attempt=self.store.lifecycle.attempts_for(job_id),
        )
        try:
            outcome = executor.execute(job, context=context)
        except Exception as exc:
            reason = f"unclassified executor exception: {type(exc).__name__}: {exc}"
            self.store.fail_job_infrastructure(job_id, reason=reason)
            raise StudyExecutorCrashed(reason) from exc

        if not isinstance(outcome, StudyJobOutcome):
            reason = "executor returned a non-StudyJobOutcome result"
            self.store.fail_job_infrastructure(job_id, reason=reason)
            raise StudyExecutorCrashed(reason)

        for artifact in outcome.artifacts:
            if job_id not in artifact.source_job_ids:
                reason = (
                    f"executor artifact {artifact.artifact_id} does not include "
                    f"producer job {job_id} in source_job_ids"
                )
                self.store.fail_job_infrastructure(job_id, reason=reason)
                raise StudyExecutorCrashed(reason)
            try:
                self.store.record_artifact(artifact)
            except Exception as exc:
                reason = (
                    f"artifact registration failed for {artifact.artifact_id}: "
                    f"{type(exc).__name__}: {exc}"
                )
                self.store.fail_job_infrastructure(job_id, reason=reason)
                raise StudyExecutorCrashed(reason) from exc

        if outcome.kind is JobOutcomeKind.COMPLETED:
            self.store.complete_job(job_id)
        elif outcome.kind is JobOutcomeKind.SCIENTIFIC_FAILURE:
            self.store.fail_job_scientifically(job_id, reason=outcome.message)
        elif outcome.kind is JobOutcomeKind.INFRASTRUCTURE_FAILURE:
            self.store.fail_job_infrastructure(job_id, reason=outcome.message)
        else:  # pragma: no cover - enum/dataclass validation makes this defensive.
            raise AssertionError(f"unhandled outcome kind: {outcome.kind}")
        return ScheduledJobResult(job_id=job_id, outcome=outcome)

    def run_ready(
        self,
        *,
        max_jobs: int | None = None,
        stop_on_infrastructure_failure: bool = True,
    ) -> tuple[ScheduledJobResult, ...]:
        if max_jobs is not None and (
            not isinstance(max_jobs, int) or isinstance(max_jobs, bool) or max_jobs <= 0
        ):
            raise ValueError("max_jobs must be a positive integer or None")
        results: list[ScheduledJobResult] = []
        while max_jobs is None or len(results) < max_jobs:
            ready = self.store.lifecycle.ready_jobs()
            if not ready:
                break
            result = self.run_job(ready[0].job_id)
            results.append(result)
            if (
                stop_on_infrastructure_failure
                and result.outcome.kind is JobOutcomeKind.INFRASTRUCTURE_FAILURE
            ):
                break
        return tuple(results)
