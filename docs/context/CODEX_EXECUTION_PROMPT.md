# Codex Execution Prompt

## How to use

This is the single tracked, canonical, directly executable Codex prompt for the thesis project.

After cloning or updating the repository on the actual thesis machine, give Codex only this instruction:

> Read `docs/context/CODEX_EXECUTION_PROMPT.md` and execute it completely.

Do not copy this prompt into another task file and do not delete it after use.

---

Continue work autonomously in the private repository `MariosGiannakaras/resilient-ai-agents-thesis` from the **actual current repository state**.

“Execute it completely” means: advance the project as far as the current environment, permissions, task dependencies, review gates, and accepted scientific workflow validly allow. It does **not** mean attempting the entire thesis in one session, bypassing blockers, starting `BLOCKED`/`DEFERRED` tasks, or reopening completed work.

## Authority and conflict handling

Use these authorities in order for normal execution:

1. `AGENTS.md` — project policy, scientific/technical safeguards, source hierarchy, Git and documentation rules.
2. `docs/context/TASKS.md` — the only concrete task/status/dependency/resume ledger.
3. `docs/context/CURRENT_STATUS.md` — shortest authoritative current-state summary.
4. Current Git state, files, tests, PR/check status, actual machine evidence, and task-specific active specifications.
5. Available session/conversation memory, verified against durable repository evidence.

Do not reconstruct the project from chat history. Do not redo checked/accepted work unless current repository evidence shows a regression or an explicit newer decision reopens it. If active authorities conflict, reconcile them in the same branch/PR before continuing substantive work; do not silently choose whichever wording is convenient.

## Mandatory startup and resume procedure

Run this procedure at the start of **every Codex session**, including after quota exhaustion, interruption, machine restart, or context loss:

1. Inspect `git status`, current branch, recent commits, uncommitted changes, and any relevant open PR/check state.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Inspect `Resume state` and every task marked `IN_PROGRESS`.
4. Use available session memory to understand prior work, then verify it against Git, files, tests, and PR state. Durable repository evidence wins on conflict.
5. Resume the existing `IN_PROGRESS` task before selecting another unless it is genuinely blocked.
6. If no task is in progress, select the first task that is actually `READY` and dependency-valid. Never begin a `BLOCKED` or `DEFERRED` task merely because it appears earlier in the roadmap.
7. Define one active scope: the selected task or one clearly coherent work package needed to satisfy its acceptance condition.
8. Read only the task entry, files it explicitly names, and the relevant task-domain specifications required by `AGENTS.md`. Use repository search before broad reading. Do not reread the entire repository, historical records, or generated bibliography for a bounded task unless the task is explicitly a cross-cutting audit.
9. For substantial work, create or reuse a descriptive branch and mark the task `IN_PROGRESS` with a recoverable `Resume state` no later than the first meaningful checkpoint.

Do not spend the session merely summarizing files already read. After resolving scope and constraints, begin the task.

## Execution loop

For the active task:

1. Confirm its dependencies, acceptance condition, relevant constraints, and required evidence.
2. Form a concise implementation/research plan and execute it without asking the user for information that can be obtained reliably from the repository, actual machine, verified bibliography, prototypes, tests, or authoritative sources.
3. Implement the smallest complete solution that satisfies the task. Do not silently expand scope or freeze scientific choices beyond available evidence.
4. Validate the affected behavior and scientific invariants with relevant tests, fixtures, reference traces, reproducibility checks, or documented visual/end-to-end review as appropriate.
5. Reconcile `TASKS.md`, `Resume state`, and every affected active source-of-truth file in the same change according to `docs/context/DOCUMENTATION_GOVERNANCE.md`.
6. Run the documentation consistency validator, relevant tests, and the full repository checks required before the work is ready for review.
7. Mark the task complete only when its acceptance condition is satisfied and validated. Partial work remains `IN_PROGRESS`.
8. Create/update the PR with scope, task IDs, rationale, validation, scientific/protocol impact, limitations, and deferred work. Do not self-approve or silently bypass the repository review/merge workflow.
9. Start another task only after the current task has reached its valid handoff/completion state and no review, merge, external-machine, or decision gate must be resolved first.

All safeguards in `AGENTS.md` remain mandatory. In particular, never fabricate or silently alter sources, citations, evidence status, runs, data, metrics, progress, logs, figures, tables, results, conclusions, protocol state, or presentation claims.

## Quota and interruption recovery

Assume a session can stop without warning.

- Preserve a recoverable checkpoint after each substantial validated substep when practical, especially before long experiments or a major context switch.
- Intermediate branch commits are allowed as recovery checkpoints; coherent completed work should still normally reach `main` through one squash merge.
- When the next action is not obvious from the commit, update `TASKS.md`/`Resume state` with the task ID, branch/PR, last validated point, tests already run, relevant files, uncommitted work, and exact next action.
- If interruption occurs before that update, the next session must inspect the existing working tree, branch history, PR, tests, and artifacts before deciding what remains.
- Never discard useful uncommitted or checkpointed work merely because the previous session ended.

## Stop and handoff conditions

Do not stop for routine Git operations, task/documentation reconciliation, testing, or decisions resolvable from available evidence.

Stop and report only when continuation genuinely requires one of the following:

- an academic/product choice that cannot be resolved objectively;
- new supervisor/Department guidance available only from the user;
- execution on the actual thesis machine when the current environment is not that machine and the result materially controls the next task;
- an access/credential failure that cannot be repaired from the available environment;
- a safety, legal, privacy, or licensing blocker;
- a frozen-protocol amendment requiring explicit approval;
- review/merge of a completed PR before dependency-valid downstream work can begin.

A completed PR awaiting review is a valid workflow handoff, not permission to start unrelated blocked work.

Before any intentional stop, leave the work recoverable and the repository internally consistent: checkpoint appropriate branch work, update task/resume state, record the exact blocker or handoff, and preserve all valid local results/artifacts.

## Final report

At the end of the session, report only:

- task IDs completed or still `IN_PROGRESS`;
- what was completed;
- branch, PR, merge, and checkpoint commits as applicable;
- tests/validators/checks and their results;
- scientific/architecture decisions accepted or still unfrozen;
- genuine blockers or review gates;
- the exact next task/action from `TASKS.md`;
- any concrete artifact created at a major lifecycle handoff.

This prompt and `docs/context/TASKS.md` remain tracked and must be updated whenever their execution workflow materially changes.