"""RQ-first intended-user Results presentation over validated stored outputs."""
from __future__ import annotations

from dataclasses import replace

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QSizePolicy, QTableWidget, QWidget

from .protocol import FrozenProtocolSummary
from .recovery_chart import RecoveryTrajectoryChart
from .results_page import (
    ResultsPage as _StoredResultsPage,
    _display_identifier,
    _format_bounds,
)
from .results_read_model import DesktopResultsReadModel, StoredAnalysisPackage, StoredMethodContrast


class ResultsWorkspacePage(_StoredResultsPage):
    """Keep stored-output semantics while presenting each comparison inside its RQ."""

    def __init__(
        self,
        model: DesktopResultsReadModel,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        self._context_study_id: str | None = None
        super().__init__(model, protocol, parent)

        root_layout = self.layout()
        if root_layout is not None:
            root_layout.setContentsMargins(32, 22, 36, 28)
            root_layout.setSpacing(11)
        content_layout = self.content.layout()
        if content_layout is not None:
            content_layout.setSpacing(10)

        self.learning_button.setText("RQ1 — Learning")
        self.resilience_button.setText("RQ2 — Resilience / Adaptation")
        self.recovery_button.setText("RQ3 — Recovery")
        self.learning_button.setToolTip("Nominal learning from stored validated Phase-A outputs.")
        self.resilience_button.setToolTip(
            "Matched Frozen/Adaptive disturbance loss and adaptation benefit from stored validated outputs."
        )
        self.recovery_button.setToolTip(
            "AN-vs-AD recovery under the registered 32-interaction window contract; non-recovery remains right-censored."
        )
        self.recovery_view.setItemText(2, "Recovery method contrasts")

        # Charts should dominate their supporting tables on ordinary thesis laptops.
        for chart in (
            self.learning_chart,
            self.resilience_chart,
            self.resilience_loss_chart,
        ):
            chart.setMinimumHeight(215)
            chart.setMaximumHeight(260)
            chart.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred,
            )
        self.learning_table.setMaximumHeight(220)
        self.resilience_table.setMaximumHeight(220)

        replacements = {
            "Nominal learning": "RQ1 — Learning",
            "Matched resilience": "RQ2 — Resilience / Adaptation",
            "Recovery": "RQ3 — Recovery",
            "Analysis Study": "Experiment record",
        }
        for label in self.findChildren(QLabel):
            replacement = replacements.get(label.text())
            if replacement:
                label.setText(replacement)
        self.study_combo.setAccessibleName("Results experiment record")
        self.study_combo.setToolTip(
            "Only experiment records with a registered validated analysis package appear here."
        )

        self.context_notice = QLabel()
        self.context_notice.setObjectName("SectionHint")
        self.context_notice.setWordWrap(True)
        self.context_notice.setAccessibleName("Results context notice")
        self.context_notice.hide()
        if root_layout is not None:
            root_layout.insertWidget(2, self.context_notice)

        self.provenance.setVisible(False)
        self.provenance_toggle = QPushButton("Analysis source / provenance")
        self.provenance_toggle.setObjectName("SecondaryButton")
        self.provenance_toggle.setCheckable(True)
        self.provenance_toggle.setAccessibleName("Show analysis source and provenance")
        self.provenance_toggle.setToolTip(
            "Show the registered analysis recipe and checksums. Research results remain primary."
        )
        self.provenance_toggle.toggled.connect(self.provenance.setVisible)
        if content_layout is not None:
            content_layout.insertWidget(
                0,
                self.provenance_toggle,
                0,
                Qt.AlignmentFlag.AlignLeft,
            )

        self.recovery_chart = RecoveryTrajectoryChart()
        self.recovery_chart.setToolTip(
            "Each line is one stored root-level directed-gap trajectory. The tolerance, "
            "window grid, recovery-time summary and censoring counts come from the "
            "validated backend analysis; the UI performs no root reduction."
        )
        recovery_layout = self.recovery_page.layout()
        if recovery_layout is not None:
            # Section header, guidance and controls remain above the scientific visual.
            recovery_layout.insertWidget(3, self.recovery_chart)
        self.recovery_stack.setMinimumHeight(150)
        self.recovery_stack.setMaximumHeight(220)

        self.learning_contrast_button, self.learning_contrast_table = self._add_contrast_disclosure(
            self.learning_page,
            accessible_name="Show stored RQ1 direct method comparisons",
        )
        self.resilience_contrast_button, self.resilience_contrast_table = self._add_contrast_disclosure(
            self.resilience_page,
            accessible_name="Show stored RQ2 direct method comparisons",
        )
        if self.current_package is not None:
            self._populate_rq_contrasts(self.current_package)
            self._update_recovery_chart()

    def _add_contrast_disclosure(
        self,
        page: QWidget,
        *,
        accessible_name: str,
    ) -> tuple[QPushButton, QTableWidget]:
        button = QPushButton("Direct method comparisons")
        button.setObjectName("SecondaryButton")
        button.setCheckable(True)
        button.setAccessibleName(accessible_name)
        button.setToolTip(
            "Show already-computed root-paired method contrasts for this research question."
        )

        table = QTableWidget(0, 7)
        table.setObjectName("ResultsTable")
        table.setAccessibleName(accessible_name.replace("Show ", ""))
        table.setHorizontalHeaderLabels(
            (
                "Estimand",
                "Condition",
                "Method A",
                "Method B",
                "A − B",
                "Stored interval",
                "Roots",
            )
        )
        self._configure_table(table, stretch_columns=(0, 1))
        table.setMinimumHeight(150)
        table.setMaximumHeight(210)
        table.hide()
        button.toggled.connect(table.setVisible)

        page_layout = page.layout()
        if page_layout is not None:
            page_layout.addWidget(button, 0, Qt.AlignmentFlag.AlignLeft)
            page_layout.addWidget(table)
        return button, table

    def _populate(self, package: StoredAnalysisPackage) -> None:
        super()._populate(package)
        if hasattr(self, "learning_contrast_table"):
            self._populate_rq_contrasts(package)
        if hasattr(self, "recovery_chart"):
            self._update_recovery_chart()

    def _populate_method_contrasts(self, package: StoredAnalysisPackage) -> None:
        """Keep the RQ3 built-in contrast view recovery-specific."""
        recovery_only = tuple(
            row for row in package.method_contrasts if row.source == "recovery"
        )
        super()._populate_method_contrasts(
            replace(package, method_contrasts=recovery_only)
        )

    def _populate_rq_contrasts(self, package: StoredAnalysisPackage) -> None:
        learning = tuple(row for row in package.method_contrasts if row.source == "phase-a")
        resilience = tuple(row for row in package.method_contrasts if row.source == "phase-b")
        self._fill_contrast_table(self.learning_contrast_table, learning)
        self._fill_contrast_table(self.resilience_contrast_table, resilience)
        self.learning_contrast_button.setVisible(bool(learning))
        self.resilience_contrast_button.setVisible(bool(resilience))
        if not learning:
            self.learning_contrast_table.hide()
            self.learning_contrast_button.setChecked(False)
        if not resilience:
            self.resilience_contrast_table.hide()
            self.resilience_contrast_button.setChecked(False)

    def _fill_contrast_table(
        self,
        table: QTableWidget,
        rows: tuple[StoredMethodContrast, ...],
    ) -> None:
        table.setRowCount(len(rows))
        for row_index, contrast in enumerate(rows):
            condition = (
                "—"
                if contrast.condition_id is None
                else _display_identifier(contrast.condition_id)
            )
            values = (
                _display_identifier(contrast.estimand),
                condition,
                self._method_name(contrast.method_a),
                self._method_name(contrast.method_b),
                f"{contrast.mean_difference:.5g}",
                _format_bounds(contrast.interval_lower, contrast.interval_upper),
                str(len(contrast.root_ids)),
            )
            for column, text in enumerate(values):
                tooltip = None
                if column in {4, 5, 6}:
                    tooltip = (
                        "Stored root-paired A-minus-B backend contrast. The desktop UI "
                        "does not reduce roots or calculate this value."
                    )
                table.setItem(
                    row_index,
                    column,
                    self._item(text, tooltip=tooltip),
                )

    def _recovery_condition_changed(self, _index: int = -1) -> None:
        super()._recovery_condition_changed(_index)
        if hasattr(self, "recovery_chart"):
            self._update_recovery_chart()

    def _refresh_recovery_trajectory(self, _index: int = -1) -> None:
        super()._refresh_recovery_trajectory(_index)
        if hasattr(self, "recovery_chart"):
            self._update_recovery_chart()

    def _clear_recovery(self) -> None:
        super()._clear_recovery()
        if hasattr(self, "recovery_chart"):
            self.recovery_chart.clear()

    def _update_recovery_chart(self) -> None:
        package = self.current_package
        recovery = package.recovery if package is not None else None
        condition_id = self.recovery_condition.currentData()
        method_id = self.recovery_method.currentData()
        if recovery is None or not isinstance(condition_id, str) or not isinstance(method_id, str):
            self.recovery_chart.clear()
            return

        points = tuple(
            point
            for point in recovery.trajectories
            if point.condition_id == condition_id and point.method_id == method_id
        )
        summary = next(
            (
                item
                for item in recovery.summaries
                if item.condition_id == condition_id and item.method_id == method_id
            ),
            None,
        )
        if summary is None:
            self.recovery_chart.clear()
            return

        condition = _display_identifier(condition_id)
        self.recovery_chart.set_data(
            title=f"Stored directed-gap recovery trajectories · {self._method_name(method_id)} · {condition}",
            points=points,
            tolerance=recovery.primary_tolerance,
            window_size=recovery.window_size,
            horizon=recovery.observation_horizon,
            recovered_count=summary.recovered_root_count,
            censored_count=summary.right_censored_root_count,
            stored_recovery_time_mean=summary.recovery_time_conditional_on_recovery.mean,
        )

    def set_study(self, study_id: str) -> None:
        """Follow Run context when compatible without pretending unavailable results exist."""
        self._context_study_id = study_id
        self.refresh()
        index = self.study_combo.findData(study_id)
        if index >= 0:
            self.study_combo.setCurrentIndex(index)
            self.context_notice.hide()
            return
        if self.study_combo.count() > 0:
            self.context_notice.setText(
                f"The current Run experiment ({study_id}) has no stored validated analysis yet. "
                "Any results shown below belong to the explicitly selected Experiment record, "
                "not to the current Run experiment."
            )
            self.context_notice.show()
        else:
            self.context_notice.hide()
