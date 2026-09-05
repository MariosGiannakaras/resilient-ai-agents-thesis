# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Preserve exact task/dependency/resume state across Codex sessions, quota interruptions, restarts and chat changes.

`CURRENT_STATUS.md` is the compact status summary. This file is the canonical task/dependency checklist.

## Mandatory session rule

Every implementation/repository session MUST recover from:

1. `AGENTS.md`
2. `docs/context/WORK_STATE.json`
3. `docs/context/TASKS.md`
4. `docs/context/CURRENT_STATUS.md`

Session memory and conversation/model memory are advisory only. Repository/Git/GitHub/evidence wins when memory is stale or contradictory. Inspect `git status`, the active branch, recent commits, open PR/CI state and any `IN_PROGRESS` work before selecting new work.

Status: `[x]` complete; `READY` dependency-valid; `IN_PROGRESS` active; `BLOCKED` gate/dependency unmet; `DEFERRED` intentionally later; `SUPERSEDED` retained history that must not execute. In-progress/failed work never counts as complete.

## Resume state

- **Package:** protocol-v2.0 methodology/scientific freeze remains immutable through DEC-058; the framework-neutral Study backend is complete through DEC-051/T-529; historical PySide6 application work remains complete through DEC-059/T-528; DEC-060/T-533, pre-final readiness hardening, DEC-061/T-534, intended-user hardening T-535, final visual polish/richer result visualization T-536, and final pre-T610 active-tree hygiene T-537 are complete. DEC-042/047 and candidate v1.1 remain auditable predecessor design; historical NiceGUI remains prototype history only.
- **Project:** **8/8** master milestones objectively complete (#87). The accepted application and complete T-610→T-613 final v2.1 evidence chain have passed their objective gates. The user explicitly approved entry into WP7 on 2026-09-03; T-700, T-701, T-702, T-710, T-711, T-714 and T-715 are complete. T-715 reader-scope/audit reconciliation was squash-merged through PR #138 as `35c5367f075a2f3af0bb6d40d9db08cfc484419c`.
- **Current task:** `T-717` is **IN_PROGRESS** as a bounded author-directed pre-freeze content refinement. `T-712` remains **DEFERRED** pending actual supervisor/reviewer feedback; T-010 and T-716 remain COMPLETE, and T-713 stays downstream of resolved real feedback plus authoritative official metadata/declaration and final Word/submission gates.
- **Separate scientific gate:** SATISFIED for T-610 only. The committed protocol continues to retain `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate`; authorization is supplied separately through the backend `PROTOCOL_V21_FINAL_EXECUTION_AUTHORIZATION` token without changing those immutable fields or weakening the guard.
- **State:** DEC-055 tuning remains immutable valid-complete; DEC-055/056 sizing packages remain immutable valid-failed. DEC-057 sizing-v0.3 and the combined five-method sizing package are valid-complete. DEC-058 remains the historical frozen protocol-v2.0 authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the accepted protocol-v2.1 scientific authority; T-610/T-611/T-612 execution, freeze and analysis are complete while the final roots/layouts, five methods, hyperparameters, conditions, budgets and 256-interaction Phase-B horizon remain immutable. `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain mandatory.
- **T-533 implementation:** COMPLETE. The isolated protocol-v2.1 path includes passive fixed 32-interaction Phase-B reward windows, schema-v2 temporal evidence/validation, right-censored recovery/non-recovery analysis, direct root-paired method contrasts, actual-root-count Student-t interval selection, deterministic evidence exports with v2.1 provenance, protocol-aware executor routers, fail-closed self-contained recipe materialization, and PySide6 stored-evidence recovery/contrast presentation with no UI-side estimand computation.
- **Completed Study backend:** `T-529` is COMPLETE. The framework-neutral Study lifecycle covers immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis with explicit denominators -> deterministic machine-readable evidence export, with restart-safe provenance and no frontend dependency.
- **Historical completed application baseline:** `T-528` remains COMPLETE and is not repurposed. It records the accepted PySide6 architecture/workflow/read-model/application baseline and prior intended-user acceptance history. Its presentation implementation is not the authority for the completed T-534/T-535/T-536 application; reusable UI-neutral contracts were preserved where still correct.
- **Final evidence, analysis and assets:** T-611 freeze remains valid at manifest SHA-256 `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858` and 600-record inventory SHA-256 `0c2b352b88045951d32e58ee3479656dce00e35d55899bcdea65dc07604d8045`. T-612 finalized `results/analysis/protocol-v2.1-final/` under analysis manifest SHA-256 `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`. T-613 finalized `results/thesis-assets/protocol-v2.1-final/` under asset manifest SHA-256 `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8` with generator source commit `90b2953b95f14dddf3920d192fc736718360284a`.
- **Final read-only merged-main preflight:** COMPLETE after T-536 merge. It confirmed the exact validated tree, no committed `protocol-v2.1-final` Study bundle, default final execution blocked, and the canonical 603-job plan with `final_execution_authorized=false`. T-537 changed no scientific/execution code, so these gate semantics remain unchanged.
- **Repository integration:** PR #92 is historical and was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`. Subsequent protocol-v2.1 readiness and pre-UI context cleanup were also merged. PR #107 was squash-merged as `c372c581b88c63f3b07c96bd50bbc17b9b83f835`; PR #110 as `225df138c5c5be0c39c9e474ef7fdbce6b11245b`; PR #113 as `d16f16cef06406d8af974ef3bab5be9608d65666`; post-T536 reconciliation as `4ffb7bc700b3d485324c659e94823c9d2e272cba`; README refresh PR #115 as `31877a09ec2eda7852856c6c1cf7ae059bbf72ae`; PR #117 / T-537 as `8fd32fbf68d7374ff1de5c70db21e9f95b129c1c`; T-610 authorization PR #119 as `7442dcb65674dcb3bc9ce0c71996418289d79061`; fail-closed reconciliation PR #120 as `4a2740dbf143bc0aa9eb7845180001403ac77fde`; DEC-062 recovery implementation/evidence preservation PR #122 as `86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730`; finalized replacement evidence checkpoint PR #123; T-611 validation/freeze integration PR #124; T-702 immutable sync request PR #129 as `4cb655b59481abe0edfade0340df43a3c81f8ed2`; generated complete-corpus sync PR #130 as `536ab4d76e7d5a3271730d37ad3bc03934fd82a6`; T-702 reconciliation PR #131 as `dae55c3703472a12812499aff9cd639d3390948c`; T-710 manuscript PR #132 as `b8019ece98b9f6a89350b8aa52c205b20225f013`; T-714 PR #136 as `42afba20fd5a7e9d3912418d0847b42e566aaca0`; and T-715 PR #138 as `35c5367f075a2f3af0bb6d40d9db08cfc484419c`.
- **Trackers:** #87 master 8/8 CLOSED/completed; #95 protocol-v2 10/10 CLOSED; #98 T-533 CLOSED/COMPLETE; #88 closed/superseded; #89 complete/closed; #93 T-528 complete/closed; #94 DEFERRED post-thesis; #104 T-534 COMPLETE/CLOSED; #109 T-535 COMPLETE/CLOSED; #112 T-536 COMPLETE/CLOSED; #116 T-537 COMPLETE/CLOSED after post-merge reconciliation.
- **Historical science:** protocol-v1.0 / FINAL-* / R0 evidence immutable. Candidate v1.1 remains non-final history; old `T-522` must not execute. Historical `T-530`, `T-531` and `T-532` remain completed/superseded history and are not repurposed.
- **Bibliography:** current immutable writing-gate consumer checkout is upstream SHA `27674a566ab55e4491b74243fe077a31ef81ae73`, synchronized through thesis PR #143 / merge commit `2b302173be855c914af34555a8470015085662d8` and validated at 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals. Earlier SHA `ada0d1aec7511098fd12610ae9e5abe7aea875cd`, historical SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5` and label `bibliography-integration-v3` remain immutable prior-snapshot provenance only.
- **Pre-WP7 approval:** APPROVED by explicit user direction on 2026-09-03 after T-613 completion.
- **Exact next action:** finish `T-717`: persist the reproducible DOCX/QA artifact, claim-evidence registration and all CI gates on `thesis/t717-final-content-refinement`; merge only when green, then normalize the operational pointer back to the real `T-712` external-feedback gate.

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
- [x] `T-010` — **Prompt-free self-resuming repository workflow and durable work-state checkpoints.** COMPLETE.
  - Depends on: `T-008`, `T-009` — satisfied.
  - Scope: `AGENTS.md` becomes the automatic execution/recovery contract; `WORK_STATE.json` records the active operational checkpoint; every material action/checkpoint updates it; non-trivial work is pushed and surfaced in an early PR; Git/GitHub state is inspected before task selection.
  - Acceptance: memory-independent recovery order is explicit; half-finished work resumes before new work; `scripts/project_checkpoint.py` and `scripts/validate_project_continuity.py` exist; material PRs update `WORK_STATE.json`; prompt dependency is removed; active docs/validators/CI are reconciled; PR #146 is green and merged; main is normalized to the next real task/external gate.

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

- [ ] DEFERRED `T-538` — Bounded post-final application presentation polish.
  - Non-scientific and not a T-714/T-712/T-713 blocker.
  - Reconcile the Experiment page with the completed/frozen final-study state; extend existing onboarding only where the end-to-end campaign→validation→evidence-finalization path is not already self-explanatory; add Run progress detail only when backed by stored runtime state and visually useful; optionally capture 2–4 authentic implementation screenshots for Chapter 4 if they improve explanation. Screenshots remain implementation illustrations, never scientific evidence.

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

- [x] `T-610` — Execute frozen protocol-v2.1 final matrix through the accepted study-first execution path.
  - Depends on: `T-527`, `T-529`, `T-511`, `T-533`, `T-535`, `T-536`, `T-537` — satisfied.
  - Authorization gate: satisfied. The user supplied the separate explicit scientific execution authorization on 2026-09-02; immutable protocol fields and the accepted backend guard remain unchanged.
  - Historical failed Study: `protocol-v2.1-final`, recipe SHA-256 `8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154`, plan SHA-256 `073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4`, source commit `7442dcb65674dcb3bc9ce0c71996418289d79061` on native Windows CPython 3.12.13.
  - Preserved progress: 216/603 jobs completed (all 120 Phase-A jobs and all 96 Q-Learning Phase-B matched sets); 1 infrastructure failure; 386 pending; 0 running/scientific-failed/skipped/cancelled. The Study is `active`, unfinalized and has not entered validation, analysis or export.
  - Exact blocker: first SARSA Phase-B job `pb__sarsa__t527-final-r01__gw-l1-final-a__action-remap-swap-right-down` failed on attempt 1 with `ValueError: shared no-learning prefix requires a quiescent project learner; pending/deferred Phase-A state must be resolved by the frozen protocol`.
  - Cause boundary: the frozen recipe declares DEC-054 deployment-start settlement, but the generic Study Phase-A materialization path persists the raw final checkpoint without applying the already accepted deterministic boundary settlement. The resulting SARSA checkpoint may retain a deferred update and cannot satisfy the Phase-B shared-prefix precondition. The preflight integration coverage exercised Q-Learning and did not expose this SARSA transition.
  - Recovery authority: DEC-062. The defect is an implementation omission of the pre-outcome, physically validated DEC-054 rule, not scientific tuning. Apply the existing zero-interaction method-aware settlement in the generic Phase-A Study path; preserve fail-closed handling of invalid unfinished state.
  - Historical disposition: preserve the original Study, all 216 completed bundles, index records and failure event byte-for-byte. It remains active/unfinalized historical failed evidence and is ineligible for T-611/T-612/T-613, thesis results or conclusions. Never resume it or reuse/mix any job/checkpoint.
  - Replacement identity: scientific recipe `protocol-v2.1-final`; execution instance `protocol-v2.1-final--t610-recovery-01`; predecessor `protocol-v2.1-final`; decision `DEC-062`; corrected source commit recorded at creation. Execution identity changes only storage/provenance namespace, never the recipe/plan/statistical identity.
  - Accepted execution: replacement source commit `86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730`; 603 completed, 0 infrastructure/scientific failed, 0 pending/running/skipped/cancelled; finalized `completed`; 600 finalized scientific run bundles; recipe and plan hashes unchanged. Finalization/integrity verification inspected lifecycle/provenance/checksums only, not outcome values.
  - Boundary: predeclared validation/analysis/export-shaped Study jobs completed mechanically as part of the immutable 603-job plan, but their artifacts are not accepted/frozen or interpreted by T-610. T-611 remains required before T-612 or any scientific use.
- [x] `T-611` — Validate/freeze v2.1 final evidence.
  - Depends on: `T-610`.
  - Accepted only the DEC-062 replacement execution `protocol-v2.1-final--t610-recovery-01`; the historical 216-job predecessor remains byte-verified, unfinalized and permanently excluded.
  - Re-materialized the frozen recipe/603-job plan and verified recipe SHA-256 `8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154`, plan SHA-256 `073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4` and execution source commit `86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730`.
  - Validated 603/603 resolved jobs, 600/600 scientific jobs and run bundles, 120 exact checkpoints, 3,255 registered artifacts, file/integrity-map hashes, unique run-index entries, confirmatory/derived evidence classes, scientific identities, exact checkpoint lineage, matched FN/FD/AN/AD branch sets, schema-v2 temporal windows and registered downstream handoff hashes.
  - Frozen `results/final-evidence/protocol-v2.1-final/` atomically with validator commit `b925b0ad603bf165e8632c74f2027c53f040b34b`, manifest SHA-256 `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858` and 600-record run-manifest inventory SHA-256 `0c2b352b88045951d32e58ee3479656dce00e35d55899bcdea65dc07604d8045`.
  - T-611 inspected numeric payloads only through existing schema/identity/integrity validation and made no method comparison, result interpretation, post-hoc metric, figure/table or thesis claim.
- [x] `T-612` — Predeclared v2.1 nominal-learning/resilience/recovery statistical analysis and sensitivity diagnostics.
  - Depends on: `T-611`.
  - Revalidated the exact T-611 freeze, 600 accepted runs and complete replacement lineage before interpretation; the historical 216-job attempt remained excluded.
  - Regenerated the canonical v2.1 analysis package and 12 machine-readable data exports twice from the accepted replacement; every regenerated file matched the precomputed Study artifact byte-for-byte. The tool bytes are pinned to durable merged-main analysis source commit `7e56753d581999af38510be1745ec4b87a927f2f`.
  - Finalized `results/analysis/protocol-v2.1-final/` with manifest SHA-256 `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`, full RQ1/RQ2/RQ3 coverage, complete 12-root/two-layout blocks, actual-root-count Student-t intervals, 220 declared method contrasts, right-censoring validation and 0.05/0.10/0.20 recovery sensitivity diagnostics.
  - Recorded the bounded scientific interpretation and caveats in `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`; no p-value significance family, composite ranking, protocol redesign, T-613 asset generation, WP7 writing or defense work occurred.
- [x] `T-613` — Final v2.1 figures/tables/exports and thesis/defense evidence package.
  - Depends on: `T-612`.
  - Output contract: `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`.
  - Finalized 31 figures in deterministic SVG/PDF/300-DPI PNG triplets and 12 table assets in canonical CSV plus human-readable Markdown where applicable; 117 output variants are registered in `results/thesis-assets/protocol-v2.1-final/asset-manifest.json`.
  - Covered RQ1 endpoint/time-average/root/direct contrasts; RQ2 adaptation benefit, distinct Frozen/Adaptive loss, condition/root/heatmap/direct contrasts; RQ3 trajectories, recovered proportion, restricted/conditional timing, censoring, sensitivity and direct contrasts; plus methodology, evidence-lineage and defense-only descriptive variants.
  - Explicitly dispositioned inventory categories 1 and 6 as unavailable because the finalized T-612 package contains no registered probe/checkpoint-series values; no alternate raw source or post-hoc reconstruction was used.
  - Preserved T-611/T-612 identities, exact canonical CSV bytes, stable method/condition order, colorblind-safe colors plus redundant markers/line styles, actual stored intervals/denominators and null recovery times for right-censored roots. No composite score, p-value claim, ranking or new estimand was introduced.
  - Reproduced the full 121-file package twice byte-for-byte, normalized cross-platform text bytes, validated registered source artifact IDs plus all manifest/source/output hashes and format triplets, and visually inspected representative main, appendix, contrast, trajectory and lineage renders. Asset manifest SHA-256: `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8`; generator source commit: `90b2953b95f14dddf3920d192fc736718360284a`.
  - Application screenshots are not quantitative sources. No T-700/WP7, thesis Results/Discussion prose, defense narrative or slide production occurred.

## Mandatory pre-WP7 user approval gate

**APPROVED.** The user explicitly directed the project on 2026-09-03, after T-613 completion, to begin the next required WP7 work and to request example theses when needed. This approval unlocked T-700/T-701 and later WP7 tasks through their declared dependencies. The major-writing bibliography gate is now satisfied by T-702; later supervisor/official-delivery checks remain governed by their own tasks.

## WP7 — Thesis writing/review/defense

- [x] `T-700` — Recheck current Department/University submission/formatting/defense rules and current tool assumptions.
  - Depends on: `T-613`, `T-511`, explicit pre-WP7 user approval — satisfied.
  - Re-verified current public ICE thesis-writing guidance, Article 28/internal PPS regulation and relevant University deposit workflow on 2026-09-03.
  - Dated snapshot: `docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`.
  - Current public ICE guidance still supports the recorded front matter, A4/Times New Roman 11/1.5-spacing/heading-style Word contract and does not expose a newer public replacement found by the T-700 search.
  - No public ICE-specific defense duration, slide-count, PowerPoint-template or mandatory-live-demo rule was found; these remain explicitly unresolved for later T-720/T-722 recheck rather than borrowed from another department.
  - Selected IEEE numeric citations as the project WP7 default because the Department permits multiple consistent styles and the technically closest ICE examples predominantly use numeric references; any later explicit supervisor/Department instruction overrides this project choice.
- [x] `T-701` — Review completed example theses and derive structure/style guide.
  - Reviewed 22 user-supplied files representing 21 unique completed theses; `example-theses 1.pdf` and `example-theses 10.pdf` are byte-identical and count once.
  - Examples span theoretical, software, hardware, ML/CV, simulation and experimental work; recent/research-oriented examples were weighted more heavily for structural fit, but no individual thesis is treated as a template.
  - Final structure/style authority: `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`.
  - Frozen writing architecture: seven substantive chapters — Introduction; Background/Related Work; Methodology/Experimental Design; Research-System Architecture/Implementation; Results; Discussion; Conclusions/Future Work — plus official front matter, references and appendices.
  - Dedicated Results and Discussion are intentionally separated even though many examples merge interpretation into evaluation/conclusions; the project requires this stricter structure because T-612 has three distinct RQs/estimands, paired contrasts, uncertainty intervals, sensitivity and right-censoring.
  - Examples remain contextual structure/style evidence only and were not added to `ThesisBibliography` or used for scientific claims.
- [x] `T-702` — Major-writing-gate bibliography freshness review and immutable consumer re-sync. COMPLETE.
  - Depends on: `T-701`, REQ-RES-012 / REQ-THESIS-007 — satisfied.
  - Completed dated writing-gate freshness review on 2026-09-03 in canonical `MariosGiannakaras/ThesisBibliography`; the bounded search targeted the final RQs/methods/non-stationarity/recovery/adaptation concepts without reopening protocol-v2.1.
  - Promoted two non-redundant 2025 peer-reviewed supporting sources through normal canonical source/analysis/evidence/selection governance: `SRC-6F4F8BE003` (ICLR 2025, online RL in non-stationary context-driven environments) and `SRC-D38364B32C` (CoLLAs/PMLR 2025, adaptive partial models for model-based RL).
  - No screened evidence required protocol amendment, re-analysis, new experimental roots/methods, changed estimands or changed recovery thresholds; T-611 evidence, T-612 results and T-613 quantitative assets remain frozen.
  - Accepted immutable checkout: `ada0d1aec7511098fd12610ae9e5abe7aea875cd`; complete-corpus source commit `c999dbe272baa081d3666254655aeeec17549c1f`; citation-ready source commit `84d62ec3eb18e1d3565625bc02c289131282ea27`.
  - Synchronized through the controlled read-only thesis consumer workflow and PR #130. Integrated validation passed at 599 canonical sources, 123 citation-ready sources, 19 research materials, 281 indexed originals and 1,634 integrity-covered corpus files; trust-aware reference validation reports 40 thesis references (38 citation-ready, 2 research-material).
- [x] `T-710` — Draft complete Greek thesis from accepted evidence. COMPLETE.
  - Depends on: `T-702` — satisfied.
  - Drafted according to `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md` and `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` in evidence-first order.
  - Merged manuscript package: `docs/thesis/draft/` with Greek summary/English abstract, Chapters 1–7, T-710 evidence map, glossary/acronyms, appendix draft and manuscript/asset/citation handoff register.
  - Formal external citations use validated citation-ready `SRC-*` placeholders for deterministic IEEE conversion in T-711. A corpus-only Dyna source detected by the consumer validator was removed from formal manuscript/register use; the corrected PR head passed bibliography usage validation.
  - Quantitative/result prose uses only accepted T-611/T-612/T-613 evidence and registered T-613 asset IDs; right-censoring, denominators, pointwise intervals and no-universal-ranking boundaries are preserved. No new estimand, threshold, p-value family, causal claim or post-hoc re-analysis was introduced.
  - Validation/integration: PR #132 exact corrected head `e62ea790f16ab87622c1a9cc1102d5bdb1aceaa5` passed Repository checks #929, including 427 tests and installed-bibliography validation, then squash-merged as `b8019ece98b9f6a89350b8aa52c205b20225f013`.
- [x] `T-711` — Produce and validate the review-ready editable Word thesis. COMPLETE.
  - Depends on: `T-710` — satisfied.
  - PR #134 composed the merged manuscript into a real editable `.docx`, converted validated citation-ready source IDs to IEEE numeric references, inserted all 24 planned registered scientific figures and three numbered Word tables, preserved Word headings/TOC/list/caption fields and passed structural plus full rendered-page QA; squash-merged as `8d67e578cd18253a46a8185bd00adfb2dc0f29e2`.
  - PR #135 added one unnumbered composition-only ‘results at a glance’ synthesis graphic from already frozen RQ1/RQ2/RQ3 values, strengthened final-artifact provenance/hash QA and was squash-merged as `40ea5fdddd9d463916915d5655ea14c0bb869146`.
  - Accepted T-711 review artifact before T-714 contained 24 registered scientific figures plus one synthesis graphic, 14 verified references and 3 Word tables with 83/83 pages covered by visual QA. No protocol, estimand, result, censoring decision or T-613 quantitative asset byte changed.
- [x] `T-714` — Final pre-supervisor academic/compliance hardening of the accepted T-711 thesis. COMPLETE.
  - Depends on: `T-711` — satisfied.
  - PR #136 completed the bounded editorial/composition hardening: corrected the DQN citation boundary and unsupported superiority wording; strengthened Related Work with three verified citation-ready sources; normalized 17 references; localized all 24 figure captions; added the RQ3 conditional-recovery warning and 25/25 alt texts; scrubbed generic DOCX metadata; corrected academic front/end-matter ordering; made Appendix A self-contained from the frozen protocol; removed review-production appendix prose; and enforced placeholder-aware final mode.
  - Pagination hardening removed the front-matter blank page and Chapter 2 orphan page, kept glossary terms with their definitions, and kept the Chapter 4 architecture-flow summary together. Exact PR head `901b53e3fd7a8b84daee37dbbd485f1ff2173c55` passed Repository checks and T-711/T-714 DOCX QA v18. The final review-ready DOCX SHA-256 is `70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`; 84/84 rendered pages are visually covered.
  - Squash-merged through PR #136 as `42afba20fd5a7e9d3912418d0847b42e566aaca0`. Exactly three official-person/declaration placeholders remain intentionally review-only; final-mode/T-713 must reject them. No experiment, estimand, numerical result, right-censoring decision or registered T-613 scientific media byte changed.
- [x] `T-715` — Reader-scope simplification plus audit reconciliation of the review-ready thesis. COMPLETE.
  - Depends on: `T-714` — satisfied.
  - User authorization: the reader-scope cycle was initiated on 2026-09-04 and explicitly resumed/authorized for audit reconciliation on 2026-09-05. This was an internal writing/composition task, not supervisor feedback and not `T-712`.
  - Audit reconciliation authority is recorded in `docs/thesis/T715_AUDIT_RECONCILIATION.md`. The supplied audit/prior answer was used as a review checklist only; repository protocol, implementation, tuning/sizing decisions and predeclared analysis overrode conflicting copied statements.
  - The accepted v27 composition adds 26 bounded clarification paragraphs, including three Heading-3 subsections, covering the 180-unit bounded tuning design and frozen winners, exact disturbance semantics, RQ1/RQ2/RQ3 formulas, 12-root sizing rationale, seed streams, finite-horizon recovery interpretation and corresponding limitations/appendix details. It retains 10 registered scientific figures in the main body and 14 in appendices; the two PySide6 screenshots are deterministic DEVELOPMENT-only explanatory captures, not scientific evidence.
  - No new experiment/reanalysis or post-hoc binomial test was introduced. Frozen recovery remains 32-interaction windows, directed tolerance 0.10, two-window stability and right-censoring at 256; action-failure no-op reward is −0.1; observation corruption excludes the current true state but not goal as a category.
  - Exact validated PR head `6af6eb32961da07703fbd654d0ca071200668be3` passed Repository checks #1035, T-711/T-714/T-715 DOCX QA #98 and the T-715 four-file rewrite-workbook workflow #9. The CI-produced review DOCX has SHA-256 `e06a466e667359486a86f30c561c42b74b4e209ea28bb8d94c2652c9d36616d1`, 446 paragraphs and 59 rendered pages; final visual QA covered 59/59 pages with no objective layout defect. QA preserved inline-shape/media hashes and recorded `scientific_values_modified=false` and `registered_asset_bytes_modified=false`.
  - Integration: PR #138 was squash-merged into `main` as `35c5367f075a2f3af0bb6d40d9db08cfc484419c`.
- [x] `T-716` — **Restore, expand and evidence-audit the full-content thesis** while preserving validated T-715 audit corrections. COMPLETE.
  - Depends on: `T-714`, `T-715` — satisfied.
  - User direction: on 2026-09-05 the user explicitly rejected the excessive reader-scope compression and required complete deliverables rather than partial/shortened substitutes.
  - Composition baseline: archived T-714 run #66 DOCX SHA-256 `70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`, approximately 20,925 whole-document words. Restore and, where academically justified, expand substantive Background/Related Work, Methodology, Architecture/Implementation, Results interpretation and Discussion; do not pad with filler.
  - Scientific correction overlay: retain all validated T-715 audit corrections and frozen T-611/T-612/T-613 evidence boundaries. The compressed T-715 run #98 DOCX is a historical audit-reconciled milestone, not the final composition baseline.
  - Persistence gate: every user-facing DOCX/PDF/QA milestone must be committed under `thesis/archive/` or `thesis/final/` before handoff; `/mnt/data` and Actions artifacts are transient working copies only.
  - Stage-3 checkpoint: archived `T716_stage3_full_content_review_ready.docx` has 25,265 words, 765 paragraphs, 30/30 used bibliography entries, 25 preserved scientific media items, semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e` and manual 92/92-page visual QA with no recorded defect.
  - Stage-4/final T-716 checkpoint: archived `T716_stage4_evidence_audited_review_ready.docx` has 25,327 words, 766 paragraphs, 31/31 governed references used, 25/25 scientific media preserved, semantic package SHA-256 `b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1`, and 92-page visual QA (79 pixel-identical pages from stage 3 plus manual inspection of all 13 changed pages).
  - Final acceptance: `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records PASS on all 11 `T716_REWRITE_PLAN.md` gates, including citation-ready resolution, claim registration, source precedence, frozen-science/media preservation, DOCX/visual QA and permanent archive identity.
  - Administrative boundary: three deliberate front-matter placeholders remain for official student/declaration data; these belong to T-713 and were intentionally not invented during T-716.
- [ ] IN_PROGRESS `T-717` — **Final pre-freeze content refinement after whole-manuscript audit.**
  - Depends on: `T-716` — satisfied.
  - User direction: on 2026-09-05 the user requested one final whole-thesis review before content freeze and explicitly authorized only additions that close real gaps without unnecessary expansion. This is internal author-directed work, not supervisor/reviewer feedback and not `T-712`.
  - Scope: add the bounded AI-agent→RL-agent bridge; replace the two redundant introductory diagrams with an exact held-out GridWorld/disturbance composite and a layered scientific-authority/data-flow figure; state that action-failure `p=0.15` and observation-corruption `p=0.05` are frozen severity points rather than a sweep; add bounded external-validity limitations for severity/frequency and single-change/fixed-horizon versus repeated/recurrent disruptions; register Robust-Gymnasium only for the perturbation-axis limitation.
  - Explicit exclusions: no new experiment, re-analysis, result plot, estimand, ranking, code listing, pseudocode, uncertainty-quantification subsection or duplicate change-detection theory. The recovered historical Phase-B UI fixture is excluded because `condition_unavailable`/`not-executed` state is not representative thesis illustration material.
  - Scientific boundary: protocol-v2.1, T-611 evidence, T-612 results and T-613 quantitative assets remain immutable. Of the 25 embedded media, only the two explanatory introductory figures may change; the other 23 must remain byte-identical to T-716.
  - Reproducibility gate: `scripts/t717_final_content_refinement.py` must regenerate the candidate from `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, preserving 32/32 used references, 27 SEQ + 3 TOC + 1 PAGE fields, zero comments/tracked changes/unresolved `SRC-*`, the three deliberate administrative placeholders and all frozen scientific sentinels.
  - Visual gate: 94-page render QA is complete; reproducible-build comparison must retain 92/94 pages pixel-identical to the fully reviewed candidate, with the only intentional visual differences on the two new figure pages.
  - Persistence gate: archive the generated DOCX and QA JSON under `thesis/archive/`, validate claim evidence and prompt-free continuity, open a PR, review exact diff/check state and squash-merge only when green. After merge, mark T-717 COMPLETE and restore `T-712 DEFERRED` as the operational pointer.
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
