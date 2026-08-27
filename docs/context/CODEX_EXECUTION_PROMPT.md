# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

`AGENTS.md` owns always-on policy. Durable repository state beats stale/truncated chat memory.

## Active package

Pre-WP7 protocol-v1.1 + native application refinement is governed by DEC-042/044/045/046 and issues #87–#91. DEC-043 is superseded history.

- Work only on `feat/pre-wp7-protocol-v1.1-ui-rebuild`; keep draft PR #92 open until the package reaches its human gate.
- Preserve `protocol-v1.0`, finalized historical runs/R0 pilot evidence and frozen historical evidence immutably.
- `T-520` D0 integration is complete; current primary task is `T-521 READY`. `T-530` is dependency-valid but secondary in the same branch.
- Never run v1.1 final evidence for CI/UI convenience.
- `T-511` remains USER_VALIDATION_REQUIRED and every `T-700+` task remains blocked until explicit user approval.

## Startup / resume

1. Inspect `git status`, current branch, recent commits and PR #92/check state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Verify/use the pinned branch and current task state; do not create a parallel implementation branch.
4. Resume valid IN_PROGRESS work first; otherwise select the first dependency-valid READY scope according to canonical execution order.
5. Preserve a recoverable checkpoint after substantial validated work and reconcile durable task/status/issue state.

Current order: T-521 candidate v1.1/settings/statistics → T-522 non-final tuning/freeze gate → T-530 truthful runtime service → T-531 native NiceGUI application → T-532 screenshots/native packaging → T-511 human E2E → T-610–T-613 final evidence → explicit WP7 approval gate.

## Current scientific contract

- Candidate agents: F0 frozen Q-learning, C0 continual Q-learning and D0 information-limited Dyna-Q+. R0 remains historical pilot evidence only; do not reinstate it unchanged.
- F0/C0 base values: alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48, 32 paired final roots.
- T-521 must define the exact small D0-only `planning_steps`/`kappa` search, four fresh held-out final layouts, fresh precommitted final seeds and authoritative candidate schema before non-final evidence is used for selection.
- Multiple **approved** development/tuning configurations are allowed only when predeclared. Every configuration has stable resolved identity/provenance and multiple predefined roots; no single-run/best-seed/best-final cherry-picking. F0/C0 stay fixed unless explicitly reopened; final retained settings freeze before final outcomes.
- Conditions: `nominal`, `action-remap-2-swap`, `action-remap-4-cycle`, `action-failure-1of8`, `action-failure-1of4`, `observation-corruption-1of8`, `observation-corruption-1of4`.
- Primary outcomes: cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity. Add paired effects, 95% CIs, explicit n/layout-aware views; no composite score/post-hoc favorable threshold.
- Never expose evaluator-only true state/executed action/change/disturbance/regime information to an agent.

## Application / UX contract

- NiceGUI 3.16 native mode + pywebview over UI-independent Python scientific/runtime services. No active Streamlit/React/Vite/Node application stack.
- T-530 provides truthful active-run DTOs/events/heartbeat/history/resources, read-only live GridWorld observer and capability-based controls. Unsupported controls are explicit.
- T-531 New Experiment/Runs/Compare must understand agent **and resolved configuration/settings identity**, multiple required roots/repetitions and fixed-vs-tunable settings.
- Plotly = stored/final scientific figures; ECharts = real `LIVE / PROVISIONAL` telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- Novice-first: plain-language labels, secondary technical IDs, accurate tooltips/help, units/ranges/consequences, progressive disclosure, readable pre-run review, semantic icon+text+color states, actionable empty/loading/error/disabled states.
- Modern compact UI with restrained micro-interactions and purposeful GridWorld/chart/status animation. Presentation cadence never changes scientific timing/actions/seeds/RNG; never fabricate historical replay or progress.
- `run_app.bat` remains checkout launcher; final delivery is validated NiceGUI/PyInstaller `onedir + windowed` on Windows.

After acceptance, ordinary approved experiments run directly from the finished desktop application on the validated thesis machine; Codex/console commands are not required merely to execute a frozen configuration. GitHub remains source of truth/CI/evidence coordination, not automatically the final stochastic experiment computer.

## Validation and Git

For each **one bounded scope**, verify dependencies/acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, review the actual diff, and reconcile affected docs/issues.

Testing is proportional: known-answer/determinism/information-boundary/serialization/configuration/lifecycle truthfulness and representative render/native checks. No arbitrary coverage target, broad test-expansion project or pilot/final matrices in CI. PR CI is the canonical full-suite guard.

Do not submit an `APPROVE` review on your own PR. The normal workflow may permit an **own-PR squash merge**, but this package explicitly defers own-PR squash merge until integrated user-facing acceptance.

Report `Project: X/Y` only from canonical finite state. In-progress/failed work never counts as complete.

## Downstream planning boundary

`docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` may be maintained as a future workflow specification, but this does not start writing. It records later Codex evidence duties, ChatGPT Greek drafting/review, Word/PowerPoint final QA, optional Canva polish and exact `ASSET-*` instructions for user-captured screenshots/GIF/video.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and next-task selection autonomously. Stop only for access/credential, required external-machine evidence, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, or mandatory human application/WP7 approval.

Technical completion, green CI, screenshots, packaged binaries or final evidence do not themselves authorize WP7.