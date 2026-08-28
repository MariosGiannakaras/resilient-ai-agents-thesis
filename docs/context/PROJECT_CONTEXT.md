# Project Context

## Status taxonomy

- **CONFIRMED:** established by approved application, explicit user direction, accepted decision or validated evidence.
- **RESEARCH_REQUIRED:** needs evidence before selection.
- **CANDIDATE:** defined but not yet frozen for final evidence.
- **SUPERSEDED:** preserved history that no longer controls future execution.
- **DEFERRED:** intentionally later and non-blocking now.

## Project identity

Official thesis titles:

- Greek: **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**
- English: **Comparison and Evaluation of Resilient AI Agents in Uncertain Environments**

GridWorld is the controlled experimental testbed and visualization environment, not the thesis subject. Final thesis language is Greek and the final academic document is Microsoft Word unless later official guidance changes this.

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` owns discovery, originals, conversion/OCR, scientific analysis, evidence verification and citation-ready corpus generation. This repo consumes versioned generated output read-only.

The current protocol-v2 consumer state is pinned to immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources and 19 research materials. The generated sync was merged through thesis PR #96. `bibliography-integration-v3` remains immutable historical baseline terminology; no generated bibliography content is hand-edited here.

## Immutable historical science

- `protocol-v1.0`, FINAL-* bundles and frozen v1.0 analysis/evidence are immutable.
- v1.0 is a valid within-Q-learning experiment: Fixed and Continual Q-learning start from the same selected nominal Q checkpoint, isolating the effect of post-change online learning.
- Historical R0 robust-value-iteration pilot evidence remains negative/diagnostic; its severe nominal truncation is not hidden or rewritten.
- Candidate protocol-v1.1 remains auditable non-final research history. Its common selected tabular-Q starting knowledge makes it unsuitable as an end-to-end independent algorithm-learning benchmark.
- Old `T-522` v1.1 tuning/freeze execution is **SUPERSEDED** and must not run.

## Current science — protocol v2

DEC-048, refined by DEC-050, defines the successor methodology.

### RQ-A — nominal learning

Compare independently trained retained RL methods under the same semantic environment, information, action/reward contract and principal **actual environment-interaction budget**. Separate learning dynamics, standardized no-learning nominal policy performance, variability and CPU/runtime cost.

### RQ-B — resilience/adaptation

For each method/root/layout, begin from that unit's own exact Phase-A trained scientific state. After any shared nominal no-learning prefix, fork the exact branch point into:

- **FN — Frozen nominal**;
- **FD — Frozen disturbed**;
- **AN — Adaptive nominal**;
- **AD — Adaptive disturbed**.

Adaptive learning begins only on the first post-boundary transition. The primary within-method adaptation benefit is the matched disturbed-vs-nominal interaction, not an unmatched AD-vs-FD comparison.

### Candidate methods

Strong core candidates, still pilot-gated:

1. Q-Learning — tabular off-policy value learning;
2. SARSA — tabular on-policy value learning;
3. DQN — neural off-policy value approximation;
4. PPO — neural on-policy actor-critic/policy-gradient optimization;
5. Dyna-Q+ — learned-model planning plus directed recency-based re-exploration.

Secondary roles:

- Dyna-Q — targeted planning ablation for Dyna-Q+;
- A2C — promotion-only actor-critic candidate if non-final evidence shows distinct scientific value beyond PPO at acceptable matrix/runtime cost;
- Random — non-ranked calibration/reference policy;
- historical R0 — negative/diagnostic only.

No final retained method count is frozen before T-526/T-527.

## Fair experimental contract

Fairness does not mean equal hyperparameters or equal optimizer updates.

- same project-owned task/environment semantics and agent-visible information;
- common principal actual interaction/timestep learning budget;
- bounded algorithm-specific tuning spaces with equivalent predeclared tuning opportunity;
- multiple independent roots for every retained configuration;
- periodic standardized **no-learning evaluation** checkpoints;
- wall-clock/CPU cost reported separately;
- no final-reserve tuning or outcome-driven final parameter changes;
- seeds are randomization units, never tunable parameters;
- episodes nested within a root are not independent replicates;
- scientific failures remain retained outcomes and are never replaced by favorable seeds.

Exact continuation state is method-native. DQN replay/target/optimizer/exploration state, PPO optimizer/schedule/RNG/update-boundary state and Dyna-Q+ model/recency/planning state are part of the scientific checkpoint where required.

## Environment and uncertainty

Do not add pixels, partial observability or a large external benchmark merely to justify deep learning.

Protocol-v2 pilots use a bounded project-owned GridWorld complexity ladder and retain the simplest task family that avoids clear floor/ceiling effects while remaining interpretable and CPU-feasible on the validated Windows thesis machine. Neural methods receive a deterministic numeric representation of the same semantic observation, never extra evaluator truth.

Current uncertainty candidates:

- primary persistent dynamics/rule change: action remapping;
- supporting actuation uncertainty: action-execution failure;
- supporting perceptual uncertainty: observation corruption with explicit frequency and support/magnitude.

Additional dynamic obstacles/reward shifts/drift/recurrence require an explicit later research decision before inclusion.

## Metrics/statistics

Historical component resilience measures remain useful as background, but protocol-v2 analysis is organized around independently trained Phase-A learning and matched four-branch Phase-B effects.

Current implemented analysis foundation supports:

- standardized Phase-A final probe values and equal-grid trapezoidal time-average/AUC-style learning summaries;
- root/layout blocked aggregation;
- Phase-B Frozen loss, Adaptive loss and matched adaptation benefit from FN/FD/AN/AD;
- explicit planned/completed/scientific-failure/skipped/infrastructure denominators;
- recipe-selected metric direction and complete-layout policy;
- explicit optional Student-t mean interval primitive when the critical value is frozen by the analysis recipe.

Final root count, interval/sensitivity/multiplicity recipe, contrast family and figure selection remain T-527/T-612/T-613 decisions. No composite resilience score is permitted.

## Scientific and study-first implementation foundation

Validated/current reusable infrastructure now includes:

- Python 3.12 + locked `uv` environment;
- project-owned Gymnasium GridWorld and strict evaluator-vs-agent information boundary;
- deterministic separated RNG streams;
- Q-Learning, SARSA and Dyna-Q+ project implementations;
- Stable-Baselines3 2.9.0 DQN/PPO exact scientific-state adapters on CPU-only PyTorch 2.9.0;
- actual-interaction Phase-A drivers and isolated no-learning probes;
- exact scientific checkpoint/restore/continuation and branch clone conformance;
- exact shared no-learning Phase-B prefix primitive;
- atomic matched FN/FD/AN/AD Phase-B execution;
- filesystem run bundles/provenance/checksums;
- immutable `StudyRecipe`, deterministic Study job plan, durable `StudyStore`, stage barriers and restart-safe scheduler;
- framework-neutral `StudyService` with concrete default protocol-v2 executors;
- v2 evidence validation, root-level analysis package and deterministic data/table/result-ID evidence handoff.

The currently validated Phase-B lifecycle is one exact post-boundary environment segment. Prefix or branch execution fails closed if a reset would be required. T-526/T-527, not application code, decide any multi-episode lifecycle amendment.

## Application status

DEC-051 makes the study-first backend the final application-facing architecture. The active NiceGUI runtime/application/packaging surface has been removed; Git history retains it as prototype evidence. The final frontend is **not selected or implemented yet**.

T-528 will choose a framework different from NiceGUI and build the UI from scratch only after T-527 freezes the remaining scientific/runtime contract and T-529 completes the framework-neutral backend. Historical screenshot/PyInstaller work is prototype context only. Final Windows standalone packaging remains post-thesis T-803.

## Current lifecycle

Canonical concrete state is in `TASKS.md`.

1. `T-524` — protocol-v2 scientific contract — **COMPLETE**.
2. `T-525` — framework-neutral multimethod scientific execution foundation — **COMPLETE**.
3. `T-529` — study-first recipe/orchestration/evidence/analysis/export backend reconstruction — **IN_PROGRESS** and allowed to proceed without inventing unresolved T-526/T-527 values.
4. `T-526` — bounded physical Windows environment/method/severity feasibility gate — **READY**, external.
5. `T-527` — fair tuning, precision/runtime sizing, statistics and machine-readable protocol-v2 freeze — **BLOCKED on T-526**.
6. `T-528` — new-framework final UI rebuild — **BLOCKED on T-527 + T-529**.
7. `T-511` — explicit intended-user acceptance.
8. `T-610..T-613` — frozen v2 final execution, validation, analysis and evidence package.
9. Explicit user approval before any WP7 writing.
10. T-700+ thesis/review/defense workflow.
11. `T-803` post-thesis standalone Windows package.

No green CI, pilot, screenshot, packaged app or completed analysis alone authorizes WP7.

## Current authority

Use:

- `AGENTS.md` — always-on project/Codex policy;
- `docs/context/TASKS.md` — concrete task/resume state;
- `docs/context/CURRENT_STATUS.md` — compact status;
- `docs/context/CODEX_EXECUTION_PROMPT.md` — Codex bootstrap;
- `docs/decisions/DEC-048_PROTOCOL_V2_INDEPENDENT_LEARNING_AND_MATCHED_RESILIENCE.md` — protocol-v2 scientific design;
- `docs/decisions/DEC-050_PROTOCOL_V2_CLOSURE_REFINEMENTS.md` — methodology closure/refinements;
- `docs/decisions/DEC-051_STUDY_FIRST_BACKEND_RECONSTRUCTION.md` — current backend/application architecture;
- `docs/architecture/STUDY_BACKEND_REDESIGN.md` — reconstruction implementation contract;
- `docs/thesis/THESIS_REQUIREMENTS.md` — thesis evidence/format requirements;
- `docs/thesis/PRESENTATION_WORKFLOW.md` — future defense workflow.

Earlier decisions/documents remain auditable historical context where explicitly superseded.
