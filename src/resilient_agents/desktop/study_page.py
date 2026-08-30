"""Recipe-first Thesis Study overview for the PySide6 application."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .protocol import FrozenProtocolSummary, MethodSummary
from .widgets import MetricItem, SectionHeader, StatusPill, VerticalDivider


class MethodItem(QFrame):
    def __init__(self, method: MethodSummary, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("SubtleSurface")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(13, 11, 13, 11)
        layout.setSpacing(3)

        top = QHBoxLayout()
        top.setSpacing(8)
        name = QLabel(method.name)
        name.setObjectName("MethodName")
        config = QLabel(method.config_id)
        config.setObjectName("MethodConfig")
        config.setToolTip(f"Frozen configuration identifier: {method.config_id}")
        top.addWidget(name)
        top.addStretch(1)
        top.addWidget(config)

        description = QLabel(method.description)
        description.setObjectName("MethodDescription")
        description.setWordWrap(True)
        layout.addLayout(top)
        layout.addWidget(description)


class ThesisStudyPage(QWidget):
    technical_details_toggled = Signal(bool)

    def __init__(
        self,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.protocol = protocol
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("Page")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(38, 30, 42, 38)
        self.content_layout.setSpacing(22)

        self._build_header()
        self._build_lock_banner()
        self._build_workflow()
        self._build_metrics()
        self._build_methods()
        self._build_scope()
        self._build_actions()

        self.content_layout.addStretch(1)
        scroll.setWidget(content)
        root.addWidget(scroll)

    def _build_header(self) -> None:
        row = QHBoxLayout()
        row.setSpacing(12)
        text = QVBoxLayout()
        text.setSpacing(5)
        title = QLabel("Thesis Study")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Review the frozen protocol-v2.0 study plan. Scientific settings are fixed by DEC-058."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        text.addWidget(title)
        text.addWidget(lead)
        row.addLayout(text, 1)
        row.addWidget(StatusPill("FROZEN PROTOCOL", kind="frozen"), 0, Qt.AlignmentFlag.AlignTop)
        self.content_layout.addLayout(row)

    def _build_lock_banner(self) -> None:
        banner = QFrame()
        banner.setObjectName("LockedBanner")
        layout = QHBoxLayout(banner)
        layout.setContentsMargins(16, 13, 16, 13)
        layout.setSpacing(14)
        status = StatusPill("LOCKED", kind="locked")
        status.setToolTip("Final scientific execution requires a later explicit T-610+ authorization gate.")
        text = QVBoxLayout()
        text.setSpacing(2)
        title = QLabel("Final evidence execution is not authorized yet")
        title.setObjectName("LockedTitle")
        detail = QLabel(
            "The study is scientifically frozen and ready to review. T-528 builds the application only; "
            "the final reserve remains sealed until the later authorization gate."
        )
        detail.setObjectName("LockedText")
        detail.setWordWrap(True)
        text.addWidget(title)
        text.addWidget(detail)
        layout.addWidget(status)
        layout.addLayout(text, 1)
        self.content_layout.addWidget(banner)

    def _build_workflow(self) -> None:
        self.content_layout.addWidget(
            SectionHeader(
                "Study lifecycle",
                "The application orchestrates this recipe automatically; roots, checkpoints and branch construction are not manual setup steps.",
            )
        )
        surface = QFrame()
        surface.setObjectName("Surface")
        row = QHBoxLayout(surface)
        row.setContentsMargins(18, 15, 18, 15)
        row.setSpacing(11)
        stages = (
            "Nominal learning",
            "Resilience test",
            "Validation",
            "Analysis",
            "Export",
        )
        for index, stage in enumerate(stages):
            label = QLabel(stage)
            label.setObjectName("StageLabel")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(label, 1)
            if index != len(stages) - 1:
                arrow = QLabel("→")
                arrow.setObjectName("StageArrow")
                arrow.setAccessibleName("then")
                row.addWidget(arrow)
        self.content_layout.addWidget(surface)

    def _build_metrics(self) -> None:
        surface = QFrame()
        surface.setObjectName("Surface")
        row = QHBoxLayout(surface)
        row.setContentsMargins(20, 16, 20, 16)
        row.setSpacing(20)
        metrics = (
            (str(len(self.protocol.methods)), "Methods"),
            (str(self.protocol.root_count), "Independent roots"),
            (str(self.protocol.layout_count), "Held-out layouts"),
            (str(self.protocol.condition_count), "Resilience conditions"),
            (str(self.protocol.phase_b_horizon), "Post-change interactions"),
        )
        for index, (value, label) in enumerate(metrics):
            row.addWidget(MetricItem(value, label), 1)
            if index != len(metrics) - 1:
                row.addWidget(VerticalDivider())
        self.content_layout.addWidget(surface)

    def _build_methods(self) -> None:
        self.content_layout.addWidget(
            SectionHeader(
                "Retained methods",
                "All five configurations are frozen. Technical configuration IDs remain visible for reproducibility without becoming setup controls.",
            )
        )
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        for index, method in enumerate(self.protocol.methods):
            grid.addWidget(MethodItem(method), index // 2, index % 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        self.content_layout.addWidget(grid_container)

    def _build_scope(self) -> None:
        self.content_layout.addWidget(SectionHeader("Frozen study scope"))
        surface = QFrame()
        surface.setObjectName("Surface")
        layout = QGridLayout(surface)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setHorizontalSpacing(26)
        layout.setVerticalSpacing(9)
        rows = (
            ("Phase A", f"{self.protocol.phase_a_units} units · {self.protocol.phase_a_training_interactions:,} training interactions"),
            ("Standardized probes", f"{len(self.protocol.probe_indices)} checkpoints · {self.protocol.probe_episodes} episodes per probe"),
            ("Phase B", f"{self.protocol.phase_b_matched_sets} matched sets · {self.protocol.phase_b_branches:,} FN/FD/AN/AD branches"),
            ("Post-boundary", f"{self.protocol.phase_b_post_boundary_interactions:,} branch interactions · {self.protocol.phase_b_prefix_interactions} shared-prefix interactions"),
            ("Evidence", "Root-level inference with blocked/equal-weight layouts; no composite resilience score"),
        )
        for row_index, (label_text, value_text) in enumerate(rows):
            label = QLabel(label_text)
            label.setObjectName("MethodName")
            value = QLabel(value_text)
            value.setObjectName("MethodDescription")
            value.setWordWrap(True)
            layout.addWidget(label, row_index, 0, Qt.AlignmentFlag.AlignTop)
            layout.addWidget(value, row_index, 1)
        layout.setColumnStretch(1, 1)
        self.content_layout.addWidget(surface)

        self.technical = QFrame()
        self.technical.setObjectName("SubtleSurface")
        technical_layout = QVBoxLayout(self.technical)
        technical_layout.setContentsMargins(16, 13, 16, 13)
        technical_layout.setSpacing(5)
        lines = (
            f"Authority: {self.protocol.decision_id}",
            f"Study ID: {self.protocol.study_id}",
            f"Probe interaction indices: {', '.join(str(item) for item in self.protocol.probe_indices)}",
            f"Execution authorization: {self.protocol.execution_authorization}",
            "Final reserve access: false",
        )
        for line in lines:
            label = QLabel(line)
            label.setObjectName("MethodDescription")
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            technical_layout.addWidget(label)
        self.technical.hide()
        self.content_layout.addWidget(self.technical)

    def _build_actions(self) -> None:
        row = QHBoxLayout()
        row.setSpacing(10)
        technical = QPushButton("Technical details")
        technical.setObjectName("SecondaryButton")
        technical.setCheckable(True)
        technical.setCursor(Qt.CursorShape.PointingHandCursor)
        technical.toggled.connect(self._toggle_technical)

        locked = QPushButton("Run final evidence")
        locked.setObjectName("LockedButton")
        locked.setEnabled(False)
        locked.setToolTip(
            "Unavailable during T-528. Final scientific execution requires explicit later T-610+ authorization."
        )
        locked.setAccessibleDescription(
            "Disabled because final reserve scientific execution is not authorized."
        )

        row.addWidget(technical)
        row.addStretch(1)
        row.addWidget(locked)
        self.content_layout.addLayout(row)

    def _toggle_technical(self, visible: bool) -> None:
        self.technical.setVisible(visible)
        self.technical_details_toggled.emit(visible)
