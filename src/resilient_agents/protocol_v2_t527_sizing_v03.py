"""DEC-057 structural reuse audit and one fresh T-527 sizing completion.

The physical stage executes DQN, PPO and Dyna-Q+ from root one.  It never
executes tuning and never imports incomplete DQN rows from earlier sizing
attempts.  A separate derived package composes those fresh complete strata
with only the exact complete Q-Learning/SARSA strata retained by DEC-057.
"""
from __future__ import annotations

import ast
import json
import subprocess
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .protocol_v2_boundary_settlement import settle_phase_a_interaction_boundary
from .protocol_v2_t527 import (
    _append_jsonl,
    _canonical_json,
    _close_phase_a,
    _git_commit,
    _new_output,
    _read_jsonl,
    _run_phase_a_unit,
    _run_sizing_phase_b,
    _sha256_file,
    _sha256_value,
    _sizing_root,
    _sizing_selection,
    _valid_observations,
    _write_integrity,
    _write_json,
)
from .protocol_v2_t527_sizing_v02 import (
    EXPECTED_CONFIG_IDS,
    _horizon_audit,
    _host,
    _verify_integrity,
    load_retry_plan,
    validate_historical_authority as validate_dec056_inputs,
)

PLAN_SCHEMA_VERSION = 1
BASELINE_COMMIT = "fbb5a7abda5444aebb12569e5e83b07df89b49ee"
FRESH_METHODS = ("dqn", "ppo", "dyna_q_plus")
REUSED_METHODS = ("q_learning", "sarsa")
ALL_METHODS = REUSED_METHODS + FRESH_METHODS
EXPECTED_FRESH_PHASE_A = 144
EXPECTED_FRESH_MATCHED_SETS = 288
EXPECTED_COMBINED_PHASE_A = 240
EXPECTED_COMBINED_MATCHED_SETS = 480


def load_completion_plan(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema_version", "decision_id", "study_id", "scientific_status",
        "purpose", "final_reserve_access", "required_host", "source_authority",
        "execution_scope", "reuse_authority", "outputs",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise ValueError("DEC-057 completion plan schema/keys mismatch")
    if value["schema_version"] != PLAN_SCHEMA_VERSION or value["decision_id"] != "DEC-057":
        raise ValueError("DEC-057 completion plan identity mismatch")
    if value["final_reserve_access"] is not False:
        raise ValueError("DEC-057 final-reserve firewall must be false")
    scope = value["execution_scope"]
    if (
        scope.get("mode") != "fresh-three-method-completion"
        or tuple(scope.get("fresh_methods", ())) != FRESH_METHODS
        or tuple(scope.get("reused_complete_methods", ())) != REUSED_METHODS
        or scope.get("reuse_incomplete_dqn_v02") is not False
        or scope.get("reuse_any_sizing_v01") is not False
        or tuple(scope.get("start_identity", ())) != ("dqn", "t527-size-r01", "gw-l1-a")
    ):
        raise ValueError("DEC-057 execution scope changed")
    expected = (
        int(scope.get("expected_fresh_phase_a_units", -1)),
        int(scope.get("expected_fresh_matched_sets", -1)),
        int(scope.get("expected_fresh_branches", -1)),
        int(scope.get("expected_fresh_branch_horizon_evaluations", -1)),
    )
    if expected != (144, 288, 1152, 2304):
        raise ValueError("DEC-057 fresh execution denominators changed")
    reuse = value["reuse_authority"]
    if (
        tuple(reuse.get("methods", {})) != REUSED_METHODS
        or reuse.get("performance_values_permitted_for_reuse_decision") is not False
        or reuse.get("new_correction_is_sb3_only") is not True
    ):
        raise ValueError("DEC-057 structural reuse authority changed")
    for output in value["outputs"].values():
        lowered = str(output).lower()
        if "final" in lowered or "reserve" in lowered:
            raise ValueError("DEC-057 output violates final-reserve firewall")
    return value


def _source_plan(repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Any]:
    source = plan["source_authority"]
    path = repo_root / str(source["plan"])
    if _sha256_file(path) != source["plan_sha256"]:
        raise RuntimeError("DEC-056 source plan hash changed")
    return load_retry_plan(path)


class _ProjectPrefixNormalizer(ast.NodeTransformer):
    """Remove only SB3 else bodies before code-lineage comparison."""

    def visit_If(self, node: ast.If) -> ast.AST:
        self.generic_visit(node)
        if isinstance(node.test, ast.Name) and node.test.id == "project_method":
            node.orelse = [ast.Pass()]
        return node


def _normalized_prefix_function(source: str) -> str:
    tree = ast.parse(source)
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "prepare_shared_no_learning_prefix"
    )
    normalized = _ProjectPrefixNormalizer().visit(function)
    ast.fix_missing_locations(normalized)
    return ast.dump(normalized, include_attributes=False)


def _verify_reuse_code_lineage(repo_root: Path) -> Mapping[str, Any]:
    unchanged = (
        "configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json",
        "src/resilient_agents/agents.py",
        "src/resilient_agents/sarsa.py",
        "src/resilient_agents/contracts.py",
        "src/resilient_agents/environment.py",
        "src/resilient_agents/gridworld.py",
        "src/resilient_agents/randomness.py",
        "src/resilient_agents/protocol_v2.py",
        "src/resilient_agents/protocol_v2_boundary_settlement.py",
        "src/resilient_agents/protocol_v2_gridworld.py",
        "src/resilient_agents/protocol_v2_tabular_driver.py",
        "src/resilient_agents/protocol_v2_tabular_phase_b.py",
        "src/resilient_agents/protocol_v2_t527.py",
    )
    changed = []
    for relative in unchanged:
        result = subprocess.run(
            ["git", "diff", "--quiet", BASELINE_COMMIT, "--", relative],
            cwd=repo_root,
            check=False,
        )
        if result.returncode != 0:
            changed.append(relative)
    if changed:
        raise RuntimeError(f"DEC-057 reuse-critical code lineage changed: {changed}")

    relative = "src/resilient_agents/protocol_v2_prefix.py"
    baseline = subprocess.check_output(
        ["git", "show", f"{BASELINE_COMMIT}:{relative}"],
        cwd=repo_root,
        text=True,
    )
    current = (repo_root / relative).read_text(encoding="utf-8")
    baseline_digest = _sha256_value(_normalized_prefix_function(baseline))
    current_digest = _sha256_value(_normalized_prefix_function(current))
    if current_digest != baseline_digest:
        raise RuntimeError("project-method shared-prefix semantics changed since sizing-v0.2")
    return {
        "baseline_commit": BASELINE_COMMIT,
        "unchanged_reuse_critical_paths": list(unchanged),
        "normalized_project_prefix_sha256": current_digest,
        "correction_scope": "SB3 direct-inference representation only",
    }


def _checkpoint_index(
    directory: Path,
    rows: Sequence[Mapping[str, Any]],
    integrity: Mapping[str, Any],
) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for row in rows:
        relative = str(row["deployment_start_checkpoint_path"])
        path = directory / relative
        digest = _sha256_file(path)
        if (
            digest != row["deployment_start_checkpoint_file_sha256"]
            or digest != integrity["files"][relative]["sha256"]
        ):
            raise RuntimeError(f"deployment checkpoint integrity mismatch: {relative}")
        result.append((relative, digest))
    return result


def _validate_reusable_method(
    *,
    method_id: str,
    directory: Path,
    phase_a: Sequence[Mapping[str, Any]],
    phase_b: Sequence[Mapping[str, Any]],
    integrity: Mapping[str, Any],
    source_plan: Mapping[str, Any],
    authority: Mapping[str, Any],
) -> Mapping[str, Any]:
    a_rows = [row for row in phase_a if row["method_id"] == method_id]
    b_rows = [row for row in phase_b if row["method_id"] == method_id]
    layouts = tuple(item["layout_id"] for item in source_plan["development_layouts"])
    conditions = tuple(item["condition_id"] for item in source_plan["sizing"]["conditions"])
    expected_a = {
        (method_id, f"t527-size-r{index:02d}", layout)
        for index in range(1, 25)
        for layout in layouts
    }
    expected_b = {(*unit, condition) for unit in expected_a for condition in conditions}
    if len(a_rows) != 48 or {
        (row["method_id"], row["root_id"], row["layout_id"]) for row in a_rows
    } != expected_a:
        raise RuntimeError(f"{method_id} reusable Phase-A stratum is incomplete")
    if len(b_rows) != 96 or {
        (row["method_id"], row["root_id"], row["layout_id"], row["condition_id"])
        for row in b_rows
    } != expected_b:
        raise RuntimeError(f"{method_id} reusable Phase-B stratum is incomplete")
    config_id = EXPECTED_CONFIG_IDS[method_id]
    probes = tuple(int(item) for item in source_plan["tuning"]["probe_interaction_indices"])
    for row in a_rows:
        if (
            row["config_id"] != config_id
            or int(row["training_interactions"]) != 8192
            or tuple(int(item["interaction_index"]) for item in row["probes"]) != probes
        ):
            raise RuntimeError(f"{method_id} reusable Phase-A contract mismatch")
    for row in b_rows:
        if row["config_id"] != config_id or int(row["prefix_interactions"]) != 1:
            raise RuntimeError(f"{method_id} reusable Phase-B contract mismatch")
        if set(row["horizons"]) != {"256", "512"}:
            raise RuntimeError(f"{method_id} reusable horizon mismatch")
        for horizon in ("256", "512"):
            branches = row["horizons"][horizon]
            if len(branches) != 4 or {item["branch"] for item in branches} != {
                "FN", "FD", "AN", "AD"
            }:
                raise RuntimeError(f"{method_id} reusable branch matrix mismatch")
            if any(
                "native_update_opportunities_completed" not in item["metrics"]
                for item in branches
            ):
                raise RuntimeError(f"{method_id} reusable update-opportunity evidence missing")
    phase_a_sha = _sha256_value(a_rows)
    phase_b_sha = _sha256_value(b_rows)
    checkpoint_index = _checkpoint_index(directory, a_rows, integrity)
    checkpoint_sha = _sha256_value(checkpoint_index)
    expected = authority["methods"][method_id]
    if (
        phase_a_sha != expected["phase_a_rows_sha256"]
        or phase_b_sha != expected["phase_b_rows_sha256"]
        or checkpoint_sha != expected["checkpoint_index_sha256"]
    ):
        raise RuntimeError(f"{method_id} reusable source identity changed")
    return {
        "status": "structurally-accepted",
        "phase_a_units": len(a_rows),
        "matched_sets": len(b_rows),
        "phase_a_rows_sha256": phase_a_sha,
        "phase_b_rows_sha256": phase_b_sha,
        "checkpoint_index_sha256": checkpoint_sha,
        "checkpoint_files": len(checkpoint_index),
        "performance_values_used_for_decision": False,
    }


def validate_historical_authority(
    *, repo_root: Path, plan: Mapping[str, Any]
) -> Mapping[str, Any]:
    source_plan = _source_plan(repo_root, plan)
    dec056_inputs = validate_dec056_inputs(repo_root=repo_root, plan=source_plan)
    source = plan["source_authority"]
    directory = repo_root / str(source["sizing_v02"])
    expected_files = {
        "integrity.json": source["sizing_v02_integrity_sha256"],
        "manifest.json": source["sizing_v02_manifest_sha256"],
        "phase-a-sizing.jsonl": source["sizing_v02_phase_a_sha256"],
        "phase-b-sizing.jsonl": source["sizing_v02_phase_b_sha256"],
        "failures.jsonl": source["sizing_v02_failures_sha256"],
    }
    for relative, expected in expected_files.items():
        if _sha256_file(directory / relative) != expected:
            raise RuntimeError(f"immutable sizing-v0.2 file changed: {relative}")
    integrity = _verify_integrity(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    phase_a = _read_jsonl(directory / "phase-a-sizing.jsonl")
    phase_b = _read_jsonl(directory / "phase-b-sizing.jsonl")
    failures = _read_jsonl(directory / "failures.jsonl")
    if (
        manifest.get("status") != "failed"
        or manifest.get("final_reserve_access") is not False
        or manifest.get("completed_phase_a_units") != 137
        or manifest.get("completed_phase_b_matched_sets") != 272
        or len(phase_a) != 137
        or len(phase_b) != 272
        or len(failures) != 1
    ):
        raise RuntimeError("DEC-056 sizing-v0.2 retained failure envelope changed")
    failure = failures[0]
    if (
        failure.get("method_id"), failure.get("root_id"), failure.get("layout_id"),
        failure.get("exception_type"), failure.get("message")
    ) != (
        "dqn", "t527-size-r21", "gw-l1-a", "AttributeError",
        "'tuple' object has no attribute 'shape'",
    ):
        raise RuntimeError("DEC-056 sizing-v0.2 failure identity changed")
    code_lineage = _verify_reuse_code_lineage(repo_root)
    reuse = {
        method: _validate_reusable_method(
            method_id=method,
            directory=directory,
            phase_a=phase_a,
            phase_b=phase_b,
            integrity=integrity,
            source_plan=source_plan,
            authority=plan["reuse_authority"],
        )
        for method in REUSED_METHODS
    }
    if any(failure.get("method_id") in REUSED_METHODS for failure in failures):
        raise RuntimeError("reusable method has a retained failure")
    return {
        "status": "valid-structural-composition-authority",
        "final_reserve_access": False,
        "dec056_inputs_sha256": _sha256_value(dec056_inputs),
        "sizing_v02_status": "valid-failed",
        "sizing_v02_integrity_files": len(integrity["files"]),
        "sizing_v02_integrity_bytes": sum(
            int(item["bytes"]) for item in integrity["files"].values()
        ),
        "retained_failure": failure,
        "code_lineage": code_lineage,
        "reusable_methods": reuse,
        "excluded_sources": {
            "sizing_v01_rows": "all",
            "sizing_v02_dqn_rows": "all",
            "sizing_v02_ppo_rows": "all",
            "sizing_v02_dyna_q_plus_rows": "all",
        },
        "performance_values_used_for_reuse_decision": False,
    }


def run_fresh_completion(*, repo_root: Path, plan: Mapping[str, Any]) -> Path:
    source_plan = _source_plan(repo_root, plan)
    historical = validate_historical_authority(repo_root=repo_root, plan=plan)
    output = _new_output(repo_root, str(plan["outputs"]["fresh_sizing"]))
    for filename in ("phase-a-sizing.jsonl", "phase-b-sizing.jsonl", "failures.jsonl"):
        (output / filename).write_text("", encoding="utf-8")
    base_manifest = {
        "schema_version": 1,
        "decision_id": "DEC-057",
        "source_decision_id": "DEC-056",
        "stage": "precision-runtime-sizing-completion",
        "execution_scope": "fresh-three-method-completion",
        "fresh_methods": list(FRESH_METHODS),
        "scientific_status": plan["scientific_status"],
        "final_reserve_access": False,
        "plan_sha256": _sha256_value(plan),
        "source_plan_sha256": plan["source_authority"]["plan_sha256"],
        "execution_commit": _git_commit(repo_root),
        "host": _host(),
        "historical_authority_sha256": _sha256_value(historical),
        "expected_phase_a_units": EXPECTED_FRESH_PHASE_A,
        "expected_phase_b_matched_sets": EXPECTED_FRESH_MATCHED_SETS,
        "started_unix_seconds": time.time(),
        "status": "in-progress",
    }
    _write_json(output / "historical-authority-validation.json", historical)
    _write_json(output / "manifest.json", base_manifest)
    phase_a_rows: list[Mapping[str, Any]] = []
    phase_b_rows: list[Mapping[str, Any]] = []
    budget = int(source_plan["tuning"]["selected_phase_a_budget"])
    probes = tuple(int(item) for item in source_plan["tuning"]["probe_interaction_indices"])
    for method_id in FRESH_METHODS:
        parameters = source_plan["selected_configs"][method_id]
        for index in range(1, 25):
            root_data = _sizing_root(index)
            for layout in source_plan["development_layouts"]:
                driver = None
                try:
                    row, execution, driver = _run_phase_a_unit(
                        plan=source_plan,
                        method_id=method_id,
                        parameters=parameters,
                        root_data=root_data,
                        layout=layout,
                        budget=budget,
                        probes=probes,
                        decision_id="DEC-057",
                        protocol_version="protocol-v2.0-t527-development-sizing-v0.3",
                    )
                    learner = execution.final_adapter
                    settlement = settle_phase_a_interaction_boundary(
                        learner,
                        expected_source_learner_sha256=learner.state_sha256(),
                        expected_interactions=budget,
                        valid_observations=_valid_observations(layout),
                    )
                    checkpoint = execution.result.final_checkpoint.to_mapping()
                    checkpoint["state"] = learner.export_state()
                    checkpoint["provenance"] = {
                        **dict(checkpoint["provenance"]),
                        "boundary_settlement": settlement.to_mapping(),
                        "deployment_start_learner_sha256": learner.state_sha256(),
                    }
                    relative = (
                        Path("deployment-start-checkpoints")
                        / method_id
                        / root_data["root_id"]
                        / f"{layout['layout_id']}.json"
                    )
                    target = output / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    _write_json(target, checkpoint)
                    row = {
                        **dict(row),
                        "settlement": settlement.to_mapping(),
                        "deployment_start_checkpoint_path": relative.as_posix(),
                        "deployment_start_checkpoint_file_sha256": _sha256_file(target),
                    }
                    phase_a_rows.append(row)
                    _append_jsonl(output / "phase-a-sizing.jsonl", row)
                    for condition in source_plan["sizing"]["conditions"]:
                        wall_start = time.perf_counter()
                        result = _run_sizing_phase_b(
                            plan=source_plan,
                            method_id=method_id,
                            parameters=parameters,
                            root_data=root_data,
                            layout=layout,
                            learner=learner.clone(),
                            condition=condition,
                        )
                        result = {
                            **dict(result),
                            "wall_seconds": time.perf_counter() - wall_start,
                        }
                        phase_b_rows.append(result)
                        _append_jsonl(output / "phase-b-sizing.jsonl", result)
                except Exception as exc:
                    failure = {
                        "stage": "sizing-completion",
                        "method_id": method_id,
                        "root_id": root_data["root_id"],
                        "layout_id": layout["layout_id"],
                        "exception_type": type(exc).__name__,
                        "message": str(exc),
                    }
                    _append_jsonl(output / "failures.jsonl", failure)
                    _write_json(output / "manifest.json", {
                        **base_manifest,
                        "status": "failed",
                        "completed_phase_a_units": len(phase_a_rows),
                        "completed_phase_b_matched_sets": len(phase_b_rows),
                        "failure": failure,
                    })
                    _write_integrity(output)
                    raise
                finally:
                    if driver is not None:
                        _close_phase_a(driver)
    _write_json(output / "manifest.json", {
        **base_manifest,
        "status": "complete",
        "completed_phase_a_units": len(phase_a_rows),
        "completed_phase_b_matched_sets": len(phase_b_rows),
        "completed_branch_executions": len(phase_b_rows) * 4,
        "completed_branch_horizon_evaluations": len(phase_b_rows) * 4 * 2,
        "completed_unix_seconds": time.time(),
    })
    _write_integrity(output)
    return output


def _expected_units(methods: Sequence[str], source_plan: Mapping[str, Any]) -> set[tuple[str, str, str]]:
    return {
        (method, f"t527-size-r{index:02d}", layout["layout_id"])
        for method in methods
        for index in range(1, 25)
        for layout in source_plan["development_layouts"]
    }


def validate_fresh_attempt(*, repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Any]:
    source_plan = _source_plan(repo_root, plan)
    historical = validate_historical_authority(repo_root=repo_root, plan=plan)
    output = repo_root / str(plan["outputs"]["fresh_sizing"])
    integrity = _verify_integrity(output)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    phase_a = _read_jsonl(output / "phase-a-sizing.jsonl")
    phase_b = _read_jsonl(output / "phase-b-sizing.jsonl")
    failures = _read_jsonl(output / "failures.jsonl")
    if (
        manifest.get("status") != "complete"
        or manifest.get("execution_scope") != "fresh-three-method-completion"
        or manifest.get("final_reserve_access") is not False
        or len(phase_a) != EXPECTED_FRESH_PHASE_A
        or len(phase_b) != EXPECTED_FRESH_MATCHED_SETS
        or failures
    ):
        raise RuntimeError("DEC-057 fresh sizing evidence is not valid-complete")
    expected_a = _expected_units(FRESH_METHODS, source_plan)
    if {(row["method_id"], row["root_id"], row["layout_id"]) for row in phase_a} != expected_a:
        raise RuntimeError("DEC-057 fresh Phase-A identity matrix mismatch")
    conditions = tuple(item["condition_id"] for item in source_plan["sizing"]["conditions"])
    expected_b = {(*unit, condition) for unit in expected_a for condition in conditions}
    if {
        (row["method_id"], row["root_id"], row["layout_id"], row["condition_id"])
        for row in phase_b
    } != expected_b:
        raise RuntimeError("DEC-057 fresh matched-set identity matrix mismatch")
    if any(row["method_id"] not in FRESH_METHODS for row in phase_a + phase_b):
        raise RuntimeError("DEC-057 fresh output contains a non-fresh method")
    for row in phase_b:
        for horizon in ("256", "512"):
            branches = row["horizons"][horizon]
            if len(branches) != 4 or {item["branch"] for item in branches} != {
                "FN", "FD", "AN", "AD"
            }:
                raise RuntimeError("DEC-057 fresh branch/horizon matrix mismatch")
            if any(
                "native_update_opportunities_completed" not in item["metrics"]
                for item in branches
            ):
                raise RuntimeError("DEC-057 fresh native update evidence missing")
    return {
        "status": "valid-complete",
        "final_reserve_access": False,
        "historical_authority_sha256": _sha256_value(historical),
        "phase_a_units": len(phase_a),
        "matched_sets": len(phase_b),
        "branches": len(phase_b) * 4,
        "branch_horizon_evaluations": len(phase_b) * 4 * 2,
        "files": len(integrity["files"]),
        "bytes": sum(int(item["bytes"]) for item in integrity["files"].values()),
    }


def _index_rows(
    *, package: str, rows: Sequence[Mapping[str, Any]], methods: Sequence[str], phase: str
) -> tuple[list[Mapping[str, Any]], list[Mapping[str, Any]]]:
    selected_rows: list[Mapping[str, Any]] = []
    index: list[Mapping[str, Any]] = []
    for line_number, row in enumerate(rows, start=1):
        if row["method_id"] not in methods:
            continue
        selected_rows.append(row)
        identity = {
            "method_id": row["method_id"],
            "root_id": row["root_id"],
            "layout_id": row["layout_id"],
        }
        if phase == "phase-b":
            identity["condition_id"] = row["condition_id"]
        entry: dict[str, Any] = {
            **identity,
            "source_package": package,
            "source_file": f"{phase}-sizing.jsonl",
            "source_row_number": line_number,
            "source_row_sha256": _sha256_value(row),
        }
        if phase == "phase-a":
            entry.update({
                "source_checkpoint_path": row["deployment_start_checkpoint_path"],
                "source_checkpoint_file_sha256": row[
                    "deployment_start_checkpoint_file_sha256"
                ],
            })
        index.append(entry)
    return selected_rows, index


def write_combined_evidence(*, repo_root: Path, plan: Mapping[str, Any]) -> Path:
    source_plan = _source_plan(repo_root, plan)
    reuse = validate_historical_authority(repo_root=repo_root, plan=plan)
    fresh_validation = validate_fresh_attempt(repo_root=repo_root, plan=plan)
    retained_package = str(plan["source_authority"]["sizing_v02"])
    fresh_package = str(plan["outputs"]["fresh_sizing"])
    retained_dir = repo_root / retained_package
    fresh_dir = repo_root / fresh_package
    retained_a = _read_jsonl(retained_dir / "phase-a-sizing.jsonl")
    retained_b = _read_jsonl(retained_dir / "phase-b-sizing.jsonl")
    fresh_a = _read_jsonl(fresh_dir / "phase-a-sizing.jsonl")
    fresh_b = _read_jsonl(fresh_dir / "phase-b-sizing.jsonl")
    reused_a, reused_a_index = _index_rows(
        package=retained_package,
        rows=retained_a,
        methods=REUSED_METHODS,
        phase="phase-a",
    )
    reused_b, reused_b_index = _index_rows(
        package=retained_package,
        rows=retained_b,
        methods=REUSED_METHODS,
        phase="phase-b",
    )
    new_a, new_a_index = _index_rows(
        package=fresh_package,
        rows=fresh_a,
        methods=FRESH_METHODS,
        phase="phase-a",
    )
    new_b, new_b_index = _index_rows(
        package=fresh_package,
        rows=fresh_b,
        methods=FRESH_METHODS,
        phase="phase-b",
    )
    phase_a = reused_a + new_a
    phase_b = reused_b + new_b
    phase_a_index = reused_a_index + new_a_index
    phase_b_index = reused_b_index + new_b_index
    output = _new_output(repo_root, str(plan["outputs"]["combined_sizing"]))
    for entry in phase_a_index:
        _append_jsonl(output / "phase-a-index.jsonl", entry)
    for entry in phase_b_index:
        _append_jsonl(output / "phase-b-index.jsonl", entry)
    (output / "failures.jsonl").write_text("", encoding="utf-8")
    selection = dict(_sizing_selection(
        plan=source_plan,
        phase_a_rows=phase_a,
        phase_b_rows=phase_b,
        decision_id="DEC-057",
    ))
    selection["adaptive_horizon_audit"] = _horizon_audit(phase_b)
    _write_json(output / "selection.json", selection)
    _write_json(output / "reuse-validation.json", reuse)
    _write_json(output / "fresh-validation.json", fresh_validation)
    manifest = {
        "schema_version": 1,
        "decision_id": "DEC-057",
        "stage": "precision-runtime-sizing-combined-reference-index",
        "scientific_status": plan["scientific_status"],
        "final_reserve_access": False,
        "status": "complete",
        "composition_mode": "retained-complete-two-plus-fresh-complete-three",
        "retained_methods": list(REUSED_METHODS),
        "fresh_methods": list(FRESH_METHODS),
        "excluded_incomplete_sources": [
            "results/pilots/protocol-v2-t527-sizing-v0.1/**",
            "results/pilots/protocol-v2-t527-sizing-v0.2/dqn/**",
        ],
        "source_integrity_sha256": {
            retained_package: _sha256_file(retained_dir / "integrity.json"),
            fresh_package: _sha256_file(fresh_dir / "integrity.json"),
        },
        "phase_a_units": len(phase_a),
        "matched_sets": len(phase_b),
        "branches": len(phase_b) * 4,
        "branch_horizon_evaluations": len(phase_b) * 4 * 2,
        "selection_sha256": _sha256_value(selection),
    }
    _write_json(output / "manifest.json", manifest)
    _write_integrity(output)
    return output


def _resolve_index(
    *, repo_root: Path, entries: Sequence[Mapping[str, Any]], phase: str
) -> list[Mapping[str, Any]]:
    cache: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    resolved: list[Mapping[str, Any]] = []
    for entry in entries:
        package = str(entry["source_package"])
        filename = str(entry["source_file"])
        key = (package, filename)
        if key not in cache:
            cache[key] = _read_jsonl(repo_root / package / filename)
        number = int(entry["source_row_number"])
        if number <= 0 or number > len(cache[key]):
            raise RuntimeError("combined source row number is outside its source")
        row = cache[key][number - 1]
        if _sha256_value(row) != entry["source_row_sha256"]:
            raise RuntimeError("combined source row hash mismatch")
        identity = (row["method_id"], row["root_id"], row["layout_id"])
        expected = (entry["method_id"], entry["root_id"], entry["layout_id"])
        if identity != expected:
            raise RuntimeError("combined source row identity mismatch")
        if phase == "phase-b" and row["condition_id"] != entry["condition_id"]:
            raise RuntimeError("combined source condition identity mismatch")
        if phase == "phase-a":
            checkpoint = repo_root / package / str(entry["source_checkpoint_path"])
            if _sha256_file(checkpoint) != entry["source_checkpoint_file_sha256"]:
                raise RuntimeError("combined source checkpoint hash mismatch")
        resolved.append(row)
    return resolved


def _validate_combined_identity_coverage(
    *,
    source_plan: Mapping[str, Any],
    phase_a: Sequence[Mapping[str, Any]],
    phase_b: Sequence[Mapping[str, Any]],
    phase_a_index: Sequence[Mapping[str, Any]],
    phase_b_index: Sequence[Mapping[str, Any]],
    retained_package: str,
) -> None:
    expected_a = _expected_units(ALL_METHODS, source_plan)
    actual_a = {(row["method_id"], row["root_id"], row["layout_id"]) for row in phase_a}
    if actual_a != expected_a or len(actual_a) != len(phase_a):
        raise RuntimeError("combined Phase-A coverage has missing/duplicate cells")
    conditions = tuple(item["condition_id"] for item in source_plan["sizing"]["conditions"])
    expected_b = {(*unit, condition) for unit in expected_a for condition in conditions}
    actual_b = {
        (row["method_id"], row["root_id"], row["layout_id"], row["condition_id"])
        for row in phase_b
    }
    if actual_b != expected_b or len(actual_b) != len(phase_b):
        raise RuntimeError("combined Phase-B coverage has missing/duplicate cells")
    if any(
        entry["source_package"] == retained_package
        and entry["method_id"] not in REUSED_METHODS
        for entry in tuple(phase_a_index) + tuple(phase_b_index)
    ):
        raise RuntimeError("combined sizing imported an incomplete v0.2 method")
    if any(
        "sizing-v0.1" in str(entry["source_package"])
        for entry in tuple(phase_a_index) + tuple(phase_b_index)
    ):
        raise RuntimeError("combined sizing imported sizing-v0.1 evidence")


def validate_combined_evidence(*, repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Any]:
    source_plan = _source_plan(repo_root, plan)
    reuse = validate_historical_authority(repo_root=repo_root, plan=plan)
    fresh = validate_fresh_attempt(repo_root=repo_root, plan=plan)
    output = repo_root / str(plan["outputs"]["combined_sizing"])
    integrity = _verify_integrity(output)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    phase_a_index = _read_jsonl(output / "phase-a-index.jsonl")
    phase_b_index = _read_jsonl(output / "phase-b-index.jsonl")
    if _read_jsonl(output / "failures.jsonl"):
        raise RuntimeError("combined sizing package contains failures")
    phase_a = _resolve_index(repo_root=repo_root, entries=phase_a_index, phase="phase-a")
    phase_b = _resolve_index(repo_root=repo_root, entries=phase_b_index, phase="phase-b")
    if (
        manifest.get("status") != "complete"
        or manifest.get("final_reserve_access") is not False
        or len(phase_a) != EXPECTED_COMBINED_PHASE_A
        or len(phase_b) != EXPECTED_COMBINED_MATCHED_SETS
    ):
        raise RuntimeError("combined sizing denominator/firewall mismatch")
    retained_package = str(plan["source_authority"]["sizing_v02"])
    _validate_combined_identity_coverage(
        source_plan=source_plan,
        phase_a=phase_a,
        phase_b=phase_b,
        phase_a_index=phase_a_index,
        phase_b_index=phase_b_index,
        retained_package=retained_package,
    )
    selection = json.loads((output / "selection.json").read_text(encoding="utf-8"))
    recomputed = dict(_sizing_selection(
        plan=source_plan,
        phase_a_rows=phase_a,
        phase_b_rows=phase_b,
        decision_id="DEC-057",
    ))
    recomputed["adaptive_horizon_audit"] = _horizon_audit(phase_b)
    if selection != recomputed:
        raise RuntimeError("combined sizing selection does not reproduce exactly")
    if json.loads((output / "reuse-validation.json").read_text(encoding="utf-8")) != reuse:
        raise RuntimeError("combined reuse validation changed")
    if json.loads((output / "fresh-validation.json").read_text(encoding="utf-8")) != fresh:
        raise RuntimeError("combined fresh validation changed")
    return {
        "status": "valid-complete",
        "final_reserve_access": False,
        "phase_a_units": len(phase_a),
        "matched_sets": len(phase_b),
        "branches": len(phase_b) * 4,
        "branch_horizon_evaluations": len(phase_b) * 4 * 2,
        "incomplete_dqn_v02_rows_used": 0,
        "sizing_v01_rows_used": 0,
        "files": len(integrity["files"]),
        "bytes": sum(int(item["bytes"]) for item in integrity["files"].values()),
        "selection": selection,
    }


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="DEC-057 T-527 sizing completion")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--config",
        default="configs/protocols/protocol-v2-t527-sizing-completion-v0.3.json",
    )
    parser.add_argument("--validate-inputs-only", action="store_true")
    parser.add_argument("--validate-fresh-only", action="store_true")
    parser.add_argument("--validate-combined-only", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    plan = load_completion_plan((repo_root / args.config).resolve())
    if args.validate_inputs_only:
        result = validate_historical_authority(repo_root=repo_root, plan=plan)
    elif args.validate_fresh_only:
        result = validate_fresh_attempt(repo_root=repo_root, plan=plan)
    elif args.validate_combined_only:
        result = validate_combined_evidence(repo_root=repo_root, plan=plan)
    else:
        fresh = run_fresh_completion(repo_root=repo_root, plan=plan)
        validate_fresh_attempt(repo_root=repo_root, plan=plan)
        combined = write_combined_evidence(repo_root=repo_root, plan=plan)
        result = {
            "fresh_sizing": str(fresh),
            "combined_sizing": str(combined),
            "validation": validate_combined_evidence(repo_root=repo_root, plan=plan),
        }
    print(_canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
