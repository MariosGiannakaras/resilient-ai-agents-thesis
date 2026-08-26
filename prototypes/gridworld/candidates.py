"""Same-contract GridWorld candidates for the bounded T-210 comparison.

The shared harness owns the thesis-specific information and disturbance
semantics. Candidate backends own only grid mechanics. This makes inherited
framework behavior visible: the MiniGrid candidate must translate or bypass
orientation, mission, observation, action, and reward conventions to expose
the same four-neighbour contract as the minimal Gymnasium candidate.
"""
from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from enum import IntEnum
from typing import Any, Mapping, Sequence

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall
from minigrid.minigrid_env import MiniGridEnv

from resilient_agents.contracts import (
    ChangeEvent,
    GroundTruthTransition,
    InformationPolicy,
    ScenarioSpec,
)
from resilient_agents.environment import EnvironmentSeeds


class Action(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


ACTION_NAMES = tuple(action.name.lower() for action in Action)


def _coordinate(value: Any, *, field: str) -> tuple[int, int]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{field} must be a two-item coordinate")
    if not all(isinstance(component, int) and not isinstance(component, bool) for component in value):
        raise ValueError(f"{field} components must be integers")
    return int(value[0]), int(value[1])


def _probability(value: Any, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if not 0.0 <= result <= 1.0:
        raise ValueError(f"{field} must be between 0 and 1")
    return result


@dataclass(frozen=True)
class ResolvedPrototypeScenario:
    scenario_id: str
    environment_id: str
    width: int
    height: int
    start: tuple[int, int]
    goal: tuple[int, int]
    obstacles: frozenset[tuple[int, int]]
    max_steps: int
    action_vectors: Mapping[str, tuple[int, int]]
    step_reward: float
    collision_reward: float
    goal_reward: float
    action_failure_probability: float
    observation_corruption_probability: float
    change_events: tuple[ChangeEvent, ...]
    information_policy: InformationPolicy

    @classmethod
    def from_spec(cls, spec: ScenarioSpec) -> "ResolvedPrototypeScenario":
        grid = spec.initial_state_spec.get("grid")
        if not isinstance(grid, Mapping):
            raise ValueError("initial_state_spec.grid must be explicit")
        width = grid.get("width")
        height = grid.get("height")
        if not isinstance(width, int) or isinstance(width, bool) or width <= 1:
            raise ValueError("grid width must be an integer greater than 1")
        if not isinstance(height, int) or isinstance(height, bool) or height <= 1:
            raise ValueError("grid height must be an integer greater than 1")

        start = _coordinate(grid.get("start"), field="grid.start")
        goal = _coordinate(grid.get("goal"), field="grid.goal")
        raw_obstacles = grid.get("obstacles")
        if not isinstance(raw_obstacles, (list, tuple)):
            raise ValueError("grid.obstacles must be explicit")
        obstacles = frozenset(
            _coordinate(value, field="grid.obstacles") for value in raw_obstacles
        )

        def in_bounds(coordinate: tuple[int, int]) -> bool:
            return 0 <= coordinate[0] < width and 0 <= coordinate[1] < height

        if not in_bounds(start) or not in_bounds(goal):
            raise ValueError("start and goal must be in bounds")
        if start == goal or start in obstacles or goal in obstacles:
            raise ValueError("start, goal, and obstacles must be distinct")
        if any(not in_bounds(obstacle) for obstacle in obstacles):
            raise ValueError("all obstacles must be in bounds")

        raw_vectors = spec.dynamics_spec.get("action_vectors")
        if not isinstance(raw_vectors, Mapping) or set(raw_vectors) != set(ACTION_NAMES):
            raise ValueError("all four action vectors must be explicit")
        action_vectors = {
            name: _coordinate(raw_vectors[name], field=f"action_vectors.{name}")
            for name in ACTION_NAMES
        }
        if any(abs(dx) + abs(dy) != 1 for dx, dy in action_vectors.values()):
            raise ValueError("action vectors must be four-neighbour unit moves")

        if spec.observation_spec != {"type": "position", "coordinate_order": "x-y"}:
            raise ValueError("prototype observation schema must be explicit x-y position")

        required_rewards = {"step", "collision", "goal"}
        if set(spec.reward_spec) != required_rewards:
            raise ValueError("step, collision, and goal rewards must be explicit")
        try:
            step_reward = float(spec.reward_spec["step"])
            collision_reward = float(spec.reward_spec["collision"])
            goal_reward = float(spec.reward_spec["goal"])
        except (TypeError, ValueError) as exc:
            raise ValueError("prototype rewards must be numeric") from exc

        failure_probability = _probability(
            spec.action_disturbance_spec.get("failure_probability"),
            field="action failure probability",
        )
        corruption_probability = _probability(
            spec.observation_disturbance_spec.get("mislocalization_probability"),
            field="observation corruption probability",
        )

        events = tuple(spec.change_events)
        if len(events) > 1:
            raise ValueError("the bounded prototype supports at most one change event")
        for event in events:
            if event.change_type != "action-remap" or event.affected_mechanism != "transition":
                raise ValueError("prototype change must be an action-remap transition event")
            if not event.persistent:
                raise ValueError("prototype action-remap change must be persistent")
            remap = event.post_change.get("action_remap")
            if not isinstance(remap, Mapping) or set(remap) != set(ACTION_NAMES):
                raise ValueError("post-change action remap must cover all actions")
            if set(remap.values()) != set(ACTION_NAMES):
                raise ValueError("post-change action remap must be a permutation")

        return cls(
            scenario_id=spec.scenario_id,
            environment_id=spec.environment_id,
            width=width,
            height=height,
            start=start,
            goal=goal,
            obstacles=obstacles,
            max_steps=spec.max_steps,
            action_vectors=action_vectors,
            step_reward=step_reward,
            collision_reward=collision_reward,
            goal_reward=goal_reward,
            action_failure_probability=failure_probability,
            observation_corruption_probability=corruption_probability,
            change_events=events,
            information_policy=spec.information_policy,
        )


def scenario_to_dict(spec: ScenarioSpec) -> dict[str, Any]:
    return {
        "scenario_id": spec.scenario_id,
        "environment_id": spec.environment_id,
        "max_steps": spec.max_steps,
        "reward_spec": dict(spec.reward_spec),
        "initial_state_spec": dict(spec.initial_state_spec),
        "dynamics_spec": dict(spec.dynamics_spec),
        "observation_spec": dict(spec.observation_spec),
        "action_disturbance_spec": dict(spec.action_disturbance_spec),
        "observation_disturbance_spec": dict(spec.observation_disturbance_spec),
        "change_events": [asdict(event) for event in spec.change_events],
        "information_policy": asdict(spec.information_policy),
    }


def scenario_from_dict(payload: Mapping[str, Any]) -> ScenarioSpec:
    return ScenarioSpec(
        scenario_id=str(payload["scenario_id"]),
        environment_id=str(payload["environment_id"]),
        max_steps=int(payload["max_steps"]),
        reward_spec=dict(payload["reward_spec"]),
        initial_state_spec=dict(payload["initial_state_spec"]),
        dynamics_spec=dict(payload["dynamics_spec"]),
        observation_spec=dict(payload["observation_spec"]),
        action_disturbance_spec=dict(payload["action_disturbance_spec"]),
        observation_disturbance_spec=dict(payload["observation_disturbance_spec"]),
        change_events=tuple(ChangeEvent(**event) for event in payload["change_events"]),
        information_policy=InformationPolicy(**payload["information_policy"]),
    )


def scenario_json(spec: ScenarioSpec) -> str:
    return json.dumps(scenario_to_dict(spec), sort_keys=True, separators=(",", ":"))


class _CustomMechanics:
    backend_id = "custom-gymnasium"

    def __init__(self, scenario: ResolvedPrototypeScenario) -> None:
        self.scenario = scenario
        self.position = scenario.start

    def reset(self, *, seed: int) -> tuple[int, int]:
        del seed
        self.position = self.scenario.start
        return self.position

    def move(self, action: Action | None) -> tuple[tuple[int, int], bool, bool]:
        if action is None:
            return self.position, False, self.position == self.scenario.goal
        dx, dy = self.scenario.action_vectors[action.name.lower()]
        candidate = self.position[0] + dx, self.position[1] + dy
        blocked = (
            candidate in self.scenario.obstacles
            or not 0 <= candidate[0] < self.scenario.width
            or not 0 <= candidate[1] < self.scenario.height
        )
        if not blocked:
            self.position = candidate
        return self.position, blocked, self.position == self.scenario.goal

    def debug_state(self) -> tuple[int, int]:
        return self.position

    def close(self) -> None:
        return None


class _FixtureMiniGridEnv(MiniGridEnv):
    def __init__(self, scenario: ResolvedPrototypeScenario) -> None:
        self.prototype_scenario = scenario
        super().__init__(
            mission_space=MissionSpace(mission_func=lambda: "reach the goal"),
            width=scenario.width + 2,
            height=scenario.height + 2,
            max_steps=scenario.max_steps,
            see_through_walls=True,
            render_mode="rgb_array",
        )

    def _gen_grid(self, width: int, height: int) -> None:
        self.grid = Grid(width, height)
        self.grid.wall_rect(0, 0, width, height)
        for x, y in self.prototype_scenario.obstacles:
            self.put_obj(Wall(), x + 1, y + 1)
        goal_x, goal_y = self.prototype_scenario.goal
        self.put_obj(Goal(), goal_x + 1, goal_y + 1)
        start_x, start_y = self.prototype_scenario.start
        self.agent_pos = start_x + 1, start_y + 1
        self.agent_dir = 0
        self.mission = "reach the goal"

    def _reward(self) -> float:
        return self.prototype_scenario.goal_reward


class _MiniGridMechanics:
    backend_id = "minigrid-adaptation"
    _DIRECTION = {
        Action.RIGHT: 0,
        Action.DOWN: 1,
        Action.LEFT: 2,
        Action.UP: 3,
    }

    def __init__(self, scenario: ResolvedPrototypeScenario) -> None:
        self.scenario = scenario
        self.env = _FixtureMiniGridEnv(scenario)

    @property
    def position(self) -> tuple[int, int]:
        if self.env.agent_pos is None:
            raise RuntimeError("MiniGrid backend has not been reset")
        return int(self.env.agent_pos[0]) - 1, int(self.env.agent_pos[1]) - 1

    def reset(self, *, seed: int) -> tuple[int, int]:
        self.env.reset(seed=seed)
        return self.position

    def move(self, action: Action | None) -> tuple[tuple[int, int], bool, bool]:
        before = self.position
        if action is None:
            internal_action = self.env.actions.done
        else:
            self.env.agent_dir = self._DIRECTION[action]
            internal_action = self.env.actions.forward
        _, _, terminated, _, _ = self.env.step(internal_action)
        after = self.position
        blocked = action is not None and after == before and after != self.scenario.goal
        return after, blocked, bool(terminated)

    def debug_state(self) -> tuple[int, int]:
        return self.position

    def close(self) -> None:
        self.env.close()


class _BasePrototype(gym.Env[np.ndarray, int]):
    metadata = {"render_modes": []}
    mechanics_type: type[_CustomMechanics] | type[_MiniGridMechanics]

    def __init__(self, spec: ScenarioSpec) -> None:
        super().__init__()
        self.spec = spec
        self.scenario = ResolvedPrototypeScenario.from_spec(spec)
        self.mechanics = self.mechanics_type(self.scenario)
        self.environment_id = f"{self.scenario.environment_id}:{self.mechanics.backend_id}"
        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.MultiDiscrete(
            np.array([self.scenario.width, self.scenario.height], dtype=np.int64)
        )
        self.last_transition: GroundTruthTransition | None = None
        self._seeds: EnvironmentSeeds | None = None
        self._action_rng: random.Random | None = None
        self._observation_rng: random.Random | None = None
        self._step = 0
        self._finished = False

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        if options is None or not isinstance(options.get("environment_seeds"), EnvironmentSeeds):
            raise ValueError("reset requires explicit EnvironmentSeeds in options")
        seeds = options["environment_seeds"]
        if seed is not None and seed != seeds.environment:
            raise ValueError("Gymnasium seed must match EnvironmentSeeds.environment")
        super().reset(seed=seeds.environment)
        self._seeds = seeds
        self._action_rng = random.Random(seeds.action_disturbance)
        self._observation_rng = random.Random(seeds.observation_disturbance)
        state = self.mechanics.reset(seed=seeds.environment)
        self._step = 0
        self._finished = False
        self.last_transition = None
        return np.asarray(state, dtype=np.int64), {}

    def _active_remap(self) -> tuple[dict[str, str], str, tuple[str, ...]]:
        remap = {name: name for name in ACTION_NAMES}
        regime_id = "nominal"
        onset_ids: list[str] = []
        for event in self.scenario.change_events:
            if event.onset_step == self._step:
                onset_ids.append(event.event_id)
            if event.onset_step <= self._step:
                remap = dict(event.post_change["action_remap"])
                regime_id = event.event_id
        return remap, regime_id, tuple(onset_ids)

    def _deliver_observation(self, true_state: tuple[int, int]) -> tuple[tuple[int, int], bool]:
        if self._observation_rng is None:
            raise RuntimeError("environment has not been reset")
        corrupted = (
            self._observation_rng.random()
            < self.scenario.observation_corruption_probability
        )
        if not corrupted:
            return true_state, False
        candidates = [
            (x, y)
            for x in range(self.scenario.width)
            for y in range(self.scenario.height)
            if (x, y) != true_state and (x, y) not in self.scenario.obstacles
        ]
        return self._observation_rng.choice(candidates), True

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        if self._seeds is None or self._action_rng is None:
            raise RuntimeError("environment must be reset before step")
        if self._finished:
            raise RuntimeError("cannot step a terminated or truncated episode")
        if not self.action_space.contains(action):
            raise ValueError(f"invalid action: {action!r}")

        intended = Action(int(action))
        remap, regime_id, onset_ids = self._active_remap()
        failed = self._action_rng.random() < self.scenario.action_failure_probability
        executed = None if failed else Action[remap[intended.name.lower()].upper()]
        true_state, collided, terminated = self.mechanics.move(executed)
        truncated = not terminated and self._step + 1 >= self.scenario.max_steps
        reward = (
            self.scenario.goal_reward
            if terminated
            else self.scenario.collision_reward
            if collided
            else self.scenario.step_reward
        )
        delivered, corrupted = self._deliver_observation(true_state)
        transition = GroundTruthTransition(
            step=self._step,
            true_state=true_state,
            delivered_observation=delivered,
            intended_action=intended.name.lower(),
            executed_action="noop" if executed is None else executed.name.lower(),
            reward=reward,
            terminated=terminated,
            truncated=truncated,
            regime_id=regime_id,
            disturbance_flags={
                "action_failure": failed,
                "observation_corruption": corrupted,
            },
            change_event_ids=onset_ids,
        )
        self.last_transition = transition
        self._step += 1
        self._finished = terminated or truncated
        return np.asarray(delivered, dtype=np.int64), reward, terminated, truncated, {}

    def render_debug(self) -> Mapping[str, Any]:
        return {
            "backend": self.mechanics.backend_id,
            "position": self.mechanics.debug_state(),
        }

    def close(self) -> None:
        self.mechanics.close()


class CustomGymnasiumPrototype(_BasePrototype):
    mechanics_type = _CustomMechanics


class MiniGridPrototype(_BasePrototype):
    mechanics_type = _MiniGridMechanics


class PrototypeResearchAdapter:
    """Expose a candidate through the accepted ResearchEnvironment contract."""

    def __init__(self, candidate: _BasePrototype) -> None:
        self.candidate = candidate
        self.environment_id = candidate.environment_id

    def reset(self, *, seeds: EnvironmentSeeds) -> tuple[int, int]:
        observation, info = self.candidate.reset(
            seed=seeds.environment,
            options={"environment_seeds": seeds},
        )
        if info:
            raise RuntimeError("prototype reset leaked evaluator information")
        return int(observation[0]), int(observation[1])

    def step(self, intended_action: int) -> GroundTruthTransition:
        _, _, _, _, info = self.candidate.step(intended_action)
        if info:
            raise RuntimeError("prototype step leaked evaluator information")
        if self.candidate.last_transition is None:
            raise RuntimeError("candidate did not record a ground-truth transition")
        return self.candidate.last_transition
