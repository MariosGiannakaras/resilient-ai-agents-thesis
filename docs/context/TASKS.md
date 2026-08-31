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

- **Package:** protocol-v2 methodology/scientific freeze is complete through DEC-058; the framework-neutral Study backend is complete through DEC-051/T-529; the final Python-native application architecture and rebuild are complete through DEC-059/T-528. DEC-042/047 and candidate v1.1 remain auditable predecessor design; historical NiceGUI remains prototype history only.
- **Project:** **6/8** master milestones objectively complete (#87: 1, 2, 3, 4, 5, 7). Milestone 6 awaits explicit intended-user acceptance; milestone 8 additionally awaits the final v2 evidence chain.
- **Current task:** `T-528 — Final Application / Frontend Rebuild` is COMPLETE. `T-511 — Intended-user application workflow/self-explanatory UX acceptance` is READY and is the next application gate.
- **State:** DEC-055 tuning remains immutable valid-complete; DEC-055/056 sizing packages remain immutable valid-failed. DEC-057 sizing-v0.3 and the combined five-method sizing package are valid-complete. DEC-058 accepts the frozen protocol-v2.0 scientific authority with `final_reserve_access=false`. DEC-059 selects PySide6 / Qt 6 Widgets for the final local application. Final-reserve scientific execution remains unauthorized and requires an explicit later T-610+ authority.
- **Completed Study backend:** `T-529` is COMPLETE. The framework-neutral Study lifecycle covers immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis with explicit denominators -> deterministic machine-readable evidence export, with restart-safe provenance and no frontend dependency.
- **Completed final application:** `T-528` is COMPLETE. PySide6 now provides recipe-first Thesis Study review, separate DEVELOPMENT/Exploratory workflow, durable Study creation, non-blocking local execution supervision, truthful Runs/progress, matched Frozen/Adaptive live GridWorld presentation, stored-evidence Results, registered artifact provenance, accessibility/help/locked/error/empty states and deterministic CI screenshot review artifacts. The application does not own or reimplement scientific protocol logic.
- **Validation:** the accepted implementation head before screenshot curation (`15fe9598955df1fa5fecff86fa1d9a80767045f6`) had Repository checks, Protocol-v2 pilot checks and PySide6 UI screenshot checks all green. The bounded DEVELOPMENT application smoke traverses create -> execute -> validate -> analyze -> evidence handoff without final identities. Curated screenshots live under `ui-screenshots/pyside6/`; historical NiceGUI screenshots are segregated under `ui-screenshots/historical-nicegui/`.
- **Branch / PR:** `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft, open, unmerged PR #92; no parallel main-repo implementation branch and no early merge.
- **Trackers:** #87 master 6/8; #95 protocol-v2 10/10 CLOSED; #88 closed/superseded; #89 complete/closed; #93 T-528 complete/closed; #94 DEFERRED post-thesis.
- **Historical science:** protocol-v1.0 / FINAL-* / R0 evidence immutable. Candidate v1.1 remains non-final history; old `T-522` must not execute. Historical scientific runners remain reproducible.
- **Bibliography:** immutable protocol-v2 consumer snapshot remains upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`, merged through thesis PR #96 and validated on PR #92.
- **Pre-WP7 approval:** NOT APPROVED; `T-700+` remains blocked.
- **Exact next action:** perform `T-511 — Intended-user application workflow/self-explanatory UX acceptance` using the accepted PySide6 workflow/screenshots. Do not execute T-610+, do not access the final reserve and do not start WP7 merely because T-528 is complete.

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
  - Depends on: `T-521`.
  - Completed research closure: 30-point audit fact-check, 20-check deep-chain pass, eight-part closure audit and DEC-050.
  - Frozen scientific contract includes: Phase-A independent method training; actual interaction budgets; common semantic information/reward/gamma; isolated no-learning probes; administrative truncation with bootstrap; each method/root/layout own full scientific checkpoint; exact shared Phase-B branch point; Frozen nominal/Frozen disturbed/Adaptive nominal/Adaptive disturbed branches; Adaptive updates only after boundary; same behavior-policy state at fork; DiD adaptation-benefit estimands; root-level inference/failure policy; explicit observation-corruption frequency + support/magnitude; final-reserve leakage firewall; historical v1.x truncation limitation; DEC-049 frontend boundary.
  - Bibliography closure: ThesisBibliography issue #135 completed; canonical methodology analyses/evidence/selection converged; 121 citation-ready sources; later-writing crosswalk retained in the corpus; upstream immutable SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`; thesis consumer sync PR #96 merged and current PR #92 repository checks passed after sync.

- [x] `T-525` — Implement the bounded framework-neutral multimethod training/checkpoint/deployment foundation required for v2 pilots.
  - Depends on: `T-524`.
  - Completed contract: `docs/research/PROTOCOL_V2_BACKEND_CONTRACT.md`.
  - Implemented: v2 method-discriminated config/result schemas; project-owned actual interaction accounting; common task-level gamma/reward/truncation contract; experiment-lifecycle/capability registry; independent Phase-A training; isolated interaction-indexed no-learning probes; full method-specific scientific state save/restore; process-destroy/restore/continue conformance; exact branch-point clone equality; Frozen/Adaptive behavior-policy-state semantics; exact GridWorld state/RNG branching; four post-boundary branches; root/failure provenance; evaluator-information fail-closed boundaries.
  - Core pilot implementations: Q-Learning, SARSA and Dyna-Q+ project exact-state adapters; DQN/PPO Stable-Baselines3 2.9.0 exact-state adapters using CPU-only PyTorch 2.9.0. DQN persists replay/target/optimizer/counters/schedules/RNG; PPO checkpoints only at legal completed rollout/update boundaries. Neural initialization and post-initialization behavior/update RNG streams are explicitly separated; environment/disturbance streams remain independent.
  - Phase-B conformance: Frozen learning state cannot mutate; SARSA requires quiescent fork; Frozen Dyna-Q+ bypasses the historical model-mutating learning `act()` path; DQN/PPO attach to the exact already-restored project GridWorld prefix. T-525 intentionally fails closed rather than inventing multi-episode post-boundary reset semantics; T-526/T-527 own that final lifecycle choice.
  - Validation at closure: complete dedicated protocol-v2 conformance gate (55 tests, CPU-only dependency check) and repository-wide tests/documentation/JSON/bibliography validation passed on the same reviewed PR #92 implementation head before status reconciliation.

- [x] `T-526` — Run bounded environment-discrimination + method/severity/CPU feasibility pilots on the validated Windows machine.
  - Depends on: `T-525` — satisfied.
  - Predeclared plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`.
  - Physical entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`.
  - Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`.
  - First physical pass selected `gw-l1` (7×7) as the first acceptable level. All 30 planned units completed with 61,440 training interactions and 28,524 probe interactions, with no scientific/infrastructure failures.
  - DEC-052 retained its failed DQN raw-envelope identity attempt. DEC-053 validated scientific continuation identity but its Phase B retained a SARSA lifecycle failure at 8/240. DEC-054 settled the exact budget-boundary behavior-policy state with zero environment interactions and fresh Phase-B v0.3 completed 240/240 matched sets, 960 branches, 240 prefixes and 9,600 post-boundary interactions with zero failures. All retained attempts remain immutable.

- [x] `T-526A` — DEC-054 boundary settlement and fresh Phase-B v0.3 physically validated.
  - Depends on: retained one-time T-526 Phase-A evidence.
  - Settlement evidence and Phase-B v0.3 evidence remain valid-complete and immutable; no rerun/resume is authorized.

- [x] `T-527` — Fair tuning, precision/runtime sizing, statistical freeze and machine-readable protocol-v2 firewall.
  - Depends on: `T-526`.
  - DEC-055 tuning is valid-complete at 180/180 and selected `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06`, `dyna-c03` with the common 8,192-interaction Phase-A budget.
  - DEC-055 sizing-v0.1 and DEC-056 sizing-v0.2 are immutable failed attempts.
  - DEC-057 sizing-v0.3 is valid-complete at 144/144 fresh Phase-A units and 288/288 fresh matched sets; the combined five-method matrix is valid-complete at 240/240 Phase-A units, 480/480 matched sets, 1,920 branches and 3,840 branch-horizon evaluations.
  - DEC-058 accepts the final protocol-v2.0 scientific freeze and `configs/protocols/protocol-v2.0-final.json` with `final_reserve_access=false`. Issue #95 is 10/10 and CLOSED. Final-reserve execution is unauthorized until a separate explicit T-610+ authority.

- [x] `T-529` — Reconstruct the study-first protocol-v2 backend from recipe through evidence/analysis/export, without frontend implementation.
  - Depends on: `T-525` — satisfied.
  - Controlling decision/spec: `docs/decisions/DEC-051_STUDY_FIRST_BACKEND_RECONSTRUCTION.md` and `docs/architecture/STUDY_BACKEND_REDESIGN.md`.
  - Completed immutable StudyRecipe/evidence classes, deterministic planning, framework-neutral restart-safe StudyService, real Phase-A/Phase-B executors, validation, root/layout analysis and deterministic evidence handoff/export with failure/provenance semantics.

- [x] `T-530` — Historical truthful UI-independent Python runtime service/read-only observer foundation. **Superseded for final application by DEC-051/T-529.**
- [x] `T-531` — Functional NiceGUI prototype over validated backend. **Prototype/history only; active implementation removed by DEC-049/051.**
- [x] `T-532` — Prototype screenshot/packaging feasibility work. **Prototype/history only; active implementation removed by DEC-049/051.**

- [x] `T-528` — **Final Application / Frontend Rebuild (PySide6)** (#93).
  - Depends on: `T-527`, `T-529` — satisfied.
  - Authority: `docs/decisions/DEC-059_PYSIDE6_FINAL_APPLICATION_ARCHITECTURE.md`.
  - Completed framework selection: Python-native PySide6 / Qt 6 Widgets, direct application/backend boundary, no NiceGUI/React/HTTP scientific middle layer, packaging deferred.
  - Completed global desktop shell/navigation/design system with self-explanatory help/tooltips, semantic locked/development/failure states, progressive disclosure, accessible keyboard/focus behavior and stable laptop layouts.
  - Completed recipe-first Thesis Study review with final-reserve lock, and separate Exploratory Study journey: choose study -> choose models -> optional customize -> planner-backed review -> durable DEVELOPMENT Study creation.
  - Completed Runs workspace with durable Study status, non-blocking QProcess worker supervision, safe start/resume/retry semantics and no unsafe hard-cancel behavior.
  - Completed presentation-only live event boundary and GridWorld renderer; transient events are dropping/non-blocking and cannot select actions, alter RNG/checkpoints/metrics or become scientific evidence. Matched FD/AD views pair exact interaction indices.
  - Completed Results workspace with Compare Learning / Test Resilience views driven by registered stored `analysis-package` summaries and provenance/integrity validation; no UI-side recomputation of scientific estimands or composite score.
  - Completed Artifacts provenance drill-down using registered StudyArtifact lineage only; no arbitrary filesystem browsing.
  - Completed deterministic screenshot CI and curated `ui-screenshots/pyside6/` review set; historical NiceGUI images are segregated under `ui-screenshots/historical-nicegui/`.
  - Completed proportional validation: focused desktop/backend tests, bounded DEVELOPMENT end-to-end application smoke, repository checks, Protocol-v2 checks and PySide6 screenshot checks. Accepted implementation head `15fe9598955df1fa5fecff86fa1d9a80767045f6` had all three principal PR gates green before screenshot curation.
  - Final reserve remained sealed throughout T-528; no final roots/layouts were executed and no final-reserve scientific outcome was generated, inspected or used.

- [ ] READY `T-511` — **Intended-user application workflow/self-explanatory UX acceptance.**
  - Depends on: `T-512`, `T-528` — satisfied.
  - Acceptance: user explicitly accepts final v2 thesis-study/custom configure/run/monitor/history/compare/export/error/help workflow. Automated checks never close this gate.
  - Review surface: accepted PySide6 application plus `ui-screenshots/pyside6/` and CI screenshot bundle.

## WP6 — Final scientific evidence

- [x] `T-600` — Historical frozen v1.0 final matrix.
- [x] `T-601` — Historical v1.0 evidence validation/freeze.
- [x] `T-602` — Historical v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical v1.0 evidence package.

- [ ] BLOCKED `T-610` — Execute frozen protocol-v2 final matrix through the accepted study-first execution path.
  - Depends on: `T-527`, `T-529`, `T-511`.
- [ ] BLOCKED `T-611` — Validate/freeze v2 final evidence.
  - Depends on: `T-610`.
- [ ] BLOCKED `T-612` — Predeclared v2 nominal-learning/resilience statistical analysis and sensitivity diagnostics.
  - Depends on: `T-611`.
- [ ] BLOCKED `T-613` — Final v2 figures/tables/exports and thesis/defense evidence package.
  - Depends on: `T-612`.

## Mandatory pre-WP7 user approval gate

**NOT APPROVED.** Completion of science, CI, screenshots or `T-613` does not authorize thesis writing. Only explicit user approval after accepted evidence/application unlocks WP7.

## WP7 — Thesis writing/review/defense

- [ ] BLOCKED `T-700` — Recheck current Department/University submission/formatting/defense rules and current tool assumptions.
  - Depends on: `T-613`, `T-511`, explicit pre-WP7 user approval.
- [ ] DEFERRED `T-701` — Review completed example theses and derive structure/style guide.
  - Depends on: `T-700`.
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
- [ ] DEFERRED `T-721` — Final PowerPoint + speaker material following `docs/thesis/PRESENTATION_WORKFLOW.md`.
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
  - Acceptance: package the accepted final frontend using delivery technology appropriate to the framework selected at T-528; validate local launch/close/restart, writable paths, privacy/licensing/reproducibility. Post-thesis and not a pre-WP7 gate.

## Task maintenance rule

Every material checkpoint reconciles this registry. GitHub issues are tracking views, not a competing task list. In-progress/failed work never counts as complete.
