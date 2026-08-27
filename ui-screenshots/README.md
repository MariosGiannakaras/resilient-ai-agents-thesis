# UI Screenshots

Stable accepted screenshots of the Resilient AI Agents thesis application.

## Purpose

These screenshots serve as:

- **User acceptance review** — visual evidence for T-511 intended-user validation.
- **Thesis asset planning** — reference for figures/screenshots in the thesis document.
- **Defense planning** — visual material for presentation slides.
- **Visual regression sanity** — baseline for detecting unintended layout changes.

## Scientific status

> **Screenshots are presentation/review artifacts, not scientific evidence.**
>
> No screenshot in this directory constitutes experimental data, final metrics,
> or scientific results. Any fixture/demo values shown in UI states are clearly
> non-scientific and exist only to render the UI for review purposes.

## Capture source

| Screenshot | Page / State | Capture Source | Notes |
|---|---|---|---|
| `01-dashboard.png` | Dashboard | Browser-CI (Playwright/Chromium headless) | Empty workspace state, real protocol/resource display |
| `02-new-experiment.png` | New Experiment | Browser-CI (Playwright/Chromium headless) | Development stage configurator with strategy selection |
| `03-new-experiment-settings.png` | New Experiment — settings detail | Browser-CI (Playwright/Chromium headless) | Configuration review and tunable settings |
| `04-runs-empty.png` | Runs — empty state | Browser-CI (Playwright/Chromium headless) | No active or historical runs |
| `05-compare-empty.png` | Compare — empty state | Browser-CI (Playwright/Chromium headless) | No stored evidence for comparison |
| `06-artifacts-empty.png` | Artifacts — empty state | Browser-CI (Playwright/Chromium headless) | No thesis artifacts present |
| `07-dashboard-help.png` | Dashboard — Getting Started dialog | Browser-CI (Playwright/Chromium headless) | Onboarding/help overlay |
| `08-experiment-tooltips.png` | New Experiment — tooltips | Browser-CI (Playwright/Chromium headless) | Contextual help and validation |
| `09-sidebar-navigation.png` | Sidebar — scientific state | Browser-CI (Playwright/Chromium headless) | Protocol state and workspace navigation |
| `10-native-desktop.png` | Dashboard | Windows native (pywebview) | Native desktop window, not browser tab |

## Provenance

- **Application version:** NiceGUI 3.16 native/pywebview thesis application.
- **Branch:** `feat/pre-wp7-protocol-v1.1-ui-rebuild`.
- **Task:** T-532 (screenshots, bounded CI capture, Windows packaging).
- **Captured by:** Automated browser-mode capture script (`scripts/capture_screenshots.py`) and manual native-window capture.
- **Protocol/evidence:** No final scientific evidence is shown. Fixture data for UI chrome rendering is clearly labeled as non-scientific.

## File naming convention

Files use zero-padded numeric prefixes for stable ordering:
`{NN}-{page-or-state}.png`

## Updating screenshots

Re-run the capture script after UI changes:
```
uv run python scripts/capture_screenshots.py
```

Native desktop screenshots must be captured manually on the validated Windows thesis machine.
