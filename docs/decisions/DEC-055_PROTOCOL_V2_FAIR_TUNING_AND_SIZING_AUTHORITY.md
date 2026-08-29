# DEC-055 — Protocol-v2 fair tuning and sizing authority

**Status:** accepted pre-outcome authority; physical validation pending  
**Date:** 2026-08-30  
**Task:** T-527  
**Configuration:** `configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json`

## Decision

Freeze one bounded, equal-opportunity non-final development program before any T-527 tuning outcome is generated. The program starts all five feasible core methods, gives each exactly six method-appropriate candidate configurations, and evaluates every candidate on the same three tuning-only roots, the same two selected development layouts, the same 8,192 actual-interaction budget, and the same isolated probe grid.

Configuration selection is mechanical and method-local: maximize the equal-root/equal-layout time-average standardized success curve, then final success, then time-average evaluation return, then the lexicographically smaller declared configuration identity. Seeds are randomization variables and are never tuned. Failed and poor candidates remain evidence.

The common final Phase-A budget is selected from 4,096 and 8,192 using only the already-recorded selected-configuration curves and the rule frozen in the configuration. The selected configuration for each method is then rerun from fresh initialization on 24 distinct sizing-only roots and both development layouts. Sizing evaluates the two already-declared action-remap conditions at 256 and 512 actual post-boundary interactions. Root-count candidates are exactly 12, 16, 20 and 24; the smallest count meeting the declared worst-case Student-t half-width target is selected, otherwise 24 is retained with the precision miss reported.

## Scientific rationale

Equivalent opportunity does not mean identical hyperparameters. Q-Learning/SARSA vary learning rate and exploration, Dyna-Q+ varies planning effort and recency bonus, DQN varies learning rate and target cadence, and PPO varies learning rate and update epochs. These bounded factors are continuation-relevant scientific configuration already identified by the protocol-v2 source audit. No library default is privileged as a winner, but the existing validated implementation/configuration is contained within each bounded set where applicable.

The 8,192-interaction opportunity and 128-aligned probe grid preserve exact PPO rollout/update boundaries while giving every method the same actual environment-interaction resource. The two action-remap conditions are used for sizing because they are the primary adaptation family and were predeclared before T-526 outcomes. Supporting uncertainty outcomes are not used to choose roots or horizon.

## Multi-episode Phase-B lifecycle

The final lifecycle semantics are fixed before sizing outcomes:

- the exact trained learner and all method-native learning state persist across episode resets;
- the branch actual-interaction clock and learner transition clock persist;
- the changed/disturbed regime becomes active at the common boundary and remains active for every later disturbed-branch episode;
- an episode reset changes only episode environment state and consumes the next deterministic predeclared episode seed tuple;
- nominal and disturbed branches use common episode seed schedules where scientifically valid;
- administrative truncation bootstraps under the existing common task semantics;
- no Q/model/replay/optimizer/rollout/exploration/schedule state is reset at an episode boundary;
- no change event is cleared or outcome-dependently retriggered.

The first post-boundary episode continues from the exact common prefix. A later episode uses a fresh environment instance under the same nominal or persistent post-change scenario. For action remapping, persistence means the post-change mapping is active from interaction zero of every later disturbed episode; it is not delayed until the historical within-first-episode onset index.

## Evidence and firewall

All T-526 directories are immutable inputs. T-527 creates new versioned input-diagnostic, tuning, and sizing packages only. The program must execute on the authoritative native Windows host from a clean, pushed PR #92 head after both required checks are green. It cannot read or write a final-reserve path and cannot generate final layouts, final roots, or confirmatory outcomes during tuning/sizing.

The final held-out layouts, exact final root identities, full statistics recipe, retained methods/configurations, conditions, budgets and machine-readable protocol-v2.0 firewall are a later DEC-056 freeze derived only after this declared development evidence validates. DEC-055 does not authorize final-reserve execution, T-528, T-610+, or WP7.

## Rejected alternatives

- selecting configurations from final-reserve outcomes or best seeds;
- unequal candidate counts or adaptive search budgets across methods;
- dropping PPO or Q-Learning from tuning based on provisional T-526 ranking;
- adding A2C or a full Dyna-Q arm;
- using T-526 Phase-B v0.3 outcomes to tune method configurations;
- treating layouts or episodes as independent roots;
- choosing a Phase-B lifecycle after observing sizing performance;
- resetting replay, optimizer, model, recency, exploration or schedule state at deployment episode boundaries.
