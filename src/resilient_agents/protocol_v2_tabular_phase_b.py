"""Post-boundary project-driver semantics for protocol-v2 Phase B.

Frozen means that scientific *learning* state is immutable after the branch
point. Behavior RNG and inference-only counters may advance because they affect
or record action execution, but Q values, SARSA deferred-learning state and
Dyna-Q+ model/recency/planning state may not change.

The driver executes one exact post-boundary environment segment. It deliberately
fails if the configured branch interaction target would require an environment
reset; multi-episode Phase-B lifecycle semantics remain a T-526/T-527 protocol
choice rather than being invented inside the backend implementation.
"""
from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from .contracts import AgentTransition, project_for_agent
from .environment import EnvironmentSeeds
from .gridworld import ACTION_NAMES, GridAction
from .protocol_v2 import (
    NativeStateAdapter,
    ProtocolV2Branch,
    ScientificStateAdapter,
    TabularQScientificStateAdapter,
    require_information_limited_transition,
)
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_multi_episode import reset_gridworld_branch_episode


def _agent(adapter: ScientificStateAdapter) -> Any:
    if isinstance(adapter, TabularQScientificStateAdapter):
        return adapter.agent
    if isinstance(adapter, NativeStateAdapter):
        return adapter.agent
    raise ValueError("unsupported project scientific-state adapter")


def _json_key(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _learning_state(adapter: ScientificStateAdapter) -> Mapping[str, Any]:
    state = adapter.export_state()
    if adapter.method_id == "q_learning":
        return {"checkpoint": state["checkpoint"]}
    if adapter.method_id == "sarsa":
        return {
            "checkpoint": state["checkpoint"],
            "deferred_update": state["deferred_update"],
        }
    if adapter.method_id == "dyna_q_plus":
        return {
            "checkpoint": state["checkpoint"],
            "model": state["model"],
            "time": state["time"],
            "planning_update_count": state["planning_update_count"],
            "planning_rng_state": state["planning_rng_state"],
        }
    raise ValueError("unsupported project method_id")


def _pending_is_clear(adapter: ScientificStateAdapter) -> bool:
    state = adapter.export_state()
    if adapter.method_id == "q_learning":
        return state["pending_action"] is None
    if adapter.method_id == "sarsa":
        return state["pending_action"] is None and state["deferred_update"] is None
    if adapter.method_id == "dyna_q_plus":
        return state["pending"] is None
    return False


def _frozen_act(adapter: ScientificStateAdapter, observation: Any) -> Any:
    agent = _agent(adapter)
    if adapter.method_id in {"q_learning", "sarsa"}:
        # With a quiescent fork, these act paths mutate behavior RNG/pending state
        # only. SARSA is rejected at construction if a deferred backup exists.
        return agent.act(observation)
    if adapter.method_id == "dyna_q_plus":
        agent._require_reset()
        if agent._pending is not None:
            raise RuntimeError("Dyna-Q+ frozen action has unconsumed pending state")
        state_key = _json_key(observation)
        # Do not call DynaQPlusAgent.act(): it invokes _ensure_state_model and
        # would therefore mutate the learned model during Frozen deployment.
        action_key = agent._greedy_or_explore(state_key)
        agent._pending = (state_key, action_key)
        return agent._action_by_key[action_key]
    raise ValueError("unsupported project method_id")


def _frozen_consume(
    adapter: ScientificStateAdapter,
    transition: AgentTransition,
) -> None:
    require_information_limited_transition(transition)
    agent = _agent(adapter)
    intended_key = _json_key(transition.intended_action)

    if adapter.method_id == "q_learning":
        if agent._pending is None or agent._pending[1] != intended_key:
            raise RuntimeError("Q Frozen pending action mismatch")
        agent._pending = None
        agent._last_step = transition.step
        agent._observed_transition_count += 1
        return

    if adapter.method_id == "sarsa":
        if agent._deferred_update is not None:
            raise RuntimeError("Frozen SARSA cannot carry a deferred learning update")
        if agent._pending_action is None or agent._pending_action[1] != intended_key:
            raise RuntimeError("SARSA Frozen pending action mismatch")
        agent._pending_action = None
        agent._last_step = transition.step
        agent._observed_transition_count += 1
        return

    if adapter.method_id == "dyna_q_plus":
        if agent._pending is None or agent._pending[1] != intended_key:
            raise RuntimeError("Dyna-Q+ Frozen pending action mismatch")
        agent._pending = None
        agent._last_step = transition.step
        agent._observed_transition_count += 1
        return

    raise ValueError("unsupported project method_id")


class ProjectTabularPhaseBBranchDriver:
    """One exact FN/FD/AN/AD branch for Q/SARSA/Dyna-Q+."""

    def __init__(
        self,
        *,
        branch: ProtocolV2Branch,
        adaptive: bool,
        learner: ScientificStateAdapter,
        environment: GridWorldScientificStateAdapter,
        subsequent_episode_seeds: Sequence[EnvironmentSeeds] = (),
    ) -> None:
        if learner.method_id not in {"q_learning", "sarsa", "dyna_q_plus"}:
            raise ValueError("project Phase-B driver supports Q, SARSA or Dyna-Q+")
        if not isinstance(environment, GridWorldScientificStateAdapter):
            raise ValueError("environment must be GridWorldScientificStateAdapter")
        if not _pending_is_clear(learner):
            raise ValueError(
                "project Phase-B branch requires a quiescent learner fork with no pending/deferred update"
            )
        self.branch = branch
        self.adaptive = adaptive
        self.learner = learner
        self.environment = environment
        self._agent = _agent(learner)
        self._subsequent_episode_seeds = tuple(subsequent_episode_seeds)
        if any(
            not isinstance(item, EnvironmentSeeds)
            for item in self._subsequent_episode_seeds
        ):
            raise ValueError("subsequent_episode_seeds must be EnvironmentSeeds")
        self._next_episode_seed = 0
        self._interactions = 0
        state = learner.export_state()
        last_step = state.get("last_step")
        self._next_agent_step = 0 if last_step is None else int(last_step) + 1
        self._frozen_learning_state = None if adaptive else _learning_state(learner)
        self._return_sum = 0.0
        self._terminated = False
        self._truncated = False
        self._episodes_started = 1
        self._episodes_completed = 0

    @property
    def interactions(self) -> int:
        return self._interactions

    def run_to_interaction(self, target_interaction: int) -> Mapping[str, float]:
        if (
            not isinstance(target_interaction, int)
            or isinstance(target_interaction, bool)
            or target_interaction < self._interactions
        ):
            raise ValueError("target_interaction must be an integer >= current interactions")

        prefix_transition = self.environment.environment.gym_env.last_transition
        if prefix_transition is None:
            raise RuntimeError(
                "Phase-B branch requires a delivered pre-change prefix observation; evaluator truth is not a fallback"
            )
        current_observation = prefix_transition.delivered_observation

        while self._interactions < target_interaction:
            if self._terminated or self._truncated:
                if self._next_episode_seed >= len(self._subsequent_episode_seeds):
                    raise RuntimeError("declared Phase-B episode seed sequence exhausted")
                self._agent.end_episode(
                    {
                        "episode_index": self._episodes_started - 1,
                        "outcome": "terminated" if self._terminated else "truncated",
                        "global_post_boundary_interactions": self._interactions,
                    }
                )
                current_observation = reset_gridworld_branch_episode(
                    self.environment,
                    seeds=self._subsequent_episode_seeds[self._next_episode_seed],
                )
                self._next_episode_seed += 1
                self._episodes_started += 1
                self._terminated = False
                self._truncated = False
            action_name = (
                self._agent.act(current_observation)
                if self.adaptive
                else _frozen_act(self.learner, current_observation)
            )
            if action_name not in ACTION_NAMES:
                raise ValueError("project learner returned an unknown action")
            truth = self.environment.environment.step(int(GridAction[action_name.upper()]))
            visible = replace(
                project_for_agent(
                    truth, self.environment.environment.information_policy
                ),
                step=self._next_agent_step,
            )
            if self.adaptive:
                self._agent.observe(visible)
            else:
                _frozen_consume(self.learner, visible)
                if _learning_state(self.learner) != self._frozen_learning_state:
                    raise RuntimeError(
                        f"Frozen branch {self.branch.value} mutated scientific learning state"
                    )
            self._next_agent_step += 1
            self._interactions += 1
            self._return_sum += float(truth.reward)
            self._terminated = bool(truth.terminated)
            self._truncated = bool(truth.truncated)
            if self._terminated or self._truncated:
                self._episodes_completed += 1
            current_observation = truth.delivered_observation

        return {
            "return_sum": float(self._return_sum),
            "terminated": float(self._terminated),
            "truncated": float(self._truncated),
            "adaptive": float(self.adaptive),
            "episodes_started": float(self._episodes_started),
            "episodes_completed": float(self._episodes_completed),
        }
