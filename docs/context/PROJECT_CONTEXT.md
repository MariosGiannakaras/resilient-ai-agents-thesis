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

GridWorld is the controlled experimental testbed and visualization environment, not the thesis subject. Final thesis language is Greek and the final editable academic document is Microsoft Word unless later authoritative guidance changes this.

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` owns discovery, originals, conversion/OCR, scientific analysis, evidence verification and citation-ready corpus generation. This repo consumes versioned generated output read-only.

The current major-writing-gate consumer checkout is pinned to upstream SHA `ada0d1aec7511098fd12610ae9e5abe7aea875cd` through thesis PR #130. Integrated integrity records 599 canonical sources, 123 citation-ready sources, 19 research materials and 281 indexed originals. Historical SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5` and `bibliography-integration-v3` remain immutable prior-snapshot provenance terminology; generated bibliography content is never hand-edited here.

T-710 formal manuscript citations use stable citation-ready `SRC-*` placeholders. PR #132 consumer validation caught and removed a corpus-only source residue before merge, so T-711 starts from a bibliography-valid manuscript state.

## Immutable historical science

- `protocol-v1.0`, FINAL-* bundles and frozen v1.0 analysis/evidence are immutable historical evidence.
- Historical R0 pilot evidence remains negative/diagnostic and is not rewritten.
- Candidate protocol-v1.1 and its F0/C0/D0-era implementation remain auditable non-final history only.
- Old v1.1 final/tuning execution paths are superseded and must not be restarted.
- DEC-058 and `configs/protocols/protocol-v2.0-final.json` remain immutable historical protocol-v2.0 freeze authority.

## Current science — protocol v2.1

DEC-060 explicitly amends DEC-058 before final-reserve execution. `configs/protocols/protocol-v2.1-final.json` is the self-contained accepted scientific authority.

### RQ1 — nominal learning

Compare independently trained Q-Learning, SARSA, DQN, PPO and Dyna-Q+ under the same semantic environment, agent-visible information contract and principal actual-environment-interaction budget. Primary evidence is standardized Phase-A no-learning probe performance, with final nominal value and learning-trajectory/time-average summaries.

### RQ2 — resilience/adaptation

For each method/root/layout, Phase B starts from that unit's own exact Phase-A scientific checkpoint and matched branch point: FN Frozen nominal, FD Frozen disturbed, AN Adaptive nominal and AD Adaptive disturbed. Primary adaptation benefit is `(FN-FD)-(AN-AD)`. Frozen and Adaptive are deployment regimes, not separate algorithms.

### RQ3 — recovery speed

Primary recovery family is persistent action remapping; supporting disturbance families remain diagnostics. Recovery uses passive 32-interaction reward windows over the unchanged 256-interaction Phase-B horizon, comparing AN with AD after equal layout reduction inside each root. Primary tolerance is `AN - AD <= 0.10`; sensitivity tolerances are `0.05` and `0.20`; stable recovery requires two consecutive in-tolerance windows; non-recovery is right-censored with `recovery_time=null`.

See `docs/research/RQ_EVIDENCE_TRACEABILITY.md` for the RQ → evidence → estimand → output map.

## Fair experimental contract

Fairness does not mean equal hyperparameters or equal optimizer updates.

- same project-owned task/environment semantics and agent-visible information;
- common principal actual environment-interaction learning budget;
- method-appropriate selected hyperparameters and native update mechanics;
- 12 independent final roots and 2 held-out final layouts;
- standardized no-learning Phase-A probes/checkpoint semantics;
- exact matched FN/FD/AN/AD Phase-B branching;
- no final-reserve tuning or outcome-driven root/seed replacement;
- scientific failures remain retained outcomes;
- layouts/episodes/probes/windows are repeated observations, not independent replicates.

Exact continuation state is method-native. DQN replay/target/optimizer/exploration state, PPO optimizer/schedule/RNG/update-boundary state and Dyna-Q+ model/recency/planning state are part of the scientific checkpoint where required.

## Scientific implementation foundation

Current reusable infrastructure includes Python 3.12 + locked `uv`, project-owned Gymnasium GridWorld, strict evaluator-vs-agent information boundaries, deterministic separated RNG streams, project Q-Learning/SARSA/Dyna-Q+, Stable-Baselines3 DQN/PPO scientific-state adapters, actual-interaction Phase-A execution, exact continuation checkpoints, matched Phase-B cloning, passive temporal windows, immutable Study recipes/plans/store/scheduler/service, schema-v2 validation, equal-layout root reduction, recovery/direct contrasts and deterministic evidence exports.

The first final-reserve attempt stopped fail-closed at 216/603 jobs and remains preserved unfinalized and excluded. The DEC-062 replacement completed and finalized 603/603 jobs from one clean corrected commit; T-611 froze only that replacement; T-612 reproduced and interpreted only the predeclared analysis; T-613 finalized the registered thesis/appendix/defense evidence assets from T-612 alone.

## Accepted application architecture

DEC-059 remains the **PySide6 / Qt 6 Widgets framework/runtime authority** over the framework-neutral Study backend. DEC-061 fixes the accepted experiment-first product/UX model. Historical Streamlit/React/NiceGUI implementations are superseded history/reference only.

The accepted application architecture is:

> **Experiment / Run / Results / Evidence**

All five final methods are fixed in the Thesis experiment; Phase A is nominal learning; each exact Phase-A state enters matched Phase B; Frozen means learning off and Adaptive means learning continues; Results answer RQ1/RQ2/RQ3 from stored evidence; Evidence exposes validation/exports/readiness and provenance. Scientific reductions, thresholds, recovery decisions, intervals, RNG, checkpoint identity and finalization never move into Qt state. Technical detail uses progressive disclosure.

Final standalone Windows packaging remains post-thesis/deferred and is not a blocker for WP7.

## T-710 manuscript state

T-710 is COMPLETE and merged through PR #132 as `b8019ece98b9f6a89350b8aa52c205b20225f013`.

The authoritative manuscript package is `docs/thesis/draft/` and contains:

- Greek summary/keywords and English abstract/keywords;
- Chapters 1–7;
- evidence map;
- glossary/acronyms;
- appendix draft;
- citation/T-613 asset/Word handoff register.

The manuscript preserves T-612/T-613 numbers and claim boundaries, uses only citation-ready formal external references after validation, retains right-censoring semantics and introduces no new estimand, threshold, p-value family, ranking or post-hoc analysis.

## Current lifecycle

Canonical concrete state is in `TASKS.md` and `CURRENT_STATUS.md`.

1. Protocol-v2.1 scientific authority, final execution/recovery, T-611 evidence freeze, T-612 statistical analysis and T-613 deterministic thesis/defense assets are complete.
2. The accepted PySide6 experiment-first application is complete through T-534/T-535/T-536 and active-tree cleanup T-537.
3. Explicit pre-WP7 user approval is satisfied.
4. T-700 official-guidance recheck and T-701 example-thesis structure/style review are complete.
5. T-702 major-writing-gate literature freshness review and immutable bibliography consumer re-sync are complete at checkout `ada0d1aec7511098fd12610ae9e5abe7aea875cd`.
6. T-710 evidence-grounded Greek manuscript drafting is complete and merged through PR #132.
7. T-711 review-ready Word composition and T-714 pre-supervisor academic/compliance hardening are complete; T-714 merged through PR #136 as `42afba20fd5a7e9d3912418d0847b42e566aaca0`.
8. T-712 remains input-bound on actual supervisor/reviewer corrections; T-713 final thesis freeze, defense work, final audits and standalone Windows packaging remain downstream.

No green CI, UI screenshot, synthetic smoke, repository cleanup, writing convenience or Word-layout decision authorizes changing frozen scientific evidence or redefining accepted estimands/results. T-711/T-714 composition and hardening used the accepted T-710 manuscript, T-611/T-612/T-613 artifacts and synchronized citation-ready bibliography without scientific reinterpretation; any T-712 correction cycle must preserve the same boundary.