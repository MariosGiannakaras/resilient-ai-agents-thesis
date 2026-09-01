"""Protocol-v2.1 statistical wrapper over the deterministic v2 analysis engine.

The existing engine already owns blocking, matched estimands, recovery and
failure retention.  Protocol-v2.1 adds one pre-outcome statistical refinement:
Student-t critical values are selected from a frozen table by the *actual*
number of independent paired roots, so retained scientific failures cannot make
an interval silently use the df for twelve roots.
"""
from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Mapping

from ..study import StudyStore
from .analysis import StudyAnalysisEngine

V21_ANALYSIS_RECIPE = "protocol-v2-root-level-v2.1"
V21_STUDENT_T_95_CRITICAL_BY_N: Mapping[int, float] = {
    2: 12.706,
    3: 4.303,
    4: 3.182,
    5: 2.776,
    6: 2.571,
    7: 2.447,
    8: 2.365,
    9: 2.306,
    10: 2.262,
    11: 2.228,
    12: 2.201,
}


def _critical_table(value: Any) -> dict[int, float]:
    if not isinstance(value, Mapping):
        raise ValueError("analysis.interval.critical_value_by_n must be an object")
    parsed: dict[int, float] = {}
    for raw_n, raw_value in value.items():
        try:
            n = int(raw_n)
        except (TypeError, ValueError) as exc:
            raise ValueError("Student-t critical table keys must be integer root counts") from exc
        if str(n) != str(raw_n):
            raise ValueError("Student-t critical table keys must be canonical integer strings")
        if not isinstance(raw_value, (int, float)) or isinstance(raw_value, bool):
            raise ValueError("Student-t critical values must be numeric")
        critical = float(raw_value)
        if not math.isfinite(critical) or critical <= 0:
            raise ValueError("Student-t critical values must be finite and > 0")
        parsed[n] = critical
    if parsed != dict(V21_STUDENT_T_95_CRITICAL_BY_N):
        raise ValueError("protocol-v2.1 requires the frozen two-sided 95% Student-t table for n=2..12")
    return parsed


def _validate_interval_spec(value: Any) -> dict[int, float]:
    if not isinstance(value, Mapping):
        raise ValueError("analysis.interval must be an object")
    if set(value) != {"kind", "confidence", "critical_value_by_n"}:
        raise ValueError("protocol-v2.1 interval keys mismatch")
    if value["kind"] != "student-t":
        raise ValueError("protocol-v2.1 requires Student-t intervals")
    if float(value["confidence"]) != 0.95:
        raise ValueError("protocol-v2.1 confidence is frozen at 0.95")
    return _critical_table(value["critical_value_by_n"])


def _repair_interval(interval: Mapping[str, Any], table: Mapping[int, float]) -> dict[str, Any]:
    result = dict(interval)
    n = int(result["n"])
    if n not in table:
        raise RuntimeError(f"no frozen Student-t critical value for independent-root n={n}")
    mean = float(result["mean"])
    standard_error = float(result["standard_error"])
    margin = table[n] * standard_error
    result["lower"] = mean - margin
    result["upper"] = mean + margin
    result["critical_value"] = table[n]
    result["confidence"] = 0.95
    return result


def _repair_summary(summary: Any, table: Mapping[int, float]) -> None:
    if not isinstance(summary, dict):
        return
    interval = summary.get("interval")
    if isinstance(interval, Mapping):
        summary["interval"] = _repair_interval(interval, table)


def _repair_contrasts(rows: Any, table: Mapping[int, float]) -> None:
    if not isinstance(rows, list):
        return
    for row in rows:
        if not isinstance(row, dict):
            continue
        interval = row.get("interval")
        if isinstance(interval, Mapping):
            row["interval"] = _repair_interval(interval, table)


def _repair_package_intervals(package: dict[str, Any], table: Mapping[int, float]) -> None:
    phase_a = package["phase_a"]
    for row in phase_a.get("method_summaries", []):
        _repair_summary(row.get("final_value"), table)
        _repair_summary(row.get("time_average"), table)
    _repair_contrasts(phase_a.get("method_contrasts"), table)

    phase_b = package["phase_b"]
    for row in phase_b.get("method_condition_summaries", []):
        _repair_summary(row.get("frozen_loss"), table)
        _repair_summary(row.get("adaptive_loss"), table)
        _repair_summary(row.get("adaptation_benefit"), table)
    _repair_contrasts(phase_b.get("method_contrasts"), table)

    recovery = phase_b.get("recovery")
    if isinstance(recovery, dict):
        for row in recovery.get("method_condition_summaries", []):
            _repair_summary(row.get("recovery_time_conditional_on_recovery"), table)
            _repair_summary(row.get("restricted_recovery_delay_through_horizon"), table)
        _repair_contrasts(recovery.get("method_contrasts"), table)


class StudyAnalysisEngineV21:
    """Run v2.1 recovery/comparison analysis with actual-root-df intervals."""

    def analyze(
        self,
        store: StudyStore,
        *,
        specification: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(specification, Mapping):
            raise ValueError("analysis specification must be an object")
        original = deepcopy(dict(specification))
        if original.get("analysis_recipe") != V21_ANALYSIS_RECIPE:
            raise ValueError(f"protocol-v2.1 requires analysis_recipe={V21_ANALYSIS_RECIPE}")
        table = _validate_interval_spec(original.get("interval"))

        # The base engine needs one positive scalar only to compute SD/SE and a
        # provisional margin. v2.1 deterministically replaces every such margin
        # below using the actual independent-root n and the frozen table.
        delegated = deepcopy(original)
        delegated["analysis_recipe"] = "protocol-v2-root-level-v2"
        delegated["interval"] = {
            "kind": "student-t",
            "critical_value": table[12],
        }
        package = StudyAnalysisEngine().analyze(store, specification=delegated)
        _repair_package_intervals(package, table)
        package["analysis_recipe"] = V21_ANALYSIS_RECIPE
        package["specification"] = original
        package["interval_policy"] = {
            "kind": "student-t",
            "confidence": 0.95,
            "independent_unit": "root",
            "critical_value_selected_by": "actual-independent-root-count",
            "critical_value_by_n": {str(n): table[n] for n in sorted(table)},
            "pointwise_not_simultaneous": True,
            "p_value_superiority_family": False,
        }
        return package
