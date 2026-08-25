# resilient-ai-agents-thesis

**Official Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

Version-controlled repository for the complete thesis lifecycle: research context, bibliography consumer, experimental software, runs/results, analysis artifacts, thesis writing, defense presentation, and final deliverables.

## Project principle

The goal is a scientifically valid, reproducible, and realistically completable thesis. The application supports the research; it is not the main research contribution.

> **Polished outside, bounded inside.**

The final tool is local and single-user. It must let the user configure, execute, monitor, compare, and export experiments without manual coding or routine Git work, while avoiding production-platform complexity.

## Current implementation baseline

The canonical bibliography lifecycle remains in `MariosGiannakaras/ThesisBibliography`. This repository consumes its verified immutable complete research-corpus export under `research/bibliography/`, with the nested `citation-ready/` layer as the only automatic formal-citation surface. The current synchronized baseline is `bibliography-integration-v3` and contains 585 canonical sources, 113 citation-ready sources, 19 research materials, metadata for 281 indexed original PDFs, and 1,568 integrity-covered corpus files. Bibliography PDFs, structured originals, and bibliography Git LFS objects remain upstream and are not imported here.

The active research implementation lives in the importable package:

```text
src/resilient_agents/
```

The accepted architecture uses:

- Python 3.12;
- `uv`, `pyproject.toml`, `.python-version`, and committed `uv.lock`;
- explicit scenario/experiment/protocol contracts;
- strict separation of evaluator ground truth from agent-visible information;
- independent deterministic RNG streams;
- filesystem-first experiment run bundles with provenance and checksums;
- fail-closed finalization with a last-written completion marker and checksum revalidation before automatic publication;
- one guarded automatic Git commit and push per finalized whole experiment, never per seed;
- selective Git LFS for large thesis-produced artifacts;
- a future thin Streamlit dashboard after the headless core and pilots establish the real workflow.

No final research question, model set, GridWorld scientific parameters, uncertainty severities, seed count, budgets, hyperparameters, recovery threshold, statistical plan, or final protocol is frozen yet.

## Current control files

- `docs/context/CURRENT_STATUS.md` — shortest authoritative current-state summary.
- `docs/context/TASKS.md` — canonical concrete checklist and resumable Codex progress ledger.
- `docs/context/PROJECT_CONTEXT.md` — current integrated project context.
- `docs/context/IMPLEMENTATION_ROADMAP.md` — phase/dependency explanation.
- `docs/context/EXECUTION_WORKFLOW.md` — execution responsibilities and major handoffs.
- `docs/context/DOCUMENTATION_GOVERNANCE.md` — mandatory reconciliation rules.
- `docs/decisions/DECISION_LOG.md` — accepted/superseded/pending decision index.
- `docs/context/CODEX_EXECUTION_PROMPT.md` — single tracked, canonical, directly executable Codex prompt.
- `docs/thesis/PRESENTATION_WORKFLOW.md` — deferred but already-defined final PowerPoint/speaker-material workflow.

After cloning/updating the repository on the thesis machine, start Codex with: `Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely.` Every Codex session must inspect `TASKS.md` before selecting/resuming work. Available session memory is used together with branch/working-tree/PR state; durable repository evidence is the fallback when a session or model quota is interrupted.

Historical bootstrap/pre-import files are not current instructions. Useful historical records are explicitly labelled historical; obsolete active files are removed rather than left to drift.

## Repository map

```text
src/resilient_agents/                  Independent scientific/research core
app/                                   Future thin local dashboard
configs/                               Version-controlled experiment/scenario configs
scripts/                               Reproducibility and maintenance utilities
tests/                                 Unit/integration/reproducibility tests

research/bibliography/                 Generated bibliography research corpus
results/runs/                          Whole-experiment run bundles
results/summaries/                     Derived summaries
results/thesis-final/                  Frozen final thesis evidence
artifacts/figures/                     Reproducible figures
artifacts/tables/                      Reproducible tables
artifacts/exports/                     Exports and reports

thesis/source-material/                Official thesis source material
thesis/chapters/                       Writing-stage chapter drafts
thesis/final/                          Final thesis deliverables

presentation/source/                   Future slide outline/evidence map/speaker script sources
presentation/assets/                   Future evidence-backed figures/screenshots/demo assets
presentation/final/                    Future final PowerPoint and defense deliverables

docs/context/                          Current scope, tasks, requirements, workflow, roadmap
docs/research/                         Research framing and selection work
docs/experiments/                      Protocol, run, storage, and provenance rules
docs/architecture/                     Core/UI architecture
docs/thesis/                           Thesis-writing and defense-presentation workflow rules
docs/decisions/                        Decisions and ADRs
```

The `presentation/` directories are a future output contract; they do not need to exist until the defense phase is executed.

## Lifecycle handoff

The intended end-to-end chain is:

> validated application -> frozen final experiments -> frozen evidence/analysis -> thesis evidence package -> Greek thesis/review/final freeze -> PowerPoint + speaker notes/script -> final audit/delivery

The application is therefore not the end of the project. It is the validated execution surface that hands off into the final experiment campaign. The thesis and presentation are downstream artifacts of the same frozen evidence chain.

## Experiment publication

A `run_id` means one whole experiment and may contain many seeds/episodes. The experiment writes its resolved configuration, capability snapshot, events/traces, summary, manifest, and SHA-256 checksums under `results/runs/<run-id>/`.

A run becomes publishable only after finalization writes the `FINALIZED` sentinel as its last step. After that, the publisher revalidates the final status, run identity, manifest file metadata, sizes and SHA-256 checksum scope before any Git staging. Corrupted or partially finalized evidence therefore fails closed.

When the verified experiment finalizes, the normal workflow can automatically create one commit and push containing only that run and the run index. The publisher also refuses unsafe mixed-provenance/dirty-state/non-fast-forward publication, but never deletes the local experiment data when publication cannot proceed.

Useful large thesis-produced outputs are retained while storage permits. Large traces and other configured formats use Git LFS. Bibliography PDFs and bibliography LFS objects remain upstream and are never imported here.

## Scientific integrity

Do not fabricate sources, data, runs, metrics, progress, figures, tables, presentation claims, or conclusions. Every final thesis/result/presentation claim must trace to real source evidence, a versioned protocol/configuration, recorded run data, and reproducible analysis/evidence mappings as applicable.