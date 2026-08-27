"""Deterministic browser-mode screenshot capture for the thesis application.

Starts the NiceGUI application in browser mode (THESIS_APP_BROWSER_MODE=1),
navigates to each primary route and selected UI states, and saves screenshots
to ui-screenshots/.

Screenshots are presentation/review artifacts, NOT scientific evidence.
Fixture/demo values rendered by the UI are clearly non-scientific.
No fabricated final metrics, fake active runs, or synthesized trajectories.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = REPO_ROOT / "ui-screenshots"
APP_PORT = 8599  # Avoid collisions with default ports
APP_URL = f"http://127.0.0.1:{APP_PORT}"

# Viewport matching the native desktop window size
VIEWPORT = {"width": 1480, "height": 920}

# Pages to capture — (filename, path, wait_seconds, description)
CAPTURES: list[tuple[str, str, float, str]] = [
    ("01-dashboard.png", "/", 3.0, "Dashboard overview"),
    ("02-new-experiment.png", "/experiment", 3.0, "New Experiment configurator"),
    ("04-runs-empty.png", "/runs", 2.5, "Runs workspace — empty state"),
    ("05-compare-empty.png", "/compare", 2.5, "Compare — no stored evidence"),
    ("06-artifacts-empty.png", "/artifacts", 2.5, "Artifacts — empty state"),
]


def start_app() -> subprocess.Popen:
    """Launch the application in browser mode via the locked uv environment."""
    env = os.environ.copy()
    env["THESIS_APP_BROWSER_MODE"] = "1"
    env["THESIS_APP_PORT"] = str(APP_PORT)
    proc = subprocess.Popen(
        ["uv", "run", "--locked", "resilient-agents-app"],
        cwd=str(REPO_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )
    return proc


def wait_for_server(url: str, timeout: float = 30.0) -> None:
    """Wait until the application responds to HTTP requests."""
    import urllib.request
    import urllib.error

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=2)
            return
        except (urllib.error.URLError, OSError):
            time.sleep(0.5)
    raise TimeoutError(f"Application did not start within {timeout}s at {url}")


def capture_screenshots() -> list[dict]:
    """Capture all defined screenshots and return manifest entries."""
    # Import playwright here so the script fails fast if not installed
    from playwright.sync_api import sync_playwright

    manifest = []
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
        )
        page = context.new_page()

        for filename, path, wait_ms, description in CAPTURES:
            target = SCREENSHOTS_DIR / filename
            url = f"{APP_URL}{path}"
            print(f"  Capturing {filename} <- {url}")
            page.goto(url, wait_until="networkidle")
            # Allow NiceGUI/Quasar rendering to settle
            page.wait_for_timeout(int(wait_ms * 1000))
            page.screenshot(path=str(target), full_page=False)
            manifest.append({
                "filename": filename,
                "page": path,
                "state": description,
                "capture_source": "browser-ci-playwright-chromium-headless",
                "scientific_evidence": False,
                "purpose": "presentation-review",
            })
            print(f"    -> saved {target.relative_to(REPO_ROOT)}")

        # Capture additional UI states

        # 03: New Experiment with expanded settings
        print("  Capturing 03-new-experiment-settings.png <- /experiment (expanded)")
        page.goto(f"{APP_URL}/experiment", wait_until="networkidle")
        page.wait_for_timeout(2000)
        # Try to expand the "What is the difference..." section
        expansions = page.locator("text=What is the difference")
        if expansions.count() > 0:
            expansions.first.click()
            page.wait_for_timeout(800)
        page.screenshot(
            path=str(SCREENSHOTS_DIR / "03-new-experiment-settings.png"),
            full_page=False,
        )
        manifest.append({
            "filename": "03-new-experiment-settings.png",
            "page": "/experiment",
            "state": "New Experiment — expanded help/settings",
            "capture_source": "browser-ci-playwright-chromium-headless",
            "scientific_evidence": False,
            "purpose": "presentation-review",
        })

        # 07: Dashboard with Getting Started dialog
        print("  Capturing 07-dashboard-help.png <- / (Getting Started)")
        page.goto(f"{APP_URL}/", wait_until="networkidle")
        page.wait_for_timeout(2000)
        help_btn = page.locator("text=Getting started")
        if help_btn.count() > 0:
            help_btn.first.click()
            page.wait_for_timeout(1500)
        page.screenshot(
            path=str(SCREENSHOTS_DIR / "07-dashboard-help.png"),
            full_page=False,
        )
        manifest.append({
            "filename": "07-dashboard-help.png",
            "page": "/",
            "state": "Dashboard — Getting Started dialog",
            "capture_source": "browser-ci-playwright-chromium-headless",
            "scientific_evidence": False,
            "purpose": "presentation-review",
        })

        # 08: Experiment with tooltip visible
        print("  Capturing 08-experiment-tooltips.png <- /experiment (tooltip)")
        page.goto(f"{APP_URL}/experiment", wait_until="networkidle")
        page.wait_for_timeout(2000)
        # Hover over the Stage selector to show its tooltip
        stage_field = page.locator("label:has-text('Stage')")
        if stage_field.count() > 0:
            stage_field.first.hover()
            page.wait_for_timeout(1000)
        page.screenshot(
            path=str(SCREENSHOTS_DIR / "08-experiment-tooltips.png"),
            full_page=False,
        )
        manifest.append({
            "filename": "08-experiment-tooltips.png",
            "page": "/experiment",
            "state": "New Experiment — tooltip/hover state",
            "capture_source": "browser-ci-playwright-chromium-headless",
            "scientific_evidence": False,
            "purpose": "presentation-review",
        })

        # 09: Dashboard showing the sidebar navigation and scientific state
        print("  Capturing 09-sidebar-navigation.png <- / (sidebar)")
        page.goto(f"{APP_URL}/", wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.screenshot(
            path=str(SCREENSHOTS_DIR / "09-sidebar-navigation.png"),
            full_page=False,
        )
        manifest.append({
            "filename": "09-sidebar-navigation.png",
            "page": "/",
            "state": "Sidebar — workspace navigation and scientific state",
            "capture_source": "browser-ci-playwright-chromium-headless",
            "scientific_evidence": False,
            "purpose": "presentation-review",
        })

        browser.close()

    return manifest


def write_manifest(entries: list[dict]) -> None:
    """Write the screenshot manifest JSON."""
    manifest_path = SCREENSHOTS_DIR / "manifest.json"
    manifest = {
        "description": "UI screenshot manifest for the Resilient AI Agents thesis application.",
        "scientific_evidence": False,
        "note": "All screenshots are presentation/review artifacts. No screenshot is scientific evidence.",
        "capture_branch": "feat/pre-wp7-protocol-v1.1-ui-rebuild",
        "task": "T-532",
        "screenshots": sorted(entries, key=lambda e: e["filename"]),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"  Manifest written to {manifest_path.relative_to(REPO_ROOT)}")


def main() -> None:
    print("=== Thesis Application Screenshot Capture ===")
    print(f"  Output: {SCREENSHOTS_DIR}")
    print(f"  App URL: {APP_URL}")

    print("\n1. Starting application in browser mode...")
    app_proc = start_app()
    try:
        print("2. Waiting for application to be ready...")
        wait_for_server(APP_URL)
        print("   Application is ready.")

        print("\n3. Capturing screenshots...")
        entries = capture_screenshots()
        print(f"\n4. Captured {len(entries)} screenshots.")

        write_manifest(entries)
        print("\nDone.")

    finally:
        print("\n5. Stopping application...")
        if sys.platform == "win32":
            app_proc.terminate()
        else:
            os.kill(app_proc.pid, signal.SIGTERM)
        try:
            app_proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            app_proc.kill()
            app_proc.wait()
        print("   Application stopped.")


if __name__ == "__main__":
    main()
