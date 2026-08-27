# Agent Strategy Selection

**Status:** Current pre-WP7 authority after DEC-047. GridWorld is the controlled experimental testbed/visualization surface; the thesis subject is the comparison and evaluation of resilient AI agent strategies under uncertainty and environmental change.

## Current candidate direction

Candidate `protocol-v1.1` now targets **five main agent strategies**, subject to focused implementation and non-final validation before freeze:

| User-facing name | Technical identity | Mechanism isolated | Candidate status |
|---|---|---|---|
| **Fixed Q-Learning** | historical `F0` / `tabular_q_learning_v1`, post-change updates disabled | No online adaptation; reuse nominal learned policy | RETAIN |
| **Adaptive Q-Learning** | historical `C0` / same `tabular_q_learning_v1`, updates continue | Off-policy model-free continual adaptation | RETAIN |
| **SARSA** | new v1.1 implementation | On-policy model-free continual adaptation | IMPLEMENT/VALIDATE before protocol freeze |
| **Dyna-Q** | new v1.1 implementation sharing Dyna learned-model machinery without recency bonus | Model-based learning + planning | IMPLEMENT/VALIDATE before protocol freeze |
| **Dyna-Q+** | historical technical identity `D0` / `dyna_q_plus_v1` | Model-based planning + directed re-exploration | RETAIN; Dyna-specific non-final settings still require selection |

This is a mechanism-driven set, not a target model count. It gives the thesis a controlled comparison across no adaptation, two model-free adaptation policies, learned-model planning, and planning with explicit change-seeking re-exploration.

F0/C0/D0 remain valid historical/reproducibility IDs but **must not be the primary names shown to ordinary users**.

## Why the set was broadened

The earlier F0/C0/D0 set was scientifically controlled but narrow: Fixed and Adaptive Q-Learning are two deployment regimes of one Q-learning implementation, and Dyna-Q+ was the only planning family. Broader non-stationary/continual RL literature commonly compares ordinary temporal-difference learners with planning/adaptation variants. Classical changing-environment Dyna experiments compare Dyna-Q directly with Dyna-Q+, allowing the effect of directed re-exploration to be separated from planning itself. Related empirical work also compares SARSA/Q-learning/Dyna variants over many runs.

Adding SARSA and Dyna-Q therefore answers concrete mechanism questions rather than merely enlarging the matrix.

## Main strategy definitions

### Fixed Q-Learning

User explanation: **“Uses what it learned before the change; it does not learn during evaluation.”**

- Starts from the selected common nominal Q checkpoint.
- Uses the validated Q-learning action-selection configuration.
- Suppresses all post-change learning-state mutation.
- Serves as the non-adaptive resistance/reference strategy.

### Adaptive Q-Learning

User explanation: **“Keeps updating its learned action values from new experience.”**

- Starts from the same selected nominal checkpoint/base configuration as Fixed Q-Learning.
- Continues ordinary off-policy one-step Q-learning updates online.
- Isolates the value/cost of simply permitting continual model-free learning.

Current inherited candidate base values remain:

- learning rate `α = 0.5`;
- discount factor `γ = 0.96875`;
- exploration epsilon `ε = 0.125`;
- `512` nominal training episodes per layout;
- `16` pre-change evaluation episodes;
- `32` post-change evaluation episodes;
- `48`-step evaluation horizon.

These values stay fixed for the two Q-learning strategies unless an explicit evidence-backed amendment reopens them.

### SARSA

User explanation: **“Learns from the actions it actually follows, including exploratory actions.”**

SARSA adds an on-policy model-free adaptation mechanism. Its update uses the next action selected by the behavior policy rather than the greedy maximum used by Q-learning. This makes the comparison scientifically useful under stochastic action/observation conditions and exploration.

Requirements before inclusion in candidate v1.1:

- information-limited deterministic implementation under the same `AgentTransition` boundary;
- versioned serializable state/checkpoint semantics;
- matched nominal-training/evaluation budget;
- bounded predeclared non-final tuning only where SARSA-specific fairness requires it;
- no evaluator changepoint/disturbance/true-state information;
- focused exact-update/determinism/serialization tests.

Do not blindly force every Q-learning-selected hyperparameter onto SARSA if non-final evidence shows that doing so is an unfair algorithmic handicap. Any SARSA-specific tuning surface must remain small and predeclared before selection evidence.

### Dyna-Q

User explanation: **“Learns from real experience and also plans using an internal model it learns.”**

Dyna-Q should reuse the same information-limited empirical learned-model/planning machinery as Dyna-Q+ as far as scientifically possible, but without the recency-directed exploration bonus. Its central role is an ablation/control for Dyna-Q+:

> Does improvement come from model-based planning itself, or from Dyna-Q+'s explicit re-exploration mechanism?

Requirements:

- same agent-visible information boundary as all scientific agents;
- deterministic learned-model/planning RNG state;
- matched planning-step budget with Dyna-Q+ where appropriate;
- no recency bonus (`kappa = 0` or equivalent explicit no-bonus semantics);
- same serialization/resume guarantees as Dyna-Q+;
- focused tests proving the only intended algorithmic difference from Dyna-Q+ is directed re-exploration behavior.

### Dyna-Q+

User explanation: **“Plans like Dyna-Q and deliberately re-checks actions that have not been tried recently.”**

The already validated D0 implementation uses:

- common candidate Q-learning base values where applicable;
- empirical stochastic model learned only from agent-visible transitions;
- bounded planning updates;
- deterministic independent exploration/planning RNG state;
- recency state and bonus for long-untried state/action pairs;
- episode-preserving learned Q/model/recency deployment state.

Dyna-specific non-final selection remains bounded to the predeclared planning surface, principally `planning_steps` and Dyna-Q+ `kappa`.

## Reference strategies — not equivalent ranked agents

Reference fixtures help interpret scale/correctness but must not inflate the main agent count or appear in fair rankings.

### Random Agent

- Simple lower behavioral reference and correctness fixture.
- No claim that it is a resilient learning strategy.
- May appear in optional scale/reference plots with clear labelling.

### Nominal / fully informed planner

- Optional upper/scale/debug reference where useful.
- Any privileged transition model, true environment state, or evaluator knowledge must be explicit.
- Never mixed into a fair agent ranking because its information contract differs.

## Robust-planning branch

Historical `R0` robust value iteration remains immutable pilot evidence. It represents the distinct scientific idea of **pre-deployment robustness to an uncertainty set**, but the accepted pilot configuration had approximately 96% nominal truncation and cannot be reinstated unchanged.

A revised **Robust Planner** may become a sixth main comparator only through a small predeclared non-final gate demonstrating:

1. acceptable nominal viability;
2. explicit uncertainty-set construction and prior-model disclosure;
3. bounded tuning/runtime cost;
4. fair interpretation despite stronger prior information;
5. a distinct robustness question not already answered by the five main strategies.

If this gate fails, the negative R0 evidence remains a valid thesis result/limitation and the five-agent design proceeds without it.

## Multiple-settings and repetition policy

The application and runner support **multiple protocol-approved resolved configurations**, not an unrestricted hyperparameter playground.

### Development / tuning

- Every configuration is a complete resolved parameter set with stable identity/hash/provenance.
- Every compared configuration uses multiple predefined root seeds/repetitions; single-run ranking is forbidden.
- Fixed/Adaptive Q-Learning remain on the validated shared base configuration unless formally reopened.
- SARSA receives only the smallest predeclared fairness-relevant tuning surface justified before outcomes.
- Dyna-Q/Dyna-Q+ planning settings are predeclared and selected from non-final evidence only.
- UI explains which values are fixed, tunable, advanced or unavailable and why.

### Pilot / validation

- Candidate settings are evaluated only on permitted non-final partitions.
- Failed/interrupted/cancelled/invalid/non-recovery/poor configurations remain recorded.
- Selection and tie rules are predeclared; no best-seed/best-run cherry-picking.
- Runtime/planning cost is recorded where interpretation or feasibility needs it.

### Final evidence

- Retained agents and their configurations freeze before final outcomes are inspected.
- Final matrix uses the frozen configuration for each retained strategy, precommitted final roots and every required layout/condition.
- Exploratory/tuning variants remain labelled non-final and cannot be promoted by renaming.

## Candidate-v1.1 experimental direction

### Main agents

1. Fixed Q-Learning;
2. Adaptive Q-Learning;
3. SARSA;
4. Dyna-Q;
5. Dyna-Q+.

A revised Robust Planner is conditional, not assumed.

### Conditions

1. `nominal`;
2. `action-remap-2-swap`;
3. `action-remap-4-cycle`;
4. `action-failure-1of8`;
5. `action-failure-1of4`;
6. `observation-corruption-1of8`;
7. `observation-corruption-1of4`.

### Layouts and repetitions

- four fresh held-out final layouts under the accepted controlled-environment structural constraints;
- fresh precommitted v1.1 final seed bank;
- current target `32` paired final root seeds per layout/condition experiment;
- development/tuning/pilot/final partitions remain disjoint.

T-523 must implement/validate the newly added SARSA and Dyna-Q strategies before T-521 can freeze the authoritative candidate schema. T-521 then re-estimates matrix runtime/size and may adjust only with an explicit evidence-backed amendment, not to make inconvenient results disappear.

## Capability contrasts

| Contrast | Capability isolated |
|---|---|
| Fixed Q-Learning vs Adaptive Q-Learning | Effect of continuing off-policy model-free learning |
| Adaptive Q-Learning vs SARSA | Off-policy vs on-policy continual model-free adaptation |
| Adaptive Q-Learning vs Dyna-Q | Real-experience-only learning vs learned-model planning |
| Dyna-Q vs Dyna-Q+ | Planning alone vs planning plus directed re-exploration |
| Fixed Q-Learning vs each adaptive strategy | Resistance without adaptation vs post-change adaptation/recovery |
| Conditional Robust Planner vs adaptive strategies | Pre-deployment worst-case robustness vs online adaptation, with stronger prior disclosed |

Primary reporting remains cumulative deficit, immediate degradation and terminal performance/gap. Recovery remains secondary/sensitivity because the historical pilot showed threshold/stability sensitivity. Paired effects, 95% CIs, explicit `n`, layout/condition views and failures/non-recovery remain required. No opaque composite resilience score.

## Information and fairness contract

All five main scientific agents receive the same permitted online surface: observation, intended action, reward and lifecycle information. True state, executed action, changepoint/regime identity and disturbance flags remain hidden.

Technical implementation differences are allowed only when they are the mechanism under study. Computational/planning cost and stronger priors are reported rather than hidden.

## User-facing naming contract

Primary UI label: **Agent strategy**.

Do not expect users to understand `F0`, `C0`, `D0`, schema names or config hashes. Main cards, selectors, charts, live overlays, Compare and exported thesis-facing visuals use the human-readable names above plus one-sentence explanations and mechanism badges such as:

- `Does not adapt`;
- `Model-free`;
- `On-policy` / `Off-policy`;
- `Learns online`;
- `Uses planning`;
- `Re-explores for change`.

Internal IDs/checkpoint schemas/config hashes remain available under **Technical details / Reproducibility** only. The thesis may introduce stable abbreviations after full names, but unexplained repository IDs are not presentation terminology.

## Excluded/deferred candidates

| Candidate | Decision | Reason / reopening condition |
|---|---|---|
| Expected SARSA | **DEFER** | Similar on-policy TD family; add only if SARSA non-final evidence raises a distinct variance/stability question worth a separate RQ/contrast. |
| Double Q-learning / Q(λ) / SARSA(λ) | **DEFER** | Useful variants but no current distinct resilience mechanism justifies matrix growth. |
| Detector-triggered reset/context memory | **EXCLUDE currently** | Requires a separate changepoint/context-recognition research question. |
| Changepoint oracle | **REFERENCE ONLY** | Evaluator truth violates fair scientific-agent information boundary. |
| DQN/PPO/SAC/deep actor-critic/meta-learning/neural robust methods | **DEFER/EXCLUDE** | Added representation/optimizer/tuning variance is not justified by the finite controlled testbed or current RQ. |
| Dedicated action/observation-specific robust agents | **DEFER** | Reopen only if those disturbance types become separate primary capability questions. |

## Validation state and next gate

`T-520` remains complete: Dyna-Q+ implementation/integration is validated.

DEC-047 introduces `T-523` as the immediate scientific implementation gate: deterministic information-limited SARSA + plain Dyna-Q, focused tests, runner integration, reference fixtures where useful, and updated runtime-feasibility estimate.

Only after T-523 passes does `T-521` own the authoritative candidate-v1.1 schema, exact bounded tuning surfaces, fresh held-out layouts/seeds, structural condition IDs, paired-effect/95% CI support and final stage/firewall rules. Final evidence remains blocked until non-final validation/freeze and application acceptance.