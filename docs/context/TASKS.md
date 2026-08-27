# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Preserve exact task/dependency/resume state across Codex sessions, quota interruptions, restarts and chat changes.

`CURRENT_STATUS.md` is the compact status summary. This file is the canonical task/dependency checklist.

## Mandatory session rule

Every Codex session MUST read the three-file session-start core:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Use session memory together with repository/Git/GitHub/evidence. Repository evidence wins when memory or prose is stale. Inspect `git status`, branch, recent commits, PR #92 and any `IN_PROGRESS` work before modifying anything.

Status: `[x]` complete; `READY` dependency-valid; `IN_PROGRESS` active; `BLOCKED` gate/dependency unmet; `DEFERRED` intentionally later; `SUPERSEDED` retained history that must not execute. In-progress/failed work never counts as complete.

## Resume state

- **Package:** DEC-048 protocol-v2 scientific redesign; DEC-042/047 and candidate v1.1 remain auditable predecessor design. Application DEC-044/045/046 and NiceGUI remain prototype/implementation history, not the accepted final UI architecture.
- **Project:** **4/8** master milestones complete (#87: 1, 2, 4, 5).
- **Current task:** `T-524`.
- **State:** `IN_PROGRESS`; 30-point methodology fact-check and chained research are complete, canonical bibliography promotion/selection/sync and source-backed reconciliation remain active.
- **Branch / PR:** `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; no parallel main-repo implementation branch.
- **Trackers:** #87 master **4/8**; #95 protocol-v2 **2/10**; #88 v1.1 closed/superseded at historical **9/12**; #89 runtime 6/6 complete/closed; #93 final UI redesign 0/8 PAUSED; #94 final Windows packaging DEFERRED post-thesis.
- **Historical science:** protocol-v1.0 / FINAL-* / R0 evidence immutable. Candidate v1.1 remains non-final history; its T-522 tuning/freeze path is not executed.
- **Frontend direction:** after the v2 backend/scientific redesign, the final frontend is rebuilt from scratch using a **different framework** selected at `T-528`; NiceGUI-specific choices are not final constraints.
- **Pre-WP7 approval:** NOT APPROVED; `T-700+` execution remains blocked.
- **Exact next action:** complete `T-524`: finish ThesisBibliography #135 analysis/evidence/thesis-selection and versioned sync, reconcile active source-of-truth docs, then close the source-backed RQs/estimand roles/method-role gates and hand off bounded pilot infrastructure to `T-525`. Do not access any v1.1/v2 final reserve and do not start UI implementation #93 yet.

## Quota/interruption resilience

1. Resume valid unfinished local/remote work before starting something new.
2. Never discard uncommitted/pushed/partial experiment evidence without inspection.
3. Reconcile this ledger at coherent checkpoints, not after every child run.
4. Preserve stable task/decision IDs; supersede explicitly rather than rewriting history.
5. Use `Project: X/Y` only from finite canonical denominators.
6. Testing is risk-based/proportional; scientific experiment matrices are not CI test matrices.
7. Never create another implementation branch for the active package unless a later explicit decision supersedes this rule.

## WP0 — Repository/research infrastructure

- [x] `T-001` — Repository/project identity and controlled Git/PR workflow.
- [x] `T-002` — Immutable `ThesisBibliography` integration/provenance.
- [x] `T-003` — Python 3.12 + `uv` locked environment/importable core.
- [x] `T-004` — Information/RNG/scenario/experiment/stage contracts.
- [x] `T-005` — Run bundles/provenance/checksums/metrics/publication safeguards.
- [x] `T-006` — Documentation reconciliation/canonical execution prompt.
- [x] `T-007` — End-to-end lifecycle/user/Codex/defense handoffs.
- [x] `T-008` — Lean three-file session-start core and resumable execution.
- [x] `T-009` — Project-scoped developer-documentation configuration.

## WP1 — Target-machine baseline

- [x] `T-100` — Actual-machine hardware/software/storage inventory.
- [x] `T-101` — Compute-dependent dependency/runtime constraints.
- [x] `T-102` — Durable capability-provenance reconciliation.

## WP2 — Controlled testbed

- [x] `T-200` — Source-traceable historical RQ/hypothesis framing.
- [x] `T-210` — GridWorld implementation comparison.
- [x] `T-211` — GridWorld ADR.
- [x] `T-212` — Project-owned Gymnasium GridWorld.
- [x] `T-213` — Known-answer/determinism/disturbance/information tests.

GridWorld is the controlled experimental/visualization testbed, not the thesis subject.

## WP3/WP4 — Historical methods/protocol

- [x] `T-300` — Resilience/degradation/recovery estimands.
- [x] `T-301` — Known-answer metric validation.
- [x] `T-310` — Historical bounded agent-role comparison.
- [x] `T-311` — Robust-MDP citation decision.
- [x] `T-312` — Historical F0/C0/R0-capable implementation.
- [x] `T-400` — Historical partitions/pilot protocol.
- [x] `T-401` — Headless runner/orchestration.
- [x] `T-402` — Reproducible analysis pipeline.
- [x] `T-410` — Pilot diagnostics/R0 amendment evidence.
- [x] `T-411` — Pre-freeze bibliography freshness review.
- [x] `T-412` — Immutable protocol-v1.0 freeze/statistical plan.

## WP5 — Scientific successor + application foundation

- [x] `T-500` — Historical experiment-manager baseline.
- [x] `T-510` — Historical Streamlit dashboard baseline.
- [x] `T-512` — Historical self-explanatory UX/onboarding pass.
- [x] `T-513` — Refinement governance/single branch/PR/handoff.
- [x] `T-520` — Information-limited deterministic Dyna-Q+ integration.
- [x] `T-523` — SARSA + Dyna-Q + broader mechanism implementation foundation.
- [x] `T-521` — Candidate protocol-v1.1/config identity/paired-statistics infrastructure. It remains valid non-final history but is not the future final protocol.
- [ ] `T-522` — **SUPERSEDED. Do not execute.** Historical v1.1 tuning/freeze gate, superseded by DEC-048 / `T-524`–`T-527` before any v1.1 final access.

- [ ] IN_PROGRESS `T-524` — Freeze the source-backed protocol-v2 research contract.
  - Depends on: `T-521`.
  - Acceptance: finish ThesisBibliography #135 source refresh/re-evaluation, scientific analysis/evidence, thesis-selection and versioned consumer sync; retain `docs/research/PROTOCOL_V2_AUDIT_FACT_CHECK.md` as the traceable 30-point audit→fact-check→repo-delta record; freeze RQ-A nominal learning vs RQ-B resilience/adaptation; distinguish the broader feasibility candidate pool from the minimum scientifically sufficient confirmatory core; define Phase-A and Phase-B primary/secondary estimand roles; retain and separately interpret the current uncertainty taxonomy unless evidence justifies amendment; freeze fair interaction/tuning/statistical principles, semantic-information fairness, experiment-lifecycle adapter boundary and environment-discrimination selection rule; document exact method-specific scientific checkpoint semantics; document what v1.0/v1.1 evidence remains historical/reusable and prohibit numerical pooling into v2 confirmatory estimates; reconcile DEC-041 historical counts and the new frontend-framework boundary. DEC-048, `docs/research/PROTOCOL_V2_RESEARCH_DESIGN.md` and the audit fact-check remain the durable research contract; exact machine-dependent values stay intentionally unfrozen.

- [ ] BLOCKED `T-525` — Implement the bounded framework-neutral multimethod training/checkpoint/deployment foundation required for v2 pilots.
  - Depends on: `T-524`.
  - Acceptance: new v2 method-discriminated experiment/config/result schemas; experiment-lifecycle/capability adapter boundary supporting independent training, standardized no-learning evaluation, method-specific scientific checkpoint/restore, exact Frozen/Continual cloning, algorithm-specific configuration, separate training/evaluation RNG and no evaluator leakage; reuse current GridWorld/RNG/run-bundle/runtime primitives without extending the legacy f0/c0/r0 request into an incoherent universal schema; integrate the minimum Q-Learning/SARSA/DQN/PPO/Dyna-Q+ pilot adapters needed to exercise the frozen contracts, reusing maintained deep-RL libraries where appropriate. Simple tabular methods may keep step-wise `act/observe` internally while deep adapters retain native replay/rollout/update semantics. Dyna-Q is a targeted ablation only when required to separate planning from recency. A2C may receive only the minimum feasibility adapter needed for its promotion decision, not an automatic full final arm. Do not optimize final hyperparameters, execute the final matrix or build the new UI here.

- [ ] BLOCKED `T-526` — Run bounded environment-discrimination + method-feasibility pilots on the validated thesis Windows machine.
  - Depends on: `T-525`.
  - Acceptance: use only a small **predeclared ordered** set of project-owned GridWorld complexity levels and a frozen discrimination rule; retain the simplest level that is not universally trivial or universally unsolved, preserves the semantic information/uncertainty contract and is CPU-feasible; measure CPU/wall runtime, nominal learning signal/variance, checkpoint fidelity, Frozen/Continual clone fidelity and artifact size for the core candidates; explicitly evaluate whether A2C adds a distinct thesis-relevant contrast beyond PPO at acceptable matrix cost before promotion/exclusion; retain failures/poor outcomes; use no final reserve. A method-specific poor outcome does not by itself justify selecting a different environment level.
  - External boundary: GitHub-hosted CI does not substitute for required machine/runtime pilot evidence.

- [ ] BLOCKED `T-527` — Fair tuning, precision/runtime sizing, statistics freeze and machine-readable protocol-v2 candidate/final firewall.
  - Depends on: `T-526`.
  - Acceptance: bounded algorithm-specific literature-backed tuning with equivalent predeclared configuration/search opportunity, common tuning-only roots/partitions and fixed selection/tie criteria; common Phase-A environment-interaction budget plus periodic standardized no-learning evaluation; final method/environment/condition/root counts selected from predeclared pilot evidence; exact checkpoint/Frozen/Continual/update semantics; root/run remains the independent randomization unit with layout/factor blocking and paired analysis where valid; effect sizes and 95% intervals; limited primary contrasts and predeclared multiplicity policy if p-values are used; Phase-B primaries are immediate degradation, cumulative same-regime-reference deficit and terminal performance/gap; recovery secondary/sensitivity; no composite resilience score; freeze before final access.

- [x] `T-530` — Truthful UI-independent Python runtime service/read-only observer foundation.
- [x] `T-531` — Functional NiceGUI prototype over the validated backend. **Prototype/history only; not final frontend architecture.**
- [x] `T-532` — Prototype screenshot/packaging feasibility work. **Not final delivery packaging or final UI acceptance.**

- [ ] BLOCKED `T-528` — Select a different frontend framework and rebuild the final v2-aware application UI/UX from scratch (#93).
  - Depends on: `T-527`.
  - Acceptance: choose a **different framework from NiceGUI** only after the framework-neutral v2 backend contract is stable; document the selection against local desktop use, truthful live dual-GridWorld rendering, scientific charts/tables, accessibility, maintainability, integration with the Python scientific service and later standalone-delivery constraints; rebuild rather than incrementally restyle the NiceGUI prototype; consume backend DTOs/events without duplicating scientific execution; issue #93 8/8; final UI represents v2 nominal-learning and method-specific Frozen/Continual workflows truthfully; fresh screenshots replace/segregate obsolete prototype captures. Existing NiceGUI/Plotly/ECharts/Mermaid/AG Grid choices are prototype evidence, not immutable final-stack requirements.

- [ ] BLOCKED `T-511` — Intended-user application workflow/self-explanatory UX acceptance.
  - Depends on: `T-512`, `T-528`.
  - Acceptance: user explicitly accepts the final v2-aware workflow, terminology, configuration, monitoring, comparison, errors/help and evidence surfaces. Automated checks never close this gate.

## WP6 — Final scientific evidence

- [x] `T-600` — Historical frozen v1.0 final matrix.
- [x] `T-601` — Historical v1.0 evidence validation/freeze.
- [x] `T-602` — Historical v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical v1.0 evidence package.

- [ ] BLOCKED `T-610` — Execute the frozen protocol-v2 final matrix.
  - Depends on: `T-527`, `T-511`.
- [ ] BLOCKED `T-611` — Validate/freeze v2 final evidence.
  - Depends on: `T-610`.
- [ ] BLOCKED `T-612` — Predeclared v2 learning/resilience statistical analysis and sensitivity diagnostics.
  - Depends on: `T-611`.
- [ ] BLOCKED `T-613` — Final v2 figures/tables/exports and thesis/defense evidence package.
  - Depends on: `T-612`.

## Mandatory pre-WP7 user approval gate

**NOT APPROVED.** Completion of science, CI, screenshots or `T-613` does not authorize thesis writing. Only explicit user approval after accepted evidence/application can unlock WP7.

## WP7 — Thesis writing/review/defense

- [ ] BLOCKED `T-700` — Recheck current Department/University submission/formatting/defense rules and current tool assumptions.
  - Depends on: `T-613`, `T-511` and explicit pre-WP7 user approval.
- [ ] DEFERRED `T-701` — Comparative review of completed example theses and derivation of `THESIS_STRUCTURE_AND_STYLE_GUIDE.md`.
  - Depends on: `T-700`.
  - Inputs: `local-inputs/example-theses/` plus independently discovered examples only from `ice.uniwa.gr` unless user changes that restriction. Examples are structural/contextual only, never scientific sources; current official guidance wins.
- [ ] DEFERRED `T-710` — Draft complete Greek thesis from accepted evidence.
  - Depends on: `T-700`, `T-701`.
- [ ] DEFERRED `T-711` — Produce review-ready Word thesis + manual ASSET placement register.
  - Depends on: `T-710`.
- [ ] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate.
  - Depends on: `T-711`.
- [ ] DEFERRED `T-713` — Freeze final thesis deliverable.
  - Depends on: `T-712`.
- [ ] DEFERRED `T-720` — Defense narrative/slide outline/evidence map.
  - Depends on: `T-713`.
- [ ] DEFERRED `T-721` — Final PowerPoint + speaker material per `docs/thesis/PRESENTATION_WORKFLOW.md`.
  - Depends on: `T-720`.
- [ ] DEFERRED `T-722` — Validate/rehearse defense package/demo fallback.
  - Depends on: `T-721`.

## WP8 — Final audits/delivery

- [ ] DEFERRED `T-800` — Final bibliography/citation/official-guidance audit.
  - Depends on: `T-713`, `T-722`.
- [ ] DEFERRED `T-801` — Final reproducibility/privacy/licensing/docs/thesis/defense/application-asset audit.
  - Depends on: `T-800`.
- [ ] DEFERRED `T-802` — Final academic delivery readiness.
  - Depends on: `T-801`.
- [ ] DEFERRED `T-803` — Final cleaned Windows standalone application package (#94).
  - Depends on: `T-713`, `T-511`.
  - Acceptance: package the finally accepted UI after thesis freeze using the delivery technology appropriate to the frontend selected at `T-528`; native/local launch-close-restart, safe writable paths and privacy/licensing/reproducibility packaging audit. This is intentionally post-thesis and is not a pre-WP7 gate.

## Task maintenance rule

Every material checkpoint reconciles this registry. GitHub issues are tracking views, not a competing task list. In-progress/failed work never counts as complete.
