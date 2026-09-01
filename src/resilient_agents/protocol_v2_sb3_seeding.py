"""Explicit post-initialization RNG separation for protocol-v2 SB3 methods.

SB3's constructor seed is used to make neural parameter initialization
reproducible. Protocol-v2 then reseeds the learner's stochastic behavior/update
stream from the separate root ``exploration_seed`` without changing learned
parameters or the project environment RNG streams.

The adapter already virtualizes Python/NumPy/Torch/action-space RNG state during
training and prediction. This helper only replaces that virtualized initial RNG
state after model construction.
"""
from __future__ import annotations

import random
from typing import Any

from .protocol_v2_sb3 import (
    SB3ScientificStateAdapter,
    _action_space_rng_to_json,
    _capture_global_rng,
    _imports,
    _json_copy,
    _restore_global_rng,
)


def reseed_sb3_behavior_rng(
    adapter: SB3ScientificStateAdapter,
    *,
    exploration_seed: int,
) -> None:
    """Replace post-construction stochastic RNG state without reinitializing the model."""

    if not isinstance(adapter, SB3ScientificStateAdapter):
        raise ValueError("adapter must be SB3ScientificStateAdapter")
    if (
        not isinstance(exploration_seed, int)
        or isinstance(exploration_seed, bool)
        or not 0 <= exploration_seed < 2**64
    ):
        raise ValueError("exploration_seed must be an integer in [0, 2**64)")

    np, torch, _, _ = _imports()
    process_rng = _capture_global_rng()
    try:
        random.seed(exploration_seed)
        # NumPy legacy RandomState accepts a 32-bit seed; derive it
        # deterministically without changing the root seed contract.
        np.random.seed(exploration_seed % 2**32)
        torch.manual_seed(exploration_seed)
        adapter.model.action_space.seed(exploration_seed % 2**32)
        adapter._rng_state = _json_copy(
            _capture_global_rng(),
            field="SB3 protocol-v2 behavior RNG state",
        )
        adapter._action_space_rng_state = _action_space_rng_to_json(adapter.model)
    finally:
        # Do not leak one root's stochastic stream into unrelated process work.
        _restore_global_rng(process_rng)

    # The adapter must remain a legal exact scientific checkpoint after reseed.
    adapter._validate_boundary()
