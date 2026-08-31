# UI screenshot review sets

## `pyside6/` — current T-528 application review set

These images are the accepted visual-review surfaces for the Python/PySide6
application built by **T-528 — Final Application / Frontend Rebuild**.

They are presentation QA, not scientific evidence. In particular:

- Thesis Study screens read the frozen protocol contract but do not execute it.
- `06-runs-matched-resilience.png` uses a static DEVELOPMENT presentation fixture;
  it executes zero environment steps and zero scientific jobs.
- populated Results screenshots use explicitly synthetic in-memory UI fixtures so
  chart/table layout can be inspected; their metric values are not scientific results.
- Artifacts provenance uses presentation-only DEVELOPMENT fixture records.

The GitHub Actions `T-528 PySide6 UI screenshots` artifact is the authoritative
full QA bundle and also contains 1366x768 laptop sanity renders plus the accepted
historical visual references used for side-by-side comparison.

## `historical-nicegui/` — historical prototype only

These PNGs preserve the earlier NiceGUI/prototype visual history. They are not the
current frontend and must not be used to claim current T-528 acceptance. They remain
as visual references/history only.
