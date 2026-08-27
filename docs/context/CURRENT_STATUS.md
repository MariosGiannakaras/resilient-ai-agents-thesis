# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative current-state summary

This file is intentionally short. Detailed policy/history live in the routed source-of-truth documents; use progressive disclosure rather than growing this into a second manual.

## Current execution state

- Canonical ledger: `docs/context/TASKS.md`.
- Historical milestones remain accepted and preserved, including WP0–WP4 and the completed historical v1.0 evidence path.
- `T-511` remains **USER_VALIDATION_REQUIRED**. Automated checks/screenshots never substitute for intended-user E2E acceptance.
- **Pre-WP7 user approval: NOT APPROVED.** All `T-700+` WP7/WP8 work remains blocked.
- Existing `protocol-v1.0`, every finalized `FINAL-*` bundle, and the current thesis-final evidence package remain immutable historical baseline evidence.

## Active pre-WP7 refinement

- Accepted decisions: `DEC-042` scientific/application refinement, historical `DEC-043` web-frontend exploration, superseding `DEC-044` native NiceGUI application, and `DEC-045` visual analytics stack.
- Single implementation branch: `feat/pre-wp7-protocol-v1.1-ui-rebuild`.
- Single draft integration PR: #92.
- Trackers: master #87; scientific #88; runtime #89; UI #90; screenshots/CI/Codex handoff #91.
- Do not create a parallel implementation branch for this work package.
- `T-513` governance/Codex handoff remains complete. Master tracker #87 remains **1/8** until the next whole milestone satisfies acceptance; in-progress UI/framework work does not count as complete.
- Current scientific task: `T-520 IN_PROGRESS` — complete and validate D0 integration into the headless runner/agent-construction path.
- Adjacent application migration is underway on the same branch because it does not require scientific final evidence: historical Streamlit pages and the temporary React/Vite scaffold have been removed; NiceGUI native shell/read-model/visualization code is committed but not yet validated enough to close the application tasks.

### Scientific direction

- Retain F0 frozen Q-learning and C0 continual Q-learning from their common selected nominal checkpoint.
- Add D0 Dyna-Q+ as a third scientifically distinct tabular agent using only agent-visible interaction data; evaluator-only information remains forbidden.
- Keep validated F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, 48-step horizon, and 32 paired final roots.
- `protocol-v1.1` is a **candidate**, not frozen. D0-specific planning parameters require bounded development/tuning selection and non-final validation before freeze.
- Candidate v1.1 keeps seven single-factor conditions, structurally renames remaps to `action-remap-2-swap` and `action-remap-4-cycle`, and must use four fresh held-out final layouts plus a fresh precommitted final seed bank because v1.0 final outcomes have already been inspected.
- Primary reporting: cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity with explicit `NOT_RECOVERED`; paired effects and 95% CIs are required. No composite resilience score or post-hoc favorable threshold.
- Preserve R0 pilot evidence; do not reinstate the accepted R0 construction unchanged and do not add deep RL merely to increase model count.

### Application direction

- `DEC-044` supersedes the React/Vite application choice in `DEC-043` after the final deliverable requirement was clarified: the thesis application must open in its **own standalone desktop window** and be distributable as a cleaned Windows application folder.
- Target framework: **NiceGUI 3.16 native mode** (`pywebview`) over the existing Python scientific/runtime layers. No active Node/npm/Vite frontend project remains.
- Root `run_app.bat` launches the locked Python application entry point in native mode. Explicit `THESIS_APP_BROWSER_MODE=1` is reserved for CI/browser rendering of the same pages.
- Final delivery target is a validated NiceGUI/PyInstaller **onedir + windowed** Windows package so the recipient does not need Python, Node or a browser interaction. Target-machine native/package validation remains required before final delivery.
- Keep `src/resilient_agents/` headless and UI-independent. Application/runtime service objects remain Python interfaces; NiceGUI never becomes a second runner.
- T-530 must expose real active-run state/events/heartbeat/logs and a read-only GridWorld observer. Unsupported controls remain explicit.
- Visualization interpolation/speed is presentation-only and never changes experiment timing, actions or RNG streams.
- Historical finalized runs without retained step trace display replay unavailable; never synthesize a path.

### Visual analytics direction

`DEC-045` assigns roles rather than adding overlapping libraries:

- **Plotly:** stored scientific comparisons and screenshot/presentation-ready figures; v1.0 current error bars must remain labelled SD until paired v1.1 95% CI artifacts exist.
- **ECharts:** live/provisional animated telemetry and compatible multi-agent/run overlays.
- **Mermaid:** F0/C0/D0 and experiment/information-boundary infographics.
- **AG Grid Community:** run/results/artifact inspection tables.

Live/provisional telemetry, finalized individual runs and versioned analysis/evidence are separate data classes. The UI never promotes live values into final evidence.

## Current application checkpoint

Committed on the active branch:

- NiceGUI native dependency/application packaging entry point;
- `src/app/state.py` truthful read-only workspace facade;
- `src/app/visualizations.py` Plotly/ECharts/Mermaid visualization contracts;
- NiceGUI Dashboard, New Experiment, Runs, Compare and Artifacts shell in `src/app/main.py`;
- real v1.0 comparison views from stored `aggregated_summary.csv`;
- F0/C0/D0 explanatory infographics;
- an intentionally empty live telemetry surface until T-530 provides real DTOs;
- NiceGUI onboarding component;
- Streamlit page removal and React/Vite scaffold removal;
- Python-only lock-refresh workflow and native repository launcher.

These are **implementation checkpoints, not accepted UI completion**. Current-head lock/import/tests/browser render must pass, live GridWorld/runtime integration remains incomplete, screenshots are not yet accepted, and Windows onedir packaging is not yet validated.

## Accepted repository / Codex baseline

- Python 3.12 + `uv`, project-owned Gymnasium GridWorld, explicit agent/evaluator information boundary, deterministic RNG streams, filesystem-first finalized run bundles, provenance/checksums, and guarded publication remain authoritative.
- Native Windows CPU execution remains the required scientific baseline; the Radeon RX 570 is not a validated scientific-compute backend.
- Invalid/ambiguous required scientific, provenance, or lifecycle state fails closed. Never fabricate data, evidence, state, progress, logs, metrics, protocol status or results.
- Testing remains risk-based and proportional; PR CI is the full-suite guard when available and pilot/final matrices are never CI tests.
- Codex session startup remains exactly `AGENTS.md`, `docs/context/TASKS.md`, and this file, followed by progressive task-specific reading. Bootstrap: `docs/context/CODEX_EXECUTION_PROMPT.md`.

## Bibliography baseline

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable thesis import remains `bibliography-integration-v3`; bibliography originals are not edited in this repository.

## Exact next action

1. Inspect current PR #92 head/checks after the NiceGUI dependency/migration commits; diagnose lock/import/UI errors instead of assuming success.
2. Complete/validate `T-520` D0 runner integration.
3. Reconcile `TASKS.md`/issues with DEC-044/045 and the validated application checkpoint.
4. Proceed dependency-valid work toward `T-521` and `T-530`; the live GridWorld/live charts may attach only to real T-530 observer data.
5. Build root `ui-screenshots/` and Windows native/onedir packaging validation at their defined gates.
6. Do not start `T-700+`.

After technical refinement and user review are complete, explicitly ask whether the user approves starting WP7. Only a direct affirmative answer unlocks writing/defense work.
