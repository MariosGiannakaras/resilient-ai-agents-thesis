"""Replayable lightweight onboarding for the experiment-first desktop UI."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

_STEPS = (
    (
        "Experiment",
        "Five fixed methods form the Thesis experiment: Q-Learning, SARSA, DQN, PPO and Dyna-Q+. "
        "The Thesis configuration is read-only. DEVELOPMENT experiments are separate and non-confirmatory.",
    ),
    (
        "Phase A — Nominal learning",
        "Each method learns independently under the same actual-environment-interaction fairness budget. "
        "The exact learned checkpoint is the handoff into Phase B.",
    ),
    (
        "Phase B — Frozen vs Adaptive",
        "Matched deployments start from the same method/checkpoint. Frozen means learning off; Adaptive means learning continues. "
        "They are regimes of the same method, never alternative algorithms to choose between.",
    ),
    (
        "Run",
        "GridWorld is the main live view. Live frames are lossy presentation only: they may be dropped and can never change actions, observations, RNG, timing, metrics or evidence.",
    ),
    (
        "Results",
        "RQ1 reports nominal learning, RQ2 reports matched resilience/adaptation, and RQ3 reports recovery. "
        "The application displays validated stored outputs; it does not recompute scientific estimands.",
    ),
    (
        "Evidence",
        "Evidence shows readiness, registered exports and reproducibility lineage. Technical IDs and hashes are available on demand rather than dominating the workflow.",
    ),
    (
        "Final experiment lock",
        "The final experiment remains locked during T-534. This application cannot authorize final-reserve execution; that gate stays in the Study backend and requires separate T-610 authorization.",
    ),
)


class OnboardingDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Getting started")
        self.setModal(True)
        self.setMinimumWidth(560)
        self.setAccessibleName("Getting started with the thesis experiment application")

        root = QVBoxLayout(self)
        root.setContentsMargins(26, 24, 26, 22)
        root.setSpacing(18)
        self.stack = QStackedWidget()
        for title, body in _STEPS:
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setContentsMargins(0, 0, 0, 0)
            heading = QLabel(title)
            heading.setObjectName("PageTitle")
            text = QLabel(body)
            text.setObjectName("PageLead")
            text.setWordWrap(True)
            text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(heading)
            layout.addWidget(text)
            layout.addStretch(1)
            self.stack.addWidget(page)
        root.addWidget(self.stack, 1)

        controls = QHBoxLayout()
        self.progress = QLabel()
        self.progress.setObjectName("SectionHint")
        controls.addWidget(self.progress)
        controls.addStretch(1)
        self.skip_button = QPushButton("Skip")
        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.finish_button = QPushButton("Finish")
        self.finish_button.setObjectName("PrimaryButton")
        self.skip_button.clicked.connect(self.reject)
        self.previous_button.clicked.connect(self.previous)
        self.next_button.clicked.connect(self.next)
        self.finish_button.clicked.connect(self.accept)
        for button in (
            self.skip_button,
            self.previous_button,
            self.next_button,
            self.finish_button,
        ):
            controls.addWidget(button)
        root.addLayout(controls)
        self._sync()

    def _sync(self) -> None:
        index = self.stack.currentIndex()
        last = self.stack.count() - 1
        self.progress.setText(f"{index + 1} of {self.stack.count()}")
        self.previous_button.setEnabled(index > 0)
        self.next_button.setVisible(index < last)
        self.finish_button.setVisible(index == last)

    def previous(self) -> None:
        self.stack.setCurrentIndex(max(0, self.stack.currentIndex() - 1))
        self._sync()

    def next(self) -> None:
        self.stack.setCurrentIndex(min(self.stack.count() - 1, self.stack.currentIndex() + 1))
        self._sync()
