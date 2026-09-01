"""DEC-056 one-time T-527 sizing-only retry and retained-evidence validator.

This program never executes tuning and never reads a final-reserve outcome.  It
validates the immutable DEC-055 history, starts a fresh 240-unit/480-set sizing
matrix, and applies the original DEC-055 selection rules with explicit
method-native adaptive update-opportunity accounting.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
import time
from collections import deque
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .protocol_v2_boundary_settlement import settle_phase_a_interaction_boundary
from .protocol_v2_feasibility import CORE_METHOD_IDS
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
    load_plan,
    verify_immutable_inputs,
)

PLAN_SCHEMA_VERSION = 1
EXPECTED_CONFIG_IDS = {
    "q_learning": "q-c06",
    "sarsa": "sarsa-c06",
    "dqn": "dqn-c05",
    "ppo": "ppo-c06",
    "dyna_q_plus": "dyna-c03",
}
EXPECTED_PHASE_A_UNITS = 240
EXPECTED_MATCHED_SETS = 480


def load_retry_plan(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema_version", "decision_id", "study_id", "scientific_status",
        "purpose", "final_reserve_access", "required_host", "source_authority",
        "task", "development_layouts", "tuning", "selected_configs", "sizing",
        "phase_b_lifecycle", "final_freeze_rules", "outputs",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise ValueError("DEC-056 retry plan schema/keys mismatch")
    if value["schema_version"] != PLAN_SCHEMA_VERSION or value["decision_id"] != "DEC-056":
        raise ValueError("DEC-056 retry plan identity mismatch")
    if value["final_reserve_access"] is not False:
        raise ValueError("DEC-056 final-reserve firewall must be false")
    if set(value["selected_configs"]) != set(CORE_METHOD_IDS):
        raise ValueError("DEC-056 must retain exactly the five core methods")
    actual_ids = {
        method: config["config_id"]
        for method, config in value["selected_configs"].items()
    }
    if actual_ids != EXPECTED_CONFIG_IDS:
        raise ValueError("DEC-056 selected configurations changed")
    if int(value["tuning"]["selected_phase_a_budget"]) != 8192:
        raise ValueError("DEC-056 Phase-A budget changed")
    if tuple(value["sizing"]["root_count_candidates"]) != (12, 16, 20, 24):
        raise ValueError("DEC-056 root-count candidates changed")
    if tuple(value["sizing"]["phase_b_horizon_candidates"]) != (256, 512):
        raise ValueError("DEC-056 horizon candidates changed")
    if [item["condition_id"] for item in value["sizing"]["conditions"]] != [
        "action-remap-swap-right-down", "action-remap-cycle-clockwise"
    ]:
        raise ValueError("DEC-056 sizing conditions changed")
    if value["sizing"]["common_nominal_no_learning_prefix_interactions"] != 1:
        raise ValueError("DEC-056 common prefix changed")
    if value["final_freeze_rules"]["layout_generation"]["agent_execution_permitted"] is not False:
        raise ValueError("DEC-056 final-layout firewall changed")
    for path_value in value["outputs"].values():
        lowered = str(path_value).lower()
        if "final" in lowered or "reserve" in lowered:
            raise ValueError("DEC-056 output path violates final-reserve firewall")
    return value


def _verify_integrity(directory: Path) -> Mapping[str, Any]:
    integrity_path = directory / "integrity.json"
    if not integrity_path.is_file():
        raise RuntimeError(f"retained integrity manifest missing: {directory}")
    integrity = json.loads(integrity_path.read_text(encoding="utf-8"))
    for relative, expected in integrity["files"].items():
        path = directory / relative
        if (
            not path.is_file()
            or _sha256_file(path) != expected["sha256"]
            or path.stat().st_size != expected["bytes"]
        ):
            raise RuntimeError(f"retained evidence integrity mismatch: {directory.name}/{relative}")
    return integrity


def validate_historical_authority(*, repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Any]:
    source = plan["source_authority"]
    old_plan = load_plan(repo_root / str(source["plan"]))
    immutable = verify_immutable_inputs(repo_root=repo_root, plan=old_plan)

    tuning = repo_root / str(source["tuning"])
    tuning_integrity = _verify_integrity(tuning)
    tuning_manifest = json.loads((tuning / "manifest.json").read_text(encoding="utf-8"))
    tuning_selection = json.loads((tuning / "selection.json").read_text(encoding="utf-8"))
    tuning_rows = _read_jsonl(tuning / "tuning-runs.jsonl")
    if (
        tuning_manifest.get("status") != "complete"
        or tuning_manifest.get("completed_units") != 180
        or tuning_manifest.get("final_reserve_access") is not False
        or len(tuning_rows) != 180
        or _read_jsonl(tuning / "failures.jsonl")
    ):
        raise RuntimeError("DEC-055 tuning-v0.1 is not valid-complete")
    selected_ids = {
        method: config["config_id"]
        for method, config in tuning_selection["selected_configs"].items()
    }
    if selected_ids != EXPECTED_CONFIG_IDS or tuning_selection["selected_phase_a_budget"] != 8192:
        raise RuntimeError("DEC-055 tuning selection does not match DEC-056 authority")
    if tuning_selection["selected_configs"] != plan["selected_configs"]:
        raise RuntimeError("DEC-056 selected configuration payload differs from retained tuning")

    failed = repo_root / str(source["failed_sizing"])
    failed_integrity = _verify_integrity(failed)
    failed_manifest = json.loads((failed / "manifest.json").read_text(encoding="utf-8"))
    failures = _read_jsonl(failed / "failures.jsonl")
    if (
        failed_manifest.get("status") != "failed"
        or failed_manifest.get("completed_phase_a_units") != 97
        or failed_manifest.get("completed_phase_b_matched_sets") != 192
        or failed_manifest.get("final_reserve_access") is not False
        or len(_read_jsonl(failed / "phase-a-sizing.jsonl")) != 97
        or len(_read_jsonl(failed / "phase-b-sizing.jsonl")) != 192
        or len(failures) != 1
    ):
        raise RuntimeError("DEC-055 sizing-v0.1 is not valid-failed")
    failure = failures[0]
    if (
        failure.get("method_id"), failure.get("root_id"), failure.get("layout_id"),
        failure.get("exception_type"), failure.get("message")
    ) != ("dqn", "t527-size-r01", "gw-l1-a", "AttributeError", "'tuple' object has no attribute 'shape'"):
        raise RuntimeError("DEC-055 retained failure identity changed")

    return {
        "final_reserve_access": False,
        "immutable_t526_inputs": immutable,
        "tuning_v01": {
            "status": "valid-complete", "units": 180,
            "files": len(tuning_integrity["files"]),
            "bytes": sum(int(item["bytes"]) for item in tuning_integrity["files"].values()),
            "selection_sha256": _sha256_file(tuning / "selection.json"),
        },
        "sizing_v01": {
            "status": "valid-failed", "phase_a_units": 97, "matched_sets": 192,
            "files": len(failed_integrity["files"]),
            "bytes": sum(int(item["bytes"]) for item in failed_integrity["files"].values()),
            "failure": failure,
        },
    }


def _host() -> Mapping[str, Any]:
    result = {
        "platform_system": platform.system(), "platform_release": platform.release(),
        "platform_version": platform.version(), "machine": platform.machine(),
        "python_version": platform.python_version(),
        "python_executable_basename": Path(sys.executable).name, "cpu_count": os.cpu_count(),
    }
    if result["platform_system"] != "Windows" or sys.version_info[:2] != (3, 12):
        raise RuntimeError("DEC-056 sizing retry requires native Windows CPython 3.12")
    return result


def _horizon_audit(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    result: dict[str, Any] = {}
    for method_id in CORE_METHOD_IDS:
        result[method_id] = {}
        method_rows = [row for row in rows if row["method_id"] == method_id]
        for horizon in (256, 512):
            adaptive = [
                branch
                for row in method_rows
                for branch in row["horizons"][str(horizon)]
                if branch["branch"] in {"AN", "AD"}
            ]
            result[method_id][str(horizon)] = {
                "adaptive_branch_observations": len(adaptive),
                "minimum_native_update_opportunities_completed": min(
                    int(branch["metrics"]["native_update_opportunities_completed"])
                    for branch in adaptive
                ),
                "maximum_native_update_opportunities_completed": max(
                    int(branch["metrics"]["native_update_opportunities_completed"])
                    for branch in adaptive
                ),
                "minimum_episodes_completed": min(
                    int(branch["metrics"]["episodes_completed"]) for branch in adaptive
                ),
                "maximum_episodes_completed": max(
                    int(branch["metrics"]["episodes_completed"]) for branch in adaptive
                ),
            }
    return result


def run_sizing_retry(*, repo_root: Path, plan: Mapping[str, Any]) -> Path:
    historical = validate_historical_authority(repo_root=repo_root, plan=plan)
    output = _new_output(repo_root, str(plan["outputs"]["sizing"]))
    for filename in ("phase-a-sizing.jsonl", "phase-b-sizing.jsonl", "failures.jsonl"):
        (output / filename).write_text("", encoding="utf-8")
    base_manifest = {
        "schema_version": 1, "decision_id": "DEC-056",
        "source_decision_id": "DEC-055", "stage": "precision-runtime-sizing-retry",
        "scientific_status": plan["scientific_status"], "final_reserve_access": False,
        "plan_sha256": _sha256_value(plan), "execution_commit": _git_commit(repo_root),
        "host": _host(), "historical_authority_sha256": _sha256_value(historical),
        "expected_phase_a_units": EXPECTED_PHASE_A_UNITS,
        "expected_phase_b_matched_sets": EXPECTED_MATCHED_SETS,
        "started_unix_seconds": time.time(), "status": "in-progress",
    }
    _write_json(output / "historical-authority-validation.json", historical)
    _write_json(output / "manifest.json", base_manifest)
    phase_a_rows: list[Mapping[str, Any]] = []
    phase_b_rows: list[Mapping[str, Any]] = []
    budget = int(plan["tuning"]["selected_phase_a_budget"])
    probes = tuple(int(item) for item in plan["tuning"]["probe_interaction_indices"])
    for method_id in CORE_METHOD_IDS:
        parameters = plan["selected_configs"][method_id]
        for index in range(1, 25):
            root_data = _sizing_root(index)
            for layout in plan["development_layouts"]:
                driver = None
                try:
                    row, execution, driver = _run_phase_a_unit(
                        plan=plan, method_id=method_id, parameters=parameters,
                        root_data=root_data, layout=layout, budget=budget, probes=probes,
                        decision_id="DEC-056",
                        protocol_version="protocol-v2.0-t527-development-sizing-v0.2",
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
                    relative = Path("deployment-start-checkpoints") / method_id / root_data["root_id"] / f"{layout['layout_id']}.json"
                    target = output / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    _write_json(target, checkpoint)
                    row = {
                        **dict(row), "settlement": settlement.to_mapping(),
                        "deployment_start_checkpoint_path": relative.as_posix(),
                        "deployment_start_checkpoint_file_sha256": _sha256_file(target),
                    }
                    phase_a_rows.append(row)
                    _append_jsonl(output / "phase-a-sizing.jsonl", row)
                    for condition in plan["sizing"]["conditions"]:
                        wall_start = time.perf_counter()
                        phase_b = _run_sizing_phase_b(
                            plan=plan, method_id=method_id, parameters=parameters,
                            root_data=root_data, layout=layout, learner=learner.clone(),
                            condition=condition,
                        )
                        phase_b = {**dict(phase_b), "wall_seconds": time.perf_counter() - wall_start}
                        phase_b_rows.append(phase_b)
                        _append_jsonl(output / "phase-b-sizing.jsonl", phase_b)
                except Exception as exc:
                    failure = {
                        "stage": "sizing-retry", "method_id": method_id,
                        "root_id": root_data["root_id"], "layout_id": layout["layout_id"],
                        "exception_type": type(exc).__name__, "message": str(exc),
                    }
                    _append_jsonl(output / "failures.jsonl", failure)
                    _write_json(output / "manifest.json", {
                        **base_manifest, "status": "failed",
                        "completed_phase_a_units": len(phase_a_rows),
                        "completed_phase_b_matched_sets": len(phase_b_rows), "failure": failure,
                    })
                    _write_integrity(output)
                    raise
                finally:
                    if driver is not None:
                        _close_phase_a(driver)
    selection = dict(_sizing_selection(
        plan=plan, phase_a_rows=phase_a_rows, phase_b_rows=phase_b_rows,
        decision_id="DEC-056",
    ))
    selection["adaptive_horizon_audit"] = _horizon_audit(phase_b_rows)
    _write_json(output / "selection.json", selection)
    _write_json(output / "manifest.json", {
        **base_manifest, "status": "complete",
        "completed_phase_a_units": len(phase_a_rows),
        "completed_phase_b_matched_sets": len(phase_b_rows),
        "completed_branch_executions": len(phase_b_rows) * 4,
        "completed_branch_horizon_evaluations": len(phase_b_rows) * 4 * 2,
        "completed_unix_seconds": time.time(),
    })
    _write_integrity(output)
    return output


def validate_retry_attempt(*, repo_root: Path, plan: Mapping[str, Any]) -> Mapping[str, Any]:
    historical = validate_historical_authority(repo_root=repo_root, plan=plan)
    output = repo_root / str(plan["outputs"]["sizing"])
    integrity = _verify_integrity(output)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "complete" or manifest.get("final_reserve_access") is not False:
        raise RuntimeError("DEC-056 sizing-v0.2 is not valid-complete/non-final")
    phase_a = _read_jsonl(output / "phase-a-sizing.jsonl")
    phase_b = _read_jsonl(output / "phase-b-sizing.jsonl")
    failures = _read_jsonl(output / "failures.jsonl")
    if len(phase_a) != EXPECTED_PHASE_A_UNITS or len(phase_b) != EXPECTED_MATCHED_SETS or failures:
        raise RuntimeError("DEC-056 finite sizing denominator/failure mismatch")
    expected_units = {
        (method, f"t527-size-r{index:02d}", layout["layout_id"])
        for method in CORE_METHOD_IDS for index in range(1, 25)
        for layout in plan["development_layouts"]
    }
    if {(row["method_id"], row["root_id"], row["layout_id"]) for row in phase_a} != expected_units:
        raise RuntimeError("DEC-056 Phase-A unit identity matrix mismatch")
    expected_sets = {
        (*unit, condition["condition_id"])
        for unit in expected_units for condition in plan["sizing"]["conditions"]
    }
    if {(row["method_id"], row["root_id"], row["layout_id"], row["condition_id"]) for row in phase_b} != expected_sets:
        raise RuntimeError("DEC-056 Phase-B matched-set identity matrix mismatch")
    for row in phase_b:
        for horizon in ("256", "512"):
            branches = row["horizons"][horizon]
            if len(branches) != 4 or {item["branch"] for item in branches} != {"FN", "FD", "AN", "AD"}:
                raise RuntimeError("DEC-056 branch/horizon matrix mismatch")
            for branch in branches:
                if "native_update_opportunities_completed" not in branch["metrics"]:
                    raise RuntimeError("DEC-056 native update evidence missing")
                expected = 0 if branch["branch"] in {"FN", "FD"} else None
                if expected is not None and branch["metrics"]["native_update_opportunities_completed"] != expected:
                    raise RuntimeError("Frozen branch reported an adaptive update opportunity")
    selection = json.loads((output / "selection.json").read_text(encoding="utf-8"))
    recomputed = dict(_sizing_selection(
        plan=plan, phase_a_rows=phase_a, phase_b_rows=phase_b, decision_id="DEC-056"
    ))
    for key, value in recomputed.items():
        if selection.get(key) != value:
            raise RuntimeError(f"DEC-056 sizing selection mismatch: {key}")
    if selection.get("adaptive_horizon_audit") != _horizon_audit(phase_b):
        raise RuntimeError("DEC-056 adaptive horizon audit mismatch")
    return {
        "status": "valid-complete", "final_reserve_access": False,
        "historical_authority_sha256": _sha256_value(historical),
        "phase_a_units": len(phase_a), "matched_sets": len(phase_b),
        "branch_executions": len(phase_b) * 4,
        "branch_horizon_evaluations": len(phase_b) * 4 * 2,
        "files": len(integrity["files"]),
        "bytes": sum(int(item["bytes"]) for item in integrity["files"].values()),
        "selection": selection,
    }


def _shortest_path(layout: Mapping[str, Any]) -> int | None:
    width, height = int(layout["width"]), int(layout["height"])
    start, goal = tuple(layout["start"]), tuple(layout["goal"])
    blocked = {tuple(item) for item in layout["obstacles"]}
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, distance = queue.popleft()
        if state == goal:
            return distance
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nxt = (state[0] + dx, state[1] + dy)
            if 0 <= nxt[0] < width and 0 <= nxt[1] < height and nxt not in blocked and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, distance + 1))
    return None


def generate_final_layouts(plan: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """Materialize structural reserve inputs only; no learner is constructed."""
    rule = plan["final_freeze_rules"]["layout_generation"]
    if rule["agent_execution_permitted"] is not False:
        raise RuntimeError("final layout generation firewall is not closed")
    width, height = int(rule["width"]), int(rule["height"])
    start, goal = tuple(rule["start"]), tuple(rule["goal"])
    cells = [(x, y) for x in range(width) for y in range(height) if (x, y) not in {start, goal}]
    accepted: list[Mapping[str, Any]] = []
    seed = int(rule["candidate_seed_start"])
    while len(accepted) < int(rule["count"]):
        obstacles = sorted(random.Random(seed).sample(cells, int(rule["obstacle_count"])))
        layout = {
            "layout_id": f"gw-l1-final-{chr(ord('a') + len(accepted))}",
            "generation_seed": seed, "width": width, "height": height,
            "start": list(start), "goal": list(goal),
            "obstacles": [list(item) for item in obstacles],
            "shortest_path_length": int(rule["required_shortest_path_length"]),
            "max_steps": int(rule["max_steps"]),
        }
        distance = _shortest_path(layout)
        free_count = width * height - len(obstacles)
        connected = 0
        if distance is not None:
            probe = dict(layout)
            for cell in cells:
                if cell not in set(obstacles):
                    probe["goal"] = list(cell)
                    connected += int(_shortest_path(probe) is not None)
        if distance == rule["required_shortest_path_length"] and (
            not rule["require_all_free_cells_connected"] or connected == free_count - 2
        ):
            layout["spec_sha256"] = _sha256_value({key: value for key, value in layout.items() if key != "spec_sha256"})
            accepted.append(layout)
        seed += int(rule["candidate_seed_increment"])
        if seed - int(rule["candidate_seed_start"]) > 100000:
            raise RuntimeError("final layout structural generator exhausted bounded candidates")
    return accepted


def generate_final_roots(plan: Mapping[str, Any], count: int) -> list[Mapping[str, Any]]:
    if count not in tuple(int(item) for item in plan["sizing"]["root_count_candidates"]):
        raise ValueError("final root count must be a predeclared sizing candidate")
    return [
        {
            "root_id": f"t527-final-r{index:02d}",
            "initialization_seed": 71000 + index, "exploration_seed": 72000 + index,
            "scenario_seed": 73000 + index, "environment_seed": 74000 + index,
            "action_disturbance_seed": 75000 + index,
            "observation_disturbance_seed": 76000 + index,
        }
        for index in range(1, count + 1)
    ]


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="DEC-056 T-527 sizing-only retry")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default="configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json")
    parser.add_argument("--validate-inputs-only", action="store_true")
    parser.add_argument("--validate-attempt-only", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    plan = load_retry_plan((repo_root / args.config).resolve())
    if args.validate_inputs_only:
        result = validate_historical_authority(repo_root=repo_root, plan=plan)
    elif args.validate_attempt_only:
        result = validate_retry_attempt(repo_root=repo_root, plan=plan)
    else:
        result = {"sizing": str(run_sizing_retry(repo_root=repo_root, plan=plan))}
    print(_canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
