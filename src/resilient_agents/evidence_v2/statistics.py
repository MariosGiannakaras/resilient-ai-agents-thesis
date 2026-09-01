"""Pure protocol-v2 statistical primitives independent of plotting/UI code."""
from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping, Sequence

from ..protocol_v2 import ProtocolV2Branch


class MetricDirection(str, Enum):
    HIGHER_IS_BETTER = "higher-is-better"
    HIGHER_IS_WORSE = "higher-is-worse"


def _finite(value: float, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


@dataclass(frozen=True)
class MeanInterval:
    n: int
    mean: float
    standard_deviation: float
    standard_error: float
    lower: float
    upper: float


@dataclass(frozen=True)
class MatchedAdaptationEffect:
    frozen_nominal: float
    frozen_disturbed: float
    adaptive_nominal: float
    adaptive_disturbed: float
    frozen_loss: float
    adaptive_loss: float
    adaptation_benefit: float


def trapezoidal_time_average(points: Sequence[tuple[int, float]]) -> float:
    """Area-under-curve divided by interaction span.

    The caller supplies the frozen probe grid. Duplicate/unsorted interaction
    indices are rejected so the analysis cannot silently reinterpret a curve.
    """

    if len(points) < 2:
        raise ValueError("at least two evaluation points are required")
    normalized: list[tuple[int, float]] = []
    previous: int | None = None
    for index, value in points:
        if not isinstance(index, int) or isinstance(index, bool) or index < 0:
            raise ValueError("interaction index must be a non-negative integer")
        if previous is not None and index <= previous:
            raise ValueError("evaluation interaction indices must be strictly increasing")
        normalized.append((index, _finite(value, field="evaluation value")))
        previous = index
    start = normalized[0][0]
    end = normalized[-1][0]
    if end == start:
        raise ValueError("evaluation curve interaction span must be > 0")
    area = 0.0
    for (x0, y0), (x1, y1) in zip(normalized, normalized[1:]):
        area += (x1 - x0) * (y0 + y1) / 2.0
    return area / (end - start)


def matched_adaptation_effect(
    branch_values: Mapping[ProtocolV2Branch, float],
    *,
    direction: MetricDirection,
) -> MatchedAdaptationEffect:
    """Compute four-branch matched loss and adaptation benefit.

    Loss is always oriented positive-is-worse. For a higher-is-better metric,
    regime loss is nominal minus disturbed. For a higher-is-worse metric, it is
    disturbed minus nominal. Adaptation benefit is then Frozen loss - Adaptive
    loss, so positive values mean ordinary continued learning reduced the
    disturbance-associated loss relative to its matched nominal reference.
    """

    if not isinstance(direction, MetricDirection):
        raise ValueError("direction must be MetricDirection")
    if set(branch_values) != set(ProtocolV2Branch):
        raise ValueError("branch_values must contain exactly FN/FD/AN/AD")
    values = {
        branch: _finite(value, field=f"{branch.value} value")
        for branch, value in branch_values.items()
    }
    fn = values[ProtocolV2Branch.FROZEN_NOMINAL]
    fd = values[ProtocolV2Branch.FROZEN_DISTURBED]
    an = values[ProtocolV2Branch.ADAPTIVE_NOMINAL]
    ad = values[ProtocolV2Branch.ADAPTIVE_DISTURBED]
    if direction is MetricDirection.HIGHER_IS_BETTER:
        frozen_loss = fn - fd
        adaptive_loss = an - ad
    else:
        frozen_loss = fd - fn
        adaptive_loss = ad - an
    return MatchedAdaptationEffect(
        frozen_nominal=fn,
        frozen_disturbed=fd,
        adaptive_nominal=an,
        adaptive_disturbed=ad,
        frozen_loss=frozen_loss,
        adaptive_loss=adaptive_loss,
        adaptation_benefit=frozen_loss - adaptive_loss,
    )


def mean_across_layouts(layout_values: Mapping[str, float]) -> float:
    """Equal-weight blocked layout aggregation within one independent root."""

    if not layout_values:
        raise ValueError("at least one layout value is required")
    values = [_finite(value, field=f"layout {layout_id}") for layout_id, value in layout_values.items()]
    return statistics.fmean(values)


def paired_root_differences(
    first: Mapping[str, float],
    second: Mapping[str, float],
) -> dict[str, float]:
    """Return first-second paired effects under identical root identities."""

    if not first or set(first) != set(second):
        raise ValueError("paired root maps must contain the same non-empty root identities")
    return {
        root_id: _finite(first[root_id], field=f"first[{root_id}]")
        - _finite(second[root_id], field=f"second[{root_id}]")
        for root_id in sorted(first)
    }


def student_t_mean_interval(
    values: Iterable[float],
    *,
    critical_value: float,
) -> MeanInterval:
    """Mean +/- frozen Student-t critical value * root-level standard error.

    T-527 owns the final root count and therefore the exact two-sided critical
    value. Keeping it in the frozen analysis recipe avoids a new runtime
    dependency and prevents hidden alpha/df choices inside analysis code.
    """

    normalized = [_finite(value, field="root value") for value in values]
    if len(normalized) < 2:
        raise ValueError("Student-t interval requires at least two independent roots")
    critical = _finite(critical_value, field="critical_value")
    if critical <= 0:
        raise ValueError("critical_value must be > 0")
    mean = statistics.fmean(normalized)
    standard_deviation = statistics.stdev(normalized)
    standard_error = standard_deviation / math.sqrt(len(normalized))
    margin = critical * standard_error
    return MeanInterval(
        n=len(normalized),
        mean=mean,
        standard_deviation=standard_deviation,
        standard_error=standard_error,
        lower=mean - margin,
        upper=mean + margin,
    )
