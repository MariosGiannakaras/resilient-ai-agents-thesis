from __future__ import annotations

import hashlib
import math
import tempfile
import unittest
from pathlib import Path

from resilient_agents.study import (
    ArtifactRole,
    EvidenceClass,
    JobState,
    StudyArtifact,
    StudyJobSpec,
    StudyLifecycle,
    StudyPlan,
    StudyRecipe,
    StudyStage,
    StudyStore,
)


class StudyBackendTests(unittest.TestCase):
    def _recipe(
        self,
        *,
        recipe_id: str = "study-001",
        evidence_class: EvidenceClass = EvidenceClass.DEVELOPMENT,
        frozen: bool = False,
    ) -> StudyRecipe:
        return StudyRecipe(
            recipe_id=recipe_id,
            protocol_version="protocol-v2.0-candidate",
            evidence_class=evidence_class,
            scientific_status="test-only",
            frozen=frozen,
            study={
                "methods": ["q_learning", "ppo"],
                "roots": ["root-01"],
                "layouts": ["layout-a"],
            },
        )

    def _plan(self, study_id: str = "study-001") -> StudyPlan:
        return StudyPlan(
            study_id=study_id,
            jobs=(
                StudyJobSpec(
                    job_id="pa-q-root01-layouta",
                    stage=StudyStage.PHASE_A,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    payload={"method_id": "q_learning"},
                ),
                StudyJobSpec(
                    job_id="pb-q-root01-layouta-fd",
                    stage=StudyStage.PHASE_B,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    dependencies=("pa-q-root01-layouta",),
                    payload={"branch": "fd"},
                ),
                StudyJobSpec(
                    job_id="validate-study",
                    stage=StudyStage.VALIDATION,
                    evidence_class=EvidenceClass.DERIVED,
                    payload={"validation": "matrix-integrity"},
                ),
            ),
        )

    def test_confirmatory_recipe_must_be_frozen_and_hash_is_deterministic(self) -> None:
        with self.assertRaisesRegex(ValueError, "confirmatory recipes must be frozen"):
            self._recipe(
                evidence_class=EvidenceClass.CONFIRMATORY,
                frozen=False,
            )

        first = StudyRecipe(
            recipe_id="final-study",
            protocol_version="protocol-v2.0",
            evidence_class=EvidenceClass.CONFIRMATORY,
            scientific_status="frozen-final",
            frozen=True,
            study={"b": 2, "a": {"y": 4, "x": 3}},
        )
        second = StudyRecipe(
            recipe_id="final-study",
            protocol_version="protocol-v2.0",
            evidence_class=EvidenceClass.CONFIRMATORY,
            scientific_status="frozen-final",
            frozen=True,
            study={"a": {"x": 3, "y": 4}, "b": 2},
        )
        self.assertEqual(first.sha256(), second.sha256())
        self.assertEqual(first.to_dict(), second.to_dict())

    def test_recipe_rejects_nonfinite_and_derived_launches(self) -> None:
        with self.assertRaisesRegex(ValueError, "strict JSON-compatible"):
            StudyRecipe(
                recipe_id="bad-nan",
                protocol_version="protocol-v2.0-candidate",
                evidence_class=EvidenceClass.DEVELOPMENT,
                scientific_status="invalid",
                frozen=False,
                study={"value": math.nan},
            )
        with self.assertRaisesRegex(ValueError, "cannot be launched"):
            self._recipe(evidence_class=EvidenceClass.DERIVED)

    def test_plan_rejects_later_stage_dependency_and_cycles(self) -> None:
        with self.assertRaisesRegex(ValueError, "later-stage"):
            StudyPlan(
                study_id="later-dependency",
                jobs=(
                    StudyJobSpec(
                        job_id="analysis",
                        stage=StudyStage.ANALYSIS,
                        evidence_class=EvidenceClass.DERIVED,
                    ),
                    StudyJobSpec(
                        job_id="phase-a",
                        stage=StudyStage.PHASE_A,
                        evidence_class=EvidenceClass.CONFIRMATORY,
                        dependencies=("analysis",),
                    ),
                ),
            )

        with self.assertRaisesRegex(ValueError, "cycle"):
            StudyPlan(
                study_id="cycle-study",
                jobs=(
                    StudyJobSpec(
                        job_id="a",
                        stage=StudyStage.PHASE_A,
                        evidence_class=EvidenceClass.DEVELOPMENT,
                        dependencies=("b",),
                    ),
                    StudyJobSpec(
                        job_id="b",
                        stage=StudyStage.PHASE_A,
                        evidence_class=EvidenceClass.DEVELOPMENT,
                        dependencies=("a",),
                    ),
                ),
            )

    def test_stage_barrier_waits_for_every_earlier_stage_job(self) -> None:
        plan = StudyPlan(
            study_id="barrier-study",
            jobs=(
                StudyJobSpec(
                    job_id="pa-a",
                    stage=StudyStage.PHASE_A,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                ),
                StudyJobSpec(
                    job_id="pa-b",
                    stage=StudyStage.PHASE_A,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                ),
                StudyJobSpec(
                    job_id="pb-a",
                    stage=StudyStage.PHASE_B,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    dependencies=("pa-a",),
                ),
            ),
        )
        lifecycle = StudyLifecycle(plan)
        self.assertEqual(
            {job.job_id for job in lifecycle.ready_jobs()},
            {"pa-a", "pa-b"},
        )
        lifecycle.start("pa-a")
        lifecycle.complete_job("pa-a")
        self.assertEqual(
            {job.job_id for job in lifecycle.ready_jobs()},
            {"pa-b"},
        )
        lifecycle.start("pa-b")
        lifecycle.complete_job("pa-b")
        self.assertEqual(
            [job.job_id for job in lifecycle.ready_jobs()],
            ["pb-a"],
        )

    def test_scientific_failure_is_retained_and_dependent_job_is_skipped(self) -> None:
        lifecycle = StudyLifecycle(self._plan())
        lifecycle.start("pa-q-root01-layouta")
        lifecycle.fail_scientifically("pa-q-root01-layouta")

        self.assertIs(
            lifecycle.state_for("pa-q-root01-layouta"),
            JobState.SCIENTIFIC_FAILED,
        )
        self.assertIs(
            lifecycle.state_for("pb-q-root01-layouta-fd"),
            JobState.SKIPPED,
        )
        self.assertEqual(
            [job.job_id for job in lifecycle.ready_jobs()],
            ["validate-study"],
        )

    def test_infrastructure_failure_is_retryable_under_same_job_identity(self) -> None:
        lifecycle = StudyLifecycle(self._plan())
        lifecycle.start("pa-q-root01-layouta")
        lifecycle.fail_infrastructure("pa-q-root01-layouta")
        self.assertEqual(lifecycle.attempts_for("pa-q-root01-layouta"), 1)
        self.assertEqual(lifecycle.ready_jobs(), ())

        lifecycle.retry_infrastructure_failure("pa-q-root01-layouta")
        lifecycle.start("pa-q-root01-layouta")
        self.assertEqual(lifecycle.attempts_for("pa-q-root01-layouta"), 2)
        lifecycle.complete_job("pa-q-root01-layouta")

    def test_lifecycle_snapshot_restore_roundtrip(self) -> None:
        plan = self._plan()
        lifecycle = StudyLifecycle(plan)
        lifecycle.start("pa-q-root01-layouta")
        lifecycle.complete_job("pa-q-root01-layouta")
        snapshot = lifecycle.snapshot()
        restored = StudyLifecycle.restore(
            plan,
            states=snapshot["states"],
            attempts=snapshot["attempts"],
        )
        self.assertEqual(restored.snapshot(), snapshot)
        self.assertEqual(
            [job.job_id for job in restored.ready_jobs()],
            ["pb-q-root01-layouta-fd"],
        )

    def test_store_create_load_artifact_lineage_and_finalize(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = self._recipe()
            plan = self._plan()
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=recipe,
                plan=plan,
            )
            reloaded = StudyStore.load(
                repo_root=root,
                writable_root=root,
                study_id=plan.study_id,
            )
            self.assertEqual(reloaded.recipe.sha256(), recipe.sha256())
            self.assertEqual(reloaded.lifecycle.progress()["pending"], 3)

            store.start_job("pa-q-root01-layouta")
            artifact_path = root / "results" / "runs" / "run-01" / "summary.json"
            artifact_path.parent.mkdir(parents=True)
            artifact_path.write_text('{"status":"completed"}\n', encoding="utf-8")
            digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            store.record_artifact(
                StudyArtifact(
                    artifact_id="run-01-summary",
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path="results/runs/run-01/summary.json",
                    sha256=digest,
                    source_job_ids=("pa-q-root01-layouta",),
                )
            )
            store.complete_job("pa-q-root01-layouta")
            store.start_job("pb-q-root01-layouta-fd")
            store.complete_job("pb-q-root01-layouta-fd")
            store.start_job("validate-study")
            store.complete_job("validate-study")
            store.finalize()

            finalized = StudyStore.load(
                repo_root=root,
                writable_root=root,
                study_id=plan.study_id,
            )
            self.assertTrue(finalized.lifecycle.complete)
            self.assertEqual(len(finalized.artifacts()), 1)
            with self.assertRaisesRegex(RuntimeError, "immutable"):
                finalized.retry_job("pa-q-root01-layouta")

    def test_store_rejects_tampered_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=self._recipe(),
                plan=self._plan(),
            )
            store.start_job("pa-q-root01-layouta")
            artifact_path = root / "results" / "runs" / "run-01" / "checkpoint.bin"
            artifact_path.parent.mkdir(parents=True)
            artifact_path.write_bytes(b"original")
            store.record_artifact(
                StudyArtifact(
                    artifact_id="checkpoint-01",
                    role=ArtifactRole.SCIENTIFIC_CHECKPOINT,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path="results/runs/run-01/checkpoint.bin",
                    sha256=hashlib.sha256(b"original").hexdigest(),
                    source_job_ids=("pa-q-root01-layouta",),
                )
            )
            artifact_path.write_bytes(b"tampered")
            with self.assertRaisesRegex(RuntimeError, "artifact file/hash"):
                StudyStore.load(
                    repo_root=root,
                    writable_root=root,
                    study_id="study-001",
                )

    def test_finalized_store_rejects_tampered_internal_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=self._recipe(),
                plan=self._plan(),
            )
            store.start_job("pa-q-root01-layouta")
            store.complete_job("pa-q-root01-layouta")
            store.start_job("pb-q-root01-layouta-fd")
            store.complete_job("pb-q-root01-layouta-fd")
            store.start_job("validate-study")
            store.complete_job("validate-study")
            store.finalize()

            events = root / "results" / "studies" / "study-001" / "events.jsonl"
            events.write_text(events.read_text(encoding="utf-8") + "{}\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "finalized study file"):
                StudyStore.load(
                    repo_root=root,
                    writable_root=root,
                    study_id="study-001",
                )


if __name__ == "__main__":
    unittest.main()
