"""Protocol-v2 evidence validation, analysis and deterministic export layer."""

from .executors import StudyValidationExecutor
from .statistics import (
    MatchedAdaptationEffect,
    MeanInterval,
    MetricDirection,
    matched_adaptation_effect,
    mean_across_layouts,
    paired_root_differences,
    student_t_mean_interval,
    trapezoidal_time_average,
)
from .validation import (
    EvidenceValidationFinding,
    StudyEvidenceValidationReport,
    StudyEvidenceValidator,
)

__all__ = [
    "EvidenceValidationFinding",
    "MatchedAdaptationEffect",
    "MeanInterval",
    "MetricDirection",
    "StudyEvidenceValidationReport",
    "StudyEvidenceValidator",
    "StudyValidationExecutor",
    "matched_adaptation_effect",
    "mean_across_layouts",
    "paired_root_differences",
    "student_t_mean_interval",
    "trapezoidal_time_average",
]
