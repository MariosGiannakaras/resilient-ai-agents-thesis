# Codex Execution Prompt

## User entrypoint

After cloning/updating the repository on the actual thesis machine, give Codex only this Goal-mode command:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent work package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, squash merge, task reconciliation, and selection of the next READY task as work to perform—not reasons to stop. Continue until the project lifecycle is complete or continuation genuinely requires user/supervisor/external input that cannot be resolved from repository evidence and accepted rules. Never bypass BLOCKED or DEFERRED work, fabricate evidence, or cross an explicit external approval gate.`

This file is the single tracked execution bootstrap. Do not copy it into disposable task prompts. A separate startup `/plan` is not required because the repository already contains the accepted roadmap, dependency ledger, and task acceptance conditions; use plan mode only when a specific task has a genuinely unclear approach that benefits from investigation before editing.

## Execute from repository state

Goal mode is the persistent long-horizon wrapper. Within it, work **one bounded scope at a time**: one task or one genuinely coherent adjacent task package. After each validated scope, resolve routine repository/PR/CI/merge work with available permissions, reconcile the task ledger, then continue automatically with the next dependency-valid `READY` work.

“Execute it completely” means continuing through the canonical project lifecycle as far as the actual evidence and accepted rules permit. It does not mean treating the whole thesis as one undifferentiated edit, bypassing `BLOCKED`/`DEFERRED` dependencies, reopening accepted work without evidence, or inventing missing academic/external input.

Evidence-backed research, architecture, implementation, test, and ADR decisions that the active task can resolve from its acceptance criteria and available sources are normal autonomous work. Do not turn them into artificial user gates merely because they involve scientific or architectural judgment. Pause only when the controlling task/specification explicitly requires external/user/supervisor approval or the choice cannot be resolved objectively from accepted evidence and constraints.

`AGENTS.md` contains the always-on project rules and routing map. Do not duplicate or reconstruct those rules from chat history.

## Startup / resume

1. Inspect `git status`, branch, recent commits, uncommitted work, and relevant open PR/check state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Inspect `Resume state` and any `IN_PROGRESS` task. Repository/Git evidence wins if memory or stale handoff prose conflicts with actual merged PR/check state; reconcile stale state before continuing.
4. Resume valid `IN_PROGRESS` work first. Otherwise select the first dependency-valid `READY` task. Never start `BLOCKED`/`DEFERRED` work just because it is next numerically.
5. Define one bounded scope: one task or one genuinely coherent adjacent task package permitted by `AGENTS.md`.
6. Read only the task entry, explicitly referenced files, and the smallest relevant active specifications/evidence. Search before broad reading.
7. For substantial work, create/reuse a descriptive branch and make the task recoverable in `TASKS.md` no later than the first meaningful checkpoint.

Do not spend the session summarizing context already established. Once scope/dependencies are clear, execute.

## Execution contract

For each active bounded scope:

1. Confirm dependencies, acceptance condition, constraints, and evidence needed.
2. Implement/research the smallest complete solution that satisfies the acceptance condition. Follow all scientific, bibliography, provenance, UI, lifecycle, and scope rules routed by `AGENTS.md`.
3. Fail closed on invalid/ambiguous required state; do not fabricate fallbacks or apparent success.
4. Validate with the smallest relevant deterministic checks during implementation.
5. Keep `TASKS.md`, `Resume state`, and affected active source-of-truth docs consistent in the same change.
6. Before PR/update, run the documentation consistency validator and directly affected targeted checks. Do not duplicate an available PR full-suite CI run locally.
7. Mark a task complete only when its acceptance condition is actually satisfied and validated; otherwise keep it `IN_PROGRESS` or correctly blocked.
8. Create/update a coherent PR with task IDs, scope/rationale, validation, scientific/protocol impact, and deferred/excluded work.
9. Use GitHub PR CI as the canonical full-suite pre-merge guard when available. On success, record the conclusion without rereading logs. On failure, inspect only the failing step/log, reproduce narrowly when useful, fix, and let CI verify the whole repository again.
10. Review the actual diff before merge. Do not submit an `APPROVE` review on your own PR. When CI is green, the diff is sound, no unresolved review finding exists, and repository policy does not require a distinct human approval, squash-merge with available permissions. A routine own-PR merge is not “self-approval”; it is an execution step after objective review. If branch protection or an explicit task/policy genuinely requires another human's approval, that external approval is a real gate.
11. After merge, synchronize the local repository to the resulting `main`, verify task/status state against the merge, select the next dependency-valid task, and continue under the same active goal.

## Progress and quota discipline

- Give concise user updates after scope is set and at meaningful completed/validated checkpoints or genuine blockers—not after routine commands.
- Use `X/Y` only for objective finite denominators. `Project: X/Y` comes from checked/all canonical `T-*` entries in `TASKS.md`; add the current work-package/deliverable count when useful. Add active-task `X/Y` only if real finite substeps exist.
- In-progress/failed work never counts as complete. Do not create another tracker or invented percentage.
- Prefer targeted search/ranges and bounded outputs; avoid broad repository/corpus dumps and unnecessary successful-log reading.
- Preserve recoverable checkpoint commits/state after substantial validated substeps when practical, especially before long experiments or major context switches.
- Do not clear or declare the persistent goal complete merely because one task, branch, PR, CI run, merge, or work package completed while another dependency-valid scope can proceed.

## Stop conditions

Continue without asking the user for routine repository, Git, PR, CI, diff review, merge, validation, evidence-retrieval, task-selection, research synthesis, implementation, or next-task work that can be resolved from available sources and accepted rules.

Pause/stop Goal mode and report only when continuation genuinely requires one of these:

- a non-objective academic/product choice that the task/specification reserves for the user;
- new supervisor/Department guidance or private input available only from the user and required now;
- execution on another physical machine when the current environment cannot provide evidence required by the next task;
- an unrecoverable access/credential, safety, privacy, legal, or licensing blocker;
- an explicit external approval required by a frozen-protocol amendment, repository protection, or controlling task/specification;
- all canonical tasks that can proceed without one of the above external inputs are complete.

A task boundary, successful validation, PR creation, green CI, objective self-review, own-PR squash merge, evidence-backed research/ADR decision, or newly unblocked next task is **not** by itself a stop condition.

Before an intentional pause/stop, leave branch/task/resume state internally consistent and recoverable.

## Final report

Report only:

- final objective progress line;
- completed/`IN_PROGRESS` task IDs;
- material work completed;
- branch/PR/merge/checkpoint state;
- validators/tests/CI conclusions;
- accepted or still-unfrozen scientific/architecture decisions;
- genuine external blockers/approval gates;
- exact next task/action from `TASKS.md`;
- major artifact produced, if any.
