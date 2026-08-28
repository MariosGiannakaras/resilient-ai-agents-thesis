"""Deterministic protocol-v2 evidence handoff tables and result identifiers.

This layer deliberately exports data/tables from the frozen analysis package;
it does not inspect UI state and does not choose a thesis figure design.  Final
figure/table selection remains a frozen recipe decision after T-527/T-612.
"""
from __future__ import annotations

import csv
import hashlib
import json
from io import StringIO
from pathlib import Path
from typing import Any, Mapping, Sequence

EXPORT_PACKAGE_SCHEMA_VERSION = 1
_SUPPORTED_PACKAGE = "protocol-v2-evidence-handoff-v1"


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
    writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="raise", lineterminator="\n")
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


def _normalize_root_rows(rows: Any, *, field: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError(f"{field} must be a list")
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized.append(_mapping(row, field=field))
    return normalized


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
        if spec["package"] != _SUPPORTED_PACKAGE:
            raise ValueError("unsupported protocol-v2 export package")
        if spec["emit_csv"] is not True:
            raise ValueError("protocol-v2 evidence handoff v1 requires emit_csv=true")
        if not isinstance(source_analysis_artifact_id, str) or not source_analysis_artifact_id:
            raise ValueError("source_analysis_artifact_id must be explicit")
        if not isinstance(source_analysis_sha256, str) or len(source_analysis_sha256) != 64:
            raise ValueError("source_analysis_sha256 must be a SHA-256 digest")

        output_dir.mkdir(parents=True, exist_ok=True)
        files: list[dict[str, Any]] = []

        phase_a_summary = _phase_a_summary_rows(package)
        phase_b_summary = _phase_b_summary_rows(package)
        phase_a_root = _normalize_root_rows(
            _mapping(package["phase_a"], field="analysis.phase_a").get("root_records"),
            field="analysis.phase_a.root_records",
        )
        phase_b_root = _normalize_root_rows(
            _mapping(package["phase_b"], field="analysis.phase_b").get("root_records"),
            field="analysis.phase_b.root_records",
        )

        csv_specs = (
            (
                "phase-a-method-summary.csv",
                phase_a_summary,
                (
                    "result_id",
                    "method_id",
                    "metric",
                    "direction",
                    "planned_root_count",
                    "included_root_count",
                    "final_n",
                    "final_mean",
                    "final_ci_lower",
                    "final_ci_upper",
                    "time_average_n",
                    "time_average_mean",
                    "time_average_ci_lower",
                    "time_average_ci_upper",
                ),
                "thesis-table-phase-a-method-summary",
            ),
            (
                "phase-b-method-condition-summary.csv",
                phase_b_summary,
                (
                    "result_id",
                    "method_id",
                    "condition_id",
                    "metric",
                    "direction",
                    "planned_root_count",
                    "included_root_count",
                    "frozen_loss_n",
                    "frozen_loss_mean",
                    "frozen_loss_ci_lower",
                    "frozen_loss_ci_upper",
                    "adaptive_loss_n",
                    "adaptive_loss_mean",
                    "adaptive_loss_ci_lower",
                    "adaptive_loss_ci_upper",
                    "adaptation_benefit_n",
                    "adaptation_benefit_mean",
                    "adaptation_benefit_ci_lower",
                    "adaptation_benefit_ci_upper",
                ),
                "thesis-table-phase-b-method-condition-summary",
            ),
            (
                "phase-a-root-records.csv",
                phase_a_root,
                (
                    "method_id",
                    "root_id",
                    "planned_layout_count",
                    "observed_layout_count",
                    "missing_layout_ids",
                    "complete_layout_block",
                    "included_in_primary_summary",
                    "final_value",
                    "time_average",
                ),
                "analysis-table-phase-a-root-records",
            ),
            (
                "phase-b-root-records.csv",
                phase_b_root,
                (
                    "method_id",
                    "root_id",
                    "condition_id",
                    "planned_layout_count",
                    "observed_layout_count",
                    "missing_layout_ids",
                    "complete_layout_block",
                    "included_in_primary_summary",
                    "frozen_loss",
                    "adaptive_loss",
                    "adaptation_benefit",
                ),
                "analysis-table-phase-b-root-records",
            ),
        )

        for filename, rows, fields, artifact_id in csv_specs:
            normalized_rows = []
            for row in rows:
                normalized = dict(row)
                for key, value in tuple(normalized.items()):
                    if isinstance(value, list):
                        normalized[key] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                    elif value is None:
                        normalized[key] = ""
                normalized_rows.append(normalized)
            path = output_dir / filename
            digest = _write_text_atomic(path, _csv_text(normalized_rows, fields=fields))
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
        result_index.sort(key=lambda row: row["result_id"])
        result_index_path = output_dir / "result-index.json"
        result_index_sha = _write_json_atomic(
            result_index_path,
            {
                "schema_version": EXPORT_PACKAGE_SCHEMA_VERSION,
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
            "schema_version": EXPORT_PACKAGE_SCHEMA_VERSION,
            "package": _SUPPORTED_PACKAGE,
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
