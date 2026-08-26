"""Deterministic finalized-bundle analysis and pilot diagnostics."""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from statistics import fmean, stdev
from typing import Any

from .agents import TabularQLearningAgent, TabularQLearningConfig
from .contracts import ProtocolStage
from .experiment_runner import (
    HEADLESS_RUNNER_SCHEMA_VERSION,
    HeadlessExperimentRequest,
    HeadlessExperimentRunner,
)
from .git_publish import FINAL_STATUSES, validate_finalized_run
from .gridworld import ACTION_NAMES
from .metrics import compute_resilience_metrics
from .pilot_protocol import PilotProtocol
from .run_bundle import sha256_file, source_provenance

ANALYSIS_SCHEMA_VERSION = 1
ANALYSIS_FINALIZATION_MARKER = "FINALIZED"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _reject_nonfinite_json(value: str) -> None:
    raise ValueError(f"non-finite JSON number is forbidden: {value}")


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "value") and isinstance(value.value, str):
        return value.value
    return value


def _read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), parse_constant=_reject_nonfinite_json
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON object: {path}") from exc
    if not isinstance(value, dict):
        raise TypeError(f"JSON value must be an object: {path}")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], *, field: str) -> None:
    if set(value) != expected:
        raise ValueError(
            f"{field} keys mismatch; "
            f"missing={sorted(expected - set(value))}, unknown={sorted(set(value) - expected)}"
        )


def _finite_series(value: Any, *, field: str, length: int) -> tuple[float, ...]:
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"{field} must have exactly {length} values")
    result: list[float] = []
    for item in value:
        if not isinstance(item, (int, float)) or isinstance(item, bool):
            raise TypeError(f"{field} must be numeric")
        converted = float(item)
        if not math.isfinite(converted):
            raise ValueError(f"{field} must be finite")
        result.append(converted)
    return tuple(result)


def _git_commit(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _canonical_json(payload: Any) -> str:
    return json.dumps(
        _jsonable(payload),
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _metric_payload(metrics: Any) -> dict[str, Any]:
    return _jsonable(asdict(metrics))


def _sensitivity_id(
    *,
    immediate_window: int,
    worst_window: int,
    terminal_window: int,
    recovery_tolerance: float,
    recovery_stability_steps: int,
) -> str:
    payload = {
        "immediate_window": immediate_window,
        "worst_window": worst_window,
        "terminal_window": terminal_window,
        "recovery_tolerance": float(recovery_tolerance),
        "recovery_stability_steps": recovery_stability_steps,
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class DerivedRunRecords:
    inventory: Mapping[str, Any]
    units: Sequence[Mapping[str, Any]]
    sensitivity: Sequence[Mapping[str, Any]]


@dataclass(frozen=True)
class AnalysisResult:
    analysis_dir: Path
    unit_count: int
    sensitivity_record_count: int


def derive_completed_run_records(
    *,
    run_id: str,
    manifest: Mapping[str, Any],
    resolved_config: Mapping[str, Any],
    summary: Mapping[str, Any],
    repo_root: Path,
) -> DerivedRunRecords:
    """Revalidate one completed runner summary and derive all sensitivity rows."""

    _exact_keys(
        resolved_config,
        {
            "headless_runner_schema_version",
            "entrypoint",
            "seed_derivation",
            "protocol",
            "request",
        },
        field="resolved_config",
    )
    if (
        resolved_config["headless_runner_schema_version"]
        != HEADLESS_RUNNER_SCHEMA_VERSION
    ):
        raise ValueError("unsupported headless runner schema")
    if resolved_config["entrypoint"] != "resilient_agents.experiment_runner.v1":
        raise ValueError("unknown scientific execution entrypoint")
    protocol = PilotProtocol.from_dict(resolved_config["protocol"])
    request = HeadlessExperimentRequest.from_dict(resolved_config["request"])
    HeadlessExperimentRunner(repo_root=repo_root, protocol=protocol, request=request)
    if manifest.get("protocol_version") != protocol.protocol_version:
        raise ValueError("manifest and resolved protocol versions differ")
    if manifest.get("stage") != request.stage.value:
        raise ValueError("manifest and request stages differ")
    _exact_keys(
        summary,
        {
            "status",
            "protocol_version",
            "stage",
            "layout_id",
            "condition_id",
            "completed_root_count",
            "requested_root_count",
            "root_results",
        },
        field="completed summary",
    )
    expected_summary_identity = {
        "status": "completed",
        "protocol_version": protocol.protocol_version,
        "stage": request.stage.value,
        "layout_id": request.layout_id,
        "condition_id": request.condition_id,
        "completed_root_count": len(request.root_seeds),
        "requested_root_count": len(request.root_seeds),
    }
    if any(
        summary.get(key) != value for key, value in expected_summary_identity.items()
    ):
        raise ValueError("completed summary identity/counts are inconsistent")
    root_results = summary["root_results"]
    if not isinstance(root_results, list) or [
        item.get("root_seed") if isinstance(item, Mapping) else None
        for item in root_results
    ] != list(request.root_seeds):
        raise ValueError("root results do not exactly match the requested seed order")

    metric_spec = protocol.to_dict()["metric_sensitivity"]
    total_episodes = request.pre_change_episodes + request.post_change_episodes
    training_layouts = (
        tuple(protocol.to_dict()["partitions"]["tuning"])
        if request.stage in {ProtocolStage.TUNING, ProtocolStage.PILOT}
        else (request.layout_id,)
    )
    units: list[dict[str, Any]] = []
    sensitivity: list[dict[str, Any]] = []
    for root_result in root_results:
        _exact_keys(
            root_result,
            {
                "root_seed",
                "training_episode_returns",
                "common_q_checkpoint",
                "common_q_checkpoint_sha256",
                "agent_results",
            },
            field="root result",
        )
        root_seed = root_result["root_seed"]
        training = root_result["training_episode_returns"]
        if not isinstance(training, Mapping) or tuple(training) != training_layouts:
            raise ValueError("training curves do not match the permitted layout order")
        for layout_id in training_layouts:
            _finite_series(
                training[layout_id],
                field=f"training curve {layout_id}",
                length=request.training_episodes_per_layout,
            )
        checkpoint = root_result["common_q_checkpoint"]
        checkpoint_audit = TabularQLearningAgent(
            TabularQLearningConfig(
                agent_id="analysis-checkpoint-audit",
                actions=ACTION_NAMES,
                learning_rate=float(request.q_learning_rate),
                discount_factor=float(request.discount_factor),
                exploration_epsilon=float(request.exploration_epsilon),
                learning_enabled=False,
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=checkpoint,
        )
        if (
            checkpoint_audit.checkpoint_sha256()
            != root_result["common_q_checkpoint_sha256"]
        ):
            raise ValueError("common Q checkpoint checksum is inconsistent")
        agent_results = root_result["agent_results"]
        if not isinstance(agent_results, list) or [
            item.get("agent_id") if isinstance(item, Mapping) else None
            for item in agent_results
        ] != list(request.agent_ids):
            raise ValueError("agent results do not exactly match the request order")
        for agent_result in agent_results:
            _exact_keys(
                agent_result,
                {
                    "agent_id",
                    "reference_episode_returns",
                    "observed_episode_returns",
                    "metrics",
                    "reference_final_state_sha256",
                    "observed_final_state_sha256",
                },
                field="agent result",
            )
            agent_id = agent_result["agent_id"]
            reference = _finite_series(
                agent_result["reference_episode_returns"],
                field="reference curve",
                length=total_episodes,
            )
            observed = _finite_series(
                agent_result["observed_episode_returns"],
                field="observed curve",
                length=total_episodes,
            )
            if (
                observed[: request.pre_change_episodes]
                != reference[: request.pre_change_episodes]
            ):
                raise ValueError("stored branches diverge before the change boundary")
            for field in (
                "reference_final_state_sha256",
                "observed_final_state_sha256",
            ):
                if not isinstance(agent_result[field], str) or not _SHA256_RE.fullmatch(
                    agent_result[field]
                ):
                    raise ValueError(f"{field} must be a SHA-256 digest")
            common_checkpoint_sha = root_result["common_q_checkpoint_sha256"]
            if agent_id == "f0" and (
                agent_result["reference_final_state_sha256"] != common_checkpoint_sha
                or agent_result["observed_final_state_sha256"] != common_checkpoint_sha
            ):
                raise ValueError("frozen-agent state changed during evaluation")
            primary = compute_resilience_metrics(
                observed,
                reference_values=reference,
                change_index=request.pre_change_episodes,
                immediate_window=request.immediate_window,
                worst_window=request.worst_window,
                terminal_window=request.terminal_window,
                recovery_tolerance=float(request.recovery_tolerance),
                recovery_stability_steps=request.recovery_stability_episodes,
            )
            primary_payload = _metric_payload(primary)
            if agent_result["metrics"] != primary_payload:
                raise ValueError("stored primary metrics do not reproduce exactly")
            unit_id = f"{run_id}:{root_seed}:{agent_id}"
            units.append(
                {
                    "unit_id": unit_id,
                    "run_id": run_id,
                    "protocol_version": protocol.protocol_version,
                    "stage": request.stage.value,
                    "layout_id": request.layout_id,
                    "condition_id": request.condition_id,
                    "root_seed": root_seed,
                    "agent_id": agent_id,
                    "starting_state_type": (
                        "common_q_checkpoint"
                        if agent_id in {"f0", "c0"}
                        else "planner_config"
                    ),
                    "starting_scientific_state_sha256": (
                        common_checkpoint_sha if agent_id in {"f0", "c0"} else None
                    ),
                    "reference_final_state_sha256": agent_result[
                        "reference_final_state_sha256"
                    ],
                    "observed_final_state_sha256": agent_result[
                        "observed_final_state_sha256"
                    ],
                    "reference_episode_returns": list(reference),
                    "observed_episode_returns": list(observed),
                    "primary_metrics": primary_payload,
                }
            )
            for immediate in metric_spec["immediate_windows"]:
                for worst in metric_spec["worst_windows"]:
                    for terminal in metric_spec["terminal_windows"]:
                        for tolerance in metric_spec[
                            "recovery_tolerances_step_reward_units"
                        ]:
                            for stability in metric_spec["recovery_stability_episodes"]:
                                metrics = compute_resilience_metrics(
                                    observed,
                                    reference_values=reference,
                                    change_index=request.pre_change_episodes,
                                    immediate_window=immediate,
                                    worst_window=worst,
                                    terminal_window=terminal,
                                    recovery_tolerance=float(tolerance),
                                    recovery_stability_steps=stability,
                                )
                                sensitivity.append(
                                    {
                                        "unit_id": unit_id,
                                        "run_id": run_id,
                                        "layout_id": request.layout_id,
                                        "condition_id": request.condition_id,
                                        "root_seed": root_seed,
                                        "agent_id": agent_id,
                                        "sensitivity_id": _sensitivity_id(
                                            immediate_window=immediate,
                                            worst_window=worst,
                                            terminal_window=terminal,
                                            recovery_tolerance=float(tolerance),
                                            recovery_stability_steps=stability,
                                        ),
                                        "parameters": {
                                            "immediate_window": immediate,
                                            "worst_window": worst,
                                            "terminal_window": terminal,
                                            "recovery_tolerance": float(tolerance),
                                            "recovery_stability_steps": stability,
                                        },
                                        "metrics": _metric_payload(metrics),
                                    }
                                )
    inventory = {
        "run_id": run_id,
        "status": "completed",
        "protocol_version": manifest.get("protocol_version"),
        "stage": manifest.get("stage"),
        "source_git_commit": manifest.get("source", {}).get("git_commit"),
        "unit_count": len(units),
    }
    return DerivedRunRecords(inventory=inventory, units=units, sensitivity=sensitivity)


def _event_diagnostics(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "events.jsonl"
    if not path.exists():
        return {"event_count": 0, "episode_attempt_count": 0}
    events = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid events JSON at line {number}") from exc
        if not isinstance(event, dict):
            raise TypeError(f"event line {number} must be an object")
        events.append(event)
    episodes = [event for event in events if event.get("event") == "episode_completed"]
    lengths = [float(event["length"]) for event in episodes]
    returns = [float(event["return"]) for event in episodes]
    return {
        "event_count": len(events),
        "episode_attempt_count": len(episodes),
        "episode_outcome_counts": dict(
            sorted(Counter(event.get("outcome") for event in episodes).items())
        ),
        "episode_phase_counts": dict(
            sorted(Counter(event.get("phase") for event in episodes).items())
        ),
        "mean_attempt_episode_length": None if not lengths else fmean(lengths),
        "mean_attempt_episode_return": None if not returns else fmean(returns),
        "root_started_count": sum(
            event.get("event") == "root_started" for event in events
        ),
        "root_completed_count": sum(
            event.get("event") == "root_completed" for event in events
        ),
    }


def _wall_clock_seconds(manifest: Mapping[str, Any]) -> float:
    try:
        started = datetime.fromisoformat(str(manifest["started_at_utc"]))
        finished = datetime.fromisoformat(str(manifest["finished_at_utc"]))
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(
            "finalized run timestamps must be valid ISO-8601 values"
        ) from exc
    elapsed = (finished - started).total_seconds()
    if not math.isfinite(elapsed) or elapsed < 0:
        raise ValueError(
            "finalized run wall-clock duration must be finite and non-negative"
        )
    return elapsed


def _aggregate_units(units: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for unit in units:
        groups[
            (str(unit["layout_id"]), str(unit["condition_id"]), str(unit["agent_id"]))
        ].append(unit)
    aggregates = []
    numeric_fields = (
        "nominal_mean",
        "nominal_gap",
        "immediate_degradation",
        "worst_degradation",
        "post_change_mean",
        "post_change_gap",
        "cumulative_deficit",
    )
    for key in sorted(groups):
        group = sorted(
            groups[key], key=lambda item: (str(item["run_id"]), int(item["root_seed"]))
        )
        metrics = [item["primary_metrics"] for item in group]
        statuses = [str(item["recovery_status"]) for item in metrics]
        delays = [
            item["recovery_delay"]
            for item in metrics
            if item["recovery_delay"] is not None
        ]
        aggregates.append(
            {
                "layout_id": key[0],
                "condition_id": key[1],
                "agent_id": key[2],
                "valid_unit_count": len(group),
                "unit_ids": [item["unit_id"] for item in group],
                "recovery_status_counts": dict(sorted(Counter(statuses).items())),
                "mean_recovery_delay_among_recovered": None
                if not delays
                else fmean(delays),
                "metric_means": {
                    field: fmean(float(item[field]) for item in metrics)
                    for field in numeric_fields
                },
                "metric_sample_standard_deviations": {
                    field: (
                        None
                        if len(metrics) < 2
                        else stdev(float(item[field]) for item in metrics)
                    )
                    for field in numeric_fields
                },
            }
        )
    return aggregates


def _aggregate_sensitivity(
    records: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for record in records:
        groups[
            (
                str(record["layout_id"]),
                str(record["condition_id"]),
                str(record["agent_id"]),
                str(record["sensitivity_id"]),
            )
        ].append(record)
    aggregates: list[dict[str, Any]] = []
    for key in sorted(groups):
        group = sorted(groups[key], key=lambda item: str(item["unit_id"]))
        metrics = [item["metrics"] for item in group]
        aggregates.append(
            {
                "layout_id": key[0],
                "condition_id": key[1],
                "agent_id": key[2],
                "sensitivity_id": key[3],
                "parameters": group[0]["parameters"],
                "valid_unit_count": len(group),
                "recovery_status_counts": dict(
                    sorted(
                        Counter(
                            str(item["recovery_status"]) for item in metrics
                        ).items()
                    )
                ),
                "mean_cumulative_deficit": fmean(
                    float(item["cumulative_deficit"]) for item in metrics
                ),
                "mean_post_change_gap": fmean(
                    float(item["post_change_gap"]) for item in metrics
                ),
            }
        )
    return aggregates


def build_analysis_payload(
    *, repo_root: Path, analysis_id: str, run_ids: Sequence[str]
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if (
        not isinstance(analysis_id, str)
        or not analysis_id
        or Path(analysis_id).name != analysis_id
    ):
        raise ValueError("analysis_id must be a safe non-empty name")
    if not isinstance(run_ids, (list, tuple)) or not run_ids:
        raise ValueError("run_ids must be an explicit non-empty sequence")
    ordered_run_ids = tuple(sorted(run_ids))
    if len(set(ordered_run_ids)) != len(ordered_run_ids):
        raise ValueError("run_ids must be unique")
    root = repo_root.resolve()
    inventories: list[dict[str, Any]] = []
    all_units: list[dict[str, Any]] = []
    all_sensitivity: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    pilot_input = False
    for run_id in ordered_run_ids:
        manifest = validate_finalized_run(repo_root=root, run_id=run_id)
        status = manifest.get("status")
        if status not in FINAL_STATUSES:
            raise ValueError("input run has unsupported final status")
        run_dir = root / "results" / "runs" / run_id
        resolved = _read_object(run_dir / "resolved-config.json")
        summary = _read_object(run_dir / "summary.json")
        stage = str(manifest.get("stage"))
        pilot_input = pilot_input or stage == ProtocolStage.PILOT.value
        if status == "completed":
            derived = derive_completed_run_records(
                run_id=run_id,
                manifest=manifest,
                resolved_config=resolved,
                summary=summary,
                repo_root=root,
            )
            inventories.append(dict(derived.inventory))
            all_units.extend(dict(item) for item in derived.units)
            all_sensitivity.extend(dict(item) for item in derived.sensitivity)
        else:
            inventories.append(
                {
                    "run_id": run_id,
                    "status": status,
                    "protocol_version": manifest.get("protocol_version"),
                    "stage": stage,
                    "source_git_commit": manifest.get("source", {}).get("git_commit"),
                    "unit_count": 0,
                    "failure": summary.get("failure"),
                }
            )
        file_sizes = [
            path.stat().st_size for path in run_dir.iterdir() if path.is_file()
        ]
        event_diagnostics = _event_diagnostics(run_dir)
        event_diagnostics.update(
            {
                "run_id": run_id,
                "wall_clock_seconds": _wall_clock_seconds(manifest),
                "bundle_size_bytes": sum(file_sizes),
                "manifest_sha256": sha256_file(run_dir / "manifest.json"),
                "summary_sha256": sha256_file(run_dir / "summary.json"),
            }
        )
        diagnostics.append(event_diagnostics)
    if pilot_input:
        provenance = source_provenance(root)
        if (
            provenance.get("git_commit") is None
            or provenance.get("tracked_changes_present") is not False
            or provenance.get("untracked_nonoutput_present") is not False
        ):
            raise ValueError(
                "pilot analysis requires a clean committed analysis source"
            )
    all_units.sort(key=lambda item: item["unit_id"])
    all_sensitivity.sort(key=lambda item: (item["unit_id"], item["sensitivity_id"]))
    payload = {
        "analysis_schema_version": ANALYSIS_SCHEMA_VERSION,
        "analysis_id": analysis_id,
        "analysis_source_git_commit": _git_commit(root),
        "input_run_ids": list(ordered_run_ids),
        "run_inventory": inventories,
        "operational_diagnostics": diagnostics,
        "completed_run_count": sum(
            item["status"] == "completed" for item in inventories
        ),
        "noncompleted_run_count": sum(
            item["status"] != "completed" for item in inventories
        ),
        "valid_unit_count": len(all_units),
        "sensitivity_record_count": len(all_sensitivity),
        "primary_aggregates": _aggregate_units(all_units),
        "sensitivity_aggregates": _aggregate_sensitivity(all_sensitivity),
        "interpretation_boundary": "diagnostic summaries only; no inferential or final claim",
    }
    return payload, all_units, all_sensitivity


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def validate_analysis(*, analysis_dir: Path) -> dict[str, Any]:
    """Fail closed unless an analysis directory is complete and internally consistent."""

    if not isinstance(analysis_dir, Path) or not analysis_dir.is_dir():
        raise ValueError("analysis_dir must be an existing directory")
    expected_names = {
        "FINALIZED",
        "analysis.json",
        "units.jsonl",
        "sensitivity.jsonl",
        "manifest.json",
        "checksums.sha256",
    }
    entries = {path.name for path in analysis_dir.iterdir()}
    if entries != expected_names:
        raise ValueError("analysis directory file set is incomplete or contains extras")
    if any(path.is_symlink() or not path.is_file() for path in analysis_dir.iterdir()):
        raise ValueError("analysis artifacts must be regular files")
    marker = (analysis_dir / "FINALIZED").read_text(encoding="utf-8")
    if marker != f"analysis_schema_version={ANALYSIS_SCHEMA_VERSION}\n":
        raise ValueError("analysis finalization marker is invalid")

    manifest = _read_object(analysis_dir / "manifest.json")
    _exact_keys(
        manifest,
        {"analysis_schema_version", "analysis_id", "input_run_ids", "files"},
        field="analysis manifest",
    )
    if manifest["analysis_schema_version"] != ANALYSIS_SCHEMA_VERSION:
        raise ValueError("analysis manifest schema version is unsupported")
    if manifest["analysis_id"] != analysis_dir.name:
        raise ValueError("analysis manifest identity does not match its directory")
    artifact_names = {"analysis.json", "units.jsonl", "sensitivity.jsonl"}
    files = manifest["files"]
    if not isinstance(files, dict) or set(files) != artifact_names:
        raise ValueError("analysis manifest artifact inventory is invalid")
    for name in sorted(artifact_names):
        metadata = files[name]
        _exact_keys(metadata, {"sha256", "size_bytes"}, field=f"manifest file {name}")
        path = analysis_dir / name
        if (
            metadata["sha256"] != sha256_file(path)
            or metadata["size_bytes"] != path.stat().st_size
        ):
            raise ValueError(f"analysis artifact integrity mismatch: {name}")

    checksums: dict[str, str] = {}
    for line in (
        (analysis_dir / "checksums.sha256").read_text(encoding="utf-8").splitlines()
    ):
        parts = line.split("  ")
        if (
            len(parts) != 2
            or not _SHA256_RE.fullmatch(parts[0])
            or Path(parts[1]).name != parts[1]
        ):
            raise ValueError("analysis checksum inventory is malformed")
        if parts[1] in checksums:
            raise ValueError("analysis checksum inventory contains duplicates")
        checksums[parts[1]] = parts[0]
    checksum_names = artifact_names | {"manifest.json"}
    if set(checksums) != checksum_names:
        raise ValueError("analysis checksum inventory is incomplete")
    for name, expected in checksums.items():
        if sha256_file(analysis_dir / name) != expected:
            raise ValueError(f"analysis checksum mismatch: {name}")

    analysis = _read_object(analysis_dir / "analysis.json")
    if analysis.get("analysis_schema_version") != ANALYSIS_SCHEMA_VERSION:
        raise ValueError("analysis payload schema version is unsupported")
    if analysis.get("analysis_id") != manifest["analysis_id"]:
        raise ValueError("analysis payload identity does not match its manifest")
    if analysis.get("input_run_ids") != manifest["input_run_ids"]:
        raise ValueError("analysis input inventory does not match its manifest")
    for name, count_field in (
        ("units.jsonl", "valid_unit_count"),
        ("sensitivity.jsonl", "sensitivity_record_count"),
    ):
        count = 0
        for number, line in enumerate(
            (analysis_dir / name).read_text(encoding="utf-8").splitlines(), start=1
        ):
            try:
                record = json.loads(line, parse_constant=_reject_nonfinite_json)
            except (json.JSONDecodeError, ValueError) as exc:
                raise ValueError(f"invalid {name} record at line {number}") from exc
            if not isinstance(record, dict):
                raise TypeError(f"{name} line {number} must be an object")
            count += 1
        if analysis.get(count_field) != count:
            raise ValueError(f"{name} count does not match analysis payload")
    return analysis


def write_analysis(
    *, repo_root: Path, analysis_id: str, run_ids: Sequence[str]
) -> AnalysisResult:
    payload, units, sensitivity = build_analysis_payload(
        repo_root=repo_root, analysis_id=analysis_id, run_ids=run_ids
    )
    root = repo_root.resolve()
    destination = root / "results" / "summaries" / analysis_id
    temporary = destination.with_name(f".{analysis_id}.tmp")
    if destination.exists() or temporary.exists():
        raise FileExistsError("analysis output identity already exists")
    temporary.mkdir(parents=True)
    try:
        _write_text(
            temporary / "analysis.json",
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        _write_text(
            temporary / "units.jsonl",
            "".join(_canonical_json(item) + "\n" for item in units),
        )
        _write_text(
            temporary / "sensitivity.jsonl",
            "".join(_canonical_json(item) + "\n" for item in sensitivity),
        )
        output_files = sorted(path for path in temporary.iterdir() if path.is_file())
        manifest = {
            "analysis_schema_version": ANALYSIS_SCHEMA_VERSION,
            "analysis_id": analysis_id,
            "input_run_ids": sorted(run_ids),
            "files": {
                path.name: {
                    "sha256": sha256_file(path),
                    "size_bytes": path.stat().st_size,
                }
                for path in output_files
            },
        }
        _write_text(
            temporary / "manifest.json",
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        checksum_files = sorted(path for path in temporary.iterdir() if path.is_file())
        _write_text(
            temporary / "checksums.sha256",
            "".join(f"{sha256_file(path)}  {path.name}\n" for path in checksum_files),
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary.replace(destination)
        _write_text(
            destination / ANALYSIS_FINALIZATION_MARKER,
            f"analysis_schema_version={ANALYSIS_SCHEMA_VERSION}\n",
        )
        validate_analysis(analysis_dir=destination)
    except Exception:
        if temporary.exists():
            for path in temporary.iterdir():
                if path.is_file():
                    path.unlink()
            temporary.rmdir()
        if destination.exists():
            for path in destination.iterdir():
                if path.is_file():
                    path.unlink()
            destination.rmdir()
        raise
    return AnalysisResult(
        analysis_dir=destination,
        unit_count=len(units),
        sensitivity_record_count=len(sensitivity),
    )
