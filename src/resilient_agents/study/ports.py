"""Framework-neutral ports between study orchestration and concrete executors."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Protocol, runtime_checkable

from .model import StudyArtifact, StudyJobSpec
from .recipe import StudyRecipe


class JobOutcomeKind(str, Enum):
    COMPLETED = "completed"
    SCIENTIFIC_FAILURE = "scientific-failure"
    INFRASTRUCTURE_FAILURE = "infrastructure-failure"


@dataclass(frozen=True)
class StudyJobContext:
    """Immutable execution context supplied by orchestration, never by UI state."""

    study_id: str
    recipe: StudyRecipe
    recipe_sha256: str
    repo_root: Path
    writable_root: Path
    study_dir: Path
    attempt: int

    def __post_init__(self) -> None:
        if self.study_id != self.recipe.recipe_id:
            raise ValueError("context study_id must equal recipe_id")
        if self.recipe_sha256 != self.recipe.sha256():
            raise ValueError("context recipe hash mismatch")
        if not isinstance(self.attempt, int) or isinstance(self.attempt, bool):
            raise ValueError("attempt must be an integer")
        if self.attempt <= 0:
            raise ValueError("attempt must be > 0")


@dataclass(frozen=True)
class StudyJobOutcome:
    """Explicit executor result; scheduler does not infer scientific meaning."""

    kind: JobOutcomeKind
    message: str = ""
    artifacts: tuple[StudyArtifact, ...] = ()
    measurements: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.kind, JobOutcomeKind):
            raise ValueError("kind must be JobOutcomeKind")
        if not isinstance(self.message, str):
            raise ValueError("message must be a string")
        if self.kind is not JobOutcomeKind.COMPLETED and not self.message.strip():
            raise ValueError("failure outcomes require a non-empty message")
        if not isinstance(self.artifacts, tuple) or not all(
            isinstance(item, StudyArtifact) for item in self.artifacts
        ):
            raise ValueError("artifacts must be a tuple of StudyArtifact")
        if not isinstance(self.measurements, Mapping):
            raise ValueError("measurements must be a mapping")


@runtime_checkable
class StudyJobExecutor(Protocol):
    """Concrete execution port for exactly one declared ``job_type``."""

    job_type: str

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome: ...
