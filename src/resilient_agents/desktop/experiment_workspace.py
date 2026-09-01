"""Final visual polish for the accepted Experiment workflow."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QSizePolicy, QWidget

from .experiment_page import ExperimentPage as _ExperimentPage
from .protocol import FrozenProtocolSummary


class ExperimentPage(_ExperimentPage):
    """Keep Experiment semantics unchanged while using sparse review space better."""

    def __init__(
        self,
        protocol: FrozenProtocolSummary,
        *,
        repo_root: Path,
        writable_root: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            protocol,
            repo_root=repo_root,
            writable_root=writable_root,
            parent=parent,
        )
        root = self.layout()
        if root is not None:
            root.setContentsMargins(32, 22, 36, 28)
            root.setSpacing(12)

        self.review_surface.setMinimumHeight(178)
        self.review_surface.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self.review_detail.setMinimumHeight(48)
        self.review_secondary.setMinimumHeight(48)
