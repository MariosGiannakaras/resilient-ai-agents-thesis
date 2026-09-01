# DEC-052 — T-526 Checkpoint Materialization Recovery and Bounded Phase-B Calibration

**Date:** 2026-08-29
**Status:** Accepted and implemented; one authorized physical recovery attempt failed the exact barrier, so Phase B remains blocked
**Scope:** narrow non-final T-526 recovery and Phase-B feasibility evidence only

## Context

The one-time physical T-526 Phase-A run at source commit `5198dbe077119b7caa4e9a101b55b115a979c22e` is scientifically valid. It selected `gw-l1` through the predeclared discrimination rule, completed all 30 five-method/root/layout units, and recorded exact checkpoint sizes, checkpoint identities and learner-state identities without a scientific or infrastructure failure.

The runner created complete scientific checkpoint payloads in memory but retained only their sizes and cryptographic identities. That is an implementation/evidence-handoff defect discovered after the valid run. The immutable Phase-A bundle consequently cannot directly supply the exact trained states required by DEC-048/050 Phase B.

## Decision

### 1. Original Phase-A authority is unchanged

The five files under `results/pilots/protocol-v2-feasibility-v0.1/` remain authoritative and byte-for-byte immutable. Their environment-selection and method-feasibility conclusions are retained. No Phase-A outcome, root, seed, probe, method, hyperparameter, environment level or evidence field may be changed.

The recovery does not rerun the GridWorld ladder, does not evaluate `gw-l2` or `gw-l3`, and does not create replacement Phase-A observations.

### 2. Deterministic payload materialization is permitted narrowly

Only the already-selected `gw-l1` 30 units may be recomputed, using the exact original plan, roots, all seed streams, method configurations, interaction budget, probe schedule/seeds, implementation semantics and checkpoint provenance.

Before recovery, every Phase-A-affecting implementation/configuration/dependency-lock path declared in `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.1.json` must have no Git diff from the original source commit. The original evidence files must match their predeclared SHA-256 values.

For every unit, all pre-existing scientifically deterministic row fields must match exactly, including the complete probe record, checkpoint byte size and both state identities. In particular:

`reconstructed checkpoint SHA-256 == authoritative checkpoint_sha256`

`reconstructed learner-state SHA-256 == authoritative learner_state_sha256`

There is no numerical tolerance. A single mismatch is a recovery/infrastructure failure, is retained diagnostically, and blocks Phase B. Seeds/configuration may not be changed to obtain a match. Reconstructed payloads are eligible for Phase B only after the complete 30/30 barrier passes.

### 3. Recovery evidence is separate

Checkpoint payloads and recovery diagnostics are written only to `results/pilots/protocol-v2-feasibility-v0.1-recovery/`. Every payload is hash-covered and linked to the original source commit, plan, immutable evidence hashes, expected checkpoint identity and expected learner identity. This materialization evidence cannot replace or alter the original Phase-A evidence.

### 4. T-526 pilot-only Phase-B lifecycle is frozen before execution

Phase B uses exactly the selected `gw-l1`, five core methods, three existing roots, two existing layouts and eight conditions already declared in the original plan:

- categorical action remaps `swap-right-down` and `cycle-clockwise`;
- action-failure probabilities `0.05`, `0.15`, `0.30`;
- observation-corruption probabilities `0.02`, `0.05`, `0.10` with the declared global valid-cell support excluding true state.

Each matched set uses one nominal no-learning prefix interaction, then exact FN/FD/AN/AD forks and ten actual post-boundary interactions per branch with no episode reset. Both layouts have shortest-path length 12, and `1 + 10 = 11 < 12`; none of the declared disturbances can shorten the physical graph path. Terminal/reset ambiguity is therefore excluded by construction.

This `1/10` lifecycle is T-526 calibration-only. It does not freeze final protocol-v2 lifecycle or budgets; T-527 retains that authority.

### 5. Matched execution and stochastic fairness

All 240 method/root/layout/condition matched sets consume their exact verified checkpoint. Each condition for one method/root/layout begins from the same nominal prefix seed/state, not a condition-specific prefix. The four learner forks are identical at the branch point and nominal/disturbed environments are identical before the first post-boundary transition except for the declared future disturbance mechanism.

Adaptive learning begins at the first post-boundary transition. No exploration, optimizer, replay, target-network, model, recency, schedule, warm-up counter or RNG state is reset. Within stochastic families, identical restored disturbance RNG state provides common-random-number semantics across probabilities.

PPO's predeclared native rollout/update quantum is 128 interactions. In this ten-interaction pilot segment Adaptive PPO begins method-native rollout collection at interaction one but cannot complete an optimizer update. Its exact transient rollout state is hash-retained as feasibility evidence and is not represented as a legal restorable scientific checkpoint. This does not alter the original checkpoint adapter or Phase-A implementation.

### 6. Evidence and interpretation

Phase-B evidence is written separately under `results/pilots/protocol-v2-feasibility-phase-b-v0.1/` and retains amendment/config/checkpoint lineage, branch-point identities, exact branch assignments/interactions, final state identities, returns, exposed disturbance occurrence counters, runtimes, failures, artifact sizes and complete denominators.

All eight candidates are executed and retained. T-526 does not select final probabilities or a preferred remap, does not manufacture a scalar remap severity, and does not rank/select candidates by method outcomes. T-527 later owns final bounded severity/lifecycle/statistical decisions.

No A2C or additional Dyna-Q arm is added. No final reserve is accessed.

## Supersession boundary

This decision supersedes only the narrow T-526 one-time wording that unintentionally prevented deterministic materialization of already-identified checkpoint payloads. It does not weaken prohibitions on replacing scientific failures, changing roots/seeds/methods/candidates, outcome-driven tuning, mutating original/final evidence, or starting T-527 before T-526 completes.

## Physical result

The reviewed implementation head `5e784d31729ad09c40f2633f3d1682896e624317` passed both required PR checks and executed once on the physical Windows thesis machine. The immutable original hashes and Phase-A source-compatibility gate passed. Q-Learning and SARSA for the first root/layout exactly reproduced both identities. DQN reproduced its authoritative learner-state identity and canonical checkpoint byte size, but its checkpoint-envelope identity differed (`7b385564...` reconstructed versus `f2da03f3...` authoritative).

DEC-052 requires both identities with no tolerance. The runner therefore retained the mismatch as recovery/infrastructure evidence, stopped at 2/30 exact matches and did not start Phase B. This matching learner fingerprint does not satisfy or relax the checkpoint-envelope requirement. No retry or new amendment is authorized by this decision.
