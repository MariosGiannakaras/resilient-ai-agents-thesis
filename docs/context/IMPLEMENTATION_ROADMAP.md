# Implementation Roadmap

The roadmap is phase-gated and optimized for thesis completion, scientific adequacy, and bounded engineering complexity.

## How to use this roadmap

The fourteen numbered phases are **checkpoints**, not fourteen mandatory separate prompts, branches, PRs, or approval meetings. Combine adjacent phases when one bounded task can complete them safely.

Operationally, the work can be managed as eight larger blocks:

1. Research definition, verified bibliography import, and source validation.
2. GridWorld decision and environment specification.
3. Models, metrics, and experimental protocol.
4. Independent core and validation.
5. Pilots and final protocol freeze.
6. Minimal experiment management and polished dashboard.
7. Final experiments, analysis, and artifacts.
8. Thesis writing and final validation.

Use separate review gates only for decisions that materially affect scientific validity, feasibility, architecture, or final evidence.

## Phase 1 — Context and system validation

- **Goal:** Establish trusted sources, current scope, and actual machine capabilities.
- **Deliverables:** Source audit, official-application SHA-256 verification, bibliography-import status, automated hardware/software inventory.
- **Gate:** No compute-dependent or stack decision before completion.

## Phase 2 — Bibliography and research framing

- **Goal:** Convert the official topic and verified bibliography evidence into a clear and bounded research problem.
- **Deliverables:** Validated `research/bibliography/` import with exact `SOURCE_COMMIT`, focused related-work synthesis, main research question, minimal secondary questions, and candidate hypotheses.
- **Source action:** Use the verified generated package from `MariosGiannakaras/ThesisBibliography`. Fresh source discovery/acquisition/verification occurs only in `ThesisBibliography`, followed by controlled export/synchronization; do not acquire papers directly in this repository.
- **Gate:** Every question maps to measurable verified evidence and remains feasible.

## Phase 3 — GridWorld landscape and decision

- **Goal:** Compare reuse, adapt/wrap, and minimal custom implementation.
- **Deliverables:** Candidate matrix, license/maintenance/API audit, small prototypes, and ADR.
- **Gate:** No third-party integration before a documented decision.

## Phase 4 — Environment and uncertainty specification

- **Goal:** Define the simplest environment that adequately answers the research question.
- **Deliverables:** Versioned state/action/reward/termination rules, minimal uncertainty taxonomy, severity design, and validation fixtures.
- **Gate:** Environment reference traces and invariant tests pass.

## Phase 5 — Minimal model and metric selection

- **Goal:** Select only scientifically distinct and feasible models/baselines and outcomes.
- **Deliverables:** Inclusion/exclusion matrix, common agent contract, metric definitions, and estimands.
- **Gate:** No model, uncertainty type, or metric without a distinct research role.

## Phase 6 — Pilot experimental protocol

- **Goal:** Define training/tuning/evaluation separation and pilot work.
- **Deliverables:** Pilot configs, stopping/failure rules, preliminary statistical plan, and compute estimate.
- **Literature refresh:** Recheck recent directly relevant work in `ThesisBibliography`, verify any new evidence there, and synchronize a new package before freezing decisions if the evidence changes the design.
- **Gate:** Protocol can be executed without hidden manual choices.

## Phase 7 — Independent research core

- **Goal:** Implement only environment, selected agent adapters, runner, persistence, manifests, and CLI.
- **Deliverables:** Minimal reproducible headless workflow.
- **Debug UI allowance:** A lightweight visualization/debug surface may be used if it helps validate environment or agent behavior, but it must use the same core interfaces and must not duplicate scientific logic or expand into the final dashboard.
- **Done when:** A full run completes without UI and produces valid real outputs.
- **Gate:** Architecture and contract tests pass.

## Phase 8 — Validation and pilots

- **Goal:** Verify correctness and estimate runtime, variance, failures, and metric behavior.
- **Deliverables:** Unit/integration/recovery tests, pilot registry, and pilot report.
- **Gate:** Pilots answer protocol-design questions; no pilot result is treated as final evidence.

## Phase 9 — Freeze final protocol

- **Goal:** Set a feasible and scientifically fair final experiment matrix.
- **Deliverables:** Frozen models, scenarios, seeds/repetitions, budgets, metrics, statistical plan, and exclusions.
- **Literature refresh:** Confirm through the canonical `ThesisBibliography` evidence chain that no recent primary study materially changes the design or required comparisons; synchronize the verified package used for the freeze.
- **Gate:** Any later change requires an explicit amendment.

## Phase 10 — Minimal experiment management

- **Goal:** Provide reliable run registry, lifecycle state, and recovery required by the frozen protocol.
- **Deliverables:** Real status/events, safe interruption handling, provenance, and essential batch support.
- **Gate:** Do not implement queue priorities, remote workers, or advanced orchestration unless required by measured workflow.

## Phase 11 — Polished bounded dashboard

- **Goal:** Enable the user to execute and understand the thesis experiments without code or console commands.
- **Required workflows:** Dashboard, New Experiment, Runs, Compare, and Artifacts.
- **Required quality:** Modern, consistent, responsive, screenshot-ready, and based on real data.
- **Deliverables:** Configuration/launch, truthful monitoring, GridWorld view, history/details, comparison charts/tables, and export.
- **Scope note:** Telemetry is a lightweight current snapshot. Detailed checksums/provenance use expandable details and exports.
- **Gate:** Every screen and feature maps to a real thesis workflow. Advanced features remain deferred.

## Phase 12 — Final runs

- **Goal:** Produce the frozen thesis evidence set.
- **Deliverables:** Complete run set, checksums, failures/exclusions registry, and immutable raw outputs.
- **Gate:** Completeness and provenance audits pass; no cherry-picking.

## Phase 13 — Statistical analysis and artifacts

- **Goal:** Produce reproducible estimates, figures, tables, and exports.
- **Deliverables:** Versioned scripts, intervals/effect sizes where appropriate, diagnostics, and artifact manifests.
- **Gate:** Every reported value traces to source runs, configs, and code.

## Phase 14 — Thesis writing and final validation

- **Goal:** Complete the Greek Microsoft Word thesis and repository package.
- **Deliverables:** Background, related work, methods, implementation, results, discussion, limitations, conclusions, Word formatting, and reproduction guide.
- **Writing literature review:** Before drafting Related Work, Methodology, and Discussion, complete the required freshness/full-evidence check in `ThesisBibliography`, synchronize the verified package, and write only from the pinned imported `SRC-*` evidence and associated analyses/limitations. Distinguish peer-reviewed work, preprints, and benchmark/tool papers.
- **Submission freshness check:** Recheck recent sources in `ThesisBibliography`, synchronize the final verified bibliography package, and recheck the official Word template/submission guidance shortly before final delivery.
- **Gate:** Claims, citations, figures, cross-references, privacy, and provenance audits pass.

## Completion rule

The project is complete when the research question is answered with reliable evidence and the polished local dashboard supports the required experiment workflow. Production-platform scope is not required.