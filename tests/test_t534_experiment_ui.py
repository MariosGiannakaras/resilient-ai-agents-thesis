from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6.QtWidgets import QApplication
except ImportError:  # application overlay is intentionally optional for core-only installs
    QApplication = None  # type: ignore[assignment]

REPO_ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(QApplication is None, "PySide6 application overlay is not installed")
class T534ExperimentUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        assert QApplication is not None
        cls.app = QApplication.instance() or QApplication([])

    def test_thesis_mode_has_fixed_five_methods_and_no_method_checkboxes(self) -> None:
        from PySide6.QtWidgets import QCheckBox
        from resilient_agents.desktop.experiment_page import ExperimentPage
        from resilient_agents.desktop.protocol import load_frozen_protocol

        with tempfile.TemporaryDirectory() as directory:
            page = ExperimentPage(
                load_frozen_protocol(REPO_ROOT),
                repo_root=REPO_ROOT,
                writable_root=Path(directory),
            )
            page.set_mode(page.THESIS)
            self.assertEqual(len(page.protocol.methods), 5)
            self.assertEqual(page.stack.currentWidget().findChildren(QCheckBox), [])
            text = " ".join(label.text() for label in page.stack.currentWidget().findChildren(__import__("PySide6.QtWidgets", fromlist=["QLabel"]).QLabel))
            for name in ("Q-Learning", "SARSA", "DQN", "PPO", "Dyna-Q+"):
                self.assertIn(name, text)
            self.assertIn("Frozen", text)
            self.assertIn("Adaptive", text)

    def test_development_selection_is_rejected_when_empty_by_backend_preview(self) -> None:
        from resilient_agents.desktop.experiment_page import ExperimentPage
        from resilient_agents.desktop.protocol import load_frozen_protocol

        with tempfile.TemporaryDirectory() as directory:
            page = ExperimentPage(
                load_frozen_protocol(REPO_ROOT),
                repo_root=REPO_ROOT,
                writable_root=Path(directory),
            )
            page.set_mode(page.DEVELOPMENT)
            for check in page.method_checks.values():
                check.setChecked(False)
            page.review_development()
            self.assertTrue(page.configure_error.isVisibleTo(page))
            self.assertIsNone(page._preview)

    def test_main_window_primary_navigation_is_exactly_four_experiment_first_destinations(self) -> None:
        from resilient_agents.desktop.main_window import MainWindow

        with tempfile.TemporaryDirectory() as directory:
            window = MainWindow(repo_root=REPO_ROOT, writable_root=Path(directory))
            self.assertEqual([button.text() for button in window.nav_buttons], [
                "Experiment", "Run", "Results", "Evidence"
            ])
            self.assertIn("protocol-v2.1", window.statusBar().currentMessage() if window.statusBar() else "protocol-v2.1")


if __name__ == "__main__":
    unittest.main()
