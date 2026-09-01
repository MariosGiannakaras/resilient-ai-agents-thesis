"""Protocol-v2.1 experiment-first PySide6 shell."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from . import APP_NAME, APP_SUBTITLE
from .evidence_page import EvidencePage
from .experiment_page import ExperimentPage
from .onboarding import OnboardingDialog
from .protocol import load_frozen_protocol
from .results_read_model import DesktopResultsReadModel
from .results_workspace import ResultsWorkspacePage
from .run_workspace import RunWorkspacePage
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

        self.protocol = load_frozen_protocol(self.repo_root)
        self.study_read_model = DesktopStudyReadModel(repo_root=self.repo_root, writable_root=self.writable_root)
        self.results_read_model = DesktopResultsReadModel(self.study_read_model)

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
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 20, 14, 18)
        sidebar_layout.setSpacing(7)
        workspace = QLabel("THESIS WORKSPACE")
        workspace.setObjectName("SidebarSection")
        sidebar_layout.addWidget(workspace)
        sidebar_layout.addSpacing(8)

        self.experiment_page = ExperimentPage(
            self.protocol,
            repo_root=self.repo_root,
            writable_root=self.writable_root,
        )
        self.runs_page = RunWorkspacePage(self.study_read_model, self.protocol)
        self.results_page = ResultsWorkspacePage(self.results_read_model, self.protocol)
        self.evidence_page = EvidencePage(self.study_read_model)
        self.artifacts_page = self.evidence_page
        self.pages = (self.experiment_page, self.runs_page, self.results_page, self.evidence_page)
        self.stack = QStackedWidget()
        for page in self.pages:
            self.stack.addWidget(page)
        self.experiment_page.study_created.connect(self._study_created)
        self.runs_page.study_selected.connect(self._show_evidence_for_study)

        self.nav_buttons: list[NavButton] = []
        nav_items = (
            ("Experiment", "Understand the Thesis experiment or prepare a DEVELOPMENT experiment."),
            ("Run", "Observe Phase A or an exact matched Frozen/Adaptive Phase-B pair."),
            ("Results", "Inspect stored validated outputs organized as RQ1, RQ2 and RQ3."),
            ("Evidence", "See readiness and reproducibility from registered evidence."),
        )
        for index, (label, tooltip) in enumerate(nav_items):
            button = NavButton(label)
            button.setAccessibleName(f"Open {label}")
            button.setToolTip(f"Alt+{index + 1} · {tooltip}")
            button.clicked.connect(lambda checked=False, i=index: self.set_page(i))
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)
        sidebar_layout.addStretch(1)
        state = QLabel("protocol-v2.1\nFinal experiment locked")
        state.setObjectName("SidebarState")
        state.setWordWrap(True)
        state.setToolTip("Final-reserve execution remains blocked until separate explicit T-610 authorization.")
        sidebar_layout.addWidget(state)

        body_layout.addWidget(sidebar)
        body_layout.addWidget(self.stack, 1)
        app_layout.addWidget(body, 1)
        self.setCentralWidget(root)
        self.set_page(0)
        for index in range(4):
            QShortcut(QKeySequence(f"Alt+{index + 1}"), self, activated=lambda i=index: self.set_page(i))

    def _build_top_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("TopHeader")
        header.setFixedHeight(62)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(12)
        brand_group = QVBoxLayout()
        brand_group.setSpacing(0)
        brand = QLabel(APP_NAME)
        brand.setObjectName("HeaderBrand")
        subtitle = QLabel("Resilient learning thesis experiment")
        subtitle.setObjectName("HeaderSubtitle")
        brand_group.addWidget(brand)
        brand_group.addWidget(subtitle)
        layout.addLayout(brand_group)
        layout.addStretch(1)
        help_button = QPushButton("Getting started")
        help_button.setObjectName("HeaderHelp")
        help_button.setAccessibleName("Open getting started guide")
        help_button.setToolTip("Replay the short, skippable guide to Experiment, Run, Results and Evidence.")
        help_button.clicked.connect(self._show_getting_started)
        layout.addWidget(help_button)
        lock = QLabel("FINAL EXPERIMENT LOCKED")
        lock.setObjectName("HeaderLock")
        lock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock.setFixedHeight(24)
        lock.setToolTip("The desktop UI cannot authorize final execution. T-610 remains separately blocked.")
        layout.addWidget(lock)
        return header

    def _show_getting_started(self) -> None:
        OnboardingDialog(self).exec()

    def set_page(self, index: int) -> None:
        if not 0 <= index < len(self.pages):
            raise IndexError("page index out of range")
        self.stack.setCurrentIndex(index)
        for button_index, button in enumerate(self.nav_buttons):
            button.setChecked(button_index == index)
        if index == 1:
            self.runs_page.refresh()
        elif index == 2:
            self.results_page.refresh()
        elif index == 3:
            self.evidence_page.refresh()

    def _study_created(self, study_id: str) -> None:
        self.runs_page.refresh()
        self.set_page(1)

    def _show_evidence_for_study(self, study_id: str) -> None:
        self.evidence_page.refresh()
        self.evidence_page.set_study(study_id)
