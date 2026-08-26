from __future__ import annotations

import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import (  # noqa: E402
    ChangeEvent,
    InformationPolicy,
    ScenarioSpec,
    project_for_agent,
)
from resilient_agents.environment import EnvironmentSeeds  # noqa: E402
from resilient_agents.gridworld import (  # noqa: E402
    GRIDWORLD_SCHEMA_VERSION,
    GridAction,
    GridWorldEnvironment,
    GridWorldGymEnv,
    ResolvedGridWorldScenario,
    gridworld_scenario_from_dict,
    gridworld_scenario_json,
    gridworld_scenario_to_dict,
)


STRICT_POLICY = InformationPolicy(False, False, False, False, False)


def fixture_seeds(*, action: int = 1, observation: int = 3) -> EnvironmentSeeds:
    return EnvironmentSeeds(
        scenario=101,
        environment=202,
        action_disturbance=action,
        observation_disturbance=observation,
    )


def fixture_spec(
    *,
    action_failure: float,
    observation_corruption: float,
    max_steps: int,
    include_change: bool,
) -> ScenarioSpec:
    events = (
        ChangeEvent(
            event_id="persistent-right-to-down",
            change_type="action-remap",
            onset_step=2,
            persistent=True,
            affected_mechanism="transition",
            severity={"remapped_actions": 2},
            pre_change={
                "action_remap": {
                    "up": "up",
                    "right": "right",
                    "down": "down",
                    "left": "left",
                }
            },
            post_change={
                "action_remap": {
                    "up": "up",
                    "right": "down",
                    "down": "right",
                    "left": "left",
                }
            },
        ),
    ) if include_change else ()
    return ScenarioSpec(
        scenario_id="t213-known-answer-v1",
        environment_id="project-gridworld-v1",
        max_steps=max_steps,
        reward_spec={"step": -0.1, "collision": -0.25, "goal": 1.0},
        initial_state_spec={
            "grid": {
                "width": 5,
                "height": 4,
                "start": [0, 1],
                "goal": [2, 3],
                "obstacles": [[1, 0]],
            }
        },
        dynamics_spec={
            "action_vectors": {
                "up": [0, -1],
                "right": [1, 0],
                "down": [0, 1],
                "left": [-1, 0],
            }
        },
        observation_spec={
            "type": "position",
            "coordinate_order": "x-y",
            "reset_observation": "true-state",
        },
        action_disturbance_spec={
            "type": "no-op-failure",
            "failure_probability": action_failure,
        },
        observation_disturbance_spec={
            "type": "position-mislocalization",
            "mislocalization_probability": observation_corruption,
        },
        change_events=events,
        information_policy=STRICT_POLICY,
    )


def trace(
    spec: ScenarioSpec,
    seeds: EnvironmentSeeds,
    actions: list[GridAction],
):
    environment = GridWorldEnvironment(spec)
    initial = environment.reset(seeds=seeds)
    transitions = []
    try:
        for action in actions:
            transitions.append(environment.step(action))
            if transitions[-1].terminated or transitions[-1].truncated:
                break
        return initial, transitions, environment.debug_state()
    finally:
        environment.close()


class GridWorldKnownAnswerTests(unittest.TestCase):
    def test_reference_trace_has_exact_persistent_change_onset(self) -> None:
        spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=6,
            include_change=True,
        )
        initial, transitions, debug = trace(
            spec, fixture_seeds(), [GridAction.RIGHT] * 4
        )
        self.assertEqual(initial, (0, 1))
        self.assertEqual(
            [item.true_state for item in transitions],
            [(1, 1), (2, 1), (2, 2), (2, 3)],
        )
        self.assertEqual(
            [item.executed_action for item in transitions],
            ["right", "right", "down", "down"],
        )
        self.assertEqual(transitions[2].change_event_ids, ("persistent-right-to-down",))
        self.assertEqual(transitions[3].change_event_ids, ())
        self.assertEqual(transitions[3].regime_id, "persistent-right-to-down")
        self.assertEqual(transitions[-1].reward, 1.0)
        self.assertTrue(transitions[-1].terminated)
        self.assertFalse(transitions[-1].truncated)
        self.assertEqual(debug["position"], transitions[-1].true_state)
        self.assertEqual(debug["regime_id"], "persistent-right-to-down")

    def test_boundary_obstacle_and_truncation_semantics(self) -> None:
        spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=4,
            include_change=False,
        )
        _, transitions, _ = trace(
            spec,
            fixture_seeds(),
            [GridAction.LEFT, GridAction.UP, GridAction.RIGHT, GridAction.LEFT],
        )
        self.assertEqual(
            [item.true_state for item in transitions],
            [(0, 1), (0, 0), (0, 0), (0, 0)],
        )
        self.assertEqual(
            [item.reward for item in transitions],
            [-0.25, -0.1, -0.25, -0.25],
        )
        self.assertFalse(transitions[-1].terminated)
        self.assertTrue(transitions[-1].truncated)

    def test_reset_isolates_episode_state_and_replay_is_exact(self) -> None:
        spec = fixture_spec(
            action_failure=0.5,
            observation_corruption=0.5,
            max_steps=5,
            include_change=False,
        )
        environment = GridWorldEnvironment(spec)
        seeds = fixture_seeds()
        try:
            first_initial = environment.reset(seeds=seeds)
            first = [environment.step(GridAction.RIGHT) for _ in range(2)]
            second_initial = environment.reset(seeds=seeds)
            second = [environment.step(GridAction.RIGHT) for _ in range(2)]
        finally:
            environment.close()
        self.assertEqual(first_initial, (0, 1))
        self.assertEqual(second_initial, (0, 1))
        self.assertEqual(first, second)


class GridWorldDisturbanceAndInformationTests(unittest.TestCase):
    def test_action_failure_is_explicit_and_preserves_intended_action(self) -> None:
        spec = fixture_spec(
            action_failure=1.0,
            observation_corruption=0.0,
            max_steps=3,
            include_change=False,
        )
        _, transitions, _ = trace(spec, fixture_seeds(), [GridAction.RIGHT])
        transition = transitions[0]
        self.assertEqual(transition.intended_action, "right")
        self.assertEqual(transition.executed_action, "noop")
        self.assertEqual(transition.true_state, (0, 1))
        self.assertTrue(transition.disturbance_flags["action_failure"])

    def test_observation_corruption_does_not_mutate_or_leak_truth(self) -> None:
        spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=1.0,
            max_steps=3,
            include_change=False,
        )
        _, transitions, _ = trace(spec, fixture_seeds(), [GridAction.RIGHT])
        transition = transitions[0]
        self.assertEqual(transition.true_state, (1, 1))
        self.assertNotEqual(transition.delivered_observation, transition.true_state)
        self.assertTrue(transition.disturbance_flags["observation_corruption"])
        visible = project_for_agent(transition, spec.information_policy)
        self.assertEqual(visible.observation, transition.delivered_observation)
        self.assertEqual(visible.optional_information, {})

    def test_action_and_observation_rng_streams_are_independent(self) -> None:
        action_spec = fixture_spec(
            action_failure=0.5,
            observation_corruption=0.0,
            max_steps=3,
            include_change=False,
        )
        failed = trace(action_spec, fixture_seeds(action=1), [GridAction.RIGHT])[1][0]
        succeeded = trace(action_spec, fixture_seeds(action=2), [GridAction.RIGHT])[1][0]
        self.assertTrue(failed.disturbance_flags["action_failure"])
        self.assertFalse(succeeded.disturbance_flags["action_failure"])
        self.assertEqual(failed.delivered_observation, failed.true_state)
        self.assertEqual(succeeded.delivered_observation, succeeded.true_state)

        observation_spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=1.0,
            max_steps=3,
            include_change=False,
        )
        first = trace(
            observation_spec, fixture_seeds(observation=3), [GridAction.RIGHT]
        )[1][0]
        second = trace(
            observation_spec, fixture_seeds(observation=5), [GridAction.RIGHT]
        )[1][0]
        self.assertEqual(first.true_state, second.true_state)
        self.assertEqual(first.executed_action, second.executed_action)
        self.assertNotEqual(first.delivered_observation, second.delivered_observation)

    def test_evaluator_truth_never_uses_gymnasium_info(self) -> None:
        spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=3,
            include_change=False,
        )
        environment = GridWorldGymEnv(spec)
        try:
            _, reset_info = environment.reset(
                seed=202,
                options={"environment_seeds": fixture_seeds()},
            )
            _, _, _, _, step_info = environment.step(GridAction.RIGHT)
        finally:
            environment.close()
        self.assertEqual(reset_info, {})
        self.assertEqual(step_info, {})
        self.assertIsNotNone(environment.last_transition)


class GridWorldContractTests(unittest.TestCase):
    def test_scenario_serialization_is_versioned_and_canonical(self) -> None:
        spec = fixture_spec(
            action_failure=0.25,
            observation_corruption=0.5,
            max_steps=7,
            include_change=True,
        )
        encoded = gridworld_scenario_json(spec)
        payload = json.loads(encoded)
        self.assertEqual(payload["gridworld_schema_version"], GRIDWORLD_SCHEMA_VERSION)
        restored = gridworld_scenario_from_dict(payload)
        self.assertEqual(
            ResolvedGridWorldScenario.from_spec(spec),
            ResolvedGridWorldScenario.from_spec(restored),
        )
        self.assertEqual(encoded, gridworld_scenario_json(restored))

    def test_invalid_or_ambiguous_configuration_fails_closed(self) -> None:
        spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=4,
            include_change=False,
        )
        invalid_observation = replace(spec, observation_spec={"type": "position"})
        with self.assertRaises(ValueError):
            GridWorldEnvironment(invalid_observation)

        payload = gridworld_scenario_to_dict(spec)
        payload["unexpected"] = True
        with self.assertRaises(ValueError):
            gridworld_scenario_from_dict(payload)

        blocked_grid = {
            "grid": {
                "width": 3,
                "height": 3,
                "start": [0, 0],
                "goal": [2, 2],
                "obstacles": [[1, 0], [1, 1], [1, 2]],
            }
        }
        with self.assertRaises(ValueError):
            GridWorldEnvironment(replace(spec, initial_state_spec=blocked_grid))

        changed = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=4,
            include_change=True,
        )
        inconsistent_event = replace(changed.change_events[0], severity={"remapped_actions": 1})
        with self.assertRaises(ValueError):
            GridWorldEnvironment(replace(changed, change_events=(inconsistent_event,)))

    def test_reset_and_lifecycle_require_explicit_valid_state(self) -> None:
        spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=1,
            include_change=False,
        )
        environment = GridWorldGymEnv(spec)
        try:
            with self.assertRaises(ValueError):
                environment.reset(seed=202)
            with self.assertRaises(RuntimeError):
                environment.step(GridAction.RIGHT)
            environment.reset(seed=202, options={"environment_seeds": fixture_seeds()})
            environment.step(GridAction.RIGHT)
            with self.assertRaises(RuntimeError):
                environment.step(GridAction.RIGHT)
        finally:
            environment.close()


if __name__ == "__main__":
    unittest.main()
