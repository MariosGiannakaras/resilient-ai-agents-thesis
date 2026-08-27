# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

`AGENTS.md` owns always-on policy; repository evidence beats stale chat/session memory.

## Active package

Pre-WP7 refinement is governed by DEC-042/044/045/046/047 and issues #87–#91.

- Use only `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; do not merge early or create a parallel implementation branch.
- Preserve v1.0/final historical evidence and R0 pilot evidence immutably.
- `T-520`, `T-523`, `T-521`, `T-530`, `T-531`, and `T-532` are complete. Current scientific task: **`T-522 READY`** only on the validated thesis machine. Otherwise the active repository task is **`T-511 USER_VALIDATION_REQUIRED`**.
- Never generate or inspect v1.1 final outcomes for CI/UI/protocol-selection convenience.
- `T-511` remains USER_VALIDATION_REQUIRED; all `T-700+` execution is blocked until explicit user approval.

## Startup / resume

1. Inspect `git status`, current branch, recent commits and PR #92/check state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Inspect/resume IN_PROGRESS work before READY work.
4. Follow the ledger: attempt T-522 only where validated thesis-machine evidence is available; otherwise wait for T-511 human acceptance without inventing a new gate or branch.
5. Preserve recoverable validated checkpoints and reconcile durable status/issues.

## Current scientific contract

The thesis compares resilient AI agent strategies under uncertainty/change. GridWorld is the controlled experimental/visualization testbed, not the thesis subject.

Main strategies:
- **Fixed Q-Learning** — historical F0; learned nominal checkpoint, no post-change updates.
- **Adaptive Q-Learning** — historical C0; continual off-policy Q updates.
- **SARSA** — on-policy continual model-free TD control.
- **Dyna-Q** — empirical learned-model planning over experienced pairs; no Dyna-Q+ recency/untried-action mechanism.
- **Dyna-Q+** — historical D0; learned model + planning + recency-directed re-exploration.

Random Agent and any fully-informed planner are reference fixtures, never fair-ranked agents. Historical R0 remains negative/diagnostic pilot evidence; redesigned Robust Planner is conditional on its explicit non-final viability/fairness/runtime gate.

All five agents receive only agent-visible observations, intended actions, rewards and lifecycle information. Never expose evaluator-only executed action, disturbance/change flags, regime or true state.

T-521 is validated by PR CI run **409**. Candidate `protocol-v1.1` preserves Fixed/Adaptive Q alpha `.5`, gamma `.96875`, epsilon `.125`, 512 training episodes/layout and 16/32 evaluation blocks; defines bounded SARSA/Dyna/Dyna-Q+ configuration IDs; four fresh held-out final layouts; fresh/disjoint seeds with 32 final roots; seven structural single-factor conditions; protocol/config SHA-256 provenance; complete-root/no-best-seed tuning; primary cumulative deficit/immediate degradation/terminal performance; recovery secondary/sensitivity; and root-blocked equal-layout paired effects with deterministic 95% percentile-bootstrap CIs. Candidate lifecycle permits DEVELOPMENT/TUNING only and rejects PILOT/FINAL.

T-522 may use only the predeclared non-final matrix. Retain failures/poor/non-recovery outcomes, measure Dyna planning cost on the validated thesis machine, apply the fixed selection/tie rules, resolve the optional Robust Planner gate explicitly, and freeze/amend/reject before any final reserve is accessed. Do not substitute GitHub-hosted CI for required physical-machine scientific evidence.

## Application / UX contract

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services; no active Streamlit/React/Vite/Node stack.
- Primary UI concept is **Agent strategy** with full names, concise explanations and mechanism badges. Technical IDs/hashes appear only under **Technical details / Reproducibility**.
- T-530 provides truthful active-run DTOs/events/history/resources, read-only live GridWorld and capability-based controls.
- T-531 completed approved strategy/configuration/repetition selection, truthful live/history views, stored-evidence Compare/Artifacts and novice-first self-explanatory UX. Issue #90 is 9/9 and closed.
- T-532 completed accepted root screenshots, bounded browser/CI capture, actual Windows native-window behavior and `onedir + windowed` packaging validation. Issue #91 is 6/6 and closed.
- Plotly = stored/final figures; ECharts = LIVE/PROVISIONAL telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- Use accurate tooltips/help, units/consequences, progressive disclosure, resolved-config review, semantic icon+text+color states, actionable errors/empty states and restrained micro-interactions.
- Animation is presentation-only and never changes timing/actions/seeds/RNG or fabricates progress/replay.
- `run_app.bat` remains checkout launcher; final Windows delivery is validated NiceGUI/PyInstaller `onedir + windowed`.

## Validation and Git

For each **one bounded scope**: verify dependencies/acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, review the actual diff, and reconcile docs/issues.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle truthfulness and representative render/native checks. No arbitrary coverage project or scientific pilot/final matrices in CI. PR CI is the canonical full-suite guard.

Do not submit an `APPROVE` review on your own PR. The normal workflow may permit an **own-PR squash merge**, but this package defers own-PR squash merge until integrated user-facing acceptance.

Report `Project: X/Y` only from canonical finite state. In-progress/failed work never counts as complete.

`docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` is future planning only; it does not authorize writing.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and next-task selection autonomously. Stop only for access/credential, required external-machine evidence, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, or mandatory human application/WP7 approval.

Technical completion, green CI, screenshots, packaged binaries or final evidence do not authorize WP7.
