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

The current protocol-v2 consumer snapshot is pinned to upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5` through thesis PR #96. `bibliography-integration-v3` remains immutable historical terminology; generated bibliography content is not hand-edited here.

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

The final reserve has not been executed or inspected.

## Application architecture and current restart

DEC-059 remains the **PySide6 / Qt 6 Widgets framework/runtime authority** over the framework-neutral Study backend. DEC-061 is the current T-534 product/UX amendment. Historical Streamlit/React/NiceGUI implementations are superseded and exist only as history/reference.

The T-534 application is **experiment-first**. Its primary user-facing architecture is:

> **Experiment / Run / Results / Evidence**

The user should understand the scientific experiment before StudyStore/jobs/artifacts:

- all five final methods are fixed in the Thesis experiment;
- Phase A is nominal learning;
- each exact Phase-A state enters matched Phase B;
- Frozen means learning off and Adaptive means learning continues;
- Frozen/Adaptive are simultaneous matched regimes, not algorithms or alternatives;
- Results answer RQ1 Learning, RQ2 Resilience/Adaptation and RQ3 Recovery;
- Evidence exposes validation/exports/readiness first and reproducibility internals on demand.

The previously paused/historical UI implementation is not the basis for continued presentation work. T-534 starts from fresh current `main` and derives its design from current protocol-v2.1/scientific contracts and DEC-061 rather than pre-v2.1 assumptions.

Existing `src/resilient_agents/desktop/` code must be classified before replacement:

- preserve UI-neutral Study/results/evidence read models, execution supervision/policy, live-observer/event and provenance behavior that still encodes current backend contracts;
- reuse truthful GridWorld drawing primitives where useful;
- presentation widgets/windows/pages/styles/navigation/copy may be replaced from scratch as needed;
- remove active protocol-v2.0/DEC-058-only/T-528 presentation assumptions;
- never move scientific reduction, thresholds, recovery decisions, intervals, RNG, checkpoint identity or finalization into Qt state;
- UI displays validated stored evidence and DEVELOPMENT/synthetic fixtures only during implementation/testing;
- no UI action may bypass the separate final-scientific-experiment authorization gate.

Run must prioritize the GridWorld: one large nominal panel in Phase A and two exact-matched large Frozen/Adaptive panels side-by-side in Phase B. Results are organized explicitly by RQ1/RQ2/RQ3. Technical IDs, roots/layouts, states/observations, hashes and lineage use progressive disclosure rather than dominate primary screens.

Final standalone Windows packaging remains post-thesis/deferred and is not a blocker for the UI restart.

## Repository state and hygiene

`main` is the only implementation base. Historical scientific/evidence history remains in Git and must not be rewritten. Remote merged/stale working branches may be removed after confirming they contain no unique required work; deliberate archive/provenance branches may remain.

For the UI implementation, use one fresh branch from current `main` and one corresponding PR. Do not continue an old paused worktree or branch.

## Current lifecycle

Canonical concrete state is in `TASKS.md` and `CURRENT_STATUS.md`.

1. Protocol-v2.1 scientific authority, recovery/comparison amendment and pre-final readiness hardening are complete.
2. DEC-061 now fixes the experiment-first T-534 product/UX contract without changing science.
3. T-534 UI implementation is allowed without opening the final reserve.
4. Final scientific execution remains blocked by a separate explicit authorization gate.
5. Validation/analysis/evidence packaging follow only after the authorized final execution.
6. Explicit user approval is still required before thesis Results/Discussion/WP7 writing.
7. Final Windows standalone packaging remains deferred until after the thesis.

No green CI, UI screenshot, synthetic smoke, repository cleanup or completed implementation task by itself authorizes the final scientific experiment or thesis Results/Discussion writing.
