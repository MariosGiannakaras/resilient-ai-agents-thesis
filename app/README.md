# Dashboard application

The dashboard is intentionally a thin presentation/control layer over `src/resilient_agents/`.

The research core, experiment lifecycle, metrics, storage, provenance, and Git publication must work without the UI. The planned final implementation is a bounded local Streamlit dashboard unless pilots establish a concrete reason to choose another UI stack.

Dashboard implementation remains gated behind a validated headless core and real pilot workflow. A lightweight debug view may be added earlier, but it must call the same core APIs and must not duplicate scientific logic.
