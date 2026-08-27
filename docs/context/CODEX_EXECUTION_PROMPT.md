# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

`AGENTS.md` owns always-on policy; repository state beats stale chat memory.

## Active package

Pre-WP7 refinement is governed by DEC-042/044/045/046/**047** and issues #87–#91.

- Use only `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; do not merge early or create a parallel implementation branch.
- Preserve v1.0/final historical evidence and R0 pilot evidence immutably.
- `T-520` is complete. Current primary task: **`T-523 READY`**. `T-521` is blocked on T-523; `T-530` remains secondary dependency-valid work.
- Never generate v1.1 final evidence for CI/UI convenience.
- `T-511` remains USER_VALIDATION_REQUIRED; all `T-700+` execution is blocked until explicit user approval.

## Startup / resume

1. Inspect `git status`, current branch, recent commits and PR #92/check state.
2. Read only `AGENTS.md`, `docs/context/TASKS.md`, `docs/context/CURRENT_STATUS.md`.
3. Inspect/resume IN_PROGRESS work before READY work.
4. Follow canonical scientific order: **T-523 → T-521 → T-522**; then runtime/UI dependencies; never bypass gates.
5. Preserve recoverable validated checkpoints and reconcile durable status/issues.

## Current scientific contract

The thesis compares resilient AI agent strategies under uncertainty/change. GridWorld is the controlled experimental/visualization testbed, not the thesis subject.

Main candidate strategies after DEC-047:

- **Fixed Q-Learning** — historical technical identity F0; common learned nominal checkpoint, no post-change updates.
- **Adaptive Q-Learning** — historical C0; same checkpoint/base config, continual off-policy Q updates.
- **SARSA** — new on-policy continual model-free strategy; implement/validate in T-523.
- **Dyna-Q** — new learned-model/planning strategy without recency bonus; implement/validate in T-523.
- **Dyna-Q+** — historical D0; learned model + planning + recency-directed re-exploration.

Random Agent and nominal/fully-informed planner are optional clearly labelled reference fixtures, never equivalent fair-ranked agents. Historical R0 remains immutable diagnostic/negative pilot evidence; a redesigned Robust Planner becomes a conditional sixth comparator only if its explicit non-final nominal-viability/fairness/runtime gate passes.

All five scientific agents receive only agent-visible observations, intended actions, rewards and lifecycle information. Never expose evaluator-only executed action, disturbance/change flags, regime or true state.

Preserve Fixed/Adaptive Q-Learning alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and current target 32 paired final roots unless an explicit later evidence-backed amendment changes the matrix.

T-523 must add deterministic/versioned SARSA and plain Dyna-Q, exact-update/determinism/serialization/information-boundary tests, runner/config identities and bounded runtime estimate. SARSA may receive only a small predeclared fairness-relevant non-final tuning surface. Dyna-Q/Dyna-Q+ should share model/planning machinery and matched planning-step budgets where appropriate, with Dyna-Q explicitly no-recency-bonus.

T-521 then owns the authoritative five-agent candidate schema, small predeclared tuning surfaces, four fresh held-out final layouts, fresh final seed bank, structural remap IDs, stable configuration identity/provenance, paired effects/95% CIs/explicit n/layout views, primary cumulative deficit/immediate degradation/terminal performance and secondary/sensitivity recovery. No composite score, best-seed selection or post-hoc favorable threshold.

## Application / UX contract

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services; no active Streamlit/React/Vite/Node stack.
- Primary UI concept is **Agent strategy**. Ordinary users see the five full human-readable names plus one-sentence explanations/mechanism badges. F0/C0/D0/schema/config hashes appear only under **Technical details / Reproducibility**.
- Use the same human-readable names in New Experiment, Runs, Compare, chart legends, screenshots and thesis-facing exports.
- T-530 provides truthful active-run DTOs/events/history/resources, read-only live GridWorld and capability-based controls.
- T-531 handles agent/configuration/settings identity, repeated roots, fixed-vs-tunable explanations and compatible live/final comparisons.
- Plotly = stored/final figures; ECharts = real LIVE/PROVISIONAL telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- Novice-first compact UX: plain labels, accurate tooltips/help, units/consequences, progressive disclosure, resolved-config review, semantic icon+text+color states and actionable errors/empty states.
- Purposeful GridWorld/chart/status animation is presentation-only and never changes timing/actions/seeds/RNG or fabricates progress/replay.
- `run_app.bat` remains checkout launcher; final Windows delivery is validated NiceGUI/PyInstaller `onedir + windowed`.
- After acceptance, approved experiments run directly from the desktop app on the validated thesis machine; Codex/console is not needed merely to execute frozen configurations.

## Validation and Git

For each bounded scope: verify dependencies/acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, review the actual diff, and reconcile docs/issues.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle truthfulness and representative render/native checks. No arbitrary coverage project or pilot/final matrices in CI. PR CI is the canonical full-suite guard.

Do not submit an `APPROVE` review on your own PR. The normal workflow may permit an **own-PR squash merge**, but this package explicitly defers own-PR squash merge until integrated user-facing acceptance.

Report progress only from canonical finite state. In-progress/failed work never counts as complete.

`docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` is future planning only; it does not authorize writing.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and next-task selection autonomously. Stop only for access/credential, required external-machine evidence, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, or mandatory human application/WP7 approval.

Technical completion, green CI, screenshots, packaged binaries or final evidence do not authorize WP7.