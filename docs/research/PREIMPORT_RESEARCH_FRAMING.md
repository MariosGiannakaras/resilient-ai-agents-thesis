# Pre-Import Research Framing Workspace

**Status:** `PROPOSED / PRE-IMPORT / NON-BINDING`  
**Date:** 2026-08-03  
**Purpose:** preserve evidence-led research framing work that can be completed before the first controlled bibliography import and target-system capability report.

## Gate boundary

This document is a research workspace, not a frozen thesis decision.

It does **not** satisfy the Phase 2 research-framing gate because:

1. `research/bibliography/` has not yet been populated through the controlled import workflow;
2. the target-system capability report has not yet been generated and accepted;
3. exact agent implementations and feasible training budgets have not been prototyped;
4. the final GridWorld implementation has not been selected through the prototype/ADR gate.

The current cross-repository bibliography synchronization is blocked by an invalid `BIBLIOGRAPHY_SYNC_TOKEN`. Direct inspection of the canonical `ThesisBibliography` repository is used here only to prepare the structure of later work. No canonical source identifiers are referenced in this document because source-ID validation begins only after the generated package is installed.

The candidate questions and constructs below must be revalidated against the imported manifest, analyses, evidence, actual machine capabilities, and the selected environment implementation before they can become `CONFIRMED` or `FROZEN`.

## Evidence-led framing principles

The canonical bibliography currently supports the following design principles strongly enough to guide a provisional workspace:

1. **Robustness and resilience must not be treated as synonyms.** A policy that preserves acceptable performance under a shift without further learning demonstrates robustness. A system that detects or experiences degradation and then improves through continued interaction demonstrates adaptation/recovery. Both can be compared, but their capabilities and allowed update regimes must be reported separately.
2. **Resilience is a temporal process.** Evaluation should preserve the performance trajectory around a disruption rather than compressing behavior into only final or average return.
3. **Immediate resistance and later recovery are different outcomes.** An agent can have a small initial performance drop but poor long-run adaptation, or a severe initial drop followed by fast recovery.
4. **Disturbance channels must be explicit.** Observation corruption, action-execution disturbance, and environment/rule change occur at different points in the agent-environment loop and must not be hidden inside one generic noise parameter.
5. **Severity and frequency are experimental factors.** The same disturbance family can produce materially different conclusions at different magnitudes, schedules, or recurrence patterns.
6. **Nominal utility must remain visible.** A conservative policy that performs poorly even before disruption must not appear resilient merely because its relative degradation is small.
7. **Environment, interaction regime, and analysis procedure jointly define an experiment.** The simulator alone does not define the scientific benchmark.
8. **Small GridWorld tasks are appropriate diagnostic environments when their limitations are stated.** Their value is controllability, interpretability, causal isolation, and reproducibility, not realism or universal external validity.
9. **Frozen-policy testing, online adaptation, and recurring-context recall are distinct evaluation regimes.** Results from one regime must not be described as evidence for another.
10. **Statistical uncertainty must be reported.** Multiple independent runs, raw per-run retention, uncertainty intervals, and effect-size-oriented summaries are required; best-run or single-run comparisons are invalid.

## Candidate research problem

The official thesis problem can provisionally be operationalized as follows:

> Compare decision-making agents with different robustness and adaptation capabilities in a controlled GridWorld, and evaluate how their task performance degrades and recovers when explicitly parameterized uncertainty or environmental changes are introduced.

This formulation deliberately leaves the following open:

- exact agents and algorithms;
- whether the final implementation is custom Gymnasium or a thin MiniGrid adaptation;
- grid dimensions and reward scale;
- exact uncertainty distributions;
- severity values;
- training and adaptation budgets;
- number of independent runs;
- statistical estimators used for final inference.

Those values require the remaining gates.

## Candidate main research question

**MRQ-P1 — provisional**

> How do decision-making agents with different robustness and online-adaptation capabilities differ in immediate performance degradation and post-change recovery under controlled uncertainty and abrupt environmental changes in a simple GridWorld?

### Why this is currently the strongest framing

- It maps directly to the official requirement to compare resilient AI agents under uncertainty and dynamic change.
- It makes recovery speed an explicit outcome rather than an informal observation.
- It permits comparison of frozen robust behavior with genuine online recovery without calling them the same capability.
- It does not require invention of a new algorithm.
- It supports a bounded empirical contribution using a small validated environment.
- It does not preselect deep versus tabular methods before hardware and feasibility checks.

### What would falsify or invalidate this framing

The MRQ should be replaced or narrowed if later evidence shows that:

- the feasible agent set does not contain scientifically distinct robustness/adaptation regimes;
- the selected GridWorld cannot represent the required uncertainty mechanisms without confounding the task definition;
- the target machine cannot execute the minimum fair comparison within a realistic thesis schedule;
- the supervisor requires a substantially different research contribution;
- a literature refresh identifies a more appropriate operational definition of resilience for the selected setting.

## Candidate secondary questions

### SRQ-P1 — disturbance dependence

> How do disturbance type and severity affect nominal performance loss, immediate degradation, and post-disruption performance across the compared agent capabilities?

**Rationale:** observation, action, and environment disruptions are not interchangeable. A method that performs well under one uncertainty channel should not be described as generally resilient.

### SRQ-P2 — frozen robustness versus online adaptation

> When online updates are permitted after a persistent environmental change, how does the recovery trajectory differ from the corresponding frozen-policy evaluation, and what nominal-performance or conservativeness trade-offs accompany that difference?

**Rationale:** this directly separates resistance from recovery and prevents a robust-but-conservative policy from being rewarded merely for having little additional degradation.

### SRQ-P3 — recurring versus novel context, conditional

> If the selected agent set contains a validated context-memory or model-reuse mechanism, how does recovery in a recurring previously encountered context differ from adaptation to a genuinely novel context?

**Status:** optional and conditional. This question must be dropped if it requires an extra agent family or experimental dimension that does not materially improve the thesis answer.

### Exploratory diagnostic — detector quality, conditional

For agents with an explicit change detector, record detection delay, precision/recall where definable, and the relationship between detection time and subsequent recovery. This is **not** a universal research question because agents without explicit detection should remain valid comparators.

## Minimum uncertainty taxonomy candidate

The provisional minimum taxonomy mirrors the official examples while maintaining separate intervention points.

### U1 — observation disturbance

Examples to prototype later:

- stochastic corruption of the observed state;
- masking or substitution of a bounded subset of observation features;
- controlled observation error with known severity and RNG stream.

Required trace distinction:

- ground-truth environment state;
- observation delivered to the agent.

Do not silently change the ground-truth transition when testing observation noise.

### U2 — action-execution disturbance

Examples to prototype later:

- intended action fails and becomes no-op;
- intended action is replaced by another valid action according to a controlled stochastic kernel.

Required trace distinction:

- intended action selected by the agent;
- action actually executed by the environment;
- disturbance event and probability/severity parameters.

### U3 — environment/rule change

Candidate mechanisms to choose later:

- transition-rule change;
- obstacle/topology change;
- movement-cost or reward-rule change.

The final design should select the smallest subset that represents a genuine rule/dynamics change without mixing several mechanisms in one condition.

### Excluded from the minimum set for now

The following may be scientifically interesting but should not be added unless they answer a distinct approved question:

- adversarial observation attacks;
- reward corruption as a separate fourth family;
- safety constraints/CMDPs;
- multi-agent disturbances;
- high-dimensional visual shifts;
- continuous-control physics variation;
- simultaneous compound disturbances.

## Disturbance timing proposal

Recovery can only be interpreted cleanly when the disturbance schedule is explicit.

### Persistent post-change regime — preferred for recovery

1. establish a nominal pre-change phase;
2. introduce a known experimental change point that is hidden from the agent;
3. keep the changed condition active for a predefined evaluation horizon;
4. permit or forbid agent updates according to the declared regime;
5. measure degradation and recovery relative to a nominal reference.

This regime avoids confusing agent recovery with automatic restoration of the environment.

### Transient disturbance regime — diagnostic only

Short-lived disturbances may be useful for immediate robustness tests, but recovery after the environment automatically returns to normal has a different interpretation. Such tests should not be the primary evidence for adaptive resilience.

## Candidate evaluation regimes

### R0 — nominal reference

No deliberate disturbance. Used to establish expected utility, variance, learning behavior, and reference performance curves.

### R1 — frozen-policy robustness

After the training checkpoint is frozen:

- no policy/value/model learning updates are allowed during shifted evaluation;
- the shifted environment is evaluated using the same declared interaction budget;
- results represent zero-shot robustness/generalization, not adaptation.

Agent-internal recurrent state must have an explicit reset policy so memory is not accidentally treated as online learning.

### R2 — online adaptation/recovery

After the change:

- the agent may update only the components allowed by its declared adaptation contract;
- the post-change interaction/update budget is recorded;
- the change variable itself remains hidden unless the algorithm scientifically assumes context observability;
- recovery is evaluated from the time series, not just the final checkpoint.

### R3 — recurring-context recall, optional

A previously encountered context reappears after one or more intervening contexts. This regime is used only if recall/retention is part of an approved agent capability. It must be distinguished from adaptation to a novel context.

## Candidate outcome constructs

No single scalar should initially stand for “resilience.” Preserve interpretable components and only derive a composite score if later literature/protocol review justifies it.

### Nominal task performance

Purpose: quantify the clean-performance cost of robustness/adaptation mechanisms.

Possible final estimands:

- mean or robust aggregate episode return;
- task success probability;
- path efficiency or episode length where task semantics justify it.

### Immediate degradation

Purpose: quantify resistance at or immediately after the change.

Candidate measurements:

- absolute performance drop from the matched nominal reference;
- relative degradation ratio when the denominator is well behaved;
- minimum post-change performance within a predefined window.

### Failure magnitude / failure profile

Purpose: characterize the depth and duration of disruption rather than a single point.

Candidate measurements:

- area between reference and disrupted performance curves during the failure interval;
- worst-window performance gap;
- duration below a predefined scientifically justified threshold.

### Recovery time

Purpose: operationalize the official “speed of recovery” requirement.

A final definition must specify:

- reference value or reference curve;
- recovery threshold;
- required stabilization duration;
- censoring rule if recovery does not occur within the evaluation horizon.

Do not choose the threshold after viewing final results.

### Recovery profile / area

Purpose: retain information when two agents reach a similar endpoint through different recovery trajectories.

Candidate summaries:

- area under the post-change performance curve;
- integrated performance relative to nominal reference;
- slope or piecewise rate estimates only if stable enough after pilots.

### Post-change asymptotic or end-window performance

Purpose: distinguish fast but incomplete recovery from slower convergence to a stronger final policy.

Use a predefined terminal evaluation window rather than the best observed value.

### Reliability across runs

Purpose: prevent conclusions from depending on a favorable seed or unstable training run.

Required reporting direction:

- all predefined independent runs retained;
- per-run distributions preserved;
- confidence intervals or compatible uncertainty intervals;
- no silent removal of failed or low-performing runs.

### Detector metrics, method-specific

Only for explicit detector-based agents:

- detection delay;
- precision/recall or event-level false-positive/false-negative counts;
- detector activation frequency;
- relation between detection and performance recovery.

## Statistical direction before pilot design

The final analysis plan is not yet frozen, but the canonical evaluation literature already rules out several weak practices.

Do not use:

- single-run comparisons;
- best-run selection;
- final point estimates without uncertainty;
- post-hoc removal of failed runs;
- a single grand average that hides disturbance type and severity;
- p-values as the sole evidence of practical superiority.

Pilot work should determine whether final reporting can use:

- per-condition effect estimates with bootstrap confidence intervals;
- probability-of-improvement style comparisons where meaningful;
- robust aggregate statistics where the scenario structure supports them;
- censored/time-to-recovery analysis when non-recovery is common.

The number of independent runs must be chosen from pilot variance, desired precision, compute cost, and the final statistical estimand rather than inherited from unrelated papers.

## Candidate agent capability roles

This workspace intentionally avoids naming final algorithms. The smallest scientifically useful comparison is likely to require roles rather than a long model catalog.

### A0 — nominal reference agent

Purpose: establish how a competent ordinary learner behaves without a dedicated robust/adaptive mechanism.

### A1 — frozen robustness-oriented agent or policy

Purpose: test resistance to uncertainty when post-change learning is forbidden.

The exact method remains open. It must not be selected solely because it is labelled “robust” in the literature.

### A2 — online adaptive/resilient agent

Purpose: test actual post-change learning/recovery under the same environment and evaluation accounting.

The exact adaptation mechanism may involve direct continual updating, explicit detection, context inference, model reuse, Bayesian uncertainty, or another evidence-backed mechanism. Feasibility and fairness determine the final choice.

### A3 — context-recall capability, optional

Include only if recurring-context recovery is retained as a distinct secondary question and can be represented without making the experiment matrix disproportionate.

## Fair-comparison constraints to preserve

1. Environment truth and disturbance schedule are identical across agents for matched evaluation cases.
2. Information access must be declared. An agent given the true change point or context identifier is not directly equivalent to one that must infer it.
3. Training, adaptation, and evaluation budgets must be measured and reported even when algorithms use different internal update rules.
4. Algorithm-specific hyperparameters are allowed, but tuning effort and data access must follow a documented policy.
5. Frozen-policy and online-adaptation results must not be pooled into one ranking without preserving regime labels.
6. Nominal performance is always reported alongside disturbed performance.
7. Failed, timed-out, invalid, cancelled, and non-recovered runs remain part of the audit trail.

## GridWorld implications for later prototype work

The provisional framing strengthens the earlier technical pre-screen in several ways.

The final environment must make it straightforward to expose and test:

- ground-truth state separately from the agent observation;
- intended action separately from executed action;
- named disturbance events and exact onset steps;
- persistent rule/dynamics changes without recreating the environment object implicitly;
- deterministic replay from explicit RNG streams;
- a nominal reference configuration and changed configuration with stable serialization;
- headless traces independent from rendering;
- event-aligned performance extraction around known experimental change points.

This makes a small project-owned Gymnasium environment an especially important prototype, while MiniGrid remains a legitimate alternative if a thin adaptation can preserve the same transparency. The prototype comparison, not this document, decides the implementation.

## Explicit non-decisions

This workspace does **not** select:

- Q-learning, DQN, PPO, SAC, Bayesian RL, robust MDP algorithms, continual RL, meta-RL, or any other specific final agent;
- a neural-network architecture;
- a state representation;
- a grid size;
- a reward value;
- a recovery threshold;
- severity levels;
- disturbance probabilities;
- a change-point time;
- episode length;
- training timesteps;
- tuning budget;
- number of seeds/runs;
- a statistical significance threshold;
- Gymnasium custom versus MiniGrid as the final environment.

## Conversion to a final research brief

After the bibliography import and target-system report are available:

1. validate every decision-driving statement against imported analysis and original-language evidence;
2. replace title-level provisional traceability with canonical imported source identifiers;
3. map each retained RQ to exact evidence, environment factors, agent roles, metrics, and analysis estimands;
4. use the target-system report to remove infeasible agent families before implementation work;
5. complete the custom-Gymnasium versus MiniGrid prototypes and ADR;
6. freeze the minimum uncertainty taxonomy;
7. select the smallest feasible model set;
8. design pilot conditions and estimate runtime/variance;
9. perform the required literature refresh before protocol freeze;
10. promote only the validated material into `RESEARCH_BRIEF.md`, model/metric workspaces, and experiment protocol documents.

## Current recommendation

Retain the provisional main question and the first two secondary questions as the default research-framing candidates. Keep recurring-context recall conditional. Treat detector metrics as method-specific diagnostics rather than a universal thesis outcome.

The most defensible minimal scientific shape currently appears to be:

> one controlled GridWorld + three explicit disturbance channels + nominal/frozen/adaptive evaluation regimes + degradation/recovery trajectories + a very small set of capability-distinct agents.

This is a proposal to test against the remaining gates, not a frozen experimental matrix.
