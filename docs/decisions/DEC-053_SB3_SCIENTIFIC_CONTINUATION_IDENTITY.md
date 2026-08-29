# DEC-053 — SB3 Scientific-Continuation Identity for T-526 Recovery

**Date:** 2026-08-29
**Status:** Accepted and implemented; physical validation pending
**Scope:** narrow correction to SB3 identity semantics for a single versioned T-526A recovery attempt

## Context

DEC-052 remains a valid historical decision. Its reviewed physical attempt correctly failed closed when the reconstructed DQN checkpoint-envelope SHA differed from the authoritative Phase-A SHA, even though the authoritative learner-state SHA and checkpoint byte size matched. The original Phase-A and failed recovery evidence remain immutable.

The subsequent audit in `docs/research/T526_SB3_SCIENTIFIC_CONTINUATION_IDENTITY_AUDIT.md` establishes that SB3 2.9.0 raw archives include persistence metadata outside scientific learner state. In particular, `BaseAlgorithm.start_time` is serialized into the `data` member even though it affects only runtime/FPS logging. The original and recovery runs necessarily have different values. SB3's JSON also adds process-address-bearing human-readable class metadata that is ignored on restore. Canonical ZIP wrapping does not remove either category.

The audit separately proves the historical DQN/PPO learner fingerprint coverage against SB3 2.9.0 source and focused perturbation/restore tests. DQN `_n_calls` is not a direct historical field, but is uniquely and independently established as equal to retained `num_timesteps` under the frozen fresh-start, `n_envs=1`, one-`_on_step`-per-environment-step path. PPO checkpoints occur only at a completed rollout/update boundary, where consumed rollout contents are reset before the next collection. No continuation-relevant state remains unknown.

## Decision

### 1. Preserve both historical decisions and evidence trees

DEC-052 is not rewritten or reclassified. Its 2/30 failure remains valid under its declared raw-envelope rule. The original Phase-A evidence and `results/pilots/protocol-v2-feasibility-v0.1-recovery/` remain byte-exact, immutable history.

### 2. Distinguish transport identity from scientific continuation identity

For SB3 DQN/PPO, raw serialized checkpoint-envelope identity is retained as transport/audit evidence but is not a valid equality requirement for independently generated archives. Nonidentical raw archives must never be described as byte-identical.

The physically recorded historical `learner_state_sha256` remains mandatory and exact. A reconstructed SB3 state is accepted only when all of these pass:

- exact method/root/layout and selected `gw-l1` identity;
- exact frozen Phase-A implementation, dependency lock and method configuration;
- exact 2,048 training interactions and original probe accounting/results;
- exact authoritative historical learner-state SHA;
- successful project-adapter restore;
- exact post-restore and clone/round-trip historical learner-state SHA;
- exact online/policy/value, target, optimizer, replay and RNG state covered by that SHA;
- exact relevant counters and schedule state, including the independently derived DQN `_n_calls == num_timesteps` invariant;
- standard DQN replay operational mode and no normalization/SDE state outside the declared configuration;
- exact scientific provenance and final-reserve firewall.

`scientific_continuation_sha256` is a clearly labeled DEC-053 derived round-trip audit identity. It was not physically recorded during Phase A and cannot replace the historical learner SHA. It adds explicit schedule, DQN target-update/replay-operational and PPO-boundary invariants to the reconstructed-state audit.

Both original and reconstructed raw checkpoint-envelope SHAs and byte sizes are retained per unit.

### 3. Keep the stronger native-method rule

Q-Learning, SARSA and Dyna-Q+ retain DEC-052's exact canonical checkpoint-envelope SHA/size and learner-state SHA requirements. Their deterministic project serialization is meaningful and is not weakened because SB3 uses a different transport format.

### 4. Authorize one versioned physical v0.2 attempt

The only authorized new attempt uses:

- `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.2.json`;
- `src/resilient_agents/protocol_v2_t526_recovery_v02.py`;
- `scripts/run_protocol_v2_t526_recovery_phase_b_v02_windows.ps1`;
- `results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2/`; and
- if and only if recovery reaches 30/30, `results/pilots/protocol-v2-feasibility-phase-b-v0.2/`.

The attempt starts from unit one and reconstructs all 30 selected states. It cannot resume DEC-052 at unit three. One scientific-identity failure stops the attempt, is retained, blocks Phase B and authorizes no further relaxation or retry.

### 5. Phase B is unchanged and conditional on 30/30

Only 30/30 accepted scientific continuation states unlock the already-predeclared T-526 Phase-B matrix: selected `gw-l1`; five core methods; three roots; two layouts; eight existing disturbance conditions; one nominal no-learning prefix interaction; exact FN/FD/AN/AD branches; ten actual interactions per branch; no reset; 240 matched sets, 960 branches and 9,600 post-boundary interactions. Adaptive learning starts only after the boundary, Frozen learners cannot mutate, failures are retained and no A2C/final reserve/final protocol choice is introduced.

T-527 retains all final freeze authority.

## Non-outcome-driven basis

This is a serialization-semantics correction established without observing a new scientific outcome. The distinction would apply to any SB3 archive with runtime metadata, regardless of method performance or whether Phase B later succeeds. It does not change seeds, roots, methods, budgets, environments, probes, candidates or outcome interpretation.

## Stop conditions

Before execution, the DEC-053 implementation/configuration/tests/docs must be committed and pushed, both required PR checks must be green on that exact commit, PR #92 must point to it, and the native Windows worktree must be clean. The v0.2 entrypoint may execute exactly once only after those gates.
