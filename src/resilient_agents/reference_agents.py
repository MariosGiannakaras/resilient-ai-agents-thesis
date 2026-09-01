"""Clearly non-ranked reference agents for scale/correctness checks.

Reference agents are not part of the fair resilience-agent ranking.  They are
kept separate so a simple scale fixture cannot be mistaken for a scientific
competitor in protocol-v1.1 results.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .contracts import AgentTransition


@dataclass(frozen=True)
class RandomReferenceConfig:
    agent_id: str
    actions: Sequence[Any]

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str) or not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        actions = tuple(self.actions)
        if not actions:
            raise ValueError("actions must be non-empty")
        if len({repr(action) for action in actions}) != len(actions):
            raise ValueError("actions must be unique")
        object.__setattr__(self, "actions", actions)


class RandomReferenceAgent:
    """Seeded uniform-random action reference; never a ranked resilience agent."""

    def __init__(self, config: RandomReferenceConfig) -> None:
        if not isinstance(config, RandomReferenceConfig):
            raise ValueError("config must be RandomReferenceConfig")
        self.config = config
        self.agent_id = config.agent_id
        self._rng: random.Random | None = None
        self._initialization_seed: int | None = None
        self._exploration_seed: int | None = None
        self._pending_action: Any | None = None
        self._observed_transition_count = 0

    @staticmethod
    def _validate_seed(value: Any, *, field: str) -> int:
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not 0 <= value < 2**64
        ):
            raise ValueError(f"{field} must be an integer in [0, 2**64)")
        return value

    def reset(self, *, initialization_seed: int, exploration_seed: int) -> None:
        self._initialization_seed = self._validate_seed(
            initialization_seed, field="initialization_seed"
        )
        self._exploration_seed = self._validate_seed(
            exploration_seed, field="exploration_seed"
        )
        self._rng = random.Random(self._exploration_seed)
        self._pending_action = None
        self._observed_transition_count = 0

    def act(self, observation: Any) -> Any:
        del observation
        if self._rng is None:
            raise RuntimeError("agent must be reset before use")
        if self._pending_action is not None:
            raise RuntimeError("observe must consume the previous action before act")
        action = self._rng.choice(tuple(self.config.actions))
        self._pending_action = action
        return action

    def observe(self, transition: AgentTransition) -> None:
        if self._rng is None:
            raise RuntimeError("agent must be reset before use")
        if not isinstance(transition, AgentTransition):
            raise ValueError("transition must be AgentTransition")
        if transition.optional_information:
            raise ValueError("Random reference forbids optional evaluator information")
        if self._pending_action is None:
            raise RuntimeError("act must precede observe")
        if transition.intended_action != self._pending_action:
            raise ValueError("transition intended_action does not match pending action")
        self._pending_action = None
        self._observed_transition_count += 1

    def end_episode(self, summary: Mapping[str, Any]) -> None:
        if not isinstance(summary, Mapping):
            raise ValueError("episode summary must be an object")
        if self._pending_action is not None:
            raise RuntimeError("cannot end an episode with an unobserved action")

    def get_state(self) -> Mapping[str, Any]:
        return {
            "agent_id": self.agent_id,
            "method": "uniform_random_reference_v1",
            "classification": "reference-only-not-ranked",
            "initialized": self._rng is not None,
            "initialization_seed": self._initialization_seed,
            "exploration_seed": self._exploration_seed,
            "observed_transition_count": self._observed_transition_count,
        }
