# Historical accepted T-528 UI screenshot set

## `pyside6/`

These ten images are the final T-511 accepted visual-review surfaces for the **historical T-528** Python/PySide6 application. They remain useful implementation/QA history but are **not** the layout, navigation or visual-design authority for the clean T-534 rebuild under DEC-061.

They are presentation QA, not scientific evidence. In particular:

- Thesis Study screens read the then-current frozen protocol presentation but do not execute final evidence.
- `06-runs-matched-resilience.png` uses a static DEVELOPMENT presentation fixture; it executes zero environment steps and zero scientific jobs.
- populated Results screenshots use explicitly synthetic in-memory UI fixtures so chart/table layout can be inspected; their metric values are not scientific results.
- the adaptation-benefit and Frozen/Adaptive-loss views are intentionally separate;
- Artifacts provenance uses presentation-only DEVELOPMENT fixture records.

For T-534, useful ideas may be retained after audit, but the new application is experiment-first with primary **Experiment / Run / Results / Evidence** surfaces, a larger Run/GridWorld hierarchy and explicit RQ1/RQ2/RQ3 Results organization. New acceptance screenshots must be generated from DEVELOPMENT/synthetic fixtures after the new structure is implemented; these T-528 images do not satisfy that future acceptance by themselves.

The historical GitHub Actions `T-528 PySide6 UI screenshots` artifact remains the authoritative full QA bundle for the T-528/T-511 baseline and also contains 1366x768 laptop sanity renders. Superseded NiceGUI screenshots remain available through Git history.
