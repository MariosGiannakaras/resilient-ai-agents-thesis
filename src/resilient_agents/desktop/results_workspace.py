"""RQ-first active Results presentation over the validated stored-output reader."""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QWidget

from .protocol import FrozenProtocolSummary
from .results_page import ResultsPage as _StoredResultsPage
from .results_read_model import DesktopResultsReadModel


class ResultsWorkspacePage(_StoredResultsPage):
    """Keep proven stored-output/chart behavior while making the RQs explicit."""

    def __init__(
        self,
        model: DesktopResultsReadModel,
        protocol: FrozenProtocolSummary,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(model, protocol, parent)
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
        replacements = {
            "Nominal learning": "RQ1 — Learning",
            "Matched resilience": "RQ2 — Resilience / Adaptation",
            "Recovery": "RQ3 — Recovery",
        }
        for label in self.findChildren(QLabel):
            replacement = replacements.get(label.text())
            if replacement:
                label.setText(replacement)
