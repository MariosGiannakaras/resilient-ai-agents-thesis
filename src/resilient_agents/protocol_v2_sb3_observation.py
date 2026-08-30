"""Strict representation-only observations for direct SB3 continuation paths."""
from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces


def as_sb3_gridworld_observation(
    observation: Any,
    observation_space: gym.Space,
) -> np.ndarray:
    """Return the same project coordinate as a declared-dtype SB3 ndarray."""

    if not isinstance(observation_space, spaces.MultiDiscrete):
        raise TypeError("SB3 GridWorld observation space must be MultiDiscrete")
    if not isinstance(observation, (tuple, list, np.ndarray)):
        raise TypeError("GridWorld observation must be a coordinate sequence")
    raw = np.asarray(observation)
    if raw.shape != observation_space.shape:
        raise ValueError(
            f"GridWorld observation shape {raw.shape!r} does not match {observation_space.shape!r}"
        )
    if raw.dtype.kind not in {"i", "u"}:
        raise ValueError("GridWorld observation coordinates must be exact integers")
    converted = np.asarray(observation, dtype=observation_space.dtype)
    if converted.shape != observation_space.shape:
        raise ValueError("SB3 GridWorld observation conversion changed shape")
    if not np.array_equal(raw, converted):
        raise ValueError("SB3 GridWorld observation conversion changed coordinate values")
    if not observation_space.contains(converted):
        raise ValueError("GridWorld observation is outside the declared observation space")
    return converted
