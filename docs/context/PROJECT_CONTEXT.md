# Project Context

## Status taxonomy

- **CONFIRMED:** established by the official application or an explicit current user instruction.
- **RESEARCH_REQUIRED:** must be evaluated again with current research before a proposal or decision is made.
- **PROPOSED:** evidence-backed proposal that has not yet been approved.
- **OPEN:** critical information or a decision is still missing.
- **UNVERIFIED:** mentioned but not yet checked against a primary source, code, or the real system.
- **HISTORICAL_CONTEXT_ONLY:** appeared in an old conversation and is retained only for historical understanding; it is not a candidate or preference by itself.

## What the project is

This project is the complete research, experimental, technical, and writing infrastructure for the thesis:

> **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**

Academic context — **CONFIRMED**:

- University of West Attica.
- School of Engineering.
- Department of Informatics and Computer Engineering.
- Department thesis, according to the official application.
- Main thesis text in Greek and final deliverable in Microsoft Word.

The supervisor's name, supervisor-specific requirements, and deadline remain **OPEN**.

## Official academic purpose

The official application defines the objective as the study and comparative evaluation of resilient AI agents in environments with uncertainty and dynamic change. Using a simple simulated environment, decision-making algorithms must be compared with respect to their ability to adapt to unexpected changes. The application gives examples including:

- data/observation noise,
- rule changes,
- action-execution failures.

Evaluation must address resilience and recovery speed.

## Bibliography and scientific evidence

Primary bibliography management no longer occurs in this repository.

The private repository `MariosGiannakaras/ThesisBibliography` is the independent canonical source of truth for source discovery, metadata, originals, Markdown/OCR, scientific analysis, verified evidence, inclusion/exclusion decisions, and controlled thesis export.

The current complete scientific selection has been completed there for **580/580 active sources**. Canonical status records **109 selected/verified sources**, **470 exclusions**, **1 theory-only/non-citation source**, **0 pending decisions**, and **109 verified evidence sets**.

This repository consumes only the verified generated package under `research/bibliography/`, bound to an exact `SOURCE_COMMIT`. It does not copy the full bibliography repository, PDFs, raw conversion material, or repository history.

Synchronization is pull-based and performed through a Pull Request. The binding architecture is defined in `docs/context/BIBLIOGRAPHY_INTEGRATION.md` and `bibliography/README.md`.

The first controlled synchronization is currently **BLOCKED** at cross-repository authentication. A real synchronization run on 2026-08-03 confirmed that the `BIBLIOGRAPHY_SYNC_TOKEN` repository secret is non-empty, but `actions/checkout` cannot authenticate a read-only fetch of the private `MariosGiannakaras/ThesisBibliography` repository. The failed run stopped before export/import, so `research/bibliography/` has not been populated and no bibliography content was partially installed. The secret must be replaced with a valid credential that has read access to `ThesisBibliography`, after which a fresh controlled trigger can be used without changing the integration design.

Source-derived scientific text and citation-ready evidence remain in the original language of the source. Translation for the final Greek thesis occurs only during writing and does not replace the original-language evidence record.

Literature freshness gates remain active before protocol freeze, major writing gates, and final submission. New searches and verification occur in `ThesisBibliography` and enter this repository only through a new verified export.

## Role of GridWorld

GridWorld is the currently confirmed direction for the simple controlled environment. The final implementation has not been selected.

The choice starts from zero and compares:

1. a current library/framework that can be reused or adapted,
2. a small custom implementation,
3. a library plus project-specific wrappers/extensions.

There is no requirement to recover old user-owned code. Any third-party repository or package must be discovered through fresh research and pass license, maintenance, API, determinism, testability, and suitability review before download or integration.

The final environment must support:

- explicit states, actions, goals, obstacles, rewards, and termination semantics,
- parameterized uncertainty/change mechanisms,
- seeded and repeatable experiments,
- trace/metric/artifact production,
- execution independently from the dashboard.

## Role of models

Models/algorithms are the compared agents or baselines. **There is no shortlist inherited from old conversations.** Selection will use verified bibliography evidence, final GridWorld/observability framing, the hardware/software inventory, feasibility prototypes, and pilots.

`MODEL_CANDIDATES.md` is a selection process and evidence matrix, not a preselected model catalog.

## Role of experiments

Experiments are the primary mechanism for producing scientific findings. They must:

- follow a predefined protocol,
- include multiple seeds/repetitions,
- keep pilot, exploratory, and final runs distinct,
- store complete run provenance,
- retain failures/cancellations/exclusions,
- support fair statistical comparison,
- produce real figures and tables.

No historical run count, seed count, budget, or hyperparameter is carried forward as a default or candidate without new justification.

## Role of the dashboard

The dashboard is a supporting tool for one local user. It should reduce reliance on manual scripts/console commands and provide configuration, run control, truthful status/progress/logs/metrics, GridWorld visualization, history/comparison, exports, and screenshot-ready views.

It is not the main research contribution. A lightweight debug/visualization surface may support core validation, but the polished final dashboard follows validated core work and pilot evidence.

## Role of thesis writing

Writing develops alongside implementation, but every chapter distinguishes verified facts/citations, proposed methodology, frozen protocol, real results, interpretation, and limitations. Final conclusions are written only from the frozen final result set.

Bibliographic claims connect to canonical `SRC-XXXXXXXXXX` identifiers present in the imported manifest and to verified evidence from the corresponding `SOURCE_COMMIT`.

## Connection between application, results, and thesis text

```text
Official topic + verified bibliography + system inventory
          ↓
Research questions / hypotheses
          ↓
GridWorld build/reuse decision + model/metric selection
          ↓
Versioned experiment protocol
          ↓
Independent core + validated pilots
          ↓
Immutable raw results + provenance
          ↓
Processing scripts → figures/tables
          ↓
Dashboard exploration + thesis evidence
          ↓
Greek Microsoft Word thesis
```

## What is still missing

- Valid cross-repository read credential for the first controlled `ThesisBibliography` synchronization.
- Actual automated hardware/software inventory and capability benchmark.
- Fresh GridWorld landscape review and build/reuse/integration decision, using verified bibliography evidence as the basis.
- Supervisor identity and supervisor-specific academic instructions.
- Final research questions/hypotheses.
- Final environment variants, models, metrics, and statistical protocol.
- Current official Word template/submission package.
- First successful synchronization of the verified `ThesisBibliography` package into `research/bibliography/`.
