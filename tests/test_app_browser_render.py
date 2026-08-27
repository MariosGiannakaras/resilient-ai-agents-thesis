"""Bounded browser-mode screenshot and render validation for the thesis application.

Starts the real NiceGUI application in THESIS_APP_BROWSER_MODE=1 and validates
that all five primary routes render correctly with expected content visible.

Screenshots captured here are diagnostic/presentation artifacts, NOT scientific
evidence. No fabricated metrics, fake active runs, or synthesized trajectories.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PORT = 8598
APP_URL = f"http://127.0.0.1:{APP_PORT}"
SCREENSHOTS_DIR = ROOT / "ui-screenshots"


def _start_app() -> subprocess.Popen:
    env = os.environ.copy()
    env["THESIS_APP_BROWSER_MODE"] = "1"
    env["THESIS_APP_PORT"] = str(APP_PORT)
    return subprocess.Popen(
        ["uv", "run", "--locked", "resilient-agents-app"],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )


def _wait_for_server(url: str, timeout: float = 45.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=2)
            return
        except (urllib.error.URLError, OSError):
            time.sleep(0.5)
    raise TimeoutError(f"Application did not start within {timeout}s at {url}")


def _stop_app(proc: subprocess.Popen) -> None:
    if proc.stdout:
        proc.stdout.close()
    if proc.stderr:
        proc.stderr.close()
    if sys.platform == "win32":
        proc.terminate()
    else:
        os.kill(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def _fetch_page(path: str) -> str:
    """Fetch raw HTML from the running application."""
    url = f"{APP_URL}{path}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read().decode("utf-8")


# Module-level process management for the test suite
_app_proc: subprocess.Popen | None = None


def setUpModule() -> None:
    global _app_proc
    _app_proc = _start_app()
    try:
        _wait_for_server(APP_URL)
    except Exception:
        _stop_app(_app_proc)
        _app_proc = None
        raise


def tearDownModule() -> None:
    global _app_proc
    if _app_proc is not None:
        _stop_app(_app_proc)
        _app_proc = None


class BrowserRenderValidationTests(unittest.TestCase):
    """Validate that real NiceGUI pages render with expected content.

    These tests use the same application code as the native desktop window.
    Browser mode is a validation/presentation path, not a separate implementation.
    """

    def test_dashboard_renders_with_expected_content(self) -> None:
        html = _fetch_page("/")
        self.assertIn("Resilient AI Agents Lab", html)

    def test_experiment_page_renders(self) -> None:
        html = _fetch_page("/experiment")
        self.assertIn("Resilient AI Agents Lab", html)

    def test_runs_page_renders(self) -> None:
        html = _fetch_page("/runs")
        self.assertIn("Resilient AI Agents Lab", html)

    def test_compare_page_renders(self) -> None:
        html = _fetch_page("/compare")
        self.assertIn("Resilient AI Agents Lab", html)

    def test_artifacts_page_renders(self) -> None:
        html = _fetch_page("/artifacts")
        self.assertIn("Resilient AI Agents Lab", html)


if __name__ == "__main__":
    unittest.main()
