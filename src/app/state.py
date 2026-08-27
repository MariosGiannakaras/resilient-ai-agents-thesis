"""Read-only application queries used by the NiceGUI presentation layer.

This module deliberately contains no experiment execution logic. Active-run
supervision belongs to T-530; finalized evidence continues to come from the
canonical experiment registry and stored result artifacts.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from resilient_agents.experiment_manager import ExperimentRegistry, get_resource_snapshot


@dataclass(frozen=True)
class AgentProfile:
    agent_id: str
    name: str
    role: str
    adaptation: str
    planning: str
    description: str
    status: str


AGENT_PROFILES: tuple[AgentProfile, ...] = (
    AgentProfile(
        agent_id="f0",
        name="F0 · Frozen Q-learning",
        role="Non-adaptive control baseline",
        adaptation="Q updates disabled after the common nominal checkpoint",
        planning="None · model-free",
        description=(
            "Measures resistance when the learned nominal policy is kept fixed after "
            "an environmental disturbance."
        ),
        status="validated-v1.0",
    ),
    AgentProfile(
        agent_id="c0",
        name="C0 · Continual Q-learning",
        role="Online model-free adaptation",
        adaptation="Continues Q updates after the same common checkpoint",
        planning="None · model-free",
        description=(
            "Isolates the effect of continued online learning while preserving the "
            "same base Q-learning implementation and selected hyperparameters as F0."
        ),
        status="validated-v1.0",
    ),
    AgentProfile(
        agent_id="d0",
        name="D0 · Dyna-Q+",
        role="Model-based planning and directed re-exploration",
        adaptation="Learns an empirical transition model and keeps adapting online",
        planning="Dyna planning with recency exploration bonus",
        description=(
            "Candidate protocol-v1.1 agent. Planning-budget and kappa parameters remain "
            "subject to bounded development/tuning selection before protocol freeze."
        ),
        status="candidate-v1.1",
    ),
)


class ApplicationReadModel:
    """Truthful query facade for the current local thesis workspace."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.registry = ExperimentRegistry(repo_root)

    def finalized_runs(self) -> list[dict[str, Any]]:
        runs = self.registry.list_runs()
        return sorted(
            runs,
            key=lambda row: str(row.get("started_at_utc") or ""),
            reverse=True,
        )

    def finalized_run(self, run_id: str) -> dict[str, Any] | None:
        return self.registry.get_run(run_id)

    def system_snapshot(self) -> dict[str, Any]:
        return get_resource_snapshot(self.repo_root)

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
