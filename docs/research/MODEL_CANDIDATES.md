# Agent and Model Role Selection

**Status:** Current pre-WP7 authority for the agent set. Historical F0/C0/R0 pilot evidence is preserved, `T-520` D0 implementation/integration is complete, and `T-521`/`T-522` own candidate-v1.1 tuning/freeze decisions.

## Current selection outcome

The current candidate `protocol-v1.1` uses three scientifically distinct deployment regimes:

| ID | Exact method / regime | Scientific role | Current status |
|---|---|---|---|
| F0 | `tabular_q_learning_v1` from the common selected nominal checkpoint; evaluation updates disabled | Frozen nominal resistance reference | **RETAIN for v1.1 candidate** |
| C0 | Same `tabular_q_learning_v1` checkpoint/base configuration; online Q updates continue after change | Model-free continual adaptation baseline | **RETAIN for v1.1 candidate** |
| D0 | `dyna_q_plus_v1` from the same information-limited interaction surface; empirical model + bounded planning + recency bonus | Model-based continual adaptation / directed re-exploration comparator | **RETAIN for v1.1 candidate; D0-only planning settings still require bounded non-final selection** |
| R0 | Historical `rectangular_robust_value_iteration_v1` pilot comparator | Declared-set frozen robustness / conservativeness | **HISTORICAL PILOT EVIDENCE ONLY; do not reinstate unchanged** |

F0 and C0 remain two deployment regimes of the same tabular Q-learning implementation, not an inflated algorithm count. D0 adds a genuinely distinct adaptation mechanism without introducing deep/function-approximation complexity. R0 remains scientifically useful historical evidence, but its accepted pilot configuration produced approximately 96% nominal truncation and therefore is not part of the current v1.1 candidate set.

Do not add deep RL merely to increase the number of models. A new model family requires a distinct research-question role, information/fairness contract, bounded tuning budget, feasibility evidence, and an explicit protocol amendment before final evidence.

## Exact current agent identities

### F0 / C0 — tabular Q-learning

For delivered observation/state `s`, intended action `a`, reward `r`, and next delivered observation `s'`:

`Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') − Q(s,a)]`

F0 and C0 share the selected nominal checkpoint and base evaluation configuration. F0 suppresses post-change learning-state mutation. C0 continues ordinary online Q-learning updates. Both receive only agent-visible information through the accepted transition contract and never true state, executed action, regime/change identifiers, disturbance flags, or evaluator truth.

The candidate-v1.1 base values inherited from accepted tuning evidence are:

- learning rate `α = 0.5`;
- discount factor `γ = 0.96875`;
- exploration epsilon `ε = 0.125`;
- `512` nominal training episodes per layout;
- `16` pre-change evaluation episodes;
- `32` post-change evaluation episodes;
- `48`-step evaluation horizon.

These values are the current candidate-v1.1 F0/C0 base configuration. They are not an invitation for unrestricted final-result tuning.

### D0 — Dyna-Q+

D0 uses the same agent-visible observation/intended-action/reward surface and never receives evaluator-only state or changepoint information. It maintains:

- tabular Q values;
- an empirical stochastic transition/reward model learned only from experienced agent-visible transitions;
- experienced state-action/model support required by the implementation;
- deterministic exploration and planning RNG state under the established seed contracts;
- Dyna-Q+ recency state used to support directed re-exploration;
- explicit JSON-compatible serializable state/checksum semantics.

During deployment, D0 preserves learned Q/model/recency state across evaluation episodes while episode-scoped RNG/pending-action state is reset according to the validated runner contract. Reference and disrupted matched branches begin from equivalent branch initialization and then evolve independently.

D0 uses the common candidate-v1.1 Q-learning base values where applicable. Only genuinely D0-specific planning parameters are eligible for bounded non-final tuning:

- `dyna_planning_steps`;
- `dyna_kappa`.

`T-521` must predeclare the small allowed development/tuning search before outcomes are used for selection. `T-522` selects/freeze-amends/rejects using non-final evidence only. No D0 planning value may be selected from v1.1 final outcomes.

## Multiple-settings and repetition policy

The application and runner must support **multiple approved configurations per model/regime** where the protocol allows them, but configuration exploration is stage-controlled rather than an unrestricted parameter playground.

### Development / tuning

- A configuration variant is a complete resolved parameter set with a stable configuration identity/hash and stored provenance.
- Multiple approved variants may be launched for a model when the active development/tuning plan explicitly declares them.
- Every compared variant uses multiple predefined root seeds/repetitions; single-run configuration ranking is forbidden.
- D0 receives the bounded planning-parameter search defined by T-521.
- F0/C0 candidate-v1.1 base hyperparameters remain fixed unless an explicit scientific amendment reopens them; do not silently retune them merely to match D0.
- The UI may expose only protocol-approved values/ranges/combinations and must explain which settings are fixed, tunable, advanced, or unavailable and why.

### Pilot / validation

- Candidate settings are evaluated only on permitted non-final partitions.
- Failed, interrupted, cancelled, invalid, non-recovery, and poor-performing configurations remain recorded.
- Selection criteria and tie rules are predeclared; no best-seed/best-run cherry-picking.
- Resource/runtime costs are recorded when useful to interpret feasibility.

### Final evidence

- Final model settings are frozen before final outcomes are inspected.
- The final matrix uses the frozen configuration for each retained regime, the precommitted final root seeds, and all required layouts/conditions.
- Final comparison reports the number of paired roots/units and preserves layout/condition breakdowns.
- Exploratory/tuning configurations remain visible as non-final provenance and never become final evidence by relabeling.

## Candidate-v1.1 experimental matrix

Current direction from DEC-042/T-521:

### Agents

- F0 frozen Q-learning;
- C0 continual Q-learning;
- D0 Dyna-Q+.

### Conditions

1. `nominal`;
2. `action-remap-2-swap`;
3. `action-remap-4-cycle`;
4. `action-failure-1of8`;
5. `action-failure-1of4`;
6. `observation-corruption-1of8`;
7. `observation-corruption-1of4`.

### Layouts and repetitions

- four fresh held-out final layouts under the accepted GridWorld structural constraints;
- fresh precommitted v1.1 final seed bank;
- `32` paired final root seeds per final layout/condition experiment;
- development/tuning/pilot/final partitions remain disjoint and stage-validated.

The exact fresh layout definitions, final seed values, D0 search values, and candidate protocol schema are owned by T-521 and must be committed before the corresponding evidence is inspected.

## RQ and metric mapping

| Contrast | Capability isolated | Required evidence |
|---|---|---|
| F0 vs C0 | Cost/benefit of ordinary continual model-free updating from the same nominal checkpoint | nominal performance, immediate degradation, cumulative deficit, terminal performance/gap, secondary recovery outcome |
| F0 vs D0 | Frozen nominal behavior versus model-based continual adaptation/re-exploration | same component outcomes + paired effect/CI and trajectory view |
| C0 vs D0 | Ordinary model-free updating versus learned-model planning + recency-directed re-exploration | full post-change curves, component outcomes, paired effects/95% CIs, runtime/resource context where useful |

The primary candidate-v1.1 reporting roles are cumulative deficit, immediate degradation, and terminal gap/performance. Recovery remains secondary/sensitivity because accepted pilot evidence showed threshold/stability sensitivity. Preserve `NO_DEGRADATION`, `RECOVERED`, and `NOT_RECOVERED`; never encode non-recovery as a fabricated horizon recovery time. No composite resilience score is used.

Observation corruption and action-execution failure remain single-factor supporting conditions using the same retained regimes rather than requiring a dedicated model for each disturbance type.

## Information and fairness contract

| Property | F0 | C0 | D0 |
|---|---|---|---|
| Online agent-visible information | observation, intended action, reward, lifecycle | same | same |
| True state / executed action / change / disturbance / regime | hidden | hidden | hidden |
| Common selected nominal Q checkpoint | yes | yes | compatible starting checkpoint | 
| Post-change learning | none | Q updates | Q updates + empirical-model/planning updates |
| Prior privileged transition model | none | none | none; model is learned from permitted interaction |
| Changepoint oracle | none | none | none |
| Final configuration selection | frozen pre-final | frozen pre-final | bounded D0-only non-final tuning then frozen |

Comparisons therefore study declared adaptation mechanisms under a common information boundary. Differences in computational planning cost are reported rather than hidden, but the scientific interface does not give D0 privileged evaluator knowledge.

## Historical R0 boundary

R0 remains in repository history/pilot evidence because it demonstrated a meaningful declared-set robustness contrast and exposed a real feasibility failure. Do not delete, rewrite, or relabel that evidence. Do not include R0 in current v1.1 agent selection, UI default final configuration, final-v1.1 matrices, or result rankings unless a future explicit protocol amendment scientifically reopens and revalidates it.

## Excluded or deferred candidates

| Candidate | Decision | Reopening condition |
|---|---|---|
| Context Q-learning / recurring-context memory | **EXCLUDE** | Reopen only if recurring-context recall becomes a distinct accepted RQ. |
| Detector-triggered reset/restart | **EXCLUDE** | Reopen only if changepoint detection itself becomes an accepted mechanism question. |
| Changepoint oracle | **EXCLUDE as scientific agent** | Debug/reference fixture only; evaluator truth cannot enter scientific rankings. |
| Sarsa / Double Q / extra recency-window tabular variants | **EXCLUDE** | Reopen only for a concrete scientifically material failure not answered by F0/C0/D0. |
| DQN / PPO / SAC / meta-learning / neural context or robust methods | **DEFER/EXCLUDE** | Reopen only if the accepted representation/RQ requires function approximation and added tuning/compute is justified. |
| Dedicated action/observation robust agents | **EXCLUDE** | Reopen only if those disturbances become separate primary agent-role RQs. |
| Random/oracle/optimal planner | **REFERENCE FIXTURE ONLY** | Correctness/scale checks, not comparable resilience agents. |

## Validation state and next gate

`T-520` is complete: standalone D0, deterministic serialization, episode-preserving deployment, development-only v1.1 adapter and F0/C0/D0 runner integration are covered by focused tests and PR CI run 346.

`T-521` is now the authoritative next scientific configuration task. It must commit the candidate-v1.1 protocol/schema, exact bounded D0-only search, fresh held-out layout definitions, fresh final seed bank, structural condition IDs, paired-effect/95% CI support and stage/firewall rules before `T-522` uses any non-final tuning/pilot evidence. Final evidence remains blocked until the protocol is frozen and the complete application is accepted.