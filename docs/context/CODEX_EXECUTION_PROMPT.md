# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, documentation reconciliation, and next-task selection as work to perform, not reasons to stop. Recover actual repository/Git/GitHub/evidence state before acting. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or continue a superseded UI branch.`

Repository/Git/GitHub/evidence state beats stale session memory or stale prose.

## Current package

Protocol-v2.1 scientific design and pre-final readiness hardening are complete. DEC-058 remains immutable historical protocol-v2.0 freeze authority; DEC-060 plus `configs/protocols/protocol-v2.1-final.json` are current pre-execution authority.

Current facts:

- retained methods are Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
- final scientific dimensions/configurations/statistics are frozen;
- Study backend, temporal/recovery/direct-comparison evidence contracts, validation, analysis and deterministic exports are implemented;
- the generic Study service denies confirmatory/final execution without the separate explicit authorization token;
- `final_reserve_access=false`; no protocol-v2.1 final outcome has been generated or inspected;
- PySide6 / Qt 6 Widgets is the current application architecture under DEC-059;
- the paused/pre-v2.1 UI implementation is not the implementation base for continuation;
- standalone Windows packaging remains deferred until after the thesis.

## Startup / resume

1. Inspect `git status`, current branch, staged/unstaged/untracked work, recent commits, upstream/ahead-behind state, remote head, open PR and CI state. Resume valid `IN_PROGRESS` work before selecting new work.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Preserve unique interrupted work and recover objective state before acting; never recreate completed work because an old note says it is incomplete.
4. Read only task-specific decisions/specifications needed for the recovered active task.
5. Work on one bounded scope at a time; a coherent adjacent package is allowed only when no explicit approval/scientific gate lies between its parts.

## Clean UI restart

When the active goal is the application rebuild:

1. start from a fresh branch from current `main`; do not continue an old paused UI branch/worktree;
2. additionally read DEC-059, DEC-060, `configs/protocols/protocol-v2.1-final.json`, `docs/research/RQ_EVIDENCE_TRACEABILITY.md`, and relevant `docs/architecture/` UI guidance;
3. audit `src/resilient_agents/desktop/` before editing: preserve current UI-neutral read-model, Study/evidence adapter, provenance and execution-policy contracts; presentation widgets/windows/pages/styles may be replaced from scratch;
4. derive UI behavior from current Study/evidence contracts, not pre-v2.1 assumptions or historical screenshots;
5. use DEVELOPMENT/synthetic fixtures for implementation tests/screenshots unless separately validated real evidence is read-only;
6. never calculate scientific thresholds, root reductions, estimands or conclusions inside Qt presentation code;
7. never access or authorize the final reserve from the UI.

The UI must be novice-first, self-explanatory, compact and coherent. Use plain-language primary labels, progressive disclosure for technical IDs/provenance, and actionable empty/loading/disabled/warning/error/locked states. Motion must never fabricate progress or data.

## Scientific boundary to preserve

- Phase A independently trains each retained method under the common semantic task/information contract and actual-environment-interaction fairness budget.
- Phase B branches exact scientific state into FN/FD/AN/AD.
- Root is the independent unit; layouts/episodes/probes/windows are repeated observations.
- RQ2 primary adaptation benefit is `(FN-FD)-(AN-AD)`.
- RQ3 uses AN versus AD passive 32-interaction windows over horizon 256, primary tolerance 0.10, sensitivity 0.05/0.20, two-window stable recovery and right-censoring with `recovery_time=null` for non-recovery.
- Direct method contrasts are root-paired after equal layout reduction; pointwise Student-t intervals use the predeclared critical value for actual independent-root count.
- Scientific failures remain outcomes; roots/seeds are never replaced from outcomes.

## Validation and Git

For each bounded scope, implement the smallest complete solution, run targeted deterministic checks, inspect the diff, reconcile affected active docs/tests/workflows, then use PR CI as the canonical full-repository guard. Fix actual failures narrowly rather than expanding test scope for reassurance.

Do not submit an `APPROVE` review on your own PR. When CI is green, scope/evidence/docs are sound and repository policy permits it, perform the routine own-PR squash merge and continue.

Report `Project: X/Y` only from a real canonical finite denominator in `TASKS.md`. In-progress/failed work never counts as complete.

## Final-experiment gate

Repository cleanup, UI implementation, CI, screenshots and synthetic smoke do not authorize the final scientific experiment. Do not enable final-reserve access, inspect final outcomes, run the final protocol-v2.1 matrix, tune from final identities or begin Results/Discussion writing. Stop at the separate explicit authorization gate if final execution becomes the next scientific action.

## Stop conditions

Continue routine Git/GitHub work, implementation, CI diagnosis, objective review, own-PR squash merge, reconciliation and dependency-valid next-task selection autonomously. Stop only when the next action genuinely requires explicit user/supervisor/external-machine/scientific authorization or another non-resolvable external boundary.
