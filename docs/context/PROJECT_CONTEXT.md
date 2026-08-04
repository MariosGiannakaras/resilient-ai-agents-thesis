# Project Context

## Status taxonomy

- **CONFIRMED:** established by the official application, current explicit user instruction, or an accepted repository decision.
- **RESEARCH_REQUIRED:** requires current scientific/technical evidence before selection.
- **PROPOSED:** evidence-backed proposal not yet frozen.
- **OPEN:** unresolved decision or external input still needed.
- **DEFERRED:** valid later-stage input that does not block current research/implementation.
- **HISTORICAL_CONTEXT_ONLY:** retained only to explain earlier reasoning; not active guidance.

## Project identity

This repository is the permanent private source of truth for the complete thesis lifecycle:

> **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**

Confirmed academic context:

- University of West Attica, School of Engineering, Department of Informatics and Computer Engineering.
- Official English title: **Comparison and Evaluation of Resilient AI Agents in Uncertain Environments**.
- Topic approved by the supervisor.
- Final thesis remains a Greek Microsoft Word deliverable unless official guidance changes.
- No current supervisor-specific instruction or deadline blocks the research/program work.

The official application defines the broad objective: compare resilient decision-making agents in a simple simulated environment under uncertainty/dynamic change, including examples such as observation/data noise, rule changes, and action-execution failures, with evaluation of resilience and recovery speed.

## Bibliography — current accepted state

`MariosGiannakaras/ThesisBibliography` is the canonical source of truth for source discovery, originals/PDFs, conversion/OCR, canonical Markdown, scientific analysis, evidence verification, source selection, research materials, notes, and generated exports.

The first complete immutable consumer import is **finished** and accepted by DEC-021/DEC-022.

Pinned baseline:

- requested ref: `bibliography-integration-v2`;
- checkout: `27e325a74722b8f80643e6d1902e4bf3847036f5`;
- complete-corpus source commit: `ca511a0ff91388e7798e011642cc6b5608b336d8`;
- citation-ready source commit: `ef44fe3c30e6648f591ad9d3546ffc336fce4287`;
- 583 canonical sources;
- 112 citation-ready selected sources;
- 19 research materials;
- metadata for 280 indexed original PDFs;
- 1561 consumer-recorded corpus files.

Private authentication/read access, upstream validators, SHA-256 manifests, ancestry, consumer integrity, contextual source-reference validation, and repository tests passed for this baseline. The former HTTP 401 and incomplete-import blockers are resolved.

`research/bibliography/citation-ready/` is the only automatic formal-citation surface. Full-corpus/rejected/theory-only/`MAT-*`/note content remains available for internal research without silent promotion. New formal evidence promotion occurs only upstream in `ThesisBibliography`, followed by a new immutable synchronization.

No bibliography PDF or bibliography Git LFS object is imported into this repository.

## Current technical architecture — accepted

DEC-023 establishes the current implementation baseline:

- Python 3.12;
- `uv`, `pyproject.toml`, `.python-version`, and committed `uv.lock`;
- independent importable package at `src/resilient_agents/`;
- strict separation of evaluator ground truth from agent-visible information;
- deterministic independent RNG streams;
- explicit scenario/experiment/change/protocol contracts with no hidden scientific defaults;
- filesystem-first self-contained run bundles with resolved config, capability snapshot, provenance, checksums, events/traces, and summary;
- one guarded automatic Git commit and push per finalized **whole experiment**, never per seed;
- selective Git LFS for configured large thesis-produced artifacts;
- filesystem run bundles as source of truth; any later database/index is rebuildable cache;
- future final dashboard as a thin local Streamlit layer over the same core, after headless workflow/pilot validation.

Large thesis-produced experiment artifacts are retained by default rather than manually excluded merely because they are large. The configured LFS policy handles selected large formats; retention is revisited only if a real storage constraint appears.

## Codex execution continuity — accepted

DEC-025 establishes `docs/context/TASKS.md` as the single concrete execution checklist and resumable progress ledger.

Every Codex session reads it before selecting/resuming work. Codex uses available session/conversation memory to continue efficiently, but verifies that memory against durable repository evidence: branch/commits, working-tree diff, PR state, tests, task state, and active docs. If model quota/session interruption occurs, unfinished work is resumed rather than reconstructed or restarted.

Intermediate branch commits are allowed as recovery checkpoints. Coherent work still normally reaches `main` through a squash merge, so recovery checkpoints do not create unnecessary permanent main history.

`READY` has a strict meaning: required task dependencies are complete. Future work remains `BLOCKED`/`DEFERRED` until its dependencies/conditions actually permit execution.

## End-to-end lifecycle — accepted

DEC-026 defines how the project continues beyond implementation. `IMPLEMENTATION_ROADMAP.md` explains the phase order, `EXECUTION_WORKFLOW.md` records responsibilities/handoffs, and `TASKS.md` is the only concrete status/dependency ledger.

The intended handoff chain is:

> validated research/pilots -> frozen protocol -> validated application -> final experiments -> frozen evidence/statistics -> thesis/defense evidence package -> Greek thesis/review/final freeze -> PowerPoint defense package -> final audit/delivery

The polished application is not the end of the project. It becomes the validated user-facing execution surface for the frozen final experiment campaign. Final experiments normally wait for both the frozen protocol and validated application workflow so the user does not have to switch to a separate manual execution path.

After final analysis, a dedicated evidence package maps RQs, protocol/method references, citation-ready sources, run/result IDs, figures/tables/captions, and planned claims. Thesis and presentation work consume this package rather than reinterpreting raw runs ad hoc.

The final defense phase is already specified but deferred. `docs/thesis/PRESENTATION_WORKFLOW.md` requires a final `.pptx`, embedded speaker notes, a separate full spoken Greek script, evidence mapping, validated application screenshots/demo fallback, and rehearsal/PowerPoint checks. Codex prepares/verifies repository-backed evidence/assets; ChatGPT is the preferred narrative/Greek-writing/speaker-script layer; PowerPoint-capable tooling creates the file and Microsoft PowerPoint is the final inspection/rehearsal target.

## Research direction — not frozen

The imported evidence supports a bounded direction but does not yet freeze the final protocol:

- distinguish robustness from post-change adaptation/recovery;
- use persistent rule/dynamics change as the leading recovery axis;
- treat observation corruption and action-execution failure as supporting robustness diagnostics unless the final RQ requires more;
- evaluate nominal performance, disruption depth, recovery trajectory/time, post-change performance, non-recovery, and across-run uncertainty rather than one opaque resilience score;
- compare a small number of scientifically distinct capability roles rather than a catalogue of algorithms;
- keep the tuning/pilot/final boundary explicit and leakage-resistant.

Decision-driving citation-ready evidence currently includes `SRC-70772C0629`, `SRC-9464421E55`, and `SRC-76B2247457`. Robust-MDP full-corpus records may guide internal research but require upstream verification/promotion before supporting a formal final claim if that comparator is retained.

## GridWorld — current state

GridWorld remains the confirmed simple controlled environment direction. The final implementation is **not yet selected**.

The technical landscape pre-screen retained two bounded prototype paths:

1. a small project-owned Gymnasium-compatible environment;
2. a thin MiniGrid adaptation if inherited semantics do not introduce unnecessary confounds.

The final choice requires the bounded prototype/ADR gate. Current shared contracts in `src/resilient_agents/` should be reused rather than creating a second environment interface.

## Models and metrics — current state

There is no final algorithm shortlist, metric set, seed count, severity set, hyperparameter set, or statistical plan.

Selection remains evidence/pilot driven. Candidate roles are intentionally small: nominal/reference behavior, a naive continual learner, a robustness-oriented comparator only if its assumptions/evidence fit, an explicit change/context-aware adaptive comparator, and an optional detector/reset decomposition only if it answers a distinct question.

Metric primitives and known-answer test infrastructure now exist, but final estimands/thresholds/windows are not frozen. Non-recovery must remain explicit rather than being replaced with the experiment horizon.

## Experiments and repository automation

A run ID represents one whole experiment and may contain many seeds/episodes.

The intended user workflow is:

> configure experiment -> run -> automatic persistence/provenance -> finalize -> one guarded commit/push

The user should not manually stage, commit, move, or upload routine experiment artifacts. Publication safety may block the Git operation when provenance/working-tree/remote conditions are unsafe, but local run data is preserved.

Development, tuning, pilot, exploratory, and final evidence remain separated. Final figures/tables are generated only from real stored data by version-controlled code. Final experiment execution is followed by explicit run-completeness validation and evidence freeze before statistical interpretation/writing.

## Dashboard, thesis writing, and defense

The dashboard is a supporting local single-user tool, not the scientific contribution. A small debug surface may be used during environment/core validation; the polished Streamlit dashboard follows pilot-established workflows and must not duplicate scientific logic.

Application completion requires the actual user workflow—not only rendered screens—to work on real backend state: configure, run/monitor, history, compare/detailed analysis, and artifacts/export.

Normal chapter drafting and final Word styling remain later stages. Structured evidence mappings, method records, captions, figures, tables, provenance, and task progress are collected during implementation; a formal evidence package is frozen after final analysis so writing is not reconstructed from memory.

A review-ready thesis precedes final thesis freeze. Supervisor/reviewer corrections are incorporated when received and affected evidence/citations/figures/method descriptions are revalidated.

The final presentation is a distinct downstream deliverable after thesis stability, not an independent manual summary. It inherits the same evidence mappings and is finalized only after speaker notes/script, PowerPoint rendering, timing, factual consistency, and demo fallback checks pass.

## Current genuine gates

The canonical concrete task/dependency list is `docs/context/TASKS.md`. The current first gate is `T-100`: actual system inventory on the thesis experiment machine. GridWorld, research framing, metrics, model selection, pilots, application, final experiments/evidence, writing/review, presentation, and audits follow the dependency/acceptance conditions recorded in that registry.

Deferred, non-blocking inputs remain later supervisor corrections, eventual submission/presentation dates, a current official Word template, exact defense duration/file rules, and optional contextual example theses supplied near writing.

## Current authority

Use:

- `docs/context/CURRENT_STATUS.md` for the shortest current-state summary;
- `docs/context/TASKS.md` for concrete task status/resume/next action;
- `docs/context/IMPLEMENTATION_ROADMAP.md` for phase/dependency explanation;
- `docs/context/EXECUTION_WORKFLOW.md` for responsibilities and major handoffs;
- `docs/context/DOCUMENTATION_GOVERNANCE.md` for keeping related files synchronized;
- `docs/thesis/PRESENTATION_WORKFLOW.md` for the deferred defense workflow.

Historical bootstrap/pre-import records must not be used as current blockers or instructions.
