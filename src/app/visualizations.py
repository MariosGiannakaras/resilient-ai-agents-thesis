"""Visualization builders for the native NiceGUI thesis application.

Stable analysis charts are Plotly figures sourced from stored evidence. Live
operational charts are ECharts option dictionaries sourced from runtime DTOs.
No function in this module executes or mutates a scientific experiment.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import pandas as pd
import plotly.graph_objects as go


AGENT_LABELS = {
    "f0": "F0 · Frozen Q-learning",
    "c0": "C0 · Continual Q-learning",
    "d0": "D0 · Dyna-Q+",
}

AGENT_COLORS = {
    "f0": "#64748b",
    "c0": "#2563eb",
    "d0": "#7c3aed",
}

AGENT_DASHES = {
    "f0": "solid",
    "c0": "dash",
    "d0": "dot",
}

METRIC_LABELS = {
    "nominal_mean": "Nominal return",
    "post_change_mean": "Post-change return",
    "cumulative_deficit": "Cumulative deficit",
    "immediate_degradation": "Immediate degradation",
    "terminal_gap": "Terminal gap",
}

CONDITION_LABELS = {
    "nominal": "Nominal",
    "action-failure-1of8": "Action failure · p=0.125",
    "action-failure-1of4": "Action failure · p=0.25",
    "observation-corruption-1of8": "Observation corruption · p=0.125",
    "observation-corruption-1of4": "Observation corruption · p=0.25",
    "remap-min-in-set": "2-action remap · historical v1.0 ID",
    "remap-max-out-of-set": "4-action remap · historical v1.0 ID",
    "action-remap-2-swap": "2-action swap",
    "action-remap-4-cycle": "4-action cyclic remap",
}

PLOTLY_CONFIG: dict[str, Any] = {
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": ["lasso2d"],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "resilient-agents-figure",
        "width": 1600,
        "height": 900,
        "scale": 2,
    },
}


def _base_layout(title: str, subtitle: str | None = None) -> dict[str, Any]:
    title_text = title if not subtitle else f"{title}<br><sup>{subtitle}</sup>"
    return {
        "title": {"text": title_text, "x": 0.02, "xanchor": "left"},
        "template": "plotly_white",
        "font": {"family": "Inter, Segoe UI, Arial, sans-serif", "size": 13},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": {"l": 70, "r": 28, "t": 82, "b": 72},
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.01,
            "xanchor": "right",
            "x": 1.0,
        },
        "hoverlabel": {"namelength": -1},
    }


def aggregated_metric_figure(
    frame: pd.DataFrame,
    metric: str,
    *,
    protocol_label: str = "protocol-v1.0 historical finalized evidence",
) -> go.Figure:
    """Build a screenshot-ready agent×condition comparison from stored aggregates.

    Historical v1.0 artifacts contain mean/std rather than the paired 95% CIs
    required for protocol-v1.1. Error bars are therefore labelled as SD and are
    never presented as confidence intervals.
    """
    mean_column = (metric, "mean")
    std_column = (metric, "std")
    if mean_column not in frame.columns:
        raise KeyError(f"Metric {metric!r} is not available in aggregated evidence")

    figure = go.Figure()
    agents = list(dict.fromkeys(str(value) for value in frame.index.get_level_values(0)))
    conditions = list(dict.fromkeys(str(value) for value in frame.index.get_level_values(1)))

    for agent_id in agents:
        means: list[float | None] = []
        stds: list[float | None] = []
        for condition_id in conditions:
            key = (agent_id, condition_id)
            if key not in frame.index:
                means.append(None)
                stds.append(None)
                continue
            row = frame.loc[key]
            mean_value = row[mean_column]
            std_value = row[std_column] if std_column in frame.columns else None
            means.append(None if pd.isna(mean_value) else float(mean_value))
            stds.append(None if std_value is None or pd.isna(std_value) else float(std_value))

        figure.add_trace(
            go.Bar(
                name=AGENT_LABELS.get(agent_id, agent_id.upper()),
                x=[CONDITION_LABELS.get(item, item) for item in conditions],
                y=means,
                marker={"color": AGENT_COLORS.get(agent_id)},
                error_y={
                    "type": "data",
                    "array": stds,
                    "visible": any(value is not None for value in stds),
                },
                hovertemplate=(
                    "%{x}<br>%{fullData.name}<br>mean=%{y:.3f}"
                    "<br>error bar=SD<extra></extra>"
                ),
            )
        )

    metric_label = METRIC_LABELS.get(metric, metric.replace("_", " ").title())
    figure.update_layout(
        **_base_layout(
            f"{metric_label} by uncertainty condition",
            f"{protocol_label} · bars = mean · error bars = SD",
        ),
        barmode="group",
        xaxis={"title": "Condition", "tickangle": -24, "automargin": True},
        yaxis={"title": metric_label, "zeroline": True, "automargin": True},
    )
    return figure


def metric_heatmap_figure(
    frame: pd.DataFrame,
    metric: str,
    *,
    protocol_label: str = "protocol-v1.0 historical finalized evidence",
) -> go.Figure:
    """Build an overview heatmap using stored aggregate means only."""
    mean_column = (metric, "mean")
    if mean_column not in frame.columns:
        raise KeyError(f"Metric {metric!r} is not available in aggregated evidence")

    agents = list(dict.fromkeys(str(value) for value in frame.index.get_level_values(0)))
    conditions = list(dict.fromkeys(str(value) for value in frame.index.get_level_values(1)))
    z: list[list[float | None]] = []
    text: list[list[str]] = []
    for agent_id in agents:
        agent_values: list[float | None] = []
        agent_text: list[str] = []
        for condition_id in conditions:
            key = (agent_id, condition_id)
            if key not in frame.index:
                agent_values.append(None)
                agent_text.append("Unavailable")
                continue
            value = frame.loc[key][mean_column]
            numeric = None if pd.isna(value) else float(value)
            agent_values.append(numeric)
            agent_text.append("Unavailable" if numeric is None else f"{numeric:.2f}")
        z.append(agent_values)
        text.append(agent_text)

    figure = go.Figure(
        go.Heatmap(
            z=z,
            x=[CONDITION_LABELS.get(item, item) for item in conditions],
            y=[AGENT_LABELS.get(item, item.upper()) for item in agents],
            text=text,
            texttemplate="%{text}",
            hovertemplate="%{y}<br>%{x}<br>mean=%{z:.3f}<extra></extra>",
            colorscale="RdYlBu",
            reversescale=True,
            colorbar={"title": METRIC_LABELS.get(metric, metric)},
        )
    )
    figure.update_layout(
        **_base_layout(
            f"{METRIC_LABELS.get(metric, metric)} overview",
            f"{protocol_label} · cell values = stored aggregate means",
        ),
        xaxis={"tickangle": -24, "automargin": True},
        yaxis={"automargin": True},
    )
    return figure


def live_series_options(
    series: Mapping[str, Sequence[tuple[int | float, int | float]]],
    *,
    title: str,
    y_axis_label: str,
    x_axis_label: str = "Episode",
    event_markers: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Return ECharts options for real live/provisional telemetry.

    Empty input intentionally produces an empty chart rather than demo data.
    """
    chart_series: list[dict[str, Any]] = []
    for index, (series_id, points) in enumerate(series.items()):
        color = AGENT_COLORS.get(series_id.casefold())
        chart_series.append(
            {
                "id": series_id,
                "name": AGENT_LABELS.get(series_id.casefold(), series_id),
                "type": "line",
                "showSymbol": False,
                "smooth": 0.18,
                "sampling": "lttb",
                "animationDurationUpdate": 180,
                "data": [[x, y] for x, y in points],
                "lineStyle": {
                    "width": 2.5,
                    **({"color": color} if color else {}),
                    "type": ["solid", "dashed", "dotted"][index % 3],
                },
                "emphasis": {"focus": "series"},
            }
        )

    mark_lines = []
    for marker in event_markers:
        x = marker.get("x")
        label = marker.get("label")
        if isinstance(x, (int, float)):
            mark_lines.append(
                {
                    "xAxis": x,
                    "label": {"formatter": str(label or "event")},
                }
            )
    if chart_series and mark_lines:
        chart_series[0]["markLine"] = {
            "silent": True,
            "symbol": ["none", "none"],
            "data": mark_lines,
        }

    return {
        "animation": True,
        "title": {
            "text": title,
            "subtext": "LIVE / PROVISIONAL · backend-derived telemetry",
            "left": 12,
        },
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 46, "type": "scroll"},
        "grid": {"left": 64, "right": 28, "top": 90, "bottom": 62},
        "toolbox": {
            "feature": {
                "dataZoom": {"yAxisIndex": "none"},
                "restore": {},
                "saveAsImage": {"name": "live-run-chart", "pixelRatio": 2},
            }
        },
        "dataZoom": [
            {"type": "inside", "xAxisIndex": 0},
            {"type": "slider", "xAxisIndex": 0, "height": 18, "bottom": 18},
        ],
        "xAxis": {"type": "value", "name": x_axis_label, "nameLocation": "middle", "nameGap": 38},
        "yAxis": {"type": "value", "name": y_axis_label, "nameLocation": "middle", "nameGap": 48},
        "series": chart_series,
    }


def agent_infographic_mermaid(agent_id: str) -> str:
    """Return a static explanatory diagram for one documented agent regime."""
    normalized = agent_id.casefold()
    if normalized == "f0":
        return """
flowchart LR
    O[Agent-visible observation] --> P[Frozen Q-table policy]
    P --> A[Intended action]
    A --> E[GridWorld]
    E --> R[Reward + next observation]
    R -. no post-checkpoint Q update .-> P
""".strip()
    if normalized == "c0":
        return """
flowchart LR
    O[Agent-visible observation] --> P[Q-learning policy]
    P --> A[Intended action]
    A --> E[GridWorld]
    E --> X[Reward + next observation]
    X --> U[Online TD update]
    U --> P
""".strip()
    if normalized == "d0":
        return """
flowchart LR
    O[Agent-visible observation] --> P[Dyna-Q+ policy]
    P --> A[Intended action]
    A --> E[GridWorld]
    E --> X[Reward + next observation]
    X --> Q[Direct Q update]
    X --> M[Empirical transition/reward model]
    M --> PL[Planning updates + recency bonus]
    Q --> P
    PL --> P
""".strip()
    raise KeyError(f"Unknown agent profile: {agent_id}")
