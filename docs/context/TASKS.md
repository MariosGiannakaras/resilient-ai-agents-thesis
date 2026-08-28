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

- **Package:** DEC-048 protocol-v2 redesign refined by DEC-050 methodology closure. DEC-042/047 and candidate v1.1 remain auditable predecessor design. DEC-049 controls the later new-framework frontend rebuild.
- **Project:** **4/8** master milestones complete (#87: 1, 2, 4, 5).
- **Current task:** `T-526`.
- **State:** `READY`; T-525 framework-neutral multimethod backend implementation is complete and validated. The next scientific evidence is the predeclared non-final physical Windows feasibility gate; hosted CI cannot substitute for it.
- **Branch / PR:** `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; no parallel main-repo implementation branch.
- **Trackers:** #87 master 4/8; #95 protocol-v2 4/10; #88 closed/superseded; #89 complete/closed; #93 PAUSED; #94 DEFERRED post-thesis.
- **Historical science:** protocol-v1.0 / FINAL-* / R0 evidence immutable. Candidate v1.1 remains non-final history; old `T-522` must not execute.
- **Bibliography:** immutable protocol-v2 consumer snapshot remains upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`, merged through thesis PR #96 and validated on PR #92.
- **Frontend direction:** final frontend is rebuilt from scratch with a **different framework from NiceGUI** at `T-528` only after T-527 freezes the remaining v2 scientific/runtime contract.
- **Pre-WP7 approval:** NOT APPROVED; `T-700+` remains blocked.
- **Exact next action:** on the validated physical Windows thesis machine, execute `scripts/run_protocol_v2_feasibility_windows.ps1` exactly once from a clean reviewed branch state. Retain the generated `results/pilots/protocol-v2-feasibility-v0.1/` artifacts for review before Phase-B severity calibration. Do not access any final reserve, tune methods, start old T-522, or resume UI implementation early.

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
  - Do not perform final tuning, final matrix execution or UI work here.

- [ ] READY `T-526` — Run bounded environment-discrimination + method/severity/CPU feasibility pilots on the validated Windows machine.
  - Depends on: `T-525` — satisfied.
  - Predeclared plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`.
  - Physical entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`.
  - Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`.
  - First physical pass: ordered 7×7 → 10×10 → 14×14 GridWorld ladder, two layouts/level, three roots, five core methods, common 2048-interaction Phase-A budget, no-learning probes at 0/512/1024/2048, CPU/wall/checkpoint/failure evidence; stop at the first level that is neither a universal final floor nor a universal early ceiling.
  - Acceptance: small **predeclared ordered** GridWorld complexity ladder; common task semantics; simplest level avoiding universal floor/ceiling and CPU-feasible; project-owned interaction/runtime measurements; checkpoint/clone fidelity; artifact size; learning signal/variance; method-native update-boundary feasibility.
  - After level selection, use only the already-predeclared Phase-B calibration candidates: action-remap mappings; action-failure probabilities; observation-corruption probabilities with explicit global valid-cell support. Calibrate semantics/non-degeneracy, never preferred method ranking. Exact action-remap identities remain categorical rather than falsely scalar severity.
  - Evaluate A2C promotion only for distinct thesis value vs PPO at acceptable matrix cost. Retain poor/failing outcomes. No final reserve.
  - External boundary: hosted CI does not substitute for the physical Windows runtime/feasibility evidence gate.

- [ ] BLOCKED `T-527` — Fair tuning, precision/runtime sizing, statistical freeze and machine-readable protocol-v2 firewall.
  - Depends on: `T-526`.
  - Acceptance: bounded method-specific tuning with equivalent predeclared opportunity; common protocol-level gamma/reward/horizon values; fixed actual interaction budgets/probe grid compatible with retained update quanta; final retained methods/environment/severities/root count chosen only from non-final evidence; no best-seed/best-final-checkpoint selection.
  - Statistical freeze: root/run independent; block/equal layout handling; paired/DiD primary effects; Student-t root-level mean CI as default candidate subject to final pilot diagnostics/precision sizing; root-bootstrap/robust sensitivity; explicit failure denominators; limited primary contrast family and frozen multiplicity rule if p-values are used.
  - Freeze final layout/root reserve and exact Phase-B branch/update behavior before access.

- [x] `T-530` — Truthful UI-independent Python runtime service/read-only observer foundation.
- [x] `T-531` — Functional NiceGUI prototype over validated backend. **Prototype/history only.**
- [x] `T-532` — Prototype screenshot/packaging feasibility work. **Not final UI/delivery packaging.**

- [ ] BLOCKED `T-528` — Select a different frontend framework and rebuild the final v2-aware application UI/UX from scratch (#93).
  - Depends on: `T-527`.
  - Acceptance: select a **different framework from NiceGUI** only after the framework-neutral v2 backend is stable; document selection for local desktop use, dual Frozen/Adaptive GridWorld rendering, scientific charts/tables, accessibility, maintainability, Python-service integration and later standalone delivery; rebuild rather than restyle the NiceGUI prototype; consume backend DTOs/events without duplicating scientific execution.
  - Exact chart/table/diagram libraries and packaging technology are selected here/later, not inherited from the historical NiceGUI stack.

- [ ] BLOCKED `T-511` — Intended-user application workflow/self-explanatory UX acceptance.
  - Depends on: `T-512`, `T-528`.
  - Acceptance: user explicitly accepts final v2 configure/run/monitor/history/compare/export/error/help workflow. Automated checks never close this gate.

## WP6 — Final scientific evidence

- [x] `T-600` — Historical frozen v1.0 final matrix.
- [x] `T-601` — Historical v1.0 evidence validation/freeze.
- [x] `T-602` — Historical v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical v1.0 evidence package.

- [ ] BLOCKED `T-610` — Execute frozen protocol-v2 final matrix.
  - Depends on: `T-527`, `T-511`.
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
