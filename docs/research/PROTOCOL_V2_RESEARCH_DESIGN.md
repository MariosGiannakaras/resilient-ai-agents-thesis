# Protocol v2 Research Design

**Status:** source-backed research contract; bibliography promotion and machine-dependent values remain gated  
**Decision:** DEC-048  
**Tracker:** #95  
**Historical authority:** protocol-v1.0 remains immutable; candidate v1.1 remains auditable non-final history

## 1. Thesis-level research objective

The thesis studies how resilient reinforcement-learning agents behave under uncertainty and environmental change. GridWorld is the controlled diagnostic testbed and visualization mechanism, not the thesis subject.

Protocol v2 separates two questions that must not be collapsed:

### RQ-A — nominal learning

Under a common controlled environment/information/resource contract, how do scientifically distinct RL methods differ in learning efficiency, standardized nominal performance, variability and computational cost?

### RQ-B — resilience/adaptation

Starting from each method's own trained checkpoint, how do Frozen and ordinary-training Continual deployment regimes differ in immediate resistance, cumulative performance loss and terminal/post-change performance under matched uncertainty/change conditions?

Secondary analyses may examine relationships between nominal learning and resilience and sensitivity to uncertainty class. Directional hypotheses require source support or pre-final pilot justification before the final statistical freeze.

## 2. Methodology verdict after chained research

### Stays

- Phase A independent method-native learning.
- Phase B exact own-checkpoint cloning into Frozen/Continual × changed/no-change references.
- Environment interactions/timesteps as the main common Phase-A learning budget.
- Periodic standardized no-learning evaluation.
- Core candidates Q-Learning, SARSA, DQN, PPO and Dyna-Q+.
- Component-level resilience interpretation and root-level paired designs where valid.
- Current three uncertainty mechanisms, with distinct roles.

### Changes

- Dyna-Q becomes a targeted Dyna-Q+ planning-versus-recency ablation, not an automatic full final arm.
- A2C is not a default full final arm; it is only a bounded fallback/diagnostic if later evidence establishes a distinct unresolved contrast beyond PPO.
- DQN replay contents/cursor/policy are explicit scientific checkpoint state; reset or recency-biased replay is a separate intervention.
- PPO-like cloning is allowed only at a completed rollout/update boundary.
- Loss of plasticity/interference is an interpretation risk for ordinary continued deep training; no mitigation enters the matrix without a separate RQ.
- Environment complexity is selected by a predeclared ordered discrimination rule, not by preferred algorithm rankings.
- The three uncertainty classes are not pooled into one undifferentiated resilience claim.
- Historical v1.0/v1.1 evidence is never numerically pooled into v2 confirmatory estimates.

### Pilot-gated

Final retained methods, environment complexity, interaction budget, evaluation cadence, hyperparameters/update schedules, final roots/layouts, selected cross-method contrasts and confirmatory matrix size.

### Rejected as default protocol choices

Equal episode counts; equal optimizer updates; best-seed selection; treating seeds as tuning variables; library defaults as automatically fair; arbitrary DQN replay reset; pixels or partial observability solely to justify neural methods; adding redundant agents/conditions for variety; specialized continual-learning mitigations without a distinct RQ; composite resilience scores; and numerical pooling of historical and v2 confirmatory evidence.

## 3. Candidate method-role matrix

| Method | Family | Policy relation | Representation | Distinct scientific role | Current role |
|---|---|---|---|---|---|
| Q-Learning | value-based | off-policy | tabular | classical tabular baseline | core candidate |
| SARSA | value-based | on-policy | tabular | clean on-policy tabular contrast | core candidate |
| DQN | value-based | off-policy | neural | function approximation + replay + target network | core candidate |
| PPO | actor-critic / policy optimization | on-policy | neural | clipped policy-gradient / actor-critic contrast | core candidate |
| Dyna-Q+ | learned-model planning | off-policy-style Q updates | tabular/model | planning + explicit recency-directed re-exploration | core candidate |
| Dyna-Q | learned-model planning | off-policy-style Q updates | tabular/model | isolates planning from Dyna-Q+ recency bonus | targeted ablation only |
| A2C | actor-critic | on-policy | neural | overlaps PPO at family/mechanism level | fallback/diagnostic only |
| Random | non-learning reference | n/a | n/a | lower behavioral reference/correctness check | reference only; never fair-ranked |
| Historical R0 | robust planner | n/a | model/prior based | historical pre-deployment robustness attempt | immutable negative/diagnostic history |

No method is retained merely because it is popular. Each final method must add a distinct scientific contrast and pass the declared feasibility/discrimination gate.

## 4. Common information and representation contract

Every scientific method receives the same semantic online information allowed by the protocol. The existing evaluator/agent separation remains non-negotiable.

Agent-visible information may include delivered observation, intended action, reward and lifecycle information required by the algorithm. Evaluator-only truth can include true state under observation corruption, executed action, disturbance/change flags, regime identity and hidden action mappings. UI/analysis may inspect evaluator truth, but it never enters the agent transition/update path.

Tabular agents may receive the canonical discrete state. Neural agents may receive a deterministic vector/one-hot encoding of exactly the same semantic information. Pixels, extra map channels, change flags, hidden mappings or other evaluator truth are not introduced to favor deep methods.

## 5. Phase A — independent nominal learning

### 5.1 Initialization and independent unit

Each method starts from method-appropriate fresh initialization for every root. No method begins from another algorithm's trained state. Root/run is the independent randomization unit; episodes inside a run are repeated/nested observations, not independent replicates.

### 5.2 Main common budget

Use a fixed number of **agent-environment interactions/timesteps** as the principal common learning budget. Equal episode counts are unfair when episode lengths differ. Equal optimizer updates are also inappropriate because update semantics differ across families. Wall-clock/CPU time is a measured resource outcome, not the main fairness currency.

The exact interaction budget is selected only after the non-final Windows feasibility/discrimination pilot and later tuning/precision review. It must be large enough to expose early/sample-efficient learning and mature nominal performance without wasting compute after saturation.

### 5.3 Standardized no-learning evaluation

Raw online training return is not the primary cross-family policy-quality measure because exploration and stochastic action sampling differ.

At predeclared training-step checkpoints:

1. freeze learner updates;
2. evaluate on a standardized evaluation schedule with no training-state mutation;
3. use the predeclared method-appropriate inference action rule;
4. record evaluation interactions separately from the training budget;
5. restore/continue training without contaminating learner RNG/state unless the frozen contract explicitly uses isolated evaluation RNG streams.

The deterministic-versus-stochastic PPO inference rule is frozen before confirmatory evidence and reported explicitly. The evaluator never supplies information unavailable during normal agent interaction.

### 5.4 Phase-A measurements

Retain enough information to reconstruct learning without unbounded step logs:

- training environment interactions;
- episode return/success/goal completion/length/truncation and collisions where defined;
- standardized evaluation-checkpoint performance;
- final standardized nominal evaluation;
- failed/invalid training runs;
- wall-clock and CPU time;
- artifact/checkpoint size where relevant.

Learning-curve AUC may summarize sample efficiency only alongside the actual curves/checkpoint summaries; it is never the sole learning result.

## 6. Fair method-specific tuning contract

Fairness does not require identical hyperparameters. It requires comparable opportunity and predeclared selection rules.

Default tuning contract before final freeze:

- define method-specific, literature-backed bounded parameter ranges/configuration sets;
- use one common predeclared configuration/search opportunity across retained methods;
- use the same tuning-only root and environment partitions;
- use the same Phase-A training interaction budget per candidate configuration unless a single common alternative rule is frozen beforehand;
- repeat candidate configurations over multiple independent tuning roots;
- predeclare the configuration-selection metric and deterministic tie rule;
- retain failed, poor and unstable configurations;
- freeze selected configurations before final-reserve access.

Library defaults or RL-Zoo settings may seed the ranges but are not privileged as fair final settings. Seeds are randomization variables and never tuned. Historical v1.0 Q-learning settings may be one Q-Learning candidate but do not remove Q-Learning's right to the same bounded tuning opportunity as new methods.

Alternative sequential/Bayesian search is allowed only if a single equivalent search-budget rule is frozen for all retained methods before tuning; do not mix generous adaptive search for one family with a fixed handful of defaults for another.

The known complete final non-stationary lifetime/schedule is never repeatedly used for configuration selection. Development/tuning partitions precede configuration freeze and final reserve.

## 7. Method-specific scientific state

The scientific checkpoint is all state necessary to reproduce the learned policy and, for Continual deployment, resume native learning faithfully.

### Q-Learning / SARSA

- Q table;
- exploration/schedule state;
- relevant counters;
- algorithm RNG state.

### Dyna-Q / Dyna-Q+

- Q table;
- learned empirical model;
- planning state and planning RNG;
- exploration/schedule state;
- Dyna-Q+ recency/tau state;
- relevant counters and RNG.

### DQN

- online network;
- target network;
- optimizer state;
- replay-buffer contents, capacity, logical size, cursor/position and sampling policy/state;
- exploration schedule and counters;
- preprocessing/normalization state if used;
- framework/agent RNG state required for faithful continuation.

Normal library model serialization is not assumed to contain replay state; the project adapter must validate exact scientific resume. Replay reset, recency-biased replay or any other stale-experience handling is a separate scientific intervention. The default exact-clone semantics preserve the trained replay state because both Frozen/Continual scientific origins must be identical, not because replay preservation is assumed optimal.

If cheap and reproducible, pilot diagnostics may record replay age or pre-change/post-change mixture for interpretation. Such diagnostics do not alter the buffer.

### PPO-like actor-critic

- policy and value-function parameters, including shared feature state where applicable;
- optimizer state;
- learning-rate/schedule state;
- observation/reward normalization state if used;
- counters required for rollout/update continuation;
- relevant framework/agent RNG state.

Checkpoint/deployment cloning occurs only after a completed rollout and optimizer-update boundary. Never snapshot halfway through a rollout/update and label it an exact scientific checkpoint.

## 8. Phase B — matched resilience/adaptation design

For each retained `method × root × layout`:

```text
trained method-specific checkpoint
        |
        +-- Frozen disturbed/change branch
        +-- Frozen matched nominal-reference branch
        +-- Continual disturbed/change branch
        +-- Continual matched nominal-reference branch
```

Frozen and Continual start from the exact same trained scientific state. Each disturbed branch is compared with the same-regime nominal reference so the effect of continued training itself is not mistaken for the effect of environmental change.

**Frozen:** no scientific learning-state update after deployment. Inference-only counters needed for logging may change only if they are explicitly excluded from learning state and cannot influence behavior.

**Continual:** ordinary method-native training continues with a predeclared update/exploration schedule. It is a naive continued-training adaptation baseline, not a specialized continual-RL method.

Where scientifically valid, common environment randomness is paired across compared branches to reduce nuisance variance without leaking evaluator truth. The exact four-branch layout is a project causal-isolation design; it is not presented as a universally standardized RL protocol.

## 9. Deep continual-training interpretation

Ordinary gradient updates after a change do not guarantee effective adaptation. Deep agents may exhibit loss of plasticity, primacy effects, catastrophic interference/forgetting or stale-experience effects.

Protocol implications:

- interpret Continual DQN/PPO as ordinary continued training only;
- do not describe them as specialized continual-learning algorithms;
- retain poor adaptation/non-recovery rather than repairing it post hoc;
- allow only low-cost pilot diagnostics that help interpret failures without changing the algorithm;
- do not add resets, regularizers, reinitialization, shrink-and-perturb, special replay management or other plasticity-preserving mechanisms to the default final matrix without a distinct RQ and pilot justification.

## 10. Uncertainty/change taxonomy and claim separation

### Primary adaptation condition — action remapping

Persistent action remapping is an abrupt unannounced change in transition/action semantics. It is the primary test of post-change adaptation. Existing two-action swap/four-action cycle severities remain candidates subject to environment compatibility and final matrix sizing.

### Supporting robustness condition — action-execution failure

Action-execution failure is stationary/stochastic actuation noise. It probes robustness under unreliable execution, not recovery from a persistent new regime.

### Supporting perceptual condition — observation corruption

Observation corruption is stochastic information-quality/perceptual uncertainty. It may make the agent's effective observation process ambiguous or POMDP-like. It remains supporting evidence and is not used alone for broad cross-method superiority claims.

These mechanisms are analyzed as distinct condition families. No single aggregate claim implies that adaptation to persistent dynamics change, robustness to actuation noise and robustness to perceptual corruption are the same capability.

Dynamic obstacles, reward changes, gradual drift, recurrent tasks and other mechanisms are not added for variety. They remain limitations/future work unless explicitly promoted before protocol freeze.

## 11. Environment-discrimination pilot

The current 7×7 position-state GridWorld is a valid low-complexity anchor but may create ceiling effects.

Before any environment outcome is observed for the v2 discrimination decision:

1. define a small ordered ladder of project-owned complexity levels using only controlled structural changes such as grid dimensions, obstacle structure/count, shortest-path complexity, layout diversity and a horizon scaled to structural difficulty;
2. freeze the shared information/action/reward/uncertainty semantics across that ladder;
3. freeze development roots and provisional non-final method configurations used only for discrimination;
4. freeze a simple pass/fail discrimination rule for universal floor/ceiling behavior and CPU feasibility;
5. select the **lowest-complexity** level that is not universally trivial and not universally unsolved across the core candidate set, still supports the uncertainty contract and is feasible on the thesis machine.

A method-specific failure is retained as evidence and does not by itself authorize moving to another level. Likewise, a preferred cross-method ordering must not influence level selection. If no level passes, revise the ladder/feasibility assumptions transparently before final freeze rather than choosing the most attractive ranking post hoc.

Do not introduce pixel vision, procedural-generation scale or partial observability solely to manufacture a neural-method advantage. Generalization to unseen procedural levels remains a limitation/future-work topic unless it becomes an explicit RQ before freeze.

## 12. Pilot-gated method selection and CPU feasibility

The validated thesis machine is CPU-first: Windows 10, Ryzen 5 2600X, about 32 GiB RAM, Radeon RX 570 without a validated CUDA/NVIDIA backend, native Windows CPython 3.12 + `uv`.

Compact vector-state MLP DQN/PPO are technically compatible with this baseline; feasibility is not inferred from GPU assumptions. Exact throughput, stability and matrix cost must be measured on the physical thesis machine.

Core-method pilot checks:

- implementation correctness and information-boundary compliance;
- nominal learning signal/variance and universal floor/ceiling status;
- wall/CPU time per declared interaction budget;
- exact checkpoint/resume fidelity;
- exact Frozen/Continual clone fidelity;
- artifact size;
- failures/instability under the bounded non-final configuration allowance.

A method may be excluded if it adds no distinct scientific contrast in practice, fails a reasonable bounded feasibility/correctness gate, or makes the confirmatory matrix infeasible. The reason is retained. Compute reduction removes secondary/redundant arms/conditions before weakening statistical rigor through best-seed selection.

## 13. Metrics and statistical design

### Phase-A primary/secondary roles

Primary candidates:

- standardized final nominal evaluation performance;
- learning efficiency over a fixed interaction budget using checkpoint curves and, where useful, an AUC/time-average summary accompanied by those curves;
- root-level distribution/uncertainty of those outcomes.

Computational cost and failure rate are mandatory reported outcomes but not fairness-normalized into the primary learning budget.

### Phase-B primary roles

- **Immediate degradation:** short-horizon loss immediately after disturbance/change relative to the matched same-regime nominal reference.
- **Cumulative deficit:** integrated/cumulative performance shortfall versus the matched same-regime nominal reference over the fixed post-change horizon.
- **Terminal performance/gap:** standardized end-of-horizon performance or remaining reference gap.

Recovery/no-recovery is secondary/sensitivity because threshold/stability definitions can materially alter it. No composite resilience score is used.

### Statistical hierarchy

- Root/run is the independent randomization unit.
- Episodes/checkpoints within a root are nested repeated observations.
- Layouts are handled under a frozen aggregation/hierarchical plan; they are not silently treated as independent roots.
- Use paired root/layout differences where common randomness is valid.
- Report effect sizes and 95% uncertainty intervals/bootstraps appropriate to the root-level estimand.
- Do not mechanically apply multi-task benchmark aggregates such as IQM when the experimental unit/hierarchy does not match that setting.
- Retain raw per-root data, negative/null/failed/non-recovery outcomes and predeclared exclusions with reasons.

### Confirmatory contrast family

Limit primary contrasts to:

1. **Within each retained method:** Continual − Frozen adaptation benefit.
2. **Frozen across retained methods:** intrinsic resistance without online adaptation.
3. **Selected cross-method Continual/adaptation-benefit contrasts:** only where a specific mechanism-level rationale is frozen beforehand.

Do not declare every pairwise comparison confirmatory. If formal p-values are used, multiplicity handling is frozen before final evidence; the default emphasis remains effect estimation with uncertainty.

### Root count

Do not copy v1.1's root count. Use non-final root-level variance, desired interval precision and measured runtime from the actual thesis machine. Deep-RL few-run uncertainty is a reason to size roots deliberately, not to report favorable seeds.

## 14. Historical evidence boundary

### Reusable historical/foundational evidence

- immutable protocol-v1.0 and FINAL-* evidence for their original within-Q-learning estimands;
- historical R0 negative pilot evidence;
- environment/information/RNG/provenance infrastructure;
- component resilience metric definitions and known-answer validation;
- v1.1 SARSA/Dyna-Q/Dyna-Q+ implementation concepts and paired-statistics infrastructure where semantics remain valid;
- runtime observer/service infrastructure after v2 schema adaptation.

### Must be newly generated for v2 confirmatory claims

- independent Phase-A training evidence for every retained method;
- v2 tuning selections;
- environment-discrimination/feasibility evidence;
- method-specific trained scientific checkpoints;
- v2 Frozen/Continual branches and nominal references;
- v2 cross-method analysis, figures and tables.

Protocol-v1.0 may be discussed separately as a foundational experiment and compared narratively with v2. Candidate v1.1 may be discussed as an adaptation-mechanism design. Neither is numerically pooled with v2 confirmatory estimates because the protocol, estimands and training provenance differ.

## 15. Bibliography/provenance boundary

`MariosGiannakaras/ThesisBibliography` is the canonical bibliography source of truth. The accepted thesis import `bibliography-integration-v3` remains immutable.

The 2026-08-27 chained research first deduplicated by content/title/identifier. Existing sources are reused/re-evaluated instead of duplicated. Genuine methodology gaps are upstreamed through ThesisBibliography issue #135 and its canonical intake/analysis/evidence/selection workflow. Formal citation support enters this repository only through a later versioned synchronization after upstream validation; do not hand-copy formal citations into the thesis repo.

Until that sync completes, `T-524` remains IN_PROGRESS even though the methodology verdict is recorded.

## 16. Protocol lifecycle

```text
SOURCE-BACKED RESEARCH / RQ FREEZE
    -> BOUNDED PILOT INFRASTRUCTURE
    -> ENVIRONMENT + METHOD + CPU FEASIBILITY PILOT
    -> FAIR TUNING + PRECISION/RUNTIME SIZING
    -> MACHINE-READABLE V2 CANDIDATE/STATISTICS FREEZE
    -> FINAL RESERVE EXECUTION
    -> VALIDATION / STATISTICS / EVIDENCE PACKAGE
```

Final partitions remain fail-closed until the candidate/statistical plan is frozen and all upstream gates pass.

## 17. Next implementation package after T-524

`T-525` is deliberately bounded. It does **not** perform final tuning or expand the final matrix. It implements only what the pilot contract needs:

1. method-agnostic independent training lifecycle and interaction accounting;
2. standardized no-learning evaluation with isolated evaluation state/RNG;
3. a scientific-checkpoint interface with exact round-trip fidelity assertions;
4. exact Frozen/Continual clone construction and nominal references;
5. minimum maintained-library adapters for DQN/PPO plus the existing tabular/planning candidates;
6. method-specific configuration/provenance serialization;
7. targeted deterministic tests for information leakage, budget accounting, checkpoint fidelity and clone equality.

A2C is not part of the default T-525 full adapter set. Dyna-Q is implemented/reused only as the already-existing targeted ablation capability.

After T-525, `T-526` must run on the validated physical Windows thesis machine. Hosted Linux CI may validate deterministic software contracts but cannot satisfy the CPU/runtime/environment-discrimination evidence gate.

Do not run old T-522, redesign the UI, access any final reserve, or start thesis writing.
