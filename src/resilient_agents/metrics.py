"""Operational resilience estimands with explicit protocol parameters."""
from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from statistics import fmean
from typing import Sequence


class RecoveryStatus(str, Enum):
    """Mutually exclusive recovery outcomes for one valid independent run."""

    NO_DEGRADATION = "no_degradation"
    RECOVERED = "recovered"
    NOT_RECOVERED = "not_recovered"


@dataclass(frozen=True)
class ResilienceMetrics:
    """Per-run, per-condition estimands on a higher-is-better performance series."""

    nominal_mean: float
    nominal_reference_mean: float
    nominal_gap: float
    immediate_degradation: float
    worst_degradation: float
    post_change_mean: float
    post_change_reference_mean: float
    post_change_gap: float
    cumulative_deficit: float
    first_degradation_index: int | None
    recovery_index: int | None
    recovery_delay: int | None
    recovery_status: RecoveryStatus


@dataclass(frozen=True)
class RecoverySummary:
    """Counts/rate across predefined valid independent runs in one condition."""

    total_runs: int
    no_degradation_runs: int
    recovered_runs: int
    non_recovered_runs: int
    non_recovery_rate: float


def _finite_series(values: Sequence[float], *, field: str) -> tuple[float, ...]:
    if not values:
        raise ValueError(f"{field} must be non-empty")
    result: list[float] = []
    for value in values:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{field} values must be numeric")
        converted = float(value)
        if not math.isfinite(converted):
            raise ValueError(f"{field} values must be finite")
        result.append(converted)
    return tuple(result)


def _positive_window(value: int, *, field: str, maximum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{field} must be a positive integer")
    if value > maximum:
        raise ValueError(f"{field} exceeds the post-change horizon")
    return value


def compute_resilience_metrics(
    values: Sequence[float],
    *,
    reference_values: Sequence[float],
    change_index: int,
    immediate_window: int,
    worst_window: int,
    terminal_window: int,
    recovery_tolerance: float,
    recovery_stability_steps: int,
) -> ResilienceMetrics:
    """Compute explicit curve-based estimands for one valid independent run.

    ``values`` and ``reference_values`` must be aligned, higher-is-better
    performance series. The reference is the predeclared matched no-change
    curve, not a value selected after observing the disrupted run.

    A sample is below the recovery criterion when
    ``reference - observed > recovery_tolerance``. Recovery is the earliest
    post-degradation start of ``recovery_stability_steps`` consecutive samples
    at or above that criterion. Real non-recovery returns ``None`` for both
    recovery index and delay. A run that never falls below the criterion is
    labelled ``NO_DEGRADATION`` rather than being described as recovered.
    """

    observed = _finite_series(values, field="values")
    reference = _finite_series(reference_values, field="reference_values")
    if len(observed) != len(reference):
        raise ValueError("values and reference_values must have equal length")
    if (
        not isinstance(change_index, int)
        or isinstance(change_index, bool)
        or change_index <= 0
        or change_index >= len(observed)
    ):
        raise ValueError("change_index must split non-empty pre/post segments")
    if (
        not isinstance(recovery_tolerance, (int, float))
        or isinstance(recovery_tolerance, bool)
        or not math.isfinite(float(recovery_tolerance))
        or recovery_tolerance < 0
    ):
        raise ValueError("recovery_tolerance must be finite and non-negative")

    post_length = len(observed) - change_index
    immediate_window = _positive_window(
        immediate_window, field="immediate_window", maximum=post_length
    )
    worst_window = _positive_window(
        worst_window, field="worst_window", maximum=post_length
    )
    terminal_window = _positive_window(
        terminal_window, field="terminal_window", maximum=post_length
    )
    stability = _positive_window(
        recovery_stability_steps,
        field="recovery_stability_steps",
        maximum=post_length,
    )
    tolerance = float(recovery_tolerance)

    pre_observed = observed[:change_index]
    pre_reference = reference[:change_index]
    post_observed = observed[change_index:]
    post_reference = reference[change_index:]
    gaps = tuple(
        expected - actual for expected, actual in zip(post_reference, post_observed)
    )

    nominal_mean = fmean(pre_observed)
    nominal_reference_mean = fmean(pre_reference)
    terminal_observed = post_observed[-terminal_window:]
    terminal_reference = post_reference[-terminal_window:]

    first_degradation_offset = next(
        (offset for offset, gap in enumerate(gaps) if gap > tolerance), None
    )
    recovery_offset: int | None = None
    if first_degradation_offset is not None:
        first_candidate = first_degradation_offset + 1
        final_candidate = len(gaps) - stability
        for offset in range(first_candidate, final_candidate + 1):
            if all(gap <= tolerance for gap in gaps[offset : offset + stability]):
                recovery_offset = offset
                break

    if first_degradation_offset is None:
        recovery_status = RecoveryStatus.NO_DEGRADATION
    elif recovery_offset is None:
        recovery_status = RecoveryStatus.NOT_RECOVERED
    else:
        recovery_status = RecoveryStatus.RECOVERED

    return ResilienceMetrics(
        nominal_mean=nominal_mean,
        nominal_reference_mean=nominal_reference_mean,
        nominal_gap=nominal_reference_mean - nominal_mean,
        immediate_degradation=fmean(gaps[:immediate_window]),
        worst_degradation=max(gaps[:worst_window]),
        post_change_mean=fmean(terminal_observed),
        post_change_reference_mean=fmean(terminal_reference),
        post_change_gap=fmean(terminal_reference) - fmean(terminal_observed),
        cumulative_deficit=sum(max(0.0, gap) for gap in gaps),
        first_degradation_index=(
            None
            if first_degradation_offset is None
            else change_index + first_degradation_offset
        ),
        recovery_index=(
            None if recovery_offset is None else change_index + recovery_offset
        ),
        recovery_delay=recovery_offset,
        recovery_status=recovery_status,
    )


def summarize_recovery_statuses(statuses: Sequence[RecoveryStatus]) -> RecoverySummary:
    """Summarize predefined valid independent runs without hiding non-recovery."""

    if not statuses:
        raise ValueError("recovery statuses must be non-empty")
    if not all(isinstance(status, RecoveryStatus) for status in statuses):
        raise ValueError("every recovery status must be a RecoveryStatus")
    total = len(statuses)
    no_degradation = statuses.count(RecoveryStatus.NO_DEGRADATION)
    recovered = statuses.count(RecoveryStatus.RECOVERED)
    non_recovered = statuses.count(RecoveryStatus.NOT_RECOVERED)
    return RecoverySummary(
        total_runs=total,
        no_degradation_runs=no_degradation,
        recovered_runs=recovered,
        non_recovered_runs=non_recovered,
        non_recovery_rate=non_recovered / total,
    )
