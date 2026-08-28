"""Study-first backend domain for the protocol-v2 thesis workflow.

This package is intentionally UI-independent. It models the research study as a
single traceable lifecycle whose individual scientific executions are delegated
to validated protocol-v2 method/environment adapters.
"""

from .lifecycle import StudyLifecycle
from .model import (
    ArtifactRole,
    EvidenceClass,
    JobState,
    StudyArtifact,
    StudyJobSpec,
    StudyPlan,
    StudyStage,
)
from .planner import (
    STUDY_MATRIX_SCHEMA_VERSION,
    StudyMatrixDefinition,
    StudyPlanPreview,
    StudyPlanner,
)
from .ports import (
    JobOutcomeKind,
    StudyJobContext,
    StudyJobExecutor,
    StudyJobOutcome,
)
from .recipe import STUDY_RECIPE_SCHEMA_VERSION, StudyRecipe
from .scheduler import (
    ScheduledJobResult,
    StudyExecutorCrashed,
    StudyExecutorRegistry,
    StudyScheduler,
)
from .store import (
    STUDY_BUNDLE_SCHEMA_VERSION,
    STUDY_FINALIZATION_MARKER,
    StudyStore,
)

__all__ = [
    "STUDY_BUNDLE_SCHEMA_VERSION",
    "STUDY_FINALIZATION_MARKER",
    "STUDY_MATRIX_SCHEMA_VERSION",
    "STUDY_RECIPE_SCHEMA_VERSION",
    "ArtifactRole",
    "EvidenceClass",
    "JobOutcomeKind",
    "JobState",
    "ScheduledJobResult",
    "StudyArtifact",
    "StudyExecutorCrashed",
    "StudyExecutorRegistry",
    "StudyJobContext",
    "StudyJobExecutor",
    "StudyJobOutcome",
    "StudyJobSpec",
    "StudyLifecycle",
    "StudyMatrixDefinition",
    "StudyPlan",
    "StudyPlanPreview",
    "StudyPlanner",
    "StudyRecipe",
    "StudyScheduler",
    "StudyStage",
    "StudyStore",
]
