# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

`AGENTS.md` owns always-on rules; do not reconstruct policy from chat history.

## Active package

Current package: pre-WP7 protocol-v1.1 + application refinement governed by DEC-042, DEC-044, DEC-045, DEC-046 and issues #87–#91. DEC-043 is retained only as the superseded React/Vite exploration.

- Work only on `feat/pre-wp7-protocol-v1.1-ui-rebuild`; never create a parallel implementation branch.
- Keep draft PR #92 open through scientific/runtime/native-UI/screenshots/packaging/human acceptance; do not merge early.
- Preserve `protocol-v1.0`, finalized historical runs and frozen evidence immutably.
- `protocol-v1.1` remains candidate until bounded D0 tuning/pilot validates freeze. Never run a v1.1 final campaign for CI/UI convenience.
- Keep `TASKS.md`, `CURRENT_STATUS.md`, decisions and #87–#91 synchronized at meaningful checkpoints.
- `T-511` remains USER_VALIDATION_REQUIRED; every `T-700+` task remains blocked until explicit user approval.

## Startup / resume

The explicit three-file session-start core is:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Before selecting work, inspect `git status`, current branch, recent commits and PR #92/check state. Verify/use the existing pinned branch. Resume valid IN_PROGRESS work first; otherwise select the first dependency-valid READY task. Preserve recoverable commits after substantial validated slices.

Current order: finish D0 → candidate v1.1/statistics → truthful runtime service → native NiceGUI application/live GridWorld → screenshots/browser/Windows packaging → human E2E → ask whether WP7 may begin.

## Scientific contract

- F0 = frozen Q-learning; C0 = continual Q-learning; both start from the common selected checkpoint.
- D0 = information-limited Dyna-Q+ using only agent-visible observations, intended actions and rewards. Never expose evaluator-only executed action, disturbance/change flags, regime or true state.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.
- Tune only D0 planning parameters through a small predeclared development/tuning search.
- v1.1 uses four fresh held-out final layouts and a fresh precommitted final seed bank. New remap IDs: `action-remap-2-swap`, `action-remap-4-cycle`.
- Primary outcomes: cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity. Add paired effects, 95% CIs, explicit n and layout-aware views. No composite resilience score or post-hoc favorable threshold.
- Keep R0 pilot evidence; do not reinstate it unchanged or add deep RL merely to increase model count.
- Historical `PilotProtocol` validation stays unchanged. T-520 may use only an explicit development-only v1.1 adapter; T-521 owns the authoritative candidate-v1.1 protocol schema/lifecycle.

## Application and UX contract

DEC-044/045/046 are authoritative.

- Framework: **NiceGUI 3.16 native mode** with pywebview, Python 3.12 + `uv`. No active React/Vite/Node or Streamlit application stack.
- `src/resilient_agents/` works without UI and owns scientific execution/evidence. NiceGUI never reimplements the runner.
- `run_app.bat` launches the locked application in its own native window. `THESIS_APP_BROWSER_MODE=1` is CI/browser-render mode only.
- Final delivery: validated Windows NiceGUI/PyInstaller `onedir` + `windowed`; recipient needs no Python/Node/browser interaction.
- T-530 provides UI-independent Python DTO/services for truthful lifecycle state, heartbeat/progress/events, unfinished history, safe controls and read-only live GridWorld observation. Unsupported controls are explicit; visualization speed/animation never changes experiment timing/actions/RNG.
- Historical runs without step trace show replay unavailable.
- The primary interface must be understandable by a non-programmer with no RL/model/configuration knowledge. Use plain-language labels while retaining technical IDs as secondary reproducibility detail.
- Use concise helper text, info icons/tooltips, units/ranges/consequences, progressive disclosure for advanced settings, readable resolved-config review, agent/condition/metric explanations and actionable invalid/empty/loading/error/disabled states.
- Use consistent icon + text + semantic color status language; color is never the sole signal. Keep agent identity consistent across GridWorld/charts/tables.
- Use modern compact layouts, restrained hover/focus/selection micro-interactions, smooth purposeful animations and reduced-motion-safe behavior where practical. Never animate or imply scientific progress that did not occur.
- Onboarding is short/skippable/replayable, but every page must remain understandable when it is skipped.

## Visual analytics contract

- **Plotly:** stored scientific/thesis-ready comparisons, distributions, heatmaps and paired CIs. Historical v1.0 error bars remain labelled SD until real CI artifacts exist.
- **ECharts:** real `LIVE / PROVISIONAL` telemetry and compatible agent/settings overlays. Empty runtime input stays empty; never generate demo traces.
- **Mermaid:** explanatory F0/C0/D0, lifecycle and information-boundary infographics.
- **AG Grid Community:** filterable/sortable/selectable run/result/artifact tables; no Enterprise/CDN-only features.
- Visibly distinguish live/provisional, finalized-run and versioned analysis/evidence data. Never promote provisional values into thesis evidence.

## Validation and Git

For each **one bounded scope**: verify dependencies/acceptance, implement the smallest complete solution, fail closed, run the smallest relevant deterministic checks, reconcile docs/issues and review the actual diff.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle truthfulness, visualization-data contracts, native/browser launch and representative render checks. Prefer fast NiceGUI user-level tests; reserve browser/screenshot tests for browser-specific behavior. No arbitrary coverage target or pilot/final matrices in CI. PR CI is the canonical full-suite guard.

Do not submit an `APPROVE` review on your own PR. The normal workflow may permit an **own-PR squash merge**, but this package explicitly defers own-PR squash merge until integrated user-facing acceptance.

Progress uses finite canonical denominators only. Report `Project: X/Y` only from the canonical registry. In-progress/failed work never counts as complete.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and next-task selection autonomously. Stop only for access/credential, external-machine, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, or mandatory human application/WP7 approval.

Technical completion, screenshots, packaged binaries or green CI are not WP7 approval.
