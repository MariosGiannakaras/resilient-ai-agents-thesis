# Documentation Governance

## Purpose

Repository documentation is part of the thesis source of truth. A code, research, architecture, workflow, storage, or protocol change is incomplete if related active documentation still describes the previous state.

## Document classes

### 1. Active source of truth

These files must describe the current repository state and must be reconciled in the same Pull Request as any material change that affects them:

- `AGENTS.md`
- `README.md`
- `docs/context/CURRENT_STATUS.md`
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
- the current Codex execution prompt
- active research/protocol/architecture workspaces relevant to the changed subject.

`CURRENT_STATUS.md` is the shortest authoritative current-state summary. It does not excuse stale statements in other active files.

### 2. Accepted decision/history records

Accepted decisions and historical audits may preserve the state and reasoning that existed when they were written. They must not be silently rewritten to pretend they originally reflected later knowledge.

When a historical file contains statements that are no longer current, add a prominent historical-status notice or supersession pointer if a future reader could mistake it for active guidance.

Examples include:

- `docs/context/FINAL_BOOTSTRAP_AUDIT.md`
- `docs/research/PREIMPORT_*.md`
- superseded decision records.

### 3. Generated or externally owned content

Do not reconcile generated bibliography files by editing them manually. `research/bibliography/` is replaced only through the controlled bibliography synchronization workflow. Source-derived scientific text remains unchanged.

### 4. Local one-shot task files

`CODEX_TASK.md` and `.codex-task.md` at repository root are git-ignored local files. They may be copied from the tracked current Codex execution prompt and deleted after use without creating Git history.

## Change-impact matrix

| Change | Files that must be reviewed in the same PR |
|---|---|
| Project phase/status/blocker resolved | `CURRENT_STATUS`, `PROJECT_CONTEXT`, `OPEN_QUESTIONS`, `IMPLEMENTATION_ROADMAP`, `DEFINITION_OF_DONE`, Codex prompt, changelog |
| User requirement/decision | `CONFIRMED_REQUIREMENTS`, `USER_DECISIONS`, `CONSTRAINTS`, `CONTRADICTIONS`, decision log/changelog, affected implementation docs |
| Architecture/stack/storage/runner | `AGENTS`, `README`, architecture docs, `PROJECT_CONTEXT`, requirements/constraints, decision log, Codex prompt, CI/tests |
| GridWorld/environment | GridWorld research/spec/ADR, current status, roadmap, open questions, requirements, tests, Codex prompt if next task changes |
| Models/metrics/protocol | corresponding research/protocol files, current status, open questions, roadmap, decision log, Codex prompt, tests |
| Bibliography contract/baseline | bibliography integration docs, README/context, current status, decision log/changelog, import validation/workflow; never hand-edit generated evidence |
| Experiment/run data policy | run/provenance docs, constraints, requirements, `.gitignore`/`.gitattributes`, publisher/tests, decision log/changelog |
| Dashboard workflow | architecture/UI docs, requirements, roadmap, current status, Codex prompt, tests |
| Thesis/delivery guidance | thesis/university docs, requirements, open questions, roadmap, current status where relevant |

The matrix is a minimum, not an exhaustive list. Review transitive dependencies when a statement is repeated elsewhere.

## Reconciliation procedure

Before merge:

1. identify what changed semantically, not only which files changed;
2. search active documentation for the old assumption, phase, path, status, stack, count, or blocker;
3. update all active occurrences;
4. delete obsolete files that no longer serve a purpose;
5. mark useful historical records explicitly historical rather than leaving ambiguous stale instructions;
6. update decisions/changelog when the change is material;
7. run `scripts/validate_documentation_consistency.py` and the normal repository test suite.

## Prompt rule

There is only one tracked current Codex execution prompt. It must be written to remain as state-driven as possible: Codex reads `CURRENT_STATUS.md` and the roadmap and must not redo work merely because an older phase is mentioned in the prompt.

When workflow, responsibilities, architecture, or the active next task materially changes, the prompt is reviewed in the same PR.

## No silent stale-state policy

Known obsolete statements must not remain in active documentation as a convenience. If the old wording is scientifically or historically useful, move/mark it as historical and point to the current authority.
