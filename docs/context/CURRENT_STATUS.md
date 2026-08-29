# Current Project Status

**Date:** 2026-08-29  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use **progressive** task-specific reading of DEC-048/049/050/051/052/053 and `docs/research/` / `docs/architecture/` only as needed.

## Current execution state

- Historical accepted baseline includes completed `T-100` target-machine validation and `T-200` research framing through protocol-v1.0 WP6 evidence. Protocol-v1.0, FINAL-* and R0 evidence remain immutable. Candidate v1.1 is non-final history; old `T-522` must not execute.
- `T-524`, `T-525` and `T-529` are COMPLETE.
- `T-529` completed DEC-051's framework-neutral Study lifecycle: immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis with explicit denominators -> deterministic machine-readable evidence export. No final frontend, thesis prose, final thesis figures or PPTX were generated.
- **Current scientific gate: `T-526 BLOCKED`; recovery sub-gate `T-526A BLOCKED` after DEC-053 recovery passed 30/30 but Phase B failed closed at 8/240 on exact SARSA deferred state.** Hosted CI cannot substitute for the retained physical-machine evidence.
- The physical checkout was safely recovered to reviewed source commit `5198dbe077119b7caa4e9a101b55b115a979c22e`. The untracked `temp_body.md` was inspected, confirmed to be an obsolete PR-body draft with no unique durable information and removed. Native Windows Git preflight was clean, and `scripts/run_protocol_v2_feasibility_windows.ps1` executed exactly once.
- The retained Phase-A bundle selected `gw-l1` (7×7) by the predeclared discrimination rule. All 30 declared method/root/layout units completed; no scientific or infrastructure failure, runtime hard-abort or checkpoint warning occurred. The bundle validated against the declared file set, plan hash, source commit, unit matrix, interaction/probe budgets, guardrails and accepted capability snapshot.
- DEC-052 implementation was committed/pushed and both required checks were green at clean reviewed head `5e784d31729ad09c40f2633f3d1682896e624317`. The physical recovery then executed once. Q-Learning and SARSA `t526-r01/gw-l1-a` reproduced exact checkpoint and learner identities. DQN reproduced the authoritative learner-state SHA and serialized byte size, but its checkpoint-envelope SHA was `7b385564...` instead of `f2da03f3...`. The 30/30 barrier failed at 2 exact matches, the infrastructure/recovery failure was retained, and Phase B correctly did not start.
- The SB3 2.9.0 audit proves the raw mismatch is transport/runtime metadata, at minimum the necessarily different `data.start_time`; controlled field-level tests also expose process-address-bearing human-readable class metadata. The historical DQN/PPO learner fingerprint covers all continuation state. DQN `_n_calls`, although not directly hashed, is uniquely fixed at retained `num_timesteps` by the frozen fresh-start/`n_envs=1` step invariant and is asserted explicitly.
- DEC-053 executed from clean reviewed head `167d012a6eb1b0a2a5638836dea73d799128375f`. Recovery independently validates 30/30 accepted states, 12 raw DQN/PPO transport mismatches, exact checkpoint sizes, zero historical learner mismatches and no recovery failure. Phase B completed all eight Q-Learning conditions for the first unit (32 branches, eight prefix and 320 post-boundary interactions), then failed before the first SARSA prefix because the exact checkpoint contains a deferred update. The retained failure is infrastructure/lifecycle, not a scientific method outcome.
- `T-527` is BLOCKED on T-526. Final methods/layouts/budgets/hyperparameters/severities/roots/statistics remain unfrozen.
- `T-528` / #93 is PAUSED/BLOCKED on T-527; its T-529 backend dependency is satisfied. The final frontend must use a framework different from NiceGUI.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution.

## Completed Study-first backend

Current reusable backend/evidence foundation includes:

- immutable content-addressed `StudyRecipe`, evidence classes and frozen-confirmatory firewall;
- deterministic stable-ID job DAG with stage barriers and exact Phase-A producer dependencies;
- durable restart-safe `StudyStore`/`StudyService` with artifact lineage/finalization integrity;
- explicit scientific failure, infrastructure failure and downstream skip semantics;
- real Q-Learning/SARSA/DQN/PPO/Dyna-Q+ Phase-A Study execution and explicit Random supporting reference execution;
- method-native exact scientific checkpoints and fail-closed checkpoint integrity checks;
- one shared no-learning Phase-B prefix and atomic matched FN/FD/AN/AD execution from the exact same branch point;
- structural evidence validation;
- Phase-A interaction-axis learning summaries and root/layout blocked Phase-B matched adaptation effects;
- explicit planned/completed/scientific-failure/skipped/infrastructure-failure/cancelled/pending/running denominators;
- deterministic analysis/export lineage with machine-readable CSV/JSON, stable `RESULT-*` IDs and integrity/provenance manifests;
- default concrete protocol-v2 executor registry behind the framework-neutral StudyService.

The reviewed implementation head had repository-wide `sanity` and dedicated protocol-v2 `focused-conformance` checks green before the documentation closure checkpoint. Documentation-only follow-up CI must remain green before the checkpoint is considered fully reconciled.

## Protocol-v2 invariants

Phase A independently trains each retained method under common semantic task/information/action/reward/gamma semantics and a principal actual-environment-interaction budget, with isolated no-learning probes.

Each Phase-B `method × root × layout` starts from its own exact Phase-A checkpoint. The exact branch point is cloned into FN/FD/AN/AD. Adaptive updates begin only after the boundary; replay, optimizer, exploration, warm-up, model/recency, schedules, counters and RNG state are not silently reset.

Primary adaptation benefit remains matched four-branch DiD. Root/run is the independent unit; layouts/episodes/checkpoints are blocked/repeated observations. Scientific failures remain retained outcomes and seeds are not replaced from outcomes.

## T-526 physical gate

Plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`  
Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`  
Entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`

Historical failed recovery authority/config/entrypoint: `docs/decisions/DEC-052_T526_CHECKPOINT_MATERIALIZATION_AND_PHASE_B.md`, `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.1.json`, `scripts/run_protocol_v2_t526_recovery_phase_b_windows.ps1`.

Current v0.2 authority/config/entrypoint: `docs/decisions/DEC-053_SB3_SCIENTIFIC_CONTINUATION_IDENTITY.md`, `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.2.json`, `scripts/run_protocol_v2_t526_recovery_phase_b_v02_windows.ps1`.

DEC-053 evidence: `results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2/` — valid-complete 30/30, 33 hash-covered files, 4,760,652 bytes, 132.519 seconds. `results/pilots/protocol-v2-feasibility-phase-b-v0.2/` — valid failed attempt, 8/240 matched sets, 32/960 branches, 8 prefix + 320/9,600 post-boundary interactions, one infrastructure failure, 3 hash-covered files, 24,957 bytes, 1.355 seconds.

Failed recovery evidence: `results/pilots/protocol-v2-feasibility-v0.1-recovery/` — 3 attempted payloads, 2 exact matches, 1 retained checkpoint-identity failure, 499,535 hash-covered bytes. The failed-attempt validator passes. No Phase-B output directory exists; matched sets/interactions are 0/240 and 0.

The predeclared one-time first pass evaluated `gw-l1` first and selected it, so the ordered ladder correctly stopped before `gw-l2`/`gw-l3`. The completed matrix contains two layouts, three roots, five core methods, 2048 actual Phase-A training interactions per unit and probes at 0/512/1024/2048.

Recorded physical totals are 61,440 training interactions, 28,524 probe interactions, 129.344 summed unit wall-seconds, 459.469 summed unit process-CPU-seconds and 4,680,026 aggregate serialized checkpoint bytes. The retained five-file artifact bundle is 40,488 bytes. Per-method median unit wall times were Q-Learning 0.169 s, SARSA 0.168 s, Dyna-Q+ 0.363 s, DQN 11.792 s and PPO 8.465 s; maximum serialized checkpoint sizes were 17,225, 17,124, 49,338, 463,739 and 236,224 bytes respectively.

Evidence path: `results/pilots/protocol-v2-feasibility-v0.1/`. Do not rerun, delete, rename, replace or hand-edit it.

## Statistics / provenance

Final statistical values and the contrast family freeze only in T-527. Filesystem evidence remains authoritative and any future index/database must be rebuildable.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography`, immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources and 19 research materials. `bibliography-integration-v3` remains immutable historical terminology.

## Still intentionally unfrozen

Final retained methods/A2C decision, selected GridWorld level/layouts, final budgets/gamma/reward/horizon, method hyperparameters, probe cadence, Phase-B reset lifecycle, uncertainty settings, roots/statistics, confirmatory Study recipe values, final frontend framework and final evidence remain T-526/T-527 gated.

## Exact next action

Obtain a new explicit scientific/lifecycle decision for the exact SARSA deferred-update boundary. Do not rerun/resume v0.2, discard/resolve the update ad hoc, overwrite retained evidence, start T-527/T-528 or access final reserve.
