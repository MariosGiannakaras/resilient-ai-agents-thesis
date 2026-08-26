# Pilot v0.2 Diagnostic Report

**Task:** `T-410`

**Evidence state:** complete, validated diagnostic pilot evidence; not final or inferential evidence

## Evidence inventory

The amended campaign completed all 14 planned `PV02-PILOT-*` whole experiments: two pilot layouts by seven conditions, with eight precommitted roots and three agent regimes per experiment. `PV02-PILOT-ANALYSIS` validates 336 scientific units and 18,144 sensitivity records. Every included run is finalized, checksummed, semantically reproduced, and recorded as `completed`; no poor outcome, truncation, or non-recovery was excluded.

The immutable evidence is:

- `results/runs/PV02-PILOT-*` for run bundles and per-episode events;
- `results/summaries/PV02-PILOT-ANALYSIS/` for validated units, aggregates, operational diagnostics, and all 54 predeclared metric settings;
- `results/campaigns/pilot-v0.2/campaign-state.json` for tuning selection, execution totals, and the superseded v0.1 attempt inventory.

The analysis source commit is `04244bab8a2a47f4e65b36578e969beab5373439`. The evidence remains limited to feasibility and protocol design. Eight roots do not support final comparisons or confirm the provisional hypotheses.

## Execution and failure integrity

The v0.1 execution retained two real fail-closed discoveries. Sequential publication of the second tuning child initially failed because leading Git porcelain status whitespace was stripped; the finalized bundle was validated and published without rerunning it, and PR #70 added the regression fix. Later, `PV01-PILOT-L01-C06` finalized as `failed` because an active corrupted R0 observation aliased the modeled goal. Five earlier v0.1 pilot attempts remain completed but are superseded. PR #71 introduced the bounded information-safe v0.2 amendment, reused only the unaffected F0 tuning evidence, retained the same pilot seeds, and assigned new identities to the complete retry.

The v0.2 retry completed 14/14 experiments with no execution failure, timeout, integrity failure, or analysis exclusion. The earlier failed bundle and traceback remain in the campaign inventory rather than being relabeled as scientific non-recovery.

## Tuning outcome

All 36 v0.1 F0-only tuning runs were revalidated and rescored. The stage-one winner used learning rate `0.5`, exploration epsilon `0.125`, and discount `0.9375` (mean nominal return `-15.389`, worst-layout mean `-17.301`, collision rate `0.1110`). Stage two selected the same learning rate/exploration pair with discount `0.96875` (mean `-15.227`, worst-layout mean `-17.383`, collision rate `0.1063`). The amended pilot did not search its outcomes or retune this configuration.

## Runtime and storage feasibility

The preflight took 21 seconds and deterministically produced a 420-second child deadline. The 14 pilot children used 890 seconds of recorded wall-clock time in total; individual runs ranged from 63 to 65 seconds (median 63.5). Their bundles total 92,311,912 bytes (92.3 MB decimal), with 6,584,389 to 6,599,752 bytes per run (median 6,593,549.5). The validated analysis bundle adds 14,726,598 bytes. Execution produced 146,944 episode attempts and 147,182 persisted events.

Concurrency one is operationally feasible on the accepted CPU baseline. The observed runtime does not justify distributed execution. Final campaign budgeting must account for roughly one minute and 6.6 MB per comparable child, then recompute from the frozen matrix rather than extrapolating an unstated matrix.

## Primary descriptive diagnostics

The table aggregates both layouts and all 16 root-layout units per agent/condition at the predeclared central metric setting. Values are mean with sample standard deviation in parentheses. Recovery is `RECOVERED / 16`; `ND` means all 16 units were correctly classified `NO_DEGRADATION`. A dash means no unit recovered, so no recovery time exists.

| Agent | Condition | Immediate degradation | Worst degradation | Terminal gap | Cumulative deficit | Recovery | Mean delay among recovered |
|---|---|---:|---:|---:|---:|---:|---:|
| C0 | nominal | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | ND | — |
| C0 | remap-min-in-set | 40.500 (2.875) | 40.875 (2.473) | 0.047 (0.993) | 114.812 (21.211) | 15/16 | 15.733 |
| C0 | remap-max-out-of-set | 51.125 (4.209) | 51.125 (4.209) | 0.844 (1.384) | 108.625 (25.487) | 14/16 | 6.714 |
| C0 | action-failure-1of8 | 1.500 (1.155) | 5.000 (3.578) | 2.195 (1.113) | 76.375 (13.135) | 8/16 | 12.250 |
| C0 | action-failure-1of4 | 5.188 (6.400) | 10.125 (5.932) | 5.852 (2.600) | 181.562 (35.601) | 0/16 | — |
| C0 | observation-corruption-1of8 | 1.000 (1.789) | 12.062 (13.964) | 14.633 (7.673) | 370.312 (123.328) | 1/16 | 10.000 |
| C0 | observation-corruption-1of4 | 3.000 (3.502) | 28.562 (17.791) | 32.438 (4.302) | 833.125 (149.420) | 0/16 | — |
| F0 | nominal | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | ND | — |
| F0 | remap-min-in-set | 25.312 (36.747) | 45.125 (14.537) | 16.211 (12.380) | 832.312 (125.569) | 2/16 | 24.000 |
| F0 | remap-max-out-of-set | 53.750 (31.882) | 74.125 (11.752) | 48.258 (12.524) | 1,680.812 (282.536) | 0/16 | — |
| F0 | action-failure-1of8 | 2.938 (27.733) | 21.625 (26.638) | -1.312 (7.970) | 196.812 (102.573) | 14/16 | 10.429 |
| F0 | action-failure-1of4 | -3.000 (28.185) | 22.688 (22.893) | -1.344 (7.232) | 302.750 (104.767) | 6/16 | 11.000 |
| F0 | observation-corruption-1of8 | -11.500 (22.370) | 4.500 (11.742) | -11.180 (8.299) | 54.312 (48.516) | 16/16 | 8.000 |
| F0 | observation-corruption-1of4 | -12.625 (28.486) | 11.250 (17.976) | -14.180 (10.336) | 87.562 (46.045) | 14/16 | 12.500 |
| R0 | nominal | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | ND | — |
| R0 | remap-min-in-set | -0.625 (6.479) | 3.438 (6.449) | -0.164 (2.036) | 35.125 (16.661) | 16/16 | 7.438 |
| R0 | remap-max-out-of-set | 37.000 (8.602) | 46.125 (6.946) | 39.625 (4.168) | 1,256.812 (111.003) | 0/16 | — |
| R0 | action-failure-1of8 | -0.625 (1.668) | 0.875 (0.619) | -0.180 (1.681) | 21.125 (19.172) | 12/16 | 11.417 |
| R0 | action-failure-1of4 | -0.125 (1.408) | 2.625 (6.541) | -0.180 (1.682) | 24.188 (15.017) | 14/16 | 9.786 |
| R0 | observation-corruption-1of8 | 1.312 (1.621) | 3.125 (1.500) | 1.508 (2.074) | 61.000 (20.363) | 11/16 | 12.545 |
| R0 | observation-corruption-1of4 | 2.688 (1.852) | 6.500 (6.419) | 2.742 (2.245) | 111.688 (20.758) | 3/16 | 10.333 |

These are descriptive pilot diagnostics, not agent rankings. In particular, signed negative gaps can arise from paired stochastic trajectories and do not establish beneficial disturbance.

## Nominal cost, layout/seed variance, and terminal behavior

Nominal mean return across the 16 units was `-14.719` (SD `1.229`) for C0, `-34.730` (SD `8.899`) for F0, and `-48.551` (SD `1.072`) for R0. F0 is strongly layout-sensitive: means were `-28.977` on `pilot-l01` and `-40.484` on `pilot-l02`. C0 changed from `-13.891` to `-15.547`; R0 changed from `-49.078` to `-48.023`. The largest observed layout contrast was also F0 under the out-of-set remap: 30.5 return units for immediate degradation and 526.875 for cumulative deficit. Both pilot layouts therefore remain necessary blocking factors; a one-layout final matrix would be unsupported.

The 48-step horizon materially censors some roles. Across both layouts and roots, disrupted-branch truncation rates were:

| Agent | Nominal | In-set remap | Out-of-set remap | Action 1/8 | Action 1/4 | Observation 1/8 | Observation 1/4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| C0 | 0.00% | 2.34% | 1.56% | 0.00% | 0.13% | 4.43% | 22.92% |
| F0 | 18.10% | 72.01% | 72.01% | 20.96% | 22.27% | 7.55% | 6.12% |
| R0 | 95.96% | 95.83% | 98.57% | 95.18% | 96.48% | 94.01% | 95.44% |

Matched reference truncation was 0% for C0, 18.10% for F0, and 95.96% for R0. R0's near-universal nominal censoring is a decisive protocol gate: its current prior/policy/horizon combination cannot be frozen unchanged or interpreted as a clean resilience comparator. F0 remains a useful frozen-reference role but its nominal/layout variability and remap censoring must be represented explicitly in the final design.

## Metric sensitivity and recovery interpretation

All 54 predeclared combinations were retained. Recovery counts changed across parameter settings in 33 of 42 agent-condition-layout cells. The largest cell-level swing covered all eight roots (zero to eight recovered). Terminal mean-gap variation reached 6.75 return units in one cell as the terminal window changed. Cumulative deficit was invariant to this sensitivity grid, as its definition does not use the varied recovery/terminal/worst-window settings.

Recovery/non-recovery is therefore empirically observable, but its binary classification is not stable enough to select a favorable pilot threshold. The final plan must predeclare an externally justified practical tolerance/stability rule, retain non-recovery as censored with null time, and keep component curve estimands and sensitivity reporting. A composite resilience score remains unjustified.

## Agent-specific feasibility conclusions

- **C0:** executes reliably and exhibits a distinct adaptive pattern: large immediate remap degradation followed by low terminal gaps, but poor recovery under observation corruption. It remains a feasible final candidate.
- **F0:** executes reliably and provides the intended frozen nominal reference, but has the largest seed/layout variance and severe remap censoring. It remains useful as a comparator if blocking and censored outcomes are explicit.
- **R0:** correctness and information-boundary execution now succeed, and its in-set/out-of-set behavior is descriptively distinct. However, approximately 96% nominal truncation means the present robust prior/policy/horizon combination fails the repeated-run informativeness gate. `protocol-v1.0` must not retain it unchanged. A bounded pre-final decision must either justify and validate a revised robust construction using only non-final partitions or remove/reframe the role before final evidence is inspected.

## Answers to the pilot questions

1. The complete workflow is reproducible and operationally feasible on the accepted machine; sequential one-child publication is recoverable and the amended campaign completes within the measured budget.
2. The in-set and out-of-set remaps, action failures, and observation corruption produce distinguishable diagnostic behavior, but the selected severities and horizon are not automatically final values.
3. Layout and root variability are material, especially for F0; final analysis must block/pair by layout and seed and justify repetitions from the pilot variance rather than use a convenience count.
4. Recovery is frequently censored and parameter-sensitive; non-recovery must remain real and recovery time cannot stand alone as a primary outcome.
5. C0 and F0 remain feasible roles. R0 is computationally executable but not scientifically informative enough under its current nominally saturated configuration, creating a mandatory `T-411`/`T-412` decision before freeze.

No final-reserve layout was executed, no final evidence was inspected, and no final RQ, hypothesis, severity, horizon, repetition count, model set, or metric threshold is frozen by this report.
