# Local thesis application

The application is the local execution, monitoring, analysis, and presentation surface for the validated headless research core. It is not a second implementation of the scientific logic.

## Architecture

`DEC-043` selects the application stack for the current pre-WP7 refinement:

```text
React + TypeScript + Vite frontend
        │
        ├── REST
        └── WebSocket
        │
FastAPI + Uvicorn application/runtime service
        │
existing src/resilient_agents headless core
        │
filesystem run bundles / artifacts / provenance
```

The historical Streamlit dashboard remains in Git history as the previous baseline but is not the target implementation.

### Boundary rules

- Scientific configuration, agent/environment execution, metrics, result persistence, provenance, and protocol validation stay in Python under `src/resilient_agents/`.
- FastAPI routes/WebSockets adapt application/runtime services; they do not reimplement the runner.
- The browser receives only truthful backend-derived state. No mock final metrics, fabricated progress/logs, or invented historical replay.
- Live GridWorld data is read-only observer state. Client animation/interpolation and visualization speed never affect experiment timing, actions, seeds, or RNG streams.
- Historical finalized runs without retained step traces show replay unavailable.
- Lifecycle controls are capability-based. Unsupported pause/resume/stop/cancel/restart operations are shown as unsupported rather than simulated.

## User information architecture

The primary navigation remains intentionally small:

1. **Dashboard** — active/recent runs, warnings, protocol state, current resources, quick actions.
2. **New Experiment** — validated configuration, agents/layouts/conditions/seeds, resolved-config review, launch.
3. **Runs** — active/history/detail workspace, live GridWorld, event timeline, logs/metrics, truthful lifecycle state.
4. **Compare** — compatible run/model comparisons, distributions, paired effects/CIs, counts and condition/layout breakdowns.
5. **Artifacts** — real figures/tables/CSV/JSON/HTML outputs, provenance and exports.

The UI must remain self-explanatory through precise labels, units, contextual help/tooltips, semantic text+icon statuses, accessible colors, actionable empty/loading/error/disabled states, and lightweight onboarding.

## Runtime and frontend build

The final supported user path is root `run_app.bat`. It must start one local FastAPI/Uvicorn process through the locked `uv` environment and serve the prebuilt frontend assets.

Node/Vite is a **build-time dependency**. Normal application use on the validated thesis machine must not silently require Node unless the target-machine contract is explicitly amended. Frontend source and its package lock are versioned; CI builds the frontend and performs bounded browser validation.

During frontend development, a Vite development server may be used as a developer convenience, but that is not the normal thesis-user launch path.

## Repository layout target

- `src/app/` — FastAPI application/runtime API adapter and static-SPA serving.
- `frontend/` — React/TypeScript/Vite source, package manifest/lock, tests and build configuration.
- `frontend/dist/` — prebuilt runtime assets according to the accepted build/packaging policy.
- `ui-screenshots/` — stable accepted UI screenshots captured through the bounded browser-validation workflow.
- `run_app.bat` — one-click Windows launcher.

## Validation

Application validation is layered and proportional:

- Python contract/integration tests protect the runtime API and scientific boundary.
- Frontend type/build checks protect the React application.
- A small set of browser tests protects the critical configure → launch → live run → history → compare → export journey and screenshot rendering.
- CI fixtures are diagnostic only and never scientific evidence.
- `T-511` remains a human acceptance gate; automated rendering or screenshots cannot close it.
