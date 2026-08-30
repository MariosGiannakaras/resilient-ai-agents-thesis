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
        layout.setContentsMargins(11, 9, 11, 9)
        layout.setSpacing(3)

        top = QHBoxLayout()
        top.setSpacing(6)
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
        description.setToolTip(method.description)
        layout.addLayout(top)
        layout.addWidget(description)
        layout.addStretch(1)


class ScopeItem(QWidget):
    def __init__(self, label: str, value: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        heading = QLabel(label)
        heading.setObjectName("MethodName")
        detail = QLabel(value)
        detail.setObjectName("MethodDescription")
        detail.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(detail)


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
        self.content_layout.setContentsMargins(38, 24, 42, 28)
        self.content_layout.setSpacing(15)

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
        self.scroll = scroll

    def _build_header(self) -> None:
        row = QHBoxLayout()
        row.setSpacing(12)
        text = QVBoxLayout()
        text.setSpacing(3)
        title = QLabel("Thesis Study")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Review the frozen protocol-v2.0 plan. Scientific settings are fixed by DEC-058."
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
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(12)
        status = StatusPill("LOCKED", kind="locked")
        status.setToolTip("Final scientific execution requires a later explicit T-610+ authorization gate.")
        text = QVBoxLayout()
        text.setSpacing(1)
        title = QLabel("Final evidence execution is not authorized yet")
        title.setObjectName("LockedTitle")
        detail = QLabel(
            "The protocol is frozen and ready to review; final-reserve execution stays sealed until the later authorization gate."
        )
        detail.setObjectName("LockedText")
        detail.setWordWrap(True)
        text.addWidget(title)
        text.addWidget(detail)
        layout.addWidget(status)
        layout.addLayout(text, 1)
        self.content_layout.addWidget(banner)

    def _build_workflow(self) -> None:
        surface = QFrame()
        surface.setObjectName("Surface")
        outer = QVBoxLayout(surface)
        outer.setContentsMargins(16, 11, 16, 11)
        outer.setSpacing(7)

        header = QHBoxLayout()
        title = QLabel("Study lifecycle")
        title.setObjectName("SectionTitle")
        hint = QLabel("Automatically orchestrated from the frozen recipe")
        hint.setObjectName("SectionHint")
        hint.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(hint)
        outer.addLayout(header)

        row = QHBoxLayout()
        row.setSpacing(9)
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
            label.setToolTip(
                "Roots, checkpoints and branch construction are backend recipe responsibilities, not manual UI setup."
            )
            row.addWidget(label, 1)
            if index != len(stages) - 1:
                arrow = QLabel("→")
                arrow.setObjectName("StageArrow")
                arrow.setAccessibleName("then")
                row.addWidget(arrow)
        outer.addLayout(row)
        self.content_layout.addWidget(surface)

    def _build_metrics(self) -> None:
        surface = QFrame()
        surface.setObjectName("Surface")
        row = QHBoxLayout(surface)
        row.setContentsMargins(18, 11, 18, 11)
        row.setSpacing(16)
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
                "Frozen configurations; IDs remain visible for reproducibility, not editing.",
            )
        )
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(0)
        for index, method in enumerate(self.protocol.methods):
            grid.addWidget(MethodItem(method), 0, index)
            grid.setColumnStretch(index, 1)
        self.content_layout.addWidget(grid_container)

    def _build_scope(self) -> None:
        self.content_layout.addWidget(SectionHeader("Frozen study scope"))
        surface = QFrame()
        surface.setObjectName("Surface")
        row = QHBoxLayout(surface)
        row.setContentsMargins(16, 11, 16, 11)
        row.setSpacing(16)
        items = (
            (
                "Phase A",
                f"{self.protocol.phase_a_units} units · {self.protocol.phase_a_training_interactions:,} training interactions",
            ),
            (
                "Phase B",
                f"{self.protocol.phase_b_matched_sets} matched sets · {self.protocol.phase_b_branches:,} branches · {self.protocol.phase_b_post_boundary_interactions:,} post-boundary interactions",
            ),
            (
                "Inference",
                "Root-level uncertainty · equal-weight layouts · no composite resilience score",
            ),
        )
        for index, (label, value) in enumerate(items):
            row.addWidget(ScopeItem(label, value), 1)
            if index != len(items) - 1:
                row.addWidget(VerticalDivider())
        self.content_layout.addWidget(surface)

        self.technical = QFrame()
        self.technical.setObjectName("SubtleSurface")
        technical_layout = QGridLayout(self.technical)
        technical_layout.setContentsMargins(14, 10, 14, 10)
        technical_layout.setHorizontalSpacing(22)
        technical_layout.setVerticalSpacing(4)
        details = (
            ("Authority", self.protocol.decision_id),
            ("Study ID", self.protocol.study_id),
            ("Probe indices", ", ".join(str(item) for item in self.protocol.probe_indices)),
            ("Probe episodes", str(self.protocol.probe_episodes)),
            ("Shared prefix", f"{self.protocol.phase_b_prefix_interactions} total interactions across matched sets"),
            ("Execution gate", self.protocol.execution_authorization),
            ("Final reserve", "access=false"),
        )
        for index, (name, value) in enumerate(details):
            name_label = QLabel(name)
            name_label.setObjectName("MethodName")
            value_label = QLabel(value)
            value_label.setObjectName("MethodDescription")
            value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            column = (index % 2) * 2
            row_index = index // 2
            technical_layout.addWidget(name_label, row_index, column)
            technical_layout.addWidget(value_label, row_index, column + 1)
        technical_layout.setColumnStretch(1, 1)
        technical_layout.setColumnStretch(3, 1)
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
        if visible:
            self.scroll.ensureWidgetVisible(self.technical, 0, 18)
        self.technical_details_toggled.emit(visible)
