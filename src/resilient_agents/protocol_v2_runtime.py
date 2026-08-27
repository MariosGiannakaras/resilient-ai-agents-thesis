"""Run-level schemas and accounting for protocol-v2.

The runtime layer is intentionally environment- and framework-neutral.  It
turns the accepted protocol into executable validation rules before the method-
specific training loops are attached.  Legacy v1.x orchestration remains
unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence

from .protocol_v2 import (
    InteractionLedger,
    ProtocolV2Branch,
    ProtocolV2TaskSemantics,
    ScientificCheckpoint,
)


class RunFailureKind(str, Enum):
    SCIENTIFIC = "scientific"
    INFRASTRUCTURE = "infrastructure"


@dataclass(frozen=True)
class ProtocolV2RootIdentity:
    """Stable randomization-unit identity; never a tunable hyperparameter."""

    root_id: str
    initialization_seed: int
    exploration_seed: int
    scenario_seed: int
    environment_seed: int
    action_disturbance_seed: int
    observation_disturbance_seed: int

    def __post_init__(self) -> None:
        if not isinstance(self.root_id, str) or not self.root_id.strip():
            raise ValueError("root_id must be non-empty")
        for name in (
            "initialization_seed",
            "exploration_seed",
            "scenario_seed",
            "environment_seed",
            "action_disturbance_seed",
            "observation_disturbance_seed",
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"{name} must be an integer >= 0")


@dataclass(frozen=True)
class ProtocolV2MethodConfig:
    """Method-discriminated configuration without fake shared hyperparameters."""

    method_id: str
    implementation_id: str
    parameters: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.method_id.strip() or not self.implementation_id.strip():
            raise ValueError("method_id and implementation_id must be non-empty")
        if not isinstance(self.parameters, Mapping):
            raise ValueError("parameters must be an object")


@dataclass(frozen=True)
class NoLearningProbePlan:
    """Interaction-indexed probe checkpoints, separate from training budget."""

    interaction_indices: Sequence[int]
    episodes_per_probe: int

    def __post_init__(self) -> None:
        indices = tuple(self.interaction_indices)
        if not indices:
            raise ValueError("interaction_indices must be explicit and non-empty")
        if any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for value in indices
        ):
            raise ValueError("probe interaction indices must be integers >= 0")
        if tuple(sorted(set(indices))) != indices:
            raise ValueError("probe interaction indices must be sorted and unique")
        if (
            not isinstance(self.episodes_per_probe, int)
            or isinstance(self.episodes_per_probe, bool)
            or self.episodes_per_probe <= 0
        ):
            raise ValueError("episodes_per_probe must be an integer > 0")
        object.__setattr__(self, "interaction_indices", indices)

    def validate_against_training_budget(self, training_budget: int) -> None:
        if (
            not isinstance(training_budget, int)
            or isinstance(training_budget, bool)
            or training_budget <= 0
        ):
            raise ValueError("training_budget must be an integer > 0")
        if self.interaction_indices[-1] > training_budget:
            raise ValueError("probe schedule extends beyond training budget")


@dataclass(frozen=True)
class PhaseARequest:
    protocol_version: str
    experiment_id: str
    layout_id: str
    root: ProtocolV2RootIdentity
    task: ProtocolV2TaskSemantics
    method: ProtocolV2MethodConfig
    training_interaction_budget: int
    probe_plan: NoLearningProbePlan

    def __post_init__(self) -> None:
        if not self.protocol_version.startswith("protocol-v2"):
            raise ValueError("PhaseARequest requires a protocol-v2 version")
        if not self.experiment_id.strip() or not self.layout_id.strip():
            raise ValueError("experiment_id and layout_id must be non-empty")
        if self.training_interaction_budget <= 0:
            raise ValueError("training_interaction_budget must be > 0")
        self.probe_plan.validate_against_training_budget(
            self.training_interaction_budget
        )
        method_gamma = self.method.parameters.get("discount_factor")
        if method_gamma is not None and float(method_gamma) != float(self.task.gamma):
            raise ValueError(
                "method discount_factor must match common task-level gamma"
            )
        bootstrap = self.method.parameters.get("bootstrap_on_truncation")
        if bootstrap is not None and bool(bootstrap) != self.task.bootstrap_on_truncation:
            raise ValueError(
                "method bootstrap_on_truncation must match common task semantics"
            )


@dataclass(frozen=True)
class ProbeResult:
    training_interaction_index: int
    probe_environment_interactions: int
    episodes: int
    metrics: Mapping[str, float]

    def __post_init__(self) -> None:
        if self.training_interaction_index < 0:
            raise ValueError("training_interaction_index must be >= 0")
        if self.probe_environment_interactions <= 0 or self.episodes <= 0:
            raise ValueError("probe interactions and episodes must be > 0")
        if not isinstance(self.metrics, Mapping) or not self.metrics:
            raise ValueError("probe metrics must be explicit and non-empty")


@dataclass(frozen=True)
class PhaseAResult:
    request: PhaseARequest
    ledger: InteractionLedger
    probes: tuple[ProbeResult, ...]
    final_checkpoint: ScientificCheckpoint
    completed: bool
    failure_id: str | None = None

    def __post_init__(self) -> None:
        if self.ledger.training_interactions > self.request.training_interaction_budget:
            raise ValueError("Phase-A result exceeds the actual interaction budget")
        if self.completed:
            if self.ledger.training_interactions != self.request.training_interaction_budget:
                raise ValueError(
                    "completed Phase-A result must consume the exact training budget"
                )
            if self.failure_id is not None:
                raise ValueError("completed Phase-A result cannot carry failure_id")
        elif not self.failure_id:
            raise ValueError("incomplete Phase-A result requires failure_id")
        if self.final_checkpoint.method_id != self.request.method.method_id:
            raise ValueError("final checkpoint method does not match request")
        if self.final_checkpoint.root_id != self.request.root.root_id:
            raise ValueError("final checkpoint root does not match request")
        if self.final_checkpoint.layout_id != self.request.layout_id:
            raise ValueError("final checkpoint layout does not match request")
        if (
            self.final_checkpoint.training_interaction_index
            != self.ledger.training_interactions
        ):
            raise ValueError("checkpoint interaction index does not match ledger")
        probe_interactions = sum(item.probe_environment_interactions for item in self.probes)
        if probe_interactions != self.ledger.probe_interactions:
            raise ValueError("probe results do not reconcile with probe ledger")


@dataclass(frozen=True)
class PhaseBBranchPlan:
    branch: ProtocolV2Branch
    disturbed: bool
    adaptive: bool


FOUR_BRANCH_PLAN: tuple[PhaseBBranchPlan, ...] = (
    PhaseBBranchPlan(
        branch=ProtocolV2Branch.FROZEN_NOMINAL,
        disturbed=False,
        adaptive=False,
    ),
    PhaseBBranchPlan(
        branch=ProtocolV2Branch.FROZEN_DISTURBED,
        disturbed=True,
        adaptive=False,
    ),
    PhaseBBranchPlan(
        branch=ProtocolV2Branch.ADAPTIVE_NOMINAL,
        disturbed=False,
        adaptive=True,
    ),
    PhaseBBranchPlan(
        branch=ProtocolV2Branch.ADAPTIVE_DISTURBED,
        disturbed=True,
        adaptive=True,
    ),
)


@dataclass
class PhaseBInteractionLedger:
    """Enforces equal post-boundary opportunity across all four branches."""

    interaction_budget_per_branch: int
    counts: dict[ProtocolV2Branch, int] = field(
        default_factory=lambda: {branch: 0 for branch in ProtocolV2Branch}
    )

    def __post_init__(self) -> None:
        if (
            not isinstance(self.interaction_budget_per_branch, int)
            or isinstance(self.interaction_budget_per_branch, bool)
            or self.interaction_budget_per_branch <= 0
        ):
            raise ValueError("interaction_budget_per_branch must be an integer > 0")

    def record(self, branch: ProtocolV2Branch, count: int = 1) -> None:
        if not isinstance(branch, ProtocolV2Branch):
            raise ValueError("branch must be ProtocolV2Branch")
        if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            raise ValueError("count must be an integer > 0")
        next_count = self.counts[branch] + count
        if next_count > self.interaction_budget_per_branch:
            raise RuntimeError(
                f"branch {branch.value} exceeded its post-boundary interaction budget"
            )
        self.counts[branch] = next_count

    def require_complete(self) -> None:
        incomplete = {
            branch.value: count
            for branch, count in self.counts.items()
            if count != self.interaction_budget_per_branch
        }
        if incomplete:
            raise RuntimeError(f"Phase-B branch budgets are incomplete: {incomplete}")


@dataclass(frozen=True)
class RunFailureRecord:
    """Retained outcome/provenance for scientific or infrastructure failures."""

    failure_id: str
    kind: RunFailureKind
    root_id: str
    method_id: str
    layout_id: str
    branch: ProtocolV2Branch | None
    interaction_index: int
    exception_type: str
    message: str
    retry_of_failure_id: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "failure_id",
            "root_id",
            "method_id",
            "layout_id",
            "exception_type",
            "message",
        ):
            if not str(getattr(self, field_name)).strip():
                raise ValueError(f"{field_name} must be non-empty")
        if self.interaction_index < 0:
            raise ValueError("interaction_index must be >= 0")
        if self.kind is RunFailureKind.SCIENTIFIC and self.retry_of_failure_id is not None:
            raise ValueError("scientific failures must not be replaced by retry roots")


def require_same_branch_opportunity(
    counts: Mapping[ProtocolV2Branch, int],
) -> int:
    """Return the common branch count or fail if opportunity differs."""

    if set(counts) != set(ProtocolV2Branch):
        raise ValueError("counts must cover exactly the four protocol-v2 branches")
    values = set(counts.values())
    if len(values) != 1:
        raise ValueError("protocol-v2 branches must receive equal interaction opportunity")
    common = next(iter(values))
    if common < 0:
        raise ValueError("branch interaction counts must be >= 0")
    return common
