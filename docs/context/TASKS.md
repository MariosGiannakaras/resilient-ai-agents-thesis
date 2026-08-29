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

- **Package:** DEC-048/050 protocol-v2 methodology, completed DEC-051 study-first backend reconstruction, historical failed DEC-052 recovery and DEC-053's SB3 scientific-continuation identity correction/versioned T-526A recovery. DEC-042/047 and candidate v1.1 remain auditable predecessor design. DEC-049 controls the later new-framework frontend rebuild.
- **Project:** **4/8** master milestones complete (#87: 1, 2, 4, 5).
- **Current task:** `T-526` / recovery sub-gate `T-526A`.
- **State:** `T-526 BLOCKED`; `T-526A IN_PROGRESS`. DEC-052 remains a valid failed 2/30 attempt. The SB3 2.9.0 audit proved that raw archives contain non-scientific `data.start_time` and process-sensitive display metadata while the historical learner fingerprint covers all continuation state; omitted DQN `_n_calls` is independently fixed as `num_timesteps` by the frozen one-environment step invariant. DEC-053 now authorizes one versioned v0.2 physical attempt after exact reviewed-head/green-CI/clean-Windows gates. No v0.2 scientific execution has occurred yet.
- **Completed parallel backend work:** `T-529` is COMPLETE. The framework-neutral Study lifecycle now covers immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis with explicit denominators -> deterministic machine-readable evidence export, with restart-safe provenance and no frontend dependency.
- **Branch / PR:** `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; no parallel main-repo implementation branch and no early merge.
- **Trackers:** #87 master 4/8; #95 protocol-v2 6/10 after reconciliation of the completed physical environment-discrimination and five-core-method feasibility pilots; #88 closed/superseded; #89 complete/closed; #93 PAUSED; #94 DEFERRED post-thesis.
- **Historical science:** protocol-v1.0 / FINAL-* / R0 evidence immutable. Candidate v1.1 remains non-final history; old `T-522` must not execute. Historical scientific runners remain reproducible even when superseded application/runtime surfaces are removed from the active tree.
- **Bibliography:** immutable protocol-v2 consumer snapshot remains upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`, merged through thesis PR #96 and validated on PR #92.
- **Frontend direction:** final frontend is rebuilt from scratch with a **different framework from NiceGUI** at `T-528` only after T-527 scientific freeze. T-529's backend dependency is already satisfied.
- **Pre-WP7 approval:** NOT APPROVED; `T-700+` remains blocked.
- **Exact next action:** commit/push the DEC-053 audit, identity proofs and v0.2 config/runner; require both PR #92 checks green on that exact head and a clean native Windows worktree; then execute the v0.2 entrypoint exactly once. Phase B remains mechanically blocked until 30/30 accepted scientific continuation states. T-527 remains blocked.

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

- [ ] BLOCKED `T-526` — Run bounded environment-discrimination + method/severity/CPU feasibility pilots on the validated Windows machine.
  - Depends on: `T-525` — satisfied.
  - Predeclared plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`.
  - Physical entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`.
  - Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`.
  - First physical pass: ordered 7×7 → 10×10 → 14×14 GridWorld ladder, two layouts/level, three roots, five core methods, common 2048-interaction Phase-A budget, no-learning probes at 0/512/1024/2048, CPU/wall/checkpoint/failure evidence; stop at the first level that is neither a universal final floor nor a universal early ceiling.
  - After level selection, use only the already-predeclared Phase-B calibration candidates: action-remap mappings; action-failure probabilities; observation-corruption probabilities with explicit global valid-cell support. Calibrate semantics/non-degeneracy, never preferred method ranking. Exact action-remap identities remain categorical rather than falsely scalar severity.
  - Evaluate A2C promotion only for distinct thesis value vs PPO at acceptable matrix cost. Retain poor/failing outcomes. No final reserve.
  - External boundary: hosted CI does not substitute for the physical Windows runtime/feasibility evidence gate.
  - Physical Phase-A result (2026-08-29): repository recovery and clean native-Windows preflight completed at reviewed source commit `5198dbe077119b7caa4e9a101b55b115a979c22e`; the entrypoint executed exactly once. `gw-l1` (7×7) was the first acceptable level. All 30 planned units (five methods × three roots × two layouts) completed with 61,440 total training interactions, 28,524 probe interactions, 129.344 summed unit wall-seconds, 459.469 summed unit CPU-seconds and 4,680,026 aggregate serialized checkpoint bytes. No scientific failure, infrastructure failure, hard runtime abort or checkpoint warning occurred. Evidence: `results/pilots/protocol-v2-feasibility-v0.1/`.
  - Recovery result: DEC-052 preserved the original bundle/conclusions and correctly stopped on `dqn/t526-r01/gw-l1-a` when its raw checkpoint-envelope SHA differed despite exact checkpoint size and learner SHA. That failed evidence remains immutable; Phase B has 0/240 matched sets and 0 branch interactions.
  - Technical diagnosis: SB3 `model.save()` persists `data.start_time` and process-sensitive human-readable class metadata outside the scientific fingerprint; canonical ZIP wrapping preserves those bytes. The original and DEC-052 runs necessarily have different `start_time` values. Focused tests prove raw-byte inequality with exact historical/derived identities and exact restores, and prove online/target/optimizer/replay/counter/RNG perturbations fail. Full audit: `docs/research/T526_SB3_SCIENTIFIC_CONTINUATION_IDENTITY_AUDIT.md`.

- [ ] IN_PROGRESS `T-526A` — DEC-053 versioned scientific-continuation recovery is implemented and awaits its reviewed physical gate.
  - Depends on: retained one-time T-526 Phase-A evidence at `results/pilots/protocol-v2-feasibility-v0.1/`.
  - Authority: DEC-052 remains historical authority for its failed attempt. DEC-053 narrowly corrects SB3 transport-versus-scientific identity without changing outcomes/design and authorizes one from-scratch v0.2 attempt; it does not authorize replacement evidence, changed roots/seeds/methods/candidates, final-reserve access or outcome-driven tuning.
  - Pre-execution gate was satisfied: clean reviewed head `5e784d31729ad09c40f2633f3d1682896e624317` matched remote/PR #92 and both Repository/Protocol-v2 checks were green before physical execution.
  - Physical result: original hashes and unchanged-source check passed; Q-Learning and SARSA exact-matched; DQN `t526-r01/gw-l1-a` had expected learner SHA `bee1cce1...` and expected serialized size `460571`, but reconstructed checkpoint SHA `7b385564...` differed from expected `f2da03f3...`. The fail-closed runner retained 3 attempted checkpoint payloads, 2 exact matches and 1 infrastructure/recovery failure, then blocked Phase B.
  - Evidence: `results/pilots/protocol-v2-feasibility-v0.1-recovery/` (validated failed-barrier bundle; 499,535 hash-covered bytes). No Phase-B output directory exists.
  - DEC-053 paths: `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.2.json`, `src/resilient_agents/protocol_v2_t526_recovery_v02.py`, `scripts/run_protocol_v2_t526_recovery_phase_b_v02_windows.ps1`; new evidence is restricted to `results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2/` and, only after 30/30, `results/pilots/protocol-v2-feasibility-phase-b-v0.2/`.
  - Gate: commit/push, both required PR checks green on the exact head, PR #92 head equality and clean native Windows worktree. Reconstruct all 30 from unit one. Any scientific identity failure stops and retains the attempt; no additional relaxation is authorized.

- [ ] BLOCKED `T-527` — Fair tuning, precision/runtime sizing, statistical freeze and machine-readable protocol-v2 firewall.
  - Depends on: `T-526`.
  - Acceptance: bounded method-specific tuning with equivalent predeclared opportunity; common protocol-level gamma/reward/horizon values; fixed actual interaction budgets/probe grid compatible with retained update quanta; final retained methods/environment/severities/root count chosen only from non-final evidence; no best-seed/best-final-checkpoint selection.
  - Statistical freeze: root/run independent; block/equal layout handling; paired/DiD primary effects; Student-t root-level mean CI as default candidate subject to final pilot diagnostics/precision sizing; root-bootstrap/robust sensitivity; explicit failure denominators; limited primary contrast family and frozen multiplicity rule if p-values are used.
  - Freeze final layout/root reserve and exact Phase-B branch/update behavior before access.

- [x] `T-529` — Reconstruct the study-first protocol-v2 backend from recipe through evidence/analysis/export, without frontend implementation.
  - Depends on: `T-525` — satisfied. Completed without consuming or inventing unresolved T-526/T-527 values.
  - Controlling decision/spec: `docs/decisions/DEC-051_STUDY_FIRST_BACKEND_RECONSTRUCTION.md` and `docs/architecture/STUDY_BACKEND_REDESIGN.md`.
  - [x] Remove superseded NiceGUI application/runtime/packaging surfaces from the active tree while preserving historical scientific reproducibility in Git/history.
  - [x] Implement immutable `StudyRecipe`, evidence classes, ordered stages, job DAG, stage barriers, scientific/infrastructure failure distinction, durable `StudyStore`, lineage and finalized-integrity checks.
  - [x] Implement deterministic recipe-to-plan materialization with stable Phase-A/Phase-B job IDs, method-specific condition eligibility and exact Phase-A producer dependencies.
  - [x] Implement generic execution ports, scheduler and framework-neutral restart-safe `StudyService` facade.
  - [x] Implement real protocol-v2 Phase-A/Phase-B study executors over the validated Q/SARSA/DQN/PPO/Dyna-Q+ drivers, emitting standardized scientific artifacts/analysis records; Phase-B remains fail-closed for any lifecycle not yet frozen by T-527.
  - [x] Implement structural v2 evidence validation and a validation-stage executor that reconciles expected jobs/artifacts/checkpoint lineage and retained scientific failures.
  - [x] Complete standardized v2 analysis records/statistical engine with root/layout blocking, matched FN/FD/AN/AD estimands, explicit failure denominators and explicit recipe-driven statistical inputs.
  - [x] Implement deterministic study export/handoff package for machine-readable CSV/JSON tables, stable evidence/result IDs and provenance/lineage for later thesis/defense tooling; T-529 generates no thesis prose, thesis figures or PPTX.
  - [x] Reconcile active docs/decision index and quarantine remaining v1.x application assumptions; historical scientific evidence/runners stay reproducible and cannot contaminate v2 confirmatory analysis.
  - Acceptance satisfied: one immutable Study recipe is covered end to end through planning, restart-safe execution, real Phase A, exact checkpoint consumption, common no-learning prefix, atomic FN/FD/AN/AD, retained scientific failure semantics, validation, root/layout analysis, explicit denominators and deterministic lineage-preserving export without UI logic. Dedicated protocol-v2 and repository-wide CI were green on the reviewed implementation head; this checkpoint closes the remaining documentation reconciliation.

- [x] `T-530` — Historical truthful UI-independent Python runtime service/read-only observer foundation. **Superseded for final application by DEC-051/T-529; implementation removed from active tree after study-first replacement began.**
- [x] `T-531` — Functional NiceGUI prototype over validated backend. **Prototype/history only; active implementation removed by DEC-049/051.**
- [x] `T-532` — Prototype screenshot/packaging feasibility work. **Prototype/history only; active implementation removed by DEC-049/051.**

- [ ] BLOCKED `T-528` — Select a different frontend framework and rebuild the final v2-aware application UI/UX from scratch (#93).
  - Depends on: `T-527`; `T-529` is satisfied.
  - Acceptance: select a **different framework from NiceGUI** only after the framework-neutral v2 scientific/study backend is stable and T-527 freezes the remaining scientific/runtime contract; document selection for local desktop use, synchronized Frozen/Adaptive GridWorld rendering, scientific charts/tables, accessibility, maintainability, Python-service integration and later standalone delivery; consume `StudyService` DTOs/events without duplicating scientific execution.
  - Exact chart/table/diagram libraries and packaging technology are selected here/later, not inherited from the historical NiceGUI stack.

- [ ] BLOCKED `T-511` — Intended-user application workflow/self-explanatory UX acceptance.
  - Depends on: `T-512`, `T-528`.
  - Acceptance: user explicitly accepts final v2 thesis-study/custom configure/run/monitor/history/compare/export/error/help workflow. Automated checks never close this gate.

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
