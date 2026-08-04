"""Protocol lifecycle rules that prevent tuning/final-evaluation leakage."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .contracts import ProtocolStage


@dataclass(frozen=True)
class ProtocolPartition:
    development_scenarios: Sequence[str]
    tuning_scenarios: Sequence[str]
    pilot_scenarios: Sequence[str]
    final_scenarios: Sequence[str]

    def validate(self) -> None:
        groups = {
            "development": set(self.development_scenarios),
            "tuning": set(self.tuning_scenarios),
            "pilot": set(self.pilot_scenarios),
            "final": set(self.final_scenarios),
        }
        if not groups["final"]:
            raise ValueError("final scenario partition must be explicit and non-empty")
        labels = list(groups)
        for index, left in enumerate(labels):
            for right in labels[index + 1 :]:
                overlap = groups[left] & groups[right]
                if overlap:
                    raise ValueError(f"scenario leakage between {left} and {right}: {sorted(overlap)}")

    def scenarios_for(self, stage: ProtocolStage) -> set[str]:
        mapping = {
            ProtocolStage.DEVELOPMENT: set(self.development_scenarios),
            ProtocolStage.TUNING: set(self.tuning_scenarios),
            ProtocolStage.PILOT: set(self.pilot_scenarios),
            ProtocolStage.FINAL: set(self.final_scenarios),
        }
        return mapping[stage]


def assert_stage_access(
    *, stage: ProtocolStage, scenario_ids: Sequence[str], partition: ProtocolPartition
) -> None:
    partition.validate()
    allowed = partition.scenarios_for(stage)
    unauthorized = set(scenario_ids) - allowed
    if unauthorized:
        raise ValueError(
            f"{stage.value} run requested scenarios outside its partition: {sorted(unauthorized)}"
        )
