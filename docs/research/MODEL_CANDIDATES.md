# Agent / Method Selection

**Status:** Final retained method set frozen by DEC-058 and preserved by DEC-060.  
**Current protocol authority:** `configs/protocols/protocol-v2.1-final.json`

GridWorld is the controlled experimental testbed and visualization surface. The thesis subject is the comparison/evaluation of resilient reinforcement-learning agents under uncertainty and environmental change.

## Final retained methods

| Method | Family | Policy relation | Representation | Scientific role |
|---|---|---|---|---|
| **Q-Learning** | value learning | off-policy | tabular | classical low-complexity value-learning baseline |
| **SARSA** | value learning | on-policy | tabular | on-policy tabular contrast |
| **DQN** | deep value learning | off-policy | neural | function approximation, replay and target-network dynamics |
| **PPO** | policy optimization / actor-critic | on-policy | neural | policy-gradient/actor-critic optimization with clipped updates |
| **Dyna-Q+** | learned-model planning | Q/value based | tabular + empirical model | planning plus recency-directed re-exploration under change |

The confirmatory set is exactly these five methods. It is no longer provisional.

## Frozen selected configurations

- Q-Learning: `q-c06`
- SARSA: `sarsa-c06`
- DQN: `dqn-c05`
- PPO: `ppo-c06`
- Dyna-Q+: `dyna-c03`

Their complete parameters and implementation identifiers are defined only by `configs/protocols/protocol-v2.1-final.json`; this document does not duplicate mutable parameter values.

## Method is not deployment regime

Protocol v2.x separates learning method from post-training deployment/adaptation regime.

For every retained method:

1. train independently from method-appropriate initialization;
2. retain an exact method-specific scientific checkpoint;
3. create matched `FN`, `FD`, `AN`, `AD` branches from one exact branch point;
4. keep Frozen branches non-learning and Adaptive branches on ordinary method-native continuation;
5. preserve replay, optimizer, exploration, rollout/update, planning/model and RNG state required for exact continuation.

Frozen and Adaptive/Continual are regimes, not additional algorithms.

## Fair comparison contract

Fairness does **not** mean identical hyperparameters or identical optimizer/planning update counts across algorithms.

The frozen comparison instead requires:

- same controlled task/reward/action semantics;
- same agent-visible information contract;
- common primary actual-environment-interaction budget;
- independent Phase-A learning for every method;
- method-appropriate configurations selected through the completed bounded tuning process;
- exact no-learning probes at the frozen checkpoints;
- common final roots/layouts and matched Phase-B branch origins;
- root as the independent unit, with layouts blocked/equally reduced within root;
- scientific failures retained and no outcome-driven root/seed replacement;
- no final-reserve access during selection/tuning.

Neural methods receive a deterministic numeric encoding of the same semantic position observation. They receive no pixels, hidden map truth, disturbance flags, change indicator, regime identity, or executed-action feedback unavailable to tabular methods.

## Secondary/historical methods

### Dyna-Q

Dyna-Q remains a useful historical/mechanistic ablation for distinguishing planning from Dyna-Q+'s recency-directed re-exploration. It is not part of the final five-method confirmatory matrix.

### A2C

A2C remains a technically plausible actor-critic candidate from earlier design work but was not retained for the final matrix. It must not be introduced into T-610 without a new explicit pre-outcome protocol amendment.

### Historical R0 robust planner

The robust value-iteration path remains immutable historical negative/diagnostic evidence. It is not part of the protocol-v2.1 confirmatory matrix and is not to be redesigned opportunistically after final outcomes.

### References/oracles

Random or privileged/oracle strategies may remain calibration/debug references where already defined, but they are not fair-ranked members of the five-method confirmatory comparison if they receive different information or model access.

## Continual deployment caveat

Adaptive/Continual means ordinary continued learning by the retained base method under its frozen method-native semantics. It does not imply a purpose-built continual-learning algorithm.

Potential interference, forgetting, loss of plasticity, replay effects, policy instability or planning-model behavior under non-stationarity are legitimate empirical outcomes. They must not be hidden with post-change resets or special interventions not frozen in the protocol.

## Historical candidate-v1.1 status

The former v1.1 strategy set and old T-522 tuning/freeze path remain valid historical context only. Historical T-530/T-531/T-532 application/prototype tasks likewise retain their original meanings. They do not override DEC-058/DEC-060 or the five-method independent-learning protocol.

## Current gate

T-533 may implement/validate protocol-v2.1 recovery and direct-comparison evidence mechanics without touching final outcomes. The method set itself is closed. `final_reserve_access=false` remains sealed until a separate explicit T-610 authorization.
