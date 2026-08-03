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

The first controlled synchronization is currently **BLOCKED** at cross-repository authentication. The hardened credential probe was rerun on 2026-08-03 and the configured `BIBLIOGRAPHY_SYNC_TOKEN` produced **HTTP 401 Bad credentials** when requesting canonical content from the private `MariosGiannakaras/ThesisBibliography` repository. The workflow therefore stopped before checkout, export, or import. `research/bibliography/` has not been populated and no bibliography content was partially installed. The secret must be replaced with a valid credential that has read access to `ThesisBibliography`; the existing integration architecture does not need redesign.

Source-derived scientific text and citation-ready evidence remain in the original language of the source. Translation for the final Greek thesis occurs only during writing and does not replace the original-language evidence record.

Literature freshness gates remain active before protocol freeze, major writing gates, and final submission. New searches and verification occur in `ThesisBibliography` and enter this repository only through a new verified export.

## Current research proposal — not frozen

Direct inspection of decision-driving canonical analyses has produced a deliberately non-binding pre-import framing workspace under `docs/research/`.

The current **PROPOSED** direction is:

- treat robustness without post-change learning separately from adaptation/recovery;
- use persistent environment/rule/dynamics change as the primary resilience/recovery axis;
- retain observation noise and action-execution failure as supporting robustness diagnostics rather than three symmetric full recovery experiments;
- preserve nominal utility, immediate degradation, failure/recovery profiles, recovery speed, post-change performance, non-recovery, and across-run uncertainty instead of relying on one opaque resilience score;
- keep recurring-context recall conditional rather than mandatory;
- select exact algorithms only after controlled bibliography import, target-system inventory, environment prototypes, and feasibility checks.

This proposal is documented in `docs/research/PREIMPORT_RESEARCH_FRAMING.md` and `docs/research/PREIMPORT_SCOPE_REVIEW.md`. It must not be treated as final methodology or citation-ready thesis evidence.

## Role of GridWorld

GridWorld is the currently confirmed direction for the simple controlled environment. The final implementation has not been selected.

The fresh 2026-08-03 technical landscape pre-screen is complete. It retained two bounded prototype candidates:

1. a small project-owned environment implementing the Gymnasium API;
2. a thin MiniGrid adaptation if the required semantics remain transparent and the inherited action/observation conventions do not introduce confounds.

Gymnasium Toy Text environments remain reference fixtures only, and Griddly is not retained for initial prototyping because its engine/dependency surface is disproportionate to the current scope.

The final choice still requires bounded prototypes and an ADR. There is no requirement to recover old user-owned code. Any third-party repository or package must pass license, maintenance, API, determinism, testability, and suitability review before integration.

The final environment must support:

- explicit states, actions, goals, obstacles, rewards, and termination semantics,
- parameterized uncertainty/change mechanisms,
- seeded and repeatable experiments,
- trace/metric/artifact production,
- execution independently from the dashboard.

## Role of models

Models/algorithms are the compared agents or baselines. **There is no algorithm shortlist inherited from old conversations or created by the pre-import framing work.** Selection will use verified imported bibliography evidence, final GridWorld/observability framing, the target-system hardware/software inventory, feasibility prototypes, and pilots.

`MODEL_CANDIDATES.md` is a selection process and evidence matrix, not a preselected model catalog. The current workspace uses capability roles only: nominal reference, robustness-oriented comparator, online-adaptive comparator, and optional context-recall capability.

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

- A valid cross-repository read credential for the first controlled `ThesisBibliography` synchronization.
- Execution and acceptance of the automated hardware/software inventory on the actual target system; the collector itself is implemented and tested.
- Bounded custom-Gymnasium versus MiniGrid prototypes and the final GridWorld ADR; the fresh landscape pre-screen is complete.
- Supervisor identity and supervisor-specific academic instructions.
- Final research questions/hypotheses; pre-import candidates exist but are not frozen.
- Final uncertainty mechanisms/severities, environment variants, models, metrics, and statistical protocol.
- Current official Word template/submission package.
- First successful synchronization of the verified `ThesisBibliography` package into `research/bibliography/`.
