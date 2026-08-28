from __future__ import annotations

import math
import unittest

from resilient_agents.evidence_v2 import (
    MetricDirection,
    matched_adaptation_effect,
    mean_across_layouts,
    paired_root_differences,
    student_t_mean_interval,
    trapezoidal_time_average,
)
from resilient_agents.protocol_v2 import ProtocolV2Branch


class EvidenceV2StatisticsTests(unittest.TestCase):
    def test_trapezoidal_time_average_uses_actual_interaction_axis(self) -> None:
        value = trapezoidal_time_average([(0, 0.0), (10, 1.0), (30, 3.0)])
        # Areas: 10*(0+1)/2=5; 20*(1+3)/2=40; total/30=1.5.
        self.assertAlmostEqual(value, 1.5)
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            trapezoidal_time_average([(0, 0.0), (10, 1.0), (10, 2.0)])

    def test_matched_adaptation_effect_higher_is_better(self) -> None:
        effect = matched_adaptation_effect(
            {
                ProtocolV2Branch.FROZEN_NOMINAL: 10.0,
                ProtocolV2Branch.FROZEN_DISTURBED: 4.0,
                ProtocolV2Branch.ADAPTIVE_NOMINAL: 11.0,
                ProtocolV2Branch.ADAPTIVE_DISTURBED: 8.0,
            },
            direction=MetricDirection.HIGHER_IS_BETTER,
        )
        self.assertEqual(effect.frozen_loss, 6.0)
        self.assertEqual(effect.adaptive_loss, 3.0)
        self.assertEqual(effect.adaptation_benefit, 3.0)

    def test_matched_adaptation_effect_higher_is_worse(self) -> None:
        effect = matched_adaptation_effect(
            {
                ProtocolV2Branch.FROZEN_NOMINAL: 2.0,
                ProtocolV2Branch.FROZEN_DISTURBED: 8.0,
                ProtocolV2Branch.ADAPTIVE_NOMINAL: 3.0,
                ProtocolV2Branch.ADAPTIVE_DISTURBED: 5.0,
            },
            direction=MetricDirection.HIGHER_IS_WORSE,
        )
        self.assertEqual(effect.frozen_loss, 6.0)
        self.assertEqual(effect.adaptive_loss, 2.0)
        self.assertEqual(effect.adaptation_benefit, 4.0)

    def test_four_branch_effect_rejects_missing_reference_branch(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly FN/FD/AN/AD"):
            matched_adaptation_effect(
                {
                    ProtocolV2Branch.FROZEN_NOMINAL: 1.0,
                    ProtocolV2Branch.FROZEN_DISTURBED: 0.0,
                    ProtocolV2Branch.ADAPTIVE_DISTURBED: 0.5,
                },
                direction=MetricDirection.HIGHER_IS_BETTER,
            )

    def test_layouts_are_equal_weight_blocks_within_root(self) -> None:
        self.assertEqual(mean_across_layouts({"layout-a": 1.0, "layout-b": 3.0}), 2.0)

    def test_paired_root_differences_require_same_root_identities(self) -> None:
        self.assertEqual(
            paired_root_differences(
                {"root-02": 5.0, "root-01": 4.0},
                {"root-01": 1.0, "root-02": 2.0},
            ),
            {"root-01": 3.0, "root-02": 3.0},
        )
        with self.assertRaisesRegex(ValueError, "same non-empty root identities"):
            paired_root_differences({"root-01": 1.0}, {"root-02": 1.0})

    def test_student_t_interval_uses_frozen_critical_value(self) -> None:
        interval = student_t_mean_interval([1.0, 2.0, 3.0, 4.0], critical_value=3.182)
        self.assertEqual(interval.n, 4)
        self.assertAlmostEqual(interval.mean, 2.5)
        expected_sd = math.sqrt(5.0 / 3.0)
        self.assertAlmostEqual(interval.standard_deviation, expected_sd)
        expected_se = expected_sd / 2.0
        self.assertAlmostEqual(interval.standard_error, expected_se)
        self.assertAlmostEqual(interval.lower, 2.5 - 3.182 * expected_se)
        self.assertAlmostEqual(interval.upper, 2.5 + 3.182 * expected_se)
        with self.assertRaisesRegex(ValueError, "at least two independent roots"):
            student_t_mean_interval([1.0], critical_value=12.706)


if __name__ == "__main__":
    unittest.main()
