"""Recipe-first Study entry journey for the PySide6 application."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .exploratory_preview import DesktopExploratoryPreviewModel, ExploratoryPlanPreview
from .protocol import FrozenProtocolSummary, MethodSummary
from .study_page import ThesisStudyPage
from .widgets import StatusPill


class StepRail(QWidget):
    """Compact three-step progress cue for the exploratory configuration flow."""

    def __init__(self, current_step: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        for index, label in enumerate(("Models", "Customize", "Review"), start=1):
            pill = QLabel(f"{index}  {label}")
            if index < current_step:
                pill.setObjectName("StepComplete")
            elif index == current_step:
                pill.setObjectName("StepCurrent")
            else:
                pill.setObjectName("StepUpcoming")
            pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(pill)
            if index < 3:
                arrow = QLabel("→")
                arrow.setObjectName("StepArrow")
                arrow.setAccessibleName("then")
                layout.addWidget(arrow)


class StudyChoiceCard(QFrame):
    selected = Signal()

    def __init__(
        self,
        *,
        title: str,
        description: str,
        status_text: str,
        status_kind: str,
        facts: tuple[str, ...],
        button_text: str,
        primary: bool,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("ChoiceCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(10)
        title_label = QLabel(title)
        title_label.setObjectName("ChoiceTitle")
        top.addWidget(title_label)
        top.addStretch(1)
        top.addWidget(StatusPill(status_text, kind=status_kind))
        layout.addLayout(top)

        body = QLabel(description)
        body.setObjectName("ChoiceBody")
        body.setWordWrap(True)
        layout.addWidget(body)

        facts_box = QFrame()
        facts_box.setObjectName("ChoiceFacts")
        facts_layout = QVBoxLayout(facts_box)
        facts_layout.setContentsMargins(13, 11, 13, 11)
        facts_layout.setSpacing(7)
        for fact in facts:
            item = QLabel(f"✓  {fact}")
            item.setObjectName("ChoiceFact")
            item.setWordWrap(True)
            facts_layout.addWidget(item)
        layout.addWidget(facts_box)
        layout.addStretch(1)

        button = QPushButton(button_text)
        button.setObjectName("PrimaryButton" if primary else "SecondaryButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.selected.emit)
        layout.addWidget(button, 0, Qt.AlignmentFlag.AlignLeft)
        self.action_button = button


class StudyChooserPage(QWidget):
    thesis_requested = Signal()
    exploratory_requested = Signal()

    def __init__(
        self,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("Page")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(50, 40, 50, 36)
        layout.setSpacing(18)

        intro = QFrame()
        intro.setObjectName("HeroSurface")
        intro_layout = QVBoxLayout(intro)
        intro_layout.setContentsMargins(24, 20, 24, 21)
        intro_layout.setSpacing(7)
        eyebrow = QLabel("STUDY")
        eyebrow.setObjectName("PageEyebrow")
        title = QLabel("Choose a study")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Review the frozen thesis design or prepare non-final exploratory work. "
            "Final evidence and development activity stay clearly separated."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        intro_layout.addWidget(eyebrow)
        intro_layout.addWidget(title)
        intro_layout.addWidget(lead)
        layout.addWidget(intro)

        banner = QFrame()
        banner.setObjectName("LockedBanner")
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(15, 11, 15, 11)
        banner_layout.setSpacing(12)
        banner_layout.addWidget(StatusPill("LOCKED", kind="locked"))
        banner_text = QVBoxLayout()
        banner_text.setSpacing(1)
        banner_title = QLabel("Final reserve remains sealed")
        banner_title.setObjectName("LockedTitle")
        banner_detail = QLabel(
            "Exploratory studies are development evidence only. Nothing on this screen authorizes final-reserve execution."
        )
        banner_detail.setObjectName("LockedText")
        banner_detail.setWordWrap(True)
        banner_text.addWidget(banner_title)
        banner_text.addWidget(banner_detail)
        banner_layout.addLayout(banner_text, 1)
        layout.addWidget(banner)

        self.help_detail = QLabel(
            "Thesis Study is the accepted DEC-058 design and is read-only here. "
            "Exploratory Study is non-final development work; the UI only exposes choices that the Python backend can validate."
        )
        self.help_detail.setObjectName("HelpDetail")
        self.help_detail.setWordWrap(True)
        self.help_detail.hide()
        help_button = QPushButton(
            "?   What is the difference between Thesis Study and Exploratory Study?"
        )
        help_button.setObjectName("HelpDisclosure")
        help_button.setCheckable(True)
        help_button.setCursor(Qt.CursorShape.PointingHandCursor)
        help_button.setToolTip("Show the scientific boundary between the two study types.")
        help_button.toggled.connect(self.help_detail.setVisible)
        layout.addWidget(help_button)
        layout.addWidget(self.help_detail)

        choices = QHBoxLayout()
        choices.setSpacing(20)
        thesis = StudyChoiceCard(
            title="Thesis Study",
            description="Inspect the frozen protocol-v2.0 plan before final execution is authorized at a later gate.",
            status_text="FROZEN",
            status_kind="frozen",
            facts=(
                f"{len(protocol.methods)} retained methods · {protocol.root_count} independent roots",
                f"{protocol.layout_count} held-out layouts · {protocol.condition_count} resilience conditions",
                "Scientific settings are fixed by DEC-058",
            ),
            button_text="Review thesis study",
            primary=False,
        )
        thesis.setToolTip("Read-only review of the accepted thesis protocol.")
        thesis.selected.connect(self.thesis_requested.emit)

        exploratory = StudyChoiceCard(
            title="Exploratory Study",
            description="Prepare development-only studies while preserving the frozen thesis design and final-reserve boundary.",
            status_text="DEVELOPMENT",
            status_kind="development",
            facts=(
                "Choose from the retained model implementations",
                "Customize only safe non-final preview scope",
                "No final-reserve roots, layouts or outcomes are used",
            ),
            button_text="Start exploratory study",
            primary=True,
        )
        exploratory.setToolTip("Start a non-final development study configuration.")
        exploratory.selected.connect(self.exploratory_requested.emit)

        choices.addWidget(thesis, 1)
        choices.addWidget(exploratory, 1)
        layout.addLayout(choices)
        layout.addStretch(1)

        scroll.setWidget(content)
        root.addWidget(scroll)

        self.thesis_card = thesis
        self.exploratory_card = exploratory
        self.help_button = help_button


class ModelChoiceCard(QFrame):
    selection_changed = Signal()

    def __init__(self, method: MethodSummary, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.method = method
        self.setObjectName("ModelChoiceCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(7)

        check = QCheckBox(method.name)
        check.setObjectName("ModelChoiceCheck")
        check.setChecked(True)
        check.setCursor(Qt.CursorShape.PointingHandCursor)
        check.setToolTip(f"Include {method.name} in this exploratory development study.")
        check.toggled.connect(lambda _checked: self.selection_changed.emit())
        layout.addWidget(check)

        config = QLabel(f"Retained implementation · {method.config_id}")
        config.setObjectName("ModelChoiceConfig")
        config.setToolTip(
            "Configuration ID is shown for traceability. Scientific mechanics remain backend-owned."
        )
        layout.addWidget(config)

        description = QLabel(method.description)
        description.setObjectName("ChoiceBody")
        description.setWordWrap(True)
        layout.addWidget(description)
        layout.addStretch(1)
        self.check = check

    @property
    def selected(self) -> bool:
        return self.check.isChecked()


class ExploratoryModelsPage(QWidget):
    back_requested = Signal()
    models_confirmed = Signal(tuple)

    def __init__(
        self,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.protocol = protocol
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("Page")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(50, 22, 50, 20)
        layout.setSpacing(12)

        back = QPushButton("←  Study types")
        back.setObjectName("TextButton")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        layout.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(StepRail(1))

        intro = QFrame()
        intro.setObjectName("HeroSurface")
        intro_layout = QVBoxLayout(intro)
        intro_layout.setContentsMargins(24, 16, 24, 17)
        intro_layout.setSpacing(6)
        eyebrow = QLabel("EXPLORATORY STUDY")
        eyebrow.setObjectName("PageEyebrow")
        title = QLabel("Choose models")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Select the model implementations to include. This is development-only configuration; "
            "final-reserve identities and outcomes stay outside the exploratory workflow."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        intro_layout.addWidget(eyebrow)
        intro_layout.addWidget(title)
        intro_layout.addWidget(lead)
        layout.addWidget(intro)

        banner = QFrame()
        banner.setObjectName("DevelopmentBanner")
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(15, 10, 15, 10)
        banner_layout.setSpacing(12)
        banner_layout.addWidget(StatusPill("DEVELOPMENT", kind="development"))
        banner_text = QLabel(
            "Only non-final study choices belong here. Frozen thesis settings remain read-only and final evidence cannot be started from this flow."
        )
        banner_text.setObjectName("DevelopmentText")
        banner_text.setWordWrap(True)
        banner_layout.addWidget(banner_text, 1)
        layout.addWidget(banner)

        help_button = QPushButton("?   What can I change on this screen?")
        help_button.setObjectName("HelpDisclosure")
        help_button.setCheckable(True)
        help_button.setCursor(Qt.CursorShape.PointingHandCursor)
        help_button.setToolTip(
            "Explain which model choices are owned by the UI and which remain backend-owned."
        )
        layout.addWidget(help_button)
        help_detail = QLabel(
            "You can include or exclude retained implementations. Randomness contracts, "
            "final roots/layouts, checkpoint identity and final-reserve material are never editable here."
        )
        help_detail.setObjectName("HelpDetail")
        help_detail.setWordWrap(True)
        help_detail.hide()
        help_button.toggled.connect(help_detail.setVisible)
        layout.addWidget(help_detail)

        heading_row = QHBoxLayout()
        heading = QLabel("Retained implementations")
        heading.setObjectName("SectionTitle")
        self.selection_label = QLabel()
        self.selection_label.setObjectName("SectionHint")
        heading_row.addWidget(heading)
        heading_row.addStretch(1)
        heading_row.addWidget(self.selection_label)
        layout.addLayout(heading_row)

        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)
        self.model_cards: list[ModelChoiceCard] = []
        for index, method in enumerate(protocol.methods):
            card = ModelChoiceCard(method)
            card.selection_changed.connect(self._sync_selection)
            grid.addWidget(card, index // 3, index % 3)
            grid.setColumnStretch(index % 3, 1)
            self.model_cards.append(card)
        layout.addWidget(grid_container)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        select_all = QPushButton("Select all")
        select_all.setObjectName("TextButton")
        select_all.setCursor(Qt.CursorShape.PointingHandCursor)
        select_all.clicked.connect(self._select_all)
        actions.addWidget(select_all)
        actions.addStretch(1)
        self.continue_button = QPushButton("Continue to customize")
        self.continue_button.setObjectName("PrimaryButton")
        self.continue_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.continue_button.clicked.connect(self._confirm_models)
        actions.addWidget(self.continue_button)
        layout.addLayout(actions)
        layout.addStretch(1)

        scroll.setWidget(content)
        root.addWidget(scroll)
        self.scroll = scroll
        self.help_button = help_button
        self.help_detail = help_detail
        self._sync_selection()

    def selected_method_ids(self) -> tuple[str, ...]:
        return tuple(card.method.method_id for card in self.model_cards if card.selected)

    def _select_all(self) -> None:
        for card in self.model_cards:
            card.check.setChecked(True)
        self._sync_selection()

    def _sync_selection(self) -> None:
        count = len(self.selected_method_ids())
        self.selection_label.setText(f"{count} of {len(self.model_cards)} selected")
        self.continue_button.setEnabled(count > 0)
        self.continue_button.setToolTip(
            "Continue with the selected development model implementations."
            if count
            else "Select at least one model to continue."
        )

    def _confirm_models(self) -> None:
        selected = self.selected_method_ids()
        if selected:
            self.models_confirmed.emit(selected)


class ExploratoryCustomizePage(QWidget):
    back_requested = Signal()
    review_requested = Signal()

    def __init__(
        self,
        preview_model: DesktopExploratoryPreviewModel,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.preview_model = preview_model
        self.selected_methods: tuple[str, ...] = ()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("Page")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(50, 30, 50, 34)
        layout.setSpacing(15)

        back = QPushButton("←  Models")
        back.setObjectName("TextButton")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        layout.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(StepRail(2))

        intro = QFrame()
        intro.setObjectName("HeroSurface")
        intro_layout = QVBoxLayout(intro)
        intro_layout.setContentsMargins(24, 18, 24, 19)
        intro_layout.setSpacing(6)
        eyebrow = QLabel("EXPLORATORY STUDY")
        eyebrow.setObjectName("PageEyebrow")
        title = QLabel("Customize (optional)")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Adjust only the safe non-final preview scope. Scientific protocol mechanics and all final-reserve identities remain backend-owned."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        intro_layout.addWidget(eyebrow)
        intro_layout.addWidget(title)
        intro_layout.addWidget(lead)
        layout.addWidget(intro)

        form_surface = QFrame()
        form_surface.setObjectName("Surface")
        form = QGridLayout(form_surface)
        form.setContentsMargins(20, 18, 20, 18)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

        name_label = QLabel("Study label")
        name_label.setObjectName("MethodName")
        self.study_label = QLineEdit()
        self.study_label.setObjectName("StudyLabelInput")
        self.study_label.setPlaceholderText("Exploratory study")
        self.study_label.setToolTip(
            "A human-readable label only. It does not affect scientific identity or seeds."
        )
        self.study_label.setAccessibleName("Study label")
        name_label.setBuddy(self.study_label)
        form.addWidget(name_label, 0, 0)
        form.addWidget(self.study_label, 0, 1, 1, 3)

        roots_label = QLabel("Preview roots")
        roots_label.setObjectName("MethodName")
        self.root_count = QComboBox()
        self.root_count.setObjectName("ScopeCombo")
        for value in range(1, preview_model.max_root_count + 1):
            self.root_count.addItem(str(value), value)
        self.root_count.setCurrentIndex(0)
        self.root_count.setToolTip(
            "Preview-only development roots generated by the backend adapter. These are never final roots."
        )
        self.root_count.setAccessibleName("Preview roots")
        roots_label.setBuddy(self.root_count)

        layouts_label = QLabel("Development layouts")
        layouts_label.setObjectName("MethodName")
        self.layout_count = QComboBox()
        self.layout_count.setObjectName("ScopeCombo")
        for value in range(1, preview_model.max_layout_count + 1):
            suffix = "layout" if value == 1 else "layouts"
            self.layout_count.addItem(f"{value} {suffix}", value)
        self.layout_count.setCurrentIndex(0)
        self.layout_count.setToolTip(
            "Uses only the historical non-final gw-l1 development layouts; held-out final layouts are excluded."
        )
        self.layout_count.setAccessibleName("Development layouts")
        layouts_label.setBuddy(self.layout_count)
        form.addWidget(roots_label, 1, 0)
        form.addWidget(self.root_count, 1, 1)
        form.addWidget(layouts_label, 1, 2)
        form.addWidget(self.layout_count, 1, 3)
        form.setColumnStretch(1, 1)
        form.setColumnStretch(3, 1)
        layout.addWidget(form_surface)

        boundary = QFrame()
        boundary.setObjectName("DevelopmentBanner")
        boundary_layout = QVBoxLayout(boundary)
        boundary_layout.setContentsMargins(16, 12, 16, 12)
        boundary_layout.setSpacing(4)
        heading = QLabel("What remains fixed")
        heading.setObjectName("DevelopmentTitle")
        details = QLabel(
            "Model configurations come from the frozen retained implementations; the preview uses the existing non-final development layouts "
            "and development action-remap conditions. Final roots, final held-out layouts and final outcomes are never selected."
        )
        details.setObjectName("DevelopmentText")
        details.setWordWrap(True)
        boundary_layout.addWidget(heading)
        boundary_layout.addWidget(details)
        layout.addWidget(boundary)

        self.selected_summary = QLabel()
        self.selected_summary.setObjectName("SectionHint")
        self.selected_summary.setWordWrap(True)
        layout.addWidget(self.selected_summary)

        actions = QHBoxLayout()
        back_action = QPushButton("Back")
        back_action.setObjectName("SecondaryButton")
        back_action.clicked.connect(self.back_requested.emit)
        actions.addWidget(back_action)
        actions.addStretch(1)
        review = QPushButton("Review plan")
        review.setObjectName("PrimaryButton")
        review.setCursor(Qt.CursorShape.PointingHandCursor)
        review.clicked.connect(self.review_requested.emit)
        actions.addWidget(review)
        layout.addLayout(actions)
        layout.addStretch(1)

        scroll.setWidget(content)
        root.addWidget(scroll)

    def configure(self, method_ids: tuple[str, ...], method_names: tuple[str, ...]) -> None:
        self.selected_methods = tuple(method_ids)
        self.selected_summary.setText(
            f"Selected models: {', '.join(method_names)}. Conditions in this preview remain the two established non-final action-remap development conditions."
        )

    def scope(self) -> tuple[int, int]:
        return int(self.root_count.currentData()), int(self.layout_count.currentData())


class ExploratoryReviewPage(QWidget):
    back_requested = Signal()

    def __init__(
        self,
        preview_model: DesktopExploratoryPreviewModel,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.preview_model = preview_model
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("Page")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(50, 30, 50, 34)
        layout.setSpacing(15)

        back = QPushButton("←  Customize")
        back.setObjectName("TextButton")
        back.clicked.connect(self.back_requested.emit)
        layout.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(StepRail(3))

        intro = QFrame()
        intro.setObjectName("HeroSurface")
        intro_layout = QVBoxLayout(intro)
        intro_layout.setContentsMargins(24, 18, 24, 19)
        intro_layout.setSpacing(6)
        eyebrow = QLabel("EXPLORATORY STUDY")
        eyebrow.setObjectName("PageEyebrow")
        title = QLabel("Review plan")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "This is a truthful backend-resolved preview. No study has been created and no scientific execution has started."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        intro_layout.addWidget(eyebrow)
        intro_layout.addWidget(title)
        intro_layout.addWidget(lead)
        layout.addWidget(intro)

        banner = QFrame()
        banner.setObjectName("DevelopmentBanner")
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(15, 10, 15, 10)
        banner_layout.setSpacing(12)
        banner_layout.addWidget(StatusPill("DEVELOPMENT", kind="development"))
        text = QLabel(
            "StudyService.preview() resolves this matrix through the same framework-neutral StudyPlanner used by the application backend."
        )
        text.setObjectName("DevelopmentText")
        text.setWordWrap(True)
        banner_layout.addWidget(text, 1)
        layout.addWidget(banner)

        self.summary_surface = QFrame()
        self.summary_surface.setObjectName("Surface")
        self.summary_grid = QGridLayout(self.summary_surface)
        self.summary_grid.setContentsMargins(20, 17, 20, 17)
        self.summary_grid.setHorizontalSpacing(24)
        self.summary_grid.setVerticalSpacing(11)
        layout.addWidget(self.summary_surface)

        self.detail = QLabel()
        self.detail.setObjectName("HelpDetail")
        self.detail.setWordWrap(True)
        layout.addWidget(self.detail)

        actions = QHBoxLayout()
        back_action = QPushButton("Back")
        back_action.setObjectName("SecondaryButton")
        back_action.clicked.connect(self.back_requested.emit)
        actions.addWidget(back_action)
        actions.addStretch(1)
        self.create_button = QPushButton("Create exploratory study")
        self.create_button.setObjectName("LockedButton")
        self.create_button.setEnabled(False)
        self.create_button.setToolTip(
            "Execution creation is intentionally not connected in this preview slice. The next application-service checkpoint will add authorized development creation."
        )
        actions.addWidget(self.create_button)
        layout.addLayout(actions)
        layout.addStretch(1)

        scroll.setWidget(content)
        root.addWidget(scroll)

    def show_preview(
        self,
        *,
        preview: ExploratoryPlanPreview,
        method_names: tuple[str, ...],
        study_label: str,
    ) -> None:
        while self.summary_grid.count():
            item = self.summary_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        facts = (
            ("Study", study_label or "Exploratory study"),
            ("Evidence class", "DEVELOPMENT"),
            ("Models", f"{preview.method_count} · {', '.join(method_names)}"),
            ("Preview roots", str(preview.root_count)),
            ("Development layouts", f"{preview.layout_count} · {', '.join(preview.development_layout_ids)}"),
            ("Conditions", str(preview.condition_count)),
            ("Phase-A jobs", str(preview.phase_a_jobs)),
            ("Phase-B matched sets", str(preview.phase_b_jobs)),
            ("Validation / analysis / export", f"{preview.validation_jobs} / {preview.analysis_jobs} / {preview.export_jobs}"),
            ("Total planner jobs", str(preview.total_jobs)),
        )
        for index, (label, value) in enumerate(facts):
            label_widget = QLabel(label)
            label_widget.setObjectName("ReviewLabel")
            value_widget = QLabel(value)
            value_widget.setObjectName("ReviewValue")
            value_widget.setWordWrap(True)
            row = index // 2
            column = (index % 2) * 2
            self.summary_grid.addWidget(label_widget, row, column)
            self.summary_grid.addWidget(value_widget, row, column + 1)
        self.summary_grid.setColumnStretch(1, 1)
        self.summary_grid.setColumnStretch(3, 1)
        self.detail.setText(
            "Preview conditions: "
            + ", ".join(preview.condition_ids)
            + ". Final-reserve execution remains unauthorized, and this preview cannot be promoted to thesis evidence."
        )


class StudyWorkspacePage(QWidget):
    """Own Study sub-navigation while preserving the global workspace shell."""

    HOME = 0
    THESIS = 1
    MODELS = 2
    CUSTOMIZE = 3
    REVIEW = 4

    def __init__(
        self,
        protocol: FrozenProtocolSummary,
        *,
        repo_root: Path | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.protocol = protocol
        resolved_repo_root = (
            Path(repo_root).resolve()
            if repo_root is not None
            else Path(__file__).resolve().parents[3]
        )
        self.preview_model = DesktopExploratoryPreviewModel(repo_root=resolved_repo_root)
        self._selected_method_ids: tuple[str, ...] = tuple(
            method.method_id for method in protocol.methods
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()

        self.chooser = StudyChooserPage(protocol)
        self.thesis = ThesisStudyPage(protocol, show_back=True)
        self.models = ExploratoryModelsPage(protocol)
        self.exploratory = self.models
        self.customize = ExploratoryCustomizePage(self.preview_model)
        self.review = ExploratoryReviewPage(self.preview_model)
        for page in (
            self.chooser,
            self.thesis,
            self.models,
            self.customize,
            self.review,
        ):
            self.stack.addWidget(page)
        root.addWidget(self.stack)

        self.chooser.thesis_requested.connect(self.show_thesis)
        self.chooser.exploratory_requested.connect(self.show_exploratory)
        self.thesis.back_requested.connect(self.show_home)
        self.models.back_requested.connect(self.show_home)
        self.models.models_confirmed.connect(self._show_customize)
        self.customize.back_requested.connect(self.show_exploratory)
        self.customize.review_requested.connect(self._show_review)
        self.review.back_requested.connect(self.show_customize)
        self.show_home()

    def _method_names(self, method_ids: tuple[str, ...]) -> tuple[str, ...]:
        by_id = {method.method_id: method.name for method in self.protocol.methods}
        return tuple(by_id[item] for item in method_ids)

    def show_home(self) -> None:
        self.stack.setCurrentIndex(self.HOME)

    def show_thesis(self) -> None:
        self.stack.setCurrentIndex(self.THESIS)

    def show_exploratory(self) -> None:
        self.stack.setCurrentIndex(self.MODELS)

    def show_customize(self) -> None:
        method_ids = self.models.selected_method_ids()
        if not method_ids:
            return
        self._show_customize(method_ids)

    def _show_customize(self, method_ids: tuple[str, ...]) -> None:
        self._selected_method_ids = tuple(method_ids)
        self.customize.configure(
            self._selected_method_ids,
            self._method_names(self._selected_method_ids),
        )
        self.stack.setCurrentIndex(self.CUSTOMIZE)

    def _show_review(self) -> None:
        roots, layouts = self.customize.scope()
        preview = self.preview_model.preview(
            selected_method_ids=self._selected_method_ids,
            root_count=roots,
            layout_count=layouts,
        )
        self.review.show_preview(
            preview=preview,
            method_names=self._method_names(self._selected_method_ids),
            study_label=self.customize.study_label.text().strip(),
        )
        self.stack.setCurrentIndex(self.REVIEW)

    @property
    def current_view(self) -> str:
        return ("choose", "thesis", "exploratory", "customize", "review")[
            self.stack.currentIndex()
        ]
