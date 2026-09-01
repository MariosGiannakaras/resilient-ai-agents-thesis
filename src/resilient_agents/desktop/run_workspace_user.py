"""Intended-user hardening and final visual polish for the accepted Run workspace."""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget

from .protocol import FrozenProtocolSummary
from .run_workspace import RunWorkspacePage as _RunWorkspacePage
from .study_read_model import DesktopStudyReadModel, StudyListItem


class RunWorkspacePage(_RunWorkspacePage):
    """Keep scientific Run behavior intact while strengthening visual orientation."""

    def __init__(
        self,
        model: DesktopStudyReadModel,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(model, protocol, parent)

        root = self.layout()
        if root is not None:
            root.setContentsMargins(28, 18, 30, 22)
            root.setSpacing(9)

        self.current_method_label = QLabel(
            "Five-method Thesis sequence · waiting for a live presentation frame"
        )
        self.current_method_label.setObjectName("CurrentMethod")
        self.current_method_label.setAccessibleName("Current method in live presentation")
        self.current_method_label.setWordWrap(True)
        status_frame = self.progress.parentWidget()
        status_layout = status_frame.layout() if status_frame is not None else None
        if status_layout is not None:
            status_layout.insertWidget(2, self.current_method_label)

        # The GridWorld pair is the primary visual evidence on Run. The previous
        # cap left too much unused laptop space; this remains responsive rather
        # than forcing a fixed pixel canvas.
        self.grid.setMinimumHeight(285)
        self.grid.setMaximumSize(900, 470)
        self.grid.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        live_layout = self.grid.parentWidget().layout() if self.grid.parentWidget() else None
        if live_layout is not None:
            live_layout.setSpacing(6)

        self._refresh_method_orientation(self._selected_item(), current_method_id=None)

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
        if hasattr(self, "current_method_label"):
            self._refresh_method_orientation(item, current_method_id=None)

    def _refresh_method_orientation(
        self,
        item: StudyListItem | None,
        *,
        current_method_id: str | None,
    ) -> None:
        self._clear_method_strip()
        status_by_id = {} if item is None else dict(item.method_statuses)
        selected = set() if item is None else set(item.method_ids)

        for method in self.protocol.methods:
            if item is None:
                status = "Locked"
            elif method.method_id in selected:
                status = status_by_id.get(method.method_id, "Pending")
            else:
                status = "Not selected"
            label = QLabel(f"{method.name} · {status}")
            label.setObjectName(
                "CurrentMethodStatus"
                if method.method_id == current_method_id
                else "MethodStatus"
            )
            label.setAccessibleName(f"{method.name}: {status}")
            label.setToolTip(
                "Durable method lifecycle status. Highlighting identifies the method "
                "shown by the current live presentation frame; it is not a score or ranking."
            )
            self.method_strip.addWidget(label)
        self.method_strip.addStretch(1)

        if not hasattr(self, "current_method_label"):
            return
        if item is None:
            self.current_method_label.setText(
                "Five-method Thesis sequence · final scientific execution is gated"
            )
            return
        if current_method_id is None:
            self.current_method_label.setText(
                "Method progress · awaiting a live presentation frame"
            )
            return

        ordered_ids = [method.method_id for method in self.protocol.methods]
        try:
            index = ordered_ids.index(current_method_id) + 1
        except ValueError:
            self.current_method_label.setText(
                f"Current live method · {self._method_name(current_method_id)}"
            )
            return
        self.current_method_label.setText(
            f"Method {index} of {len(ordered_ids)} · {self._method_name(current_method_id)}"
        )

    def refresh_live(self) -> None:
        super().refresh_live()
        if not hasattr(self, "current_method_label"):
            return
        item = self._selected_item()
        frame = self._latest_frame
        current_method_id = None if frame is None else frame.method_id
        self._refresh_method_orientation(item, current_method_id=current_method_id)

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
