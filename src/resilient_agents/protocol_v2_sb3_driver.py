"""Method-native Stable-Baselines3 Phase-A driver and no-learning probes.

The driver plugs the exact SB3 scientific-state adapter into the framework-
neutral protocol-v2 executor.  Training targets are absolute actual interaction
indices.  Standardized probes act on an executor-supplied clone and therefore
cannot enter replay, optimizer, rollout or training RNG state.
"""
from __future__ import annotations

import math
from statistics import fmean
from typing import Any, Callable, Sequence

from .protocol_v2 import ScientificStateAdapter
from .protocol_v2_runtime import ProbeResult
from .protocol_v2_sb3 import SB3ScientificStateAdapter

SB3_IMPLEMENTATION_ID = "stable-baselines3-scientific-state-adapter"


class SB3PhaseADriver:
    """Phase-A training driver for DQN/PPO scientific adapters."""

    implementation_id = SB3_IMPLEMENTATION_ID

    def __init__(self, adapter: SB3ScientificStateAdapter) -> None:
        if not isinstance(adapter, SB3ScientificStateAdapter):
            raise ValueError("adapter must be SB3ScientificStateAdapter")
        if int(adapter.model.num_timesteps) != 0:
            raise ValueError("Phase-A SB3 driver must start from zero interactions")
        self.state_adapter = adapter
        self.method_id = adapter.method_id

    @property
    def training_interactions(self) -> int:
        return int(self.state_adapter.model.num_timesteps)

    def train_to_interaction(self, target_interaction: int) -> None:
        self.state_adapter.learn_to_total_interactions(target_interaction)
        if self.training_interactions != target_interaction:
            raise RuntimeError("SB3 Phase-A driver failed exact interaction target")


def _scalar_action(action: Any) -> Any:
    if hasattr(action, "shape") and getattr(action, "size", None) == 1:
        return action.item()
    return action


class SB3NoLearningProbeEvaluator:
    """Standardized isolated evaluation for a cloned DQN/PPO learner.

    No scientific seed defaults are hidden here.  The caller supplies an exact
    sequence of episode seeds and explicitly selects deterministic versus
    stochastic inference.  Probe interactions are returned for separate ledger
    accounting and never passed to ``model.learn``.
    """

    def __init__(
        self,
        *,
        environment_factory: Callable[[], Any],
        episode_seeds: Sequence[int],
        deterministic: bool,
    ) -> None:
        if not callable(environment_factory):
            raise ValueError("environment_factory must be callable")
        seeds = tuple(episode_seeds)
        if not seeds:
            raise ValueError("episode_seeds must be explicit and non-empty")
        if any(
            not isinstance(seed, int) or isinstance(seed, bool) or seed < 0
            for seed in seeds
        ):
            raise ValueError("probe episode seeds must be integers >= 0")
        if len(set(seeds)) != len(seeds):
            raise ValueError("probe episode seeds must be unique")
        if not isinstance(deterministic, bool):
            raise ValueError("deterministic must be boolean")
        self.environment_factory = environment_factory
        self.episode_seeds = seeds
        self.deterministic = deterministic

    def __call__(
        self,
        adapter: ScientificStateAdapter,
        *,
        training_interaction_index: int,
        episodes: int,
    ) -> ProbeResult:
        if not isinstance(adapter, SB3ScientificStateAdapter):
            raise ValueError("SB3 probe requires SB3ScientificStateAdapter")
        if not isinstance(episodes, int) or isinstance(episodes, bool) or episodes <= 0:
            raise ValueError("episodes must be an integer > 0")
        if episodes > len(self.episode_seeds):
            raise ValueError("not enough predeclared probe episode seeds")
        if training_interaction_index < 0:
            raise ValueError("training_interaction_index must be >= 0")

        returns: list[float] = []
        lengths: list[int] = []
        terminated_count = 0
        truncated_count = 0
        interactions = 0

        for seed in self.episode_seeds[:episodes]:
            env = self.environment_factory()
            try:
                observation, info = env.reset(seed=seed)
                if info:
                    # The standardized agent-visible evaluator must not rely on
                    # environment reset metadata.
                    raise ValueError("probe environment reset info must be empty")
                episode_return = 0.0
                episode_length = 0
                while True:
                    action = _scalar_action(
                        adapter.predict(observation, deterministic=self.deterministic)
                    )
                    observation, reward, terminated, truncated, info = env.step(action)
                    if info:
                        raise ValueError("probe environment step info must be empty")
                    reward_value = float(reward)
                    if not math.isfinite(reward_value):
                        raise ValueError("probe reward must be finite")
                    episode_return += reward_value
                    episode_length += 1
                    interactions += 1
                    if terminated or truncated:
                        terminated_count += int(bool(terminated))
                        truncated_count += int(bool(truncated))
                        break
                returns.append(episode_return)
                lengths.append(episode_length)
            finally:
                close = getattr(env, "close", None)
                if callable(close):
                    close()

        return ProbeResult(
            training_interaction_index=training_interaction_index,
            probe_environment_interactions=interactions,
            episodes=episodes,
            metrics={
                "return_mean": float(fmean(returns)),
                "episode_length_mean": float(fmean(lengths)),
                "terminated_rate": terminated_count / episodes,
                "truncated_rate": truncated_count / episodes,
            },
        )
