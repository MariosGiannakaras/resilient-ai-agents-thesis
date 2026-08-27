"""Application-facing query/control model for the NiceGUI presentation layer.

The model composes existing scientific/runtime contracts; it does not implement
agent logic, GridWorld dynamics or experiment execution itself. Live status and
telemetry come only from ``RuntimeService``. Finalized historical evidence stays
under the canonical ``ExperimentRegistry``.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from resilient_agents.contracts import ProtocolStage, RetentionPolicy
from resilient_agents.experiment_manager import ExperimentRegistry
from resilient_agents.runtime_service import RuntimeRunSnapshot, RuntimeService
from resilient_agents.v11_candidate_runner import V11CandidateExperimentRequest
from resilient_agents.v11_protocol import V11CandidateProtocol, load_v11_candidate_protocol


@dataclass(frozen=True)
class AgentProfile:
    agent_id: str
    name: str
    role: str
    mechanism_badge: str
    adaptation: str
    planning: str
    description: str
    status: str


AGENT_PROFILES: tuple[AgentProfile, ...] = (
    AgentProfile(
        agent_id="f0",
        name="Fixed Q-Learning",
        role="Non-adaptive control baseline",
        mechanism_badge="Does not adapt",
        adaptation="Keeps the common nominal Q-values fixed during evaluation",
        planning="None · model-free",
        description=(
            "Uses what it learned before the change; it does not learn during "
            "evaluation. This measures resilience without post-change adaptation."
        ),
        status="validated-baseline",
    ),
    AgentProfile(
        agent_id="c0",
        name="Adaptive Q-Learning",
        role="Online off-policy model-free adaptation",
        mechanism_badge="Model-free · off-policy",
        adaptation="Continues Q-learning updates from new experience",
        planning="None · model-free",
        description=(
            "Keeps updating its learned action values from new experience while "
            "starting from the same nominal checkpoint as Fixed Q-Learning."
        ),
        status="validated-baseline",
    ),
    AgentProfile(
        agent_id="s0",
        name="SARSA",
        role="Online on-policy model-free adaptation",
        mechanism_badge="Model-free · on-policy",
        adaptation="Updates values for the action sequence it actually follows",
        planning="None · model-free",
        description=(
            "Learns from the actions it actually follows, including exploratory "
            "actions. Its small alpha choice remains a bounded non-final setting."
        ),
        status="candidate-v1.1",
    ),
    AgentProfile(
        agent_id="dq0",
        name="Dyna-Q",
        role="Learned-model planning",
        mechanism_badge="Uses planning",
        adaptation="Learns from real transitions and continues online updates",
        planning="Planning over an empirical model learned from experience",
        description=(
            "Learns from real experience and also plans using an internal model it "
            "learns. It has no Dyna-Q+ recency exploration bonus."
        ),
        status="candidate-v1.1",
    ),
    AgentProfile(
        agent_id="d0",
        name="Dyna-Q+",
        role="Planning plus directed re-exploration",
        mechanism_badge="Re-explores for change",
        adaptation="Learns an empirical model and continues adapting online",
        planning="Dyna planning plus a recency bonus for long-untried actions",
        description=(
            "Plans like Dyna-Q and deliberately re-checks actions that have not "
            "been tried recently, helping it search for environmental change."
        ),
        status="candidate-v1.1",
    ),
)

AGENT_PROFILE_BY_ID = {profile.agent_id: profile for profile in AGENT_PROFILES}


@dataclass(frozen=True)
class CandidateConfigurationOption:
    configuration_id: str
    agent_id: str
    strategy_name: str
    settings: Mapping[str, Any]
    sha256: str


@dataclass(frozen=True)
class CandidateExperimentForm:
    """Resolved user-facing candidate selection before request creation."""

    run_id: str
    stage: ProtocolStage
    layout_id: str
    condition_id: str
    agent_configuration_ids: Mapping[str, str]


SETTING_PRESENTATION: Mapping[str, Mapping[str, str]] = {
    "learning_rate": {
        "label": "Learning responsiveness",
        "range": "0 to 1 (unit-free)",
        "consequence": "Higher values give more weight to recent experience.",
    },
    "discount_factor": {
        "label": "Future-reward weight",
        "range": "0 to 1 (unit-free)",
        "consequence": "Higher values place more weight on rewards further ahead.",
    },
    "exploration_epsilon": {
        "label": "Exploration probability",
        "range": "0 to 1 (probability)",
        "consequence": "The chance of deliberately trying a non-greedy action.",
    },
    "planning_steps": {
        "label": "Planning updates",
        "range": "Non-negative count per real transition",
        "consequence": "More updates may improve adaptation but increase compute time.",
    },
    "kappa": {
        "label": "Re-exploration strength",
        "range": "Non-negative bonus scale",
        "consequence": "Higher values more strongly revisit actions not tried recently.",
    },
    "bootstrap_on_truncation": {
        "label": "Truncation handling",
        "range": "Fixed protocol rule",
        "consequence": "Disabled so a time-limit truncation is not treated as continuing value.",
    },
    "initial_q_value": {
        "label": "Initial action value",
        "range": "Reward units",
        "consequence": "The common starting estimate before nominal training.",
    },
}


class ApplicationReadModel:
    """Truthful query/control facade for the current local thesis workspace."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.registry = ExperimentRegistry(self.repo_root)
        self.runtime = RuntimeService(self.repo_root)
        self.v11_protocol_path = self.repo_root / "configs" / "protocols" / "protocol-v1.1.json"
        self._v11_protocol: V11CandidateProtocol | None = None

    def finalized_runs(self) -> list[dict[str, Any]]:
        runs = self.registry.list_runs()
        return sorted(
            runs,
            key=lambda row: str(row.get("started_at_utc") or ""),
            reverse=True,
        )

    @lru_cache(maxsize=256)
    def finalized_run(self, run_id: str) -> dict[str, Any] | None:
        return self.registry.get_run(run_id)

    def runtime_runs(self) -> list[RuntimeRunSnapshot]:
        return list(self.runtime.list_runs())

    def runtime_run(self, run_id: str) -> RuntimeRunSnapshot:
        return self.runtime.get_run(run_id)

    def runtime_telemetry(
        self, run_id: str, *, after_sequence: int = -1, limit: int = 500
    ) -> tuple[dict[str, Any], ...]:
        return self.runtime.tail_telemetry(
            run_id,
            after_sequence=after_sequence,
            limit=limit,
        )

    def system_snapshot(self) -> dict[str, Any]:
        return self.runtime.resource_snapshot()

    def candidate_protocol(self) -> V11CandidateProtocol:
        if self._v11_protocol is None:
            self._v11_protocol = load_v11_candidate_protocol(self.v11_protocol_path)
        return self._v11_protocol

    def candidate_protocol_summary(self) -> dict[str, Any]:
        protocol = self.candidate_protocol()
        payload = protocol.to_dict()
        return {
            "protocol_version": payload["protocol_version"],
            "status": payload["status"],
            "sha256": protocol.protocol_sha256(),
            "strategy_count": len(protocol.strategy_ids()),
            "condition_count": len(payload["conditions"]),
            "final_layout_count": len(payload["evaluation"]["final_layout_ids"]),
            "final_root_count": len(payload["evaluation"]["root_seeds"]),
            "final_evidence_allowed": bool(
                payload["failure_and_exclusion_policy"]["final_evidence_allowed"]
            ),
        }

    def protocol_inventory(self) -> list[dict[str, str]]:
        protocol_dir = self.repo_root / "configs" / "protocols"
        records: list[dict[str, str]] = []
        if not protocol_dir.is_dir():
            return records
        for path in sorted(protocol_dir.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                records.append(
                    {
                        "file": path.name,
                        "protocol_version": "unreadable",
                        "status": "invalid",
                    }
                )
                continue
            records.append(
                {
                    "file": path.name,
                    "protocol_version": str(
                        payload.get("protocol_version")
                        or payload.get("version")
                        or path.stem
                    ),
                    "status": str(payload.get("status") or "unspecified"),
                }
            )
        return records

    def stage_layout_ids(self, stage: ProtocolStage) -> tuple[str, ...]:
        payload = self.candidate_protocol().to_dict()
        if stage is ProtocolStage.DEVELOPMENT:
            return tuple(payload["partitions"]["development"])
        if stage is ProtocolStage.TUNING:
            return tuple(payload["partitions"]["tuning"])
        return ()

    def stage_condition_ids(self, stage: ProtocolStage) -> tuple[str, ...]:
        payload = self.candidate_protocol().to_dict()
        if stage is ProtocolStage.TUNING:
            return tuple(payload["tuning"]["condition_ids"])
        if stage is ProtocolStage.DEVELOPMENT:
            return tuple(item["condition_id"] for item in payload["conditions"])
        return ()

    def stage_root_seeds(self, stage: ProtocolStage) -> tuple[int, ...]:
        return self.candidate_protocol().root_seeds_for(stage)

    def candidate_configuration_options(
        self, *, stage: ProtocolStage
    ) -> dict[str, tuple[CandidateConfigurationOption, ...]]:
        if stage not in {ProtocolStage.DEVELOPMENT, ProtocolStage.TUNING}:
            return {}
        protocol = self.candidate_protocol()
        payload = protocol.to_dict()
        catalog = payload["configuration_catalog"]
        if stage is ProtocolStage.TUNING:
            allowed_by_agent = payload["tuning"]["candidate_configuration_ids"]
        else:
            development_ids = set(payload["development"]["allowed_configuration_ids"])
            allowed_by_agent = {
                agent_id: [
                    configuration_id
                    for configuration_id in development_ids
                    if catalog[configuration_id]["agent_id"] == agent_id
                ]
                for agent_id in protocol.strategy_ids()
            }
        result: dict[str, tuple[CandidateConfigurationOption, ...]] = {}
        for agent_id in protocol.strategy_ids():
            options: list[CandidateConfigurationOption] = []
            for configuration_id in sorted(allowed_by_agent[agent_id]):
                configuration = protocol.configuration(configuration_id)
                profile = AGENT_PROFILE_BY_ID[agent_id]
                options.append(
                    CandidateConfigurationOption(
                        configuration_id=configuration_id,
                        agent_id=agent_id,
                        strategy_name=profile.name,
                        settings=dict(configuration["settings"]),
                        sha256=protocol.configuration_sha256(configuration_id),
                    )
                )
            result[agent_id] = tuple(options)
        return result

    def resolved_candidate_request(
        self, selection: CandidateExperimentForm
    ) -> V11CandidateExperimentRequest:
        if not isinstance(selection, CandidateExperimentForm):
            raise ValueError("selection must be CandidateExperimentForm")
        if selection.stage not in {ProtocolStage.DEVELOPMENT, ProtocolStage.TUNING}:
            raise ValueError("candidate application permits development/tuning only")
        protocol = self.candidate_protocol()
        payload = protocol.to_dict()
        selected_agents = tuple(
            agent_id
            for agent_id in protocol.strategy_ids()
            if agent_id in selection.agent_configuration_ids
        )
        if not selected_agents:
            raise ValueError("select at least one Agent strategy")
        checkpoint = payload["checkpoint_training"]
        return V11CandidateExperimentRequest(
            run_id=selection.run_id,
            stage=selection.stage,
            layout_id=selection.layout_id,
            condition_id=selection.condition_id,
            root_seeds=protocol.root_seeds_for(selection.stage),
            agent_ids=selected_agents,
            q_learning_rate=float(checkpoint["learning_rate"]),
            discount_factor=float(checkpoint["discount_factor"]),
            exploration_epsilon=float(checkpoint["exploration_epsilon"]),
            training_episodes_per_layout=int(checkpoint["training_episodes_per_layout"]),
            pre_change_episodes=16,
            post_change_episodes=32,
            immediate_window=1,
            worst_window=2,
            terminal_window=4,
            recovery_tolerance=0.0,
            recovery_stability_episodes=2,
            retention_policy=RetentionPolicy.EVENTS,
            auto_publish=False,
            execution_timeout_seconds=None,
            agent_configuration_ids=dict(selection.agent_configuration_ids),
        )

    def queue_candidate(self, request: V11CandidateExperimentRequest) -> RuntimeRunSnapshot:
        if not isinstance(request, V11CandidateExperimentRequest):
            raise ValueError("request must be V11CandidateExperimentRequest")
        return self.runtime.enqueue_v11_candidate(
            protocol_path=self.v11_protocol_path,
            request=request.to_dict(),
        )

    def start_next_runtime_run(self) -> RuntimeRunSnapshot | None:
        return self.runtime.start_next()

    def cancel_runtime_run(self, run_id: str) -> RuntimeRunSnapshot:
        return self.runtime.cancel(run_id)

    def restart_runtime_run(self, run_id: str) -> RuntimeRunSnapshot:
        return self.runtime.restart(run_id)

    @lru_cache(maxsize=256)
    def runtime_request(self, run_id: str) -> dict[str, Any] | None:
        """Return a persisted runtime request for identity display only."""
        path = self.repo_root / "results" / "runtime" / run_id / "request.json"
        if not path.is_file():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"runtime request is unreadable for {run_id}") from exc
        if not isinstance(payload, dict) or payload.get("run_id") != run_id:
            raise RuntimeError(f"runtime request identity mismatch for {run_id}")
        return payload

    def run_identity(self, run_id: str) -> dict[str, Any] | None:
        runtime_request = self.runtime_request(run_id)
        finalized = self.finalized_run(run_id)
        manifest = finalized.get("manifest", {}) if finalized else {}
        config = finalized.get("config", {}) if finalized else {}
        request = runtime_request
        if request is None and isinstance(config, dict):
            candidate = config.get("request")
            request = candidate if isinstance(candidate, dict) else None
        if request is None and not finalized:
            return None
        agent_ids = request.get("agent_ids", []) if request else []
        return {
            "protocol_version": (
                manifest.get("protocol_version")
                or ("protocol-v1.1" if runtime_request is not None else None)
            ),
            "stage": request.get("stage") if request else manifest.get("stage"),
            "layout_id": request.get("layout_id") if request else None,
            "condition_id": request.get("condition_id") if request else None,
            "agent_ids": tuple(str(value) for value in agent_ids),
            "strategy_names": tuple(
                AGENT_PROFILE_BY_ID[value].name if value in AGENT_PROFILE_BY_ID else value
                for value in (str(item) for item in agent_ids)
            ),
            "agent_configuration_ids": (
                dict(request.get("agent_configuration_ids", {}))
                if request and isinstance(request.get("agent_configuration_ids"), dict)
                else {}
            ),
            "retention_policy": request.get("retention_policy") if request else None,
            "source_git_commit": (
                manifest.get("source", {}).get("git_commit")
                if isinstance(manifest.get("source"), dict)
                else None
            ),
        }

    @lru_cache(maxsize=256)
    def historical_trace_available(self, run_id: str) -> bool:
        """Report only an explicitly retained GridWorld step trace.

        Episode summaries are not trajectories and therefore never enable replay.
        """
        path = self.repo_root / "results" / "runs" / run_id / "events.jsonl"
        if not path.is_file():
            return False
        try:
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise RuntimeError(f"historical event trace is unreadable for {run_id}") from exc
                    if isinstance(event, dict) and event.get("event") == "gridworld_step":
                        return True
        except (OSError, UnicodeError) as exc:
            raise RuntimeError(f"historical event trace is unreadable for {run_id}") from exc
        return False

    def thesis_final_artifacts(self) -> list[dict[str, Any]]:
        root = self.repo_root / "results" / "thesis-final" / "artifacts"
        manifest = self.repo_root / "results" / "thesis-final" / "freeze-manifest.json"
        if not root.is_dir() and not manifest.is_file():
            return []
        rows: list[dict[str, Any]] = []
        paths = list(sorted(root.iterdir())) if root.is_dir() else []
        if manifest.is_file():
            paths.append(manifest)
        evidence_package = self.repo_root / "results" / "thesis_evidence_package.zip"
        if evidence_package.is_file():
            paths.append(evidence_package)
        for path in paths:
            if not path.is_file():
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append(
                {
                    "name": path.name,
                    "suffix": path.suffix.lower(),
                    "size_bytes": path.stat().st_size,
                    "path": path,
                    "sha256": digest,
                    "evidence_class": "Frozen historical protocol-v1.0 evidence",
                    "preview_kind": (
                        path.suffix.lower().lstrip(".")
                        if path.suffix.lower() in {".csv", ".json", ".html"}
                        else None
                    ),
                }
            )
        return rows

    def thesis_final_freeze_summary(self) -> dict[str, Any] | None:
        path = self.repo_root / "results" / "thesis-final" / "freeze-manifest.json"
        if not path.is_file():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        return {
            "protocol_version": payload.get("protocol_version"),
            "freeze_time_utc": payload.get("freeze_time_utc"),
            "included_runs": payload.get("included_runs"),
            "total_final_runs_found": payload.get("total_final_runs_found"),
            "provenance_archive_ref": payload.get("provenance_archive_ref"),
        }

    def artifact_preview(self, name: str, *, row_limit: int = 40) -> dict[str, Any]:
        artifacts = {item["name"]: item for item in self.thesis_final_artifacts()}
        if name not in artifacts:
            raise KeyError(name)
        artifact = artifacts[name]
        path = artifact["path"]
        suffix = artifact["suffix"]
        if suffix == ".csv":
            try:
                frame = pd.read_csv(path, nrows=row_limit)
            except (OSError, UnicodeError, ValueError, pd.errors.ParserError) as exc:
                raise RuntimeError(f"CSV artifact is unreadable: {name}") from exc
            return {
                "kind": "csv",
                "columns": [str(column) for column in frame.columns],
                "rows": frame.where(pd.notna(frame), None).to_dict(orient="records"),
                "truncated": path.name == "primary_metrics.csv" and len(frame) >= row_limit,
            }
        if suffix == ".json":
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"JSON artifact is unreadable: {name}") from exc
            return {"kind": "json", "value": payload}
        if suffix == ".html":
            return {
                "kind": "html",
                "relative_url": f"/stored-thesis-artifacts/{path.name}",
            }
        return {"kind": "unavailable"}

    def v10_primary_metrics(self) -> pd.DataFrame | None:
        path = self.repo_root / "results" / "thesis-final" / "artifacts" / "primary_metrics.csv"
        if not path.is_file():
            return None
        try:
            frame = pd.read_csv(path)
        except (OSError, UnicodeError, ValueError, pd.errors.ParserError):
            return None
        required = {
            "agent_id",
            "condition_id",
            "layout_id",
            "run_id",
            "nominal_mean",
            "post_change_mean",
            "cumulative_deficit",
            "immediate_degradation",
        }
        return frame if required.issubset(frame.columns) else None

    def v10_aggregated_summary(self) -> pd.DataFrame | None:
        path = (
            self.repo_root
            / "results"
            / "thesis-final"
            / "artifacts"
            / "aggregated_summary.csv"
        )
        if not path.is_file():
            return None
        try:
            frame = pd.read_csv(path, header=[0, 1], index_col=[0, 1])
        except (OSError, UnicodeError, ValueError, pd.errors.ParserError):
            return None
        frame.index.names = ["agent_id", "condition_id"]
        return frame


def bytes_to_gib(value: Any) -> str:
    if not isinstance(value, (int, float)) or value < 0:
        return "Unavailable"
    return f"{value / (1024 ** 3):.1f} GiB"


def shortened_hash(value: str, length: int = 12) -> str:
    if not isinstance(value, str):
        return "Unavailable"
    return value[:length]


def setting_summary(settings: Mapping[str, Any]) -> str:
    order = ("learning_rate", "discount_factor", "exploration_epsilon", "planning_steps", "kappa")
    parts = [
        f"{SETTING_PRESENTATION[key]['label']}: {settings[key]}"
        for key in order
        if key in settings
    ]
    return " · ".join(parts)


def layout_label(layout_id: str) -> str:
    prefixes = {
        "dev-l": "Development layout ",
        "tune-l": "Tuning layout ",
        "final-l": "Historical final layout ",
        "v11-final-l": "Reserved final layout ",
    }
    for prefix, label in prefixes.items():
        if layout_id.startswith(prefix):
            suffix = layout_id.removeprefix(prefix).lstrip("0") or "0"
            return label + suffix
    return "Protocol-approved layout"


def setting_rows(
    selected: CandidateConfigurationOption,
    available: tuple[CandidateConfigurationOption, ...],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    preferred_order = (
        "learning_rate",
        "exploration_epsilon",
        "discount_factor",
        "planning_steps",
        "kappa",
        "bootstrap_on_truncation",
        "initial_q_value",
    )
    ordered_keys = [key for key in preferred_order if key in selected.settings]
    ordered_keys.extend(key for key in selected.settings if key not in ordered_keys)
    for key in ordered_keys:
        value = selected.settings[key]
        presentation = SETTING_PRESENTATION.get(
            key,
            {
                "label": key.replace("_", " ").title(),
                "range": "Protocol-defined",
                "consequence": "Defined by the approved protocol configuration.",
            },
        )
        values = {option.settings.get(key) for option in available}
        rows.append(
            {
                "setting": str(presentation["label"]),
                "value": str(value),
                "availability": "Tunable across approved choices" if len(values) > 1 else "Fixed by protocol",
                "range": str(presentation["range"]),
                "consequence": str(presentation["consequence"]),
            }
        )
    return rows
