from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app.live import build_runtime_telemetry_view, gridworld_html  # noqa: E402


class ApplicationLiveViewTests(unittest.TestCase):
    def test_real_started_and_step_events_build_gridworld_without_inference(self) -> None:
        rows = [
            {
                "runtime_telemetry_schema_version": 1,
                "sequence": 0,
                "event": "episode_started",
                "run_id": "RUN",
                "root_seed": 11,
                "agent_id": "s0",
                "branch": "disrupted",
                "phase": "post-change",
                "episode_index": 16,
                "scenario_id": "dev-l01",
                "grid": {
                    "width": 3,
                    "height": 3,
                    "start": [0, 0],
                    "goal": [2, 2],
                    "obstacles": [[1, 1]],
                },
                "delivered_observation": [0, 0],
            },
            {
                "runtime_telemetry_schema_version": 1,
                "sequence": 1,
                "event": "gridworld_step",
                "run_id": "RUN",
                "root_seed": 11,
                "agent_id": "s0",
                "branch": "disrupted",
                "phase": "post-change",
                "episode_index": 16,
                "scenario_id": "dev-l01",
                "step": 3,
                "true_state": [1, 0],
                "delivered_observation": [0, 1],
                "intended_action": "right",
                "executed_action": "right",
                "reward": -1.0,
                "terminated": False,
                "truncated": False,
                "disturbance_flags": {"observation_corrupted": True},
                "change_event_ids": [],
                "cumulative_episode_return": -3.0,
            },
        ]
        view = build_runtime_telemetry_view(rows)
        self.assertIsNotNone(view.gridworld)
        assert view.gridworld is not None
        self.assertEqual(view.gridworld.strategy_name, "SARSA")
        self.assertEqual(view.gridworld.position, (1, 0))
        self.assertEqual(view.gridworld.delivered_observation, (0, 1))
        self.assertEqual(view.gridworld.obstacles, ((1, 1),))
        html = gridworld_html(view.gridworld)
        self.assertIn("gw-agent", html)
        self.assertIn("gw-observation", html)
        self.assertIn("gw-obstacle", html)

    def test_step_without_matching_episode_start_does_not_synthesize_grid(self) -> None:
        view = build_runtime_telemetry_view(
            [
                {
                    "runtime_telemetry_schema_version": 1,
                    "sequence": 0,
                    "event": "gridworld_step",
                    "root_seed": 11,
                    "agent_id": "f0",
                    "branch": "reference",
                    "phase": "pre-change",
                    "episode_index": 0,
                    "scenario_id": "dev-l01",
                    "step": 1,
                    "true_state": [0, 1],
                }
            ]
        )
        self.assertIsNone(view.gridworld)
        self.assertIn("No live GridWorld step yet", gridworld_html(view.gridworld))

    def test_completed_events_form_real_agent_branch_phase_return_series(self) -> None:
        rows = [
            {
                "runtime_telemetry_schema_version": 1,
                "sequence": 0,
                "event": "episode_completed",
                "agent_id": "c0",
                "branch": "reference",
                "phase": "pre-change",
                "episode_index": 0,
                "return": -12.0,
            },
            {
                "runtime_telemetry_schema_version": 1,
                "sequence": 1,
                "event": "episode_completed",
                "agent_id": "c0",
                "branch": "disrupted",
                "phase": "post-change",
                "episode_index": 16,
                "return": -25.0,
            },
        ]
        view = build_runtime_telemetry_view(rows)
        self.assertEqual(
            view.return_series,
            {
                "c0:reference:pre-change": ((0, -12.0),),
                "c0:disrupted:post-change": ((16, -25.0),),
            },
        )
        self.assertEqual(view.latest_sequence, 1)

    def test_out_of_order_telemetry_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "sequence-ordered"):
            build_runtime_telemetry_view(
                [
                    {"sequence": 2, "event": "episode_completed"},
                    {"sequence": 1, "event": "episode_completed"},
                ]
            )


if __name__ == "__main__":
    unittest.main()
