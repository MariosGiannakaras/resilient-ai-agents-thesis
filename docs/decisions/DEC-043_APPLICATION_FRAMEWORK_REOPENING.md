# DEC-043 — Application framework reopening: React/Vite + FastAPI

**Date:** 2026-08-27  
**Status:** Accepted user-directed pre-WP7 architecture amendment  
**Scope:** Application presentation/runtime boundary only; scientific core, protocol evidence, run bundles, and provenance remain unchanged.

## Context

The historical dashboard was implemented as a thin local Streamlit layer. That choice was appropriate for the earlier bounded dashboard requirement, and `REQ-ARCH-008` explicitly allowed reopening it when measured application needs justified an amendment.

The current user-directed refinement materially raises the presentation/runtime requirements. The application is now expected to provide a smooth live GridWorld, detailed model/agent infographics, continuous run/event/log/progress feedback, rich configuration review, responsive multi-page navigation, polished self-explanatory interaction states, presentation-quality screenshots, and deterministic browser validation. These are first-class thesis-application requirements rather than optional decoration.

The framework choice was therefore reopened rather than preserving Streamlit by inertia.

## Options reviewed

### Streamlit

Strengths: very low Python-only implementation cost; excellent data-app ergonomics; fragments can rerun independently and `run_every` supports bounded live polling; Components v2 now provides integrated, bidirectional custom JavaScript/TypeScript components.

Limitation for this application: smooth continuous GridWorld animation, rich coordinated interaction state, bespoke model infographics, and product-like onboarding would increasingly live in custom frontend components while the surrounding application still follows Streamlit rerun semantics. The result would combine a custom frontend subsystem with Streamlit rather than avoid one.

### Dash 4.2 + FastAPI

Strengths: strong Plotly/scientific visualization fit; Python-first callbacks; Dash 4.2 supports FastAPI as a backend and native WebSocket callbacks for progress streams, real-time logs, and continuous server push. It is the preferred Python-only alternative.

Limitation for this application: the custom GridWorld/infographic/onboarding surface would still require increasingly substantial React components. Once those components become central rather than exceptional, Dash adds an intermediate callback/component abstraction without reducing the frontend work enough to justify it.

### NiceGUI

Strengths: modern Python-first reactive UI; FastAPI/Uvicorn foundation; Socket.IO real-time communication; Quasar/Vue component system; useful headless-browser testing support.

Limitation for this application: polished bespoke visualizations still require custom Vue/JavaScript components, while the thesis already needs a separate runtime/application service boundary. NiceGUI is a credible simpler alternative but gives less direct control over the custom visualization layer than a dedicated frontend.

### Panel

Strengths: mature scientific Python/dashboard ecosystem and reactive visualization support.

Limitation for this application: best fit is analytical/dashboard workflows rather than the product-like animated GridWorld and custom interaction system now required. It does not provide a material advantage over Dash or NiceGUI here.

### React + TypeScript + Vite frontend with FastAPI backend

Strengths: direct control over SVG/Canvas animation, layout, accessibility, onboarding, client state, responsive behavior, custom scientific infographics, browser testing, and screenshot stability. FastAPI provides REST/WebSocket endpoints and can serve the built Vite SPA, so the final local application can still run as one Uvicorn/FastAPI process. The existing Python scientific core stays completely headless and does not move into TypeScript.

Cost: a real frontend build toolchain and typed API contracts are required. This is justified because the frontend is now a substantial application surface rather than a small dashboard wrapper.

## Decision

Use **React + TypeScript + Vite** for the application frontend and **FastAPI + Uvicorn** for the application/runtime API and WebSocket transport.

This supersedes only the historical Streamlit-specific portion of DEC-001/DEC-023/`REQ-ARCH-008`. The following remain unchanged:

- Python 3.12 + `uv` scientific/runtime baseline;
- `src/resilient_agents/` works without any UI;
- scientific configuration, execution, metrics, and provenance remain Python-owned;
- filesystem run bundles remain evidence source of truth;
- the UI never fabricates progress, metrics, logs, results, controls, or historical replay;
- evaluator-only state remains unavailable to agents;
- visualization must not alter experiment timing, actions, or RNG streams;
- historical finalized runs without retained step traces show replay unavailable;
- local single-user operation; no auth/cloud/microservice architecture.

## Target architecture

```text
React/TypeScript/Vite SPA
        │
        ├── REST: configuration/history/results/artifacts/resources
        └── WebSocket: active-run state/events/logs/live GridWorld observer
        │
FastAPI application/runtime service
        │
        ├── capability-based run supervision
        └── read-only observation/event adapters
        │
existing Python headless runner/session/core
        │
filesystem run bundles / provenance / artifacts
```

The live GridWorld is an observer of real backend state. Animation/interpolation and the user-selected visualization speed are presentation-only client behavior.

## Runtime and build boundary

Node/Vite is a **build-time frontend dependency**, not a scientific runtime dependency. The supported end-user path remains root `run_app.bat` using the locked Python environment. The final launcher starts one FastAPI/Uvicorn application that serves prebuilt frontend assets. Do not silently require the validated thesis machine to have Node for normal application use unless the target-machine capability contract is explicitly amended.

Frontend source and package lock are versioned. CI builds the SPA and performs bounded browser validation. Stable accepted UI screenshots are stored under repository-root `ui-screenshots/`; CI fixtures/screenshots are never scientific evidence.

## Initial implementation constraints

- Vite rather than Next.js: no SSR, SEO, server components, or internet deployment requirement justifies the additional framework/runtime surface.
- Keep the frontend dependency set small. Prefer native React, CSS variables, accessible semantic HTML, and focused libraries over a large UI platform.
- Use Plotly.js for stored scientific charts where it preserves the existing Plotly analysis ecosystem; custom GridWorld/model infographics may use SVG/Canvas directly.
- Large visualization dependencies should be route/lazy loaded where practical.
- REST/WebSocket payloads require explicit versioned/validated schemas; the browser does not infer scientific state from files ad hoc.
- FastAPI endpoints remain adapters over application/runtime services, not a second implementation of experiment logic.

## Evidence used for the decision

Official framework documentation reviewed on 2026-08-27:

- Streamlit fragments and Components v2 documentation.
- Plotly Dash 4.2 WebSocket callbacks and FastAPI server-backend documentation.
- NiceGUI technological foundations/testing documentation.
- FastAPI WebSocket documentation.
- Vite React/TypeScript project documentation.

## Reopening condition

Reopen this decision only if a bounded implementation prototype demonstrates a material reliability, target-machine, accessibility, performance, or maintenance problem that cannot be corrected within this architecture. A preference for fewer frontend files by itself is not sufficient, and a framework switch must never require changes to scientific evidence or protocol semantics.
