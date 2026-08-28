"""Protocol-v2 evidence validation, analysis and deterministic export layer."""

from .analysis import ANALYSIS_PACKAGE_SCHEMA_VERSION, StudyAnalysisEngine
from .executors import StudyAnalysisExecutor, StudyValidationExecutor
from .export_executor import StudyExportExecutor
from .exports import EXPORT_PACKAGE_SCHEMA_VERSION, StudyExportEngine
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
    "ANALYSIS_PACKAGE_SCHEMA_VERSION",
    "EXPORT_PACKAGE_SCHEMA_VERSION",
    "EvidenceValidationFinding",
    "MatchedAdaptationEffect",
    "MeanInterval",
    "MetricDirection",
    "StudyAnalysisEngine",
    "StudyAnalysisExecutor",
    "StudyEvidenceValidationReport",
    "StudyEvidenceValidator",
    "StudyExportEngine",
    "StudyExportExecutor",
    "StudyValidationExecutor",
    "matched_adaptation_effect",
    "mean_across_layouts",
    "paired_root_differences",
    "student_t_mean_interval",
    "trapezoidal_time_average",
]
