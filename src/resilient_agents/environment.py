"""Environment contract with explicit RNG channels and evaluator-only truth."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .contracts import GroundTruthTransition


@dataclass(frozen=True)
class EnvironmentSeeds:
    scenario: int
    environment: int
    action_disturbance: int
    observation_disturbance: int


class ResearchEnvironment(Protocol):
    environment_id: str

    def reset(self, *, seeds: EnvironmentSeeds) -> Any: ...

    def step(self, intended_action: Any) -> GroundTruthTransition: ...
