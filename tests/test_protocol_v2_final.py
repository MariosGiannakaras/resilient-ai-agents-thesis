import unittest
import json
from pathlib import Path

class TestProtocolV2Final(unittest.TestCase):
    def setUp(self):
        self.config_path = Path("configs/protocols/protocol-v2.0-final.json")
        self.assertTrue(self.config_path.exists(), "Final configuration file must exist")
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))

    def test_schema_and_decision_id(self):
        self.assertEqual(self.config.get("schema_version"), 1)
        self.assertEqual(self.config.get("decision_id"), "DEC-058")
        self.assertEqual(self.config.get("scientific_status"), "final-frozen-scientific-authority")

    def test_final_reserve_access_firewall(self):
        # The most important regression check: firewall must be False
        self.assertIs(self.config.get("final_reserve_access"), False)
        self.assertEqual(self.config.get("execution_authorization"), "requires-explicit-t610-gate")

    def test_retained_methods(self):
        methods = self.config.get("retained_methods", [])
        self.assertEqual(len(methods), 5)
        self.assertCountEqual(methods, ["q_learning", "sarsa", "dqn", "ppo", "dyna_q_plus"])
        configs = self.config.get("selected_configs", {})
        self.assertEqual(len(configs), 5)

    def test_final_layouts(self):
        layouts = self.config.get("final_layouts", [])
        self.assertEqual(len(layouts), 2)
        for layout in layouts:
            self.assertEqual(layout["width"], 7)
            self.assertEqual(layout["height"], 7)
            self.assertIn("gw-l1-final", layout["layout_id"])
            self.assertEqual(layout["shortest_path_length"], 12)

    def test_final_roots_and_no_control_chars(self):
        roots = self.config.get("final_roots", [])
        self.assertEqual(len(roots), 12)
        for root in roots:
            root_id = root["root_id"]
            self.assertIn("t527-final-r", root_id)
            # Ensure no control characters
            self.assertTrue(all(ord(c) >= 32 for c in root_id))
            self.assertEqual(root["initialization_seed"] // 1000, 71)

    def test_conditions(self):
        conditions = self.config.get("phase_b", {}).get("conditions", [])
        self.assertEqual(len(conditions), 4)
        c_ids = [c["condition_id"] for c in conditions]
        self.assertCountEqual(c_ids, [
            "action-remap-swap-right-down",
            "action-remap-cycle-clockwise",
            "action-failure-0.15",
            "observation-corruption-0.05"
        ])
        for cid in c_ids:
            self.assertTrue(all(ord(c) >= 32 for c in cid))

    def test_horizon_and_budget(self):
        self.assertEqual(self.config.get("phase_b", {}).get("horizon"), 256)
        self.assertEqual(self.config.get("phase_a", {}).get("training_interaction_budget"), 8192)
        self.assertEqual(self.config.get("phase_b", {}).get("common_nominal_no_learning_prefix_interactions"), 1)

    def test_exact_denominators(self):
        sc = self.config.get("statistical_contract", {})
        self.assertEqual(sc.get("expected_phase_a_units"), 120)
        self.assertEqual(sc.get("expected_phase_a_training_interactions"), 983040)
        self.assertEqual(sc.get("expected_phase_b_matched_sets"), 480)
        self.assertEqual(sc.get("expected_phase_b_branches"), 1920)
        self.assertEqual(sc.get("expected_phase_b_prefix_interactions"), 480)
        self.assertEqual(sc.get("expected_phase_b_post_boundary_interactions"), 491520)

if __name__ == "__main__":
    unittest.main()
