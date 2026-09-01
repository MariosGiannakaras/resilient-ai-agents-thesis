"""Protocol-v2.1 passive temporal evidence for project tabular Phase B.

The historical Q-learning/SARSA/Dyna-Q+ driver remains immutable.  This v2.1
subclass preserves its branch lifecycle and adds one observational operation
after each actual environment step: recording the received reward into a fixed
32-interaction window.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace

from .contracts import project_for_agent
from .gridworld import ACTION_NAMES, GridAction
from .protocol_v2_multi_episode import reset_gridworld_branch_episode
from .protocol_v2_tabular_phase_b import (
    ProjectTabularPhaseBBranchDriver,
    _frozen_act,
    _frozen_consume,
    _learning_state,
)
from .protocol_v2_temporal import FixedRewardWindowRecorder, RewardWindow


class ProjectTabularPhaseBBranchDriverV21(ProjectTabularPhaseBBranchDriver):
    """Exact historical tabular branch semantics plus passive reward windows."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._reward_recorder = FixedRewardWindowRecorder(window_size=32)

    @property
    def reward_windows(self) -> tuple[RewardWindow, ...]:
        return self._reward_recorder.completed_windows

    def require_complete_reward_windows(self, *, total_interactions: int) -> None:
        self._reward_recorder.require_complete(total_interactions=total_interactions)

    def run_to_interaction(self, target_interaction: int) -> Mapping[str, float]:
        # This method intentionally mirrors the immutable parent method.  The
        # only scientific-output addition is _reward_recorder.record(...) after
        # the environment transition has already occurred.
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
            self._reward_recorder.record(float(truth.reward))
            self._terminated = bool(truth.terminated)
            self._truncated = bool(truth.truncated)
            if self._terminated or self._truncated:
                self._episodes_completed += 1
            current_observation = truth.delivered_observation

        state = self.learner.export_state()
        observed_delta = (
            int(state["observed_transition_count"])
            - self._base_observed_transition_count
        )
        if not self.adaptive:
            native_opportunities = 0
        elif self.learner.method_id == "sarsa":
            native_opportunities = observed_delta - int(
                state["deferred_update"] is not None
            )
        else:
            native_opportunities = observed_delta
        planning_updates = (
            int(state.get("planning_update_count", 0))
            - self._base_planning_update_count
            if self.adaptive and self.learner.method_id == "dyna_q_plus"
            else 0
        )
        if native_opportunities < 0 or planning_updates < 0:
            raise RuntimeError("project native update accounting regressed")
        return {
            "return_sum": float(self._return_sum),
            "terminated": float(self._terminated),
            "truncated": float(self._truncated),
            "adaptive": float(self.adaptive),
            "episodes_started": float(self._episodes_started),
            "episodes_completed": float(self._episodes_completed),
            "native_update_opportunities_completed": float(native_opportunities),
            "native_planning_updates_completed": float(planning_updates),
        }
