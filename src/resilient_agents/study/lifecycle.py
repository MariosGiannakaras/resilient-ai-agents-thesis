"""Fail-closed lifecycle state machine for materialized study plans."""
from __future__ import annotations

from dataclasses import dataclass, field

from .model import JobState, StudyJobSpec, StudyPlan, StudyStage


@dataclass
class StudyLifecycle:
    """Track one study plan without conflating scientific and infrastructure failure.

    The lifecycle enforces a global stage barrier: all units in an earlier stage
    must be scientifically resolved before a later stage can start. A direct job
    dependency is stricter: only a successful producer satisfies it. If a
    scientific producer fails, its dependent jobs are explicitly marked skipped
    rather than being executed against missing/fictional artifacts.
    """

    plan: StudyPlan
    _states: dict[str, JobState] = field(init=False, repr=False)
    _attempts: dict[str, int] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.plan, StudyPlan):
            raise ValueError("plan must be StudyPlan")
        self._states = {job.job_id: JobState.PENDING for job in self.plan.jobs}
        self._attempts = {job.job_id: 0 for job in self.plan.jobs}

    def state_for(self, job_id: str) -> JobState:
        try:
            return self._states[job_id]
        except KeyError as exc:
            raise KeyError(f"unknown study job: {job_id}") from exc

    def attempts_for(self, job_id: str) -> int:
        if job_id not in self._attempts:
            raise KeyError(f"unknown study job: {job_id}")
        return self._attempts[job_id]

    @property
    def current_stage(self) -> StudyStage | None:
        unresolved = [
            job.stage
            for job in self.plan.jobs
            if not self._states[job.job_id].resolves_stage
        ]
        return min(unresolved, key=lambda stage: stage.order) if unresolved else None

    @property
    def complete(self) -> bool:
        return all(state.resolves_stage for state in self._states.values())

    def _stage_barrier_open(self, job: StudyJobSpec) -> bool:
        for earlier in self.plan.jobs:
            if earlier.stage.order >= job.stage.order:
                continue
            if not self._states[earlier.job_id].resolves_stage:
                return False
        return True

    def _dependencies_successful(self, job: StudyJobSpec) -> bool:
        return all(
            self._states[dependency].satisfies_dependencies
            for dependency in job.dependencies
        )

    def ready_jobs(self) -> tuple[StudyJobSpec, ...]:
        self.skip_jobs_with_failed_dependencies()
        return tuple(
            job
            for job in self.plan.jobs
            if self._states[job.job_id] is JobState.PENDING
            and self._stage_barrier_open(job)
            and self._dependencies_successful(job)
        )

    def start(self, job_id: str) -> None:
        job = self.plan.by_id().get(job_id)
        if job is None:
            raise KeyError(f"unknown study job: {job_id}")
        if self._states[job_id] is not JobState.PENDING:
            raise RuntimeError(f"job {job_id} is not pending")
        self.skip_jobs_with_failed_dependencies()
        if self._states[job_id] is JobState.SKIPPED:
            raise RuntimeError(f"job {job_id} is skipped because an upstream job failed")
        if not self._stage_barrier_open(job):
            raise RuntimeError(f"earlier study stage is not resolved for job {job_id}")
        if not self._dependencies_successful(job):
            raise RuntimeError(f"job dependencies are not successful for {job_id}")
        self._attempts[job_id] += 1
        self._states[job_id] = JobState.RUNNING

    def complete_job(self, job_id: str) -> None:
        self._require_running(job_id)
        self._states[job_id] = JobState.COMPLETED

    def fail_scientifically(self, job_id: str) -> None:
        self._require_running(job_id)
        self._states[job_id] = JobState.SCIENTIFIC_FAILED
        self.skip_jobs_with_failed_dependencies()

    def fail_infrastructure(self, job_id: str) -> None:
        self._require_running(job_id)
        self._states[job_id] = JobState.INFRASTRUCTURE_FAILED

    def cancel(self, job_id: str) -> None:
        state = self.state_for(job_id)
        if state not in {JobState.PENDING, JobState.RUNNING}:
            raise RuntimeError(f"job {job_id} cannot be cancelled from {state.value}")
        self._states[job_id] = JobState.CANCELLED

    def retry_infrastructure_failure(self, job_id: str) -> None:
        if not self.state_for(job_id).retryable:
            raise RuntimeError(f"job {job_id} is not an infrastructure failure")
        self._states[job_id] = JobState.PENDING

    def skip_jobs_with_failed_dependencies(self) -> tuple[str, ...]:
        """Propagate scientifically unavailable downstream units deterministically."""

        skipped: list[str] = []
        changed = True
        while changed:
            changed = False
            for job in self.plan.jobs:
                if self._states[job.job_id] is not JobState.PENDING:
                    continue
                dependency_states = [self._states[item] for item in job.dependencies]
                if any(
                    state in {JobState.SCIENTIFIC_FAILED, JobState.SKIPPED}
                    for state in dependency_states
                ):
                    self._states[job.job_id] = JobState.SKIPPED
                    skipped.append(job.job_id)
                    changed = True
        return tuple(skipped)

    def progress(self) -> dict[str, int]:
        return {
            "total": len(self._states),
            "resolved": sum(state.resolves_stage for state in self._states.values()),
            "completed": sum(
                state is JobState.COMPLETED for state in self._states.values()
            ),
            "scientific_failed": sum(
                state is JobState.SCIENTIFIC_FAILED for state in self._states.values()
            ),
            "skipped": sum(state is JobState.SKIPPED for state in self._states.values()),
            "infrastructure_failed": sum(
                state is JobState.INFRASTRUCTURE_FAILED for state in self._states.values()
            ),
            "running": sum(state is JobState.RUNNING for state in self._states.values()),
            "pending": sum(state is JobState.PENDING for state in self._states.values()),
            "cancelled": sum(state is JobState.CANCELLED for state in self._states.values()),
        }

    def snapshot_states(self) -> dict[str, JobState]:
        return dict(self._states)

    def _require_running(self, job_id: str) -> None:
        if self.state_for(job_id) is not JobState.RUNNING:
            raise RuntimeError(f"job {job_id} is not running")
