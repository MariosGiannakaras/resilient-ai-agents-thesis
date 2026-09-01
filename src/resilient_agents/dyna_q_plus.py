"""Information-limited tabular Dyna-Q+ agent for the v1.1 thesis refinement.

D0 deliberately uses only the same observation, intended-action and reward
surface available to F0/C0.  It never receives executed-action, change,
disturbance, regime or true-state evaluator information.  The learned model is
therefore a model of *experienced agent-visible dynamics*, which is the
scientifically relevant constraint under action/observation uncertainty.

The implementation uses:

* one-step Q-learning on every real transition;
* an empirical stochastic model for experienced state/action pairs;
* the standard Dyna-Q+ self-loop/zero-reward model for actions not yet tried in
  an already visited state;
* a recency exploration bonus only on planning backups; and
* independent deterministic action-selection and planning RNGs supplied by the
  existing two-seed Agent.reset contract.

No scientific defaults are hidden here.  D0-specific planning_steps and kappa
must be supplied explicitly and selected only on non-final tuning evidence.
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

DYNA_Q_PLUS_STATE_SCHEMA_VERSION = 1


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


def _require_exact_keys(
    value: Mapping[str, Any], expected: set[str], *, field: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{field} keys mismatch; "
            f"missing={sorted(expected - actual)}, unknown={sorted(actual - expected)}"
        )


def _sha256(payload: Mapping[str, Any]) -> str:
    encoded = _canonical_json(payload, field="serialized Dyna-Q+ state").encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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
class DynaQPlusConfig:
    """Complete explicit configuration for D0 Dyna-Q+."""

    agent_id: str
    actions: Sequence[Any]
    learning_rate: float
    discount_factor: float
    exploration_epsilon: float
    planning_steps: int
    kappa: float
    bootstrap_on_truncation: bool
    initial_q_value: float

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str) or not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        actions = tuple(self.actions)
        if not actions:
            raise ValueError("actions must be explicit and non-empty")
        action_keys = tuple(_canonical_json(action, field="action") for action in actions)
        if len(set(action_keys)) != len(action_keys):
            raise ValueError("actions must be unique after canonical serialization")
        object.__setattr__(self, "actions", actions)
        _unit_interval(self.learning_rate, field="learning_rate")
        discount = _unit_interval(self.discount_factor, field="discount_factor")
        if discount >= 1.0:
            raise ValueError("discount_factor must be less than 1")
        _unit_interval(self.exploration_epsilon, field="exploration_epsilon")
        if (
            not isinstance(self.planning_steps, int)
            or isinstance(self.planning_steps, bool)
            or self.planning_steps < 0
        ):
            raise ValueError("planning_steps must be an integer >= 0")
        kappa = _finite_number(self.kappa, field="kappa")
        if kappa < 0.0:
            raise ValueError("kappa must be >= 0")
        if not isinstance(self.bootstrap_on_truncation, bool):
            raise ValueError("bootstrap_on_truncation must be boolean")
        _finite_number(self.initial_q_value, field="initial_q_value")


@dataclass
class _OutcomeStats:
    next_state_key: str
    terminal: bool
    count: int
    mean_reward: float


class DynaQPlusAgent:
    """Tabular Dyna-Q+ using only agent-visible transition information."""

    def __init__(
        self,
        config: DynaQPlusConfig,
        *,
        checkpoint: Mapping[str, Any] | None,
    ) -> None:
        if not isinstance(config, DynaQPlusConfig):
            raise ValueError("config must be DynaQPlusConfig")
        self.config = config
        self.agent_id = config.agent_id
        self._action_by_key = {
            _canonical_json(action, field="action"): action for action in config.actions
        }
        self._base_q_values = self._load_checkpoint(checkpoint)
        self._q_values: dict[tuple[str, str], float] = dict(self._base_q_values)
        self._model: dict[tuple[str, str], dict[tuple[str, bool], _OutcomeStats]] = {}
        self._experienced: set[tuple[str, str]] = set()
        self._last_real_visit: dict[tuple[str, str], int] = {}
        self._exploration_rng: random.Random | None = None
        self._planning_rng: random.Random | None = None
        self._initialization_seed: int | None = None
        self._exploration_seed: int | None = None
        self._pending: tuple[str, str] | None = None
        self._last_step: int | None = None
        self._time = 0
        self._observed_transition_count = 0
        self._planning_update_count = 0

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
                item,
                {"state", "action", "value"},
                field=f"checkpoint.q_values[{index}]",
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
        # The Agent contract supplies two independent seed channels.  Use the
        # initialization channel for planning and the exploration channel only
        # for action selection; never consume environment/evaluator RNG state.
        self._planning_rng = random.Random(self._initialization_seed)
        self._exploration_rng = random.Random(self._exploration_seed)
        self._q_values = dict(self._base_q_values)
        self._model = {}
        self._experienced = set()
        self._last_real_visit = {}
        self._pending = None
        self._last_step = None
        self._time = 0
        self._observed_transition_count = 0
        self._planning_update_count = 0

    def _require_reset(self) -> tuple[random.Random, random.Random]:
        if self._exploration_rng is None or self._planning_rng is None:
            raise RuntimeError("agent must be reset before use")
        return self._exploration_rng, self._planning_rng

    def _q_value(self, state_key: str, action_key: str) -> float:
        return self._q_values.get(
            (state_key, action_key), float(self.config.initial_q_value)
        )

    def _ensure_state_model(self, state_key: str) -> None:
        """Give every action in a visited state the Dyna-Q+ default model."""
        for action_key in self._action_by_key:
            pair = (state_key, action_key)
            if pair not in self._model:
                self._model[pair] = {
                    (state_key, False): _OutcomeStats(
                        next_state_key=state_key,
                        terminal=False,
                        count=1,
                        mean_reward=0.0,
                    )
                }
                self._last_real_visit[pair] = 0

    def _greedy_or_explore(self, state_key: str) -> str:
        exploration_rng, _ = self._require_reset()
        action_keys = tuple(self._action_by_key)
        if exploration_rng.random() < float(self.config.exploration_epsilon):
            return exploration_rng.choice(action_keys)
        values = [self._q_value(state_key, key) for key in action_keys]
        best = max(values)
        tied = tuple(
            key for key, value in zip(action_keys, values, strict=True) if value == best
        )
        return exploration_rng.choice(tied)

    def act(self, observation: Any) -> Any:
        self._require_reset()
        if self._pending is not None:
            raise RuntimeError("observe must consume the previous action before act")
        state_key = _canonical_json(observation, field="observation")
        self._ensure_state_model(state_key)
        action_key = self._greedy_or_explore(state_key)
        self._pending = state_key, action_key
        return self._action_by_key[action_key]

    def _backup(
        self,
        *,
        state_key: str,
        action_key: str,
        reward: float,
        next_state_key: str,
        terminal: bool,
    ) -> None:
        bootstrap = 0.0
        if not terminal:
            bootstrap = max(
                self._q_value(next_state_key, candidate)
                for candidate in self._action_by_key
            )
        old_value = self._q_value(state_key, action_key)
        target = reward + float(self.config.discount_factor) * bootstrap
        updated = old_value + float(self.config.learning_rate) * (target - old_value)
        if not math.isfinite(updated):
            raise ValueError("Dyna-Q+ Q update produced a non-finite value")
        self._q_values[(state_key, action_key)] = updated

    def _record_real_model(
        self,
        *,
        state_key: str,
        action_key: str,
        next_state_key: str,
        reward: float,
        terminal: bool,
    ) -> None:
        pair = (state_key, action_key)
        # The synthetic self-loop prior exists only until the pair is tried for
        # real.  It must not dilute the empirical transition distribution.
        if pair not in self._experienced:
            self._model[pair] = {}
            self._experienced.add(pair)
        outcomes = self._model[pair]
        outcome_key = (next_state_key, terminal)
        current = outcomes.get(outcome_key)
        if current is None:
            outcomes[outcome_key] = _OutcomeStats(
                next_state_key=next_state_key,
                terminal=terminal,
                count=1,
                mean_reward=reward,
            )
        else:
            new_count = current.count + 1
            current.mean_reward += (reward - current.mean_reward) / new_count
            current.count = new_count
        self._last_real_visit[pair] = self._time

    def _sample_outcome(
        self, outcomes: Mapping[tuple[str, bool], _OutcomeStats]
    ) -> _OutcomeStats:
        _, planning_rng = self._require_reset()
        ordered = [outcomes[key] for key in sorted(outcomes)]
        total = sum(item.count for item in ordered)
        draw = planning_rng.randrange(total)
        cursor = 0
        for item in ordered:
            cursor += item.count
            if draw < cursor:
                return item
        raise RuntimeError("unreachable empirical-model sampling state")

    def _plan(self) -> None:
        if self.config.planning_steps == 0 or not self._model:
            return
        _, planning_rng = self._require_reset()
        pairs = sorted(self._model)
        for _ in range(self.config.planning_steps):
            state_key, action_key = planning_rng.choice(pairs)
            outcome = self._sample_outcome(self._model[(state_key, action_key)])
            elapsed = max(0, self._time - self._last_real_visit[(state_key, action_key)])
            bonus = float(self.config.kappa) * math.sqrt(float(elapsed))
            planned_reward = outcome.mean_reward + bonus
            if not math.isfinite(planned_reward):
                raise ValueError("Dyna-Q+ planning reward produced a non-finite value")
            self._backup(
                state_key=state_key,
                action_key=action_key,
                reward=planned_reward,
                next_state_key=outcome.next_state_key,
                terminal=outcome.terminal,
            )
            self._planning_update_count += 1

    def observe(self, transition: AgentTransition) -> None:
        self._require_reset()
        if not isinstance(transition, AgentTransition):
            raise ValueError("transition must be AgentTransition")
        if not isinstance(transition.optional_information, Mapping):
            raise ValueError("transition.optional_information must be an object")
        if transition.optional_information:
            raise ValueError("D0 forbids optional evaluator information")
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

        state_key, action_key = self._pending
        delivered_action_key = _canonical_json(
            transition.intended_action, field="transition intended_action"
        )
        if delivered_action_key != action_key:
            raise ValueError("transition intended_action does not match the pending action")
        next_state_key = _canonical_json(
            transition.observation, field="transition observation"
        )
        reward = _finite_number(transition.reward, field="transition reward")
        terminal = transition.terminated or (
            transition.truncated and not self.config.bootstrap_on_truncation
        )

        self._time += 1
        self._ensure_state_model(next_state_key)
        self._backup(
            state_key=state_key,
            action_key=action_key,
            reward=reward,
            next_state_key=next_state_key,
            terminal=terminal,
        )
        self._record_real_model(
            state_key=state_key,
            action_key=action_key,
            next_state_key=next_state_key,
            reward=reward,
            terminal=terminal,
        )
        self._plan()

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
            "actions": [_json_value(key) for key in self._action_by_key],
            "initial_q_value": float(self.config.initial_q_value),
            "q_values": entries,
        }

    def checkpoint_sha256(self) -> str:
        return _sha256(self.checkpoint())

    def _serialized_model(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for state_key, action_key in sorted(self._model):
            outcomes = self._model[(state_key, action_key)]
            result.append(
                {
                    "state": _json_value(state_key),
                    "action": _json_value(action_key),
                    "experienced": (state_key, action_key) in self._experienced,
                    "last_real_visit": self._last_real_visit[(state_key, action_key)],
                    "outcomes": [
                        {
                            "next_state": _json_value(item.next_state_key),
                            "terminal": item.terminal,
                            "count": item.count,
                            "mean_reward": item.mean_reward,
                        }
                        for _, item in sorted(outcomes.items())
                    ],
                }
            )
        return result

    def get_state(self) -> Mapping[str, Any]:
        initialized = self._exploration_rng is not None and self._planning_rng is not None
        return {
            "schema_version": DYNA_Q_PLUS_STATE_SCHEMA_VERSION,
            "agent_id": self.agent_id,
            "method": "dyna_q_plus_v1",
            "initialized": initialized,
            "initialization_seed": self._initialization_seed,
            "exploration_seed": self._exploration_seed,
            "time": self._time,
            "last_step": self._last_step,
            "observed_transition_count": self._observed_transition_count,
            "planning_update_count": self._planning_update_count,
            "pending": None
            if self._pending is None
            else {
                "state": _json_value(self._pending[0]),
                "action": _json_value(self._pending[1]),
            },
            "checkpoint_sha256": self.checkpoint_sha256(),
            "checkpoint": self.checkpoint(),
            "model": self._serialized_model(),
            "exploration_rng_state": None
            if self._exploration_rng is None
            else _json_rng_state(self._exploration_rng.getstate()),
            "planning_rng_state": None
            if self._planning_rng is None
            else _json_rng_state(self._planning_rng.getstate()),
        }

    def state_sha256(self) -> str:
        return _sha256(self.get_state())

    def restore_state(self, state: Mapping[str, Any]) -> None:
        """Restore a JSON-compatible state produced by get_state().

        This is deliberately strict so a partial/cross-agent resume cannot look
        successful.  It is intended for deterministic checkpoint/recovery tests
        and later runner integration; normal new roots still use reset().
        """
        if not isinstance(state, Mapping):
            raise ValueError("state must be an object")
        expected = {
            "schema_version",
            "agent_id",
            "method",
            "initialized",
            "initialization_seed",
            "exploration_seed",
            "time",
            "last_step",
            "observed_transition_count",
            "planning_update_count",
            "pending",
            "checkpoint_sha256",
            "checkpoint",
            "model",
            "exploration_rng_state",
            "planning_rng_state",
        }
        _require_exact_keys(state, expected, field="state")
        if state["schema_version"] != DYNA_Q_PLUS_STATE_SCHEMA_VERSION:
            raise ValueError("unsupported Dyna-Q+ state schema_version")
        if state["agent_id"] != self.agent_id or state["method"] != "dyna_q_plus_v1":
            raise ValueError("state identity does not match D0 configuration")
        if not isinstance(state["initialized"], bool) or not state["initialized"]:
            raise ValueError("only initialized Dyna-Q+ states can be restored")

        initialization_seed = _validate_seed(
            state["initialization_seed"], field="state.initialization_seed"
        )
        exploration_seed = _validate_seed(
            state["exploration_seed"], field="state.exploration_seed"
        )
        restored_q = self._load_checkpoint(state["checkpoint"])
        if _sha256(state["checkpoint"]) != state["checkpoint_sha256"]:
            raise ValueError("state checkpoint checksum mismatch")

        for field in ("time", "observed_transition_count", "planning_update_count"):
            value = state[field]
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"state.{field} must be an integer >= 0")
        last_step = state["last_step"]
        if last_step is not None and (
            not isinstance(last_step, int) or isinstance(last_step, bool)
        ):
            raise ValueError("state.last_step must be an integer or null")

        model: dict[tuple[str, str], dict[tuple[str, bool], _OutcomeStats]] = {}
        experienced: set[tuple[str, str]] = set()
        last_visit: dict[tuple[str, str], int] = {}
        raw_model = state["model"]
        if not isinstance(raw_model, list):
            raise ValueError("state.model must be a list")
        for index, entry in enumerate(raw_model):
            if not isinstance(entry, Mapping):
                raise ValueError(f"state.model[{index}] must be an object")
            _require_exact_keys(
                entry,
                {"state", "action", "experienced", "last_real_visit", "outcomes"},
                field=f"state.model[{index}]",
            )
            state_key = _canonical_json(entry["state"], field="model state")
            action_key = _canonical_json(entry["action"], field="model action")
            if action_key not in self._action_by_key:
                raise ValueError("state.model contains unknown action")
            pair = (state_key, action_key)
            if pair in model:
                raise ValueError("state.model contains duplicate state/action pair")
            if not isinstance(entry["experienced"], bool):
                raise ValueError("state.model.experienced must be boolean")
            visit = entry["last_real_visit"]
            if not isinstance(visit, int) or isinstance(visit, bool) or visit < 0:
                raise ValueError("state.model.last_real_visit must be integer >= 0")
            raw_outcomes = entry["outcomes"]
            if not isinstance(raw_outcomes, list) or not raw_outcomes:
                raise ValueError("state.model.outcomes must be non-empty list")
            parsed: dict[tuple[str, bool], _OutcomeStats] = {}
            for out_index, raw in enumerate(raw_outcomes):
                if not isinstance(raw, Mapping):
                    raise ValueError("state.model outcome must be an object")
                _require_exact_keys(
                    raw,
                    {"next_state", "terminal", "count", "mean_reward"},
                    field=f"state.model[{index}].outcomes[{out_index}]",
                )
                next_key = _canonical_json(raw["next_state"], field="model next_state")
                terminal = raw["terminal"]
                count = raw["count"]
                if not isinstance(terminal, bool):
                    raise ValueError("model terminal must be boolean")
                if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
                    raise ValueError("model count must be an integer > 0")
                key = (next_key, terminal)
                if key in parsed:
                    raise ValueError("state.model contains duplicate outcome")
                parsed[key] = _OutcomeStats(
                    next_state_key=next_key,
                    terminal=terminal,
                    count=count,
                    mean_reward=_finite_number(raw["mean_reward"], field="model reward"),
                )
            model[pair] = parsed
            last_visit[pair] = visit
            if entry["experienced"]:
                experienced.add(pair)

        pending = state["pending"]
        pending_pair: tuple[str, str] | None = None
        if pending is not None:
            if not isinstance(pending, Mapping):
                raise ValueError("state.pending must be an object or null")
            _require_exact_keys(pending, {"state", "action"}, field="state.pending")
            p_state = _canonical_json(pending["state"], field="pending state")
            p_action = _canonical_json(pending["action"], field="pending action")
            if p_action not in self._action_by_key:
                raise ValueError("state.pending contains unknown action")
            pending_pair = (p_state, p_action)

        exploration_rng_state = state["exploration_rng_state"]
        planning_rng_state = state["planning_rng_state"]
        if exploration_rng_state is None or planning_rng_state is None:
            raise ValueError("initialized state must contain both RNG states")
        exploration_rng = random.Random()
        planning_rng = random.Random()
        try:
            exploration_rng.setstate(_tuple_rng_state(exploration_rng_state))
            planning_rng.setstate(_tuple_rng_state(planning_rng_state))
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid serialized RNG state") from exc

        self._initialization_seed = initialization_seed
        self._exploration_seed = exploration_seed
        self._exploration_rng = exploration_rng
        self._planning_rng = planning_rng
        self._q_values = restored_q
        self._model = model
        self._experienced = experienced
        self._last_real_visit = last_visit
        self._pending = pending_pair
        self._last_step = last_step
        self._time = state["time"]
        self._observed_transition_count = state["observed_transition_count"]
        self._planning_update_count = state["planning_update_count"]
