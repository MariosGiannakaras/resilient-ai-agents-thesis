"""Deterministic protocol-v2 evidence handoff tables and result identifiers.

This layer exports data/tables from the analysis package; it does not inspect UI
state or recompute scientific estimands. Version 2 adds predeclared recovery and
direct cross-method comparison tables while preserving the historical v1 handoff.
"""
from __future__ import annotations

import csv
import hashlib
import json
from io import StringIO
from pathlib import Path
from typing import Any, Mapping, Sequence

EXPORT_PACKAGE_SCHEMA_VERSION = 1
EXPORT_PACKAGE_SCHEMA_VERSION_V2 = 2
_SUPPORTED_PACKAGE_V1 = "protocol-v2-evidence-handoff-v1"
_SUPPORTED_PACKAGE_V2 = "protocol-v2-evidence-handoff-v2"


def _mapping(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return dict(value)


def _write_text_atomic(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    data = text.encode("utf-8")
    temporary.write_bytes(data)
    temporary.replace(path)
    return hashlib.sha256(data).hexdigest()


def _write_json_atomic(path: Path, payload: object) -> str:
    return _write_text_atomic(
        path,
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )


def _csv_text(rows: Sequence[Mapping[str, Any]], *, fields: Sequence[str]) -> str:
    handle = StringIO(newline="")
    writer = csv.DictWriter(
        handle,
        fieldnames=list(fields),
        extrasaction="raise",
        lineterminator="\n",
    )
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return handle.getvalue()


def _interval_value(summary: Mapping[str, Any], field: str) -> Any:
    interval = summary.get("interval")
    if not isinstance(interval, Mapping):
        return None
    return interval.get(field)


def _phase_a_summary_rows(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    phase_a = _mapping(package.get("phase_a"), field="analysis.phase_a")
    summaries = phase_a.get("method_summaries")
    if not isinstance(summaries, list):
        raise ValueError("analysis.phase_a.method_summaries must be a list")
    rows: list[dict[str, Any]] = []
    for summary in summaries:
        item = _mapping(summary, field="Phase-A method summary")
        final_value = _mapping(item.get("final_value"), field="Phase-A final summary")
        time_average = _mapping(item.get("time_average"), field="Phase-A time-average summary")
        method_id = str(item["method_id"])
        rows.append(
            {
                "result_id": f"RESULT-PA-{method_id}",
                "method_id": method_id,
                "metric": item["metric"],
                "direction": item["direction"],
                "planned_root_count": item["planned_root_count"],
                "included_root_count": item["included_root_count"],
                "final_n": final_value.get("n"),
                "final_mean": final_value.get("mean"),
                "final_ci_lower": _interval_value(final_value, "lower"),
                "final_ci_upper": _interval_value(final_value, "upper"),
                "time_average_n": time_average.get("n"),
                "time_average_mean": time_average.get("mean"),
                "time_average_ci_lower": _interval_value(time_average, "lower"),
                "time_average_ci_upper": _interval_value(time_average, "upper"),
            }
        )
    return rows


def _phase_b_summary_rows(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    phase_b = _mapping(package.get("phase_b"), field="analysis.phase_b")
    summaries = phase_b.get("method_condition_summaries")
    if not isinstance(summaries, list):
        raise ValueError("analysis.phase_b.method_condition_summaries must be a list")
    rows: list[dict[str, Any]] = []
    for summary in summaries:
        item = _mapping(summary, field="Phase-B method/condition summary")
        frozen = _mapping(item.get("frozen_loss"), field="Phase-B frozen-loss summary")
        adaptive = _mapping(item.get("adaptive_loss"), field="Phase-B adaptive-loss summary")
        benefit = _mapping(item.get("adaptation_benefit"), field="Phase-B benefit summary")
        method_id = str(item["method_id"])
        condition_id = str(item["condition_id"])
        rows.append(
            {
                "result_id": f"RESULT-PB-{method_id}-{condition_id}",
                "method_id": method_id,
                "condition_id": condition_id,
                "metric": item["metric"],
                "direction": item["direction"],
                "planned_root_count": item["planned_root_count"],
                "included_root_count": item["included_root_count"],
                "frozen_loss_n": frozen.get("n"),
                "frozen_loss_mean": frozen.get("mean"),
                "frozen_loss_ci_lower": _interval_value(frozen, "lower"),
                "frozen_loss_ci_upper": _interval_value(frozen, "upper"),
                "adaptive_loss_n": adaptive.get("n"),
                "adaptive_loss_mean": adaptive.get("mean"),
                "adaptive_loss_ci_lower": _interval_value(adaptive, "lower"),
                "adaptive_loss_ci_upper": _interval_value(adaptive, "upper"),
                "adaptation_benefit_n": benefit.get("n"),
                "adaptation_benefit_mean": benefit.get("mean"),
                "adaptation_benefit_ci_lower": _interval_value(benefit, "lower"),
                "adaptation_benefit_ci_upper": _interval_value(benefit, "upper"),
            }
        )
    return rows


def _normalize_rows(rows: Any, *, field: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError(f"{field} must be a list")
    return [_mapping(row, field=field) for row in rows]


def _contrast_rows(rows: Any, *, phase: str) -> list[dict[str, Any]]:
    normalized = _normalize_rows(rows, field=f"analysis.{phase}.method_contrasts")
    result: list[dict[str, Any]] = []
    for item in normalized:
        interval = _mapping(item.get("interval"), field="method contrast interval")
        condition_id = item.get("condition_id")
        result_id = (
            f"RESULT-{phase.upper()}-CONTRAST-{item['estimand']}-"
            f"{item['method_a']}-vs-{item['method_b']}"
        )
        if condition_id is not None:
            result_id += f"-{condition_id}"
        result.append(
            {
                "result_id": result_id,
                "estimand": item["estimand"],
                "condition_id": condition_id,
                "primary_recovery_axis": item.get("primary_recovery_axis"),
                "method_a": item["method_a"],
                "method_b": item["method_b"],
                "difference_orientation": item["difference_orientation"],
                "root_ids": item["root_ids"],
                "differences": item["differences"],
                "n": interval.get("n"),
                "mean_difference": interval.get("mean"),
                "ci_lower": interval.get("lower"),
                "ci_upper": interval.get("upper"),
            }
        )
    return result


def _recovery_summary_rows(recovery: Mapping[str, Any]) -> list[dict[str, Any]]:
    summaries = _normalize_rows(
        recovery.get("method_condition_summaries"),
        field="analysis.phase_b.recovery.method_condition_summaries",
    )
    rows: list[dict[str, Any]] = []
    for item in summaries:
        conditional = _mapping(
            item.get("recovery_time_conditional_on_recovery"),
            field="recovery conditional-time summary",
        )
        restricted = _mapping(
            item.get("restricted_recovery_delay_through_horizon"),
            field="recovery restricted-delay summary",
        )
        rows.append(
            {
                "result_id": (
                    f"RESULT-RQ3-{item['method_id']}-{item['condition_id']}"
                ),
                "method_id": item["method_id"],
                "condition_id": item["condition_id"],
                "condition_family": item["condition_family"],
                "primary_recovery_axis": item["primary_recovery_axis"],
                "included_root_count": item["included_root_count"],
                "recovered_root_count": item["recovered_root_count"],
                "right_censored_root_count": item["right_censored_root_count"],
                "recovered_proportion": item["recovered_proportion"],
                "conditional_recovery_time_n": conditional.get("n"),
                "conditional_recovery_time_mean": conditional.get("mean"),
                "conditional_recovery_time_ci_lower": _interval_value(conditional, "lower"),
                "conditional_recovery_time_ci_upper": _interval_value(conditional, "upper"),
                "restricted_delay_n": restricted.get("n"),
                "restricted_delay_mean": restricted.get("mean"),
                "restricted_delay_ci_lower": _interval_value(restricted, "lower"),
                "restricted_delay_ci_upper": _interval_value(restricted, "upper"),
            }
        )
    return rows


def _normalize_csv_values(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    normalized_rows: list[dict[str, Any]] = []
    for row in rows:
        normalized = dict(row)
        for key, value in tuple(normalized.items()):
            if isinstance(value, list):
                normalized[key] = json.dumps(
                    value,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            elif value is None:
                normalized[key] = ""
        normalized_rows.append(normalized)
    return normalized_rows


class StudyExportEngine:
    """Write one deterministic data/table handoff from an analysis package."""

    def export(
        self,
        *,
        analysis_package: Mapping[str, Any],
        specification: Mapping[str, Any],
        output_dir: Path,
        source_analysis_artifact_id: str,
        source_analysis_sha256: str,
    ) -> dict[str, Any]:
        package = _mapping(analysis_package, field="analysis package")
        spec = _mapping(specification, field="export specification")
        if set(spec) != {"package", "emit_csv"}:
            raise ValueError("export specification requires exactly package and emit_csv")
        package_id = spec["package"]
        if package_id not in {_SUPPORTED_PACKAGE_V1, _SUPPORTED_PACKAGE_V2}:
            raise ValueError("unsupported protocol-v2 export package")
        if spec["emit_csv"] is not True:
            raise ValueError("protocol-v2 evidence handoff requires emit_csv=true")
        if not isinstance(source_analysis_artifact_id, str) or not source_analysis_artifact_id:
            raise ValueError("source_analysis_artifact_id must be explicit")
        if not isinstance(source_analysis_sha256, str) or len(source_analysis_sha256) != 64:
            raise ValueError("source_analysis_sha256 must be a SHA-256 digest")
        version2 = package_id == _SUPPORTED_PACKAGE_V2
        if version2:
            if package.get("schema_version") != 2:
                raise ValueError("evidence handoff v2 requires analysis package schema_version=2")
            if package.get("analysis_recipe") != "protocol-v2-root-level-v2":
                raise ValueError("evidence handoff v2 requires root-level-v2 analysis")

        output_dir.mkdir(parents=True, exist_ok=True)
        files: list[dict[str, Any]] = []

        phase_a = _mapping(package["phase_a"], field="analysis.phase_a")
        phase_b = _mapping(package["phase_b"], field="analysis.phase_b")
        phase_a_summary = _phase_a_summary_rows(package)
        phase_b_summary = _phase_b_summary_rows(package)
        phase_a_root = _normalize_rows(
            phase_a.get("root_records"),
            field="analysis.phase_a.root_records",
        )
        phase_b_root = _normalize_rows(
            phase_b.get("root_records"),
            field="analysis.phase_b.root_records",
        )

        csv_specs: list[tuple[str, list[dict[str, Any]], tuple[str, ...], str]] = [
            (
                "phase-a-method-summary.csv",
                phase_a_summary,
                (
                    "result_id", "method_id", "metric", "direction",
                    "planned_root_count", "included_root_count", "final_n",
                    "final_mean", "final_ci_lower", "final_ci_upper",
                    "time_average_n", "time_average_mean", "time_average_ci_lower",
                    "time_average_ci_upper",
                ),
                "thesis-table-phase-a-method-summary",
            ),
            (
                "phase-b-method-condition-summary.csv",
                phase_b_summary,
                (
                    "result_id", "method_id", "condition_id", "metric", "direction",
                    "planned_root_count", "included_root_count", "frozen_loss_n",
                    "frozen_loss_mean", "frozen_loss_ci_lower", "frozen_loss_ci_upper",
                    "adaptive_loss_n", "adaptive_loss_mean", "adaptive_loss_ci_lower",
                    "adaptive_loss_ci_upper", "adaptation_benefit_n",
                    "adaptation_benefit_mean", "adaptation_benefit_ci_lower",
                    "adaptation_benefit_ci_upper",
                ),
                "thesis-table-phase-b-method-condition-summary",
            ),
            (
                "phase-a-root-records.csv",
                phase_a_root,
                (
                    "method_id", "root_id", "planned_layout_count",
                    "observed_layout_count", "missing_layout_ids",
                    "complete_layout_block", "included_in_primary_summary",
                    "final_value", "time_average",
                ),
                "analysis-table-phase-a-root-records",
            ),
            (
                "phase-b-root-records.csv",
                phase_b_root,
                (
                    "method_id", "root_id", "condition_id", "planned_layout_count",
                    "observed_layout_count", "missing_layout_ids",
                    "complete_layout_block", "included_in_primary_summary",
                    "frozen_loss", "adaptive_loss", "adaptation_benefit",
                ),
                "analysis-table-phase-b-root-records",
            ),
        ]

        contrast_result_rows: list[dict[str, Any]] = []
        recovery_summary: list[dict[str, Any]] = []
        if version2:
            phase_a_contrasts = _contrast_rows(
                phase_a.get("method_contrasts"),
                phase="pa",
            )
            phase_b_contrasts = _contrast_rows(
                phase_b.get("method_contrasts"),
                phase="pb",
            )
            recovery = _mapping(phase_b.get("recovery"), field="analysis.phase_b.recovery")
            recovery_root = _normalize_rows(
                recovery.get("root_records"),
                field="analysis.phase_b.recovery.root_records",
            )
            recovery_trajectory = _normalize_rows(
                recovery.get("trajectory_records"),
                field="analysis.phase_b.recovery.trajectory_records",
            )
            recovery_summary = _recovery_summary_rows(recovery)
            recovery_contrasts = _contrast_rows(
                recovery.get("method_contrasts"),
                phase="rq3",
            )
            recovery_sensitivity = _normalize_rows(
                recovery.get("sensitivity_root_records"),
                field="analysis.phase_b.recovery.sensitivity_root_records",
            )
            contrast_fields = (
                "result_id", "estimand", "condition_id", "primary_recovery_axis",
                "method_a", "method_b", "difference_orientation", "root_ids",
                "differences", "n", "mean_difference", "ci_lower", "ci_upper",
            )
            csv_specs.extend(
                [
                    (
                        "phase-a-method-contrasts.csv",
                        phase_a_contrasts,
                        contrast_fields,
                        "thesis-table-phase-a-method-contrasts",
                    ),
                    (
                        "phase-b-method-contrasts.csv",
                        phase_b_contrasts,
                        contrast_fields,
                        "thesis-table-phase-b-method-contrasts",
                    ),
                    (
                        "recovery-root-records.csv",
                        recovery_root,
                        (
                            "method_id", "root_id", "condition_id", "condition_family",
                            "primary_recovery_axis", "planned_layout_count",
                            "observed_layout_count", "missing_layout_ids",
                            "complete_layout_block", "included_in_recovery_summary",
                            "status", "recovery_time", "confirmation_time",
                            "censoring_time", "restricted_recovery_delay_through_horizon",
                        ),
                        "analysis-table-recovery-root-records",
                    ),
                    (
                        "recovery-trajectory-records.csv",
                        recovery_trajectory,
                        (
                            "method_id", "root_id", "condition_id", "condition_family",
                            "primary_recovery_axis", "window_index", "window_start",
                            "window_end", "nominal_value", "disturbed_value",
                            "directed_gap", "within_tolerance",
                        ),
                        "analysis-table-recovery-trajectories",
                    ),
                    (
                        "recovery-method-condition-summary.csv",
                        recovery_summary,
                        (
                            "result_id", "method_id", "condition_id", "condition_family",
                            "primary_recovery_axis", "included_root_count",
                            "recovered_root_count", "right_censored_root_count",
                            "recovered_proportion", "conditional_recovery_time_n",
                            "conditional_recovery_time_mean", "conditional_recovery_time_ci_lower",
                            "conditional_recovery_time_ci_upper", "restricted_delay_n",
                            "restricted_delay_mean", "restricted_delay_ci_lower",
                            "restricted_delay_ci_upper",
                        ),
                        "thesis-table-recovery-method-condition-summary",
                    ),
                    (
                        "recovery-method-contrasts.csv",
                        recovery_contrasts,
                        contrast_fields,
                        "thesis-table-recovery-method-contrasts",
                    ),
                    (
                        "recovery-sensitivity-root-records.csv",
                        recovery_sensitivity,
                        (
                            "method_id", "root_id", "condition_id", "condition_family",
                            "primary_recovery_axis", "tolerance", "status",
                            "recovery_time", "confirmation_time", "censoring_time",
                        ),
                        "analysis-table-recovery-sensitivity",
                    ),
                ]
            )
            contrast_result_rows = phase_a_contrasts + phase_b_contrasts + recovery_contrasts

        for filename, rows, fields, artifact_id in csv_specs:
            path = output_dir / filename
            digest = _write_text_atomic(
                path,
                _csv_text(_normalize_csv_values(rows), fields=fields),
            )
            files.append(
                {
                    "artifact_id": artifact_id,
                    "filename": filename,
                    "sha256": digest,
                    "row_count": len(rows),
                }
            )

        result_index = [
            {
                "result_id": row["result_id"],
                "phase": "phase-a",
                "method_id": row["method_id"],
            }
            for row in phase_a_summary
        ] + [
            {
                "result_id": row["result_id"],
                "phase": "phase-b",
                "method_id": row["method_id"],
                "condition_id": row["condition_id"],
            }
            for row in phase_b_summary
        ]
        if version2:
            result_index.extend(
                {
                    "result_id": row["result_id"],
                    "phase": "recovery",
                    "method_id": row["method_id"],
                    "condition_id": row["condition_id"],
                }
                for row in recovery_summary
            )
            result_index.extend(
                {
                    "result_id": row["result_id"],
                    "phase": "method-contrast",
                    "method_a": row["method_a"],
                    "method_b": row["method_b"],
                    "condition_id": row.get("condition_id"),
                    "estimand": row["estimand"],
                }
                for row in contrast_result_rows
            )
        result_index.sort(key=lambda row: row["result_id"])
        result_index_path = output_dir / "result-index.json"
        export_schema = (
            EXPORT_PACKAGE_SCHEMA_VERSION_V2 if version2 else EXPORT_PACKAGE_SCHEMA_VERSION
        )
        result_index_sha = _write_json_atomic(
            result_index_path,
            {
                "schema_version": export_schema,
                "study_id": package["study_id"],
                "recipe_sha256": package["recipe_sha256"],
                "results": result_index,
            },
        )
        files.append(
            {
                "artifact_id": "result-index",
                "filename": "result-index.json",
                "sha256": result_index_sha,
                "row_count": len(result_index),
            }
        )

        manifest = {
            "schema_version": export_schema,
            "package": package_id,
            "study_id": package["study_id"],
            "recipe_sha256": package["recipe_sha256"],
            "analysis_recipe": package["analysis_recipe"],
            "source_analysis_artifact_id": source_analysis_artifact_id,
            "source_analysis_sha256": source_analysis_sha256,
            "figure_rendering_status": "deferred-until-frozen-figure-recipe",
            "files": sorted(files, key=lambda item: item["artifact_id"]),
        }
        manifest_path = output_dir / "evidence-handoff-manifest.json"
        manifest_sha = _write_json_atomic(manifest_path, manifest)
        return {
            "manifest": manifest,
            "manifest_path": manifest_path,
            "manifest_sha256": manifest_sha,
            "files": tuple(files),
        }
