"""Deterministically separated random-number streams."""
from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass

STREAM_NAMES = (
    "scenario",
    "environment",
    "action_disturbance",
    "observation_disturbance",
    "agent_exploration",
    "agent_initialization",
)


def derive_seed(master_seed: int, stream_name: str) -> int:
    if stream_name not in STREAM_NAMES:
        raise ValueError(f"unknown RNG stream: {stream_name}")
    payload = f"resilient-agents-v1\0{master_seed}\0{stream_name}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big", signed=False)


@dataclass
class RandomStreams:
    master_seed: int

    def __post_init__(self) -> None:
        self._streams = {
            name: random.Random(derive_seed(self.master_seed, name)) for name in STREAM_NAMES
        }

    def get(self, name: str) -> random.Random:
        try:
            return self._streams[name]
        except KeyError as exc:
            raise ValueError(f"unknown RNG stream: {name}") from exc

    def derived_seeds(self) -> dict[str, int]:
        return {name: derive_seed(self.master_seed, name) for name in STREAM_NAMES}
