from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PYSIDE6_AVAILABLE = importlib.util.find_spec("PySide6") is not None

if PYSIDE6_AVAILABLE:
    from resilient_agents.desktop.app import create_application
    from resilient_agents.desktop.protocol import load_frozen_protocol
    from resilient_agents.desktop.study_workspace import StudyWorkspacePage


REPO_ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(PYSIDE6_AVAILABLE, "PySide6 is an application-only T-528 dependency")
class StudyWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_application([])
        cls.protocol = load_frozen_protocol(REPO_ROOT)

    def setUp(self) -> None:
        self.page = StudyWorkspacePage(self.protocol, repo_root=REPO_ROOT)
        self.page.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        self.page.close()
        self.app.processEvents()

    def test_routes_across_full_exploratory_review_journey(self) -> None:
        self.assertEqual(self.page.current_view, "choose")
        self.page.show_thesis()
        self.assertEqual(self.page.current_view, "thesis")
        self.page.show_exploratory()
        self.assertEqual(self.page.current_view, "exploratory")
        self.page.show_customize()
        self.assertEqual(self.page.current_view, "customize")
        self.page._show_review()
        self.assertEqual(self.page.current_view, "review")
        self.page.show_home()
        self.assertEqual(self.page.current_view, "choose")

    def test_exploratory_models_project_only_retained_implementations(self) -> None:
        expected = tuple(method.method_id for method in self.protocol.methods)
        self.assertEqual(self.page.models.selected_method_ids(), expected)
        self.assertTrue(self.page.models.continue_button.isEnabled())

        for card in self.page.models.model_cards:
            card.check.setChecked(False)
        self.app.processEvents()
        self.assertEqual(self.page.models.selected_method_ids(), ())
        self.assertFalse(self.page.models.continue_button.isEnabled())

    def test_exploratory_primary_action_fits_laptop_viewport(self) -> None:
        # The application shell leaves 1066x704 for page content at 1366x768.
        self.page.resize(1066, 704)
        self.page.show_exploratory()
        self.app.processEvents()

        models = self.page.models
        viewport = models.scroll.viewport()
        button_bottom = models.continue_button.mapTo(
            viewport,
            models.continue_button.rect().bottomRight(),
        ).y()
        self.assertLessEqual(button_bottom, viewport.rect().bottom() - 12)

    def test_review_is_backend_resolved_and_creation_is_separate_from_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = StudyWorkspacePage(
                self.protocol,
                repo_root=REPO_ROOT,
                writable_root=Path(directory),
            )
            page.show()
            page.show_exploratory()
            page.show_customize()
            page.customize.root_count.setCurrentIndex(1)
            page.customize.layout_count.setCurrentIndex(1)
            page._show_review()
            self.app.processEvents()
            self.assertTrue(page.review.create_button.isEnabled())
            self.assertIn("Final-reserve execution remains unauthorized", page.review.detail.text())

            page.review.create_button.click()
            self.app.processEvents()
            self.assertIsNotNone(page._created_study_id)
            study_dir = Path(directory) / "results" / "studies" / str(page._created_study_id)
            self.assertTrue((study_dir / "recipe.json").is_file())
            self.assertFalse((Path(directory) / "results" / "runs").exists())
            self.assertIn("No scientific job has executed", page.review.detail.text())
            page.close()

    def test_repeated_review_replaces_summary_without_accumulating_widgets(self) -> None:
        self.page.show_customize()
        self.page._show_review()
        first_count = self.page.review.summary_grid.count()
        self.page.show_customize()
        self.page._show_review()
        self.app.processEvents()
        self.assertEqual(self.page.review.summary_grid.count(), first_count)

    def test_thesis_back_and_help_are_progressively_disclosed(self) -> None:
        self.page.show_thesis()
        self.app.processEvents()
        self.assertTrue(self.page.thesis.show_back)
        self.assertFalse(self.page.thesis.help_detail.isVisible())
        self.page.thesis.help_button.setChecked(True)
        self.app.processEvents()
        self.assertTrue(self.page.thesis.help_detail.isVisible())


if __name__ == "__main__":
    unittest.main()
