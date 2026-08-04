# Documentation Governance

## Purpose

Repository documentation is part of the thesis source of truth. A code, research, architecture, workflow, storage, protocol, or task-state change is incomplete if related active documentation still describes the previous state.

## Document classes

### 1. Active source of truth

These files must describe the current repository state and must be reconciled in the same Pull Request as any material change that affects them:

- `AGENTS.md`
- `README.md`
- `docs/context/CURRENT_STATUS.md`
- `docs/context/TASKS.md`
- `docs/context/PROJECT_CONTEXT.md`
- `docs/context/CONFIRMED_REQUIREMENTS.md`
- `docs/context/USER_DECISIONS.md`
- `docs/context/CONSTRAINTS.md`
- `docs/context/OPEN_QUESTIONS.md`
- `docs/context/CONTRADICTIONS.md`
- `docs/context/EXECUTION_WORKFLOW.md`
- `docs/context/IMPLEMENTATION_ROADMAP.md`
- `docs/context/DEFINITION_OF_DONE.md`
- `docs/decisions/DECISION_LOG.md`
- `docs/context/CHANGELOG_CONTEXT.md`
- `docs/context/CODEX_EXECUTION_PROMPT.md`
- active research/protocol/architecture workspaces relevant to the changed subject.

`CURRENT_STATUS.md` is the shortest authoritative current-state summary. `TASKS.md` is the canonical concrete execution checklist/resume ledger. Neither excuses stale statements in other active files.

### 2. Accepted decision/history records

Accepted decisions and historical audits may preserve the state and reasoning that existed when they were written. They must not be silently rewritten to pretend they originally reflected later knowledge.

When a historical file contains statements that are no longer current, add a prominent historical-status notice or supersession pointer if a future reader could mistake it for active guidance.

Examples include:

- `docs/context/FINAL_BOOTSTRAP_AUDIT.md`
- `docs/research/PREIMPORT_*.md`
- superseded decision records.

### 3. Generated or externally owned content

Do not reconcile generated bibliography files by editing them manually. `research/bibliography/` is replaced only through the controlled bibliography synchronization workflow. Source-derived scientific text remains unchanged.

## Task-registry governance

`docs/context/TASKS.md` is the only canonical detailed task checklist. Do not create a competing permanent checklist elsewhere.

Every material PR must review the registry and update it when the PR:

- starts or completes a task;
- blocks or unblocks a task;
- changes dependencies or acceptance conditions;
- discovers required work;
- supersedes/removes work;
- changes the exact next action or active resume state.

Started unfinished work must remain unchecked and be marked `IN_PROGRESS` with enough durable resume information to continue after a session/model-quota interruption. Completed tasks remain checked for auditability.

Session/conversation memory may assist continuation, but durable repository state is the recovery authority. Do not encode task progress only in chat.

## Change-impact matrix

| Change | Files that must be reviewed in the same PR |
|---|---|
| Any material task/work-package change | `TASKS`, resume state, affected active docs, PR metadata/tests |
| Project phase/status/blocker resolved | `CURRENT_STATUS`, `TASKS`, `PROJECT_CONTEXT`, `OPEN_QUESTIONS`, `IMPLEMENTATION_ROADMAP`, `DEFINITION_OF_DONE`, Codex prompt, changelog |
| User requirement/decision | `CONFIRMED_REQUIREMENTS`, `USER_DECISIONS`, `CONSTRAINTS`, `CONTRADICTIONS`, `TASKS` if execution changes, decision log/changelog, affected implementation docs |
| Architecture/stack/storage/runner | `AGENTS`, `README`, architecture docs, `PROJECT_CONTEXT`, requirements/constraints, `TASKS`, decision log, Codex prompt, CI/tests |
| GridWorld/environment | GridWorld research/spec/ADR, current status, `TASKS`, roadmap, open questions, requirements, tests, Codex prompt if execution rules change |
| Models/metrics/protocol | corresponding research/protocol files, current status, `TASKS`, open questions, roadmap, decision log, Codex prompt, tests |
| Bibliography contract/baseline | bibliography integration docs, README/context, current status, `TASKS` when research gates change, decision log/changelog, import validation/workflow; never hand-edit generated evidence |
| Experiment/run data policy | run/provenance docs, constraints, requirements, `TASKS`, `.gitignore`/`.gitattributes`, publisher/tests, decision log/changelog |
| Dashboard workflow | architecture/UI docs, requirements, roadmap, current status, `TASKS`, Codex prompt, tests |
| Thesis/delivery guidance | thesis/university docs, requirements, open questions, roadmap, current status, `TASKS` where relevant |

The matrix is a minimum, not an exhaustive list. Review transitive dependencies when a statement is repeated elsewhere.

## Reconciliation procedure

Before merge:

1. identify what changed semantically, not only which files changed;
2. review `TASKS.md` for affected task state/dependencies/acceptance/resume information;
3. search active documentation for the old assumption, phase, path, status, stack, count, or blocker;
4. update all active occurrences;
5. delete obsolete files that no longer serve a purpose;
6. mark useful historical records explicitly historical rather than leaving ambiguous stale instructions;
7. update decisions/changelog when the change is material;
8. run `scripts/validate_documentation_consistency.py` and the normal repository test suite.

## Prompt rule

There is only one tracked current Codex execution prompt: `docs/context/CODEX_EXECUTION_PROMPT.md`.

It is the directly executable entrypoint for Codex after the repository is cloned or updated. Every session must pass through `TASKS.md` before selecting or resuming work. The prompt must remain state-driven and interruption-resilient: available session memory is used, but work can always be recovered from the registry and Git/repository state.

When workflow, responsibilities, architecture, project state, task-governance rules, or active execution materially changes, the prompt is reviewed and updated in the same PR.

## No silent stale-state policy

Known obsolete statements must not remain in active documentation as a convenience. If the old wording is scientifically or historically useful, move/mark it as historical and point to the current authority.
