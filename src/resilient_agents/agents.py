"""Small, information-limited tabular agent set selected for the thesis.

The module implements two methods and three declared capability regimes:
frozen/continual tabular Q-learning and frozen finite rectangular robust value
iteration.  Configuration is explicit, state is versioned and serializable,
and evaluator-only transition fields are rejected rather than ignored.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .contracts import AgentTransition

TABULAR_Q_CHECKPOINT_SCHEMA_VERSION = 1
ROBUST_PLAN_SCHEMA_VERSION = 1
_PROBABILITY_TOLERANCE = 1e-12


def _finite_number(value: Any, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _unit_interval(value: Any, *, field: str) -> float:
    result = _finite_number(value, field=field)
    if not 0.0 <= result <= 1.0:
        raise ValueError(f"{field} must be between 0 and 1")
    return result


def _canonical_json(value: Any, *, field: str) -> str:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be JSON-compatible and finite") from exc


def _json_value(key: str) -> Any:
    return json.loads(key)


def _require_exact_keys(
    value: Mapping[str, Any], expected: set[str], *, field: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{field} keys mismatch; "
            f"missing={sorted(expected - actual)}, unknown={sorted(actual - expected)}"
        )


def _validate_seed(value: Any, *, field: str) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or not 0 <= value < 2**64
    ):
        raise ValueError(f"{field} must be an integer in [0, 2**64)")
    return value


def _sha256(payload: Mapping[str, Any]) -> str:
    encoded = _canonical_json(payload, field="serialized agent state").encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class TabularQLearningConfig:
    """Complete configuration for frozen or continual one-step Q-learning."""

    agent_id: str
    actions: Sequence[Any]
    learning_rate: float
    discount_factor: float
    exploration_epsilon: float
    learning_enabled: bool
    bootstrap_on_truncation: bool
    initial_q_value: float

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str) or not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        actions = tuple(self.actions)
        if not actions:
            raise ValueError("actions must be explicit and non-empty")
        action_keys = tuple(
            _canonical_json(action, field="action") for action in actions
        )
        if len(set(action_keys)) != len(action_keys):
            raise ValueError("actions must be unique after canonical serialization")
        object.__setattr__(self, "actions", actions)
        _unit_interval(self.learning_rate, field="learning_rate")
        discount = _unit_interval(self.discount_factor, field="discount_factor")
        if discount >= 1.0:
            raise ValueError("discount_factor must be less than 1")
        _unit_interval(self.exploration_epsilon, field="exploration_epsilon")
        if not isinstance(self.learning_enabled, bool):
            raise ValueError("learning_enabled must be boolean")
        if not isinstance(self.bootstrap_on_truncation, bool):
            raise ValueError("bootstrap_on_truncation must be boolean")
        _finite_number(self.initial_q_value, field="initial_q_value")


class TabularQLearningAgent:
    """One implementation used as frozen F0 and continual C0 regimes."""

    def __init__(
        self,
        config: TabularQLearningConfig,
        *,
        checkpoint: Mapping[str, Any] | None,
    ) -> None:
        if not isinstance(config, TabularQLearningConfig):
            raise ValueError("config must be TabularQLearningConfig")
        self.config = config
        self.agent_id = config.agent_id
        self._action_by_key = {
            _canonical_json(action, field="action"): action for action in config.actions
        }
        self._base_q_values = self._load_checkpoint(checkpoint)
        self._q_values: dict[tuple[str, str], float] = {}
        self._exploration_rng: random.Random | None = None
        self._initialization_seed: int | None = None
        self._exploration_seed: int | None = None
        self._pending: tuple[str, str] | None = None
        self._last_step: int | None = None
        self._observed_transition_count = 0

    def _load_checkpoint(
        self, checkpoint: Mapping[str, Any] | None
    ) -> dict[tuple[str, str], float]:
        if checkpoint is None:
            return {}
        if not isinstance(checkpoint, Mapping):
            raise ValueError("checkpoint must be an object or None")
        _require_exact_keys(
            checkpoint,
            {"schema_version", "actions", "initial_q_value", "q_values"},
            field="checkpoint",
        )
        if checkpoint["schema_version"] != TABULAR_Q_CHECKPOINT_SCHEMA_VERSION:
            raise ValueError("unsupported tabular Q checkpoint schema_version")
        raw_actions = checkpoint["actions"]
        if not isinstance(raw_actions, list):
            raise ValueError("checkpoint.actions must be a list")
        checkpoint_action_keys = tuple(
            _canonical_json(action, field="checkpoint action") for action in raw_actions
        )
        if checkpoint_action_keys != tuple(self._action_by_key):
            raise ValueError("checkpoint actions must exactly match configured actions")
        checkpoint_initial = _finite_number(
            checkpoint["initial_q_value"], field="checkpoint.initial_q_value"
        )
        if checkpoint_initial != float(self.config.initial_q_value):
            raise ValueError("checkpoint initial_q_value must match configuration")
        raw_values = checkpoint["q_values"]
        if not isinstance(raw_values, list):
            raise ValueError("checkpoint.q_values must be a list")
        loaded: dict[tuple[str, str], float] = {}
        for index, item in enumerate(raw_values):
            if not isinstance(item, Mapping):
                raise ValueError(f"checkpoint.q_values[{index}] must be an object")
            _require_exact_keys(
                item, {"state", "action", "value"}, field=f"checkpoint.q_values[{index}]"
            )
            state_key = _canonical_json(item["state"], field="checkpoint state")
            action_key = _canonical_json(item["action"], field="checkpoint action")
            if action_key not in self._action_by_key:
                raise ValueError("checkpoint contains an unknown action")
            key = (state_key, action_key)
            if key in loaded:
                raise ValueError("checkpoint contains duplicate state/action values")
            loaded[key] = _finite_number(item["value"], field="checkpoint Q value")
        return loaded

    def reset(self, *, initialization_seed: int, exploration_seed: int) -> None:
        self._initialization_seed = _validate_seed(
            initialization_seed, field="initialization_seed"
        )
        self._exploration_seed = _validate_seed(
            exploration_seed, field="exploration_seed"
        )
        self._exploration_rng = random.Random(self._exploration_seed)
        self._q_values = dict(self._base_q_values)
        self._pending = None
        self._last_step = None
        self._observed_transition_count = 0

    def _require_reset(self) -> random.Random:
        if self._exploration_rng is None:
            raise RuntimeError("agent must be reset before use")
        return self._exploration_rng

    def _q_value(self, state_key: str, action_key: str) -> float:
        return self._q_values.get(
            (state_key, action_key), float(self.config.initial_q_value)
        )

    def act(self, observation: Any) -> Any:
        rng = self._require_reset()
        if self._pending is not None:
            raise RuntimeError("observe must consume the previous action before act")
        state_key = _canonical_json(observation, field="observation")
        action_keys = tuple(self._action_by_key)
        if rng.random() < float(self.config.exploration_epsilon):
            action_key = rng.choice(action_keys)
        else:
            values = [self._q_value(state_key, key) for key in action_keys]
            best = max(values)
            tied = tuple(
                key for key, value in zip(action_keys, values, strict=True) if value == best
            )
            action_key = rng.choice(tied)
        self._pending = state_key, action_key
        return self._action_by_key[action_key]

    def observe(self, transition: AgentTransition) -> None:
        self._require_reset()
        if not isinstance(transition, AgentTransition):
            raise ValueError("transition must be AgentTransition")
        if transition.optional_information:
            raise ValueError("selected tabular agents forbid optional evaluator information")
        if self._pending is None:
            raise RuntimeError("act must precede observe")
        if not isinstance(transition.step, int) or isinstance(transition.step, bool):
            raise ValueError("transition.step must be an integer")
        if self._last_step is not None and transition.step <= self._last_step:
            raise ValueError("transition steps must be strictly increasing")
        if not isinstance(transition.terminated, bool) or not isinstance(
            transition.truncated, bool
        ):
            raise ValueError("terminated and truncated must be boolean")
        prior_state_key, action_key = self._pending
        delivered_action_key = _canonical_json(
            transition.intended_action, field="transition intended_action"
        )
        if delivered_action_key != action_key:
            raise ValueError("transition intended_action does not match the pending action")
        next_state_key = _canonical_json(
            transition.observation, field="transition observation"
        )
        reward = _finite_number(transition.reward, field="transition reward")
        if self.config.learning_enabled:
            terminal_boundary = transition.terminated or (
                transition.truncated and not self.config.bootstrap_on_truncation
            )
            bootstrap = 0.0
            if not terminal_boundary:
                bootstrap = max(
                    self._q_value(next_state_key, candidate)
                    for candidate in self._action_by_key
                )
            old_value = self._q_value(prior_state_key, action_key)
            target = reward + float(self.config.discount_factor) * bootstrap
            updated = old_value + float(self.config.learning_rate) * (target - old_value)
            if not math.isfinite(updated):
                raise ValueError("Q update produced a non-finite value")
            self._q_values[(prior_state_key, action_key)] = updated
        self._pending = None
        self._last_step = transition.step
        self._observed_transition_count += 1

    def end_episode(self, summary: Mapping[str, Any]) -> None:
        self._require_reset()
        if not isinstance(summary, Mapping):
            raise ValueError("episode summary must be an object")
        if self._pending is not None:
            raise RuntimeError("cannot end an episode with an unobserved action")

    def checkpoint(self) -> dict[str, Any]:
        entries = [
            {
                "state": _json_value(state_key),
                "action": _json_value(action_key),
                "value": value,
            }
            for (state_key, action_key), value in sorted(self._q_values.items())
        ]
        return {
            "schema_version": TABULAR_Q_CHECKPOINT_SCHEMA_VERSION,
            "actions": [
                _json_value(action_key) for action_key in self._action_by_key
            ],
            "initial_q_value": float(self.config.initial_q_value),
            "q_values": entries,
        }

    def checkpoint_sha256(self) -> str:
        return _sha256(self.checkpoint())

    def get_state(self) -> Mapping[str, Any]:
        return {
            "agent_id": self.agent_id,
            "method": "tabular_q_learning_v1",
            "learning_enabled": self.config.learning_enabled,
            "initialized": self._exploration_rng is not None,
            "initialization_seed": self._initialization_seed,
            "exploration_seed": self._exploration_seed,
            "observed_transition_count": self._observed_transition_count,
            "checkpoint_sha256": self.checkpoint_sha256(),
            "checkpoint": self.checkpoint(),
        }


@dataclass(frozen=True)
class RobustTransitionOutcome:
    next_state: Any
    probability: float
    reward: float
    terminal: bool

    def __post_init__(self) -> None:
        _canonical_json(self.next_state, field="next_state")
        _unit_interval(self.probability, field="probability")
        _finite_number(self.reward, field="reward")
        if not isinstance(self.terminal, bool):
            raise ValueError("terminal must be boolean")


@dataclass(frozen=True)
class RobustTransitionRow:
    outcomes: Sequence[RobustTransitionOutcome]

    def __post_init__(self) -> None:
        outcomes = tuple(self.outcomes)
        if not outcomes or not all(
            isinstance(outcome, RobustTransitionOutcome) for outcome in outcomes
        ):
            raise ValueError("outcomes must be a non-empty outcome sequence")
        total = sum(float(outcome.probability) for outcome in outcomes)
        if not math.isclose(
            total, 1.0, rel_tol=0.0, abs_tol=_PROBABILITY_TOLERANCE
        ):
            raise ValueError("transition-row probabilities must sum to 1")
        object.__setattr__(self, "outcomes", outcomes)


@dataclass(frozen=True)
class RobustStateAction:
    state: Any
    action: Any
    candidate_rows: Sequence[RobustTransitionRow]

    def __post_init__(self) -> None:
        _canonical_json(self.state, field="state")
        _canonical_json(self.action, field="action")
        rows = tuple(self.candidate_rows)
        if not rows or not all(isinstance(row, RobustTransitionRow) for row in rows):
            raise ValueError("candidate_rows must be a non-empty row sequence")
        object.__setattr__(self, "candidate_rows", rows)


@dataclass(frozen=True)
class RobustValueIterationConfig:
    """Explicit finite s,a-rectangular robust planning model."""

    agent_id: str
    states: Sequence[Any]
    terminal_states: Sequence[Any]
    actions: Sequence[Any]
    state_actions: Sequence[RobustStateAction]
    discount_factor: float
    convergence_tolerance: float
    max_iterations: int
    initial_value: float
    exploration_epsilon: float

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str) or not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        states = tuple(self.states)
        terminals = tuple(self.terminal_states)
        actions = tuple(self.actions)
        entries = tuple(self.state_actions)
        if not states or not actions:
            raise ValueError("states and actions must be explicit and non-empty")
        state_keys = tuple(_canonical_json(state, field="state") for state in states)
        terminal_keys = tuple(
            _canonical_json(state, field="terminal state") for state in terminals
        )
        action_keys = tuple(_canonical_json(action, field="action") for action in actions)
        if len(set(state_keys)) != len(state_keys):
            raise ValueError("states must be unique")
        if len(set(terminal_keys)) != len(terminal_keys):
            raise ValueError("terminal_states must be unique")
        if not set(terminal_keys).issubset(state_keys):
            raise ValueError("terminal_states must be a subset of states")
        if len(set(action_keys)) != len(action_keys):
            raise ValueError("actions must be unique")
        if not all(isinstance(entry, RobustStateAction) for entry in entries):
            raise ValueError("state_actions must contain RobustStateAction values")
        expected = {
            (state_key, action_key)
            for state_key in state_keys
            if state_key not in set(terminal_keys)
            for action_key in action_keys
        }
        actual: set[tuple[str, str]] = set()
        for entry in entries:
            state_key = _canonical_json(entry.state, field="state_action state")
            action_key = _canonical_json(entry.action, field="state_action action")
            key = (state_key, action_key)
            if key in actual:
                raise ValueError("state_actions contains a duplicate state/action")
            actual.add(key)
            for row in entry.candidate_rows:
                for outcome in row.outcomes:
                    next_key = _canonical_json(outcome.next_state, field="outcome next_state")
                    if next_key not in set(state_keys):
                        raise ValueError("outcome next_state is not a configured state")
                    if outcome.terminal != (next_key in set(terminal_keys)):
                        raise ValueError(
                            "outcome terminal flag must match terminal_states membership"
                        )
        if actual != expected:
            raise ValueError("state_actions must exactly cover nonterminal state/action pairs")
        discount = _unit_interval(self.discount_factor, field="discount_factor")
        if discount >= 1.0:
            raise ValueError("discount_factor must be less than 1")
        tolerance = _finite_number(
            self.convergence_tolerance, field="convergence_tolerance"
        )
        if tolerance <= 0.0:
            raise ValueError("convergence_tolerance must be greater than 0")
        if (
            not isinstance(self.max_iterations, int)
            or isinstance(self.max_iterations, bool)
            or self.max_iterations <= 0
        ):
            raise ValueError("max_iterations must be a positive integer")
        _finite_number(self.initial_value, field="initial_value")
        _unit_interval(self.exploration_epsilon, field="exploration_epsilon")
        object.__setattr__(self, "states", states)
        object.__setattr__(self, "terminal_states", terminals)
        object.__setattr__(self, "actions", actions)
        object.__setattr__(self, "state_actions", entries)


class RectangularRobustValueIterationAgent:
    """Frozen deployment policy from finite rectangular robust value iteration."""

    def __init__(self, config: RobustValueIterationConfig) -> None:
        if not isinstance(config, RobustValueIterationConfig):
            raise ValueError("config must be RobustValueIterationConfig")
        self.config = config
        self.agent_id = config.agent_id
        self._state_by_key = {
            _canonical_json(state, field="state"): state for state in config.states
        }
        self._terminal_keys = {
            _canonical_json(state, field="terminal state")
            for state in config.terminal_states
        }
        self._action_by_key = {
            _canonical_json(action, field="action"): action for action in config.actions
        }
        self._entries = {
            (
                _canonical_json(entry.state, field="state_action state"),
                _canonical_json(entry.action, field="state_action action"),
            ): entry
            for entry in config.state_actions
        }
        self._values, self._q_values, self._iterations, self._residual = self._plan()
        self._exploration_rng: random.Random | None = None
        self._initialization_seed: int | None = None
        self._exploration_seed: int | None = None
        self._pending_action_key: str | None = None
        self._last_step: int | None = None
        self._observed_transition_count = 0

    def _backup(
        self, state_key: str, action_key: str, values: Mapping[str, float]
    ) -> float:
        entry = self._entries[(state_key, action_key)]
        row_returns = []
        for row in entry.candidate_rows:
            row_return = 0.0
            for outcome in row.outcomes:
                next_key = _canonical_json(outcome.next_state, field="outcome next_state")
                continuation = 0.0 if outcome.terminal else values[next_key]
                row_return += float(outcome.probability) * (
                    float(outcome.reward)
                    + float(self.config.discount_factor) * continuation
                )
            row_returns.append(row_return)
        return min(row_returns)

    def _plan(
        self,
    ) -> tuple[dict[str, float], dict[tuple[str, str], float], int, float]:
        values = {
            state_key: (
                0.0
                if state_key in self._terminal_keys
                else float(self.config.initial_value)
            )
            for state_key in self._state_by_key
        }
        action_keys = tuple(self._action_by_key)
        residual = math.inf
        for iteration in range(1, self.config.max_iterations + 1):
            next_values = dict(values)
            for state_key in self._state_by_key:
                if state_key in self._terminal_keys:
                    continue
                next_values[state_key] = max(
                    self._backup(state_key, action_key, values)
                    for action_key in action_keys
                )
            residual = max(
                abs(next_values[state_key] - values[state_key])
                for state_key in self._state_by_key
            )
            values = next_values
            if residual <= float(self.config.convergence_tolerance):
                q_values = {
                    (state_key, action_key): self._backup(
                        state_key, action_key, values
                    )
                    for state_key in self._state_by_key
                    if state_key not in self._terminal_keys
                    for action_key in action_keys
                }
                return values, q_values, iteration, residual
        raise ValueError(
            "robust value iteration did not converge within max_iterations; "
            f"final residual={residual}"
        )

    def reset(self, *, initialization_seed: int, exploration_seed: int) -> None:
        self._initialization_seed = _validate_seed(
            initialization_seed, field="initialization_seed"
        )
        self._exploration_seed = _validate_seed(
            exploration_seed, field="exploration_seed"
        )
        self._exploration_rng = random.Random(self._exploration_seed)
        self._pending_action_key = None
        self._last_step = None
        self._observed_transition_count = 0

    def _require_reset(self) -> random.Random:
        if self._exploration_rng is None:
            raise RuntimeError("agent must be reset before use")
        return self._exploration_rng

    def act(self, observation: Any) -> Any:
        rng = self._require_reset()
        if self._pending_action_key is not None:
            raise RuntimeError("observe must consume the previous action before act")
        state_key = _canonical_json(observation, field="observation")
        if state_key not in self._state_by_key:
            raise ValueError("observation is not in the robust planning state space")
        if state_key in self._terminal_keys:
            raise ValueError("cannot act from a terminal state")
        action_keys = tuple(self._action_by_key)
        if rng.random() < float(self.config.exploration_epsilon):
            action_key = rng.choice(action_keys)
        else:
            values = [self._q_values[(state_key, key)] for key in action_keys]
            best = max(values)
            tied = tuple(
                key for key, value in zip(action_keys, values, strict=True) if value == best
            )
            action_key = rng.choice(tied)
        self._pending_action_key = action_key
        return self._action_by_key[action_key]

    def observe(self, transition: AgentTransition) -> None:
        self._require_reset()
        if not isinstance(transition, AgentTransition):
            raise ValueError("transition must be AgentTransition")
        if transition.optional_information:
            raise ValueError("robust deployment forbids optional evaluator information")
        if self._pending_action_key is None:
            raise RuntimeError("act must precede observe")
        if not isinstance(transition.step, int) or isinstance(transition.step, bool):
            raise ValueError("transition.step must be an integer")
        if self._last_step is not None and transition.step <= self._last_step:
            raise ValueError("transition steps must be strictly increasing")
        delivered_action_key = _canonical_json(
            transition.intended_action, field="transition intended_action"
        )
        if delivered_action_key != self._pending_action_key:
            raise ValueError("transition intended_action does not match the pending action")
        _canonical_json(transition.observation, field="transition observation")
        _finite_number(transition.reward, field="transition reward")
        if not isinstance(transition.terminated, bool) or not isinstance(
            transition.truncated, bool
        ):
            raise ValueError("terminated and truncated must be boolean")
        self._pending_action_key = None
        self._last_step = transition.step
        self._observed_transition_count += 1

    def end_episode(self, summary: Mapping[str, Any]) -> None:
        self._require_reset()
        if not isinstance(summary, Mapping):
            raise ValueError("episode summary must be an object")
        if self._pending_action_key is not None:
            raise RuntimeError("cannot end an episode with an unobserved action")

    def plan(self) -> dict[str, Any]:
        return {
            "schema_version": ROBUST_PLAN_SCHEMA_VERSION,
            "method": "rectangular_robust_value_iteration_v1",
            "iterations": self._iterations,
            "residual": self._residual,
            "values": [
                {"state": _json_value(state_key), "value": value}
                for state_key, value in sorted(self._values.items())
            ],
            "q_values": [
                {
                    "state": _json_value(state_key),
                    "action": _json_value(action_key),
                    "value": value,
                }
                for (state_key, action_key), value in sorted(self._q_values.items())
            ],
        }

    def plan_sha256(self) -> str:
        return _sha256(self.plan())

    def get_state(self) -> Mapping[str, Any]:
        return {
            "agent_id": self.agent_id,
            "method": "rectangular_robust_value_iteration_v1",
            "initialized": self._exploration_rng is not None,
            "initialization_seed": self._initialization_seed,
            "exploration_seed": self._exploration_seed,
            "observed_transition_count": self._observed_transition_count,
            "plan_sha256": self.plan_sha256(),
            "plan": self.plan(),
        }
