"""Episode-boundary semantics for continual D0 Dyna-Q+ deployment.

The common Agent.reset contract means "start from the configured base state".
That is correct for a new matched branch/root but not for every episode of a
continual deployment: D0 must retain its learned Q values, empirical model and
recency clock across episodes while using the runner's fresh, episode-scoped
agent RNG seeds just like C0 gets a freshly seeded exploration RNG each
episode.

This small specialization makes that distinction explicit without weakening
the generic Agent contract or changing the standalone Dyna-Q+ implementation.
"""
from __future__ import annotations

import random
from typing import Any

from .dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig


def _validated_seed(value: Any, *, field: str) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or not 0 <= value < 2**64
    ):
        raise ValueError(f"{field} must be an integer in [0, 2**64)")
    return value


class DynaQPlusDeploymentAgent(DynaQPlusAgent):
    """D0 with explicit fresh-branch versus next-episode boundaries."""

    def __init__(
        self,
        config: DynaQPlusConfig,
        *,
        checkpoint: dict[str, Any] | None,
    ) -> None:
        super().__init__(config, checkpoint=checkpoint)
        self._episode_count = 0

    def start_branch(
        self, *, initialization_seed: int, exploration_seed: int
    ) -> None:
        """Start a new matched branch from the common nominal checkpoint.

        All Dyna learning/model/recency state is intentionally cleared here.
        Reference and disrupted branches each call this exactly once so their
        pre-change state starts identically and then evolves independently.
        """
        super().reset(
            initialization_seed=initialization_seed,
            exploration_seed=exploration_seed,
        )
        self._episode_count = 1

    def start_next_episode(
        self, *, initialization_seed: int, exploration_seed: int
    ) -> None:
        """Reseed episode-local RNG/step state while preserving learning.

        Q values, the empirical transition/reward model, experienced-pair set,
        recency clock and planning counters are deliberately preserved.  The
        pending action and per-environment step monotonicity guard are reset
        because GridWorld step indices restart from zero each episode.
        """
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
        """Honor Agent.reset as a fresh branch/root reset."""
        self.start_branch(
            initialization_seed=initialization_seed,
            exploration_seed=exploration_seed,
        )

    def get_state(self) -> dict[str, Any]:
        state = dict(super().get_state())
        state["deployment_episode_count"] = self._episode_count
        return state
