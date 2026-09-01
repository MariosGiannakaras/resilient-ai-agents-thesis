"""Truthful empty pages used until their T-528 feature slices are connected."""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .widgets import EmptyState


class PlaceholderPage(QWidget):
    def __init__(self, title: str, message: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Page")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(38, 30, 42, 38)
        layout.setSpacing(20)
        title_label = QLabel(title)
        title_label.setObjectName("PageTitle")
        layout.addWidget(title_label)
        layout.addWidget(EmptyState(f"No {title.lower()} to show yet", message))
        layout.addStretch(1)
