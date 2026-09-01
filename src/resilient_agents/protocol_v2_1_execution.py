"""Protocol-v2.1 temporal evidence orchestration.

This module deliberately composes the immutable protocol-v2 matched-branch
executor instead of modifying it.  The scientific branch lifecycle therefore
remains byte-identical to the historical T-526/T-527 authority while v2.1
collects passive fixed-window reward evidence from dedicated branch drivers.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .protocol_v2 import ProtocolV2Branch, ScientificStateAdapter
from .protocol_v2_executor import (
    BranchDriverFactory,
    BranchExecutionResult,
    PhaseBBranchDriver,
    execute_phase_b,
)
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_temporal import RewardWindow


@dataclass(frozen=True)
class BranchExecutionResultV21:
    """One protocol-v2.1 branch result with passive temporal evidence."""

    branch: ProtocolV2Branch
    interactions: int
    metrics: Mapping[str, float]
    final_learner_state_sha256: str
    final_environment_state_sha256: str
    reward_windows: tuple[RewardWindow, ...]

    @classmethod
    def from_v2(
        cls,
        result: BranchExecutionResult,
        *,
        reward_windows: tuple[RewardWindow, ...],
    ) -> "BranchExecutionResultV21":
        return cls(
            branch=result.branch,
            interactions=result.interactions,
            metrics=result.metrics,
            final_learner_state_sha256=result.final_learner_state_sha256,
            final_environment_state_sha256=result.final_environment_state_sha256,
            reward_windows=reward_windows,
        )

    def __post_init__(self) -> None:
        if not self.reward_windows:
            raise ValueError("protocol-v2.1 requires explicit reward windows")
        previous_end = 0
        for window in self.reward_windows:
            if not isinstance(window, RewardWindow):
                raise ValueError("reward_windows must contain RewardWindow values")
            if window.start_interaction != previous_end + 1:
                raise ValueError("reward windows must be contiguous and ordered")
            if window.end_interaction > self.interactions:
                raise ValueError("reward window exceeds branch interactions")
            previous_end = window.end_interaction
        if previous_end != self.interactions:
            raise ValueError("reward windows must cover the complete branch horizon")


@dataclass(frozen=True)
class PhaseBExecutionV21:
    branch_point_learner_sha256: str
    branch_point_environment_sha256: str
    results: tuple[BranchExecutionResultV21, ...]

    def __post_init__(self) -> None:
        if {item.branch for item in self.results} != set(ProtocolV2Branch):
            raise ValueError("PhaseBExecutionV21 must contain exactly FN/FD/AN/AD")


TemporalBranchDriverFactory = Callable[
    [ProtocolV2Branch, bool, ScientificStateAdapter, GridWorldScientificStateAdapter],
    PhaseBBranchDriver,
]


def execute_phase_b_v21(
    *,
    learner: ScientificStateAdapter,
    shared_environment: GridWorldScientificStateAdapter,
    nominal_spec: Any,
    disturbed_spec: Any,
    interaction_budget_per_branch: int,
    driver_factory: TemporalBranchDriverFactory,
) -> PhaseBExecutionV21:
    """Execute the immutable matched design and attach passive reward windows.

    The delegated v2 executor still invokes every branch driver exactly once at
    the full post-boundary horizon.  In particular, adaptive PPO is never split
    at temporal-window boundaries.
    """

    if interaction_budget_per_branch <= 0 or interaction_budget_per_branch % 32:
        raise ValueError("protocol-v2.1 branch horizon must be a positive multiple of 32")

    drivers: dict[ProtocolV2Branch, PhaseBBranchDriver] = {}

    def capturing_factory(
        branch: ProtocolV2Branch,
        adaptive: bool,
        branch_learner: ScientificStateAdapter,
        environment: GridWorldScientificStateAdapter,
    ) -> PhaseBBranchDriver:
        driver = driver_factory(branch, adaptive, branch_learner, environment)
        if branch in drivers:
            raise RuntimeError(f"branch driver constructed more than once: {branch.value}")
        drivers[branch] = driver
        return driver

    base = execute_phase_b(
        learner=learner,
        shared_environment=shared_environment,
        nominal_spec=nominal_spec,
        disturbed_spec=disturbed_spec,
        interaction_budget_per_branch=interaction_budget_per_branch,
        driver_factory=capturing_factory,
    )
    if set(drivers) != set(ProtocolV2Branch):
        raise RuntimeError("protocol-v2.1 did not capture all four branch drivers")

    results: list[BranchExecutionResultV21] = []
    expected_endpoints = tuple(range(32, interaction_budget_per_branch + 1, 32))
    for result in base.results:
        driver = drivers[result.branch]
        require_complete = getattr(driver, "require_complete_reward_windows", None)
        if not callable(require_complete):
            raise RuntimeError(
                f"protocol-v2.1 driver {result.branch.value} does not expose temporal validation"
            )
        require_complete(total_interactions=interaction_budget_per_branch)
        windows = tuple(getattr(driver, "reward_windows", ()))
        if tuple(window.end_interaction for window in windows) != expected_endpoints:
            raise RuntimeError(
                f"protocol-v2.1 branch {result.branch.value} has incomplete reward windows"
            )
        results.append(
            BranchExecutionResultV21.from_v2(result, reward_windows=windows)
        )

    return PhaseBExecutionV21(
        branch_point_learner_sha256=base.branch_point_learner_sha256,
        branch_point_environment_sha256=base.branch_point_environment_sha256,
        results=tuple(results),
    )
