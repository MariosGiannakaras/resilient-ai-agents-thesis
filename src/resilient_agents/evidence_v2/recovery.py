"""Predeclared protocol-v2.1 recovery and cross-method comparison primitives.

The functions in this module are pure analysis utilities. They do not inspect UI
state, final-reserve metadata, or choose thresholds from observed outcomes.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations
from typing import Mapping, Sequence

from .statistics import (
    MeanInterval,
    MetricDirection,
    paired_root_differences,
    student_t_mean_interval,
)


@dataclass(frozen=True)
class RecoveryDefinition:
    """Frozen recovery-speed operationalization for one trajectory metric."""

    window_size: int = 32
    observation_horizon: int = 256
    tolerance: float = 0.10
    stability_windows: int = 2
    direction: MetricDirection = MetricDirection.HIGHER_IS_BETTER

    def __post_init__(self) -> None:
        if (
            not isinstance(self.window_size, int)
            or isinstance(self.window_size, bool)
            or self.window_size <= 0
        ):
            raise ValueError("window_size must be an integer > 0")
        if (
            not isinstance(self.observation_horizon, int)
            or isinstance(self.observation_horizon, bool)
            or self.observation_horizon <= 0
        ):
            raise ValueError("observation_horizon must be an integer > 0")
        if self.observation_horizon % self.window_size != 0:
            raise ValueError("observation_horizon must be divisible by window_size")
        if not isinstance(self.tolerance, (int, float)) or isinstance(self.tolerance, bool):
            raise ValueError("tolerance must be numeric")
        if not math.isfinite(float(self.tolerance)) or float(self.tolerance) < 0.0:
            raise ValueError("tolerance must be finite and >= 0")
        if (
            not isinstance(self.stability_windows, int)
            or isinstance(self.stability_windows, bool)
            or self.stability_windows <= 0
        ):
            raise ValueError("stability_windows must be an integer > 0")
        if not isinstance(self.direction, MetricDirection):
            raise ValueError("direction must be MetricDirection")

    @property
    def expected_window_count(self) -> int:
        return self.observation_horizon // self.window_size


@dataclass(frozen=True)
class RecoveryTrajectoryPoint:
    window_index: int
    window_start: int
    window_end: int
    nominal_value: float
    disturbed_value: float
    directed_gap: float
    within_tolerance: bool


@dataclass(frozen=True)
class RecoveryResult:
    status: str
    recovery_time: int | None
    confirmation_time: int | None
    censoring_time: int
    trajectory: tuple[RecoveryTrajectoryPoint, ...]

    def __post_init__(self) -> None:
        if self.status not in {"recovered", "right-censored"}:
            raise ValueError("unsupported recovery status")
        if self.status == "recovered" and self.recovery_time is None:
            raise ValueError("recovered result requires recovery_time")
        if self.status == "right-censored" and self.recovery_time is not None:
            raise ValueError("right-censored result must not invent recovery_time")


def _finite_series(values: Sequence[float], *, field: str) -> tuple[float, ...]:
    result: list[float] = []
    for raw in values:
        if not isinstance(raw, (int, float)) or isinstance(raw, bool):
            raise ValueError(f"{field} values must be numeric")
        value = float(raw)
        if not math.isfinite(value):
            raise ValueError(f"{field} values must be finite")
        result.append(value)
    return tuple(result)


def assess_recovery(
    *,
    nominal_windows: Sequence[float],
    disturbed_windows: Sequence[float],
    definition: RecoveryDefinition,
) -> RecoveryResult:
    """Assess stable recovery against the matched adaptive-nominal trajectory.

    Each input value is the mean reward per *actual* environment interaction in
    one deterministic interaction window. Episode boundaries neither reset nor
    realign windows. The first in-tolerance window of the first stable run is
    reported as recovery_time; confirmation_time is the end of the final window
    required by the stability rule. If no stable run occurs, recovery_time is
    None and the observation is explicitly right-censored at the fixed horizon.
    """

    nominal = _finite_series(nominal_windows, field="nominal_windows")
    disturbed = _finite_series(disturbed_windows, field="disturbed_windows")
    if len(nominal) != definition.expected_window_count:
        raise ValueError("nominal_windows length does not match frozen horizon/window size")
    if len(disturbed) != len(nominal):
        raise ValueError("matched nominal/disturbed window counts differ")

    points: list[RecoveryTrajectoryPoint] = []
    stable_run = 0
    run_start = 0
    recovery_time: int | None = None
    confirmation_time: int | None = None
    tolerance = float(definition.tolerance)

    for index, (nominal_value, disturbed_value) in enumerate(
        zip(nominal, disturbed, strict=True)
    ):
        if definition.direction is MetricDirection.HIGHER_IS_BETTER:
            directed_gap = nominal_value - disturbed_value
        else:
            directed_gap = disturbed_value - nominal_value
        within = directed_gap <= tolerance
        window_start = index * definition.window_size
        window_end = (index + 1) * definition.window_size
        points.append(
            RecoveryTrajectoryPoint(
                window_index=index,
                window_start=window_start,
                window_end=window_end,
                nominal_value=nominal_value,
                disturbed_value=disturbed_value,
                directed_gap=directed_gap,
                within_tolerance=within,
            )
        )
        if within:
            if stable_run == 0:
                run_start = index
            stable_run += 1
            if stable_run >= definition.stability_windows and recovery_time is None:
                recovery_time = (run_start + 1) * definition.window_size
                confirmation_time = window_end
        else:
            stable_run = 0

    status = "recovered" if recovery_time is not None else "right-censored"
    return RecoveryResult(
        status=status,
        recovery_time=recovery_time,
        confirmation_time=confirmation_time,
        censoring_time=definition.observation_horizon,
        trajectory=tuple(points),
    )


@dataclass(frozen=True)
class MethodContrast:
    method_a: str
    method_b: str
    root_ids: tuple[str, ...]
    differences: tuple[float, ...]
    interval: MeanInterval


def pairwise_method_contrasts(
    root_values_by_method: Mapping[str, Mapping[str, float]],
    *,
    critical_value: float,
) -> tuple[MethodContrast, ...]:
    """Return pointwise root-paired A-minus-B method contrasts.

    Layouts and episodes must already have been reduced within each independent
    root. When a scientific failure leaves asymmetric method root sets, only the
    shared roots form the paired estimand and their identities remain explicit.
    ``critical_value`` is supplied by the frozen analysis recipe; this function
    never chooses alpha/df or upgrades pointwise intervals to simultaneous
    multiple-comparison inference.
    """

    methods = tuple(sorted(root_values_by_method))
    contrasts: list[MethodContrast] = []
    for method_a, method_b in combinations(methods, 2):
        left = root_values_by_method[method_a]
        right = root_values_by_method[method_b]
        common_roots = tuple(sorted(set(left).intersection(right)))
        if len(common_roots) < 2:
            continue
        left_common = {root_id: left[root_id] for root_id in common_roots}
        right_common = {root_id: right[root_id] for root_id in common_roots}
        differences_map = paired_root_differences(left_common, right_common)
        differences = tuple(float(differences_map[root]) for root in common_roots)
        contrasts.append(
            MethodContrast(
                method_a=method_a,
                method_b=method_b,
                root_ids=common_roots,
                differences=differences,
                interval=student_t_mean_interval(
                    differences,
                    critical_value=critical_value,
                ),
            )
        )
    return tuple(contrasts)
