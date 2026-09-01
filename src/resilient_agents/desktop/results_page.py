"""Read-only stored-evidence Results workspace."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .protocol import FrozenProtocolSummary
from .results_charts import StoredBar, StoredIntervalBarChart
from .results_read_model import (
    DesktopResultsReadModel,
    StoredAnalysisPackage,
    StoredSummary,
)
from .widgets import EmptyState, SectionHeader, StatusPill

_CONDITION_NAMES = {
    "action-remap-swap-right-down": "Action remap · swap right/down",
    "action-remap-cycle-clockwise": "Action remap · clockwise cycle",
    "action-failure-0.15": "Action failure · 15%",
    "observation-corruption-0.05": "Observation corruption · 5%",
}


def _display_identifier(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def _format_number(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:.5g}"


def _format_interval(summary: StoredSummary) -> str:
    if summary.interval_lower is not None and summary.interval_upper is not None:
        return f"[{_format_number(summary.interval_lower)}, {_format_number(summary.interval_upper)}]"
    if summary.interval_status == "insufficient-independent-roots":
        return "Unavailable (n < 2 roots)"
    return "—"


class ResultsPage(QWidget):
    def __init__(
        self,
        read_model: DesktopResultsReadModel,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.read_model = read_model
        self.method_names = {method.method_id: method.name for method in protocol.methods}
        self.current_package: StoredAnalysisPackage | None = None
        self.setObjectName("Page")

        root = QVBoxLayout(self)
        root.setContentsMargins(38, 28, 42, 34)
        root.setSpacing(15)

        header = QHBoxLayout()
        title_block = QVBoxLayout()
        title_block.setSpacing(4)
        title = QLabel("Results")
        title.setObjectName("PageTitle")
        lead = QLabel(
            "Compare stored learning and resilience analysis produced by the backend. "
            "This view does not recompute estimands, intervals or rankings."
        )
        lead.setObjectName("PageLead")
        lead.setWordWrap(True)
        title_block.addWidget(title)
        title_block.addWidget(lead)
        header.addLayout(title_block, 1)
        refresh = QPushButton("Refresh")
        refresh.setObjectName("SecondaryButton")
        refresh.setToolTip("Rescan durable Studies for registered analysis-package artifacts.")
        refresh.clicked.connect(self.refresh)
        header.addWidget(refresh, 0, Qt.AlignmentFlag.AlignTop)
        root.addLayout(header)

        self.selector_surface = QFrame()
        self.selector_surface.setObjectName("Surface")
        selector_layout = QHBoxLayout(self.selector_surface)
        selector_layout.setContentsMargins(18, 13, 18, 13)
        selector_layout.setSpacing(12)
        selector_label = QLabel("Analysis Study")
        selector_label.setObjectName("ReviewLabel")
        selector_layout.addWidget(selector_label)
        self.study_combo = QComboBox()
        self.study_combo.setMinimumWidth(330)
        self.study_combo.setToolTip(
            "Only Studies with a registered derived analysis-package artifact appear here."
        )
        self.study_combo.setAccessibleName("Analysis study")
        selector_label.setBuddy(self.study_combo)
        self.study_combo.currentIndexChanged.connect(self._selection_changed)
        selector_layout.addWidget(self.study_combo)
        selector_layout.addStretch(1)
        selector_layout.addWidget(StatusPill("STORED ANALYSIS", kind="frozen"))
        root.addWidget(self.selector_surface)

        self.error = QLabel()
        self.error.setObjectName("ErrorText")
        self.error.setWordWrap(True)
        self.error.hide()
        root.addWidget(self.error)

        self.empty = EmptyState(
            "No stored analysis yet",
            "Results become available only after a Study reaches backend validation and analysis. "
            "Creating or configuring a Study does not invent preview metrics here.",
        )
        root.addWidget(self.empty, 1)

        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(13)

        self.provenance = QFrame()
        self.provenance.setObjectName("SubtleSurface")
        provenance_layout = QVBoxLayout(self.provenance)
        provenance_layout.setContentsMargins(16, 11, 16, 11)
        provenance_layout.setSpacing(3)
        self.provenance_title = QLabel("Stored backend analysis")
        self.provenance_title.setObjectName("SectionTitle")
        self.provenance_detail = QLabel()
        self.provenance_detail.setObjectName("SectionHint")
        self.provenance_detail.setWordWrap(True)
        provenance_layout.addWidget(self.provenance_title)
        provenance_layout.addWidget(self.provenance_detail)
        content_layout.addWidget(self.provenance)

        tabs = QHBoxLayout()
        tabs.setSpacing(8)
        self.learning_button = QPushButton("Compare Learning")
        self.resilience_button = QPushButton("Test Resilience")
        self.tab_group = QButtonGroup(self)
        self.tab_group.setExclusive(True)
        for index, button in enumerate((self.learning_button, self.resilience_button)):
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.tab_group.addButton(button, index)
            tabs.addWidget(button)
        tabs.addStretch(1)
        self.learning_button.setChecked(True)
        self.learning_button.setAccessibleName("Show stored nominal learning results")
        self.resilience_button.setAccessibleName("Show stored matched resilience results")
        self.tab_group.idClicked.connect(self._show_tab)
        self._apply_tab_style(0)
        content_layout.addLayout(tabs)

        self.stack = QStackedWidget()
        self.learning_page = self._build_learning_page()
        self.resilience_page = self._build_resilience_page()
        self.stack.addWidget(self.learning_page)
        self.stack.addWidget(self.resilience_page)
        content_layout.addWidget(self.stack, 1)
        root.addWidget(self.content, 1)

        self.refresh()

    def _build_learning_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(9)
        layout.addWidget(
            SectionHeader(
                "Nominal learning",
            )
        )
        self.learning_guidance = QLabel()
        self.learning_guidance.setObjectName("SectionHint")
        self.learning_guidance.setWordWrap(True)
        layout.addWidget(self.learning_guidance)
        self.learning_chart = StoredIntervalBarChart()
        self.learning_chart.setToolTip(
            "Visual rendering of stored backend means and intervals. The desktop UI does not calculate these values."
        )
        layout.addWidget(self.learning_chart)
        self.learning_table = QTableWidget(0, 6)
        self.learning_table.setObjectName("ResultsTable")
        self.learning_table.setAccessibleName("Stored nominal learning summaries")
        self.learning_table.setHorizontalHeaderLabels(
            ("Method", "Final value", "Stored interval", "Learning average", "Stored interval", "Roots")
        )
        self._configure_table(self.learning_table, stretch_columns=(0,))
        layout.addWidget(self.learning_table, 1)
        return page

    def _build_resilience_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(9)
        layout.addWidget(
            SectionHeader(
                "Matched resilience",
            )
        )
        filter_row = QHBoxLayout()
        filter_label = QLabel("Condition")
        filter_label.setObjectName("ReviewLabel")
        filter_row.addWidget(filter_label)
        self.resilience_condition = QComboBox()
        self.resilience_condition.setMinimumWidth(300)
        self.resilience_condition.setToolTip(
            "Filter the stored chart and table to one uncertainty condition. This does not recompute the analysis."
        )
        self.resilience_condition.setAccessibleName("Resilience condition")
        filter_label.setBuddy(self.resilience_condition)
        self.resilience_condition.currentIndexChanged.connect(self._refresh_resilience_view)
        filter_row.addWidget(self.resilience_condition)
        filter_row.addStretch(1)
        layout.addLayout(filter_row)

        self.resilience_guidance = QLabel()
        self.resilience_guidance.setObjectName("SectionHint")
        self.resilience_guidance.setWordWrap(True)
        layout.addWidget(self.resilience_guidance)

        chart_controls = QHBoxLayout()
        chart_label = QLabel("Chart")
        chart_label.setObjectName("ReviewLabel")
        chart_controls.addWidget(chart_label)
        self.benefit_chart_button = QPushButton("Adaptation benefit")
        self.loss_chart_button = QPushButton("Frozen vs Adaptive losses")
        self.resilience_chart_group = QButtonGroup(self)
        self.resilience_chart_group.setExclusive(True)
        for index, button in enumerate(
            (self.benefit_chart_button, self.loss_chart_button)
        ):
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.resilience_chart_group.addButton(button, index)
            chart_controls.addWidget(button)
        self.benefit_chart_button.setChecked(True)
        self.benefit_chart_button.setAccessibleName("Show matched adaptation benefit chart")
        self.loss_chart_button.setAccessibleName("Show Frozen and Adaptive loss chart")
        self.resilience_chart_group.idClicked.connect(self._show_resilience_chart)
        chart_controls.addStretch(1)
        layout.addLayout(chart_controls)

        self.resilience_chart = StoredIntervalBarChart()
        self.resilience_chart.setToolTip(
            "Primary adaptation effect from the stored matched DiD analysis, with its stored root-level interval."
        )
        self.resilience_loss_chart = StoredIntervalBarChart()
        self.resilience_loss_chart.setToolTip(
            "Supporting stored Frozen and Adaptive disturbance-associated losses. "
            "The desktop UI does not calculate these values."
        )
        self.resilience_chart_stack = QStackedWidget()
        self.resilience_chart_stack.addWidget(self.resilience_chart)
        self.resilience_chart_stack.addWidget(self.resilience_loss_chart)
        layout.addWidget(self.resilience_chart_stack)
        self._apply_resilience_chart_style(0)

        self.resilience_table = QTableWidget(0, 7)
        self.resilience_table.setObjectName("ResultsTable")
        self.resilience_table.setAccessibleName("Stored matched resilience summaries")
        self.resilience_table.setHorizontalHeaderLabels(
            (
                "Method",
                "Condition",
                "Frozen loss",
                "Adaptive loss",
                "Adaptation benefit",
                "Stored interval",
                "Roots",
            )
        )
        self._configure_table(self.resilience_table, stretch_columns=(0, 1))
        layout.addWidget(self.resilience_table, 1)
        return page

    @staticmethod
    def _configure_table(table: QTableWidget, *, stretch_columns: tuple[int, ...]) -> None:
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setShowGrid(False)
        table.setSortingEnabled(False)
        header = table.horizontalHeader()
        for column in range(table.columnCount()):
            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.Stretch
                if column in stretch_columns
                else QHeaderView.ResizeMode.ResizeToContents,
            )

    def refresh(self) -> None:
        previous = self.study_combo.currentData()
        self.error.hide()
        try:
            study_ids = self.read_model.study_ids()
        except Exception as exc:
            study_ids = ()
            self._show_error(exc)

        self.study_combo.blockSignals(True)
        self.study_combo.clear()
        for study_id in study_ids:
            self.study_combo.addItem(study_id, study_id)
        if previous in study_ids:
            self.study_combo.setCurrentIndex(study_ids.index(previous))
        self.study_combo.blockSignals(False)

        has_analysis = bool(study_ids)
        self.selector_surface.setVisible(has_analysis)
        self.empty.setVisible(not has_analysis)
        self.content.setVisible(has_analysis)
        if has_analysis:
            self._load_selected()
        else:
            self.current_package = None
            self.learning_table.setRowCount(0)
            self.resilience_table.setRowCount(0)
            self.learning_chart.set_data(title="Stored nominal summary", bars=())
            self.resilience_chart.set_data(title="Stored adaptation benefit", bars=())
            self.resilience_loss_chart.set_data(title="Stored disturbance losses", bars=())

    def _selection_changed(self, _index: int) -> None:
        self._load_selected()

    def _load_selected(self) -> None:
        study_id = self.study_combo.currentData()
        if not isinstance(study_id, str) or not study_id:
            return
        self.error.hide()
        try:
            package = self.read_model.load(study_id)
        except Exception as exc:
            self.current_package = None
            self.learning_table.setRowCount(0)
            self.resilience_table.setRowCount(0)
            self._show_error(exc)
            return
        self.current_package = package
        self._populate(package)

    def _show_error(self, exc: Exception) -> None:
        self.error.setText(
            "Stored analysis could not be verified and will not be displayed. No state was changed.\n"
            f"Technical detail: {type(exc).__name__}: {exc}"
        )
        self.error.show()

    def _populate(self, package: StoredAnalysisPackage) -> None:
        artifact_short = package.artifact_sha256[:12]
        recipe_short = package.recipe_sha256[:12]
        self.provenance_detail.setText(
            f"{package.analysis_recipe} · artifact SHA-256 {artifact_short}… · "
            f"Study recipe SHA-256 {recipe_short}…\n"
            "Research use: quantitative thesis claims must use registered, versioned "
            "exports—not screenshots of this inspection page."
        )
        self.provenance_detail.setToolTip(
            f"Artifact: {package.artifact_sha256}\nRecipe: {package.recipe_sha256}\n"
            f"Path: {package.relative_path}"
        )
        direction = (
            "Higher values are better"
            if package.phase_a_direction == "higher-is-better"
            else "Lower values are better"
        )
        self.learning_guidance.setText(
            f"Stored metric: {package.phase_a_metric} · {direction}. Read final probe "
            "and interaction-axis time-average as separate outcomes; inspect stored "
            "intervals and included/planned roots before comparing methods."
        )
        self.resilience_guidance.setText(
            "Positive adaptation benefit means continued learning reduced the "
            "disturbance-associated loss relative to its matched nominal reference; "
            "zero means no matched benefit. Inspect Frozen/Adaptive losses and root "
            "denominators before interpreting the effect."
        )
        self._populate_learning(package)
        self._prepare_resilience(package)

    def _method_name(self, method_id: str) -> str:
        return self.method_names.get(method_id, _display_identifier(method_id))

    @staticmethod
    def _item(text: str, *, tooltip: str | None = None) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        if tooltip:
            item.setToolTip(tooltip)
        return item

    def _populate_learning(self, package: StoredAnalysisPackage) -> None:
        self.learning_table.setRowCount(len(package.learning))
        bars: list[StoredBar] = []
        for row, summary in enumerate(package.learning):
            roots = f"{summary.included_root_count} / {summary.planned_root_count}"
            values = (
                self._method_name(summary.method_id),
                _format_number(summary.final_value.mean),
                _format_interval(summary.final_value),
                _format_number(summary.time_average.mean),
                _format_interval(summary.time_average),
                roots,
            )
            for column, value in enumerate(values):
                tooltip = None
                if column == 0:
                    tooltip = f"Backend method_id: {summary.method_id}"
                elif column in {1, 3}:
                    tooltip = (
                        f"Stored metric: {summary.metric}; direction: {summary.direction}. "
                        "No value was recomputed by the desktop UI."
                    )
                self.learning_table.setItem(row, column, self._item(value, tooltip=tooltip))
            if summary.final_value.mean is not None:
                bars.append(
                    StoredBar(
                        key=summary.method_id,
                        label=self._method_name(summary.method_id),
                        value=summary.final_value.mean,
                        lower=summary.final_value.interval_lower,
                        upper=summary.final_value.interval_upper,
                        variant="primary",
                    )
                )
            if summary.time_average.mean is not None:
                bars.append(
                    StoredBar(
                        key=summary.method_id,
                        label=self._method_name(summary.method_id),
                        value=summary.time_average.mean,
                        lower=summary.time_average.interval_lower,
                        upper=summary.time_average.interval_upper,
                        variant="secondary",
                    )
                )
        self.learning_chart.set_data(
            title=f"Stored nominal summary · {package.phase_a_metric}",
            bars=tuple(bars),
            legend=(("Final probe", "primary"), ("Time-average", "secondary")),
        )

    def _prepare_resilience(self, package: StoredAnalysisPackage) -> None:
        conditions: list[str] = []
        for summary in package.resilience:
            if summary.condition_id not in conditions:
                conditions.append(summary.condition_id)

        previous = self.resilience_condition.currentData()
        self.resilience_condition.blockSignals(True)
        self.resilience_condition.clear()
        for condition_id in conditions:
            self.resilience_condition.addItem(
                _CONDITION_NAMES.get(condition_id, _display_identifier(condition_id)),
                condition_id,
            )
        if previous in conditions:
            self.resilience_condition.setCurrentIndex(conditions.index(previous))
        self.resilience_condition.blockSignals(False)
        self._refresh_resilience_view()

    def _refresh_resilience_view(self, _index: int = -1) -> None:
        package = self.current_package
        condition_id = self.resilience_condition.currentData()
        if package is None or not isinstance(condition_id, str):
            self.resilience_table.setRowCount(0)
            self.resilience_chart.set_data(title="Stored adaptation benefit", bars=())
            self.resilience_loss_chart.set_data(title="Stored disturbance losses", bars=())
            return

        summaries = tuple(
            summary
            for summary in package.resilience
            if summary.condition_id == condition_id
        )
        self.resilience_table.setRowCount(len(summaries))
        bars: list[StoredBar] = []
        loss_bars: list[StoredBar] = []
        for row, summary in enumerate(summaries):
            condition = _CONDITION_NAMES.get(
                summary.condition_id,
                _display_identifier(summary.condition_id),
            )
            roots = f"{summary.included_root_count} / {summary.planned_root_count}"
            values = (
                self._method_name(summary.method_id),
                condition,
                _format_number(summary.frozen_loss.mean),
                _format_number(summary.adaptive_loss.mean),
                _format_number(summary.adaptation_benefit.mean),
                _format_interval(summary.adaptation_benefit),
                roots,
            )
            for column, value in enumerate(values):
                tooltip = None
                if column == 0:
                    tooltip = f"Backend method_id: {summary.method_id}"
                elif column == 1:
                    tooltip = f"Backend condition_id: {summary.condition_id}"
                elif column in {2, 3, 4}:
                    tooltip = (
                        f"Stored metric: {summary.metric}; direction: {summary.direction}. "
                        "FN/FD/AN/AD effects were computed by the backend analysis engine."
                    )
                self.resilience_table.setItem(
                    row,
                    column,
                    self._item(value, tooltip=tooltip),
                )
            if summary.adaptation_benefit.mean is not None:
                bars.append(
                    StoredBar(
                        key=summary.method_id,
                        label=self._method_name(summary.method_id),
                        value=summary.adaptation_benefit.mean,
                        lower=summary.adaptation_benefit.interval_lower,
                        upper=summary.adaptation_benefit.interval_upper,
                    )
                )
            if summary.frozen_loss.mean is not None:
                loss_bars.append(
                    StoredBar(
                        key=summary.method_id,
                        label=self._method_name(summary.method_id),
                        value=summary.frozen_loss.mean,
                        lower=summary.frozen_loss.interval_lower,
                        upper=summary.frozen_loss.interval_upper,
                        variant="primary",
                    )
                )
            if summary.adaptive_loss.mean is not None:
                loss_bars.append(
                    StoredBar(
                        key=summary.method_id,
                        label=self._method_name(summary.method_id),
                        value=summary.adaptive_loss.mean,
                        lower=summary.adaptive_loss.interval_lower,
                        upper=summary.adaptive_loss.interval_upper,
                        variant="secondary",
                    )
                )

        condition_name = _CONDITION_NAMES.get(
            condition_id,
            _display_identifier(condition_id),
        )
        self.resilience_chart.set_data(
            title=f"Matched adaptation benefit · {condition_name}",
            bars=tuple(bars),
            zero_label="No matched benefit",
        )
        self.resilience_loss_chart.set_data(
            title=f"Disturbance-associated loss · {condition_name}",
            bars=tuple(loss_bars),
            legend=(("Frozen loss", "primary"), ("Adaptive loss", "secondary")),
        )

    def _apply_resilience_chart_style(self, selected: int) -> None:
        for index, button in enumerate(
            (self.benefit_chart_button, self.loss_chart_button)
        ):
            button.setObjectName(
                "ChartToggleActive" if index == selected else "ChartToggleInactive"
            )
            button.style().unpolish(button)
            button.style().polish(button)

    def _show_resilience_chart(self, index: int) -> None:
        self.resilience_chart_stack.setCurrentIndex(index)
        self._apply_resilience_chart_style(index)

    def _apply_tab_style(self, selected: int) -> None:
        for index, button in enumerate((self.learning_button, self.resilience_button)):
            button.setObjectName("PrimaryButton" if index == selected else "SecondaryButton")
            button.style().unpolish(button)
            button.style().polish(button)

    def _show_tab(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        self._apply_tab_style(index)
