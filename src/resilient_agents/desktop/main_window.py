"""Main PySide6 desktop shell and navigation."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

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
        shell = QHBoxLayout(root)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(218)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(17, 22, 17, 18)
        sidebar_layout.setSpacing(7)

        brand = QLabel(APP_NAME)
        brand.setObjectName("Brand")
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setObjectName("BrandSubtitle")
        subtitle.setWordWrap(True)
        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(22)

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
        for index, label in enumerate(("Study", "Runs", "Results", "Artifacts")):
            button = NavButton(label)
            button.clicked.connect(lambda checked=False, i=index: self.set_page(i))
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

        sidebar_layout.addStretch(1)
        help_button = QPushButton("Help && terminology")
        help_button.setObjectName("NavButton")
        help_button.setToolTip("Contextual scientific help will be connected in a later T-528 feature slice.")
        help_button.setEnabled(False)
        sidebar_layout.addWidget(help_button)
        utility = QLabel("Protocol v2.0 · DEC-058\nFinal reserve locked")
        utility.setObjectName("SidebarUtility")
        sidebar_layout.addWidget(utility)

        shell.addWidget(sidebar)
        shell.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        self.set_page(0)
        QShortcut(QKeySequence("Alt+1"), self, activated=lambda: self.set_page(0))
        QShortcut(QKeySequence("Alt+2"), self, activated=lambda: self.set_page(1))
        QShortcut(QKeySequence("Alt+3"), self, activated=lambda: self.set_page(2))
        QShortcut(QKeySequence("Alt+4"), self, activated=lambda: self.set_page(3))

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
