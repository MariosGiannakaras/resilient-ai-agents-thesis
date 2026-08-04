# AGENTS.md

## Mission

Develop and document a scientifically valid, reproducible, and realistically completable thesis with the official titles:

> **Greek:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα
>
> **English:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

The project compares decision-making agents in a controlled simulated environment under uncertainty and dynamic change. The application is an important research deliverable and a tool for execution, observation, interpretation, and presentation; it is not the main research contribution and must not become a production-grade platform.

This repository is the permanent source of truth for the thesis project, with one explicit boundary: the complete bibliography lifecycle has its canonical source of truth in the separate private repository `MariosGiannakaras/ThesisBibliography`. This repository consumes only its verified generated export.

## Language policy

Repository-authored operational and technical material is written in **English** so Codex, code, tests, APIs, and documentation use one consistent technical language.

This includes:

- agent instructions and prompts,
- repository READMEs and technical/context documentation,
- architecture, protocol, schema, and testing instructions,
- code comments, identifiers, configuration names, branches, commits, and Pull Request text.

Exceptions:

- preserve the exact official Greek thesis title and other official Greek text when it must be quoted faithfully,
- scientific source text and citation-ready evidence remain in the **original language of the source**,
- the final thesis remains a Greek Microsoft Word deliverable unless an official requirement changes.

Do not translate canonical scientific evidence merely to make repository documentation linguistically uniform. Translation for the final Greek thesis is a writing-stage operation.

## Core scope principle

Read and apply `docs/context/SCOPE_REFINEMENT.md`.

**Polished outside, bounded inside.**

Architecture and feature count remain deliberately bounded. The final dashboard must still be modern, polished, coherent, and sufficient for all real thesis workflows. Simplicity does not justify a rough interface, and visual quality does not justify production infrastructure or unnecessary engineering.

## Current accepted technical baseline

DEC-023 is the current architecture authority:

- Python 3.12;
- `uv`, `pyproject.toml`, `.python-version`, and committed `uv.lock`;
- independent importable research package under `src/resilient_agents/`;
- strict evaluator-ground-truth versus agent-visible information separation;
- independent deterministic RNG streams;
- explicit scenario/experiment/protocol contracts without hidden scientific defaults;
- filesystem-first run bundles with provenance/checksums;
- one guarded automatic Git commit and push per finalized whole experiment, never per seed;
- selective Git LFS for configured large thesis-produced artifacts;
- future thin Streamlit dashboard after headless core/pilot validation.

Do not reinterpret old conversations or older bootstrap files as evidence against this accepted baseline. Scientific dependencies and exact dashboard details remain subject to the inventory/prototype/pilot gates.

## Zero-base scientific decisions

Old conversations are historical context only. They do not establish:

- a selected model list,
- an approved GridWorld specification,
- approved metrics,
- approved hyperparameters, seeds, repetitions, or budgets,
- a feature backlog,
- a requirement to recover old code.

Historical stack proposals also have no authority; use the current accepted technical baseline above and record any later architecture amendment explicitly.

Every remaining scientific selection is made from the official application, verified bibliography evidence, official technical documentation, actual hardware/software, prototypes, and pilots.

## Priority order

1. Clear and bounded research question.
2. Simple and validated GridWorld.
3. Small, scientifically justified set of models and uncertainty types.
4. Fair and reproducible experimental protocol.
5. Reliable and comparable results.
6. Modern and complete UI for execution, monitoring, and interpretation.
7. Advanced features only when they solve a real need without threatening thesis completion.

## Operating model and responsibilities

The full process is defined in `docs/context/EXECUTION_WORKFLOW.md`.

- **User:** provides goals, real feedback, source material when needed, and supervisor instructions. The user does not need to approve routine branches, commits, tests, Pull Requests, or merges.
- **ChatGPT:** scopes bounded tasks, reviews research, diffs, naming, comments, tests, experiment evidence, results, and review findings, and decides technical readiness or required corrections.
- **Codex:** executes the assigned bounded task and may continue through objectively resolvable dependent steps; it does not self-approve, silently broaden scientific scope, or change a frozen protocol.
- **GitHub:** runs repeatable automated checks. Passing CI is necessary but not sufficient; test quality and scientific correctness are also reviewed.
- **User consultation:** required only for genuinely academic, product, supervisor-facing, or personal choices that cannot be resolved objectively from evidence.

Normal flow:

> Discuss goal → bounded task → Codex branch/PR → GitHub checks → ChatGPT review → corrections → merge → brief user report

## Reading policy

### Permanent core reading

Before substantial work, read only:

1. `AGENTS.md`
2. `README.md`
3. `docs/context/CURRENT_STATUS.md`
4. `docs/context/SCOPE_REFINEMENT.md`
5. `docs/context/PROJECT_CONTEXT.md`
6. `docs/context/CONFIRMED_REQUIREMENTS.md`

For a local Codex continuation session also read `docs/context/IMPLEMENTATION_ROADMAP.md` and `docs/context/DOCUMENTATION_GOVERNANCE.md`.

### Task-specific reading

- **Research framing / bibliography:** `docs/context/BIBLIOGRAPHY_INTEGRATION.md`, `bibliography/README.md`, the imported `research/bibliography/manifest.csv`, and only relevant imported analyses/evidence. Read `USER_DECISIONS.md`, `CONSTRAINTS.md`, `OPEN_QUESTIONS.md`, `SOURCE_AUDIT.md`, and `docs/research/RESEARCH_BRIEF.md` only when directly relevant. Historical/pre-import workspaces are not current evidence authorities.
- **GridWorld:** `docs/research/GRIDWORLD_SPEC.md`, relevant imported bibliography evidence, and related decisions/ADRs.
- **Models, metrics, and experiments:** the corresponding active candidate/protocol files, relevant imported bibliography evidence, and only the relevant files under `docs/experiments/`.
- **Architecture or UI:** only the relevant `docs/architecture/` files and decisions.
- **Thesis writing:** `docs/thesis/`, `docs/university/`, `research/bibliography/citation-ready/manifest.csv`, and only citation-relevant imported analyses/evidence.
- **Git/GitHub workflow:** `docs/context/EXECUTION_WORKFLOW.md`, `docs/context/DOCUMENTATION_GOVERNANCE.md`, and `.github/pull_request_template.md`.
- **Project-wide decision change:** `docs/decisions/DECISION_LOG.md`, `docs/context/CHANGELOG_CONTEXT.md`, `docs/context/OPEN_QUESTIONS.md`, and `docs/context/CONTRADICTIONS.md`.

Do not reread the entire generated bibliography or entire repository for a small clearly bounded task. A repository-wide active-document audit is required for cross-cutting architecture, workflow, status, or source-of-truth changes.

Do not ask the user for information that can be collected reliably from this repository, `ThesisBibliography`, the local execution system, or authoritative public sources.

## Documentation consistency

Follow `docs/context/DOCUMENTATION_GOVERNANCE.md`.

A material change is incomplete until all affected active documentation is reconciled in the same Pull Request. Do not use `CURRENT_STATUS.md` as an excuse to leave contradictory active files untouched.

For every material change:

1. identify transitive document/prompt/workflow/test dependencies;
2. search active docs for the old assumption, path, count, status, architecture, or blocker;
3. update all affected active files;
4. update `CURRENT_STATUS.md`, `OPEN_QUESTIONS.md`, `DECISION_LOG.md`, and `CHANGELOG_CONTEXT.md` when their claims change;
5. review the current Codex execution prompt when the active phase, responsibilities, architecture, or next task changes;
6. delete obsolete files or mark useful historical files prominently as historical;
7. run the documentation consistency validator before merge.

Generated bibliography content is excluded from manual reconciliation and must only change through the controlled sync workflow.

## Source hierarchy

1. Newer explicit user instruction.
2. Official approved application or formal thesis description.
3. Current official University/Department/supervisor guidance.
4. Verified primary or high-quality scientific literature through the canonical `ThesisBibliography` evidence chain.
5. Official technical documentation, source code, releases, licenses, and reproducible benchmarks.
6. Actual system inventory, prototypes, and pilots.
7. Old conversations only as historical context.

## Bibliography research cycle

Bibliography work is not a one-time action. It is refreshed at these gates:

1. **Initial research framing:** use the completed verified bibliography corpus for related studies, benchmark designs, models, uncertainty mechanisms, and metrics.
2. **Before pilot/final protocol freeze:** search in `ThesisBibliography` for newer or more directly relevant work that could change the design.
3. **Before Related Work, Methodology, and Discussion:** confirm in `ThesisBibliography` that decision-driving sources and claims have complete verified evidence and correctly recorded limitations.
4. **Before final submission:** perform a short freshness and citation audit in `ThesisBibliography`, then create a new controlled export/synchronization.

Full bibliographic identity, stable URL/DOI, publication status, access/license information, method, experimental setup, results, limitations, and thesis relevance are recorded in `ThesisBibliography`, not duplicated here.

Do **not** download or store new papers, PDFs, Markdown source copies, source notes, or excerpts in this repository. New sources, NotebookLM discoveries, and user-provided bibliography files are ingested into `ThesisBibliography`. Scientific source text and citation-ready evidence remain in the source's original language.

`research/bibliography/` is generated and replaced only through the PR-based synchronization workflow. Do not edit it manually and do not alter `SOURCE_COMMIT` or `IMPORT_INTEGRITY.json` by hand.

## Phase order

`docs/context/IMPLEMENTATION_ROADMAP.md` is the canonical phase/checkpoint definition. Do not maintain a second competing phase numbering in this file.

The current next work begins with actual target-machine inventory, GridWorld prototype/ADR work, source-traceable research framing/model roles/metrics, and pilots. Skip any roadmap checkpoint already proven complete by current repository evidence.

A lightweight debug/visualization surface may be used during core development when it helps verify behavior and does not duplicate scientific logic. The **polished final dashboard** remains gated behind a validated independent core and pilot evidence.

## GridWorld discovery

- Do not assume existing user-owned code.
- Compare current reuse, adapt/wrap, and minimal custom implementation.
- Check maintenance, license, API compatibility, determinism, seeding, disturbance extensibility, testability, performance, and dependency cost.
- Do not integrate third-party code before a documented audit, prototype, and ADR.
- Prefer the simplest solution that fully supports the frozen research design.

## Hardware discovery

- Collect CPU, RAM, GPU/VRAM, OS, drivers, runtimes, storage, and supported acceleration automatically on the actual experiment machine.
- Do not ask the user to transcribe information the system can inspect directly.
- Do not assume NVIDIA, CUDA, or usable GPU acceleration.
- Until the accepted capability report exists, keep compute-dependent choices CPU-compatible and unfrozen.

## Research and experiment rules

- Every model, uncertainty type, and metric must map to an approved research question or validity check.
- Keep the design small, understandable, and executable.
- Do not expose unjustifiably many models or parameters to the user.
- Do not choose hyperparameters, seeds, repetitions, or budgets arbitrarily.
- Single-run model comparison is not allowed.
- Keep development, tuning, pilot, exploratory, and final runs distinct as defined by the current protocol contracts.
- Retain failed, cancelled, interrupted, invalid, and excluded runs with reasons.
- Every run stores resolved configuration, seeds, software/hardware snapshot, and source Git commit.
- Raw/finalized results are immutable. Figures and tables are generated from version-controlled scripts and real stored data.
- Do not cherry-pick runs or results.
- A run ID represents one whole experiment and may contain many seeds/episodes.
- Finalized whole experiments use the guarded automatic one-commit/one-push publication path; never create a permanent result commit per seed.

## Software and UI rules

- `src/resilient_agents/` must work without the UI.
- The UI must use the same validated configuration/core interfaces and must not reimplement scientific logic.
- Run/result storage must not depend on the UI lifecycle.
- Filesystem run bundles are the source of truth; any later database/index is rebuildable cache.
- Prefer a modular monolith or equivalently simple local architecture.
- Do not introduce microservices, Kubernetes, cloud infrastructure, multi-user authentication, distributed workers, or production observability.
- Do not add a feature without a real thesis workflow or documented requirement.
- Consolidate screens and controls instead of exposing internal architecture.
- The final UI must be polished, consistent, responsive, and screenshot-ready.
- Essential workflows are configure, run, monitor, inspect GridWorld, review history, compare results, and export artifacts.
- Primary views show only scientifically and operationally useful information. Full checksums, manifests, Git/runtime details, and provenance chains remain available through expandable details or exports.
- Resource telemetry is a lightweight current snapshot: CPU, RAM, disk, and GPU/VRAM only when easy and reliable to support. No historical telemetry charts, monitoring agents, alerting subsystem, or telemetry database are required.
- Fake progress, mock scientific metrics, fabricated logs, and backend-inconsistent state are forbidden.
- Queue priorities, plugins, remote execution, advanced checkpoint UX, and optional AI remain deferred until a real need is demonstrated.

## Tests and validation

Every change that affects the core or experiments needs appropriate tests, including as applicable:

- environment invariants,
- transition/reward/termination behavior,
- seeding and deterministic replay,
- configuration validation,
- information-boundary enforcement,
- run lifecycle and recovery,
- serialization/schema compatibility,
- metric correctness on known-answer fixtures,
- statistical-processing fixtures,
- provenance linkage and automatic publication safety,
- regression tests.

Bibliography-import changes additionally require package/source-commit consistency, forbidden-artifact checks, generated-file integrity, and validation that every canonical `SRC-*` reference exists in the imported manifest.

Synthetic fixtures are allowed only in clearly labelled tests.

Automated checks run on every relevant Pull Request. CI may expand as scientific dependencies and later UI dependencies are selected, but must not become a production deployment pipeline.

## Git and documentation

- Use small logical commits with a concise conventional title and a body that explains **what** changed, **why**, **how it was validated**, and important exclusions.
- Prefer one logical squash merge to `main` for one coherent PR when branch tooling produced many mechanical commits.
- Use descriptive lowercase kebab-case branches with prefixes such as `research/`, `feat/`, `fix/`, `test/`, `docs/`, or `chore/`.
- Research, architecture, protocol, or implementation changes use a branch and Pull Request with summary, rationale, validation, scientific impact, exclusions, and deferred work.
- Follow `.github/pull_request_template.md` and address all automated review findings before merge.
- Do not request routine GitHub approval from the user. ChatGPT decides merge readiness or required corrections unless a genuine academic decision is needed.
- Use clear English naming. Avoid names such as `test2`, `final_new`, `best_model`, or unexplained abbreviations.
- Comments explain non-obvious reasoning, invariants, scientific constraints, or workarounds; they do not restate obvious code.
- Do not store secrets, credentials, caches, or unjustified binaries.
- Large thesis-produced evidence/artifacts are allowed and use the configured Git LFS policy when applicable; bibliography PDFs/LFS objects remain upstream.
- Do not silently change a frozen protocol or raw/final evidence.
- Significant GridWorld, model, metric, stack, storage, runner, and UI-scope decisions must record evidence and alternatives.

## Scientific integrity

Do not fabricate sources, DOI values, citations, runs, metrics, progress, logs, data, figures, tables, results, or conclusions.
