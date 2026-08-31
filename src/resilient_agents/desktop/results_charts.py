"""Lightweight Qt-native charts for already-computed stored analysis summaries.

These widgets perform presentation scaling only. They never calculate scientific
estimands, confidence intervals, rankings or aggregate scores.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

_METHOD_COLORS = {
    "q_learning": "#245DE8",
    "sarsa": "#0E7490",
    "dqn": "#7C3AED",
    "ppo": "#C25B16",
    "dyna_q_plus": "#14866D",
}


@dataclass(frozen=True)
class StoredBar:
    key: str
    label: str
    value: float
    lower: float | None = None
    upper: float | None = None
    variant: str = "primary"

    def __post_init__(self) -> None:
        if not self.key or not self.label:
            raise ValueError("chart bar key/label must be non-empty")
        if not isfinite(self.value):
            raise ValueError("chart bar value must be finite")
        if (self.lower is None) != (self.upper is None):
            raise ValueError("chart interval requires both lower and upper")
        if self.lower is not None:
            if not isfinite(self.lower) or not isfinite(self.upper):
                raise ValueError("chart interval bounds must be finite")
            if self.lower > self.upper:
                raise ValueError("chart interval bounds are reversed")


class StoredIntervalBarChart(QWidget):
    """Read-only bar chart with optional stored interval whiskers."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._bars: tuple[StoredBar, ...] = ()
        self._title = "Stored analysis summary"
        self._legend: tuple[tuple[str, str], ...] = ()
        self.setMinimumHeight(205)
        self.setMaximumHeight(285)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setAccessibleName("Stored analysis chart")

    def sizeHint(self) -> QSize:
        return QSize(760, 230)

    def set_data(
        self,
        *,
        title: str,
        bars: tuple[StoredBar, ...],
        legend: tuple[tuple[str, str], ...] = (),
    ) -> None:
        self._title = title
        self._bars = tuple(bars)
        self._legend = tuple(legend)
        parts = [title]
        for bar in self._bars:
            interval = ""
            if bar.lower is not None and bar.upper is not None:
                interval = f", stored interval {bar.lower:.5g} to {bar.upper:.5g}"
            parts.append(f"{bar.label}: {bar.value:.5g}{interval}")
        self.setAccessibleDescription(". ".join(parts))
        self.update()

    @staticmethod
    def _method_color(key: str, *, secondary: bool = False) -> QColor:
        base = QColor(_METHOD_COLORS.get(key, "#667085"))
        if secondary:
            base.setAlpha(105)
        return base

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt naming contract
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), QColor("#FFFFFF"))

        title_pen = QPen(QColor("#101828"))
        hint_pen = QPen(QColor("#667085"))
        grid_pen = QPen(QColor("#E4E7EC"), 1.0)
        axis_pen = QPen(QColor("#98A2B3"), 1.0)
        painter.setPen(title_pen)
        painter.drawText(14, 24, self._title)

        if not self._bars:
            painter.setPen(hint_pen)
            painter.drawText(self.rect().adjusted(14, 38, -14, -12), Qt.AlignmentFlag.AlignCenter, "No stored values available")
            return

        values: list[float] = [0.0]
        for bar in self._bars:
            values.append(bar.value)
            if bar.lower is not None and bar.upper is not None:
                values.extend((bar.lower, bar.upper))
        minimum = min(values)
        maximum = max(values)
        if minimum == maximum:
            padding = 1.0 if minimum == 0 else abs(minimum) * 0.2
            minimum -= padding
            maximum += padding
        else:
            padding = (maximum - minimum) * 0.12
            minimum -= padding
            maximum += padding

        left = 58.0
        right = 18.0
        top = 44.0
        bottom = 46.0
        if self._legend:
            top += 20.0
        plot = QRectF(left, top, max(1.0, self.width() - left - right), max(1.0, self.height() - top - bottom))

        def y_for(value: float) -> float:
            fraction = (value - minimum) / (maximum - minimum)
            return plot.bottom() - fraction * plot.height()

        # Sparse horizontal guides with numeric labels.
        metrics = QFontMetrics(painter.font())
        for step in range(5):
            value = minimum + (maximum - minimum) * step / 4.0
            y = y_for(value)
            painter.setPen(grid_pen)
            painter.drawLine(plot.left(), y, plot.right(), y)
            painter.setPen(hint_pen)
            label = f"{value:.3g}"
            painter.drawText(QRectF(2, y - 9, left - 10, 18), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, label)

        zero_y = y_for(0.0)
        painter.setPen(axis_pen)
        painter.drawLine(plot.left(), zero_y, plot.right(), zero_y)

        if self._legend:
            x = plot.left()
            painter.setPen(hint_pen)
            for text, variant in self._legend:
                color = QColor("#245DE8")
                if variant == "secondary":
                    color.setAlpha(105)
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(QRectF(x, 35, 10, 10), 2, 2)
                painter.setPen(hint_pen)
                painter.drawText(QRectF(x + 15, 30, 120, 20), Qt.AlignmentFlag.AlignVCenter, text)
                x += 120

        group_count = len({bar.label for bar in self._bars})
        bar_count = len(self._bars)
        slot = plot.width() / max(1, bar_count)
        width = min(32.0, max(8.0, slot * 0.56))

        for index, bar in enumerate(self._bars):
            center_x = plot.left() + slot * (index + 0.5)
            value_y = y_for(bar.value)
            rect_top = min(value_y, zero_y)
            rect_bottom = max(value_y, zero_y)
            color = self._method_color(bar.key, secondary=bar.variant == "secondary")
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(center_x - width / 2, rect_top, width, max(1.5, rect_bottom - rect_top)), 3, 3)

            if bar.lower is not None and bar.upper is not None:
                high_y = y_for(bar.upper)
                low_y = y_for(bar.lower)
                painter.setPen(QPen(QColor("#344054"), 1.2))
                painter.drawLine(center_x, high_y, center_x, low_y)
                painter.drawLine(center_x - 5, high_y, center_x + 5, high_y)
                painter.drawLine(center_x - 5, low_y, center_x + 5, low_y)

        # X labels are drawn once per consecutive label group to avoid duplicating
        # method names for paired learning bars.
        seen: dict[str, list[int]] = {}
        for index, bar in enumerate(self._bars):
            seen.setdefault(bar.label, []).append(index)
        for label, indexes in seen.items():
            first = indexes[0]
            last = indexes[-1]
            center_x = plot.left() + slot * ((first + last) / 2.0 + 0.5)
            text_rect = QRectF(center_x - 58, plot.bottom() + 7, 116, 30)
            painter.setPen(hint_pen)
            elided = metrics.elidedText(label, Qt.TextElideMode.ElideRight, int(text_rect.width()))
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, elided)
