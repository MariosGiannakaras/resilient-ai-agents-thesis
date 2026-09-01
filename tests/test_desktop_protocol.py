from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.protocol import load_frozen_protocol


REPO_ROOT = Path(__file__).resolve().parents[1]


class FrozenProtocolPresentationTests(unittest.TestCase):
    def test_current_frozen_protocol_projects_expected_read_only_summary(self) -> None:
        summary = load_frozen_protocol(REPO_ROOT)
        self.assertTrue(summary.final_execution_locked)
        self.assertFalse(summary.final_reserve_access)
        self.assertEqual(summary.decision_id, "DEC-058")
        self.assertEqual(len(summary.methods), 5)
        self.assertEqual(summary.root_count, 12)
        self.assertEqual(summary.layout_count, 2)
        self.assertEqual(summary.condition_count, 4)
        self.assertEqual(summary.phase_a_units, 120)
        self.assertEqual(summary.phase_a_training_interactions, 983_040)
        self.assertEqual(summary.phase_b_matched_sets, 480)
        self.assertEqual(summary.phase_b_branches, 1_920)
        self.assertEqual(summary.phase_b_prefix_interactions, 480)
        self.assertEqual(summary.phase_b_post_boundary_interactions, 491_520)
        self.assertEqual(summary.phase_b_horizon, 256)

    def test_t528_fails_closed_if_final_reserve_access_is_enabled(self) -> None:
        source = json.loads(
            (REPO_ROOT / "configs" / "protocols" / "protocol-v2.0-final.json").read_text(
                encoding="utf-8"
            )
        )
        source["final_reserve_access"] = True
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "configs" / "protocols"
            target.mkdir(parents=True)
            (target / "protocol-v2.0-final.json").write_text(
                json.dumps(source), encoding="utf-8"
            )
            with self.assertRaisesRegex(RuntimeError, "refuses a protocol"):
                load_frozen_protocol(root)


if __name__ == "__main__":
    unittest.main()
