"""Strict read-only projection of stored protocol-v2 analysis packages."""
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
_ANALYSIS_RECIPE = "protocol-v2-root-level-v1"
_DIRECTIONS = {"higher-is-better", "higher-is-worse"}
_INTERVAL_KEYS = {
    "n",
    "mean",
    "standard_deviation",
    "standard_error",
    "lower",
    "upper",
}


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
        interval_payload = _mapping(interval, field=f"{field}.interval")
        if set(interval_payload) != _INTERVAL_KEYS:
            raise RuntimeError(f"{field}.interval keys mismatch")
        if _count(interval_payload["n"], field=f"{field}.interval.n") != n:
            raise RuntimeError(f"{field} interval n does not match summary n")
        interval_mean = _number(interval_payload["mean"], field=f"{field}.interval.mean")
        if mean is None or interval_mean != mean:
            raise RuntimeError(f"{field} interval mean does not match stored summary mean")
        _number(
            interval_payload["standard_deviation"],
            field=f"{field}.interval.standard_deviation",
        )
        _number(
            interval_payload["standard_error"],
            field=f"{field}.interval.standard_error",
        )
        lower = _number(interval_payload["lower"], field=f"{field}.interval.lower")
        upper = _number(interval_payload["upper"], field=f"{field}.interval.upper")
        if lower > upper:
            raise RuntimeError(f"{field} stored interval bounds are reversed")

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
        if set(root) != expected_root:
            raise RuntimeError("analysis-package root keys mismatch")
        if root["schema_version"] != 1:
            raise RuntimeError("unsupported analysis-package schema_version")
        if root["analysis_recipe"] != _ANALYSIS_RECIPE:
            raise RuntimeError("unsupported analysis_recipe")
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
        phase_a = _mapping(root["phase_a"], field="phase_a")
        phase_b = _mapping(root["phase_b"], field="phase_b")
        if set(phase_a) != {"metric", "direction", "unit_records", "root_records", "method_summaries"}:
            raise RuntimeError("phase_a keys mismatch")
        if set(phase_b) != {"metric", "direction", "unit_records", "root_records", "method_condition_summaries"}:
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

        return StoredAnalysisPackage(
            study_id=study_id,
            recipe_sha256=recipe_sha,
            analysis_recipe=_ANALYSIS_RECIPE,
            artifact_sha256=artifact.sha256,
            relative_path=artifact.relative_path,
            phase_a_metric=phase_a_metric,
            phase_a_direction=phase_a_direction,
            phase_b_metric=phase_b_metric,
            phase_b_direction=phase_b_direction,
            learning=tuple(learning),
            resilience=tuple(resilience),
        )
