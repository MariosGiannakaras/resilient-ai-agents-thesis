# Metrics Selection Workspace

**Status:** `RESEARCH_REQUIRED`. There is no metric shortlist.

The official application requires evaluation of **resilience** and **recovery speed**, but it does not define formulas, thresholds, windows, units or aggregation. No metric receives candidate or preferred status merely because it appeared in an old conversation.

## Selection process

1. Define the research questions and the exact evaluation/adaptation regime.
2. Review primary and peer-reviewed literature on task performance, robustness, resilience, recovery and sequential-decision evaluation.
3. Identify outcome constructs before choosing formulas.
4. Define the unit of analysis and nesting structure: episode, run, independent seed/repetition, layout, scenario or another justified unit.
5. Specify formula, direction, units, horizon, windows, thresholds, censoring and missing/failure handling.
6. Test construct validity and known-answer behavior on controlled fixtures.
7. Check comparability across reward/rule changes and model families.
8. Define aggregation, interval/effect-size procedure and sensitivity analyses before final runs.
9. Record primary, secondary and diagnostic roles in the decision log/protocol.

## Constructs that must be operationalized

These constructs come from the official topic or general experimental necessity; they are not preselected formulas:

| Construct | Why required | Questions the literature/protocol must resolve |
|---|---|---|
| Nominal task performance | A disruption effect needs a meaningful reference | Which task outcome is valid and comparable? At what level is it aggregated? |
| Immediate disruption impact | Resilience includes response to an adverse change | What is the baseline, onset window and direction-adjusted scale? |
| Recovery speed | Explicitly requested by the official application | What counts as recovery, how is sustained recovery defined, and how are non-recoveries censored? |
| Degree/quality of recovery | Returning quickly to a poor level is not sufficient | Is recovery relative to pre-change performance, a new optimum, or another justified reference? |
| Reliability across independent runs | Single-run conclusions are forbidden | What distributional summaries and uncertainty intervals are appropriate? |
| Resource use/fairness | Comparisons may differ in internal computation | Which resources are controlled, equalized or only reported? |
| Failure/safety behavior | Some disturbances may cause invalid or unrecoverable behavior | Which events are meaningful and how are they distinguished from software faults? |

Additional constructs such as generalization, retention, detection delay or sample efficiency are included only when a research question and literature justify them.

## Metric evidence matrix to populate

| Metric ID | Construct | Exact definition/formula | Unit and direction | Analysis level | Window/horizon/threshold | Failure/censoring rule | Literature support | Validation fixture | Protocol role | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| TBD |  |  |  |  |  |  |  |  |  | RESEARCH_REQUIRED |

## Statistical reporting decisions to make

The statistical plan must justify rather than assume:

- descriptive summaries appropriate to the observed distributions,
- uncertainty intervals and effect-size estimands,
- paired/blocking structure where scenarios legitimately match,
- aggregation across episodes, repetitions, layouts and severities,
- treatment of censored recovery and failed/invalid runs,
- correction or hierarchical strategy for multiple comparisons,
- sensitivity analyses for thresholds, windows and exclusions,
- whether formal hypothesis tests are needed at all.

## Non-acceptable practices

- Single best-run reporting.
- Choosing primary outcomes after inspecting final results.
- Using training reward as a universal cross-condition measure when reward definitions differ.
- Hiding failed, cancelled, invalid, excluded or non-recovered runs.
- Treating dashboard smoothness or visual appeal as scientific resilience outcomes.
- Using an opaque AI-generated composite score.
- Reporting a formula without source, operational rationale and known-answer tests.
- Treating episodes from the same run as independent experimental replications.

## Metric freeze gate

Metrics may be frozen for final experiments only when:

- every metric maps to a research question or predefined diagnostic purpose,
- definitions and code are versioned,
- formulas pass known-answer tests,
- aggregation and statistical roles are pre-specified,
- comparability and limitations are documented,
- primary/secondary/diagnostic labels are recorded before final result inspection.
