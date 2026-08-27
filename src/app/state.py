"""Application-facing query/control model for the NiceGUI presentation layer.

The model composes existing scientific/runtime contracts; it does not implement
agent logic, GridWorld dynamics or experiment execution itself. Live status and
telemetry come only from ``RuntimeService``. Finalized historical evidence stays
under the canonical ``ExperimentRegistry``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from resilient_agents.contracts import ProtocolStage
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
            retention_policy=__import__(
                "resilient_agents.contracts", fromlist=["RetentionPolicy"]
            ).RetentionPolicy.EVENTS,
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

    def thesis_final_artifacts(self) -> list[dict[str, Any]]:
        root = self.repo_root / "results" / "thesis-final" / "artifacts"
        if not root.is_dir():
            return []
        rows: list[dict[str, Any]] = []
        for path in sorted(root.iterdir()):
            if not path.is_file():
                continue
            rows.append(
                {
                    "name": path.name,
                    "suffix": path.suffix.lower(),
                    "size_bytes": path.stat().st_size,
                    "path": path,
                }
            )
        return rows

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
    order = (
        ("learning_rate", "α"),
        ("discount_factor", "γ"),
        ("exploration_epsilon", "ε"),
        ("planning_steps", "planning"),
        ("kappa", "κ"),
    )
    parts = [f"{label}={settings[key]}" for key, label in order if key in settings]
    return " · ".join(parts)
