from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.gridworld import ResolvedGridWorldScenario
from resilient_agents.protocol_v2_feasibility import (
    CORE_METHOD_IDS,
    _scenario,
    load_plan,
    summarize_level,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = REPO_ROOT / "configs" / "protocols" / "protocol-v2-feasibility-v0.1.json"


class ProtocolV2FeasibilityPlanTests(unittest.TestCase):
    def test_committed_plan_is_nonfinal_ordered_and_all_layouts_are_valid(self):
        plan = load_plan(PLAN_PATH)
        self.assertFalse(plan["final_reserve_access"])
        self.assertEqual(
            tuple(sorted(plan["provisional_method_configs"])),
            tuple(sorted(CORE_METHOD_IDS)),
        )
        self.assertEqual(
            [item["selection_order"] for item in plan["ordered_gridworld_ladder"]],
            [1, 2, 3],
        )
        for level in plan["ordered_gridworld_ladder"]:
            for layout in level["layouts"]:
                resolved = ResolvedGridWorldScenario.from_spec(_scenario(plan, layout))
                self.assertEqual(resolved.max_steps, layout["max_steps"])
                self.assertGreaterEqual(layout["max_steps"], 4 * layout["shortest_path_length"])

    def test_probe_grid_aligns_with_ppo_quantum(self):
        plan = load_plan(PLAN_PATH)
        quantum = int(plan["provisional_method_configs"]["ppo"]["n_steps"])
        self.assertTrue(
            all(index % quantum == 0 for index in plan["phase_a"]["probe_interaction_indices"])
        )

    def _records(self, *, early: float, final: float):
        plan = load_plan(PLAN_PATH)
        level = plan["ordered_gridworld_ladder"][0]
        records = []
        for layout in level["layouts"]:
            for root in plan["roots"]:
                for method in CORE_METHOD_IDS:
                    records.append(
                        {
                            "status": "completed",
                            "level_id": level["level_id"],
                            "layout_id": layout["layout_id"],
                            "root_id": root["root_id"],
                            "method_id": method,
                            "wall_seconds": 1.0,
                            "process_cpu_seconds": 0.5,
                            "checkpoint_bytes": 100,
                            "probes": [
                                {"interaction_index": 0, "metrics": {"terminated_rate": 0.0}},
                                {"interaction_index": 512, "metrics": {"terminated_rate": early}},
                                {"interaction_index": 1024, "metrics": {"terminated_rate": early}},
                                {"interaction_index": 2048, "metrics": {"terminated_rate": final}},
                            ],
                        }
                    )
        return plan, level, records

    def test_selection_rule_rejects_universal_early_ceiling(self):
        plan, level, records = self._records(early=0.95, final=1.0)
        summary = summarize_level(plan, level["level_id"], records)
        self.assertTrue(summary["universal_early_ceiling"])
        self.assertFalse(summary["selected"])

    def test_selection_rule_rejects_universal_floor(self):
        plan, level, records = self._records(early=0.0, final=0.05)
        summary = summarize_level(plan, level["level_id"], records)
        self.assertTrue(summary["universal_floor"])
        self.assertFalse(summary["selected"])

    def test_selection_rule_accepts_non_degenerate_level_without_ranking_methods(self):
        plan, level, records = self._records(early=0.25, final=0.65)
        summary = summarize_level(plan, level["level_id"], records)
        self.assertFalse(summary["universal_floor"])
        self.assertFalse(summary["universal_early_ceiling"])
        self.assertTrue(summary["selected"])

    def test_plan_rejects_final_reserve_access(self):
        payload = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        payload["final_reserve_access"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "final-reserve"):
                load_plan(path)


if __name__ == "__main__":
    unittest.main()
