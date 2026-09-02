"""Core immutable domain objects for study-first research orchestration."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
from typing import Any, Mapping


class EvidenceClass(str, Enum):
    """Scientific interpretation class attached to every study/job/artifact."""

    DEVELOPMENT = "development"
    TUNING = "tuning"
    CONFIRMATORY = "confirmatory"
    DERIVED = "derived"
    EXPLORATORY = "exploratory"
    HISTORICAL = "historical"


class StudyStage(str, Enum):
    """Ordered backend stages from development evidence to thesis-ready exports."""

    FEASIBILITY = "feasibility"
    TUNING_FREEZE = "tuning-freeze"
    PHASE_A = "phase-a"
    PHASE_B = "phase-b"
    VALIDATION = "validation"
    ANALYSIS = "analysis"
    EXPORT = "export"

    @property
    def order(self) -> int:
        return _STAGE_ORDER[self]


_STAGE_ORDER = {
    StudyStage.FEASIBILITY: 10,
    StudyStage.TUNING_FREEZE: 20,
    StudyStage.PHASE_A: 30,
    StudyStage.PHASE_B: 40,
    StudyStage.VALIDATION: 50,
    StudyStage.ANALYSIS: 60,
    StudyStage.EXPORT: 70,
}


class JobState(str, Enum):
    """Operational state with scientific/infrastructure failures kept distinct."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    SCIENTIFIC_FAILED = "scientific-failed"
    INFRASTRUCTURE_FAILED = "infrastructure-failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"

    @property
    def satisfies_dependencies(self) -> bool:
        """Only a successful producer can satisfy a direct artifact dependency."""

        return self is JobState.COMPLETED

    @property
    def resolves_stage(self) -> bool:
        """Scientific failure/derived skip are retained outcomes, not missing work."""

        return self in {
            JobState.COMPLETED,
            JobState.SCIENTIFIC_FAILED,
            JobState.SKIPPED,
        }

    @property
    def retryable(self) -> bool:
        return self is JobState.INFRASTRUCTURE_FAILED


class ArtifactRole(str, Enum):
    """Stable role labels used to build evidence/thesis/presentation lineage."""

    RUN_BUNDLE = "run-bundle"
    SCIENTIFIC_CHECKPOINT = "scientific-checkpoint"
    FAILURE_RECORD = "failure-record"
    VALIDATION_REPORT = "validation-report"
    ANALYSIS_DATA = "analysis-data"
    ANALYSIS_TABLE = "analysis-table"
    FIGURE = "figure"
    THESIS_TABLE = "thesis-table"
    THESIS_FIGURE = "thesis-figure"
    PRESENTATION_ASSET = "presentation-asset"
    EVIDENCE_PACKAGE = "evidence-package"
    PROVENANCE = "provenance"


def _safe_identifier(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    if value != value.strip() or any(char.isspace() for char in value):
        raise ValueError(f"{field_name} must not contain whitespace")
    path = PurePosixPath(value)
    if path.name != value or value in {".", ".."}:
        raise ValueError(f"{field_name} must be a path-safe identifier")
    return value


@dataclass(frozen=True)
class StudyExecutionIdentity:
    """Storage/provenance identity for one execution of a scientific recipe."""

    execution_instance_id: str
    scientific_recipe_id: str
    kind: str
    predecessor_execution_instance_id: str | None = None
    recovery_decision_id: str | None = None

    def __post_init__(self) -> None:
        _safe_identifier(
            self.execution_instance_id, field_name="execution_instance_id"
        )
        _safe_identifier(self.scientific_recipe_id, field_name="scientific_recipe_id")
        if self.kind == "initial":
            if self.execution_instance_id != self.scientific_recipe_id:
                raise ValueError(
                    "initial execution_instance_id must equal scientific_recipe_id"
                )
            if (
                self.predecessor_execution_instance_id is not None
                or self.recovery_decision_id is not None
            ):
                raise ValueError("initial execution cannot carry recovery lineage")
            return
        if self.kind != "replacement":
            raise ValueError("execution identity kind must be initial or replacement")
        if self.execution_instance_id == self.scientific_recipe_id:
            raise ValueError(
                "replacement execution_instance_id must be distinct from recipe identity"
            )
        if self.predecessor_execution_instance_id is None:
            raise ValueError("replacement execution requires a predecessor instance")
        _safe_identifier(
            self.predecessor_execution_instance_id,
            field_name="predecessor_execution_instance_id",
        )
        if self.predecessor_execution_instance_id == self.execution_instance_id:
            raise ValueError("replacement execution cannot be its own predecessor")
        if (
            not isinstance(self.recovery_decision_id, str)
            or not self.recovery_decision_id.startswith("DEC-")
            or not self.recovery_decision_id[4:].isdigit()
        ):
            raise ValueError("replacement execution requires a DEC-NNN recovery decision")

    @classmethod
    def initial(cls, scientific_recipe_id: str) -> "StudyExecutionIdentity":
        return cls(
            execution_instance_id=scientific_recipe_id,
            scientific_recipe_id=scientific_recipe_id,
            kind="initial",
        )

    @classmethod
    def replacement(
        cls,
        *,
        execution_instance_id: str,
        scientific_recipe_id: str,
        predecessor_execution_instance_id: str,
        recovery_decision_id: str,
    ) -> "StudyExecutionIdentity":
        return cls(
            execution_instance_id=execution_instance_id,
            scientific_recipe_id=scientific_recipe_id,
            kind="replacement",
            predecessor_execution_instance_id=predecessor_execution_instance_id,
            recovery_decision_id=recovery_decision_id,
        )


@dataclass(frozen=True)
class StudyJobSpec:
    """One immutable unit in a materialized study plan.

    Jobs within the same stage may be scheduled independently when their
    dependencies are satisfied. Cross-stage dependencies must never point
    backwards from an earlier stage to a later one.
    """

    job_id: str
    stage: StudyStage
    evidence_class: EvidenceClass
    dependencies: tuple[str, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _safe_identifier(self.job_id, field_name="job_id")
        if not isinstance(self.stage, StudyStage):
            raise ValueError("stage must be StudyStage")
        if not isinstance(self.evidence_class, EvidenceClass):
            raise ValueError("evidence_class must be EvidenceClass")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise ValueError("job dependencies must be unique")
        if self.job_id in self.dependencies:
            raise ValueError("a job cannot depend on itself")
        for dependency in self.dependencies:
            _safe_identifier(dependency, field_name="dependency")
        if not isinstance(self.payload, Mapping):
            raise ValueError("payload must be a mapping")


@dataclass(frozen=True)
class StudyPlan:
    """Validated DAG plus deterministic ordered view of all research jobs."""

    study_id: str
    jobs: tuple[StudyJobSpec, ...]

    def __post_init__(self) -> None:
        _safe_identifier(self.study_id, field_name="study_id")
        if not self.jobs:
            raise ValueError("study plan must contain at least one job")
        by_id: dict[str, StudyJobSpec] = {}
        for job in self.jobs:
            if job.job_id in by_id:
                raise ValueError(f"duplicate study job_id: {job.job_id}")
            by_id[job.job_id] = job
        for job in self.jobs:
            for dependency_id in job.dependencies:
                dependency = by_id.get(dependency_id)
                if dependency is None:
                    raise ValueError(
                        f"job {job.job_id} depends on unknown job {dependency_id}"
                    )
                if dependency.stage.order > job.stage.order:
                    raise ValueError(
                        f"job {job.job_id} depends on later-stage job {dependency_id}"
                    )
        self._validate_acyclic(by_id)

    @staticmethod
    def _validate_acyclic(by_id: Mapping[str, StudyJobSpec]) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(job_id: str) -> None:
            if job_id in visited:
                return
            if job_id in visiting:
                raise ValueError("study job dependency graph contains a cycle")
            visiting.add(job_id)
            for dependency in by_id[job_id].dependencies:
                visit(dependency)
            visiting.remove(job_id)
            visited.add(job_id)

        for job_id in by_id:
            visit(job_id)

    def by_id(self) -> dict[str, StudyJobSpec]:
        return {job.job_id: job for job in self.jobs}

    def jobs_for_stage(self, stage: StudyStage) -> tuple[StudyJobSpec, ...]:
        return tuple(job for job in self.jobs if job.stage is stage)


@dataclass(frozen=True)
class StudyArtifact:
    """Content-addressed logical artifact with explicit scientific lineage."""

    artifact_id: str
    role: ArtifactRole
    evidence_class: EvidenceClass
    relative_path: str
    sha256: str
    source_job_ids: tuple[str, ...] = ()
    source_artifact_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _safe_identifier(self.artifact_id, field_name="artifact_id")
        if not isinstance(self.role, ArtifactRole):
            raise ValueError("role must be ArtifactRole")
        if not isinstance(self.evidence_class, EvidenceClass):
            raise ValueError("evidence_class must be EvidenceClass")
        if not isinstance(self.relative_path, str) or not self.relative_path.strip():
            raise ValueError("relative_path must be non-empty")
        path = PurePosixPath(self.relative_path)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("relative_path must remain inside the writable evidence root")
        if (
            not isinstance(self.sha256, str)
            or len(self.sha256) != 64
            or any(char not in "0123456789abcdef" for char in self.sha256)
        ):
            raise ValueError("sha256 must be a lowercase SHA-256 digest")
        if len(set(self.source_job_ids)) != len(self.source_job_ids):
            raise ValueError("source_job_ids must be unique")
        if len(set(self.source_artifact_ids)) != len(self.source_artifact_ids):
            raise ValueError("source_artifact_ids must be unique")
        for job_id in self.source_job_ids:
            _safe_identifier(job_id, field_name="source_job_id")
        for artifact_id in self.source_artifact_ids:
            _safe_identifier(artifact_id, field_name="source_artifact_id")
        if not isinstance(self.metadata, Mapping):
            raise ValueError("metadata must be a mapping")
