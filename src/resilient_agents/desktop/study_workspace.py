"""Study entry journey for the PySide6 application."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .protocol import FrozenProtocolSummary, MethodSummary
from .study_page import ThesisStudyPage
from .widgets import StatusPill


class StudyChoiceCard(QFrame):
    """Large, self-contained study-type choice used on the Study landing page."""

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
        layout.setContentsMargins(50, 44, 50, 38)
        layout.setSpacing(21)

        intro = QFrame()
        intro.setObjectName("HeroSurface")
        intro_layout = QVBoxLayout(intro)
        intro_layout.setContentsMargins(24, 21, 24, 22)
        intro_layout.setSpacing(8)
        eyebrow = QLabel("STUDY")
        eyebrow.setObjectName("PageEyebrow")
        title = QLabel("Choose a study")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Review the frozen thesis design or prepare non-final exploratory work. "
            "The application keeps final evidence separate from development activity."
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
            "Exploratory Study is for non-final development work and can expose only choices supported by the backend recipe contract."
        )
        self.help_detail.setObjectName("HelpDetail")
        self.help_detail.setWordWrap(True)
        self.help_detail.hide()
        help_button = QPushButton("?   What is the difference between Thesis Study and Exploratory Study?")
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
            description="Inspect the frozen protocol-v2.0 study before final execution is authorized at a later gate.",
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
                "Only backend-approved choices are exposed",
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
            "Configuration ID is shown for traceability. Additional development controls are exposed only when explicitly supported by the recipe layer."
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


class ExploratoryStudyPage(QWidget):
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
        layout.setContentsMargins(50, 34, 50, 38)
        layout.setSpacing(18)

        back = QPushButton("←  Study types")
        back.setObjectName("TextButton")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        layout.addWidget(back, 0, Qt.AlignmentFlag.AlignLeft)

        intro = QFrame()
        intro.setObjectName("HeroSurface")
        intro_layout = QVBoxLayout(intro)
        intro_layout.setContentsMargins(24, 20, 24, 21)
        intro_layout.setSpacing(7)
        eyebrow = QLabel("EXPLORATORY STUDY · STEP 1")
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
        banner_layout.setContentsMargins(15, 11, 15, 11)
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
        help_button.setToolTip("Explain which model choices are owned by the UI and which remain backend-owned.")
        layout.addWidget(help_button)
        help_detail = QLabel(
            "You can include or exclude retained implementations. Roots, layouts, disturbance definitions, "
            "randomness contracts and final-reserve material are not editable here; those remain recipe/backend responsibilities."
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
        self.continue_button = QPushButton("Continue")
        self.continue_button.setObjectName("PrimaryButton")
        self.continue_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.continue_button.setToolTip("Continue with the selected development model implementations.")
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
        if count == 0:
            self.continue_button.setToolTip("Select at least one model to continue.")
        else:
            self.continue_button.setToolTip("Continue with the selected development model implementations.")

    def _confirm_models(self) -> None:
        selected = self.selected_method_ids()
        if selected:
            self.models_confirmed.emit(selected)


class StudyWorkspacePage(QWidget):
    """Own the Study sub-navigation without changing the global workspace navigation."""

    HOME = 0
    THESIS = 1
    EXPLORATORY = 2

    def __init__(
        self,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()

        self.chooser = StudyChooserPage(protocol)
        self.thesis = ThesisStudyPage(protocol, show_back=True)
        self.exploratory = ExploratoryStudyPage(protocol)
        for page in (self.chooser, self.thesis, self.exploratory):
            self.stack.addWidget(page)
        root.addWidget(self.stack)

        self.chooser.thesis_requested.connect(self.show_thesis)
        self.chooser.exploratory_requested.connect(self.show_exploratory)
        self.thesis.back_requested.connect(self.show_home)
        self.exploratory.back_requested.connect(self.show_home)
        self.show_home()

    def show_home(self) -> None:
        self.stack.setCurrentIndex(self.HOME)

    def show_thesis(self) -> None:
        self.stack.setCurrentIndex(self.THESIS)

    def show_exploratory(self) -> None:
        self.stack.setCurrentIndex(self.EXPLORATORY)

    @property
    def current_view(self) -> str:
        return ("choose", "thesis", "exploratory")[self.stack.currentIndex()]
