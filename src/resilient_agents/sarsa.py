"""Deterministic information-limited tabular SARSA for candidate protocol v1.1.

SARSA uses the same small Agent interface as the other thesis strategies.  The
runner calls ``act(observation)`` before ``observe(transition)``, so a standard
on-policy SARSA backup is deferred until the next ``act`` call has selected the
behavior-policy action A' for the delivered next observation S'.  Terminal (or
non-bootstrapped truncated) transitions are updated immediately with zero
bootstrap.

Only observation, intended action and reward are consumed.  Evaluator-only
optional information is rejected rather than ignored.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .agents import TABULAR_Q_CHECKPOINT_SCHEMA_VERSION
from .contracts import AgentTransition

SARSA_STATE_SCHEMA_VERSION = 1


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


def _validate_seed(value: Any, *, field: str) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or not 0 <= value < 2**64
    ):
        raise ValueError(f"{field} must be an integer in [0, 2**64)")
    return value


def _sha256(value: Mapping[str, Any]) -> str:
    payload = _canonical_json(value, field="serialized SARSA state").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], *, field: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{field} keys mismatch; missing={sorted(expected - actual)}, "
            f"unknown={sorted(actual - expected)}"
        )


def _json_rng_state(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_json_rng_state(item) for item in value]
    if isinstance(value, list):
        return [_json_rng_state(item) for item in value]
    return value


def _tuple_rng_state(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_tuple_rng_state(item) for item in value)
    return value


@dataclass(frozen=True)
class SarsaConfig:
    """Complete explicit configuration for tabular one-step SARSA."""

    agent_id: str
    actions: Sequence[Any]
    learning_rate: float
    discount_factor: float
    exploration_epsilon: float
    bootstrap_on_truncation: bool
    initial_q_value: float

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str) or not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        actions = tuple(self.actions)
        if not actions:
            raise ValueError("actions must be explicit and non-empty")
        keys = tuple(_canonical_json(action, field="action") for action in actions)
        if len(set(keys)) != len(keys):
            raise ValueError("actions must be unique after canonical serialization")
        object.__setattr__(self, "actions", actions)
        _unit_interval(self.learning_rate, field="learning_rate")
        discount = _unit_interval(self.discount_factor, field="discount_factor")
        if discount >= 1.0:
            raise ValueError("discount_factor must be less than 1")
        _unit_interval(self.exploration_epsilon, field="exploration_epsilon")
        if not isinstance(self.bootstrap_on_truncation, bool):
            raise ValueError("bootstrap_on_truncation must be boolean")
        _finite_number(self.initial_q_value, field="initial_q_value")


class SarsaAgent:
    """One-step epsilon-greedy SARSA with strict information boundaries."""

    def __init__(self, config: SarsaConfig, *, checkpoint: Mapping[str, Any] | None) -> None:
        if not isinstance(config, SarsaConfig):
            raise ValueError("config must be SarsaConfig")
        self.config = config
        self.agent_id = config.agent_id
        self._action_by_key = {
            _canonical_json(action, field="action"): action for action in config.actions
        }
        self._base_q_values = self._load_checkpoint(checkpoint)
        self._q_values: dict[tuple[str, str], float] = dict(self._base_q_values)
        self._exploration_rng: random.Random | None = None
        self._initialization_seed: int | None = None
        self._exploration_seed: int | None = None
        self._pending_action: tuple[str, str] | None = None
        self._deferred_update: tuple[str, str, float, str] | None = None
        self._last_step: int | None = None
        self._observed_transition_count = 0

    def _load_checkpoint(self, checkpoint: Mapping[str, Any] | None) -> dict[tuple[str, str], float]:
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
        checkpoint_keys = tuple(
            _canonical_json(action, field="checkpoint action") for action in raw_actions
        )
        if checkpoint_keys != tuple(self._action_by_key):
            raise ValueError("checkpoint actions must exactly match configured actions")
        if _finite_number(
            checkpoint["initial_q_value"], field="checkpoint.initial_q_value"
        ) != float(self.config.initial_q_value):
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
            pair = (state_key, action_key)
            if pair in loaded:
                raise ValueError("checkpoint contains duplicate state/action values")
            loaded[pair] = _finite_number(item["value"], field="checkpoint Q value")
        return loaded

    def reset(self, *, initialization_seed: int, exploration_seed: int) -> None:
        self._initialization_seed = _validate_seed(initialization_seed, field="initialization_seed")
        self._exploration_seed = _validate_seed(exploration_seed, field="exploration_seed")
        self._exploration_rng = random.Random(self._exploration_seed)
        self._q_values = dict(self._base_q_values)
        self._pending_action = None
        self._deferred_update = None
        self._last_step = None
        self._observed_transition_count = 0

    def _require_reset(self) -> random.Random:
        if self._exploration_rng is None:
            raise RuntimeError("agent must be reset before use")
        return self._exploration_rng

    def _q_value(self, state_key: str, action_key: str) -> float:
        return self._q_values.get((state_key, action_key), float(self.config.initial_q_value))

    def _select_action_key(self, state_key: str) -> str:
        rng = self._require_reset()
        action_keys = tuple(self._action_by_key)
        if rng.random() < float(self.config.exploration_epsilon):
            return rng.choice(action_keys)
        values = [self._q_value(state_key, key) for key in action_keys]
        best = max(values)
        tied = tuple(
            key for key, value in zip(action_keys, values, strict=True) if value == best
        )
        return rng.choice(tied)

    def _update(
        self,
        *,
        state_key: str,
        action_key: str,
        reward: float,
        bootstrap: float,
    ) -> None:
        old = self._q_value(state_key, action_key)
        target = reward + float(self.config.discount_factor) * bootstrap
        updated = old + float(self.config.learning_rate) * (target - old)
        if not math.isfinite(updated):
            raise ValueError("SARSA update produced a non-finite value")
        self._q_values[(state_key, action_key)] = updated

    def act(self, observation: Any) -> Any:
        self._require_reset()
        if self._pending_action is not None:
            raise RuntimeError("observe must consume the previous action before act")
        state_key = _canonical_json(observation, field="observation")
        action_key = self._select_action_key(state_key)

        # Standard SARSA: choose A' under the current behavior policy first,
        # then use Q(S', A') in the previous transition's backup.
        if self._deferred_update is not None:
            prior_state, prior_action, reward, expected_next_state = self._deferred_update
            if state_key != expected_next_state:
                raise ValueError("next act observation does not match deferred SARSA transition")
            self._update(
                state_key=prior_state,
                action_key=prior_action,
                reward=reward,
                bootstrap=self._q_value(state_key, action_key),
            )
            self._deferred_update = None

        self._pending_action = (state_key, action_key)
        return self._action_by_key[action_key]

    def observe(self, transition: AgentTransition) -> None:
        self._require_reset()
        if not isinstance(transition, AgentTransition):
            raise ValueError("transition must be AgentTransition")
        if not isinstance(transition.optional_information, Mapping):
            raise ValueError("transition.optional_information must be an object")
        if transition.optional_information:
            raise ValueError("SARSA forbids optional evaluator information")
        if self._pending_action is None:
            raise RuntimeError("act must precede observe")
        if self._deferred_update is not None:
            raise RuntimeError("deferred SARSA update must be consumed by act first")
        if not isinstance(transition.step, int) or isinstance(transition.step, bool):
            raise ValueError("transition.step must be an integer")
        if self._last_step is not None and transition.step <= self._last_step:
            raise ValueError("transition steps must be strictly increasing")
        if not isinstance(transition.terminated, bool) or not isinstance(transition.truncated, bool):
            raise ValueError("terminated and truncated must be boolean")

        state_key, action_key = self._pending_action
        delivered_action_key = _canonical_json(
            transition.intended_action, field="transition intended_action"
        )
        if delivered_action_key != action_key:
            raise ValueError("transition intended_action does not match the pending action")
        next_state_key = _canonical_json(transition.observation, field="transition observation")
        reward = _finite_number(transition.reward, field="transition reward")
        terminal_boundary = transition.terminated or (
            transition.truncated and not self.config.bootstrap_on_truncation
        )

        self._pending_action = None
        if terminal_boundary:
            self._update(
                state_key=state_key,
                action_key=action_key,
                reward=reward,
                bootstrap=0.0,
            )
        elif transition.truncated:
            # A bootstrapped truncation has no next executed action in this
            # episode. Select one under the behavior policy solely for the
            # configured continuation estimate, then discard it at the boundary.
            bootstrap_action = self._select_action_key(next_state_key)
            self._update(
                state_key=state_key,
                action_key=action_key,
                reward=reward,
                bootstrap=self._q_value(next_state_key, bootstrap_action),
            )
        else:
            self._deferred_update = (state_key, action_key, reward, next_state_key)

        self._last_step = transition.step
        self._observed_transition_count += 1

    def end_episode(self, summary: Mapping[str, Any]) -> None:
        self._require_reset()
        if not isinstance(summary, Mapping):
            raise ValueError("episode summary must be an object")
        if self._pending_action is not None:
            raise RuntimeError("cannot end an episode with an unobserved action")
        if self._deferred_update is not None:
            raise RuntimeError("cannot end an episode with an unresolved SARSA update")

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
            "actions": [_json_value(key) for key in self._action_by_key],
            "initial_q_value": float(self.config.initial_q_value),
            "q_values": entries,
        }

    def checkpoint_sha256(self) -> str:
        return _sha256(self.checkpoint())

    def get_state(self) -> Mapping[str, Any]:
        return {
            "schema_version": SARSA_STATE_SCHEMA_VERSION,
            "agent_id": self.agent_id,
            "method": "sarsa_v1",
            "initialized": self._exploration_rng is not None,
            "initialization_seed": self._initialization_seed,
            "exploration_seed": self._exploration_seed,
            "last_step": self._last_step,
            "observed_transition_count": self._observed_transition_count,
            "pending_action": None
            if self._pending_action is None
            else {
                "state": _json_value(self._pending_action[0]),
                "action": _json_value(self._pending_action[1]),
            },
            "deferred_update": None
            if self._deferred_update is None
            else {
                "state": _json_value(self._deferred_update[0]),
                "action": _json_value(self._deferred_update[1]),
                "reward": self._deferred_update[2],
                "next_state": _json_value(self._deferred_update[3]),
            },
            "checkpoint_sha256": self.checkpoint_sha256(),
            "checkpoint": self.checkpoint(),
            "exploration_rng_state": None
            if self._exploration_rng is None
            else _json_rng_state(self._exploration_rng.getstate()),
        }

    def state_sha256(self) -> str:
        return _sha256(self.get_state())

    def restore_state(self, state: Mapping[str, Any]) -> None:
        if not isinstance(state, Mapping):
            raise ValueError("state must be an object")
        expected = {
            "schema_version", "agent_id", "method", "initialized",
            "initialization_seed", "exploration_seed", "last_step",
            "observed_transition_count", "pending_action", "deferred_update",
            "checkpoint_sha256", "checkpoint", "exploration_rng_state",
        }
        _require_exact_keys(state, expected, field="state")
        if state["schema_version"] != SARSA_STATE_SCHEMA_VERSION:
            raise ValueError("unsupported SARSA state schema_version")
        if state["agent_id"] != self.agent_id or state["method"] != "sarsa_v1":
            raise ValueError("state identity does not match SARSA configuration")
        if not isinstance(state["initialized"], bool) or not state["initialized"]:
            raise ValueError("only initialized SARSA states can be restored")
        init_seed = _validate_seed(state["initialization_seed"], field="state.initialization_seed")
        explore_seed = _validate_seed(state["exploration_seed"], field="state.exploration_seed")
        restored_q = self._load_checkpoint(state["checkpoint"])
        if _sha256(state["checkpoint"]) != state["checkpoint_sha256"]:
            raise ValueError("state checkpoint checksum mismatch")
        count = state["observed_transition_count"]
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("state.observed_transition_count must be integer >= 0")
        last_step = state["last_step"]
        if last_step is not None and (
            not isinstance(last_step, int) or isinstance(last_step, bool)
        ):
            raise ValueError("state.last_step must be integer or null")

        pending_action: tuple[str, str] | None = None
        raw_pending = state["pending_action"]
        if raw_pending is not None:
            if not isinstance(raw_pending, Mapping):
                raise ValueError("state.pending_action must be object or null")
            _require_exact_keys(raw_pending, {"state", "action"}, field="state.pending_action")
            action_key = _canonical_json(raw_pending["action"], field="pending action")
            if action_key not in self._action_by_key:
                raise ValueError("state.pending_action contains unknown action")
            pending_action = (
                _canonical_json(raw_pending["state"], field="pending state"), action_key
            )

        deferred: tuple[str, str, float, str] | None = None
        raw_deferred = state["deferred_update"]
        if raw_deferred is not None:
            if not isinstance(raw_deferred, Mapping):
                raise ValueError("state.deferred_update must be object or null")
            _require_exact_keys(
                raw_deferred, {"state", "action", "reward", "next_state"},
                field="state.deferred_update",
            )
            action_key = _canonical_json(raw_deferred["action"], field="deferred action")
            if action_key not in self._action_by_key:
                raise ValueError("state.deferred_update contains unknown action")
            deferred = (
                _canonical_json(raw_deferred["state"], field="deferred state"),
                action_key,
                _finite_number(raw_deferred["reward"], field="deferred reward"),
                _canonical_json(raw_deferred["next_state"], field="deferred next_state"),
            )
        if pending_action is not None and deferred is not None:
            raise ValueError("state cannot contain both pending action and deferred update")

        raw_rng = state["exploration_rng_state"]
        if raw_rng is None:
            raise ValueError("initialized state must contain exploration RNG state")
        rng = random.Random()
        try:
            rng.setstate(_tuple_rng_state(raw_rng))
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid serialized RNG state") from exc

        self._initialization_seed = init_seed
        self._exploration_seed = explore_seed
        self._exploration_rng = rng
        self._q_values = restored_q
        self._pending_action = pending_action
        self._deferred_update = deferred
        self._last_step = last_step
        self._observed_transition_count = count
