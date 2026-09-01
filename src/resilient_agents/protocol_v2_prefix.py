"""Shared no-learning prefix preparation for protocol-v2 Phase B.

Phase B may begin with one nominal environment prefix executed under the exact
Phase-A behavior-policy state but with learning disabled.  This module owns that
boundary so Study orchestration does not reimplement learner-specific Frozen
semantics.

The prefix is intentionally one environment segment.  If it terminates or
truncates before the branch point, execution fails closed; multi-episode prefix
or post-boundary reset semantics remain a T-526/T-527 protocol decision.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from .contracts import ScenarioSpec, project_for_agent
from .environment import EnvironmentSeeds
from .gridworld import ACTION_NAMES, GridAction, GridWorldEnvironment
from .protocol_v2 import ScientificStateAdapter
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_sb3 import SB3ScientificStateAdapter
from .protocol_v2_sb3_observation import predict_sb3_gridworld_action
from .protocol_v2_sb3_phase_b import _frozen_learning_state as _sb3_frozen_learning_state
from .protocol_v2_tabular_phase_b import (
    _frozen_act as _project_frozen_act,
    _frozen_consume as _project_frozen_consume,
    _learning_state as _project_learning_state,
    _pending_is_clear as _project_pending_is_clear,
)


@dataclass(frozen=True)
class SharedNoLearningPrefix:
    """Exact branch-point state after a common nominal no-learning prefix."""

    learner: ScientificStateAdapter
    environment: GridWorldScientificStateAdapter
    interactions: int
    learner_state_sha256: str
    environment_state_sha256: str

    def __post_init__(self) -> None:
        if self.interactions <= 0:
            raise ValueError("shared prefix interactions must be > 0")
        if self.learner.state_sha256() != self.learner_state_sha256:
            raise ValueError("shared prefix learner digest mismatch")
        if self.environment.state_sha256() != self.environment_state_sha256:
            raise ValueError("shared prefix environment digest mismatch")


def _scalar_action(action: Any) -> Any:
    if hasattr(action, "shape") and getattr(action, "size", None) == 1:
        return action.item()
    return action


def prepare_shared_no_learning_prefix(
    *,
    learner: ScientificStateAdapter,
    nominal_spec: ScenarioSpec,
    environment_seeds: EnvironmentSeeds,
    interactions: int,
) -> SharedNoLearningPrefix:
    """Advance one exact nominal prefix without changing scientific learning state.

    Behavior-policy RNG is allowed to advance because it is part of actual
    deployment behavior.  Project learner bookkeeping counters may also advance;
    Q/model/optimizer/replay/planning learning state may not.
    """

    if not isinstance(nominal_spec, ScenarioSpec):
        raise ValueError("nominal_spec must be ScenarioSpec")
    if not isinstance(environment_seeds, EnvironmentSeeds):
        raise ValueError("environment_seeds must be EnvironmentSeeds")
    if not isinstance(interactions, int) or isinstance(interactions, bool) or interactions <= 0:
        raise ValueError("interactions must be an integer > 0")

    environment = GridWorldEnvironment(nominal_spec)
    observation = environment.reset(seeds=environment_seeds)
    environment_adapter = GridWorldScientificStateAdapter(environment)

    project_method = learner.method_id in {"q_learning", "sarsa", "dyna_q_plus"}
    if project_method:
        if not _project_pending_is_clear(learner):
            environment.close()
            raise ValueError(
                "shared no-learning prefix requires a quiescent project learner; "
                "pending/deferred Phase-A state must be resolved by the frozen protocol"
            )
        frozen_learning_state = _project_learning_state(learner)
        learner_state = learner.export_state()
        last_step = learner_state.get("last_step")
        next_agent_step = 0 if last_step is None else int(last_step) + 1
    elif isinstance(learner, SB3ScientificStateAdapter):
        frozen_learning_state = _sb3_frozen_learning_state(learner)
        next_agent_step = None
    else:
        environment.close()
        raise ValueError(f"unsupported shared-prefix learner method: {learner.method_id!r}")

    try:
        for index in range(interactions):
            if environment.gym_env._finished:
                raise RuntimeError(
                    "shared no-learning prefix reached a finished environment before the branch point"
                )

            if project_method:
                action_name = _project_frozen_act(learner, observation)
                if action_name not in ACTION_NAMES:
                    raise ValueError("project learner returned an unknown GridWorld action")
                truth = environment.step(int(GridAction[str(action_name).upper()]))
                visible = replace(
                    project_for_agent(truth, environment.information_policy),
                    step=next_agent_step,
                )
                _project_frozen_consume(learner, visible)
                next_agent_step += 1
                if _project_learning_state(learner) != frozen_learning_state:
                    raise RuntimeError("shared prefix mutated project scientific learning state")
            else:
                action = _scalar_action(
                    predict_sb3_gridworld_action(
                        learner,
                        observation,
                        environment.gym_env.observation_space,
                        deterministic=False,
                    )
                )
                truth = environment.step(int(action))
                if _sb3_frozen_learning_state(learner) != frozen_learning_state:
                    raise RuntimeError("shared prefix mutated SB3 scientific learning state")

            observation = truth.delivered_observation
            if truth.terminated or truth.truncated:
                raise RuntimeError(
                    "shared no-learning prefix ended at/before the requested branch point; "
                    "multi-episode prefix semantics are not frozen"
                )

        if environment.gym_env.last_transition is None:
            raise RuntimeError("shared no-learning prefix produced no delivered transition")
        return SharedNoLearningPrefix(
            learner=learner,
            environment=environment_adapter,
            interactions=interactions,
            learner_state_sha256=learner.state_sha256(),
            environment_state_sha256=environment_adapter.state_sha256(),
        )
    except Exception:
        environment.close()
        raise
