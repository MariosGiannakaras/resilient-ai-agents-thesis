# AGENTS.md

## Mission

Build a scientifically valid, reproducible, realistically completable thesis on resilient AI agents under uncertainty. Keep the research contribution primary; the local application is a polished execution, inspection, analysis, and presentation tool, not a production platform.

This repository is the project source of truth. Conversation/model memory is never authority. `MariosGiannakaras/ThesisBibliography` remains the separate canonical bibliography lifecycle repository; this repository consumes its generated export read-only.

## Prompt-free entrypoint

The user must not need to provide a task prompt. When the user says **"continue implementation"**, "continue", "resume", or equivalent, recover the actual repository state and continue autonomously. Do not ask what to do unless objective repository/external evidence still leaves a genuinely blocking ambiguity.

Repository/Git/GitHub evidence overrides stale or conflicting conversation/model memory.

## Mandatory recovery sequence

Before any implementation decision:

1. read `AGENTS.md`;
2. read `docs/context/WORK_STATE.json` — the operational resume pointer;
3. read `docs/context/TASKS.md` — the canonical task/dependency ledger;
4. read `docs/context/CURRENT_STATUS.md` — compact accepted project state;
5. inspect actual Git state: working tree, current branch, recent commits and unpushed/unmerged work;
6. inspect GitHub state when available: open PRs, their heads, reviews/checks/CI and relevant issues;
7. reconcile any disagreement before new work. Objective Git/GitHub/evidence state wins.

Read deeper documents only for the recovered/selected task. Prefer targeted search and direct dependencies over whole-repository rereads.

## Deterministic task recovery

Resume unfinished work in this order:

1. non-empty working-tree changes that have not been safely checkpointed;
2. an open implementation PR with unfinished/ready-to-merge work;
3. a pushed unmerged branch containing unique required work;
4. the task identified by `WORK_STATE.json` when still valid;
5. any `IN_PROGRESS` task in `TASKS.md`;
6. the first dependency-valid `READY` task;
7. if only `BLOCKED`/`DEFERRED` work remains, stop at the exact external gate and record it durably.

Never start a new package while recoverable unfinished work exists unless the existing package is objectively blocked and the task ledger explicitly allows independent work.

## Mandatory durable checkpoint rule

`docs/context/WORK_STATE.json` is the operational resume pointer. It is not a second task ledger.

- Update it **before every material change** with the active task/work package, phase and exact next action.
- Update it **after every material validated checkpoint** with what completed, validation outcome and exact next action.
- Update it immediately when work becomes blocked, a PR is opened/updated, CI changes the next action, or a task becomes ready to merge/complete.
- Before a long/risky operation, context switch, quota boundary, or session end, create a coherent Git checkpoint and push it when access permits so the state file and work are remotely recoverable.
- Never leave substantial uncommitted/unpushed work with a stale `WORK_STATE.json`.
- Use `python scripts/project_checkpoint.py ...` when convenient; direct edits are acceptable only if the same schema/semantics are preserved.

For non-trivial work, create the branch and first coherent checkpoint early, then **open a draft PR** (or normal PR when already reviewable) as soon as there is a meaningful remote checkpoint. The open PR is part of the recovery surface, not an end-of-task afterthought.

## Task/status authority

- `TASKS.md` is the only detailed task/dependency checklist.
- `CURRENT_STATUS.md` records compact accepted state and external gates.
- `WORK_STATE.json` records only the active operational checkpoint/resume pointer.
- Started unfinished work stays unchecked and `IN_PROGRESS` in `TASKS.md`.
- Material discoveries that create required work get a stable task ID/dependency; do not leave required work only in chat, TODO comments, PR prose or memory.
- In-progress/failed work never counts as complete. Use `X/Y` only from a real finite denominator.

## Completion and merge protocol

A task is complete only after its acceptance criteria and required validation pass.

1. checkpoint the final implementation/result state;
2. reconcile affected active docs/tasks/status/workflows/tests in the same PR;
3. run the narrowest relevant checks, then required PR CI;
4. review the actual diff and unresolved review threads;
5. do not submit an `APPROVE` review on your own PR;
6. if CI/review/policy permit, squash-merge autonomously;
7. immediately reconcile `WORK_STATE.json` on `main` to the next valid task or exact external gate so a new session never sees the merged branch as active work.

Routine Git, PR creation, CI inspection, objective correction and allowed own-PR merge are implementation work, not reasons to ask the user to continue.

## Scientific integrity

- Never fabricate or silently alter sources, citations, evidence status, runs, metrics, data, figures, results, conclusions, protocol state or progress.
- Keep development/tuning/pilot/final evidence separated; never inspect final evidence and silently retune.
- Frozen protocol, raw/finalized results and accepted final evidence are immutable except through an explicit documented amendment/revision path.
- Agents never receive hidden evaluator/regime/change ground truth unless the protocol explicitly permits it.
- Failed/cancelled/interrupted/invalid scientific units remain recorded. Never replace roots/seeds based on outcomes.
- Non-recovery stays explicit; never substitute the horizon as fake recovery time.

## Bibliography boundary

- Do not download/edit primary bibliography sources here.
- `research/bibliography/` changes only through controlled immutable synchronization.
- `research/bibliography/citation-ready/` is the strict automatic formal-citation layer.
- Never invent metadata, DOI values, evidence or citation status.

## Software/provenance invariants

- `src/resilient_agents/` must work without the UI; UI never reimplements scientific logic.
- Filesystem run bundles are evidence source of truth; indexes/databases are rebuildable views.
- Required config/schema/provenance/lifecycle ambiguity fails closed; optional probes may explicitly report unavailable/unsupported.
- Preserve resolved config, seeds, capability snapshot and source commit for scientific runs.
- Avoid speculative platform engineering unrelated to thesis requirements.
- Accepted compute baseline remains native Windows CPython 3.12 via locked `uv`, CPU-supported baseline.

## Testing and CI

Testing is risk-based and proportional.

- Use the smallest targeted checks protecting the changed acceptance/reliability/scientific boundary.
- Prefer strong known-answer/contract/invariant/integration checks over broad duplicate suites.
- Do not turn pilot/final experiment matrices into tests.
- PR CI is the canonical full-suite pre-merge check when available.
- On CI failure inspect the failed step/log and reproduce narrowly; on success record the conclusion without rereading successful logs.
- `scripts/validate_project_continuity.py` must pass for material work.

## Documentation and routing

Active routing:

- operational resume: `docs/context/WORK_STATE.json`
- task/dependencies: `docs/context/TASKS.md`
- compact status: `docs/context/CURRENT_STATUS.md`
- execution/recovery workflow: `docs/context/EXECUTION_WORKFLOW.md`
- documentation governance: `docs/context/DOCUMENTATION_GOVERNANCE.md`
- research/protocol: `docs/research/`, `docs/experiments/`
- UI/application: `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`, `app/README.md`
- thesis/defense: `docs/thesis/`
- decisions: `docs/decisions/DECISION_LOG.md`

Historical files and old conversations are context only. Known stale current-state prose must be reconciled rather than tolerated.
