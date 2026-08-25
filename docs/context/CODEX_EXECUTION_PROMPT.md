# Codex Execution Prompt

## User entrypoint

After cloning/updating the repository on the actual thesis machine, give Codex only this Goal-mode command:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Continue autonomously across successive dependency-valid tasks and coherent work packages while the next work can proceed without a genuine user, external-machine, scientific, protocol, access, or review gate. Treat the goal as complete only when no dependency-valid work remains before such a gate. Validate and checkpoint each bounded scope; never bypass BLOCKED or DEFERRED work or accepted gates.`

This file is the single tracked execution bootstrap. Do not copy it into disposable task prompts. A separate startup `/plan` is not required because the repository already contains the accepted roadmap, dependency ledger, and task acceptance conditions; use plan mode only when a specific task has a genuinely unclear approach that benefits from investigation before editing.

## Execute from repository state

Goal mode is the persistent long-horizon wrapper. Within it, work **one bounded scope at a time**: one task or one genuinely coherent adjacent task package. After a scope is validated and any required review/merge gate has resolved, re-read the task state and continue automatically with the next dependency-valid `READY` work instead of stopping merely because one task finished.

“Execute it completely” therefore means continue through successive valid scopes as far as the environment, permissions, evidence, review gates, and accepted workflow allow. It does not mean treating the whole thesis as one undifferentiated task, bypassing `BLOCKED`/`DEFERRED` work, reopening accepted work without evidence, or crossing a scientific/user/external-machine/protocol/review gate.

`AGENTS.md` contains the always-on project rules and routing map. Do not duplicate or reconstruct those rules from chat history.

## Startup / resume

1. Inspect `git status`, branch, recent commits, uncommitted work, and relevant open PR/check state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Inspect `Resume state` and any `IN_PROGRESS` task. Repository/Git evidence wins if memory conflicts.
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
10. Review the actual diff before merge. Do not self-approve or bypass a genuine review/decision gate.
11. When the scope is fully resolved and no gate requires external input, select the next dependency-valid task and continue under the same active goal.

## Progress and quota discipline

- Give concise user updates after scope is set and at meaningful completed/validated checkpoints, gates, or blockers—not after routine commands.
- Use `X/Y` only for objective finite denominators. `Project: X/Y` comes from checked/all canonical `T-*` entries in `TASKS.md`; add the current work-package/deliverable count when useful. Add active-task `X/Y` only if real finite substeps exist.
- In-progress/failed work never counts as complete. Do not create another tracker or invented percentage.
- Prefer targeted search/ranges and bounded outputs; avoid broad repository/corpus dumps and unnecessary successful-log reading.
- Preserve recoverable checkpoint commits/state after substantial validated substeps when practical, especially before long experiments or major context switches.
- Do not clear or declare the persistent goal complete merely because one bounded task, branch, PR, or work package completed while another dependency-valid scope can proceed without a genuine gate.

## Stop conditions

Continue without asking the user for routine repository, Git, validation, evidence-retrieval, task-selection, or next-task work that can be resolved from available sources.

Pause/stop Goal mode and report only when continuation genuinely requires one of these:

- a non-objective academic/product choice;
- new supervisor/Department guidance or private input available only from the user;
- execution on another physical machine when the current environment cannot provide evidence required by the next task;
- an unrecoverable access/credential, safety, privacy, legal, or licensing blocker;
- an explicit frozen-protocol amendment/approval;
- a PR/review/merge or other external gate that must resolve before dependency-valid downstream work;
- no remaining dependency-valid work before one of the above gates.

A routine task boundary, successful validation, completed branch, or newly unblocked next task is **not** by itself a stop condition.

Before an intentional pause/stop, leave branch/task/resume state internally consistent and recoverable.

## Final report

Report only:

- final objective progress line;
- completed/`IN_PROGRESS` task IDs;
- material work completed;
- branch/PR/merge/checkpoint state;
- validators/tests/CI conclusions;
- accepted or still-unfrozen scientific/architecture decisions;
- genuine blockers/review gates;
- exact next task/action from `TASKS.md`;
- major artifact produced, if any.
