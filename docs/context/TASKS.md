# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Preserve exact task/dependency/resume state across Codex sessions, quota interruptions, restarts and chat changes.

`CURRENT_STATUS.md` is the compact status summary. This file is the canonical task/dependency checklist.

## Mandatory session rule

Every Codex session MUST read:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Use available **session memory** together with repository/Git/GitHub/evidence, with repository evidence winning when stale. Inspect `git status`, the active branch, recent commits, PR #92 and any `IN_PROGRESS` work before modification.

Status: `[x]` complete; `READY` dependency-valid; `IN_PROGRESS` active; `BLOCKED` gate/dependency unmet; `DEFERRED` intentionally later; `SUPERSEDED` retained history that must not execute. In-progress/failed work never counts as complete.

## Resume state

- **Package:** protocol-v2.0 methodology/scientific freeze remains immutable through DEC-058; the framework-neutral Study backend is complete through DEC-051/T-529; the final Python-native application architecture/rebuild is complete through DEC-059/T-528. DEC-060/T-533 is the active explicit pre-outcome protocol-v2.1 recovery/comparison amendment. DEC-042/047 and candidate v1.1 remain auditable predecessor design; historical NiceGUI remains prototype history only.
- **Project:** **7/8** master milestones objectively complete (#87: 1, 2, 3, 4, 5, 6, 7). Milestone 8 awaits the final v2 evidence chain.
- **Current task:** `T-533` — protocol-v2.1 pre-final recovery/direct-comparison amendment is IN_PROGRESS under issue #98 / DEC-060.
- **State:** DEC-055 tuning remains immutable valid-complete; DEC-055/056 sizing packages remain immutable valid-failed. DEC-057 sizing-v0.3 and the combined five-method sizing package are valid-complete. DEC-058 remains the historical frozen protocol-v2.0 authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the current pre-execution amendment while preserving final roots/layouts, five methods, hyperparameters, conditions, budgets and 256-interaction Phase-B horizon. `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain mandatory.
- **T-533 implementation:** isolated protocol-v2.1 temporal Phase-B execution, fixed 32-interaction reward windows, schema-v2 temporal evidence/validation, recovery/non-recovery analysis, direct root-paired method contrasts, actual-root-count Student-t interval selection, deterministic evidence exports with v2.1 provenance, protocol-aware executor routers and a fail-closed self-contained recipe materializer are present on PR #92. Affected CI and remaining PySide6/docs reconciliation are still required before completion.
- **Completed Study backend:** `T-529` is COMPLETE. The framework-neutral Study lifecycle covers immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis with explicit denominators -> deterministic machine-readable evidence export, with restart-safe provenance and no frontend dependency.
- **Completed final application:** `T-528` is COMPLETE. PySide6 provides recipe-first Thesis Study review, separate DEVELOPMENT/Exploratory workflow, durable Study creation, non-blocking local execution supervision, truthful Runs/progress, matched Frozen/Adaptive live GridWorld presentation, stored-evidence Results, registered artifact provenance, accessibility/help/locked/error/empty states and deterministic CI screenshot review artifacts. T-511 review hardening additionally makes both matched branch actions/rewards/states and change context visible, adds redundant GridWorld symbols/direction cues, separates stored adaptation-benefit and Frozen/Adaptive-loss charts, and gives explicit research-use/onboarding guidance. The application does not own or reimplement scientific protocol logic.
- **Validation:** T-511 review-hardening implementation head (`8e8a863d51584923eb325ee7d11e4e4a2d0cbf83`) had Repository checks, Protocol-v2 pilot checks and PySide6 UI screenshot checks all green. T-533 has its own affected CI cycle and is not complete until those gates are green at its final implementation head.
- **Branch / PR:** PR #92 on `feat/pre-wp7-protocol-v1.1-ui-rebuild` remains OPEN, DRAFT and UNMERGED. Previous squash-merge sequencing is superseded: finish T-533 on this same branch/PR before merge or any T-610 authorization.
- **Trackers:** #87 master 7/8; #95 protocol-v2 10/10 CLOSED; #98 T-533 IN_PROGRESS; #88 closed/superseded; #89 complete/closed; #93 T-528 complete/closed; #94 DEFERRED post-thesis.
- **Historical science:** protocol-v1.0 / FINAL-* / R0 evidence immutable. Candidate v1.1 remains non-final history; old `T-522` must not execute. Historical `T-530`, `T-531` and `T-532` remain completed/superseded history and are not repurposed.
- **Bibliography:** immutable protocol-v2 consumer snapshot remains upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`, merged through thesis PR #96 and validated on PR #92.
- **Pre-WP7 approval:** NOT APPROVED; `T-700+` remains blocked.
- **Exact next action:** finish T-533 stored-evidence UI/docs/CI reconciliation, then stop at the explicit T-610 authorization gate. Do not access the final reserve or start WP7.

## Quota/interruption resilience

1. Resume valid unfinished work before starting a new package.
2. Never discard partial experiment evidence without inspection.
3. Reconcile this ledger at coherent checkpoints.
4. Preserve stable task/decision IDs; supersede explicitly.
5. Use `X/Y` only for objective finite denominators.
6. Testing is risk-based/proportional; scientific experiment matrices are not CI test matrices.
7. Do not create a parallel implementation branch for the active main-repo package.

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
- [x] `T-521` — Candidate protocol-v1.1/config identity/paired-statistics infrastructure; valid non-final history only.
- [ ] `T-522` — **SUPERSEDED. Do not execute.** Historical v1.1 tuning/freeze gate superseded by DEC-048/050 and T-524–T-527.

- [x] `T-524` — Freeze the source-backed protocol-v2 research contract.
- [x] `T-525` — Implement the bounded framework-neutral multimethod training/checkpoint/deployment foundation required for v2 pilots.
- [x] `T-526` — Run bounded environment-discrimination + method/severity/CPU feasibility pilots on the validated Windows machine.
- [x] `T-526A` — DEC-054 boundary settlement and fresh Phase-B v0.3 physically validated.
- [x] `T-527` — Fair tuning, precision/runtime sizing, statistical freeze and machine-readable protocol-v2 firewall.
- [x] `T-529` — Reconstruct the study-first protocol-v2 backend from recipe through evidence/analysis/export, without frontend implementation.
- [x] `T-530` — Historical truthful UI-independent Python runtime service/read-only observer foundation. **Superseded for final application by DEC-051/T-529.**
- [x] `T-531` — Functional NiceGUI prototype over validated backend. **Prototype/history only; active implementation removed by DEC-049/051.**
- [x] `T-532` — Prototype screenshot/packaging feasibility work. **Prototype/history only; active implementation removed by DEC-049/051.**
- [ ] IN_PROGRESS `T-533` — **Protocol-v2.1 pre-final recovery and direct-comparison amendment** (#98 / DEC-060).
  - Depends on: `T-527`, `T-529`, `T-511` — satisfied.
  - Preserve DEC-058/protocol-v2.0 and all completed T-526/T-527 evidence as immutable history; protocol-v2.1 is an explicit pre-outcome amendment only.
  - Keep the final reserve sealed: `final_reserve_access=false`; this task cannot authorize T-610.
  - Freeze final RQ1 nominal learning, RQ2 resilience/adaptation benefit and RQ3 recovery speed.
  - Preserve the five retained methods, common actual-interaction fairness budget, Phase-A probes/checkpoints, final roots/layouts, hyperparameters, four conditions and 256-interaction Phase-B horizon.
  - Add passive fixed 32-interaction reward windows without changing method-native learning boundaries; episode resets do not realign the windows.
  - Store/validate schema-v2 temporal branch evidence and retain exact Phase-A -> Phase-B lineage.
  - RQ3 primary axis: persistent action-remap; AN-vs-AD matched root-level trajectory; tolerance 0.10 with 0.05/0.20 sensitivity; two-window stability; right-censor non-recovery at 256 with `recovery_time=null`.
  - Add root-paired direct method contrasts after equal layout reduction. Use pointwise Student-t intervals selected by the actual independent-root `n`; no p-value superiority family or post-hoc significance language.
  - Export deterministic recovery/contrast tables and provenance; computational time/update counters remain secondary descriptive evidence.
  - Materialize `configs/protocols/protocol-v2.1-final.json` into one frozen confirmatory Study recipe only if the explicit T-610 gate and final-reserve lock remain intact.
  - PySide6 may present only validated stored recovery/contrast evidence; no UI-side thresholds or estimand recomputation.
  - Complete only after affected tests/CI, active research-doc reconciliation and objective review are green/consistent. Then stop at T-610 authorization.

- [x] `T-528` — **Final Application / Frontend Rebuild (PySide6)** (#93).
  - Depends on: `T-527`, `T-529` — satisfied.
  - Authority: `docs/decisions/DEC-059_PYSIDE6_FINAL_APPLICATION_ARCHITECTURE.md`.
  - Completed framework selection: Python-native PySide6 / Qt 6 Widgets, direct application/backend boundary, no NiceGUI/React/HTTP scientific middle layer, packaging deferred.
  - Completed global desktop shell/navigation/design system with self-explanatory help/tooltips, semantic locked/development/failure states, progressive disclosure, accessible keyboard/focus behavior and stable laptop layouts.
  - Completed recipe-first Thesis Study review with final-reserve lock, and separate Exploratory Study journey: choose study -> choose models -> optional customize -> planner-backed review -> durable DEVELOPMENT Study creation.
  - Completed Runs workspace with durable Study status, non-blocking QProcess worker supervision, safe start/resume/retry semantics and no unsafe hard-cancel behavior.
  - Completed presentation-only live event boundary and GridWorld renderer; transient events are dropping/non-blocking and cannot select actions, alter RNG/checkpoints/metrics or become scientific evidence. Matched FD/AD views pair exact interaction indices and visibly retain both branch actions, rewards, true states, observations and change context, with redundant start/goal/agent/action encodings.
  - Completed Results workspace with Compare Learning / Test Resilience views driven by registered stored `analysis-package` summaries and provenance/integrity validation; stored adaptation-benefit and Frozen/Adaptive-loss charts remain distinct, and there is no UI-side recomputation of scientific estimands or composite score.
  - Completed Artifacts provenance drill-down using registered StudyArtifact lineage only; no arbitrary filesystem browsing.
  - Completed deterministic screenshot CI and the final curated ten-image `ui-screenshots/pyside6/` review set; superseded NiceGUI PNGs remain available through Git history only.
  - Completed proportional validation: focused desktop/backend tests, bounded DEVELOPMENT end-to-end application smoke, repository checks, Protocol-v2 checks and PySide6 screenshot checks. T-511 review-hardening head `8e8a863d51584923eb325ee7d11e4e4a2d0cbf83` had all three principal PR gates green; exact-head artifact `9788923062` was visually inspected at all required viewport classes.
  - Final reserve remained sealed throughout T-528; no final roots/layouts were executed and no final-reserve scientific outcome was generated, inspected or used.

- [x] `T-511` — **Intended-user application workflow/self-explanatory UX acceptance.**
  - Depends on: `T-512`, `T-528` — satisfied.
  - Accepted: 2026-09-01, after the user explicitly delegated final intended-user acceptance based on the completed UI/research-workflow audit and verified screenshot/live-presentation requirements.
  - Scope: final v2 thesis-study/custom configure/run/monitor/history/compare/export/error/help workflow. This accepts the application workflow only; it does not authorize final-reserve execution or accept future scientific results.
  - Capture boundary: the application is screenshot-ready and exposes truthful live GridWorld for external GIF/video capture; it does not claim an integrated GIF exporter. Real thesis/defense captures require later `ASSET-*` provenance records and static fallbacks.
  - Review surface: accepted PySide6 application plus the final `ui-screenshots/pyside6/` set and exact-head CI screenshot bundle.

## WP6 — Final scientific evidence

- [x] `T-600` — Historical frozen v1.0 final matrix.
- [x] `T-601` — Historical v1.0 evidence validation/freeze.
- [x] `T-602` — Historical v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical v1.0 evidence package.

- [ ] BLOCKED `T-610` — Execute frozen protocol-v2.1 final matrix through the accepted study-first execution path.
  - Depends on: `T-527`, `T-529`, `T-511`, `T-533`.
  - State: T-533 is not complete and `final_reserve_access=false` remains sealed. After T-533 completes, a separate explicit scientific execution authorization is still mandatory.
- [ ] BLOCKED `T-611` — Validate/freeze v2.1 final evidence.
  - Depends on: `T-610`.
- [ ] BLOCKED `T-612` — Predeclared v2.1 nominal-learning/resilience/recovery statistical analysis and sensitivity diagnostics.
  - Depends on: `T-611`.
- [ ] BLOCKED `T-613` — Final v2.1 figures/tables/exports and thesis/defense evidence package.
  - Depends on: `T-612`.

## Mandatory pre-WP7 user approval gate

**NOT APPROVED.** Completion of science, CI, screenshots or `T-613` does not authorize thesis writing. Only explicit user approval after accepted evidence/application unlocks WP7.

## WP7 — Thesis writing/review/defense

- [ ] BLOCKED `T-700` — Recheck current Department/University submission/formatting/defense rules and current tool assumptions.
  - Depends on: `T-613`, `T-511`, explicit pre-WP7 user approval.
- [ ] DEFERRED `T-701` — Review completed example theses and derive structure/style guide.
- [ ] DEFERRED `T-710` — Draft complete Greek thesis from accepted evidence.
- [ ] DEFERRED `T-711` — Produce review-ready Word thesis + manual ASSET placement register.
- [ ] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate.
- [ ] DEFERRED `T-713` — Freeze final thesis deliverable.
- [ ] DEFERRED `T-720` — Defense narrative/slide outline/evidence map.
- [ ] DEFERRED `T-721` — Final PowerPoint + speaker material following `docs/thesis/PRESENTATION_WORKFLOW.md`.
- [ ] DEFERRED `T-722` — Validate/rehearse defense package/demo fallback.

## WP8 — Final audits/delivery

- [ ] DEFERRED `T-800` — Final bibliography/citation/official-guidance audit.
- [ ] DEFERRED `T-801` — Final reproducibility/privacy/licensing/docs/thesis/defense/application-asset audit.
- [ ] DEFERRED `T-802` — Final academic delivery readiness.
- [ ] DEFERRED `T-803` — Final cleaned Windows standalone application package (#94).
  - Depends on: `T-713`, `T-511`.
  - Acceptance: package the accepted final frontend using delivery technology appropriate to the framework selected at T-528; validate local launch/close/restart, writable paths, privacy/licensing/reproducibility. Post-thesis and not a pre-WP7 gate.

## Task maintenance rule

Every material checkpoint reconciles this registry. GitHub issues are tracking views, not a competing task list. In-progress/failed work never counts as complete.
