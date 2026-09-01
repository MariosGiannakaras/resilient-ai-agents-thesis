from __future__ import annotations

import unittest
from pathlib import Path

from resilient_agents.desktop.exploratory_preview import DesktopExploratoryPreviewModel

REPO_ROOT = Path(__file__).resolve().parents[1]


class DesktopExploratoryPreviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = DesktopExploratoryPreviewModel(repo_root=REPO_ROOT)

    def test_preview_uses_only_non_final_development_layouts(self) -> None:
        preview = self.model.preview(
            selected_method_ids=("q_learning", "ppo"),
            root_count=2,
            layout_count=2,
        )
        self.assertEqual(preview.method_count, 2)
        self.assertEqual(preview.root_count, 2)
        self.assertEqual(preview.layout_count, 2)
        self.assertEqual(preview.development_layout_ids, ("gw-l1-a", "gw-l1-b"))
        self.assertFalse(any("final" in item for item in preview.development_layout_ids))
        self.assertEqual(
            preview.condition_ids,
            (
                "action-remap-swap-right-down",
                "action-remap-cycle-clockwise",
            ),
        )

    def test_preview_counts_come_from_real_study_planner(self) -> None:
        preview = self.model.preview(
            selected_method_ids=("q_learning", "sarsa", "dqn"),
            root_count=2,
            layout_count=1,
        )
        self.assertEqual(preview.phase_a_jobs, 6)
        self.assertEqual(preview.phase_b_jobs, 12)
        self.assertEqual(preview.validation_jobs, 1)
        self.assertEqual(preview.analysis_jobs, 1)
        self.assertEqual(preview.export_jobs, 1)
        self.assertEqual(preview.total_jobs, 21)

    def test_preview_bounds_are_small_and_final_reserve_independent(self) -> None:
        self.assertEqual(self.model.max_root_count, 2)
        self.assertEqual(self.model.max_layout_count, 2)
        with self.assertRaisesRegex(ValueError, "root_count"):
            self.model.preview(
                selected_method_ids=("q_learning",),
                root_count=3,
                layout_count=1,
            )


if __name__ == "__main__":
    unittest.main()
