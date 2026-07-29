# Implementation Roadmap

Το roadmap είναι phase-gated. Δεν δεσμεύει πρόωρα το project σε συγκεκριμένη βιβλιοθήκη ή UI stack.

## Phase 1 — Context transfer and validation
- **Goal:** Repository source of truth, source hierarchy, requirements, blockers.
- **Inputs:** Official application, chat exports, explicit user decisions.
- **Deliverables:** Context/research/experiment/architecture/thesis docs, source audit.
- **Done when:** Required files exist, contradictions are resolved or open, no raw chats committed.
- **Gate:** User reviews critical factual errors/blockers.

## Phase 1.5 - Automated system inventory
- **Goal:** Codex records actual CPU/RAM/GPU/OS/drivers/runtimes/storage and capability baselines.
- **Inputs:** Local system access.
- **Deliverables:** Versioned inventory and benchmark notes.
- **Done when:** Compute-dependent decisions no longer rely on historical hardware claims.
- **Gate:** No acceleration or final batch-budget decision before completion.

## Phase 2 — Add and inventory primary material
- **Goal:** Collect real bibliography and remaining source material.
- **Inputs:** PDFs, references and supervisor material.
- **Deliverables:** Source manifests, checksums, bibliography inventory.
- **Done when:** Every source has provenance and status.
- **Gate:** No final research decision without relevant primary material.

## Phase 3 — Fresh GridWorld landscape review and prototype decision
- **Goal:** Compare current reuse, adapt/wrap and minimal custom implementation strategies without assuming any legacy repository.
- **Inputs:** Official topic, current technical sources, literature needs and measured execution environment.
- **Deliverables:** Candidate matrix, license/maintenance/API audit, small compatibility prototypes and ADR recommendation.
- **Done when:** The selected strategy is justified by current evidence, pinned where third-party code is used, and suitable for deterministic research tests.
- **Gate:** No external GridWorld code is downloaded/integrated into the main project before the audit, prototype and decision.

## Phase 4 — Research-question clarification
- **Goal:** Convert official broad objective into precise, answerable questions.
- **Inputs:** Application, literature, GridWorld audit, constraints.
- **Deliverables:** Main/secondary RQs, scope boundaries, candidate hypotheses.
- **Done when:** Each RQ maps to variables, comparisons and evidence.
- **Gate:** Supervisor/user approval where required.

## Phase 5 — Focused literature review
- **Goal:** Establish definitions, methods, metrics and related work.
- **Inputs:** Real bibliography plus targeted current research.
- **Deliverables:** Structured notes, evidence matrix, gap analysis.
- **Done when:** Model/metric/protocol choices can be justified by sources.
- **Gate:** Citation verification complete for decision-driving claims.

## Phase 6 — Finalize GridWorld specification
- **Goal:** Define deterministic base environment and uncertainty mechanisms.
- **Inputs:** Audit, RQs, literature.
- **Deliverables:** Versioned schema, transition/reward rules, severity taxonomy, examples.
- **Done when:** Reference traces and invariant tests pass.
- **Gate:** Environment version frozen for pilot phase.

## Phase 7 — Select models and baselines
- **Goal:** Choose minimal scientifically informative comparison set.
- **Inputs:** RQs, environment properties, literature, hardware.
- **Deliverables:** Inclusion/exclusion table, common agent interface, ADR.
- **Done when:** Each model has a role and feasible implementation/evaluation plan.
- **Gate:** No redundant model without added evidence value.

## Phase 8 — Select metrics and estimands
- **Goal:** Operationalize performance, robustness, degradation and recovery.
- **Inputs:** RQs, literature, environment.
- **Deliverables:** Primary/secondary metrics, formulas, aggregation rules.
- **Done when:** Metrics have unit tests and unambiguous interpretation.
- **Gate:** Primary outcome(s) frozen before final runs.

## Phase 9 — Experimental protocol
- **Goal:** Define tuning, evaluation, seeds, repetitions, budgets and analysis.
- **Inputs:** Models, metrics, hardware benchmarks.
- **Deliverables:** Experiment matrix, statistical plan, exclusions, run schema.
- **Done when:** Protocol can be executed without hidden manual choices.
- **Gate:** Final conditions isolated from exploratory tuning.

## Phase 10 — Independent research core
- **Goal:** Implement environment, agent adapters, runner, persistence and CLI.
- **Inputs:** Frozen pilot specifications.
- **Deliverables:** Minimal core and reproducible CLI workflow.
- **Done when:** A complete run executes without UI and emits valid manifest/results.
- **Gate:** Architecture and contract tests pass.

## Phase 11 — Validation and tests
- **Goal:** Verify scientific and software correctness.
- **Inputs:** Core implementation.
- **Deliverables:** Unit, property, integration, recovery and known-answer tests.
- **Done when:** Transition/reward/metric/run-lifecycle evidence is documented.
- **Gate:** No unresolved correctness defect affecting pilots.

## Phase 12 — Pilot runs
- **Goal:** Measure variance, runtime, failure modes and metric behavior.
- **Inputs:** Validated core, small configurations.
- **Deliverables:** Pilot registry, timing/variance report, anomalies.
- **Done when:** Pilots answer protocol-design questions, not thesis RQs.
- **Gate:** Pilot findings reviewed; no pilot result presented as final.

## Phase 13 — Freeze experiment matrix
- **Goal:** Set feasible final configurations.
- **Inputs:** Pilot evidence and compute budget.
- **Deliverables:** Versioned/frozen protocol, seeds/repetitions, resource estimate.
- **Done when:** Changes require explicit protocol amendment.
- **Gate:** Analysis plan and artifact IDs reserved.

## Phase 14 — Experiment management
- **Goal:** Reliable queues, checkpoints, pause/resume/cancel/restart and provenance.
- **Inputs:** Frozen runner semantics.
- **Deliverables:** Run registry, recovery logic, lifecycle events.
- **Done when:** Interruption/recovery integration tests pass.
- **Gate:** Real state is observable without UI fabrication.

## Phase 15 — Dashboard
- **Goal:** Local control, monitoring, comparison and export.
- **Inputs:** Validated core and experiment-management API.
- **Deliverables:** Essential pages and real backend integrations.
- **Done when:** Main workflows work end-to-end with truthful status.
- **Gate:** UI cannot alter scientific results silently.

## Phase 16 — Final runs
- **Goal:** Produce frozen thesis evidence.
- **Inputs:** Frozen protocol, stable code, available compute.
- **Deliverables:** Complete run set, checksums, failure/exclusion registry.
- **Done when:** Completeness and provenance audits pass.
- **Gate:** No silent reruns or cherry-picking.

## Phase 17 — Statistical analysis
- **Goal:** Estimate effects and uncertainty according to plan.
- **Inputs:** Frozen final data.
- **Deliverables:** Analysis outputs, effect sizes, intervals, diagnostics.
- **Done when:** Scripts reproduce all reported values.
- **Gate:** Deviations labeled and justified.

## Phase 18 — Figures and tables
- **Goal:** Produce publication/thesis-ready evidence.
- **Inputs:** Analysis outputs.
- **Deliverables:** Versioned figures/tables with provenance manifests.
- **Done when:** Every item maps to runs, scripts, config and commit.
- **Gate:** Captions do not overclaim.

## Phase 19 — Complete thesis writing
- **Goal:** Integrate verified background, methods, implementation and results.
- **Inputs:** Sources, decision log, frozen artifacts.
- **Deliverables:** Greek chapter drafts and complete Word document.
- **Done when:** Claims/citations/cross-references/terminology are audited.
- **Gate:** Supervisor review and required revisions.

## Phase 20 — Final Word and repository validation
- **Goal:** Submit a consistent, reproducible package.
- **Inputs:** Final Word, code, data/artifacts, official checklist.
- **Deliverables:** Final `.docx`, release manifest, reproduction guide, archived result set.
- **Done when:** Formatting, privacy, citation, provenance, build and repository checks pass.
- **Gate:** Submission/presentation package approved.
