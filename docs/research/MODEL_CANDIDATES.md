# Agent / Method Candidate Selection

**Status:** Current pre-WP7 method-role authority under DEC-048 / issue #95.  
**Exact final set:** intentionally unfrozen until bounded literature, environment-discrimination and Windows CPU feasibility pilots complete.

GridWorld is the controlled experimental testbed and visualization surface. The thesis subject is the comparison/evaluation of resilient RL agents under uncertainty and environmental change.

## Method is not deployment regime

Protocol v2 separates the learning **method** from post-training **deployment/adaptation regime**.

For every retained method:

1. train independently from method-appropriate fresh initialization;
2. freeze a reproducible method-specific trained checkpoint;
3. clone that exact checkpoint into matched `Frozen` and `Continual` branches;
4. evaluate both under the same uncertainty/change design and same-regime nominal references.

`Frozen Q-Learning` and `Adaptive Q-Learning` remain valid historical/user-facing descriptions for protocol-v1.0/v1.1 contexts. In v2, Q-Learning is the method and Frozen/Continual are deployment regimes.

## Strong core candidates — pilot-gated

| Method | Family | Policy relation | Representation | Distinct scientific role |
|---|---|---|---|---|
| **Q-Learning** | value learning | off-policy | tabular | classical low-complexity value-learning baseline |
| **SARSA** | value learning | on-policy | tabular | isolates on-policy tabular learning/exploration behavior |
| **DQN** | deep value learning | off-policy | neural | adds function approximation, replay and target-network dynamics |
| **PPO** | policy optimization / actor-critic | on-policy | neural | adds policy-gradient/actor-critic optimization with clipped updates |
| **Dyna-Q+** | learned-model planning | Q/value based | tabular + empirical model | adds planning plus recency-directed re-exploration, directly relevant to change |

These five are **candidates**, not a target count. A method reaches the confirmatory matrix only if it adds a useful distinct contrast and passes feasibility/discrimination/fair-tuning gates.

## Secondary candidates / ablations

### Dyna-Q

Retained implementation and scientifically useful ablation:

> Does Dyna-Q+ benefit from planning itself or specifically from directed recency-based re-exploration?

It need not automatically double the full final matrix. Depending on pilot results, it may remain a focused ablation/non-final mechanism comparison while Dyna-Q+ represents planning/change-directed behavior in the main matrix.

### A2C

Technically compatible with discrete actions and CPU execution through maintained RL libraries. It is a valid actor-critic method, but it overlaps substantially with PPO at the family/mechanism level. Promote it to the full final matrix only if literature/pilots show a distinct useful RQ/contrast that justifies the additional tuning, roots and Frozen/Continual runs.

### Historical R0 Robust Planner

Historical robust value iteration remains immutable negative/diagnostic pilot evidence. The accepted pilot suffered severe nominal truncation. Protocol v2 does not require redesigning it. Reopen only if a distinct pre-deployment-robustness RQ is justified before protocol freeze.

## Reference strategies

- **Random Agent:** lower behavioral/correctness reference only; never fair-ranked.
- **Privileged/oracle planner:** optional analytical/debug upper reference only; never fair-ranked if it receives evaluator/model knowledge unavailable to scientific agents.

## Why deep methods are candidates, not automatic winners

DQN/PPO/A2C are technically compatible with the discrete GridWorld action space, but technical compatibility is insufficient scientific justification.

The current 7×7 position-state task may be too small/easy to reveal meaningful representation/optimization differences. Conversely, increasing environment complexity solely to make neural methods look useful would bias the study. Protocol v2 therefore pilots a small number of project-owned complexity levels and keeps the **simplest** one that avoids obvious floor/ceiling effects and remains interpretable/CPU-feasible.

Neural methods receive a deterministic numeric/one-hot encoding of the same semantic observation available to tabular methods. They do not receive pixels, hidden map truth, disturbance flags or extra evaluator information merely because they use a neural network.

## Fair comparison contract

Do **not** force identical hyperparameters across algorithms.

Fairness is instead defined by:

- same environment semantics, action/reward and agent-visible information;
- common main environment-interaction/timestep budget;
- matched environment/root schedules where meaningful;
- bounded literature-backed algorithm-specific configuration candidates;
- equivalent predeclared tuning opportunity and tuning partitions;
- multiple independent roots for every candidate configuration;
- standardized periodic no-learning evaluation checkpoints;
- separate wall-clock/CPU reporting;
- no final-reserve access during tuning/model selection.

Historical Q-learning hyperparameters remain valid for historical v1.0. For v2 they are not treated as an unfair permanent advantage: the v2 tuning policy decides whether the historical Q configuration is one candidate or whether Q receives a bounded fresh tuning allowance equivalent to other methods.

## Continual deployment caveat

`Continual` means ordinary continued learning by the base method under a predeclared update schedule. It does **not** mean the method is a purpose-built continual-learning algorithm.

Deep agents can suffer catastrophic interference/forgetting or loss of plasticity under non-stationarity. These are legitimate findings, not implementation failures to hide through post-hoc resets.

Method-specific scientific checkpoints preserve whatever is required for exact continuation. DQN replay buffer/target network/optimizer/exploration state and actor-critic optimizer/schedule/update-boundary state are therefore part of the deployment contract. Resetting replay/optimizer/network state after change is a separate intervention and must not happen silently.

## Historical candidate-v1.1 status

The former five-strategy v1.1 set — Fixed Q-Learning, Adaptive Q-Learning, SARSA, Dyna-Q, Dyna-Q+ — remains a valid **adaptation-mechanism candidate design** because all agents began from common selected tabular-Q knowledge. It is not deleted or reinterpreted as an independent-learning benchmark.

Old T-522/v1.1 tuning/freeze execution is superseded. Future confirmatory evidence is governed by protocol v2 after its pilot gates.

## Current gate

`T-524` / issue #95 must finish source-backed RQ/estimand/method-role definition before `T-525` implements deep-method adapters. The final method set is frozen only after `T-526` environment/method feasibility pilots and `T-527` fair tuning/statistical/resource review.
