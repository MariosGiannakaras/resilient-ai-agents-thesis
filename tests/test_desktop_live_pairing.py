from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.live_events import DesktopLiveReadModel, DroppingLiveEventSink


class DesktopLivePairingTests(unittest.TestCase):
    @staticmethod
    def _event(*, branch: str, interaction: int, state: tuple[int, int]) -> dict:
        return {
            "schema_version": 1,
            "event_type": "gridworld-transition",
            "stream_id": f"phase-b:q_learning:dev-root:dev-layout:{branch}",
            "phase": "phase-b",
            "method_id": "q_learning",
            "root_id": "dev-root",
            "layout_id": "dev-layout",
            "branch": branch,
            "episode_index": 0,
            "interaction_index": interaction,
            "environment_step": interaction,
            "grid": {
                "width": 3,
                "height": 3,
                "start": [0, 0],
                "goal": [2, 2],
                "obstacles": [[1, 1]],
            },
            "true_state": list(state),
            "delivered_observation": list(state),
            "intended_action": "right",
            "executed_action": "right",
            "reward": -0.1,
            "terminated": False,
            "truncated": False,
            "regime_id": "changed",
            "disturbance_flags": {
                "action_failure": False,
                "observation_corruption": False,
            },
            "change_event_ids": ["presentation-test-change"],
        }

    def test_exact_interaction_fd_ad_frames_are_exposed_as_one_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory).resolve()
            sink = DroppingLiveEventSink(
                writable_root=writable,
                study_id="live-pair-test",
                flush_interval_seconds=0.01,
            )
            sink.emit(self._event(branch="FD", interaction=7, state=(0, 1)))
            sink.emit(self._event(branch="AD", interaction=7, state=(1, 0)))
            sink.close()

            frames = DesktopLiveReadModel(writable_root=writable).latest("live-pair-test")

        self.assertGreaterEqual(len(frames), 1)
        paired = next(frame for frame in frames if frame.comparison is not None)
        comparison = paired.comparison
        assert comparison is not None
        self.assertEqual(comparison.frozen.branch, "FD")
        self.assertEqual(comparison.adaptive.branch, "AD")
        self.assertEqual(comparison.frozen.interaction_index, 7)
        self.assertEqual(comparison.adaptive.interaction_index, 7)
        self.assertEqual(comparison.frozen.true_state, (0, 1))
        self.assertEqual(comparison.adaptive.true_state, (1, 0))

    def test_new_fd_branch_invalidates_previous_exposed_pair_until_new_ad_matches(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory).resolve()
            sink = DroppingLiveEventSink(
                writable_root=writable,
                study_id="live-pair-reset-test",
                flush_interval_seconds=0.01,
            )
            sink.emit(self._event(branch="FD", interaction=1, state=(0, 0)))
            sink.emit(self._event(branch="AD", interaction=1, state=(0, 1)))
            sink.emit(self._event(branch="FD", interaction=1, state=(1, 0)))
            sink.close()

            frames = DesktopLiveReadModel(writable_root=writable).latest(
                "live-pair-reset-test"
            )

        self.assertTrue(frames)
        self.assertTrue(all(frame.comparison is None for frame in frames))


if __name__ == "__main__":
    unittest.main()
