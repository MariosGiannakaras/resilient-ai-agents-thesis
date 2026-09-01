from __future__ import annotations

import unittest

from resilient_agents.evidence_v2.recovery import (
    RecoveryDefinition,
    assess_recovery,
    pairwise_method_contrasts,
)
from resilient_agents.evidence_v2.statistics import MetricDirection


def _definition(**overrides):
    values = {
        "window_size": 32,
        "observation_horizon": 256,
        "tolerance": 0.10,
        "stability_windows": 2,
        "direction": MetricDirection.HIGHER_IS_BETTER,
    }
    values.update(overrides)
    return RecoveryDefinition(**values)


class EvidenceV2RecoveryTests(unittest.TestCase):
    def test_very_fast_recovery_is_stability_confirmed(self) -> None:
        result = assess_recovery(
            nominal_windows=[0.5] * 8,
            disturbed_windows=[0.45, 0.46, 0.44, 0.45, 0.45, 0.45, 0.45, 0.45],
            definition=_definition(),
        )
        self.assertEqual(result.status, "recovered")
        self.assertEqual(result.recovery_time, 32)
        self.assertEqual(result.confirmation_time, 64)

    def test_slower_recovery_reports_first_stable_window_not_confirmation_window(self) -> None:
        result = assess_recovery(
            nominal_windows=[0.5] * 8,
            disturbed_windows=[0.0, 0.1, 0.2, 0.39, 0.41, 0.42, 0.43, 0.44],
            definition=_definition(),
        )
        # Window 128 is still outside the 0.10 neighborhood: 0.50 - 0.39 = 0.11.
        # Windows ending 160 and 192 are the first stable in-tolerance pair.
        self.assertEqual(result.status, "recovered")
        self.assertEqual(result.recovery_time, 160)
        self.assertEqual(result.confirmation_time, 192)

    def test_never_recovered_is_right_censored_without_artificial_horizon_time(self) -> None:
        result = assess_recovery(
            nominal_windows=[0.5] * 8,
            disturbed_windows=[0.0] * 8,
            definition=_definition(),
        )
        self.assertEqual(result.status, "right-censored")
        self.assertIsNone(result.recovery_time)
        self.assertIsNone(result.confirmation_time)
        self.assertEqual(result.censoring_time, 256)

    def test_temporary_threshold_crossing_is_not_stable_recovery(self) -> None:
        result = assess_recovery(
            nominal_windows=[0.5] * 8,
            disturbed_windows=[0.0, 0.45, 0.0, 0.45, 0.0, 0.45, 0.0, 0.45],
            definition=_definition(),
        )
        self.assertEqual(result.status, "right-censored")
        self.assertIsNone(result.recovery_time)

    def test_recovery_can_start_in_penultimate_window_and_confirm_at_horizon(self) -> None:
        result = assess_recovery(
            nominal_windows=[0.5] * 8,
            disturbed_windows=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45, 0.45],
            definition=_definition(),
        )
        self.assertEqual(result.recovery_time, 224)
        self.assertEqual(result.confirmation_time, 256)

    def test_higher_is_worse_direction_is_supported(self) -> None:
        result = assess_recovery(
            nominal_windows=[1.0] * 8,
            disturbed_windows=[2.0, 1.5, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0],
            definition=_definition(direction=MetricDirection.HIGHER_IS_WORSE),
        )
        self.assertEqual(result.recovery_time, 96)
        self.assertEqual(result.confirmation_time, 128)

    def test_calculation_is_deterministic_and_uses_matched_nominal_reference(self) -> None:
        definition = _definition()
        nominal = [0.50, 0.49, 0.48, 0.47, 0.46, 0.45, 0.44, 0.43]
        disturbed = [0.0, 0.1, 0.2, 0.37, 0.36, 0.35, 0.34, 0.33]
        first = assess_recovery(
            nominal_windows=nominal,
            disturbed_windows=disturbed,
            definition=definition,
        )
        second = assess_recovery(
            nominal_windows=nominal,
            disturbed_windows=disturbed,
            definition=definition,
        )
        self.assertEqual(first, second)
        self.assertEqual([point.nominal_value for point in first.trajectory], nominal)
        self.assertEqual(first.recovery_time, 128)
        self.assertEqual(first.confirmation_time, 160)

    def test_decimal_gap_equal_to_frozen_tolerance_is_not_lost_to_binary_rounding(self) -> None:
        result = assess_recovery(
            nominal_windows=[0.46] * 8,
            disturbed_windows=[0.0, 0.0, 0.36, 0.36, 0.0, 0.0, 0.0, 0.0],
            definition=_definition(),
        )
        # Python represents 0.46 - 0.36 slightly above 0.10 on some paths;
        # the scientific rule is mathematical <= 0.10, not binary-float > 0.10.
        self.assertEqual(result.recovery_time, 96)
        self.assertEqual(result.confirmation_time, 128)
        self.assertTrue(result.trajectory[2].within_tolerance)
        self.assertTrue(result.trajectory[3].within_tolerance)

    def test_pairwise_method_contrasts_pair_only_common_independent_roots(self) -> None:
        contrasts = pairwise_method_contrasts(
            {
                "a": {"r1": 1.0, "r2": 2.0, "r3": 3.0},
                "b": {"r1": 0.0, "r2": 1.0, "r4": 99.0},
                "c": {"r1": 2.0, "r2": 4.0},
            },
            critical_value=2.201,
        )
        ab = next(item for item in contrasts if (item.method_a, item.method_b) == ("a", "b"))
        self.assertEqual(ab.root_ids, ("r1", "r2"))
        self.assertEqual(ab.differences, (1.0, 1.0))
        self.assertAlmostEqual(ab.interval.mean, 1.0)

    def test_recovery_definition_rejects_non_divisible_windows(self) -> None:
        with self.assertRaisesRegex(ValueError, "divisible"):
            RecoveryDefinition(window_size=30, observation_horizon=256)


if __name__ == "__main__":
    unittest.main()
