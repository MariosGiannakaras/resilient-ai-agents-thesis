# Research Brief

**Status:** `RESEARCH_REQUIRED` except where explicitly marked `CONFIRMED`.

This file defines the research problem and the process for deriving the final questions. It does not preserve model, metric, GridWorld-rule or experimental preferences from old conversations.

## Identity

- **Greek title — CONFIRMED:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα.
- **English title — CONFIRMED:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments.
- **Institution — CONFIRMED:** Πανεπιστήμιο Δυτικής Αττικής, Σχολή Μηχανικών, Τμήμα Μηχανικών Πληροφορικής και Υπολογιστών.

## Official subject and problem

- **CONFIRMED:** Study and comparative evaluation of resilient AI decision agents under uncertainty and dynamic environmental changes.
- **CONFIRMED:** Use of a simple simulated environment; GridWorld is the current project direction.
- **CONFIRMED:** Official examples include data/observation noise, rule changes and failed action execution.
- **CONFIRMED:** Evaluation must address resilience and recovery speed.
- **RESEARCH_REQUIRED:** Operational definitions of agent, resilience, adaptation, uncertainty, dynamic change and recovery for this thesis.

## Research-question generation

The final main and secondary research questions are **not yet written**. They must be generated after:

1. analysis of the official application,
2. review of the user's real bibliography,
3. fresh primary/peer-reviewed literature search,
4. current GridWorld landscape review and environment-class decision,
5. automated system inventory and feasibility measurements,
6. supervisor/user review where required.

A valid main research question must specify:

- the exact class of decision agents being compared,
- the environment and information assumptions,
- the uncertainty/change conditions,
- the adaptation/evaluation regime,
- the primary outcome constructs,
- the scope within which conclusions are valid.

Secondary questions may be added only when they estimate a distinct effect, test a validity threat or explain a relevant trade-off. They must not be added merely to justify a preferred model or feature.

## Hypothesis policy

- **OPEN:** No directional or model-specific hypothesis is confirmed.
- Hypotheses must follow from verified theory or prior evidence, not from model names mentioned in old chats.
- Every hypothesis must identify independent/dependent variables, expected direction or equivalence/non-inferiority claim where appropriate, unit of analysis and falsification criterion.
- Exploratory questions must remain labeled exploratory rather than being rewritten post hoc as hypotheses.

## Expected contribution

The exact contribution is **RESEARCH_REQUIRED**. The official topic is compatible with a comparative empirical contribution; it does not require invention of a new algorithm.

Possible contribution categories to evaluate, without selecting them in advance, include:

- a validated controlled evaluation environment,
- a reproducible uncertainty/disturbance protocol,
- operational definitions and measurements of resilience/recovery,
- a scientifically fair comparative study,
- transparent software/provenance infrastructure supporting the study,
- negative or boundary-condition findings that clarify where methods do or do not work.

The final contribution statement must be supported by literature-gap analysis and actual results.

## Role of project components

- **GridWorld — CONFIRMED:** Controlled simulated environment; implementation and exact specification remain open.
- **Models/agents — CONFIRMED:** Objects of comparison; no shortlist exists.
- **Experiments — CONFIRMED:** Primary evidence-production mechanism.
- **Dashboard — CONFIRMED:** Supporting control, observation, comparison and export tool; not the scientific core.
- **Thesis — CONFIRMED:** Greek Microsoft Word synthesis of verified sources, methodology, implementation and real results.

## Variable-definition workspace

No final variable list is frozen. The research phase must define and justify:

### Independent/explanatory factors
- agent identity/capability dimension,
- environment/scenario identity,
- uncertainty/change type and severity,
- timing and duration of change,
- information/observability assumptions,
- training, adaptation and evaluation regime,
- controlled resource/tuning conditions.

### Outcomes
- nominal task performance,
- immediate impact of disruption,
- recovery behavior and post-change performance,
- reliability/variability across independent runs,
- resource cost where scientifically relevant.

### Blocking/nuisance factors
- seed and repetition,
- layout/scenario,
- implementation/software version,
- hardware/load for timing measurements,
- tuning effort and checkpoint-selection rule.

Exact variables and measurement formulas require literature and protocol decisions.

## Threats to validity to address

### Internal validity
- implementation errors,
- unequal tuning or information access,
- leakage from final evaluation into selection,
- selective run exclusion,
- inconsistent adaptation regimes.

### Construct validity
- ambiguous definitions of resilience or recovery,
- metrics that do not represent the intended construct,
- reward changes that break comparability,
- conflating training performance with evaluation resilience.

### External validity
- conclusions limited to the selected environment, layouts, disturbances and compute regime,
- simplified GridWorld properties not representing broader domains,
- model selection constrained by feasible local resources.

### Statistical conclusion validity
- insufficient independent repetitions,
- dependence between nested observations,
- post-hoc outcome selection,
- multiple comparisons,
- censored/non-recovered runs and heavy-tailed results.

### Reproducibility
- uncontrolled randomness,
- missing source/config/environment metadata,
- mutable raw results,
- manually edited final values,
- third-party source/version/license ambiguity.

## Research freeze gate

The research brief may be marked frozen only when:

- the source review is documented,
- the main and secondary questions are approved,
- hypotheses/exploratory questions are clearly separated,
- every question maps to environment factors, agents, metrics and analysis,
- the proposed scope is feasible on the measured system,
- the decision log records important alternatives and exclusions.
