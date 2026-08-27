"""Pure view-model helpers for truthful runtime telemetry.

These functions transform T-530 operational events into presentation state.
They never infer missing historical steps and never feed values back into a run.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .state import AGENT_PROFILE_BY_ID


@dataclass(frozen=True)
class GridWorldLiveView:
    width: int
    height: int
    start: tuple[int, int]
    goal: tuple[int, int]
    obstacles: tuple[tuple[int, int], ...]
    position: tuple[int, int]
    delivered_observation: tuple[int, int] | None
    agent_id: str
    strategy_name: str
    branch: str
    phase: str
    episode_index: int
    step: int
    intended_action: str | None
    executed_action: str | None
    cumulative_episode_return: float | None
    disturbance_flags: Mapping[str, bool]
    change_event_ids: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeTelemetryView:
    gridworld: GridWorldLiveView | None
    return_series: Mapping[str, tuple[tuple[int, float], ...]]
    recent_events: tuple[Mapping[str, Any], ...]
    latest_sequence: int | None


def _xy(value: Any) -> tuple[int, int] | None:
    if (
        isinstance(value, (list, tuple))
        and len(value) == 2
        and all(isinstance(item, int) and not isinstance(item, bool) for item in value)
    ):
        return int(value[0]), int(value[1])
    return None


def _episode_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        row.get("root_seed"),
        row.get("agent_id"),
        row.get("branch"),
        row.get("phase"),
        row.get("episode_index"),
        row.get("scenario_id"),
    )


def build_runtime_telemetry_view(
    rows: Sequence[Mapping[str, Any]], *, recent_event_limit: int = 12
) -> RuntimeTelemetryView:
    """Build one current live view from ordered runtime telemetry rows."""
    if not isinstance(recent_event_limit, int) or isinstance(recent_event_limit, bool) or recent_event_limit <= 0:
        raise ValueError("recent_event_limit must be a positive integer")

    starts: dict[tuple[Any, ...], Mapping[str, Any]] = {}
    latest_step: Mapping[str, Any] | None = None
    completed_returns: dict[str, list[tuple[int, float]]] = {}
    compact_events: list[Mapping[str, Any]] = []
    latest_sequence: int | None = None

    for raw in rows:
        if not isinstance(raw, Mapping):
            raise ValueError("runtime telemetry rows must be objects")
        sequence = raw.get("sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool):
            raise ValueError("runtime telemetry sequence is required")
        if latest_sequence is not None and sequence <= latest_sequence:
            raise ValueError("runtime telemetry must be strictly sequence-ordered")
        latest_sequence = sequence
        event = raw.get("event")
        if event == "episode_started":
            starts[_episode_key(raw)] = raw
        elif event == "gridworld_step":
            latest_step = raw
        elif event == "episode_completed":
            agent_id = str(raw.get("agent_id") or "unknown")
            branch = str(raw.get("branch") or "unknown")
            phase = str(raw.get("phase") or "unknown")
            episode_index = raw.get("episode_index")
            value = raw.get("return")
            if (
                isinstance(episode_index, int)
                and not isinstance(episode_index, bool)
                and isinstance(value, (int, float))
                and not isinstance(value, bool)
            ):
                series_id = f"{agent_id}:{branch}:{phase}"
                completed_returns.setdefault(series_id, []).append(
                    (int(episode_index), float(value))
                )
        if event in {"episode_started", "episode_completed", "gridworld_step"}:
            compact_events.append(raw)

    gridworld: GridWorldLiveView | None = None
    if latest_step is not None:
        start_row = starts.get(_episode_key(latest_step))
        if start_row is not None:
            grid = start_row.get("grid")
            if isinstance(grid, Mapping):
                start = _xy(grid.get("start"))
                goal = _xy(grid.get("goal"))
                position = _xy(latest_step.get("true_state"))
                delivered = _xy(latest_step.get("delivered_observation"))
                width = grid.get("width")
                height = grid.get("height")
                raw_obstacles = grid.get("obstacles")
                obstacles = (
                    tuple(item for raw in raw_obstacles if (item := _xy(raw)) is not None)
                    if isinstance(raw_obstacles, (list, tuple))
                    else ()
                )
                if (
                    start is not None
                    and goal is not None
                    and position is not None
                    and isinstance(width, int)
                    and not isinstance(width, bool)
                    and isinstance(height, int)
                    and not isinstance(height, bool)
                    and width > 0
                    and height > 0
                ):
                    agent_id = str(latest_step.get("agent_id") or "unknown")
                    profile = AGENT_PROFILE_BY_ID.get(agent_id)
                    flags = latest_step.get("disturbance_flags")
                    changes = latest_step.get("change_event_ids")
                    cumulative = latest_step.get("cumulative_episode_return")
                    gridworld = GridWorldLiveView(
                        width=width,
                        height=height,
                        start=start,
                        goal=goal,
                        obstacles=obstacles,
                        position=position,
                        delivered_observation=delivered,
                        agent_id=agent_id,
                        strategy_name=profile.name if profile else agent_id,
                        branch=str(latest_step.get("branch") or "unknown"),
                        phase=str(latest_step.get("phase") or "unknown"),
                        episode_index=int(latest_step.get("episode_index") or 0),
                        step=int(latest_step.get("step") or 0),
                        intended_action=(
                            str(latest_step["intended_action"])
                            if latest_step.get("intended_action") is not None
                            else None
                        ),
                        executed_action=(
                            str(latest_step["executed_action"])
                            if latest_step.get("executed_action") is not None
                            else None
                        ),
                        cumulative_episode_return=(
                            float(cumulative)
                            if isinstance(cumulative, (int, float)) and not isinstance(cumulative, bool)
                            else None
                        ),
                        disturbance_flags=(
                            {str(key): bool(value) for key, value in flags.items()}
                            if isinstance(flags, Mapping)
                            else {}
                        ),
                        change_event_ids=(
                            tuple(str(value) for value in changes)
                            if isinstance(changes, (list, tuple))
                            else ()
                        ),
                    )

    return RuntimeTelemetryView(
        gridworld=gridworld,
        return_series={key: tuple(values) for key, values in completed_returns.items()},
        recent_events=tuple(compact_events[-recent_event_limit:]),
        latest_sequence=latest_sequence,
    )


def gridworld_html(view: GridWorldLiveView | None) -> str:
    """Render a compact semantic GridWorld; absent state stays explicitly empty."""
    if view is None:
        return (
            '<div class="grid-empty">'
            '<div class="grid-empty-icon">▦</div>'
            '<strong>No live GridWorld step yet</strong>'
            '<span>The panel activates only after a real runtime telemetry step.</span>'
            '</div>'
        )
    obstacles = set(view.obstacles)
    cells: list[str] = []
    for y in range(view.height):
        for x in range(view.width):
            point = (x, y)
            classes = ["gw-cell"]
            label = ""
            title = f"Cell ({x}, {y})"
            if point in obstacles:
                classes.append("gw-obstacle")
                label = "■"
                title += " · obstacle"
            if point == view.start:
                classes.append("gw-start")
                label = "S"
                title += " · start"
            if point == view.goal:
                classes.append("gw-goal")
                label = "G"
                title += " · goal"
            if point == view.position:
                classes.append("gw-agent")
                label = "●"
                title += f" · {view.strategy_name} current true position"
            if view.delivered_observation is not None and point == view.delivered_observation and point != view.position:
                classes.append("gw-observation")
                label = "◇"
                title += " · delivered observation differs from true position"
            cells.append(
                f'<div class="{" ".join(classes)}" title="{title}">{label}</div>'
            )
    return (
        f'<div class="gw-board" style="grid-template-columns:repeat({view.width},1fr)">'
        + "".join(cells)
        + "</div>"
    )


__all__ = [
    "GridWorldLiveView",
    "RuntimeTelemetryView",
    "build_runtime_telemetry_view",
    "gridworld_html",
]
