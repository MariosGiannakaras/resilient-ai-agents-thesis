# Agent and Model Role Selection

**Status:** `T-310`/`T-311` selection/evidence and `T-312` correctness implementation are complete. Exact hyperparameters/budgets and final post-pilot freeze remain open.

## Selection outcome

The smallest set that answers the retained provisional RQs uses two implementations in three declared capability regimes:

| ID | Exact method / regime | Scientific role | Inclusion |
|---|---|---|---|
| F0 | `tabular_q_learning_v1` loaded from the common nominal checkpoint, action selection active, Q updates disabled | Frozen nominal resistance reference | **RETAIN** |
| C0 | The same `tabular_q_learning_v1` checkpoint and action-selection schedule, Q updates continued through the persistent change | Naive model-free online adaptation baseline | **RETAIN** |
| R0 | `rectangular_robust_value_iteration_v1`, planned before deployment over an explicit finite s,a-rectangular transition uncertainty set, then frozen | Declared-set robustness and nominal-conservativeness comparator | **RETAIN** |

F0 and C0 are separate evaluation regimes of one implementation, not inflated algorithm count. Their identical nominal checkpoint, action-selection schedule, exploration RNG policy, and agent-visible information isolate the effect of permitting post-change updates. R0 is intentionally a different information regime: its model and uncertainty family are declared prior knowledge and must be reported as such.

This is the implementation/pilot set, not a promise that every role survives final protocol freeze. A role is removed if correctness, assumption fit, fairness, repeated-run feasibility, or distinct empirical behavior fails the later gates.

## Exact algorithm identities

### F0/C0 — tabular Q-learning

Use the standard off-policy one-step update for delivered state/observation `s`, intended action `a`, reward `r`, and next delivered observation `s'`:

`Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') − Q(s,a)]`

Terminal/truncated episode handling, learning rate, discount, initialization, exploration schedule, tie breaking, budgets, and checkpoint lifecycle are explicit configuration with no library defaults. F0 and C0 start shifted evaluation from the same serialized nominal Q table. F0 suppresses all learning-state mutation; C0 applies the same update continuously. Both receive only the accepted `AgentTransition` projection and never true state, executed action, regime ID, disturbance flags, or changepoint truth under the strict policy.

Citation-ready `SRC-D52DF7B9A4` supports Q-learning's tabular off-policy update and stationary convergence boundary. Citation-ready `SRC-70772C0629` prevents the false claim that ordinary Q-learning is universally incapable under all non-stationarity, while also showing that structured long-run switching convergence does not predict rapid recovery after this thesis's single persistent change.

### R0 — finite rectangular robust value iteration

For each observable state/action pair, configure a non-empty finite set of explicit candidate next-state probability rows. Its convex hull is the local s,a-rectangular uncertainty set. Because the robust Bellman objective is linear in the row, the inner minimum is evaluated over the declared extreme rows:

`Q_R(s,a) = min_{p ∈ U(s,a)} Σ_s' p(s') [r(s,a,s') + γ V_R(s')]`

and `V_R(s) = max_a Q_R(s,a)` until the explicit convergence rule or iteration limit. Goal states are terminal. The uncertainty-set construction, candidate kernels, whether the realized post-change kernel is in-set, discount, convergence tolerance, iteration cap, model source, and planning cost are recorded. R0 is frozen during evaluation and receives no true active kernel or changepoint signal.

Citation-ready `SRC-52E62452B8` is sufficient formal support for rectangular transition uncertainty and robust Bellman dynamic programming. It explicitly distinguishes stationary/time-varying uncertainty and warns that broad sets can be overly conservative. Citation-ready `SRC-FC42D9798A` supports the robustness-versus-online-adaptation conceptual boundary but is not used to claim a need for function approximation. Citation-ready `SRC-3C0F7CC819` supports tabular robust-RL feasibility but does not establish changepoint detection or faster recovery. No further upstream bibliography promotion is required for the retained bounded claims, satisfying `T-311`.

## RQ and metric mapping

| Contrast | Capability isolated | Required schema-v1 evidence |
|---|---|---|
| F0 vs C0 | Benefit/cost of ordinary continued updating from the same nominal knowledge | nominal performance, immediate/worst degradation, recovery status/delay, terminal gap, cumulative deficit |
| F0 vs R0 | Declared-set pre-deployment robustness and conservativeness versus nominal training | nominal performance/gap, immediate/worst degradation, terminal gap, in-set/out-of-set label |
| C0 vs R0 | Online sample-driven adaptation versus stronger-prior frozen robustness | full post-change curves and all component estimands; no unqualified universal ranking |

Observation corruption and action failure reuse these roles as supporting robustness diagnostics. No extra observation/action-robust algorithm is added merely to enlarge the matrix.

## Information and fairness contract

| Property | F0 | C0 | R0 |
|---|---|---|---|
| Agent-visible online information | observation, intended action, reward, lifecycle | same | same |
| True state/regime/change/disturbance/executed action | hidden | hidden | hidden |
| Nominal checkpoint | common learned Q table | same common Q table | not applicable; planned model recorded |
| Post-change learning | none | ordinary Q updates | none |
| Prior transition model | none online beyond learned values | none online beyond learned values | explicit nominal model + declared uncertainty rows |
| True realized post-change kernel | hidden | hidden | hidden; only in-set/out-of-set evaluated by evaluator |
| Exploration/action selection | matched explicit schedule and RNG policy | identical to F0 | explicit comparable deployment action-selection policy |

R0's stronger prior means the thesis compares declared capability/assumption regimes, not equal-information algorithms. Interaction, planning/model queries, tuning trials, CPU time, and memory are controlled or reported separately. Hyperparameters are selected only on development/tuning/pilot partitions and frozen before final trajectories, following citation-ready `SRC-76B2247457`.

## Excluded or deferred candidates

| Candidate | Decision | Evidence-backed reason / reopening condition |
|---|---|---|
| Context Q-learning / context memory | **EXCLUDE from current set** | Citation-ready `SRC-E6A5B7584B` supports a change/context-aware method but assumes detectable structured contexts. The retained RQs contain one novel persistent change, not recurring-context recall; adding detector/context storage would introduce a new RQ, calibration surface, and matrix branch without current necessity. Reopen only if pilots or final framing retain recurring-context recall as distinct. |
| Detector-triggered reset/restart | **EXCLUDE from current set** | Citation-ready `SRC-7456165CEA` shows detection delay/false alarms and relearning are distinct and explicitly recommends feasibility validation. Detector mechanism attribution is not a retained RQ. Reopen only if F0/C0/R0 results cannot explain adaptation mechanisms and a bounded detector question is formally added before protocol freeze. |
| Changepoint oracle | **EXCLUDE as scientific agent** | Evaluator truth would violate the common information contract. It may be a clearly labelled debugging upper bound only, never mixed into agent rankings. |
| Sarsa, Double Q-learning, recency/window variants | **EXCLUDE initially** | They duplicate the ordinary tabular role unless a concrete Q-learning regression/instability appears in pilots. Reopen only for a demonstrated failure that changes the scientific interpretation. |
| Deep DQN/PPO/SAC, meta-learning, neural context/robust methods | **DEFER/EXCLUDE** | The finite observable GridWorld needs no function approximation; extra architecture/optimizer variance, tuning and compute would reduce independent-run evidence without a distinct RQ capability. Reopen only if tabular representation becomes inadequate under an accepted amendment. |
| Dedicated action/observation robust agents | **EXCLUDE** | Those disturbances are supporting diagnostics, not separate primary agent-role questions. |
| Random policy or optimal/oracle planner | **REFERENCE FIXTURE ONLY** | Useful for correctness/scale checks, not a scientifically comparable resilience capability role. |

## T-312 correctness and feasibility results

### Common tabular implementation

- deterministic seeded tie-breaking/exploration and exact replay;
- hand-computed one-step Q update and tiny-MDP optimal policy;
- stable versioned Q-table serialization;
- common nominal checkpoint checksum for F0/C0;
- F0 mutation prohibition and C0 update confirmation;
- terminal/truncation behavior explicit;
- no evaluator-only information in action/update paths.

### Robust planner

- probability rows and uncertainty sets validate and fail closed;
- singleton nominal uncertainty reduces to ordinary value iteration;
- hand-computed robust Bellman backup matches exactly;
- wider set changes only declared transition uncertainty;
- in-set/out-of-set labeling remains evaluator-only;
- frozen deployment cannot update planning state;
- CPU runtime is measured before pilot matrix construction.

## Remaining freeze gates

`T-312` implements and validates these gates in `src/resilient_agents/agents.py` and `tests/test_agents.py`: eight focused tests cover exact Q updates, terminal behavior, common checkpoint/frozen mutation, deterministic replay/round-trip state, hidden-information rejection, singleton and worst-row robust backups, frozen deployment, and invalid model/probability failure. `T-400` now fixes a bounded pre-outcome Q search, common deployment exploration policy, and R0 prior in `pilot-v0.1`; pilots determine feasibility, selected pilot configuration behavior, and whether every role remains informative. `T-412` freezes the final set and fair statistical protocol before final results are inspected.
