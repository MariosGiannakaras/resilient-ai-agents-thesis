# Final accepted UI screenshot set

## `pyside6/`

These ten images are the final T-511 accepted visual-review surfaces for the
Python/PySide6 application built by T-528 and hardened for research presentation.

They are presentation QA, not scientific evidence. In particular:

- Thesis Study screens read the frozen protocol contract but do not execute it.
- `06-runs-matched-resilience.png` uses a static DEVELOPMENT presentation fixture;
  it executes zero environment steps and zero scientific jobs.
- populated Results screenshots use explicitly synthetic in-memory UI fixtures so
  chart/table layout can be inspected; their metric values are not scientific results.
- the adaptation-benefit and Frozen/Adaptive-loss views are intentionally separate;
- Artifacts provenance uses presentation-only DEVELOPMENT fixture records.

The GitHub Actions `T-528 PySide6 UI screenshots` artifact is the authoritative
full QA bundle and also contains 1366x768 laptop sanity renders. Superseded NiceGUI
screenshots were removed from the active tree after T-511 acceptance; Git history
retains their audit trail.
