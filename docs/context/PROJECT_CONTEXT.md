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

Current accepted immutable import: **`bibliography-integration-v3`**. New protocol-v2 methodology sources are being refreshed upstream in ThesisBibliography issue #135 and must later enter through a new versioned sync rather than hand edits here.

## Immutable historical science

- `protocol-v1.0`, FINAL-* bundles and frozen v1.0 analysis/evidence are immutable.
- v1.0 is a valid within-Q-learning experiment: Fixed and Continual Q-learning start from the same selected nominal Q checkpoint, isolating the effect of post-change online learning.
- Historical R0 robust-value-iteration pilot evidence remains negative/diagnostic; its severe nominal truncation is not hidden or rewritten.
- Candidate protocol-v1.1 remains auditable non-final research history. It broadened adaptation mechanisms to Fixed Q-Learning, Adaptive Q-Learning, SARSA, Dyna-Q and Dyna-Q+, but all begin evaluation from common selected tabular-Q knowledge. Therefore it is not an end-to-end algorithm-learning benchmark.
- Old `T-522` v1.1 tuning/freeze execution is **SUPERSEDED** and must not run.

## Current science — protocol v2

DEC-048 / issue #95 defines the successor direction.

### RQ-A — nominal learning

Compare independently trained RL methods under the same semantic environment, information, action/reward and principal **environment-interaction/timestep budget**. Separate learning dynamics, standardized nominal policy performance, variability and CPU cost.

### RQ-B — resilience/adaptation

For each method/root/layout, clone the exact trained checkpoint into:

- **Frozen:** no deployment learning-state mutation;
- **Continual:** ordinary method-native continued learning under a predeclared schedule.

Each regime also gets a matched no-change reference. This enables within-method adaptation effects and cross-method resistance/adaptation comparisons without confusing learning with deployment regime.

### Candidate methods

Strong core candidates, still pilot-gated:

1. Q-Learning — tabular off-policy value learning;
2. SARSA — tabular on-policy value learning;
3. DQN — neural off-policy value approximation;
4. PPO — neural on-policy policy-gradient/actor-critic optimization;
5. Dyna-Q+ — learned-model planning + directed recency-based re-exploration.

Secondary candidates:

- Dyna-Q — planning ablation for Dyna-Q+;
- A2C — valid discrete actor-critic candidate, promoted to full final only if it adds distinct scientific value beyond PPO at acceptable cost;
- historical R0 — negative/diagnostic, not automatically redesigned.

No final method count is frozen before pilots.

## Fair experimental contract

Fairness does not mean equal hyperparameters or equal optimizer updates.

- same project-owned environment semantics and agent-visible information;
- common main interaction/timestep learning budget;
- bounded algorithm-specific literature-backed tuning spaces;
- equivalent predeclared tuning opportunity on tuning-only partitions;
- multiple independent roots for every candidate configuration;
- periodic standardized **no-learning evaluation** checkpoints so exploratory/stochastic training returns are not treated as directly comparable policy quality;
- wall-clock/CPU cost reported separately;
- no final-reserve/lifetime tuning;
- seeds are randomization units, never tunable parameters;
- episodes nested within a root are not independent replicates.

Deep `Continual` branches are ordinary continued-training baselines, not claims of specialized continual-learning algorithms. DQN replay/target/optimizer/exploration state and actor-critic optimizer/schedule/RNG/update-boundary state are part of the scientific checkpoint semantics when exact continuation requires them.

## Environment and uncertainty

Do not add pixels, partial observability or a large external benchmark merely to justify deep learning.

Protocol-v2 pilots test a small bounded number of project-owned GridWorld complexity levels and retain the simplest environment family that avoids clear floor/ceiling effects while remaining interpretable and CPU-feasible on the validated Windows thesis machine. Neural agents receive a deterministic numeric/one-hot representation of the same semantic observation, not extra evaluator truth.

Current uncertainty classes remain strong candidates:

- primary persistent dynamics/rule change: action remapping;
- supporting actuation uncertainty: action-execution failure;
- supporting perceptual uncertainty: observation corruption.

Additional dynamic obstacles/reward shifts/gradual drift/recurring changes require a distinct research question before inclusion.

## Metrics/statistics

Historical component resilience estimands remain useful: immediate degradation, cumulative deficit, terminal/post-change performance/gap, explicit recovery/no-recovery. Recovery remains secondary/sensitivity and no composite resilience score is permitted.

Protocol v2 adds learning estimands: standardized final nominal evaluation and learning efficiency over a fixed interaction budget, with curves/checkpoint summaries and independent-root uncertainty. Final root count, layouts, method count and contrast family are selected from non-final variance/precision/runtime evidence before final access rather than copied automatically from v1.1.

Use paired/common-randomness comparisons where construction permits without leaking hidden information. Emphasize effect sizes and 95% intervals. Any formal p-value/multiplicity family must be predeclared.

## Scientific implementation foundation

Validated reusable infrastructure includes:

- Python 3.12 + locked `uv` environment;
- project-owned Gymnasium GridWorld;
- strict evaluator-vs-agent information boundary;
- deterministic separated RNG streams;
- versioned protocols/configuration identity;
- filesystem run bundles/provenance/checksums/events/results;
- tabular Q/SARSA and Dyna implementations;
- paired-statistics components;
- UI-independent runtime service and read-only observer.

Protocol v2 must add a method-agnostic independent training/checkpoint/deployment lifecycle and maintained-library adapters for complex neural algorithms where appropriate. It must not force neural methods into a Q-table abstraction.

## Application status

NiceGUI/runtime work is a functional technical prototype. The user explicitly rejected the current visual/UX design as final. Issue #93 tracks a radical redesign but is **PAUSED until protocol-v2 science stabilizes** so the interface is not redesigned twice.

Earlier screenshots/PyInstaller work is prototype/feasibility evidence only. Final Windows standalone packaging is deferred until after final thesis freeze through issue #94 / `T-803`.

## Current lifecycle

Canonical concrete state is in `TASKS.md`.

1. `T-524` — protocol-v2 source/RQ/estimand/method-role freeze (**current**).
2. `T-525` — common multimethod training/checkpoint implementation.
3. `T-526` — bounded environment/method Windows CPU feasibility pilots.
4. `T-527` — fair tuning, precision/runtime sizing, statistics and protocol-v2 freeze.
5. `T-528` — v2-aware radical UI redesign.
6. `T-511` — explicit intended-user acceptance.
7. `T-610..T-613` — frozen v2 final execution, validation, analysis and evidence package.
8. Explicit user approval before any WP7 writing.
9. T-700+ thesis/review/defense workflow.
10. `T-803` post-thesis standalone Windows package.

No green CI, pilot, screenshot, packaged app or completed final analysis alone authorizes WP7.

## Current authority

Use:

- `AGENTS.md` — always-on project/Codex policy;
- `docs/context/TASKS.md` — concrete task/resume state;
- `docs/context/CURRENT_STATUS.md` — compact status;
- `docs/context/CODEX_EXECUTION_PROMPT.md` — Codex bootstrap;
- `docs/decisions/DEC-048_PROTOCOL_V2_INDEPENDENT_LEARNING_AND_MATCHED_RESILIENCE.md` — current scientific direction;
- `docs/research/PROTOCOL_V2_RESEARCH_DESIGN.md` — current methodology contract;
- `docs/research/MODEL_CANDIDATES.md` — current method-role policy;
- `docs/thesis/THESIS_REQUIREMENTS.md` — thesis evidence/format requirements;
- `docs/thesis/PRESENTATION_WORKFLOW.md` — future defense workflow.

Earlier decisions/documents remain auditable historical context where explicitly superseded.
