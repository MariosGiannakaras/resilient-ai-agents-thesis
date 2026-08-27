# Protocol v2 Research Design

**Status:** pre-implementation research contract; method/environment/budget values remain pilot-gated  
**Decision:** DEC-048  
**Tracker:** #95  
**Historical authority:** protocol-v1.0 remains immutable; candidate v1.1 remains auditable non-final history

## 1. Thesis-level research objective

The thesis studies how resilient reinforcement-learning agents behave under uncertainty and environmental change. GridWorld is the controlled testbed, not the thesis subject.

Protocol v2 separates two questions that must not be collapsed:

### RQ-A — nominal learning
Under a common controlled environment/information/resource contract, how do scientifically distinct RL methods differ in learning efficiency, nominal performance, variability and computational cost?

### RQ-B — resilience/adaptation
Starting from each method's own trained checkpoint, how do Frozen and Continual deployment regimes differ in immediate resistance, cumulative performance loss and post-change adaptation under matched uncertainty/change conditions?

Secondary questions may examine whether nominal-learning characteristics predict resilience and whether conclusions vary by uncertainty class. Directional hypotheses must be literature/pilot justified before final freeze.

## 2. Candidate method-role matrix

| Method | Family | Policy relation | Representation | Distinct scientific role | Current role |
|---|---|---|---|---|---|
| Q-Learning | value-based | off-policy | tabular | classical tabular baseline | core candidate |
| SARSA | value-based | on-policy | tabular | on-policy tabular contrast | core candidate |
| DQN | value-based | off-policy | neural | function approximation + replay/target network | core candidate |
| PPO | actor-critic / policy optimization | on-policy | neural | policy-gradient / clipped actor-critic contrast | core candidate |
| Dyna-Q+ | model-based planning | off-policy-style Q updates | tabular/model | learned planning + explicit recency-directed re-exploration | core candidate |
| Dyna-Q | model-based planning | off-policy-style Q updates | tabular/model | planning ablation without Dyna-Q+ bonus | secondary/ablation candidate |
| A2C | actor-critic | on-policy | neural | synchronous actor-critic baseline | secondary candidate; final inclusion needs distinct-value evidence |
| Random | non-learning reference | n/a | n/a | lower behavioral scale/correctness reference | reference only |
| Historical R0 | robust planner | n/a | model/prior based | historical pre-deployment robustness attempt | negative/diagnostic history |

No method is retained in the final matrix merely because it is popular. Each retained method must add a distinct scientific contrast and pass feasibility/discrimination gates.

## 3. Common information contract

Every scientific method receives the same semantic online information allowed by the protocol. The existing evaluator/agent separation remains non-negotiable.

Agent-visible information may include the delivered observation, intended action chosen by the agent, reward and lifecycle information required by the algorithm.

Evaluator-only ground truth can include true state under observation corruption, executed action, disturbance/change flags, regime/change identity and hidden environment mappings. UI/analysis may inspect evaluator truth, but it may never leak into the agent transition/update path.

Neural observation encoding may differ in representation mechanics but not semantic content. A one-hot/vector encoding of the same fully observed state is acceptable; pixels or extra map/evaluator features are not introduced merely to advantage deep methods.

## 4. Phase A — independent nominal learning

### 4.1 Initialization

Each method starts from its own method-appropriate fresh initialization for every independent root. No method begins from another algorithm's trained checkpoint.

### 4.2 Main common budget

Use a fixed number of **environment interactions/timesteps** as the principal common learning budget. Equal episode counts are not sufficient because episode lengths can differ between methods. Equal optimizer updates are also inappropriate because update semantics differ.

The final step budget is selected from non-final pilot learning curves and CPU feasibility. The aim is to capture both early/sample-efficient learning and sufficiently mature nominal performance without wasting compute after all methods have saturated.

### 4.3 Training measurements

Retain enough information to reconstruct and interpret learning without storing unbounded step-level training logs:

- environment interactions;
- episodic return and/or stable binned return rate;
- success/goal completion;
- episode length;
- truncation/timeout;
- collision count where defined;
- periodic evaluation checkpoint performance;
- wall-clock/CPU time;
- failed/invalid training runs.

### 4.4 Periodic evaluation

Raw online training return is not a fully fair cross-family performance measure because exploration and stochastic behavior differ. At predeclared step checkpoints, evaluate the current learned policy under a standardized **no-learning evaluation procedure** and a predeclared evaluation-action rule.

The evaluation policy must be method-appropriate and reproducible: for example greedy/inference Q action selection for value agents and normal inference policy behavior for stochastic policy agents. The exact stochastic/deterministic inference choice is frozen before final evidence and reported explicitly.

Training data remain useful for learning dynamics, but nominal method rankings should rely primarily on standardized evaluation checkpoints and final nominal evaluation rather than a single training trajectory.

## 5. Fair algorithm-specific tuning

Fairness does not require identical hyperparameters.

Before final freeze:

- define a small literature-backed candidate configuration set for each method;
- provide each method the same number of tested configurations, or a formally equivalent fixed optimization budget;
- use the same tuning interaction budget, tuning partitions and number of tuning roots;
- repeat each candidate configuration over multiple roots;
- predeclare the configuration-selection criterion and deterministic tie rule;
- retain failed, poor and unstable configurations;
- freeze selected configurations before final-reserve access.

Library defaults or RL-Zoo settings may inform the center/range of candidate configurations but may not be treated as automatically fair final values.

Historical v1.0 Q-learning settings remain historically valid. Protocol v2 may either include them as one candidate or justify a new bounded Q-learning tuning allowance so Q-learning does not receive asymmetrical prior optimization relative to new methods.

No lifetime tuning: the final non-stationary deployment schedule is not repeatedly used to optimize hyperparameters.

## 6. Method-specific trained state

The scientific checkpoint is whatever state is necessary to reproduce the learned policy and, for Continual deployment, resume the method's native learning process exactly.

Examples:

### Q-Learning / SARSA
- Q table;
- exploration/schedule state;
- algorithm RNG state;
- relevant counters.

### Dyna-Q / Dyna-Q+
- Q table;
- learned empirical model;
- planning RNG state;
- exploration state;
- recency/tau state for Dyna-Q+;
- relevant counters.

### DQN
- online network;
- target network;
- optimizer state;
- replay buffer and buffer position/policy;
- exploration schedule and counters;
- framework/agent RNG state;
- normalization/preprocessing state if any.

Replay-buffer retention/reset is a scientific intervention in non-stationary learning, not an implementation detail. Default v2 semantics should preserve the trained state when cloning Frozen/Continual branches. Any buffer reset or recency-biased replay requires an explicitly separate predeclared strategy.

### PPO / A2C
- policy and value-function parameters;
- optimizer state;
- learning-rate/schedule state;
- normalization state if any;
- RNG state;
- counters needed for exact continuation.

Checkpoint/deployment cloning occurs only at a valid algorithm boundary (e.g. completed PPO rollout/update), never midway through an update.

## 7. Phase B — matched resilience design

For each retained `method × root × layout`:

```text
trained method-specific checkpoint
        |
        +-- Frozen disturbed/change branch
        +-- Frozen matched nominal-reference branch
        +-- Continual disturbed/change branch
        +-- Continual matched nominal-reference branch
```

Frozen and Continual disturbed branches begin from the exact same trained state. Each regime's disturbed branch is compared to the same-regime nominal reference so continued training itself is not mistaken for an environmental-change effect.

Where scientifically valid, environment randomness is paired/common across compared branches to reduce nuisance variance without leaking hidden state.

## 8. Uncertainty/change taxonomy

### Primary persistent change

**Action remapping** remains the main adaptation condition because it creates an unannounced structural change in transition/action semantics and directly tests post-change adaptation.

The existing bounded two-action swap and four-action cycle are strong candidate severities, subject to v2 environment pilot compatibility.

### Supporting actuation uncertainty

**Action-execution failure** remains a stochastic robustness diagnostic. It probes resistance under noisy actuation rather than recovery from a persistent new rule.

### Supporting perceptual uncertainty

**Observation corruption** remains a stochastic information-quality diagnostic. It can induce observation ambiguity, so conclusions must acknowledge that memoryless policies do not solve a general POMDP. It should not be the sole basis for broad cross-method superiority claims.

Do not automatically add dynamic obstacles, reward changes, gradual drift or recurring changes. Additional mechanisms require a distinct RQ/diagnostic benefit that outweighs matrix growth.

## 9. Environment-discrimination pilot

The current 7×7 position-state GridWorld is a valid low-complexity anchor, but it may be too easy to discriminate deep and tabular learning families.

Pilot only a small bounded set of complexity levels in the project-owned environment, for example an easy anchor and one or two modestly harder structures. Exact sizes/layout counts are not precommitted here.

Complexity can increase through controlled structural features such as:

- grid dimensions;
- obstacle count/placement constraints;
- shortest-path structure;
- layout diversity;
- horizon matched to structural difficulty.

Selection rule: retain the **simplest** environment family that avoids obvious floor/ceiling effects for candidate methods, supports the uncertainty contract and remains CPU-feasible.

Do not introduce pixel vision, procedural-generation scale or partial observability solely to manufacture a reason for neural methods.

## 10. Pilot-gated method selection

The validated thesis machine is CPU-first. DQN/PPO/A2C are technically compatible with a discrete action space, but final feasibility must be measured locally with small MLPs and bounded budgets.

For each candidate, pilots assess:

- implementation correctness;
- nominal learning signal and variance;
- floor/ceiling behavior;
- time per interaction / training budget;
- checkpoint/resume fidelity;
- Frozen/Continual cloning feasibility;
- artifact size;
- information-boundary compliance.

A method may be excluded if it adds no discernible scientific contrast in the chosen environment, is unstable under a reasonable/fair bounded tuning budget, or makes the confirmatory matrix infeasible. The exact reason must be retained; exclusion is not allowed merely to simplify coding.

## 11. Statistical unit and primary estimands

Episodes within a training/evaluation run are repeated observations, not independent statistical replicates.

The independent unit remains rooted in independently initialized/environment-randomized roots, with layouts treated according to the predeclared aggregation plan.

### Learning phase primary candidates

- standardized final nominal evaluation performance;
- learning efficiency / time-average or area-under-standardized-evaluation-curve over a fixed interaction budget;
- explicit distribution/interval across roots.

Learning-curve AUC compresses temporal behavior and therefore should be accompanied by curves/checkpoint summaries, not used alone.

### Resilience phase primary roles

Preserve component interpretation:

- immediate degradation;
- cumulative deficit relative to the matched same-regime nominal reference;
- terminal/post-change performance or terminal gap.

Recovery/no-recovery remains secondary/sensitivity because threshold/stability definitions affect it.

### Contrasts

Prioritize a small set of interpretable contrasts instead of every pairwise comparison:

1. **Within each method:** Continual − Frozen adaptation benefit.
2. **Frozen across methods:** intrinsic resistance without online adaptation.
3. **Continual/adaptation-benefit across selected mechanism families:** predeclared method contrasts, with Q-Learning as a natural classical baseline where useful.

Report effect sizes and 95% uncertainty intervals. If formal p-value families are added, multiplicity handling must be predeclared; the default emphasis is estimation, not binary significance labels.

## 12. Root count and matrix size

Do not automatically reuse 32 final roots simply because v1.1 used 32.

After non-final pilots, estimate variability/precision and measured CPU cost. Choose a root count that supports defensible interval precision for the predeclared primary estimands within realistic compute. Few-run deep-RL comparisons are known to be unreliable; conversely, running an unnecessarily large factorial matrix can make the thesis infeasible.

If matrix size must be reduced, reduce low-value axes first (secondary methods, redundant conditions/severities or excessive layouts), not statistical rigor through best-seed selection.

## 13. Reused versus new evidence

### Reusable as historical/foundational evidence

- protocol-v1.0 and immutable F0/C0 final evidence;
- historical R0 negative pilot evidence;
- environment/information/RNG/provenance infrastructure;
- resilience metric definitions and known-answer validation;
- v1.1 implementation work for SARSA, Dyna-Q/Dyna-Q+ and paired-statistics concepts where semantically applicable;
- runtime observer/service infrastructure, after adapting schemas to v2.

### Must be newly generated for v2 confirmatory claims

- independent method training evidence;
- v2 tuning selections;
- environment-discrimination pilot/freeze evidence;
- trained method checkpoints;
- v2 Frozen/Continual resilience runs;
- v2 cross-method analysis and final figures/tables.

Historical runs that were not generated under the v2 comparison contract cannot become v2 confirmatory evidence by relabelling.

## 14. Protocol lifecycle

```text
RESEARCH DESIGN
    -> IMPLEMENTATION / DEVELOPMENT
    -> TUNING
    -> ENVIRONMENT + METHOD PILOT
    -> RESOURCE / VARIANCE REVIEW
    -> CANDIDATE V2 FREEZE
    -> FINAL RESERVE EXECUTION
    -> VALIDATION / STATISTICS / EVIDENCE PACKAGE
```

Final partitions remain fail-closed until the candidate is frozen and all upstream gates pass.

## 15. Current blockers / next work

Before implementing deep agents, complete:

1. bibliography intake/verification for missing primary/methodology sources;
2. exact v2 RQ/estimand freeze;
3. common agent training/checkpoint interface specification;
4. bounded Windows CPU feasibility plan.

Do not run the old T-522 v1.1 tuning matrix. Do not redesign the UI yet. Do not access any final reserve.
