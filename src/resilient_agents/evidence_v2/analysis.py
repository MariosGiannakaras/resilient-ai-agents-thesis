"""Recipe-driven protocol-v2 study analysis over frozen scientific records.

The engine consumes standardized Phase-A/Phase-B analysis records registered in
a StudyStore.  It never reads UI state and never replaces missing scientific
units.  Root/layout blocking and interval behavior are explicit analysis-recipe
inputs so T-527 can freeze them without changing analysis code.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping

from ..protocol_v2 import ProtocolV2Branch
from ..study import ArtifactRole, JobState, StudyStage, StudyStore
from .records import PhaseAAnalysisRecord, PhaseBAnalysisRecord
from .statistics import (
    MetricDirection,
    matched_adaptation_effect,
    mean_across_layouts,
    student_t_mean_interval,
    trapezoidal_time_average,
)

ANALYSIS_PACKAGE_SCHEMA_VERSION = 1
_SUPPORTED_RECIPE = "protocol-v2-root-level-v1"


def _mapping(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return dict(value)


def _direction(value: Any, *, field: str) -> MetricDirection:
    try:
        return MetricDirection(str(value))
    except ValueError as exc:
        raise ValueError(f"{field} must be a supported metric direction") from exc


def _identifier(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _read_json(path: Path, *, field: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{field} is unreadable: {path}") from exc
    if not isinstance(payload, Mapping):
        raise RuntimeError(f"{field} must contain a JSON object")
    return dict(payload)


def _interval_spec(value: Any) -> tuple[str, float | None]:
    payload = _mapping(value, field="analysis.interval")
    kind = payload.get("kind")
    if kind == "none":
        if set(payload) != {"kind"}:
            raise ValueError("analysis.interval kind=none accepts no additional fields")
        return "none", None
    if kind == "student-t":
        if set(payload) != {"kind", "critical_value"}:
            raise ValueError("student-t interval requires exactly critical_value")
        critical = payload["critical_value"]
        if not isinstance(critical, (int, float)) or isinstance(critical, bool):
            raise ValueError("analysis.interval.critical_value must be numeric")
        critical_float = float(critical)
        if critical_float <= 0:
            raise ValueError("analysis.interval.critical_value must be > 0")
        return "student-t", critical_float
    raise ValueError("analysis.interval.kind must be none or student-t")


def _summary(values: list[float], *, interval_kind: str, critical_value: float | None) -> dict[str, Any]:
    if not values:
        return {"n": 0, "mean": None, "interval": None}
    mean = sum(values) / len(values)
    if interval_kind == "none":
        return {"n": len(values), "mean": mean, "interval": None}
    if critical_value is None:
        raise AssertionError("student-t interval critical value missing")
    if len(values) < 2:
        return {
            "n": len(values),
            "mean": mean,
            "interval": None,
            "interval_status": "insufficient-independent-roots",
        }
    interval = student_t_mean_interval(values, critical_value=critical_value)
    return {
        "n": interval.n,
        "mean": interval.mean,
        "interval": asdict(interval),
    }


class StudyAnalysisEngine:
    """Build deterministic root-level Phase-A and matched Phase-B datasets."""

    def analyze(
        self,
        store: StudyStore,
        *,
        specification: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(store, StudyStore):
            raise ValueError("store must be StudyStore")
        spec = _mapping(specification, field="analysis specification")
        expected = {
            "analysis_recipe",
            "phase_a_metric",
            "phase_a_direction",
            "phase_b_metric",
            "phase_b_direction",
            "layout_aggregation",
            "require_complete_layout_blocks",
            "interval",
        }
        if set(spec) != expected:
            raise ValueError(
                "analysis specification keys mismatch; "
                f"missing={sorted(expected - set(spec))}, unknown={sorted(set(spec) - expected)}"
            )
        if spec["analysis_recipe"] != _SUPPORTED_RECIPE:
            raise ValueError("unsupported protocol-v2 analysis_recipe")
        if spec["layout_aggregation"] != "equal-weight":
            raise ValueError("protocol-v2 analysis currently requires equal-weight layout blocking")
        if not isinstance(spec["require_complete_layout_blocks"], bool):
            raise ValueError("require_complete_layout_blocks must be boolean")

        phase_a_metric = _identifier(spec["phase_a_metric"], field="phase_a_metric")
        phase_b_metric = _identifier(spec["phase_b_metric"], field="phase_b_metric")
        phase_a_direction = _direction(spec["phase_a_direction"], field="phase_a_direction")
        phase_b_direction = _direction(spec["phase_b_direction"], field="phase_b_direction")
        interval_kind, critical_value = _interval_spec(spec["interval"])
        require_complete = spec["require_complete_layout_blocks"]

        phase_a_records, phase_b_records = self._load_records(store)
        phase_a = self._phase_a(
            store,
            phase_a_records,
            metric=phase_a_metric,
            direction=phase_a_direction,
            require_complete=require_complete,
            interval_kind=interval_kind,
            critical_value=critical_value,
        )
        phase_b = self._phase_b(
            store,
            phase_b_records,
            metric=phase_b_metric,
            direction=phase_b_direction,
            require_complete=require_complete,
            interval_kind=interval_kind,
            critical_value=critical_value,
        )
        return {
            "schema_version": ANALYSIS_PACKAGE_SCHEMA_VERSION,
            "analysis_recipe": _SUPPORTED_RECIPE,
            "study_id": store.plan.study_id,
            "recipe_sha256": store.recipe.sha256(),
            "specification": spec,
            "phase_a": phase_a,
            "phase_b": phase_b,
        }

    def _load_records(
        self,
        store: StudyStore,
    ) -> tuple[list[PhaseAAnalysisRecord], list[PhaseBAnalysisRecord]]:
        phase_a: list[PhaseAAnalysisRecord] = []
        phase_b: list[PhaseBAnalysisRecord] = []
        for artifact in store.artifacts():
            if artifact.role is not ArtifactRole.ANALYSIS_DATA:
                continue
            record_type = artifact.metadata.get("record_type")
            path = store.writable_root / artifact.relative_path
            if record_type == "phase-a":
                phase_a.append(PhaseAAnalysisRecord.from_dict(_read_json(path, field="Phase-A analysis record")))
            elif record_type == "phase-b":
                phase_b.append(PhaseBAnalysisRecord.from_dict(_read_json(path, field="Phase-B analysis record")))
        return phase_a, phase_b

    @staticmethod
    def _planned_layouts_for_phase_a(store: StudyStore) -> dict[tuple[str, str], set[str]]:
        result: dict[tuple[str, str], set[str]] = {}
        for job in store.plan.jobs_for_stage(StudyStage.PHASE_A):
            if job.payload.get("job_type") != "phase-a-training":
                continue
            method = job.payload.get("method", {})
            root = job.payload.get("root", {})
            layout = job.payload.get("layout", {})
            key = (str(method.get("method_id")), str(root.get("root_id")))
            result.setdefault(key, set()).add(str(layout.get("layout_id")))
        return result

    @staticmethod
    def _planned_layouts_for_phase_b(store: StudyStore) -> dict[tuple[str, str, str], set[str]]:
        result: dict[tuple[str, str, str], set[str]] = {}
        for job in store.plan.jobs_for_stage(StudyStage.PHASE_B):
            if job.payload.get("job_type") != "phase-b-matched-set":
                continue
            method = job.payload.get("method", {})
            root = job.payload.get("root", {})
            layout = job.payload.get("layout", {})
            condition = job.payload.get("condition", {})
            key = (
                str(method.get("method_id")),
                str(root.get("root_id")),
                str(condition.get("condition_id")),
            )
            result.setdefault(key, set()).add(str(layout.get("layout_id")))
        return result

    def _phase_a(
        self,
        store: StudyStore,
        records: list[PhaseAAnalysisRecord],
        *,
        metric: str,
        direction: MetricDirection,
        require_complete: bool,
        interval_kind: str,
        critical_value: float | None,
    ) -> dict[str, Any]:
        unit_records: list[dict[str, Any]] = []
        by_block: dict[tuple[str, str], dict[str, dict[str, float]]] = {}
        seen_units: set[tuple[str, str, str]] = set()
        for record in records:
            unit_key = (record.method_id, record.root_id, record.layout_id)
            if unit_key in seen_units:
                raise RuntimeError(f"duplicate Phase-A analysis unit: {unit_key}")
            seen_units.add(unit_key)
            values: list[tuple[int, float]] = []
            for probe in record.probes:
                if metric not in probe.metrics:
                    raise RuntimeError(
                        f"Phase-A metric {metric!r} missing from {record.job_id} probe"
                    )
                values.append((probe.interaction_index, float(probe.metrics[metric])))
            final_value = values[-1][1]
            time_average = trapezoidal_time_average(values)
            unit_records.append(
                {
                    "method_id": record.method_id,
                    "root_id": record.root_id,
                    "layout_id": record.layout_id,
                    "job_id": record.job_id,
                    "final_value": final_value,
                    "time_average": time_average,
                }
            )
            by_block.setdefault((record.method_id, record.root_id), {})[record.layout_id] = {
                "final_value": final_value,
                "time_average": time_average,
            }

        planned = self._planned_layouts_for_phase_a(store)
        root_records: list[dict[str, Any]] = []
        method_values: dict[str, dict[str, list[float]]] = {}
        for key in sorted(planned):
            method_id, root_id = key
            expected_layouts = planned[key]
            observed = by_block.get(key, {})
            observed_layouts = set(observed)
            complete = observed_layouts == expected_layouts
            eligible = complete or (not require_complete and bool(observed_layouts))
            row: dict[str, Any] = {
                "method_id": method_id,
                "root_id": root_id,
                "planned_layout_count": len(expected_layouts),
                "observed_layout_count": len(observed_layouts),
                "missing_layout_ids": sorted(expected_layouts - observed_layouts),
                "complete_layout_block": complete,
                "included_in_primary_summary": eligible,
                "final_value": None,
                "time_average": None,
            }
            if eligible:
                row["final_value"] = mean_across_layouts(
                    {layout: values["final_value"] for layout, values in observed.items()}
                )
                row["time_average"] = mean_across_layouts(
                    {layout: values["time_average"] for layout, values in observed.items()}
                )
                bucket = method_values.setdefault(
                    method_id,
                    {"final_value": [], "time_average": []},
                )
                bucket["final_value"].append(float(row["final_value"]))
                bucket["time_average"].append(float(row["time_average"]))
            root_records.append(row)

        summaries = []
        methods = sorted({method for method, _ in planned})
        for method_id in methods:
            planned_roots = sum(1 for method, _ in planned if method == method_id)
            values = method_values.get(method_id, {"final_value": [], "time_average": []})
            summaries.append(
                {
                    "method_id": method_id,
                    "metric": metric,
                    "direction": direction.value,
                    "planned_root_count": planned_roots,
                    "included_root_count": len(values["final_value"]),
                    "final_value": _summary(
                        values["final_value"],
                        interval_kind=interval_kind,
                        critical_value=critical_value,
                    ),
                    "time_average": _summary(
                        values["time_average"],
                        interval_kind=interval_kind,
                        critical_value=critical_value,
                    ),
                }
            )
        return {
            "metric": metric,
            "direction": direction.value,
            "unit_records": sorted(
                unit_records,
                key=lambda row: (row["method_id"], row["root_id"], row["layout_id"]),
            ),
            "root_records": root_records,
            "method_summaries": summaries,
        }

    def _phase_b(
        self,
        store: StudyStore,
        records: list[PhaseBAnalysisRecord],
        *,
        metric: str,
        direction: MetricDirection,
        require_complete: bool,
        interval_kind: str,
        critical_value: float | None,
    ) -> dict[str, Any]:
        by_unit: dict[
            tuple[str, str, str, str],
            dict[ProtocolV2Branch, PhaseBAnalysisRecord],
        ] = {}
        for record in records:
            key = (
                record.method_id,
                record.root_id,
                record.layout_id,
                record.condition_id,
            )
            branches = by_unit.setdefault(key, {})
            if record.branch in branches:
                raise RuntimeError(f"duplicate Phase-B branch analysis record: {key} {record.branch.value}")
            branches[record.branch] = record

        unit_records: list[dict[str, Any]] = []
        by_block: dict[tuple[str, str, str], dict[str, dict[str, float]]] = {}
        for key in sorted(by_unit):
            method_id, root_id, layout_id, condition_id = key
            branches = by_unit[key]
            if set(branches) != set(ProtocolV2Branch):
                raise RuntimeError(f"completed Phase-B analysis unit lacks four branches: {key}")
            branch_values: dict[ProtocolV2Branch, float] = {}
            for branch, record in branches.items():
                if metric not in record.metrics:
                    raise RuntimeError(
                        f"Phase-B metric {metric!r} missing from {record.job_id} {branch.value}"
                    )
                branch_values[branch] = float(record.metrics[metric])
            effect = matched_adaptation_effect(branch_values, direction=direction)
            row = {
                "method_id": method_id,
                "root_id": root_id,
                "layout_id": layout_id,
                "condition_id": condition_id,
                **asdict(effect),
            }
            unit_records.append(row)
            by_block.setdefault((method_id, root_id, condition_id), {})[layout_id] = {
                "frozen_loss": effect.frozen_loss,
                "adaptive_loss": effect.adaptive_loss,
                "adaptation_benefit": effect.adaptation_benefit,
            }

        planned = self._planned_layouts_for_phase_b(store)
        root_records: list[dict[str, Any]] = []
        summary_values: dict[tuple[str, str], dict[str, list[float]]] = {}
        for key in sorted(planned):
            method_id, root_id, condition_id = key
            expected_layouts = planned[key]
            observed = by_block.get(key, {})
            observed_layouts = set(observed)
            complete = observed_layouts == expected_layouts
            eligible = complete or (not require_complete and bool(observed_layouts))
            row: dict[str, Any] = {
                "method_id": method_id,
                "root_id": root_id,
                "condition_id": condition_id,
                "planned_layout_count": len(expected_layouts),
                "observed_layout_count": len(observed_layouts),
                "missing_layout_ids": sorted(expected_layouts - observed_layouts),
                "complete_layout_block": complete,
                "included_in_primary_summary": eligible,
                "frozen_loss": None,
                "adaptive_loss": None,
                "adaptation_benefit": None,
            }
            if eligible:
                for name in ("frozen_loss", "adaptive_loss", "adaptation_benefit"):
                    row[name] = mean_across_layouts(
                        {layout: values[name] for layout, values in observed.items()}
                    )
                bucket = summary_values.setdefault(
                    (method_id, condition_id),
                    {"frozen_loss": [], "adaptive_loss": [], "adaptation_benefit": []},
                )
                for name in bucket:
                    bucket[name].append(float(row[name]))
            root_records.append(row)

        summaries: list[dict[str, Any]] = []
        method_conditions = sorted({(method, condition) for method, _, condition in planned})
        for method_id, condition_id in method_conditions:
            planned_roots = sum(
                1
                for method, _, condition in planned
                if method == method_id and condition == condition_id
            )
            values = summary_values.get(
                (method_id, condition_id),
                {"frozen_loss": [], "adaptive_loss": [], "adaptation_benefit": []},
            )
            summaries.append(
                {
                    "method_id": method_id,
                    "condition_id": condition_id,
                    "metric": metric,
                    "direction": direction.value,
                    "planned_root_count": planned_roots,
                    "included_root_count": len(values["adaptation_benefit"]),
                    "frozen_loss": _summary(
                        values["frozen_loss"],
                        interval_kind=interval_kind,
                        critical_value=critical_value,
                    ),
                    "adaptive_loss": _summary(
                        values["adaptive_loss"],
                        interval_kind=interval_kind,
                        critical_value=critical_value,
                    ),
                    "adaptation_benefit": _summary(
                        values["adaptation_benefit"],
                        interval_kind=interval_kind,
                        critical_value=critical_value,
                    ),
                }
            )
        return {
            "metric": metric,
            "direction": direction.value,
            "unit_records": unit_records,
            "root_records": root_records,
            "method_condition_summaries": summaries,
        }
