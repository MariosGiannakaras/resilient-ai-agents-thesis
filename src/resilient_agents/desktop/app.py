"""Desktop application entry point."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from . import APP_NAME
from .main_window import MainWindow
from .theme import application_stylesheet

_PROTOCOL_FILE = Path("configs/protocols/protocol-v2.1-final.json")


def find_repo_root(start: Path | None = None) -> Path:
    override = os.environ.get("RESILIENT_AGENTS_REPO_ROOT")
    if override:
        root = Path(override).expanduser().resolve()
        if (root / _PROTOCOL_FILE).is_file():
            return root
        raise RuntimeError("RESILIENT_AGENTS_REPO_ROOT does not contain protocol-v2.1-final.json")

    origin = (start or Path.cwd()).resolve()
    candidates = (origin, *origin.parents, Path(__file__).resolve().parents[3])
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / _PROTOCOL_FILE).is_file():
            return candidate
    raise RuntimeError(
        "cannot locate repository root; run from the thesis repository or set RESILIENT_AGENTS_REPO_ROOT"
    )


def create_application(argv: list[str] | None = None) -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication(argv if argv is not None else sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("THESIS")
    app.setStyle("Fusion")
    app.setStyleSheet(application_stylesheet())
    return app


def run() -> int:
    app = create_application()
    window = MainWindow(repo_root=find_repo_root())
    window.show()
    return app.exec()
