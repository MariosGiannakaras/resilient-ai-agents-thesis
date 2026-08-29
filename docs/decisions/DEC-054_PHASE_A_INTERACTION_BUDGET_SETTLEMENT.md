# DEC-054 — Phase-A Interaction-Budget Settlement for Exact Deployment Start

**Date:** 2026-08-30
**Status:** Accepted, implemented and physically validated
**Scope:** T-526 boundary settlement and one fresh versioned Phase-B v0.3 attempt only

## Context

Original Phase A, failed DEC-052 recovery, successful DEC-053 recovery v0.2 and failed DEC-053 Phase-B v0.2 remain immutable. DEC-053 recovery provides 30/30 exact accepted scientific continuation states. Phase-B v0.2 failed closed because the first encountered SARSA source retained the on-policy backup for its final already-consumed Phase-A transition.

The lifecycle audit in `docs/research/T526_PHASE_A_BOUNDARY_SETTLEMENT_AUDIT.md` proves that the project Phase-A driver stops exactly after the 2,048th actual interaction and deliberately makes no extra `act()` call. SARSA therefore may retain one nonterminal transition whose backup requires selection of `A'` under the continuing behavior policy. The fresh Phase-B environment cannot supply that `A'` because it is not continuation of the Phase-A episode.

The implementation already resolves the equivalent administrative-truncation case by selecting a bootstrap-only action under the exact behavior policy, applying the one-step backup, and discarding the action without environment execution. The fixed Phase-A interaction budget uses the same accepted task-boundary semantics.

## Decision

### 1. Preserve three distinct scientific identities

1. **Historical Phase-A checkpoint:** immutable state physically recorded/reconstructed and accepted by DEC-053.
2. **Boundary-settled deployment-start state:** deterministic derived learner state after completing only algorithmic work attributable to the final already-counted Phase-A transition.
3. **Phase-B branch-point state:** exact learner/environment state after the frozen one-interaction common nominal no-learning prefix.

A settled SARSA state that changes Q/RNG state is never described as byte-identical to its source. Both identities and explicit lineage are retained.

### 2. Method-aware settlement is mandatory

- Q-Learning: require exact counters and no pending action; settlement is a no-op.
- SARSA: require exact counters, no pending action and at most one schema-valid deferred update. A quiescent source is a no-op. A valid deferred source uses the rule below.
- DQN: require the accepted DEC-053 scientific-continuation invariants and exact 2,048-interaction counter; settlement is a no-op.
- PPO: require the accepted DEC-053 legal completed rollout/update boundary and exact counter; settlement is a no-op.
- Dyna-Q+: require exact counters/time and no pending action; direct/model/planning work is already complete, so settlement is a no-op.

Unknown, inconsistent or additional unfinished state fails closed. No orchestrator may silently invent a method-specific repair.

### 3. Exact SARSA rule

For one valid deferred nonterminal update `(S, A, R, S')`:

1. restore the exact accepted DEC-053 checkpoint and verify historical learner SHA, method/root/layout/configuration and 2,048-interaction provenance;
2. require `pending_action is None`, one valid deferred update, valid `S'`, `observed_transition_count == 2048` and `last_step == 2047`;
3. use the exact restored Phase-A Q values, epsilon, declared action ordering and exploration RNG state to select `A'` under the existing epsilon-greedy behavior policy;
4. apply exactly `Q(S,A) <- Q(S,A) + alpha * [R + gamma * Q(S',A') - Q(S,A)]` once;
5. clear the deferred update and retain the correctly advanced exploration RNG;
6. retain no pending deployment action and never execute the bootstrap-only `A'`;
7. consume zero environment interactions and leave observed-transition count/last step unchanged.

Greedy substitution, Expected SARSA, fresh RNG, evaluator information, Phase-B observation/state or manually chosen action are prohibited.

### 4. Settlement evidence and barrier

The single authorized settlement attempt writes only to:

`results/pilots/protocol-v2-feasibility-boundary-settlement-v0.1/`

Each of all 30 rows retains source recovery path/file/raw/learner identity, policy/no-op status, pre/post learner SHA and counters, zero-interaction accounting, exact SARSA calculation/RNG provenance when applicable, quiescence, deterministic replay, round-trip restore and a separate derived deployment-start checkpoint.

Phase B cannot start unless all 30/30 rows validate, failures are empty, source evidence remains immutable and every deployment-start state is quiescent.

### 5. One fresh Phase-B v0.3 attempt

After the reviewed authority gate passes, one fresh attempt starts from matched set one and writes only to:

`results/pilots/protocol-v2-feasibility-phase-b-v0.3/`

No v0.2 row is copied or combined. The frozen design remains exactly `gw-l1`, five core methods, three roots, two layouts, eight conditions, one common nominal no-learning prefix interaction, FN/FD/AN/AD, ten post-boundary interactions per branch and no episode reset: 240 matched sets, 960 branches, 240 prefix interactions and 9,600 post-boundary interactions.

Adaptive learning begins only on the first post-boundary transition. Frozen learning state cannot mutate. All condition instances for the same method/root/layout must reproduce the exact same branch-point learner/environment identities.

## Authority and stop conditions

Configuration: `configs/protocols/protocol-v2-t526-boundary-settlement-phase-b-v0.3.json`
Implementation: `src/resilient_agents/protocol_v2_boundary_settlement.py` and `src/resilient_agents/protocol_v2_t526_boundary_phase_b_v03.py`
Windows entrypoint: `scripts/run_protocol_v2_t526_boundary_settlement_phase_b_v03_windows.ps1`

Before execution, these files, focused tests and canonical reconciliation must be committed/pushed; both required PR #92 checks must be green on the exact current head; PR #92 must point to it; and native Windows Git must be clean.

The entrypoint validates original Phase A, DEC-052, DEC-053 recovery v0.2 and DEC-053 failed Phase-B v0.2 before writing. It does not execute Phase A or either recovery.

Any settlement or Phase-B failure is retained and authorizes no rerun, resume, seed replacement or post-outcome lifecycle change. No final reserve, A2C promotion, T-527 execution, UI work or final experiment is authorized by this decision.

## Physical validation result

The pre-run authority commit was `14002a47763991234a1d0623f27330a895f348f0`. PR #92 pointed to that exact head, both required checks were green and native Windows Git was clean before execution.

- Immutable original Phase A, DEC-052, DEC-053 recovery v0.2 and failed Phase-B v0.2 integrity/lineage validation passed.
- Settlement accepted 30/30 states: 25 no-ops and five non-no-op SARSA settlements. Each non-no-op retained exact pre/post learner identities, behavior-policy bootstrap action/RNG provenance, unchanged 2,048/2,047 counters and zero environment interactions. Deterministic replay, quiescence and round-trip restore passed.
- Fresh Phase-B v0.3 completed 240/240 matched sets, 960 branches, 240 prefix interactions and 9,600 post-boundary interactions with zero scientific and infrastructure failures.
- Settlement evidence contains 33 hash-covered files and 4,755,471 bytes; Phase-B evidence contains four hash-covered files and 803,558 bytes. Scientific wall times were 21.289 and 223.710 seconds respectively.
- No original/recovery/v0.2 evidence was modified, no final reserve was accessed and T-527 was not started.

The validated evidence is immutable at `results/pilots/protocol-v2-feasibility-boundary-settlement-v0.1/` and `results/pilots/protocol-v2-feasibility-phase-b-v0.3/`. T-526A and T-526 are complete; T-527 becomes ready.

## Non-outcome-driven basis

The rule follows from the already-frozen actual-interaction budget, administrative-boundary bootstrap and exact SARSA behavior-policy semantics. It would be required for any deferred final-budget SARSA transition regardless of Phase-B performance. The eight retained Q-Learning v0.2 outcomes were not used.
