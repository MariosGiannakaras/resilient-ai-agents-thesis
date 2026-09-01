# T-526 Phase-A Interaction-Budget Boundary Settlement Audit

**Date:** 2026-08-30
**Scope:** exact Phase-A chronology, SARSA deferred-update semantics, all five retained method boundaries, and the DEC-053 recovery input bundle
**Conclusion:** deterministic zero-environment-interaction settlement is scientifically defensible and required for five retained SARSA states

## Evidence boundary

This audit reads only committed implementation, protocol authority and immutable non-final T-526 evidence. It does not rerun Phase A or recovery, inspect final reserve, resume Phase-B v0.2, or use the eight Q-Learning v0.2 outcomes to choose lifecycle mechanics.

The DEC-053 recovery independently validates as 30/30 accepted scientific continuation states. Its exact checkpoint payloads are immutable input to DEC-054.

## Phase-A chronology

`ProjectTabularPhaseADriver.train_to_interaction(target)` loops only while the project-owned actual-interaction counter is below the absolute target. For each iteration it:

1. calls the persistent learner's `act()` on the current delivered observation;
2. executes exactly one GridWorld environment interaction;
3. projects the resulting transition through the declared information policy;
4. assigns the root-global transition index equal to the pre-increment interaction counter;
5. calls `observe()`;
6. increments the actual-interaction counter exactly once; and
7. starts no further iteration once the target is reached.

At target 2,048, the last observed transition therefore has root-global index 2,047 and `observed_transition_count == 2048`. No extra `act()` is called merely to settle algorithm bookkeeping.

SARSA `observe()` clears the action that produced the transition. For a nonterminal, nontruncated transition it stores `(S, A, R, S')` as one deferred update because exact one-step SARSA requires the next behavior-policy action `A'`. That transition was physically observed and counted even though its backup awaits action selection. This is a legitimate exact continuation state, not missing evidence.

## Phase-B chronology

`prepare_shared_no_learning_prefix()` constructs and resets a new nominal deployment `GridWorldEnvironment` from explicit Phase-B seeds. It does not restore or continue the active Phase-A episode. Before the prefix it requires Q-Learning, SARSA and Dyna-Q+ learners to be quiescent; SARSA may carry neither a pending action nor a deferred backup.

Consequently, selecting `A'` from the fresh deployment reset observation would be methodologically wrong: that observation is not the `S'` belonging to the final consumed Phase-A transition. The bootstrap-only `A'` must not become the first deployment action.

## Existing SARSA precedent

The accepted v2 task contract treats GridWorld time limits as administrative truncation and requires value bootstrap. `SarsaAgent.observe()` already handles a bootstrapped truncation where no next action is executed:

1. use the exact current epsilon-greedy behavior policy and exploration RNG to select an action for the delivered next observation;
2. use its Q value in the one-step on-policy target;
3. apply the update once;
4. discard the selected action instead of storing/executing it.

Focused tests establish exact state equality between this existing path and DEC-054 settlement applied to the same transition represented as a deferred nonterminal boundary. The fixed Phase-A interaction budget is likewise an administrative data-collection boundary, not a terminal MDP transition. Applying the same behavior-policy bootstrap semantics completes learning attributable to the already-consumed interaction without adding an observation or interaction.

## Retained-state audit

All 30 DEC-053 recovery checkpoints were restored and inspected under exact historical learner SHA validation.

| Method | States | Already quiescent | Settlement |
| --- | ---: | ---: | --- |
| Q-Learning | 6 | 6 | no-op; `observe()` completed the final Q backup |
| SARSA | 6 | 1 | five exact behavior-policy bootstrap settlements; one no-op |
| DQN | 6 | 6 | no-op; final transition/replay/update/counter state is complete |
| PPO | 6 | 6 | no-op; all checkpoints are legal completed rollout/update boundaries |
| Dyna-Q+ | 6 | 6 | no-op; direct/model/planning work completed inside final `observe()` |

The five deferred SARSA sources are:

- `t526-r01 / gw-l1-a`: `[1,5]`, `down`, `-0.1`, `[1,6]`;
- `t526-r02 / gw-l1-a`: `[2,6]`, `right`, `-0.1`, `[3,6]`;
- `t526-r01 / gw-l1-b`: `[0,3]`, `down`, `-0.1`, `[0,4]`;
- `t526-r02 / gw-l1-b`: `[0,4]`, `right`, `-0.25`, `[0,4]`;
- `t526-r03 / gw-l1-b`: `[1,0]`, `down`, `-0.1`, `[1,1]`.

All have `pending_action == null`, `observed_transition_count == 2048` and `last_step == 2047`. `t526-r03 / gw-l1-a` is already quiescent and requires no-op settlement.

## Validity conclusion

The settlement is a deterministic derived-state transformation, not an extra Phase-A training interaction, new observation, checkpoint replacement, reset, seed change or Phase-B outcome-dependent choice. It advances only the restored SARSA behavior RNG required by the existing on-policy bootstrap and records the resulting state as a distinct deployment-start identity.

The required lineage is:

`immutable DEC-053 recovery checkpoint -> DEC-054 boundary-settled deployment-start checkpoint -> one common nominal no-learning prefix -> exact FN/FD/AN/AD branch point`.

This narrowly resolves the isolated lifecycle defect without changing the Phase-B matrix or any final protocol choice.
