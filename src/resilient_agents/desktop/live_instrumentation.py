"""Runtime-only GridWorld presentation instrumentation for the desktop worker.

This module deliberately does not modify protocol-v2 driver sources. The T-528
DEVELOPMENT worker may temporarily wrap the public ``GridWorldEnvironment``
reset/step methods inside its own subprocess. Scientific methods are called
first; presentation copying happens afterwards and every presentation failure is
swallowed. The original methods are restored on context exit.
"""
from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

from ..gridworld import GridWorldEnvironment
from ..presentation_observer import PresentationEventSink, bound_presentation_sink, emit_gridworld_transition


@dataclass(frozen=True)
class LiveJobIdentity:
    phase: str
    method_id: str
    root_id: str
    layout_id: str

    def __post_init__(self) -> None:
        for field_name in ("phase", "method_id", "root_id", "layout_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")


def live_identity_from_job_payload(payload: dict) -> LiveJobIdentity | None:
    """Project one materialized Phase-A/B job into presentation metadata.

    Post-processing jobs intentionally return ``None`` because they do not own a
    live GridWorld environment.
    """

    job_type = payload.get("job_type")
    if job_type not in {"phase-a-training", "phase-b-matched-set"}:
        return None
    method = payload.get("method")
    root = payload.get("root")
    layout = payload.get("layout")
    if not isinstance(method, dict) or not isinstance(root, dict) or not isinstance(layout, dict):
        return None
    phase = "phase-a" if job_type == "phase-a-training" else "phase-b"
    try:
        return LiveJobIdentity(
            phase=phase,
            method_id=str(method["method_id"]),
            root_id=str(root["root_id"]),
            layout_id=str(layout["layout_id"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


@contextmanager
def instrument_gridworld_for_live_presentation(
    *,
    sink: PresentationEventSink,
    identity: LiveJobIdentity,
) -> Iterator[None]:
    """Temporarily observe GridWorld transitions in this worker process only.

    The wrappers call the original scientific methods first. Observer bookkeeping
    is protected by ``try/except`` and never changes the method return value. A
    Phase-B job may own several branch environments; presentation-only stream
    labels distinguish runtime environment instances without claiming FN/FD/AN/AD
    semantics that are not exposed at this boundary.
    """

    original_reset = GridWorldEnvironment.reset
    original_step = GridWorldEnvironment.step
    episode_index: defaultdict[int, int] = defaultdict(lambda: -1)
    interaction_index: defaultdict[int, int] = defaultdict(int)
    stream_serial: dict[int, int] = {}
    next_stream = 0

    def observed_reset(self: GridWorldEnvironment, *, seeds):
        observation = original_reset(self, seeds=seeds)
        try:
            key = id(self)
            episode_index[key] += 1
            interaction_index[key] = 0
        except Exception:
            pass
        return observation

    def observed_step(self: GridWorldEnvironment, intended_action: int):
        transition = original_step(self, intended_action)
        try:
            nonlocal next_stream
            key = id(self)
            if key not in stream_serial:
                stream_serial[key] = next_stream
                next_stream += 1
            interaction_index[key] += 1
            branch = None
            if identity.phase == "phase-b":
                branch = f"presentation-stream-{stream_serial[key] + 1}"
            emit_gridworld_transition(
                phase=identity.phase,
                method_id=identity.method_id,
                root_id=identity.root_id,
                scenario=self.gym_env.spec,
                episode_index=max(0, episode_index[key]),
                interaction_index=interaction_index[key],
                transition=transition,
                branch=branch,
            )
        except Exception:
            pass
        return transition

    GridWorldEnvironment.reset = observed_reset
    GridWorldEnvironment.step = observed_step
    try:
        with bound_presentation_sink(sink):
            yield
    finally:
        GridWorldEnvironment.reset = original_reset
        GridWorldEnvironment.step = original_step
