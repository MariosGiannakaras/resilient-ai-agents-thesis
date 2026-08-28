from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.study import (
    EvidenceClass,
    JobOutcomeKind,
    JobState,
    StudyExecutorCrashed,
    StudyExecutorRegistry,
    StudyJobContext,
    StudyJobOutcome,
    StudyJobSpec,
    StudyPlan,
    StudyRecipe,
    StudyScheduler,
    StudyStage,
    StudyStore,
)


class _FakeExecutor:
    def __init__(self, job_type: str, outcomes: dict[str, list[StudyJobOutcome]]) -> None:
        self.job_type = job_type
        self.outcomes = outcomes

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        self.assert_context(job, context)
        queue = self.outcomes.setdefault(
            job.job_id,
            [StudyJobOutcome(kind=JobOutcomeKind.COMPLETED)],
        )
        return queue.pop(0)

    @staticmethod
    def assert_context(job: StudyJobSpec, context: StudyJobContext) -> None:
        if context.study_id != context.recipe.recipe_id:
            raise AssertionError("bad study context")
        if context.recipe_sha256 != job.payload["recipe_sha256"]:
            raise AssertionError("job/context recipe hash mismatch")


class _CrashingExecutor:
    job_type = "phase-a-training"

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        raise RuntimeError("simulated worker crash")


class StudySchedulerTests(unittest.TestCase):
    def _recipe(self, recipe_id: str = "scheduler-study") -> StudyRecipe:
        return StudyRecipe(
            recipe_id=recipe_id,
            protocol_version="protocol-v2.0-candidate",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="scheduler-test",
            frozen=False,
            study={"purpose": "scheduler-test"},
        )

    def _plan(self, recipe: StudyRecipe) -> StudyPlan:
        digest = recipe.sha256()
        return StudyPlan(
            study_id=recipe.recipe_id,
            jobs=(
                StudyJobSpec(
                    job_id="phase-a",
                    stage=StudyStage.PHASE_A,
                    evidence_class=recipe.evidence_class,
                    payload={
                        "job_type": "phase-a-training",
                        "recipe_sha256": digest,
                    },
                ),
                StudyJobSpec(
                    job_id="phase-b",
                    stage=StudyStage.PHASE_B,
                    evidence_class=recipe.evidence_class,
                    dependencies=("phase-a",),
                    payload={
                        "job_type": "phase-b-branch",
                        "recipe_sha256": digest,
                    },
                ),
                StudyJobSpec(
                    job_id="validate",
                    stage=StudyStage.VALIDATION,
                    evidence_class=EvidenceClass.DERIVED,
                    payload={
                        "job_type": "study-validation",
                        "recipe_sha256": digest,
                    },
                ),
                StudyJobSpec(
                    job_id="analyze",
                    stage=StudyStage.ANALYSIS,
                    evidence_class=EvidenceClass.DERIVED,
                    dependencies=("validate",),
                    payload={
                        "job_type": "study-analysis",
                        "recipe_sha256": digest,
                    },
                ),
                StudyJobSpec(
                    job_id="export",
                    stage=StudyStage.EXPORT,
                    evidence_class=EvidenceClass.DERIVED,
                    dependencies=("analyze",),
                    payload={
                        "job_type": "study-export",
                        "recipe_sha256": digest,
                    },
                ),
            ),
        )

    def _store(self, root: Path) -> StudyStore:
        recipe = self._recipe()
        return StudyStore.create(
            repo_root=root,
            writable_root=root,
            recipe=recipe,
            plan=self._plan(recipe),
        )

    def _registry(
        self,
        outcomes: dict[str, list[StudyJobOutcome]] | None = None,
    ) -> StudyExecutorRegistry:
        outcomes = outcomes or {}
        return StudyExecutorRegistry(
            [
                _FakeExecutor("phase-a-training", outcomes),
                _FakeExecutor("phase-b-branch", outcomes),
                _FakeExecutor("study-validation", outcomes),
                _FakeExecutor("study-analysis", outcomes),
                _FakeExecutor("study-export", outcomes),
            ]
        )

    def test_runs_complete_study_in_stage_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self._store(Path(directory))
            scheduler = StudyScheduler(store=store, executors=self._registry())
            results = scheduler.run_ready()
            self.assertEqual(
                [item.job_id for item in results],
                ["phase-a", "phase-b", "validate", "analyze", "export"],
            )
            self.assertTrue(store.lifecycle.complete)
            self.assertEqual(store.lifecycle.progress()["completed"], 5)

    def test_scientific_failure_skips_dependent_branch_but_keeps_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self._store(Path(directory))
            outcomes = {
                "phase-a": [
                    StudyJobOutcome(
                        kind=JobOutcomeKind.SCIENTIFIC_FAILURE,
                        message="non-finite scientific update",
                    )
                ]
            }
            scheduler = StudyScheduler(store=store, executors=self._registry(outcomes))
            results = scheduler.run_ready()
            self.assertEqual(
                [item.job_id for item in results],
                ["phase-a", "validate", "analyze", "export"],
            )
            self.assertIs(store.lifecycle.state_for("phase-a"), JobState.SCIENTIFIC_FAILED)
            self.assertIs(store.lifecycle.state_for("phase-b"), JobState.SKIPPED)
            self.assertTrue(store.lifecycle.complete)

    def test_infrastructure_failure_stops_and_retries_same_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self._store(Path(directory))
            outcomes = {
                "phase-a": [
                    StudyJobOutcome(
                        kind=JobOutcomeKind.INFRASTRUCTURE_FAILURE,
                        message="worker terminated",
                    ),
                    StudyJobOutcome(kind=JobOutcomeKind.COMPLETED),
                ]
            }
            scheduler = StudyScheduler(store=store, executors=self._registry(outcomes))
            first = scheduler.run_ready()
            self.assertEqual([item.job_id for item in first], ["phase-a"])
            self.assertIs(
                store.lifecycle.state_for("phase-a"),
                JobState.INFRASTRUCTURE_FAILED,
            )
            self.assertEqual(store.lifecycle.attempts_for("phase-a"), 1)

            store.retry_job("phase-a")
            second = scheduler.run_ready()
            self.assertEqual(
                [item.job_id for item in second],
                ["phase-a", "phase-b", "validate", "analyze", "export"],
            )
            self.assertEqual(store.lifecycle.attempts_for("phase-a"), 2)
            self.assertTrue(store.lifecycle.complete)

    def test_unexpected_executor_exception_is_recorded_as_infrastructure_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self._store(Path(directory))
            registry = StudyExecutorRegistry([_CrashingExecutor()])
            scheduler = StudyScheduler(store=store, executors=registry)
            with self.assertRaisesRegex(StudyExecutorCrashed, "simulated worker crash"):
                scheduler.run_job("phase-a")
            self.assertIs(
                store.lifecycle.state_for("phase-a"),
                JobState.INFRASTRUCTURE_FAILED,
            )
            self.assertEqual(store.lifecycle.attempts_for("phase-a"), 1)

    def test_missing_executor_does_not_start_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self._store(Path(directory))
            scheduler = StudyScheduler(
                store=store,
                executors=StudyExecutorRegistry(),
            )
            with self.assertRaisesRegex(RuntimeError, "no study executor registered"):
                scheduler.run_job("phase-a")
            self.assertIs(store.lifecycle.state_for("phase-a"), JobState.PENDING)
            self.assertEqual(store.lifecycle.attempts_for("phase-a"), 0)

    def test_duplicate_executor_registration_rejected(self) -> None:
        first = _FakeExecutor("phase-a-training", {})
        second = _FakeExecutor("phase-a-training", {})
        registry = StudyExecutorRegistry([first])
        with self.assertRaisesRegex(ValueError, "duplicate study executor"):
            registry.register(second)

    def test_failure_outcomes_require_explicit_message(self) -> None:
        with self.assertRaisesRegex(ValueError, "failure outcomes require"):
            StudyJobOutcome(kind=JobOutcomeKind.SCIENTIFIC_FAILURE)
        with self.assertRaisesRegex(ValueError, "failure outcomes require"):
            StudyJobOutcome(kind=JobOutcomeKind.INFRASTRUCTURE_FAILURE)


if __name__ == "__main__":
    unittest.main()
