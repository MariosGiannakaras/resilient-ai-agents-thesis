"""Passive temporal evidence primitives for protocol-v2 Phase B.

The recorder observes rewards after actual environment interactions. It never
controls learner stepping, episode resets, rollout boundaries, or update timing.
That separation is required so recovery evidence cannot change the experiment
it is intended to measure.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping


@dataclass(frozen=True)
class RewardWindow:
    """One completed fixed-width post-boundary reward window."""

    start_interaction: int
    end_interaction: int
    interaction_count: int
    mean_reward: float

    def __post_init__(self) -> None:
        if (
            not isinstance(self.start_interaction, int)
            or isinstance(self.start_interaction, bool)
            or self.start_interaction <= 0
        ):
            raise ValueError("start_interaction must be a positive integer")
        if (
            not isinstance(self.end_interaction, int)
            or isinstance(self.end_interaction, bool)
            or self.end_interaction < self.start_interaction
        ):
            raise ValueError("end_interaction must be an integer >= start_interaction")
        expected_count = self.end_interaction - self.start_interaction + 1
        if self.interaction_count != expected_count:
            raise ValueError("interaction_count must match the inclusive window bounds")
        if not math.isfinite(float(self.mean_reward)):
            raise ValueError("mean_reward must be finite")

    def to_dict(self) -> dict[str, int | float]:
        return {
            "start_interaction": self.start_interaction,
            "end_interaction": self.end_interaction,
            "interaction_count": self.interaction_count,
            "mean_reward": float(self.mean_reward),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RewardWindow":
        if set(payload) != {
            "start_interaction",
            "end_interaction",
            "interaction_count",
            "mean_reward",
        }:
            raise ValueError("reward window keys do not match the declared schema")
        return cls(
            start_interaction=int(payload["start_interaction"]),
            end_interaction=int(payload["end_interaction"]),
            interaction_count=int(payload["interaction_count"]),
            mean_reward=float(payload["mean_reward"]),
        )


class FixedRewardWindowRecorder:
    """Accumulate bounded fixed windows without influencing execution control."""

    def __init__(self, *, window_size: int = 32) -> None:
        if (
            not isinstance(window_size, int)
            or isinstance(window_size, bool)
            or window_size <= 0
        ):
            raise ValueError("window_size must be a positive integer")
        self._window_size = window_size
        self._interactions = 0
        self._window_sum = 0.0
        self._windows: list[RewardWindow] = []

    @property
    def window_size(self) -> int:
        return self._window_size

    @property
    def interactions(self) -> int:
        return self._interactions

    @property
    def completed_windows(self) -> tuple[RewardWindow, ...]:
        return tuple(self._windows)

    @property
    def partial_window_interactions(self) -> int:
        return self._interactions % self._window_size

    def record(self, reward: float) -> None:
        value = float(reward)
        if not math.isfinite(value):
            raise ValueError("reward must be finite")
        self._interactions += 1
        self._window_sum += value
        if self._interactions % self._window_size:
            return
        end = self._interactions
        start = end - self._window_size + 1
        self._windows.append(
            RewardWindow(
                start_interaction=start,
                end_interaction=end,
                interaction_count=self._window_size,
                mean_reward=self._window_sum / self._window_size,
            )
        )
        self._window_sum = 0.0

    def require_complete(self, *, total_interactions: int) -> None:
        if (
            not isinstance(total_interactions, int)
            or isinstance(total_interactions, bool)
            or total_interactions <= 0
        ):
            raise ValueError("total_interactions must be a positive integer")
        if self._interactions != total_interactions:
            raise RuntimeError("temporal recorder interaction count does not reconcile")
        if total_interactions % self._window_size:
            raise RuntimeError("interaction horizon does not end on a complete reward window")
        if self.partial_window_interactions:
            raise RuntimeError("temporal recorder contains a partial final window")
        expected_endpoints = tuple(range(self._window_size, total_interactions + 1, self._window_size))
        actual_endpoints = tuple(item.end_interaction for item in self._windows)
        if actual_endpoints != expected_endpoints:
            raise RuntimeError("temporal recorder has missing or duplicate reward windows")
