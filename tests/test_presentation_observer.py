from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.agents import TabularQLearningAgent, TabularQLearningConfig
from resilient_agents.desktop.live_events import DesktopLiveReadModel, DroppingLiveEventSink
from resilient_agents.gridworld import ACTION_NAMES
from resilient_agents.presentation_observer import (
    bound_presentation_sink,
    emit_presentation_event,
)
from resilient_agents.protocol_v2 import TabularQScientificStateAdapter
from resilient_agents.protocol_v2_runtime import ProtocolV2RootIdentity
from resilient_agents.protocol_v2_sb3_gridworld import ExplicitSeededGridWorldEnv
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
            root_id="presentation-observer-root",
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
                agent_id="presentation-observer-q",
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

    def test_failing_presentation_sink_cannot_change_tabular_scientific_state(self) -> None:
        baseline_driver, baseline_adapter = self._driver()
        baseline_driver.train_to_interaction(12)
        baseline_sha = baseline_adapter.state_sha256()
        baseline_driver.close()

        observed_driver, observed_adapter = self._driver()
        with bound_presentation_sink(_RaisingSink()):
            observed_driver.train_to_interaction(12)
        observed_sha = observed_adapter.state_sha256()
        observed_driver.close()

        self.assertEqual(observed_sha, baseline_sha)

    def test_tabular_driver_emits_copy_only_phase_a_snapshots(self) -> None:
        collector = _Collector()
        driver, _ = self._driver()
        with bound_presentation_sink(collector):
            driver.train_to_interaction(4)
        driver.close()

        self.assertEqual(len(collector.events), 4)
        first = collector.events[0]
        self.assertEqual(first["event_type"], "gridworld-transition")
        self.assertEqual(first["phase"], "phase-a")
        self.assertEqual(first["method_id"], "q_learning")
        self.assertEqual(first["root_id"], self._root().root_id)
        self.assertEqual(first["interaction_index"], 1)
        self.assertGreater(first["grid"]["width"], 0)
        self.assertGreater(first["grid"]["height"], 0)

    def test_sb3_gridworld_presentation_metadata_does_not_change_transition(self) -> None:
        scenario = self._scenario()
        seeds = (fixture_seeds(action=71, observation=81),)
        baseline = ExplicitSeededGridWorldEnv(scenario=scenario, episode_seeds=seeds)
        observed = ExplicitSeededGridWorldEnv(
            scenario=scenario,
            episode_seeds=seeds,
            presentation_method_id="dqn",
            presentation_root_id="dev-root",
        )
        collector = _Collector()
        try:
            baseline_reset, _ = baseline.reset()
            observed_reset, _ = observed.reset()
            self.assertEqual(baseline_reset, observed_reset)
            with bound_presentation_sink(collector):
                baseline_step = baseline.step(1)
                observed_step = observed.step(1)
            self.assertEqual(baseline_step, observed_step)
            self.assertEqual(len(collector.events), 1)
            self.assertEqual(collector.events[0]["method_id"], "dqn")
        finally:
            baseline.close()
            observed.close()

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

    def test_emit_helper_swallows_sink_failure(self) -> None:
        with bound_presentation_sink(_RaisingSink()):
            emit_presentation_event({"stream_id": "test", "event_type": "noop"})


if __name__ == "__main__":
    unittest.main()
