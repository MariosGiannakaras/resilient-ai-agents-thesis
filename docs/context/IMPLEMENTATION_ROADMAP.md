# Implementation Roadmap

The roadmap is phase-gated and optimized for thesis completion, scientific adequacy and bounded engineering complexity.

## Phase 1 — Context and system validation

- **Goal:** Establish trusted sources, current scope and actual machine capabilities.
- **Deliverables:** Source audit, SHA-256 verification, automated hardware/software inventory.
- **Gate:** No compute-dependent or stack decision before completion.

## Phase 2 — Bibliography and research framing

- **Goal:** Convert the official topic into a clear and bounded research problem.
- **Deliverables:** Verified bibliography inventory, main research question, minimal secondary questions and candidate hypotheses.
- **Gate:** Every question maps to measurable evidence and remains feasible.

## Phase 3 — GridWorld landscape and decision

- **Goal:** Compare reuse, adapt/wrap and minimal custom implementation.
- **Deliverables:** Candidate matrix, license/maintenance/API audit, small prototypes and ADR.
- **Gate:** No third-party integration before documented decision.

## Phase 4 — Environment and uncertainty specification

- **Goal:** Define the simplest environment that adequately answers the research question.
- **Deliverables:** Versioned state/action/reward/termination rules, minimal uncertainty taxonomy, severity design and validation fixtures.
- **Gate:** Environment reference traces and invariant tests pass.

## Phase 5 — Minimal model and metric selection

- **Goal:** Select only scientifically distinct and feasible models/baselines and outcomes.
- **Deliverables:** Inclusion/exclusion matrix, common agent contract, metric definitions and estimands.
- **Gate:** No model, uncertainty type or metric without a distinct research role.

## Phase 6 — Pilot experimental protocol

- **Goal:** Define training/tuning/evaluation separation and pilot work.
- **Deliverables:** Pilot configs, stopping/failure rules, preliminary statistical plan and compute estimate.
- **Gate:** Protocol can be executed without hidden manual choices.

## Phase 7 — Independent research core

- **Goal:** Implement only environment, selected agent adapters, runner, persistence, manifests and CLI.
- **Deliverables:** Minimal reproducible headless workflow.
- **Done when:** A full run completes without UI and produces valid real outputs.
- **Gate:** Architecture and contract tests pass.

## Phase 8 — Validation and pilots

- **Goal:** Verify correctness and estimate runtime, variance, failures and metric behavior.
- **Deliverables:** Unit/integration/recovery tests, pilot registry and pilot report.
- **Gate:** Pilots answer protocol-design questions; no pilot result is treated as final evidence.

## Phase 9 — Freeze final protocol

- **Goal:** Set a feasible and scientifically fair final experiment matrix.
- **Deliverables:** Frozen models, scenarios, seeds/repetitions, budgets, metrics, statistical plan and exclusions.
- **Gate:** Any later change requires explicit amendment.

## Phase 10 — Minimal experiment management

- **Goal:** Provide reliable run registry, lifecycle state and recovery required by the frozen protocol.
- **Deliverables:** Real status/events, safe interruption handling, provenance and essential batch support.
- **Gate:** Do not implement queue priorities, remote workers or advanced orchestration unless required by measured workflow.

## Phase 11 — Polished bounded dashboard

- **Goal:** Enable the user to execute and understand the thesis experiments without code or console commands.
- **Required workflows:** Dashboard, New Experiment, Runs, Compare and Artifacts.
- **Required quality:** Modern, consistent, responsive, screenshot-ready and based on real data.
- **Deliverables:** Configuration/launch, truthful monitoring, GridWorld view, history/details, comparison charts/tables and export.
- **Gate:** Every screen and feature maps to a real thesis workflow. Advanced features remain deferred.

## Phase 12 — Final runs

- **Goal:** Produce the frozen thesis evidence set.
- **Deliverables:** Complete run set, checksums, failures/exclusions registry and immutable raw outputs.
- **Gate:** Completeness and provenance audits pass; no cherry-picking.

## Phase 13 — Statistical analysis and artifacts

- **Goal:** Produce reproducible estimates, figures, tables and exports.
- **Deliverables:** Versioned scripts, intervals/effect sizes where appropriate, diagnostics and artifact manifests.
- **Gate:** Every reported value traces to source runs, configs and code.

## Phase 14 — Thesis writing and final validation

- **Goal:** Complete the Greek Microsoft Word thesis and repository package.
- **Deliverables:** Background, methods, implementation, results, discussion, limitations, conclusions, Word formatting and reproduction guide.
- **Gate:** Claims, citations, figures, cross-references, privacy and provenance audits pass.

## Completion rule

The project is complete when the research question is answered with reliable evidence and the polished local dashboard supports the required experiment workflow. It is not necessary to reach production-platform scope.
