# resilient-ai-agents-thesis

**Official Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

Private, version-controlled repository for the full thesis project of the Department of Informatics and Computer Engineering, School of Engineering, University of West Attica.

## Repository role

This repository is the permanent source of truth for the thesis academic/research context, requirements and decisions, GridWorld, experimental core, local dashboard, data and results, writing, and final Microsoft Word deliverable.

The complete bibliography lifecycle has a separate canonical source of truth in `MariosGiannakaras/ThesisBibliography`. This repository consumes only its controlled generated export.

## Language policy

Repository-authored operational and technical documentation is written in English. Code identifiers, comments, filenames, branches, commits, Pull Requests, schemas, and agent prompts also use English.

The exact official Greek thesis title is preserved where required. Scientific source text and citation-ready evidence remain in the original language of each source. The final thesis remains a Greek Microsoft Word deliverable unless an official requirement changes.

## Refined objective

The primary success criterion is a correct, scientifically adequate, and realistically completable thesis. The application is an important deliverable, but it is neither a production-grade product nor the main research contribution.

> **Polished outside, bounded inside.**

Architecture and engineering remain simple and proportional to a local single-user research tool. The UI must still be modern, coherent, usable, screenshot-ready, and complete enough for the user to execute, monitor, compare, and export the required experiments without writing code or using console commands.

The binding scope direction is defined in `docs/context/SCOPE_REFINEMENT.md`.

## Priority order

1. Clear and bounded research question.
2. Simple and properly validated GridWorld.
3. Small, justified set of models and uncertainty types.
4. Fair and reproducible protocol.
5. Reliable and comparable results.
6. Independent research program and experiment implementation.
7. Polished research dashboard for execution, monitoring, and interpretation.
8. Advanced features only when they solve a real need.
9. Final writing and presentation work after the evidence-producing system is mature.

## Old-conversation rule

Old conversation exports were used only for historical context. They do not establish selected data, a shortlist, a specification, or evidence of preference. Models, GridWorld implementation, metrics, stack, hyperparameters, and experimental design are evaluated again using current research and real evidence.

## Current phase

Bootstrap is complete. The current complete scientific bibliography selection is also complete in `ThesisBibliography`: **583/583 active sources** have a final decision, **112 selected sources** have verified citation-ready evidence, **470 sources are rejected**, **1 source is theory-only/non-exported**, and there are **0 pending scientific decisions**.

The complete research-corpus consumer migration and first controlled import into `research/bibliography/` are not yet complete. On 2026-08-04 the user created a repository-scoped fine-grained token and replaced the `BIBLIOGRAPHY_SYNC_TOKEN` Actions secret in this repository. The token value is never stored in Git or chat. Its effective read access will be verified by the migrated synchronization workflow before any import replacement. The obsolete citation-only workflow must not be used as proof that the final full-corpus integration is complete.

Preparatory Phase-1/research work has progressed without bypassing the bibliography gate:

- the official application repository copy is integrity-pinned by SHA-256;
- a privacy-minimal target-system inventory collector is implemented and tested, but still needs to run on the actual thesis machine;
- the current GridWorld landscape pre-screen is complete, retaining a custom Gymnasium environment and a thin MiniGrid adaptation for bounded prototype comparison;
- non-binding pre-import research workspaces distinguish robustness from adaptation/recovery and propose persistent rule/dynamics change as the primary resilience axis, with observation/action disturbances as supporting robustness diagnostics;
- an August 2026 freshness review added three recent, fully verified supporting sources to the canonical bibliography and tightened the provisional methodology around structured switching, practical change-detector validation, and leakage-free continual-RL tuning.

The main application, final model implementation, final experiments, and normal results writing have not started.

The active next phase is:

1. migrate the thesis repository to the complete `research-corpus/` consumer contract and complete the controlled import from the immutable bibliography baseline,
2. run and accept the system capability inventory on the actual machine that will execute the thesis experiments,
3. perform the bounded custom-Gymnasium versus MiniGrid prototypes and record the final GridWorld ADR,
4. perform source-traceable model/agent-family research and convert the preparatory framing into final research-question, uncertainty, model-role, and metric proposals,
5. define a small and manageable pilot protocol,
6. build the independent research core and experiment program, with a lightweight debug/visualization surface only when useful for validation,
7. run pilots, freeze the final protocol, and implement only the dashboard functionality required by the real experiment workflow,
8. execute final experiments and produce reproducible evidence before normal thesis writing begins.

Old code is not required. External GridWorld code is integrated only after code, license, maintenance, compatibility, and prototype review.

The official application is stored at `thesis/source-material/GiannakarasMariosThesisApplication.pdf`. The user confirmed that it is the authoritative file provided for analysis. The repository copy is integrity-pinned at SHA-256 `6f2026c7582e4ac396261b7686e799317515542c59c0ac505da11bf7611de4b5` and size `395338` bytes; automated tests reject accidental replacement or corruption.

## Operating model

The practical sequence is intentionally simple:

1. Use the verified bibliography analyses and repeat freshness searches in `ThesisBibliography` at the defined literature gates.
2. Research and select a small set of scientifically distinct model roles after bibliography import, environment definition, and capability inspection.
3. Build a small working research core and, when useful, an early visual/debug surface for validation.
4. Add only useful settings, logs, charts, history, comparison, and exports.
5. Validate the system, run pilots, freeze the final protocol, and execute final experiments.
6. Collect results, screenshots, figures, tables, videos, and writing notes while the work is being performed.
7. Write the thesis from verified bibliography and frozen evidence.
8. Create the PowerPoint, visuals, key points, and presentation script from the same verified evidence.

Codex executes bounded tasks. GitHub runs automated checks. ChatGPT reviews research, diffs, naming, comments, tests, results, and merges. The user does not need to approve routine GitHub operations; the user is involved in genuinely academic/product decisions and provides feedback from the running system. Later supervisor corrections are incorporated when they are actually received rather than anticipated as current blockers.

The detailed process is defined in `docs/context/EXECUTION_WORKFLOW.md`.

## Agent reading policy

Before substantial work, read only:

1. `AGENTS.md`
2. `README.md`
3. `docs/context/SCOPE_REFINEMENT.md`
4. `docs/context/PROJECT_CONTEXT.md`
5. `docs/context/CONFIRMED_REQUIREMENTS.md`

Then read only the task-specific files defined by `AGENTS.md`. A full repository reread is reserved for bootstrap, repository-wide audits, or major cross-cutting changes.

## Bibliography research and related work

The active policy is defined in:

- `bibliography/README.md`
- `docs/context/BIBLIOGRAPHY_INTEGRATION.md`

`MariosGiannakaras/ThesisBibliography` is the only canonical repository for source acquisition, original PDFs, conversion/OCR, full-source Markdown, scientific analysis, citation-ready evidence, source selection, research materials, author notes, and generated exports.

This repository imports generated bibliography content into:

```text
research/bibliography/
```

The final consumer migration must import the complete generated research corpus while preserving its nested citation-ready layer as the only automatically trusted formal-citation surface. The import remains integrity-protected, reproducible from an explicit immutable ref, excludes PDFs and Git LFS objects, and is synchronized through a Pull Request.

Scientific source text and citation-ready evidence remain in the original source language. Translation for the final Greek thesis occurs only during writing and does not replace canonical evidence.

Literature refresh gates before protocol freeze, Related Work/Methodology/Discussion, and final submission remain mandatory. They are executed in `ThesisBibliography` and enter this repository only through a new verified export/synchronization.

## Repository map

```text
app/                                  Polished local dashboard/control layer
core/                                 Independent research and experimental core
experiments/                          Experiment definitions, runners, and manifests
configs/                              Version-controlled validated configurations
notebooks/                            Controlled exploratory notebooks; not source of truth
scripts/                              Reproducibility, processing, and maintenance scripts
tests/                                Unit, integration, statistical, and reproducibility tests

data/raw/                             Primary data and immutable run inputs/outputs
data/processed/                       Derived data with provenance
results/runs/                         Run outputs and manifests
results/summaries/                    Aggregated analysis outputs
results/thesis-final/                 Frozen thesis evidence set
artifacts/figures/                    Reproducible figures
artifacts/tables/                     Reproducible tables
artifacts/exports/                    CSV/JSON/report exports

research/bibliography/                Generated research corpus from ThesisBibliography
bibliography/                         Integration policy and retired compatibility markers only

thesis/source-material/               Official application and primary thesis material
thesis/chapters/                      Chapter drafts
thesis/final/                         Final Word document and accompanying deliverables

docs/context/                         Source of truth, scope, requirements, and blockers
docs/research/                        Research framing and selection workspaces
docs/experiments/                     Protocol, schemas, and provenance
docs/architecture/                    Bounded application and UI requirements
docs/thesis/                          Writing and formatting requirements
docs/university/                      Official UniWA/Department requirements
docs/decisions/                       Decision log and ADRs
```

## Deferred writing-stage inputs

No supervisor identity, special supervisor instruction, submission deadline, or Word template is required to continue bibliography integration, model research, GridWorld selection, implementation, pilots, or experiments.

The topic has been approved. No additional supervisor requirements or deadlines have been provided. The supervisor may review and request corrections after the work or a draft exists; those corrections will be recorded and incorporated when received.

Near the writing phase, the user may provide two or three completed theses from friends as contextual examples of expected presentation and structure. They are not authoritative requirements and must not override verified Department guidance or an official template.

New bibliography sources or files are added to `ThesisBibliography`, not to this repository.

The application checksum, system-inventory collector, and GridWorld landscape pre-screen are complete. The actual target-system inventory run, complete bibliography-corpus import, and bounded GridWorld prototype/ADR decision remain pending.

## Scientific integrity

Do not fabricate bibliography entries, DOI values, data, runs, metrics, progress, logs, figures, results, or conclusions. Every final result must trace to a real run, configuration, source data, processing code, and Git commit.
