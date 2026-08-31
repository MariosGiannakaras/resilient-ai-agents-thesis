from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.live_events import DesktopLiveReadModel, DroppingLiveEventSink
from resilient_agents.gridworld import GridWorldEnvironment
from resilient_agents.presentation_observer import (
    bound_presentation_sink,
    emit_gridworld_transition,
    emit_presentation_event,
)
from tests.test_gridworld import fixture_seeds, fixture_spec


class _RaisingSink:
    def emit(self, _event) -> None:
        raise RuntimeError("presentation failure must be swallowed")


class _Collector:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def emit(self, event) -> None:
        self.events.append(dict(event))


class PresentationObserverTests(unittest.TestCase):
    def test_emit_helper_swallows_sink_failure(self) -> None:
        with bound_presentation_sink(_RaisingSink()):
            emit_presentation_event({"stream_id": "test", "event_type": "noop"})

    def test_gridworld_snapshot_is_copy_only_after_existing_transition(self) -> None:
        scenario = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=5,
            include_change=False,
        )
        environment = GridWorldEnvironment(scenario)
        collector = _Collector()
        try:
            environment.reset(seeds=fixture_seeds(action=71, observation=81))
            transition = environment.step(1)
            state_before = environment.debug_state()
            with bound_presentation_sink(collector):
                emit_gridworld_transition(
                    phase="presentation-test",
                    method_id="ui-test",
                    root_id="dev-root",
                    scenario=scenario,
                    episode_index=0,
                    interaction_index=1,
                    transition=transition,
                )
            state_after = environment.debug_state()
        finally:
            environment.close()

        self.assertEqual(state_before, state_after)
        self.assertEqual(len(collector.events), 1)
        event = collector.events[0]
        self.assertEqual(event["event_type"], "gridworld-transition")
        self.assertEqual(event["phase"], "presentation-test")
        self.assertEqual(event["method_id"], "ui-test")
        self.assertEqual(event["root_id"], "dev-root")
        self.assertEqual(event["true_state"], list(transition.true_state))
        self.assertEqual(
            event["delivered_observation"],
            list(transition.delivered_observation),
        )

    def test_live_sink_is_outside_evidence_paths_and_readable_after_close(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory).resolve()
            sink = DroppingLiveEventSink(
                writable_root=writable,
                study_id="dev-live-read-test",
                queue_size=2,
                flush_interval_seconds=0.01,
            )
            event = {
                "schema_version": 1,
                "event_type": "gridworld-transition",
                "stream_id": "phase-a:q_learning:dev-root:dev-layout:nominal",
                "phase": "phase-a",
                "method_id": "q_learning",
                "root_id": "dev-root",
                "layout_id": "dev-layout",
                "branch": None,
                "episode_index": 0,
                "interaction_index": 1,
                "environment_step": 0,
                "grid": {
                    "width": 3,
                    "height": 3,
                    "start": [0, 0],
                    "goal": [2, 2],
                    "obstacles": [[1, 1]],
                },
                "true_state": [0, 1],
                "delivered_observation": [0, 1],
                "intended_action": "down",
                "executed_action": "down",
                "reward": -0.1,
                "terminated": False,
                "truncated": False,
                "regime_id": "nominal",
                "disturbance_flags": {
                    "action_failure": False,
                    "observation_corruption": False,
                },
                "change_event_ids": [],
            }
            sink.emit(event)
            sink.close()

            self.assertIn("presentation", sink.path.parts)
            self.assertNotIn("studies", sink.path.parts)
            self.assertNotIn("runs", sink.path.parts)
            frames = DesktopLiveReadModel(writable_root=writable).latest("dev-live-read-test")
            self.assertEqual(len(frames), 1)
            self.assertEqual(frames[0].true_state, (0, 1))
            self.assertEqual(frames[0].goal, (2, 2))


if __name__ == "__main__":
    unittest.main()
