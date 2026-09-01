from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class T534LauncherTests(unittest.TestCase):
    def test_root_launcher_targets_locked_pyside6_desktop_entrypoint(self) -> None:
        launcher = (REPO_ROOT / "run_app.bat").read_text(encoding="utf-8")
        lowered = launcher.lower()
        self.assertIn("uv sync --locked --group gridworld-prototype", lowered)
        self.assertIn("requirements\\application-ui.txt", lowered)
        self.assertIn("uv run --no-sync python -m resilient_agents.desktop", lowered)
        self.assertIn("set \"repo_root=%~dp0\"", lowered)
        self.assertIn("where uv", lowered)
        self.assertNotIn("streamlit", lowered)
        self.assertNotIn("nicegui", lowered)
        self.assertNotIn("protocol-v2.0", lowered)

    def test_pyside6_entrypoint_and_overlay_are_present(self) -> None:
        entrypoint = (REPO_ROOT / "src" / "resilient_agents" / "desktop" / "__main__.py")
        overlay = REPO_ROOT / "requirements" / "application-ui.txt"
        self.assertTrue(entrypoint.is_file())
        self.assertTrue(overlay.is_file())
        text = overlay.read_text(encoding="utf-8")
        self.assertIn("PySide6==", text)
        self.assertIn("T-534", text)


if __name__ == "__main__":
    unittest.main()
