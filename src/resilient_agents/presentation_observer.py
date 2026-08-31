"""Optional process-local presentation observer for non-scientific live UI state.

This module is deliberately outside the evidence model. Scientific execution is
identical when no sink is bound, which is the default for every protocol runner,
test, pilot and final-reserve path. The T-528 DEVELOPMENT desktop worker may bind
a sink for transient visualization only.

Observer failures are swallowed by design: presentation must never become an
input, backpressure source, failure mode or evidence channel for scientific
execution.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Iterator, Mapping, Protocol, runtime_checkable

from .contracts import GroundTruthTransition, ScenarioSpec
from .gridworld import ResolvedGridWorldScenario


@runtime_checkable
class PresentationEventSink(Protocol):
    """Non-blocking best-effort sink for transient presentation events."""

    def emit(self, event: Mapping[str, Any]) -> None: ...


_CURRENT_SINK: ContextVar[PresentationEventSink | None] = ContextVar(
    "resilient_agents_presentation_sink",
    default=None,
)


@contextmanager
def bound_presentation_sink(
    sink: PresentationEventSink | None,
) -> Iterator[None]:
    """Temporarily bind a presentation sink in the current execution context."""

    if sink is not None and not isinstance(sink, PresentationEventSink):
        raise ValueError("sink must satisfy PresentationEventSink")
    token = _CURRENT_SINK.set(sink)
    try:
        yield
    finally:
        _CURRENT_SINK.reset(token)


def emit_presentation_event(event: Mapping[str, Any]) -> None:
    """Best-effort emission that can never alter scientific control flow."""

    sink = _CURRENT_SINK.get()
    if sink is None:
        return
    try:
        sink.emit(dict(event))
    except Exception:
        # Presentation is explicitly lossy and non-scientific. A renderer,
        # filesystem or consumer failure must not affect experiment execution.
        return


def emit_gridworld_transition(
    *,
    phase: str,
    method_id: str,
    root_id: str,
    scenario: ScenarioSpec,
    episode_index: int,
    interaction_index: int,
    transition: GroundTruthTransition,
    branch: str | None = None,
) -> None:
    """Emit an immutable JSON-shaped GridWorld presentation snapshot.

    This function only copies state already produced by the scientific
    environment. It never returns a value to the learner or executor. When no
    presentation sink is bound it returns before resolving/copying any geometry,
    preserving the normal protocol path as a near-zero-cost no-op.
    """

    if _CURRENT_SINK.get() is None:
        return
    try:
        resolved = ResolvedGridWorldScenario.from_spec(scenario)
        event = {
            "schema_version": 1,
            "event_type": "gridworld-transition",
            "stream_id": (
                f"{phase}:{method_id}:{root_id}:{scenario.scenario_id}:"
                f"{branch or 'nominal'}"
            ),
            "phase": str(phase),
            "method_id": str(method_id),
            "root_id": str(root_id),
            "layout_id": str(scenario.scenario_id),
            "branch": None if branch is None else str(branch),
            "episode_index": int(episode_index),
            "interaction_index": int(interaction_index),
            "environment_step": int(transition.step),
            "grid": {
                "width": int(resolved.width),
                "height": int(resolved.height),
                "start": list(resolved.start),
                "goal": list(resolved.goal),
                "obstacles": [list(item) for item in sorted(resolved.obstacles)],
            },
            "true_state": list(transition.true_state),
            "delivered_observation": list(transition.delivered_observation),
            "intended_action": transition.intended_action,
            "executed_action": transition.executed_action,
            "reward": float(transition.reward),
            "terminated": bool(transition.terminated),
            "truncated": bool(transition.truncated),
            "regime_id": transition.regime_id,
            "disturbance_flags": dict(transition.disturbance_flags),
            "change_event_ids": list(transition.change_event_ids),
        }
    except Exception:
        # Snapshot conversion itself is presentation-only and must remain unable
        # to perturb scientific execution.
        return
    emit_presentation_event(event)
