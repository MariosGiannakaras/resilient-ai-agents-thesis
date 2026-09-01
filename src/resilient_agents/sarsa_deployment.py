"""Episode-boundary semantics for continual SARSA deployment."""
from __future__ import annotations

import random
from typing import Any, Mapping

from .sarsa import SarsaAgent, SarsaConfig, _validate_seed


class SarsaDeploymentAgent(SarsaAgent):
    """SARSA strategy that preserves learned Q values across evaluation episodes."""

    def __init__(
        self,
        config: SarsaConfig,
        *,
        checkpoint: Mapping[str, Any] | None,
    ) -> None:
        super().__init__(config, checkpoint=checkpoint)
        self._episode_count = 0

    @property
    def deployment_episode_count(self) -> int:
        return self._episode_count

    def start_branch(self, *, initialization_seed: int, exploration_seed: int) -> None:
        super().reset(
            initialization_seed=initialization_seed,
            exploration_seed=exploration_seed,
        )
        self._episode_count = 1

    def start_next_episode(self, *, initialization_seed: int, exploration_seed: int) -> None:
        if self._exploration_rng is None:
            raise RuntimeError("start_branch must precede start_next_episode")
        if self._pending_action is not None or self._deferred_update is not None:
            raise RuntimeError("cannot start a new episode with unresolved SARSA state")
        init_seed = _validate_seed(initialization_seed, field="initialization_seed")
        explore_seed = _validate_seed(exploration_seed, field="exploration_seed")
        self._initialization_seed = init_seed
        self._exploration_seed = explore_seed
        self._exploration_rng = random.Random(explore_seed)
        self._last_step = None
        self._episode_count += 1

    def reset(self, *, initialization_seed: int, exploration_seed: int) -> None:
        self.start_branch(
            initialization_seed=initialization_seed,
            exploration_seed=exploration_seed,
        )
