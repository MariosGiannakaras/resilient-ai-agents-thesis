from __future__ import annotations

import json
import unittest
from pathlib import Path

from resilient_agents.study import EvidenceClass, StudyPlanner
from resilient_agents.study.protocol_v2_1_recipe import load_protocol_v21_final_recipe


ROOT = Path(__file__).resolve().parents[1]
V20 = ROOT / "configs" / "protocols" / "protocol-v2.0-final.json"
V21 = ROOT / "configs" / "protocols" / "protocol-v2.1-final.json"


class ProtocolV21FinalRecipeTests(unittest.TestCase):
    def _authority(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_v21_preserves_dec058_experimental_choices(self) -> None:
        old = self._authority(V20)
        new = self._authority(V21)
        self.assertFalse(new["final_reserve_access"])
        self.assertEqual(new["execution_authorization"], "requires-explicit-t610-gate")
        self.assertEqual(new["final_layouts"], old["final_layouts"])
        self.assertEqual(new["final_roots"], old["final_roots"])
        self.assertEqual(new["retained_methods"], old["retained_methods"])
        self.assertEqual(new["selected_configs"], old["selected_configs"])
        self.assertEqual(new["phase_a"], old["phase_a"])
        self.assertEqual(new["phase_a"]["deployment_start_settlement"], "DEC-054")
        for key in (
            "conditions",
            "horizon",
            "common_nominal_no_learning_prefix_interactions",
            "learning_state_reset_on_episode_boundary",
            "disturbance_retriggered_or_cleared_on_reset",
        ):
            self.assertEqual(new["phase_b"][key], old["phase_b"][key])

    def test_materialized_recipe_is_frozen_confirmatory_but_not_execution_authority(self) -> None:
        recipe = load_protocol_v21_final_recipe(ROOT)
        self.assertEqual(recipe.recipe_id, "protocol-v2.1-final")
        self.assertEqual(recipe.protocol_version, "protocol-v2.1")
        self.assertIs(recipe.evidence_class, EvidenceClass.CONFIRMATORY)
        self.assertTrue(recipe.frozen)

        authority = self._authority(V21)
        self.assertFalse(authority["final_reserve_access"])
        self.assertEqual(authority["execution_authorization"], "requires-explicit-t610-gate")

    def test_materialized_matrix_matches_frozen_dimensions(self) -> None:
        recipe = load_protocol_v21_final_recipe(ROOT)
        planner = StudyPlanner(recipe)
        preview = planner.preview()
        self.assertEqual(preview.method_count, 5)
        self.assertEqual(preview.reference_count, 0)
        self.assertEqual(preview.root_count, 12)
        self.assertEqual(preview.layout_count, 2)
        self.assertEqual(preview.condition_count, 4)
        self.assertEqual(preview.phase_a_jobs, 120)
        self.assertEqual(preview.phase_b_jobs, 480)
        self.assertEqual(preview.validation_jobs, 1)
        self.assertEqual(preview.analysis_jobs, 1)
        self.assertEqual(preview.export_jobs, 1)
        self.assertEqual(preview.total_jobs, 603)

    def test_phase_b_jobs_use_only_the_v21_temporal_execution_contract(self) -> None:
        plan = StudyPlanner(load_protocol_v21_final_recipe(ROOT)).materialize()
        job = plan.by_id()[
            "pb__ppo__t527-final-r12__gw-l1-final-b__action-remap-cycle-clockwise"
        ]
        self.assertEqual(
            set(job.payload["execution"]),
            {
                "prefix_interactions",
                "interaction_budget_per_branch",
                "episode_reset_policy_id",
                "subsequent_episode_seed_count",
                "temporal_evidence_id",
                "temporal_window_size",
            },
        )
        self.assertEqual(job.payload["execution"]["prefix_interactions"], 1)
        self.assertEqual(job.payload["execution"]["interaction_budget_per_branch"], 256)
        self.assertEqual(job.payload["execution"]["temporal_window_size"], 32)
        self.assertEqual(job.payload["branches"], ["FN", "FD", "AN", "AD"])

    def test_materialized_nominal_layout_keeps_agent_information_hidden(self) -> None:
        plan = StudyPlanner(load_protocol_v21_final_recipe(ROOT)).materialize()
        job = plan.by_id()["pa__q_learning__t527-final-r01__gw-l1-final-a"]
        scenario = job.payload["layout"]["scenario"]
        self.assertEqual(scenario["change_events"], [])
        self.assertEqual(scenario["action_disturbance_spec"]["failure_probability"], 0.0)
        self.assertEqual(
            scenario["observation_disturbance_spec"]["mislocalization_probability"],
            0.0,
        )
        self.assertEqual(
            scenario["information_policy"],
            {
                "expose_executed_action": False,
                "expose_disturbance_flags": False,
                "expose_change_indicator": False,
                "expose_regime_id": False,
                "expose_true_state": False,
            },
        )

    def test_analysis_and_export_jobs_keep_v21_identity_and_frozen_statistics(self) -> None:
        plan = StudyPlanner(load_protocol_v21_final_recipe(ROOT)).materialize()
        analysis = plan.by_id()["analyze-study"].payload["specification"]
        export = plan.by_id()["export-study"].payload["specification"]
        self.assertEqual(analysis["analysis_recipe"], "protocol-v2-root-level-v2.1")
        self.assertEqual(analysis["phase_a_metric"], "return_mean")
        self.assertEqual(analysis["phase_b_metric"], "return_sum")
        self.assertEqual(analysis["recovery"]["primary_condition_family"], "action-remap")
        self.assertEqual(analysis["recovery"]["tolerance"], 0.1)
        self.assertEqual(analysis["recovery"]["sensitivity_tolerances"], [0.05, 0.2])
        self.assertEqual(analysis["recovery"]["stability_windows"], 2)
        self.assertEqual(analysis["interval"]["confidence"], 0.95)
        self.assertEqual(analysis["interval"]["critical_value_by_n"]["12"], 2.201)
        self.assertEqual(export, {"package": "protocol-v2-evidence-handoff-v2", "emit_csv": True})


if __name__ == "__main__":
    unittest.main()
