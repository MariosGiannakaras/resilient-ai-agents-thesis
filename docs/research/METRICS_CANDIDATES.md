# Resilience Metric Estimands

**Status:** Operational schema v1 implemented and validated by `T-300`/`T-301`; protocol parameter values and final statistical roles remain pilot/freeze decisions.

## Evidence and adaptation boundary

The official application requires resilience and recovery-speed evaluation. Citation-ready `SRC-0A594EACC0` supports treating resilience as a temporal process, comparing a disrupted performance curve with a nominal reference, and keeping degradation and recovery profiles distinct. Its cooperative multi-agent aggregation and composite score are not transferred to this single-agent GridWorld. Citation-ready `SRC-0A4AFAC8E9` supports preserving independent-run distributions and reporting uncertainty/effect sizes rather than best runs or isolated point estimates; it does not prescribe a universal run count or aggregate for this experiment.

Accordingly, schema v1 preserves interpretable components and defines no composite “resilience score.” Numeric windows, tolerances, evaluation-block size, run count, interval method, and primary/secondary roles are selected from development/pilot evidence and frozen before final evaluation.

## Unit of analysis and required inputs

The metric function operates on one valid independent run in one exact agent × scenario × severity × update-regime condition. Nested episodes/checkpoints are repeated measurements, not independent replications.

Inputs are mandatory and contain no defaults:

- `values[t]`: the predeclared higher-is-better performance signal at evaluation unit `t` (normally a versioned evaluation-block episode-return aggregate);
- `reference_values[t]`: an aligned, predeclared matched no-change reference curve for the same agent/scenario evaluation design, never selected from the disrupted result;
- `change_index = c`: the first post-change evaluation unit, splitting non-empty pre/post segments;
- positive `immediate_window`, `worst_window`, and `terminal_window`, each bounded by the post-change horizon;
- non-negative absolute performance-unit `recovery_tolerance = τ`;
- positive `recovery_stability_steps = S`, bounded by the post-change horizon.

All samples and parameters must be finite. The function rejects mismatched curves, ambiguous indices/windows, booleans used as numbers, negative tolerance, empty series, and non-finite values.

## Per-run operational estimands

For aligned observed performance `y_t`, matched reference `r_t`, and signed gap `g_t = r_t - y_t`, positive gap means worse-than-reference performance and negative gap means improvement.

| Output | Definition | Interpretation / RQ mapping |
|---|---|---|
| `nominal_mean` | Mean `y_t` for `t < c`. | Absolute clean performance; required so robustness/adaptation cost remains visible. |
| `nominal_reference_mean` | Mean `r_t` for `t < c`. | Matched clean reference level. |
| `nominal_gap` | Reference nominal mean minus observed nominal mean. | Signed pre-change mismatch/cost diagnostic. |
| `immediate_degradation` | Mean `g_t` over the first declared post-change immediate window. | Immediate resistance/disruption depth in the main and robustness-vs-adaptation RQs. |
| `worst_degradation` | Maximum `g_t` in the declared early worst window. | Worst observed early failure depth without choosing the best/worst time post hoc. |
| `post_change_mean` | Mean observed performance in the declared terminal window. | Absolute retained/end-window task performance. |
| `post_change_reference_mean` | Mean matched reference in the same terminal window. | Terminal comparison level. |
| `post_change_gap` | Terminal reference mean minus terminal observed mean. | Incomplete/overshooting recovery and persistent post-change cost. |
| `cumulative_deficit` | Sum of `max(0, g_t)` over the complete post-change horizon. | Non-negative integrated below-reference loss; units are performance × evaluation unit. Improvements never cancel losses. |
| `first_degradation_index` | First absolute index with `g_t > τ`, else `None`. | Evaluator-ground-truth failure onset relative to the declared criterion. |
| `recovery_index` | Earliest absolute index after first degradation starting `S` consecutive samples with `g_t ≤ τ`, else `None`. | Criterion-based recovery location; later terminal metrics still reveal subsequent deterioration. |
| `recovery_delay` | `recovery_index - c`, else `None`. | Recovery speed measured from the known environmental change, in evaluation units. |
| `recovery_status` | `NO_DEGRADATION`, `RECOVERED`, or `NOT_RECOVERED`. | Prevents resistance/no observed loss from being called recovery and preserves real non-recovery. |

The tolerance is an absolute value in the declared performance units, not a fraction of a possibly negative nominal score. Exact `τ`, `S`, and window lengths are protocol parameters justified through pilots and sensitivity checks; they cannot be chosen after final results are inspected.

## Across-run estimands and statistical boundary

For each exact condition, retain every predefined independent run and its per-run metric record. `summarize_recovery_statuses` reports counts of all three recovery outcomes and `non_recovery_rate = NOT_RECOVERED / valid_runs`. Execution failures, invalid runs, cancellations, interruptions, and later analysis exclusions are not passed off as valid metric rows: they remain explicit in run lifecycle/provenance and must accompany the valid-run denominator.

Agent contrasts are formed from per-run estimands, paired/blocked only where seeds/scenarios are legitimately matched. The complete `pilot-v0.2` analysis preserves matched root/layout/checkpoint/episode-seed branches and all 54 predeclared window/tolerance/stability settings. Recovery counts vary across settings in 33 of 42 agent-condition-layout cells, while non-recovery remains explicitly censored. The final interval/effect-size estimator, recovery rule, aggregation across layouts/severities, multiplicity strategy, and required independent-run count remain `T-412` freeze decisions informed by `T-411`; no favorable pilot setting, single-run, or best-run conclusion is valid.

## Supporting diagnostics and interpretation limits

- Observation corruption and action-execution failure conditions use nominal, immediate, worst, terminal, and cumulative-deficit outputs as robustness diagnostics.
- Recovery status/time is interpreted as adaptation only for a persistent change with post-change updates permitted. A frozen policy meeting the criterion demonstrates resistance, not learning-based recovery.
- DEC-034 retains no detector role, so detector metrics are outside schema v1; adding them requires a recorded pre-freeze role/RQ amendment, and evaluator change truth must never be exposed to the agent.
- Resource use, tuning interactions, safety costs/violations, and execution failures remain separate diagnostics rather than ingredients of a composite score.
- Metrics are compared within compatible reward/reference/evaluation-unit definitions. Cross-scenario pooling requires a predeclared validated normalization and may not silently mix scales or horizons.

## Known-answer validation

`tests/test_metrics.py` verifies by hand calculation:

- signed nominal/immediate/worst/terminal gaps and cumulative deficit;
- recovery after a required stabilization interval;
- time-varying matched references and explicit windows;
- negative-valued performance without fraction-threshold errors;
- `NO_DEGRADATION` distinct from recovery;
- true `NOT_RECOVERED` with `None` index/delay rather than the horizon;
- complete recovery-status counts/rate; and
- fail-closed invalid/non-finite inputs.

## Freeze gate

The formulas and outcome states above are versioned implementation semantics. Final primary/secondary/diagnostic roles and numeric protocol parameters freeze only after pilots establish meaningful scale, variance, censoring prevalence, threshold/window sensitivity, and feasible precision, and before final evidence is inspected.
