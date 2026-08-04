# resilient-ai-agents-thesis

**Official Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

Private, version-controlled repository for the complete thesis lifecycle: research context, bibliography consumer, experimental software, runs/results, analysis artifacts, thesis writing, and final deliverables.

## Project principle

The goal is a scientifically valid, reproducible, and realistically completable thesis. The application supports the research; it is not the main research contribution.

> **Polished outside, bounded inside.**

The final tool is local and single-user. It must let the user configure, execute, monitor, compare, and export experiments without manual coding or routine Git work, while avoiding production-platform complexity.

## Current implementation baseline

The canonical bibliography lifecycle remains in the private `MariosGiannakaras/ThesisBibliography` repository. This repository consumes its verified immutable export under `research/bibliography/`. The current imported baseline contains 583 canonical sources, 112 citation-ready sources, 19 research materials, and metadata for 280 indexed original PDFs.

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
- one guarded automatic Git commit and push per finalized whole experiment, never per seed;
- selective Git LFS for large thesis-produced artifacts;
- a future thin Streamlit dashboard after the headless core and pilots establish the real workflow.

No final research question, model set, GridWorld scientific parameters, uncertainty severities, seed count, budgets, hyperparameters, recovery threshold, statistical plan, or final protocol is frozen yet.

## Current control files

- `docs/context/CURRENT_STATUS.md` — shortest authoritative current-state summary.
- `docs/context/PROJECT_CONTEXT.md` — current integrated project context.
- `docs/context/IMPLEMENTATION_ROADMAP.md` — phase/dependency order.
- `docs/context/DOCUMENTATION_GOVERNANCE.md` — mandatory rule for updating/deleting related active files whenever a material change occurs.
- `docs/decisions/DECISION_LOG.md` — accepted/superseded/pending decision index.
- `docs/context/CODEX_EXECUTION_PROMPT.md` — only tracked current Codex prompt template.

For a local Codex session, copy the canonical prompt to repository-root `CODEX_TASK.md`. That local file is git-ignored and may be deleted after Codex reads it.

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
thesis/final/                          Final Word/PDF deliverables

docs/context/                          Current scope, requirements, workflow, roadmap
docs/research/                         Research framing and selection work
docs/experiments/                      Protocol, run, storage, and provenance rules
docs/architecture/                     Core/UI architecture
docs/decisions/                        Decisions and ADRs
```

## Experiment publication

A `run_id` means one whole experiment and may contain many seeds/episodes. The experiment writes its resolved configuration, capability snapshot, events/traces, summary, manifest, and SHA-256 checksums under `results/runs/<run-id>/`.

When the experiment finalizes, the normal workflow can automatically create one commit and push containing only that run and the run index. The publisher refuses unsafe mixed-provenance commits, but never deletes the local experiment data when publication cannot proceed.

Useful large thesis-produced outputs are retained while storage permits. Large traces and other configured formats use Git LFS. Bibliography PDFs and bibliography LFS objects remain upstream and are never imported here.

## Scientific integrity

Do not fabricate sources, data, runs, metrics, progress, figures, tables, or conclusions. Every final thesis result must trace to real source evidence, a versioned protocol/configuration, a recorded Git commit, stored run data, and reproducible analysis code.
