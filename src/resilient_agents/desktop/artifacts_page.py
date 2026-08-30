"""Read-only study artifact and provenance workspace."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .study_read_model import DesktopStudyReadModel
from .widgets import EmptyState, SectionHeader


class ArtifactsPage(QWidget):
    def __init__(self, read_model: DesktopStudyReadModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.read_model = read_model
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(38, 28, 42, 34)
        root.setSpacing(17)

        header = QHBoxLayout()
        title_block = QVBoxLayout()
        title_block.setSpacing(4)
        title = QLabel("Artifacts")
        title.setObjectName("PageTitle")
        lead = QLabel("Content-addressed Study artifacts and reproducibility lineage from durable evidence records.")
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        title_block.addWidget(title)
        title_block.addWidget(lead)
        header.addLayout(title_block, 1)
        refresh = QPushButton("Refresh")
        refresh.setObjectName("SecondaryButton")
        refresh.clicked.connect(self.refresh)
        header.addWidget(refresh, 0, Qt.AlignmentFlag.AlignTop)
        root.addLayout(header)

        controls = QHBoxLayout()
        controls.setSpacing(10)
        label = QLabel("Study")
        label.setObjectName("MethodName")
        self.study_picker = QComboBox()
        self.study_picker.setMinimumWidth(320)
        self.study_picker.setAccessibleName("Study artifact source")
        self.study_picker.currentIndexChanged.connect(self._load_selected)
        controls.addWidget(label)
        controls.addWidget(self.study_picker)
        controls.addStretch(1)
        root.addLayout(controls)

        root.addWidget(
            SectionHeader(
                "Recorded artifacts",
                "Paths and hashes are backend-owned evidence metadata. This view never scans arbitrary filesystem locations.",
            )
        )

        self.empty = EmptyState(
            "No recorded artifacts",
            "Choose a study with finalized or intermediate Study artifacts. Nothing is fabricated when a study has not produced an artifact yet.",
        )
        root.addWidget(self.empty)

        self.table = QTableWidget(0, 5)
        self.table.setObjectName("ArtifactTable")
        self.table.setHorizontalHeaderLabels(("Artifact", "Role", "Evidence", "Path", "SHA-256"))
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        root.addWidget(self.table, 1)

        self.error = QLabel()
        self.error.setObjectName("ErrorText")
        self.error.setWordWrap(True)
        self.error.hide()
        root.addWidget(self.error)
        self.refresh()

    @staticmethod
    def _cell(text: str, tooltip: str | None = None) -> QTableWidgetItem:
        cell = QTableWidgetItem(text)
        if tooltip:
            cell.setToolTip(tooltip)
        return cell

    def set_study(self, study_id: str) -> None:
        index = self.study_picker.findData(study_id)
        if index >= 0:
            self.study_picker.setCurrentIndex(index)

    def refresh(self) -> None:
        current = self.study_picker.currentData()
        self.study_picker.blockSignals(True)
        self.study_picker.clear()
        self.error.hide()
        try:
            studies = self.read_model.studies()
        except Exception as exc:
            studies = ()
            self.error.setText(
                "Study list could not be read. No evidence was changed.\n"
                f"Technical detail: {type(exc).__name__}: {exc}"
            )
            self.error.show()
        for item in studies:
            self.study_picker.addItem(item.study_id, item.study_id)
        self.study_picker.blockSignals(False)

        if current is not None:
            index = self.study_picker.findData(current)
            if index >= 0:
                self.study_picker.setCurrentIndex(index)
        self.study_picker.setEnabled(self.study_picker.count() > 0)
        self._load_selected()

    def _load_selected(self) -> None:
        self.table.setRowCount(0)
        study_id = self.study_picker.currentData()
        if not isinstance(study_id, str) or not study_id:
            self.empty.setVisible(True)
            self.table.setVisible(False)
            return
        self.error.hide()
        try:
            artifacts = self.read_model.artifacts(study_id)
        except Exception as exc:
            artifacts = ()
            self.error.setText(
                f"Artifacts for {study_id} could not be read. No evidence was changed.\n"
                f"Technical detail: {type(exc).__name__}: {exc}"
            )
            self.error.show()
        for row_index, artifact in enumerate(artifacts):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, self._cell(artifact.artifact_id))
            self.table.setItem(row_index, 1, self._cell(artifact.role.replace("-", " ").title()))
            self.table.setItem(row_index, 2, self._cell(artifact.evidence_class.title()))
            self.table.setItem(row_index, 3, self._cell(artifact.relative_path, artifact.relative_path))
            self.table.setItem(row_index, 4, self._cell(artifact.sha256[:12] + "…", artifact.sha256))
        has_artifacts = bool(artifacts)
        self.empty.setVisible(not has_artifacts)
        self.table.setVisible(has_artifacts)
