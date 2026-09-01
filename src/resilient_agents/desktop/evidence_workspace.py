"""Intended-user Evidence copy over the backend-registered evidence surface."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget

from .evidence_page import EvidencePage as _EvidencePage
from .study_read_model import DesktopStudyReadModel, StudyListItem


class EvidencePage(_EvidencePage):
    """Keep evidence/provenance semantics unchanged while making next steps actionable."""

    def __init__(
        self,
        model: DesktopStudyReadModel,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(model, parent)

    def _render(self, item: StudyListItem | None) -> None:
        super()._render(item)
        if item is None:
            self.next_action.setText(
                "Next: open Experiment, create a DEVELOPMENT experiment, then open "
                "Run and choose Start / resume DEVELOPMENT to produce registered evidence."
            )
            return

        roles = {artifact.role for artifact in self._artifacts}
        validation_ready = "validation-report" in roles
        analysis_ready = bool({"analysis-data", "analysis-table"} & roles)
        export_ready = "evidence-package" in roles

        if export_ready:
            self.next_action.setText(
                "Next: inspect the registered evidence package here, or open Technical / "
                "reproducibility details for lineage and checksums."
            )
        elif analysis_ready:
            self.next_action.setText(
                "Next: open Run for this Experiment record and choose Start / resume "
                "DEVELOPMENT to continue the backend export stage."
            )
        elif validation_ready:
            self.next_action.setText(
                "Next: open Run for this Experiment record and choose Start / resume "
                "DEVELOPMENT to continue the backend analysis stage."
            )
        else:
            self.next_action.setText(
                "Next: open Run for this Experiment record and choose Start / resume "
                "DEVELOPMENT to continue execution and validation."
            )
