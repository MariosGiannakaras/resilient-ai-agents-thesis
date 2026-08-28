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
                "matrix_schema_version": 2,
                "phase_a": {
                    "execution": {
                        "training_interaction_budget": 128,
                        "probe_interaction_indices": [0, 64, 128],
                        "episodes_per_probe": 2,
                        "task": {
                            "gamma": 0.95,
                            "reward_contract": {
                                "step": -0.1,
                                "collision": -0.25,
                                "goal": 1.0,
                            },
                            "administrative_truncation": True,
                            "bootstrap_on_truncation": True,
                        },
                    },
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
                    "execution": {
                        "interaction_budget_per_branch": 32,
                        "prefix_interactions": 8,
                    },
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

        self.assertEqual(preview.phase_a_jobs, 12)
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

    def test_execution_contract_is_copied_into_scientific_job_payloads(self) -> None:
        plan = StudyPlanner(self._recipe()).materialize()
        phase_a = plan.by_id()["pa__q_learning__root-01__layout-a"]
        phase_b = plan.by_id()[
            "pb__q_learning__root-01__layout-a__remap-swap__fn"
        ]
        self.assertEqual(phase_a.payload["execution"]["training_interaction_budget"], 128)
        self.assertEqual(phase_a.payload["execution"]["task"]["gamma"], 0.95)
        self.assertEqual(phase_b.payload["execution"]["interaction_budget_per_branch"], 32)
        self.assertEqual(phase_b.payload["execution"]["prefix_interactions"], 8)

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

    def test_requires_explicit_phase_execution_objects(self) -> None:
        payload = self._recipe().to_dict()
        del payload["study"]["phase_a"]["execution"]
        recipe = StudyRecipe.from_dict(payload)
        with self.assertRaisesRegex(ValueError, "study.phase_a keys mismatch"):
            StudyPlanner(recipe)


if __name__ == "__main__":
    unittest.main()
