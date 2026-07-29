# Research Brief

Every item is labeled `CONFIRMED`, `PROVISIONAL`, `PROPOSED`, or `OPEN`.

## Identity

- **Greek title — CONFIRMED:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα.
- **English title — CONFIRMED:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments.
- **Institution — CONFIRMED:** Πανεπιστήμιο Δυτικής Αττικής, Σχολή Μηχανικών, Τμήμα Μηχανικών Πληροφορικής και Υπολογιστών.

## Subject and problem

- **CONFIRMED:** Study and comparative evaluation of resilient AI decision agents under uncertainty and dynamic changes.
- **CONFIRMED:** Use of a simple simulated environment; GridWorld is the chosen project direction.
- **CONFIRMED:** Official examples of disruptions include data/observation noise, rule changes and failed action execution.
- **CONFIRMED:** Evaluation must address resilience and recovery speed.
- **OPEN:** Exact operational definition of “resilient agent” for this thesis.

## Provisional main research question

- **PROVISIONAL:** How do selected decision-making agents differ in task performance, degradation and recovery when exposed to controlled uncertainty and dynamic changes in a common GridWorld environment, under comparable evaluation conditions and feasible local compute budgets?

This wording is not final until literature, supervisor input and environment/model scope are reviewed.

## Provisional secondary questions

1. **PROPOSED:** How does each uncertainty type and severity affect immediate performance degradation?
2. **PROPOSED:** Which agents recover faster and to what fraction of their pre-disruption performance?
3. **PROPOSED:** Do rankings remain stable across GridWorld layouts and disturbance schedules?
4. **PROPOSED:** What trade-offs exist between resilience, sample efficiency, runtime and implementation complexity?
5. **PROPOSED:** Does access to memory, planning or an environment model provide measurable benefit only under specific uncertainty classes?
6. **PROPOSED:** How sensitive are conclusions to seeds, metric definition and evaluation budget?

## Hypotheses

- **OPEN:** No directional hypothesis is confirmed.
- **PROPOSED FOR LATER TESTING:** Planning/model-based or memory-enabled methods may recover more effectively under certain non-stationary or partially observable conditions, but may cost more compute or data.
- **PROPOSED FOR LATER TESTING:** Simple tabular baselines may remain competitive in small fully observable environments and provide essential calibration.
- These proposals must not appear as findings before testing.

## Expected contribution

- **PROVISIONAL:** A reproducible benchmark protocol for controlled resilience evaluation in a compact GridWorld.
- **PROVISIONAL:** An explicit taxonomy and parameterization of uncertainty/dynamic changes.
- **PROVISIONAL:** A comparative empirical analysis with multiple runs, effect estimates and recovery-focused metrics.
- **PROVISIONAL:** A local dashboard that exposes real experiment state and generates traceable artifacts.
- **OPEN:** Whether a novel algorithm is required. The official topic permits comparative evaluation; novelty can arise from the experimental framing, benchmark, metrics, analysis or implementation, subject to supervisor expectations.

## Role of components

- **GridWorld — CONFIRMED:** Controlled test environment and disturbance generator.
- **Models — CONFIRMED:** Objects of comparison; final set open.
- **Experiments — CONFIRMED:** Primary evidence production mechanism.
- **Dashboard — CONFIRMED:** Supporting control/visualization/export tool, not the scientific core.
- **Thesis — CONFIRMED:** Greek Microsoft Word synthesis of verified sources, methodology and real results.

## Variables

### Candidate independent variables
- Agent/model family and version.
- GridWorld layout/configuration.
- Uncertainty/disturbance type.
- Disturbance severity.
- Disturbance onset, duration and schedule.
- Observation level/full vs partial observability, if included.
- Training/evaluation budget.
- Seed/repetition.
- Hyperparameters within a documented tuning policy.

### Candidate dependent variables
- Success rate, return and episode length.
- Immediate performance drop.
- Recovery time and recovered-performance ratio.
- Area of performance loss after disruption.
- Failure/collision/invalid-action rates.
- Sample efficiency and generalization gap.
- Wall-clock, CPU/RAM and supported GPU/VRAM use.

### Controlled or blocked variables
- Common environment version and evaluation scenarios.
- Comparable evaluation episodes and disturbance schedules.
- Software/hardware versions.
- Tuning data separated from final evaluation data.
- Logging and metric computation version.

## Threats to validity

### Internal
- Implementation bugs in transitions, rewards or metrics.
- Unequal tuning effort or compute budget.
- Leakage from final scenarios into model selection.
- Seed dependence and selective run exclusion.
- UI or logging overhead changing timing results.

### Construct
- A resilience metric may not represent the intended concept.
- Average return may hide failure/recovery dynamics.
- GridWorld simplification may omit real-world properties.
- “Recovery” may be ambiguous for agents that do or do not learn online during evaluation.

### External
- Findings from a small GridWorld may not generalize to complex environments.
- Results may depend on specific disturbance taxonomy/layouts.
- Hardware constraints may exclude larger methods.

### Statistical conclusion
- Too few repetitions.
- Multiple comparisons and post-hoc metric selection.
- Non-normal/heavy-tailed run distributions.
- Dependence between repeated observations.

### Reproducibility
- Uncontrolled nondeterminism.
- Missing dependency, hardware or configuration metadata.
- Mutable raw results or manually edited thesis values.
