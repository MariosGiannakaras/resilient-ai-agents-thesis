"""Predeclared paired statistical support for protocol-v1.1.

The final v1.1 analysis is paired by root seed within layout/condition.  The
layout-specific agent effect is calculated first, then the four held-out layout
effects are averaged equally within each root.  Confidence intervals resample
those root-level paired effects, preserving the blocking structure instead of
pretending every layout/episode is an independent replicate.

Positive contrast effects always favor the first-listed agent.  For lower-is-
better resilience metrics the raw difference is sign-reversed; for terminal
performance the ordinary first-minus-second difference is used.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from statistics import fmean
from typing import Sequence

from .metrics import ResilienceMetrics

V11_PRIMARY_METRIC_DIRECTIONS = {
    "cumulative_deficit": "lower-is-better",
    "immediate_degradation": "lower-is-better",
    "terminal_performance": "higher-is-better",
}
V11_TERMINAL_PERFORMANCE_SOURCE_FIELD = "post_change_mean"


@dataclass(frozen=True)
class PairedMetricObservation:
    """One agent metric for one root/layout within one already-selected condition."""

    root_seed: int
    layout_id: str
    agent_id: str
    value: float


@dataclass(frozen=True)
class PairedContrastResult:
    """One predeclared agent contrast with root-blocked percentile bootstrap CI."""

    metric: str
    first_agent: str
    second_agent: str
    estimate: float
    ci_lower: float
    ci_upper: float
    confidence_level: float
    n_roots: int
    n_layouts: int
    bootstrap_resamples: int
    analysis_seed: int
    root_effects: tuple[tuple[int, float], ...]
    layout_effects: tuple[tuple[str, float], ...]


def metric_value(metrics: ResilienceMetrics, metric: str) -> float:
    """Map protocol-v1.1 public metric names to the existing metric contract."""

    if not isinstance(metrics, ResilienceMetrics):
        raise ValueError("metrics must be ResilienceMetrics")
    if metric == "cumulative_deficit":
        return float(metrics.cumulative_deficit)
    if metric == "immediate_degradation":
        return float(metrics.immediate_degradation)
    if metric == "terminal_performance":
        # ``post_change_mean`` is the existing contract's terminal-window mean,
        # despite the historical field name not containing the word terminal.
        return float(metrics.post_change_mean)
    raise ValueError(f"unsupported protocol-v1.1 primary metric: {metric}")


def _finite_number(value: object, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _unique_roots(values: Sequence[int]) -> tuple[int, ...]:
    roots = tuple(values)
    if not roots:
        raise ValueError("root_seeds must be non-empty")
    if any(
        not isinstance(root, int)
        or isinstance(root, bool)
        or not 0 <= root < 2**64
        for root in roots
    ):
        raise ValueError("root_seeds must be uint64-compatible integers")
    if len(set(roots)) != len(roots):
        raise ValueError("root_seeds must be unique")
    return roots


def _unique_layouts(values: Sequence[str]) -> tuple[str, ...]:
    layouts = tuple(values)
    if not layouts or any(not isinstance(item, str) or not item.strip() for item in layouts):
        raise ValueError("layout_ids must be non-empty strings")
    if len(set(layouts)) != len(layouts):
        raise ValueError("layout_ids must be unique")
    return layouts


def _percentile(sorted_values: Sequence[float], quantile: float) -> float:
    """Linear-interpolated sample quantile (Type-7 style) over sorted values."""

    if not sorted_values:
        raise ValueError("percentile input must be non-empty")
    if not 0.0 <= quantile <= 1.0:
        raise ValueError("quantile must be in [0, 1]")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    position = (len(sorted_values) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    weight = position - lower
    return float(sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight)


def paired_bootstrap_contrast(
    observations: Sequence[PairedMetricObservation],
    *,
    metric: str,
    first_agent: str,
    second_agent: str,
    root_seeds: Sequence[int],
    layout_ids: Sequence[str],
    confidence_level: float = 0.95,
    bootstrap_resamples: int = 10_000,
    analysis_seed: int = 110_920_260_827,
) -> PairedContrastResult:
    """Compute the predeclared root-blocked paired effect and percentile CI.

    ``observations`` must contain exactly one value for each
    ``root × layout × {first_agent, second_agent}`` cell for a single condition.
    This deliberate fail-closed requirement prevents silently changing ``n`` or
    treating incomplete layout blocks as equivalent to complete paired roots.
    """

    if metric not in V11_PRIMARY_METRIC_DIRECTIONS:
        raise ValueError("metric is not a protocol-v1.1 primary metric")
    if not isinstance(first_agent, str) or not first_agent.strip():
        raise ValueError("first_agent must be non-empty")
    if not isinstance(second_agent, str) or not second_agent.strip():
        raise ValueError("second_agent must be non-empty")
    if first_agent == second_agent:
        raise ValueError("paired contrast requires two distinct agents")
    roots = _unique_roots(root_seeds)
    layouts = _unique_layouts(layout_ids)
    level = _finite_number(confidence_level, field="confidence_level")
    if not 0.0 < level < 1.0:
        raise ValueError("confidence_level must be strictly between 0 and 1")
    if (
        not isinstance(bootstrap_resamples, int)
        or isinstance(bootstrap_resamples, bool)
        or bootstrap_resamples <= 0
    ):
        raise ValueError("bootstrap_resamples must be a positive integer")
    if (
        not isinstance(analysis_seed, int)
        or isinstance(analysis_seed, bool)
        or not 0 <= analysis_seed < 2**64
    ):
        raise ValueError("analysis_seed must be a uint64-compatible integer")

    allowed_roots = set(roots)
    allowed_layouts = set(layouts)
    allowed_agents = {first_agent, second_agent}
    cells: dict[tuple[int, str, str], float] = {}
    for observation in observations:
        if not isinstance(observation, PairedMetricObservation):
            raise ValueError("every observation must be PairedMetricObservation")
        if observation.root_seed not in allowed_roots:
            raise ValueError("observation root_seed is outside the predeclared bank")
        if observation.layout_id not in allowed_layouts:
            raise ValueError("observation layout_id is outside the predeclared layout set")
        if observation.agent_id not in allowed_agents:
            raise ValueError("observation agent_id is outside this paired contrast")
        key = (observation.root_seed, observation.layout_id, observation.agent_id)
        if key in cells:
            raise ValueError("duplicate paired observation cell")
        cells[key] = _finite_number(observation.value, field="observation value")

    expected = {
        (root, layout, agent)
        for root in roots
        for layout in layouts
        for agent in (first_agent, second_agent)
    }
    missing = expected - set(cells)
    if missing:
        raise ValueError("paired contrast is incomplete; every root/layout/agent cell is required")
    if set(cells) != expected:
        raise ValueError("paired contrast contains unexpected cells")

    lower_is_better = V11_PRIMARY_METRIC_DIRECTIONS[metric] == "lower-is-better"

    def effect(first: float, second: float) -> float:
        raw = first - second
        return -raw if lower_is_better else raw

    root_effect_values: list[tuple[int, float]] = []
    for root in roots:
        within_layout = [
            effect(
                cells[(root, layout, first_agent)],
                cells[(root, layout, second_agent)],
            )
            for layout in layouts
        ]
        root_effect_values.append((root, fmean(within_layout)))

    layout_effect_values: list[tuple[str, float]] = []
    for layout in layouts:
        within_roots = [
            effect(
                cells[(root, layout, first_agent)],
                cells[(root, layout, second_agent)],
            )
            for root in roots
        ]
        layout_effect_values.append((layout, fmean(within_roots)))

    root_values = tuple(value for _, value in root_effect_values)
    estimate = fmean(root_values)
    rng = random.Random(analysis_seed)
    bootstrapped: list[float] = []
    for _ in range(bootstrap_resamples):
        bootstrapped.append(fmean(rng.choice(root_values) for _ in roots))
    bootstrapped.sort()
    tail = (1.0 - level) / 2.0
    lower = _percentile(bootstrapped, tail)
    upper = _percentile(bootstrapped, 1.0 - tail)

    return PairedContrastResult(
        metric=metric,
        first_agent=first_agent,
        second_agent=second_agent,
        estimate=estimate,
        ci_lower=lower,
        ci_upper=upper,
        confidence_level=level,
        n_roots=len(roots),
        n_layouts=len(layouts),
        bootstrap_resamples=bootstrap_resamples,
        analysis_seed=analysis_seed,
        root_effects=tuple(root_effect_values),
        layout_effects=tuple(layout_effect_values),
    )


__all__ = [
    "PairedContrastResult",
    "PairedMetricObservation",
    "V11_PRIMARY_METRIC_DIRECTIONS",
    "V11_TERMINAL_PERFORMANCE_SOURCE_FIELD",
    "metric_value",
    "paired_bootstrap_contrast",
]
