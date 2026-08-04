# Metrics Selection Workspace

**Status:** Active post-import workspace; metric primitives exist, but the final metric/estimand set is not frozen.

The official application requires evaluation of **resilience** and **recovery speed**. DEC-023 and `src/resilient_agents/metrics.py` now provide known-answer metric infrastructure, including explicit non-recovery handling, but no recovery threshold/window/primary outcome has been accepted merely as a software default.

## Current construct direction

The evaluation should preserve the degradation/recovery trajectory rather than collapse resilience into one opaque score.

Candidate constructs:

| Construct | Current role | Remaining scientific decision |
|---|---|---|
| Nominal performance | Required reference | Exact task outcome and aggregation level. |
| Immediate disruption impact | Required | Baseline/onset window and direction-adjusted scale. |
| Worst degradation/failure depth | Strong candidate | Window/horizon and comparability across scenarios. |
| Recovery trajectory | Required evidence shape | Smoothing/windowing, if any, and analysis level. |
| Recovery time | Explicit official requirement | Recovery definition, sustained criterion, threshold/reference, censoring. |
| Post-change/end-window performance | Strong candidate | Window and reference/optimality definition. |
| Cumulative post-change loss | Diagnostic/possible secondary | Reference value and whether regret-like interpretation is justified. |
| Non-recovery | Required state | Censoring/reporting/statistical treatment. |
| Across-seed variability/uncertainty | Required | Interval/effect-size procedure and nesting. |
| Detector delay/error | Conditional diagnostic | Only for methods with a detector and only against evaluator ground truth. |
| Resource/tuning cost | Fairness/diagnostic | Which costs are controlled versus reported. |

## Implemented infrastructure, not frozen science

`compute_resilience_metrics(...)` currently supports known-answer testing of basic constructs and requires the recovery fraction explicitly. It returns `None` for non-recovery instead of substituting the horizon.

This code is a testable primitive. The final protocol may refine or replace formulas after literature/pilot validation; doing so requires an explicit versioned decision and updated tests.

## Selection process

1. Finalize the main/secondary RQ constructs and exact environment/reward semantics.
2. Use citation-ready literature to justify outcome meanings and limitations.
3. Define unit of analysis/nesting: independent seed/run versus episode/layout/scenario.
4. Specify formula, direction, units, horizon, windows, thresholds, censoring, and failure handling.
5. Validate formulas against synthetic/hand-calculated trajectories before complex agents.
6. Check comparability across disturbance/reward/rule changes.
7. Use pilots to inspect variance, censoring/non-recovery prevalence, threshold sensitivity, and distribution shape.
8. Freeze primary/secondary/diagnostic roles and statistical estimands before final evidence is inspected.

## Statistical decisions still required

- descriptive summaries appropriate to actual distributions;
- uncertainty intervals/effect-size estimands;
- paired/blocking structure where scenarios/seeds are legitimately matched;
- aggregation across episodes, seeds, layouts, and severities;
- treatment of censored recovery and failed/invalid runs;
- multiple-comparison or hierarchical strategy where needed;
- sensitivity analyses for recovery thresholds/windows/exclusions;
- whether formal hypothesis tests add value beyond interval/effect-size reporting.

## Non-acceptable practices

- single best-run reporting;
- treating episodes from the same run as independent replications;
- selecting primary outcomes after inspecting final results;
- converting non-recovery to the final timestep;
- hiding failed/invalid/excluded runs;
- using dashboard smoothness/visual appeal as scientific resilience evidence;
- using an opaque AI-generated composite resilience score;
- hard-coding a recovery threshold merely because a code primitive needs an input.

## Freeze gate

Metrics may be frozen only when every primary/secondary/diagnostic metric maps to an RQ or predefined validity purpose, definitions/code are versioned, known-answer tests pass, aggregation/censoring/statistical roles are prespecified, comparability/limitations are documented, and pilot evidence shows the estimands behave meaningfully in the selected environment.
