# Contributing

This repository serves one thesis project, but changes must follow a controlled process.

## Before making a change

- Read `AGENTS.md`, `docs/context/TASKS.md`, and the relevant canonical context files.
- Identify the canonical task ID(s), requirement, or decision that justifies the change.
- If required work is newly discovered, add a stable task ID/dependency to `TASKS.md` before it can be forgotten.
- Identify every active document, prompt, test, workflow, schema, task state, lifecycle handoff, or status statement that depends on the thing being changed.

## Task and documentation consistency rule

A change is not complete when only the code or primary document is updated.

In the same Pull Request:

1. review `TASKS.md` and update started/completed/blocked/unblocked/discovered/superseded tasks and `Resume state` where applicable;
2. ensure any task marked `READY` really has its required task dependencies complete;
3. update every active source-of-truth document affected by the change;
4. review `docs/context/IMPLEMENTATION_ROADMAP.md` and `docs/context/EXECUTION_WORKFLOW.md` if a major application/experiment/evidence/thesis/defense/delivery handoff changes;
5. review `docs/thesis/PRESENTATION_WORKFLOW.md` if defense outputs/tooling/speaker material/rehearsal rules change;
6. update `docs/context/CODEX_EXECUTION_PROMPT.md` only when bootstrap, resume, task-selection, checkpoint, stop, review-gate, or reporting behavior changes; domain rules stay in `AGENTS.md` or their controlling specification;
7. delete obsolete compatibility files when they no longer serve a purpose;
8. preserve genuinely historical records only when useful, and mark them prominently as historical so they cannot be mistaken for current instructions;
9. update `CURRENT_STATUS.md`, `OPEN_QUESTIONS.md`, `DECISION_LOG.md`, and `CHANGELOG_CONTEXT.md` when their claims are affected;
10. add/update automated consistency checks when stale state can be detected mechanically.

`docs/context/DOCUMENTATION_GOVERNANCE.md` defines the dependency/update matrix. `CURRENT_STATUS.md` summarizes current state. `TASKS.md` is the canonical concrete execution/resume ledger. `IMPLEMENTATION_ROADMAP.md` explains phase/dependency order, while `EXECUTION_WORKFLOW.md` owns responsibilities and major handoffs; neither is a second task list.

## Interruption-safe work

Codex work may be interrupted by quota/session loss.

- Preserve useful current-session memory but verify it against Git/repository state.
- Use descriptive work branches and intermediate checkpoint commits after meaningful validated substeps when practical.
- Keep unfinished tasks `IN_PROGRESS` with an exact resume note.
- On a new session inspect branch, commits, working-tree diff, PR/tests, and task resume state before restarting work.
- Normally squash the coherent PR into `main`; checkpoint commits need not become permanent main history.

## Branches and commits

- `main`: stable thesis source of truth.
- Feature/research branches: use short descriptive names such as `research/gridworld-spec`, `feat/run-registry`, `experiments/run-schema-v1`.
- Keep commits small but meaningful; intermediate recovery commits are acceptable on branches.
- Squash coherent connector/checkpoint commits before merging when appropriate.
- Typical prefixes: `docs:`, `research:`, `feat:`, `experiments:`, `test:`, `fix:`, `chore:`.
- Commit and Pull Request text is written in English.

## Pull Request checklist

- [ ] The PR lists the affected canonical task ID(s).
- [ ] `TASKS.md` and `Resume state` were reconciled where applicable.
- [ ] `READY` task/dependency state remains valid.
- [ ] The change maps to a requirement/decision/research need.
- [ ] Relevant tests were added or updated.
- [ ] No secrets or generated artifacts without provenance were added.
- [ ] Every affected active source-of-truth/status/prompt/lifecycle file was reviewed and reconciled.
- [ ] Obsolete files were deleted or explicitly marked historical rather than left as misleading current guidance.
- [ ] Results are not presented as final without a frozen protocol.
- [ ] Thesis/presentation claims do not outrun frozen evidence/citation-ready support.
- [ ] Figures/tables can be reproduced.
- [ ] Documentation matches actual behavior and current repository state.
- [ ] Automated review findings were addressed or explicitly rejected with a reason.

## Data and results

- Do not modify finalized raw results.
- Whole-experiment outputs are retained and versioned automatically; large configured artifact formats use Git LFS.
- Do not manually prune large run data merely to reduce repository size. Change retention only through an explicit storage/protocol decision if real storage limits appear.
- Every processed artifact must identify source run IDs and the processing script.
- Failed runs retain metadata and a failure reason.
- Final writing/presentation consumes the frozen thesis/defense evidence package rather than ad-hoc reinterpretation of raw final runs.

## Bibliography

- Do not acquire, copy, convert, or curate new primary bibliography sources in this repository.
- The canonical bibliography lifecycle belongs to `MariosGiannakaras/ThesisBibliography`.
- This repository consumes only the verified generated package under `research/bibliography/` through the controlled synchronization workflow.
- Do not hand-edit generated bibliography imports.

## Thesis and presentation content

- Every factual claim requires a real citation-ready source or real frozen project result as appropriate.
- Every result claim must map to run IDs/figure/table IDs.
- Source-derived scientific evidence remains in the original source language.
- Current official Department guidance overrides repository placeholders.
- Supervisor/reviewer revisions must revalidate affected evidence/citations/figures/method statements.
- Defense slides/speaker material must trace to the final thesis/frozen evidence and follow `docs/thesis/PRESENTATION_WORKFLOW.md`.
