"""Default concrete executor registry for the framework-neutral StudyService."""
from __future__ import annotations

from ..evidence_v2.analysis_executor_v21 import StudyAnalysisExecutorRouter
from ..evidence_v2.executors import StudyValidationExecutor
from ..evidence_v2.export_executor_v21 import StudyExportExecutorRouter
from .protocol_v2_executors import ProtocolV2PhaseAStudyExecutor
from .protocol_v2_phase_b_router import ProtocolV2PhaseBStudyExecutorRouter
from .reference_executors import ProtocolV2PhaseAReferenceExecutor
from .scheduler import StudyExecutorRegistry


def default_study_executor_registry() -> StudyExecutorRegistry:
    """Return the supported protocol-v2 backend execution surface.

    Construction itself has no scientific side effects. Optional SB3 imports
    remain lazy until a DQN/PPO job actually executes. Phase-B, analysis and
    export dispatch are protocol-aware: legacy recipes retain historical behavior
    while the explicit protocol-v2.1 recipe uses DEC-060 temporal/statistical
    evidence with v2.1 provenance.
    """

    return StudyExecutorRegistry(
        (
            ProtocolV2PhaseAStudyExecutor(),
            ProtocolV2PhaseAReferenceExecutor(),
            ProtocolV2PhaseBStudyExecutorRouter(),
            StudyValidationExecutor(),
            StudyAnalysisExecutorRouter(),
            StudyExportExecutorRouter(),
        )
    )
