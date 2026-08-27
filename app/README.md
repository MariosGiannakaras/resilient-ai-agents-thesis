# Local thesis application

The application is the local execution, monitoring, analysis, and presentation surface for the validated headless research core. It is not a second implementation of the scientific logic.

## Architecture

`DEC-044` supersedes the temporary React/Vite choice in `DEC-043` after the final standalone-delivery requirement was clarified. The target stack is:

```text
NiceGUI 3.16 native desktop window (pywebview)
        │
        ├── ordinary NiceGUI/Quasar UI
        ├── Plotly scientific figures
        ├── ECharts live telemetry
        ├── Mermaid model/experiment infographics
        └── AG Grid Community analytical tables
        │
Python application/runtime services
        │
existing src/resilient_agents headless core
        │
filesystem run bundles / artifacts / provenance
```

The historical Streamlit dashboard and the short-lived React/Vite prototype remain in Git history only; they are not active application stacks.

### Boundary rules

- Scientific configuration, agent/environment execution, metrics, result persistence, provenance, and protocol validation stay in Python under `src/resilient_agents/`.
- NiceGUI calls Python application/runtime services; it never reimplements the runner.
- The UI receives only truthful backend-derived state. No mock final metrics, fabricated progress/logs, or invented historical replay.
- Live GridWorld data is read-only observer state. Animation/interpolation and visualization speed never affect experiment timing, actions, seeds, or RNG streams.
- Historical finalized runs without retained step traces show replay unavailable.
- Lifecycle controls are capability-based. Unsupported pause/resume/stop/cancel/restart operations are shown as unsupported rather than simulated.

## Visual analytics

`DEC-045` assigns a specific role to each built-in visualization surface:

- **Plotly:** thesis/presentation-ready stored analysis figures, distributions, uncertainty, paired effects and comparison plots.
- **ECharts:** high-frequency live/provisional run telemetry and multi-agent overlays.
- **Mermaid:** F0/C0/D0 and experiment-flow infographics.
- **AG Grid Community:** run history, comparison selection and detailed result/artifact tables.

Live/provisional telemetry, finalized individual runs, and versioned analysis/evidence are separate visual data classes. A live chart is never silently promoted into thesis evidence.

## User information architecture

The primary navigation remains intentionally small:

1. **Dashboard** — active/recent runs, warnings, protocol state, current resources, quick actions.
2. **New Experiment** — agent explanations, validated configuration, layouts/conditions/seeds, resolved-config review, launch.
3. **Runs** — active/history/detail workspace, live GridWorld, event timeline, logs/metrics, truthful lifecycle state and compatible live comparisons.
4. **Compare** — compatible run/model comparisons, distributions, paired effects/CIs, counts and condition/layout breakdowns.
5. **Artifacts** — real figures/tables/CSV/JSON/HTML outputs, provenance and exports.

The UI must remain self-explanatory through precise labels, units, contextual help/tooltips, semantic text+icon statuses, accessible colors, actionable empty/loading/error/disabled states, and lightweight onboarding.

## Running from the repository

Root `run_app.bat` is the supported development/repository launcher. It runs the locked Python environment and starts the application in a **native desktop window**, not a browser tab.

For deterministic CI/browser rendering only, set `THESIS_APP_BROWSER_MODE=1`; this runs the same NiceGUI pages on localhost without opening a browser automatically. Browser mode is a validation/presentation path, not a separate application implementation.

No Node/npm/Vite installation is required by the active application architecture.

## Final standalone distribution target

The thesis submission should include a cleaned Windows application directory produced from the accepted branch after user E2E validation. The intended packaging path is NiceGUI/PyInstaller `onedir` + `windowed`, validated on the target Windows machine. The folder should contain the executable/runtime plus the explicitly packaged read-only protocols/evidence and writable application-data locations required for local runs.

The final packaged application must:

- open its own window without a browser or visible terminal;
- not require the recipient to install Python or Node;
- keep mutable run/output data outside temporary PyInstaller extraction internals;
- include only required application/runtime/evidence assets;
- pass native-window, close/restart, live-run, Plotly, download and deterministic-observer validation.

## Repository layout

- `src/app/` — NiceGUI pages, presentation components, read models and visualization builders.
- `src/resilient_agents/` — headless scientific/runtime core and application-facing services.
- `ui-screenshots/` — stable accepted UI review screenshots once T-532 is implemented.
- `run_app.bat` — one-click repository launcher.
- no active `frontend/` Node project.

## Validation

Application validation is layered and proportional:

- Python contract tests protect scientific/runtime boundaries and visualization data contracts.
- NiceGUI fast user-level tests cover high-value UI behavior without expensive browser automation where possible.
- A bounded real-browser/screenshot path covers rendering, responsive layout, interactive charts and the critical configure → launch → live run → history → compare → export journey.
- CI fixtures/screenshots are diagnostic presentation artifacts, never scientific evidence.
- Windows native/onedir packaging requires a target-machine validation checkpoint.
- `T-511` remains a human acceptance gate; automated rendering or screenshots cannot close it.
