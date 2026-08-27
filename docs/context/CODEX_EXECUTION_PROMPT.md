# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

`AGENTS.md` owns always-on policy; repository state beats stale chat memory.

## Active package

Pre-WP7 refinement is governed by DEC-042/044/045/046 and issues #87–#91.

- Use only `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; do not merge early or create a parallel implementation branch.
- Preserve v1.0/final historical evidence and R0 pilot evidence immutably.
- `T-520` is complete. Current primary task: `T-521 READY`; `T-530` is secondary dependency-valid work.
- Never generate v1.1 final evidence for CI/UI convenience.
- `T-511` remains USER_VALIDATION_REQUIRED; all `T-700+` execution is blocked until explicit user approval.

## Startup / resume

1. Inspect `git status`, current branch, recent commits and PR #92/check state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Verify the pinned branch/current task and inspect any IN_PROGRESS work before selecting READY work.
4. Follow canonical order: T-521 → T-522 → T-530 → T-531 → T-532 → T-511 → T-610–T-613 → explicit WP7 gate.
5. Preserve recoverable validated checkpoints and reconcile durable status/issues.

## Current scientific contract

- Candidate agents: F0 frozen Q-learning, C0 continual Q-learning, D0 information-limited Dyna-Q+. R0 is historical only for current v1.1 direction.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48, 32 paired final roots.
- T-521 defines exact D0 `planning_steps`/`kappa` search, four fresh held-out final layouts, fresh final seeds and authoritative candidate schema before tuning evidence is used.
- Multiple approved development/tuning configurations require stable identity/provenance and multiple predefined roots. No best-run/seed/final cherry-picking. F0/C0 remain fixed unless explicitly reopened; final retained settings freeze pre-final.
- Conditions: `nominal`, `action-remap-2-swap`, `action-remap-4-cycle`, action failure 1/8 and 1/4, observation corruption 1/8 and 1/4.
- Primary: cumulative deficit, immediate degradation, terminal gap/performance. Recovery secondary/sensitivity. Paired effects + 95% CIs + explicit n/layout views; no composite/post-hoc favorable threshold.
- Never expose evaluator-only state/action/change/disturbance/regime truth to agents.

## Application / UX contract

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services; no active Streamlit/React/Vite/Node stack.
- T-530 provides truthful active-run DTOs/events/history/resources, read-only live GridWorld and capability-based controls.
- T-531 handles agent **and resolved configuration/settings identity**, repeated roots, fixed-vs-tunable explanations and compatible live/final comparisons.
- Plotly = stored/final figures; ECharts = real LIVE/PROVISIONAL telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- Novice-first compact UX: plain labels, secondary IDs, accurate tooltips/help, units/consequences, progressive disclosure, resolved-config review, semantic icon+text+color states and actionable errors/empty states.
- Purposeful GridWorld/chart/status animation is presentation-only and never changes timing/actions/seeds/RNG or fabricates progress/replay.
- `run_app.bat` remains checkout launcher; final Windows delivery is validated NiceGUI/PyInstaller `onedir + windowed`.
- After acceptance, approved experiments run directly from the desktop app on the validated thesis machine; Codex/console is not needed merely to execute a frozen configuration. GitHub remains source-of-truth/CI/evidence coordination, not automatically the final stochastic compute host.

## Validation and Git

For each **one bounded scope**: verify dependencies/acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, review the actual diff, and reconcile docs/issues.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle truthfulness and representative render/native checks. No arbitrary coverage, broad test-expansion project or pilot/final matrices in CI. PR CI is the canonical full-suite guard.

Do not submit an `APPROVE` review on your own PR. The normal workflow may permit an **own-PR squash merge**, but this package explicitly defers own-PR squash merge until integrated user-facing acceptance.

Report `Project: X/Y` only from canonical finite state. In-progress/failed work never counts as complete.

`docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` is future planning only; it does not authorize writing.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and next-task selection autonomously. Stop only for access/credential, required external-machine evidence, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, or mandatory human application/WP7 approval.

Technical completion, green CI, screenshots, packaged binaries or final evidence do not authorize WP7.