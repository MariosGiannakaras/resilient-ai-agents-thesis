"""Strict project-GridWorld representation boundary for direct SB3 inference."""
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


def predict_sb3_gridworld_action(
    adapter: Any,
    observation: Any,
    observation_space: gym.Space,
    *,
    deterministic: bool,
) -> Any:
    """Predict from the unchanged project coordinate through one strict ingress.

    The helper owns representation conversion only.  It does not normalize,
    scale, clip, add information, or consume RNG before delegating.  A
    stochastic adapter prediction may advance only the adapter's existing
    behavior RNG according to its normal scientific semantics.
    """

    if not isinstance(deterministic, bool):
        raise TypeError("deterministic must be boolean")
    predict = getattr(adapter, "predict", None)
    if not callable(predict):
        raise TypeError("SB3 GridWorld inference requires a prediction adapter")
    converted = as_sb3_gridworld_observation(observation, observation_space)
    return predict(converted, deterministic=deterministic)
