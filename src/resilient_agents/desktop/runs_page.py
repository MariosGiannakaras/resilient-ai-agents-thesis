"""Truthful durable-study Runs workspace."""
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .execution_supervisor import DesktopExecutionSupervisor
from .gridworld_widget import GridWorldLiveWidget
from .live_events import DesktopLiveReadModel, LiveGridFrame
from .study_read_model import DesktopStudyReadModel, StudyListItem
from .widgets import EmptyState, MetricItem, SectionHeader, VerticalDivider


class RunsPage(QWidget):
    study_selected = Signal(str)

    def __init__(self, read_model: DesktopStudyReadModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.read_model = read_model
        self.live_read_model = DesktopLiveReadModel(writable_root=read_model.writable_root)
        self.items: tuple[StudyListItem, ...] = ()
        self.supervisor = DesktopExecutionSupervisor(
            repo_root=read_model.repo_root,
            writable_root=read_model.writable_root,
            parent=self,
        )
        self.supervisor.started.connect(self._worker_started)
        self.supervisor.output.connect(self._worker_output)
        self.supervisor.finished.connect(self._worker_finished)

        self.poll_timer = QTimer(self)
        self.poll_timer.setInterval(1000)
        self.poll_timer.timeout.connect(self.refresh)
        self.live_timer = QTimer(self)
        self.live_timer.setInterval(150)
        self.live_timer.timeout.connect(self._refresh_live)
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(38, 28, 42, 34)
        root.setSpacing(15)

        header = QHBoxLayout()
        title_block = QVBoxLayout()
        title_block.setSpacing(4)
        title = QLabel("Runs")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Run and monitor durable development Studies from backend-owned state — "
            "no synthesized progress, replay or ETA."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        title_block.addWidget(title)
        title_block.addWidget(lead)
        header.addLayout(title_block, 1)
        refresh = QPushButton("Refresh")
        refresh.setObjectName("SecondaryButton")
        refresh.setToolTip("Reload Study state from the durable StudyStore on disk.")
        refresh.clicked.connect(self.refresh)
        header.addWidget(refresh, 0, Qt.AlignmentFlag.AlignTop)
        root.addLayout(header)

        self.summary = QFrame()
        self.summary.setObjectName("Surface")
        self.summary_layout = QHBoxLayout(self.summary)
        self.summary_layout.setContentsMargins(18, 12, 18, 12)
        self.summary_layout.setSpacing(16)
        root.addWidget(self.summary)

        self.control = QFrame()
        self.control.setObjectName("Surface")
        control_layout = QVBoxLayout(self.control)
        control_layout.setContentsMargins(20, 15, 20, 15)
        control_layout.setSpacing(8)

        control_top = QHBoxLayout()
        control_text = QVBoxLayout()
        control_text.setSpacing(2)
        self.control_title = QLabel("Selected study")
        self.control_title.setObjectName("SectionTitle")
        self.control_detail = QLabel()
        self.control_detail.setObjectName("PageLead")
        self.control_detail.setWordWrap(True)
        control_text.addWidget(self.control_title)
        control_text.addWidget(self.control_detail)
        control_top.addLayout(control_text, 1)

        self.start_button = QPushButton("Start / Resume")
        self.start_button.setObjectName("PrimaryButton")
        self.start_button.setToolTip(
            "Launch a separate local worker process. The Qt GUI remains responsive "
            "and progress continues to come from the durable StudyStore."
        )
        self.start_button.clicked.connect(self._start_selected)
        control_top.addWidget(self.start_button, 0, Qt.AlignmentFlag.AlignVCenter)

        self.retry_button = QPushButton("Retry failed job")
        self.retry_button.setObjectName("SecondaryButton")
        self.retry_button.setToolTip(
            "Retry the single infrastructure-failed job under the same scientific "
            "identity, then resume the Study."
        )
        self.retry_button.clicked.connect(self._retry_selected)
        control_top.addWidget(self.retry_button, 0, Qt.AlignmentFlag.AlignVCenter)
        control_layout.addLayout(control_top)

        self.worker_message = QLabel()
        self.worker_message.setObjectName("SectionHint")
        self.worker_message.setWordWrap(True)
        self.worker_message.hide()
        control_layout.addWidget(self.worker_message)
        self.control.hide()
        root.addWidget(self.control)

        self.live_surface = self._build_live_surface()
        self.live_surface.hide()
        root.addWidget(self.live_surface)

        root.addWidget(
            SectionHeader(
                "Study history",
                "Select a development Study to start/resume execution or inspect its durable state.",
            )
        )

        self.empty = EmptyState(
            "No studies yet",
            "No framework-neutral Study has been created in this workspace. "
            "Exploratory studies will appear here after they are created through the application.",
        )
        root.addWidget(self.empty)

        self.table = QTableWidget(0, 7)
        self.table.setObjectName("StudyTable")
        self.table.setAccessibleName("Durable study history")
        self.table.setHorizontalHeaderLabels(
            ("Study", "Evidence", "Stage", "Progress", "Status", "Failures", "Finalized")
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(False)
        self.table.itemSelectionChanged.connect(self._selection_changed)
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        root.addWidget(self.table, 1)

        self.error = QLabel()
        self.error.setObjectName("ErrorText")
        self.error.setWordWrap(True)
        self.error.hide()
        root.addWidget(self.error)

        self.refresh()

    def _build_live_surface(self) -> QFrame:
        surface = QFrame()
        surface.setObjectName("Surface")
        layout = QHBoxLayout(surface)
        layout.setContentsMargins(18, 14, 20, 14)
        layout.setSpacing(20)

        self.live_grid = GridWorldLiveWidget()
        layout.addWidget(self.live_grid, 0, Qt.AlignmentFlag.AlignTop)

        details = QVBoxLayout()
        details.setSpacing(6)
        header = QHBoxLayout()
        title = QLabel("Live GridWorld")
        title.setObjectName("SectionTitle")
        header.addWidget(title)
        header.addStretch(1)
        badge = QLabel("PRESENTATION ONLY · LOSSY")
        badge.setObjectName("StatusDevelopment")
        badge.setToolTip(
            "Frames may be dropped. This stream is not Study evidence and cannot "
            "feed information back to the learner."
        )
        header.addWidget(badge)
        details.addLayout(header)

        self.live_identity = QLabel()
        self.live_identity.setObjectName("PageLead")
        self.live_identity.setWordWrap(True)
        details.addWidget(self.live_identity)

        legend = QLabel(
            "A / arrow  Agent and executed direction   ·   G  Goal   ·   "
            "S  Start   ·   ■  Wall   ·   dashed outline  Delivered observation"
        )
        legend.setObjectName("GridLegend")
        legend.setWordWrap(True)
        legend.setAccessibleName("GridWorld visual key")
        details.addWidget(legend)

        self.live_interaction = QLabel()
        self.live_interaction.setObjectName("ReviewValue")
        self.live_interaction.setWordWrap(True)
        details.addWidget(self.live_interaction)

        self.live_transition = QLabel()
        self.live_transition.setObjectName("SectionHint")
        self.live_transition.setWordWrap(True)
        details.addWidget(self.live_transition)

        self.live_observation = QLabel()
        self.live_observation.setObjectName("SectionHint")
        self.live_observation.setWordWrap(True)
        details.addWidget(self.live_observation)

        self.live_context = QLabel()
        self.live_context.setObjectName("SectionHint")
        self.live_context.setWordWrap(True)
        details.addWidget(self.live_context)

        boundary = QLabel(
            "Read-only evaluator presentation. The scientific worker never waits "
            "for this panel; renderer disconnects or dropped frames do not change "
            "actions, RNG, checkpoints, metrics or Study evidence."
        )
        boundary.setObjectName("DevelopmentText")
        boundary.setWordWrap(True)
        details.addWidget(boundary)
        details.addStretch(1)
        layout.addLayout(details, 1)
        return surface

    def _clear_summary(self) -> None:
        while self.summary_layout.count():
            item = self.summary_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def _populate_summary(self) -> None:
        self._clear_summary()
        total = len(self.items)
        running = sum(item.running_jobs > 0 for item in self.items)
        finalized = sum(item.finalized for item in self.items)
        infra = sum(item.infrastructure_failures for item in self.items)
        scientific = sum(item.scientific_failures for item in self.items)
        metrics = (
            (str(total), "Studies"),
            (str(running), "Currently running"),
            (str(finalized), "Finalized"),
            (str(infra), "Infrastructure failures"),
            (str(scientific), "Scientific failures"),
        )
        for index, (value, label) in enumerate(metrics):
            self.summary_layout.addWidget(MetricItem(value, label), 1)
            if index != len(metrics) - 1:
                self.summary_layout.addWidget(VerticalDivider())

    @staticmethod
    def _text_item(text: str, *, user_data: str | None = None) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        if user_data is not None:
            item.setData(Qt.ItemDataRole.UserRole, user_data)
        return item

    def _progress_widget(self, item: StudyListItem) -> QProgressBar:
        progress = QProgressBar()
        progress.setRange(0, max(1, item.total_jobs))
        progress.setValue(item.resolved_jobs)
        progress.setFormat(f"{item.resolved_jobs} / {item.total_jobs}")
        progress.setTextVisible(True)
        progress.setAccessibleName(
            f"{item.resolved_jobs} of {item.total_jobs} study jobs scientifically resolved"
        )
        return progress

    def _selected_study_id(self) -> str | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        item = self.table.item(selected[0].row(), 0)
        if item is None:
            return None
        study_id = item.data(Qt.ItemDataRole.UserRole)
        return study_id if isinstance(study_id, str) and study_id else None

    def _selected_item(self) -> StudyListItem | None:
        study_id = self._selected_study_id()
        if study_id is None:
            return None
        return next((item for item in self.items if item.study_id == study_id), None)

    def refresh(self) -> None:
        previous_selection = self._selected_study_id()
        self.error.hide()
        try:
            self.items = self.read_model.studies()
        except Exception as exc:
            self.items = ()
            self.error.setText(
                "Study history could not be read. No state was changed.\n"
                f"Technical detail: {type(exc).__name__}: {exc}"
            )
            self.error.show()

        self._populate_summary()
        self.table.setRowCount(0)
        selected_row: int | None = None
        for row_index, item in enumerate(self.items):
            self.table.insertRow(row_index)
            study = self._text_item(item.study_id, user_data=item.study_id)
            study.setToolTip(f"Protocol: {item.protocol_version}")
            self.table.setItem(row_index, 0, study)
            self.table.setItem(row_index, 1, self._text_item(item.evidence_class.title()))
            self.table.setItem(row_index, 2, self._text_item(item.stage_label))
            self.table.setCellWidget(row_index, 3, self._progress_widget(item))
            self.table.setItem(
                row_index,
                4,
                self._text_item(item.status.replace("-", " ").title()),
            )
            failures = item.scientific_failures + item.infrastructure_failures
            failure_text = "—" if failures == 0 else str(failures)
            failure_cell = self._text_item(failure_text)
            if failures:
                failure_cell.setToolTip(
                    f"Scientific: {item.scientific_failures}; "
                    f"infrastructure: {item.infrastructure_failures}"
                )
            self.table.setItem(row_index, 5, failure_cell)
            self.table.setItem(
                row_index,
                6,
                self._text_item("Yes" if item.finalized else "No"),
            )
            if item.study_id == previous_selection:
                selected_row = row_index

        has_items = bool(self.items)
        self.empty.setVisible(not has_items)
        self.table.setVisible(has_items)
        if selected_row is not None:
            self.table.selectRow(selected_row)
        else:
            self._update_control(None)
            self._update_live(None)

    def _selection_changed(self) -> None:
        item = self._selected_item()
        self._update_control(item)
        self._update_live(item)
        if item is not None:
            self.study_selected.emit(item.study_id)

    def _update_control(self, item: StudyListItem | None) -> None:
        if item is None:
            self.control.hide()
            return
        self.control.show()
        self.control_title.setText(item.study_id)
        detail = (
            f"{item.evidence_class.title()} evidence · {item.stage_label} · "
            f"{item.resolved_jobs}/{item.total_jobs} jobs resolved"
        )
        self.control_detail.setText(detail)

        is_development = item.evidence_class == "development"
        worker_busy = self.supervisor.busy
        active_here = self.supervisor.active_study_id == item.study_id

        self.start_button.setEnabled(False)
        self.retry_button.setEnabled(False)
        self.retry_button.setVisible(item.infrastructure_failures > 0)

        if not is_development:
            self.start_button.setText("Final execution locked")
            self.start_button.setToolTip(
                "T-528 does not authorize confirmatory/final-reserve execution."
            )
            return
        if item.finalized:
            self.start_button.setText("Study complete")
            return
        if item.running_jobs > 0:
            self.start_button.setText("Worker running" if active_here else "Study running")
            return
        if worker_busy:
            self.start_button.setText("Another worker is active")
            return
        if item.infrastructure_failures > 0:
            self.start_button.setText("Resolve infrastructure failure")
            self.retry_button.setEnabled(True)
            return

        if item.resolved_jobs >= item.total_jobs:
            self.start_button.setText("Finalize study")
        else:
            self.start_button.setText("Start / Resume")
        self.start_button.setEnabled(True)

    def _refresh_live(self) -> None:
        self._update_live(self._selected_item())

    def _update_live(self, item: StudyListItem | None) -> None:
        if item is None:
            self.live_grid.set_frame(None)
            self.live_surface.hide()
            return
        frames = self.live_read_model.latest(item.study_id)
        frame = frames[0] if frames else None
        if frame is None:
            self.live_grid.set_frame(None)
            self.live_surface.hide()
            return
        self._show_live_frame(frame, is_running=item.running_jobs > 0)

    def _show_live_frame(self, frame: LiveGridFrame, *, is_running: bool) -> None:
        self.live_grid.set_frame(frame)
        phase = {
            "phase-a": "Nominal learning",
            "phase-b": "Resilience test",
        }.get(frame.phase, frame.phase)
        prefix = "Live" if is_running else "Last presentation frame"
        self.live_identity.setText(
            f"{prefix} · {phase} · {frame.method_id.replace('_', ' ').title()} · "
            f"root {frame.root_id} · {frame.layout_id}"
        )
        comparison = frame.comparison
        if comparison is None:
            branch = f" · branch {frame.branch}" if frame.branch else ""
            self.live_interaction.setText(
                f"Interaction {frame.interaction_index:,} · episode {frame.episode_index + 1} · "
                f"environment step {frame.environment_step}{branch}"
            )
            self.live_transition.setText(
                f"Action: {frame.intended_action} → {frame.executed_action} · "
                f"reward {frame.reward:g} · true state {frame.true_state}"
            )
            self.live_observation.setText(self._observation_note(frame))
        else:
            frozen = comparison.frozen
            adaptive = comparison.adaptive
            self.live_interaction.setText(
                f"Matched interaction {adaptive.interaction_index:,} · episode "
                f"{adaptive.episode_index + 1} · environment step "
                f"{adaptive.environment_step} · exact FD/AD pair"
            )
            self.live_transition.setText(
                f"Frozen — action {frozen.intended_action} → {frozen.executed_action} · "
                f"reward {frozen.reward:g} · true state {frozen.true_state}\n"
                f"Adaptive — action {adaptive.intended_action} → {adaptive.executed_action} · "
                f"reward {adaptive.reward:g} · true state {adaptive.true_state}"
            )
            self.live_observation.setText(
                f"Frozen: {self._observation_note(frozen)}\n"
                f"Adaptive: {self._observation_note(adaptive)}"
            )

        flags = [
            name.replace("_", " ")
            for name, active in frame.disturbance_flags.items()
            if active
        ]
        disturbance = ", ".join(flags) if flags else "none"
        change_events = ", ".join(frame.change_event_ids) if frame.change_event_ids else "none"
        self.live_context.setText(
            f"Regime: {frame.regime_id or '—'} · active disturbance flags: {disturbance} · "
            f"change events: {change_events}"
        )
        self.live_surface.show()

    @staticmethod
    def _observation_note(frame: LiveGridFrame) -> str:
        if frame.delivered_observation == frame.true_state:
            return "delivered observation matches true state."
        return (
            f"delivered observation {frame.delivered_observation} differs from "
            f"true state {frame.true_state}."
        )

    def _start_selected(self) -> None:
        item = self._selected_item()
        if item is None:
            return
        try:
            self.supervisor.start_or_resume(item.study_id)
        except Exception as exc:
            self.error.setText(
                "Study worker could not start. No scientific state was changed by the UI.\n"
                f"Technical detail: {type(exc).__name__}: {exc}"
            )
            self.error.show()

    def _retry_selected(self) -> None:
        item = self._selected_item()
        if item is None:
            return
        try:
            self.supervisor.retry_and_resume(item.study_id)
        except Exception as exc:
            self.error.setText(
                "Infrastructure retry could not start.\n"
                f"Technical detail: {type(exc).__name__}: {exc}"
            )
            self.error.show()

    def _worker_started(self, study_id: str) -> None:
        self.worker_message.setText(
            f"Local worker active for {study_id}. Progress below is reloaded from "
            "the durable StudyStore; live GridWorld frames are a separate lossy presentation stream."
        )
        self.worker_message.show()
        self.poll_timer.start()
        self.live_timer.start()
        self.refresh()

    def _worker_output(self, study_id: str, _chunk: str) -> None:
        if self._selected_study_id() == study_id:
            self.worker_message.setText(
                f"Local worker active for {study_id}. Durable job state refreshes "
                "automatically while execution continues outside the Qt thread."
            )
            self.worker_message.show()

    def _worker_finished(self, study_id: str, exit_code: int, output: str) -> None:
        self.poll_timer.stop()
        self.live_timer.stop()
        self.refresh()
        self._refresh_live()
        if exit_code == 0:
            self.worker_message.setText(
                f"Worker finished for {study_id}. The table now reflects the "
                "latest durable Study state; any displayed GridWorld is the last presentation frame."
            )
            self.worker_message.show()
            return

        detail = output[-2500:] if output else "worker exited without diagnostic output"
        self.error.setText(
            "Study worker stopped with an infrastructure/runtime error. "
            "Durable state was reloaded; scientific failures are not inferred "
            "from the process exit code.\n"
            f"Technical detail: {detail}"
        )
        self.error.show()
        self.worker_message.hide()
