"""Qt-native read-only GridWorld presentation widget."""
from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
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
            return QSize(520, 270)
        return QSize(250, 250)

    def set_frame(self, frame: LiveGridFrame | None) -> None:
        self._frame = frame
        if frame is None:
            self.setAccessibleDescription("No live GridWorld frame is available.")
        elif frame.comparison is not None:
            pair = frame.comparison
            condition = pair.adaptive.condition_id or "unavailable"
            self.setAccessibleDescription(
                f"Matched Frozen and Adaptive GridWorld presentation for condition "
                f"{condition} at interaction {pair.adaptive.interaction_index}. Frozen, "
                f"learning off, true state {pair.frozen.true_state}, intended action "
                f"{pair.frozen.intended_action}, executed action "
                f"{pair.frozen.executed_action}, reward {pair.frozen.reward:g}; "
                f"Adaptive, learning continues, true state {pair.adaptive.true_state}, "
                f"intended action {pair.adaptive.intended_action}, executed action "
                f"{pair.adaptive.executed_action}, reward {pair.adaptive.reward:g}; "
                f"goal {pair.adaptive.goal}."
            )
        else:
            self.setAccessibleDescription(
                f"{frame.width} by {frame.height} GridWorld. Agent true state "
                f"{frame.true_state}; goal {frame.goal}; interaction "
                f"{frame.interaction_index}; intended action "
                f"{frame.intended_action}; executed action {frame.executed_action}; "
                f"reward {frame.reward:g}."
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
        self._paint_grid(
            painter,
            comparison.frozen,
            left,
            title="Frozen — learning off",
        )
        self._paint_grid(
            painter,
            comparison.adaptive,
            right,
            title="Adaptive — learning continues",
        )

    @staticmethod
    def _paint_grid(
        painter: QPainter,
        frame: LiveGridFrame,
        area: QRectF,
        *,
        title: str | None = None,
    ) -> None:
        # QPainter keeps pen/brush state between calls. Each panel explicitly
        # starts from a neutral brush so the first panel's agent marker cannot
        # leak into the second panel's cell rectangles.
        painter.setBrush(Qt.BrushStyle.NoBrush)

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
                painter.setBrush(Qt.BrushStyle.NoBrush)
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
        painter.setPen(QColor("#067647"))
        painter.drawText(goal_rect, Qt.AlignmentFlag.AlignCenter, "G")

        sx, sy = frame.start
        start_rect = QRectF(
            origin_x + sx * cell,
            origin_y + sy * cell,
            cell,
            cell,
        )
        painter.setPen(QColor("#315B70"))
        painter.drawText(start_rect, Qt.AlignmentFlag.AlignCenter, "S")

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

        directions = {
            "up": QPointF(0.0, -1.0),
            "right": QPointF(1.0, 0.0),
            "down": QPointF(0.0, 1.0),
            "left": QPointF(-1.0, 0.0),
        }
        direction = directions.get(frame.executed_action.lower())
        if direction is None:
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(
                QRectF(
                    center.x() - radius,
                    center.y() - radius,
                    radius * 2,
                    radius * 2,
                ),
                Qt.AlignmentFlag.AlignCenter,
                "A",
            )
            return

        perpendicular = QPointF(-direction.y(), direction.x())
        tail = QPointF(
            center.x() - direction.x() * radius * 0.48,
            center.y() - direction.y() * radius * 0.48,
        )
        tip = QPointF(
            center.x() + direction.x() * radius * 0.55,
            center.y() + direction.y() * radius * 0.55,
        )
        head_base = QPointF(
            center.x() + direction.x() * radius * 0.08,
            center.y() + direction.y() * radius * 0.08,
        )
        head_left = QPointF(
            head_base.x() + perpendicular.x() * radius * 0.32,
            head_base.y() + perpendicular.y() * radius * 0.32,
        )
        head_right = QPointF(
            head_base.x() - perpendicular.x() * radius * 0.32,
            head_base.y() - perpendicular.y() * radius * 0.32,
        )
        painter.setPen(QPen(QColor("#FFFFFF"), max(1.5, cell * 0.055)))
        painter.drawLine(tail, tip)
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(QPolygonF([tip, head_left, head_right]))
