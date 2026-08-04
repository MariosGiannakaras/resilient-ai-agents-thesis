# Documentation Governance

## Purpose

Repository documentation is part of the thesis source of truth. A code, research, architecture, workflow, storage, protocol, task-state, lifecycle-handoff, UX, or delivery change is incomplete if related active documentation still describes the previous state.

## Document classes

### 1. Active source of truth

These files must describe the current repository state and must be reconciled in the same Pull Request as any material change that affects them:

- `AGENTS.md`
- `README.md`
- `app/README.md`
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
- `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`
- `docs/thesis/PRESENTATION_WORKFLOW.md`
- active research/protocol/architecture/thesis workspaces relevant to the changed subject.

`CURRENT_STATUS.md` is the shortest authoritative current-state summary. `TASKS.md` is the canonical concrete execution checklist/resume ledger. `IMPLEMENTATION_ROADMAP.md` explains phases, while `EXECUTION_WORKFLOW.md` records responsibilities and major handoffs. `UI_INFORMATION_ARCHITECTURE.md` controls the bounded dashboard information/UX contract when dashboard work is active. None excuses stale statements in other active files.

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

`READY` has a strict meaning: all required task-ID dependencies are completed and any non-task precondition explicitly stated for readiness is satisfied. Do not label future dependency-blocked work `READY` merely because it belongs to the planned roadmap. The documentation validator checks task-ID dependencies mechanically.

Started unfinished work must remain unchecked and be marked `IN_PROGRESS` with enough durable resume information to continue after a session/model-quota interruption. Completed tasks remain checked for auditability.

Session/conversation memory may assist continuation, but durable repository state is the recovery authority. Do not encode task progress only in chat.

## Lifecycle-handoff governance

Major boundaries (application -> final experiments, experiments -> evidence/analysis, analysis -> thesis, thesis -> defense, defense -> delivery) are controlled by DEC-026, the corresponding `TASKS.md` dependencies/acceptance conditions, `IMPLEMENTATION_ROADMAP.md`, and `EXECUTION_WORKFLOW.md`.

Downstream thesis/presentation artifacts must never become an independent source of scientific truth. They inherit from frozen experiment evidence and citation-ready bibliography mappings.

`docs/thesis/PRESENTATION_WORKFLOW.md` is the active deferred specification for the defense phase and must be reconciled if presentation tooling, output format, speaker-material requirements, evidence mapping, or rehearsal/delivery rules change.

## Dashboard UX governance

DEC-027, `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`, `app/README.md`, confirmed `REQ-UI-*` requirements, and the `T-510`/`T-512`/`T-511` task chain control the final dashboard UX baseline.

The self-explanatory UX/onboarding baseline is a required application-completion condition, not an optional cosmetic enhancement. Exact palette values and other implementation-level styling details remain intentionally unfrozen until the real dashboard exists.

Changes to dashboard wording, terminology, status semantics, contextual help, pre-run review, onboarding/help flow, or UI architecture must reconcile the relevant requirements/tasks and must not introduce a parallel manual/help system that can drift from implemented behavior.

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
| Application/dashboard workflow or UX | `app/README`, `UI_INFORMATION_ARCHITECTURE`, `AGENTS`, requirements/user decisions/constraints, roadmap, workflow, current/project status, `TASKS`, Codex prompt, definition of done, tests, decision log/changelog |
| Final experiment/analysis -> writing handoff | `TASKS`, roadmap, workflow, experiment/analysis docs, thesis docs, requirements, current status, decision log/changelog |
| Thesis/review workflow | thesis/university docs, requirements/user decisions, roadmap, workflow, current status, `TASKS`, Codex prompt when execution changes |
| Defense presentation workflow | `PRESENTATION_WORKFLOW`, requirements/user decisions, roadmap, workflow, definition of done, `TASKS`, source register, decision log/changelog |
| Final delivery guidance | thesis/university/presentation docs, requirements, open questions, roadmap, current status, `TASKS`, definition of done |

The matrix is a minimum, not an exhaustive list. Review transitive dependencies when a statement is repeated elsewhere.

## Reconciliation procedure

Before merge:

1. identify what changed semantically, not only which files changed;
2. review `TASKS.md` for affected task state/dependencies/acceptance/resume information;
3. review relevant roadmap/workflow handoffs when the changed subject crosses a major project boundary;
4. search active documentation for the old assumption, phase, path, status, stack, count, or blocker;
5. update all active occurrences;
6. delete obsolete files that no longer serve a purpose;
7. mark useful historical records explicitly historical rather than leaving ambiguous stale instructions;
8. update decisions/changelog when the change is material;
9. run `scripts/validate_documentation_consistency.py` and the normal repository test suite.

## Prompt rule

There is only one tracked current Codex execution prompt: `docs/context/CODEX_EXECUTION_PROMPT.md`.

It is the directly executable entrypoint for Codex after the repository is cloned or updated. Every session must pass through `TASKS.md` before selecting or resuming work. The prompt must remain state-driven and interruption-resilient: available session memory is used, but work can always be recovered from the registry and Git/repository state.

When workflow, responsibilities, architecture, project state, task-governance rules, lifecycle handoffs, or active execution materially changes, the prompt is reviewed and updated in the same PR.

## No silent stale-state policy

Known obsolete statements must not remain in active documentation as a convenience. If the old wording is scientifically or historically useful, move/mark it as historical and point to the current authority.
