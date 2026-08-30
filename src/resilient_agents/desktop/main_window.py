"""Main PySide6 desktop shell and navigation."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from . import APP_NAME, APP_SUBTITLE
from .artifacts_page import ArtifactsPage
from .placeholder_page import PlaceholderPage
from .protocol import load_frozen_protocol
from .runs_page import RunsPage
from .study_page import ThesisStudyPage
from .study_read_model import DesktopStudyReadModel
from .widgets import NavButton


class MainWindow(QMainWindow):
    def __init__(self, *, repo_root: Path, writable_root: Path | None = None) -> None:
        super().__init__()
        self.repo_root = Path(repo_root).resolve()
        self.writable_root = Path(writable_root).resolve() if writable_root else self.repo_root
        self.setWindowTitle(f"{APP_NAME} — {APP_SUBTITLE}")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        protocol = load_frozen_protocol(self.repo_root)
        self.study_read_model = DesktopStudyReadModel(repo_root=self.repo_root, writable_root=self.writable_root)

        root = QWidget()
        root.setObjectName("AppRoot")
        app_layout = QVBoxLayout(root)
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)
        app_layout.addWidget(self._build_top_header())

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(282)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(22, 22, 18, 18)
        sidebar_layout.setSpacing(7)

        workspace = QLabel("WORKSPACE")
        workspace.setObjectName("SidebarSection")
        sidebar_layout.addWidget(workspace)
        sidebar_layout.addSpacing(10)

        self.thesis_page = ThesisStudyPage(protocol)
        self.runs_page = RunsPage(self.study_read_model)
        self.results_page = PlaceholderPage(
            "Results",
            "Compare Learning and Test Resilience become available from stored analysis evidence. The application will not invent example scientific outcomes.",
        )
        self.artifacts_page = ArtifactsPage(self.study_read_model)
        self.pages = (self.thesis_page, self.runs_page, self.results_page, self.artifacts_page)

        self.stack = QStackedWidget()
        for page in self.pages:
            self.stack.addWidget(page)
        self.runs_page.study_selected.connect(self._show_artifacts_for_study)

        self.nav_buttons: list[NavButton] = []
        nav_items = (
            ("▦   Study", "Review the frozen thesis plan or prepare an exploratory study."),
            ("▶   Runs", "Inspect durable Study records and real execution state."),
            ("↔   Results", "Compare stored learning and resilience analysis when evidence exists."),
            ("▣   Artifacts", "Inspect artifacts registered by durable Study records."),
        )
        for index, (label, tooltip) in enumerate(nav_items):
            button = NavButton(label)
            button.setToolTip(tooltip)
            button.clicked.connect(lambda checked=False, i=index: self.set_page(i))
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

        sidebar_layout.addSpacing(20)
        sidebar_rule = QWidget()
        sidebar_rule.setFixedHeight(1)
        sidebar_rule.setStyleSheet("background:#DDE3EC;")
        sidebar_layout.addWidget(sidebar_rule)
        sidebar_layout.addSpacing(20)

        scientific_state = QLabel("SCIENTIFIC STATE")
        scientific_state.setObjectName("SidebarSection")
        sidebar_layout.addWidget(scientific_state)
        sidebar_layout.addSpacing(8)
        for text, tooltip in (
            ("✓  Protocol v2.0 frozen", "DEC-058 frozen scientific protocol."),
            ("▣  Final reserve locked", "Final scientific execution remains sealed until explicit later authorization."),
        ):
            state = QLabel(text)
            state.setObjectName("SidebarState")
            state.setToolTip(tooltip)
            sidebar_layout.addWidget(state)

        sidebar_layout.addStretch(1)
        utility = QLabel("DEC-058 authority\nPresentation layer: T-528")
        utility.setObjectName("SidebarUtility")
        sidebar_layout.addWidget(utility)

        body_layout.addWidget(sidebar)
        body_layout.addWidget(self.stack, 1)
        app_layout.addWidget(body, 1)
        self.setCentralWidget(root)

        self.set_page(0)
        QShortcut(QKeySequence("Alt+1"), self, activated=lambda: self.set_page(0))
        QShortcut(QKeySequence("Alt+2"), self, activated=lambda: self.set_page(1))
        QShortcut(QKeySequence("Alt+3"), self, activated=lambda: self.set_page(2))
        QShortcut(QKeySequence("Alt+4"), self, activated=lambda: self.set_page(3))

    def _build_top_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("TopHeader")
        header.setFixedHeight(64)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)
        layout.setSpacing(12)

        mark = QLabel("✦")
        mark.setStyleSheet("color:#245DE8;font-size:24px;font-weight:700;")
        mark.setToolTip("Resilient Agents research application")
        layout.addWidget(mark)

        brand_group = QVBoxLayout()
        brand_group.setSpacing(0)
        brand = QLabel(APP_NAME)
        brand.setObjectName("HeaderBrand")
        subtitle = QLabel("Local thesis research application")
        subtitle.setObjectName("HeaderSubtitle")
        brand_group.addWidget(brand)
        brand_group.addWidget(subtitle)
        layout.addLayout(brand_group)
        layout.addStretch(1)

        help_button = QPushButton("?  Getting started")
        help_button.setObjectName("HeaderHelp")
        help_button.setToolTip("Open a short guide to the application surfaces and scientific boundary.")
        help_button.clicked.connect(self._show_getting_started)
        layout.addWidget(help_button)

        lock = QLabel("FINAL RESERVE LOCKED")
        lock.setObjectName("HeaderLock")
        lock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock.setFixedHeight(24)
        lock.setToolTip("Final-reserve execution is not authorized during T-528.")
        layout.addWidget(lock)
        return header

    def _show_getting_started(self) -> None:
        QMessageBox.information(
            self,
            "Getting started",
            "Study prepares or reviews a study. Runs shows durable execution state. "
            "Results exposes stored analysis only, and Artifacts shows registered outputs.\n\n"
            "Final-reserve scientific execution remains locked until a later explicit authorization gate.",
        )

    def set_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        for button_index, button in enumerate(self.nav_buttons):
            button.setChecked(button_index == index)
        if index == 1:
            self.runs_page.refresh()
        elif index == 3:
            self.artifacts_page.refresh()

    def _show_artifacts_for_study(self, study_id: str) -> None:
        self.artifacts_page.refresh()
        self.artifacts_page.set_study(study_id)
