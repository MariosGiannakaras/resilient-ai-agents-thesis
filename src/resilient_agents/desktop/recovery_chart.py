"""Qt-native RQ3 trajectory visualization over already-stored recovery evidence.

The widget performs presentation scaling only. It does not reduce roots, apply
recovery thresholds, determine recovery times, or replace right-censoring. All
scientific classifications and summary markers are supplied by the stored
validated analysis package.
"""
from __future__ import annotations

from collections import defaultdict
from math import isfinite

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from .results_read_model import RecoveryTrajectoryPoint


class RecoveryTrajectoryChart(QWidget):
    """Present stored root trajectories, tolerance contract and censoring state."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._title = "Stored recovery trajectories"
        self._points: tuple[RecoveryTrajectoryPoint, ...] = ()
        self._tolerance = 0.0
        self._window_size = 1
        self._horizon = 1
        self._recovered_count = 0
        self._censored_count = 0
        self._stored_recovery_time_mean: float | None = None
        self.setMinimumHeight(210)
        self.setMaximumHeight(270)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setAccessibleName("Stored recovery trajectory chart")

    def sizeHint(self) -> QSize:
        return QSize(820, 235)

    def set_data(
        self,
        *,
        title: str,
        points: tuple[RecoveryTrajectoryPoint, ...],
        tolerance: float,
        window_size: int,
        horizon: int,
        recovered_count: int,
        censored_count: int,
        stored_recovery_time_mean: float | None,
    ) -> None:
        if tolerance < 0 or not isfinite(tolerance):
            raise ValueError("recovery chart tolerance must be finite and non-negative")
        if window_size <= 0 or horizon <= 0 or horizon % window_size:
            raise ValueError("recovery chart window grid is invalid")
        if recovered_count < 0 or censored_count < 0:
            raise ValueError("recovery chart counts must be non-negative")
        if stored_recovery_time_mean is not None:
            if not isfinite(stored_recovery_time_mean) or stored_recovery_time_mean < 0:
                raise ValueError("stored recovery-time marker must be finite and non-negative")
        self._title = title
        self._points = tuple(points)
        self._tolerance = float(tolerance)
        self._window_size = int(window_size)
        self._horizon = int(horizon)
        self._recovered_count = int(recovered_count)
        self._censored_count = int(censored_count)
        self._stored_recovery_time_mean = stored_recovery_time_mean
        marker = (
            f"stored conditional recovery-time mean {stored_recovery_time_mean:.5g}"
            if stored_recovery_time_mean is not None
            else f"no observed recovery-time summary; right-censored through {horizon}"
        )
        self.setAccessibleDescription(
            f"{title}. {recovered_count} recovered roots and {censored_count} right-censored roots. "
            f"Stored tolerance {tolerance:.5g}, {window_size}-interaction windows, {marker}. "
            "Each line is one stored root trajectory; no UI aggregation is performed."
        )
        self.update()

    def clear(self) -> None:
        self.set_data(
            title="Stored recovery trajectories",
            points=(),
            tolerance=0.0,
            window_size=1,
            horizon=1,
            recovered_count=0,
            censored_count=0,
            stored_recovery_time_mean=None,
        )

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt naming contract
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), QColor("#FFFFFF"))

        title_pen = QPen(QColor("#101828"))
        hint_pen = QPen(QColor("#536781"))
        grid_pen = QPen(QColor("#E4E9F0"), 1.0)
        baseline_pen = QPen(QColor("#667085"), 1.2)
        baseline_pen.setStyle(Qt.PenStyle.DashLine)
        tolerance_pen = QPen(QColor("#245DE8"), 1.25)
        tolerance_pen.setStyle(Qt.PenStyle.DashLine)

        painter.setPen(title_pen)
        painter.drawText(14, 22, self._title)
        status = f"{self._recovered_count} recovered · {self._censored_count} right-censored"
        painter.setPen(hint_pen)
        painter.drawText(
            QRectF(max(180.0, self.width() - 310.0), 8.0, 294.0, 20.0),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
            status,
        )

        if not self._points:
            painter.drawText(
                self.rect().adjusted(14, 34, -14, -12),
                Qt.AlignmentFlag.AlignCenter,
                "No stored recovery trajectory is available for this selection.",
            )
            return

        left = 62.0
        right = 24.0
        top = 44.0
        bottom = 38.0
        plot = QRectF(
            left,
            top,
            max(1.0, self.width() - left - right),
            max(1.0, self.height() - top - bottom),
        )

        gaps = [point.directed_gap for point in self._points]
        minimum = min(0.0, min(gaps))
        maximum = max(self._tolerance, max(gaps))
        if minimum == maximum:
            maximum = minimum + 1.0
        padding = max((maximum - minimum) * 0.12, 0.02)
        minimum -= padding
        maximum += padding

        def x_for(interaction: float) -> float:
            fraction = max(0.0, min(1.0, interaction / self._horizon))
            return plot.left() + fraction * plot.width()

        def y_for(value: float) -> float:
            fraction = (value - minimum) / (maximum - minimum)
            return plot.bottom() - fraction * plot.height()

        # Stored tolerance band: presentation of the frozen contract, not a new test.
        zero_y = y_for(0.0)
        tolerance_y = y_for(self._tolerance)
        band_top = min(zero_y, tolerance_y)
        band_bottom = max(zero_y, tolerance_y)
        painter.fillRect(
            QRectF(plot.left(), band_top, plot.width(), max(1.0, band_bottom - band_top)),
            QBrush(QColor("#EDF3FF")),
        )

        window_count = self._horizon // self._window_size
        metrics = QFontMetrics(painter.font())
        for index in range(window_count + 1):
            interaction = index * self._window_size
            x = x_for(interaction)
            painter.setPen(grid_pen)
            painter.drawLine(x, plot.top(), x, plot.bottom())
            if index in {0, window_count} or window_count <= 8 or index % 2 == 0:
                painter.setPen(hint_pen)
                label = str(interaction)
                width = metrics.horizontalAdvance(label) + 8
                painter.drawText(
                    QRectF(x - width / 2, plot.bottom() + 6, width, 18),
                    Qt.AlignmentFlag.AlignCenter,
                    label,
                )

        for step in range(4):
            value = minimum + (maximum - minimum) * step / 3.0
            y = y_for(value)
            painter.setPen(grid_pen)
            painter.drawLine(plot.left(), y, plot.right(), y)
            painter.setPen(hint_pen)
            painter.drawText(
                QRectF(2, y - 9, left - 10, 18),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"{value:.3g}",
            )

        painter.setPen(baseline_pen)
        painter.drawLine(plot.left(), zero_y, plot.right(), zero_y)
        painter.setPen(hint_pen)
        painter.drawText(
            QRectF(plot.left() + 6, zero_y - 18, 120, 17),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            "Baseline gap = 0",
        )

        painter.setPen(tolerance_pen)
        painter.drawLine(plot.left(), tolerance_y, plot.right(), tolerance_y)
        painter.drawText(
            QRectF(plot.right() - 180, tolerance_y - 18, 176, 17),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
            f"Stored tolerance ≤ {self._tolerance:.3g}",
        )

        by_root: dict[str, list[RecoveryTrajectoryPoint]] = defaultdict(list)
        for point in self._points:
            by_root[point.root_id].append(point)
        for root_index, root_id in enumerate(sorted(by_root)):
            points = sorted(by_root[root_id], key=lambda item: item.window_end)
            color = QColor("#245DE8")
            color.setAlpha(max(70, 210 - root_index * 10))
            line_pen = QPen(color, 1.4)
            painter.setPen(line_pen)
            previous = None
            for point in points:
                current = (x_for(point.window_end), y_for(point.directed_gap))
                if previous is not None:
                    painter.drawLine(previous[0], previous[1], current[0], current[1])
                radius = 3.2 if point.within_tolerance else 2.5
                painter.setBrush(
                    QBrush(QColor("#FFFFFF") if point.within_tolerance else color)
                )
                painter.setPen(QPen(color, 1.3))
                painter.drawEllipse(QRectF(current[0] - radius, current[1] - radius, radius * 2, radius * 2))
                previous = current

        if self._stored_recovery_time_mean is not None:
            marker_x = x_for(self._stored_recovery_time_mean)
            marker_pen = QPen(QColor("#173F98"), 1.6)
            painter.setPen(marker_pen)
            painter.drawLine(marker_x, plot.top(), marker_x, plot.bottom())
            painter.setPen(title_pen)
            painter.drawText(
                QRectF(marker_x + 5, plot.top() + 4, 220, 18),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                f"Stored mean recovery time* {self._stored_recovery_time_mean:.3g}",
            )
        else:
            horizon_x = x_for(self._horizon)
            censor_pen = QPen(QColor("#667085"), 1.5)
            censor_pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(censor_pen)
            painter.drawLine(horizon_x, plot.top(), horizon_x, plot.bottom())
            painter.setPen(title_pen)
            painter.drawText(
                QRectF(plot.right() - 250, plot.top() + 4, 242, 18),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"Right-censored through {self._horizon}",
            )

        painter.setPen(hint_pen)
        painter.drawText(
            QRectF(plot.left(), self.height() - 20, plot.width(), 17),
            Qt.AlignmentFlag.AlignCenter,
            f"Interaction window end · stored {self._window_size}-interaction windows",
        )
