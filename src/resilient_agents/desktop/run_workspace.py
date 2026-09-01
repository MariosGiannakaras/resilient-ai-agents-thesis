"""Experiment-first Run surface built on the existing Study/live boundaries."""
from __future__ import annotations

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .execution_supervisor import DesktopExecutionSupervisor
from .gridworld_widget import GridWorldLiveWidget
from .live_events import DesktopLiveReadModel, LiveGridFrame
from .protocol import FrozenProtocolSummary
from .study_read_model import DesktopStudyReadModel, StudyListItem
from .widgets import SectionHeader, StatusPill


class RunWorkspacePage(QWidget):
    """Prioritize current scientific process and truthful live GridWorld state."""

    study_selected = Signal(str)

    def __init__(
        self,
        model: DesktopStudyReadModel,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.model = model
        self.protocol = protocol
        self.supervisor = DesktopExecutionSupervisor(
            repo_root=model.repo_root,
            writable_root=model.writable_root,
            parent=self,
        )
        self.live_model = DesktopLiveReadModel(writable_root=model.writable_root)
        self._items: tuple[StudyListItem, ...] = ()
        self._latest_frame: LiveGridFrame | None = None
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(34, 24, 36, 28)
        root.setSpacing(12)

        header = QHBoxLayout()
        titles = QVBoxLayout()
        title = QLabel("Run")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Observe the experiment as it executes. GridWorld is the primary live view; technical job detail stays secondary."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        titles.addWidget(title)
        titles.addWidget(lead)
        header.addLayout(titles, 1)
        header.addWidget(StatusPill("FINAL EXPERIMENT LOCKED", kind="development"))
        root.addLayout(header)

        selector_row = QHBoxLayout()
        selector_label = QLabel("Experiment record")
        self.study_combo = QComboBox()
        self.study_combo.setMinimumWidth(320)
        self.study_combo.setAccessibleName("Experiment record to observe")
        selector_label.setBuddy(self.study_combo)
        self.study_combo.currentIndexChanged.connect(self._selection_changed)
        selector_row.addWidget(selector_label)
        selector_row.addWidget(self.study_combo, 1)
        self.start_button = QPushButton("Start / resume DEVELOPMENT")
        self.start_button.setObjectName("PrimaryButton")
        self.start_button.clicked.connect(self.start_or_resume)
        self.retry_button = QPushButton("Retry infrastructure failure")
        self.retry_button.setObjectName("SecondaryButton")
        self.retry_button.clicked.connect(self.retry_and_resume)
        selector_row.addWidget(self.retry_button)
        selector_row.addWidget(self.start_button)
        root.addLayout(selector_row)

        status = QFrame()
        status.setObjectName("Surface")
        status_layout = QVBoxLayout(status)
        status_layout.setContentsMargins(16, 12, 16, 12)
        status_layout.setSpacing(7)
        top = QHBoxLayout()
        self.stage_label = QLabel("No DEVELOPMENT experiment selected")
        self.stage_label.setObjectName("SectionTitle")
        self.progress_label = QLabel("Create a DEVELOPMENT experiment from Experiment to execute locally.")
        self.progress_label.setObjectName("SectionHint")
        self.progress_label.setWordWrap(True)
        top.addWidget(self.stage_label)
        top.addStretch(1)
        status_layout.addLayout(top)
        status_layout.addWidget(self.progress_label)
        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)
        self.progress.setTextVisible(False)
        status_layout.addWidget(self.progress)
        self.method_strip = QHBoxLayout()
        self.method_strip.setSpacing(8)
        status_layout.addLayout(self.method_strip)
        root.addWidget(status)

        live = QFrame()
        live.setObjectName("Surface")
        live_layout = QVBoxLayout(live)
        live_layout.setContentsMargins(18, 14, 18, 16)
        live_layout.setSpacing(8)
        self.live_title = QLabel("Live GridWorld")
        self.live_title.setObjectName("SectionTitle")
        self.live_explanation = QLabel(
            "Presentation-only stream. Frames may be dropped and never affect actions, observations, RNG, timing, metrics or evidence."
        )
        self.live_explanation.setObjectName("SectionHint")
        self.live_explanation.setWordWrap(True)
        live_layout.addWidget(self.live_title)
        live_layout.addWidget(self.live_explanation)
        self.grid = GridWorldLiveWidget()
        self.grid.setMinimumHeight(360)
        self.grid.setMaximumSize(16_777_215, 16_777_215)
        live_layout.addWidget(self.grid, 1)
        self.frame_summary = QLabel("No live presentation frame is available yet.")
        self.frame_summary.setObjectName("SectionHint")
        self.frame_summary.setWordWrap(True)
        live_layout.addWidget(self.frame_summary)
        root.addWidget(live, 1)

        self.technical_button = QPushButton("Technical details")
        self.technical_button.setCheckable(True)
        self.technical_button.setAccessibleName("Show Run technical details")
        self.technical_text = QLabel()
        self.technical_text.setObjectName("SectionHint")
        self.technical_text.setWordWrap(True)
        self.technical_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.technical_text.hide()
        self.technical_button.toggled.connect(self.technical_text.setVisible)
        root.addWidget(self.technical_button, 0, Qt.AlignmentFlag.AlignLeft)
        root.addWidget(self.technical_text)

        self.error_text = QLabel()
        self.error_text.setObjectName("ErrorText")
        self.error_text.setWordWrap(True)
        self.error_text.hide()
        root.addWidget(self.error_text)

        self.supervisor.started.connect(lambda _sid: self.refresh())
        self.supervisor.finished.connect(self._worker_finished)
        self.timer = QTimer(self)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.refresh_live)
        self.timer.start()
        self.refresh()

    def refresh(self) -> None:
        selected = self.selected_study_id()
        self._items = self.model.studies()
        self.study_combo.blockSignals(True)
        self.study_combo.clear()
        for item in self._items:
            self.study_combo.addItem(item.study_id, item.study_id)
        if selected:
            index = self.study_combo.findData(selected)
            if index >= 0:
                self.study_combo.setCurrentIndex(index)
        self.study_combo.blockSignals(False)
        self._selection_changed()

    def selected_study_id(self) -> str | None:
        value = self.study_combo.currentData()
        return value if isinstance(value, str) and value else None

    def _selected_item(self) -> StudyListItem | None:
        study_id = self.selected_study_id()
        if study_id is None:
            return None
        return next((item for item in self._items if item.study_id == study_id), None)

    def _selection_changed(self, *_args) -> None:
        item = self._selected_item()
        self._render_status(item)
        self.refresh_live()
        if item is not None:
            self.study_selected.emit(item.study_id)

    def _render_status(self, item: StudyListItem | None) -> None:
        while self.method_strip.count():
            entry = self.method_strip.takeAt(0)
            widget = entry.widget()
            if widget is not None:
                widget.deleteLater()
        if item is None:
            self.stage_label.setText("No DEVELOPMENT experiment selected")
            self.progress_label.setText("Configure and create one from Experiment. Creation never starts execution automatically.")
            self.progress.setValue(0)
            self.start_button.setEnabled(False)
            self.retry_button.setEnabled(False)
            self.technical_text.setText("Final execution remains sealed behind the separate T-610 gate.")
            return

        self.stage_label.setText(item.stage_label)
        self.progress_label.setText(
            f"{item.resolved_jobs}/{item.total_jobs} jobs resolved · {item.running_jobs} running · "
            f"{item.scientific_failures} scientific failure(s) retained · {item.infrastructure_failures} infrastructure failure(s)."
        )
        self.progress.setValue(round(item.progress_fraction * 1000))
        names = {method.method_id: method.name for method in self.protocol.methods}
        for method_id in item.method_ids:
            label = QLabel(names.get(method_id, method_id))
            label.setObjectName("MethodStatus")
            label.setToolTip("Configured method in this durable experiment record.")
            self.method_strip.addWidget(label)
        self.method_strip.addStretch(1)

        executable = item.evidence_class == "development" and not item.finalized and not self.supervisor.busy
        self.start_button.setEnabled(executable)
        self.retry_button.setEnabled(executable and item.infrastructure_failures > 0)
        self.technical_text.setText(
            f"Study ID: {item.study_id} · protocol: {item.protocol_version} · evidence: {item.evidence_class} · "
            f"backend status: {item.status} · finalized: {item.finalized}. "
            "The desktop execution path accepts DEVELOPMENT evidence only."
        )

    def refresh_live(self) -> None:
        item = self._selected_item()
        if item is None:
            self._latest_frame = None
            self.grid.set_frame(None)
            return
        frames = self.live_model.latest(item.study_id)
        frame = frames[0] if frames else None
        self._latest_frame = frame
        if frame is None:
            self.live_title.setText("Live GridWorld")
            self.grid.set_frame(None)
            self.frame_summary.setText("Awaiting a presentation frame. Durable Study progress above remains authoritative.")
            return

        if frame.phase == "phase-b":
            if frame.comparison is None:
                self.live_title.setText("Phase B — Frozen vs Adaptive")
                self.grid.set_frame(None)
                self.frame_summary.setText(
                    "Awaiting an exact matched Frozen-disturbed / Adaptive-disturbed interaction pair. "
                    "No side-by-side comparison is shown until identity matching is valid."
                )
                return
            pair = frame.comparison
            self.live_title.setText("Phase B — Frozen vs Adaptive")
            self.grid.set_frame(frame)
            self.frame_summary.setText(
                f"Exact matched interaction {pair.adaptive.interaction_index}. Frozen: learning off. "
                "Adaptive: learning continues. Both panels are the same method/root/layout/interaction identity."
            )
            return

        self.live_title.setText("Phase A — Nominal learning")
        self.grid.set_frame(frame)
        self.frame_summary.setText(
            f"{self._method_name(frame.method_id)} · interaction {frame.interaction_index} · "
            "one nominal-learning GridWorld. Method switching follows durable backend progress."
        )

    def _method_name(self, method_id: str) -> str:
        for method in self.protocol.methods:
            if method.method_id == method_id:
                return method.name
        return method_id

    def start_or_resume(self) -> None:
        study_id = self.selected_study_id()
        if study_id is None:
            return
        self.error_text.hide()
        try:
            self.supervisor.start_or_resume(study_id)
        except Exception as exc:
            self.error_text.setText(f"DEVELOPMENT execution could not start: {type(exc).__name__}: {exc}")
            self.error_text.show()
        self._render_status(self._selected_item())

    def retry_and_resume(self) -> None:
        study_id = self.selected_study_id()
        if study_id is None:
            return
        self.error_text.hide()
        try:
            self.supervisor.retry_and_resume(study_id)
        except Exception as exc:
            self.error_text.setText(f"Infrastructure retry could not start: {type(exc).__name__}: {exc}")
            self.error_text.show()
        self._render_status(self._selected_item())

    def _worker_finished(self, study_id: str, exit_code: int, output: str) -> None:
        if exit_code != 0:
            detail = output[-1200:] if output else "No worker detail was returned."
            self.error_text.setText(
                f"DEVELOPMENT worker stopped with exit code {exit_code}. Durable state is preserved. {detail}"
            )
            self.error_text.show()
        self.refresh()
