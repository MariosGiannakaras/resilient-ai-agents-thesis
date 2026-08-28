"""Default concrete executor registry for the framework-neutral StudyService."""
from __future__ import annotations

from ..evidence_v2.executors import StudyAnalysisExecutor, StudyValidationExecutor
from ..evidence_v2.export_executor import StudyExportExecutor
from .protocol_v2_executors import ProtocolV2PhaseAStudyExecutor
from .protocol_v2_phase_b_executor import ProtocolV2PhaseBStudyExecutor
from .reference_executors import ProtocolV2PhaseAReferenceExecutor
from .scheduler import StudyExecutorRegistry


def default_study_executor_registry() -> StudyExecutorRegistry:
    """Return the supported protocol-v2 backend execution surface.

    Construction itself has no scientific side effects. Optional SB3 imports
    remain lazy until a DQN/PPO job actually executes.
    """

    return StudyExecutorRegistry(
        (
            ProtocolV2PhaseAStudyExecutor(),
            ProtocolV2PhaseAReferenceExecutor(),
            ProtocolV2PhaseBStudyExecutor(),
            StudyValidationExecutor(),
            StudyAnalysisExecutor(),
            StudyExportExecutor(),
        )
    )
