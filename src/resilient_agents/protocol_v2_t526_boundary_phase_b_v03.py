"""DEC-054 boundary settlement and fresh T-526 Phase-B v0.3 execution.

The module consumes the immutable, valid-complete DEC-053 recovery checkpoints.
It never regenerates Phase A or recovery.  It first derives 30 quiescent
deployment-start states using zero environment interactions, then requires the
complete settlement barrier before starting a fresh 240-set Phase-B matrix.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from .protocol_v2 import ProtocolV2Branch, ScientificStateAdapter
from .protocol_v2_boundary_settlement import (
    CORE_METHOD_IDS,
    SETTLEMENT_POLICY_ID,
    require_quiescent_deployment_state,
    settle_phase_a_interaction_boundary,
)
from .protocol_v2_executor import execute_phase_b
from .protocol_v2_feasibility import _canonical_json, _scenario, _sha256, load_plan
from .protocol_v2_prefix import prepare_shared_no_learning_prefix
from .protocol_v2_sb3 import SB3ScientificStateAdapter
from .protocol_v2_sb3_identity import scientific_continuation_sha256
from .protocol_v2_t526_phase_b import T526PPOTransientStateAdapter, t526_branch_driver
from .protocol_v2_t526_recovery import (
    EXPECTED_BRANCHES,
    _append_jsonl,
    _authoritative_rows,
    _checkpoint_from_mapping,
    _close_phase_b_drivers,
    _file_sha256,
    _git_commit,
    _host_snapshot,
    _integrity_payload,
    _prefix_seed,
    _read_jsonl,
    _require_empty_or_absent,
    _restore_learner,
    _validate_integrity,
    _write_json,
)
from .protocol_v2_t526_recovery_v02 import (
    load_amendment as load_dec053_amendment,
    validate_phase_b_attempt_evidence as validate_dec053_phase_b_attempt,
    validate_recovery_evidence as validate_dec053_recovery,
)
from .study.protocol_v2_phase_b_executor import _disturbed_spec


CONFIG_SCHEMA_VERSION = 1
DECISION_ID = "DEC-054"
SETTLEMENT_CHECKPOINT_SCHEMA_VERSION = 1
PILOT_ID = "protocol-v2-t526-boundary-settlement-phase-b-v0.3"
SCIENTIFIC_STATUS = (
    "non-final-feasibility-boundary-settlement-and-calibration-only"
)
PURPOSE = (
    "Derive quiescent deployment-start states by completing only algorithmic "
    "bookkeeping attributable to the already-consumed final Phase-A interaction, "
    "then execute one fresh unchanged T-526 Phase-B matrix"
)
REQUIRED_HOST = {
    "os": "Windows 10",
    "architecture": "AMD64",
    "python": "3.12",
    "execution_baseline": "cpu-only",
}


def load_config(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "schema_version",
        "decision_id",
        "pilot_id",
        "scientific_status",
        "purpose",
        "final_reserve_access",
        "required_host",
        "prior_dec053",
        "settlement",
        "phase_b",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ValueError("DEC-054 configuration keys mismatch")
    if value["schema_version"] != CONFIG_SCHEMA_VERSION:
        raise ValueError("unsupported DEC-054 configuration schema")
    if (
        value["decision_id"] != DECISION_ID
        or value["pilot_id"] != PILOT_ID
        or value["scientific_status"] != SCIENTIFIC_STATUS
        or value["purpose"] != PURPOSE
        or value["required_host"] != REQUIRED_HOST
        or value["final_reserve_access"] is not False
    ):
        raise ValueError("DEC-054 identity/final-reserve firewall changed")
    prior = value["prior_dec053"]
    if set(prior) != {
        "amendment_path",
        "amendment_file_sha256",
        "recovery_directory",
        "recovery_file_sha256",
        "failed_phase_b_directory",
        "failed_phase_b_file_sha256",
    }:
        raise ValueError("DEC-054 prior DEC-053 lineage keys mismatch")
    settlement = value["settlement"]
    if settlement != {
        "policy_id": SETTLEMENT_POLICY_ID,
        "output_directory": "results/pilots/protocol-v2-feasibility-boundary-settlement-v0.1",
        "checkpoint_path_template": "deployment-start-checkpoints/{method_id}/{root_id}/{layout_id}.json",
        "source_training_interactions": 2048,
        "required_accepted_states": 30,
        "required_environment_interactions_per_state": 0,
        "method_policy": {
            "q_learning": "verified-quiescent-no-op",
            "sarsa": "behavior-policy-bootstrap-final-consumed-transition-or-quiescent-no-op",
            "dqn": "verified-quiescent-no-op",
            "ppo": "verified-completed-rollout-update-boundary-no-op",
            "dyna_q_plus": "verified-quiescent-no-op",
        },
        "idempotence": "already-quiescent-state-is-an-explicit-no-op; physical lineage always begins from the exact accepted DEC-053 source SHA",
    }:
        raise ValueError("DEC-054 settlement contract changed")
    phase_b = value["phase_b"]
    if phase_b["output_directory"] != "results/pilots/protocol-v2-feasibility-phase-b-v0.3":
        raise ValueError("DEC-054 Phase-B output path changed")
    if phase_b["expected_prefix_interactions"] != 240:
        raise ValueError("DEC-054 Phase-B prefix denominator changed")
    return value


def _dec053_authority(
    *, repo_root: Path, config: Mapping[str, Any]
) -> tuple[Mapping[str, Any], Path]:
    prior = config["prior_dec053"]
    amendment_path = repo_root / str(prior["amendment_path"])
    if _file_sha256(amendment_path) != prior["amendment_file_sha256"]:
        raise RuntimeError("immutable DEC-053 amendment hash mismatch")
    amendment = load_dec053_amendment(amendment_path)
    current = dict(config["phase_b"])
    current.pop("output_directory")
    current.pop("expected_prefix_interactions")
    historical = dict(amendment["phase_b"])
    historical.pop("output_directory")
    if current != historical:
        raise RuntimeError("DEC-054 changed the frozen DEC-053 Phase-B design")
    return amendment, amendment_path


def verify_immutable_inputs(
    *, repo_root: Path, config: Mapping[str, Any]
) -> Mapping[str, Any]:
    """Verify original, DEC-052, DEC-053 recovery and failed Phase-B evidence."""

    amendment, amendment_path = _dec053_authority(repo_root=repo_root, config=config)
    recovery_validation = validate_dec053_recovery(
        repo_root=repo_root, amendment=amendment
    )
    phase_b_validation = validate_dec053_phase_b_attempt(
        repo_root=repo_root, amendment=amendment
    )
    if recovery_validation["accepted_scientific_continuation_states"] != 30:
        raise RuntimeError("DEC-053 recovery is not valid-complete 30/30")
    if phase_b_validation["status"] != "valid-failed":
        raise RuntimeError("DEC-053 failed Phase-B evidence changed status")
    prior = config["prior_dec053"]
    for directory_key, hashes_key in (
        ("recovery_directory", "recovery_file_sha256"),
        ("failed_phase_b_directory", "failed_phase_b_file_sha256"),
    ):
        directory = repo_root / str(prior[directory_key])
        for relative, expected in prior[hashes_key].items():
            if _file_sha256(directory / relative) != expected:
                raise RuntimeError(
                    f"immutable DEC-053 evidence hash mismatch: {directory.name}/{relative}"
                )
    return {
        "dec053_amendment_path": amendment_path.relative_to(repo_root).as_posix(),
        "dec053_amendment_file_sha256": _file_sha256(amendment_path),
        "recovery": recovery_validation,
        "failed_phase_b": phase_b_validation,
    }


def _selected_inputs(
    *, repo_root: Path, config: Mapping[str, Any]
) -> tuple[
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Mapping[str, Any]],
    Mapping[str, Mapping[str, Any]],
    Mapping[tuple[str, str, str], Mapping[str, Any]],
]:
    amendment, _ = _dec053_authority(repo_root=repo_root, config=config)
    plan = load_plan(repo_root / str(amendment["original_phase_a"]["plan_path"]))
    level = next(
        item
        for item in plan["ordered_gridworld_ladder"]
        if item["level_id"] == config["phase_b"]["selected_level_id"]
    )
    layouts = {str(item["layout_id"]): item for item in level["layouts"]}
    roots = {str(item["root_id"]): item for item in plan["roots"]}
    recovery_dir = repo_root / str(config["prior_dec053"]["recovery_directory"])
    recovery_rows = {
        (str(row["method_id"]), str(row["root_id"]), str(row["layout_id"])): row
        for row in _read_jsonl(recovery_dir / "reconstruction.jsonl")
    }
    if len(recovery_rows) != 30:
        raise RuntimeError("DEC-053 recovery row matrix is not 30 unique states")
    return amendment, plan, layouts, roots, recovery_rows


def _valid_observations(layout: Mapping[str, Any]) -> frozenset[tuple[int, int]]:
    obstacles = {tuple(item) for item in layout["obstacles"]}
    return frozenset(
        (x, y)
        for x in range(int(layout["width"]))
        for y in range(int(layout["height"]))
        if (x, y) not in obstacles
    )


def _source_checkpoint(
    *,
    repo_root: Path,
    config: Mapping[str, Any],
    plan: Mapping[str, Any],
    layout: Mapping[str, Any],
    root_data: Mapping[str, Any],
    method_id: str,
    recovery_row: Mapping[str, Any],
) -> tuple[ScientificStateAdapter, Path]:
    recovery_dir = repo_root / str(config["prior_dec053"]["recovery_directory"])
    path = recovery_dir / str(recovery_row["checkpoint_path"])
    if _file_sha256(path) != recovery_row["checkpoint_file_sha256"]:
        raise RuntimeError("DEC-053 source checkpoint file hash mismatch")
    checkpoint = _checkpoint_from_mapping(json.loads(path.read_text(encoding="utf-8")))
    if checkpoint.sha256 != recovery_row["reconstructed_raw_checkpoint_sha256"]:
        raise RuntimeError("DEC-053 source checkpoint envelope mismatch")
    learner = _restore_learner(
        plan=plan,
        layout=layout,
        root_data=root_data,
        method_id=method_id,
        checkpoint=checkpoint,
    )
    expected = recovery_row["reconstructed_historical_learner_state_sha256"]
    if learner.state_sha256() != expected:
        raise RuntimeError("DEC-053 source learner SHA mismatch")
    if method_id in {"dqn", "ppo"}:
        if not isinstance(learner, SB3ScientificStateAdapter):
            raise RuntimeError("DEC-054 expected SB3 source adapter")
        if scientific_continuation_sha256(learner) != recovery_row[
            "scientific_continuation_sha256"
        ]:
            raise RuntimeError("DEC-053 source derived continuation mismatch")
    return learner, path


def _settlement_checkpoint_relative(
    config: Mapping[str, Any], *, method_id: str, root_id: str, layout_id: str
) -> Path:
    template = str(config["settlement"]["checkpoint_path_template"])
    return Path(
        template.format(method_id=method_id, root_id=root_id, layout_id=layout_id)
    )


def _settle_source(
    *,
    repo_root: Path,
    config: Mapping[str, Any],
    plan: Mapping[str, Any],
    layout: Mapping[str, Any],
    root_data: Mapping[str, Any],
    method_id: str,
    recovery_row: Mapping[str, Any],
) -> tuple[ScientificStateAdapter, Mapping[str, Any]]:
    learner, _ = _source_checkpoint(
        repo_root=repo_root,
        config=config,
        plan=plan,
        layout=layout,
        root_data=root_data,
        method_id=method_id,
        recovery_row=recovery_row,
    )
    result = settle_phase_a_interaction_boundary(
        learner,
        expected_source_learner_sha256=recovery_row[
            "reconstructed_historical_learner_state_sha256"
        ],
        expected_interactions=int(config["settlement"]["source_training_interactions"]),
        valid_observations=_valid_observations(layout),
    )
    return learner, result.to_mapping()


def _deployment_checkpoint_mapping(
    *,
    learner: ScientificStateAdapter,
    settlement: Mapping[str, Any],
    recovery_row: Mapping[str, Any],
    execution_commit: str,
    root_id: str,
    layout_id: str,
) -> Mapping[str, Any]:
    return {
        "schema_version": SETTLEMENT_CHECKPOINT_SCHEMA_VERSION,
        "role": "dec-054-boundary-settled-deployment-start",
        "decision_id": DECISION_ID,
        "settlement_policy_id": SETTLEMENT_POLICY_ID,
        "execution_authority_commit": execution_commit,
        "method_id": learner.method_id,
        "root_id": root_id,
        "layout_id": layout_id,
        "source_recovery_checkpoint_path": recovery_row["checkpoint_path"],
        "source_recovery_checkpoint_file_sha256": recovery_row[
            "checkpoint_file_sha256"
        ],
        "source_historical_learner_state_sha256": recovery_row[
            "reconstructed_historical_learner_state_sha256"
        ],
        "pre_settlement_learner_state_sha256": settlement[
            "pre_learner_state_sha256"
        ],
        "post_settlement_learner_state_sha256": settlement[
            "post_learner_state_sha256"
        ],
        "source_training_interactions": 2048,
        "settlement_environment_interactions": 0,
        "state": learner.export_state(),
    }


def materialize_boundary_settlement(
    *, repo_root: Path, config: Mapping[str, Any]
) -> Mapping[str, Any]:
    input_validation = verify_immutable_inputs(repo_root=repo_root, config=config)
    _, plan, layouts, roots, recovery_rows = _selected_inputs(
        repo_root=repo_root, config=config
    )
    output = repo_root / str(config["settlement"]["output_directory"])
    _require_empty_or_absent(output)
    output.mkdir(parents=True, exist_ok=True)
    rows_path = output / "settlement.jsonl"
    failures_path = output / "failures.jsonl"
    rows_path.write_text("", encoding="utf-8")
    failures_path.write_text("", encoding="utf-8")
    manifest_path = output / "manifest.json"
    started = time.time()
    execution_commit = _git_commit(repo_root)
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "pilot_id": config["pilot_id"],
        "role": "dec-054-zero-interaction-boundary-settlement",
        "scientific_status": config["scientific_status"],
        "decision_id": DECISION_ID,
        "settlement_policy_id": SETTLEMENT_POLICY_ID,
        "final_reserve_access": False,
        "status": "in-progress",
        "execution_authority_commit": execution_commit,
        "config_sha256": _sha256(config),
        "dec053_recovery_manifest_sha256": config["prior_dec053"][
            "recovery_file_sha256"
        ]["manifest.json"],
        "dec053_recovery_integrity_sha256": config["prior_dec053"][
            "recovery_file_sha256"
        ]["integrity.json"],
        "dec053_failed_phase_b_integrity_sha256": config["prior_dec053"][
            "failed_phase_b_file_sha256"
        ]["integrity.json"],
        "host": _host_snapshot(),
        "started_unix_seconds": started,
        "expected_states": 30,
        "accepted_states": 0,
        "environment_interactions_consumed": 0,
        "non_noop_sarsa_states": 0,
    }
    _write_json(manifest_path, manifest)
    accepted = 0
    non_noop_sarsa = 0
    try:
        for layout_id, layout in layouts.items():
            for root_id, root_data in roots.items():
                for method_id in CORE_METHOD_IDS:
                    key = (method_id, root_id, layout_id)
                    recovery_row = recovery_rows[key]
                    wall_started = time.perf_counter()
                    try:
                        learner, settlement = _settle_source(
                            repo_root=repo_root,
                            config=config,
                            plan=plan,
                            layout=layout,
                            root_data=root_data,
                            method_id=method_id,
                            recovery_row=recovery_row,
                        )
                        replay_learner, replay = _settle_source(
                            repo_root=repo_root,
                            config=config,
                            plan=plan,
                            layout=layout,
                            root_data=root_data,
                            method_id=method_id,
                            recovery_row=recovery_row,
                        )
                        if settlement != replay or learner.state_sha256() != replay_learner.state_sha256():
                            raise RuntimeError("boundary settlement is not deterministic")
                        post_sha = learner.state_sha256()
                        clone = learner.clone()
                        if clone.state_sha256() != post_sha:
                            raise RuntimeError("settled learner round trip changed state")
                        require_quiescent_deployment_state(
                            clone,
                            expected_interactions=int(
                                config["settlement"]["source_training_interactions"]
                            ),
                        )
                        checkpoint_relative = _settlement_checkpoint_relative(
                            config,
                            method_id=method_id,
                            root_id=root_id,
                            layout_id=layout_id,
                        )
                        checkpoint_path = output / checkpoint_relative
                        checkpoint_mapping = _deployment_checkpoint_mapping(
                            learner=learner,
                            settlement=settlement,
                            recovery_row=recovery_row,
                            execution_commit=execution_commit,
                            root_id=root_id,
                            layout_id=layout_id,
                        )
                        _write_json(checkpoint_path, checkpoint_mapping)
                        no_op = bool(settlement["no_op"])
                        non_noop_sarsa += int(method_id == "sarsa" and not no_op)
                        row = {
                            "status": "accepted",
                            "method_id": method_id,
                            "root_id": root_id,
                            "layout_id": layout_id,
                            "source_recovery_checkpoint_path": recovery_row[
                                "checkpoint_path"
                            ],
                            "source_recovery_checkpoint_file_sha256": recovery_row[
                                "checkpoint_file_sha256"
                            ],
                            "source_recovery_raw_checkpoint_sha256": recovery_row[
                                "reconstructed_raw_checkpoint_sha256"
                            ],
                            "source_historical_learner_state_sha256": recovery_row[
                                "reconstructed_historical_learner_state_sha256"
                            ],
                            "settlement_policy": config["settlement"][
                                "method_policy"
                            ][method_id],
                            "settlement": settlement,
                            "learner_state_sha256_identical": settlement[
                                "pre_learner_state_sha256"
                            ]
                            == settlement["post_learner_state_sha256"],
                            "deterministic_replay_passed": True,
                            "round_trip_restore_passed": True,
                            "post_settlement_quiescent": True,
                            "deployment_start_checkpoint_path": checkpoint_relative.as_posix(),
                            "deployment_start_checkpoint_sha256": _sha256(
                                checkpoint_mapping
                            ),
                            "deployment_start_checkpoint_file_sha256": _file_sha256(
                                checkpoint_path
                            ),
                            "deployment_start_checkpoint_file_bytes": checkpoint_path.stat().st_size,
                            "decision_id": DECISION_ID,
                            "config_sha256": _sha256(config),
                            "execution_authority_commit": execution_commit,
                            "wall_seconds": time.perf_counter() - wall_started,
                        }
                        _append_jsonl(rows_path, row)
                        accepted += 1
                    except Exception as exc:
                        _append_jsonl(
                            failures_path,
                            {
                                "failure_kind": "infrastructure",
                                "stage": "boundary-settlement",
                                "method_id": method_id,
                                "root_id": root_id,
                                "layout_id": layout_id,
                                "exception_type": type(exc).__name__,
                                "message": str(exc),
                            },
                        )
                        raise
        if accepted != 30:
            raise RuntimeError("DEC-054 settlement barrier did not reach 30/30")
        verify_immutable_inputs(repo_root=repo_root, config=config)
        manifest.update(
            {
                "status": "complete-barrier-passed",
                "accepted_states": accepted,
                "environment_interactions_consumed": 0,
                "non_noop_sarsa_states": non_noop_sarsa,
                "completed_unix_seconds": time.time(),
                "wall_seconds": time.time() - started,
                "input_validation": input_validation,
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
                "accepted_states": accepted,
                "environment_interactions_consumed": 0,
                "non_noop_sarsa_states": non_noop_sarsa,
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


def _validate_deployment_checkpoint(
    *,
    path: Path,
    row: Mapping[str, Any],
    source_learner: ScientificStateAdapter,
    expected_interactions: int,
) -> ScientificStateAdapter:
    value = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "schema_version",
        "role",
        "decision_id",
        "settlement_policy_id",
        "execution_authority_commit",
        "method_id",
        "root_id",
        "layout_id",
        "source_recovery_checkpoint_path",
        "source_recovery_checkpoint_file_sha256",
        "source_historical_learner_state_sha256",
        "pre_settlement_learner_state_sha256",
        "post_settlement_learner_state_sha256",
        "source_training_interactions",
        "settlement_environment_interactions",
        "state",
    }
    if set(value) != expected:
        raise RuntimeError("deployment-start checkpoint keys mismatch")
    if (
        value["schema_version"] != SETTLEMENT_CHECKPOINT_SCHEMA_VERSION
        or value["role"] != "dec-054-boundary-settled-deployment-start"
        or value["decision_id"] != DECISION_ID
        or value["settlement_policy_id"] != SETTLEMENT_POLICY_ID
        or value["settlement_environment_interactions"] != 0
        or value["source_training_interactions"] != expected_interactions
    ):
        raise RuntimeError("deployment-start checkpoint contract mismatch")
    if (
        source_learner.state_sha256()
        != value["source_historical_learner_state_sha256"]
    ):
        raise RuntimeError("deployment-start checkpoint source learner mismatch")
    if _sha256(value) != row["deployment_start_checkpoint_sha256"]:
        raise RuntimeError("deployment-start checkpoint scientific envelope mismatch")
    if _file_sha256(path) != row["deployment_start_checkpoint_file_sha256"]:
        raise RuntimeError("deployment-start checkpoint file hash mismatch")
    source_learner.restore_state(value["state"])
    if source_learner.state_sha256() != value["post_settlement_learner_state_sha256"]:
        raise RuntimeError("deployment-start learner restore mismatch")
    require_quiescent_deployment_state(
        source_learner, expected_interactions=expected_interactions
    )
    return source_learner


def validate_settlement_evidence(
    *, repo_root: Path, config: Mapping[str, Any]
) -> Mapping[str, Any]:
    verify_immutable_inputs(repo_root=repo_root, config=config)
    _, plan, layouts, roots, recovery_rows = _selected_inputs(
        repo_root=repo_root, config=config
    )
    output = repo_root / str(config["settlement"]["output_directory"])
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    rows = _read_jsonl(output / "settlement.jsonl")
    failures = _read_jsonl(output / "failures.jsonl")
    if len(rows) != 30 or failures:
        raise RuntimeError("DEC-054 settlement evidence is not a complete 30/30 barrier")
    observed: set[tuple[str, str, str]] = set()
    non_noop_sarsa = 0
    expected_config_sha = _sha256(config)
    for row in rows:
        key = (row["method_id"], row["root_id"], row["layout_id"])
        if key in observed or key not in recovery_rows:
            raise RuntimeError("DEC-054 settlement matrix identity mismatch")
        observed.add(key)
        recovery_row = recovery_rows[key]
        if (
            row["decision_id"] != DECISION_ID
            or row["config_sha256"] != expected_config_sha
            or row["execution_authority_commit"]
            != manifest["execution_authority_commit"]
            or row["settlement_policy"]
            != config["settlement"]["method_policy"][row["method_id"]]
            or row["source_recovery_checkpoint_path"]
            != recovery_row["checkpoint_path"]
            or row["source_recovery_raw_checkpoint_sha256"]
            != recovery_row["reconstructed_raw_checkpoint_sha256"]
            or row["source_historical_learner_state_sha256"]
            != recovery_row["reconstructed_historical_learner_state_sha256"]
        ):
            raise RuntimeError("settlement authority/source lineage mismatch")
        learner, expected_settlement = _settle_source(
            repo_root=repo_root,
            config=config,
            plan=plan,
            layout=layouts[row["layout_id"]],
            root_data=roots[row["root_id"]],
            method_id=row["method_id"],
            recovery_row=recovery_row,
        )
        if row["settlement"] != expected_settlement:
            raise RuntimeError(f"settlement evidence does not replay exactly: {key}")
        if row["source_recovery_checkpoint_file_sha256"] != recovery_row[
            "checkpoint_file_sha256"
        ]:
            raise RuntimeError("settlement source lineage mismatch")
        relative = Path(row["deployment_start_checkpoint_path"])
        source_learner, _ = _source_checkpoint(
            repo_root=repo_root,
            config=config,
            plan=plan,
            layout=layouts[row["layout_id"]],
            root_data=roots[row["root_id"]],
            method_id=row["method_id"],
            recovery_row=recovery_row,
        )
        restored = _validate_deployment_checkpoint(
            path=output / relative,
            row=row,
            source_learner=source_learner,
            expected_interactions=int(
                config["settlement"]["source_training_interactions"]
            ),
        )
        if restored.state_sha256() != learner.state_sha256():
            raise RuntimeError("settlement checkpoint differs from deterministic replay")
        checkpoint_value = json.loads(
            (output / relative).read_text(encoding="utf-8")
        )
        if (
            checkpoint_value["method_id"] != row["method_id"]
            or checkpoint_value["root_id"] != row["root_id"]
            or checkpoint_value["layout_id"] != row["layout_id"]
            or checkpoint_value["execution_authority_commit"]
            != row["execution_authority_commit"]
            or checkpoint_value["source_recovery_checkpoint_path"]
            != row["source_recovery_checkpoint_path"]
            or checkpoint_value["source_recovery_checkpoint_file_sha256"]
            != row["source_recovery_checkpoint_file_sha256"]
            or checkpoint_value["source_historical_learner_state_sha256"]
            != row["source_historical_learner_state_sha256"]
            or checkpoint_value["pre_settlement_learner_state_sha256"]
            != row["settlement"]["pre_learner_state_sha256"]
            or checkpoint_value["post_settlement_learner_state_sha256"]
            != row["settlement"]["post_learner_state_sha256"]
        ):
            raise RuntimeError("deployment-start checkpoint lineage mismatch")
        non_noop_sarsa += int(
            row["method_id"] == "sarsa" and not row["settlement"]["no_op"]
        )
        if row["settlement"]["environment_interactions_consumed"] != 0:
            raise RuntimeError("settlement evidence consumed an environment interaction")
    if (
        manifest["pilot_id"] != PILOT_ID
        or manifest["scientific_status"] != SCIENTIFIC_STATUS
        or manifest["decision_id"] != DECISION_ID
        or manifest["settlement_policy_id"] != SETTLEMENT_POLICY_ID
        or manifest["final_reserve_access"] is not False
        or manifest["config_sha256"] != expected_config_sha
        or manifest["status"] != "complete-barrier-passed"
        or manifest["accepted_states"] != 30
        or manifest["environment_interactions_consumed"] != 0
        or manifest["non_noop_sarsa_states"] != non_noop_sarsa
    ):
        raise RuntimeError("DEC-054 settlement manifest does not reconcile")
    integrity = _validate_integrity(output)
    return {
        "status": "valid-complete",
        "accepted_states": 30,
        "non_noop_sarsa_states": non_noop_sarsa,
        "environment_interactions_consumed": 0,
        "failures": 0,
        "artifact_files": integrity["total_files"],
        "artifact_bytes": integrity["total_bytes"],
    }


def _settlement_rows(
    *, repo_root: Path, config: Mapping[str, Any]
) -> Mapping[tuple[str, str, str], Mapping[str, Any]]:
    output = repo_root / str(config["settlement"]["output_directory"])
    rows = {
        (row["method_id"], row["root_id"], row["layout_id"]): row
        for row in _read_jsonl(output / "settlement.jsonl")
    }
    if len(rows) != 30:
        raise RuntimeError("Phase B requires 30 unique settled states")
    return rows


def _restore_deployment_learner(
    *,
    repo_root: Path,
    config: Mapping[str, Any],
    plan: Mapping[str, Any],
    layout: Mapping[str, Any],
    root_data: Mapping[str, Any],
    recovery_row: Mapping[str, Any],
    settlement_row: Mapping[str, Any],
) -> ScientificStateAdapter:
    learner, _ = _source_checkpoint(
        repo_root=repo_root,
        config=config,
        plan=plan,
        layout=layout,
        root_data=root_data,
        method_id=settlement_row["method_id"],
        recovery_row=recovery_row,
    )
    settlement_dir = repo_root / str(config["settlement"]["output_directory"])
    return _validate_deployment_checkpoint(
        path=settlement_dir / settlement_row["deployment_start_checkpoint_path"],
        row=settlement_row,
        source_learner=learner,
        expected_interactions=int(config["settlement"]["source_training_interactions"]),
    )


def run_phase_b_v03(
    *, repo_root: Path, config: Mapping[str, Any]
) -> Mapping[str, Any]:
    verify_immutable_inputs(repo_root=repo_root, config=config)
    settlement_validation = validate_settlement_evidence(
        repo_root=repo_root, config=config
    )
    if settlement_validation["accepted_states"] != 30:
        raise RuntimeError("Phase-B v0.3 blocked by incomplete settlement barrier")
    _, plan, layouts, roots, recovery_rows = _selected_inputs(
        repo_root=repo_root, config=config
    )
    settlement_rows = _settlement_rows(repo_root=repo_root, config=config)
    output = repo_root / str(config["phase_b"]["output_directory"])
    _require_empty_or_absent(output)
    output.mkdir(parents=True, exist_ok=True)
    sets_path = output / "matched-sets.jsonl"
    failures_path = output / "failures.jsonl"
    sets_path.write_text("", encoding="utf-8")
    failures_path.write_text("", encoding="utf-8")
    manifest_path = output / "manifest.json"
    started = time.time()
    settlement_dir = repo_root / str(config["settlement"]["output_directory"])
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "pilot_id": config["pilot_id"],
        "scientific_status": config["scientific_status"],
        "decision_id": DECISION_ID,
        "settlement_policy_id": SETTLEMENT_POLICY_ID,
        "final_reserve_access": False,
        "status": "in-progress",
        "config_sha256": _sha256(config),
        "settlement_manifest_sha256": _file_sha256(settlement_dir / "manifest.json"),
        "settlement_integrity_sha256": _file_sha256(settlement_dir / "integrity.json"),
        "execution_commit": _git_commit(repo_root),
        "host": _host_snapshot(),
        "started_unix_seconds": started,
        "expected_matched_sets": 240,
        "completed_matched_sets": 0,
        "expected_branch_executions": 960,
        "completed_branch_executions": 0,
        "expected_prefix_interactions": 240,
        "completed_prefix_interactions": 0,
        "expected_post_boundary_interactions": 9600,
        "completed_post_boundary_interactions": 0,
    }
    _write_json(manifest_path, manifest)
    completed_sets = 0
    branches_total = 0
    prefix_interactions = 0
    post_interactions = 0
    branch_points: dict[tuple[str, str, str], tuple[str, str]] = {}
    wall_by_method: dict[str, float] = {method: 0.0 for method in CORE_METHOD_IDS}
    try:
        for layout_id, layout in layouts.items():
            if int(layout["shortest_path_length"]) != 12:
                raise RuntimeError("gw-l1 no-reset shortest-path safety failed")
            nominal = _scenario(plan, layout)
            for root_id, root_data in roots.items():
                for method_id in CORE_METHOD_IDS:
                    key = (method_id, root_id, layout_id)
                    recovery_row = recovery_rows[key]
                    settlement_row = settlement_rows[key]
                    for condition in config["phase_b"]["conditions"]:
                        set_started = time.perf_counter()
                        prefix = None
                        created_drivers: list[Any] = []
                        try:
                            learner = _restore_deployment_learner(
                                repo_root=repo_root,
                                config=config,
                                plan=plan,
                                layout=layout,
                                root_data=root_data,
                                recovery_row=recovery_row,
                                settlement_row=settlement_row,
                            )
                            prefix = prepare_shared_no_learning_prefix(
                                learner=learner,
                                nominal_spec=nominal,
                                environment_seeds=_prefix_seed(
                                    root_data, layout_id=layout_id
                                ),
                                interactions=1,
                            )
                            source_learner: ScientificStateAdapter = prefix.learner
                            if method_id == "ppo":
                                if not isinstance(source_learner, SB3ScientificStateAdapter):
                                    raise RuntimeError("PPO prefix lost SB3 adapter")
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
                                    f"condition-specific prefix/fork state detected: {key}"
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
                                raise RuntimeError("Phase-B branch ordering changed")
                            if any(item["interactions"] != 10 for item in branches):
                                raise RuntimeError("Phase-B branch interaction budget changed")
                            wall = time.perf_counter() - set_started
                            wall_by_method[method_id] += wall
                            _append_jsonl(
                                sets_path,
                                {
                                    "status": "completed",
                                    "method_id": method_id,
                                    "root_id": root_id,
                                    "layout_id": layout_id,
                                    "condition_id": condition["condition_id"],
                                    "condition_family": condition["family"],
                                    "condition_specification": condition["specification"],
                                    "source_recovery_checkpoint_path": recovery_row[
                                        "checkpoint_path"
                                    ],
                                    "source_historical_learner_state_sha256": recovery_row[
                                        "reconstructed_historical_learner_state_sha256"
                                    ],
                                    "deployment_start_checkpoint_path": settlement_row[
                                        "deployment_start_checkpoint_path"
                                    ],
                                    "deployment_start_checkpoint_sha256": settlement_row[
                                        "deployment_start_checkpoint_sha256"
                                    ],
                                    "pre_settlement_learner_state_sha256": settlement_row[
                                        "settlement"
                                    ]["pre_learner_state_sha256"],
                                    "post_settlement_learner_state_sha256": settlement_row[
                                        "settlement"
                                    ]["post_learner_state_sha256"],
                                    "settlement_no_op": settlement_row["settlement"][
                                        "no_op"
                                    ],
                                    "settlement_environment_interactions": 0,
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
                            branches_total += 4
                            prefix_interactions += 1
                            post_interactions += 40
                        except Exception as exc:
                            _append_jsonl(
                                failures_path,
                                {
                                    "failure_kind": "infrastructure",
                                    "stage": "phase-b-v0.3-matched-set",
                                    "method_id": method_id,
                                    "root_id": root_id,
                                    "layout_id": layout_id,
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
        if (
            completed_sets != 240
            or branches_total != 960
            or prefix_interactions != 240
            or post_interactions != 9600
        ):
            raise RuntimeError("Phase-B v0.3 final denominator accounting failed")
        verify_immutable_inputs(repo_root=repo_root, config=config)
        validate_settlement_evidence(repo_root=repo_root, config=config)
        _write_json(
            output / "denominators.json",
            {
                "schema_version": 1,
                "planned_matched_sets": 240,
                "completed_matched_sets": completed_sets,
                "scientific_failure_matched_sets": 0,
                "infrastructure_failure_matched_sets": 0,
                "planned_branch_executions": 960,
                "completed_branch_executions": branches_total,
                "planned_prefix_interactions": 240,
                "completed_prefix_interactions": prefix_interactions,
                "planned_post_boundary_interactions": 9600,
                "completed_post_boundary_interactions": post_interactions,
                "methods": list(CORE_METHOD_IDS),
                "roots": list(roots),
                "layouts": list(layouts),
                "conditions": [
                    item["condition_id"] for item in config["phase_b"]["conditions"]
                ],
                "branches": list(EXPECTED_BRANCHES),
            },
        )
        manifest.update(
            {
                "status": "complete",
                "completed_matched_sets": completed_sets,
                "completed_branch_executions": branches_total,
                "completed_prefix_interactions": prefix_interactions,
                "completed_post_boundary_interactions": post_interactions,
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
                "completed_branch_executions": branches_total,
                "completed_prefix_interactions": prefix_interactions,
                "completed_post_boundary_interactions": post_interactions,
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


def _planned_phase_b_keys(
    *, config: Mapping[str, Any], layouts: Mapping[str, Any], roots: Mapping[str, Any]
) -> list[tuple[str, str, str, str]]:
    return [
        (method_id, root_id, layout_id, condition["condition_id"])
        for layout_id in layouts
        for root_id in roots
        for method_id in CORE_METHOD_IDS
        for condition in config["phase_b"]["conditions"]
    ]


def validate_phase_b_v03_attempt(
    *, repo_root: Path, config: Mapping[str, Any]
) -> Mapping[str, Any]:
    verify_immutable_inputs(repo_root=repo_root, config=config)
    validate_settlement_evidence(repo_root=repo_root, config=config)
    _, _, layouts, roots, _ = _selected_inputs(repo_root=repo_root, config=config)
    settlement_rows = _settlement_rows(repo_root=repo_root, config=config)
    output = repo_root / str(config["phase_b"]["output_directory"])
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    settlement_manifest = json.loads(
        (
            repo_root
            / str(config["settlement"]["output_directory"])
            / "manifest.json"
        ).read_text(encoding="utf-8")
    )
    if (
        manifest["pilot_id"] != PILOT_ID
        or manifest["scientific_status"] != SCIENTIFIC_STATUS
        or manifest["decision_id"] != DECISION_ID
        or manifest["settlement_policy_id"] != SETTLEMENT_POLICY_ID
        or manifest["final_reserve_access"] is not False
        or manifest["config_sha256"] != _sha256(config)
        or manifest["execution_commit"]
        != settlement_manifest["execution_authority_commit"]
        or manifest["settlement_manifest_sha256"]
        != _file_sha256(
            repo_root
            / str(config["settlement"]["output_directory"])
            / "manifest.json"
        )
    ):
        raise RuntimeError("Phase-B v0.3 execution authority lineage mismatch")
    rows = _read_jsonl(output / "matched-sets.jsonl")
    failures = _read_jsonl(output / "failures.jsonl")
    planned = _planned_phase_b_keys(config=config, layouts=layouts, roots=roots)
    observed: list[tuple[str, str, str, str]] = []
    branch_points: dict[tuple[str, str, str], tuple[str, str]] = {}
    post_interactions = 0
    for row in rows:
        key = (
            row["method_id"],
            row["root_id"],
            row["layout_id"],
            row["condition_id"],
        )
        observed.append(key)
        settlement = settlement_rows[key[:3]]
        if (
            row["deployment_start_checkpoint_sha256"]
            != settlement["deployment_start_checkpoint_sha256"]
            or row["post_settlement_learner_state_sha256"]
            != settlement["settlement"]["post_learner_state_sha256"]
            or row["settlement_environment_interactions"] != 0
        ):
            raise RuntimeError("Phase-B v0.3 settlement lineage mismatch")
        if row["prefix_interactions"] != 1 or row["episode_resets"] is not False:
            raise RuntimeError("Phase-B v0.3 prefix/reset contract mismatch")
        branches = row["branches"]
        if tuple(item["branch"] for item in branches) != EXPECTED_BRANCHES:
            raise RuntimeError("Phase-B v0.3 branch assignment mismatch")
        if any(item["interactions"] != 10 for item in branches):
            raise RuntimeError("Phase-B v0.3 branch budget mismatch")
        post_interactions += sum(item["interactions"] for item in branches)
        branch_point = (
            row["branch_point_learner_sha256"],
            row["branch_point_environment_sha256"],
        )
        previous = branch_points.setdefault(key[:3], branch_point)
        if previous != branch_point:
            raise RuntimeError("Phase-B v0.3 condition-specific branch point")
    if observed != planned[: len(observed)]:
        raise RuntimeError("Phase-B v0.3 rows are not a contiguous fresh plan prefix")
    if (
        manifest["completed_matched_sets"] != len(rows)
        or manifest["completed_branch_executions"] != len(rows) * 4
        or manifest["completed_prefix_interactions"] != len(rows)
        or manifest["completed_post_boundary_interactions"] != post_interactions
    ):
        raise RuntimeError("Phase-B v0.3 manifest counts do not reconcile")
    if manifest["status"] == "complete":
        if len(rows) != 240 or failures:
            raise RuntimeError("complete Phase-B v0.3 evidence is not 240/240")
        denominators = json.loads(
            (output / "denominators.json").read_text(encoding="utf-8")
        )
        if (
            denominators["completed_matched_sets"] != 240
            or denominators["completed_branch_executions"] != 960
            or denominators["completed_prefix_interactions"] != 240
            or denominators["completed_post_boundary_interactions"] != 9600
        ):
            raise RuntimeError("Phase-B v0.3 denominators changed")
        status = "valid-complete"
    elif manifest["status"] == "failed":
        if len(rows) >= 240 or len(failures) != 1:
            raise RuntimeError("failed Phase-B v0.3 evidence lacks one failure")
        failure = failures[0]
        failure_key = (
            failure["method_id"],
            failure["root_id"],
            failure["layout_id"],
            failure["condition_id"],
        )
        if (
            failure_key != planned[len(rows)]
            or failure["failure_kind"] != "infrastructure"
            or failure["stage"] != "phase-b-v0.3-matched-set"
        ):
            raise RuntimeError("Phase-B v0.3 retained failure identity mismatch")
        status = "valid-failed"
    else:
        raise RuntimeError("unsupported Phase-B v0.3 attempt status")
    integrity = _validate_integrity(output)
    return {
        "status": status,
        "attempt_status": manifest["status"],
        "matched_sets": len(rows),
        "branch_executions": len(rows) * 4,
        "prefix_interactions": len(rows),
        "post_boundary_interactions": post_interactions,
        "scientific_failures": int(manifest.get("scientific_failures", 0)),
        "infrastructure_failures": len(failures),
        "artifact_files": integrity["total_files"],
        "artifact_bytes": integrity["total_bytes"],
    }


def run_physical_settlement_and_phase_b(
    *, repo_root: Path, config: Mapping[str, Any]
) -> Mapping[str, Any]:
    _host_snapshot()
    settlement = materialize_boundary_settlement(repo_root=repo_root, config=config)
    if settlement["status"] != "complete-barrier-passed":
        raise RuntimeError("Phase-B v0.3 blocked by DEC-054 settlement failure")
    phase_b = run_phase_b_v03(repo_root=repo_root, config=config)
    return {
        "status": "complete",
        "settlement": validate_settlement_evidence(
            repo_root=repo_root, config=config
        ),
        "phase_b": validate_phase_b_v03_attempt(
            repo_root=repo_root, config=config
        ),
        "phase_b_runtime": {
            "wall_seconds": phase_b["wall_seconds"],
            "wall_seconds_by_method": phase_b["wall_seconds_by_method"],
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run reviewed DEC-054 settlement and fresh T-526 Phase-B v0.3."
    )
    parser.add_argument(
        "--config",
        default="configs/protocols/protocol-v2-t526-boundary-settlement-phase-b-v0.3.json",
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--validate-inputs-only", action="store_true")
    parser.add_argument("--validate-settlement-only", action="store_true")
    parser.add_argument("--validate-attempt-only", action="store_true")
    args = parser.parse_args(argv)
    if sum(
        int(item)
        for item in (
            args.validate_inputs_only,
            args.validate_settlement_only,
            args.validate_attempt_only,
        )
    ) > 1:
        parser.error("validation modes are mutually exclusive")
    repo_root = Path(args.repo_root).resolve()
    config = load_config((repo_root / args.config).resolve())
    if args.validate_inputs_only:
        result = {"inputs": verify_immutable_inputs(repo_root=repo_root, config=config)}
    elif args.validate_settlement_only:
        result = {
            "settlement": validate_settlement_evidence(
                repo_root=repo_root, config=config
            )
        }
    elif args.validate_attempt_only:
        result = {
            "settlement": validate_settlement_evidence(
                repo_root=repo_root, config=config
            ),
            "phase_b": validate_phase_b_v03_attempt(
                repo_root=repo_root, config=config
            ),
        }
    else:
        result = run_physical_settlement_and_phase_b(
            repo_root=repo_root, config=config
        )
    print(_canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
