# DEC-044 — Native standalone application: NiceGUI

**Date:** 2026-08-27  
**Status:** Accepted user-directed pre-WP7 architecture amendment  
**Scope:** Application presentation/runtime boundary only; scientific core, protocols, run bundles, evidence, and provenance remain unchanged.

## Context

DEC-043 selected React/TypeScript/Vite + FastAPI after the application requirements expanded beyond the historical Streamlit dashboard. The user then clarified a material deployment requirement that DEC-043 did not optimize for: the thesis deliverable must run as a **standalone desktop application in its own window** and should be distributable as a clean application folder together with the thesis, without requiring a browser, Node.js, or a frontend development toolchain on the end-user machine.

That requirement reopens the application framework decision. Existing React/FastAPI scaffold work is intentionally treated as disposable prototype work; sunk implementation cost is not a reason to preserve a more complex architecture.

## Required application characteristics

The selected framework must support all of the following without changing the Python scientific core:

- native/standalone Windows application window;
- smooth live GridWorld visualization with presentation-only animation/speed control;
- real backend-derived run status, heartbeat, progress, events, logs, warnings and metrics;
- detailed model/agent infographics and self-explanatory scientific UX;
- rich experiment configuration and resolved-config review;
- Plotly-heavy comparison/results/artifact views;
- responsive desktop/laptop layout and polished loading/empty/error/disabled states;
- testable deterministic browser/render mode for CI screenshots;
- simple packaging into a clean distributable folder;
- no Node.js requirement for normal development, scientific execution, or end-user operation;
- no duplication of experiment logic outside `src/resilient_agents/`.

## Options reviewed

### Streamlit

Python-only and efficient for ordinary data apps, but the application would rely increasingly on custom components for the live GridWorld, coordinated interaction state and bespoke infographics while retaining rerun-oriented application semantics. It remains a weaker fit for a polished standalone native deliverable.

### React/Vite + FastAPI + native wrapper

Maximum frontend control, but standalone delivery requires an additional native-window wrapper on top of a TypeScript build, compiled assets, typed API/WebSocket contracts and the Python runtime service. This is technically valid but larger than necessary for the thesis once native standalone delivery is a first-class requirement.

### Flet

Strong Python desktop framework with first-class Windows packaging and Plotly support. However its production build path uses the Flutter toolchain; Windows builds require the relevant Visual Studio desktop tooling, and truly bespoke controls may require Flutter/Dart extensions. This increases the build/toolchain surface for the custom GridWorld without improving the scientific core.

### PySide6 / Qt

The strongest traditional native-desktop option and capable of producing standalone executables. It also carries the largest UI implementation and styling cost for the requested dashboard-like information architecture, Plotly-centric analytics, responsive cards, infographics and browser-quality presentation. Choosing it would spend a disproportionate share of the thesis implementation on desktop-widget plumbing.

### NiceGUI native mode

NiceGUI is Python-first and internally uses FastAPI/Uvicorn, Vue/Quasar and a persistent Socket.IO/WebSocket connection. It supports asynchronous/background work, CPU-bound isolation helpers, Plotly elements with live updates/events, arbitrary HTML/CSS/JavaScript and custom client-side event handling. The same application can run in browser mode for deterministic CI validation or in native mode through pywebview for the end-user desktop window.

Official packaging supports `nicegui-pack`/PyInstaller, native mode and `--windowed`; `--onedir` produces a clean directory that starts faster than one-file packaging and can be zipped for distribution. Normal end-user execution does not require Node.js or a browser window.

## Decision

Use **NiceGUI 3.16 native mode** as the application framework.

The target stack is:

```text
NiceGUI native desktop window (pywebview)
        │
        ├── Python UI components / Plotly / HTML-CSS-JS GridWorld observer
        └── persistent NiceGUI client-server channel
        │
Python application/runtime service
        │
        ├── truthful active-run registry and lifecycle capabilities
        └── read-only live observation/event adapters
        │
existing Python headless runner/session/core
        │
filesystem run bundles / provenance / artifacts
```

NiceGUI's internal FastAPI/Uvicorn server is an implementation detail of the UI framework; the thesis does **not** require a separately designed REST frontend/backend boundary for local single-user operation. Application/runtime services remain ordinary Python interfaces so they can be tested without UI and can later be exposed through HTTP only if a concrete requirement appears.

DEC-044 supersedes the React/Vite + explicit FastAPI application choice in DEC-043. DEC-043 remains preserved as historical decision evidence; its scientific and truthfulness constraints remain valid.

## Runtime and packaging contract

- Development/repository launcher: root `run_app.bat` executes the NiceGUI application through the locked `uv` environment.
- Normal user mode: native window, no browser tab, no visible terminal in the final packaged build.
- CI/render mode: the same UI can run non-native on localhost for deterministic browser capture; this is a presentation/testing mode only.
- Final distribution target: `nicegui-pack --onedir --windowed` (or equivalent pinned PyInstaller invocation) on Windows, producing a clean directory containing the executable and required runtime files.
- Prefer onedir over onefile because it starts faster and the user explicitly wants a clean application folder rather than a single self-extracting binary.
- Mutable experiment results/configuration/export paths must live outside PyInstaller temporary internals and use explicit application/repository data paths.
- Packaged native entry points must call `multiprocessing.freeze_support()` as required by NiceGUI/PyInstaller.
- Windows native mode depends on the EdgeChromium/.NET runtime used by pywebview; target-machine packaging validation must verify this explicitly before final delivery.

## GridWorld and live-feedback contract

The scientific runner owns all states, actions, rewards, disturbances and RNG. The UI receives a read-only observation DTO/event stream. The GridWorld renderer may interpolate movement and change visualization cadence client-side, but it may never change scientific step timing, action choice, seeds or result retention.

Use ordinary NiceGUI/Quasar elements for application chrome and forms. Use Plotly for scientific charts. Use a focused custom HTML/SVG/JavaScript element for the live GridWorld only where native NiceGUI elements cannot provide smooth presentation. This is still a Python-owned application and does not introduce a separate frontend project or Node build.

Historical finalized runs without retained step traces must explicitly show replay unavailable; no renderer may synthesize plausible trajectories.

## Validation contract

Before this decision is treated as final-delivery proven, validate on the actual Windows target path:

1. native window launch/close/restart;
2. packaged onedir launch without Python/Node/browser interaction;
3. live GridWorld update smoothness under a real development run;
4. UI responsiveness while scientific work executes out of the UI event loop;
5. Plotly interaction and artifact downloads;
6. deterministic browser-mode screenshots in CI;
7. no change to deterministic scientific results when the observer/UI is enabled versus disabled.

Failure of one of these measured acceptance points may reopen only the presentation framework; it never justifies changing historical evidence or scientific protocol semantics.

## Evidence used

Official documentation reviewed on 2026-08-27 included current NiceGUI native-mode/configuration/packaging, Plotly and background-task documentation; current Flet Windows packaging, Plotly and custom-extension documentation; and current Qt for Python deployment documentation. NiceGUI 3.16.0 is the current PyPI release as of 2026-08-27.
