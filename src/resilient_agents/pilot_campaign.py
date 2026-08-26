"""Predeclared tuning and diagnostic-pilot campaign orchestration."""

from __future__ import annotations

import json
import math
import subprocess
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import fmean
from typing import Any

from .analysis import build_analysis_payload, validate_analysis, write_analysis
from .contracts import ProtocolStage, RetentionPolicy
from .experiment_runner import HeadlessExperimentRequest, HeadlessExperimentRunner
from .git_publish import validate_finalized_run
from .pilot_protocol import PilotProtocol, load_pilot_protocol
from .run_bundle import source_provenance

PILOT_CAMPAIGN_SCHEMA_VERSION = 1
PILOT_ANALYSIS_ID = "PV01-PILOT-ANALYSIS"
PILOT_CAMPAIGN_ID = "pilot-v0.1"
AMENDED_PILOT_ANALYSIS_ID = "PV02-PILOT-ANALYSIS"
AMENDED_PILOT_CAMPAIGN_ID = "pilot-v0.2"


@dataclass(frozen=True, order=True)
class QConfiguration:
    learning_rate: float
    discount_factor: float
    exploration_epsilon: float

    def to_dict(self) -> dict[str, float]:
        return {
            "learning_rate": float(self.learning_rate),
            "discount_factor": float(self.discount_factor),
            "exploration_epsilon": float(self.exploration_epsilon),
        }

    def canonical_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"), sort_keys=True)


@dataclass(frozen=True)
class TuningScore:
    configuration: QConfiguration
    run_ids: tuple[str, ...]
    mean_nominal_return: float
    worst_layout_mean_nominal_return: float
    collision_rate_per_transition: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "configuration": self.configuration.to_dict(),
            "run_ids": list(self.run_ids),
            "mean_nominal_return": self.mean_nominal_return,
            "worst_layout_mean_nominal_return": self.worst_layout_mean_nominal_return,
            "collision_rate_per_transition": self.collision_rate_per_transition,
        }


def stage_one_configurations(protocol: PilotProtocol) -> tuple[QConfiguration, ...]:
    search = protocol.to_dict()["tuning"]["q_learning_search"]
    configurations = tuple(
        QConfiguration(
            float(alpha), float(search["stage_one_discount_factor"]), float(epsilon)
        )
        for alpha in search["learning_rates"]
        for epsilon in search["exploration_epsilons"]
    )
    if len(configurations) != 16 or len(set(configurations)) != 16:
        raise ValueError(
            "pilot-v0.1 stage-one tuning grid must contain 16 configurations"
        )
    return configurations


def stage_two_configurations(
    protocol: PilotProtocol, winner: QConfiguration
) -> tuple[QConfiguration, ...]:
    search = protocol.to_dict()["tuning"]["q_learning_search"]
    configurations = tuple(
        QConfiguration(
            winner.learning_rate, float(discount), winner.exploration_epsilon
        )
        for discount in search["discount_factors"]
        if float(discount) != winner.discount_factor
    )
    if len(configurations) != 2 or len(set(configurations)) != 2:
        raise ValueError("pilot-v0.1 stage two must add exactly two discount factors")
    return configurations


def select_tuning_winner(scores: Sequence[TuningScore]) -> TuningScore:
    if not scores:
        raise ValueError("at least one tuning score is required")
    configurations = [score.configuration for score in scores]
    if len(set(configurations)) != len(configurations):
        raise ValueError("tuning scores must contain unique configurations")
    for score in scores:
        values = (
            score.mean_nominal_return,
            score.worst_layout_mean_nominal_return,
            score.collision_rate_per_transition,
        )
        if any(not math.isfinite(value) for value in values):
            raise ValueError("tuning scores must be finite")
        if not 0.0 <= score.collision_rate_per_transition <= 1.0:
            raise ValueError("collision rate must be in [0, 1]")
    return min(
        scores,
        key=lambda score: (
            -score.mean_nominal_return,
            -score.worst_layout_mean_nominal_return,
            score.collision_rate_per_transition,
            score.configuration.canonical_json(),
        ),
    )


def _metric_parameters() -> dict[str, int | float]:
    # Central pre-outcome pilot-v0.1 settings; the full declared grid is always analyzed.
    return {
        "immediate_window": 1,
        "worst_window": 4,
        "terminal_window": 8,
        "recovery_tolerance": 1.0,
        "recovery_stability_episodes": 4,
    }


def tuning_request(
    *,
    protocol: PilotProtocol,
    configuration: QConfiguration,
    configuration_index: int,
    layout_id: str,
    stage_label: str,
    timeout_seconds: float,
) -> HeadlessExperimentRequest:
    payload = protocol.to_dict()
    tuning = payload["tuning"]
    evaluation_episodes = int(tuning["nominal_evaluation_episodes_per_layout"])
    layout_number = tuple(payload["partitions"]["tuning"]).index(layout_id) + 1
    run_id = f"PV01-TUNE-{stage_label}-{configuration_index:02d}-L{layout_number:02d}"
    return HeadlessExperimentRequest(
        run_id=run_id,
        stage=ProtocolStage.TUNING,
        layout_id=layout_id,
        condition_id="nominal",
        root_seeds=tuple(tuning["root_seeds"]),
        agent_ids=("f0",),
        q_learning_rate=configuration.learning_rate,
        discount_factor=configuration.discount_factor,
        exploration_epsilon=configuration.exploration_epsilon,
        training_episodes_per_layout=int(tuning["training_episodes_per_layout"]),
        pre_change_episodes=16,
        post_change_episodes=evaluation_episodes - 16,
        retention_policy=RetentionPolicy.EVENTS,
        auto_publish=True,
        execution_timeout_seconds=float(timeout_seconds),
        **_metric_parameters(),
    )


def pilot_requests(
    *, protocol: PilotProtocol, configuration: QConfiguration, timeout_seconds: float
) -> tuple[HeadlessExperimentRequest, ...]:
    payload = protocol.to_dict()
    tuning = payload["tuning"]
    evaluation = payload["evaluation"]
    requests: list[HeadlessExperimentRequest] = []
    try:
        run_prefix = {"pilot-v0.1": "PV01", "pilot-v0.2": "PV02"}[
            protocol.protocol_version
        ]
    except KeyError as exc:
        raise ValueError("unsupported pilot campaign protocol version") from exc
    for layout_number, layout_id in enumerate(payload["partitions"]["pilot"], start=1):
        for condition_number, condition_id in enumerate(
            evaluation["condition_ids"], start=1
        ):
            requests.append(
                HeadlessExperimentRequest(
                    run_id=f"{run_prefix}-PILOT-L{layout_number:02d}-C{condition_number:02d}",
                    stage=ProtocolStage.PILOT,
                    layout_id=layout_id,
                    condition_id=condition_id,
                    root_seeds=tuple(evaluation["root_seeds"]),
                    agent_ids=("f0", "c0", "r0"),
                    q_learning_rate=configuration.learning_rate,
                    discount_factor=configuration.discount_factor,
                    exploration_epsilon=configuration.exploration_epsilon,
                    training_episodes_per_layout=int(
                        tuning["training_episodes_per_layout"]
                    ),
                    pre_change_episodes=int(evaluation["pre_change_episodes"]),
                    post_change_episodes=int(evaluation["post_change_episodes"]),
                    retention_policy=RetentionPolicy.EVENTS,
                    auto_publish=True,
                    execution_timeout_seconds=float(timeout_seconds),
                    **_metric_parameters(),
                )
            )
    if len(requests) != 14 or len({item.run_id for item in requests}) != 14:
        raise ValueError("pilot-v0.1 must create exactly 14 unique child experiments")
    return tuple(requests)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def _elapsed_seconds(manifest: Mapping[str, Any]) -> float:
    started = datetime.fromisoformat(str(manifest["started_at_utc"]))
    finished = datetime.fromisoformat(str(manifest["finished_at_utc"]))
    elapsed = (finished - started).total_seconds()
    if not math.isfinite(elapsed) or elapsed < 0.0:
        raise ValueError("run duration must be finite and non-negative")
    return elapsed


def _execute_or_validate(
    *, repo_root: Path, protocol: PilotProtocol, request: HeadlessExperimentRequest
) -> dict[str, Any]:
    run_dir = repo_root / "results" / "runs" / request.run_id
    if run_dir.exists():
        manifest = validate_finalized_run(repo_root=repo_root, run_id=request.run_id)
        resolved = _read_json(run_dir / "resolved-config.json")
        if resolved.get("request") != request.to_dict():
            raise ValueError(
                f"existing run request differs from campaign plan: {request.run_id}"
            )
    else:
        HeadlessExperimentRunner(
            repo_root=repo_root, protocol=protocol, request=request
        ).run()
        manifest = validate_finalized_run(repo_root=repo_root, run_id=request.run_id)
    if manifest.get("status") != "completed":
        raise RuntimeError(f"campaign child is not completed: {request.run_id}")
    return manifest


def _collision_totals(run_dir: Path, *, layout_id: str) -> tuple[int, int]:
    collisions = 0
    transitions = 0
    for number, line in enumerate(
        (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines(), start=1
    ):
        event = json.loads(line)
        if not isinstance(event, dict):
            raise TypeError(f"event line {number} must be an object")
        if not (
            event.get("event") == "episode_completed"
            and event.get("agent_id") == "f0"
            and event.get("branch") == "reference"
            and event.get("scenario_id") == f"{layout_id}--nominal"
        ):
            continue
        length = int(event["length"])
        episode_return = float(event["return"])
        baseline = length - 1 if event.get("outcome") == "terminated" else length
        collision_count = -episode_return - baseline
        rounded = round(collision_count)
        if abs(collision_count - rounded) > 1e-9 or not 0 <= rounded <= length:
            raise ValueError(
                "nominal collision count is inconsistent with return/length"
            )
        collisions += rounded
        transitions += length
    if transitions <= 0:
        raise ValueError("tuning run contains no reference evaluation transitions")
    return collisions, transitions


def collect_tuning_score(
    *,
    repo_root: Path,
    configuration: QConfiguration,
    run_ids: Sequence[str],
) -> TuningScore:
    if len(run_ids) != 2:
        raise ValueError("one tuning configuration requires exactly two layout runs")
    layout_returns: dict[str, list[float]] = {}
    collisions = 0
    transitions = 0
    _, units, _ = build_analysis_payload(
        repo_root=repo_root,
        analysis_id="TUNING-SCORE",
        run_ids=tuple(run_ids),
    )
    for run_id in sorted(run_ids):
        manifest = validate_finalized_run(repo_root=repo_root, run_id=run_id)
        if manifest.get("status") != "completed" or manifest.get("stage") != "tuning":
            raise ValueError("tuning score input must be a completed tuning run")
        run_dir = repo_root / "results" / "runs" / run_id
        resolved = _read_json(run_dir / "resolved-config.json")
        request = HeadlessExperimentRequest.from_dict(resolved["request"])
        actual = QConfiguration(
            float(request.q_learning_rate),
            float(request.discount_factor),
            float(request.exploration_epsilon),
        )
        if actual != configuration:
            raise ValueError(
                "tuning run hyperparameters do not match their score group"
            )
        returns = [
            float(value)
            for unit in units
            if unit["run_id"] == run_id
            for value in unit["reference_episode_returns"]
        ]
        layout_returns[request.layout_id] = returns
        run_collisions, run_transitions = _collision_totals(
            run_dir, layout_id=request.layout_id
        )
        collisions += run_collisions
        transitions += run_transitions
    if len(layout_returns) != 2 or any(
        not values for values in layout_returns.values()
    ):
        raise ValueError("tuning score must contain both non-empty tuning layouts")
    layout_means = [fmean(values) for values in layout_returns.values()]
    return TuningScore(
        configuration=configuration,
        run_ids=tuple(sorted(run_ids)),
        mean_nominal_return=fmean(
            value for values in layout_returns.values() for value in values
        ),
        worst_layout_mean_nominal_return=min(layout_means),
        collision_rate_per_transition=collisions / transitions,
    )


def _git_branch(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "branch", "--show-current"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def _require_durable_main(repo_root: Path) -> None:
    if _git_branch(repo_root) != "main":
        raise RuntimeError("pilot-v0.1 execution must publish from durable main")
    provenance = source_provenance(repo_root)
    if (
        provenance.get("git_commit") is None
        or provenance.get("tracked_changes_present") is not False
        or provenance.get("untracked_nonoutput_present") is not False
    ):
        raise RuntimeError(
            "pilot-v0.1 execution requires a clean committed source tree"
        )
    subprocess.run(
        ["git", "-C", str(repo_root), "fetch", "origin", "main"],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    local = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    remote = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "origin/main"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    if local != remote:
        raise RuntimeError(
            "local main must exactly match origin/main before the campaign"
        )


def _write_state(
    repo_root: Path, payload: Mapping[str, Any], *, campaign_id: str
) -> Path:
    directory = repo_root / "results" / "campaigns" / campaign_id
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / "campaign-state.json"
    temporary = directory / ".campaign-state.tmp"
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(destination)
    return destination


def execute_pilot_campaign(*, repo_root: Path, protocol: PilotProtocol) -> Path:
    """Execute/resume the complete predeclared campaign and derive its analysis."""

    root = repo_root.resolve()
    payload = protocol.to_dict()
    if protocol.protocol_version == AMENDED_PILOT_CAMPAIGN_ID:
        return _execute_amended_pilot_campaign(repo_root=root, protocol=protocol)
    if protocol.protocol_version != PILOT_CAMPAIGN_ID:
        raise ValueError("campaign driver supports only pilot-v0.1")
    _require_durable_main(root)
    tuning_layouts = tuple(payload["partitions"]["tuning"])
    rule = payload["resource_policy"]["child_timeout_rule"]
    stage_one = stage_one_configurations(protocol)
    preflight_request = tuning_request(
        protocol=protocol,
        configuration=stage_one[0],
        configuration_index=0,
        layout_id=tuning_layouts[0],
        stage_label="S1",
        timeout_seconds=float(rule["maximum_seconds"]),
    )
    preflight_manifest = _execute_or_validate(
        repo_root=root, protocol=protocol, request=preflight_request
    )
    preflight_seconds = _elapsed_seconds(preflight_manifest)
    measured_timeout = max(
        float(rule["minimum_seconds"]),
        math.ceil(float(rule["measured_preflight_multiplier"]) * preflight_seconds),
    )
    if measured_timeout > float(rule["maximum_seconds"]):
        raise RuntimeError("measured child timeout exceeds pilot-v0.1 maximum")

    stage_one_scores: list[TuningScore] = []
    all_tuning_scores: list[TuningScore] = []
    tuning_run_ids: list[str] = []
    for index, configuration in enumerate(stage_one):
        requests = tuple(
            tuning_request(
                protocol=protocol,
                configuration=configuration,
                configuration_index=index,
                layout_id=layout_id,
                stage_label="S1",
                timeout_seconds=(
                    float(rule["maximum_seconds"])
                    if index == 0 and layout_id == tuning_layouts[0]
                    else measured_timeout
                ),
            )
            for layout_id in tuning_layouts
        )
        for request in requests:
            _execute_or_validate(repo_root=root, protocol=protocol, request=request)
            tuning_run_ids.append(request.run_id)
        score = collect_tuning_score(
            repo_root=root,
            configuration=configuration,
            run_ids=tuple(request.run_id for request in requests),
        )
        stage_one_scores.append(score)
        all_tuning_scores.append(score)
    stage_one_winner = select_tuning_winner(stage_one_scores)

    for index, configuration in enumerate(
        stage_two_configurations(protocol, stage_one_winner.configuration), start=16
    ):
        requests = tuple(
            tuning_request(
                protocol=protocol,
                configuration=configuration,
                configuration_index=index,
                layout_id=layout_id,
                stage_label="S2",
                timeout_seconds=measured_timeout,
            )
            for layout_id in tuning_layouts
        )
        for request in requests:
            _execute_or_validate(repo_root=root, protocol=protocol, request=request)
            tuning_run_ids.append(request.run_id)
        all_tuning_scores.append(
            collect_tuning_score(
                repo_root=root,
                configuration=configuration,
                run_ids=tuple(request.run_id for request in requests),
            )
        )
    selected = select_tuning_winner(all_tuning_scores)

    planned_pilot_requests = pilot_requests(
        protocol=protocol,
        configuration=selected.configuration,
        timeout_seconds=measured_timeout,
    )
    pilot_manifests = [
        _execute_or_validate(repo_root=root, protocol=protocol, request=request)
        for request in planned_pilot_requests
    ]
    pilot_run_ids = [request.run_id for request in planned_pilot_requests]
    analysis_dir = root / "results" / "summaries" / PILOT_ANALYSIS_ID
    if analysis_dir.exists():
        analysis = validate_analysis(analysis_dir=analysis_dir)
        if analysis["input_run_ids"] != sorted(pilot_run_ids):
            raise ValueError("existing pilot analysis input inventory differs")
    else:
        write_analysis(
            repo_root=root, analysis_id=PILOT_ANALYSIS_ID, run_ids=pilot_run_ids
        )
        analysis = validate_analysis(analysis_dir=analysis_dir)

    state = {
        "pilot_campaign_schema_version": PILOT_CAMPAIGN_SCHEMA_VERSION,
        "campaign_id": PILOT_CAMPAIGN_ID,
        "protocol_version": protocol.protocol_version,
        "preflight": {
            "run_id": preflight_request.run_id,
            "measured_seconds": preflight_seconds,
            "derived_child_timeout_seconds": measured_timeout,
        },
        "tuning": {
            "configuration_count": len(all_tuning_scores),
            "run_ids": tuning_run_ids,
            "stage_one_winner": stage_one_winner.to_dict(),
            "selected": selected.to_dict(),
            "scores": [score.to_dict() for score in all_tuning_scores],
        },
        "pilot": {
            "run_ids": pilot_run_ids,
            "status_counts": dict(
                sorted(Counter(str(item["status"]) for item in pilot_manifests).items())
            ),
            "total_wall_clock_seconds": sum(
                _elapsed_seconds(item) for item in pilot_manifests
            ),
            "total_bundle_size_bytes": sum(
                int(item["bundle_size_bytes"])
                for item in analysis["operational_diagnostics"]
            ),
            "analysis_id": PILOT_ANALYSIS_ID,
            "valid_unit_count": analysis["valid_unit_count"],
            "sensitivity_record_count": analysis["sensitivity_record_count"],
        },
        "interpretation_boundary": "diagnostic pilot evidence only; no inferential or final claim",
    }
    return _write_state(root, state, campaign_id=PILOT_CAMPAIGN_ID)


def _baseline_tuning_selection(
    repo_root: Path, protocol: PilotProtocol
) -> tuple[float, TuningScore, TuningScore, list[TuningScore], list[str], float]:
    payload = protocol.to_dict()
    layouts = tuple(payload["partitions"]["tuning"])
    rule = payload["resource_policy"]["child_timeout_rule"]
    preflight = validate_finalized_run(
        repo_root=repo_root, run_id="PV01-TUNE-S1-00-L01"
    )
    preflight_seconds = _elapsed_seconds(preflight)
    timeout = max(
        float(rule["minimum_seconds"]),
        math.ceil(float(rule["measured_preflight_multiplier"]) * preflight_seconds),
    )
    stage_one_scores: list[TuningScore] = []
    all_scores: list[TuningScore] = []
    run_ids: list[str] = []
    stage_one = stage_one_configurations(protocol)
    for index, configuration in enumerate(stage_one):
        config_runs = tuple(
            f"PV01-TUNE-S1-{index:02d}-L{layout_number:02d}"
            for layout_number, _ in enumerate(layouts, start=1)
        )
        score = collect_tuning_score(
            repo_root=repo_root, configuration=configuration, run_ids=config_runs
        )
        stage_one_scores.append(score)
        all_scores.append(score)
        run_ids.extend(config_runs)
    stage_one_winner = select_tuning_winner(stage_one_scores)
    for index, configuration in enumerate(
        stage_two_configurations(protocol, stage_one_winner.configuration), start=16
    ):
        config_runs = tuple(
            f"PV01-TUNE-S2-{index:02d}-L{layout_number:02d}"
            for layout_number, _ in enumerate(layouts, start=1)
        )
        all_scores.append(
            collect_tuning_score(
                repo_root=repo_root,
                configuration=configuration,
                run_ids=config_runs,
            )
        )
        run_ids.extend(config_runs)
    return (
        timeout,
        stage_one_winner,
        select_tuning_winner(all_scores),
        all_scores,
        run_ids,
        preflight_seconds,
    )


def _execute_amended_pilot_campaign(
    *, repo_root: Path, protocol: PilotProtocol
) -> Path:
    _require_durable_main(repo_root)
    baseline_path = repo_root / "configs" / "protocols" / "pilot-v0.1.json"
    baseline = load_pilot_protocol(baseline_path)
    (
        timeout,
        stage_one_winner,
        selected,
        tuning_scores,
        tuning_run_ids,
        preflight_seconds,
    ) = _baseline_tuning_selection(repo_root, baseline)
    requests = pilot_requests(
        protocol=protocol,
        configuration=selected.configuration,
        timeout_seconds=timeout,
    )
    manifests = [
        _execute_or_validate(repo_root=repo_root, protocol=protocol, request=request)
        for request in requests
    ]
    run_ids = [request.run_id for request in requests]
    analysis_dir = repo_root / "results" / "summaries" / AMENDED_PILOT_ANALYSIS_ID
    if analysis_dir.exists():
        analysis = validate_analysis(analysis_dir=analysis_dir)
        if analysis["input_run_ids"] != sorted(run_ids):
            raise ValueError("existing amended pilot analysis input inventory differs")
    else:
        write_analysis(
            repo_root=repo_root,
            analysis_id=AMENDED_PILOT_ANALYSIS_ID,
            run_ids=run_ids,
        )
        analysis = validate_analysis(analysis_dir=analysis_dir)

    prior_attempts: list[dict[str, Any]] = []
    for layout_number in (1, 2):
        for condition_number in range(1, 8):
            run_id = f"PV01-PILOT-L{layout_number:02d}-C{condition_number:02d}"
            if not (repo_root / "results" / "runs" / run_id).exists():
                continue
            manifest = validate_finalized_run(repo_root=repo_root, run_id=run_id)
            summary = _read_json(repo_root / "results" / "runs" / run_id / "summary.json")
            prior_attempts.append(
                {
                    "run_id": run_id,
                    "status": manifest["status"],
                    "failure": summary.get("failure"),
                    "supersession_reason": (
                        "pilot-v0.2 reruns the complete matrix after the confirmed "
                        "R0 terminal-observation alias implementation defect"
                    ),
                }
            )
    state = {
        "pilot_campaign_schema_version": PILOT_CAMPAIGN_SCHEMA_VERSION,
        "campaign_id": AMENDED_PILOT_CAMPAIGN_ID,
        "protocol_version": protocol.protocol_version,
        "amendment": {
            "base_protocol": PILOT_CAMPAIGN_ID,
            "reason": "R0 rejected an active corrupted observation that aliased the modeled goal",
            "tuning_reused": True,
            "pilot_seed_bank_reused_for_paired_implementation_retry": True,
            "prior_attempts": prior_attempts,
        },
        "preflight": {
            "run_id": "PV01-TUNE-S1-00-L01",
            "measured_seconds": preflight_seconds,
            "derived_child_timeout_seconds": timeout,
        },
        "tuning": {
            "configuration_count": len(tuning_scores),
            "run_ids": tuning_run_ids,
            "stage_one_winner": stage_one_winner.to_dict(),
            "selected": selected.to_dict(),
            "scores": [score.to_dict() for score in tuning_scores],
        },
        "pilot": {
            "run_ids": run_ids,
            "status_counts": dict(
                sorted(Counter(str(item["status"]) for item in manifests).items())
            ),
            "total_wall_clock_seconds": sum(_elapsed_seconds(item) for item in manifests),
            "total_bundle_size_bytes": sum(
                int(item["bundle_size_bytes"])
                for item in analysis["operational_diagnostics"]
            ),
            "analysis_id": AMENDED_PILOT_ANALYSIS_ID,
            "valid_unit_count": analysis["valid_unit_count"],
            "sensitivity_record_count": analysis["sensitivity_record_count"],
        },
        "interpretation_boundary": "diagnostic pilot evidence only; no inferential or final claim",
    }
    return _write_state(
        repo_root, state, campaign_id=AMENDED_PILOT_CAMPAIGN_ID
    )
