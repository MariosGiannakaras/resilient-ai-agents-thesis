"""Stable import boundary for the T-528 recipe-first Study flow.

The evolving implementation lives in :mod:`study_flow`; this module also owns a
small Qt lifecycle hardening layer so repeat Review visits detach old summary
widgets immediately rather than relying on deferred deletion.
"""
from __future__ import annotations

from .study_flow import (
    ExploratoryCustomizePage,
    ExploratoryModelsPage,
    ExploratoryReviewPage as _ExploratoryReviewPage,
    StudyChooserPage,
    StudyWorkspacePage as _StudyWorkspacePage,
)


class ExploratoryReviewPage(_ExploratoryReviewPage):
    """Review surface with deterministic immediate summary replacement."""

    def show_preview(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        # Qt deleteLater() alone can leave old labels paintable until the event
        # loop reaches deferred-delete events. Detach them first so repeated
        # Review visits and deterministic screenshot passes cannot overlap text.
        while self.summary_grid.count():
            item = self.summary_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.hide()
                widget.setParent(None)
                widget.deleteLater()
        super().show_preview(**kwargs)


class StudyWorkspacePage(_StudyWorkspacePage):
    """Use the hardened Review surface without changing scientific services."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        old_review = self.review
        self.stack.removeWidget(old_review)
        old_review.hide()
        old_review.setParent(None)
        old_review.deleteLater()

        self.review = ExploratoryReviewPage(self.preview_model)
        self.stack.insertWidget(self.REVIEW, self.review)
        self.review.back_requested.connect(self.show_customize)
        self.show_home()


__all__ = [
    "ExploratoryCustomizePage",
    "ExploratoryModelsPage",
    "ExploratoryReviewPage",
    "StudyChooserPage",
    "StudyWorkspacePage",
]
