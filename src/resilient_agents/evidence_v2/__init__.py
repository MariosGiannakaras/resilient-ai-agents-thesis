"""Protocol-v2 evidence validation, analysis and deterministic export layer."""

from .analysis import ANALYSIS_PACKAGE_SCHEMA_VERSION, StudyAnalysisEngine
from .executors import StudyAnalysisExecutor, StudyValidationExecutor
from .export_executor import StudyExportExecutor
from .exports import EXPORT_PACKAGE_SCHEMA_VERSION, StudyExportEngine
from .freeze import (
    FREEZE_PACKAGE_SCHEMA_VERSION,
    validate_and_freeze_protocol_v21_final,
    validate_protocol_v21_final_freeze,
)
from .recovery import (
    MethodContrast,
    RecoveryDefinition,
    RecoveryResult,
    RecoveryTrajectoryPoint,
    assess_recovery,
    pairwise_method_contrasts,
)
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
    "FREEZE_PACKAGE_SCHEMA_VERSION",
    "EvidenceValidationFinding",
    "MatchedAdaptationEffect",
    "MeanInterval",
    "MethodContrast",
    "MetricDirection",
    "RecoveryDefinition",
    "RecoveryResult",
    "RecoveryTrajectoryPoint",
    "StudyAnalysisEngine",
    "StudyAnalysisExecutor",
    "StudyEvidenceValidationReport",
    "StudyEvidenceValidator",
    "StudyExportEngine",
    "StudyExportExecutor",
    "StudyValidationExecutor",
    "assess_recovery",
    "matched_adaptation_effect",
    "mean_across_layouts",
    "paired_root_differences",
    "pairwise_method_contrasts",
    "student_t_mean_interval",
    "trapezoidal_time_average",
    "validate_and_freeze_protocol_v21_final",
    "validate_protocol_v21_final_freeze",
]
