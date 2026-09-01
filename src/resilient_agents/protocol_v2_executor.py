"""Framework-neutral protocol-v2 execution orchestration.

The executor owns scientific lifecycle invariants, not algorithm internals.
Concrete method drivers may use project tabular code, Stable-Baselines3, or a
future implementation, provided they expose exact scientific state and report
*actual* environment interactions.

This separation is deliberate: PPO/DQN retain method-native rollout/replay
semantics instead of being forced into the historical tabular ``Agent.observe``
shape, while the protocol still enforces identical resource accounting,
isolated evaluation, checkpoint provenance and the matched four-branch design.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol, runtime_checkable

from .protocol_v2 import (
    InteractionLedger,
    ProtocolV2Branch,
    ProtocolV2Phase,
    ScientificStateAdapter,
    fork_four_branches,
    make_scientific_checkpoint,
    run_isolated_probe,
)
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_runtime import (
    FOUR_BRANCH_PLAN,
    PhaseARequest,
    PhaseAResult,
    PhaseBInteractionLedger,
    ProbeResult,
)


@runtime_checkable
class PhaseAMethodDriver(Protocol):
    """Method-native Phase-A training surface.

    ``train_to_interaction`` receives an *absolute* target, not a requested
    library timestep delta. The driver must stop exactly at the target or fail.
    """

    method_id: str
    implementation_id: str
    state_adapter: ScientificStateAdapter

    @property
    def training_interactions(self) -> int: ...

    def train_to_interaction(self, target_interaction: int) -> None: ...


@runtime_checkable
class ProbeEvaluator(Protocol):
    """No-learning evaluator operating only on a cloned learner state."""

    def __call__(
        self,
        adapter: ScientificStateAdapter,
        *,
        training_interaction_index: int,
        episodes: int,
    ) -> ProbeResult: ...


@dataclass(frozen=True)
class PhaseAExecution:
    """Completed Phase-A output plus final live adapter for downstream forking."""

    result: PhaseAResult
    final_adapter: ScientificStateAdapter

    def __post_init__(self) -> None:
        if not self.result.completed:
            raise ValueError("PhaseAExecution requires a completed PhaseAResult")
        if self.final_adapter.method_id != self.result.request.method.method_id:
            raise ValueError("final adapter method does not match Phase-A request")
        if self.final_adapter.export_state() != self.result.final_checkpoint.state:
            raise ValueError("final adapter does not match Phase-A checkpoint state")


def execute_phase_a(
    request: PhaseARequest,
    *,
    driver: PhaseAMethodDriver,
    probe_evaluator: ProbeEvaluator,
    checkpoint_provenance: Mapping[str, Any],
) -> PhaseAExecution:
    """Execute one Phase-A method/root/layout under exact interaction accounting."""

    if not isinstance(request, PhaseARequest):
        raise ValueError("request must be PhaseARequest")
    if not isinstance(driver, PhaseAMethodDriver):
        raise ValueError("driver must satisfy PhaseAMethodDriver")
    if driver.method_id != request.method.method_id:
        raise ValueError("driver method_id does not match Phase-A request")
    if driver.implementation_id != request.method.implementation_id:
        raise ValueError("driver implementation_id does not match Phase-A request")
    if driver.state_adapter.method_id != driver.method_id:
        raise ValueError("driver state adapter method_id mismatch")
    if driver.training_interactions != 0:
        raise ValueError("Phase-A driver must start at interaction index 0")

    ledger = InteractionLedger()
    probes: list[ProbeResult] = []

    for probe_index in request.probe_plan.interaction_indices:
        if probe_index < driver.training_interactions:
            raise RuntimeError("probe schedule moved backwards")
        if probe_index > driver.training_interactions:
            before = driver.training_interactions
            driver.train_to_interaction(probe_index)
            after = driver.training_interactions
            if after != probe_index:
                raise RuntimeError(
                    "method driver failed exact actual-interaction target during Phase A"
                )
            ledger.record_training(after - before)
            ledger.require_training_budget(request.training_interaction_budget)

        probe = run_isolated_probe(
            driver.state_adapter,
            lambda clone, index=probe_index: probe_evaluator(
                clone,
                training_interaction_index=index,
                episodes=request.probe_plan.episodes_per_probe,
            ),
        )
        if not isinstance(probe, ProbeResult):
            raise ValueError("probe_evaluator must return ProbeResult")
        if probe.training_interaction_index != probe_index:
            raise ValueError("probe result interaction index mismatch")
        if probe.episodes != request.probe_plan.episodes_per_probe:
            raise ValueError("probe result episode count mismatch")
        ledger.record_probe(probe.probe_environment_interactions)
        probes.append(probe)

    if driver.training_interactions < request.training_interaction_budget:
        before = driver.training_interactions
        driver.train_to_interaction(request.training_interaction_budget)
        after = driver.training_interactions
        if after != request.training_interaction_budget:
            raise RuntimeError("method driver failed final exact Phase-A interaction target")
        ledger.record_training(after - before)
        ledger.require_training_budget(request.training_interaction_budget)
    elif driver.training_interactions > request.training_interaction_budget:
        raise RuntimeError("method driver exceeded Phase-A interaction budget")

    checkpoint = make_scientific_checkpoint(
        adapter=driver.state_adapter,
        root_id=request.root.root_id,
        layout_id=request.layout_id,
        phase=ProtocolV2Phase.NOMINAL_TRAINING,
        training_interaction_index=ledger.training_interactions,
        provenance={
            **dict(checkpoint_provenance),
            "implementation_id": driver.implementation_id,
            "actual_training_interactions": ledger.training_interactions,
            "probe_environment_interactions": ledger.probe_interactions,
        },
    )
    result = PhaseAResult(
        request=request,
        ledger=ledger,
        probes=tuple(probes),
        final_checkpoint=checkpoint,
        completed=True,
    )
    return PhaseAExecution(result=result, final_adapter=driver.state_adapter)


@dataclass(frozen=True)
class BranchExecutionResult:
    branch: ProtocolV2Branch
    interactions: int
    metrics: Mapping[str, float]
    final_learner_state_sha256: str
    final_environment_state_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.branch, ProtocolV2Branch):
            raise ValueError("branch must be ProtocolV2Branch")
        if not isinstance(self.interactions, int) or isinstance(self.interactions, bool):
            raise ValueError("interactions must be an integer")
        if self.interactions <= 0:
            raise ValueError("interactions must be > 0")
        if not isinstance(self.metrics, Mapping) or not self.metrics:
            raise ValueError("branch metrics must be explicit and non-empty")
        if not self.final_learner_state_sha256 or not self.final_environment_state_sha256:
            raise ValueError("final state digests must be non-empty")


@runtime_checkable
class PhaseBBranchDriver(Protocol):
    """Method-native post-boundary branch execution surface."""

    branch: ProtocolV2Branch
    adaptive: bool
    learner: ScientificStateAdapter
    environment: GridWorldScientificStateAdapter

    @property
    def interactions(self) -> int: ...

    def run_to_interaction(self, target_interaction: int) -> Mapping[str, float]: ...


BranchDriverFactory = Callable[
    [ProtocolV2Branch, bool, ScientificStateAdapter, GridWorldScientificStateAdapter],
    PhaseBBranchDriver,
]


@dataclass(frozen=True)
class PhaseBExecution:
    branch_point_learner_sha256: str
    branch_point_environment_sha256: str
    results: tuple[BranchExecutionResult, ...]

    def __post_init__(self) -> None:
        if {item.branch for item in self.results} != set(ProtocolV2Branch):
            raise ValueError("PhaseBExecution must contain exactly the four branches")


def execute_phase_b(
    *,
    learner: ScientificStateAdapter,
    shared_environment: GridWorldScientificStateAdapter,
    nominal_spec: Any,
    disturbed_spec: Any,
    interaction_budget_per_branch: int,
    driver_factory: BranchDriverFactory,
) -> PhaseBExecution:
    """Execute the matched FN/FD/AN/AD post-boundary factorial.

    Learner clones are proven identical before execution. Environment branches
    restore the exact shared prefix; only the target branch scenario's declared
    post-boundary uncertainty/change mechanisms may differ.
    """

    learner_digest = learner.state_sha256()
    environment_digest = shared_environment.state_sha256()
    learner_branches = fork_four_branches(learner)
    ledger = PhaseBInteractionLedger(interaction_budget_per_branch)
    results: list[BranchExecutionResult] = []

    plans = {item.branch: item for item in FOUR_BRANCH_PLAN}
    for branch in ProtocolV2Branch:
        plan = plans[branch]
        environment_branch = shared_environment.fork_into(
            disturbed_spec if plan.disturbed else nominal_spec
        )
        state = environment_branch.export_state()
        source = shared_environment.export_state()
        for key in (
            "position",
            "step",
            "finished",
            "seeds",
            "action_rng_state",
            "observation_rng_state",
            "gym_np_random_state",
            "last_transition",
            "task_sha256",
        ):
            if state[key] != source[key]:
                raise RuntimeError(
                    f"branch {branch.value} environment differs before first post-boundary interaction"
                )

        branch_driver = driver_factory(
            branch,
            plan.adaptive,
            learner_branches[branch],
            environment_branch,
        )
        if not isinstance(branch_driver, PhaseBBranchDriver):
            raise ValueError("driver_factory must return PhaseBBranchDriver")
        if branch_driver.branch is not branch or branch_driver.adaptive is not plan.adaptive:
            raise ValueError("branch driver factor assignment mismatch")
        if branch_driver.interactions != 0:
            raise ValueError("Phase-B branch driver must start at interaction index 0")
        if branch_driver.learner.state_sha256() != learner_digest:
            raise RuntimeError("branch learner is not identical at fork")

        metrics = branch_driver.run_to_interaction(interaction_budget_per_branch)
        if branch_driver.interactions != interaction_budget_per_branch:
            raise RuntimeError(
                f"branch {branch.value} failed exact post-boundary interaction target"
            )
        ledger.record(branch, branch_driver.interactions)
        results.append(
            BranchExecutionResult(
                branch=branch,
                interactions=branch_driver.interactions,
                metrics=dict(metrics),
                final_learner_state_sha256=branch_driver.learner.state_sha256(),
                final_environment_state_sha256=branch_driver.environment.state_sha256(),
            )
        )

    ledger.require_complete()
    return PhaseBExecution(
        branch_point_learner_sha256=learner_digest,
        branch_point_environment_sha256=environment_digest,
        results=tuple(results),
    )
