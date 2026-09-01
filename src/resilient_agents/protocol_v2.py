"""Framework-neutral protocol-v2 scientific lifecycle primitives.

This module deliberately lives beside the legacy v1.x experiment runner.  It
encodes the scientific invariants accepted for protocol-v2 without forcing
neural methods into the historical F0/C0/R0 or episode-budget abstractions.

The first implementation slice provides:

* task-level objective/truncation semantics;
* method capability registration for the bounded v2 candidate pool;
* actual environment-interaction accounting separated from probe interactions;
* deterministic scientific checkpoint envelopes and branch-point cloning;
* isolated no-learning probe execution on cloned learner state; and
* exact-state adapters for the existing Q-Learning, SARSA and Dyna-Q+ agents.

DQN/PPO capability requirements are represented here before their concrete
library-backed adapters are added.  No tuning or final-experiment policy lives
in this module.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Generic, Mapping, Protocol, TypeVar, runtime_checkable

from .agents import TabularQLearningAgent, TabularQLearningConfig
from .contracts import AgentTransition

PROTOCOL_V2_CHECKPOINT_SCHEMA_VERSION = 1
TABULAR_Q_SCIENTIFIC_STATE_SCHEMA_VERSION = 1


class ProtocolV2Phase(str, Enum):
    NOMINAL_TRAINING = "nominal-training"
    NOMINAL_PROBE = "nominal-probe"
    PRECHANGE_PREFIX = "prechange-prefix"
    DEPLOYMENT = "deployment"


class ProtocolV2Branch(str, Enum):
    FROZEN_NOMINAL = "FN"
    FROZEN_DISTURBED = "FD"
    ADAPTIVE_NOMINAL = "AN"
    ADAPTIVE_DISTURBED = "AD"


class MethodFamily(str, Enum):
    TABULAR_VALUE = "tabular-value"
    NEURAL_VALUE = "neural-value"
    POLICY_GRADIENT_ACTOR_CRITIC = "policy-gradient-actor-critic"
    MODEL_BASED_PLANNING = "model-based-planning"


class CheckpointBoundary(str, Enum):
    INTERACTION_BOUNDARY = "interaction-boundary"
    EPISODE_BOUNDARY = "episode-boundary"
    ROLLOUT_UPDATE_BOUNDARY = "rollout-update-boundary"


def _finite_float(value: Any, *, field_name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field_name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field_name} must be finite")
    return result


def _canonical_json(value: Any, *, field_name: str = "value") -> str:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be finite JSON-compatible data") from exc


def _json_copy(value: Any, *, field_name: str = "value") -> Any:
    return json.loads(_canonical_json(value, field_name=field_name))


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


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


def _positive_count(value: int, *, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{field_name} must be an integer > 0")
    return value


@dataclass(frozen=True)
class ProtocolV2TaskSemantics:
    """Task objective shared across retained methods.

    Administrative truncation is not a true task terminal in protocol-v2.
    Therefore a task that declares administrative truncation must also require
    value bootstrap across that boundary.
    """

    gamma: float
    reward_contract: Mapping[str, Any]
    administrative_truncation: bool = True
    bootstrap_on_truncation: bool = True

    def __post_init__(self) -> None:
        gamma = _finite_float(self.gamma, field_name="gamma")
        if not 0.0 <= gamma < 1.0:
            raise ValueError("gamma must be in [0, 1)")
        _canonical_json(self.reward_contract, field_name="reward_contract")
        if not isinstance(self.administrative_truncation, bool):
            raise ValueError("administrative_truncation must be boolean")
        if not isinstance(self.bootstrap_on_truncation, bool):
            raise ValueError("bootstrap_on_truncation must be boolean")
        if self.administrative_truncation and not self.bootstrap_on_truncation:
            raise ValueError(
                "protocol-v2 administrative truncation requires bootstrap_on_truncation"
            )

    @property
    def reward_contract_sha256(self) -> str:
        return _sha256_json(self.reward_contract)


@dataclass(frozen=True)
class MethodCapabilities:
    method_id: str
    family: MethodFamily
    checkpoint_boundary: CheckpointBoundary
    exact_restore_required: bool
    supports_frozen_deployment: bool
    supports_adaptive_deployment: bool
    required_checkpoint_components: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.method_id, str) or not self.method_id.strip():
            raise ValueError("method_id must be non-empty")
        if not isinstance(self.family, MethodFamily):
            raise ValueError("family must be MethodFamily")
        if not isinstance(self.checkpoint_boundary, CheckpointBoundary):
            raise ValueError("checkpoint_boundary must be CheckpointBoundary")
        if not self.exact_restore_required:
            raise ValueError("protocol-v2 retained methods require exact restore")
        if not self.supports_frozen_deployment or not self.supports_adaptive_deployment:
            raise ValueError("retained methods must support both deployment regimes")
        if not self.required_checkpoint_components:
            raise ValueError("required_checkpoint_components must be non-empty")
        if len(set(self.required_checkpoint_components)) != len(
            self.required_checkpoint_components
        ):
            raise ValueError("required_checkpoint_components must be unique")


CORE_METHOD_CAPABILITIES: tuple[MethodCapabilities, ...] = (
    MethodCapabilities(
        method_id="q_learning",
        family=MethodFamily.TABULAR_VALUE,
        checkpoint_boundary=CheckpointBoundary.INTERACTION_BOUNDARY,
        exact_restore_required=True,
        supports_frozen_deployment=True,
        supports_adaptive_deployment=True,
        required_checkpoint_components=(
            "q_values",
            "exploration_rng_state",
            "behavior_state",
            "counters",
        ),
    ),
    MethodCapabilities(
        method_id="sarsa",
        family=MethodFamily.TABULAR_VALUE,
        checkpoint_boundary=CheckpointBoundary.INTERACTION_BOUNDARY,
        exact_restore_required=True,
        supports_frozen_deployment=True,
        supports_adaptive_deployment=True,
        required_checkpoint_components=(
            "q_values",
            "exploration_rng_state",
            "pending_or_deferred_update_state",
            "counters",
        ),
    ),
    MethodCapabilities(
        method_id="dqn",
        family=MethodFamily.NEURAL_VALUE,
        checkpoint_boundary=CheckpointBoundary.INTERACTION_BOUNDARY,
        exact_restore_required=True,
        supports_frozen_deployment=True,
        supports_adaptive_deployment=True,
        required_checkpoint_components=(
            "online_network",
            "target_network",
            "optimizer",
            "replay_buffer_contents",
            "replay_buffer_logical_state",
            "sampling_rng_state",
            "exploration_schedule_state",
            "update_and_warmup_counters",
            "preprocessing_state",
        ),
    ),
    MethodCapabilities(
        method_id="ppo",
        family=MethodFamily.POLICY_GRADIENT_ACTOR_CRITIC,
        checkpoint_boundary=CheckpointBoundary.ROLLOUT_UPDATE_BOUNDARY,
        exact_restore_required=True,
        supports_frozen_deployment=True,
        supports_adaptive_deployment=True,
        required_checkpoint_components=(
            "policy_and_value_parameters",
            "optimizer",
            "learning_rate_and_update_schedule_state",
            "rollout_update_counters",
            "preprocessing_or_normalization_state",
            "rng_state",
        ),
    ),
    MethodCapabilities(
        method_id="dyna_q_plus",
        family=MethodFamily.MODEL_BASED_PLANNING,
        checkpoint_boundary=CheckpointBoundary.INTERACTION_BOUNDARY,
        exact_restore_required=True,
        supports_frozen_deployment=True,
        supports_adaptive_deployment=True,
        required_checkpoint_components=(
            "q_values",
            "learned_model",
            "planning_state",
            "recency_state",
            "action_and_planning_rng_state",
            "counters",
        ),
    ),
)


@dataclass(frozen=True)
class MethodRegistration:
    capabilities: MethodCapabilities
    implementation_id: str
    implementation_version: str | None = None

    def __post_init__(self) -> None:
        if not self.implementation_id.strip():
            raise ValueError("implementation_id must be non-empty")
        if self.implementation_version is not None and not self.implementation_version.strip():
            raise ValueError("implementation_version must be non-empty when supplied")


class MethodRegistry:
    """Deterministic registry with explicit duplicate rejection."""

    def __init__(self) -> None:
        self._registrations: dict[str, MethodRegistration] = {}

    def register(self, registration: MethodRegistration) -> None:
        if not isinstance(registration, MethodRegistration):
            raise ValueError("registration must be MethodRegistration")
        method_id = registration.capabilities.method_id
        if method_id in self._registrations:
            raise ValueError(f"method_id already registered: {method_id}")
        self._registrations[method_id] = registration

    def get(self, method_id: str) -> MethodRegistration:
        try:
            return self._registrations[method_id]
        except KeyError as exc:
            raise KeyError(f"unknown method_id: {method_id}") from exc

    def method_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._registrations))

    @classmethod
    def core_candidates(cls) -> "MethodRegistry":
        registry = cls()
        for capabilities in CORE_METHOD_CAPABILITIES:
            registry.register(
                MethodRegistration(
                    capabilities=capabilities,
                    implementation_id=(
                        "project-tabular"
                        if capabilities.method_id in {"q_learning", "sarsa", "dyna_q_plus"}
                        else "library-adapter-pending-t525"
                    ),
                )
            )
        return registry


@dataclass
class InteractionLedger:
    """Counts actual environment transitions by scientific role.

    Probe interactions are deliberately separate from the learner's training
    budget.  Requested library timesteps or episodes are not accepted as
    substitutes for these counters.
    """

    training_interactions: int = 0
    probe_interactions: int = 0
    deployment_interactions: dict[ProtocolV2Branch, int] = field(
        default_factory=lambda: {branch: 0 for branch in ProtocolV2Branch}
    )

    def record_training(self, count: int = 1) -> None:
        self.training_interactions += _positive_count(count, field_name="count")

    def record_probe(self, count: int = 1) -> None:
        self.probe_interactions += _positive_count(count, field_name="count")

    def record_deployment(self, branch: ProtocolV2Branch, count: int = 1) -> None:
        if not isinstance(branch, ProtocolV2Branch):
            raise ValueError("branch must be ProtocolV2Branch")
        self.deployment_interactions[branch] += _positive_count(
            count, field_name="count"
        )

    @property
    def deployment_total(self) -> int:
        return sum(self.deployment_interactions.values())

    @property
    def all_environment_interactions(self) -> int:
        return self.training_interactions + self.probe_interactions + self.deployment_total

    def require_training_budget(self, budget: int) -> None:
        if not isinstance(budget, int) or isinstance(budget, bool) or budget < 0:
            raise ValueError("budget must be an integer >= 0")
        if self.training_interactions > budget:
            raise RuntimeError("actual training interactions exceeded the frozen budget")


@dataclass(frozen=True)
class ScientificCheckpoint:
    """Method-neutral envelope around exact learner continuation state."""

    method_id: str
    root_id: str
    layout_id: str
    phase: ProtocolV2Phase
    training_interaction_index: int
    state: Mapping[str, Any]
    provenance: Mapping[str, Any]
    schema_version: int = PROTOCOL_V2_CHECKPOINT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != PROTOCOL_V2_CHECKPOINT_SCHEMA_VERSION:
            raise ValueError("unsupported scientific checkpoint schema_version")
        for field_name, value in (
            ("method_id", self.method_id),
            ("root_id", self.root_id),
            ("layout_id", self.layout_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be non-empty")
        if not isinstance(self.phase, ProtocolV2Phase):
            raise ValueError("phase must be ProtocolV2Phase")
        if (
            not isinstance(self.training_interaction_index, int)
            or isinstance(self.training_interaction_index, bool)
            or self.training_interaction_index < 0
        ):
            raise ValueError("training_interaction_index must be an integer >= 0")
        _canonical_json(self.state, field_name="checkpoint state")
        _canonical_json(self.provenance, field_name="checkpoint provenance")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "method_id": self.method_id,
            "root_id": self.root_id,
            "layout_id": self.layout_id,
            "phase": self.phase.value,
            "training_interaction_index": self.training_interaction_index,
            "state": _json_copy(self.state, field_name="checkpoint state"),
            "provenance": _json_copy(
                self.provenance, field_name="checkpoint provenance"
            ),
        }

    @property
    def sha256(self) -> str:
        return _sha256_json(self.to_mapping())


@runtime_checkable
class ScientificStateAdapter(Protocol):
    method_id: str

    def export_state(self) -> Mapping[str, Any]: ...

    def restore_state(self, state: Mapping[str, Any]) -> None: ...

    def clone(self) -> "ScientificStateAdapter": ...

    def state_sha256(self) -> str: ...


T = TypeVar("T")
A = TypeVar("A")


class NativeStateAdapter(Generic[A]):
    """Adapter for project agents that already expose strict get/restore state."""

    def __init__(
        self,
        *,
        method_id: str,
        agent: A,
        factory: Callable[[], A],
    ) -> None:
        if not method_id.strip():
            raise ValueError("method_id must be non-empty")
        if not hasattr(agent, "get_state") or not hasattr(agent, "restore_state"):
            raise ValueError("agent must expose get_state and restore_state")
        self.method_id = method_id
        self.agent = agent
        self._factory = factory

    def export_state(self) -> Mapping[str, Any]:
        state = self.agent.get_state()  # type: ignore[attr-defined]
        return _json_copy(state, field_name=f"{self.method_id} state")

    def restore_state(self, state: Mapping[str, Any]) -> None:
        self.agent.restore_state(  # type: ignore[attr-defined]
            _json_copy(state, field_name=f"{self.method_id} state")
        )

    def clone(self) -> "NativeStateAdapter[A]":
        clone_agent = self._factory()
        clone = NativeStateAdapter(
            method_id=self.method_id,
            agent=clone_agent,
            factory=self._factory,
        )
        clone.restore_state(self.export_state())
        return clone

    def state_sha256(self) -> str:
        return _sha256_json(self.export_state())


def sarsa_state_adapter(agent: Any) -> NativeStateAdapter[Any]:
    """Return an exact-state adapter for the project SARSA implementation."""

    from .sarsa import SarsaAgent

    if not isinstance(agent, SarsaAgent):
        raise ValueError("agent must be SarsaAgent")
    config = agent.config
    return NativeStateAdapter(
        method_id="sarsa",
        agent=agent,
        factory=lambda: SarsaAgent(config, checkpoint=None),
    )


def dyna_q_plus_state_adapter(agent: Any) -> NativeStateAdapter[Any]:
    """Return an exact-state adapter for the project Dyna-Q+ implementation."""

    from .dyna_q_plus import DynaQPlusAgent

    if not isinstance(agent, DynaQPlusAgent):
        raise ValueError("agent must be DynaQPlusAgent")
    config = agent.config
    return NativeStateAdapter(
        method_id="dyna_q_plus",
        agent=agent,
        factory=lambda: DynaQPlusAgent(config, checkpoint=None),
    )


def _q_checkpoint_from_values(
    *,
    config: TabularQLearningConfig,
    action_by_key: Mapping[str, Any],
    q_values: Mapping[tuple[str, str], float],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "actions": [json.loads(key) for key in action_by_key],
        "initial_q_value": float(config.initial_q_value),
        "q_values": [
            {
                "state": json.loads(state_key),
                "action": json.loads(action_key),
                "value": value,
            }
            for (state_key, action_key), value in sorted(q_values.items())
        ],
    }


def _q_config_mapping(config: TabularQLearningConfig) -> dict[str, Any]:
    return {
        "agent_id": config.agent_id,
        "actions": _json_copy(list(config.actions), field_name="Q actions"),
        "learning_rate": float(config.learning_rate),
        "discount_factor": float(config.discount_factor),
        "exploration_epsilon": float(config.exploration_epsilon),
        "learning_enabled": config.learning_enabled,
        "bootstrap_on_truncation": config.bootstrap_on_truncation,
        "initial_q_value": float(config.initial_q_value),
    }


class TabularQScientificStateAdapter:
    """Exact scientific-state bridge around the historical Q implementation.

    The historical ``checkpoint()`` remains the same Q-only artifact used by
    v1.x.  This adapter adds a separate protocol-v2 continuation state that also
    captures behavior-policy RNG, pending action, counters and the immutable
    reset baseline.  Private attributes are intentionally contained inside this
    compatibility bridge so the historical agent file need not be rewritten.
    """

    method_id = "q_learning"

    def __init__(self, agent: TabularQLearningAgent) -> None:
        if not isinstance(agent, TabularQLearningAgent):
            raise ValueError("agent must be TabularQLearningAgent")
        self.agent = agent
        self.config = agent.config

    def export_state(self) -> Mapping[str, Any]:
        agent = self.agent
        base_checkpoint = _q_checkpoint_from_values(
            config=self.config,
            action_by_key=agent._action_by_key,
            q_values=agent._base_q_values,
        )
        pending = None
        if agent._pending is not None:
            pending = {
                "state": json.loads(agent._pending[0]),
                "action": json.loads(agent._pending[1]),
            }
        state = {
            "schema_version": TABULAR_Q_SCIENTIFIC_STATE_SCHEMA_VERSION,
            "method": "q_learning",
            "config": _q_config_mapping(self.config),
            "initialized": agent._exploration_rng is not None,
            "initialization_seed": agent._initialization_seed,
            "exploration_seed": agent._exploration_seed,
            "last_step": agent._last_step,
            "observed_transition_count": agent._observed_transition_count,
            "pending_action": pending,
            "base_checkpoint": base_checkpoint,
            "checkpoint": agent.checkpoint(),
            "exploration_rng_state": None
            if agent._exploration_rng is None
            else _json_rng_state(agent._exploration_rng.getstate()),
        }
        return _json_copy(state, field_name="Q scientific state")

    def restore_state(self, state: Mapping[str, Any]) -> None:
        if not isinstance(state, Mapping):
            raise ValueError("state must be an object")
        expected = {
            "schema_version",
            "method",
            "config",
            "initialized",
            "initialization_seed",
            "exploration_seed",
            "last_step",
            "observed_transition_count",
            "pending_action",
            "base_checkpoint",
            "checkpoint",
            "exploration_rng_state",
        }
        if set(state) != expected:
            raise ValueError(
                "Q scientific state keys mismatch; "
                f"missing={sorted(expected - set(state))}, "
                f"unknown={sorted(set(state) - expected)}"
            )
        if state["schema_version"] != TABULAR_Q_SCIENTIFIC_STATE_SCHEMA_VERSION:
            raise ValueError("unsupported Q scientific state schema_version")
        if state["method"] != self.method_id:
            raise ValueError("Q scientific state method mismatch")
        if state["config"] != _q_config_mapping(self.config):
            raise ValueError("Q scientific state configuration mismatch")
        initialized = state["initialized"]
        if not isinstance(initialized, bool):
            raise ValueError("initialized must be boolean")
        observed_count = state["observed_transition_count"]
        if (
            not isinstance(observed_count, int)
            or isinstance(observed_count, bool)
            or observed_count < 0
        ):
            raise ValueError("observed_transition_count must be an integer >= 0")
        last_step = state["last_step"]
        if last_step is not None and (
            not isinstance(last_step, int) or isinstance(last_step, bool) or last_step < 0
        ):
            raise ValueError("last_step must be None or an integer >= 0")

        base_loader = TabularQLearningAgent(
            self.config, checkpoint=state["base_checkpoint"]
        )
        current_loader = TabularQLearningAgent(
            self.config, checkpoint=state["checkpoint"]
        )
        self.agent._base_q_values = dict(base_loader._base_q_values)
        self.agent._q_values = dict(current_loader._q_values)
        self.agent._initialization_seed = state["initialization_seed"]
        self.agent._exploration_seed = state["exploration_seed"]
        self.agent._last_step = last_step
        self.agent._observed_transition_count = observed_count

        pending = state["pending_action"]
        if pending is None:
            self.agent._pending = None
        else:
            if not isinstance(pending, Mapping) or set(pending) != {"state", "action"}:
                raise ValueError("pending_action must be null or {state, action}")
            state_key = _canonical_json(pending["state"], field_name="pending state")
            action_key = _canonical_json(pending["action"], field_name="pending action")
            if action_key not in self.agent._action_by_key:
                raise ValueError("pending_action contains an unknown action")
            self.agent._pending = (state_key, action_key)

        rng_state = state["exploration_rng_state"]
        if initialized:
            if rng_state is None:
                raise ValueError("initialized Q state requires exploration_rng_state")
            rng = random.Random()
            rng.setstate(_tuple_rng_state(rng_state))
            self.agent._exploration_rng = rng
        else:
            if rng_state is not None:
                raise ValueError("uninitialized Q state cannot contain RNG state")
            self.agent._exploration_rng = None

        if self.export_state() != _json_copy(state, field_name="Q scientific state"):
            raise ValueError("Q scientific state failed exact round-trip validation")

    def clone(self) -> "TabularQScientificStateAdapter":
        clone_agent = TabularQLearningAgent(self.config, checkpoint=None)
        clone = TabularQScientificStateAdapter(clone_agent)
        clone.restore_state(self.export_state())
        return clone

    def state_sha256(self) -> str:
        return _sha256_json(self.export_state())


def make_scientific_checkpoint(
    *,
    adapter: ScientificStateAdapter,
    root_id: str,
    layout_id: str,
    phase: ProtocolV2Phase,
    training_interaction_index: int,
    provenance: Mapping[str, Any],
) -> ScientificCheckpoint:
    return ScientificCheckpoint(
        method_id=adapter.method_id,
        root_id=root_id,
        layout_id=layout_id,
        phase=phase,
        training_interaction_index=training_interaction_index,
        state=adapter.export_state(),
        provenance=provenance,
    )


def fork_four_branches(
    adapter: ScientificStateAdapter,
) -> dict[ProtocolV2Branch, ScientificStateAdapter]:
    """Clone identical scientific state into the four protocol-v2 branches."""

    source_digest = adapter.state_sha256()
    branches: dict[ProtocolV2Branch, ScientificStateAdapter] = {}
    for branch in ProtocolV2Branch:
        clone = adapter.clone()
        if clone.state_sha256() != source_digest:
            raise RuntimeError(f"branch {branch.value} does not match source state")
        branches[branch] = clone
    if len({clone.state_sha256() for clone in branches.values()}) != 1:
        raise RuntimeError("protocol-v2 branch clones are not identical at the fork")
    return branches


def run_isolated_probe(
    adapter: ScientificStateAdapter,
    probe: Callable[[ScientificStateAdapter], T],
) -> T:
    """Run a no-learning probe on a cloned state and prove source non-mutation."""

    before = adapter.state_sha256()
    probe_adapter = adapter.clone()
    result = probe(probe_adapter)
    after = adapter.state_sha256()
    if after != before:
        raise RuntimeError("isolated probe mutated the training adapter state")
    return result


def require_information_limited_transition(transition: AgentTransition) -> None:
    """Fail closed if evaluator-only information reaches a core v2 method."""

    if not isinstance(transition, AgentTransition):
        raise ValueError("transition must be AgentTransition")
    if not isinstance(transition.optional_information, Mapping):
        raise ValueError("transition.optional_information must be an object")
    if transition.optional_information:
        raise ValueError("protocol-v2 core methods forbid evaluator-only information")
