"""Read-only study artifact and provenance workspace."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QGridLayout,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .study_read_model import ArtifactListItem, DesktopStudyReadModel
from .widgets import EmptyState, SectionHeader


class ArtifactsPage(QWidget):
    def __init__(self, read_model: DesktopStudyReadModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.read_model = read_model
        self._artifacts: tuple[ArtifactListItem, ...] = ()
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(38, 28, 42, 34)
        root.setSpacing(15)

        header = QHBoxLayout()
        title_block = QVBoxLayout()
        title_block.setSpacing(4)
        title = QLabel("Artifacts")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Content-addressed Study artifacts and reproducibility lineage from durable evidence records."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        title_block.addWidget(title)
        title_block.addWidget(lead)
        header.addLayout(title_block, 1)
        refresh = QPushButton("Refresh")
        refresh.setObjectName("SecondaryButton")
        refresh.setToolTip("Reload registered artifacts from the durable StudyStore.")
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
        label.setBuddy(self.study_picker)
        self.study_picker.currentIndexChanged.connect(self._load_selected)
        controls.addWidget(label)
        controls.addWidget(self.study_picker)
        controls.addStretch(1)
        root.addLayout(controls)

        root.addWidget(
            SectionHeader(
                "Recorded artifacts",
                "Only backend-registered paths, hashes and lineage are shown. This view never scans arbitrary filesystem locations.",
            )
        )

        self.empty = EmptyState(
            "No recorded artifacts",
            "Choose a study with finalized or intermediate Study artifacts. Nothing is fabricated when a study has not produced an artifact yet.",
        )
        root.addWidget(self.empty)

        self.table = QTableWidget(0, 5)
        self.table.setObjectName("ArtifactTable")
        self.table.setAccessibleName("Registered study artifacts")
        self.table.setHorizontalHeaderLabels(("Artifact", "Role", "Evidence", "Path", "SHA-256"))
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.itemSelectionChanged.connect(self._show_selected_artifact)
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        root.addWidget(self.table, 1)

        self.detail = QFrame()
        self.detail.setObjectName("SubtleSurface")
        detail_layout = QVBoxLayout(self.detail)
        detail_layout.setContentsMargins(17, 12, 17, 13)
        detail_layout.setSpacing(8)
        detail_header = QHBoxLayout()
        detail_title = QLabel("Selected artifact provenance")
        detail_title.setObjectName("SectionTitle")
        detail_header.addWidget(detail_title)
        detail_header.addStretch(1)
        self.detail_identity = QLabel()
        self.detail_identity.setObjectName("StatusDevelopment")
        detail_header.addWidget(self.detail_identity)
        detail_layout.addLayout(detail_header)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(5)
        self.detail_values: dict[str, QLabel] = {}
        fields = (
            ("identity", "Artifact"),
            ("path", "Registered path"),
            ("sha", "SHA-256"),
            ("jobs", "Producer jobs"),
            ("upstream", "Upstream artifacts"),
        )
        for row, (key, caption) in enumerate(fields):
            caption_label = QLabel(caption)
            caption_label.setObjectName("ReviewLabel")
            caption_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            value_label = QLabel()
            value_label.setObjectName("ReviewValue")
            value_label.setWordWrap(True)
            value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            grid.addWidget(caption_label, row, 0)
            grid.addWidget(value_label, row, 1)
            self.detail_values[key] = value_label
        grid.setColumnStretch(1, 1)
        detail_layout.addLayout(grid)
        self.detail.hide()
        root.addWidget(self.detail)

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

    @staticmethod
    def _lineage_text(values: tuple[str, ...]) -> tuple[str, str]:
        if not values:
            return "None recorded", "No lineage IDs are registered for this artifact."
        visible = ", ".join(values[:3])
        if len(values) > 3:
            visible += f"  +{len(values) - 3} more"
        return visible, "\n".join(values)

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
        self.detail.hide()
        self._artifacts = ()
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
        self._artifacts = tuple(artifacts)
        for row_index, artifact in enumerate(self._artifacts):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, self._cell(artifact.artifact_id))
            self.table.setItem(row_index, 1, self._cell(artifact.role.replace("-", " ").title()))
            self.table.setItem(row_index, 2, self._cell(artifact.evidence_class.title()))
            self.table.setItem(row_index, 3, self._cell(artifact.relative_path, artifact.relative_path))
            self.table.setItem(row_index, 4, self._cell(artifact.sha256[:12] + "…", artifact.sha256))
        has_artifacts = bool(self._artifacts)
        self.empty.setVisible(not has_artifacts)
        self.table.setVisible(has_artifacts)
        if has_artifacts:
            self.table.selectRow(0)
        else:
            self.detail.hide()

    def _show_selected_artifact(self) -> None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            self.detail.hide()
            return
        row = selected[0].row()
        if row < 0 or row >= len(self._artifacts):
            self.detail.hide()
            return
        artifact = self._artifacts[row]
        jobs, jobs_tooltip = self._lineage_text(artifact.source_job_ids)
        upstream, upstream_tooltip = self._lineage_text(artifact.source_artifact_ids)
        self.detail_identity.setText(artifact.evidence_class.upper())
        self.detail_identity.setToolTip(
            f"Evidence class: {artifact.evidence_class}; role: {artifact.role}"
        )
        self.detail_values["identity"].setText(
            f"{artifact.artifact_id} · {artifact.role.replace('-', ' ').title()}"
        )
        self.detail_values["path"].setText(artifact.relative_path)
        self.detail_values["path"].setToolTip(artifact.relative_path)
        self.detail_values["sha"].setText(artifact.sha256)
        self.detail_values["sha"].setToolTip("Registered content hash from StudyStore lineage.")
        self.detail_values["jobs"].setText(jobs)
        self.detail_values["jobs"].setToolTip(jobs_tooltip)
        self.detail_values["upstream"].setText(upstream)
        self.detail_values["upstream"].setToolTip(upstream_tooltip)
        self.detail.show()
