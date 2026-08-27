# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative current-state summary

This file is intentionally short. Detailed policy/history live in the routed source-of-truth documents; use progressive disclosure rather than growing this into a second manual.

## Current execution state

- Canonical ledger: `docs/context/TASKS.md`.
- Historical milestones remain accepted and preserved, including `T-100` target-machine baseline and `T-200` research framing through completed WP6 evidence production.
- `T-511` remains **USER_VALIDATION_REQUIRED**. Automated checks/screenshots never substitute for intended-user E2E acceptance.
- **Pre-WP7 user approval: NOT APPROVED.** All `T-700+` WP7/WP8 work remains blocked.
- Existing `protocol-v1.0`, every finalized `FINAL-*` bundle, and the current thesis-final evidence package remain immutable historical baseline evidence.

## Active pre-WP7 refinement

- Accepted decisions: `DEC-042` scientific/application refinement and `DEC-043` application-framework reopening.
- Single implementation branch: `feat/pre-wp7-protocol-v1.1-ui-rebuild`.
- Single draft integration PR: #92.
- Trackers: master #87; scientific #88; runtime #89; UI #90; screenshots/CI/Codex handoff #91.
- Do not create a parallel implementation branch for this work package.
- `T-513` governance/Codex handoff is complete. Master tracker #87 is **1/8**.
- Current task: `T-520 IN_PROGRESS` — integrate D0 into the headless runner/agent-construction path. Framework migration may proceed as an adjacent application checkpoint on the same branch but does not make blocked runtime/UI acceptance tasks complete.
- Standalone D0, episode-preserving deployment semantics, and an initial versioned v1.1 runner extension are committed; their current branch CI must be checked before `T-520` can close.

### Scientific direction

- Retain F0 frozen Q-learning and C0 continual Q-learning from their common selected nominal checkpoint.
- Add D0 Dyna-Q+ as a third scientifically distinct tabular agent using only agent-visible interaction data; evaluator-only information remains forbidden.
- Keep the existing validated F0/C0 values: alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, 48-step horizon, and 32 paired final roots.
- `protocol-v1.1` is a **candidate**, not frozen. D0-specific planning parameters require bounded development/tuning selection and non-final validation before any freeze.
- Candidate v1.1 keeps seven single-factor conditions, structurally renames the remaps to `action-remap-2-swap` and `action-remap-4-cycle`, and must use four fresh held-out final layouts plus a fresh precommitted final seed bank because v1.0 final outcomes have already been inspected.
- Primary reporting: cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity with explicit `NOT_RECOVERED`; paired effects and 95% CIs are required. No composite resilience score or post-hoc favorable threshold.
- Preserve R0 pilot evidence; do not reinstate the accepted R0 construction unchanged and do not add deep RL merely to increase model count.

### Application direction

- `DEC-043` supersedes the historical Streamlit-specific application-layer choice after comparing current Streamlit, Dash 4.2 + FastAPI, NiceGUI, Panel, and a dedicated web frontend.
- Target frontend: **React + TypeScript + Vite**. Target application/runtime backend: **FastAPI + Uvicorn** with explicit REST/WebSocket contracts.
- Dash 4.2 + FastAPI is the preferred Python-only alternative, but the dedicated React frontend is selected because smooth GridWorld animation, custom model infographics, onboarding, rich interaction state, accessibility, browser validation, and screenshot-level polish are first-class requirements.
- Keep `src/resilient_agents/` headless and UI-independent. FastAPI is an adapter over a truthful application/runtime service, never a second scientific runner.
- WebSocket live state covers real active-run status/events/logs and a read-only GridWorld observer. Unsupported lifecycle controls remain explicit.
- Visualization interpolation/speed is client presentation only and never changes experiment timing, actions, or RNG streams.
- Historical finalized runs without retained step trace display replay unavailable; never synthesize a path.
- Node/Vite is build-time only for the normal supported user path. Root `run_app.bat` must launch one FastAPI/Uvicorn process serving prebuilt frontend assets through the locked Python environment.
- Create repository-root `ui-screenshots/` for stable accepted browser screenshots; screenshot fixtures are not scientific evidence.

## Accepted repository / Codex baseline

- Python 3.12 + `uv`, project-owned Gymnasium GridWorld, explicit agent/evaluator information boundary, deterministic RNG streams, filesystem-first finalized run bundles, provenance/checksums, and guarded publication remain authoritative.
- Native Windows CPU execution remains the required scientific baseline; the Radeon RX 570 is not a validated scientific-compute backend.
- Invalid/ambiguous required scientific, provenance, or lifecycle state fails closed. Never fabricate data, evidence, state, progress, logs, metrics, protocol status, or results.
- Testing remains risk-based and proportional; PR CI is the full-suite guard when available and pilot/final matrices are never CI tests.
- Codex session startup remains exactly `AGENTS.md`, `docs/context/TASKS.md`, and this file, followed by progressive task-specific reading. Bootstrap: `docs/context/CODEX_EXECUTION_PROMPT.md`.

## Bibliography baseline

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable thesis import remains `bibliography-integration-v3`; bibliography originals are not edited in this repository.

## Still intentionally unfrozen

The v1.1 D0-specific planning parameters, final v1.1 freeze, and any new v1.1 final evidence remain intentionally unfrozen until bounded non-final tuning/pilot and protocol acceptance gates are satisfied. Application implementation details below the DEC-043 boundary may evolve during the prototype, but switching frameworks again requires measured evidence. Later supervisor/deadline/template/defense inputs remain deferred and do not block this package.

## Exact next action

Continue `T-520` on the existing branch and validate the D0/v1.1 runner checkpoint. In parallel only where it does not bypass dependencies, replace the historical Streamlit shell with the DEC-043 React/Vite + FastAPI scaffold, update the locked build/runtime dependencies and active application documentation, and keep the UI connected only to truthful backend data. `T-530`/`T-531` remain incomplete until their acceptance conditions are actually satisfied. No `T-700+` action is permitted.

After technical refinement and user review are complete, explicitly ask whether the user approves starting WP7. Only a direct affirmative answer unlocks writing/defense work.
