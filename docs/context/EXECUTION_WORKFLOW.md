# Execution and Review Workflow

## Operating model

The user provides goals, observed behavior, genuinely academic/product choices, later supervisor feedback, and private material when required. The user is not responsible for routine branches, commits, tests, PRs, CI, review corrections, merges, or experiment-result Git publication.

ChatGPT scopes/reviews scientific and technical work and decides merge readiness. Codex executes bounded work from the actual repository state without self-approval or silent scientific scope expansion. GitHub runs repeatable checks; passing CI is necessary but not sufficient.

Normal development flow:

> goal → bounded task → branch/PR → CI/review → corrections → squash merge → concise outcome

Current supervisor identity, deadlines, and final Word formatting are not implementation blockers. Later feedback is recorded as an explicit change when received.

## Codex continuation

The tracked canonical and directly executable prompt is `docs/context/CODEX_EXECUTION_PROMPT.md`. After cloning/updating the repository on the thesis machine, start Codex with: `Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely.`

Codex reads the current repository/status rather than replaying old chat or obsolete bootstrap phases. The prompt remains tracked and is updated whenever the project state or workflow materially changes.

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

## Documentation reconciliation

Every material change follows `docs/context/DOCUMENTATION_GOVERNANCE.md`. A change is not ready to merge if related active docs/status/prompts/decisions still describe the previous state.

Delete obsolete files when they have no continuing value. Preserve useful historical records only with a clear historical/superseded notice. Generated bibliography files are never hand-edited for consistency.

## Git and review rules

Use descriptive lowercase branches with `research/`, `feat/`, `fix/`, `test/`, `docs/`, or `chore/`. Branch tooling may create several mechanical commits, but one coherent PR should normally reach `main` as one squash commit.

Substantial PRs state scope, rationale, validation, scientific/protocol impact, limitations, deferred work, and documentation reconciliation. Merge only when scope is correct, tests meaningfully cover the change, CI passes, review findings are resolved, source-of-truth docs agree, and no data/results/logs/metrics/citations/progress are fabricated.

## Current project sequence

1. Run/accept the actual target-machine inventory.
2. Complete bounded GridWorld prototypes and ADR.
3. Finalize source-traceable RQ/environment/model-role/metric proposals.
4. Implement the selected environment and small justified agent set in the existing independent package.
5. Define/run pilots and freeze the final protocol only after pilot questions are answered.
6. Complete headless experiment/analysis workflow.
7. Build only the polished bounded Streamlit dashboard required by that validated workflow.
8. Execute final experiments, freeze evidence, and generate reproducible analysis artifacts.
9. Complete Greek Word thesis/presentation from verified bibliography and frozen evidence.

Structured research notes, decisions, evidence mappings, figures, captions, and implementation explanations are preserved throughout so writing is not reconstructed later.
