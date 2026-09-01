"""Intended-user hardening for the accepted Run workspace."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget

from .protocol import FrozenProtocolSummary
from .run_workspace import RunWorkspacePage as _RunWorkspacePage
from .study_read_model import DesktopStudyReadModel, StudyListItem


class RunWorkspacePage(_RunWorkspacePage):
    """Keep scientific Run behavior intact while tightening user-facing transitions."""

    def __init__(
        self,
        model: DesktopStudyReadModel,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(model, protocol, parent)

    def _render_status(self, item: StudyListItem | None) -> None:
        super()._render_status(item)
        self.retry_button.setVisible(
            item is not None and item.infrastructure_failures > 0
        )
        if item is None:
            self.technical_text.setText(
                "No DEVELOPMENT record is selected. Final scientific execution is "
                "controlled by the separate backend authorization gate and cannot "
                "be granted from this desktop application."
            )

    def set_study(self, study_id: str) -> bool:
        """Select one durable experiment record after creation or context propagation."""
        if not isinstance(study_id, str) or not study_id:
            return False
        self.refresh()
        index = self.study_combo.findData(study_id)
        if index < 0:
            return False
        self.study_combo.setCurrentIndex(index)
        return True
