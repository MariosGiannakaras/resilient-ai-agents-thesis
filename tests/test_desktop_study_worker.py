from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.study_worker import run_development_study
from resilient_agents.study import (
    EvidenceClass,
    StudyJobSpec,
    StudyPlan,
    StudyRecipe,
    StudyStage,
    StudyStore,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _recipe(study_id: str) -> StudyRecipe:
    return StudyRecipe(
        recipe_id=study_id,
        protocol_version="protocol-v2.0-development",
        evidence_class=EvidenceClass.DEVELOPMENT,
        scientific_status="non-final-development-worker-test",
        frozen=False,
        study={"purpose": "worker-control-test"},
    )


def _job() -> StudyJobSpec:
    return StudyJobSpec(
        job_id="manual-job",
        stage=StudyStage.PHASE_A,
        evidence_class=EvidenceClass.DEVELOPMENT,
        payload={"job_type": "test-only-manual-job"},
    )


class DesktopStudyWorkerTests(unittest.TestCase):
    def test_worker_finalizes_already_resolved_development_lifecycle_without_executing_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            recipe = _recipe("t528-dev-worker-finalize")
            job = _job()
            store = StudyStore.create(
                repo_root=REPO_ROOT,
                writable_root=writable,
                recipe=recipe,
                plan=StudyPlan(study_id=recipe.recipe_id, jobs=(job,)),
            )
            store.start_job(job.job_id)
            store.complete_job(job.job_id)

            summary = run_development_study(
                repo_root=REPO_ROOT,
                writable_root=writable,
                study_id=recipe.recipe_id,
            )
            self.assertEqual(summary["executed_jobs"], 0)
            self.assertTrue(summary["finalized"])
            self.assertEqual(summary["status"], "completed")
            self.assertFalse((writable / "results" / "runs").exists())

    def test_worker_requires_explicit_retry_for_infrastructure_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            recipe = _recipe("t528-dev-worker-infra")
            job = _job()
            store = StudyStore.create(
                repo_root=REPO_ROOT,
                writable_root=writable,
                recipe=recipe,
                plan=StudyPlan(study_id=recipe.recipe_id, jobs=(job,)),
            )
            store.start_job(job.job_id)
            store.fail_job_infrastructure(job.job_id, reason="test infrastructure failure")

            with self.assertRaisesRegex(RuntimeError, "explicit retry action"):
                run_development_study(
                    repo_root=REPO_ROOT,
                    writable_root=writable,
                    study_id=recipe.recipe_id,
                )


if __name__ == "__main__":
    unittest.main()
