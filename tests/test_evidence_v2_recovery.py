from __future__ import annotations

import pytest

from resilient_agents.evidence_v2.recovery import (
    RecoveryDefinition,
    assess_recovery,
    pairwise_method_contrasts,
)
from resilient_agents.evidence_v2.statistics import MetricDirection


def _definition(**overrides):
    values = {
        "window_size": 32,
        "observation_horizon": 256,
        "tolerance": 0.10,
        "stability_windows": 2,
        "direction": MetricDirection.HIGHER_IS_BETTER,
    }
    values.update(overrides)
    return RecoveryDefinition(**values)


def test_very_fast_recovery_is_stability_confirmed() -> None:
    nominal = [0.5] * 8
    disturbed = [0.45, 0.46, 0.44, 0.45, 0.45, 0.45, 0.45, 0.45]
    result = assess_recovery(nominal_windows=nominal, disturbed_windows=disturbed, definition=_definition())
    assert result.status == "recovered"
    assert result.recovery_time == 32
    assert result.confirmation_time == 64


def test_slower_recovery_reports_first_stable_window_not_confirmation_window() -> None:
    nominal = [0.5] * 8
    disturbed = [0.0, 0.1, 0.2, 0.39, 0.41, 0.42, 0.43, 0.44]
    result = assess_recovery(nominal_windows=nominal, disturbed_windows=disturbed, definition=_definition())
    assert result.status == "recovered"
    assert result.recovery_time == 160
    assert result.confirmation_time == 192


def test_never_recovered_is_right_censored_without_artificial_horizon_time() -> None:
    result = assess_recovery(
        nominal_windows=[0.5] * 8,
        disturbed_windows=[0.0] * 8,
        definition=_definition(),
    )
    assert result.status == "right-censored"
    assert result.recovery_time is None
    assert result.confirmation_time is None
    assert result.censoring_time == 256


def test_temporary_threshold_crossing_is_not_stable_recovery() -> None:
    result = assess_recovery(
        nominal_windows=[0.5] * 8,
        disturbed_windows=[0.0, 0.45, 0.0, 0.45, 0.0, 0.45, 0.0, 0.45],
        definition=_definition(),
    )
    assert result.status == "right-censored"
    assert result.recovery_time is None


def test_recovery_can_start_in_penultimate_window_and_confirm_at_horizon() -> None:
    result = assess_recovery(
        nominal_windows=[0.5] * 8,
        disturbed_windows=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45, 0.45],
        definition=_definition(),
    )
    assert result.recovery_time == 224
    assert result.confirmation_time == 256


def test_higher_is_worse_direction_is_supported() -> None:
    result = assess_recovery(
        nominal_windows=[1.0] * 8,
        disturbed_windows=[2.0, 1.5, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0],
        definition=_definition(direction=MetricDirection.LOWER_IS_BETTER),
    )
    assert result.recovery_time == 96
    assert result.confirmation_time == 128


def test_calculation_is_deterministic_and_uses_matched_nominal_reference() -> None:
    definition = _definition()
    nominal = [0.50, 0.49, 0.48, 0.47, 0.46, 0.45, 0.44, 0.43]
    disturbed = [0.0, 0.1, 0.2, 0.37, 0.36, 0.35, 0.34, 0.33]
    first = assess_recovery(nominal_windows=nominal, disturbed_windows=disturbed, definition=definition)
    second = assess_recovery(nominal_windows=nominal, disturbed_windows=disturbed, definition=definition)
    assert first == second
    assert [point.nominal_value for point in first.trajectory] == nominal
    assert first.recovery_time == 128


def test_pairwise_method_contrasts_pair_only_common_independent_roots() -> None:
    contrasts = pairwise_method_contrasts(
        {
            "a": {"r1": 1.0, "r2": 2.0, "r3": 3.0},
            "b": {"r1": 0.0, "r2": 1.0, "r4": 99.0},
            "c": {"r1": 2.0, "r2": 4.0},
        }
    )
    ab = next(item for item in contrasts if (item.method_a, item.method_b) == ("a", "b"))
    assert ab.root_ids == ("r1", "r2")
    assert ab.differences == pytest.approx((1.0, 1.0))
    assert ab.interval.mean == pytest.approx(1.0)


def test_recovery_definition_rejects_non_divisible_windows() -> None:
    with pytest.raises(ValueError, match="divisible"):
        RecoveryDefinition(window_size=30, observation_horizon=256)
