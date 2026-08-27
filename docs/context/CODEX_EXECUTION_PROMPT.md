# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR/issue updates, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

This is the tracked bootstrap. `AGENTS.md` owns always-on rules; do not reconstruct policy from chat history.

## Active package override — 2026-08-27

The current package is the user-approved pre-WP7 protocol-v1.1 + application refinement governed by DEC-042, DEC-044, DEC-045 and issues #87–#91. DEC-043 is retained only as historical evidence of the superseded React/Vite exploration.

- Work only on `feat/pre-wp7-protocol-v1.1-ui-rebuild`; do not create another implementation branch for this package.
- Keep draft PR #92 open through integrated scientific/runtime/UI/screenshots/native-package and user-facing acceptance; do not merge early.
- Preserve `protocol-v1.0`, finalized historical runs and frozen evidence immutably.
- `protocol-v1.1` remains candidate until D0-specific non-final tuning/pilot evidence and validation justify freeze. Never run a v1.1 final campaign for CI/UI convenience.
- Keep `TASKS.md`, `CURRENT_STATUS.md`, decisions and #87–#91 synchronized at meaningful checkpoints.
- Root `ui-screenshots/` contains stable UI review screenshots; screenshots/fixtures are never scientific evidence.
- `T-511` remains USER_VALIDATION_REQUIRED and all `T-700+` work remains blocked until explicit user approval.

## Startup / resume

1. Inspect `git status`, current branch, recent commits, PR #92/check state and current Resume state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Verify the branch is exactly `feat/pre-wp7-protocol-v1.1-ui-rebuild`; switch/update that existing branch rather than creating another one.
4. Resume valid IN_PROGRESS work first, otherwise the first dependency-valid READY refinement task. Read task-specific evidence only after selection.
5. Work one bounded scope at a time and preserve recoverable checkpoint commits after substantial validated slices.

## Current execution order

1. Finish D0 runner integration and candidate protocol-v1.1/statistical support.
2. Build truthful Python application/runtime service for active experiments and the read-only observer.
3. Complete the **NiceGUI 3.16 native** application: Dashboard → New Experiment → Runs/live GridWorld → Compare → Artifacts.
4. Complete visual analytics per DEC-045: Plotly stored-evidence figures, ECharts live telemetry, Mermaid explanatory infographics and AG Grid Community analytical tables.
5. Add root UI screenshots + bounded browser render validation + Windows native/onedir packaging validation.
6. Human E2E acceptance; only afterward ask explicitly whether WP7 may begin.

## Scientific package contract

- Retain F0 frozen Q-learning and C0 continual Q-learning from the common selected checkpoint.
- Add D0 Dyna-Q+ using only agent-visible observations, intended actions and rewards. Evaluator-only executed action, change/disturbance flags, regime and true state remain forbidden.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48, and 32 paired final roots.
- Tune only D0-specific planning parameters through a small predeclared development/tuning search; never invent the selected planning budget/kappa.
- Use four fresh held-out v1.1 final layouts and a fresh precommitted final seed bank before any new final evidence is inspected.
- New remap IDs are `action-remap-2-swap` and `action-remap-4-cycle`; historical IDs remain unchanged.
- Primary reporting: cumulative deficit, immediate degradation and terminal gap/performance. Recovery remains secondary/sensitivity with explicit non-recovery. Add paired effects + 95% CIs, explicit n and layout-aware views. No composite resilience score or post-hoc favorable threshold.
- Keep R0 pilot evidence; do not reinstate its accepted construction unchanged or add deep RL merely to increase model count.

## Application architecture contract

DEC-044 is authoritative:

- Application framework: **NiceGUI 3.16 native mode** with pywebview.
- Python 3.12 + `uv` remains the repository/runtime baseline.
- `src/resilient_agents/` must work without UI and owns all scientific execution/state/evidence.
- NiceGUI is presentation/control only and calls Python application/runtime service interfaces; do not create a duplicate scientific runner inside UI callbacks.
- No active React/Vite/Node frontend project. Do not reintroduce Node, npm, Vite, Dash, Streamlit, Flet or Qt without a new evidence-backed ADR that supersedes DEC-044.
- Repository `run_app.bat` launches the locked NiceGUI application in its own native desktop window.
- `THESIS_APP_BROWSER_MODE=1` is allowed only for deterministic CI/browser rendering of the same application pages.
- Final distribution target: Windows NiceGUI/PyInstaller `onedir` + `windowed`, tested on the target machine. End-user operation must not require Python/Node/browser interaction.
- Mutable results/configuration/export paths must not rely on PyInstaller temporary extraction paths.

## Runtime / live experiment contract

- Put active orchestration/observation in a UI-independent Python application service: backend-derived queued/running/completed/failed/cancelled/interrupted state, heartbeat/progress/events, read-only live GridWorld observation, history and only safe lifecycle capabilities.
- NiceGUI's internal FastAPI/Uvicorn/Socket.IO implementation is framework plumbing, not a requirement to design a separate REST frontend/backend split. Add HTTP APIs only if a concrete application need appears.
- Unsupported controls are explicitly unsupported; no fake state/progress/logs/metrics.
- Live observation must not change scientific RNG/actions. Visualization speed affects rendering cadence only.
- Historical runs without retained step trace display replay unavailable; never reconstruct a plausible trajectory.
- Scientific work must execute outside/blocking-safe from the NiceGUI event loop where necessary; UI responsiveness cannot be purchased by changing scientific semantics.

## Visual analytics contract

DEC-045 is authoritative:

- **Plotly**: stored scientific comparison/distribution/CI/heatmap figures suitable for thesis/presentation screenshots. For historical v1.0 aggregates, label current error bars as SD; never relabel them as CI. Use paired 95% CIs only when T-522 produces versioned paired statistics.
- **ECharts**: real live/provisional telemetry, compatible multi-agent/run overlays and smooth differential updates. Empty runtime data produces an empty/unsupported state, never demo traces.
- **Mermaid**: explanatory F0/C0/D0, experiment lifecycle and information-boundary infographics; these are explanatory artifacts, not evidence.
- **AG Grid Community**: filterable/sortable/selectable run/result/artifact tables. Do not enable AG Grid Enterprise/CDN-only features.
- Keep consistent agent identities, metric names/units, semantic statuses and screenshot-ready layouts. Color cannot be the sole comparison channel.
- Distinguish `LIVE / PROVISIONAL`, finalized-run and analysis/evidence classes visibly. Never promote provisional data into thesis evidence.
- For live charts, support compatible F0/C0/D0/settings overlays only when axes/configuration are scientifically comparable; otherwise show separate views or compatibility warnings.

## Current application checkpoint to preserve/review

The branch currently contains a NiceGUI native scaffold with `src/app/state.py`, `src/app/visualizations.py`, a five-page `src/app/main.py`, migrated onboarding, real v1.0 comparison plots and an intentionally empty T-530 live surface. Historical Streamlit pages and temporary React/Vite files were removed. Treat this as **unvalidated in-progress implementation** until current-head lock/import/tests/browser render pass.

Do not populate the live GridWorld/ECharts panels with fixture trajectories merely to make screenshots attractive. Deterministic fixture chrome is allowed only under T-532 and must be visibly diagnostic/non-scientific.

## Execution / validation contract

For each scope, confirm dependencies/acceptance, implement the smallest complete solution, fail closed on invalid required state, run the smallest relevant deterministic checks, reconcile docs/tasks/issues, and review the actual diff.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle-truthfulness, visualization-data contracts, native/browser launch and representative render checks. Prefer NiceGUI's fast user-level tests for ordinary UI behavior and reserve real browser/screenshot tests for browser-specific rendering/interaction. No arbitrary coverage target, broad fuzz/mutation/combinatorial expansion, or pilot/final matrices in CI. PR CI is the canonical full-suite guard when available; do not duplicate it merely for reassurance.

Do not submit an `APPROVE` review on your own PR. This package explicitly defers own-PR merge until the integrated user-facing acceptance checkpoint.

Progress uses finite canonical denominators only. Report `Project: X/Y` only from canonical `T-*` entries, with issue/milestone X/Y when useful. In-progress/failed work never counts as complete.

## Stop conditions

Continue routine repository reading, implementation, Git, CI diagnosis, objective review and task selection without asking the user when accepted rules resolve them. Stop only for a genuine access/credential, external-machine, safety/privacy/legal/licensing blocker, a non-objective choice explicitly reserved for the user, or the mandatory human application/WP7 approval gate.

Technical completion, screenshots, packaged binaries or green CI are not WP7 approval.

## Final report

Report objective progress; changed scientific/runtime/UI behavior; branch/PR/CI state; protocol-v1.1 candidate/frozen state; native application/package state; UI screenshots available for review; remaining human acceptance; exact next action; and confirmation that WP7 is blocked unless the user directly approved it.
