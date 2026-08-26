"""Explicit known-answer fixtures for T-210; not scientific defaults."""
from __future__ import annotations

from resilient_agents.contracts import ChangeEvent, InformationPolicy, ScenarioSpec
from resilient_agents.environment import EnvironmentSeeds


def fixture_seeds(
    *,
    action_disturbance: int,
    observation_disturbance: int,
) -> EnvironmentSeeds:
    return EnvironmentSeeds(
        scenario=101,
        environment=202,
        action_disturbance=action_disturbance,
        observation_disturbance=observation_disturbance,
    )


def prototype_fixture(
    *,
    action_failure_probability: float,
    observation_corruption_probability: float,
    max_steps: int,
    include_change: bool,
) -> ScenarioSpec:
    change_events = (
        ChangeEvent(
            event_id="persistent-right-to-down",
            change_type="action-remap",
            onset_step=2,
            persistent=True,
            affected_mechanism="transition",
            severity={"remapped_actions": 1},
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
        scenario_id="t210-known-answer-v1",
        environment_id="gridworld-prototype-v1",
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
        observation_spec={"type": "position", "coordinate_order": "x-y"},
        action_disturbance_spec={
            "type": "no-op-failure",
            "failure_probability": action_failure_probability,
        },
        observation_disturbance_spec={
            "type": "position-mislocalization",
            "mislocalization_probability": observation_corruption_probability,
        },
        change_events=change_events,
        information_policy=InformationPolicy(
            expose_executed_action=False,
            expose_disturbance_flags=False,
            expose_change_indicator=False,
            expose_regime_id=False,
            expose_true_state=False,
        ),
    )
