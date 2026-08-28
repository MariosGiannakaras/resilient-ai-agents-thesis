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
from .recipe import STUDY_RECIPE_SCHEMA_VERSION, StudyRecipe

__all__ = [
    "STUDY_RECIPE_SCHEMA_VERSION",
    "ArtifactRole",
    "EvidenceClass",
    "JobState",
    "StudyArtifact",
    "StudyJobSpec",
    "StudyLifecycle",
    "StudyPlan",
    "StudyRecipe",
    "StudyStage",
]
