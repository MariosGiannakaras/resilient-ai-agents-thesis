# Codex Execution Prompt

## How to use

This file is the single tracked canonical and directly executable Codex prompt for the thesis project.

After cloning or updating the repository on the thesis machine, give Codex only this instruction:

> Read `docs/context/CODEX_EXECUTION_PROMPT.md` and execute it completely.

Do not copy this prompt to another task file and do not delete it after use. Whenever workflow, architecture, responsibilities, project state, or active work materially changes, this file and the canonical task registry must be reconciled in the same Pull Request.

---

Work autonomously in the private repository `MariosGiannakaras/resilient-ai-agents-thesis` and continue the thesis project from the **actual current repository state**.

Do not reconstruct the project from chat history and do not redo work already implemented, validated, merged, or recorded as accepted. Use current session/context memory when it is available, but always reconcile it with durable repository evidence.

## Mandatory startup and resume procedure

This procedure runs at the start of **every Codex session**, including continuation after model-quota exhaustion or an interrupted previous session:

1. inspect `git status`, current branch, recent commits, and any relevant open PR;
2. read `docs/context/TASKS.md` **before selecting work**;
3. read its `Resume state` and locate any task marked `IN_PROGRESS`;
4. use current-session/conversation memory to understand where work was left, if that memory exists;
5. verify that memory against branch commits, working-tree diff, tests, PR state, and repository files;
6. resume the existing `IN_PROGRESS` task before starting another task unless it is genuinely blocked;
7. only when no task is in progress, select the first dependency-valid pending task from `TASKS.md`.

`TASKS.md` is the durable recovery/checklist authority. Session memory is useful context, not a replacement for persisted progress. If memory is absent or conflicts with repository evidence, repository evidence wins.

## Required initial reading

Read first:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`
4. `README.md`
5. `docs/context/SCOPE_REFINEMENT.md`
6. `docs/context/PROJECT_CONTEXT.md`
7. `docs/context/CONFIRMED_REQUIREMENTS.md`
8. `docs/context/IMPLEMENTATION_ROADMAP.md`
9. `docs/context/DOCUMENTATION_GOVERNANCE.md`

Then read only task-specific files required by `AGENTS.md`. Historical files are context only and must not override current active files.

## Task execution and checkpoint rules

- Treat `docs/context/TASKS.md` as the canonical concrete checklist; the roadmap explains phases but does not replace the registry.
- Do not skip a task because it seems implied by another task. Check its acceptance condition explicitly.
- Do not mark a task complete until its acceptance condition is satisfied and validated.
- Newly discovered required work receives a stable task ID/dependency in `TASKS.md` before it can be forgotten.
- A task started but not completed becomes `IN_PROGRESS`, with branch/PR and an exact resume note.
- Keep work on descriptive branches. Intermediate branch commits are recovery checkpoints; the coherent PR should normally be squash-merged to `main`.
- Assume quota/session interruption can happen unexpectedly. When practical, do not pass more than one substantial logical substep without a recoverable checkpoint.
- At useful checkpoints record the last validated point and exact next action when they are not obvious from the commit.
- If a previous session ended before updating the registry, inspect uncommitted changes and branch history before deciding what remains. Never discard useful work merely because the prior session ended.

## Already accepted baseline — verify, do not redo

Unless the repository itself shows otherwise, the accepted baseline includes:

- complete immutable bibliography consumer under `research/bibliography/` with strict nested citation-ready layer;
- verified bibliography synchronization/authentication/integrity;
- Python 3.12 + `uv` + committed `uv.lock`;
- independent importable package `src/resilient_agents/`;
- evaluator-ground-truth versus agent-visible information separation;
- independent deterministic RNG streams;
- scenario/experiment/change/protocol contracts with no hidden scientific defaults;
- filesystem-first self-contained run bundles with provenance/checksums;
- guarded one-commit/one-push publication per finalized **whole experiment**, never per seed;
- selective Git LFS for configured large thesis-produced artifacts;
- development/tuning/pilot/final separation infrastructure;
- future dashboard as a thin Streamlit layer over the same research core, gated behind validated headless workflow and pilots.

Validate these rather than reimplementing them. `TASKS.md` records the accepted completion state and remaining work.

## Bibliography rules

`MariosGiannakaras/ThesisBibliography` is the canonical source of truth for discovery, originals/PDFs, OCR/conversion, scientific analysis, evidence verification, source selection, research materials, notes, and generated exports.

In this repository:

- consume the verified import under `research/bibliography/`;
- treat `research/bibliography/citation-ready/` as the only automatic formal-citation layer;
- use full-corpus/rejected/theory-only/`MAT-*`/notes for internal research only unless promoted upstream and resynchronized;
- do not acquire or edit bibliography sources locally;
- do not fabricate bibliographic identity, DOI, source status, evidence, or conclusions;
- if final support is needed from a non-citation-ready item, record the exact upstream verification/promotion task rather than locally promoting it.

## Scientific rules

- Keep the research design small and completable.
- Do not freeze a model, severity, seed count, budget, threshold, hyperparameter, or statistical method without evidence/pilot justification.
- No single-run model comparison.
- Keep development, tuning, pilot, and final evaluation separated.
- No agent receives hidden regime/change/disturbance/ground-truth information unless the protocol explicitly gives the same scientifically justified signal.
- Preserve non-recovery explicitly; do not convert it to artificial recovery at the horizon.
- Retain failures, cancellations, interruptions, invalid runs, and exclusions with reasons.
- Do not inspect final evidence and then silently retune or redefine primary outcomes.

## Experiment and Git automation rules

A run ID represents one **whole experiment**, potentially containing many seeds/episodes.

- Persist results continuously and safely during execution.
- Finalize the self-contained run bundle only at the correct lifecycle boundary.
- Use the existing guarded publisher for one complete commit/push per finalized experiment.
- Never create a commit per seed/episode.
- Stage only finalized experiment data and required registry/index metadata.
- Preserve local results if publication fails.
- Do not force-push, hide unrelated tracked changes, or publish mixed provenance.
- Retain useful large thesis-produced outputs and use the configured Git LFS policy while storage permits.

## Architecture/UI rules

- Scientific logic lives in `src/resilient_agents/`, not UI callbacks.
- Headless workflow must remain fully usable/testable without the dashboard.
- Filesystem run bundles are source of truth; any later database/index is rebuildable cache.
- Avoid microservices, Kubernetes, cloud-only infrastructure, distributed workers, authentication systems, or production observability.
- Lightweight debug visualization is allowed when useful for validation.
- Polished dashboard follows validated pilots and remains a thin local Streamlit layer unless measured requirements justify another decision.

## Documentation and task consistency — mandatory

For every material change follow `docs/context/DOCUMENTATION_GOVERNANCE.md`.

In the same PR:

- update `TASKS.md` for any task started/completed/blocked/unblocked/discovered/superseded;
- update its `Resume state` while work is incomplete;
- search for old assumptions/status/paths/counts/architecture statements;
- update affected active source-of-truth files;
- update `CURRENT_STATUS.md`, `OPEN_QUESTIONS.md`, `DECISION_LOG.md`, and `CHANGELOG_CONTEXT.md` when affected;
- update this prompt when workflow, architecture, responsibilities, or execution rules materially change;
- delete obsolete files or mark useful historical records prominently as historical;
- never rewrite generated bibliography evidence by hand.

Run the documentation consistency validator before merge.

## Testing and review

Use a branch and Pull Request for substantive work. Run relevant tests plus repository checks. Tests must cover affected scientific/behavioral invariants, not only syntax.

Passing CI is necessary but not sufficient if implementation or scientific assumptions are wrong. Record rationale, validation, exclusions, and remaining gates.

## Stop conditions

Do not stop for routine Git operations, documentation/task updates, tests, or decisions resolvable from repository evidence, actual local system, verified bibliography, prototypes, or authoritative technical documentation.

Stop and report only when continuation truly requires:

- an academic/product choice that cannot be objectively resolved;
- new supervisor/Department guidance only the user can supply;
- access/credential failure that cannot be repaired from the available environment;
- execution on the actual thesis machine when the current environment is not that machine and the result materially affects the next decision;
- a safety/legal/licensing blocker;
- a frozen-protocol change requiring explicit amendment.

Before an intentional stop, make the current work recoverable: checkpoint appropriate branch work, update `TASKS.md`/`Resume state`, and leave the repository internally consistent. If quota ends without warning, the next session follows the mandatory startup procedure and recovers from existing repository state.

## Final report

At the end of a session report only:

- task IDs completed or still in progress;
- what was completed;
- PR(s) and merge/checkpoint commit(s);
- tests/validators and results;
- scientific/architecture decisions accepted or still unfrozen;
- real blockers/gates;
- exact next task/action from `TASKS.md`.

This tracked prompt and `docs/context/TASKS.md` remain in the repository and are maintained as part of the project source of truth.