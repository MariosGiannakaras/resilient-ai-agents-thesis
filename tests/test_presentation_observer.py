from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.agents import TabularQLearningAgent, TabularQLearningConfig
from resilient_agents.desktop.live_events import DesktopLiveReadModel, DroppingLiveEventSink
from resilient_agents.desktop.live_instrumentation import (
    LiveJobIdentity,
    instrument_gridworld_for_live_presentation,
)
from resilient_agents.gridworld import ACTION_NAMES, GridWorldEnvironment
from resilient_agents.presentation_observer import (
    bound_presentation_sink,
    emit_gridworld_transition,
    emit_presentation_event,
)
from resilient_agents.protocol_v2 import TabularQScientificStateAdapter
from resilient_agents.protocol_v2_runtime import ProtocolV2RootIdentity
from resilient_agents.protocol_v2_tabular_driver import ProjectTabularPhaseADriver
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
    @staticmethod
    def _root() -> ProtocolV2RootIdentity:
        return ProtocolV2RootIdentity(
            root_id="presentation-runtime-root",
            initialization_seed=5101,
            exploration_seed=5102,
            scenario_seed=5103,
            environment_seed=5104,
            action_disturbance_seed=5105,
            observation_disturbance_seed=5106,
        )

    @staticmethod
    def _scenario():
        return fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=5,
            include_change=False,
        )

    def _driver(self) -> tuple[ProjectTabularPhaseADriver, TabularQScientificStateAdapter]:
        agent = TabularQLearningAgent(
            TabularQLearningConfig(
                agent_id="presentation-runtime-q",
                actions=ACTION_NAMES,
                learning_rate=0.2,
                discount_factor=0.9,
                exploration_epsilon=0.2,
                learning_enabled=True,
                bootstrap_on_truncation=True,
                initial_q_value=0.0,
            ),
            checkpoint=None,
        )
        adapter = TabularQScientificStateAdapter(agent)
        return (
            ProjectTabularPhaseADriver(
                adapter=adapter,
                scenario=self._scenario(),
                root=self._root(),
            ),
            adapter,
        )

    def test_emit_helper_swallows_sink_failure(self) -> None:
        with bound_presentation_sink(_RaisingSink()):
            emit_presentation_event({"stream_id": "test", "event_type": "noop"})

    def test_gridworld_snapshot_is_copy_only_after_existing_transition(self) -> None:
        scenario = self._scenario()
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

    def test_runtime_instrumentation_preserves_tabular_scientific_state(self) -> None:
        baseline_driver, baseline_adapter = self._driver()
        baseline_driver.train_to_interaction(12)
        baseline_sha = baseline_adapter.state_sha256()
        baseline_driver.close()

        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory).resolve()
            sink = DroppingLiveEventSink(
                writable_root=writable,
                study_id="runtime-invariance",
                flush_interval_seconds=0.01,
            )
            observed_driver, observed_adapter = self._driver()
            identity = LiveJobIdentity(
                phase="phase-a",
                method_id="q_learning",
                root_id=self._root().root_id,
                layout_id=self._scenario().scenario_id,
            )
            try:
                with instrument_gridworld_for_live_presentation(
                    sink=sink,
                    identity=identity,
                ):
                    observed_driver.train_to_interaction(12)
            finally:
                observed_driver.close()
                sink.close()
            observed_sha = observed_adapter.state_sha256()
            frames = DesktopLiveReadModel(writable_root=writable).latest(
                "runtime-invariance"
            )

        self.assertEqual(observed_sha, baseline_sha)
        self.assertGreaterEqual(len(frames), 1)
        self.assertEqual(frames[0].method_id, "q_learning")
        self.assertEqual(frames[0].root_id, self._root().root_id)

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
