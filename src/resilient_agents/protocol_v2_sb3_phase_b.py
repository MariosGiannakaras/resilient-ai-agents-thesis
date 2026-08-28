"""Protocol-v2 Phase-B branch execution for SB3 DQN/PPO.

Frozen branches perform inference only: model/optimizer/replay/counters remain
unchanged while behavior RNG may advance. Adaptive branches resume ordinary
method-native SB3 learning from the exact learner checkpoint while the first
environment reset attaches to the already-restored GridWorld branch point.

This driver intentionally supports one exact post-boundary segment only.
Environment reset after termination/truncation remains fail-closed until the
multi-episode Phase-B lifecycle is frozen by T-526/T-527.
"""
from __future__ import annotations

from typing import Any, Mapping

from .protocol_v2 import ProtocolV2Branch
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_sb3 import SB3ScientificStateAdapter
from .protocol_v2_sb3_gridworld import BranchContinuationGridWorldEnv


def _scalar_action(action: Any) -> Any:
    if hasattr(action, "shape") and getattr(action, "size", None) == 1:
        return action.item()
    return action


def _frozen_learning_state(adapter: SB3ScientificStateAdapter) -> Mapping[str, Any]:
    """Return all SB3 state that Frozen deployment is forbidden to mutate."""

    state = adapter.export_state()
    return {
        "schema_version": state["schema_version"],
        "method_id": state["method_id"],
        "provenance": state["provenance"],
        "configuration": state["configuration"],
        "model_zip_b64": state["model_zip_b64"],
        "replay_buffer_b64": state["replay_buffer_b64"],
        "counters": state["counters"],
    }


class SB3PhaseBBranchDriver:
    """One exact FN/FD/AN/AD branch for DQN or PPO."""

    def __init__(
        self,
        *,
        branch: ProtocolV2Branch,
        adaptive: bool,
        learner: SB3ScientificStateAdapter,
        environment: GridWorldScientificStateAdapter,
        deterministic_inference: bool,
    ) -> None:
        if learner.method_id not in {"dqn", "ppo"}:
            raise ValueError("SB3 Phase-B driver supports DQN or PPO")
        if not isinstance(branch, ProtocolV2Branch):
            raise ValueError("branch must be ProtocolV2Branch")
        if not isinstance(adaptive, bool):
            raise ValueError("adaptive must be boolean")
        if not isinstance(environment, GridWorldScientificStateAdapter):
            raise ValueError("environment must be GridWorldScientificStateAdapter")
        if not isinstance(deterministic_inference, bool):
            raise ValueError("deterministic_inference must be boolean")
        if environment.environment.gym_env.last_transition is None:
            raise ValueError("SB3 Phase-B requires a delivered pre-change prefix observation")
        if environment.environment.gym_env._finished:
            raise ValueError("SB3 Phase-B cannot start from a finished environment")
        if learner.model.get_env() is not None:
            raise ValueError(
                "SB3 Phase-B learner clone must be detached from its Phase-A environment"
            )

        self.branch = branch
        self.adaptive = adaptive
        self.learner = learner
        self.environment = environment
        self.deterministic_inference = deterministic_inference
        self._interactions = 0
        self._return_sum = 0.0
        self._terminated = False
        self._truncated = False
        self._base_model_interactions = int(learner.model.num_timesteps)
        self._continuation = BranchContinuationGridWorldEnv(environment)
        self._frozen_state = None if adaptive else _frozen_learning_state(learner)
        if adaptive:
            # The scientific-state fingerprint deliberately excludes the
            # environment factory. It is execution plumbing, not learner state.
            self.learner.environment_factory = lambda: self._continuation

    @property
    def interactions(self) -> int:
        return self._interactions

    def _run_frozen_to(self, target_interaction: int) -> Mapping[str, float]:
        if self._interactions == 0:
            observation, info = self._continuation.reset()
            if info:
                raise RuntimeError("Phase-B continuation reset leaked information")
        else:
            transition = self.environment.environment.gym_env.last_transition
            if transition is None:
                raise RuntimeError("Phase-B branch lost its delivered observation")
            observation = transition.delivered_observation

        while self._interactions < target_interaction:
            if self._terminated or self._truncated:
                raise RuntimeError(
                    "Phase-B segment ended before target; multi-episode reset semantics are not frozen yet"
                )
            action = _scalar_action(
                self.learner.predict(
                    observation,
                    deterministic=self.deterministic_inference,
                )
            )
            observation, reward, terminated, truncated, info = self._continuation.step(action)
            if info:
                raise RuntimeError("Phase-B continuation step leaked information")
            self._interactions += 1
            self._return_sum += float(reward)
            self._terminated = bool(terminated)
            self._truncated = bool(truncated)

        if _frozen_learning_state(self.learner) != self._frozen_state:
            raise RuntimeError(f"Frozen SB3 branch {self.branch.value} mutated learning state")
        return self._metrics()

    def _run_adaptive_to(self, target_interaction: int) -> Mapping[str, float]:
        absolute_target = self._base_model_interactions + target_interaction
        self.learner.learn_to_total_interactions(absolute_target)
        if self._continuation.interactions != target_interaction:
            raise RuntimeError("SB3 adaptive branch environment interactions do not reconcile")
        self._interactions = target_interaction
        self._return_sum = self._continuation.return_sum
        self._terminated = self._continuation.terminated
        self._truncated = self._continuation.truncated
        return self._metrics()

    def _metrics(self) -> Mapping[str, float]:
        return {
            "return_sum": float(self._return_sum),
            "terminated": float(self._terminated),
            "truncated": float(self._truncated),
            "adaptive": float(self.adaptive),
            "deterministic_inference": float(self.deterministic_inference),
        }

    def run_to_interaction(self, target_interaction: int) -> Mapping[str, float]:
        if (
            not isinstance(target_interaction, int)
            or isinstance(target_interaction, bool)
            or target_interaction < self._interactions
        ):
            raise ValueError("target_interaction must be an integer >= current interactions")
        if target_interaction == self._interactions:
            return self._metrics()
        if self.adaptive:
            return self._run_adaptive_to(target_interaction)
        return self._run_frozen_to(target_interaction)
