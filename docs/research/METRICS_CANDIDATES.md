# Metrics Candidates

No primary metric is final. A metric becomes final only after its construct validity, formula, aggregation and analysis role are recorded.

## Notation candidate

Let:
- `P_pre` = reference performance before disruption.
- `P_t` = performance at time/window `t` after disruption.
- `P_post` = stable post-recovery performance estimate.
- Higher-is-better metrics should be normalized or direction-adjusted before resilience calculations.
- Windowing, smoothing and baseline estimation must be fixed before final analysis.

## Task-performance metrics

| Metric | Status | What it measures | Computation | Scope / limits | Use |
|---|---|---|---|---|---|
| Success rate | PROPOSED | Fraction of evaluation episodes reaching goal | successes / episodes | Needs consistent truncation and impossible-case policy | Evaluation |
| Episodic return | PROPOSED | Total reward under defined reward function | sum of rewards per episode | Not comparable if reward scales/rules differ without normalization | Training/evaluation |
| Episode length / steps to goal | PROPOSED | Navigation efficiency | transitions until terminal/truncated | Condition on success or report failures separately | Evaluation |
| Collision/invalid-action rate | PROPOSED | Safety/constraint violations | events / steps or episodes | Semantics must be explicit | Diagnostic |
| Catastrophic failure rate | NEEDS DEFINITION | Unrecoverable or severe failure | predefined event count / episodes | Cannot be used before “catastrophic” is operationalized | Evaluation |
| Goal-regret / path inefficiency | PROPOSED | Extra cost vs valid reference path | agent cost − oracle/reference cost | Requires comparable oracle under changed map | Evaluation |

## Resilience and recovery metrics

| Metric | Status | What it measures | Candidate computation | Limits | Use |
|---|---|---|---|---|---|
| Immediate relative degradation | PROPOSED | Initial shock | `(P_pre - P_early) / max(|P_pre|, ε)` after direction normalization | Sensitive to window and near-zero baseline | Primary/secondary candidate |
| Minimum performance after disturbance | PROPOSED | Worst observed drop | `min_t P_t` in fixed horizon | Multiple-testing/noise sensitive | Diagnostic |
| Recovery time | OFFICIAL CONCEPT, FORMULA OPEN | Time/interactions to return to threshold | first sustained `t` where `P_t ≥ α P_pre` | Threshold `α`, sustain window and censoring must be fixed | Primary candidate |
| Recovered-performance ratio | PROPOSED | Extent of recovery | `P_post / P_pre` or bounded normalized variant | Baseline instability; >1 improvement possible | Primary/secondary candidate |
| Area of performance loss | PROPOSED | Magnitude × duration of degradation | integral/sum of `max(0, P_pre - P_t)` over fixed horizon | Requires common time axis and horizon | Strong summary candidate |
| Unrecovered/censored rate | PROPOSED | Fraction not recovering within horizon | censored recoveries / runs | Should accompany recovery-time estimates | Evaluation |
| Robustness curve over severity | PROPOSED | Graceful degradation | metric versus severity, optionally area/profile | Severity must have meaningful scale | Evaluation |
| Adaptation gain | PROPOSED | Benefit of online adaptation | adapted regime − frozen regime | Requires paired/common scenarios | Evaluation |
| Change-detection delay | PROPOSED | Time to identify disturbance | declared detection − true onset | Only for agents with explicit detector | Diagnostic |

## Learning/generalization metrics

| Metric | Status | Relevance | Limits | Use |
|---|---|---|---|---|
| Sample efficiency | PROPOSED | Performance per environment interaction | Requires aligned budgets and learning curves | Training |
| Learning-curve area | PROPOSED | Aggregate learning progress | Window/horizon dependent | Training |
| Generalization gap | PROPOSED | Seen vs unseen layout/disturbance performance | Requires held-out scenario design | Evaluation |
| Retention / forgetting | PROPOSED | Performance on old regime after adapting | Requires return-to-old-regime protocol | Evaluation |
| Stability across seeds | CONFIRMED REQUIREMENT | Variability/reliability | Report distribution and intervals, not only SD | Training/evaluation |

## System-performance metrics

| Metric | Status | Computation/collection | Limits | Use |
|---|---|---|---|---|
| Wall-clock training/evaluation time | PROPOSED | Monotonic timer per phase | Hardware/load dependent | Resource report |
| Environment interactions | PROPOSED | Exact counter | Does not capture planning/internal compute | Budget/fairness |
| CPU time/utilization | PROPOSED | OS process/system metrics | Sampling overhead/platform differences | System performance |
| Peak/mean RAM | PROPOSED | Process measurements | Platform/tool dependent | Feasibility |
| GPU/VRAM usage | CONDITIONAL | Vendor/platform-supported telemetry | May be unavailable on RX 570/software stack | Feasibility |
| Checkpoint size/startup time | OPTIONAL | File size and timed restore | Only relevant to recovery/application | Engineering |

## Statistical summaries

Candidate reporting:
- individual run values and distributions,
- median and mean where each is informative,
- interquartile mean (IQM) or robust aggregate when justified,
- bootstrap confidence intervals,
- effect sizes with intervals,
- paired estimates when scenarios/seeds are legitimately paired,
- performance profiles or probability-of-improvement summaries when multiple tasks/configurations exist.

Formal hypothesis tests are not automatically required and must not replace effect estimation.

## Unsuitable or incomplete historical metrics

- **“Survival error limit” — NOT DEFINED:** Historical wording without an accepted formula; do not use.
- **Single best run — NOT SUITABLE:** Encourages cherry-picking.
- **Only average reward — INSUFFICIENT:** Does not directly characterize degradation/recovery.
- **Training reward across different reward functions — NOT COMPARABLE:** Needs common scale or separate reporting.
- **Dashboard FPS/animation smoothness as research outcome — NOT SUITABLE:** Engineering metric only.
- **Unverified AI-generated resilience score — NOT SUITABLE:** Composite index requires transparent formula and validation.

## Metric decision checklist

1. What construct does it represent?
2. Is higher/lower better and is direction consistent?
3. What unit, horizon, window and threshold are used?
4. How are failures and censored recoveries handled?
5. Is the metric per episode, run, seed, layout or model?
6. Is aggregation pre-specified?
7. Does it remain comparable when rules/rewards change?
8. Which RQ and thesis figure/table use it?
9. Can it be verified with a known-answer fixture?
