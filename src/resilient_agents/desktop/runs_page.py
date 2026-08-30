"""Truthful durable-study Runs workspace."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
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

from .study_read_model import DesktopStudyReadModel, StudyListItem
from .widgets import EmptyState, MetricItem, SectionHeader, VerticalDivider


class RunsPage(QWidget):
    study_selected = Signal(str)

    def __init__(self, read_model: DesktopStudyReadModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.read_model = read_model
        self.items: tuple[StudyListItem, ...] = ()
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(38, 28, 42, 34)
        root.setSpacing(17)

        header = QHBoxLayout()
        title_block = QVBoxLayout()
        title_block.setSpacing(4)
        title = QLabel("Runs")
        title.setObjectName("PageTitle")
        lead = QLabel("Durable Study lifecycle state from the Python backend — no synthesized progress or replay.")
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        title_block.addWidget(title)
        title_block.addWidget(lead)
        header.addLayout(title_block, 1)
        refresh = QPushButton("Refresh")
        refresh.setObjectName("SecondaryButton")
        refresh.setToolTip("Reload study state from the durable StudyStore on disk.")
        refresh.clicked.connect(self.refresh)
        header.addWidget(refresh, 0, Qt.AlignmentFlag.AlignTop)
        root.addLayout(header)

        self.summary = QFrame()
        self.summary.setObjectName("Surface")
        self.summary_layout = QHBoxLayout(self.summary)
        self.summary_layout.setContentsMargins(18, 12, 18, 12)
        self.summary_layout.setSpacing(16)
        root.addWidget(self.summary)

        root.addWidget(SectionHeader("Study history", "Select a row to inspect its durable artifacts."))

        self.empty = EmptyState(
            "No studies yet",
            "No framework-neutral Study has been created in this workspace. Exploratory studies will appear here after they are created through the application.",
        )
        root.addWidget(self.empty)

        self.table = QTableWidget(0, 7)
        self.table.setObjectName("StudyTable")
        self.table.setHorizontalHeaderLabels(("Study", "Evidence", "Stage", "Progress", "Status", "Failures", "Finalized"))
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(False)
        self.table.itemSelectionChanged.connect(self._emit_selection)
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

    def _clear_summary(self) -> None:
        while self.summary_layout.count():
            item = self.summary_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
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
        progress.setAccessibleName(f"{item.resolved_jobs} of {item.total_jobs} study jobs scientifically resolved")
        return progress

    def refresh(self) -> None:
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
        for row_index, item in enumerate(self.items):
            self.table.insertRow(row_index)
            study = self._text_item(item.study_id, user_data=item.study_id)
            study.setToolTip(f"Protocol: {item.protocol_version}")
            self.table.setItem(row_index, 0, study)
            self.table.setItem(row_index, 1, self._text_item(item.evidence_class.title()))
            self.table.setItem(row_index, 2, self._text_item(item.stage_label))
            self.table.setCellWidget(row_index, 3, self._progress_widget(item))
            self.table.setItem(row_index, 4, self._text_item(item.status.replace("-", " ").title()))
            failures = item.scientific_failures + item.infrastructure_failures
            failure_text = "—" if failures == 0 else str(failures)
            failure_cell = self._text_item(failure_text)
            if failures:
                failure_cell.setToolTip(f"Scientific: {item.scientific_failures}; infrastructure: {item.infrastructure_failures}")
            self.table.setItem(row_index, 5, failure_cell)
            self.table.setItem(row_index, 6, self._text_item("Yes" if item.finalized else "No"))

        has_items = bool(self.items)
        self.empty.setVisible(not has_items)
        self.table.setVisible(has_items)

    def _emit_selection(self) -> None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return
        item = self.table.item(selected[0].row(), 0)
        if item is None:
            return
        study_id = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(study_id, str) and study_id:
            self.study_selected.emit(study_id)
