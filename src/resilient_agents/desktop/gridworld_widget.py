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
        self.setMaximumSize(320, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleName("Live GridWorld presentation")
        self.setToolTip(
            "Presentation-only evaluator view. Dropped frames are allowed and this "
            "visualization cannot feed information back to the agent."
        )

    def sizeHint(self) -> QSize:
        return QSize(250, 250)

    def set_frame(self, frame: LiveGridFrame | None) -> None:
        self._frame = frame
        if frame is None:
            self.setAccessibleDescription("No live GridWorld frame is available.")
        else:
            self.setAccessibleDescription(
                f"{frame.width} by {frame.height} GridWorld. Agent true state "
                f"{frame.true_state}; goal {frame.goal}; interaction {frame.interaction_index}."
            )
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

        padding = 12.0
        available_w = max(1.0, self.width() - 2 * padding)
        available_h = max(1.0, self.height() - 2 * padding)
        cell = min(available_w / frame.width, available_h / frame.height)
        grid_w = cell * frame.width
        grid_h = cell * frame.height
        origin_x = (self.width() - grid_w) / 2.0
        origin_y = (self.height() - grid_h) / 2.0

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

        # Goal marker.
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

        # Delivered observation is evaluator-visible here only as presentation;
        # a dashed outline makes corruption legible without becoming agent input.
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

        # True agent state.
        ax, ay = frame.true_state
        center = QPointF(
            origin_x + (ax + 0.5) * cell,
            origin_y + (ay + 0.5) * cell,
        )
        radius = cell * 0.27
        painter.setPen(QPen(QColor("#173F98"), max(1.0, cell * 0.04)))
        painter.setBrush(QBrush(QColor("#245DE8")))
        painter.drawEllipse(center, radius, radius)
