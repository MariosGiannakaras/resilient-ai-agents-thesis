# Draft Thesis Structure

**Status:** HISTORICAL/SUPERSEDED structure-only preparation. WP7/T-716 composition is complete; current thesis structure authority is `THESIS_STRUCTURE_AND_STYLE_GUIDE.md` plus the accepted T-716 DOCX. This outline remains only as pre-writing history and must not be used to reopen completed chapter architecture.

Chapter boundaries may be merged during WP7 if the approved examples/template show that a less fragmented structure is preferable.

## Front matter

- Greek title page.
- English title page.
- Required originality/copyright/declaration pages from the current official template.
- Optional dedication/acknowledgements if appropriate.
- Greek summary and keywords.
- English abstract and keywords.
- Table of contents.
- Lists of figures/tables.
- Glossary/acronyms where useful.

## 1. Introduction

- Problem context: resilient AI agents under uncertainty/environmental change.
- Official thesis purpose, title and bounded scope.
- Why GridWorld is a controlled testbed rather than the thesis subject.
- Final research questions:
  - RQ1 nominal learning performance/efficiency;
  - RQ2 resilience, Frozen/Adaptive loss and matched adaptation benefit;
  - RQ3 recovery speed, trajectory and non-recovery after persistent change.
- High-level contribution claim categories only; evidence-supported final contribution wording is deferred until T-613/WP7.
- Method overview and thesis organization.

## 2. Theoretical background

- Intelligent agents, reinforcement learning and sequential decision-making.
- Value-based, on-policy/off-policy, policy-gradient/actor-critic and model-based planning concepts needed for the retained methods.
- Uncertainty, non-stationarity and persistent environmental change.
- Robustness/resistance, adaptation and recovery as distinct constructs.
- Censoring/non-recovery and repeated/nested observations at the conceptual level.
- Reproducibility and information-fair evaluation.

## 3. Related work and research positioning

- Resilient/adaptive RL agents under non-stationarity.
- Controlled benchmark/GridWorld evaluation approaches.
- Robustness, degradation, adaptation-benefit and recovery-speed measurement.
- Fair multimethod comparison and continual-evaluation concerns.
- Identified empirical gap and bounded positioning of this thesis.
- Only canonical citation-ready bibliography evidence may support formal literature claims.

## 4. Controlled GridWorld testbed and uncertainty model

- Build/reuse/adapt decision and implementation/license provenance.
- Nominal state, action, transition, reward and truncation/bootstrap semantics.
- Agent-visible information contract versus evaluator hidden truth.
- Final held-out layout role and scenario provenance.
- Uncertainty/change families:
  - persistent action remapping;
  - action-execution failure;
  - observation corruption.
- Why persistent action remapping is the primary RQ3 recovery axis.
- Validation and synthetic/known-answer examples; no final outcomes here.

## 5. Compared methods and deployment regimes

- Final retained methods: Q-Learning, SARSA, DQN, PPO and Dyna-Q+.
- Scientific role of each method family.
- Method-specific implementation/checkpoint state.
- Independent Phase-A learning and same semantic observation/action contract.
- Frozen versus Adaptive/Continual deployment regimes as regimes, not algorithms.
- Historical/secondary methods (for example Dyna-Q/R0/A2C) only where needed to explain selection decisions; they are not final confirmatory competitors.
- Inclusion/exclusion and fair-tuning rationale from the frozen protocol decisions.

## 6. Methodology and experimental design

### 6.1 Protocol lifecycle and leakage controls
- Development/tuning/pilot/sizing/final separation.
- Final-reserve firewall and pre-outcome freeze.
- Immutable DEC-058 protocol-v2.0 history and explicit DEC-060 protocol-v2.1 amendment.

### 6.2 Phase A — nominal learning
- Independent training per method/root/layout.
- Common actual-environment-interaction budget.
- Exact no-learning probe checkpoints.
- RQ1 final-probe and time-average estimands.

### 6.3 Phase B — matched resilience/adaptation
- Exact Phase-A checkpoint restoration.
- Shared one-interaction no-learning prefix.
- Atomic FN/FD/AN/AD branch point.
- Persistent multi-episode continuation semantics.
- RQ2 directed Frozen loss, Adaptive loss and `(FN-FD)-(AN-AD)` adaptation benefit.

### 6.4 Recovery-speed operationalization
- Passive 32-interaction reward windows across the unchanged 256-interaction horizon.
- AN-versus-AD root-level matched trajectory.
- Equal layout reduction inside root before inference.
- Primary tolerance 0.10; sensitivity 0.05/0.20.
- Two-window stability rule.
- Recovery/confirmation time definitions.
- Right-censoring and explicit non-recovery.
- Restricted fixed-horizon delay kept distinct from recovery time.

### 6.5 Statistical comparison plan
- Root as independent unit; layouts/episodes/probes/windows as repeated/nested observations.
- Direct root-paired method A-minus-B contrasts.
- Actual-independent-root-count two-sided 95% Student-t pointwise intervals.
- Failure/missing-root handling and contrast eligibility.
- No formal p-value superiority family and no post-hoc significance relabeling.
- Predeclared sensitivity analyses.

### 6.6 Computational/resource evidence
- Actual environment interactions as primary fairness/accounting axis.
- Wall-clock, process CPU and interpretable method-native update counts as secondary descriptive evidence.

### 6.7 Validity and reproducibility controls
- Failure retention/no outcome-driven seed replacement.
- RNG separation/checkpoint identity/evidence hashes.
- Threat controls and interpretation boundaries.

## 7. Software architecture and implementation

- Framework-neutral Study aggregate and deterministic job plan.
- Scientific Phase-A/Phase-B executors and protocol-aware v2.1 routing.
- Exact checkpoints, continuation-state restoration and matched branch lineage.
- Temporal evidence capture without changing method-native learning boundaries.
- Evidence schemas, validation, root-level analysis and deterministic exports.
- Filesystem evidence as authority and derived indexes/read models.
- Risk-based tests, known-answer validation and CI.
- Hardware/software execution environment.

## 8. Research application and visualization

- DEC-059 PySide6 application architecture and research-interface role.
- Thesis Study review versus DEVELOPMENT/Exploratory Study flow.
- Durable Runs/progress and presentation-only live matched GridWorld.
- Stored-evidence Results:
  - nominal learning;
  - Frozen/Adaptive loss and adaptation benefit;
  - recovery summaries/AN-vs-AD trajectories;
  - direct method contrasts.
- Artifact/provenance inspection.
- Explicit boundary: UI does not choose thresholds, recompute estimands or become scientific authority.
- Screenshots/assets only with provenance and only where they clarify the implementation/research workflow.

## 9. Experimental results — **BLOCKED until accepted final evidence**

This chapter is an outline only. Do not populate numeric values, rankings, claims or narrative before T-610–T-613 are complete and accepted.

Planned evidence order:

- final evidence completeness, retained failures and denominators;
- **RQ1:** nominal final-probe performance and learning efficiency/time-average comparison;
- **RQ2:** Frozen loss, Adaptive loss and matched adaptation benefit by condition;
- **RQ3:** action-remap recovery status, recovery trajectories, conditional observed recovery time, restricted fixed-horizon delay and non-recovery;
- predeclared direct method contrasts with stored pointwise intervals;
- supporting action-failure/observation-corruption diagnostics;
- sensitivity analyses;
- secondary computational/resource observations.

Every figure/table must be generated from registered validated evidence and carry traceable provenance.

## 10. Discussion — **BLOCKED until Chapter 9 evidence is accepted**

Planned structure only:

- direct evidence-bounded answer to RQ1;
- direct evidence-bounded answer to RQ2;
- direct evidence-bounded answer to RQ3;
- comparison with theory/related work without exceeding source or experimental scope;
- trade-offs and boundary conditions;
- negative/unexpected findings if present;
- distinction between capability, resistance, adaptation benefit and recovery;
- practical/scientific implications limited to the controlled setting.

## 11. Threats to validity and limitations

- Internal validity and implementation/information fairness.
- Construct validity of resilience/adaptation/recovery definitions.
- Statistical validity: independent roots, blocking, failures, censoring, pointwise comparisons.
- External validity: selected GridWorld layouts/disturbances/five methods/local CPU environment.
- Reproducibility and evidence/provenance limitations.
- Mitigations and residual uncertainty supported by the final evidence audit.

## 12. Conclusions and future work — **final claims deferred**

- Objective/method recap.
- Evidence-supported findings only after Results/Discussion are accepted.
- Final contribution statement only after final evidence exists.
- Limitations and realistic extensions.

## Bibliography

Only verified sources actually cited in the text, using the canonical bibliography/citation-ready workflow.

## Appendices

- Frozen protocol/config schemas where useful.
- Extended result tables/plots not needed in the main text.
- Validation/reproducibility details.
- Reproduction instructions.
- Selected relevant code/config excerpts rather than a full source dump.
- Study/run/artifact provenance register and evidence-map references.
