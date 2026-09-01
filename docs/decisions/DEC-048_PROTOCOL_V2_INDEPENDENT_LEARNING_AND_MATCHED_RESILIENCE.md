# DEC-048 — Protocol v2: Independent Learning + Matched Resilience

**Status:** Accepted methodology direction; exact machine-dependent values and final retained method set remain pilot-gated  
**Date:** 2026-08-27  
**Supersedes for future final evidence:** execution/freeze of candidate protocol-v1.1  
**Does not supersede:** immutable protocol-v1.0, FINAL-* evidence, historical R0 evidence, validated runtime/information-boundary infrastructure

## Decision

The successor scientific protocol separates two related but distinct questions:

1. **Nominal learning:** how independently trained reinforcement-learning methods learn the controlled task under a fair interaction/information/tuning contract.
2. **Post-training resilience/adaptation:** how each method's own trained state resists and adapts after uncertainty or an unannounced environmental change.

Candidate protocol-v1.1 remains valuable historical/non-final design evidence, but it is no longer the intended final successor protocol. Its strategies begin evaluation from a common selected tabular Q-learning checkpoint; that design isolates post-change adaptation mechanisms but cannot support end-to-end claims about learning differences among algorithms.

A new `protocol-v2.0` lifecycle is therefore designed instead of mutating v1.1 into a fundamentally different experiment.

## Methodology-pass verdict

The 2026-08-27 chained methodology pass retains the two-phase design and sharpens its interpretation.

### Retained

- independent method-native Phase-A training;
- environment interactions/timesteps as the principal common training budget;
- periodic standardized no-learning evaluation checkpoints;
- each method/root/layout's own trained checkpoint as the Phase-B origin;
- exact matched Frozen/Continual cloning plus same-regime nominal references;
- Q-Learning, SARSA, DQN, PPO and Dyna-Q+ as the strong mechanism-spanning core candidates;
- action remapping as the primary persistent-change condition;
- action-execution failure and observation corruption as supporting diagnostics;
- component resilience metrics, paired root-level contrasts where valid, effect sizes/95% intervals, and recovery as secondary/sensitivity.

### Changed / clarified

- The exact four-branch Phase-B construction is a project experimental design for isolating environmental-change and continued-learning effects. Literature supports its component controls and paired-comparison principles, but this exact layout is not represented as a universal standard protocol.
- Dyna-Q is a targeted planning-versus-recency ablation, not an automatic full final arm.
- A2C is **not retained as a full final arm by default** because its mechanism-level actor-critic contrast substantially overlaps PPO. It may be used only as a bounded fallback/diagnostic if later evidence establishes distinct value.
- Replay contents and management are part of DQN's scientific learning state. Reset, recency bias or other replay handling is a separate intervention, never a default implementation convenience.
- Ordinary continued training of deep agents is interpreted with possible loss of plasticity/interference. No plasticity-preserving intervention enters the final matrix without a distinct RQ and pilot justification.
- The three uncertainty classes support separate scientific claims rather than one pooled undifferentiated resilience claim.
- Protocol-v1.0 may be reported as foundational historical evidence and v1.1 as historical candidate-design evidence, but neither is numerically pooled into v2 confirmatory estimates.

### Still pilot-gated

- final retained method count after the core-candidate feasibility/discrimination gate;
- exact GridWorld complexity level;
- exact Phase-A interaction budget and evaluation cadence;
- method hyperparameters and continued-update schedules;
- final root/layout counts and exact primary contrast family;
- CPU/runtime feasibility and matrix size on the validated Windows thesis machine.

### Rejected for the default final design

- equal episode counts as the main cross-family learning budget;
- best-seed selection or treating seeds as hyperparameters;
- library defaults as automatically fair settings;
- arbitrary replay-buffer reset after change;
- adding A2C, Dyna-Q, pixels, partial observability, extra change classes or specialized continual-learning mitigations merely to enlarge the matrix;
- a composite resilience score;
- numerical pooling of historical v1.0/v1.1 results with v2 confirmatory evidence.

## Why

The approved thesis scope supports comparison of resilient AI agents, not only deployment variants of one learned Q-function. A credible multimethod comparison must not conflate:

- sample-efficient nominal learning;
- final nominal policy quality;
- immediate resistance to environmental change;
- continued-learning benefit after change;
- recovery dynamics;
- computational cost.

Empirical-RL methodology requires explicit control of stochastic variability, hyperparameter-selection bias, independent randomization units and comparison budgets. For multimethod learning, the principal common training budget is **environment interactions/steps**, not equal episode count, optimizer-update count or wall-clock time. Wall/CPU time remains a reported resource outcome.

## Candidate method roles

The current strong core candidates, subject to bounded feasibility/discrimination pilots, are:

1. **Q-Learning** — tabular, off-policy value learning.
2. **SARSA** — tabular, on-policy value learning.
3. **DQN** — neural, off-policy value approximation with replay/target-network state.
4. **PPO** — neural, on-policy policy-gradient / actor-critic optimization.
5. **Dyna-Q+** — learned-model planning plus recency-directed re-exploration for change.

These roles span tabular/deep, on-/off-policy, value/policy optimization, model-free/planning and explicit change-directed re-exploration without selecting methods merely to increase model count.

Secondary roles:

- **Dyna-Q:** targeted ablation only when required to separate generic planning from Dyna-Q+ recency-directed re-exploration.
- **A2C:** fallback/diagnostic only; no default full final arm. A later pilot may promote it only if a distinct unresolved scientific contrast outweighs added matrix/compute cost.
- **Historical R0 Robust Planner:** immutable negative/diagnostic evidence. No redesign is required by protocol v2 absent a new explicit RQ.

No final method count is frozen by this decision.

## Phase A — nominal learning

Each retained algorithm trains independently from method-appropriate fresh initialization.

Fairness is defined by the experimental contract rather than identical hyperparameters:

- same project-owned environment semantics;
- same agent-visible information;
- same action and reward contract;
- matched root/layout schedules where scientifically valid;
- common main environment-interaction budget;
- bounded, algorithm-specific literature-backed hyperparameter ranges;
- equivalent predeclared tuning/search opportunity;
- independent tuning roots/partitions and frozen selection/tie criteria;
- no final-reserve or complete final-lifetime access during tuning;
- separate wall-clock/CPU-cost reporting.

Learning reporting distinguishes online training behavior from evaluation policy quality. At predeclared interaction checkpoints, a standardized no-learning evaluator measures the current policy without updating learner state. Evaluation interactions are recorded separately from the training budget. The primary evaluation action rule is frozen before final evidence; method-specific implementation mechanics may differ, but evaluator information may not.

## Phase B — resilience/adaptation

For each retained `method × root × layout`, the trained scientific checkpoint is cloned into matched deployment regimes:

- **Frozen:** no learning-state updates during deployment/evaluation.
- **Continual:** ordinary method-native learning continues according to a predeclared update schedule.

The Frozen and Continual pair starts from the exact same trained scientific state for that method/root. Each regime also receives a matched no-change reference branch so environmental change is not confounded with continued learning itself.

`Continual` means ordinary continued training for the base algorithm. It is a naive adaptation baseline, not a claim that DQN/PPO/etc. are specialized continual-RL algorithms.

### Scientific checkpoint semantics

Checkpoint state is algorithm-specific and includes whatever is necessary for exact scientific continuation:

- **Q-Learning/SARSA:** Q table, exploration/schedule state, relevant counters and RNG.
- **Dyna-Q/Dyna-Q+:** Q table, learned model, planning state/RNG, exploration schedule, relevant counters, and Dyna-Q+ recency/tau state.
- **DQN:** online network, target network, optimizer, replay contents/capacity/size/cursor/sampling policy, exploration schedule/counters, preprocessing/normalization if used, and relevant framework/agent RNG state.
- **PPO-like actor-critic:** policy/value parameters, optimizer, learning-rate/schedule state, normalization if used, counters and RNG; cloning only at a completed rollout/update boundary.

Replay reset/recency weighting and plasticity-preserving changes are separate scientific interventions. They are not part of the default Continual branch.

## Environment decision

Do not switch to pixels, partial observation or a large external benchmark merely to justify deep learning. The neural representation may be a deterministic vector/one-hot encoding of the same semantic state available to tabular methods; it receives no extra evaluator truth.

Before v2 freeze, run a bounded **environment-discrimination pilot** over a small **predeclared ordered** set of project-owned GridWorld complexity levels.

The selection rule is frozen before observing the pilot outcomes: retain the simplest level that is not universally trivial and not universally unsolved across the core candidate set, preserves the uncertainty/information contract and is feasible on the thesis CPU. A method-specific poor outcome does not by itself authorize choosing a different environment level, and method rankings must not drive environment selection.

Generalization to procedurally unseen levels remains a limitation/future-work topic unless explicitly promoted to a research question before freeze.

## Uncertainty scope and claims

Retain the current interpretable conditions, with distinct claim roles:

- **Action remapping:** abrupt persistent transition/action-semantics change; primary adaptation condition.
- **Action-execution failure:** stationary/stochastic actuation uncertainty; supporting robustness diagnostic.
- **Observation corruption:** perceptual/information uncertainty; supporting robustness diagnostic with explicit acknowledgement that ambiguity may become POMDP-like.

Do not pool these mechanisms into one undifferentiated superiority claim. Do not add gradual drift, recurring tasks, reward shifts, dynamic obstacles or other conditions for variety alone.

## Metrics, statistics and tuning

### Phase A

Retain standardized final nominal evaluation, checkpoint learning curves, learning efficiency and/or AUC only alongside the curves, variability, failures and CPU/wall cost.

### Phase B primary roles

- immediate degradation;
- cumulative deficit relative to the matched same-regime nominal reference;
- terminal/post-change performance or terminal gap.

Recovery/no-recovery remains secondary/sensitivity because threshold and stability definitions affect it. No composite resilience score is used.

### Statistical unit and contrasts

- Roots/runs are the independent randomization units; episodes nested inside a root are repeated observations, not independent replicates.
- Use paired root/layout designs wherever common environment randomness is scientifically valid.
- Report effect sizes and 95% uncertainty intervals; retain raw per-root results and failed/null/non-recovery outcomes.
- Do not mechanically import a multi-task aggregate such as IQM when it does not match the single-testbed root/layout hierarchy.
- Predeclare a small primary contrast family: (1) within-method Continual − Frozen; (2) Frozen cross-method resistance; (3) selected cross-method adaptation-benefit contrasts with explicit mechanistic rationale. Do not calculate every pairwise comparison as a confirmatory family.
- If formal p-values are used, multiplicity handling is frozen before final evidence.
- Final root count and matrix size come from non-final precision/variance and measured runtime, not from v1.1's historical root count.

### Tuning fairness

Use method-appropriate hyperparameters but equivalent opportunity. The default contract is a common predeclared number/search budget of method-specific candidate configurations, the same tuning-only root/partition structure and training interaction budget per configuration, plus a frozen selection metric and tie rule. Literature/library settings may seed ranges but do not receive privileged final status. Alternative sequential search is permissible only if one common search-budget rule is frozen before tuning and applied consistently.

The known full final deployment lifetime/non-stationarity schedule is never repeatedly used for configuration selection.

## Historical evidence

`protocol-v1.0` remains valid frozen foundational evidence for its own within-Q-learning estimands and may be reported separately.

Candidate `protocol-v1.1` remains auditable non-final adaptation-mechanism design evidence. It is not deleted, rewritten or relabelled as a multimethod learning benchmark.

No v1.0/v1.1 tuning/final outcome is silently promoted or numerically pooled into v2 confirmatory estimates.

## Bibliography boundary

`ThesisBibliography` remains the canonical bibliography source of truth. The 2026-08-27 research pass identified and upstreamed only genuine gaps after content/title/identifier deduplication. Formal thesis citation support is not hand-copied into this repository; it becomes available only through the next accepted versioned bibliography synchronization after upstream analysis/evidence/selection.

## Execution order

1. Finish upstream bibliography analysis/evidence/selection and freeze the source-backed v2 RQs/method roles (`T-524`).
2. Implement only the bounded common training/evaluation/checkpoint/clone foundation and minimum pilot adapters (`T-525`).
3. Run the predeclared environment-discrimination and method/CPU feasibility pilot on the validated thesis Windows machine (`T-526`).
4. Perform bounded fair tuning, precision/runtime sizing and freeze the machine-readable v2 statistical/protocol contract (`T-527`).
5. Only then redesign the UI around the accepted scientific workflow (`T-528`/`T-511`).
6. Later final evidence uses the existing guarded T-610+ lifecycle after all gates pass.

UI redesign remains paused until the scientific contract stabilizes. Final standalone Windows packaging remains deferred until after the thesis document is frozen.
