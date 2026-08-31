"""Compatibility import for the T-528 recipe-first Study flow.

The implementation lives in :mod:`study_flow` so the entry journey can evolve
without making the historical module name part of the scientific backend.
"""

from .study_flow import (
    ExploratoryCustomizePage,
    ExploratoryModelsPage,
    ExploratoryReviewPage,
    StudyChooserPage,
    StudyWorkspacePage,
)

__all__ = [
    "ExploratoryCustomizePage",
    "ExploratoryModelsPage",
    "ExploratoryReviewPage",
    "StudyChooserPage",
    "StudyWorkspacePage",
]
