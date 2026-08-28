from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.study import (
    EvidenceClass,
    JobOutcomeKind,
    StudyExecutorRegistry,
    StudyJobContext,
    StudyJobOutcome,
    StudyJobSpec,
    StudyRecipe,
    StudyService,
)


class _SuccessExecutor:
    def __init__(self, job_type: str) -> None:
        self.job_type = job_type

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        return StudyJobOutcome(kind=JobOutcomeKind.COMPLETED)


class StudyServiceTests(unittest.TestCase):
    def _recipe(self) -> StudyRecipe:
        return StudyRecipe(
            recipe_id="service-study",
            protocol_version="protocol-v2.0-candidate",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="service-test",
            frozen=False,
            study={
                "matrix_schema_version": 2,
                "phase_a": {
                    "execution": {
                        "training_interaction_budget": 32,
                        "probe_interaction_indices": [0, 32],
                        "episodes_per_probe": 1,
                        "task": {
                            "gamma": 0.95,
                            "reward_contract": {"step": -0.1, "goal": 1.0},
                            "administrative_truncation": True,
                            "bootstrap_on_truncation": True,
                        },
                    },
                    "methods": [
                        {
                            "method_id": "q_learning",
                            "configuration_id": "q-test",
                            "role": "core",
                            "phase_b_condition_ids": ["remap"],
                        }
                    ],
                    "references": [],
                    "roots": [{"root_id": "root-01"}],
                    "layouts": [{"layout_id": "layout-a"}],
                },
                "phase_b": {
                    "execution": {
                        "interaction_budget_per_branch": 8,
                        "prefix_interactions": 2,
                    },
                    "conditions": [
                        {
                            "condition_id": "remap",
                            "family": "action-remap",
                        }
                    ],
                    "branches": ["FN", "FD", "AN", "AD"],
                },
                "postprocessing": {
                    "validation": {"kind": "test"},
                    "analysis": {"kind": "test"},
                    "exports": {"kind": "test"},
                },
            },
        )

    def _executors(self) -> StudyExecutorRegistry:
        return StudyExecutorRegistry(
            _SuccessExecutor(job_type)
            for job_type in (
                "phase-a-training",
                "phase-b-branch",
                "study-validation",
                "study-analysis",
                "study-export",
            )
        )

    def test_preview_is_recipe_derived_and_does_not_create_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service = StudyService(repo_root=root, writable_root=root)
            preview = service.preview(self._recipe())
            self.assertEqual(preview.study_id, "service-study")
            self.assertEqual(preview.preview.phase_a_jobs, 1)
            self.assertEqual(preview.preview.phase_b_jobs, 4)
            self.assertEqual(preview.preview.total_jobs, 8)
            self.assertFalse((root / "results" / "studies").exists())

    def test_create_status_restart_and_list_are_durable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = StudyService(repo_root=root, writable_root=root)
            created = first.create(self._recipe())
            self.assertEqual(created.current_stage, "phase-a")
            self.assertEqual(created.ready_job_ids, ("pa__q_learning__root-01__layout-a",))

            restarted = StudyService(repo_root=root, writable_root=root)
            status = restarted.status("service-study")
            self.assertEqual(status.recipe_sha256, created.recipe_sha256)
            self.assertEqual(status.progress, created.progress)
            self.assertEqual([item.study_id for item in restarted.list_studies()], ["service-study"])

    def test_run_complete_study_and_finalize_through_facade(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service = StudyService(
                repo_root=root,
                writable_root=root,
                executors=self._executors(),
            )
            service.create(self._recipe())
            results = service.run_ready("service-study")
            self.assertEqual(len(results), 8)
            pre_finalize = service.status("service-study")
            self.assertEqual(pre_finalize.progress["completed"], 8)
            self.assertFalse(pre_finalize.finalized)

            finalized = service.finalize("service-study")
            self.assertTrue(finalized.finalized)
            self.assertEqual(finalized.status, "completed")
            self.assertEqual(finalized.current_stage, None)
            self.assertEqual(finalized.ready_job_ids, ())

    def test_finalize_refuses_unresolved_study(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service = StudyService(repo_root=root, writable_root=root)
            service.create(self._recipe())
            with self.assertRaisesRegex(RuntimeError, "lifecycle is unresolved"):
                service.finalize("service-study")


if __name__ == "__main__":
    unittest.main()
