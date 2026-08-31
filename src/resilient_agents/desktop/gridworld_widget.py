"""Qt-native read-only GridWorld presentation widget."""
from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from .live_events import LiveGridFrame


class GridWorldLiveWidget(QWidget):
    """Render evaluator-visible state without exposing controls to the learner."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._frame: LiveGridFrame | None = None
        self.setMinimumSize(210, 210)
        self.setMaximumSize(560, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleName("Live GridWorld presentation")
        self.setToolTip(
            "Presentation-only evaluator view. Dropped frames are allowed and this "
            "visualization cannot feed information back to the agent."
        )

    def sizeHint(self) -> QSize:
        if self._frame is not None and self._frame.comparison is not None:
            return QSize(520, 250)
        return QSize(250, 250)

    def set_frame(self, frame: LiveGridFrame | None) -> None:
        self._frame = frame
        if frame is None:
            self.setAccessibleDescription("No live GridWorld frame is available.")
        elif frame.comparison is not None:
            pair = frame.comparison
            self.setAccessibleDescription(
                f"Matched Frozen and Adaptive GridWorld presentation at interaction "
                f"{pair.adaptive.interaction_index}. Frozen true state "
                f"{pair.frozen.true_state}; Adaptive true state {pair.adaptive.true_state}; "
                f"goal {pair.adaptive.goal}."
            )
        else:
            self.setAccessibleDescription(
                f"{frame.width} by {frame.height} GridWorld. Agent true state "
                f"{frame.true_state}; goal {frame.goal}; interaction {frame.interaction_index}."
            )
        self.updateGeometry()
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt naming contract
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), QColor("#F8FAFD"))
        frame = self._frame
        if frame is None:
            painter.setPen(QColor("#667085"))
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                "Live GridWorld\nNo presentation frame available",
            )
            return

        comparison = frame.comparison
        if comparison is None:
            self._paint_grid(
                painter,
                frame,
                QRectF(0.0, 0.0, float(self.width()), float(self.height())),
            )
            return

        gap = 12.0
        full = QRectF(0.0, 0.0, float(self.width()), float(self.height()))
        panel_width = max(1.0, (full.width() - gap) / 2.0)
        left = QRectF(full.left(), full.top(), panel_width, full.height())
        right = QRectF(left.right() + gap, full.top(), panel_width, full.height())
        self._paint_grid(painter, comparison.frozen, left, title="Frozen disturbed")
        self._paint_grid(painter, comparison.adaptive, right, title="Adaptive disturbed")

    @staticmethod
    def _paint_grid(
        painter: QPainter,
        frame: LiveGridFrame,
        area: QRectF,
        *,
        title: str | None = None,
    ) -> None:
        title_height = 24.0 if title else 0.0
        if title:
            painter.setPen(QColor("#344054"))
            painter.drawText(
                QRectF(area.left(), area.top(), area.width(), title_height),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                title,
            )

        padding = 10.0
        usable = QRectF(
            area.left() + padding,
            area.top() + title_height + padding,
            max(1.0, area.width() - 2 * padding),
            max(1.0, area.height() - title_height - 2 * padding),
        )
        cell = min(usable.width() / frame.width, usable.height() / frame.height)
        grid_w = cell * frame.width
        grid_h = cell * frame.height
        origin_x = usable.left() + (usable.width() - grid_w) / 2.0
        origin_y = usable.top() + (usable.height() - grid_h) / 2.0

        border = QPen(QColor("#D0D5DD"), 1.0)
        obstacle_brush = QBrush(QColor("#344054"))
        goal_brush = QBrush(QColor("#D1FADF"))
        start_brush = QBrush(QColor("#EAF1FF"))
        observation_pen = QPen(QColor("#9B51E0"), max(1.5, cell * 0.06))
        observation_pen.setStyle(Qt.PenStyle.DashLine)

        obstacles = set(frame.obstacles)
        for y in range(frame.height):
            for x in range(frame.width):
                rect = QRectF(origin_x + x * cell, origin_y + y * cell, cell, cell)
                if (x, y) in obstacles:
                    painter.fillRect(rect, obstacle_brush)
                elif (x, y) == frame.goal:
                    painter.fillRect(rect, goal_brush)
                elif (x, y) == frame.start:
                    painter.fillRect(rect, start_brush)
                painter.setPen(border)
                painter.drawRect(rect)

        gx, gy = frame.goal
        goal_rect = QRectF(
            origin_x + gx * cell + cell * 0.27,
            origin_y + gy * cell + cell * 0.27,
            cell * 0.46,
            cell * 0.46,
        )
        painter.setPen(QPen(QColor("#067647"), max(1.0, cell * 0.045)))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(goal_rect)

        if frame.delivered_observation != frame.true_state:
            ox, oy = frame.delivered_observation
            obs_rect = QRectF(
                origin_x + ox * cell + cell * 0.12,
                origin_y + oy * cell + cell * 0.12,
                cell * 0.76,
                cell * 0.76,
            )
            painter.setPen(observation_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(obs_rect, cell * 0.12, cell * 0.12)

        ax, ay = frame.true_state
        center = QPointF(
            origin_x + (ax + 0.5) * cell,
            origin_y + (ay + 0.5) * cell,
        )
        radius = cell * 0.27
        painter.setPen(QPen(QColor("#173F98"), max(1.0, cell * 0.04)))
        painter.setBrush(QBrush(QColor("#245DE8")))
        painter.drawEllipse(center, radius, radius)
