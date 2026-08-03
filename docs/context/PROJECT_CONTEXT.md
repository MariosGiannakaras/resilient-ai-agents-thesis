# Project Context

## Status taxonomy

- **CONFIRMED:** established by the official application or an explicit current user instruction.
- **RESEARCH_REQUIRED:** must be evaluated again with current research before a proposal or decision is made.
- **PROPOSED:** evidence-backed proposal that has not yet been approved.
- **OPEN:** critical information or a decision is still missing.
- **UNVERIFIED:** mentioned but not yet checked against a primary source, code, or the real system.
- **HISTORICAL_CONTEXT_ONLY:** appeared in an old conversation and is retained only for historical understanding; it is not a candidate or preference by itself.
- **DEFERRED:** valid later-stage input that does not block the current research or implementation phase.

## What the project is

This project is the complete research, experimental, technical, and writing infrastructure for the thesis:

> **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**

Academic context — **CONFIRMED**:

- University of West Attica.
- School of Engineering.
- Department of Informatics and Computer Engineering.
- Department thesis, according to the official application.
- Main thesis text in Greek and final deliverable in Microsoft Word.
- The proposed topic has been approved by the supervisor.
- No current supervisor-specific instructions or deadlines have been provided.
- The supervisor may provide corrections after implementation, experiments, or a draft is available; later feedback is incorporated when received and is not anticipated as a current blocker.

Supervisor identity, eventual submission dates, and final Word-format examples are **DEFERRED**, not open blockers for bibliography integration, model research, GridWorld work, implementation, pilots, or experiments.

## Official academic purpose

The official application defines the objective as the study and comparative evaluation of resilient AI agents in environments with uncertainty and dynamic change. Using a simple simulated environment, decision-making algorithms must be compared with respect to their ability to adapt to unexpected changes. The application gives examples including:

- data/observation noise,
- rule changes,
- action-execution failures.

Evaluation must address resilience and recovery speed.

## Bibliography and scientific evidence

Primary bibliography management does not occur in this repository.

The private repository `MariosGiannakaras/ThesisBibliography` is the independent canonical source of truth for source discovery, metadata, originals, Markdown/OCR, scientific analysis, verified evidence, inclusion/exclusion decisions, otherwise-uncovered research material, author notes, and controlled exports.

The current complete scientific selection has been completed there for **583/583 active sources**. Canonical status records **112 selected/verified sources**, **470 exclusions**, **1 theory-only/non-citation source**, **0 pending decisions**, and **112 verified evidence sets**. The complete generated research corpus additionally preserves all canonical source text and identified `MAT-*` material for writing and discovery.

The final thesis-repository consumer architecture imports the complete generated `research-corpus/` under `research/bibliography/`, while the nested `citation-ready/` directory remains the strict formal-citation layer. The repository does not copy original PDFs, Git LFS objects, conversion workspaces, or bibliography repository history.

Synchronization remains pull-based and performed through a Pull Request. The binding architecture is defined in `docs/context/BIBLIOGRAPHY_INTEGRATION.md` and `bibliography/README.md`; the current citation-only consumer implementation still requires migration before the first complete-corpus import.

On 2026-08-04 the user created a fine-grained token and replaced the `BIBLIOGRAPHY_SYNC_TOKEN` Actions secret in this repository. The token value is not stored in Git or chat. Effective read access must be tested by the migrated synchronization workflow before any generated import directory is replaced. The previous HTTP 401 result describes the superseded credential and must not be treated as the current secret's tested outcome.

Source-derived scientific text and citation-ready evidence remain in the original language of the source. Translation for the final Greek thesis occurs only during writing and does not replace the original-language evidence record.

Literature freshness gates remain active before protocol freeze, major writing gates, and final submission. New searches and verification occur in `ThesisBibliography` and enter this repository only through a new verified export.

## Current research proposal — not frozen

Direct inspection of decision-driving canonical analyses has produced deliberately non-binding pre-import research workspaces under `docs/research/`.

The current **PROPOSED** direction is:

- treat robustness without post-change learning separately from adaptation/recovery;
- use persistent environment/rule/dynamics change as the primary resilience/recovery axis;
- retain observation noise and action-execution failure as supporting robustness diagnostics rather than three symmetric full recovery experiments;
- preserve nominal utility, immediate degradation, failure/recovery profiles, recovery speed, post-change performance, non-recovery, and across-run uncertainty instead of relying on one opaque resilience score;
- keep recurring-context recall conditional rather than mandatory;
- compare capability roles rather than building an algorithm catalogue, with CPU-friendly tabular prototypes preferred until evidence or environment complexity requires function approximation;
- select exact algorithms only after controlled bibliography import, target-system inventory, environment prototypes, and feasibility checks.

The August 2026 freshness pass tightened three methodological points without freezing them as final protocol:

1. ordinary tabular Q-learning should not be described as intrinsically incapable under every form of non-stationarity; recent structured Markov-switching theory gives convergence under explicit assumptions, so the thesis must define and test its specific changepoint/recovery regime empirically;
2. detector-based methods need practical-horizon activation/delay/error validation rather than relying only on asymptotic non-stationary guarantees; recent empirical evidence motivating quickest-change-detection restart methods is bandit-specific and must not be generalized directly to GridWorld MDPs;
3. final non-stationary trajectories should not be reused as an unrestricted hyperparameter-tuning surface; the tuning/pilot/final-evaluation boundary must be fixed before final evidence is inspected, without copying a universal tuning fraction from another study.

These proposals are documented in `docs/research/PREIMPORT_RESEARCH_FRAMING.md`, `docs/research/PREIMPORT_SCOPE_REVIEW.md`, `docs/research/PREIMPORT_AGENT_FAMILY_REVIEW.md`, and `docs/research/PREIMPORT_FRESHNESS_IMPLICATIONS.md`. They must not be treated as final methodology or citation-ready thesis evidence until the complete bibliography corpus import provides canonical source-ID traceability.

The user's immediate priority is the program and the scientific research/selection of models. Normal prose writing, final Word layout, and presentation preparation remain later phases, although structured writing notes and reproducible artifacts should be collected during research and implementation.

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

Models/algorithms are the compared agents or baselines. **There is no final algorithm shortlist inherited from old conversations or created by the pre-import framing work.** Selection will use verified imported bibliography evidence, final GridWorld/observability framing, the target-system hardware/software inventory, feasibility prototypes, and pilots.

`MODEL_CANDIDATES.md` remains the formal selection process and evidence matrix. The current pre-import agent-family review uses capability roles only: frozen nominal reference, naive continual learner, robustness-oriented comparator, explicit change/context-aware comparator, and an optional detector-reset decomposition if pilots show that it is scientifically necessary.

Model research is an immediate project priority. It must compare scientifically distinct capability roles, evidence, information access, feasibility, and implementation risk rather than accumulating many named algorithms.

## Role of experiments

Experiments are the primary mechanism for producing scientific findings. They must:

- follow a predefined protocol,
- include multiple seeds/repetitions,
- keep pilot, exploratory, and final runs distinct,
- store complete run provenance,
- retain failures/cancellations/exclusions,
- support fair statistical comparison,
- produce real figures and tables.

No historical run count, seed count, budget, hyperparameter, detector threshold, or tuning fraction is carried forward as a default or candidate without new justification.

## Role of the dashboard

The dashboard is a supporting tool for one local user. It should reduce reliance on manual scripts/console commands and provide configuration, run control, truthful status/progress/logs/metrics, GridWorld visualization, history/comparison, exports, and screenshot-ready views.

It is not the main research contribution. A lightweight debug/visualization surface may support core validation, but the polished final dashboard follows validated core work and pilot evidence.

## Role of thesis writing

Writing develops alongside implementation only as structured notes, definitions, evidence mappings, method records, and artifact captions. Normal chapter drafting and final Word styling are later phases after the research system, protocol, and evidence are sufficiently mature.

Every chapter must distinguish verified facts/citations, proposed methodology, frozen protocol, real results, interpretation, and limitations. Final conclusions are written only from the frozen final result set.

Bibliographic claims connect to canonical `SRC-XXXXXXXXXX` identifiers present in the imported citation-ready manifest and to verified evidence from the corresponding source commit.

Near the writing phase, the user may provide two or three completed theses from friends as contextual examples of expected structure and presentation. They are not authoritative requirements and must not override verified Department instructions, supervisor corrections, or an official template if one later becomes available.

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

Current research/implementation blockers or gates:

- Migration of the thesis consumer from the citation-only package to the complete `research-corpus/` contract and the first successful controlled import.
- Execution and acceptance of the automated hardware/software inventory on the actual target system; the collector itself is implemented and tested.
- Bounded custom-Gymnasium versus MiniGrid prototypes and the final GridWorld ADR; the fresh landscape pre-screen is complete.
- Final research questions/hypotheses; pre-import candidates and freshness implications exist but are not frozen.
- Final uncertainty mechanisms/severities, environment variants, model set, metrics, tuning boundary, and statistical protocol.

Deferred non-blocking writing/delivery inputs:

- Any later supervisor corrections.
- Eventual submission/presentation dates and procedure.
- A current official Word template, or later contextual example theses supplied by the user.
