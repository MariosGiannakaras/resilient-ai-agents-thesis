"""Gymnasium facades connecting SB3 to the project-owned protocol-v2 GridWorld.

The facades do not add information or scientific defaults.

* ``ExplicitSeededGridWorldEnv`` is for nominal learning and consumes an exact,
  caller-supplied sequence of ``EnvironmentSeeds`` at episode resets.
* ``BranchContinuationGridWorldEnv`` is for one exact post-boundary Phase-B
  segment. Its first reset returns the already-delivered branch-point
  observation without mutating the underlying GridWorld. A second reset fails
  closed until multi-episode Phase-B reset semantics are frozen by T-526/T-527.
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import gymnasium as gym

from .contracts import ScenarioSpec
from .environment import EnvironmentSeeds
from .gridworld import GridWorldEnvironment
from .protocol_v2_gridworld import (
    GridWorldScientificStateAdapter,
    reset_gridworld_branch_episode,
)


class ExplicitSeededGridWorldEnv(gym.Env):
    """SB3-compatible GridWorld with explicit per-episode environment seeds."""

    metadata = {"render_modes": []}

    def __init__(
        self,
        *,
        scenario: ScenarioSpec,
        episode_seeds: Sequence[EnvironmentSeeds],
    ) -> None:
        super().__init__()
        seeds = tuple(episode_seeds)
        if not seeds or any(not isinstance(item, EnvironmentSeeds) for item in seeds):
            raise ValueError("episode_seeds must be a non-empty explicit EnvironmentSeeds sequence")
        self._environment = GridWorldEnvironment(scenario)
        self.action_space = self._environment.gym_env.action_space
        self.observation_space = self._environment.gym_env.observation_space
        self._episode_seeds = seeds
        self._next_episode = 0

    @property
    def environment(self) -> GridWorldEnvironment:
        return self._environment

    @property
    def consumed_episode_seeds(self) -> int:
        return self._next_episode

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None):
        del options
        if seed is not None and (not isinstance(seed, int) or isinstance(seed, bool) or seed < 0):
            raise ValueError("Gymnasium seed must be a non-negative integer when supplied")
        if self._next_episode >= len(self._episode_seeds):
            raise RuntimeError("explicit GridWorld episode seed sequence exhausted")
        episode_seeds = self._episode_seeds[self._next_episode]
        # SB3's algorithm seed and the project's environment seed are separate
        # scientific streams. The Gymnasium seed supplied by SB3 is therefore
        # intentionally not forwarded into the project environment; the exact
        # predeclared EnvironmentSeeds object remains authoritative.
        observation = self._environment.reset(seeds=episode_seeds)
        self._next_episode += 1
        return observation, {}

    def step(self, action):
        transition = self._environment.step(int(action))
        return (
            transition.delivered_observation,
            float(transition.reward),
            bool(transition.terminated),
            bool(transition.truncated),
            {},
        )

    def close(self) -> None:
        self._environment.close()


class BranchContinuationGridWorldEnv(gym.Env):
    """Expose an exact protocol-v2 branch and declared later episodes to SB3.

    The first reset is an attachment handshake only. It returns the last
    delivered observation already present in the exact branch state and does
    not reset position, regime, disturbance RNGs or Gymnasium RNG state.
    """

    metadata = {"render_modes": []}

    def __init__(
        self,
        branch: GridWorldScientificStateAdapter,
        *,
        subsequent_episode_seeds: Sequence[EnvironmentSeeds] = (),
    ) -> None:
        super().__init__()
        if not isinstance(branch, GridWorldScientificStateAdapter):
            raise ValueError("branch must be GridWorldScientificStateAdapter")
        transition = branch.environment.gym_env.last_transition
        if transition is None:
            raise ValueError("SB3 branch continuation requires a delivered pre-change prefix observation")
        if branch.environment.gym_env._finished:
            raise ValueError("SB3 branch continuation cannot attach to a finished episode")
        self.branch = branch
        self.action_space = branch.environment.gym_env.action_space
        self.observation_space = branch.environment.gym_env.observation_space
        self._attached = False
        self._subsequent_episode_seeds = tuple(subsequent_episode_seeds)
        if any(
            not isinstance(item, EnvironmentSeeds)
            for item in self._subsequent_episode_seeds
        ):
            raise ValueError("subsequent_episode_seeds must be EnvironmentSeeds")
        self._next_episode_seed = 0
        self._interactions = 0
        self._return_sum = 0.0
        self._terminated = False
        self._truncated = False
        self._episodes_started = 1
        self._episodes_completed = 0

    @property
    def interactions(self) -> int:
        return self._interactions

    @property
    def return_sum(self) -> float:
        return self._return_sum

    @property
    def terminated(self) -> bool:
        return self._terminated

    @property
    def truncated(self) -> bool:
        return self._truncated

    @property
    def episodes_started(self) -> int:
        return self._episodes_started

    @property
    def episodes_completed(self) -> int:
        return self._episodes_completed

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None):
        del seed, options
        if not self._attached:
            transition = self.branch.environment.gym_env.last_transition
            if transition is None:
                raise RuntimeError("branch lost its delivered prefix observation")
            self._attached = True
            return transition.delivered_observation, {}
        if not (self._terminated or self._truncated):
            raise RuntimeError("Phase-B environment reset requested before episode completion")
        if self._next_episode_seed >= len(self._subsequent_episode_seeds):
            raise RuntimeError("declared Phase-B episode seed sequence exhausted")
        observation = reset_gridworld_branch_episode(
            self.branch,
            seeds=self._subsequent_episode_seeds[self._next_episode_seed],
        )
        self._next_episode_seed += 1
        self._terminated = False
        self._truncated = False
        self._episodes_started += 1
        return observation, {}

    def step(self, action):
        if not self._attached:
            raise RuntimeError("branch continuation must be attached through reset before step")
        if self._terminated or self._truncated:
            raise RuntimeError("cannot step a completed Phase-B branch segment")
        transition = self.branch.environment.step(int(action))
        self._interactions += 1
        self._return_sum += float(transition.reward)
        self._terminated = bool(transition.terminated)
        self._truncated = bool(transition.truncated)
        if self._terminated or self._truncated:
            self._episodes_completed += 1
        return (
            transition.delivered_observation,
            float(transition.reward),
            self._terminated,
            self._truncated,
            {},
        )

    def close(self) -> None:
        # Ownership remains with the scientific branch adapter/executor.
        return None
