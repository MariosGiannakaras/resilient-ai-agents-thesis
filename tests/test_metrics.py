from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.metrics import (  # noqa: E402
    RecoveryStatus,
    compute_resilience_metrics,
    summarize_recovery_statuses,
)


class ResilienceMetricKnownAnswerTests(unittest.TestCase):
    def test_recovery_estimands_match_hand_calculation(self) -> None:
        metrics = compute_resilience_metrics(
            [9.0, 11.0, 4.0, 7.0, 9.0, 9.5, 10.0],
            reference_values=[10.0] * 7,
            change_index=2,
            immediate_window=1,
            worst_window=3,
            terminal_window=2,
            recovery_tolerance=1.0,
            recovery_stability_steps=2,
        )
        self.assertEqual(metrics.nominal_mean, 10.0)
        self.assertEqual(metrics.nominal_reference_mean, 10.0)
        self.assertEqual(metrics.nominal_gap, 0.0)
        self.assertEqual(metrics.immediate_degradation, 6.0)
        self.assertEqual(metrics.worst_degradation, 6.0)
        self.assertEqual(metrics.post_change_mean, 9.75)
        self.assertEqual(metrics.post_change_reference_mean, 10.0)
        self.assertEqual(metrics.post_change_gap, 0.25)
        self.assertEqual(metrics.cumulative_deficit, 10.5)
        self.assertEqual(metrics.first_degradation_index, 2)
        self.assertEqual(metrics.recovery_index, 4)
        self.assertEqual(metrics.recovery_delay, 2)
        self.assertEqual(metrics.recovery_status, RecoveryStatus.RECOVERED)

    def test_non_recovery_remains_none_not_horizon(self) -> None:
        metrics = compute_resilience_metrics(
            [10.0, 10.0, 4.0, 5.0, 6.0],
            reference_values=[10.0] * 5,
            change_index=2,
            immediate_window=1,
            worst_window=3,
            terminal_window=2,
            recovery_tolerance=1.0,
            recovery_stability_steps=2,
        )
        self.assertEqual(metrics.recovery_status, RecoveryStatus.NOT_RECOVERED)
        self.assertEqual(metrics.first_degradation_index, 2)
        self.assertIsNone(metrics.recovery_index)
        self.assertIsNone(metrics.recovery_delay)

    def test_no_degradation_is_not_mislabelled_as_recovery(self) -> None:
        metrics = compute_resilience_metrics(
            [-2.0, -2.0, -1.5, -1.0, -2.0],
            reference_values=[-2.0] * 5,
            change_index=2,
            immediate_window=2,
            worst_window=3,
            terminal_window=2,
            recovery_tolerance=0.0,
            recovery_stability_steps=2,
        )
        self.assertEqual(metrics.recovery_status, RecoveryStatus.NO_DEGRADATION)
        self.assertIsNone(metrics.first_degradation_index)
        self.assertIsNone(metrics.recovery_index)
        self.assertEqual(metrics.cumulative_deficit, 0.0)
        self.assertLess(metrics.immediate_degradation, 0.0)

    def test_time_varying_reference_and_explicit_windows(self) -> None:
        metrics = compute_resilience_metrics(
            [1.0, 2.0, 1.0, 2.5, 3.5, 5.0],
            reference_values=[1.0, 2.0, 3.0, 4.0, 4.0, 5.0],
            change_index=2,
            immediate_window=2,
            worst_window=3,
            terminal_window=2,
            recovery_tolerance=0.5,
            recovery_stability_steps=2,
        )
        self.assertEqual(metrics.immediate_degradation, 1.75)
        self.assertEqual(metrics.worst_degradation, 2.0)
        self.assertEqual(metrics.post_change_mean, 4.25)
        self.assertEqual(metrics.post_change_reference_mean, 4.5)
        self.assertEqual(metrics.cumulative_deficit, 4.0)
        self.assertEqual(metrics.recovery_index, 4)
        self.assertEqual(metrics.recovery_delay, 2)


class RecoveryAggregationTests(unittest.TestCase):
    def test_status_summary_preserves_all_outcomes(self) -> None:
        summary = summarize_recovery_statuses(
            [
                RecoveryStatus.RECOVERED,
                RecoveryStatus.NOT_RECOVERED,
                RecoveryStatus.NOT_RECOVERED,
                RecoveryStatus.NO_DEGRADATION,
            ]
        )
        self.assertEqual(summary.total_runs, 4)
        self.assertEqual(summary.recovered_runs, 1)
        self.assertEqual(summary.non_recovered_runs, 2)
        self.assertEqual(summary.no_degradation_runs, 1)
        self.assertEqual(summary.non_recovery_rate, 0.5)

    def test_invalid_inputs_fail_closed(self) -> None:
        valid = dict(
            reference_values=[1.0, 1.0, 1.0],
            change_index=1,
            immediate_window=1,
            worst_window=1,
            terminal_window=1,
            recovery_tolerance=0.0,
            recovery_stability_steps=1,
        )
        with self.assertRaises(ValueError):
            compute_resilience_metrics([1.0, math.nan, 1.0], **valid)
        with self.assertRaises(ValueError):
            compute_resilience_metrics([1.0, 1.0], **valid)
        with self.assertRaises(ValueError):
            compute_resilience_metrics([1.0, 1.0, 1.0], **(valid | {"worst_window": 3}))
        with self.assertRaises(ValueError):
            compute_resilience_metrics(
                [1.0, 1.0, 1.0], **(valid | {"recovery_tolerance": -0.1})
            )
        with self.assertRaises(ValueError):
            summarize_recovery_statuses([])
        with self.assertRaises(ValueError):
            summarize_recovery_statuses(["recovered"])  # type: ignore[list-item]


if __name__ == "__main__":
    unittest.main()
