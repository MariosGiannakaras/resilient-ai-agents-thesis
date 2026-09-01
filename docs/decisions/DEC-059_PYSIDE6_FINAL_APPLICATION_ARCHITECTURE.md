# DEC-059 — PySide6 final application architecture

**Date:** 2026-08-31  
**Status:** Accepted  
**Task:** T-528 — Final Application / Frontend Rebuild

## Context

DEC-049 intentionally reopened the final frontend choice after the protocol-v2 backend and scientific contract were stable. That gate is now satisfied: T-527 is complete under DEC-058, `protocol-v2.0` is scientifically frozen, and T-529 provides a framework-neutral `StudyService`/`StudyStore` lifecycle.

The final application is a local, single-user thesis/research tool. It does not need a browser deployment model, server-side rendering, cloud infrastructure, authentication, or a second language runtime to satisfy its accepted requirements. The user also requires the final implementation to remain Python-native rather than returning to the historical React/Vite direction.

The useful product/UX evidence from the historical Streamlit/NiceGUI prototypes remains valid: compact desktop navigation, contextual help/tooltips, progressive disclosure, truthful live state, readable scientific comparison, and screenshot-quality presentation. Their framework-specific implementation is historical only.

## Decision

Use **PySide6 / Qt 6 Widgets** as the final application UI framework.

The application boundary is:

```text
PySide6 / Qt Widgets desktop UI
        |
        | presentation/controller adapters only
        v
framework-neutral StudyService / StudyStore / StudyPlanner
        |
        v
validated Python scientific/runtime core
        |
        v
filesystem study/run evidence
```

### Runtime principles

- Python 3.12 remains the supported runtime.
- The UI imports the existing Python application/scientific services directly; no HTTP layer is introduced without a demonstrated requirement.
- Long-running study execution must run outside the Qt GUI thread. The durable StudyStore remains the source of truth across application restarts.
- Qt presentation state never owns scientific identity, RNG, checkpoint state, experiment configuration, metrics, or evidence finalization.
- `src/resilient_agents/` continues to work without importing or launching PySide6.

### Rendering and analytics

- GridWorld is rendered with Qt-native drawing (`QGraphicsView`/`QPainter` or an equivalent read-only Qt surface) from truthful observer state only.
- Scientific results are visualized from stored backend/analysis outputs; the UI does not recompute scientific estimands.
- Heavy or additional chart dependencies are added only when an implemented result view demonstrates the need.
- Animation/interpolation is presentation-only, may drop frames, and must never backpressure or influence scientific execution.

### Product model

The primary application is recipe-first:

1. **Thesis Study** — immutable protocol review, lifecycle/results/evidence access, and an explicit final-evidence execution lock while `final_reserve_access=false`.
2. **Exploratory Study** — clearly non-final development/custom studies using backend-owned validation and planning.

The compact top-level navigation is **Study / Runs / Results / Artifacts**, with contextual Help rather than a separate scientific product area.

## Final-reserve firewall

T-528 does not authorize final scientific execution.

The application may read and display `configs/protocols/protocol-v2.0-final.json`, but while it contains:

```json
"final_reserve_access": false
```

final-reserve execution must be unavailable. The UI must explain that the protocol is frozen and ready but final evidence execution requires the later explicit T-610+ authority. A future UI change alone may not bypass the server/backend/application guard.

## Visual direction

The final interface is rebuilt from scratch rather than visually cloning NiceGUI. Preserve only validated UX ideas from the prototype screenshots and DEC-046:

- compact desktop information density;
- clear sidebar navigation;
- plain-language labels with technical detail on demand;
- contextual help/tooltips;
- consistent status + icon/text/color semantics;
- restrained motion and strong focus/keyboard states;
- screenshot-ready scientific views;
- no fake telemetry, fake ETA, fabricated replay, or decorative scientific metrics.

Use a calm neutral light theme with one restrained accent, generous but efficient spacing, explicit locked/exploratory/failure semantics, and layouts designed first for ordinary 1366×768 and 1440×900 thesis laptops/desktops.

## CI screenshots

T-528 must add a deterministic headless Qt screenshot workflow. Accepted UI checkpoints are rendered with `QT_QPA_PLATFORM=offscreen`, uploaded as a GitHub Actions artifact, and a curated review set is retained under repository-root `ui-screenshots/` once visually accepted.

Historical NiceGUI screenshots are reference/history and must be segregated from the final accepted PySide6 review set.

## Supersession boundary

This decision supersedes the final-framework clauses of DEC-043 and DEC-044 and the framework-specific portions of DEC-045/046. It does **not** supersede their validated product/UX/scientific-integrity requirements.

DEC-049 remains the authority for rebuilding with a different framework from NiceGUI. DEC-051 remains the Study backend authority. DEC-058 remains the frozen scientific authority.

Standalone executable/package technology remains deferred to the post-thesis packaging task/tracker and is not selected here.
