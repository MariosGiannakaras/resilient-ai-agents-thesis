"""DEC-055 persistent multi-episode protocol-v2 deployment lifecycle.

This module is intentionally separate from the immutable T-526 Phase-A and
single-segment compatibility surfaces. It extends only post-boundary execution.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import Any

from .contracts import ScenarioSpec
from .environment import EnvironmentSeeds
from .gridworld import GridWorldEnvironment
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_sb3_gridworld import BranchContinuationGridWorldEnv


def persistent_post_boundary_episode_spec(spec: ScenarioSpec) -> ScenarioSpec:
    """Return the same branch regime with a persistent change active at reset."""

    events = tuple(spec.change_events)
    if not events:
        return spec
    if len(events) != 1 or not events[0].persistent:
        raise ValueError("multi-episode Phase B requires one persistent change event")
    return replace(
        spec,
        scenario_id=f"{spec.scenario_id}--persistent-episode",
        change_events=(replace(events[0], onset_step=0),),
    )


def reset_gridworld_branch_episode(
    branch: GridWorldScientificStateAdapter,
    *,
    seeds: EnvironmentSeeds,
) -> Any:
    """Reset an episode without resetting learner, clock, or branch regime."""

    if not isinstance(branch, GridWorldScientificStateAdapter):
        raise TypeError("branch must be GridWorldScientificStateAdapter")
    if not isinstance(seeds, EnvironmentSeeds):
        raise TypeError("episode reset seeds must be explicit EnvironmentSeeds")
    current = branch.environment
    next_spec = persistent_post_boundary_episode_spec(current.gym_env.spec)
    if next_spec is not current.gym_env.spec:
        replacement = GridWorldEnvironment(next_spec)
        observation = replacement.reset(seeds=seeds)
        current.close()
        branch.environment = replacement
        return observation
    return current.reset(seeds=seeds)


class PersistentMultiEpisodeBranchGridWorldEnv(BranchContinuationGridWorldEnv):
    """SB3 continuation facade with a finite declared reset seed schedule."""

    def __init__(
        self,
        branch: GridWorldScientificStateAdapter,
        *,
        subsequent_episode_seeds: Sequence[EnvironmentSeeds],
    ) -> None:
        super().__init__(branch)
        self._subsequent_episode_seeds = tuple(subsequent_episode_seeds)
        if any(
            not isinstance(item, EnvironmentSeeds)
            for item in self._subsequent_episode_seeds
        ):
            raise TypeError("subsequent_episode_seeds must be EnvironmentSeeds")
        self._next_episode_seed = 0
        self._episodes_started = 1
        self._episodes_completed = 0

    @property
    def episodes_started(self) -> int:
        return self._episodes_started

    @property
    def episodes_completed(self) -> int:
        return self._episodes_completed

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None):
        if not self._attached:
            return super().reset(seed=seed, options=options)
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
        result = super().step(action)
        if self._terminated or self._truncated:
            self._episodes_completed += 1
        return result
