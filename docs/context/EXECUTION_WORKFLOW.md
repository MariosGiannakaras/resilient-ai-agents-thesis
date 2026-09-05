# Execution and Review Workflow

## Operating model

The repository is the durable execution authority. The user may simply say **continue implementation**. The agent recovers state, resumes unfinished work, executes the next dependency-valid scope, performs routine Git/PR/CI work, and stops only at a genuine external or explicit authorization gate.

Conversation/model memory is advisory only. Repository/Git/GitHub evidence overrides it.

## Prompt-free session bootstrap

1. Load `AGENTS.md`.
2. Read `docs/context/WORK_STATE.json`.
3. Read `docs/context/TASKS.md`.
4. Read `docs/context/CURRENT_STATUS.md`.
5. Inspect working-tree status, current branch, recent commits and unpushed/unmerged work.
6. Inspect open PRs, CI/check status and relevant issues when GitHub access exists.
7. Reconcile discrepancies before new implementation.

No separate task prompt is required or authoritative.

## Recovery order

Resume in this order:

1. uncommitted working-tree changes;
2. open implementation PRs with unfinished or ready-to-merge work;
3. pushed unmerged branches with unique required work;
4. valid `WORK_STATE.json` active package;
5. `TASKS.md` `IN_PROGRESS` task;
6. first dependency-valid `READY` task;
7. exact `BLOCKED`/`DEFERRED` external gate.

Do not start new work while recoverable unfinished work exists unless it is objectively blocked and the ledger explicitly permits an independent package.

## Durable checkpoint protocol

`WORK_STATE.json` is the operational resume pointer and must never become a competing task ledger.

Before every material change, update:

- active task/work package;
- phase;
- branch/PR identity when known;
- last durable checkpoint;
- exact next action;
- blockers and pending substeps.

After every material validated checkpoint, update:

- completed substep/checkpoint;
- relevant validation result;
- exact next action;
- any changed blocker/PR/CI state.

Before long/risky operations, quota/context boundaries or session end, create a coherent Git checkpoint and push it when access permits. Substantial work must not exist only in a local working tree or conversation.

Use `scripts/project_checkpoint.py` for structured updates when convenient.

## Branch/PR lifecycle

For non-trivial work:

1. create/recover one coherent branch;
2. record the work package in `WORK_STATE.json` and `TASKS.md` before substantial implementation;
3. commit/push an early coherent checkpoint;
4. open a draft PR as soon as useful remote recovery state exists; convert to normal review when reviewable;
5. continue implementation with checkpoint updates rather than waiting until the end to expose the branch;
6. run targeted checks, then canonical PR CI;
7. review the actual diff/review threads; never self-`APPROVE`;
8. squash-merge when checks/review/repository policy permit;
9. immediately reconcile `WORK_STATE.json` on `main` to the next dependency-valid task or exact external gate.

## Task/document governance

`TASKS.md` is the canonical task/dependency ledger. Started work is `IN_PROGRESS`; completed work is checked; discovered required work receives a stable task ID. `CURRENT_STATUS.md` is compact accepted state. `WORK_STATE.json` is only the active checkpoint/resume pointer.

Every material PR reviews and reconciles affected active docs, status, tasks, tests, workflows and decisions according to `DOCUMENTATION_GOVERNANCE.md`.

## Validation discipline

Use the smallest relevant checks during implementation. GitHub PR CI is the canonical full-suite pre-merge guard. `scripts/validate_project_continuity.py` and `scripts/validate_documentation_consistency.py` are mandatory continuity/documentation guards for material work.

Scientific matrices are not CI test matrices. Required scientific/provenance/configuration state fails closed.

## Scientific/bibliography boundaries

Protocol-v2.1, frozen evidence, T-612 analysis, T-613 assets and accepted T-716 thesis lineage remain immutable except through their declared amendment/revision workflows. Bibliography lifecycle work remains upstream in `MariosGiannakaras/ThesisBibliography`; generated consumer files are never hand-edited.

## Current academic gate after T-010

T-716 is COMPLETE. Unless actual supervisor/reviewer feedback has arrived, T-712 remains DEFERRED. T-713 remains downstream of actual feedback where applicable plus authoritative official metadata/declaration and final Word/submission checks. Do not manufacture work to bypass an external gate.
