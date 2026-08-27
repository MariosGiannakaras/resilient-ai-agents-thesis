# DEC-049: Frontend Reselection After the Protocol-v2 Backend

**Date:** 2026-08-27  
**Status:** Accepted  

## Context

DEC-044/045/046 and the NiceGUI implementation established useful application feasibility: a local desktop-oriented workflow, truthful runtime state, live GridWorld/telemetry, novice-first explanations, comparison/history/export requirements and separation of scientific logic from UI callbacks.

Those decisions also froze NiceGUI and several framework-specific visualization/package choices as the then-current final implementation path.

The scientific backend is now being redesigned around protocol-v2 multi-method nominal learning plus matched Frozen/Continual resilience. The user has explicitly required that, after this backend redesign, the final UI be designed again from scratch using a **different framework**.

## Decision

1. NiceGUI is **not** the final frontend framework.
2. The current NiceGUI code, screenshots and DEC-044/045/046 implementation details remain auditable prototype/history and may inform workflow requirements, but they do not constrain the final frontend stack.
3. The Python scientific/runtime backend remains the authoritative execution layer and must expose framework-neutral application contracts.
4. `T-528` selects a **different frontend framework from NiceGUI** only after the protocol-v2 scientific/backend contract is stable, then rebuilds the frontend from scratch against those contracts.
5. The framework decision is evaluated against the real local-thesis application needs: desktop/laptop use, reliable integration with the Python scientific service, selected-method dual-GridWorld rendering, live/provisional telemetry, stored scientific charts/tables, accessibility, maintainability, screenshot/presentation quality and later standalone-delivery constraints.
6. Existing Plotly/ECharts/Mermaid/AG Grid Community and NiceGUI/PyInstaller choices are prototype implementation evidence, not immutable final-stack requirements. Equivalent or better tooling is selected with the new framework.
7. Scientific logic, agent-visible/evaluator boundaries, RNG, experiment execution, metrics, provenance and final-evidence semantics must never be reimplemented or altered in the frontend.

## Supersession boundary

This decision supersedes only the **framework-specific final-implementation clauses** of DEC-044/045/046 and active requirements that mandate NiceGUI, NiceGUI-native onboarding, the exact old chart/table stack, or NiceGUI/PyInstaller packaging.

It does **not** supersede the validated product/scientific requirements those prototypes helped establish, including:

- local single-user use;
- a polished self-explanatory research application;
- real configure/run/monitor/history/compare/export workflows;
- truthful live/provisional state and stored/final evidence distinction;
- live GridWorld visualization that cannot alter scientific execution;
- semantic labels/tooltips/accessibility and actionable states;
- explicit pre-run resolved-configuration validation;
- backend-owned experiment execution/provenance;
- later cleaned standalone Windows delivery after the thesis/application gates.

## Architecture consequence

Before `T-528`, protocol-v2 backend work must prefer stable framework-neutral DTO/event/service boundaries over NiceGUI component shapes. At minimum the final frontend must be able to consume:

- experiment/config validation and resolved specifications;
- run lifecycle/capability state;
- method/root/layout/regime/condition identities;
- append-only/provisional telemetry and synchronized Frozen/Continual visualization events;
- read-only evaluator truth that is never fed back to learners;
- stored learning/resilience result summaries and provenance;
- history/export/resource snapshots.

## Execution consequence

- `T-524` records this boundary but does not select the replacement framework.
- `T-525`/`T-526`/`T-527` must not implement new frontend work.
- #93 remains paused and is now the new-framework rebuild tracker.
- `T-803` packaging technology follows the framework accepted at `T-528`; it must not assume PyInstaller/NiceGUI in advance.
