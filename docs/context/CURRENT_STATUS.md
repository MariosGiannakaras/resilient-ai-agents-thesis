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
- Master progress remains **1/8**. Current task: `T-520 IN_PROGRESS`.

## Continuity / interruption audit

The branch was audited for work left half-finished by interruptions or superseding instructions. Findings are durable in #87/TASKS:

- **D0 integration is unfinished, not lost.** Standalone D0, deterministic/serializable state, episode-preserving deployment and a v1.1 runner exist. A development-only `V11DevelopmentProtocol` adapter was added because historical `PilotProtocol` correctly rejects D0; historical validation must remain unchanged. Focused v1.1 runner tests/current-head CI are required before T-520 closes.
- **Framework migration is source-clean.** React/Vite is historical only; active application code is NiceGUI. Historical Streamlit pages and temporary React/Vite files are removed from the active implementation.
- **NiceGUI is an early shell, not completed T-531.** Read model, five-page shell, historical v1.0 Plotly views, agent infographics and an intentionally empty ECharts live surface exist. Real runtime DTOs, live GridWorld/charts, full configurator, final help/error states, screenshots and packaging remain required.
- Latest checked head failed at documentation consistency before Python compile/tests. The Codex prompt has been repaired; a new current-head CI result must prove the newer D0/NiceGUI checkpoint rather than relying on older run 266.
- Master issue #87 was reconciled from stale Streamlit wording and now includes an interruption checklist.

No second active frontend implementation was found.

## Scientific direction

- Keep F0 frozen Q-learning and C0 continual Q-learning from the common checkpoint; add D0 Dyna-Q+ using only agent-visible information.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.
- Candidate v1.1: seven single-factor conditions; structural remap IDs; four fresh held-out final layouts; fresh precommitted final seeds; bounded D0-only planning tuning.
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

1. Confirm a new current-head CI reaches compile/locked environment/tests after the repaired prompt.
2. Validate the new focused `V11DevelopmentProtocol`/`V11ExperimentRunner` tests and fix any real failures without changing historical protocol semantics.
3. Close T-520 only when green; then proceed dependency-valid T-521/T-530.
4. Attach live GridWorld/charts only to truthful T-530 observer data. Do not start `T-700+`.
