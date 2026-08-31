from __future__ import annotations

import importlib.util
import os
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
        self.page = StudyWorkspacePage(self.protocol)
        self.page.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        self.page.close()
        self.app.processEvents()

    def test_starts_at_choose_study_and_routes_between_subviews(self) -> None:
        self.assertEqual(self.page.current_view, "choose")
        self.page.show_thesis()
        self.assertEqual(self.page.current_view, "thesis")
        self.page.show_exploratory()
        self.assertEqual(self.page.current_view, "exploratory")
        self.page.show_home()
        self.assertEqual(self.page.current_view, "choose")

    def test_exploratory_models_project_only_retained_implementations(self) -> None:
        expected = tuple(method.method_id for method in self.protocol.methods)
        self.assertEqual(self.page.exploratory.selected_method_ids(), expected)
        self.assertTrue(self.page.exploratory.continue_button.isEnabled())

        for card in self.page.exploratory.model_cards:
            card.check.setChecked(False)
        self.app.processEvents()
        self.assertEqual(self.page.exploratory.selected_method_ids(), ())
        self.assertFalse(self.page.exploratory.continue_button.isEnabled())

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
