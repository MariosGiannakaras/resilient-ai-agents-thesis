"""Finalize and verify the predeclared T-612 protocol-v2.1 analysis package.

This module does not define statistical estimands.  It reruns the frozen
``StudyAnalysisEngineV21`` and ``StudyExportEngineV21`` contracts against the
T-611 accepted Study, verifies byte identity with the mechanical T-610
artifacts, and writes a small immutable T-612 provenance envelope.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ..run_bundle import sha256_file
from ..study import StudyStore
from .analysis_v21 import (
    V21_ANALYSIS_RECIPE,
    V21_STUDENT_T_95_CRITICAL_BY_N,
    StudyAnalysisEngineV21,
)
from .denominators import build_scientific_denominators
from .executors import _write_json_atomic
from .exports_v21 import StudyExportEngineV21
from .freeze import (
    ACCEPTED_EXECUTION_ID,
    EXPECTED_EXECUTION_SOURCE_COMMIT,
    EXPECTED_PLAN_SHA256,
    EXPECTED_RECIPE_SHA256,
    validate_protocol_v21_final_freeze,
)
from .validation import StudyEvidenceValidator

T612_PACKAGE_SCHEMA_VERSION = 1
T612_RELATIVE_DIR = Path("results/analysis/protocol-v2.1-final")
EXPECTED_FREEZE_MANIFEST_SHA256 = (
    "20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858"
)
EXPECTED_RUN_INVENTORY_SHA256 = (
    "0c2b352b88045951d32e58ee3479656dce00e35d55899bcdea65dc07604d8045"
)
REPORT_RELATIVE_PATH = Path("docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md")
TOOL_SOURCE_FILES = (
    "scripts/analyze_protocol_v21_final.py",
    "src/resilient_agents/evidence_v2/final_analysis.py",
    "src/resilient_agents/evidence_v2/analysis.py",
    "src/resilient_agents/evidence_v2/analysis_v21.py",
    "src/resilient_agents/evidence_v2/recovery.py",
    "src/resilient_agents/evidence_v2/statistics.py",
    "src/resilient_agents/evidence_v2/denominators.py",
    "src/resilient_agents/evidence_v2/exports.py",
    "src/resilient_agents/evidence_v2/exports_v21.py",
)


def _canonical_json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(repo_root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=False,
        capture_output=True,
        timeout=120,
    )
    if result.returncode:
        raise RuntimeError(
            result.stderr.decode("utf-8", errors="replace").strip()
            or "git command failed"
        )
    return result.stdout


def _analysis_and_export_specs(
    store: StudyStore,
) -> tuple[dict[str, Any], dict[str, Any]]:
    analysis_jobs = [
        job
        for job in store.plan.jobs
        if job.payload.get("job_type") == "study-analysis"
    ]
    export_jobs = [
        job for job in store.plan.jobs if job.payload.get("job_type") == "study-export"
    ]
    if len(analysis_jobs) != 1 or len(export_jobs) != 1:
        raise RuntimeError(
            "accepted Study must contain one analysis and one export job"
        )
    analysis_spec = analysis_jobs[0].payload.get("specification")
    export_spec = export_jobs[0].payload.get("specification")
    if not isinstance(analysis_spec, Mapping) or not isinstance(export_spec, Mapping):
        raise TypeError("accepted Study analysis/export specifications must be objects")
    return dict(analysis_spec), dict(export_spec)


def _recompute(
    store: StudyStore, output_dir: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    analysis_spec, export_spec = _analysis_and_export_specs(store)
    package = StudyAnalysisEngineV21().analyze(store, specification=analysis_spec)
    package["scientific_denominators"] = build_scientific_denominators(store)
    analysis_path = output_dir / "analysis-package.json"
    analysis_sha256 = _write_json_atomic(analysis_path, package)
    exported = StudyExportEngineV21().export(
        analysis_package=package,
        specification=export_spec,
        output_dir=output_dir / "export",
        source_analysis_artifact_id="analysis-package",
        source_analysis_sha256=analysis_sha256,
    )
    return package, exported


def _summary_interval(summary: Mapping[str, Any]) -> Mapping[str, Any] | None:
    interval = summary.get("interval")
    return interval if isinstance(interval, Mapping) else None


def _all_scalar_summaries(package: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    summaries: list[Mapping[str, Any]] = []
    phase_a = package["phase_a"]
    for row in phase_a["method_summaries"]:
        summaries.extend((row["final_value"], row["time_average"]))
    phase_b = package["phase_b"]
    for row in phase_b["method_condition_summaries"]:
        summaries.extend(
            (row["frozen_loss"], row["adaptive_loss"], row["adaptation_benefit"])
        )
    recovery = phase_b["recovery"]
    for row in recovery["method_condition_summaries"]:
        summaries.extend(
            (
                row["recovery_time_conditional_on_recovery"],
                row["restricted_recovery_delay_through_horizon"],
            )
        )
    return summaries


def _validate_interval_policy(package: Mapping[str, Any]) -> None:
    policy = package.get("interval_policy")
    if policy != {
        "kind": "student-t",
        "confidence": 0.95,
        "independent_unit": "root",
        "critical_value_selected_by": "actual-independent-root-count",
        "critical_value_by_n": {
            str(n): value for n, value in V21_STUDENT_T_95_CRITICAL_BY_N.items()
        },
        "pointwise_not_simultaneous": True,
        "p_value_superiority_family": False,
    }:
        raise RuntimeError("analysis interval policy differs from DEC-060")
    contrasts = [
        *package["phase_a"]["method_contrasts"],
        *package["phase_b"]["method_contrasts"],
        *package["phase_b"]["recovery"]["method_contrasts"],
    ]
    for summary in [*_all_scalar_summaries(package), *contrasts]:
        interval = (
            _summary_interval(summary) if "mean" in summary else summary.get("interval")
        )
        if interval is None:
            if int(summary["n"]) >= 2:
                raise RuntimeError(
                    "eligible scalar summary is missing its Student-t interval"
                )
            continue
        n = int(interval["n"])
        if interval["critical_value"] != V21_STUDENT_T_95_CRITICAL_BY_N[n]:
            raise RuntimeError(
                "Student-t interval did not use actual independent-root n"
            )


def _validate_analysis_invariants(package: Mapping[str, Any]) -> dict[str, Any]:
    if (
        package.get("schema_version") != 2
        or package.get("study_id") != ACCEPTED_EXECUTION_ID
        or package.get("recipe_sha256") != EXPECTED_RECIPE_SHA256
        or package.get("analysis_recipe") != V21_ANALYSIS_RECIPE
    ):
        raise RuntimeError(
            "regenerated analysis identity differs from frozen authority"
        )
    specification = package.get("specification")
    expected_recovery = {
        "observation_horizon": 256,
        "primary_condition_family": "action-remap",
        "sensitivity_tolerances": [0.05, 0.2],
        "stability_windows": 2,
        "tolerance": 0.1,
        "window_size": 32,
    }
    if (
        not isinstance(specification, Mapping)
        or specification.get("recovery") != expected_recovery
    ):
        raise RuntimeError("regenerated recovery specification differs from DEC-060")
    if (
        specification.get("layout_aggregation") != "equal-weight"
        or specification.get("require_complete_layout_blocks") is not True
    ):
        raise RuntimeError("root/layout reduction differs from the frozen contract")

    phase_a = package["phase_a"]
    phase_b = package["phase_b"]
    recovery = phase_b["recovery"]
    expected_counts = {
        "rq1_method_summaries": 5,
        "rq1_root_records": 60,
        "rq1_direct_contrasts": 20,
        "rq2_method_condition_summaries": 20,
        "rq2_root_records": 240,
        "rq2_direct_contrasts": 120,
        "rq3_method_condition_summaries": 20,
        "rq3_root_records": 240,
        "rq3_trajectory_records": 1920,
        "rq3_sensitivity_root_records": 480,
        "rq3_direct_contrasts": 80,
    }
    actual_counts = {
        "rq1_method_summaries": len(phase_a["method_summaries"]),
        "rq1_root_records": len(phase_a["root_records"]),
        "rq1_direct_contrasts": len(phase_a["method_contrasts"]),
        "rq2_method_condition_summaries": len(phase_b["method_condition_summaries"]),
        "rq2_root_records": len(phase_b["root_records"]),
        "rq2_direct_contrasts": len(phase_b["method_contrasts"]),
        "rq3_method_condition_summaries": len(recovery["method_condition_summaries"]),
        "rq3_root_records": len(recovery["root_records"]),
        "rq3_trajectory_records": len(recovery["trajectory_records"]),
        "rq3_sensitivity_root_records": len(recovery["sensitivity_root_records"]),
        "rq3_direct_contrasts": len(recovery["method_contrasts"]),
    }
    if actual_counts != expected_counts:
        raise RuntimeError(f"analysis coverage mismatch: {actual_counts!r}")
    if any(not row["complete_layout_block"] for row in phase_a["root_records"]):
        raise RuntimeError("RQ1 contains an incomplete root/layout block")
    if any(not row["complete_layout_block"] for row in phase_b["root_records"]):
        raise RuntimeError("RQ2 contains an incomplete root/layout block")
    if any(not row["complete_layout_block"] for row in recovery["root_records"]):
        raise RuntimeError("RQ3 contains an incomplete root/layout block")
    if any(row["interval"]["n"] != 12 for row in phase_a["method_contrasts"]):
        raise RuntimeError("RQ1 direct contrast does not contain twelve paired roots")
    if any(row["interval"]["n"] != 12 for row in phase_b["method_contrasts"]):
        raise RuntimeError("RQ2 direct contrast does not contain twelve paired roots")
    if any(row["interval"]["n"] != 12 for row in recovery["method_contrasts"]):
        raise RuntimeError("RQ3 direct contrast does not contain twelve paired roots")

    censored = [
        row for row in recovery["root_records"] if row["status"] == "right-censored"
    ]
    if any(
        row["recovery_time"] is not None
        or row["censoring_time"] != 256
        or row["restricted_recovery_delay_through_horizon"] != 256
        for row in censored
    ):
        raise RuntimeError("right-censored recovery semantics were not preserved")
    sensitivity_tolerances = sorted(
        {float(row["tolerance"]) for row in recovery["sensitivity_root_records"]}
    )
    if sensitivity_tolerances != [0.05, 0.2]:
        raise RuntimeError("RQ3 sensitivity tolerance family differs from DEC-060")
    _validate_interval_policy(package)
    return {
        **actual_counts,
        "right_censored_primary_records": sum(
            row["status"] == "right-censored" and row["primary_recovery_axis"]
            for row in recovery["root_records"]
        ),
    }


def _sensitivity_diagnostics(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    recovery = package["phase_b"]["recovery"]
    rows: list[dict[str, Any]] = []
    primary_records = [
        {**row, "tolerance": 0.1}
        for row in recovery["root_records"]
        if row["primary_recovery_axis"]
    ]
    sensitivity_records = [
        row
        for row in recovery["sensitivity_root_records"]
        if row["primary_recovery_axis"]
    ]
    keys = sorted(
        {
            (row["method_id"], row["condition_id"], float(row["tolerance"]))
            for row in [*primary_records, *sensitivity_records]
        }
    )
    all_records = [*primary_records, *sensitivity_records]
    for method_id, condition_id, tolerance in keys:
        selected = [
            row
            for row in all_records
            if row["method_id"] == method_id
            and row["condition_id"] == condition_id
            and float(row["tolerance"]) == tolerance
        ]
        recovered = sum(row["status"] == "recovered" for row in selected)
        rows.append(
            {
                "method_id": method_id,
                "condition_id": condition_id,
                "tolerance": tolerance,
                "root_count": len(selected),
                "recovered_root_count": recovered,
                "right_censored_root_count": len(selected) - recovered,
                "recovered_proportion": recovered / len(selected),
            }
        )
    if len(rows) != 30 or any(row["root_count"] != 12 for row in rows):
        raise RuntimeError("RQ3 sensitivity diagnostic coverage is incomplete")
    return rows


def _file_inventory(directory: Path) -> list[dict[str, Any]]:
    return [
        {
            "relative_path": path.relative_to(directory).as_posix(),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        }
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    ]


def _compare_regeneration(
    repo_root: Path,
    first_dir: Path,
    second_dir: Path,
) -> list[dict[str, Any]]:
    stored_dir = repo_root / "results/studies" / ACCEPTED_EXECUTION_ID / "derived"
    pairs = [
        (
            first_dir / "analysis-package.json",
            stored_dir / "analysis/analysis-package.json",
        )
    ] + [
        (path, stored_dir / "export" / path.name)
        for path in sorted((first_dir / "export").iterdir())
    ]
    records: list[dict[str, Any]] = []
    for generated, stored in pairs:
        relative = (
            "analysis/analysis-package.json"
            if generated.name == "analysis-package.json"
            else f"export/{generated.name}"
        )
        second = (
            second_dir / "analysis-package.json"
            if generated.name == "analysis-package.json"
            else second_dir / "export" / generated.name
        )
        generated_bytes = generated.read_bytes()
        if generated_bytes != second.read_bytes():
            raise RuntimeError(f"repeated regeneration disagrees: {relative}")
        if generated_bytes != stored.read_bytes():
            raise RuntimeError(
                f"regeneration disagrees with T-610 artifact: {relative}"
            )
        records.append(
            {
                "relative_path": (
                    Path("results/studies")
                    / ACCEPTED_EXECUTION_ID
                    / "derived"
                    / relative
                ).as_posix(),
                "sha256": _sha256_bytes(generated_bytes),
                "size_bytes": len(generated_bytes),
                "repeated_regeneration_identical": True,
                "t610_mechanical_artifact_identical": True,
            }
        )
    return records


def _write_package_atomic(
    output_dir: Path,
    *,
    manifest: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
) -> str:
    if output_dir.exists():
        raise RuntimeError("T-612 analysis package already exists; refusing overwrite")
    staging = output_dir.with_name(output_dir.name + ".staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    (staging / "diagnostics.json").write_bytes(_canonical_json_bytes(diagnostics))
    manifest_bytes = _canonical_json_bytes(manifest)
    (staging / "analysis-manifest.json").write_bytes(manifest_bytes)
    manifest_sha256 = _sha256_bytes(manifest_bytes)
    (staging / "FINALIZED").write_text(
        f"schema_version={T612_PACKAGE_SCHEMA_VERSION}\n"
        "status=finalized\n"
        f"manifest_sha256={manifest_sha256}\n",
        encoding="utf-8",
        newline="\n",
    )
    staging.replace(output_dir)
    return manifest_sha256


def finalize_protocol_v21_t612(
    repo_root: Path,
    *,
    analysis_source_git_commit: str,
) -> dict[str, Any]:
    """Regenerate, diagnose, provenance-link and atomically finalize T-612."""

    repo_root = Path(repo_root).resolve()
    if not re.fullmatch(r"[0-9a-f]{40}", analysis_source_git_commit):
        raise ValueError("analysis_source_git_commit must be a full lowercase Git SHA")
    if (
        _git(repo_root, "rev-parse", "HEAD").decode().strip()
        != analysis_source_git_commit
    ):
        raise RuntimeError("analysis source commit must equal checked-out HEAD")
    if _git(repo_root, "status", "--porcelain", "--untracked-files=all").strip():
        raise RuntimeError("working tree must be clean before T-612 finalization")
    freeze = validate_protocol_v21_final_freeze(repo_root)
    if freeze != {
        "valid": True,
        "freeze_manifest_sha256": EXPECTED_FREEZE_MANIFEST_SHA256,
        "run_manifest_inventory_sha256": EXPECTED_RUN_INVENTORY_SHA256,
        "run_bundle_count": 600,
    }:
        raise RuntimeError("T-611 freeze identity differs from accepted authority")

    store = StudyStore.load(
        repo_root=repo_root,
        writable_root=repo_root,
        study_id=ACCEPTED_EXECUTION_ID,
    )
    validation = StudyEvidenceValidator().validate(store)
    if not validation.valid or not validation.ready_for_analysis or validation.findings:
        raise RuntimeError("fresh T-611 evidence validation did not pass")

    report_path = repo_root / REPORT_RELATIVE_PATH
    if not report_path.is_file():
        raise RuntimeError("T-612 scientific interpretation report is missing")
    tool_sources: list[dict[str, Any]] = []
    for relative_path in TOOL_SOURCE_FILES:
        working_bytes = (repo_root / relative_path).read_bytes()
        committed_bytes = _git(
            repo_root, "show", f"{analysis_source_git_commit}:{relative_path}"
        )
        if working_bytes != committed_bytes:
            raise RuntimeError(
                f"analysis tool differs from source commit: {relative_path}"
            )
        tool_sources.append(
            {"relative_path": relative_path, "sha256": _sha256_bytes(working_bytes)}
        )

    with (
        tempfile.TemporaryDirectory() as first_name,
        tempfile.TemporaryDirectory() as second_name,
    ):
        first_dir, second_dir = Path(first_name), Path(second_name)
        package, _ = _recompute(store, first_dir)
        second_package, _ = _recompute(store, second_dir)
        if _canonical_json_bytes(package) != _canonical_json_bytes(second_package):
            raise RuntimeError("repeated in-memory analysis regeneration disagrees")
        coverage = _validate_analysis_invariants(package)
        regenerated_files = _compare_regeneration(repo_root, first_dir, second_dir)
        sensitivity = _sensitivity_diagnostics(package)

    # Confirm the read-only analysis did not alter the accepted freeze envelope.
    if validate_protocol_v21_final_freeze(repo_root) != freeze:
        raise RuntimeError("T-611 freeze changed during analysis")

    diagnostics = {
        "schema_version": T612_PACKAGE_SCHEMA_VERSION,
        "task_id": "T-612",
        "analysis_recipe": V21_ANALYSIS_RECIPE,
        "coverage": coverage,
        "recovery_sensitivity_primary_action_remap": sensitivity,
        "interval_rule": "two-sided-95-percent-Student-t-by-actual-root-count",
        "right_censoring_valid": True,
        "complete_root_layout_blocks": True,
        "historical_failed_attempt_used": False,
    }
    diagnostics_bytes = _canonical_json_bytes(diagnostics)
    manifest = {
        "schema_version": T612_PACKAGE_SCHEMA_VERSION,
        "status": "finalized",
        "task_id": "T-612",
        "scientific_recipe_id": "protocol-v2.1-final",
        "accepted_execution_instance_id": ACCEPTED_EXECUTION_ID,
        "execution_source_git_commit": EXPECTED_EXECUTION_SOURCE_COMMIT,
        "recipe_sha256": EXPECTED_RECIPE_SHA256,
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "t611_freeze_manifest_sha256": EXPECTED_FREEZE_MANIFEST_SHA256,
        "t611_run_manifest_inventory_sha256": EXPECTED_RUN_INVENTORY_SHA256,
        "analysis_source_git_commit": analysis_source_git_commit,
        "analysis_recipe": V21_ANALYSIS_RECIPE,
        "analysis_tool_source_files": tool_sources,
        "canonical_analysis_artifacts": regenerated_files,
        "deterministic_regeneration_count": 2,
        "all_regenerations_byte_identical": True,
        "t610_mechanical_artifacts_byte_identical": True,
        "diagnostics": {
            "relative_path": (T612_RELATIVE_DIR / "diagnostics.json").as_posix(),
            "sha256": _sha256_bytes(diagnostics_bytes),
        },
        "scientific_interpretation_report": {
            "relative_path": REPORT_RELATIVE_PATH.as_posix(),
            "sha256": sha256_file(report_path),
        },
        "rq_coverage": ["RQ1", "RQ2", "RQ3"],
        "recovery_tolerances": [0.05, 0.1, 0.2],
        "historical_failed_attempt": {
            "study_id": "protocol-v2.1-final",
            "completed_jobs": 216,
            "eligible": False,
            "used_as_scientific_input": False,
        },
        "frozen_evidence_mutated": False,
        "t613_or_wp7_work_performed": False,
    }
    output_dir = repo_root / T612_RELATIVE_DIR
    manifest_sha256 = _write_package_atomic(
        output_dir,
        manifest=manifest,
        diagnostics=diagnostics,
    )
    return {
        "valid": True,
        "analysis_directory": T612_RELATIVE_DIR.as_posix(),
        "analysis_manifest_sha256": manifest_sha256,
        "canonical_analysis_artifact_count": len(regenerated_files),
        "rq_coverage": manifest["rq_coverage"],
        "recovery_tolerances": manifest["recovery_tolerances"],
    }


def verify_protocol_v21_t612(repo_root: Path) -> dict[str, Any]:
    """Verify the finalized T-612 envelope and all referenced immutable inputs."""

    repo_root = Path(repo_root).resolve()
    output_dir = repo_root / T612_RELATIVE_DIR
    manifest_path = output_dir / "analysis-manifest.json"
    diagnostics_path = output_dir / "diagnostics.json"
    marker_path = output_dir / "FINALIZED"
    if not all(
        path.is_file() for path in (manifest_path, diagnostics_path, marker_path)
    ):
        raise RuntimeError("T-612 analysis package is incomplete")
    manifest_sha256 = sha256_file(manifest_path)
    expected_marker = (
        f"schema_version={T612_PACKAGE_SCHEMA_VERSION}\n"
        "status=finalized\n"
        f"manifest_sha256={manifest_sha256}\n"
    )
    if marker_path.read_text(encoding="utf-8") != expected_marker:
        raise RuntimeError("T-612 finalization marker does not match manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, Mapping):
        raise TypeError("T-612 analysis manifest must be an object")
    expected_identity = {
        "schema_version": T612_PACKAGE_SCHEMA_VERSION,
        "status": "finalized",
        "task_id": "T-612",
        "scientific_recipe_id": "protocol-v2.1-final",
        "accepted_execution_instance_id": ACCEPTED_EXECUTION_ID,
        "execution_source_git_commit": EXPECTED_EXECUTION_SOURCE_COMMIT,
        "recipe_sha256": EXPECTED_RECIPE_SHA256,
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "t611_freeze_manifest_sha256": EXPECTED_FREEZE_MANIFEST_SHA256,
        "t611_run_manifest_inventory_sha256": EXPECTED_RUN_INVENTORY_SHA256,
        "analysis_recipe": V21_ANALYSIS_RECIPE,
        "deterministic_regeneration_count": 2,
        "all_regenerations_byte_identical": True,
        "t610_mechanical_artifacts_byte_identical": True,
        "rq_coverage": ["RQ1", "RQ2", "RQ3"],
        "recovery_tolerances": [0.05, 0.1, 0.2],
        "frozen_evidence_mutated": False,
        "t613_or_wp7_work_performed": False,
    }
    if any(manifest.get(key) != value for key, value in expected_identity.items()):
        raise RuntimeError("T-612 analysis manifest identity is invalid")
    freeze = validate_protocol_v21_final_freeze(repo_root)
    if (
        freeze["freeze_manifest_sha256"] != EXPECTED_FREEZE_MANIFEST_SHA256
        or freeze["run_manifest_inventory_sha256"] != EXPECTED_RUN_INVENTORY_SHA256
    ):
        raise RuntimeError("T-612 no longer points to the accepted T-611 freeze")
    diagnostics_ref = manifest.get("diagnostics")
    report_ref = manifest.get("scientific_interpretation_report")
    for reference in (diagnostics_ref, report_ref):
        if not isinstance(reference, Mapping):
            raise TypeError("T-612 referenced artifact must be an object")
        path = repo_root / str(reference.get("relative_path"))
        if reference.get("sha256") != sha256_file(path):
            raise RuntimeError("T-612 referenced artifact hash mismatch")
    source_commit = manifest.get("analysis_source_git_commit")
    if not isinstance(source_commit, str) or not re.fullmatch(
        r"[0-9a-f]{40}", source_commit
    ):
        raise RuntimeError("T-612 analysis source commit is invalid")
    for record in manifest.get("analysis_tool_source_files", []):
        if not isinstance(record, Mapping):
            raise TypeError("T-612 tool source record must be an object")
        committed = _git(
            repo_root, "show", f"{source_commit}:{record['relative_path']}"
        )
        if record.get("sha256") != _sha256_bytes(committed):
            raise RuntimeError("T-612 committed tool source hash mismatch")
    for record in manifest.get("canonical_analysis_artifacts", []):
        if not isinstance(record, Mapping):
            raise TypeError("T-612 analysis artifact record must be an object")
        path = repo_root / str(record.get("relative_path"))
        if record.get("sha256") != sha256_file(path):
            raise RuntimeError("T-612 canonical analysis artifact hash mismatch")
    return {
        "valid": True,
        "analysis_manifest_sha256": manifest_sha256,
        "analysis_source_git_commit": source_commit,
        "canonical_analysis_artifact_count": len(
            manifest["canonical_analysis_artifacts"]
        ),
        "rq_coverage": manifest["rq_coverage"],
        "recovery_tolerances": manifest["recovery_tolerances"],
    }
