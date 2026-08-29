"""DEC-053 versioned T-526A recovery and unchanged Phase-B execution.

This implementation preserves both historical evidence trees.  Native project
methods retain DEC-052's raw-envelope identity.  SB3 methods instead require
the physically recorded historical learner fingerprint, explicit continuation
invariants, and an exact export/restore derived-identity round trip while
retaining both nonidentical raw envelope hashes as audit evidence.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from .protocol_v2 import ProtocolV2Branch, ScientificStateAdapter
from .protocol_v2_executor import execute_phase_b
from .protocol_v2_feasibility import CORE_METHOD_IDS, _canonical_json, _scenario, _sha256, load_plan
from .protocol_v2_prefix import prepare_shared_no_learning_prefix
from .protocol_v2_sb3 import SB3ScientificStateAdapter
from .protocol_v2_sb3_identity import (
    require_scientific_continuation_invariants,
    scientific_continuation_sha256,
)
from .protocol_v2_t526_phase_b import T526PPOTransientStateAdapter, t526_branch_driver
from .protocol_v2_t526_recovery import (
    EXPECTED_BRANCHES,
    EXPECTED_CONDITIONS,
    _append_jsonl,
    _authoritative_rows,
    _checkpoint_from_mapping,
    _checkpoint_relative_path,
    _close_phase_b_drivers,
    _file_sha256,
    _git_commit,
    _host_snapshot,
    _integrity_payload,
    _materialize_unit,
    _prefix_seed,
    _read_jsonl,
    _require_empty_or_absent,
    _restore_learner,
    _validate_integrity,
    _write_json,
    compare_reconstruction_row,
    load_amendment as load_dec052_amendment,
    require_complete_recovery_barrier,
    validate_phase_b_evidence,
    verify_original_bundle,
    verify_source_compatibility,
)
from .study.protocol_v2_phase_b_executor import _disturbed_spec


AMENDMENT_SCHEMA_VERSION = 2
NATIVE_METHOD_IDS = ("q_learning", "sarsa", "dyna_q_plus")
SB3_METHOD_IDS = ("dqn", "ppo")


def load_amendment(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "schema_version",
        "amendment_id",
        "pilot_id",
        "scientific_status",
        "purpose",
        "final_reserve_access",
        "required_host",
        "original_phase_a",
        "prior_failed_recovery",
        "source_compatibility",
        "identity_policy",
        "recovery",
        "phase_b",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ValueError("DEC-053 amendment configuration keys mismatch")
    if value["schema_version"] != AMENDMENT_SCHEMA_VERSION:
        raise ValueError("unsupported DEC-053 amendment schema_version")
    if value["amendment_id"] != "DEC-053":
        raise ValueError("T-526 v0.2 recovery must be governed by DEC-053")

    # Reuse every frozen DEC-052 design/denominator check after removing only
    # the two DEC-053 policy additions and substituting the historical header.
    legacy = {key: item for key, item in value.items() if key not in {
        "prior_failed_recovery",
        "identity_policy",
    }}
    legacy["schema_version"] = 1
    legacy["amendment_id"] = "DEC-052"
    with _temporary_json(legacy) as temporary:
        load_dec052_amendment(temporary)

    policy = value["identity_policy"]
    if policy != {
        "policy_id": "dec-053-scientific-continuation-identity-v1",
        "native_methods": list(NATIVE_METHOD_IDS),
        "sb3_methods": list(SB3_METHOD_IDS),
        "native_require_raw_checkpoint_envelope_sha256": True,
        "sb3_require_raw_checkpoint_envelope_sha256": False,
        "sb3_require_historical_learner_state_sha256": True,
        "sb3_require_post_restore_historical_learner_state_sha256": True,
        "sb3_require_derived_scientific_continuation_round_trip": True,
        "retain_original_and_reconstructed_raw_sha256": True,
    }:
        raise ValueError("DEC-053 identity policy changed")
    recovery = value["recovery"]
    if recovery["output_directory"] != (
        "results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2"
    ):
        raise ValueError("DEC-053 recovery output directory changed")
    if recovery["common_scientific_row_fields"] != [
        "status",
        "level_id",
        "layout_id",
        "root_id",
        "method_id",
        "implementation_id",
        "training_interactions",
        "probe_interactions",
        "learner_state_sha256",
        "probes",
    ]:
        raise ValueError("DEC-053 common scientific row fields changed")
    if recovery["native_additional_exact_row_fields"] != [
        "checkpoint_bytes",
        "checkpoint_sha256",
    ]:
        raise ValueError("DEC-053 native exact row fields changed")
    if value["phase_b"]["output_directory"] != (
        "results/pilots/protocol-v2-feasibility-phase-b-v0.2"
    ):
        raise ValueError("DEC-053 Phase-B output directory changed")
    return value


class _temporary_json:
    """Small no-repository-write adapter for the legacy configuration validator."""

    def __init__(self, value: Mapping[str, Any]) -> None:
        import tempfile

        self._directory = tempfile.TemporaryDirectory()
        self.path = Path(self._directory.name) / "amendment.json"
        self.path.write_text(json.dumps(value), encoding="utf-8")

    def __enter__(self) -> Path:
        return self.path

    def __exit__(self, *_: Any) -> None:
        self._directory.cleanup()


def verify_prior_failed_recovery(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, str]:
    prior = amendment["prior_failed_recovery"]
    if prior["decision_id"] != "DEC-052":
        raise ValueError("prior failed recovery must remain DEC-052")
    directory = repo_root / str(prior["evidence_directory"])
    actual = {}
    for relative, expected in prior["evidence_file_sha256"].items():
        path = directory / relative
        actual[str(relative)] = _file_sha256(path)
        if actual[str(relative)] != expected:
            raise RuntimeError(
                f"immutable DEC-052 failed evidence hash mismatch: {relative}"
            )
    return actual


def _identity_evidence(
    *,
    plan: Mapping[str, Any],
    layout: Mapping[str, Any],
    root_data: Mapping[str, Any],
    method_id: str,
    checkpoint_value: Mapping[str, Any],
    authoritative: Mapping[str, Any],
) -> Mapping[str, Any]:
    checkpoint = _checkpoint_from_mapping(checkpoint_value)
    if (
        checkpoint.method_id != method_id
        or checkpoint.root_id != root_data["root_id"]
        or checkpoint.layout_id != layout["layout_id"]
        or checkpoint.training_interaction_index
        != int(plan["phase_a"]["training_interaction_budget"])
    ):
        raise RuntimeError("reconstructed checkpoint scientific provenance mismatch")
    restored = _restore_learner(
        plan=plan,
        layout=layout,
        root_data=root_data,
        method_id=method_id,
        checkpoint=checkpoint,
    )
    expected_historical = str(authoritative["learner_state_sha256"])
    post_restore_historical = restored.state_sha256()
    clone = restored.clone()
    round_trip_historical = clone.state_sha256()
    evidence: dict[str, Any] = {
        "adapter_restore_passed": post_restore_historical == expected_historical,
        "post_restore_learner_state_sha256": post_restore_historical,
        "round_trip_learner_state_sha256": round_trip_historical,
        "round_trip_historical_identity_passed": round_trip_historical
        == expected_historical,
        "scientific_provenance_passed": True,
    }
    if method_id in SB3_METHOD_IDS:
        if not isinstance(restored, SB3ScientificStateAdapter) or not isinstance(
            clone, SB3ScientificStateAdapter
        ):
            raise RuntimeError("SB3 recovery did not restore through the project adapter")
        components = require_scientific_continuation_invariants(restored)
        derived = scientific_continuation_sha256(restored)
        round_trip_derived = scientific_continuation_sha256(clone)
        evidence.update(
            {
                "derived_identity_name": components["identity_name"],
                "scientific_continuation_sha256": derived,
                "round_trip_scientific_continuation_sha256": round_trip_derived,
                "derived_round_trip_passed": derived == round_trip_derived,
                "continuation_components": components,
            }
        )
    return evidence


def materialize_recovery(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    original_hashes = verify_original_bundle(repo_root=repo_root, amendment=amendment)
    prior_hashes = verify_prior_failed_recovery(repo_root=repo_root, amendment=amendment)
    verified_paths = verify_source_compatibility(repo_root=repo_root, amendment=amendment)
    plan = load_plan(repo_root / str(amendment["original_phase_a"]["plan_path"]))
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
        "schema_version": 2,
        "pilot_id": amendment["pilot_id"],
        "role": amendment["recovery"]["role"],
        "scientific_status": amendment["scientific_status"],
        "identity_policy_id": amendment["identity_policy"]["policy_id"],
        "final_reserve_access": False,
        "status": "in-progress",
        "source_phase_a_commit": amendment["original_phase_a"]["source_commit"],
        "recovery_implementation_commit": _git_commit(repo_root),
        "amendment_config_sha256": _sha256(amendment),
        "original_plan_sha256": amendment["original_phase_a"]["canonical_plan_sha256"],
        "original_evidence_file_sha256": original_hashes,
        "prior_failed_recovery_file_sha256": prior_hashes,
        "source_compatibility_paths": list(verified_paths),
        "started_unix_seconds": started,
        "host": _host_snapshot(),
        "expected_units": 30,
        "accepted_scientific_continuation_states": 0,
        "raw_checkpoint_mismatches": 0,
        "scientific_learner_fingerprint_mismatches": 0,
    }
    _write_json(manifest_path, manifest)
    authoritative_rows = _authoritative_rows(repo_root=repo_root, amendment=amendment)
    selected = next(
        level
        for level in plan["ordered_gridworld_ladder"]
        if level["level_id"] == "gw-l1"
    )
    common_fields = tuple(amendment["recovery"]["common_scientific_row_fields"])
    native_fields = common_fields + tuple(
        amendment["recovery"]["native_additional_exact_row_fields"]
    )
    accepted = 0
    raw_mismatches = 0
    learner_mismatches = 0
    try:
        for layout in selected["layouts"]:
            if int(layout["shortest_path_length"]) != 12:
                raise RuntimeError("selected gw-l1 shortest-path declaration changed")
            for root_data in plan["roots"]:
                for method_id in CORE_METHOD_IDS:
                    key = (method_id, str(root_data["root_id"]), str(layout["layout_id"]))
                    wall_start = time.perf_counter()
                    try:
                        row, checkpoint_value = _materialize_unit(
                            plan,
                            level_id="gw-l1",
                            layout=layout,
                            root_data=root_data,
                            method_id=method_id,
                        )
                        authoritative = authoritative_rows[key]
                        fields = native_fields if method_id in NATIVE_METHOD_IDS else common_fields
                        comparison = compare_reconstruction_row(
                            authoritative=authoritative,
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
                        _write_json(checkpoint_path, checkpoint_value)
                        identity = _identity_evidence(
                            plan=plan,
                            layout=layout,
                            root_data=root_data,
                            method_id=method_id,
                            checkpoint_value=checkpoint_value,
                            authoritative=authoritative,
                        )
                        raw_match = row["checkpoint_sha256"] == authoritative["checkpoint_sha256"]
                        learner_match = (
                            row["learner_state_sha256"]
                            == authoritative["learner_state_sha256"]
                        )
                        raw_mismatches += int(not raw_match)
                        learner_mismatches += int(not learner_match)
                        accepted_state = (
                            comparison["exact_match"]
                            and learner_match
                            and identity["adapter_restore_passed"]
                            and identity["round_trip_historical_identity_passed"]
                            and identity.get("derived_round_trip_passed", True)
                            and (raw_match if method_id in NATIVE_METHOD_IDS else True)
                        )
                        evidence = {
                            "method_id": method_id,
                            "root_id": root_data["root_id"],
                            "layout_id": layout["layout_id"],
                            "source_phase_a_commit": amendment["original_phase_a"]["source_commit"],
                            "identity_policy": (
                                "native-exact-envelope-and-learner"
                                if method_id in NATIVE_METHOD_IDS
                                else "sb3-exact-scientific-continuation"
                            ),
                            "accepted_scientific_continuation_state": accepted_state,
                            "original_raw_checkpoint_sha256": authoritative["checkpoint_sha256"],
                            "reconstructed_raw_checkpoint_sha256": row["checkpoint_sha256"],
                            "raw_checkpoint_sha256_match": raw_match,
                            "original_checkpoint_bytes": authoritative["checkpoint_bytes"],
                            "reconstructed_checkpoint_bytes": row["checkpoint_bytes"],
                            "original_historical_learner_state_sha256": authoritative[
                                "learner_state_sha256"
                            ],
                            "reconstructed_historical_learner_state_sha256": row[
                                "learner_state_sha256"
                            ],
                            "historical_learner_state_sha256_match": learner_match,
                            "checkpoint_path": relative.as_posix(),
                            "checkpoint_file_bytes": checkpoint_path.stat().st_size,
                            "checkpoint_file_sha256": _file_sha256(checkpoint_path),
                            "scientific_row_comparison": comparison,
                            "wall_seconds": time.perf_counter() - wall_start,
                            **identity,
                        }
                        _append_jsonl(records_path, evidence)
                        if not accepted_state:
                            _append_jsonl(
                                failures_path,
                                {
                                    "failure_kind": "infrastructure",
                                    "stage": "scientific-continuation-reconstruction",
                                    **evidence,
                                },
                            )
                            raise RuntimeError(
                                f"scientific continuation identity mismatch for {key}"
                            )
                        accepted += 1
                    except Exception as exc:
                        if not isinstance(exc, RuntimeError) or not str(exc).startswith(
                            "scientific continuation identity mismatch"
                        ):
                            _append_jsonl(
                                failures_path,
                                {
                                    "failure_kind": "infrastructure",
                                    "stage": "scientific-continuation-reconstruction",
                                    "method_id": method_id,
                                    "root_id": root_data["root_id"],
                                    "layout_id": layout["layout_id"],
                                    "exception_type": type(exc).__name__,
                                    "message": str(exc),
                                },
                            )
                        raise
        if accepted != 30:
            raise RuntimeError("the DEC-053 recovery barrier did not reach 30/30")
        verify_original_bundle(repo_root=repo_root, amendment=amendment)
        verify_prior_failed_recovery(repo_root=repo_root, amendment=amendment)
        manifest.update(
            {
                "status": "complete-barrier-passed",
                "exact_matches": accepted,
                "accepted_scientific_continuation_states": accepted,
                "raw_checkpoint_mismatches": raw_mismatches,
                "scientific_learner_fingerprint_mismatches": learner_mismatches,
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
                "status": "failed-barrier-blocks-phase-b",
                "exact_matches": accepted,
                "accepted_scientific_continuation_states": accepted,
                "raw_checkpoint_mismatches": raw_mismatches,
                "scientific_learner_fingerprint_mismatches": learner_mismatches,
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


def validate_recovery_attempt_evidence(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    verify_original_bundle(repo_root=repo_root, amendment=amendment)
    verify_prior_failed_recovery(repo_root=repo_root, amendment=amendment)
    directory = repo_root / str(amendment["recovery"]["output_directory"])
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    rows = _read_jsonl(directory / "reconstruction.jsonl")
    failures = _read_jsonl(directory / "failures.jsonl")
    accepted = sum(row["accepted_scientific_continuation_state"] is True for row in rows)
    if accepted != int(manifest["accepted_scientific_continuation_states"]):
        raise RuntimeError("DEC-053 accepted-state count does not reconcile")
    if len(rows) > 30:
        raise RuntimeError("DEC-053 recovery exceeds the 30-unit denominator")
    authoritative = _authoritative_rows(repo_root=repo_root, amendment=amendment)
    seen = set()
    for row in rows:
        key = (row["method_id"], row["root_id"], row["layout_id"])
        if key in seen:
            raise RuntimeError(f"duplicate DEC-053 recovery row: {key}")
        seen.add(key)
        source = authoritative[key]
        if row["original_raw_checkpoint_sha256"] != source["checkpoint_sha256"]:
            raise RuntimeError(f"original raw checkpoint identity changed: {key}")
        if row["original_historical_learner_state_sha256"] != source[
            "learner_state_sha256"
        ]:
            raise RuntimeError(f"original learner identity changed: {key}")
        path = directory / row["checkpoint_path"]
        if _file_sha256(path) != row["checkpoint_file_sha256"]:
            raise RuntimeError(f"DEC-053 checkpoint file hash mismatch: {key}")
        checkpoint = _checkpoint_from_mapping(json.loads(path.read_text(encoding="utf-8")))
        if checkpoint.sha256 != row["reconstructed_raw_checkpoint_sha256"]:
            raise RuntimeError(f"DEC-053 reconstructed raw identity mismatch: {key}")
        if row["method_id"] in NATIVE_METHOD_IDS and not row[
            "raw_checkpoint_sha256_match"
        ]:
            raise RuntimeError(f"native method lost exact raw identity: {key}")
        required = (
            row["scientific_row_comparison"]["exact_match"]
            and row["scientific_provenance_passed"]
            and row["historical_learner_state_sha256_match"]
            and row["adapter_restore_passed"]
            and row["round_trip_historical_identity_passed"]
            and row.get("derived_round_trip_passed", True)
            and (
                row["raw_checkpoint_sha256_match"]
                if row["method_id"] in NATIVE_METHOD_IDS
                else True
            )
        )
        if row["accepted_scientific_continuation_state"] is not bool(required):
            raise RuntimeError(f"DEC-053 identity result does not reconcile: {key}")
    integrity = _validate_integrity(directory)
    status = str(manifest["status"])
    if status == "complete-barrier-passed":
        if len(rows) != 30 or accepted != 30 or failures:
            raise RuntimeError("DEC-053 successful evidence lacks the 30/30 barrier")
    elif status == "failed-barrier-blocks-phase-b":
        if len(rows) >= 30 or not failures:
            raise RuntimeError("DEC-053 failed evidence lacks a retained barrier failure")
    else:
        raise RuntimeError(f"unsupported DEC-053 recovery status: {status!r}")
    return {
        "status": "valid-complete" if status == "complete-barrier-passed" else "valid-failed-barrier",
        "attempt_status": status,
        "rows_attempted": len(rows),
        "accepted_scientific_continuation_states": accepted,
        "raw_checkpoint_mismatches": sum(
            row["raw_checkpoint_sha256_match"] is False for row in rows
        ),
        "scientific_learner_fingerprint_mismatches": sum(
            row["historical_learner_state_sha256_match"] is False for row in rows
        ),
        "failures": len(failures),
        "checkpoint_files": len(rows),
        "artifact_files": integrity["total_files"],
        "artifact_bytes": integrity["total_bytes"],
    }


def validate_recovery_evidence(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    result = validate_recovery_attempt_evidence(repo_root=repo_root, amendment=amendment)
    if result["attempt_status"] != "complete-barrier-passed":
        raise RuntimeError("DEC-053 recovery evidence does not prove the 30/30 barrier")
    return result


def run_phase_b(
    *, repo_root: Path, amendment: Mapping[str, Any]
) -> Mapping[str, Any]:
    """Execute the unchanged DEC-052 Phase-B design after the DEC-053 barrier."""

    verify_original_bundle(repo_root=repo_root, amendment=amendment)
    verify_prior_failed_recovery(repo_root=repo_root, amendment=amendment)
    recovery_dir = repo_root / str(amendment["recovery"]["output_directory"])
    recovery_manifest = json.loads(
        (recovery_dir / "manifest.json").read_text(encoding="utf-8")
    )
    require_complete_recovery_barrier(recovery_manifest)
    validate_recovery_evidence(repo_root=repo_root, amendment=amendment)
    recovery_rows = {
        (row["method_id"], row["root_id"], row["layout_id"]): row
        for row in _read_jsonl(recovery_dir / "reconstruction.jsonl")
    }

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
        "schema_version": 2,
        "pilot_id": amendment["pilot_id"],
        "scientific_status": amendment["scientific_status"],
        "identity_policy_id": amendment["identity_policy"]["policy_id"],
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
                    recovered = recovery_rows[key]
                    if recovered["accepted_scientific_continuation_state"] is not True:
                        raise RuntimeError(f"Phase B received an unaccepted source state: {key}")
                    relative = _checkpoint_relative_path(
                        amendment,
                        method_id=method_id,
                        root_id=str(root_data["root_id"]),
                        layout_id=str(layout["layout_id"]),
                    )
                    checkpoint = _checkpoint_from_mapping(
                        json.loads((recovery_dir / relative).read_text(encoding="utf-8"))
                    )
                    if checkpoint.sha256 != recovered[
                        "reconstructed_raw_checkpoint_sha256"
                    ]:
                        raise RuntimeError(f"Phase-B reconstructed checkpoint mismatch: {key}")
                    if method_id in NATIVE_METHOD_IDS and checkpoint.sha256 != expected_rows[
                        key
                    ]["checkpoint_sha256"]:
                        raise RuntimeError(f"Phase-B native exact checkpoint mismatch: {key}")

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
                            if learner.state_sha256() != expected_rows[key][
                                "learner_state_sha256"
                            ]:
                                raise RuntimeError(
                                    f"Phase-B restored learner identity mismatch: {key}"
                                )
                            if method_id in SB3_METHOD_IDS:
                                if not isinstance(learner, SB3ScientificStateAdapter):
                                    raise RuntimeError(
                                        f"Phase-B SB3 adapter type mismatch: {key}"
                                    )
                                if scientific_continuation_sha256(learner) != recovered[
                                    "scientific_continuation_sha256"
                                ]:
                                    raise RuntimeError(
                                        f"Phase-B derived continuation identity mismatch: {key}"
                                    )
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
                                    raise RuntimeError(
                                        "PPO prefix did not retain the project adapter"
                                    )
                                source_learner = T526PPOTransientStateAdapter(source_learner)
                            disturbed = _disturbed_spec(
                                nominal=nominal,
                                condition=condition,
                                onset_step=1,
                            )

                            def factory(
                                branch: ProtocolV2Branch,
                                adaptive: bool,
                                branch_learner: ScientificStateAdapter,
                                environment: Any,
                            ) -> Any:
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
                            _append_jsonl(
                                sets_path,
                                {
                                    "status": "completed",
                                    "method_id": method_id,
                                    "root_id": root_data["root_id"],
                                    "layout_id": layout["layout_id"],
                                    "condition_id": condition["condition_id"],
                                    "condition_family": condition["family"],
                                    "condition_specification": condition["specification"],
                                    "source_checkpoint_path": relative.as_posix(),
                                    "source_original_raw_checkpoint_sha256": recovered[
                                        "original_raw_checkpoint_sha256"
                                    ],
                                    "source_reconstructed_raw_checkpoint_sha256": checkpoint.sha256,
                                    "source_learner_state_sha256": expected_rows[key][
                                        "learner_state_sha256"
                                    ],
                                    "prefix_interactions": 1,
                                    "branch_point_learner_sha256": execution.branch_point_learner_sha256,
                                    "branch_point_environment_sha256": execution.branch_point_environment_sha256,
                                    "post_boundary_interactions_per_branch": 10,
                                    "episode_resets": False,
                                    "branches": branches,
                                    "wall_seconds": wall,
                                },
                            )
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
        verify_prior_failed_recovery(repo_root=repo_root, amendment=amendment)
        _write_json(
            output / "denominators.json",
            {
                "schema_version": 2,
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
            },
        )
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


def run_physical_recovery_and_phase_b(
    *, repo_root: Path, amendment_path: Path
) -> Mapping[str, Any]:
    amendment = load_amendment(amendment_path)
    _host_snapshot()
    recovery = materialize_recovery(repo_root=repo_root, amendment=amendment)
    if recovery["status"] != "complete-barrier-passed":
        raise RuntimeError("Phase B blocked by incomplete DEC-053 recovery")
    phase_b = run_phase_b(repo_root=repo_root, amendment=amendment)
    return {
        "status": "complete",
        "recovery": validate_recovery_evidence(repo_root=repo_root, amendment=amendment),
        "phase_b": validate_phase_b_evidence(repo_root=repo_root, amendment=amendment),
        "phase_b_runtime": {
            "wall_seconds": phase_b["wall_seconds"],
            "wall_seconds_by_method": phase_b["wall_seconds_by_method"],
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run reviewed DEC-053 T-526A recovery and bounded Phase-B calibration."
    )
    parser.add_argument(
        "--amendment",
        default="configs/protocols/protocol-v2-t526-recovery-phase-b-v0.2.json",
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--validate-recovery-attempt-only", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    amendment_path = (repo_root / args.amendment).resolve()
    amendment = load_amendment(amendment_path)
    if args.validate_only and args.validate_recovery_attempt_only:
        parser.error("validation modes are mutually exclusive")
    if args.validate_recovery_attempt_only:
        result = {
            "recovery": validate_recovery_attempt_evidence(
                repo_root=repo_root, amendment=amendment
            )
        }
    elif args.validate_only:
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
            repo_root=repo_root, amendment_path=amendment_path
        )
    print(_canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
