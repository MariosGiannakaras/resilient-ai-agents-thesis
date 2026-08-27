# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

`AGENTS.md` owns always-on policy; repository state beats stale chat memory.

## Active package

Pre-WP7 refinement is governed by DEC-042/044/045/046/047 and issues #87–#91.

- Use only `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; do not merge early or create a parallel implementation branch.
- Preserve v1.0/final historical evidence and R0 pilot evidence immutably.
- `T-520` and `T-523` are complete. Current primary task: **`T-521 READY`**. `T-530` remains secondary dependency-valid work; `T-522` is blocked on T-521.
- Never generate or inspect v1.1 final outcomes for CI/UI/protocol-selection convenience.
- `T-511` remains USER_VALIDATION_REQUIRED; all `T-700+` execution is blocked until explicit user approval.

## Startup / resume

1. Inspect `git status`, current branch, recent commits and PR #92/check state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Inspect/resume IN_PROGRESS work before READY work.
4. Follow canonical scientific order: **T-521 → T-522**; then runtime/UI dependencies; never bypass gates.
5. Preserve recoverable validated checkpoints and reconcile durable status/issues.

## Current scientific contract

The thesis compares resilient AI agent strategies under uncertainty/change. GridWorld is the controlled experimental/visualization testbed, not the thesis subject.

Validated main strategies:
- **Fixed Q-Learning** — historical F0; common learned nominal checkpoint, no post-change updates.
- **Adaptive Q-Learning** — historical C0; continual off-policy Q updates.
- **SARSA** — on-policy continual model-free TD control.
- **Dyna-Q** — empirical learned-model planning over experienced state-action pairs; no Dyna-Q+ recency/untried-action bonus.
- **Dyna-Q+** — historical D0; learned model + planning + recency-directed re-exploration.

T-523 validated deterministic/serializable SARSA and Dyna-Q, episode persistence, five-strategy runner/config identities, the Dyna-Q/Dyna-Q+ mechanism contrast, Random Agent reference fixture and bounded matrix-size feasibility. PR CI run 396 passed the complete 143-test suite plus documentation/JSON/compile/lock/bibliography checks.

Random Agent and any nominal/fully-informed planner are clearly labelled reference fixtures, never equivalent fair-ranked agents. Historical R0 remains immutable diagnostic/negative pilot evidence; a redesigned Robust Planner becomes a conditional sixth comparator only if its explicit T-521/T-522 non-final nominal-viability/fairness/runtime gate passes.

All five scientific agents receive only agent-visible observations, intended actions, rewards and lifecycle information. Never expose evaluator-only executed action, disturbance/change flags, regime or true state.

Preserve Fixed/Adaptive Q-Learning alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and current target 32 paired final roots unless an explicit evidence-backed amendment changes the matrix.

T-521 must define **before selection evidence is examined**: authoritative candidate-v1.1 schema; exact bounded SARSA fairness-tuning and Dyna/Dyna-Q+ planning surfaces; four fresh held-out final layouts; fresh precommitted final seed bank; structural remap IDs; stable configuration identity/provenance; paired effects/95% CIs/explicit n/layout aggregation; primary cumulative deficit/immediate degradation/terminal performance and secondary/sensitivity recovery. No composite score, best-seed selection, best-final switching or post-hoc favorable threshold.

T-522 then runs only bounded non-final tuning/pilot evidence and freezes/amends/rejects strategies/settings before final outcomes. Actual Dyna planning runtime is measured there; the current 888,832-episode matrix accounting is feasibility only, not a runtime guarantee.

## Application / UX contract

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services; no active Streamlit/React/Vite/Node stack.
- Primary UI concept is **Agent strategy**. Ordinary users see full human-readable names plus one-sentence explanations/mechanism badges. F0/C0/D0/schema/config hashes appear only under **Technical details / Reproducibility**.
- Use the same human-readable names in New Experiment, Runs, Compare, chart legends, screenshots and thesis-facing exports.
- T-530 provides truthful active-run DTOs/events/history/resources, read-only live GridWorld and capability-based controls.
- T-531 handles strategy/configuration/settings identity, repeated roots, fixed-vs-tunable explanations and compatible live/final comparisons.
- Plotly = stored/final figures; ECharts = real LIVE/PROVISIONAL telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- Novice-first compact UX: plain labels, accurate tooltips/help, units/consequences, progressive disclosure, resolved-config review, semantic icon+text+color states and actionable errors/empty states.
- GridWorld/chart/status animation is presentation-only and never changes timing/actions/seeds/RNG or fabricates progress/replay.
- `run_app.bat` remains checkout launcher; final Windows delivery is validated NiceGUI/PyInstaller `onedir + windowed`.

## Validation and Git

For each **one bounded scope**: verify dependencies/acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, review the actual diff, and reconcile docs/issues.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle truthfulness and representative render/native checks. No arbitrary coverage project or pilot/final matrices in CI. PR CI is the canonical full-suite guard.

Do not submit an `APPROVE` review on your own PR. The normal workflow may permit an **own-PR squash merge**, but this package explicitly defers own-PR squash merge until integrated user-facing acceptance.

Report `Project: X/Y` only from canonical finite state. In-progress/failed work never counts as complete.

`docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` is future planning only; it does not authorize writing.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and next-task selection autonomously. Stop only for access/credential, required external-machine evidence, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, or mandatory human application/WP7 approval.

Technical completion, green CI, screenshots, packaged binaries or final evidence do not authorize WP7.