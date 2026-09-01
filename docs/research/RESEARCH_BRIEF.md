# Research Brief

**Status:** Active pre-final research authority; RQ1/RQ2/RQ3 frozen by DEC-060 before final-reserve execution.  
**Protocol authority:** `configs/protocols/protocol-v2.1-final.json`  
**Historical authority retained:** DEC-058 / `configs/protocols/protocol-v2.0-final.json`

This file states the active research framing only. Historical/pre-import framing remains auditable history but does not override DEC-060 or the self-contained protocol-v2.1 authority.

## Confirmed identity and purpose

- **Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα.
- **English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments.
- **Institution:** University of West Attica, School of Engineering, Department of Informatics and Computer Engineering.
- GridWorld is the controlled experimental and visualization testbed, not the thesis subject.
- The study compares five retained reinforcement-learning methods under a shared controlled task and agent-visible information contract.
- The official uncertainty examples remain represented by persistent rule/dynamics change, action-execution failure and observation corruption.
- Evaluation explicitly separates nominal learning, degradation/resilience, adaptation benefit and recovery speed/non-recovery.

## Evidence state and literature boundary

The bibliography corpus is imported and pinned. Formal thesis claims use the canonical citation-ready layer rather than ad-hoc external citations.

Decision-driving anchors already retained in the project include:

- `SRC-70772C0629` — structured switching/non-stationarity cautions against blanket claims that ordinary Q-learning is universally incapable;
- `SRC-9464421E55` — supports finite-horizon validation of detection/restart behavior when such mechanisms are studied;
- `SRC-76B2247457` — supports strict tuning/pilot/final-evaluation separation in continual-RL evaluation;
- `SRC-FC42D9798A` and `SRC-3C0F7CC819` — support the conceptual distinction between robustness inside an explicit uncertainty set and recovery after an unknown persistent change.

These sources motivate constructs and validity boundaries; they do not predetermine the final ranking of the five retained methods.

## Final research questions

### RQ1 — Nominal learning

Under the common controlled GridWorld task, shared agent-visible information contract and common actual-environment-interaction budget, how do Q-Learning, SARSA, DQN, PPO and Dyna-Q+ differ in nominal learning performance and learning efficiency?

Operational mapping:

- Phase A independently trains every method from method-appropriate initialization.
- Primary nominal estimand: final no-learning probe performance.
- Secondary nominal estimand: predeclared time-average learning-trajectory performance.
- Independent statistical unit: root identity.
- The two final layouts are repeated/blocked observations and are equally reduced within root before inference.
- Direct comparisons use root-paired method A-minus-B contrasts on shared independent roots.

Interpretation is limited to the controlled task, information contract, actual-interaction budget and selected method configurations; it is not a universal algorithm ranking.

### RQ2 — Resilience and adaptation benefit

After controlled uncertainty/change, how much does each retained method degrade, and how much does ordinary continued online learning reduce disturbance-associated loss relative to its matched frozen deployment?

Operational mapping:

- Phase B uses exact matched `FN`, `FD`, `AN`, `AD` branches from one scientific branch point.
- Frozen and Adaptive/Continual are deployment regimes, not separate algorithms.
- All four frozen Phase-B conditions remain in the final matrix.
- Directed Frozen loss and Adaptive loss preserve metric direction.
- Matched adaptation benefit remains `(FN-FD)-(AN-AD)` after direction normalization.
- Roots are independent; layouts are equally reduced within root before inference.
- Direct root-paired method contrasts are predeclared for adaptation benefit and, secondarily, Frozen/Adaptive loss.

Adaptation benefit is not recovery speed and must not be described as such.

### RQ3 — Recovery speed and non-recovery

After persistent unannounced change, how quickly does each adaptive method return to its matched adaptive-nominal performance neighborhood, what trajectory does it show, and when does it fail to recover within the fixed observation horizon?

Operational mapping:

- Primary recovery family: persistent `action-remap` conditions.
- Action-failure and observation-corruption remain supporting robustness/adaptation diagnostics.
- Matched branches: Adaptive-Nominal (`AN`) versus Adaptive-Disturbed (`AD`).
- Primary trajectory metric: mean reward per actual environment interaction in deterministic 32-interaction windows.
- Horizon: 256 post-boundary interactions, yielding 8 windows with endpoints 32, 64, 96, 128, 160, 192, 224 and 256.
- Episode boundaries do not reset or realign the windows.
- The two final layouts are equally weighted within root at each window before recovery inference.
- Higher-is-better directed gap: `AN - AD`.
- Primary recovery tolerance: `0.10` reward per interaction; sensitivity tolerances: `0.05` and `0.20`.
- Stability requirement: two consecutive in-tolerance windows.
- Recovery time: end of the first window in the first stable run; confirmation time: end of the second required window.
- If no stable run is confirmed, the root is right-censored at interaction 256 with `recovery_time=null`; 256 is never fabricated as a recovery time.
- Recovery-time summaries are explicitly conditional on observed recovery. A separately named restricted fixed-horizon recovery-delay estimand may use the horizon for censored roots for method comparison without reclassifying those roots as recovered.

The 0.10 tolerance was fixed before final outcomes from the known task reward scale (`step=-0.1`, `collision=-0.25`, `goal=1.0`), not selected from final-reserve behavior.

## Frozen method set and information fairness

The final method set is exactly:

1. Q-Learning;
2. SARSA;
3. DQN;
4. PPO;
5. Dyna-Q+.

Each method receives the same semantic position observation and action space. Neural methods may encode that observation numerically but receive no pixels, hidden map truth, disturbance flags, change indicator, regime identity or executed-action feedback unavailable to the tabular methods.

The primary fairness axis is actual environment interactions, not identical algorithm hyperparameters or identical numbers of optimizer/planning updates. Method-appropriate hyperparameters are frozen from the completed tuning/sizing process.

## Final experimental structure

- Phase-A training budget: 8,192 actual environment interactions per method/root/layout.
- Final independent roots: 12.
- Final held-out layouts: 2.
- Phase-B conditions per layout: 4.
- Phase-B post-boundary horizon: 256 actual interactions per branch.
- Common nominal no-learning prefix before branching: 1 interaction.
- Branches: exact `FN`, `FD`, `AN`, `AD`.
- Failures remain scientific outcomes; roots/seeds are never replaced from observed outcomes.
- Final layouts/seeds remain sealed until separate T-610 authorization.

## Statistical interpretation policy

- Root is the independent unit; episodes, layouts, probes and temporal windows are not independent replicates.
- Layouts are equally reduced inside each root before method inference.
- Direct comparisons are method A-minus-B on common independent roots.
- Two-sided 95% Student-t pointwise intervals use the predeclared critical value corresponding to the actual independent-root count `n=2..12`.
- No formal p-value superiority family is authorized by DEC-060.
- Pointwise interval overlap/non-overlap must not be relabeled post hoc as “statistical significance”.
- No composite resilience score is introduced.
- Recovery censoring and non-recovery remain explicit rather than being silently converted into complete recovery times.

## Computational evidence

Actual environment interactions remain the primary fairness/accounting axis. Wall-clock time, process CPU time and method-native update counts where scientifically interpretable are secondary descriptive evidence. They do not define a new primary research question.

## Threats to validity retained

### Internal

- unequal information or tuning access;
- implementation errors or hidden state resets;
- final-reserve leakage into selection;
- selective failures/exclusions;
- mismatched Frozen/Adaptive branch origins.

### Construct

- conflating nominal capability, immediate degradation, adaptation benefit and recovery speed;
- threshold/window definitions that are selected from outcomes;
- treating supporting stochastic disturbances as the same construct as persistent-change recovery.

### External

- conclusions remain limited to the selected GridWorld task, held-out layouts, disturbances, local CPU regime and five retained configurations.

### Statistical

- treating layouts/episodes/windows as independent;
- unreported missing/scientific-failure roots;
- incorrect pairing after asymmetric failures;
- ignoring right-censoring/non-recovery;
- post-hoc multiplicity or significance claims.

### Reproducibility

- uncontrolled randomness;
- mutable recipe/evidence artifacts;
- incomplete checkpoint or RNG continuity;
- manual result values detached from registered evidence lineage.

## Final-reserve gate

`final_reserve_access=false` remains in force. T-533 may validate mechanics only with synthetic/non-final evidence. T-610 requires a separate explicit scientific authorization after T-533 implementation, documentation and affected CI are complete. No final results, Results/Discussion prose, or outcome-driven protocol changes are authorized by this brief.
