# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Preserve exact task/dependency/resume state across Codex sessions, quota interruptions, restarts and chat changes.

`CURRENT_STATUS.md` is the compact status summary. This file is the canonical task/dependency checklist.

## Mandatory session rule

Every Codex session MUST read:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Use available **session memory** together with repository/Git/GitHub/evidence, with repository evidence winning when stale. Inspect `git status`, the active branch, recent commits, current open PR/CI state and any `IN_PROGRESS` work before modification.

Status: `[x]` complete; `READY` dependency-valid; `IN_PROGRESS` active; `BLOCKED` gate/dependency unmet; `DEFERRED` intentionally later; `SUPERSEDED` retained history that must not execute. In-progress/failed work never counts as complete.

## Resume state

- **Package:** protocol-v2.0 methodology/scientific freeze remains immutable through DEC-058; the framework-neutral Study backend is complete through DEC-051/T-529; historical PySide6 application work remains complete through DEC-059/T-528; DEC-060/T-533, pre-final readiness hardening, DEC-061/T-534, intended-user hardening T-535, final visual polish/richer result visualization T-536, and final pre-T610 active-tree hygiene T-537 are complete. DEC-042/047 and candidate v1.1 remain auditable predecessor design; historical NiceGUI remains prototype history only.
- **Project:** **7/8** master milestones objectively complete (#87: 1, 2, 3, 4, 5, 6, 7). Milestone 8 awaits the final v2.1 evidence chain.
- **Current task:** `T-610` is **IN_PROGRESS**. The user supplied the required separate explicit final-scientific-experiment authorization on 2026-09-02. This authorizes only execution of the unchanged frozen protocol-v2.1 final Study through the accepted backend token/path and does not authorize T-611/T-612/T-613 or WP7.
- **Separate scientific gate:** SATISFIED for T-610 only. The committed protocol continues to retain `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate`; authorization is supplied separately through the backend `PROTOCOL_V21_FINAL_EXECUTION_AUTHORIZATION` token without changing those immutable fields or weakening the guard.
- **State:** DEC-055 tuning remains immutable valid-complete; DEC-055/056 sizing packages remain immutable valid-failed. DEC-057 sizing-v0.3 and the combined five-method sizing package are valid-complete. DEC-058 remains the historical frozen protocol-v2.0 authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the current pre-execution amendment while preserving final roots/layouts, five methods, hyperparameters, conditions, budgets and 256-interaction Phase-B horizon. `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain mandatory.
- **T-533 implementation:** COMPLETE. The isolated protocol-v2.1 path includes passive fixed 32-interaction Phase-B reward windows, schema-v2 temporal evidence/validation, right-censored recovery/non-recovery analysis, direct root-paired method contrasts, actual-root-count Student-t interval selection, deterministic evidence exports with v2.1 provenance, protocol-aware executor routers, fail-closed self-contained recipe materialization, and PySide6 stored-evidence recovery/contrast presentation with no UI-side estimand computation.
- **Completed Study backend:** `T-529` is COMPLETE. The framework-neutral Study lifecycle covers immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis with explicit denominators -> deterministic machine-readable evidence export, with restart-safe provenance and no frontend dependency.
- **Historical completed application baseline:** `T-528` remains COMPLETE and is not repurposed. It records the accepted PySide6 architecture/workflow/read-model/application baseline and prior intended-user acceptance history. Its presentation implementation is not the authority for the completed T-534/T-535/T-536 application; reusable UI-neutral contracts were preserved where still correct.
- **Pre-final readiness:** COMPLETE scientifically, for the accepted application, and for active-tree hygiene. Read-only preflight, backend deny-by-default final execution guard, synthetic DEVELOPMENT scientific-pipeline smoke, `docs/research/RQ_EVIDENCE_TRACEABILITY.md`, T-534, T-535, T-536 and T-537 are complete; the final reserve remains sealed.
- **Final read-only merged-main preflight:** COMPLETE after T-536 merge. It confirmed the exact validated tree, no committed `protocol-v2.1-final` Study bundle, default final execution blocked, and the canonical 603-job plan with `final_execution_authorized=false`. T-537 changed no scientific/execution code, so these gate semantics remain unchanged.
- **Repository integration:** PR #92 is historical and was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`. Subsequent protocol-v2.1 readiness and pre-UI context cleanup were also merged. PR #107 was squash-merged as `c372c581b88c63f3b07c96bd50bbc17b9b83f835`; PR #110 as `225df138c5c5be0c39c9e474ef7fdbce6b11245b`; PR #113 as `d16f16cef06406d8af974ef3bab5be9608d65666`; post-T536 reconciliation as `4ffb7bc700b3d485324c659e94823c9d2e272cba`; README refresh PR #115 as `31877a09ec2eda7852856c6c1cf7ae059bbf72ae`; PR #117 / T-537 as `8fd32fbf68d7374ff1de5c70db21e9f95b129c1c`.
- **Trackers:** #87 master 7/8; #95 protocol-v2 10/10 CLOSED; #98 T-533 CLOSED/COMPLETE; #88 closed/superseded; #89 complete/closed; #93 T-528 complete/closed; #94 DEFERRED post-thesis; #104 T-534 COMPLETE/CLOSED; #109 T-535 COMPLETE/CLOSED; #112 T-536 COMPLETE/CLOSED; #116 T-537 COMPLETE/CLOSED after post-merge reconciliation.
- **Historical science:** protocol-v1.0 / FINAL-* / R0 evidence immutable. Candidate v1.1 remains non-final history; old `T-522` must not execute. Historical `T-530`, `T-531` and `T-532` remain completed/superseded history and are not repurposed.
- **Bibliography:** immutable protocol-v2 consumer snapshot remains upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`, merged through thesis PR #96 and validated in the integrated repository.
- **Pre-WP7 approval:** NOT APPROVED; `T-700+` remains blocked.
- **Exact next action:** after merging this authorization/status checkpoint to current `main`, rerun the native Windows read-only preflight, create or resume the single `protocol-v2.1-final` Study, and execute its exact outstanding jobs through the authorized `StudyService` path. Do not begin T-611/T-612/T-613 or WP7 and do not interpret final outcomes during T-610.

## Quota/interruption resilience

1. Resume valid unfinished work before starting a new package.
2. Never discard partial experiment evidence without inspection.
3. Reconcile this ledger at coherent checkpoints.
4. Preserve stable task/decision IDs; supersede explicitly.
5. Use `X/Y` only from a real finite denominator in `TASKS.md`; in-progress/failed work never counts as complete.
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
- [x] `T-533` — **Protocol-v2.1 pre-final recovery and direct-comparison amendment** (#98 / DEC-060).
  - Depends on: `T-527`, `T-529`, `T-511` — satisfied.
  - Preserves DEC-058/protocol-v2.0 and all completed T-526/T-527 evidence as immutable history; protocol-v2.1 is an explicit pre-outcome amendment only.
  - Keeps the final reserve sealed: `final_reserve_access=false`; this task does not authorize T-610.
  - Freezes final RQ1 nominal learning, RQ2 resilience/adaptation benefit and RQ3 recovery speed.
  - Preserves the five retained methods, common actual-interaction fairness budget, Phase-A probes/checkpoints, final roots/layouts, hyperparameters, four conditions and 256-interaction Phase-B horizon.
  - Adds passive fixed 32-interaction Phase-B reward windows without changing method-native learning boundaries; episode resets do not realign the windows.
  - Stores/validates schema-v2 temporal branch evidence and retains exact Phase-A -> Phase-B lineage.
  - RQ3 primary axis: persistent action-remap; AN-vs-AD matched root-level trajectory; tolerance 0.10 with 0.05/0.20 sensitivity; two-window stability; right-censor non-recovery at 256 with `recovery_time=null`.
  - Adds root-paired direct method contrasts after equal layout reduction. Uses pointwise Student-t intervals selected by the actual independent-root `n`; no p-value superiority family or post-hoc significance language.
  - Exports deterministic recovery/contrast tables and provenance; computational time/update counters remain secondary descriptive evidence.
  - Materializes `configs/protocols/protocol-v2.1-final.json` into one frozen confirmatory Study recipe only while the explicit T-610 gate and final-reserve lock remain intact.
  - PySide6 presents only validated stored recovery/contrast evidence; no UI-side thresholds or estimand recomputation.
  - Completion validation: final closure head `72c293d0678111880ec6d260fe9c05a1970475ed` passed Repository checks #795, Protocol-v2 pilot checks #310 and PySide6 screenshot checks #136; active research/methodology/thesis-structure docs and DEC-060/decision index were reconciled before closure.

- [x] `T-528` — **Historical PySide6 Final Application / Frontend Rebuild baseline** (#93).
  - Depends on: `T-527`, `T-529` — satisfied.
  - Authority: `docs/decisions/DEC-059_PYSIDE6_FINAL_APPLICATION_ARCHITECTURE.md`.
  - Completed framework selection: Python-native PySide6 / Qt 6 Widgets, direct application/backend boundary, no NiceGUI/React/HTTP scientific middle layer, packaging deferred.
  - Completed global desktop shell/navigation/design system with self-explanatory help/tooltips, semantic locked/development/failure states, progressive disclosure, accessible keyboard/focus behavior and stable laptop layouts.
  - Completed recipe-first Thesis Study review with final-reserve lock, and separate Exploratory Study journey: choose study -> choose models -> optional customize -> planner-backed review -> durable DEVELOPMENT Study creation.
  - Completed Runs workspace with durable Study status, non-blocking QProcess worker supervision, safe start/resume/retry semantics and no unsafe hard-cancel behavior.
  - Completed presentation-only live event boundary and GridWorld renderer; transient events are dropping/non-blocking and cannot select actions, alter RNG/checkpoints/metrics or become scientific evidence. Matched FD/AD views pair exact interaction indices and visibly retain both branch actions, rewards, true states, observations and change context, with redundant start/goal/agent/action encodings.
  - Completed Results workspace with Compare Learning / Test Resilience views driven by registered stored `analysis-package` summaries and provenance/integrity validation; stored adaptation-benefit and Frozen/Adaptive-loss charts remain distinct, and there is no UI-side recomputation of scientific estimands or composite score.
  - Completed Artifacts provenance drill-down using registered StudyArtifact lineage only; no arbitrary filesystem browsing.
  - Completed deterministic screenshot CI and a curated ten-image review set. T-537 removed that superseded T-528 set from the active tree; the accepted images remain auditable through Git history and the exact-head GitHub Actions artifact. Superseded NiceGUI images likewise remain available through Git history.
  - Completed proportional validation: focused desktop/backend tests, bounded DEVELOPMENT end-to-end application smoke, repository checks, Protocol-v2 checks and PySide6 screenshot checks. T-511 review-hardening head `8e8a863d51584923eb325ee7d11e4e4a2d0cbf83` had all three principal PR gates green; exact-head artifact `9788923062` was visually inspected at all required viewport classes.
  - Final reserve remained sealed throughout T-528; no final roots/layouts were executed and no final-reserve scientific outcome was generated, inspected or used.
  - Historical completion is preserved. `T-534` is the clean successor rebuild and does not reopen or erase this record.

- [x] `T-534` — **Clean protocol-v2.1 PySide6 UI rebuild from current `main`.** COMPLETE.
  - Depends on: `T-527`, `T-529`, `T-533` — satisfied.
  - Separate scientific gate: `T-610` remains BLOCKED and is not a dependency of `T-534`.
  - Authority: DEC-059 for PySide6/runtime/scientific-firewall architecture; DEC-061 for the current experiment-first product/UX model; DEC-060 + `configs/protocols/protocol-v2.1-final.json` for current science; `docs/research/RQ_EVIDENCE_TRACEABILITY.md` for stored evidence; `docs/architecture/UI_INFORMATION_ARCHITECTURE.md` for detailed interaction/acceptance guidance.
  - Implementation: PR #107 / `feat/t-534-experiment-first-ui`, squash-merged into `main` as `c372c581b88c63f3b07c96bd50bbc17b9b83f835`.
  - Active presentation loads protocol-v2.1 fail-closed and removes stale v2.0/T-528 user-facing identity while preserving immutable historical records and compatibility-only historical DEVELOPMENT support.
  - Four primary surfaces are implemented: **Experiment / Run / Results / Evidence**; help/onboarding and technical/provenance detail are contextual/secondary.
  - **Experiment:** immutable five-method Thesis review plus backend-constrained DEVELOPMENT Configure → Review → Create; Frozen/Adaptive are paired regimes, not algorithms; no final-reserve identity/outcome is exposed.
  - **Run:** durable per-method status, one dominant Phase-A GridWorld, exact condition-aware Phase-B FD/AD pairing by method/root/layout/condition/interaction, explicit Frozen/Adaptive meanings, primary action/reward facts and progressive technical detail.
  - **Results:** explicit RQ1/RQ2/RQ3 organization over the existing strict stored-output reader; right-censored recovery remains `recovery_time=null` and the fixed horizon is shown only as the separately named restricted delay.
  - **Evidence:** backend-registered readiness/outputs first; artifact IDs, registered paths, SHA-256, actual source job/artifact IDs and registered lineage metadata under technical disclosure; no arbitrary filesystem browser.
  - Live presentation remains lossy/non-blocking and scientifically passive; the UI cannot alter actions/observations/RNG/checkpoints/timing/metrics/evidence or final authorization.
  - DEVELOPMENT/synthetic deterministic review covers 1366×768 and 1440×900 Experiment, DEVELOPMENT review, Phase A, exact Phase B, RQ1, RQ2, recovered/right-censored RQ3, Evidence and onboarding/lock states without scientific job execution or final-reserve access.
  - Objective review findings were fixed narrowly, including stale onboarding test behavior, Qt deferred-delete status overlap, laptop Run layout pressure, condition-aware pairing, truthful method status, primary live facts, full registered Evidence lineage and non-color-only status semantics.
  - Completion validation: exact PR head `0fff019d8bd1b90bd1809f2c2f5b0c0662d743da` passed Repository checks #864 and T-534 PySide6 UI acceptance #174; deterministic renders were visually reviewed; PR #107 was squash-merged; merged `main` was verified to contain the accepted implementation.
  - Completion of T-534 does **not** authorize `T-610`, final-reserve access, final results inspection or WP7/Results/Discussion writing.

- [x] `T-535` — **Pre-T610 intended-user UX hardening** (#109 / PR #110). COMPLETE.
  - Depends on: `T-534` — satisfied.
  - Origin: post-T-534 intended-user workflow analysis plus exact-head 1366×768/1440×900 screenshot review identified bounded presentation/workflow gaps not requiring any scientific amendment.
  - T-534 remains COMPLETE historical implementation/acceptance; protocol-v2.1 science, Study/read-model authority, final-reserve sealing and backend execution authorization were unchanged.
  - DEVELOPMENT Create → Run now selects the newly created experiment record even when older durable records exist.
  - Selected Run experiment context propagates to Evidence and compatible Results; when the current run has no stored analysis, Results explicitly says so instead of silently implying an older package belongs to it.
  - Primary terminology is `Experiment record`; stable record IDs remain identifiers where no separate human label exists.
  - Direct method comparisons remain inside their scientific question: Phase-A comparisons in RQ1, Phase-B comparisons in RQ2, recovery comparisons in RQ3, all projected from already-stored backend contrasts only.
  - Results provenance and direct-comparison detail use progressive disclosure so research results remain visually primary at laptop viewports.
  - Infrastructure retry is hidden when no infrastructure failure exists; Evidence next actions name the application surface/action the user should take.
  - Final-gate copy is task-agnostic while final execution remains controlled exclusively by the separate backend authorization gate.
  - Validation: exact head `710f7f4290b07dba682db2f1c548d19ec43c1876` passed Repository checks #872 and PySide6 UI acceptance #179, including focused T-535 Qt tests; deterministic artifact `9818821831` was visually reviewed at 1366×768 and 1440×900 with no objective regression.
  - Integration: PR #110 was squash-merged as `225df138c5c5be0c39c9e474ef7fdbce6b11245b`; merged-state verification confirmed the accepted hardening on `main`.
  - Explicit boundary held: no final roots/layouts/seeds/outcomes, no final-reserve access, no T-610 activation, and no scientific configuration/estimand/analysis change.

- [x] `T-536` — **Final visual polish and richer in-app result visualization** (#112 / PR #113). COMPLETE.
  - Depends on: `T-535` — satisfied.
  - Preserves the accepted **Experiment / Run / Results / Evidence** information architecture, sidebar/navigation, immutable five-method Thesis experiment, and simultaneous exact Frozen/Adaptive Phase-B presentation; no Frozen/Adaptive selector.
  - Run uses a larger GridWorld visual footprint while preserving clean 1366×768 and 1440×900 layouts; the current live method is explicit as `Method N of 5 · Name` and a compact five-method durable lifecycle strip remains status-only, never a ranking.
  - RQ1/RQ2 charts have stronger visual weight relative to supporting tables. RQ3 now has a true stored-evidence trajectory visualization with baseline gap, frozen tolerance/window contract, stored recovery-time summary where available, and explicit right-censoring where recovery is unavailable.
  - The RQ3 visual scales/positions already-stored values only; it does not reduce roots, derive thresholds, classify recovery, substitute the horizon as recovery time, or recalculate any scientific estimand/interval.
  - Readability and page/section/card/secondary hierarchy were improved through restrained spacing, typography and contrast; DEVELOPMENT review and Evidence readiness use existing content more effectively without decorative panels.
  - The Thesis state label is `Locked Thesis experiment`, reserving `Frozen` for the scientific Frozen regime and FN/FD terminology.
  - `docs/research/T-613_THESIS_FIGURE_INVENTORY.md` is the pre-execution downstream output contract: T-613 must later produce a rich reproducible main-thesis + appendix + defense figure/table package from validated stored final outputs, not from application screenshots.
  - Validation: exact head `eabdcd27855aac9e5cdcb0460c594ad1611e0a78` passed Repository checks #886 and PySide6 UI acceptance #190. Exact-head deterministic 1366×768/1440×900 renders were visually reviewed across Experiment/DEVELOPMENT, Run Phase A/B and exact matched pair, RQ1/RQ2/RQ3 recovered/right-censored states, Evidence and onboarding with no objective clipping/overlap regression.
  - Integration: PR #113 was squash-merged as `d16f16cef06406d8af974ef3bab5be9608d65666`; merged-state verification confirmed the accepted implementation and unchanged final-execution firewall on `main`.
  - Explicit boundary held: no final roots/layouts/seeds/outcomes were executed or inspected, no final-reserve execution occurred, no T-610 activation occurred, and no protocol/RQ/evidence/backend scientific contract changed.

- [x] `T-537` — **Final pre-T610 repository hygiene and active-tree cleanup** (#116 / PR #117). COMPLETE.
  - Depends on: `T-536` — satisfied.
  - Removed only superseded non-scientific residue with no active consumer: dead T-528 branch-bound workflows, committed superseded T-528 presentation screenshots, retired bibliography-downloader compatibility shim/test, orphan visual-reference pointer and redundant scaffold placeholders where a tracked README/file already preserves the directory.
  - Preserved all historical scientific protocols/configs, frozen/pilot/final evidence, result manifests, decisions and reproducibility-relevant scientific code. Seemingly redundant files inside finalized/historical evidence packages were explicitly not cleanup targets.
  - Generated UI review renders are CI/local artifacts and ignored from the active tree; the current PySide6 acceptance workflow remains available with task-agnostic naming.
  - Historical T-528/T-511 visual acceptance remains auditable through Git history and exact-head GitHub Actions artifacts after the superseded committed screenshot set was removed.
  - Validation: exact head `2d779b85c6be81b29920df4fd61406dce50c9094` passed Repository checks #892 and PySide6 UI acceptance #191, including current desktop/T-534/T-535/T-536 tests, deterministic renders and exact Frozen/Adaptive pairing.
  - Integration: PR #117 was squash-merged as `8fd32fbf68d7374ff1de5c70db21e9f95b129c1c`; merged-state verification confirmed the cleaned active tree on `main`.
  - Explicit boundary held: no protocol/RQ/estimand/backend contract changes, no final roots/layouts/seeds/outcomes, no final-reserve access and no T-610 activation.

- [x] `T-511` — **Historical intended-user application workflow/self-explanatory UX acceptance.**
  - Depends on: `T-512`, `T-528` — satisfied.
  - Accepted: 2026-09-01, after the user explicitly delegated intended-user acceptance of the then-current PySide6 workflow and verified screenshot/live-presentation requirements.
  - Scope: historical v2 thesis-study/custom configure/run/monitor/history/compare/export/error/help workflow. This acceptance remains audit history and does not declare the new `T-534` rebuild complete.
  - Capture boundary: the application is screenshot-ready and exposes truthful live GridWorld for external GIF/video capture; it does not claim an integrated GIF exporter. Real thesis/defense captures require later `ASSET-*` provenance records and static fallbacks.
  - Review surface: accepted T-528 PySide6 application plus its exact-head CI screenshot bundle and Git-history-preserved curated set; the superseded committed active-tree copy was removed by T-537.

## WP6 — Final scientific evidence

- [x] `T-600` — Historical frozen v1.0 final matrix.
- [x] `T-601` — Historical v1.0 evidence validation/freeze.
- [x] `T-602` — Historical v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical v1.0 evidence package.

- [ ] BLOCKED `T-610` — Execute frozen protocol-v2.1 final matrix through the accepted study-first execution path.
  - Depends on: `T-527`, `T-529`, `T-511`, `T-533`, `T-535`, `T-536`, `T-537` — satisfied.
  - Authorization gate: satisfied. The user supplied the separate explicit scientific execution authorization on 2026-09-02; immutable protocol fields and the accepted backend guard remain unchanged.
  - Durable Study: `protocol-v2.1-final`, recipe SHA-256 `8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154`, plan SHA-256 `073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4`, source commit `7442dcb65674dcb3bc9ce0c71996418289d79061` on native Windows CPython 3.12.13.
  - Preserved progress: 216/603 jobs completed (all 120 Phase-A jobs and all 96 Q-Learning Phase-B matched sets); 1 infrastructure failure; 386 pending; 0 running/scientific-failed/skipped/cancelled. The Study is `active`, unfinalized and has not entered validation, analysis or export.
  - Exact blocker: first SARSA Phase-B job `pb__sarsa__t527-final-r01__gw-l1-final-a__action-remap-swap-right-down` failed on attempt 1 with `ValueError: shared no-learning prefix requires a quiescent project learner; pending/deferred Phase-A state must be resolved by the frozen protocol`.
  - Cause boundary: the frozen recipe declares DEC-054 deployment-start settlement, but the generic Study Phase-A materialization path persists the raw final checkpoint without applying the already accepted deterministic boundary settlement. The resulting SARSA checkpoint may retain a deferred update and cannot satisfy the Phase-B shared-prefix precondition. The preflight integration coverage exercised Q-Learning and did not expose this SARSA transition.
  - Fail-closed rule: preserve the partial Study, run bundles, index mutation and failure event exactly as recorded. Do not retry unchanged, delete/overwrite/rerun completed jobs, patch or monkeypatch the active execution, mix source commits, finalize the Study, inspect outcomes for interpretation, or begin T-611/T-612/T-613/WP7.
  - Exact next action: require an explicit formal scientific recovery/amendment decision that defines a reproducible single-source recovery path and disposition of the existing partial final evidence before any code change or resumed execution.
- [ ] BLOCKED `T-611` — Validate/freeze v2.1 final evidence.
  - Depends on: `T-610`.
- [ ] BLOCKED `T-612` — Predeclared v2.1 nominal-learning/resilience/recovery statistical analysis and sensitivity diagnostics.
  - Depends on: `T-611`.
- [ ] BLOCKED `T-613` — Final v2.1 figures/tables/exports and thesis/defense evidence package.
  - Depends on: `T-612`.
  - Output contract: `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`.
  - Generate a deliberately rich, deterministic asset package from validated stored final outputs: RQ1 learning progression/final/time-average/root diagnostics/direct contrasts; RQ2 adaptation benefit/Frozen-vs-Adaptive losses/condition panels/paired diagnostics/heatmaps/direct contrasts; RQ3 recovery trajectories/recovered proportion/restricted delay/conditional recovery time/right-censor composition/sensitivity/root diagnostics/direct contrasts; plus methodology/evidence-lineage and defense variants.
  - Produce vector-first `SVG`/`PDF` where appropriate, high-resolution `PNG` for Word/PowerPoint compatibility, and machine-readable thesis tables such as `CSV`, with consistent method order, colorblind-safe/redundant visual encodings and no composite ranking.
  - Preserve right-censoring: non-recovery never receives the horizon as a fake observed recovery time. Use only T-612 validated estimands/root records/trajectories/contrasts; no outcome-driven post-hoc metric invention.
  - Register stable asset IDs and a manifest containing RQ/estimand/condition scope, source artifact IDs and SHA-256 values, evidence/analysis package identity, generator Git commit, presentation parameters, output variants and intended use (`main-thesis`, `appendix`, `defense`).
  - Application screenshots may illustrate the software workflow but are not the quantitative source for thesis claims.

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
  - Acceptance: package the accepted final frontend using delivery technology appropriate to the current PySide6 architecture; validate local launch/close/restart, writable paths, privacy/licensing/reproducibility. Post-thesis and not a pre-WP7 gate.

## Task maintenance rule

Every material checkpoint reconciles this registry. GitHub issues are tracking views, not a competing task list. In-progress/failed work never counts as complete.
