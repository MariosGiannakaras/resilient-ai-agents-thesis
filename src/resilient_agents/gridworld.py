"""Project-owned GridWorld with explicit research and information semantics.

The environment has no scientific defaults: callers supply a complete
``ScenarioSpec`` and four independent environment seed channels. Gymnasium
provides the API/spaces boundary; this module owns the thesis mechanics.
"""
from __future__ import annotations

import json
import math
import random
from collections import deque
from dataclasses import asdict, dataclass
from enum import IntEnum
from numbers import Integral
from typing import Any, Mapping, Sequence

import gymnasium as gym
from gymnasium import spaces

from .contracts import (
    ChangeEvent,
    GroundTruthTransition,
    InformationPolicy,
    ScenarioSpec,
)
from .environment import EnvironmentSeeds

GRIDWORLD_SCHEMA_VERSION = 1


class GridAction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


ACTION_NAMES = tuple(action.name.lower() for action in GridAction)
Coordinate = tuple[int, int]


def _coordinate(value: Any, *, field: str) -> Coordinate:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{field} must be a two-item coordinate")
    if not all(isinstance(item, int) and not isinstance(item, bool) for item in value):
        raise ValueError(f"{field} components must be integers")
    return int(value[0]), int(value[1])


def _probability(value: Any, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{field} must be finite and between 0 and 1")
    return result


def _reward(value: Any, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], *, field: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise ValueError(f"{field} keys mismatch; missing={missing}, unknown={unknown}")


def _action_mapping(value: Any, *, field: str) -> tuple[GridAction, ...]:
    if not isinstance(value, Mapping) or set(value) != set(ACTION_NAMES):
        raise ValueError(f"{field} must cover exactly {ACTION_NAMES}")
    if not all(isinstance(item, str) for item in value.values()):
        raise ValueError(f"{field} values must be action names")
    if set(value.values()) != set(ACTION_NAMES):
        raise ValueError(f"{field} must be a permutation of {ACTION_NAMES}")
    return tuple(GridAction[str(value[name]).upper()] for name in ACTION_NAMES)


@dataclass(frozen=True)
class ResolvedGridWorldScenario:
    """Validated immutable mechanics extracted from the generic scenario contract."""

    scenario_id: str
    environment_id: str
    width: int
    height: int
    start: Coordinate
    goal: Coordinate
    obstacles: frozenset[Coordinate]
    max_steps: int
    action_vectors: tuple[Coordinate, ...]
    step_reward: float
    collision_reward: float
    goal_reward: float
    action_failure_probability: float
    observation_corruption_probability: float
    change_event: ChangeEvent | None
    post_change_action_mapping: tuple[GridAction, ...] | None
    information_policy: InformationPolicy

    @classmethod
    def from_spec(cls, spec: ScenarioSpec) -> "ResolvedGridWorldScenario":
        if not isinstance(spec.information_policy, InformationPolicy):
            raise ValueError("information_policy must be explicit")
        if not isinstance(spec.max_steps, int) or isinstance(spec.max_steps, bool):
            raise ValueError("max_steps must be an integer")
        if not isinstance(spec.initial_state_spec, Mapping):
            raise ValueError("initial_state_spec must be an object")
        _require_exact_keys(spec.initial_state_spec, {"grid"}, field="initial_state_spec")
        grid = spec.initial_state_spec["grid"]
        if not isinstance(grid, Mapping):
            raise ValueError("initial_state_spec.grid must be an object")
        _require_exact_keys(
            grid,
            {"width", "height", "start", "goal", "obstacles"},
            field="initial_state_spec.grid",
        )
        width = grid["width"]
        height = grid["height"]
        if not isinstance(width, int) or isinstance(width, bool) or width <= 1:
            raise ValueError("grid width must be an integer greater than 1")
        if not isinstance(height, int) or isinstance(height, bool) or height <= 1:
            raise ValueError("grid height must be an integer greater than 1")

        start = _coordinate(grid["start"], field="grid.start")
        goal = _coordinate(grid["goal"], field="grid.goal")
        raw_obstacles = grid["obstacles"]
        if not isinstance(raw_obstacles, (list, tuple)):
            raise ValueError("grid.obstacles must be an explicit sequence")
        obstacle_sequence = tuple(
            _coordinate(item, field="grid.obstacles") for item in raw_obstacles
        )
        if len(set(obstacle_sequence)) != len(obstacle_sequence):
            raise ValueError("grid.obstacles must not contain duplicates")
        obstacles = frozenset(obstacle_sequence)

        def in_bounds(coordinate: Coordinate) -> bool:
            return 0 <= coordinate[0] < width and 0 <= coordinate[1] < height

        if not in_bounds(start) or not in_bounds(goal):
            raise ValueError("start and goal must be in bounds")
        if start == goal or start in obstacles or goal in obstacles:
            raise ValueError("start, goal, and obstacles must be distinct")
        if any(not in_bounds(obstacle) for obstacle in obstacles):
            raise ValueError("all obstacles must be in bounds")

        if not isinstance(spec.dynamics_spec, Mapping):
            raise ValueError("dynamics_spec must be an object")
        _require_exact_keys(spec.dynamics_spec, {"action_vectors"}, field="dynamics_spec")
        raw_vectors = spec.dynamics_spec["action_vectors"]
        if not isinstance(raw_vectors, Mapping) or set(raw_vectors) != set(ACTION_NAMES):
            raise ValueError(f"action_vectors must cover exactly {ACTION_NAMES}")
        action_vectors = tuple(
            _coordinate(raw_vectors[name], field=f"action_vectors.{name}")
            for name in ACTION_NAMES
        )
        canonical_vectors = ((0, -1), (1, 0), (0, 1), (-1, 0))
        if action_vectors != canonical_vectors:
            raise ValueError("action vectors must use the canonical up/right/down/left moves")

        if spec.observation_spec != {
            "type": "position",
            "coordinate_order": "x-y",
            "reset_observation": "true-state",
        }:
            raise ValueError(
                "observation_spec must explicitly select x-y position and true-state reset"
            )

        if not isinstance(spec.reward_spec, Mapping):
            raise ValueError("reward_spec must be an object")
        _require_exact_keys(spec.reward_spec, {"step", "collision", "goal"}, field="reward_spec")
        step_reward = _reward(spec.reward_spec["step"], field="reward_spec.step")
        collision_reward = _reward(
            spec.reward_spec["collision"], field="reward_spec.collision"
        )
        goal_reward = _reward(spec.reward_spec["goal"], field="reward_spec.goal")

        if not isinstance(spec.action_disturbance_spec, Mapping):
            raise ValueError("action_disturbance_spec must be an object")
        _require_exact_keys(
            spec.action_disturbance_spec,
            {"type", "failure_probability"},
            field="action_disturbance_spec",
        )
        if spec.action_disturbance_spec["type"] != "no-op-failure":
            raise ValueError("action disturbance type must be no-op-failure")
        failure_probability = _probability(
            spec.action_disturbance_spec["failure_probability"],
            field="action failure probability",
        )

        if not isinstance(spec.observation_disturbance_spec, Mapping):
            raise ValueError("observation_disturbance_spec must be an object")
        _require_exact_keys(
            spec.observation_disturbance_spec,
            {"type", "mislocalization_probability"},
            field="observation_disturbance_spec",
        )
        if spec.observation_disturbance_spec["type"] != "position-mislocalization":
            raise ValueError("observation disturbance type must be position-mislocalization")
        corruption_probability = _probability(
            spec.observation_disturbance_spec["mislocalization_probability"],
            field="observation corruption probability",
        )

        if not isinstance(spec.change_events, (list, tuple)):
            raise ValueError("change_events must be an explicit sequence")
        events = tuple(spec.change_events)
        if len(events) > 1:
            raise ValueError("GridWorld schema v1 supports at most one persistent change")
        event = events[0] if events else None
        post_mapping: tuple[GridAction, ...] | None = None
        if event is not None:
            if not isinstance(event, ChangeEvent):
                raise ValueError("change_events must contain ChangeEvent values")
            if event.change_type != "action-remap":
                raise ValueError("change_type must be action-remap")
            if event.affected_mechanism != "transition" or not event.persistent:
                raise ValueError("action-remap change must be persistent transition change")
            if event.onset_step >= spec.max_steps:
                raise ValueError("change onset_step must occur before max_steps")
            if not isinstance(event.pre_change, Mapping) or not isinstance(
                event.post_change, Mapping
            ):
                raise ValueError("change pre_change and post_change must be objects")
            _require_exact_keys(event.pre_change, {"action_remap"}, field="pre_change")
            _require_exact_keys(event.post_change, {"action_remap"}, field="post_change")
            identity = tuple(GridAction)
            if _action_mapping(event.pre_change.get("action_remap"), field="pre_change") != identity:
                raise ValueError("pre-change action mapping must be identity")
            post_mapping = _action_mapping(
                event.post_change.get("action_remap"), field="post_change"
            )
            if post_mapping == identity:
                raise ValueError("post-change action mapping must change at least one action")
            if not isinstance(event.severity, Mapping):
                raise ValueError("change severity must be an object")
            _require_exact_keys(event.severity, {"remapped_actions"}, field="severity")
            remapped_actions = event.severity["remapped_actions"]
            actual_remapped = sum(
                before != after for before, after in zip(identity, post_mapping, strict=True)
            )
            if (
                not isinstance(remapped_actions, int)
                or isinstance(remapped_actions, bool)
                or remapped_actions != actual_remapped
            ):
                raise ValueError("severity.remapped_actions must match the action mapping")

        cls._validate_nominal_reachability(
            width=width,
            height=height,
            start=start,
            goal=goal,
            obstacles=obstacles,
            action_vectors=action_vectors,
        )
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
            change_event=event,
            post_change_action_mapping=post_mapping,
            information_policy=spec.information_policy,
        )

    @staticmethod
    def _validate_nominal_reachability(
        *,
        width: int,
        height: int,
        start: Coordinate,
        goal: Coordinate,
        obstacles: frozenset[Coordinate],
        action_vectors: Sequence[Coordinate],
    ) -> None:
        frontier = deque([start])
        visited = {start}
        while frontier:
            current = frontier.popleft()
            if current == goal:
                return
            for dx, dy in action_vectors:
                candidate = current[0] + dx, current[1] + dy
                if (
                    0 <= candidate[0] < width
                    and 0 <= candidate[1] < height
                    and candidate not in obstacles
                    and candidate not in visited
                ):
                    visited.add(candidate)
                    frontier.append(candidate)
        raise ValueError("goal must be reachable from start under nominal dynamics")


def gridworld_scenario_to_dict(spec: ScenarioSpec) -> dict[str, Any]:
    """Return the canonical schema-v1 JSON-compatible representation."""

    ResolvedGridWorldScenario.from_spec(spec)
    return {
        "gridworld_schema_version": GRIDWORLD_SCHEMA_VERSION,
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


def gridworld_scenario_from_dict(payload: Mapping[str, Any]) -> ScenarioSpec:
    """Load and validate one exact schema-v1 scenario without coercive defaults."""

    if not isinstance(payload, Mapping):
        raise ValueError("GridWorld scenario payload must be an object")
    expected = {
        "gridworld_schema_version",
        "scenario_id",
        "environment_id",
        "max_steps",
        "reward_spec",
        "initial_state_spec",
        "dynamics_spec",
        "observation_spec",
        "action_disturbance_spec",
        "observation_disturbance_spec",
        "change_events",
        "information_policy",
    }
    _require_exact_keys(payload, expected, field="GridWorld scenario")
    if payload["gridworld_schema_version"] != GRIDWORLD_SCHEMA_VERSION:
        raise ValueError("unsupported GridWorld scenario schema version")
    if not isinstance(payload["change_events"], (list, tuple)):
        raise ValueError("change_events must be a sequence")
    try:
        events = tuple(ChangeEvent(**dict(item)) for item in payload["change_events"])
        policy = InformationPolicy(**dict(payload["information_policy"]))
        spec = ScenarioSpec(
            scenario_id=payload["scenario_id"],
            environment_id=payload["environment_id"],
            max_steps=payload["max_steps"],
            reward_spec=dict(payload["reward_spec"]),
            initial_state_spec=dict(payload["initial_state_spec"]),
            dynamics_spec=dict(payload["dynamics_spec"]),
            observation_spec=dict(payload["observation_spec"]),
            action_disturbance_spec=dict(payload["action_disturbance_spec"]),
            observation_disturbance_spec=dict(payload["observation_disturbance_spec"]),
            change_events=events,
            information_policy=policy,
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ValueError("invalid GridWorld scenario payload") from exc
    ResolvedGridWorldScenario.from_spec(spec)
    return spec


def gridworld_scenario_json(spec: ScenarioSpec) -> str:
    return json.dumps(
        gridworld_scenario_to_dict(spec), sort_keys=True, separators=(",", ":")
    )


class GridWorldGymEnv(gym.Env[Coordinate, int]):
    """Gymnasium mechanics surface; evaluator truth stays out of ``info``."""

    metadata = {"render_modes": []}

    def __init__(self, spec: ScenarioSpec) -> None:
        super().__init__()
        self.spec = spec
        self.scenario = ResolvedGridWorldScenario.from_spec(spec)
        self.environment_id = self.scenario.environment_id
        self.action_space = spaces.Discrete(len(GridAction))
        self.observation_space = spaces.MultiDiscrete(
            [self.scenario.width, self.scenario.height]
        )
        self.last_transition: GroundTruthTransition | None = None
        self._position = self.scenario.start
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
    ) -> tuple[Coordinate, dict[str, Any]]:
        if options is None or not isinstance(options.get("environment_seeds"), EnvironmentSeeds):
            raise ValueError("reset requires explicit EnvironmentSeeds in options")
        seeds = options["environment_seeds"]
        if seed is not None and seed != seeds.environment:
            raise ValueError("Gymnasium seed must match EnvironmentSeeds.environment")
        super().reset(seed=seeds.environment)
        self._seeds = seeds
        self._action_rng = random.Random(seeds.action_disturbance)
        self._observation_rng = random.Random(seeds.observation_disturbance)
        self._position = self.scenario.start
        self._step = 0
        self._finished = False
        self.last_transition = None
        return self._position, {}

    def _active_mapping(self) -> tuple[tuple[GridAction, ...], str, tuple[str, ...]]:
        identity = tuple(GridAction)
        event = self.scenario.change_event
        if event is None or self._step < event.onset_step:
            return identity, "nominal", ()
        onset = (event.event_id,) if self._step == event.onset_step else ()
        if self.scenario.post_change_action_mapping is None:
            raise RuntimeError("resolved change mapping is unavailable")
        return self.scenario.post_change_action_mapping, event.event_id, onset

    def _move(self, action: GridAction | None) -> tuple[Coordinate, bool, bool]:
        if action is None:
            return self._position, False, self._position == self.scenario.goal
        dx, dy = self.scenario.action_vectors[int(action)]
        candidate = self._position[0] + dx, self._position[1] + dy
        collided = (
            candidate in self.scenario.obstacles
            or not 0 <= candidate[0] < self.scenario.width
            or not 0 <= candidate[1] < self.scenario.height
        )
        if not collided:
            self._position = candidate
        return self._position, collided, self._position == self.scenario.goal

    def _deliver_observation(self) -> tuple[Coordinate, bool]:
        if self._observation_rng is None:
            raise RuntimeError("environment has not been reset")
        corrupted = (
            self._observation_rng.random()
            < self.scenario.observation_corruption_probability
        )
        if not corrupted:
            return self._position, False
        alternatives = [
            (x, y)
            for x in range(self.scenario.width)
            for y in range(self.scenario.height)
            if (x, y) != self._position and (x, y) not in self.scenario.obstacles
        ]
        return self._observation_rng.choice(alternatives), True

    def step(self, action: int) -> tuple[Coordinate, float, bool, bool, dict[str, Any]]:
        if self._seeds is None or self._action_rng is None:
            raise RuntimeError("environment must be reset before step")
        if self._finished:
            raise RuntimeError("cannot step a terminated or truncated episode")
        if isinstance(action, bool) or not isinstance(action, Integral):
            raise ValueError(f"invalid action: {action!r}")
        action_value = int(action)
        if not self.action_space.contains(action_value):
            raise ValueError(f"invalid action: {action!r}")

        intended = GridAction(action_value)
        mapping, regime_id, onset_ids = self._active_mapping()
        failed = self._action_rng.random() < self.scenario.action_failure_probability
        executed = None if failed else mapping[int(intended)]
        true_state, collided, terminated = self._move(executed)
        truncated = not terminated and self._step + 1 >= self.scenario.max_steps
        reward = (
            self.scenario.goal_reward
            if terminated
            else self.scenario.collision_reward
            if collided
            else self.scenario.step_reward
        )
        delivered, corrupted = self._deliver_observation()
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
        return delivered, reward, terminated, truncated, {}

    def debug_state(self) -> Mapping[str, Any]:
        event = self.scenario.change_event
        regime_id = (
            event.event_id
            if event is not None and self._step > event.onset_step
            else "nominal"
        )
        return {
            "schema_version": GRIDWORLD_SCHEMA_VERSION,
            "position": self._position,
            "goal": self.scenario.goal,
            "obstacles": tuple(sorted(self.scenario.obstacles)),
            "step": self._step,
            "regime_id": regime_id,
        }


class GridWorldEnvironment:
    """Accepted ``ResearchEnvironment`` adapter over the Gymnasium surface."""

    def __init__(self, spec: ScenarioSpec) -> None:
        self.gym_env = GridWorldGymEnv(spec)
        self.environment_id = self.gym_env.environment_id
        self.information_policy = self.gym_env.scenario.information_policy

    def reset(self, *, seeds: EnvironmentSeeds) -> Coordinate:
        if not isinstance(seeds, EnvironmentSeeds):
            raise ValueError("reset requires explicit EnvironmentSeeds")
        observation, info = self.gym_env.reset(
            seed=seeds.environment,
            options={"environment_seeds": seeds},
        )
        if info:
            raise RuntimeError("GridWorld reset leaked evaluator information")
        return observation

    def step(self, intended_action: int) -> GroundTruthTransition:
        _, _, _, _, info = self.gym_env.step(intended_action)
        if info:
            raise RuntimeError("GridWorld step leaked evaluator information")
        if self.gym_env.last_transition is None:
            raise RuntimeError("GridWorld did not record evaluator ground truth")
        return self.gym_env.last_transition

    def debug_state(self) -> Mapping[str, Any]:
        return self.gym_env.debug_state()

    def close(self) -> None:
        self.gym_env.close()
