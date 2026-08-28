# Protocol v2 Complete Thesis Study Plan

**Status:** complete end-to-end study blueprint; exact machine-dependent values remain T-526/T-527 gated  
**Authority:** DEC-048, DEC-050, `PROTOCOL_V2_RESEARCH_DESIGN.md`, `PROTOCOL_V2_BACKEND_CONTRACT.md`  
**Purpose:** define the smallest complete research program that can generate the thesis-ready protocol-v2 evidence without outcome-driven expansion or manual run construction.

## 1. Research program objective

The final study is one automated research program with two primary research questions and two bounded supporting analyses.

### RQ-A — Nominal learning

Under the same controlled task, semantic information contract and actual environment-interaction budget, how do scientifically distinct reinforcement-learning methods differ in:

- standardized nominal policy performance;
- learning/sample efficiency;
- variability across independent roots;
- computational and artifact cost?

### RQ-B — Resilience and adaptation

Starting from each method/root/layout's own exact trained scientific checkpoint, how do matched Frozen and Adaptive deployment regimes differ under environmental change/uncertainty in:

- immediate degradation/resistance;
- cumulative performance deficit;
- terminal post-change policy quality;
- adaptation benefit relative to same-regime nominal references?

### Supporting analysis S1 — uncertainty-family specificity

Determine whether conclusions are specific to persistent action-semantic change, stochastic actuation failure or perceptual corruption. These families are never pooled into one generic resilience score.

### Supporting analysis S2 — Dyna mechanism ablation

Compare Dyna-Q+ with matched Dyna-Q where needed to isolate the value of recency-directed re-exploration beyond planning alone. Dyna-Q is not a general sixth ranked method.

## 2. Study architecture: development is not final evidence

The study uses a strict funnel.

1. **T-526 environment/method/severity feasibility** — non-final development evidence only.
2. **T-527 fair tuning and precision/runtime sizing** — non-final development evidence only.
3. **Protocol-v2 freeze** — immutable machine-readable final recipe, final layouts, roots, method configurations, budgets, probes, branch lifecycle and statistical plan.
4. **Confirmatory Phase A** — final independent nominal learning.
5. **Confirmatory Phase B** — final matched resilience/adaptation from Phase-A checkpoints.
6. **Evidence validation/freeze** — no silent replacement of scientific failures.
7. **Predeclared statistical analysis** — root-level blocked/paired estimands.
8. **Thesis-ready artifact generation** — figures, tables, root-level data, provenance and interpretation boundaries.

Pilot/tuning outcomes may be reported as methodology/appendix evidence, but they are not pooled with confirmatory estimates. The final matrix is never changed after final-reserve outcomes are inspected.

## 3. Environment design

T-526 selects the lowest-complexity level in the predeclared 7x7 -> 10x10 -> 14x14 ladder that avoids universal floor/early-ceiling behavior and remains feasible on the validated Windows CPU machine. Selection never uses a preferred method ranking.

After level selection:

- development/tuning uses declared development layouts at that complexity;
- before final execution, T-527 freezes **two held-out final layouts** matched to the selected structural complexity and task semantics;
- final layouts are not used to choose method hyperparameters, severities or root count;
- once the final reserve opens, every retained method is trained on each final layout because zero-shot layout generalization is not the thesis question.

The known shortest-path solution is retained as evaluator-only solvability/ceiling context. A Random policy is retained as a cheap behavioral floor/calibration reference. Neither receives fair-ranking status and neither leaks evaluator information to learning agents.

## 4. Method set

### Core confirmatory methods

The default final core, subject only to T-526/T-527 feasibility evidence, is:

1. Q-Learning — tabular off-policy value learning.
2. SARSA — tabular on-policy value learning.
3. DQN — neural off-policy value approximation with replay and target network.
4. PPO — neural on-policy policy optimization / actor-critic.
5. Dyna-Q+ — learned-model planning with recency-directed re-exploration.

### Supporting methods

- **Dyna-Q:** targeted mechanism ablation only, principally for nominal Dyna comparison and primary persistent action-remap conditions.
- **A2C:** no default final arm. It is promoted only if T-526/T-527 establishes distinct scientific value beyond PPO at acceptable matrix cost.
- **Random:** calibration floor only.
- **Historical R0:** immutable historical negative/diagnostic evidence; never pooled with v2.

If compute reduction is necessary, remove redundant/supporting arms before reducing root-level statistical rigor.

## 5. T-526 development pilot

Run the committed physical Windows feasibility plan exactly once per its retained evidence rules.

It determines:

- selected GridWorld complexity;
- actual CPU throughput by method;
- checkpoint/artifact footprint;
- method feasibility/failure modes;
- viable interaction/probe cadence;
- whether the current core method set is retainable;
- non-degenerate candidate severities for supporting uncertainty families;
- whether the post-boundary persistent regime can span episode resets without ambiguity.

### Severity calibration rule

Candidate severities are development-only. Final supporting severity is selected using a predeclared pooled/non-degeneracy rule, never because it favors a method.

- **Action remapping:** retain both declared categorical mappings if both are valid and non-degenerate; they are not ordered as scalar low/high severity.
- **Action failure:** select one representative final probability from the bounded pilot candidates, with lower/higher candidates retained as development sensitivity evidence if useful.
- **Observation corruption:** freeze both occurrence probability and corruption support/magnitude. Prefer one interpretable non-degenerate final perceptual condition; any harsher global-valid-cell condition may remain a supporting sensitivity rather than becoming a second primary family.

## 6. T-527 fair tuning and freeze

Each retained method receives equivalent predeclared tuning opportunity on development-only roots/layouts.

The tuning process must freeze before final reserve access:

- one selected method configuration per retained method;
- common task-level reward semantics and gamma;
- Phase-A actual interaction budget;
- no-learning probe grid;
- Phase-B pre-boundary prefix rule, post-boundary interaction horizon and probe grid;
- final multi-episode reset/regime semantics;
- final uncertainty conditions;
- final root count from precision/runtime evidence;
- primary contrast family and multiplicity rule if p-values are retained;
- deterministic tie/selection rules;
- final layouts and all seed/root identities.

### Root-count rule

Do not choose roots by convention. Use T-526/T-527 root-level variance and runtime to select the smallest N meeting the predeclared precision target for the principal Phase-A and Phase-B estimands, subject to a bounded maximum compatible with the thesis machine. Root is the independent randomization unit; adding episodes is not a substitute for adding roots.

## 7. Confirmatory Phase A — nominal learning

For every retained `method x final root x final layout`:

1. create method-appropriate fresh initialization;
2. train to the exact frozen actual-interaction budget;
3. run standardized no-learning probes at all frozen interaction checkpoints using clone/isolation semantics;
4. record online training diagnostics separately from no-learning policy-quality probes;
5. produce one exact final scientific checkpoint;
6. validate checkpoint restore/continuation provenance;
7. retain failures rather than choosing replacement seeds.

### Phase-A primary outcomes

1. **Final standardized no-learning evaluation return** at the frozen endpoint.
2. **Learning efficiency** from the full standardized evaluation curve, summarized by equal-grid AUC/time-average together with the curve itself.

### Phase-A secondary outcomes

- success rate;
- truncation rate;
- episode/path length and path inefficiency where interpretable;
- collisions;
- online training return;
- wall time and process CPU time;
- method-native update counts;
- checkpoint/artifact size;
- scientific failure rate.

### Phase-A comparisons

All method estimates are shown descriptively, but confirmatory cross-method contrasts are limited to mechanistically meaningful predeclared comparisons rather than treating every pair as an independent discovery claim. Candidate families to freeze at T-527 include:

- Q-Learning vs SARSA — off-policy vs on-policy tabular learning;
- Q-Learning vs DQN — tabular vs neural off-policy value learning;
- DQN vs PPO — replay/value-based vs on-policy actor-critic optimization;
- Q-Learning vs Dyna-Q+ — model-free vs learned-model planning/re-exploration.

Dyna-Q+ vs Dyna-Q is handled as the targeted mechanism ablation.

## 8. Confirmatory Phase B — resilience/adaptation

Each Phase-B unit starts from the exact Phase-A checkpoint for the same `method x root x layout`.

A shared no-learning pre-change prefix may be used if frozen in T-527. At the exact causal boundary, fork the full learner + behavior + RNG + GridWorld state into four branches for each disturbance condition:

1. Frozen nominal (FN)
2. Frozen disturbed (FD)
3. Adaptive nominal (AN)
4. Adaptive disturbed (AD)

Frozen branches never mutate scientific learning state. Adaptive branches continue ordinary method-native learning only from the first post-boundary transition. No replay, epsilon, optimizer, target-network, model, recency, warm-up or learning-rate reset occurs at the boundary.

### Multi-episode regime semantics

The final default to freeze in T-527 should be:

- disturbance/change becomes active once at the boundary;
- it remains active across all subsequent episode resets for the disturbed branch;
- reset changes episode/environment start state according to predeclared seed streams but does not remove/retrigger the regime;
- learner state persists across resets;
- nominal branches follow the identical reset schedule without the disturbance;
- post-boundary opportunity is an exact common actual-interaction horizon.

This makes persistent action remapping a genuine changed deployment regime rather than a repeatedly reintroduced episode event.

## 9. Final Phase-B condition matrix

Use the smallest matrix that answers the thesis questions completely.

### Primary persistent change

Run **both predeclared action-remap mappings** for every core method/root/final layout:

- two-action swap (`swap-right-down`);
- four-action categorical cycle (`cycle-clockwise`).

Both use the full four-branch design. Mapping-specific effects are reported separately; an equal-weight across-mapping summary may be predeclared as the primary action-remap family summary.

### Supporting actuation uncertainty

Run **one pilot-calibrated representative action-failure probability** for every core method/root/final layout, again with FN/FD/AN/AD.

Other candidate probabilities remain development/sensitivity evidence rather than multiplying the final confirmatory matrix.

### Supporting perceptual uncertainty

Run **one pilot-calibrated observation-corruption condition** for every core method/root/final layout, with explicit probability and support/magnitude, again with FN/FD/AN/AD.

Do not pool this with action remapping or action failure into a composite resilience score.

### Dyna mechanism ablation

Run Dyna-Q on the final nominal-learning study and on the two primary action-remap conditions only. Compare Dyna-Q+ vs Dyna-Q with matched planning budget/configuration wherever possible so the contrast isolates recency-directed re-exploration rather than unrelated tuning differences.

## 10. Phase-B estimands

For each condition, retain all four component cells. For a larger-is-better root/layout outcome Y:

- Frozen disturbance effect: `D_F = Y(FD) - Y(FN)`
- Adaptive disturbance effect: `D_A = Y(AD) - Y(AN)`
- Adaptation benefit: `AB = D_A - D_F`

The raw `AD - FD` contrast is retained as deployed online performance, but it is not substituted for the matched adaptation-benefit estimand.

### Primary component outcomes

1. **Immediate degradation / resistance** — short frozen post-boundary window relative to same-regime nominal reference.
2. **Cumulative deficit** — integrated post-boundary shortfall relative to same-regime nominal reference.
3. **Terminal gap / terminal policy quality** — final standardized no-learning probe relative to same-regime nominal reference.

Recovery time/no-recovery remains secondary because it depends strongly on threshold/stability choices.

### Online versus probe outcomes

Report both:

- **online deployed utility**, which includes exploration/adaptation cost;
- **standardized no-learning probe policy quality**, which isolates the learned policy more cleanly.

Never describe one as the other.

## 11. Statistical analysis

### Independent unit and blocking

- root/run is the independent randomization unit;
- layouts are repeated/blocking factors inside a root;
- episodes/checkpoints are nested observations, never independent sample-size inflation.

For a primary method/condition effect:

1. compute the within-layout effect for each root;
2. equal-weight the final layouts within the same root unless T-527 freezes another justified blocked estimator;
3. perform inference over the resulting root-level values.

### Default inference

The current primary candidate is:

- root-level mean effect;
- Student-t 95% confidence interval;
- root bootstrap/robust sensitivity;
- raw root-level points/distributions shown with the summary.

The prior synthetic closure stress test supports this default over a simple percentile bootstrap for the current small-N root-level design, but T-527 must recheck the choice against physical pilot behavior.

If formal p-values are reported, use only the frozen limited confirmatory contrast families and a predeclared family-wise correction such as Holm. Descriptive pairwise tables may contain effect estimates/CIs without turning every pair into a separate confirmatory hypothesis.

### Failure policy

- scientific/algorithmic failure is retained and counted;
- infrastructure invalidation reruns the same root identity and retains invalid-attempt provenance;
- performance summaries conditional on completion are accompanied by failure-rate reporting and a predeclared failure-aware sensitivity analysis;
- no failed/poor root is replaced with a new seed.

## 12. Confirmatory matrix size formula

Let:

- `M = 5` core methods unless T-526/T-527 changes the retained set;
- `L = 2` held-out final layouts;
- `N = final root count selected by precision/runtime sizing`;
- `C = 4` core Phase-B disturbance conditions: two action-remap mappings + one action-failure condition + one observation-corruption condition.

Then the core final matrix contains:

- Phase A: `M * L * N = 10N` independent method-layout training executions;
- Phase B: `M * L * N * C * 4 = 160N` branch segments;
- Dyna-Q supporting Phase A: `L * N = 2N` additional training executions;
- Dyna-Q action-remap ablation: `L * N * 2 * 4 = 16N` additional branch segments.

Total planned final scientific executions/segments before probe episodes and reference-only Random/oracle evaluations: **`188N`**.

Illustration only, not a frozen root count:

- `N=24` -> 4,512 executions/segments;
- `N=32` -> 6,016 executions/segments.

This formula is why supporting uncertainty uses one calibrated representative final severity rather than blindly crossing every pilot severity into the final matrix.

## 13. Automated final-study recipe

After T-527, generate one immutable machine-readable `protocol-v2.0` thesis-study recipe. The final application/CLI should offer a single **Run Thesis Study** orchestration path rather than requiring manual construction of runs.

The orchestrator should automatically:

1. validate machine/protocol/final-reserve firewall;
2. materialize all frozen roots/layouts/method configurations;
3. run/resume Phase-A jobs;
4. run isolated probes and exact checkpoint validation;
5. create all Phase-B condition/branch jobs from the correct checkpoints;
6. enforce matched root/layout/environment seed structure;
7. retain scientific failures and retry only infrastructure-invalid attempts with the same identity;
8. validate checksums/manifests/completeness;
9. freeze the final evidence set;
10. execute only the predeclared analysis;
11. generate the complete thesis evidence package.

No UI user should manually enter gamma, learning rate, replay size, PPO epochs, root seeds, probe cadence, branch identities or final severities for this mode.

## 14. Thesis-ready outputs

The final evidence package should generate at least the following automatically.

### Main figures

1. standardized Phase-A learning curves with uncertainty;
2. final nominal policy performance by method;
3. learning-efficiency/AUC effect estimates;
4. runtime/failure/artifact-cost diagnostics;
5. immediate action-remap degradation/resistance;
6. Frozen vs Adaptive cumulative deficit;
7. adaptation-benefit DiD forest/effect plot by method;
8. terminal post-change gap/policy-quality plot;
9. supporting action-failure and observation-corruption results, kept as separate families;
10. Dyna-Q vs Dyna-Q+ mechanism-ablation result.

### Main tables

1. final task/method/protocol configuration table;
2. Phase-A primary effects and 95% CIs;
3. Phase-B primary action-remap effects and adaptation benefits;
4. supporting uncertainty effects;
5. failures/runtime/checkpoint sizes;
6. Dyna mechanism-ablation results.

### Appendix/reproducibility artifacts

- all root-level estimates;
- all final method configurations;
- root/layout/seed identities;
- excluded/invalid infrastructure attempts and reasons;
- scientific failures;
- checkpoint/provenance hashes;
- environment/layout specifications;
- statistical-plan machine-readable configuration;
- analysis outputs and table/figure source data;
- T-526/T-527 development evidence clearly marked non-final.

## 15. Thesis claims this design can support

If executed and validated as frozen, the study can support bounded claims about:

- relative nominal learning behavior of the retained methods in the controlled low-dimensional GridWorld family;
- sample efficiency and computational cost under a common interaction-resource contract;
- intrinsic resistance to predeclared environmental changes/uncertainties;
- benefit or harm of ordinary continued learning after a change relative to a matched Frozen regime;
- whether adaptation effects differ across method families and uncertainty mechanisms;
- the specific contribution of Dyna-Q+ recency-directed re-exploration relative to Dyna-Q planning alone.

It does **not** support universal claims about RL resilience, real robotics, autonomous change detection, specialized continual-RL, unseen-layout generalization, high-dimensional perception or arbitrary non-stationarity.

## 16. Final user-facing workflow

The thesis-valid workflow should ultimately be almost fully automated:

`Run Thesis Study -> Monitor -> Validate -> Results -> Export`

A read-only review screen may show the frozen plan before execution, but final-study settings are not manually edited. Separate exploratory/custom-study mode may expose advanced controls, with unmistakable labeling that such runs are **not** part of the frozen thesis evidence.
