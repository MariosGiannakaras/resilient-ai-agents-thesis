"""Recovery-specific T-526 Phase-B evidence drivers.

The module composes the validated protocol-v2 branch drivers and executor.  It
adds evaluator-side disturbance occurrence counters and one deliberately narrow
PPO facility: exact collection of the predeclared ten-interaction pilot segment
when that segment is shorter than PPO's native 128-interaction update quantum.
The original Phase-A adapter/checkpoint semantics remain untouched.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .contracts import GroundTruthTransition
from .protocol_v2 import ProtocolV2Branch, ScientificStateAdapter
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_sb3 import SB3ScientificStateAdapter, _digest_value
from .protocol_v2_sb3_gridworld import BranchContinuationGridWorldEnv
from .protocol_v2_sb3_observation import predict_sb3_gridworld_action
from .protocol_v2_sb3_phase_b import (
    SB3PhaseBBranchDriver,
    _frozen_learning_state,
    _scalar_action,
)
from .protocol_v2_tabular_phase_b import ProjectTabularPhaseBBranchDriver


@dataclass
class DisturbanceRecorder:
    """Evaluator-visible occurrence counts without changing transition semantics."""

    interactions: int = 0
    action_failures: int = 0
    observation_corruptions: int = 0
    action_remap_effects: int = 0
    change_onsets: int = 0

    def record(self, transition: GroundTruthTransition) -> None:
        self.interactions += 1
        self.action_failures += int(
            bool(transition.disturbance_flags.get("action_failure", False))
        )
        self.observation_corruptions += int(
            bool(transition.disturbance_flags.get("observation_corruption", False))
        )
        self.action_remap_effects += int(
            transition.regime_id not in {None, "nominal"}
            and transition.executed_action != transition.intended_action
        )
        self.change_onsets += len(transition.change_event_ids)

    def metrics(self) -> Mapping[str, float]:
        return {
            "diagnostic_interactions": float(self.interactions),
            "realized_action_failures": float(self.action_failures),
            "realized_observation_corruptions": float(
                self.observation_corruptions
            ),
            "realized_action_remap_effects": float(self.action_remap_effects),
            "realized_change_onsets": float(self.change_onsets),
        }


def attach_disturbance_recorder(
    environment: GridWorldScientificStateAdapter,
) -> DisturbanceRecorder:
    """Observe ground truth at the evidence boundary only.

    The wrapped callable delegates to the original environment step first and
    returns the exact same immutable transition object.
    """

    recorder = DisturbanceRecorder()
    gridworld = environment.environment
    original_step = gridworld.step

    def recorded_step(intended_action: int) -> GroundTruthTransition:
        transition = original_step(intended_action)
        recorder.record(transition)
        return transition

    gridworld.step = recorded_step  # type: ignore[method-assign]
    return recorder


class RecordedBranchDriver:
    """Add evaluator-side occurrence metrics to an existing branch driver."""

    def __init__(self, delegate: Any, recorder: DisturbanceRecorder) -> None:
        self._delegate = delegate
        self._recorder = recorder
        self.branch = delegate.branch
        self.adaptive = delegate.adaptive
        self.learner = delegate.learner
        self.environment = delegate.environment

    @property
    def interactions(self) -> int:
        return int(self._delegate.interactions)

    def run_to_interaction(self, target_interaction: int) -> Mapping[str, float]:
        metrics = dict(self._delegate.run_to_interaction(target_interaction))
        if self._recorder.interactions != self.interactions:
            raise RuntimeError("disturbance diagnostics do not reconcile with branch interactions")
        metrics.update(self._recorder.metrics())
        return metrics


class T526PPOTransientStateAdapter:
    """PPO adapter whose final pilot-only partial rollout can be fingerprinted.

    Exact scientific checkpoint export/restore remains delegated to the strict
    project adapter and therefore remains illegal at a partial rollout.
    """

    method_id = "ppo"

    def __init__(self, inner: SB3ScientificStateAdapter) -> None:
        if not isinstance(inner, SB3ScientificStateAdapter) or inner.method_id != "ppo":
            raise ValueError("T-526 transient adapter requires the project PPO adapter")
        self.inner = inner

    def export_state(self) -> Mapping[str, Any]:
        return self.inner.export_state()

    def restore_state(self, state: Mapping[str, Any]) -> None:
        self.inner.restore_state(state)

    def clone(self) -> "T526PPOTransientStateAdapter":
        return T526PPOTransientStateAdapter(self.inner.clone())

    def predict(self, observation: Any, *, deterministic: bool) -> Any:
        return self.inner.predict(observation, deterministic=deterministic)

    def state_sha256(self) -> str:
        rollout = self.inner.model.rollout_buffer
        pos = int(rollout.pos)
        if pos in {0, int(rollout.buffer_size)}:
            return self.inner.state_sha256()
        model = self.inner.model
        payload = {
            "schema": "t526-ppo-partial-rollout-fingerprint-v1",
            "method_id": "ppo",
            "provenance": self.inner.provenance.__dict__,
            "configuration": self.inner.configuration,
            "parameters": model.get_parameters(),
            "counters": {
                "num_timesteps": int(model.num_timesteps),
                "n_updates": int(model._n_updates),
                "current_progress_remaining": float(
                    model._current_progress_remaining
                ),
                "total_timesteps": int(model._total_timesteps),
                "n_envs": int(model.n_envs),
                "rollout_boundary": "partial-t526-pilot-only",
                "rollout_buffer_size": int(rollout.buffer_size),
                "rollout_pos": pos,
            },
            "rng_state": self.inner._rng_state,
            "action_space_rng_state": self.inner._action_space_rng_state,
            "last_observation": model._last_obs,
            "last_episode_starts": model._last_episode_starts,
            "partial_rollout": {
                "observations": rollout.observations[:pos],
                "actions": rollout.actions[:pos],
                "rewards": rollout.rewards[:pos],
                "episode_starts": rollout.episode_starts[:pos],
                "values": rollout.values[:pos],
                "log_probs": rollout.log_probs[:pos],
            },
        }
        return _digest_value(payload)


class T526PPOPhaseBBranchDriver:
    """Exact T-526 PPO branch with a ten-step partial Adaptive rollout."""

    def __init__(
        self,
        *,
        branch: ProtocolV2Branch,
        adaptive: bool,
        learner: T526PPOTransientStateAdapter,
        environment: GridWorldScientificStateAdapter,
        deterministic_inference: bool,
    ) -> None:
        if not isinstance(learner, T526PPOTransientStateAdapter):
            raise ValueError("T-526 PPO driver requires its transient adapter")
        if learner.inner.model.get_env() is not None:
            raise ValueError("T-526 PPO branch learner must be detached")
        if environment.environment.gym_env.last_transition is None:
            raise ValueError("T-526 PPO Phase B requires the common prefix")
        self.branch = branch
        self.adaptive = adaptive
        self.learner = learner
        self.environment = environment
        self.deterministic_inference = deterministic_inference
        self._continuation = BranchContinuationGridWorldEnv(environment)
        self._interactions = 0
        self._return_sum = 0.0
        self._terminated = False
        self._truncated = False
        self._base_model_interactions = int(learner.inner.model.num_timesteps)
        self._base_updates = int(learner.inner.model._n_updates)
        self._frozen_state = (
            None if adaptive else _frozen_learning_state(learner.inner)
        )
        self._recorder = attach_disturbance_recorder(environment)

    @property
    def interactions(self) -> int:
        return self._interactions

    def _metrics(self) -> Mapping[str, float]:
        model = self.learner.inner.model
        metrics = {
            "return_sum": float(self._return_sum),
            "terminated": float(self._terminated),
            "truncated": float(self._truncated),
            "adaptive": float(self.adaptive),
            "deterministic_inference": float(self.deterministic_inference),
            "adaptive_collection_started_at_interaction": float(
                1 if self.adaptive and self._interactions else 0
            ),
            "optimizer_updates_during_branch": float(
                int(model._n_updates) - self._base_updates
            ),
            "partial_rollout_interactions": float(
                int(model.rollout_buffer.pos) if self.adaptive else 0
            ),
        }
        metrics.update(self._recorder.metrics())
        return metrics

    def _run_frozen(self, target_interaction: int) -> None:
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
                raise RuntimeError("T-526 no-reset Phase-B segment ended early")
            action = _scalar_action(
                predict_sb3_gridworld_action(
                    self.learner,
                    observation,
                    self._continuation.observation_space,
                    deterministic=self.deterministic_inference,
                )
            )
            observation, reward, terminated, truncated, info = self._continuation.step(
                action
            )
            if info:
                raise RuntimeError("Phase-B continuation step leaked information")
            self._interactions += 1
            self._return_sum += float(reward)
            self._terminated = bool(terminated)
            self._truncated = bool(truncated)
        if _frozen_learning_state(self.learner.inner) != self._frozen_state:
            raise RuntimeError(f"Frozen PPO branch {self.branch.value} mutated learning state")

    def _run_adaptive(self, target_interaction: int) -> None:
        if self._interactions != 0:
            raise RuntimeError("T-526 partial PPO rollout must execute atomically once")
        model = self.learner.inner.model
        if target_interaction <= 0 or target_interaction >= int(model.n_steps):
            raise ValueError("T-526 PPO partial rollout must be within one native quantum")
        model.set_env(self._continuation, force_reset=True)
        with self.learner.inner._rng_scope():
            _, callback = model._setup_learn(
                total_timesteps=target_interaction,
                callback=None,
                reset_num_timesteps=False,
                tb_log_name="t526-phase-b",
                progress_bar=False,
            )
            callback.on_training_start(locals(), globals())
            completed = model.collect_rollouts(
                model.env,
                callback,
                model.rollout_buffer,
                n_rollout_steps=target_interaction,
            )
            callback.on_training_end()
        if not completed:
            raise RuntimeError("PPO callback interrupted T-526 partial rollout")
        if int(model.num_timesteps) != self._base_model_interactions + target_interaction:
            raise RuntimeError("PPO T-526 interaction counter did not reconcile")
        if int(model._n_updates) != self._base_updates:
            raise RuntimeError("PPO optimizer updated before its native rollout quantum")
        if self._continuation.interactions != target_interaction:
            raise RuntimeError("PPO T-526 environment interactions did not reconcile")
        self._interactions = target_interaction
        self._return_sum = self._continuation.return_sum
        self._terminated = self._continuation.terminated
        self._truncated = self._continuation.truncated

    def run_to_interaction(self, target_interaction: int) -> Mapping[str, float]:
        if (
            not isinstance(target_interaction, int)
            or isinstance(target_interaction, bool)
            or target_interaction < self._interactions
        ):
            raise ValueError("target_interaction must be an integer >= current interactions")
        if target_interaction > self._interactions:
            if self.adaptive:
                self._run_adaptive(target_interaction)
            else:
                self._run_frozen(target_interaction)
        if self._recorder.interactions != self._interactions:
            raise RuntimeError("PPO disturbance diagnostics do not reconcile")
        return self._metrics()


def t526_branch_driver(
    *,
    branch: ProtocolV2Branch,
    adaptive: bool,
    learner: ScientificStateAdapter,
    environment: GridWorldScientificStateAdapter,
) -> Any:
    """Return the method-native driver plus evaluator diagnostics."""

    if learner.method_id == "ppo":
        if not isinstance(learner, T526PPOTransientStateAdapter):
            raise ValueError("T-526 PPO learner must use the transient pilot adapter")
        return T526PPOPhaseBBranchDriver(
            branch=branch,
            adaptive=adaptive,
            learner=learner,
            environment=environment,
            deterministic_inference=True,
        )

    recorder = attach_disturbance_recorder(environment)
    if learner.method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
        delegate = ProjectTabularPhaseBBranchDriver(
            branch=branch,
            adaptive=adaptive,
            learner=learner,
            environment=environment,
        )
    elif learner.method_id == "dqn":
        if not isinstance(learner, SB3ScientificStateAdapter):
            raise ValueError("T-526 DQN learner must use the project SB3 adapter")
        delegate = SB3PhaseBBranchDriver(
            branch=branch,
            adaptive=adaptive,
            learner=learner,
            environment=environment,
            deterministic_inference=True,
        )
    else:
        raise ValueError(f"unsupported T-526 Phase-B method: {learner.method_id!r}")
    return RecordedBranchDriver(delegate, recorder)
