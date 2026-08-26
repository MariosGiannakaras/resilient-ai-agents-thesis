# Research Brief

**Status:** T-200 bounded framing complete; final operational RQ/hypotheses remain provisional until the listed feasibility and protocol gates close.

This file defines the current research problem and freeze criteria. Historical/pre-import workspaces may explain earlier reasoning but do not override this active brief.

## Confirmed identity and purpose

- **Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα.
- **English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments.
- **Institution:** University of West Attica, School of Engineering, Department of Informatics and Computer Engineering.
- Compare resilient decision agents in a simple controlled simulated environment under uncertainty/dynamic change.
- GridWorld is the confirmed environment direction.
- Official examples include observation/data noise, rule changes, and action-execution failures.
- Evaluation must address resilience and recovery speed.

## Evidence state

The complete bibliography corpus is already imported and pinned. Formal thesis claims use only the nested citation-ready layer.

Current decision-driving citation-ready anchors include:

- `SRC-70772C0629` — structured switching/non-stationarity cautions against describing ordinary Q-learning as universally incapable;
- `SRC-9464421E55` — motivates practical finite-horizon validation of detector/restart behavior under non-stationarity;
- `SRC-76B2247457` — supports a strict tuning/pilot/final-evaluation boundary in continual-RL evaluation;
- `SRC-FC42D9798A` and `SRC-3C0F7CC819` — distinguish policy robustness within an explicit model-uncertainty set from detection and recovery after an unknown persistent change. They support the conceptual distinction, not the inclusion or expected superiority of a robust-MDP comparator.

## Current bounded direction — proposed, not frozen

- Separate robustness from post-change adaptation/recovery.
- Use persistent rule/dynamics change as the leading recovery axis.
- Keep observation corruption and action-execution failure as supporting robustness diagnostics unless a distinct final RQ justifies more.
- Compare a small number of scientifically distinct capability roles, not a catalogue of algorithms.
- Preserve nominal performance, immediate/worst degradation, recovery trajectory/time, post-change performance, non-recovery, and across-run uncertainty.
- Keep development/tuning/pilot/final scenarios separated and prevent information leakage.
- Keep the final matrix CPU-feasible under the accepted target-machine baseline; the detected Radeon adapter is not a validated scientific-compute backend.

## T-200 bounded research framing

### Provisional main research question

> Under a common agent-visible information contract, how do a small set of scientifically distinct decision-agent capability roles differ in nominal performance, immediate degradation, recovery trajectory and time, post-change performance, and non-recovery after an unannounced persistent rule or dynamics change in a controlled GridWorld?

This question is bounded to the implemented finite-horizon GridWorld regime. It does not claim that one algorithm is generally superior in non-stationary reinforcement learning, and it does not assume that a method labelled robust or adaptive will recover in the selected setting.

### Minimal provisional secondary questions

1. **Robustness versus adaptation:** Under matched environment changes and information access, how do frozen-policy resistance and permitted online adaptation differ in nominal cost, immediate degradation, and later recovery profile?
2. **Supporting disturbance diagnostics:** How robust are the same retained agent roles to controlled observation corruption and action-execution failure under an explicitly declared frozen or adaptive regime, without describing stressed performance as recovery when no post-change adaptation occurs?

Recurring-context recall and detector quality remain method-conditional diagnostics rather than research questions. They become secondary questions only if `T-310` establishes a distinct retained capability role without disproportionate matrix growth.

### Provisional, falsifiable hypothesis candidates

These are pre-protocol candidates, not confirmed directional findings. `T-300`, `T-310`, `T-400`, and the pilots must replace the construct-level placeholders with the selected agent roles, validated estimands, unit of analysis, practical-effect or equivalence bounds, and final decision rules before the final evaluation is inspected.

- **H-P1 — online-adaptation recovery:** for at least one validated primary persistent-change condition, an information-matched role permitted to update online will have a more favorable post-change recovery profile than its corresponding frozen evaluation after nominal-performance cost is reported. It is falsified if the predeclared recovery and post-change estimands show no practically meaningful advantage, or show a disadvantage, across the retained primary conditions.
- **H-P2 — phase-dependent capability trade-off:** comparative conclusions will depend on evaluation phase: nominal performance, immediate resistance, and later recovery/post-change performance will not collapse into one invariant agent ordering. It is falsified if the predeclared role-by-phase contrasts are practically equivalent and ordering remains stable across the retained primary conditions.

No hypothesis asserts that ordinary Q-learning must fail, that a detector must activate usefully, or that a robust-MDP policy must recover. Those claims are excluded by the current evidence boundaries.

### Evidence-to-framing map

| Framing decision | Evidence | Supported use | Boundary retained |
|---|---|---|---|
| Compare agents under uncertainty/dynamic change and address resilience/recovery speed. | Official approved thesis application, represented by `REQ-RES-001` and `REQ-RES-003`. | Establishes the research objective and required constructs. | Does not prescribe algorithms, disturbance parameters, metrics, or statistical thresholds. |
| Make an unannounced persistent rule/dynamics change the primary recovery axis; keep observation/action disturbances as supporting diagnostics. | Official examples plus the citation-ready non-stationarity anchors summarized below. | Gives recovery a temporal changepoint interpretation while retaining the official uncertainty examples. | Exact change family, severity, onset, horizon, and observation/action mechanisms remain open. |
| Treat ordinary continual learning as a legitimate empirical comparator. | `SRC-70772C0629`. | Structured switching results prevent a blanket claim that ordinary Q-learning is inherently incapable under all non-stationarity. | Its assumptions and infinite-horizon convergence target do not predict rapid recovery after the thesis changepoint. |
| Validate detector behavior separately from return if a detector is retained. | `SRC-9464421E55`. | Requires finite-horizon activation, delay, and error diagnostics. | Its empirical results are from piecewise-stationary bandits and do not establish GridWorld superiority. |
| Separate development/tuning/pilots from frozen final evaluation. | `SRC-76B2247457`. | Prevents final-lifetime/change-schedule leakage into hyperparameter selection. | No universal tuning fraction or budget is imported from the paper. |
| Separate robustness within a declared uncertainty set from online changepoint adaptation. | `SRC-FC42D9798A`; `SRC-3C0F7CC819`. | Supports the frozen-robustness versus online-recovery construct distinction and conservativeness reporting. | Neither source detects changepoints or proves faster recovery; robust-comparator inclusion remains conditional. |

### Open feasibility and freeze gates

- `T-210`–`T-213`: select and validate a GridWorld whose hidden truth, agent observation, intended/executed actions, persistent change, and deterministic traces match the framing.
- `T-300`–`T-301` complete operational schema-v1 estimands and known-answer validation; pilots/freeze still select numeric windows/tolerance/stability, metric roles, and statistical aggregation.
- `T-310`–`T-312`: select a small feasible agent-role set, resolve any remaining citation gate, and validate information-matched implementations. A robust-MDP role may still be excluded even though conceptual support is now citation-ready.
- `T-400`–`T-410`: predeclare disjoint development/tuning/pilot/final partitions and use pilots to determine feasible budgets, severities, repetitions, variance handling, recovery behavior, and practical-effect criteria.
- `T-411`–`T-412`: refresh decision-driving literature, then freeze the final protocol, research questions, hypotheses, and statistical analysis plan before final results are inspected.

If prototypes or pilots cannot support scientifically distinct roles, identifiable recovery, or a feasible repeated-run design, the main question must be narrowed rather than forcing the current candidate framing.

## Research question freeze prerequisites

Already complete:

- official application analysis;
- complete bibliography import and evidence trust boundary;
- initial post-import evidence synthesis;
- technical architecture for information isolation, deterministic randomness, protocol partitions, run provenance, and automatic publication.
- accepted target-machine inventory and CPU-first runtime/tooling constraints (DEC-031).
- bounded GridWorld comparison/ADR/core/invariant validation (DEC-032; `T-210`–`T-213`).
- operational resilience estimands and synthetic known-answer validation (`T-300`/`T-301`).

Still required before final freeze:

1. exact small model-role/method set with evidence/feasibility rationale;
2. pilot evidence for runtime, variance, storage, recovery behavior, tuning budget, metric parameters/roles, and statistical choices.

## Valid research-question form

The final main RQ must identify:

- compared agent class/roles;
- environment and information assumptions;
- uncertainty/change regime;
- adaptation/evaluation regime;
- primary outcome constructs;
- scope within which conclusions are valid.

Secondary questions are added only for distinct scientific effects, validity checks, or explanatory trade-offs.

## Hypothesis policy

- No algorithm-specific or final directional hypothesis is currently confirmed; H-P1 and H-P2 are construct-level candidates.
- Hypotheses must follow verified theory/prior evidence and the final environment/model/metric design.
- Exploratory questions remain labelled exploratory rather than rewritten post hoc.
- Final hypotheses identify independent/dependent variables, expected direction/equivalence claim where appropriate, unit of analysis, and falsification criterion.

## Expected contribution

The likely contribution is comparative/empirical rather than invention of a new algorithm. Candidate contribution forms include:

- validated controlled evaluation environment;
- reproducible disturbance/change protocol;
- defensible operationalization of resilience/recovery;
- fair comparative evidence across distinct agent capabilities;
- reproducible software/provenance infrastructure;
- negative/boundary-condition findings.

The final contribution statement is written only after the final evidence exists.

## Threats to validity

### Internal
- unequal information/tuning access;
- implementation errors;
- leakage from final evaluation into selection;
- selective exclusions;
- inconsistent adaptation regimes.

### Construct
- ambiguous resilience/recovery definitions;
- invalid thresholds/windows;
- reward changes that destroy comparability;
- conflating training performance with resilience.

### External
- conclusions limited to selected GridWorld layouts/disturbances/compute regime;
- simplified environment properties;
- model set constrained by feasible local resources.

### Statistical
- insufficient independent seeds;
- treating nested episodes as independent replicates;
- post-hoc primary outcomes;
- censoring/non-recovery;
- inappropriate multiple-comparison handling.

### Reproducibility
- uncontrolled randomness;
- missing configs/provenance;
- mutable final results;
- manual final values;
- hidden third-party semantics.

## Freeze gate

This brief becomes frozen methodology only when every final question maps to validated environment factors, agents, estimands, and analysis; the design is feasible on measured hardware; pilot evidence resolves practical protocol choices; and the decision log records inclusions/exclusions and limitations.
