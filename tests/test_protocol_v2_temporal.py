from __future__ import annotations

import unittest

from resilient_agents.protocol_v2_temporal import (
    FixedRewardWindowRecorder,
    RewardWindow,
)


class ProtocolV2TemporalEvidenceTests(unittest.TestCase):
    def test_recorder_emits_exact_inclusive_fixed_windows(self) -> None:
        recorder = FixedRewardWindowRecorder(window_size=4)
        for reward in (1.0, 0.0, -1.0, 2.0, 4.0, 4.0, 0.0, 0.0):
            recorder.record(reward)

        recorder.require_complete(total_interactions=8)
        self.assertEqual(
            recorder.completed_windows,
            (
                RewardWindow(1, 4, 4, 0.5),
                RewardWindow(5, 8, 4, 2.0),
            ),
        )

    def test_partial_window_is_not_exported_and_fails_complete_check(self) -> None:
        recorder = FixedRewardWindowRecorder(window_size=4)
        for reward in (1.0, 2.0, 3.0):
            recorder.record(reward)
        self.assertEqual(recorder.completed_windows, ())
        self.assertEqual(recorder.partial_window_interactions, 3)
        with self.assertRaisesRegex(RuntimeError, "does not end on a complete"):
            recorder.require_complete(total_interactions=3)

    def test_exact_256_horizon_has_eight_32_interaction_windows(self) -> None:
        recorder = FixedRewardWindowRecorder(window_size=32)
        for interaction in range(1, 257):
            recorder.record(float(interaction % 5) - 2.0)
        recorder.require_complete(total_interactions=256)
        windows = recorder.completed_windows
        self.assertEqual(len(windows), 8)
        self.assertEqual(
            tuple(window.end_interaction for window in windows),
            (32, 64, 96, 128, 160, 192, 224, 256),
        )
        self.assertEqual(windows[0].start_interaction, 1)
        self.assertEqual(windows[-1].start_interaction, 225)

    def test_nonfinite_rewards_fail_closed(self) -> None:
        recorder = FixedRewardWindowRecorder(window_size=32)
        with self.assertRaisesRegex(ValueError, "finite"):
            recorder.record(float("nan"))

    def test_reward_window_round_trip_is_strict(self) -> None:
        original = RewardWindow(1, 32, 32, -0.125)
        self.assertEqual(RewardWindow.from_dict(original.to_dict()), original)
        malformed = original.to_dict()
        malformed["extra"] = 1
        with self.assertRaisesRegex(ValueError, "keys"):
            RewardWindow.from_dict(malformed)


if __name__ == "__main__":
    unittest.main()
