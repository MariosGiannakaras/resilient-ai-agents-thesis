from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prototypes.gridworld import (  # noqa: E402
    Action,
    CustomGymnasiumPrototype,
    MiniGridPrototype,
    PrototypeResearchAdapter,
    ResolvedPrototypeScenario,
    scenario_from_dict,
    scenario_to_dict,
)
from prototypes.gridworld.fixtures import fixture_seeds, prototype_fixture  # noqa: E402
from resilient_agents.contracts import project_for_agent  # noqa: E402


CANDIDATES = (CustomGymnasiumPrototype, MiniGridPrototype)


def trace(candidate_type, spec, seeds, actions):
    candidate = candidate_type(spec)
    adapter = PrototypeResearchAdapter(candidate)
    initial = adapter.reset(seeds=seeds)
    transitions = []
    try:
        for action in actions:
            transitions.append(adapter.step(action))
            if transitions[-1].terminated or transitions[-1].truncated:
                break
        return initial, transitions, candidate.render_debug()
    finally:
        candidate.close()


class GridWorldPrototypeComparisonTests(unittest.TestCase):
    def test_candidates_match_known_trace_and_exact_change_onset(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=0.0,
            observation_corruption_probability=0.0,
            max_steps=6,
            include_change=True,
        )
        seeds = fixture_seeds(action_disturbance=1, observation_disturbance=3)
        results = [
            trace(candidate, spec, seeds, [Action.RIGHT] * 4) for candidate in CANDIDATES
        ]
        self.assertEqual(results[0][:2], results[1][:2])
        initial, transitions, _ = results[0]
        self.assertEqual(initial, (0, 1))
        self.assertEqual(
            [transition.true_state for transition in transitions],
            [(1, 1), (2, 1), (2, 2), (2, 3)],
        )
        self.assertEqual(transitions[2].change_event_ids, ("persistent-right-to-down",))
        self.assertEqual(transitions[3].change_event_ids, ())
        self.assertEqual(transitions[2].executed_action, "down")
        self.assertTrue(transitions[-1].terminated)
        self.assertFalse(transitions[-1].truncated)
        self.assertEqual(transitions[-1].reward, 1.0)

    def test_action_failure_is_explicit_and_seeded_replay_is_exact(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=1.0,
            observation_corruption_probability=0.0,
            max_steps=3,
            include_change=False,
        )
        seeds = fixture_seeds(action_disturbance=1, observation_disturbance=3)
        for candidate in CANDIDATES:
            first = trace(candidate, spec, seeds, [Action.RIGHT, Action.RIGHT])
            second = trace(candidate, spec, seeds, [Action.RIGHT, Action.RIGHT])
            self.assertEqual(first, second)
            transition = first[1][0]
            self.assertEqual(transition.intended_action, "right")
            self.assertEqual(transition.executed_action, "noop")
            self.assertTrue(transition.disturbance_flags["action_failure"])
            self.assertEqual(transition.true_state, (0, 1))

    def test_observation_corruption_changes_only_delivered_view(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=0.0,
            observation_corruption_probability=1.0,
            max_steps=3,
            include_change=False,
        )
        seeds = fixture_seeds(action_disturbance=1, observation_disturbance=3)
        for candidate in CANDIDATES:
            _, transitions, _ = trace(candidate, spec, seeds, [Action.RIGHT])
            transition = transitions[0]
            self.assertEqual(transition.true_state, (1, 1))
            self.assertNotEqual(transition.delivered_observation, transition.true_state)
            self.assertTrue(transition.disturbance_flags["observation_corruption"])
            visible = project_for_agent(transition, spec.information_policy)
            self.assertEqual(visible.observation, transition.delivered_observation)
            self.assertEqual(visible.optional_information, {})

    def test_disturbance_rng_streams_are_independently_effective(self) -> None:
        action_spec = prototype_fixture(
            action_failure_probability=0.5,
            observation_corruption_probability=0.0,
            max_steps=3,
            include_change=False,
        )
        observation_spec = prototype_fixture(
            action_failure_probability=0.0,
            observation_corruption_probability=1.0,
            max_steps=3,
            include_change=False,
        )
        for candidate in CANDIDATES:
            action_failed = trace(
                candidate,
                action_spec,
                fixture_seeds(action_disturbance=1, observation_disturbance=3),
                [Action.RIGHT],
            )[1][0]
            action_succeeded = trace(
                candidate,
                action_spec,
                fixture_seeds(action_disturbance=2, observation_disturbance=3),
                [Action.RIGHT],
            )[1][0]
            self.assertTrue(action_failed.disturbance_flags["action_failure"])
            self.assertFalse(action_succeeded.disturbance_flags["action_failure"])
            self.assertEqual(action_failed.delivered_observation, action_failed.true_state)
            self.assertEqual(action_succeeded.delivered_observation, action_succeeded.true_state)

            first_view = trace(
                candidate,
                observation_spec,
                fixture_seeds(action_disturbance=1, observation_disturbance=3),
                [Action.RIGHT],
            )[1][0]
            second_view = trace(
                candidate,
                observation_spec,
                fixture_seeds(action_disturbance=1, observation_disturbance=5),
                [Action.RIGHT],
            )[1][0]
            self.assertEqual(first_view.true_state, second_view.true_state)
            self.assertEqual(first_view.executed_action, second_view.executed_action)
            self.assertNotEqual(
                first_view.delivered_observation,
                second_view.delivered_observation,
            )

    def test_collision_and_truncation_semantics_match(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=0.0,
            observation_corruption_probability=0.0,
            max_steps=2,
            include_change=False,
        )
        seeds = fixture_seeds(action_disturbance=1, observation_disturbance=3)
        for candidate in CANDIDATES:
            _, transitions, _ = trace(candidate, spec, seeds, [Action.LEFT, Action.LEFT])
            self.assertEqual([item.true_state for item in transitions], [(0, 1), (0, 1)])
            self.assertEqual([item.reward for item in transitions], [-0.25, -0.25])
            self.assertFalse(transitions[-1].terminated)
            self.assertTrue(transitions[-1].truncated)

    def test_obstacle_collision_semantics_match(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=0.0,
            observation_corruption_probability=0.0,
            max_steps=4,
            include_change=False,
        )
        seeds = fixture_seeds(action_disturbance=1, observation_disturbance=3)
        for candidate in CANDIDATES:
            _, transitions, _ = trace(candidate, spec, seeds, [Action.UP, Action.RIGHT])
            self.assertEqual(transitions[0].true_state, (0, 0))
            self.assertEqual(transitions[1].true_state, (0, 0))
            self.assertEqual(transitions[1].reward, -0.25)

    def test_serialization_round_trip_preserves_resolved_scenario(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=0.25,
            observation_corruption_probability=0.5,
            max_steps=7,
            include_change=True,
        )
        payload = json.loads(json.dumps(scenario_to_dict(spec), sort_keys=True))
        restored = scenario_from_dict(payload)
        self.assertEqual(
            ResolvedPrototypeScenario.from_spec(spec),
            ResolvedPrototypeScenario.from_spec(restored),
        )

    def test_debug_state_matches_last_recorded_truth_and_no_info_leaks(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=0.0,
            observation_corruption_probability=0.0,
            max_steps=4,
            include_change=False,
        )
        seeds = fixture_seeds(action_disturbance=1, observation_disturbance=3)
        for candidate_type in CANDIDATES:
            initial, transitions, debug = trace(
                candidate_type, spec, seeds, [Action.RIGHT, Action.DOWN]
            )
            self.assertEqual(initial, (0, 1))
            self.assertEqual(debug["position"], transitions[-1].true_state)
            self.assertIn(debug["backend"], {"custom-gymnasium", "minigrid-adaptation"})

    def test_reset_fails_closed_without_explicit_rng_channels(self) -> None:
        spec = prototype_fixture(
            action_failure_probability=0.0,
            observation_corruption_probability=0.0,
            max_steps=4,
            include_change=False,
        )
        for candidate_type in CANDIDATES:
            candidate = candidate_type(spec)
            try:
                with self.assertRaises(ValueError):
                    candidate.reset(seed=202)
            finally:
                candidate.close()


if __name__ == "__main__":
    unittest.main()
