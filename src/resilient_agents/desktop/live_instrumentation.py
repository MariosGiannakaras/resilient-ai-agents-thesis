"""Runtime-only GridWorld presentation instrumentation for the desktop worker.

This module deliberately does not modify protocol-v2 driver sources. The T-528
DEVELOPMENT worker may temporarily wrap public runtime objects inside its own
subprocess. Scientific methods are called first; presentation copying happens
afterwards and every presentation failure is swallowed. Original runtime objects
are restored on context exit.
"""
from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

from ..gridworld import GridWorldEnvironment
from ..presentation_observer import (
    PresentationEventSink,
    bound_presentation_sink,
    emit_gridworld_transition,
)


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

    The GridWorld wrapper calls the original scientific method first and never
    changes its return value. For Phase B, the existing Study executor's branch
    driver factories are wrapped *at runtime only* so the presentation layer can
    attach the authoritative ``ProtocolV2Branch`` label (FN/FD/AN/AD) to each
    forked environment. Neither the executor source nor the branch-driver source
    is modified. The shared pre-change prefix is labelled ``PREFIX``.
    """

    original_reset = GridWorldEnvironment.reset
    original_step = GridWorldEnvironment.step
    episode_index: defaultdict[int, int] = defaultdict(lambda: -1)
    interaction_index: defaultdict[int, int] = defaultdict(int)
    branch_by_environment: dict[int, str] = {}

    phase_b_module = None
    original_project_branch_driver = None
    original_sb3_branch_driver = None

    if identity.phase == "phase-b":
        # Importing the already-supported Study executor here keeps the branch
        # identity seam application-local. The worker is the only caller that
        # enables this presentation instrumentation.
        from ..study import protocol_v2_phase_b_executor as phase_b_module

        original_project_branch_driver = phase_b_module.ProjectTabularPhaseBBranchDriver
        original_sb3_branch_driver = phase_b_module.SB3PhaseBBranchDriver

        def observed_project_branch_driver(
            *, branch, adaptive, learner, environment, subsequent_episode_seeds=()
        ):
            try:
                branch_by_environment[id(environment.environment)] = str(branch.value)
            except Exception:
                pass
            return original_project_branch_driver(
                branch=branch,
                adaptive=adaptive,
                learner=learner,
                environment=environment,
                subsequent_episode_seeds=subsequent_episode_seeds,
            )

        def observed_sb3_branch_driver(
            *,
            branch,
            adaptive,
            learner,
            environment,
            deterministic_inference,
            subsequent_episode_seeds=(),
        ):
            try:
                branch_by_environment[id(environment.environment)] = str(branch.value)
            except Exception:
                pass
            return original_sb3_branch_driver(
                branch=branch,
                adaptive=adaptive,
                learner=learner,
                environment=environment,
                deterministic_inference=deterministic_inference,
                subsequent_episode_seeds=subsequent_episode_seeds,
            )

        phase_b_module.ProjectTabularPhaseBBranchDriver = observed_project_branch_driver
        phase_b_module.SB3PhaseBBranchDriver = observed_sb3_branch_driver

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
            key = id(self)
            interaction_index[key] += 1
            branch = None
            if identity.phase == "phase-b":
                branch = branch_by_environment.get(key, "PREFIX")
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
        if phase_b_module is not None:
            phase_b_module.ProjectTabularPhaseBBranchDriver = original_project_branch_driver
            phase_b_module.SB3PhaseBBranchDriver = original_sb3_branch_driver
