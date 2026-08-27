from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.metrics import ResilienceMetrics, RecoveryStatus  # noqa: E402
from resilient_agents.v11_statistics import (  # noqa: E402
    PairedMetricObservation,
    metric_value,
    paired_bootstrap_contrast,
)


def observations(
    *,
    first_values: dict[tuple[int, str], float],
    second_values: dict[tuple[int, str], float],
    first_agent: str = "c0",
    second_agent: str = "f0",
) -> list[PairedMetricObservation]:
    rows: list[PairedMetricObservation] = []
    for key, value in first_values.items():
        rows.append(PairedMetricObservation(key[0], key[1], first_agent, value))
    for key, value in second_values.items():
        rows.append(PairedMetricObservation(key[0], key[1], second_agent, value))
    return rows


class V11StatisticsTests(unittest.TestCase):
    def test_lower_is_better_effect_is_positive_when_first_agent_has_lower_deficit(self) -> None:
        roots = (11, 22, 33)
        layouts = ("l1", "l2")
        first = {(root, layout): 2.0 for root in roots for layout in layouts}
        second = {(root, layout): 5.0 for root in roots for layout in layouts}
        result = paired_bootstrap_contrast(
            observations(first_values=first, second_values=second),
            metric="cumulative_deficit",
            first_agent="c0",
            second_agent="f0",
            root_seeds=roots,
            layout_ids=layouts,
            bootstrap_resamples=200,
            analysis_seed=9,
        )
        self.assertEqual(result.estimate, 3.0)
        self.assertEqual(result.ci_lower, 3.0)
        self.assertEqual(result.ci_upper, 3.0)
        self.assertEqual(result.n_roots, 3)
        self.assertEqual(result.n_layouts, 2)

    def test_higher_is_better_terminal_effect_uses_first_minus_second(self) -> None:
        roots = (1, 2)
        layouts = ("l1", "l2")
        first = {(root, layout): 8.0 for root in roots for layout in layouts}
        second = {(root, layout): 5.0 for root in roots for layout in layouts}
        result = paired_bootstrap_contrast(
            observations(first_values=first, second_values=second),
            metric="terminal_performance",
            first_agent="c0",
            second_agent="f0",
            root_seeds=roots,
            layout_ids=layouts,
            bootstrap_resamples=100,
            analysis_seed=3,
        )
        self.assertEqual(result.estimate, 3.0)

    def test_layouts_are_averaged_within_root_before_bootstrap(self) -> None:
        roots = (1, 2)
        layouts = ("l1", "l2")
        # Higher-is-better effects are [1,3] for root 1 and [5,7] for root 2.
        first = {(1, "l1"): 1.0, (1, "l2"): 3.0, (2, "l1"): 5.0, (2, "l2"): 7.0}
        second = {(root, layout): 0.0 for root in roots for layout in layouts}
        result = paired_bootstrap_contrast(
            observations(first_values=first, second_values=second),
            metric="terminal_performance",
            first_agent="c0",
            second_agent="f0",
            root_seeds=roots,
            layout_ids=layouts,
            bootstrap_resamples=200,
            analysis_seed=17,
        )
        self.assertEqual(result.root_effects, ((1, 2.0), (2, 6.0)))
        self.assertEqual(result.layout_effects, (("l1", 3.0), ("l2", 5.0)))
        self.assertEqual(result.estimate, 4.0)

    def test_bootstrap_is_deterministic(self) -> None:
        roots = (1, 2, 3, 4)
        layouts = ("l1", "l2")
        first = {
            (root, layout): float(root + (1 if layout == "l2" else 0))
            for root in roots
            for layout in layouts
        }
        second = {(root, layout): 0.0 for root in roots for layout in layouts}
        kwargs = dict(
            observations=observations(first_values=first, second_values=second),
            metric="terminal_performance",
            first_agent="c0",
            second_agent="f0",
            root_seeds=roots,
            layout_ids=layouts,
            bootstrap_resamples=500,
            analysis_seed=1234,
        )
        self.assertEqual(paired_bootstrap_contrast(**kwargs), paired_bootstrap_contrast(**kwargs))

    def test_missing_duplicate_or_foreign_cells_fail_closed(self) -> None:
        roots = (1, 2)
        layouts = ("l1",)
        complete = observations(
            first_values={(1, "l1"): 1.0, (2, "l1"): 2.0},
            second_values={(1, "l1"): 0.0, (2, "l1"): 0.0},
        )
        with self.assertRaises(ValueError):
            paired_bootstrap_contrast(
                complete[:-1], metric="terminal_performance", first_agent="c0",
                second_agent="f0", root_seeds=roots, layout_ids=layouts,
                bootstrap_resamples=10,
            )
        with self.assertRaises(ValueError):
            paired_bootstrap_contrast(
                complete + [complete[0]], metric="terminal_performance", first_agent="c0",
                second_agent="f0", root_seeds=roots, layout_ids=layouts,
                bootstrap_resamples=10,
            )
        with self.assertRaises(ValueError):
            paired_bootstrap_contrast(
                complete + [PairedMetricObservation(1, "l1", "d0", 1.0)],
                metric="terminal_performance", first_agent="c0", second_agent="f0",
                root_seeds=roots, layout_ids=layouts, bootstrap_resamples=10,
            )

    def test_public_terminal_metric_maps_to_existing_terminal_window_mean(self) -> None:
        metrics = ResilienceMetrics(
            nominal_mean=0.0,
            nominal_reference_mean=0.0,
            nominal_gap=0.0,
            immediate_degradation=2.0,
            worst_degradation=3.0,
            post_change_mean=-7.5,
            post_change_reference_mean=-6.0,
            post_change_gap=1.5,
            cumulative_deficit=9.0,
            first_degradation_index=16,
            recovery_index=None,
            recovery_delay=None,
            recovery_status=RecoveryStatus.NOT_RECOVERED,
        )
        self.assertEqual(metric_value(metrics, "terminal_performance"), -7.5)
        self.assertEqual(metric_value(metrics, "cumulative_deficit"), 9.0)
        self.assertEqual(metric_value(metrics, "immediate_degradation"), 2.0)


if __name__ == "__main__":
    unittest.main()
