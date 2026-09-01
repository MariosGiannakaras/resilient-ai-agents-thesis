"""Strict read-only projection of stored protocol-v2 analysis packages.

The desktop layer verifies registered evidence and projects values already
computed by the backend.  It never selects recovery thresholds, reduces roots,
or recalculates scientific estimands/intervals.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from ..study.store import StudyStore
from .study_read_model import DesktopStudyReadModel

_ANALYSIS_ARTIFACT_ID = "analysis-package"
_ANALYSIS_RECIPE_V1 = "protocol-v2-root-level-v1"
_ANALYSIS_RECIPE_V2 = "protocol-v2-root-level-v2"
_ANALYSIS_RECIPE_V21 = "protocol-v2-root-level-v2.1"
_SUPPORTED_ANALYSIS_RECIPES = {
    _ANALYSIS_RECIPE_V1,
    _ANALYSIS_RECIPE_V2,
    _ANALYSIS_RECIPE_V21,
}
_DIRECTIONS = {"higher-is-better", "higher-is-worse"}
_INTERVAL_KEYS = {
    "n",
    "mean",
    "standard_deviation",
    "standard_error",
    "lower",
    "upper",
}
_INTERVAL_PROVENANCE_KEYS = {"critical_value", "confidence"}


def _mapping(value: Any, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RuntimeError(f"{field} must be an object")
    return value


def _list(value: Any, *, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise RuntimeError(f"{field} must be a list")
    return value


def _identifier(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"{field} must be a non-empty string")
    return value


def _direction(value: Any, *, field: str) -> str:
    result = _identifier(value, field=field)
    if result not in _DIRECTIONS:
        raise RuntimeError(f"{field} is unsupported")
    return result


def _count(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise RuntimeError(f"{field} must be a non-negative integer")
    return value


def _positive_count(value: Any, *, field: str) -> int:
    result = _count(value, field=field)
    if result <= 0:
        raise RuntimeError(f"{field} must be > 0")
    return result


def _number(value: Any, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise RuntimeError(f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise RuntimeError(f"{field} must be finite")
    return result


def _optional_number(value: Any, *, field: str) -> float | None:
    if value is None:
        return None
    return _number(value, field=field)


def _boolean(value: Any, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise RuntimeError(f"{field} must be boolean")
    return value


def _optional_boolean(value: Any, *, field: str) -> bool | None:
    if value is None:
        return None
    return _boolean(value, field=field)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class StoredSummary:
    n: int
    mean: float | None
    interval_lower: float | None
    interval_upper: float | None
    interval_status: str | None


@dataclass(frozen=True)
class LearningSummary:
    method_id: str
    metric: str
    direction: str
    planned_root_count: int
    included_root_count: int
    final_value: StoredSummary
    time_average: StoredSummary


@dataclass(frozen=True)
class ResilienceSummary:
    method_id: str
    condition_id: str
    metric: str
    direction: str
    planned_root_count: int
    included_root_count: int
    frozen_loss: StoredSummary
    adaptive_loss: StoredSummary
    adaptation_benefit: StoredSummary


@dataclass(frozen=True)
class StoredMethodContrast:
    source: str
    estimand: str
    condition_id: str | None
    primary_recovery_axis: bool | None
    method_a: str
    method_b: str
    difference_orientation: str
    root_ids: tuple[str, ...]
    mean_difference: float
    interval_lower: float
    interval_upper: float


@dataclass(frozen=True)
class RecoverySummary:
    method_id: str
    condition_id: str
    condition_family: str
    primary_recovery_axis: bool
    included_root_count: int
    recovered_root_count: int
    right_censored_root_count: int
    recovered_proportion: float | None
    recovery_time_conditional_on_recovery: StoredSummary
    restricted_recovery_delay_through_horizon: StoredSummary


@dataclass(frozen=True)
class RecoveryTrajectoryPoint:
    method_id: str
    root_id: str
    condition_id: str
    condition_family: str
    primary_recovery_axis: bool
    window_index: int
    window_start: int
    window_end: int
    nominal_value: float
    disturbed_value: float
    directed_gap: float
    within_tolerance: bool


@dataclass(frozen=True)
class RecoveryEvidence:
    metric: str
    direction: str
    window_size: int
    observation_horizon: int
    primary_tolerance: float
    stability_windows: int
    primary_condition_family: str
    summaries: tuple[RecoverySummary, ...]
    trajectories: tuple[RecoveryTrajectoryPoint, ...]
    method_contrasts: tuple[StoredMethodContrast, ...]


@dataclass(frozen=True)
class StoredAnalysisPackage:
    study_id: str
    recipe_sha256: str
    analysis_recipe: str
    artifact_sha256: str
    relative_path: str
    phase_a_metric: str
    phase_a_direction: str
    phase_b_metric: str
    phase_b_direction: str
    learning: tuple[LearningSummary, ...]
    resilience: tuple[ResilienceSummary, ...]
    method_contrasts: tuple[StoredMethodContrast, ...] = ()
    recovery: RecoveryEvidence | None = None


def _stored_interval(
    value: Any,
    *,
    field: str,
    expected_n: int | None = None,
    expected_mean: float | None = None,
) -> StoredSummary:
    payload = _mapping(value, field=field)
    keys = set(payload)
    if not _INTERVAL_KEYS.issubset(keys) or not keys.issubset(
        _INTERVAL_KEYS | _INTERVAL_PROVENANCE_KEYS
    ):
        raise RuntimeError(f"{field} keys mismatch")
    n = _count(payload["n"], field=f"{field}.n")
    mean = _number(payload["mean"], field=f"{field}.mean")
    if expected_n is not None and n != expected_n:
        raise RuntimeError(f"{field} n does not match stored parent")
    if expected_mean is not None and mean != expected_mean:
        raise RuntimeError(f"{field} mean does not match stored parent")
    _number(payload["standard_deviation"], field=f"{field}.standard_deviation")
    _number(payload["standard_error"], field=f"{field}.standard_error")
    lower = _number(payload["lower"], field=f"{field}.lower")
    upper = _number(payload["upper"], field=f"{field}.upper")
    if lower > upper:
        raise RuntimeError(f"{field} stored interval bounds are reversed")
    if "critical_value" in payload:
        if _number(payload["critical_value"], field=f"{field}.critical_value") <= 0:
            raise RuntimeError(f"{field}.critical_value must be > 0")
    if "confidence" in payload:
        confidence = _number(payload["confidence"], field=f"{field}.confidence")
        if not 0.0 < confidence < 1.0:
            raise RuntimeError(f"{field}.confidence must be in (0,1)")
    return StoredSummary(
        n=n,
        mean=mean,
        interval_lower=lower,
        interval_upper=upper,
        interval_status=None,
    )


def _stored_summary(value: Any, *, field: str) -> StoredSummary:
    payload = _mapping(value, field=field)
    expected = {"n", "mean", "interval"}
    allowed = expected | {"interval_status"}
    if not expected.issubset(payload) or not set(payload).issubset(allowed):
        raise RuntimeError(f"{field} summary keys mismatch")
    n = _count(payload["n"], field=f"{field}.n")
    mean = _optional_number(payload["mean"], field=f"{field}.mean")
    if (n == 0) != (mean is None):
        raise RuntimeError(f"{field} n/mean consistency mismatch")

    interval = payload["interval"]
    lower: float | None = None
    upper: float | None = None
    if interval is not None:
        if mean is None:
            raise RuntimeError(f"{field} interval requires a stored mean")
        parsed = _stored_interval(
            interval,
            field=f"{field}.interval",
            expected_n=n,
            expected_mean=mean,
        )
        lower = parsed.interval_lower
        upper = parsed.interval_upper

    status = payload.get("interval_status")
    if status is not None and (not isinstance(status, str) or not status.strip()):
        raise RuntimeError(f"{field}.interval_status must be a non-empty string")
    return StoredSummary(
        n=n,
        mean=mean,
        interval_lower=lower,
        interval_upper=upper,
        interval_status=status,
    )


def _method_contrasts(value: Any, *, source: str) -> tuple[StoredMethodContrast, ...]:
    result: list[StoredMethodContrast] = []
    seen: set[tuple[str, str, str, str | None]] = set()
    for index, item in enumerate(_list(value, field=f"{source}.method_contrasts")):
        payload = _mapping(item, field=f"{source}.method_contrasts[{index}]")
        required = {
            "estimand",
            "method_a",
            "method_b",
            "difference_orientation",
            "root_ids",
            "differences",
            "interval",
        }
        allowed = required | {"condition_id", "primary_recovery_axis"}
        if not required.issubset(payload) or not set(payload).issubset(allowed):
            raise RuntimeError(f"{source} method contrast keys mismatch")
        estimand = _identifier(payload["estimand"], field="contrast.estimand")
        method_a = _identifier(payload["method_a"], field="contrast.method_a")
        method_b = _identifier(payload["method_b"], field="contrast.method_b")
        orientation = _identifier(
            payload["difference_orientation"], field="contrast.difference_orientation"
        )
        if orientation != "method_a-minus-method_b":
            raise RuntimeError("unsupported stored method contrast orientation")
        condition_raw = payload.get("condition_id")
        condition_id = (
            None
            if condition_raw is None
            else _identifier(condition_raw, field="contrast.condition_id")
        )
        primary_axis = _optional_boolean(
            payload.get("primary_recovery_axis"),
            field="contrast.primary_recovery_axis",
        )
        root_ids = tuple(
            _identifier(raw, field="contrast.root_id")
            for raw in _list(payload["root_ids"], field="contrast.root_ids")
        )
        if len(root_ids) < 2 or len(root_ids) != len(set(root_ids)):
            raise RuntimeError("stored method contrast root identities are invalid")
        differences = tuple(
            _number(raw, field="contrast.difference")
            for raw in _list(payload["differences"], field="contrast.differences")
        )
        if len(differences) != len(root_ids):
            raise RuntimeError("stored contrast differences/root identities mismatch")
        interval = _stored_interval(
            payload["interval"],
            field="contrast.interval",
            expected_n=len(root_ids),
        )
        key = (estimand, method_a, method_b, condition_id)
        if key in seen:
            raise RuntimeError(f"duplicate stored method contrast: {key}")
        seen.add(key)
        if interval.mean is None or interval.interval_lower is None or interval.interval_upper is None:
            raise RuntimeError("stored method contrast interval is incomplete")
        result.append(
            StoredMethodContrast(
                source=source,
                estimand=estimand,
                condition_id=condition_id,
                primary_recovery_axis=primary_axis,
                method_a=method_a,
                method_b=method_b,
                difference_orientation=orientation,
                root_ids=root_ids,
                mean_difference=interval.mean,
                interval_lower=interval.interval_lower,
                interval_upper=interval.interval_upper,
            )
        )
    return tuple(result)


def _recovery_evidence(value: Any) -> RecoveryEvidence:
    payload = _mapping(value, field="phase_b.recovery")
    expected = {
        "metric",
        "direction",
        "window_size",
        "observation_horizon",
        "primary_tolerance",
        "stability_windows",
        "primary_condition_family",
        "sensitivity_tolerances",
        "censoring_policy",
        "restricted_delay_policy",
        "root_records",
        "trajectory_records",
        "method_condition_summaries",
        "method_contrasts",
        "sensitivity_root_records",
    }
    if set(payload) != expected:
        raise RuntimeError("phase_b.recovery keys mismatch")
    metric = _identifier(payload["metric"], field="recovery.metric")
    direction = _direction(payload["direction"], field="recovery.direction")
    window_size = _positive_count(payload["window_size"], field="recovery.window_size")
    horizon = _positive_count(
        payload["observation_horizon"], field="recovery.observation_horizon"
    )
    if horizon % window_size:
        raise RuntimeError("stored recovery window grid is inconsistent")
    tolerance = _number(payload["primary_tolerance"], field="recovery.primary_tolerance")
    if tolerance < 0:
        raise RuntimeError("stored recovery tolerance must be non-negative")
    stability = _positive_count(
        payload["stability_windows"], field="recovery.stability_windows"
    )
    primary_family = _identifier(
        payload["primary_condition_family"], field="recovery.primary_condition_family"
    )
    for raw in _list(payload["sensitivity_tolerances"], field="recovery.sensitivity_tolerances"):
        if _number(raw, field="recovery sensitivity tolerance") < 0:
            raise RuntimeError("stored recovery sensitivity tolerance must be non-negative")
    _identifier(payload["censoring_policy"], field="recovery.censoring_policy")
    _identifier(payload["restricted_delay_policy"], field="recovery.restricted_delay_policy")
    _list(payload["root_records"], field="recovery.root_records")
    _list(payload["sensitivity_root_records"], field="recovery.sensitivity_root_records")

    summaries: list[RecoverySummary] = []
    seen_summaries: set[tuple[str, str]] = set()
    for index, item in enumerate(
        _list(payload["method_condition_summaries"], field="recovery.method_condition_summaries")
    ):
        row = _mapping(item, field=f"recovery.method_condition_summaries[{index}]")
        fields = {
            "method_id",
            "condition_id",
            "condition_family",
            "primary_recovery_axis",
            "included_root_count",
            "recovered_root_count",
            "right_censored_root_count",
            "recovered_proportion",
            "recovery_time_conditional_on_recovery",
            "restricted_recovery_delay_through_horizon",
        }
        if set(row) != fields:
            raise RuntimeError("recovery method/condition summary keys mismatch")
        method_id = _identifier(row["method_id"], field="recovery method_id")
        condition_id = _identifier(row["condition_id"], field="recovery condition_id")
        key = (method_id, condition_id)
        if key in seen_summaries:
            raise RuntimeError(f"duplicate recovery method/condition summary: {key}")
        seen_summaries.add(key)
        included = _count(row["included_root_count"], field="recovery included_root_count")
        recovered = _count(row["recovered_root_count"], field="recovery recovered_root_count")
        censored = _count(
            row["right_censored_root_count"], field="recovery right_censored_root_count"
        )
        if recovered + censored != included:
            raise RuntimeError("recovery status counts do not match included roots")
        proportion = _optional_number(
            row["recovered_proportion"], field="recovery recovered_proportion"
        )
        if proportion is not None and not 0.0 <= proportion <= 1.0:
            raise RuntimeError("recovery recovered_proportion must be in [0,1]")
        summaries.append(
            RecoverySummary(
                method_id=method_id,
                condition_id=condition_id,
                condition_family=_identifier(
                    row["condition_family"], field="recovery condition_family"
                ),
                primary_recovery_axis=_boolean(
                    row["primary_recovery_axis"], field="recovery primary_recovery_axis"
                ),
                included_root_count=included,
                recovered_root_count=recovered,
                right_censored_root_count=censored,
                recovered_proportion=proportion,
                recovery_time_conditional_on_recovery=_stored_summary(
                    row["recovery_time_conditional_on_recovery"],
                    field="recovery_time_conditional_on_recovery",
                ),
                restricted_recovery_delay_through_horizon=_stored_summary(
                    row["restricted_recovery_delay_through_horizon"],
                    field="restricted_recovery_delay_through_horizon",
                ),
            )
        )

    trajectories: list[RecoveryTrajectoryPoint] = []
    seen_points: set[tuple[str, str, str, int]] = set()
    expected_window_count = horizon // window_size
    for index, item in enumerate(
        _list(payload["trajectory_records"], field="recovery.trajectory_records")
    ):
        row = _mapping(item, field=f"recovery.trajectory_records[{index}]")
        fields = {
            "method_id",
            "root_id",
            "condition_id",
            "condition_family",
            "primary_recovery_axis",
            "window_index",
            "window_start",
            "window_end",
            "nominal_value",
            "disturbed_value",
            "directed_gap",
            "within_tolerance",
        }
        if set(row) != fields:
            raise RuntimeError("recovery trajectory keys mismatch")
        window_index = _count(row["window_index"], field="recovery window_index")
        if window_index >= expected_window_count:
            raise RuntimeError("recovery window_index exceeds frozen horizon")
        window_start = _positive_count(row["window_start"], field="recovery window_start")
        window_end = _positive_count(row["window_end"], field="recovery window_end")
        expected_start = window_index * window_size + 1
        expected_end = (window_index + 1) * window_size
        if window_start != expected_start or window_end != expected_end:
            raise RuntimeError("stored recovery trajectory is not on its declared window grid")
        method_id = _identifier(row["method_id"], field="trajectory method_id")
        root_id = _identifier(row["root_id"], field="trajectory root_id")
        condition_id = _identifier(row["condition_id"], field="trajectory condition_id")
        key = (method_id, root_id, condition_id, window_index)
        if key in seen_points:
            raise RuntimeError(f"duplicate recovery trajectory point: {key}")
        seen_points.add(key)
        trajectories.append(
            RecoveryTrajectoryPoint(
                method_id=method_id,
                root_id=root_id,
                condition_id=condition_id,
                condition_family=_identifier(
                    row["condition_family"], field="trajectory condition_family"
                ),
                primary_recovery_axis=_boolean(
                    row["primary_recovery_axis"], field="trajectory primary_recovery_axis"
                ),
                window_index=window_index,
                window_start=window_start,
                window_end=window_end,
                nominal_value=_number(row["nominal_value"], field="trajectory nominal_value"),
                disturbed_value=_number(
                    row["disturbed_value"], field="trajectory disturbed_value"
                ),
                directed_gap=_number(row["directed_gap"], field="trajectory directed_gap"),
                within_tolerance=_boolean(
                    row["within_tolerance"], field="trajectory within_tolerance"
                ),
            )
        )

    return RecoveryEvidence(
        metric=metric,
        direction=direction,
        window_size=window_size,
        observation_horizon=horizon,
        primary_tolerance=tolerance,
        stability_windows=stability,
        primary_condition_family=primary_family,
        summaries=tuple(summaries),
        trajectories=tuple(trajectories),
        method_contrasts=_method_contrasts(
            payload["method_contrasts"], source="recovery"
        ),
    )


class DesktopResultsReadModel:
    """Read registered analysis packages without calculating scientific results."""

    def __init__(self, study_read_model: DesktopStudyReadModel) -> None:
        if not isinstance(study_read_model, DesktopStudyReadModel):
            raise ValueError("study_read_model must be DesktopStudyReadModel")
        self.study_read_model = study_read_model
        self.repo_root = study_read_model.repo_root
        self.writable_root = study_read_model.writable_root

    def study_ids(self) -> tuple[str, ...]:
        result: list[str] = []
        for study in self.study_read_model.studies():
            artifacts = self.study_read_model.artifacts(study.study_id)
            if any(
                artifact.artifact_id == _ANALYSIS_ARTIFACT_ID
                and artifact.role == "analysis-data"
                and artifact.evidence_class == "derived"
                for artifact in artifacts
            ):
                result.append(study.study_id)
        return tuple(result)

    def load(self, study_id: str) -> StoredAnalysisPackage:
        if not isinstance(study_id, str) or not study_id.strip():
            raise ValueError("study_id must be non-empty")
        artifacts = self.study_read_model.artifacts(study_id)
        matches = [
            artifact
            for artifact in artifacts
            if artifact.artifact_id == _ANALYSIS_ARTIFACT_ID
            and artifact.role == "analysis-data"
            and artifact.evidence_class == "derived"
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"study {study_id} must register exactly one derived analysis-package artifact"
            )
        artifact = matches[0]
        path = (self.writable_root / artifact.relative_path).resolve()
        try:
            path.relative_to(self.writable_root)
        except ValueError as exc:
            raise RuntimeError("analysis-package path escapes writable evidence root") from exc
        if not path.is_file():
            raise RuntimeError(f"analysis-package file is missing: {artifact.relative_path}")
        actual_sha = _sha256_file(path)
        if actual_sha != artifact.sha256:
            raise RuntimeError("analysis-package SHA-256 does not match registered artifact")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RuntimeError("analysis-package is unreadable JSON") from exc
        root = _mapping(payload, field="analysis-package")
        schema_version = root.get("schema_version")
        if schema_version not in {1, 2}:
            raise RuntimeError("unsupported analysis-package schema_version")
        analysis_recipe = _identifier(root.get("analysis_recipe"), field="analysis_recipe")
        if analysis_recipe not in _SUPPORTED_ANALYSIS_RECIPES:
            raise RuntimeError("unsupported analysis_recipe")
        if schema_version == 1 and analysis_recipe != _ANALYSIS_RECIPE_V1:
            raise RuntimeError("analysis-package schema/recipe mismatch")
        if schema_version == 2 and analysis_recipe == _ANALYSIS_RECIPE_V1:
            raise RuntimeError("analysis-package schema/recipe mismatch")

        expected_root = {
            "schema_version",
            "analysis_recipe",
            "study_id",
            "recipe_sha256",
            "specification",
            "phase_a",
            "phase_b",
            "scientific_denominators",
        }
        if analysis_recipe == _ANALYSIS_RECIPE_V21:
            expected_root = expected_root | {"interval_policy"}
        if set(root) != expected_root:
            raise RuntimeError("analysis-package root keys mismatch")
        if root["study_id"] != study_id:
            raise RuntimeError("analysis-package study_id does not match selected Study")

        store = StudyStore.load(
            repo_root=self.repo_root,
            writable_root=self.writable_root,
            study_id=study_id,
        )
        recipe_sha = store.recipe.sha256()
        package_recipe_sha = _identifier(root["recipe_sha256"], field="recipe_sha256")
        if package_recipe_sha != recipe_sha:
            raise RuntimeError("analysis-package recipe SHA-256 does not match durable Study recipe")

        _mapping(root["specification"], field="specification")
        _mapping(root["scientific_denominators"], field="scientific_denominators")
        if analysis_recipe == _ANALYSIS_RECIPE_V21:
            _mapping(root["interval_policy"], field="interval_policy")
        phase_a = _mapping(root["phase_a"], field="phase_a")
        phase_b = _mapping(root["phase_b"], field="phase_b")
        phase_a_keys = {
            "metric",
            "direction",
            "unit_records",
            "root_records",
            "method_summaries",
        }
        phase_b_keys = {
            "metric",
            "direction",
            "unit_records",
            "root_records",
            "method_condition_summaries",
        }
        if schema_version == 2:
            phase_a_keys |= {"method_contrasts"}
            phase_b_keys |= {"method_contrasts", "recovery"}
        if set(phase_a) != phase_a_keys:
            raise RuntimeError("phase_a keys mismatch")
        if set(phase_b) != phase_b_keys:
            raise RuntimeError("phase_b keys mismatch")
        for field_name in ("unit_records", "root_records"):
            _list(phase_a[field_name], field=f"phase_a.{field_name}")
            _list(phase_b[field_name], field=f"phase_b.{field_name}")

        phase_a_metric = _identifier(phase_a["metric"], field="phase_a.metric")
        phase_a_direction = _direction(phase_a["direction"], field="phase_a.direction")
        phase_b_metric = _identifier(phase_b["metric"], field="phase_b.metric")
        phase_b_direction = _direction(phase_b["direction"], field="phase_b.direction")

        learning: list[LearningSummary] = []
        seen_methods: set[str] = set()
        for index, item in enumerate(
            _list(phase_a["method_summaries"], field="phase_a.method_summaries")
        ):
            summary = _mapping(item, field=f"phase_a.method_summaries[{index}]")
            expected = {
                "method_id",
                "metric",
                "direction",
                "planned_root_count",
                "included_root_count",
                "final_value",
                "time_average",
            }
            if set(summary) != expected:
                raise RuntimeError("Phase-A method summary keys mismatch")
            method_id = _identifier(summary["method_id"], field="Phase-A method_id")
            if method_id in seen_methods:
                raise RuntimeError(f"duplicate Phase-A method summary: {method_id}")
            seen_methods.add(method_id)
            metric = _identifier(summary["metric"], field="Phase-A summary metric")
            direction = _direction(summary["direction"], field="Phase-A summary direction")
            if metric != phase_a_metric or direction != phase_a_direction:
                raise RuntimeError("Phase-A summary metadata disagrees with phase metadata")
            learning.append(
                LearningSummary(
                    method_id=method_id,
                    metric=metric,
                    direction=direction,
                    planned_root_count=_count(
                        summary["planned_root_count"], field="Phase-A planned_root_count"
                    ),
                    included_root_count=_count(
                        summary["included_root_count"], field="Phase-A included_root_count"
                    ),
                    final_value=_stored_summary(summary["final_value"], field="final_value"),
                    time_average=_stored_summary(summary["time_average"], field="time_average"),
                )
            )

        resilience: list[ResilienceSummary] = []
        seen_method_conditions: set[tuple[str, str]] = set()
        for index, item in enumerate(
            _list(
                phase_b["method_condition_summaries"],
                field="phase_b.method_condition_summaries",
            )
        ):
            summary = _mapping(item, field=f"phase_b.method_condition_summaries[{index}]")
            expected = {
                "method_id",
                "condition_id",
                "metric",
                "direction",
                "planned_root_count",
                "included_root_count",
                "frozen_loss",
                "adaptive_loss",
                "adaptation_benefit",
            }
            if set(summary) != expected:
                raise RuntimeError("Phase-B method/condition summary keys mismatch")
            method_id = _identifier(summary["method_id"], field="Phase-B method_id")
            condition_id = _identifier(summary["condition_id"], field="Phase-B condition_id")
            key = (method_id, condition_id)
            if key in seen_method_conditions:
                raise RuntimeError(f"duplicate Phase-B method/condition summary: {key}")
            seen_method_conditions.add(key)
            metric = _identifier(summary["metric"], field="Phase-B summary metric")
            direction = _direction(summary["direction"], field="Phase-B summary direction")
            if metric != phase_b_metric or direction != phase_b_direction:
                raise RuntimeError("Phase-B summary metadata disagrees with phase metadata")
            resilience.append(
                ResilienceSummary(
                    method_id=method_id,
                    condition_id=condition_id,
                    metric=metric,
                    direction=direction,
                    planned_root_count=_count(
                        summary["planned_root_count"], field="Phase-B planned_root_count"
                    ),
                    included_root_count=_count(
                        summary["included_root_count"], field="Phase-B included_root_count"
                    ),
                    frozen_loss=_stored_summary(summary["frozen_loss"], field="frozen_loss"),
                    adaptive_loss=_stored_summary(
                        summary["adaptive_loss"], field="adaptive_loss"
                    ),
                    adaptation_benefit=_stored_summary(
                        summary["adaptation_benefit"], field="adaptation_benefit"
                    ),
                )
            )

        contrasts: list[StoredMethodContrast] = []
        recovery: RecoveryEvidence | None = None
        if schema_version == 2:
            contrasts.extend(_method_contrasts(phase_a["method_contrasts"], source="phase-a"))
            contrasts.extend(_method_contrasts(phase_b["method_contrasts"], source="phase-b"))
            recovery = _recovery_evidence(phase_b["recovery"])
            contrasts.extend(recovery.method_contrasts)

        return StoredAnalysisPackage(
            study_id=study_id,
            recipe_sha256=recipe_sha,
            analysis_recipe=analysis_recipe,
            artifact_sha256=artifact.sha256,
            relative_path=artifact.relative_path,
            phase_a_metric=phase_a_metric,
            phase_a_direction=phase_a_direction,
            phase_b_metric=phase_b_metric,
            phase_b_direction=phase_b_direction,
            learning=tuple(learning),
            resilience=tuple(resilience),
            method_contrasts=tuple(contrasts),
            recovery=recovery,
        )
