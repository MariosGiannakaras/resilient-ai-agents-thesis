"""User-first Evidence surface over backend-registered artifacts only."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .study_read_model import ArtifactListItem, DesktopStudyReadModel, StudyListItem
from .widgets import StatusPill


_OUTPUT_LABELS = {
    "analysis-data": "analysis data",
    "analysis-table": "analysis table",
    "figure": "figure",
    "thesis-table": "thesis table",
    "thesis-figure": "thesis figure",
    "presentation-asset": "presentation asset",
    "evidence-package": "evidence package",
}


class EvidencePage(QWidget):
    def __init__(self, model: DesktopStudyReadModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.model = model
        self._studies: tuple[StudyListItem, ...] = ()
        self._artifacts: tuple[ArtifactListItem, ...] = ()
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(34, 24, 36, 28)
        root.setSpacing(12)
        header = QHBoxLayout()
        titles = QVBoxLayout()
        title = QLabel("Evidence")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "See what is ready and reproducible first. Artifact IDs, paths and "
            "hashes are available as technical detail."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        titles.addWidget(title)
        titles.addWidget(lead)
        header.addLayout(titles, 1)
        header.addWidget(StatusPill("REGISTERED STATE ONLY", kind="frozen"))
        root.addLayout(header)

        selection = QHBoxLayout()
        label = QLabel("Experiment record")
        self.study_combo = QComboBox()
        self.study_combo.setAccessibleName("Experiment record for evidence")
        self.study_combo.currentIndexChanged.connect(self._selection_changed)
        label.setBuddy(self.study_combo)
        selection.addWidget(label)
        selection.addWidget(self.study_combo, 1)
        root.addLayout(selection)

        self.summary = QLabel()
        self.summary.setObjectName("PageLead")
        self.summary.setWordWrap(True)
        root.addWidget(self.summary)

        cards = QGridLayout()
        cards.setSpacing(10)
        self.validation_card = self._card("Validation")
        self.analysis_card = self._card("Analysis")
        self.export_card = self._card("Evidence package")
        cards.addWidget(self.validation_card[0], 0, 0)
        cards.addWidget(self.analysis_card[0], 0, 1)
        cards.addWidget(self.export_card[0], 0, 2)
        root.addLayout(cards)

        self.outputs = QLabel()
        self.outputs.setObjectName("SectionHint")
        self.outputs.setWordWrap(True)
        self.outputs.setAccessibleName("Registered result and export outputs")
        root.addWidget(self.outputs)

        self.next_action = QLabel()
        self.next_action.setObjectName("ReviewValue")
        self.next_action.setWordWrap(True)
        self.next_action.setAccessibleName("Evidence next action")
        root.addWidget(self.next_action)

        self.technical_button = QPushButton("Technical / reproducibility details")
        self.technical_button.setCheckable(True)
        self.technical_button.setAccessibleName(
            "Show evidence technical and reproducibility details"
        )
        root.addWidget(self.technical_button, 0, Qt.AlignmentFlag.AlignLeft)

        self.technical_scroll = QScrollArea()
        self.technical_scroll.setWidgetResizable(True)
        self.technical_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.technical_content = QWidget()
        self.technical_layout = QVBoxLayout(self.technical_content)
        self.technical_layout.setContentsMargins(0, 0, 8, 0)
        self.technical_layout.setSpacing(8)
        self.technical_scroll.setWidget(self.technical_content)
        self.technical_scroll.hide()
        self.technical_button.toggled.connect(self.technical_scroll.setVisible)
        root.addWidget(self.technical_scroll, 1)
        self.refresh()

    @staticmethod
    def _card(title: str) -> tuple[QFrame, QLabel, QLabel]:
        frame = QFrame()
        frame.setObjectName("Surface")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 13, 16, 13)
        heading = QLabel(title)
        heading.setObjectName("SectionTitle")
        state = QLabel("Unavailable")
        state.setObjectName("ReviewValue")
        detail = QLabel("No experiment selected.")
        detail.setObjectName("SectionHint")
        detail.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(state)
        layout.addWidget(detail)
        return frame, state, detail

    def refresh(self) -> None:
        selected = self.selected_study_id()
        self._studies = self.model.studies()
        self.study_combo.blockSignals(True)
        self.study_combo.clear()
        for item in self._studies:
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

    def set_study(self, study_id: str) -> None:
        index = self.study_combo.findData(study_id)
        if index >= 0:
            self.study_combo.setCurrentIndex(index)

    def _selection_changed(self, *_args) -> None:
        study_id = self.selected_study_id()
        item = next(
            (entry for entry in self._studies if entry.study_id == study_id),
            None,
        )
        self._artifacts = () if study_id is None else self.model.artifacts(study_id)
        self._render(item)

    def _render(self, item: StudyListItem | None) -> None:
        if item is None:
            self.summary.setText(
                "No durable experiment record is available yet. Evidence is never "
                "inferred from arbitrary files."
            )
            for _, state, detail in (
                self.validation_card,
                self.analysis_card,
                self.export_card,
            ):
                state.setText("Unavailable")
                detail.setText("No backend-registered evidence is available.")
            self.outputs.setText("Registered outputs: none.")
            self.next_action.setText(
                "Next: create a DEVELOPMENT experiment in Experiment, then run it "
                "to produce backend-registered evidence."
            )
            self._render_technical(None)
            return

        evidence_label = (
            "DEVELOPMENT · NON-CONFIRMATORY"
            if item.evidence_class == "development"
            else item.evidence_class.upper()
        )
        self.summary.setText(
            f"{evidence_label} · {item.study_id} · {item.stage_label} · "
            f"{item.resolved_jobs}/{item.total_jobs} jobs resolved. Unavailable "
            "evidence stays unavailable rather than being inferred from the filesystem."
        )
        roles = {artifact.role for artifact in self._artifacts}
        validation_ready = "validation-report" in roles
        analysis_ready = bool({"analysis-data", "analysis-table"} & roles)
        export_ready = "evidence-package" in roles
        self._set_card(
            self.validation_card,
            available=validation_ready,
            available_text="A backend-registered validation report is available.",
            unavailable_text=(
                "No validation report is registered. Complete the required run and "
                "validation stage before analysis."
            ),
        )
        self._set_card(
            self.analysis_card,
            available=analysis_ready,
            available_text="Backend-registered analysis outputs are available.",
            unavailable_text=(
                "No validated analysis output is registered. Validation must complete "
                "before analysis can become available."
            ),
        )
        self._set_card(
            self.export_card,
            available=export_ready,
            available_text="A reproducible backend-registered evidence package is available.",
            unavailable_text=(
                "No evidence package is registered. Analysis/export must complete "
                "before a reproducible package can be shown."
            ),
        )
        output_names = sorted(
            {_OUTPUT_LABELS[role] for role in roles if role in _OUTPUT_LABELS}
        )
        self.outputs.setText(
            "Registered outputs: " + (", ".join(output_names) if output_names else "none") + "."
        )
        if export_ready:
            self.next_action.setText(
                "Next: inspect the registered evidence package or open Technical / "
                "reproducibility details for lineage and checksums."
            )
        elif analysis_ready:
            self.next_action.setText(
                "Next: complete the registered export stage to produce a reproducible "
                "evidence package."
            )
        elif validation_ready:
            self.next_action.setText(
                "Next: complete the registered analysis stage; the UI will display "
                "only stored validated outputs."
            )
        else:
            self.next_action.setText(
                "Next: complete the durable experiment and validation stage. No "
                "analysis or export is inferred ahead of the backend."
            )
        self._render_technical(item)

    @staticmethod
    def _set_card(
        card: tuple[QFrame, QLabel, QLabel],
        *,
        available: bool,
        available_text: str,
        unavailable_text: str,
    ) -> None:
        _, state, detail = card
        state.setText("Available" if available else "Not available yet")
        state.setAccessibleName(state.text())
        detail.setText(available_text if available else unavailable_text)

    def _render_technical(self, item: StudyListItem | None) -> None:
        while self.technical_layout.count():
            entry = self.technical_layout.takeAt(0)
            widget = entry.widget()
            if widget is not None:
                widget.deleteLater()
        if item is None:
            self.technical_layout.addWidget(
                QLabel("No registered provenance detail is available.")
            )
            self.technical_layout.addStretch(1)
            return

        intro = QLabel(
            f"Protocol: {item.protocol_version} · evidence class: "
            f"{item.evidence_class} · backend state: {item.status}. Only "
            "backend-registered artifact lineage appears below."
        )
        intro.setObjectName("SectionHint")
        intro.setWordWrap(True)
        self.technical_layout.addWidget(intro)
        if not self._artifacts:
            self.technical_layout.addWidget(QLabel("No registered artifacts."))
        for artifact in self._artifacts:
            frame = QFrame()
            frame.setObjectName("SubtleSurface")
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(12, 9, 12, 9)
            title = QLabel(f"{artifact.role} · {artifact.artifact_id}")
            title.setObjectName("ReviewValue")
            detail = QLabel(
                f"Path: {artifact.relative_path}\nSHA-256: {artifact.sha256}\n"
                f"Sources: {artifact.source_job_count} job(s), "
                f"{artifact.source_artifact_count} artifact(s)"
            )
            detail.setObjectName("SectionHint")
            detail.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            detail.setWordWrap(True)
            layout.addWidget(title)
            layout.addWidget(detail)
            self.technical_layout.addWidget(frame)
        self.technical_layout.addStretch(1)
