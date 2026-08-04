"""Scientific contracts shared by environments, agents, runners, and analysis.

The contracts deliberately separate evaluator-visible ground truth from the
smaller transition surface that an agent is allowed to observe.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

JsonObject = Mapping[str, Any]


class ProtocolStage(str, Enum):
    DEVELOPMENT = "development"
    TUNING = "tuning"
    PILOT = "pilot"
    FINAL = "final"


class RetentionPolicy(str, Enum):
    SUMMARY = "summary"
    EVENTS = "events"
    FULL_TRACE = "full-trace"


@dataclass(frozen=True)
class InformationPolicy:
    """Explicitly declares information that may be exposed to an agent.

    There are no permissive defaults: every experiment must state the policy.
    """

    expose_executed_action: bool
    expose_disturbance_flags: bool
    expose_change_indicator: bool
    expose_regime_id: bool
    expose_true_state: bool


@dataclass(frozen=True)
class ChangeEvent:
    event_id: str
    change_type: str
    onset_step: int
    persistent: bool
    affected_mechanism: str
    severity: JsonObject
    pre_change: JsonObject
    post_change: JsonObject

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("change event_id must be non-empty")
        if self.onset_step < 0:
            raise ValueError("change onset_step must be >= 0")
        if not self.change_type.strip() or not self.affected_mechanism.strip():
            raise ValueError("change type and affected mechanism must be non-empty")


@dataclass(frozen=True)
class ScenarioSpec:
    scenario_id: str
    environment_id: str
    max_steps: int
    reward_spec: JsonObject
    initial_state_spec: JsonObject
    dynamics_spec: JsonObject
    observation_spec: JsonObject
    action_disturbance_spec: JsonObject
    observation_disturbance_spec: JsonObject
    change_events: Sequence[ChangeEvent]
    information_policy: InformationPolicy

    def __post_init__(self) -> None:
        if not self.scenario_id.strip() or not self.environment_id.strip():
            raise ValueError("scenario_id and environment_id must be non-empty")
        if self.max_steps <= 0:
            raise ValueError("max_steps must be > 0")


@dataclass(frozen=True)
class ExperimentSpec:
    experiment_id: str
    protocol_version: str
    stage: ProtocolStage
    scenario_ids: Sequence[str]
    agent_ids: Sequence[str]
    seeds: Sequence[int]
    training_budget: JsonObject
    evaluation_budget: JsonObject
    metric_spec: JsonObject
    retention_policy: RetentionPolicy
    auto_publish: bool

    def __post_init__(self) -> None:
        if not self.experiment_id.strip() or not self.protocol_version.strip():
            raise ValueError("experiment_id and protocol_version must be non-empty")
        if not self.scenario_ids or not self.agent_ids or not self.seeds:
            raise ValueError("scenario_ids, agent_ids, and seeds must be explicit and non-empty")
        if len(set(self.seeds)) != len(self.seeds):
            raise ValueError("experiment seeds must be unique")


@dataclass(frozen=True)
class GroundTruthTransition:
    """Complete evaluator-visible transition record."""

    step: int
    true_state: Any
    delivered_observation: Any
    intended_action: Any
    executed_action: Any
    reward: float
    terminated: bool
    truncated: bool
    regime_id: str | None
    disturbance_flags: Mapping[str, bool] = field(default_factory=dict)
    change_event_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class AgentTransition:
    """Transition after applying the experiment's information policy."""

    step: int
    observation: Any
    intended_action: Any
    reward: float
    terminated: bool
    truncated: bool
    optional_information: Mapping[str, Any]


def project_for_agent(
    transition: GroundTruthTransition, policy: InformationPolicy
) -> AgentTransition:
    optional: dict[str, Any] = {}
    if policy.expose_executed_action:
        optional["executed_action"] = transition.executed_action
    if policy.expose_disturbance_flags:
        optional["disturbance_flags"] = dict(transition.disturbance_flags)
    if policy.expose_change_indicator:
        optional["change_event_ids"] = list(transition.change_event_ids)
    if policy.expose_regime_id:
        optional["regime_id"] = transition.regime_id
    if policy.expose_true_state:
        optional["true_state"] = transition.true_state
    return AgentTransition(
        step=transition.step,
        observation=transition.delivered_observation,
        intended_action=transition.intended_action,
        reward=transition.reward,
        terminated=transition.terminated,
        truncated=transition.truncated,
        optional_information=optional,
    )


@runtime_checkable
class Agent(Protocol):
    """Small common agent interface; no hidden environment state is supplied."""

    agent_id: str

    def reset(self, *, initialization_seed: int, exploration_seed: int) -> None: ...

    def act(self, observation: Any) -> Any: ...

    def observe(self, transition: AgentTransition) -> None: ...

    def end_episode(self, summary: Mapping[str, Any]) -> None: ...

    def get_state(self) -> Mapping[str, Any]: ...
