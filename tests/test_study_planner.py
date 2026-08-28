from __future__ import annotations

import unittest

from resilient_agents.study import (
    EvidenceClass,
    StudyPlanner,
    StudyRecipe,
    StudyStage,
)


class StudyPlannerTests(unittest.TestCase):
    def _recipe(self) -> StudyRecipe:
        return StudyRecipe(
            recipe_id="protocol-v2-test-study",
            protocol_version="protocol-v2.0-candidate",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="planner-test",
            frozen=False,
            study={
                "matrix_schema_version": 1,
                "phase_a": {
                    "methods": [
                        {
                            "method_id": "q_learning",
                            "configuration_id": "q-main",
                            "role": "core",
                            "phase_b_condition_ids": ["remap-swap", "action-failure"],
                        },
                        {
                            "method_id": "dyna_q",
                            "configuration_id": "dq-ablation",
                            "role": "ablation",
                            "phase_b_condition_ids": ["remap-swap"],
                        },
                    ],
                    "references": [
                        {
                            "reference_id": "random",
                            "role": "calibration-floor",
                        }
                    ],
                    "roots": [
                        {"root_id": "root-01", "seed_family": 101},
                        {"root_id": "root-02", "seed_family": 102},
                    ],
                    "layouts": [
                        {"layout_id": "layout-a", "family": "final"},
                        {"layout_id": "layout-b", "family": "final"},
                    ],
                },
                "phase_b": {
                    "conditions": [
                        {
                            "condition_id": "remap-swap",
                            "family": "action-remap",
                            "specification": {"mapping_id": "swap-right-down"},
                        },
                        {
                            "condition_id": "action-failure",
                            "family": "action-failure",
                            "specification": {"probability": 0.15},
                        },
                    ],
                    "branches": ["FN", "FD", "AN", "AD"],
                },
                "postprocessing": {
                    "validation": {"validator": "protocol-v2-study"},
                    "analysis": {"analysis_recipe": "root-level-did"},
                    "exports": {"package": "thesis-evidence"},
                },
            },
        )

    def test_materializes_full_matrix_with_method_specific_condition_eligibility(self) -> None:
        planner = StudyPlanner(self._recipe())
        plan = planner.materialize()
        preview = planner.preview()

        # Two learning methods x two roots x two layouts plus one cheap reference
        # over the same roots/layouts.
        self.assertEqual(preview.phase_a_jobs, 12)
        # Q-Learning: 2 conditions x 4 branches x 2 roots x 2 layouts = 32.
        # Dyna-Q ablation: 1 condition x 4 branches x 2 roots x 2 layouts = 16.
        self.assertEqual(preview.phase_b_jobs, 48)
        self.assertEqual(preview.total_jobs, 63)
        self.assertEqual(preview.method_count, 2)
        self.assertEqual(preview.reference_count, 1)
        self.assertEqual(preview.root_count, 2)
        self.assertEqual(preview.layout_count, 2)
        self.assertEqual(preview.condition_count, 2)

        self.assertEqual(len(plan.jobs_for_stage(StudyStage.VALIDATION)), 1)
        self.assertEqual(len(plan.jobs_for_stage(StudyStage.ANALYSIS)), 1)
        self.assertEqual(len(plan.jobs_for_stage(StudyStage.EXPORT)), 1)
        self.assertNotIn(
            "pb__dyna_q__root-01__layout-a__action-failure__fd",
            plan.by_id(),
        )

    def test_phase_b_job_depends_on_exact_matching_phase_a_checkpoint_producer(self) -> None:
        plan = StudyPlanner(self._recipe()).materialize()
        job = plan.by_id()[
            "pb__q_learning__root-02__layout-b__remap-swap__ad"
        ]
        self.assertEqual(
            job.dependencies,
            ("pa__q_learning__root-02__layout-b",),
        )
        self.assertEqual(
            job.payload["phase_a_job_id"],
            "pa__q_learning__root-02__layout-b",
        )
        self.assertEqual(job.payload["branch"], "AD")

    def test_validation_is_stage_barrier_based_so_scientific_failures_can_be_counted(self) -> None:
        plan = StudyPlanner(self._recipe()).materialize()
        validation = plan.by_id()["validate-study"]
        analysis = plan.by_id()["analyze-study"]
        export = plan.by_id()["export-study"]
        self.assertEqual(validation.dependencies, ())
        self.assertEqual(analysis.dependencies, ("validate-study",))
        self.assertEqual(export.dependencies, ("analyze-study",))

    def test_materialization_is_deterministic(self) -> None:
        first = StudyPlanner(self._recipe()).materialize()
        second = StudyPlanner(self._recipe()).materialize()
        self.assertEqual(first, second)
        self.assertEqual(
            [job.job_id for job in first.jobs],
            [job.job_id for job in second.jobs],
        )

    def test_requires_exact_protocol_v2_branch_order(self) -> None:
        payload = self._recipe().to_dict()
        payload["study"]["phase_b"]["branches"] = ["FN", "AN", "FD", "AD"]
        recipe = StudyRecipe.from_dict(payload)
        with self.assertRaisesRegex(ValueError, "exactly match"):
            StudyPlanner(recipe)

    def test_rejects_unknown_condition_eligibility(self) -> None:
        payload = self._recipe().to_dict()
        payload["study"]["phase_a"]["methods"][0]["phase_b_condition_ids"] = [
            "missing-condition"
        ]
        recipe = StudyRecipe.from_dict(payload)
        with self.assertRaisesRegex(ValueError, "unknown Phase-B conditions"):
            StudyPlanner(recipe)

    def test_rejects_reserved_identifier_delimiter(self) -> None:
        payload = self._recipe().to_dict()
        payload["study"]["phase_a"]["roots"][0]["root_id"] = "root__01"
        recipe = StudyRecipe.from_dict(payload)
        with self.assertRaisesRegex(ValueError, "reserved '__' delimiter"):
            StudyPlanner(recipe)


if __name__ == "__main__":
    unittest.main()
