# Execution and Review Workflow

## Operating model

The user provides goals, observed behavior, genuinely academic/product choices, later supervisor feedback, and private material when required. The user is not responsible for routine branches, commits, tests, PRs, CI, review corrections, merges, experiment-result Git publication, or manually remembering unfinished Codex subtasks.

ChatGPT scopes/reviews scientific and technical work and decides merge readiness. Codex executes bounded work from the actual repository state without self-approval or silent scientific scope expansion. GitHub runs repeatable checks; passing CI is necessary but not sufficient.

Normal development flow:

> goal → task registry → branch/PR → CI/review → corrections → squash merge → task/status update

Current supervisor identity, deadlines, and final Word formatting are not implementation blockers. Later feedback is recorded as an explicit change when received.

## Codex continuation and recovery

The tracked canonical and directly executable prompt is `docs/context/CODEX_EXECUTION_PROMPT.md`. The canonical concrete checklist/resume ledger is `docs/context/TASKS.md`.

After cloning/updating the repository on the thesis machine, start Codex with: `Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely.`

At the start of every Codex session:

1. inspect Git status/current branch/recent commits and relevant PR state;
2. read `TASKS.md` before selecting work;
3. resume any `IN_PROGRESS` task first unless genuinely blocked;
4. use available session/conversation memory to understand prior work;
5. verify that memory against durable repository evidence before changing task state.

If model quota or the session ends unexpectedly, the next session inspects branch history, working-tree diff, PR/tests, `Resume state`, and session memory if available. It does not restart the task merely because the previous chat/session ended.

Intermediate branch commits are valid recovery checkpoints. The coherent PR still normally reaches `main` through one squash merge, so quota resilience does not require noisy permanent main-branch history.

## Bibliography material flow

PDFs, Markdown, NotebookLM exports, source lists, and other bibliography inputs go to `MariosGiannakaras/ThesisBibliography`. The thesis repository never writes back upstream. It receives only the committed complete research corpus through the immutable read-only PR-based synchronization contract in `docs/context/BIBLIOGRAPHY_INTEGRATION.md`.

The first complete import is already accepted. Formal citation trust remains confined to `research/bibliography/citation-ready/`; other imported content is internal research context unless promoted upstream and resynchronized.

## Experiment result flow

A run ID means one whole experiment and may include many seeds/episodes.

1. The experiment persists data/provenance safely while running.
2. The run bundle is finalized at the whole-experiment lifecycle boundary.
3. The guarded publisher stages only the finalized bundle and required run index/registry metadata.
4. One informative commit is created and pushed for the whole experiment.
5. No permanent commit is created per seed/episode.
6. If publication is unsafe or fails, local result data is preserved and the Git action is blocked rather than forced.
7. Configured large result/artifact formats use Git LFS; useful evidence is not manually discarded merely because it is large.

## Documentation and task reconciliation

Every material change follows `docs/context/DOCUMENTATION_GOVERNANCE.md`. A change is not ready to merge if related active docs/status/prompts/tasks/decisions still describe the previous state.

Every material PR reviews `TASKS.md`. Starting, completing, blocking, unblocking, superseding, or discovering work must update the corresponding task and `Resume state` in the same PR when applicable.

Delete obsolete files when they have no continuing value. Preserve useful historical records only with a clear historical/superseded notice. Generated bibliography files are never hand-edited for consistency.

## Git and review rules

Use descriptive lowercase branches with `research/`, `feat/`, `fix/`, `test/`, `docs/`, or `chore/`. Branch tooling may create several mechanical/checkpoint commits, but one coherent PR should normally reach `main` as one squash commit.

Substantial PRs state task IDs, scope, rationale, validation, scientific/protocol impact, limitations, deferred work, and documentation/task reconciliation. Merge only when scope is correct, tests meaningfully cover the change, CI passes, review findings are resolved, source-of-truth docs agree, and no data/results/logs/metrics/citations/progress are fabricated.

## Current project sequence

The detailed concrete queue is maintained only in `docs/context/TASKS.md`. `IMPLEMENTATION_ROADMAP.md` explains the phase/dependency structure and must not become a second competing checklist.

Structured research notes, decisions, evidence mappings, figures, captions, task progress, and implementation explanations are preserved throughout so later work and thesis writing are not reconstructed from memory.
