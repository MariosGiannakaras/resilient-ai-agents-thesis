# RQ → evidence → estimand → output traceability

**Status:** protocol-v2.1 pre-execution traceability map  
**Authority:** DEC-058 + DEC-060 + `configs/protocols/protocol-v2.1-final.json`

This map is navigational, not a new statistical plan. It points each frozen research question to the evidence and stored outputs that already implement the protocol-v2.1 contract. The independent inferential unit is the root; layouts are equal-weight repeated blocks inside each root. UI state is never an evidence source and must not recompute these estimands.

| Research question | Primary evidence | Root-level reduction / estimand | Stored scientific outputs | Interpretation boundary |
| --- | --- | --- | --- | --- |
| **RQ1 — Nominal learning** | Phase-A standardized probe records, metric `return_mean`, at the frozen interaction checkpoints | Equal-weight layouts within each root. Primary: final nominal value at the last probe. Secondary: trapezoidal trajectory/time-average. Direct method comparisons are root-paired A-minus-B on shared roots. | `phase-a-root-records.csv`, `phase-a-method-summary.csv`, `phase-a-method-contrasts.csv`, plus corresponding `analysis-package.json` Phase-A records/summaries/contrasts and `result-index.json`. | Common actual-environment-interaction budget is the fairness axis. Probe episodes/layouts are not independent samples. |
| **RQ2 — Resilience / adaptation** | Matched Phase-B FN/FD/AN/AD standardized records, metric `return_sum`, from one exact checkpoint/branch point | Equal-weight layouts within each root. Frozen loss = FN−FD; Adaptive loss = AN−AD; adaptation benefit = `(FN−FD)−(AN−AD)`. Direct method comparisons are root-paired A-minus-B. | `phase-b-root-records.csv`, `phase-b-method-condition-summary.csv`, `phase-b-method-contrasts.csv`, plus corresponding Phase-B structures in `analysis-package.json` and `result-index.json`. | Frozen and Adaptive are deployment regimes, not separate algorithms. Conditions are matched within root/layout; branches are not independent replications. |
| **RQ3 — Recovery speed** | Schema-v2 Phase-B AN/AD reward windows: eight passive 32-interaction mean-reward windows over the unchanged 256-interaction horizon | Equal-weight layouts window-by-window within each root before recovery assessment. Primary action-remap family: recovery status and stable recovery timing under tolerance 0.10 with two consecutive in-tolerance windows. `recovery_time` is observed only when recovery occurs; non-recovery is right-censored with `recovery_time=null`. Restricted fixed-horizon recovery delay is a separate censored-comparison estimand. Sensitivities use 0.05 and 0.20. Direct method comparisons use shared roots. | `recovery-root-records.csv`, `recovery-trajectory-records.csv`, `recovery-method-condition-summary.csv`, `recovery-method-contrasts.csv`, `recovery-sensitivity-root-records.csv`, plus `analysis-package.json` recovery structures and `result-index.json`. | Persistent action-remap is the primary RQ3 axis; action-failure and observation-corruption are supporting diagnostics. Episode boundaries do not realign windows. A censored value of 256 must never be reported as an observed recovery time. |

## Shared statistical/provenance rules

- Two-sided 95% Student-t pointwise intervals use the frozen critical value indexed by the **actual independent-root count** (`n=2..12`).
- Scientific failures remain retained; roots are not replaced and no outcome-driven seed substitution is allowed.
- There is no predeclared p-value superiority family and no post-hoc “statistically significant” relabeling.
- Actual environment interactions are primary for fairness; wall/process CPU time and method-native update counts are secondary descriptive evidence.
- `analysis-package.json` is the derived scientific authority consumed by the deterministic evidence handoff. The PySide6 Results workspace may present these stored values but must not choose thresholds, aggregate layouts/roots, or derive new scientific claims.
- Final protocol-v2.1 outcomes do not exist yet. This document describes the predeclared evidence path only and does not authorize final-reserve execution.
