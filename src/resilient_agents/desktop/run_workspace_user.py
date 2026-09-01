"""Intended-user hardening and final visual polish for the accepted Run workspace."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

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
            root.setContentsMargins(28, 18, 30, 20)
            root.setSpacing(8)

        status_frame = self.progress.parentWidget()
        status_layout = status_frame.layout() if status_frame is not None else None
        top_layout = status_layout.itemAt(0).layout() if status_layout is not None else None

        self.current_method_label = QLabel("Awaiting live method")
        self.current_method_label.setObjectName("CurrentMethod")
        self.current_method_label.setAccessibleName("Current method in live presentation")
        self.current_method_label.setWordWrap(False)
        if top_layout is not None:
            # Keep current-method orientation in the existing stage row so the
            # compact status card does not steal height from the primary GridWorld.
            top_layout.insertWidget(1, self.current_method_label)

        self.method_overview = QWidget(status_frame)
        self.method_overview.setObjectName("MethodOverview")
        self.method_overview_layout = QHBoxLayout(self.method_overview)
        self.method_overview_layout.setContentsMargins(0, 0, 0, 0)
        self.method_overview_layout.setSpacing(6)
        if status_layout is not None:
            status_layout.insertWidget(
                status_layout.indexOf(self.progress) + 1,
                self.method_overview,
            )

        # The GridWorld pair is the primary visual evidence on Run. The accepted
        # baseline rendered roughly 205 px-square panels at 1366x768; this target
        # allows ~260 px-square panels while remaining responsive and unclipped.
        self.grid.setMinimumHeight(260)
        self.grid.setMaximumSize(980, 500)
        self.grid.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        live_layout = self.grid.parentWidget().layout() if self.grid.parentWidget() else None
        if live_layout is not None:
            live_layout.setSpacing(5)

        self._clear_inherited_method_strip()
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
        if hasattr(self, "method_overview_layout"):
            self._clear_inherited_method_strip()
            self._refresh_method_orientation(item, current_method_id=None)

    def _clear_inherited_method_strip(self) -> None:
        """Remove base strip labels after reading their durable status projection."""
        while self.method_strip.count():
            entry = self.method_strip.takeAt(0)
            widget = entry.widget()
            if widget is not None:
                widget.hide()
                widget.setParent(None)
                widget.deleteLater()

    def _clear_method_overview(self) -> None:
        while self.method_overview_layout.count():
            entry = self.method_overview_layout.takeAt(0)
            widget = entry.widget()
            if widget is not None:
                widget.hide()
                widget.setParent(None)
                widget.deleteLater()

    def _refresh_method_orientation(
        self,
        item: StudyListItem | None,
        *,
        current_method_id: str | None,
    ) -> None:
        self._clear_method_overview()
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
            self.method_overview_layout.addWidget(label)
            # Refreshes can occur after the window is already visible. Explicitly
            # show replacement labels so the compact strip is present in the real
            # rendered workspace, not only in the QObject tree.
            label.show()
        self.method_overview_layout.addStretch(1)
        self.method_overview.show()

        if item is None:
            self.current_method_label.setText("Final execution gated")
            return
        if current_method_id is None:
            self.current_method_label.setText("Awaiting live method")
            return

        ordered_ids = [method.method_id for method in self.protocol.methods]
        try:
            index = ordered_ids.index(current_method_id) + 1
        except ValueError:
            self.current_method_label.setText(
                f"Current · {self._method_name(current_method_id)}"
            )
            return
        self.current_method_label.setText(
            f"Method {index} of {len(ordered_ids)} · {self._method_name(current_method_id)}"
        )

    def refresh_live(self) -> None:
        super().refresh_live()
        if not hasattr(self, "method_overview_layout"):
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
