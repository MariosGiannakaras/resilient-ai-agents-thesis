"""Experiment-first configuration and immutable Thesis review surface."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .exploratory_preview import DesktopExploratoryPreviewModel, ExploratoryPlanPreview
from .exploratory_study import DesktopExploratoryStudyModel
from .protocol import FrozenProtocolSummary
from .widgets import SectionHeader, StatusPill


class ExperimentPage(QWidget):
    """Four-step mental model with read-only Thesis and constrained DEVELOPMENT modes."""

    study_created = Signal(str)
    THESIS = 0
    DEVELOPMENT = 1

    def __init__(
        self,
        protocol: FrozenProtocolSummary,
        *,
        repo_root: Path,
        writable_root: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.protocol = protocol
        self.preview_model = DesktopExploratoryPreviewModel(repo_root=repo_root)
        self.study_model = DesktopExploratoryStudyModel(
            repo_root=repo_root,
            writable_root=writable_root,
        )
        self._preview: ExploratoryPlanPreview | None = None
        self._created_study_id: str | None = None
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(36, 26, 40, 32)
        root.setSpacing(14)

        header = QHBoxLayout()
        title_block = QVBoxLayout()
        title = QLabel("Experiment")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Understand the fixed Thesis experiment or prepare a backend-constrained DEVELOPMENT experiment."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        title_block.addWidget(title)
        title_block.addWidget(lead)
        header.addLayout(title_block, 1)
        self.mode_group = QButtonGroup(self)
        self.mode_group.setExclusive(True)
        self.thesis_button = QPushButton("Thesis experiment")
        self.development_button = QPushButton("DEVELOPMENT")
        for index, button in enumerate((self.thesis_button, self.development_button)):
            button.setCheckable(True)
            button.setAccessibleName(button.text())
            self.mode_group.addButton(button, index)
            header.addWidget(button, 0, Qt.AlignmentFlag.AlignTop)
        self.thesis_button.setChecked(True)
        self.mode_group.idClicked.connect(self.set_mode)
        root.addLayout(header)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_thesis())
        self.stack.addWidget(self._build_development())
        root.addWidget(self.stack, 1)
        self.set_mode(self.THESIS)

    def set_mode(self, mode: int) -> None:
        if mode not in (self.THESIS, self.DEVELOPMENT):
            raise ValueError("unknown experiment mode")
        self.stack.setCurrentIndex(mode)
        self.thesis_button.setChecked(mode == self.THESIS)
        self.development_button.setChecked(mode == self.DEVELOPMENT)

    def _build_thesis(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(13)

        state = QFrame()
        state.setObjectName("Surface")
        state_layout = QHBoxLayout(state)
        state_layout.setContentsMargins(18, 13, 18, 13)
        text = QVBoxLayout()
        heading = QLabel("Frozen Thesis experiment")
        heading.setObjectName("SectionTitle")
        detail = QLabel(
            "protocol-v2.1 · final scientific settings are read-only · all five retained methods are always included"
        )
        detail.setObjectName("SectionHint")
        detail.setWordWrap(True)
        text.addWidget(heading)
        text.addWidget(detail)
        state_layout.addLayout(text, 1)
        state_layout.addWidget(StatusPill("FINAL EXECUTION LOCKED", kind="development"))
        layout.addWidget(state)

        layout.addWidget(
            SectionHeader(
                "Five methods",
                "These methods are fixed by the scientific protocol; there is no deselection control in Thesis mode.",
            )
        )
        method_grid = QGridLayout()
        method_grid.setHorizontalSpacing(10)
        method_grid.setVerticalSpacing(10)
        for index, method in enumerate(self.protocol.methods):
            card = QFrame()
            card.setObjectName("Surface")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 12, 15, 12)
            name = QLabel(method.name)
            name.setObjectName("SectionTitle")
            desc = QLabel(method.description)
            desc.setObjectName("SectionHint")
            desc.setWordWrap(True)
            card_layout.addWidget(name)
            card_layout.addWidget(desc)
            method_grid.addWidget(card, index // 3, index % 3)
        layout.addLayout(method_grid)

        layout.addWidget(SectionHeader("Scientific flow"))
        flow = QFrame()
        flow.setObjectName("Surface")
        flow_layout = QGridLayout(flow)
        flow_layout.setContentsMargins(16, 14, 16, 14)
        flow_layout.setHorizontalSpacing(18)
        items = (
            ("1 · Phase A", "Independent nominal learning under the common actual-environment-interaction fairness budget."),
            ("2 · Exact handoff", "Each method/root/layout unit enters Phase B from its own exact learned checkpoint state."),
            ("3 · Phase B", "Matched disturbance deployments compare Frozen (learning off) with Adaptive (learning continues)."),
            ("4 · Results", "Validated stored outputs answer RQ1 Learning, RQ2 Resilience/Adaptation and RQ3 Recovery."),
        )
        for index, (name_text, body) in enumerate(items):
            box = QFrame()
            box.setObjectName("SubtleSurface")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(13, 11, 13, 11)
            label = QLabel(name_text)
            label.setObjectName("ReviewValue")
            note = QLabel(body)
            note.setObjectName("SectionHint")
            note.setWordWrap(True)
            box_layout.addWidget(label)
            box_layout.addWidget(note)
            flow_layout.addWidget(box, index // 2, index % 2)
        layout.addWidget(flow)

        regimes = QLabel(
            "FN = Frozen nominal · FD = Frozen disturbed · AN = Adaptive nominal · AD = Adaptive disturbed. "
            "Frozen and Adaptive are matched deployment regimes of the same method, never algorithms to select between."
        )
        regimes.setObjectName("DevelopmentText")
        regimes.setWordWrap(True)
        layout.addWidget(regimes)

        technical = QPushButton("Technical details")
        technical.setCheckable(True)
        technical.setAccessibleName("Show protocol technical details")
        details = QLabel(
            f"Authority: {self.protocol.protocol_id} / {self.protocol.decision_id} (amends {self.protocol.amended_decision_id}). "
            f"Protocol dimensions: {self.protocol.root_count} independent roots, {self.protocol.layout_count} layouts, "
            f"{self.protocol.condition_count} Phase-B conditions. RQ3 uses {self.protocol.recovery_window_size}-interaction "
            f"windows through the fixed Phase-B observation horizon. Exact identities, seeds, hashes and checkpoints are not exposed here."
        )
        details.setObjectName("SectionHint")
        details.setWordWrap(True)
        details.setVisible(False)
        technical.toggled.connect(details.setVisible)
        layout.addWidget(technical, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(details)
        layout.addStretch(1)
        scroll.setWidget(content)
        return scroll

    def _build_development(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        warning = QFrame()
        warning.setObjectName("SubtleSurface")
        warning_layout = QHBoxLayout(warning)
        warning_layout.setContentsMargins(16, 12, 16, 12)
        warning_layout.addWidget(StatusPill("DEVELOPMENT · NON-CONFIRMATORY", kind="development"))
        warning_text = QLabel(
            "Uses only the backend development pool. It cannot access final-reserve roots/layouts/outcomes and cannot create Thesis evidence."
        )
        warning_text.setObjectName("SectionHint")
        warning_text.setWordWrap(True)
        warning_layout.addWidget(warning_text, 1)
        layout.addWidget(warning)

        self.development_stack = QStackedWidget()
        self.development_stack.addWidget(self._build_configure())
        self.development_stack.addWidget(self._build_review())
        layout.addWidget(self.development_stack, 1)
        return page

    def _build_configure(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(11)
        layout.addWidget(
            SectionHeader(
                "Configure",
                "Choose only options supported by the DEVELOPMENT recipe, then review the resolved backend plan before creation.",
            )
        )
        form = QFrame()
        form.setObjectName("Surface")
        grid = QGridLayout(form)
        grid.setContentsMargins(18, 16, 18, 16)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(10)

        grid.addWidget(QLabel("Methods"), 0, 0, Qt.AlignmentFlag.AlignTop)
        methods_box = QWidget()
        methods_layout = QVBoxLayout(methods_box)
        methods_layout.setContentsMargins(0, 0, 0, 0)
        self.method_checks: dict[str, QCheckBox] = {}
        for method in self.protocol.methods:
            check = QCheckBox(method.name)
            check.setChecked(True)
            check.setToolTip(method.description)
            check.setAccessibleName(f"Include {method.name} in DEVELOPMENT experiment")
            methods_layout.addWidget(check)
            self.method_checks[method.method_id] = check
        grid.addWidget(methods_box, 0, 1)

        roots_label = QLabel("Development roots")
        self.root_count = QSpinBox()
        self.root_count.setRange(1, self.preview_model.max_root_count)
        self.root_count.setValue(1)
        self.root_count.setAccessibleName("Number of development roots")
        roots_label.setBuddy(self.root_count)
        grid.addWidget(roots_label, 1, 0)
        grid.addWidget(self.root_count, 1, 1)

        layouts_label = QLabel("Development layouts")
        self.layout_count = QSpinBox()
        self.layout_count.setRange(1, self.preview_model.max_layout_count)
        self.layout_count.setValue(1)
        self.layout_count.setAccessibleName("Number of development layouts")
        layouts_label.setBuddy(self.layout_count)
        grid.addWidget(layouts_label, 2, 0)
        grid.addWidget(self.layout_count, 2, 1)

        label_label = QLabel("Label (optional)")
        self.study_label = QLineEdit()
        self.study_label.setPlaceholderText("e.g. smoke-test")
        self.study_label.setAccessibleName("Development experiment label")
        label_label.setBuddy(self.study_label)
        grid.addWidget(label_label, 3, 0)
        grid.addWidget(self.study_label, 3, 1)
        layout.addWidget(form)

        self.configure_error = QLabel()
        self.configure_error.setObjectName("ErrorText")
        self.configure_error.setWordWrap(True)
        self.configure_error.hide()
        layout.addWidget(self.configure_error)
        actions = QHBoxLayout()
        actions.addStretch(1)
        review = QPushButton("Review plan")
        review.setObjectName("PrimaryButton")
        review.setAccessibleName("Review DEVELOPMENT experiment plan")
        review.clicked.connect(self.review_development)
        actions.addWidget(review)
        layout.addLayout(actions)
        layout.addStretch(1)
        return page

    def _build_review(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(11)
        layout.addWidget(
            SectionHeader(
                "Review",
                "This is the backend-resolved DEVELOPMENT plan. Creation records durable work; it does not start any scientific job.",
            )
        )
        self.review_surface = QFrame()
        self.review_surface.setObjectName("Surface")
        review_layout = QVBoxLayout(self.review_surface)
        review_layout.setContentsMargins(18, 16, 18, 16)
        self.review_title = QLabel("No plan resolved")
        self.review_title.setObjectName("SectionTitle")
        self.review_detail = QLabel()
        self.review_detail.setObjectName("PageLead")
        self.review_detail.setWordWrap(True)
        self.review_secondary = QLabel()
        self.review_secondary.setObjectName("SectionHint")
        self.review_secondary.setWordWrap(True)
        review_layout.addWidget(self.review_title)
        review_layout.addWidget(self.review_detail)
        review_layout.addWidget(self.review_secondary)
        layout.addWidget(self.review_surface)

        actions = QHBoxLayout()
        back = QPushButton("Back to Configure")
        back.setObjectName("SecondaryButton")
        back.clicked.connect(lambda: self.development_stack.setCurrentIndex(0))
        actions.addWidget(back)
        actions.addStretch(1)
        self.create_button = QPushButton("Create DEVELOPMENT experiment")
        self.create_button.setObjectName("PrimaryButton")
        self.create_button.setAccessibleName("Create the reviewed DEVELOPMENT experiment")
        self.create_button.clicked.connect(self.create_development)
        actions.addWidget(self.create_button)
        layout.addLayout(actions)
        layout.addStretch(1)
        return page

    def selected_method_ids(self) -> tuple[str, ...]:
        return tuple(
            method_id for method_id, check in self.method_checks.items() if check.isChecked()
        )

    def review_development(self) -> None:
        self.configure_error.hide()
        try:
            preview = self.preview_model.preview(
                selected_method_ids=self.selected_method_ids(),
                root_count=self.root_count.value(),
                layout_count=self.layout_count.value(),
            )
        except Exception as exc:
            self._preview = None
            self.configure_error.setText(
                "The DEVELOPMENT plan is not valid, so nothing can be created. "
                f"Adjust the configuration and review again. Technical detail: {type(exc).__name__}: {exc}"
            )
            self.configure_error.show()
            return
        self._preview = preview
        self._created_study_id = None
        names = [
            method.name
            for method in self.protocol.methods
            if method.method_id in self.selected_method_ids()
        ]
        self.review_title.setText("Configure → Review → Create")
        self.review_detail.setText(
            f"Methods: {', '.join(names)} · {preview.root_count} development root(s) · "
            f"{preview.layout_count} development layout(s) · {preview.condition_count} disturbance condition(s)."
        )
        self.review_secondary.setText(
            f"Backend plan: Phase A {preview.phase_a_jobs} job(s), Phase B {preview.phase_b_jobs} job(s), "
            f"then validation/analysis/export; {preview.total_jobs} total planned jobs. "
            "These counts are planning detail, not scientific results."
        )
        self.create_button.setEnabled(True)
        self.create_button.setText("Create DEVELOPMENT experiment")
        self.development_stack.setCurrentIndex(1)

    def create_development(self) -> None:
        if self._preview is None or self._created_study_id is not None:
            return
        self.create_button.setEnabled(False)
        self.create_button.setText("Creating…")
        try:
            created = self.study_model.create(
                selected_method_ids=self.selected_method_ids(),
                root_count=self.root_count.value(),
                layout_count=self.layout_count.value(),
                study_label=self.study_label.text().strip(),
            )
        except Exception as exc:
            self.create_button.setEnabled(True)
            self.create_button.setText("Create DEVELOPMENT experiment")
            self.review_secondary.setText(
                "The DEVELOPMENT experiment was not created; no job executed. "
                f"Technical detail: {type(exc).__name__}: {exc}"
            )
            return
        self._created_study_id = created.study_id
        self.create_button.setText("Created")
        self.review_secondary.setText(
            f"Created DEVELOPMENT experiment {created.study_id}. No job has executed. Open Run to inspect durable state before starting work."
        )
        self.study_created.emit(created.study_id)
