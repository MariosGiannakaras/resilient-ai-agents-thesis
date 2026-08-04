"""Known-answer resilience metrics with explicit scientific parameters."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Sequence


@dataclass(frozen=True)
class ResilienceMetrics:
    nominal_mean: float
    immediate_degradation: float
    worst_degradation: float
    post_change_mean: float
    cumulative_loss: float
    recovery_step: int | None


def _validate(values: Sequence[float], change_index: int) -> None:
    if not values:
        raise ValueError("metric series must be non-empty")
    if change_index <= 0 or change_index >= len(values):
        raise ValueError("change_index must split non-empty pre/post segments")


def compute_resilience_metrics(
    values: Sequence[float],
    *,
    change_index: int,
    recovery_fraction: float,
    reference_value: float | None = None,
) -> ResilienceMetrics:
    """Compute basic recovery metrics without silently choosing a threshold.

    ``recovery_fraction`` must be supplied by the protocol. ``None`` is returned
    when recovery is not observed inside the available horizon.
    """

    _validate(values, change_index)
    if not 0.0 <= recovery_fraction <= 1.0:
        raise ValueError("recovery_fraction must be within [0, 1]")

    pre = values[:change_index]
    post = values[change_index:]
    nominal = fmean(pre)
    immediate = nominal - post[0]
    worst = nominal - min(post)
    post_mean = fmean(post)
    reference = nominal if reference_value is None else reference_value
    cumulative_loss = sum(max(0.0, reference - value) for value in post)
    threshold = nominal * recovery_fraction

    recovery_step: int | None = None
    for offset, value in enumerate(post):
        if value >= threshold:
            recovery_step = change_index + offset
            break

    return ResilienceMetrics(
        nominal_mean=nominal,
        immediate_degradation=immediate,
        worst_degradation=worst,
        post_change_mean=post_mean,
        cumulative_loss=cumulative_loss,
        recovery_step=recovery_step,
    )
