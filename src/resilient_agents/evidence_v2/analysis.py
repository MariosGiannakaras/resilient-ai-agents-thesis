"""Recipe-driven protocol-v2 study analysis over frozen scientific records.

The engine consumes standardized Phase-A/Phase-B analysis records registered in
a StudyStore. It never reads UI state and never replaces missing scientific
units. Layouts are repeated blocks within independent roots and are therefore
reduced before root-level inference or cross-method contrasts.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping

from ..protocol_v2 import ProtocolV2Branch
from ..study import ArtifactRole, StudyStage, StudyStore
from .records import (
    PHASE_B_TEMPORAL_SCHEMA_VERSION,
    PhaseAAnalysisRecord,
    PhaseBAnalysisRecord,
)
from .recovery import (
    RecoveryDefinition,
    assess_recovery,
    pairwise_method_contrasts,
)
from .statistics import (
    MetricDirection,
    matched_adaptation_effect,
    mean_across_layouts,
    student_t_mean_interval,
    trapezoidal_time_average,
)

ANALYSIS_PACKAGE_SCHEMA_VERSION = 1
ANALYSIS_PACKAGE_SCHEMA_VERSION_V2 = 2
_SUPPORTED_RECIPE_V1 = "protocol-v2-root-level-v1"
_SUPPORTED_RECIPE_V2 = "protocol-v2-root-level-v2"
_BASE_SPEC_KEYS = {
    "analysis_recipe",
    "phase_a_metric",
    "phase_a_direction",
    "phase_b_metric",
    "phase_b_direction",
    "layout_aggregation",
    "require_complete_layout_blocks",
    "interval",
}


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


def _summary(
    values: list[float],
    *,
    interval_kind: str,
    critical_value: float | None,
) -> dict[str, Any]:
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


def _recovery_spec(value: Any) -> tuple[RecoveryDefinition, tuple[float, ...], str]:
    payload = _mapping(value, field="analysis.recovery")
    expected = {
        "window_size",
        "observation_horizon",
        "tolerance",
        "sensitivity_tolerances",
        "stability_windows",
        "primary_condition_family",
    }
    if set(payload) != expected:
        raise ValueError("analysis.recovery keys mismatch")
    primary_family = _identifier(
        payload["primary_condition_family"],
        field="analysis.recovery.primary_condition_family",
    )
    raw_sensitivity = payload["sensitivity_tolerances"]
    if not isinstance(raw_sensitivity, list):
        raise ValueError("analysis.recovery.sensitivity_tolerances must be a list")
    sensitivity: list[float] = []
    for raw in raw_sensitivity:
        if not isinstance(raw, (int, float)) or isinstance(raw, bool):
            raise ValueError("recovery sensitivity tolerances must be numeric")
        value_float = float(raw)
        if value_float < 0:
            raise ValueError("recovery sensitivity tolerances must be >= 0")
        sensitivity.append(value_float)
    if len(sensitivity) != len(set(sensitivity)):
        raise ValueError("recovery sensitivity tolerances must be unique")
    definition = RecoveryDefinition(
        window_size=payload["window_size"],
        observation_horizon=payload["observation_horizon"],
        tolerance=payload["tolerance"],
        stability_windows=payload["stability_windows"],
        direction=MetricDirection.HIGHER_IS_BETTER,
    )
    return definition, tuple(sensitivity), primary_family


def _contrast_rows(
    root_values_by_method: Mapping[str, Mapping[str, float]],
    *,
    estimand: str,
    critical_value: float,
    condition_id: str | None = None,
    primary_recovery_axis: bool | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contrast in pairwise_method_contrasts(
        root_values_by_method,
        critical_value=critical_value,
    ):
        row: dict[str, Any] = {
            "estimand": estimand,
            "method_a": contrast.method_a,
            "method_b": contrast.method_b,
            "difference_orientation": "method_a-minus-method_b",
            "root_ids": list(contrast.root_ids),
            "differences": list(contrast.differences),
            "interval": asdict(contrast.interval),
        }
        if condition_id is not None:
            row["condition_id"] = condition_id
        if primary_recovery_axis is not None:
            row["primary_recovery_axis"] = primary_recovery_axis
        rows.append(row)
    return rows


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
        recipe = spec.get("analysis_recipe")
        if recipe == _SUPPORTED_RECIPE_V1:
            expected = _BASE_SPEC_KEYS
            recovery_definition = None
            sensitivity_tolerances: tuple[float, ...] = ()
            primary_condition_family = ""
            package_schema = ANALYSIS_PACKAGE_SCHEMA_VERSION
        elif recipe == _SUPPORTED_RECIPE_V2:
            expected = _BASE_SPEC_KEYS | {"recovery"}
            recovery_definition, sensitivity_tolerances, primary_condition_family = (
                _recovery_spec(spec.get("recovery"))
            )
            package_schema = ANALYSIS_PACKAGE_SCHEMA_VERSION_V2
        else:
            raise ValueError("unsupported protocol-v2 analysis_recipe")
        if set(spec) != expected:
            raise ValueError(
                "analysis specification keys mismatch; "
                f"missing={sorted(expected - set(spec))}, unknown={sorted(set(spec) - expected)}"
            )
        if spec["layout_aggregation"] != "equal-weight":
            raise ValueError("protocol-v2 analysis requires equal-weight layout blocking")
        if not isinstance(spec["require_complete_layout_blocks"], bool):
            raise ValueError("require_complete_layout_blocks must be boolean")

        phase_a_metric = _identifier(spec["phase_a_metric"], field="phase_a_metric")
        phase_b_metric = _identifier(spec["phase_b_metric"], field="phase_b_metric")
        phase_a_direction = _direction(spec["phase_a_direction"], field="phase_a_direction")
        phase_b_direction = _direction(spec["phase_b_direction"], field="phase_b_direction")
        interval_kind, critical_value = _interval_spec(spec["interval"])
        require_complete = spec["require_complete_layout_blocks"]
        if recipe == _SUPPORTED_RECIPE_V2:
            if interval_kind != "student-t" or critical_value is None:
                raise ValueError("protocol-v2-root-level-v2 requires frozen Student-t intervals")
            if phase_b_direction is not MetricDirection.HIGHER_IS_BETTER:
                raise ValueError("recovery reward-window analysis requires higher-is-better direction")

        phase_a_records, phase_b_records = self._load_records(store)
        phase_a = self._phase_a(
            store,
            phase_a_records,
            metric=phase_a_metric,
            direction=phase_a_direction,
            require_complete=require_complete,
            interval_kind=interval_kind,
            critical_value=critical_value,
            direct_comparisons=recipe == _SUPPORTED_RECIPE_V2,
        )
        phase_b = self._phase_b(
            store,
            phase_b_records,
            metric=phase_b_metric,
            direction=phase_b_direction,
            require_complete=require_complete,
            interval_kind=interval_kind,
            critical_value=critical_value,
            recovery_definition=recovery_definition,
            sensitivity_tolerances=sensitivity_tolerances,
            primary_condition_family=primary_condition_family,
        )
        return {
            "schema_version": package_schema,
            "analysis_recipe": recipe,
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
                phase_a.append(
                    PhaseAAnalysisRecord.from_dict(
                        _read_json(path, field="Phase-A analysis record")
                    )
                )
            elif record_type == "phase-b":
                phase_b.append(
                    PhaseBAnalysisRecord.from_dict(
                        _read_json(path, field="Phase-B analysis record")
                    )
                )
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

    @staticmethod
    def _condition_families(store: StudyStore) -> dict[str, str]:
        families: dict[str, str] = {}
        for job in store.plan.jobs_for_stage(StudyStage.PHASE_B):
            if job.payload.get("job_type") != "phase-b-matched-set":
                continue
            condition = job.payload.get("condition", {})
            condition_id = str(condition.get("condition_id"))
            family = str(condition.get("family"))
            previous = families.setdefault(condition_id, family)
            if previous != family:
                raise RuntimeError(f"condition family mismatch for {condition_id}")
        return families

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
        direct_comparisons: bool,
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
        root_values: dict[str, dict[str, dict[str, float]]] = {
            "final_value": {},
            "time_average": {},
        }
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
                for name in ("final_value", "time_average"):
                    value = float(row[name])
                    bucket[name].append(value)
                    root_values[name].setdefault(method_id, {})[root_id] = value
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
        contrasts: list[dict[str, Any]] = []
        if direct_comparisons:
            if critical_value is None:
                raise AssertionError("v2 direct comparison critical value missing")
            contrasts.extend(
                _contrast_rows(
                    root_values["final_value"],
                    estimand="phase-a-final-value",
                    critical_value=critical_value,
                )
            )
            contrasts.extend(
                _contrast_rows(
                    root_values["time_average"],
                    estimand="phase-a-time-average",
                    critical_value=critical_value,
                )
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
            **({"method_contrasts": contrasts} if direct_comparisons else {}),
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
        recovery_definition: RecoveryDefinition | None,
        sensitivity_tolerances: tuple[float, ...],
        primary_condition_family: str,
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
                raise RuntimeError(
                    f"duplicate Phase-B branch analysis record: {key} {record.branch.value}"
                )
            branches[record.branch] = record

        unit_records: list[dict[str, Any]] = []
        by_block: dict[tuple[str, str, str], dict[str, dict[str, float]]] = {}
        temporal_by_block: dict[
            tuple[str, str, str],
            dict[str, tuple[tuple[float, ...], tuple[float, ...]]],
        ] = {}
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
            if recovery_definition is not None:
                for branch in (
                    ProtocolV2Branch.ADAPTIVE_NOMINAL,
                    ProtocolV2Branch.ADAPTIVE_DISTURBED,
                ):
                    record = branches[branch]
                    if record.schema_version != PHASE_B_TEMPORAL_SCHEMA_VERSION:
                        raise RuntimeError(
                            "recovery analysis requires schema-v2 temporal Phase-B evidence"
                        )
                    endpoints = tuple(item.end_interaction for item in record.reward_windows)
                    expected = tuple(
                        range(
                            recovery_definition.window_size,
                            recovery_definition.observation_horizon + 1,
                            recovery_definition.window_size,
                        )
                    )
                    if endpoints != expected:
                        raise RuntimeError(
                            "Phase-B reward windows do not match the frozen recovery grid"
                        )
                    if any(
                        item.interaction_count != recovery_definition.window_size
                        for item in record.reward_windows
                    ):
                        raise RuntimeError("Phase-B reward window width mismatch")
                temporal_by_block.setdefault(
                    (method_id, root_id, condition_id), {}
                )[layout_id] = (
                    tuple(
                        item.mean_reward
                        for item in branches[
                            ProtocolV2Branch.ADAPTIVE_NOMINAL
                        ].reward_windows
                    ),
                    tuple(
                        item.mean_reward
                        for item in branches[
                            ProtocolV2Branch.ADAPTIVE_DISTURBED
                        ].reward_windows
                    ),
                )

        planned = self._planned_layouts_for_phase_b(store)
        root_records: list[dict[str, Any]] = []
        summary_values: dict[tuple[str, str], dict[str, list[float]]] = {}
        root_values_by_condition: dict[
            tuple[str, str], dict[str, dict[str, float]]
        ] = {}
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
                    value = float(row[name])
                    bucket[name].append(value)
                    root_values_by_condition.setdefault(
                        (condition_id, name), {}
                    ).setdefault(method_id, {})[root_id] = value
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

        result: dict[str, Any] = {
            "metric": metric,
            "direction": direction.value,
            "unit_records": unit_records,
            "root_records": root_records,
            "method_condition_summaries": summaries,
        }
        if recovery_definition is None:
            return result
        if critical_value is None:
            raise AssertionError("v2 direct comparison critical value missing")

        standard_contrasts: list[dict[str, Any]] = []
        for (condition_id, estimand), values_by_method in sorted(
            root_values_by_condition.items()
        ):
            standard_contrasts.extend(
                _contrast_rows(
                    values_by_method,
                    estimand=f"phase-b-{estimand.replace('_', '-')}",
                    condition_id=condition_id,
                    critical_value=critical_value,
                )
            )
        result["method_contrasts"] = standard_contrasts
        result["recovery"] = self._recovery_analysis(
            store,
            planned=planned,
            temporal_by_block=temporal_by_block,
            definition=recovery_definition,
            sensitivity_tolerances=sensitivity_tolerances,
            primary_condition_family=primary_condition_family,
            require_complete=require_complete,
            interval_kind=interval_kind,
            critical_value=critical_value,
        )
        return result

    def _recovery_analysis(
        self,
        store: StudyStore,
        *,
        planned: Mapping[tuple[str, str, str], set[str]],
        temporal_by_block: Mapping[
            tuple[str, str, str],
            Mapping[str, tuple[tuple[float, ...], tuple[float, ...]]],
        ],
        definition: RecoveryDefinition,
        sensitivity_tolerances: tuple[float, ...],
        primary_condition_family: str,
        require_complete: bool,
        interval_kind: str,
        critical_value: float,
    ) -> dict[str, Any]:
        condition_families = self._condition_families(store)
        root_records: list[dict[str, Any]] = []
        trajectory_records: list[dict[str, Any]] = []
        sensitivity_records: list[dict[str, Any]] = []
        summary_values: dict[tuple[str, str], dict[str, list[float]]] = {}
        contrast_values: dict[
            tuple[str, str], dict[str, dict[str, float]]
        ] = {}

        for key in sorted(planned):
            method_id, root_id, condition_id = key
            expected_layouts = planned[key]
            observed = temporal_by_block.get(key, {})
            observed_layouts = set(observed)
            complete = observed_layouts == expected_layouts
            eligible = complete or (not require_complete and bool(observed_layouts))
            family = condition_families.get(condition_id, "")
            primary_axis = family == primary_condition_family
            row: dict[str, Any] = {
                "method_id": method_id,
                "root_id": root_id,
                "condition_id": condition_id,
                "condition_family": family,
                "primary_recovery_axis": primary_axis,
                "planned_layout_count": len(expected_layouts),
                "observed_layout_count": len(observed_layouts),
                "missing_layout_ids": sorted(expected_layouts - observed_layouts),
                "complete_layout_block": complete,
                "included_in_recovery_summary": eligible,
                "status": None,
                "recovery_time": None,
                "confirmation_time": None,
                "censoring_time": definition.observation_horizon,
                "restricted_recovery_delay_through_horizon": None,
            }
            if not eligible:
                root_records.append(row)
                continue

            nominal_windows: list[float] = []
            disturbed_windows: list[float] = []
            for window_index in range(definition.expected_window_count):
                nominal_windows.append(
                    mean_across_layouts(
                        {
                            layout_id: windows[0][window_index]
                            for layout_id, windows in observed.items()
                        }
                    )
                )
                disturbed_windows.append(
                    mean_across_layouts(
                        {
                            layout_id: windows[1][window_index]
                            for layout_id, windows in observed.items()
                        }
                    )
                )
            assessed = assess_recovery(
                nominal_windows=nominal_windows,
                disturbed_windows=disturbed_windows,
                definition=definition,
            )
            restricted_delay = (
                float(assessed.recovery_time)
                if assessed.recovery_time is not None
                else float(definition.observation_horizon)
            )
            row.update(
                {
                    "status": assessed.status,
                    "recovery_time": assessed.recovery_time,
                    "confirmation_time": assessed.confirmation_time,
                    "censoring_time": assessed.censoring_time,
                    # This is a separately named fixed-horizon comparison
                    # estimand. A censored case still has recovery_time=None.
                    "restricted_recovery_delay_through_horizon": restricted_delay,
                }
            )
            root_records.append(row)
            status_indicator = 1.0 if assessed.status == "recovered" else 0.0
            summary = summary_values.setdefault(
                (method_id, condition_id),
                {
                    "status": [],
                    "restricted_delay": [],
                    "observed_recovery_time": [],
                },
            )
            summary["status"].append(status_indicator)
            summary["restricted_delay"].append(restricted_delay)
            if assessed.recovery_time is not None:
                summary["observed_recovery_time"].append(float(assessed.recovery_time))
            contrast_values.setdefault(
                (condition_id, "recovery-status-indicator"), {}
            ).setdefault(method_id, {})[root_id] = status_indicator
            contrast_values.setdefault(
                (condition_id, "restricted-recovery-delay-through-horizon"), {}
            ).setdefault(method_id, {})[root_id] = restricted_delay

            for point in assessed.trajectory:
                trajectory_records.append(
                    {
                        "method_id": method_id,
                        "root_id": root_id,
                        "condition_id": condition_id,
                        "condition_family": family,
                        "primary_recovery_axis": primary_axis,
                        **asdict(point),
                    }
                )

            for tolerance in sensitivity_tolerances:
                sensitivity_definition = RecoveryDefinition(
                    window_size=definition.window_size,
                    observation_horizon=definition.observation_horizon,
                    tolerance=tolerance,
                    stability_windows=definition.stability_windows,
                    direction=definition.direction,
                )
                sensitivity_result = assess_recovery(
                    nominal_windows=nominal_windows,
                    disturbed_windows=disturbed_windows,
                    definition=sensitivity_definition,
                )
                sensitivity_records.append(
                    {
                        "method_id": method_id,
                        "root_id": root_id,
                        "condition_id": condition_id,
                        "condition_family": family,
                        "primary_recovery_axis": primary_axis,
                        "tolerance": tolerance,
                        "status": sensitivity_result.status,
                        "recovery_time": sensitivity_result.recovery_time,
                        "confirmation_time": sensitivity_result.confirmation_time,
                        "censoring_time": sensitivity_result.censoring_time,
                    }
                )

        method_condition_summaries: list[dict[str, Any]] = []
        for (method_id, condition_id), values in sorted(summary_values.items()):
            recovered_count = int(sum(values["status"]))
            n = len(values["status"])
            method_condition_summaries.append(
                {
                    "method_id": method_id,
                    "condition_id": condition_id,
                    "condition_family": condition_families.get(condition_id, ""),
                    "primary_recovery_axis": (
                        condition_families.get(condition_id) == primary_condition_family
                    ),
                    "included_root_count": n,
                    "recovered_root_count": recovered_count,
                    "right_censored_root_count": n - recovered_count,
                    "recovered_proportion": recovered_count / n if n else None,
                    "recovery_time_conditional_on_recovery": _summary(
                        values["observed_recovery_time"],
                        interval_kind=interval_kind,
                        critical_value=critical_value,
                    ),
                    "restricted_recovery_delay_through_horizon": _summary(
                        values["restricted_delay"],
                        interval_kind=interval_kind,
                        critical_value=critical_value,
                    ),
                }
            )

        contrasts: list[dict[str, Any]] = []
        for (condition_id, estimand), values_by_method in sorted(contrast_values.items()):
            contrasts.extend(
                _contrast_rows(
                    values_by_method,
                    estimand=estimand,
                    condition_id=condition_id,
                    primary_recovery_axis=(
                        condition_families.get(condition_id) == primary_condition_family
                    ),
                    critical_value=critical_value,
                )
            )

        return {
            "metric": "mean-reward-per-actual-environment-interaction",
            "direction": definition.direction.value,
            "window_size": definition.window_size,
            "observation_horizon": definition.observation_horizon,
            "primary_tolerance": float(definition.tolerance),
            "stability_windows": definition.stability_windows,
            "primary_condition_family": primary_condition_family,
            "sensitivity_tolerances": list(sensitivity_tolerances),
            "censoring_policy": "right-censored-at-fixed-horizon; recovery_time-remains-null",
            "restricted_delay_policy": (
                "recovery_time-if-observed-else-fixed-horizon; separate estimand, not recovery_time"
            ),
            "root_records": root_records,
            "trajectory_records": trajectory_records,
            "method_condition_summaries": method_condition_summaries,
            "method_contrasts": contrasts,
            "sensitivity_root_records": sensitivity_records,
        }
