# DEC-048 — Protocol v2: Independent Learning + Matched Resilience

**Status:** Accepted research-design direction; exact method set/environment/budgets remain pilot-gated  
**Date:** 2026-08-27  
**Supersedes for future final evidence:** execution/freeze of candidate protocol-v1.1  
**Does not supersede:** immutable protocol-v1.0, FINAL-* evidence, historical R0 evidence, validated runtime/information-boundary infrastructure

## Decision

The successor scientific protocol will separate two related but distinct questions:

1. **Nominal learning:** how independently trained reinforcement-learning methods learn the controlled task under a fair interaction/information/tuning contract.
2. **Post-training resilience/adaptation:** how each trained method resists and adapts after uncertainty or an unannounced environmental change.

Candidate protocol-v1.1 remains valuable historical/non-final design evidence, but it is no longer the intended final successor protocol. Its five strategies begin evaluation from a common selected tabular Q-learning checkpoint; that design cleanly isolates adaptation mechanisms but cannot support claims about end-to-end learning differences among algorithms.

A new `protocol-v2.0` lifecycle will therefore be designed instead of mutating v1.1 into a fundamentally different experiment.

## Why

The approved thesis title is broad enough to support comparison of resilient AI agents, not only deployment variants of one learned Q-function. A credible multimethod comparison must not conflate:

- sample-efficient nominal learning;
- final nominal policy quality;
- immediate resistance to environmental change;
- continued-learning benefit after change;
- recovery dynamics;
- computational cost.

Current RL empirical-design literature also requires explicit handling of stochastic variability, hyperparameter-selection bias, independent runs and fair comparison budgets. For multimethod learning, the principal common training budget will be **environment interactions/steps**, not an equal episode count or equal optimizer-update count.

## Candidate method roles

The current strong core candidates, subject to bounded feasibility/discrimination pilots, are:

1. **Q-Learning** — tabular, off-policy value learning.
2. **SARSA** — tabular, on-policy value learning.
3. **DQN** — neural, off-policy value approximation.
4. **PPO** — neural, on-policy policy-gradient / actor-critic optimization.
5. **Dyna-Q+** — learned-model planning plus directed re-exploration for change.

These roles span tabular/deep, on-/off-policy, model-free/model-based and explicit change-directed exploration without selecting methods merely to increase model count.

Secondary/pilot roles:

- **Dyna-Q:** useful ablation for separating planning from Dyna-Q+ re-exploration; it need not automatically occupy a full final arm.
- **A2C:** technically feasible and scientifically valid as an actor-critic candidate, but overlaps substantially with PPO at the mechanism-family level. It enters the final matrix only if literature/pilot evidence establishes a distinct useful contrast at acceptable cost.
- **Historical R0 Robust Planner:** remains immutable negative/diagnostic evidence. No redesign is required by protocol v2 unless a later explicit research question justifies it.

No final method count is frozen by this decision.

## Phase A — nominal learning

Each retained algorithm is trained independently from method-appropriate fresh initialization.

Fairness is defined by the experimental contract rather than identical hyperparameters:

- same project-owned environment semantics;
- same agent-visible information;
- same action and reward contract;
- matched environment/root seed schedule where meaningful;
- common main environment-interaction budget;
- bounded, algorithm-specific hyperparameters;
- equivalent predeclared tuning opportunity;
- no final-reserve access during tuning;
- separate wall-clock/CPU-cost reporting.

Learning reporting must distinguish online training behavior from evaluation policy quality. Periodic no-learning evaluation checkpoints should be used so epsilon-greedy learners and stochastic policy-gradient methods are not compared solely through incomparable exploratory training returns.

## Phase B — resilience/adaptation

For each retained method, root and layout, the trained scientific checkpoint is cloned into matched deployment regimes:

- **Frozen:** no learning-state updates during deployment/evaluation.
- **Continual:** ordinary method-native learning continues according to a predeclared update schedule.

The Frozen and Continual pair must start from the exact same trained scientific state for that method/root. Each regime also receives a matched no-change reference branch so environmental change is not confounded with continued learning itself.

`Continual` means ordinary continued training for that base algorithm. It is a naive continual-learning baseline, not a claim that DQN/PPO/etc. are specialized continual-RL algorithms.

Checkpoint semantics are algorithm-specific. For example, a continual DQN scientific checkpoint includes the online network, target network, optimizer, exploration/schedule state and replay-buffer policy/state unless a separate predeclared replay-reset intervention is explicitly studied. Actor-critic checkpoints include policy/value networks, optimizer/schedule state and are cloned only at a valid rollout/update boundary.

## Environment decision

Do not switch to pixels, partial observation or a large external benchmark merely to justify deep learning.

Before v2 freeze, run a bounded **environment discrimination pilot** over a small number of project-owned GridWorld complexity levels. Keep the same semantic information contract across methods. Tabular agents may consume the canonical discrete state; neural agents may consume a deterministic numeric/one-hot encoding of the same semantics, with no additional evaluator truth.

Select the simplest environment family that:

- avoids ceiling/floor effects across candidate methods;
- remains interpretable;
- supports controlled uncertainty/change;
- fits the validated CPU budget.

Generalization to procedurally unseen levels is not automatically a new primary research question.

## Uncertainty scope

Retain the current interpretable uncertainty classes unless pilot evidence gives a specific reason to amend them:

- primary persistent dynamics/rule change: action remapping;
- supporting stochastic actuation uncertainty: action-execution failure;
- supporting perceptual uncertainty: observation corruption.

Do not add uncertainty mechanisms for variety alone. Gradual drift, recurring task changes and dynamic obstacles can remain limitations/future work unless deliberately promoted to a research question before protocol freeze.

## Statistics and tuning

- Seeds are randomization units, never tunable parameters.
- Episodes nested inside a root are not independent replicates.
- Use paired designs wherever common environment randomness permits.
- Report effect sizes and uncertainty intervals; retain raw per-run results and negative/null/non-recovery outcomes.
- Recovery remains secondary/sensitivity; no composite resilience score.
- Final root count and matrix size are chosen from pilot variability/precision and measured runtime, not copied automatically from v1.1.
- Hyperparameter tuning is bounded and fair: at minimum, comparable numbers of configurations (or a fixed optimization budget), the same tuning interaction budget, roots and environment partitions.
- Do not tune against the complete deployment/final lifetime.

## Historical evidence

`protocol-v1.0` remains a valid frozen within-Q-learning experiment isolating the value of online adaptation and can be reported as foundational/historical evidence.

Candidate `protocol-v1.1` remains an auditable non-final adaptation-mechanism design. It is not deleted, rewritten or relabelled as a multimethod learning benchmark.

No v1.0 or v1.1 final/tuning outcome may be silently promoted into v2 confirmatory rankings.

## Execution order

1. Literature/bibliography completion and v2 research-question freeze.
2. Common method/training/checkpoint contract.
3. Environment-discrimination and method-feasibility pilots on the validated thesis machine.
4. Bounded fair tuning and variance/runtime pilot.
5. Candidate/final v2 protocol freeze before final-reserve access.
6. Later final evidence through the existing guarded T-610+ lifecycle.

UI redesign is intentionally paused until the scientific contract stabilizes. Final standalone Windows packaging remains deferred until after the thesis document is frozen.
