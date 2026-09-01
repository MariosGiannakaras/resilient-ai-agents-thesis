"""Protocol-aware Study Phase-B executor routing.

Legacy recipes continue through the immutable protocol-v2 executor.  Only the
explicit protocol-v2.1 recipe is allowed to use DEC-060 temporal evidence.
"""
from __future__ import annotations

from .model import StudyJobSpec
from .ports import StudyJobContext, StudyJobOutcome
from .protocol_v2_1_phase_b_executor import ProtocolV21PhaseBStudyExecutor
from .protocol_v2_phase_b_executor import ProtocolV2PhaseBStudyExecutor


class ProtocolV2PhaseBStudyExecutorRouter:
    """Dispatch the shared Phase-B job type without changing legacy semantics."""

    job_type = "phase-b-matched-set"

    def __init__(self) -> None:
        self._legacy = ProtocolV2PhaseBStudyExecutor()
        self._v21 = ProtocolV21PhaseBStudyExecutor()

    def execute(
        self,
        job: StudyJobSpec,
        *,
        context: StudyJobContext,
    ) -> StudyJobOutcome:
        if context.recipe.protocol_version == "protocol-v2.1":
            return self._v21.execute(job, context=context)
        return self._legacy.execute(job, context=context)
