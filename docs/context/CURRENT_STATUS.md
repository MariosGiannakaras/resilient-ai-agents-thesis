# Current Project Status

**Date:** 2026-08-30
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use **progressive** task-specific reading of DEC-048/049/050/051/052/053 and `docs/research/` / `docs/architecture/` only as needed.

## Current execution state

- Historical baseline includes completed `T-100` target-machine validation and `T-200` research framing through protocol-v1.0 WP6 evidence. Protocol-v1.0, FINAL-* and R0 evidence remain immutable. Candidate v1.1 is non-final history; old `T-522` must not execute.
- `T-524`, `T-525` and `T-529` are COMPLETE.
- `T-529` completed DEC-051's framework-neutral Study lifecycle from immutable recipe through real execution, validation, root/layout analysis and deterministic evidence export. It generated no final frontend or thesis/defense material.
- **Current scientific gate: `T-527` IN_PROGRESS under reviewed-pending DEC-056 correction authority; `T-526A` and `T-526` remain COMPLETE.** DEC-055 tuning is immutable valid-complete and sizing-v0.1 is immutable valid-failed. DEC-056 authorizes no tuning rerun and exactly one fresh sizing-only v0.2 attempt after review/green CI.
- The retained Phase-A bundle selected `gw-l1` (7×7) by the predeclared rule. All 30 method/root/layout units completed without scientific/infrastructure failure, runtime hard-abort or checkpoint warning. The bundle validated its files, plan/source hashes, unit matrix, budgets, guardrails and capability snapshot.
- DEC-052 failed closed at 2/30 on a raw DQN envelope mismatch. The SB3 2.9.0 audit proved runtime/transport metadata (`data.start_time` and display-only class metadata) differed while the complete historical continuation state matched.
- DEC-053 recovery validated 30/30 states with 12 retained SB3 transport mismatches and no learner mismatch/failure. Its Phase B stopped fail-closed at 8/240 before SARSA's first prefix because the exact checkpoint retained a deferred update.
- The DEC-054 audit proves the fixed Phase-A interaction target stops after the final counted `observe()` with no extra `act()`. Five SARSA sources retain one valid deferred on-policy backup for interaction 2,048; 25 states are already quiescent. The existing bootstrapped-truncation path provides the exact behavior-policy/bootstrap-only action precedent. Settlement derives a separate deployment-start state with zero environment interactions and cannot use the fresh Phase-B observation.
- DEC-054 physical validation accepted 30/30 quiescent deployment-start states: five SARSA states were deterministically settled with exact restored behavior-policy RNG and 25 states were no-ops. Settlement consumed zero environment interactions. Fresh Phase-B v0.3 completed 240/240 matched sets, 960 branches, 240 one-interaction common prefixes and 9,600 post-boundary interactions with zero scientific/infrastructure failures; independent validators pass.
- DEC-055 remains valid history. Its tuning stage completed 180/180 and mechanically selected `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06`, `dyna-c03` and the 8,192-interaction budget. Sizing retained 97/240 Phase-A units and 192/480 matched sets before one infrastructure failure. DEC-056 now fixes only the SB3 tuple-to-declared-MultiDiscrete-array facade and the missing enforcement of DEC-055's native-update horizon criterion, then authorizes one fresh 240-unit/480-set sizing-only v0.2 attempt. Final values remain unfrozen pending that physical validation.
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

Completed DEC-054 authority/config/entrypoint: `docs/decisions/DEC-054_PHASE_A_INTERACTION_BUDGET_SETTLEMENT.md`, `configs/protocols/protocol-v2-t526-boundary-settlement-phase-b-v0.3.json`, `scripts/run_protocol_v2_t526_boundary_settlement_phase_b_v03_windows.ps1`.

DEC-054 evidence: `results/pilots/protocol-v2-feasibility-boundary-settlement-v0.1/` — valid-complete 30/30, five non-no-op SARSA states, zero environment interactions/failures, 33 hash-covered files, 4,755,471 bytes, 21.289 seconds. `results/pilots/protocol-v2-feasibility-phase-b-v0.3/` — valid-complete 240/240, 960 branches, 240 prefix + 9,600 post-boundary interactions, zero scientific/infrastructure failures, four hash-covered files, 803,558 bytes, 223.710 seconds.

DEC-053 evidence: `results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2/` — valid-complete 30/30, 33 hash-covered files, 4,760,652 bytes, 132.519 seconds. `results/pilots/protocol-v2-feasibility-phase-b-v0.2/` — valid failed attempt, 8/240 matched sets, 32/960 branches, 8 prefix + 320/9,600 post-boundary interactions, one infrastructure failure, 3 hash-covered files, 24,957 bytes, 1.355 seconds.

Failed recovery evidence: `results/pilots/protocol-v2-feasibility-v0.1-recovery/` — 3 attempted payloads, 2 exact matches, 1 retained checkpoint-identity failure, 499,535 hash-covered bytes. The failed-attempt validator passes. No Phase-B output directory exists; matched sets/interactions are 0/240 and 0.

The predeclared one-time first pass evaluated `gw-l1` first and selected it, so the ordered ladder correctly stopped before `gw-l2`/`gw-l3`. The completed matrix contains two layouts, three roots, five core methods, 2048 actual Phase-A training interactions per unit and probes at 0/512/1024/2048.

Recorded physical totals are 61,440 training interactions, 28,524 probe interactions, 129.344 summed unit wall-seconds, 459.469 summed unit process-CPU-seconds and 4,680,026 aggregate serialized checkpoint bytes. The retained five-file artifact bundle is 40,488 bytes. Per-method median unit wall times were Q-Learning 0.169 s, SARSA 0.168 s, Dyna-Q+ 0.363 s, DQN 11.792 s and PPO 8.465 s; maximum serialized checkpoint sizes were 17,225, 17,124, 49,338, 463,739 and 236,224 bytes respectively.

Evidence path: `results/pilots/protocol-v2-feasibility-v0.1/`. Do not rerun, delete, rename, replace or hand-edit it.

## Statistics / provenance

Final statistical values and the contrast family freeze only in T-527. Filesystem evidence remains authoritative and any future index/database must be rebuildable.

DEC-055 authority/config/runbook/entrypoint: `docs/decisions/DEC-055_PROTOCOL_V2_FAIR_TUNING_AND_SIZING_AUTHORITY.md`, `configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json`, `docs/research/T527_WINDOWS_TUNING_SIZING_RUNBOOK.md`, `scripts/run_protocol_v2_t527_tuning_sizing_windows.ps1`. The deterministic input package is `results/pilots/protocol-v2-t527-input-diagnostics-v0.1/`. The tuning package `results/pilots/protocol-v2-t527-tuning-v0.1/` is valid-complete at 180/180 (4 hash-covered files, 287,709 bytes). The sizing package `results/pilots/protocol-v2-t527-sizing-v0.1/` is valid-failed at 97/240 Phase-A units and 192/480 matched sets (101 hash-covered files, 3,911,282 bytes), with one infrastructure failure and zero hash mismatches.

DEC-056 authority/config/entrypoint: `docs/decisions/DEC-056_T527_SIZING_OBSERVATION_BOUNDARY_RETRY.md`, `configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json`, `scripts/run_protocol_v2_t527_sizing_v02_windows.ps1`. The reviewed commit, green checks and clean native-Windows worktree are mandatory before the one sizing-only execution. Expected new evidence is `results/pilots/protocol-v2-t527-sizing-v0.2/`; it must start at unit one and cannot reuse v0.1 rows/checkpoints.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography`, immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources and 19 research materials. `bibliography-integration-v3` remains immutable historical terminology.

## Still intentionally unfrozen

Final retained methods/A2C decision, final layout set, budgets/gamma/reward/horizon, method hyperparameters, probe cadence, Phase-B reset lifecycle, uncertainty settings, roots/statistics, confirmatory Study recipe values, final frontend framework and final evidence remain T-527 gated.

## Exact next action

Complete DEC-056 focused validation, commit/push the pre-run authority, require both current-head checks green and a clean exact native-Windows head, then execute `scripts/run_protocol_v2_t527_sizing_v02_windows.ps1` exactly once. Do not rerun tuning, resume/copy sizing-v0.1, access final reserve or start T-528. Keep #95 at 7/10 until a complete protocol-v2.0 freeze.
