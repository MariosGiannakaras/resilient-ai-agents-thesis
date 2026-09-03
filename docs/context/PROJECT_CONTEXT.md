# Project Context

## Status taxonomy

- **CONFIRMED:** established by approved application, explicit user direction, accepted decision or validated evidence.
- **FROZEN:** predeclared and not changeable from final outcomes.
- **SUPERSEDED:** preserved history that no longer controls future execution.
- **DEFERRED:** intentionally later and non-blocking now.

## Project identity

Official thesis titles:

- Greek: **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**
- English: **Comparison and Evaluation of Resilient AI Agents in Uncertain Environments**

GridWorld is the controlled experimental testbed and visualization environment, not the thesis subject. Final thesis language is Greek and the final academic document is Microsoft Word unless later official guidance changes this.

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` owns discovery, originals, conversion/OCR, scientific analysis, evidence verification and citation-ready corpus generation. This repo consumes versioned generated output read-only.

The current major-writing-gate consumer checkout is pinned to upstream SHA `ada0d1aec7511098fd12610ae9e5abe7aea875cd` through thesis PR #130. Integrated integrity records 599 canonical sources, 123 citation-ready sources, 19 research materials and 281 indexed originals. Historical SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5` and `bibliography-integration-v3` remain immutable prior-snapshot provenance terminology; generated bibliography content is never hand-edited here.

## Immutable historical science

- `protocol-v1.0`, FINAL-* bundles and frozen v1.0 analysis/evidence are immutable historical evidence.
- Historical R0 pilot evidence remains negative/diagnostic and is not rewritten.
- Candidate protocol-v1.1 and its F0/C0/D0-era implementation remain auditable non-final history only.
- Old v1.1 final/tuning execution paths are superseded and must not be restarted.
- DEC-058 and `configs/protocols/protocol-v2.0-final.json` remain immutable historical protocol-v2.0 freeze authority.

## Current science — protocol v2.1

DEC-060 explicitly amends DEC-058 before any final-reserve execution. `configs/protocols/protocol-v2.1-final.json` is the self-contained current scientific authority.

### RQ1 — nominal learning

Compare independently trained Q-Learning, SARSA, DQN, PPO and Dyna-Q+ under the same semantic environment, agent-visible information contract and principal actual-environment-interaction budget. Primary evidence is standardized Phase-A no-learning probe performance, with final nominal value and learning-trajectory/time-average summaries.

### RQ2 — resilience/adaptation

For each method/root/layout, Phase B starts from that unit's own exact Phase-A scientific checkpoint and matched branch point:

- **FN — Frozen nominal**;
- **FD — Frozen disturbed**;
- **AN — Adaptive nominal**;
- **AD — Adaptive disturbed**.

Primary adaptation benefit is `(FN-FD)-(AN-AD)`. Frozen and Adaptive are deployment regimes, not separate algorithms.

### RQ3 — recovery speed

Primary recovery family is persistent action remapping; supporting disturbance families remain diagnostics. Recovery is based on passive 32-interaction reward windows over the unchanged 256-interaction Phase-B horizon, comparing AN with AD after equal layout reduction inside each root.

Primary tolerance is `AN - AD <= 0.10`; sensitivity tolerances are `0.05` and `0.20`. Stable recovery requires two consecutive in-tolerance windows. Non-recovery is right-censored with `recovery_time=null`; cross-method comparison separates recovery status from the restricted fixed-horizon recovery delay.

See `docs/research/RQ_EVIDENCE_TRACEABILITY.md` for the concise RQ → evidence → estimand → output map.

## Fair experimental contract

Fairness does not mean equal hyperparameters or equal optimizer updates.

- same project-owned task/environment semantics and agent-visible information;
- common principal actual environment-interaction learning budget;
- method-appropriate selected hyperparameters and native update mechanics;
- 12 independent final roots and 2 held-out final layouts as frozen by protocol-v2.1;
- standardized no-learning Phase-A probes/checkpoint semantics;
- exact matched FN/FD/AN/AD Phase-B branching;
- no final-reserve tuning or outcome-driven root/seed replacement;
- scientific failures remain retained outcomes;
- layouts/episodes/probes/windows are repeated observations, not independent replicates.

Exact continuation state is method-native. DQN replay/target/optimizer/exploration state, PPO optimizer/schedule/RNG/update-boundary state and Dyna-Q+ model/recency/planning state are part of the scientific checkpoint where required.

## Scientific implementation foundation

Current reusable infrastructure includes:

- Python 3.12 + locked `uv` research environment;
- project-owned Gymnasium GridWorld and strict evaluator-vs-agent information boundary;
- deterministic separated RNG streams;
- project Q-Learning, SARSA and Dyna-Q+ implementations;
- Stable-Baselines3 DQN/PPO exact scientific-state adapters on CPU-only PyTorch;
- actual-interaction Phase-A execution and isolated no-learning probes;
- exact scientific checkpoint/restore/continuation and matched Phase-B branch cloning;
- passive protocol-v2.1 temporal reward windows;
- immutable `StudyRecipe`, deterministic Study job plan, durable `StudyStore`, stage barriers and restart-safe scheduler;
- framework-neutral `StudyService` with deny-by-default confirmatory/final execution authorization;
- schema-v2 validation, equal-layout root reduction, recovery/direct method contrasts and deterministic v2 evidence exports;
- read-only pre-final readiness checks and a synthetic DEVELOPMENT-only end-to-end scientific-pipeline smoke.

The first final-reserve attempt stopped fail-closed at 216/603 jobs and remains preserved unfinalized and excluded. The DEC-062 replacement completed and finalized 603/603 jobs from one clean corrected commit; T-611 validated and froze only that replacement. T-612 reproduced and interpreted only the predeclared analysis, and T-613 deterministically finalized the registered thesis/appendix/defense evidence assets from T-612 alone.

## Accepted application architecture

DEC-059 remains the **PySide6 / Qt 6 Widgets framework/runtime authority** over the framework-neutral Study backend. DEC-061 fixes the accepted experiment-first product/UX model. Historical Streamlit/React/NiceGUI implementations are superseded and exist only as history/reference.

The accepted application architecture is:

> **Experiment / Run / Results / Evidence**

The user should understand the scientific experiment before StudyStore/jobs/artifacts:

- all five final methods are fixed in the Thesis experiment;
- Phase A is nominal learning;
- each exact Phase-A state enters matched Phase B;
- Frozen means learning off and Adaptive means learning continues;
- Frozen/Adaptive are simultaneous matched regimes, not algorithms or alternatives;
- Results answer RQ1 Learning, RQ2 Resilience/Adaptation and RQ3 Recovery;
- Evidence exposes validation/exports/readiness first and reproducibility internals on demand.

The UI preserves UI-neutral Study/results/evidence read models, execution supervision/policy, live-observer/event and provenance behavior. Scientific reduction, thresholds, recovery decisions, intervals, RNG, checkpoint identity and finalization never move into Qt state. Technical IDs, roots/layouts, states/observations, hashes and lineage use progressive disclosure rather than dominate primary screens.

Final standalone Windows packaging remains post-thesis/deferred and is not a blocker for WP7 drafting.

## Repository state and hygiene

`main` is the only implementation base. Historical scientific/evidence history remains in Git and must not be rewritten. Remote merged/stale working branches may be removed after confirming they contain no unique required work; deliberate archive/provenance branches may remain.

## Current lifecycle

Canonical concrete state is in `TASKS.md` and `CURRENT_STATUS.md`.

1. Protocol-v2.1 scientific authority, final execution/recovery, T-611 evidence freeze, T-612 statistical analysis and T-613 deterministic thesis/defense assets are complete.
2. The accepted PySide6 experiment-first application is complete through T-534/T-535/T-536 and active-tree cleanup T-537.
3. Explicit pre-WP7 user approval is satisfied.
4. T-700 official-guidance recheck and T-701 example-thesis structure/style review are complete.
5. T-702 major-writing-gate literature freshness review and immutable bibliography consumer re-sync are complete at checkout `ada0d1aec7511098fd12610ae9e5abe7aea875cd`; the refresh changed no frozen scientific design/evidence/results/assets.
6. `T-710` complete Greek thesis drafting is the next dependency-valid task.
7. Supervisor corrections/review-ready Word/final freeze, defense work, final audits and standalone Windows packaging remain downstream under their declared tasks.

No green CI, UI screenshot, synthetic smoke, repository cleanup or writing convenience authorizes changing frozen scientific evidence or redefining accepted estimands/results. T-710 prose must map to the accepted T-611/T-612/T-613 artifacts and synchronized citation-ready bibliography.
