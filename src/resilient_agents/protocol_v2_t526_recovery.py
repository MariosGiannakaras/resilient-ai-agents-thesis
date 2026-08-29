"""Physical Windows T-526A checkpoint recovery and Phase-B calibration.

The original one-time Phase-A evidence is never opened for writing. Recovery
uses the unchanged original implementation to materialize only the selected
``gw-l1`` checkpoint payloads, then enforces a complete exact-identity barrier
before any Phase-B interaction is permitted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from .protocol_v2 import ProtocolV2Phase, ScientificCheckpoint, ScientificStateAdapter
from .protocol_v2_executor import execute_phase_a, execute_phase_b
from .protocol_v2_feasibility import (
    CORE_METHOD_IDS,
    SB3ProjectGridWorldProbeEvaluator,
    _canonical_json,
    _episode_seeds,
    _phase_a_request,
    _project_driver,
    _root,
    _sb3_driver,
    _scenario,
    _sha256,
    load_plan,
)
from .protocol_v2_prefix import prepare_shared_no_learning_prefix
from .protocol_v2_sb3 import SB3ScientificStateAdapter
from .protocol_v2_t526_phase_b import (
    T526PPOTransientStateAdapter,
    t526_branch_driver,
)
from .protocol_v2_tabular_driver import ProjectTabularNoLearningProbeEvaluator
from .study.protocol_v2_phase_b_executor import _disturbed_spec


AMENDMENT_SCHEMA_VERSION = 1
EXPECTED_BRANCHES = ("FN", "FD", "AN", "AD")
EXPECTED_CONDITIONS = (
    ("action-remap-swap-right-down", "action-remap", "swap-right-down"),
    ("action-remap-cycle-clockwise", "action-remap", "cycle-clockwise"),
    ("action-failure-p005", "action-failure", 0.05),
    ("action-failure-p015", "action-failure", 0.15),
    ("action-failure-p030", "action-failure", 0.30),
    ("observation-corruption-p002", "observation-corruption", 0.02),
    ("observation-corruption-p005", "observation-corruption", 0.05),
    ("observation-corruption-p010", "observation-corruption", 0.10),
)


def _file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_canonical_json(value) + "\n", encoding="utf-8", newline="\n")


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(_canonical_json(value) + "\n")


def _read_jsonl(path: Path) -> list[Mapping[str, Any]]:
    rows: list[Mapping[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, Mapping):
            raise ValueError(f"{path}:{line_number} must contain a JSON object")
        rows.append(value)
    return rows


def _require_empty_or_absent(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise RuntimeError(f"retained output already exists and cannot be overwritten: {path}")


def load_amendment(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "amendment_id",
        "pilot_id",
        "scientific_status",
        "purpose",
        "final_reserve_access",
        "required_host",
        "original_phase_a",
        "source_compatibility",
        "recovery",
        "phase_b",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise ValueError("T-526 amendment configuration keys mismatch")
    if value["schema_version"] != AMENDMENT_SCHEMA_VERSION:
        raise ValueError("unsupported T-526 amendment schema_version")
    if value["amendment_id"] != "DEC-052":
        raise ValueError("T-526 amendment must be governed by DEC-052")
    if value["final_reserve_access"] is not False:
        raise ValueError("T-526A must forbid final-reserve access")

    original = value["original_phase_a"]
    if original["source_commit"] != "5198dbe077119b7caa4e9a101b55b115a979c22e":
        raise ValueError("original Phase-A source commit is immutable")
    if original["selected_level_id"] != "gw-l1":
        raise ValueError("recovery is restricted to selected gw-l1")
    if tuple(original["methods"]) != CORE_METHOD_IDS:
        raise ValueError("recovery method set/order must remain the five original methods")
    if tuple(original["roots"]) != ("t526-r01", "t526-r02", "t526-r03"):
        raise ValueError("recovery roots are immutable")
    if tuple(original["layouts"]) != ("gw-l1-a", "gw-l1-b"):
        raise ValueError("recovery layouts are immutable")
    if int(original["expected_units"]) != 30:
        raise ValueError("recovery must require exactly 30 units")

    recovery = value["recovery"]
    if int(recovery["required_exact_matches"]) != 30:
        raise ValueError("the complete 30/30 recovery barrier is mandatory")
    phase_b = value["phase_b"]
    if phase_b["selected_level_id"] != "gw-l1":
        raise ValueError("Phase B must use selected gw-l1")
    if int(phase_b["common_nominal_no_learning_prefix_interactions"]) != 1:
        raise ValueError("T-526 Phase-B prefix is frozen at one interaction")
    if int(phase_b["post_boundary_interactions_per_branch"]) != 10:
        raise ValueError("T-526 branch budget is frozen at ten interactions")
    if tuple(phase_b["branches"]) != EXPECTED_BRANCHES:
        raise ValueError("T-526 requires exact FN/FD/AN/AD branches")
    if phase_b["episode_resets"] is not False:
        raise ValueError("T-526 Phase B forbids episode resets")
    if int(phase_b["expected_matched_sets"]) != 240:
        raise ValueError("T-526 Phase B must contain 240 matched sets")
    if int(phase_b["expected_post_boundary_interactions"]) != 9600:
        raise ValueError("T-526 Phase B exact interaction denominator changed")

    observed_conditions = []
    for condition in phase_b["conditions"]:
        specification = condition["specification"]
        identity = (
            specification["mapping_id"]
            if condition["family"] == "action-remap"
            else float(specification["probability"])
        )
        observed_conditions.append(
            (condition["condition_id"], condition["family"], identity)
        )
    if tuple(observed_conditions) != EXPECTED_CONDITIONS:
        raise ValueError("T-526 Phase-B candidate identities/order changed")
    safety = phase_b["shortest_path_safety"]
    if not (
        int(safety["required_shortest_path_length"]) == 12
        and int(safety["prefix_plus_branch_interactions"]) == 11
        and safety["require_strictly_less_than_shortest_path"] is True
    ):
        raise ValueError("T-526 shortest-path safety invariant changed")
    return value


def verify_original_bundle(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, str]:
    original = amendment["original_phase_a"]
    directory = repo_root / str(original["evidence_directory"])
    expected = dict(original["evidence_file_sha256"])
    actual: dict[str, str] = {}
    if set(path.name for path in directory.iterdir() if path.is_file()) != set(expected):
        raise RuntimeError("original Phase-A evidence file set changed")
    for name, digest in expected.items():
        path = directory / name
        actual[name] = _file_sha256(path)
        if actual[name] != digest:
            raise RuntimeError(f"immutable original Phase-A evidence hash mismatch: {name}")
    return actual


def verify_source_compatibility(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> tuple[str, ...]:
    source = str(amendment["original_phase_a"]["source_commit"])
    paths = tuple(amendment["source_compatibility"]["require_no_diff_from_original_source_commit"])
    result = subprocess.run(
        ["git", "diff", "--name-only", source, "--", *paths],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"unable to verify Phase-A source compatibility: {result.stderr.strip()}")
    differences = tuple(line for line in result.stdout.splitlines() if line.strip())
    if differences:
        raise RuntimeError(
            "Phase-A-affecting implementation differs from the one-time source commit: "
            + ", ".join(differences)
        )
    return paths


def _host_snapshot() -> Mapping[str, Any]:
    snapshot = {
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "python_executable_basename": Path(sys.executable).name,
        "cpu_count": os.cpu_count(),
    }
    if snapshot["platform_system"] != "Windows":
        raise RuntimeError("T-526A must execute on the physical Windows thesis machine")
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError("T-526A requires native CPython 3.12")
    return snapshot


def _git_commit(repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
    ).strip()


def _authoritative_rows(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[tuple[str, str, str], Mapping[str, Any]]:
    path = (
        repo_root
        / str(amendment["original_phase_a"]["evidence_directory"])
        / "phase-a-runs.jsonl"
    )
    rows = _read_jsonl(path)
    indexed: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    for row in rows:
        key = (str(row["method_id"]), str(row["root_id"]), str(row["layout_id"]))
        if key in indexed:
            raise RuntimeError(f"duplicate authoritative Phase-A unit: {key}")
        indexed[key] = row
    if len(indexed) != 30:
        raise RuntimeError("authoritative Phase-A row denominator is not 30")
    return indexed


def _materialize_unit(
    plan: Mapping[str, Any],
    *,
    level_id: str,
    layout: Mapping[str, Any],
    root_data: Mapping[str, Any],
    method_id: str,
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    """Run the exact original Phase-A orchestration and retain its checkpoint."""

    root = _root(root_data)
    parameters = dict(plan["provisional_method_configs"][method_id])
    scenario = _scenario(plan, layout)
    budget = int(plan["phase_a"]["training_interaction_budget"])
    probe_count = int(plan["phase_a"]["episodes_per_probe"])
    probe_seeds = _episode_seeds(
        root,
        scope=f"protocol-v2-phase-a-probe:{layout['layout_id']}",
        count=probe_count,
    )
    if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
        driver = _project_driver(method_id, parameters, scenario, root)
        evaluator = ProjectTabularNoLearningProbeEvaluator(
            scenario=scenario, environment_seeds=probe_seeds
        )
    else:
        driver = _sb3_driver(method_id, parameters, scenario, root, budget)
        evaluator = SB3ProjectGridWorldProbeEvaluator(
            scenario=scenario, seeds=probe_seeds
        )
    try:
        execution = execute_phase_a(
            _phase_a_request(
                plan,
                method_id=method_id,
                parameters=parameters,
                root=root,
                layout_id=str(layout["layout_id"]),
            ),
            driver=driver,
            probe_evaluator=evaluator,
            checkpoint_provenance={
                "pilot_id": plan["pilot_id"],
                "level_id": level_id,
                "scientific_status": "non-final-feasibility-only",
            },
        )
        checkpoint = execution.result.final_checkpoint.to_mapping()
        checkpoint_bytes = len(_canonical_json(checkpoint).encode("utf-8"))
        row = {
            "status": "completed",
            "level_id": level_id,
            "layout_id": layout["layout_id"],
            "root_id": root.root_id,
            "method_id": method_id,
            "implementation_id": parameters["implementation_id"],
            "training_interactions": execution.result.ledger.training_interactions,
            "probe_interactions": execution.result.ledger.probe_interactions,
            "checkpoint_bytes": checkpoint_bytes,
            "checkpoint_sha256": execution.result.final_checkpoint.sha256,
            "learner_state_sha256": execution.final_adapter.state_sha256(),
            "probes": [
                {
                    "interaction_index": item.training_interaction_index,
                    "environment_interactions": item.probe_environment_interactions,
                    "episodes": item.episodes,
                    "metrics": dict(item.metrics),
                }
                for item in execution.result.probes
            ],
        }
        return row, checkpoint
    finally:
        close = getattr(driver, "close", None)
        if callable(close):
            close()
        adapter = getattr(driver, "state_adapter", None)
        model = getattr(adapter, "model", None)
        env = model.get_env() if model is not None else None
        if env is not None:
            env.close()


def compare_reconstruction_row(
    *,
    authoritative: Mapping[str, Any],
    reconstructed: Mapping[str, Any],
    fields: Sequence[str],
) -> Mapping[str, Any]:
    mismatches = {
        field: {
            "expected": authoritative.get(field),
            "actual": reconstructed.get(field),
        }
        for field in fields
        if authoritative.get(field) != reconstructed.get(field)
    }
    return {"exact_match": not mismatches, "mismatches": mismatches}


def _checkpoint_relative_path(
    amendment: Mapping[str, Any], *, method_id: str, root_id: str, layout_id: str
) -> Path:
    template = str(amendment["recovery"]["checkpoint_path_template"])
    return Path(
        template.format(method_id=method_id, root_id=root_id, layout_id=layout_id)
    )


def _integrity_payload(directory: Path, *, excluded: Sequence[str]) -> Mapping[str, Any]:
    excluded_set = set(excluded)
    files = []
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        relative = path.relative_to(directory).as_posix()
        if relative in excluded_set:
            continue
        files.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": _file_sha256(path),
            }
        )
    return {
        "schema_version": 1,
        "algorithm": "sha256",
        "files": files,
        "total_files": len(files),
        "total_bytes": sum(int(item["bytes"]) for item in files),
    }


def require_complete_recovery_barrier(manifest: Mapping[str, Any]) -> None:
    if manifest.get("status") != "complete-barrier-passed" or int(
        manifest.get("exact_matches", 0)
    ) != 30:
        raise RuntimeError("Phase B is blocked until the exact 30/30 recovery barrier passes")


def materialize_recovery(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    original_hashes = verify_original_bundle(repo_root=repo_root, amendment=amendment)
    verified_paths = verify_source_compatibility(repo_root=repo_root, amendment=amendment)
    original_plan_path = repo_root / str(amendment["original_phase_a"]["plan_path"])
    plan = load_plan(original_plan_path)
    if _sha256(plan) != amendment["original_phase_a"]["canonical_plan_sha256"]:
        raise RuntimeError("original canonical feasibility plan digest mismatch")
    output = repo_root / str(amendment["recovery"]["output_directory"])
    _require_empty_or_absent(output)
    output.mkdir(parents=True, exist_ok=True)
    records_path = output / "reconstruction.jsonl"
    failures_path = output / "failures.jsonl"
    records_path.write_text("", encoding="utf-8")
    failures_path.write_text("", encoding="utf-8")
    manifest_path = output / "manifest.json"
    started = time.time()
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "pilot_id": amendment["pilot_id"],
        "role": amendment["recovery"]["role"],
        "scientific_status": amendment["scientific_status"],
        "final_reserve_access": False,
        "status": "in-progress",
        "source_phase_a_commit": amendment["original_phase_a"]["source_commit"],
        "recovery_implementation_commit": _git_commit(repo_root),
        "amendment_config_sha256": _sha256(amendment),
        "original_plan_sha256": amendment["original_phase_a"]["canonical_plan_sha256"],
        "original_evidence_file_sha256": original_hashes,
        "source_compatibility_paths": list(verified_paths),
        "started_unix_seconds": started,
        "host": _host_snapshot(),
        "expected_units": 30,
        "exact_matches": 0,
    }
    _write_json(manifest_path, manifest)
    authoritative = _authoritative_rows(repo_root=repo_root, amendment=amendment)
    fields = tuple(amendment["recovery"]["deterministic_row_fields"])
    selected = next(
        level
        for level in plan["ordered_gridworld_ladder"]
        if level["level_id"] == "gw-l1"
    )
    exact_matches = 0
    try:
        for layout in selected["layouts"]:
            if int(layout["shortest_path_length"]) != 12:
                raise RuntimeError("selected gw-l1 shortest-path declaration changed")
            for root_data in plan["roots"]:
                for method_id in CORE_METHOD_IDS:
                    key = (method_id, str(root_data["root_id"]), str(layout["layout_id"]))
                    wall_start = time.perf_counter()
                    try:
                        row, checkpoint = _materialize_unit(
                            plan,
                            level_id="gw-l1",
                            layout=layout,
                            root_data=root_data,
                            method_id=method_id,
                        )
                        comparison = compare_reconstruction_row(
                            authoritative=authoritative[key],
                            reconstructed=row,
                            fields=fields,
                        )
                        relative = _checkpoint_relative_path(
                            amendment,
                            method_id=method_id,
                            root_id=str(root_data["root_id"]),
                            layout_id=str(layout["layout_id"]),
                        )
                        checkpoint_path = output / relative
                        _write_json(checkpoint_path, checkpoint)
                        evidence = {
                            "method_id": method_id,
                            "root_id": root_data["root_id"],
                            "layout_id": layout["layout_id"],
                            "source_phase_a_commit": amendment["original_phase_a"]["source_commit"],
                            "expected_checkpoint_sha256": authoritative[key]["checkpoint_sha256"],
                            "reconstructed_checkpoint_sha256": row["checkpoint_sha256"],
                            "expected_learner_state_sha256": authoritative[key]["learner_state_sha256"],
                            "reconstructed_learner_state_sha256": row["learner_state_sha256"],
                            "checkpoint_path": relative.as_posix(),
                            "checkpoint_file_bytes": checkpoint_path.stat().st_size,
                            "checkpoint_file_sha256": _file_sha256(checkpoint_path),
                            "wall_seconds": time.perf_counter() - wall_start,
                            **comparison,
                        }
                        _append_jsonl(records_path, evidence)
                        if not comparison["exact_match"]:
                            _append_jsonl(
                                failures_path,
                                {
                                    "failure_kind": "infrastructure",
                                    "stage": "checkpoint-reconstruction",
                                    **evidence,
                                },
                            )
                            raise RuntimeError(f"exact recovery mismatch for {key}")
                        exact_matches += 1
                    except Exception as exc:
                        if not isinstance(exc, RuntimeError) or not str(exc).startswith(
                            "exact recovery mismatch"
                        ):
                            _append_jsonl(
                                failures_path,
                                {
                                    "failure_kind": "infrastructure",
                                    "stage": "checkpoint-reconstruction",
                                    "method_id": method_id,
                                    "root_id": root_data["root_id"],
                                    "layout_id": layout["layout_id"],
                                    "exception_type": type(exc).__name__,
                                    "message": str(exc),
                                },
                            )
                        raise
        if exact_matches != int(amendment["recovery"]["required_exact_matches"]):
            raise RuntimeError("the complete recovery barrier did not reach 30/30")
        verify_original_bundle(repo_root=repo_root, amendment=amendment)
        manifest.update(
            {
                "status": "complete-barrier-passed",
                "exact_matches": exact_matches,
                "completed_unix_seconds": time.time(),
                "wall_seconds": time.time() - started,
            }
        )
        _write_json(manifest_path, manifest)
        integrity = _integrity_payload(output, excluded=("integrity.json",))
        _write_json(output / "integrity.json", integrity)
        return manifest
    except Exception:
        manifest.update(
            {
                "status": "failed-barrier-blocks-phase-b",
                "exact_matches": exact_matches,
                "completed_unix_seconds": time.time(),
                "wall_seconds": time.time() - started,
            }
        )
        _write_json(manifest_path, manifest)
        integrity = _integrity_payload(output, excluded=("integrity.json",))
        _write_json(output / "integrity.json", integrity)
        raise


def _checkpoint_from_mapping(value: Mapping[str, Any]) -> ScientificCheckpoint:
    required = {
        "schema_version",
        "method_id",
        "root_id",
        "layout_id",
        "phase",
        "training_interaction_index",
        "state",
        "provenance",
    }
    if set(value) != required:
        raise ValueError("recovered scientific checkpoint keys mismatch")
    return ScientificCheckpoint(
        schema_version=int(value["schema_version"]),
        method_id=str(value["method_id"]),
        root_id=str(value["root_id"]),
        layout_id=str(value["layout_id"]),
        phase=ProtocolV2Phase(str(value["phase"])),
        training_interaction_index=int(value["training_interaction_index"]),
        state=value["state"],
        provenance=value["provenance"],
    )


def _restore_learner(
    *,
    plan: Mapping[str, Any],
    layout: Mapping[str, Any],
    root_data: Mapping[str, Any],
    method_id: str,
    checkpoint: ScientificCheckpoint,
) -> ScientificStateAdapter:
    root = _root(root_data)
    scenario = _scenario(plan, layout)
    parameters = dict(plan["provisional_method_configs"][method_id])
    if method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
        driver = _project_driver(method_id, parameters, scenario, root)
    else:
        driver = _sb3_driver(
            method_id,
            parameters,
            scenario,
            root,
            int(plan["phase_a"]["training_interaction_budget"]),
        )
        old_env = driver.state_adapter.model.get_env()
        if old_env is not None:
            old_env.close()
    adapter = driver.state_adapter
    adapter.restore_state(checkpoint.state)
    return adapter


def _prefix_seed(root_data: Mapping[str, Any], *, layout_id: str):
    root = _root(root_data)
    return _episode_seeds(
        root,
        scope=f"protocol-v2-t526-phase-b-prefix:{layout_id}",
        count=1,
    )[0]


def _close_phase_b_drivers(drivers: Sequence[Any]) -> None:
    for driver in drivers:
        learner = getattr(driver, "learner", None)
        inner = getattr(learner, "inner", learner)
        model = getattr(inner, "model", None)
        env = model.get_env() if model is not None else None
        if env is not None:
            env.close()
        environment = getattr(driver, "environment", None)
        if environment is not None:
            environment.environment.close()


def run_phase_b(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    verify_original_bundle(repo_root=repo_root, amendment=amendment)
    recovery_dir = repo_root / str(amendment["recovery"]["output_directory"])
    recovery_manifest = json.loads(
        (recovery_dir / "manifest.json").read_text(encoding="utf-8")
    )
    require_complete_recovery_barrier(recovery_manifest)
    validate_recovery_evidence(repo_root=repo_root, amendment=amendment)

    output = repo_root / str(amendment["phase_b"]["output_directory"])
    _require_empty_or_absent(output)
    output.mkdir(parents=True, exist_ok=True)
    sets_path = output / "matched-sets.jsonl"
    failures_path = output / "failures.jsonl"
    sets_path.write_text("", encoding="utf-8")
    failures_path.write_text("", encoding="utf-8")
    manifest_path = output / "manifest.json"
    started = time.time()
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "pilot_id": amendment["pilot_id"],
        "scientific_status": amendment["scientific_status"],
        "final_reserve_access": False,
        "status": "in-progress",
        "amendment_config_sha256": _sha256(amendment),
        "recovery_manifest_sha256": _file_sha256(recovery_dir / "manifest.json"),
        "recovery_integrity_sha256": _file_sha256(recovery_dir / "integrity.json"),
        "execution_commit": _git_commit(repo_root),
        "host": _host_snapshot(),
        "started_unix_seconds": started,
        "expected_matched_sets": 240,
        "completed_matched_sets": 0,
        "expected_branch_executions": 960,
        "completed_branch_executions": 0,
        "expected_post_boundary_interactions": 9600,
        "completed_post_boundary_interactions": 0,
    }
    _write_json(manifest_path, manifest)

    plan = load_plan(repo_root / str(amendment["original_phase_a"]["plan_path"]))
    selected = next(
        level
        for level in plan["ordered_gridworld_ladder"]
        if level["level_id"] == "gw-l1"
    )
    expected_rows = _authoritative_rows(repo_root=repo_root, amendment=amendment)
    completed_sets = 0
    branch_executions = 0
    interactions = 0
    branch_points: dict[tuple[str, str, str], tuple[str, str]] = {}
    wall_by_method: dict[str, float] = {method: 0.0 for method in CORE_METHOD_IDS}
    try:
        for layout in selected["layouts"]:
            if int(layout["shortest_path_length"]) != 12:
                raise RuntimeError("gw-l1 no-reset shortest-path safety failed")
            nominal = _scenario(plan, layout)
            for root_data in plan["roots"]:
                for method_id in CORE_METHOD_IDS:
                    key = (method_id, str(root_data["root_id"]), str(layout["layout_id"]))
                    relative = _checkpoint_relative_path(
                        amendment,
                        method_id=method_id,
                        root_id=str(root_data["root_id"]),
                        layout_id=str(layout["layout_id"]),
                    )
                    checkpoint_value = json.loads(
                        (recovery_dir / relative).read_text(encoding="utf-8")
                    )
                    checkpoint = _checkpoint_from_mapping(checkpoint_value)
                    if checkpoint.sha256 != expected_rows[key]["checkpoint_sha256"]:
                        raise RuntimeError(f"Phase-B source checkpoint identity mismatch: {key}")
                    for condition in amendment["phase_b"]["conditions"]:
                        set_started = time.perf_counter()
                        prefix = None
                        created_drivers: list[Any] = []
                        try:
                            learner = _restore_learner(
                                plan=plan,
                                layout=layout,
                                root_data=root_data,
                                method_id=method_id,
                                checkpoint=checkpoint,
                            )
                            if learner.state_sha256() != expected_rows[key]["learner_state_sha256"]:
                                raise RuntimeError(f"Phase-B restored learner identity mismatch: {key}")
                            prefix = prepare_shared_no_learning_prefix(
                                learner=learner,
                                nominal_spec=nominal,
                                environment_seeds=_prefix_seed(
                                    root_data, layout_id=str(layout["layout_id"])
                                ),
                                interactions=1,
                            )
                            source_learner: ScientificStateAdapter = prefix.learner
                            if method_id == "ppo":
                                if not isinstance(source_learner, SB3ScientificStateAdapter):
                                    raise RuntimeError("PPO prefix did not retain the project adapter")
                                source_learner = T526PPOTransientStateAdapter(source_learner)
                            disturbed = _disturbed_spec(
                                nominal=nominal,
                                condition=condition,
                                onset_step=1,
                            )

                            def factory(branch, adaptive, branch_learner, environment):
                                driver = t526_branch_driver(
                                    branch=branch,
                                    adaptive=adaptive,
                                    learner=branch_learner,
                                    environment=environment,
                                )
                                created_drivers.append(driver)
                                return driver

                            execution = execute_phase_b(
                                learner=source_learner,
                                shared_environment=prefix.environment,
                                nominal_spec=nominal,
                                disturbed_spec=disturbed,
                                interaction_budget_per_branch=10,
                                driver_factory=factory,
                            )
                            current_branch_point = (
                                execution.branch_point_learner_sha256,
                                execution.branch_point_environment_sha256,
                            )
                            previous = branch_points.setdefault(key, current_branch_point)
                            if previous != current_branch_point:
                                raise RuntimeError(
                                    f"condition-specific prefix/fork state detected for {key}"
                                )
                            branches = [
                                {
                                    "branch": item.branch.value,
                                    "interactions": item.interactions,
                                    "metrics": dict(item.metrics),
                                    "final_learner_state_sha256": item.final_learner_state_sha256,
                                    "final_environment_state_sha256": item.final_environment_state_sha256,
                                }
                                for item in execution.results
                            ]
                            if tuple(item["branch"] for item in branches) != EXPECTED_BRANCHES:
                                raise RuntimeError("Phase-B branch ordering/assignment changed")
                            if any(int(item["interactions"]) != 10 for item in branches):
                                raise RuntimeError("Phase-B exact branch interaction budget failed")
                            wall = time.perf_counter() - set_started
                            wall_by_method[method_id] += wall
                            record = {
                                "status": "completed",
                                "method_id": method_id,
                                "root_id": root_data["root_id"],
                                "layout_id": layout["layout_id"],
                                "condition_id": condition["condition_id"],
                                "condition_family": condition["family"],
                                "condition_specification": condition["specification"],
                                "source_checkpoint_path": relative.as_posix(),
                                "source_checkpoint_sha256": checkpoint.sha256,
                                "source_learner_state_sha256": expected_rows[key]["learner_state_sha256"],
                                "prefix_interactions": 1,
                                "branch_point_learner_sha256": execution.branch_point_learner_sha256,
                                "branch_point_environment_sha256": execution.branch_point_environment_sha256,
                                "post_boundary_interactions_per_branch": 10,
                                "episode_resets": False,
                                "branches": branches,
                                "wall_seconds": wall,
                            }
                            _append_jsonl(sets_path, record)
                            completed_sets += 1
                            branch_executions += 4
                            interactions += 40
                        except Exception as exc:
                            _append_jsonl(
                                failures_path,
                                {
                                    "failure_kind": "infrastructure",
                                    "stage": "phase-b-matched-set",
                                    "method_id": method_id,
                                    "root_id": root_data["root_id"],
                                    "layout_id": layout["layout_id"],
                                    "condition_id": condition["condition_id"],
                                    "exception_type": type(exc).__name__,
                                    "message": str(exc),
                                },
                            )
                            raise
                        finally:
                            _close_phase_b_drivers(created_drivers)
                            if prefix is not None:
                                prefix.environment.environment.close()

        if completed_sets != 240 or branch_executions != 960 or interactions != 9600:
            raise RuntimeError("Phase-B final denominator accounting failed")
        verify_original_bundle(repo_root=repo_root, amendment=amendment)
        denominators = {
            "schema_version": 1,
            "planned_matched_sets": 240,
            "completed_matched_sets": completed_sets,
            "scientific_failure_matched_sets": 0,
            "infrastructure_failure_matched_sets": 0,
            "planned_branch_executions": 960,
            "completed_branch_executions": branch_executions,
            "planned_post_boundary_interactions": 9600,
            "completed_post_boundary_interactions": interactions,
            "methods": list(CORE_METHOD_IDS),
            "roots": list(amendment["original_phase_a"]["roots"]),
            "layouts": list(amendment["original_phase_a"]["layouts"]),
            "conditions": [
                item["condition_id"] for item in amendment["phase_b"]["conditions"]
            ],
            "branches": list(EXPECTED_BRANCHES),
        }
        _write_json(output / "denominators.json", denominators)
        manifest.update(
            {
                "status": "complete",
                "completed_matched_sets": completed_sets,
                "completed_branch_executions": branch_executions,
                "completed_post_boundary_interactions": interactions,
                "scientific_failures": 0,
                "infrastructure_failures": 0,
                "wall_seconds_by_method": wall_by_method,
                "completed_unix_seconds": time.time(),
                "wall_seconds": time.time() - started,
            }
        )
        _write_json(manifest_path, manifest)
        _write_json(
            output / "integrity.json",
            _integrity_payload(output, excluded=("integrity.json",)),
        )
        return manifest
    except Exception:
        manifest.update(
            {
                "status": "failed",
                "completed_matched_sets": completed_sets,
                "completed_branch_executions": branch_executions,
                "completed_post_boundary_interactions": interactions,
                "completed_unix_seconds": time.time(),
                "wall_seconds": time.time() - started,
            }
        )
        _write_json(manifest_path, manifest)
        _write_json(
            output / "integrity.json",
            _integrity_payload(output, excluded=("integrity.json",)),
        )
        raise


def _validate_integrity(directory: Path) -> Mapping[str, Any]:
    integrity = json.loads((directory / "integrity.json").read_text(encoding="utf-8"))
    for item in integrity["files"]:
        path = directory / item["path"]
        if path.stat().st_size != int(item["bytes"]):
            raise RuntimeError(f"artifact byte-size mismatch: {path}")
        if _file_sha256(path) != item["sha256"]:
            raise RuntimeError(f"artifact SHA-256 mismatch: {path}")
    return integrity


def validate_recovery_evidence(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    verify_original_bundle(repo_root=repo_root, amendment=amendment)
    directory = repo_root / str(amendment["recovery"]["output_directory"])
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "complete-barrier-passed" or int(manifest["exact_matches"]) != 30:
        raise RuntimeError("recovery evidence does not prove the 30/30 barrier")
    rows = _read_jsonl(directory / "reconstruction.jsonl")
    if len(rows) != 30 or not all(row["exact_match"] is True for row in rows):
        raise RuntimeError("recovery reconstruction denominator/exact-match status failed")
    if (directory / "failures.jsonl").read_text(encoding="utf-8"):
        raise RuntimeError("recovery failure log is non-empty")
    original_rows = _authoritative_rows(repo_root=repo_root, amendment=amendment)
    seen = set()
    for row in rows:
        key = (row["method_id"], row["root_id"], row["layout_id"])
        if key in seen:
            raise RuntimeError(f"duplicate recovery row: {key}")
        seen.add(key)
        path = directory / row["checkpoint_path"]
        if _file_sha256(path) != row["checkpoint_file_sha256"]:
            raise RuntimeError(f"recovery checkpoint file hash mismatch: {key}")
        checkpoint = _checkpoint_from_mapping(json.loads(path.read_text(encoding="utf-8")))
        if checkpoint.sha256 != original_rows[key]["checkpoint_sha256"]:
            raise RuntimeError(f"recovery checkpoint scientific identity mismatch: {key}")
        if row["reconstructed_learner_state_sha256"] != original_rows[key]["learner_state_sha256"]:
            raise RuntimeError(f"recovery learner identity mismatch: {key}")
    integrity = _validate_integrity(directory)
    return {
        "status": "valid",
        "exact_matches": len(rows),
        "checkpoint_files": 30,
        "artifact_files": integrity["total_files"],
        "artifact_bytes": integrity["total_bytes"],
    }


def validate_phase_b_evidence(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    verify_original_bundle(repo_root=repo_root, amendment=amendment)
    directory = repo_root / str(amendment["phase_b"]["output_directory"])
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "complete":
        raise RuntimeError("Phase-B manifest is not complete")
    rows = _read_jsonl(directory / "matched-sets.jsonl")
    if len(rows) != 240:
        raise RuntimeError("Phase-B matched-set denominator is not 240")
    if (directory / "failures.jsonl").read_text(encoding="utf-8"):
        raise RuntimeError("Phase-B failure log is non-empty")
    seen = set()
    branch_points: dict[tuple[str, str, str], tuple[str, str]] = {}
    total_interactions = 0
    for row in rows:
        key = (
            row["method_id"],
            row["root_id"],
            row["layout_id"],
            row["condition_id"],
        )
        if key in seen:
            raise RuntimeError(f"duplicate Phase-B matched set: {key}")
        seen.add(key)
        if int(row["prefix_interactions"]) != 1 or row["episode_resets"] is not False:
            raise RuntimeError(f"Phase-B lifecycle mismatch: {key}")
        branches = row["branches"]
        if tuple(item["branch"] for item in branches) != EXPECTED_BRANCHES:
            raise RuntimeError(f"Phase-B branch assignment mismatch: {key}")
        if any(int(item["interactions"]) != 10 for item in branches):
            raise RuntimeError(f"Phase-B interaction mismatch: {key}")
        total_interactions += sum(int(item["interactions"]) for item in branches)
        unit = key[:3]
        point = (
            row["branch_point_learner_sha256"],
            row["branch_point_environment_sha256"],
        )
        previous = branch_points.setdefault(unit, point)
        if previous != point:
            raise RuntimeError(f"Phase-B branch point varied across conditions: {unit}")
    if total_interactions != 9600:
        raise RuntimeError("Phase-B total actual interaction accounting failed")
    denominators = json.loads((directory / "denominators.json").read_text(encoding="utf-8"))
    if (
        int(denominators["completed_matched_sets"]) != 240
        or int(denominators["completed_branch_executions"]) != 960
        or int(denominators["completed_post_boundary_interactions"]) != 9600
    ):
        raise RuntimeError("Phase-B denominator artifact failed")
    integrity = _validate_integrity(directory)
    return {
        "status": "valid",
        "matched_sets": len(rows),
        "branch_executions": 960,
        "post_boundary_interactions": total_interactions,
        "artifact_files": integrity["total_files"],
        "artifact_bytes": integrity["total_bytes"],
    }


def run_physical_recovery_and_phase_b(
    *, repo_root: Path, amendment_path: Path
) -> Mapping[str, Any]:
    amendment = load_amendment(amendment_path)
    _host_snapshot()
    recovery = materialize_recovery(repo_root=repo_root, amendment=amendment)
    if recovery["status"] != "complete-barrier-passed":
        raise RuntimeError("Phase B blocked by incomplete checkpoint recovery")
    phase_b = run_phase_b(repo_root=repo_root, amendment=amendment)
    recovery_validation = validate_recovery_evidence(
        repo_root=repo_root, amendment=amendment
    )
    phase_b_validation = validate_phase_b_evidence(
        repo_root=repo_root, amendment=amendment
    )
    return {
        "status": "complete",
        "recovery": recovery_validation,
        "phase_b": phase_b_validation,
        "phase_b_runtime": {
            "wall_seconds": phase_b["wall_seconds"],
            "wall_seconds_by_method": phase_b["wall_seconds_by_method"],
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run reviewed T-526A deterministic recovery and bounded Phase-B calibration."
    )
    parser.add_argument(
        "--amendment",
        default="configs/protocols/protocol-v2-t526-recovery-phase-b-v0.1.json",
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    amendment = load_amendment((repo_root / args.amendment).resolve())
    if args.validate_only:
        result = {
            "recovery": validate_recovery_evidence(
                repo_root=repo_root, amendment=amendment
            ),
            "phase_b": validate_phase_b_evidence(
                repo_root=repo_root, amendment=amendment
            ),
        }
    else:
        result = run_physical_recovery_and_phase_b(
            repo_root=repo_root,
            amendment_path=(repo_root / args.amendment).resolve(),
        )
    print(_canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
