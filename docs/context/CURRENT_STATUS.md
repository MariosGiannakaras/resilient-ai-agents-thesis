# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative current-state summary

This file stays compact. `docs/context/TASKS.md` is the canonical ledger; use progressive task-specific reading for decisions/evidence.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine capability validation and `T-200` research framing through completed historical WP6 v1.0 evidence.
- Existing `protocol-v1.0`, finalized `FINAL-*` bundles and thesis-final evidence are immutable historical baseline evidence.
- `T-511` remains **USER_VALIDATION_REQUIRED**. Automated checks/screenshots/package validation do not replace intended-user E2E acceptance.
- **Pre-WP7 approval: NOT APPROVED.** All `T-700+` work remains blocked.

## Active refinement

- Decisions: `DEC-042` scientific refinement; superseded `DEC-043` React/Vite exploration; authoritative `DEC-044` NiceGUI native application; `DEC-045` visual analytics; `DEC-046` novice-first compact UX.
- Single branch: `feat/pre-wp7-protocol-v1.1-ui-rebuild`; single draft PR: #92. No parallel implementation branch or early merge.
- Trackers: #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/packaging.
- Master progress is **2/8**. `T-520` is complete; current task is `T-521 READY`.
- PR CI run **346** passed documentation consistency, JSON validation, Python compile, locked environment, complete tests including `test_v11_runner.py`, and bibliography integrity on the D0/NiceGUI checkpoint.

## Continuity / interruption audit

The branch was audited for work left half-finished by interruptions or superseding instructions. Findings are durable in #87/TASKS:

- **D0 integration is complete.** Standalone D0, deterministic/serializable state, episode-preserving deployment, development-only `V11DevelopmentProtocol` and deterministic F0/C0/D0 v1.1 runner integration are validated. Historical `PilotProtocol` semantics remain unchanged.
- **Framework migration is source-clean.** React/Vite is historical only; active application code is NiceGUI. Historical Streamlit pages and temporary React/Vite files are removed from the active implementation.
- **NiceGUI is an early shell, not completed T-531.** Read model, five-page shell, historical v1.0 Plotly views, agent infographics and an intentionally empty ECharts live surface exist. Real runtime DTOs, live GridWorld/charts, full configurator, final help/error states, screenshots and packaging remain required.
- **Documentation reconciliation is still active.** Older source-of-truth rows that say Streamlit or “standalone executable not required” are superseded by the later explicit user requirement plus DEC-044/046 and must be updated rather than left contradictory.

No second active frontend implementation was found.

## Scientific direction

- Keep F0 frozen Q-learning and C0 continual Q-learning from the common checkpoint; add D0 Dyna-Q+ using only agent-visible information.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.
- T-521 candidate v1.1: seven single-factor conditions; structural remap IDs; four fresh held-out final layouts; fresh precommitted final seeds; bounded D0-only planning tuning; paired statistical support.
- Primary reporting: cumulative deficit, immediate degradation, terminal gap/performance. Recovery stays secondary/sensitivity. Paired effects + 95% CIs required; no composite resilience score/post-hoc favorable threshold.
- Preserve R0 pilot evidence; do not reinstate it unchanged or add deep RL merely to increase model count.

## Application / UX direction

- Framework: **NiceGUI 3.16 native mode** (`pywebview`) over the Python scientific/runtime layers. `src/resilient_agents/` remains headless/UI-independent.
- `run_app.bat` launches its own native window; browser mode is CI/render-only. Final target: validated PyInstaller/NiceGUI `onedir + windowed` Windows folder requiring no Python/Node/browser interaction.
- T-530 must provide truthful lifecycle DTOs/events/heartbeat/history/safe controls and a read-only GridWorld observer. Unsupported controls are explicit; visualization never changes timing/actions/RNG. Historical no-trace runs show replay unavailable.
- DEC-046 requires a non-programmer/non-RL user to understand the app: plain-language labels, technical IDs as secondary detail, helper text, info icons/tooltips, units/ranges/consequences, progressive disclosure, readable resolved config, agent/condition/metric explanations, semantic text+icon+color statuses and actionable empty/loading/error/disabled states.
- Visual style: modern compact hierarchy, consistent icons, accessible palette, restrained micro-interactions, purposeful GridWorld/chart/status animations, reduced-motion-safe behavior where practical, skippable/replayable onboarding. Animation must never imply fake scientific progress.

## Visual analytics

- **Plotly:** stored scientific/thesis/presentation-ready figures; historical v1.0 error bars remain labelled SD until real CIs exist.
- **ECharts:** real live/provisional telemetry and compatible agent/settings overlays.
- **Mermaid:** F0/C0/D0 and experiment/information-boundary infographics.
- **AG Grid Community:** analytical run/result/artifact tables.

Live/provisional, finalized-run and versioned analysis/evidence are distinct classes; provisional values never become thesis evidence automatically.

## Accepted baseline

Python 3.12 + `uv`, project GridWorld, information boundary, deterministic RNG, filesystem run bundles, provenance/checksums and guarded publication remain authoritative. Testing is risk-based/proportional; PR CI is the canonical full-suite guard. Codex startup is exactly `AGENTS.md`, `TASKS.md`, this file, then task-specific reading.

`MariosGiannakaras/ThesisBibliography` remains canonical; accepted immutable import: `bibliography-integration-v3`.

## Still intentionally unfrozen

D0 planning parameters, candidate v1.1 freeze, new layouts/seeds/final evidence, active-run runtime, final novice-first UI/screenshots and Windows packaged delivery remain unfrozen/unaccepted until their gates pass.

## Exact next action

1. Reconcile remaining active source-of-truth Streamlit/standalone contradictions to DEC-044/046.
2. Start `T-521`: implement authoritative candidate-v1.1 schema, bounded D0-only tuning plan, fresh layouts/seeds, structural remap IDs and paired statistical support.
3. Keep final-evidence use blocked until T-522 non-final validation/freeze gate passes.
4. Attach live GridWorld/charts only to truthful T-530 observer data. Do not start `T-700+`.
