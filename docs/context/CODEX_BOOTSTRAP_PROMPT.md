# Codex Research Bootstrap Prompt

Perform the research clarification for the private repository `MariosGiannakaras/resilient-ai-agents-thesis` and stop before prototype or main implementation.

## Required reading

Read first:

1. `AGENTS.md`
2. `README.md`
3. `docs/context/SCOPE_REFINEMENT.md`
4. `docs/context/PROJECT_CONTEXT.md`
5. `docs/context/CONFIRMED_REQUIREMENTS.md`

Then read only the task-specific files defined by `AGENTS.md`. Do not repeat a full repository audit without a specific reason.

Old conversations are historical context only. They do not define a model shortlist, GridWorld specification, stack preference, metric selection, feature backlog, or experimental design.

## Project direction

The primary objective is a correct, scientifically adequate, and realistically completable thesis.

The application is not a production-grade platform. It remains an important deliverable and must eventually provide a polished, modern, easy-to-use research dashboard for configuration, execution, monitoring, GridWorld observation, history, comparison, and export without code/console commands. Keep internal complexity bounded and add only justified features.

A lightweight debug/visualization surface may be used later during core development if it helps validate behavior. Do not build the polished dashboard before validated core work and pilot evidence.

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` is the canonical source of truth for source discovery, PDFs, conversion/OCR, scientific analysis, verified evidence, and source selection.

This repository must not download or curate new bibliography sources locally.

Use only the verified generated import under `research/bibliography/` and verify:

- `SOURCE_COMMIT`,
- `IMPORT_INTEGRITY.json`,
- `manifest.csv`,
- the relevant imported analyses and evidence,
- canonical `SRC-XXXXXXXXXX` references.

If the import is missing or stale, report the exact synchronization state and use the controlled workflow defined in `docs/context/BIBLIOGRAPHY_INTEGRATION.md`. Do not work around the boundary by copying papers into this repository.

If fresh literature research identifies a real gap, record it as a `ThesisBibliography` freshness/acquisition task. Source-derived scientific text and citation-ready evidence remain in the original language of the source.

## Before any implementation

- Inspect the official application and record the SHA-256 of the repository copy.
- Perform automated inventory of CPU, cores, RAM, GPU/VRAM, OS, drivers, runtimes, storage, tools, and supported acceleration.
- Validate the current bibliography import and exact `SOURCE_COMMIT`.
- Synthesize the directly relevant verified bibliography evidence instead of repeating broad source discovery from scratch.
- Perform a fresh GridWorld technical landscape review and compare reuse, adapt/wrap, and minimal custom implementation.
- Do not integrate third-party GridWorld code before source/license/maintenance/suitability review, a small prototype, and an ADR.

## First mission — four integrated outputs

Do not start GridWorld implementation, model implementation, experiment runner, research core, or polished dashboard. Produce one concise, reviewable evidence package with the following sections.

### 1. Source and system validation

- Official application status and repository SHA-256.
- Bibliography import status, exact `SOURCE_COMMIT`, integrity status, and any synchronization blocker.
- Automated hardware/software inventory.
- Small capability-benchmark plan only for decisions that actually depend on compute.

### 2. Bounded research design

Propose one coherent design containing:

- one clear main research question and only necessary secondary questions/hypotheses,
- minimal uncertainty taxonomy and environment direction,
- small scientifically useful model/baseline set with inclusion/exclusion rationale,
- primary/secondary/diagnostic metrics with operational definitions,
- pilot outline for correctness, runtime, variance, and metric sensitivity,
- small dashboard feature budget: required, justified-later, out-of-scope.

Ground each decision-driving claim in imported verified `SRC-*` evidence where applicable. Do not create separate long reports for every subsection; show dependencies and trade-offs in one integrated proposal.

### 3. GridWorld and related-work recommendation

- Fresh build/reuse/adapt matrix covering maintenance, license, API, determinism, extensibility, testability, dependencies, and integration cost.
- Recommend only one or two options worth a small prototype; do not integrate them yet.
- Review a focused set of directly relevant verified studies from the imported bibliography. For each study, record setting, method, experimental design, main results, limitations, and specific relevance to this thesis.
- Use the current imported bibliography analyses/evidence as the authoritative related-work basis. Do not update the historical `RELATED_WORK_EVIDENCE_MATRIX.md` as if it were canonical evidence.
- If a material literature gap is discovered, record the exact gap for follow-up in `ThesisBibliography` rather than acquiring sources here.

### 4. Decision/review package

Present:

- proposed decisions,
- important rejected alternatives and why,
- blockers and assumptions,
- files changed,
- the exact next bounded implementation/research task after review.

Update only relevant context, research, architecture, decision, and changelog files.

## Evaluation criteria

The proposed design must be:

- small enough to complete and explain,
- scientifically adequate for the official topic,
- feasible on measured hardware and available time,
- reproducible and testable,
- capable of producing clear comparable results,
- compatible with a polished but bounded dashboard.

Reject alternatives that add models, uncertainty types, parameters, screens, or infrastructure without distinct research or thesis-delivery value.

## Mandatory rules

- Keep official titles unchanged.
- Keep repository-authored operational/technical documentation in English.
- Keep scientific source-derived evidence in the original source language.
- The research core must work without the UI.
- A lightweight debug visualization is allowed later for validation; the polished dashboard remains gated behind validated core and pilot evidence.
- Use multiple seeds/repetitions; no single-run comparison.
- Keep pilot, exploratory, and final runs distinct.
- Retain failures, cancellations, interruptions, and exclusions.
- No fake progress, logs, metrics, data, or results.
- Raw results are immutable and have complete backend provenance.
- Telemetry remains a lightweight current snapshot, not a monitoring subsystem.
- Checksums, manifests, and detailed provenance use progressive disclosure or exports rather than cluttering primary views.
- Do not fabricate bibliography entries, DOI values, measurements, or conclusions.
- Do not inherit preferences from historical chats.
- Do not add production infrastructure or advanced features without documented need.
- Use small controlled commits and avoid overengineering.
- The final thesis is a Greek Microsoft Word deliverable under current official guidance.

Stop after presenting the first mission package. Do not start prototype or implementation until the research-direction decisions have been reviewed.