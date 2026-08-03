# Execution and Review Workflow

## Operating model

The user provides goals, observed behavior, genuinely academic/product choices, later supervisor feedback, and private material when required. The user is not responsible for routine branches, commits, tests, PRs, CI, review corrections, or merges.

ChatGPT scopes bounded work, reviews scientific and technical evidence, handles corrections, and decides merge readiness. Codex executes the bounded task and produces implementation, tests, documentation, commits, and a PR without self-approval or silent scope expansion. GitHub runs repeatable checks; passing CI is necessary but not sufficient.

Normal flow:

> goal → bounded implementation/research task → branch/PR → CI and review → corrections → merge → concise outcome

Current supervisor identity, deadlines, and final Word formatting are not implementation blockers. Later feedback is recorded as an explicit change when received.

## Bibliography material flow

PDFs, Markdown, NotebookLM exports, source lists, and all other bibliography inputs go to `MariosGiannakaras/ThesisBibliography`. That repository performs content inspection, duplicate/version handling, original preservation, OCR/conversion, metadata, analysis, evidence verification, selection, research-material identification, and corpus generation.

The thesis repository never performs those operations and never writes back upstream. It receives only a committed complete research corpus through the immutable, read-only, PR-based synchronization contract in `docs/context/BIBLIOGRAPHY_INTEGRATION.md`. Formal citation trust remains confined to the nested citation-ready layer while all other imported text remains searchable for internal research.

## Git and review rules

Use descriptive lowercase branches with `research/`, `feat/`, `fix/`, `test/`, `docs/`, or `chore/`. Commits explain what changed, why, validation, and important exclusions. Substantial PRs state scope, rationale, validation, scientific/protocol impact, limitations, and deferred work.

Merge only when scope is correct, tests meaningfully cover the change, CI passes, review findings are resolved, documentation/decisions are consistent, and no data, results, logs, metrics, citations, or progress are fabricated. Generated bibliography PRs contain only `research/bibliography/` and consumer import metadata.

## Project sequence

1. Complete immutable full-corpus integration and evidence synthesis.
2. Run and accept the actual target-system inventory.
3. Perform source-traceable model/agent research.
4. Prototype the retained GridWorld candidates and record an ADR.
5. Bound research questions, uncertainty mechanisms, metrics, and pilot protocol.
6. Build and validate the independent headless core.
7. Run pilots and freeze the final protocol.
8. Execute final experiments and statistical analysis.
9. Build only the polished bounded dashboard required by the validated workflow.
10. Complete Greek Word thesis writing and presentation from frozen evidence.

Structured research notes, decisions, evidence mappings, figures, captions, and implementation explanations are preserved throughout so writing is not reconstructed later.
