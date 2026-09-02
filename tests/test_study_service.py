from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.study import (
    EvidenceClass,
    JobOutcomeKind,
    StudyExecutorRegistry,
    StudyExecutionIdentity,
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
                "phase-b-matched-set",
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
            self.assertEqual(preview.preview.phase_b_jobs, 1)
            self.assertEqual(preview.preview.total_jobs, 5)
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
            self.assertEqual(len(results), 5)
            pre_finalize = service.status("service-study")
            self.assertEqual(pre_finalize.progress["completed"], 5)
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

    def test_replacement_execution_keeps_recipe_plan_and_predecessor_immutable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service = StudyService(
                repo_root=root,
                writable_root=root,
                executors=self._executors(),
            )
            recipe = self._recipe()
            original = service.create(recipe)
            original_manifest = (
                root / "results/studies/service-study/manifest.json"
            ).read_bytes()
            original_plan = (
                root / "results/studies/service-study/plan.json"
            ).read_bytes()

            replacement_id = "service-study--recovery-01"
            identity = StudyExecutionIdentity.replacement(
                execution_instance_id=replacement_id,
                scientific_recipe_id=recipe.recipe_id,
                predecessor_execution_instance_id=original.study_id,
                recovery_decision_id="DEC-062",
            )
            replacement = service.create(recipe, execution_identity=identity)

            self.assertEqual(replacement.study_id, replacement_id)
            self.assertEqual(replacement.recipe_sha256, original.recipe_sha256)
            replacement_dir = root / "results/studies" / replacement_id
            self.assertEqual(
                (replacement_dir / "plan.json").read_bytes(), original_plan
            )
            manifest = json.loads(
                (replacement_dir / "manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                manifest["execution_identity"],
                {
                    "execution_instance_id": replacement_id,
                    "kind": "replacement",
                    "predecessor_execution_instance_id": "service-study",
                    "recovery_decision_id": "DEC-062",
                    "schema_version": 1,
                    "scientific_recipe_id": "service-study",
                    "scientific_recipe_sha256": recipe.sha256(),
                    "source_git_commit": manifest["source"]["git_commit"],
                },
            )
            self.assertEqual(
                (root / "results/studies/service-study/manifest.json").read_bytes(),
                original_manifest,
            )
            self.assertEqual(
                service.status(replacement_id).ready_job_ids,
                ("pa__q_learning__root-01__layout-a",),
            )
            self.assertEqual(len(service.run_ready(replacement_id)), 5)
            self.assertTrue(service.finalize(replacement_id).finalized)
            self.assertEqual(
                (root / "results/studies/service-study/manifest.json").read_bytes(),
                original_manifest,
            )


if __name__ == "__main__":
    unittest.main()
