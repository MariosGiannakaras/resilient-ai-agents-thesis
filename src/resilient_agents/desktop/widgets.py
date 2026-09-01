"""Small reusable Qt widgets for the desktop design system."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class NavButton(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("NavButton")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(38)


class StatusPill(QLabel):
    _OBJECT_NAMES = {
        "locked": "StatusLocked",
        "frozen": "StatusFrozen",
        "development": "StatusDevelopment",
    }
    _SYMBOLS = {
        "locked": "⊘",
        "frozen": "■",
        "development": "◇",
    }

    def __init__(self, text: str, *, kind: str, parent: QWidget | None = None) -> None:
        try:
            object_name = self._OBJECT_NAMES[kind]
            symbol = "⊘" if "LOCK" in text.upper() else self._SYMBOLS[kind]
        except KeyError as exc:
            raise ValueError(f"unsupported status pill kind: {kind!r}") from exc
        super().__init__(f"{symbol}  {text}", parent)
        self.setObjectName(object_name)
        self.setAccessibleName(text)
        self.setToolTip(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)


class MetricItem(QWidget):
    def __init__(self, value: str, label: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        value_label = QLabel(value)
        value_label.setObjectName("MetricValue")
        label_widget = QLabel(label)
        label_widget.setObjectName("MetricLabel")
        layout.addWidget(value_label)
        layout.addWidget(label_widget)


class VerticalDivider(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Divider")
        self.setFrameShape(QFrame.Shape.NoFrame)


class SectionHeader(QWidget):
    def __init__(
        self,
        title: str,
        hint: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        title_label = QLabel(title)
        title_label.setObjectName("SectionTitle")
        layout.addWidget(title_label)
        if hint:
            hint_label = QLabel(hint)
            hint_label.setObjectName("SectionHint")
            hint_label.setWordWrap(True)
            layout.addWidget(hint_label)


class EmptyState(QFrame):
    def __init__(
        self,
        title: str,
        message: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("Surface")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(7)
        title_label = QLabel(title)
        title_label.setObjectName("SectionTitle")
        message_label = QLabel(message)
        message_label.setObjectName("PageLead")
        message_label.setWordWrap(True)
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addStretch(1)


def horizontal_row(*widgets: QWidget, spacing: int = 10) -> QWidget:
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(spacing)
    for widget in widgets:
        layout.addWidget(widget)
    return container
