# Dashboard application

The dashboard is intentionally a thin presentation/control layer over `src/resilient_agents/`.

The research core, experiment lifecycle, metrics, storage, provenance, and Git publication must work without the UI. The planned final implementation is a bounded local Streamlit dashboard unless pilots establish a concrete reason to choose another UI stack.

Dashboard implementation remains gated behind a validated headless core and real pilot workflow. A lightweight debug view may be added earlier, but it must call the same core APIs and must not duplicate scientific logic.

The final dashboard must be self-explanatory rather than merely visually polished. Use clear labels/helper text, visible units, concise tooltips and contextual explanations for non-obvious scientific/technical concepts, consistent status text/icons/semantic colors, actionable empty/warning/error states, and pre-run configuration validation/summary. Color must never be the only carrier of essential meaning.

After the final dashboard structure is stable, add a lightweight first-run onboarding/tutorial covering the essential workflow with Previous/Next/Skip/Finish controls and a replay option under Help/Getting Started. Prefer native Streamlit/lightweight state/dialog/popover primitives and a local completion flag; do not introduce a heavyweight custom JavaScript/DOM tour framework without a separately demonstrated need.
