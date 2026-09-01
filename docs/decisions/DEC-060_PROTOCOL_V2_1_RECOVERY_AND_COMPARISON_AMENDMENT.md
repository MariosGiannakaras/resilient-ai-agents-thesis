# DEC-060 — Protocol-v2.1 pre-outcome recovery and comparison amendment

**Status:** Accepted pre-outcome amendment  
**Date:** 2026-09-01  
**Amends:** DEC-058 / `configs/protocols/protocol-v2.0-final.json`  
**Tracking:** T-530 / GitHub issue #98

## Context

DEC-058 froze protocol-v2.0 before final-reserve execution. A subsequent pre-submission/pre-final-experiment audit identified three scientific completeness gaps that must be corrected before any final outcome is observed: (1) the existing matched `(FN-FD)-(AN-AD)` estimand measures adaptation benefit but not recovery speed, (2) the active research questions remained provisional despite the protocol freeze, and (3) the analysis contract summarized methods separately without a predeclared direct cross-method contrast family.

No protocol-v2 final-reserve result has been used to make this decision. `final_reserve_access=false` remains mandatory. DEC-058 remains immutable historical authority for protocol-v2.0; this record is an explicit amendment rather than a silent rewrite.

## Decision

### Unchanged scientific design

The following remain exactly as accepted by DEC-058 unless a future explicit pre-outcome amendment states otherwise:

- retained methods: Q-Learning, SARSA, DQN, PPO, Dyna-Q+;
- independent Phase-A learning and method-native learning semantics;
- common actual-environment-interaction fairness budget;
- agent-visible observation/action semantics;
- Phase-A budget, probe checkpoints and no-learning probe isolation;
- final roots and held-out final layouts;
- Phase-B FN/FD/AN/AD factorial and exact branch-point cloning;
- Phase-B horizon of 256 actual post-change interactions per branch;
- conditions and disturbance parameters;
- method hyperparameters;
- root as independent statistical unit, with equal layout weighting within root;
- failure retention and no outcome-driven root/seed replacement;
- estimation-oriented uncertainty and bootstrap sensitivity;
- no composite resilience score;
- strict tuning/pilot/final-reserve separation.

### Final research questions

**RQ1 — Nominal learning.** Under the common controlled GridWorld task, shared agent-visible information contract and common actual-environment-interaction budget, how do the retained methods differ in nominal learning performance and learning efficiency?

- Methods: all five retained methods.
- Conditions/regime: Phase A nominal learning; no Frozen/Adaptive distinction.
- Independent unit: root identity; layouts are repeated/blocked observations within root.
- Primary estimands: final nominal probe performance and predeclared learning-trajectory/time-average performance.
- Evidence: Phase-A probes, root-reduced records, resource counters.
- Comparison: direct root-paired method contrasts where roots are shared.
- Interpretation boundary: capability/learning efficiency under this controlled task and budget, not universal algorithm ranking.

**RQ2 — Resilience and adaptation benefit.** After controlled uncertainty/change, how much does each method degrade, and how much does allowed continued online learning reduce disturbance-associated loss relative to matched frozen deployment?

- Methods: all five retained methods.
- Conditions: all frozen Phase-B conditions.
- Regimes: Frozen and Adaptive/Continual are deployment regimes, not algorithms.
- Independent unit: root; layouts reduced equally within root.
- Primary estimands: directed Frozen loss, directed Adaptive loss, and matched adaptation benefit `(FN-FD)-(AN-AD)` after metric-direction normalization.
- Evidence: matched FN/FD/AN/AD branch records and root summaries.
- Comparison: root-paired method contrasts on predeclared estimands.
- Interpretation boundary: adaptation benefit is not recovery speed.

**RQ3 — Recovery speed.** After persistent unannounced rule/dynamics change, how quickly does each adaptive method return to its matched adaptive-nominal performance neighborhood, what recovery trajectory does it show, and when does it fail to recover within the fixed observation horizon?

- Primary conditions: persistent `action-remap/*` conditions.
- Supporting only: action-failure and observation-corruption remain robustness/adaptation diagnostics unless separately justified before final outcomes.
- Regime: Adaptive-Nominal versus Adaptive-Disturbed.
- Independent unit: root; the two final layouts are equally weighted within root before inference.
- Primary trajectory metric: window mean reward per actual environment interaction.
- Evidence granularity: deterministic fixed 32-interaction windows over the unchanged 256-interaction horizon (8 windows). Episode boundaries neither reset nor realign windows.
- Matched reference: the root-level Adaptive-Nominal trajectory at the same windows.
- Direction: higher mean reward per interaction is better. Generic code may support lower-is-better metrics for known-answer validation, but that does not alter the primary RQ3 metric.
- Primary tolerance: AD is in the recovery neighborhood when `AN - AD <= 0.10` reward per interaction. Better-than-AN AD values therefore satisfy the criterion rather than being penalized by an absolute-distance rule.
- Stability: two consecutive in-tolerance windows.
- Recovery time: end interaction of the first window in the first qualifying stable run; confirmation time is the end of the second qualifying window. This is a window-resolution estimand, not an exact latent crossing time.
- Non-recovery: if no stable run is confirmed by interaction 256, status is `right-censored`, censoring time is 256, and recovery time is `null`/missing — never an artificial value of 256.
- Sensitivity: repeat the recovery classification/time calculation with tolerances 0.05 and 0.20; these are sensitivity analyses, not alternative thresholds chosen after outcomes.
- Outputs: recovery status, recovery time when observed, confirmation/censoring time, trajectory, non-recovery frequency, root-level uncertainty and method contrasts.
- Interpretation boundary: recovery speed is primary for persistent changes and is distinct from immediate resistance and aggregate adaptation benefit.

The 0.10 primary tolerance is predeclared from the task reward contract (`step=-0.1`, `collision=-0.25`, `goal=1.0`) rather than selected from final outcomes. Using an absolute task-scale tolerance also avoids unstable percentage denominators for signed returns.

### Direct method contrasts

Method comparison is estimation-oriented. The canonical contrast is A-minus-B on root-reduced estimands, pairing only common root identities. Layouts, episodes and temporal windows are not independent samples.

Contrast policy:

- **Primary:** pairwise contrasts for RQ1 final nominal performance, RQ2 adaptation benefit, and RQ3 observed recovery-time/recovery-status summaries on the two primary action-remap conditions.
- **Secondary:** pairwise contrasts for RQ1 time-average learning performance and RQ2 Frozen/Adaptive losses.
- **Exploratory/supporting:** contrasts for action-failure/observation-corruption diagnostics, resource observations, and sensitivity-threshold recovery summaries.

Report effect estimates and uncertainty intervals. Student-t root intervals remain primary where the estimand is a scalar root value; root bootstrap remains a sensitivity analysis. Pointwise intervals are not simultaneous inference. Formal null-hypothesis p-value testing is not part of this amendment, so the final thesis must not relabel non-overlap or pointwise intervals as “statistically significant.” If formal multiple-comparison superiority testing is later required, its multiplicity strategy must be frozen before final-reserve access.

### Computational evidence

The primary fairness criterion remains actual environment interactions. Wall-clock time, process CPU time and scientifically interpretable method-specific update counts are secondary descriptive computational evidence; they do not become a new primary RQ.

## Evidence and implementation consequences

Before T-610, T-530 must make the complete chain consistent:

`Phase-B execution -> raw temporal evidence -> validated analysis records -> root reduction -> recovery/direct-contrast statistics -> deterministic exports -> PySide6 stored-evidence presentation`.

The UI may render validated stored recovery/contrast outputs but must not choose thresholds or recompute scientific truth independently.

## Validity and leakage statement

This amendment was made before final-reserve execution and does not change final roots, layouts, methods, hyperparameters, conditions, training budgets or Phase-B horizon. Existing tuning/pilot/sizing evidence remains valid for those unchanged choices. New non-final synthetic/development validation may verify temporal/recovery mechanics, but final layouts/seeds must not be used to tune or revise the thresholds or analysis policy above.

## Public-repository constraint

The repository remains public by explicit user decision. `thesis/source-material/ThesisApplication.pdf` and the existing source-material structure remain in place. No privacy migration, file removal or history rewrite is required for scientific completion and this matter is not a T-530/T-610 blocker.

## Gate

`final_reserve_access=false` remains in force. T-610 remains blocked until T-530 implementation, deterministic validation, affected CI, documentation reconciliation and objective review are complete. Completion of T-530 stops at the authorization gate immediately before the first final-reserve scientific execution; it does not itself authorize T-610.
