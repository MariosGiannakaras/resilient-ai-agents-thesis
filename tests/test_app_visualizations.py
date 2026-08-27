from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app.visualizations import (  # noqa: E402
    aggregated_metric_figure,
    evidence_distribution_figure,
    layout_breakdown_figure,
    live_series_options,
)


class ApplicationVisualizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.primary = pd.DataFrame(
            [
                {"agent_id": "f0", "condition_id": "nominal", "layout_id": "final-l01", "cumulative_deficit": 0.0},
                {"agent_id": "c0", "condition_id": "nominal", "layout_id": "final-l01", "cumulative_deficit": 1.0},
                {"agent_id": "f0", "condition_id": "action-failure-1of8", "layout_id": "final-l02", "cumulative_deficit": 5.0},
                {"agent_id": "c0", "condition_id": "action-failure-1of8", "layout_id": "final-l02", "cumulative_deficit": 3.0},
            ]
        )

    def test_distribution_and_layout_figures_use_only_selected_stored_rows(self) -> None:
        distribution = evidence_distribution_figure(
            self.primary,
            "cumulative_deficit",
            agent_ids=["f0"],
            condition_ids=["nominal"],
        )
        self.assertEqual(len(distribution.data), 1)
        self.assertEqual(distribution.data[0].name, "Fixed Q-Learning")
        self.assertEqual(tuple(distribution.data[0].y), (0.0,))
        self.assertIn("no CI available", distribution.layout.title.text)

        breakdown = layout_breakdown_figure(
            self.primary,
            "cumulative_deficit",
            agent_ids=["c0"],
            condition_ids=["action-failure-1of8"],
        )
        self.assertEqual(len(breakdown.data), 1)
        self.assertEqual(tuple(breakdown.data[0].y), (3.0,))

    def test_historical_aggregate_labels_error_bars_as_sd(self) -> None:
        index = pd.MultiIndex.from_tuples(
            [("f0", "nominal"), ("c0", "nominal")],
            names=["agent_id", "condition_id"],
        )
        columns = pd.MultiIndex.from_tuples(
            [("cumulative_deficit", "mean"), ("cumulative_deficit", "std")]
        )
        frame = pd.DataFrame([[0.0, 0.0], [1.0, 0.5]], index=index, columns=columns)
        figure = aggregated_metric_figure(frame, "cumulative_deficit")
        self.assertIn("error bars = SD", figure.layout.title.text)
        self.assertNotIn("confidence interval", figure.layout.title.text.casefold())

    def test_empty_live_chart_contains_no_demo_series(self) -> None:
        options = live_series_options({}, title="Live", y_axis_label="Return")
        self.assertEqual(options["series"], [])
        self.assertIn("LIVE / PROVISIONAL", options["title"]["subtext"])


if __name__ == "__main__":
    unittest.main()
