"""Stable import boundary for the T-528 recipe-first Study flow.

The evolving presentation implementation lives in :mod:`study_flow`; this
module owns small application-lifecycle integrations: deterministic Review
replacement and authorized DEVELOPMENT Study creation.  It never exposes final
reserve execution.
"""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from .exploratory_study import DesktopExploratoryStudyModel
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
    """Study journey plus durable, non-executing DEVELOPMENT creation."""

    study_created = Signal(str)

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        writable_root = kwargs.pop("writable_root", None)
        super().__init__(*args, **kwargs)
        old_review = self.review
        self.stack.removeWidget(old_review)
        old_review.hide()
        old_review.setParent(None)
        old_review.deleteLater()

        self.review = ExploratoryReviewPage(self.preview_model)
        self.stack.insertWidget(self.REVIEW, self.review)
        self.review.back_requested.connect(self.show_customize)
        self.review.create_button.setObjectName("PrimaryButton")
        self.review.create_button.setEnabled(True)
        self.review.create_button.setToolTip(
            "Create the durable DEVELOPMENT Study. Creation does not execute any scientific job."
        )
        self.review.create_button.clicked.connect(self._create_exploratory_study)

        self.study_model = DesktopExploratoryStudyModel(
            repo_root=self.preview_model.repo_root,
            writable_root=(
                Path(writable_root).resolve() if writable_root is not None else None
            ),
        )
        self._created_study_id: str | None = None
        self.show_home()

    def _show_review(self) -> None:
        self._created_study_id = None
        self.review.create_button.setText("Create exploratory study")
        self.review.create_button.setObjectName("PrimaryButton")
        self.review.create_button.setEnabled(True)
        super()._show_review()

    def _create_exploratory_study(self) -> None:
        if self._created_study_id is not None:
            return
        roots, layouts = self.customize.scope()
        self.review.create_button.setEnabled(False)
        self.review.create_button.setText("Creating…")
        try:
            created = self.study_model.create(
                selected_method_ids=self._selected_method_ids,
                root_count=roots,
                layout_count=layouts,
                study_label=self.customize.study_label.text().strip(),
            )
        except Exception as exc:  # UI boundary translates backend failure to a safe state.
            self.review.create_button.setText("Create exploratory study")
            self.review.create_button.setEnabled(True)
            self.review.detail.setText(
                "The DEVELOPMENT study was not created. No job was executed. "
                f"Technical detail: {type(exc).__name__}: {exc}"
            )
            return

        self._created_study_id = created.study_id
        self.review.create_button.setText("Study created")
        self.review.create_button.setEnabled(False)
        self.review.detail.setText(
            f"Created DEVELOPMENT study {created.study_id} with {created.total_jobs} planned jobs. "
            "No scientific job has executed. Open Runs from the sidebar to inspect durable state before starting work."
        )
        self.study_created.emit(created.study_id)


__all__ = [
    "ExploratoryCustomizePage",
    "ExploratoryModelsPage",
    "ExploratoryReviewPage",
    "StudyChooserPage",
    "StudyWorkspacePage",
]
