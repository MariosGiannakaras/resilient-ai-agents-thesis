"""Standardized analysis records emitted by heterogeneous scientific executors."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Mapping

from ..protocol_v2 import ProtocolV2Branch

ANALYSIS_RECORD_SCHEMA_VERSION = 1


def _identifier(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f"{field_name} must be a non-empty trimmed string")
    return value


def _finite_mapping(value: Any, *, field_name: str) -> dict[str, float]:
    if not isinstance(value, Mapping) or not value:
        raise ValueError(f"{field_name} must be a non-empty mapping")
    result: dict[str, float] = {}
    for key, raw in value.items():
        metric_id = _identifier(key, field_name=f"{field_name} metric id")
        if not isinstance(raw, (int, float)) or isinstance(raw, bool):
            raise ValueError(f"{field_name}.{metric_id} must be numeric")
        number = float(raw)
        if not math.isfinite(number):
            raise ValueError(f"{field_name}.{metric_id} must be finite")
        result[metric_id] = number
    return result


@dataclass(frozen=True)
class ProbeMeasurement:
    interaction_index: int
    metrics: Mapping[str, float]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.interaction_index, int)
            or isinstance(self.interaction_index, bool)
            or self.interaction_index < 0
        ):
            raise ValueError("interaction_index must be a non-negative integer")
        object.__setattr__(
            self,
            "metrics",
            _finite_mapping(self.metrics, field_name="probe metrics"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "interaction_index": self.interaction_index,
            "metrics": dict(self.metrics),
        }


@dataclass(frozen=True)
class PhaseAAnalysisRecord:
    study_id: str
    job_id: str
    method_id: str
    root_id: str
    layout_id: str
    probes: tuple[ProbeMeasurement, ...]
    resource_metrics: Mapping[str, float] = field(default_factory=dict)
    schema_version: int = ANALYSIS_RECORD_SCHEMA_VERSION
    record_type: str = "phase-a"

    def __post_init__(self) -> None:
        if self.schema_version != ANALYSIS_RECORD_SCHEMA_VERSION:
            raise ValueError("unsupported analysis record schema_version")
        if self.record_type != "phase-a":
            raise ValueError("PhaseAAnalysisRecord record_type must be phase-a")
        for field_name in ("study_id", "job_id", "method_id", "root_id", "layout_id"):
            _identifier(getattr(self, field_name), field_name=field_name)
        if not self.probes:
            raise ValueError("Phase-A analysis record must contain probe measurements")
        indices = [item.interaction_index for item in self.probes]
        if indices != sorted(set(indices)):
            raise ValueError("Phase-A probe interaction indices must be unique/increasing")
        if self.resource_metrics:
            object.__setattr__(
                self,
                "resource_metrics",
                _finite_mapping(self.resource_metrics, field_name="resource_metrics"),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "record_type": self.record_type,
            "study_id": self.study_id,
            "job_id": self.job_id,
            "method_id": self.method_id,
            "root_id": self.root_id,
            "layout_id": self.layout_id,
            "probes": [item.to_dict() for item in self.probes],
            "resource_metrics": dict(self.resource_metrics),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PhaseAAnalysisRecord":
        expected = {
            "schema_version",
            "record_type",
            "study_id",
            "job_id",
            "method_id",
            "root_id",
            "layout_id",
            "probes",
            "resource_metrics",
        }
        if not isinstance(payload, Mapping) or set(payload) != expected:
            raise ValueError("Phase-A analysis record keys mismatch")
        probes_payload = payload["probes"]
        if not isinstance(probes_payload, list):
            raise ValueError("Phase-A probes must be a list")
        probes: list[ProbeMeasurement] = []
        for item in probes_payload:
            if not isinstance(item, Mapping) or set(item) != {"interaction_index", "metrics"}:
                raise ValueError("Phase-A probe keys mismatch")
            probes.append(
                ProbeMeasurement(
                    interaction_index=item["interaction_index"],
                    metrics=item["metrics"],
                )
            )
        return cls(
            schema_version=payload["schema_version"],
            record_type=payload["record_type"],
            study_id=payload["study_id"],
            job_id=payload["job_id"],
            method_id=payload["method_id"],
            root_id=payload["root_id"],
            layout_id=payload["layout_id"],
            probes=tuple(probes),
            resource_metrics=payload["resource_metrics"],
        )


@dataclass(frozen=True)
class PhaseBAnalysisRecord:
    study_id: str
    job_id: str
    method_id: str
    root_id: str
    layout_id: str
    condition_id: str
    branch: ProtocolV2Branch
    checkpoint_artifact_id: str
    metrics: Mapping[str, float]
    resource_metrics: Mapping[str, float] = field(default_factory=dict)
    schema_version: int = ANALYSIS_RECORD_SCHEMA_VERSION
    record_type: str = "phase-b"

    def __post_init__(self) -> None:
        if self.schema_version != ANALYSIS_RECORD_SCHEMA_VERSION:
            raise ValueError("unsupported analysis record schema_version")
        if self.record_type != "phase-b":
            raise ValueError("PhaseBAnalysisRecord record_type must be phase-b")
        for field_name in (
            "study_id",
            "job_id",
            "method_id",
            "root_id",
            "layout_id",
            "condition_id",
            "checkpoint_artifact_id",
        ):
            _identifier(getattr(self, field_name), field_name=field_name)
        if not isinstance(self.branch, ProtocolV2Branch):
            raise ValueError("branch must be ProtocolV2Branch")
        object.__setattr__(self, "metrics", _finite_mapping(self.metrics, field_name="metrics"))
        if self.resource_metrics:
            object.__setattr__(
                self,
                "resource_metrics",
                _finite_mapping(self.resource_metrics, field_name="resource_metrics"),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "record_type": self.record_type,
            "study_id": self.study_id,
            "job_id": self.job_id,
            "method_id": self.method_id,
            "root_id": self.root_id,
            "layout_id": self.layout_id,
            "condition_id": self.condition_id,
            "branch": self.branch.value,
            "checkpoint_artifact_id": self.checkpoint_artifact_id,
            "metrics": dict(self.metrics),
            "resource_metrics": dict(self.resource_metrics),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PhaseBAnalysisRecord":
        expected = {
            "schema_version",
            "record_type",
            "study_id",
            "job_id",
            "method_id",
            "root_id",
            "layout_id",
            "condition_id",
            "branch",
            "checkpoint_artifact_id",
            "metrics",
            "resource_metrics",
        }
        if not isinstance(payload, Mapping) or set(payload) != expected:
            raise ValueError("Phase-B analysis record keys mismatch")
        try:
            branch = ProtocolV2Branch(str(payload["branch"]))
        except ValueError as exc:
            raise ValueError("unsupported Phase-B branch") from exc
        return cls(
            schema_version=payload["schema_version"],
            record_type=payload["record_type"],
            study_id=payload["study_id"],
            job_id=payload["job_id"],
            method_id=payload["method_id"],
            root_id=payload["root_id"],
            layout_id=payload["layout_id"],
            condition_id=payload["condition_id"],
            branch=branch,
            checkpoint_artifact_id=payload["checkpoint_artifact_id"],
            metrics=payload["metrics"],
            resource_metrics=payload["resource_metrics"],
        )
