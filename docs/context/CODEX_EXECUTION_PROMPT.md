# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

`AGENTS.md` owns always-on rules; do not reconstruct policy from chat history.

## Active package

Current package: pre-WP7 protocol-v1.1 + application refinement governed by DEC-042, DEC-044, DEC-045 and issues #87–#91. DEC-043 is retained only as the superseded React/Vite exploration.

- Work only on `feat/pre-wp7-protocol-v1.1-ui-rebuild`; never create a parallel implementation branch.
- Keep draft PR #92 open through scientific/runtime/native-UI/screenshots/packaging/human acceptance; do not merge early.
- Preserve `protocol-v1.0`, finalized historical runs and frozen evidence immutably.
- `protocol-v1.1` remains candidate until bounded D0 tuning/pilot validates freeze. Never run a v1.1 final campaign for CI/UI convenience.
- Keep `TASKS.md`, `CURRENT_STATUS.md`, decisions and #87–#91 synchronized at meaningful checkpoints.
- `T-511` remains USER_VALIDATION_REQUIRED; every `T-700+` task remains blocked until explicit user approval.

## Resume

1. Inspect `git status`, current branch, recent commits and PR #92/check state.
2. Read `AGENTS.md`, `docs/context/TASKS.md`, `docs/context/CURRENT_STATUS.md`.
3. Verify/use the existing pinned branch.
4. Resume valid IN_PROGRESS work first; otherwise select the first dependency-valid READY task.
5. Preserve recoverable commits after substantial validated slices.

Current order: finish D0 → candidate v1.1/statistics → truthful runtime service → native NiceGUI application/live GridWorld → screenshots/browser/Windows packaging → human E2E → ask whether WP7 may begin.

## Scientific contract

- F0 = frozen Q-learning; C0 = continual Q-learning; both start from the common selected checkpoint.
- D0 = information-limited Dyna-Q+ using only agent-visible observations, intended actions and rewards. Never expose evaluator-only executed action, disturbance/change flags, regime or true state to the agent.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.
- Tune only D0 planning parameters through a small predeclared development/tuning search.
- v1.1 uses four fresh held-out final layouts and a fresh precommitted final seed bank. New remap IDs: `action-remap-2-swap`, `action-remap-4-cycle`.
- Primary outcomes: cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity with explicit non-recovery. Add paired effects, 95% CIs, explicit n and layout-aware views. No composite resilience score or post-hoc favorable threshold.
- Keep R0 pilot evidence; do not reinstate it unchanged or add deep RL merely to increase model count.

## Application contract

DEC-044 is authoritative.

- Framework: **NiceGUI 3.16 native mode** with pywebview, Python 3.12 + `uv`.
- `src/resilient_agents/` works without UI and owns scientific execution/evidence. NiceGUI never reimplements the runner.
- No active React/Vite/Node, Streamlit, Dash, Flet or Qt application stack. Reopening requires a new evidence-backed ADR.
- `run_app.bat` launches the locked application in its own native window. `THESIS_APP_BROWSER_MODE=1` is CI/browser-render mode only.
- Final delivery target: validated Windows NiceGUI/PyInstaller `onedir` + `windowed`; end-user operation requires no Python/Node/browser interaction.
- T-530 provides UI-independent Python DTO/services for truthful queued/running/completed/failed/cancelled/interrupted state, heartbeat/progress/events, unfinished history, capability-based controls and a read-only live GridWorld observer.
- Unsupported controls are explicit. Visualization speed affects presentation only. Historical runs without retained step trace show replay unavailable.

## Visual analytics contract

DEC-045 is authoritative.

- **Plotly:** stored scientific/thesis-ready comparisons, distributions, heatmaps and paired CIs. Historical v1.0 error bars remain labelled SD until real CI artifacts exist.
- **ECharts:** real `LIVE / PROVISIONAL` telemetry and compatible agent/settings overlays. Empty runtime input stays empty; never generate demo traces.
- **Mermaid:** explanatory F0/C0/D0, lifecycle and information-boundary infographics.
- **AG Grid Community:** filterable/sortable/selectable run/result/artifact tables; no Enterprise/CDN-only features.
- Keep metric names/units and agent identities consistent. Color is never the sole comparison channel.
- Visibly distinguish live/provisional, finalized-run and versioned analysis/evidence data. Never promote provisional values into thesis evidence.

Current branch contains an in-progress NiceGUI five-page shell, truthful read model, visualizations and migrated onboarding; old Streamlit pages and temporary React/Vite files are removed. Treat this checkpoint as unvalidated until current-head lock/import/tests/browser render pass. Never fill live panels with invented trajectories for appearance.

## Validation and Git

For each scope: verify dependencies/acceptance, implement the smallest complete solution, fail closed, run the smallest relevant deterministic checks, reconcile docs/issues and review the actual diff.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle truthfulness, visualization-data contracts, native/browser launch and representative render checks. Prefer fast NiceGUI user-level tests; reserve browser/screenshot tests for browser-specific behavior. No arbitrary coverage target, broad fuzz/mutation expansion, or pilot/final matrices in CI. PR CI is the canonical full-suite guard.

Do not submit `APPROVE` on your own PR. The normal repository workflow may permit an **own-PR squash merge**, but this package explicitly defers own-PR squash merge until integrated user-facing acceptance.

Progress uses finite canonical denominators only; in-progress/failed work never counts complete.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and next-task selection autonomously. Stop only for access/credential, external-machine, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, or mandatory human application/WP7 approval.

Technical completion, screenshots, packaged binaries or green CI are not WP7 approval.
