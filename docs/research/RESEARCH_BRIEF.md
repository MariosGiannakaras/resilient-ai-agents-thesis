# Research Brief

**Status:** Active post-import research workspace; final RQ/hypotheses are not frozen.

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
- `SRC-76B2247457` — supports a strict tuning/pilot/final-evaluation boundary in continual-RL evaluation.

Robust-MDP full-corpus sources may inform internal comparator research but require citation-ready verification/promotion before supporting a final formal claim if retained.

## Current bounded direction — proposed, not frozen

- Separate robustness from post-change adaptation/recovery.
- Use persistent rule/dynamics change as the leading recovery axis.
- Keep observation corruption and action-execution failure as supporting robustness diagnostics unless a distinct final RQ justifies more.
- Compare a small number of scientifically distinct capability roles, not a catalogue of algorithms.
- Preserve nominal performance, immediate/worst degradation, recovery trajectory/time, post-change performance, non-recovery, and across-run uncertainty.
- Keep development/tuning/pilot/final scenarios separated and prevent information leakage.
- Keep the final matrix CPU-feasible under the accepted target-machine baseline; the detected Radeon adapter is not a validated scientific-compute backend.

## Research question freeze prerequisites

Already complete:

- official application analysis;
- complete bibliography import and evidence trust boundary;
- initial post-import evidence synthesis;
- technical architecture for information isolation, deterministic randomness, protocol partitions, run provenance, and automatic publication.
- accepted target-machine inventory and CPU-first runtime/tooling constraints (DEC-031).

Still required before final freeze:

1. bounded GridWorld prototype/ADR decision;
2. explicit environment/observability/change semantics;
3. exact small model-role/method set with evidence/feasibility rationale;
4. operational metric estimands and known-answer validation;
5. pilot evidence for runtime, variance, storage, recovery behavior, tuning budget, and statistical choices.

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

- No directional/model-specific hypothesis is currently confirmed.
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
