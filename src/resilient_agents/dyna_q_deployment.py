"""Episode-boundary semantics for continual plain Dyna-Q deployment."""
from __future__ import annotations

import random
from typing import Any, Mapping

from .dyna_deployment import _validated_seed
from .dyna_q import DynaQAgent, DynaQConfig


class DynaQDeploymentAgent(DynaQAgent):
    """Plain Dyna-Q preserving learned Q/model state across episodes."""

    def __init__(
        self,
        config: DynaQConfig,
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
        if self._exploration_rng is None or self._planning_rng is None:
            raise RuntimeError("start_branch must precede start_next_episode")
        if self._pending is not None:
            raise RuntimeError("cannot start a new episode with an unobserved action")
        init_seed = _validated_seed(initialization_seed, field="initialization_seed")
        explore_seed = _validated_seed(exploration_seed, field="exploration_seed")
        self._initialization_seed = init_seed
        self._exploration_seed = explore_seed
        self._planning_rng = random.Random(init_seed)
        self._exploration_rng = random.Random(explore_seed)
        self._last_step = None
        self._episode_count += 1

    def reset(self, *, initialization_seed: int, exploration_seed: int) -> None:
        self.start_branch(
            initialization_seed=initialization_seed,
            exploration_seed=exploration_seed,
        )
