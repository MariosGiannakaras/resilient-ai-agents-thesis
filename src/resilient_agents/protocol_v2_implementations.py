"""Resolved implementation registry for protocol-v2 pilot candidates.

``protocol_v2.MethodRegistry.core_candidates()`` was introduced before the
concrete neural adapters existed and intentionally recorded them as pending.
This module is the post-integration runtime registry: every core pilot candidate
maps to an implemented exact-state backend while keeping optional SB3 imports
out of the historical/default runtime.
"""
from __future__ import annotations

from .protocol_v2 import (
    CORE_METHOD_CAPABILITIES,
    MethodRegistration,
    MethodRegistry,
)
from .protocol_v2_sb3 import SUPPORTED_SB3_VERSION


PROJECT_STATE_ADAPTER_VERSION = "protocol-v2-state-v1"


def resolved_core_method_registry() -> MethodRegistry:
    """Return the concrete five-method implementation registry for T-525/T-526."""

    registry = MethodRegistry()
    for capabilities in CORE_METHOD_CAPABILITIES:
        if capabilities.method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
            implementation_id = "project-protocol-v2-state-adapter"
            implementation_version = PROJECT_STATE_ADAPTER_VERSION
        elif capabilities.method_id in {"dqn", "ppo"}:
            implementation_id = "stable-baselines3-scientific-state-adapter"
            implementation_version = SUPPORTED_SB3_VERSION
        else:  # fail closed if the core pool changes without implementation review
            raise RuntimeError(
                f"no resolved protocol-v2 implementation for {capabilities.method_id}"
            )
        registry.register(
            MethodRegistration(
                capabilities=capabilities,
                implementation_id=implementation_id,
                implementation_version=implementation_version,
            )
        )
    return registry


def resolved_implementation_provenance(method_id: str) -> dict[str, str]:
    registration = resolved_core_method_registry().get(method_id)
    if registration.implementation_version is None:
        raise RuntimeError("resolved implementation must have an explicit version")
    return {
        "method_id": method_id,
        "implementation_id": registration.implementation_id,
        "implementation_version": registration.implementation_version,
    }
