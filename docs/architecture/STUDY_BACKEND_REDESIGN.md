# Study-First Backend Audit and Reconstruction Plan

**Date:** 2026-08-28  
**Status:** active architecture specification under DEC-051  
**Scope:** practical thesis workflow from agent execution through evidence, analysis, export and presentation handoff; no frontend implementation

## 1. Audit question

Does the current implementation execute the practical thesis as one coherent, sequential, reproducible research workflow, or does the user/application still need to reconstruct research intent from individual experiments and historical APIs?

### Verdict

The scientific protocol-v2 foundation is strong enough to retain. The surrounding backend is not yet the final architecture.

The repository currently contains:

- a validated protocol-v2 scientific execution layer;
- a robust but run-level evidence/provenance layer;
- a historical v1.x experiment/runtime/analysis/application layer;
- a later thesis/presentation workflow specification;
- no single aggregate that connects all of these as one automated thesis study.

Therefore the final backend must be reconstructed around a `Study`/research-program lifecycle before the final frontend is built.

## 2. End-to-end thesis workflow that the backend must represent

The practical research has one conceptual sequence:

```text
methodology + bibliography
        |
        v
T-526 feasibility / environment / severity development evidence
        |
        v
T-527 fair tuning + precision/runtime sizing + protocol freeze
        |
        v
final application acceptance gate
        |
        v
frozen thesis-study recipe
        |
        +--> Phase A: independent nominal learning
        |       |
        |       +--> isolated no-learning probes
        |       +--> exact scientific checkpoints
        |
        +--> Phase B: matched resilience/adaptation
                |
                +--> FN / FD / AN / AD per condition
        |
        v
evidence completeness + integrity freeze
        |
        v
predeclared root-level statistical analysis
        |
        v
thesis evidence package
        |
        +--> tables / figures / machine-readable data
        +--> claim/result/evidence identifiers
        +--> application screenshot/demo capture instructions
        +--> presentation evidence/asset map
        |
        v
WP7 thesis + defense workflow after explicit user approval
```

The user should never need to infer which individual runs, roots, branches, settings or comparisons are required to complete this chain.

## 3. Audit by subsystem

### 3.1 Scientific agents and GridWorld — KEEP

Retain:

- project-owned GridWorld and explicit information boundary;
- deterministic/scoped RNG structure;
- Q-Learning, SARSA, Dyna-Q+ project implementations;
- Stable-Baselines3 DQN/PPO scientific adapters;
- exact checkpoint/restore/continuation conformance;
- actual-environment-interaction accounting;
- isolated no-learning probes;
- exact four-branch Phase-B executor and Frozen-state protections.

Reason: these are protocol-v2 scientific invariants already covered by focused conformance testing. Rewriting them for architectural neatness would increase scientific risk without improving the thesis question.

### 3.2 Flat `protocol_v2_*` module family — KEEP SCIENCE, HIDE BEHIND PORTS

The current files correctly preserve method-native behavior but expose implementation detail directly. They should become internal scientific execution adapters behind new study execution ports.

Do not make a future UI know which file/class implements DQN, PPO, tabular Phase A or tabular Phase B.

### 3.3 `RunBundle` — KEEP AS LOWER-LEVEL EVIDENCE PRIMITIVE

Strengths already worth preserving:

- source Git provenance;
- machine snapshot;
- atomic metadata writes;
- immutable finalization marker;
- checksums;
- strict resume identity;
- filesystem evidence as authority.

Missing final capability: it represents one run, not the complete thesis study. It needs a parent study bundle rather than being expanded into a monolithic campaign object.

### 3.4 `ExperimentRegistry` / `experiment_manager.py` — LEGACY COMPATIBILITY

Useful for historical finalized-run discovery and integrity validation, but the main abstraction is a flat list of runs. Final application history should be study-first and drill down to jobs/runs.

Do not add new protocol-v2 product concepts to this registry.

### 3.5 `RuntimeService` — REPLACE FOR FINAL APPLICATION

Current service is explicitly tied to the protocol-v1.1 candidate runner and one-run subprocess lifecycle. It is not a protocol-v2 study orchestrator.

Final replacement requirements:

- queue/schedule study jobs, not arbitrary commands;
- understand study stage/dependency barriers;
- use immutable recipe-derived jobs;
- preserve exact scientific identity on infrastructure retry;
- support scientific failure as retained evidence;
- expose truthful aggregate study progress and per-job state;
- emit framework-neutral events/telemetry;
- resume from durable study state after application restart;
- never derive scientific state from UI session memory.

### 3.6 NiceGUI `ApplicationReadModel` / `src/app` — PROTOTYPE ONLY

The current application read model is hard-coded to v1.1 protocol objects and historical F0/C0/S0/DQ0/D0 profiles. This confirms that the final frontend cannot be obtained by restyling the current UI.

The entire final application-facing contract must come from the new `StudyService` facade. T-528 will consume it from another frontend framework.

### 3.7 Historical `analysis.py` — KEEP HISTORICAL, REBUILD V2 ANALYSIS

The current analysis implementation validates and derives records for the historical headless/Q-checkpoint experiment schema. It must remain reproducible for historical evidence, but it cannot become the final protocol-v2 analysis by adding conditionals.

Create a separate v2 analysis layer whose inputs are frozen study/evidence records and whose outputs implement:

- Phase-A standardized final evaluation and equal-grid learning AUC/time-average;
- root-level distributions and failure denominators;
- Phase-B FN/FD/AN/AD component losses;
- matched four-branch adaptation-benefit/DiD estimands;
- selected predeclared cross-method contrasts;
- Student-t root-level intervals plus frozen sensitivity analysis;
- no composite resilience score;
- explicit condition-family separation.

### 3.8 Export pipeline — REBUILD AS DETERMINISTIC STUDY EXPORT

The final export should not be a collection of whatever charts happened to be visible in the UI.

It must be produced from frozen analysis/evidence by an export recipe and create stable IDs for:

- primary thesis figures;
- primary thesis tables;
- supplementary/sensitivity figures/tables;
- root-level machine-readable data;
- configuration/method/environment tables;
- runtime/failure table;
- evidence/provenance manifest;
- claim/result/evidence crosswalk;
- presentation-safe copies of selected evidence assets.

### 3.9 Thesis and presentation workflow — KEEP PROCESS, RECONCILE V2 TERMINOLOGY

The Word/PowerPoint/asset workflow is structurally sound: final documents derive from frozen repository evidence, quantitative plots are generated rather than retyped, and application media illustrates rather than replaces scientific evidence.

However, active planning text still contains historical v1.1/F0/C0/D0 assumptions. Before WP7 those documents must consume the final protocol-v2 evidence package and final method terminology.

The backend's responsibility ends at a complete evidence/handoff package. It does not own Greek thesis prose or PowerPoint layout.

### 3.10 Decision/status documentation — RECONCILE

`DECISION_LOG.md` and parts of `EXECUTION_WORKFLOW.md` still describe NiceGUI/v1.1 as current architecture even though DEC-048/049/050 and current task state supersede those assumptions.

This is a documentation-governance defect, not a scientific defect. DEC-051 and the task ledger must become the controlling reconstruction path.

## 4. Target backend architecture

```text
resilient_agents/
  [validated scientific core remains]

  study/
    model.py          # evidence classes, stages, jobs, artifacts
    recipe.py         # immutable content-addressed study recipe
    lifecycle.py      # sequential barriers and failure semantics
    store.py          # durable parent study bundle + lineage
    planner.py        # recipe -> materialized deterministic job plan
    ports.py          # execution/validation/analysis/export protocols
    scheduler.py      # local bounded CPU scheduler/resume/retry
    service.py        # framework-neutral application facade

  evidence_v2/
    validation.py
    records.py
    statistics.py
    exports.py

  legacy/
    [logical compatibility boundary; physical moves only when safe]
```

Physical file moves of old modules are optional and occur only if they reduce ambiguity without breaking historical reproducibility. Namespacing/deprecation can be achieved before any destructive move.

## 5. New study bundle contract

Parent bundle:

```text
results/studies/<study-id>/
  manifest.json
  recipe.json
  plan.json
  lifecycle.json
  events.jsonl
  artifacts.jsonl
  FINALIZED
```

Individual raw scientific jobs remain under validated run/evidence locations and are referenced by content hash/lineage. The parent study does not duplicate large checkpoint/replay artifacts unnecessarily.

Required parent properties:

- immutable recipe hash;
- immutable materialized plan hash;
- source Git provenance;
- exact job attempts/state;
- scientific vs infrastructure failure distinction;
- artifact lineage graph;
- finalization only after every study stage is scientifically resolved;
- integrity validation on reload;
- no finalized mutation.

## 6. Job model

Every automatically materialized job has a stable ID and explicit payload identity.

Representative final Phase-A ID:

`pa__ppo__root-r017__layout-f02`

Representative Phase-B IDs:

`pb__ppo__root-r017__layout-f02__remap-swap-right-down__fn`

`pb__ppo__root-r017__layout-f02__remap-swap-right-down__fd`

`pb__ppo__root-r017__layout-f02__remap-swap-right-down__an`

`pb__ppo__root-r017__layout-f02__remap-swap-right-down__ad`

The exact stable-ID grammar is frozen in the planner implementation before final recipe execution.

## 7. Evidence-class firewall

Every study, job and artifact is one of:

- development;
- tuning;
- confirmatory;
- derived;
- exploratory;
- historical.

Rules:

- confirmatory recipe must be frozen;
- development/tuning output cannot be silently promoted to confirmatory;
- exploratory custom-app runs are permanently distinguishable from thesis evidence;
- historical v1.x evidence remains queryable but cannot enter v2 confirmatory aggregate estimates;
- derived figures/tables inherit lineage to confirmatory inputs and cannot exist without them.

## 8. Automation boundary

### Backend decides automatically

For a frozen thesis recipe:

- all required methods;
- roots;
- layouts;
- conditions;
- FN/FD/AN/AD branches;
- job ordering/dependencies;
- checkpoint origins;
- validation steps;
- analysis contrasts;
- required figures/tables/exports.

### User does not configure in thesis-valid mode

- gamma/reward semantics;
- final method hyperparameters;
- final seeds/roots;
- final severities;
- probe cadence;
- branch combinations;
- checkpoint IDs;
- statistical tests/contrast family.

### User-facing intent later

Default final application path:

`Run Thesis Study -> Monitor -> Validate -> Results -> Export`

A separate custom/exploratory workflow may expose advanced settings without affecting the frozen thesis study.

## 9. Sequential implementation plan

### R1 — Domain / study envelope — IN PROGRESS

- study domain enums/dataclasses;
- immutable recipe/hash;
- stage barriers and failure semantics;
- study bundle persistence;
- artifact lineage;
- focused tests.

### R2 — Plan materializer

- generic deterministic matrix axes;
- development recipe materialization;
- protocol-v2 confirmatory recipe materialization after T-527 values exist;
- stable job IDs and checkpoint dependencies;
- plan-size/runtime preview DTO.

### R3 — Execution ports/scheduler

- adapters over existing Phase-A/Phase-B drivers;
- bounded CPU-local scheduler;
- subprocess isolation only where useful;
- resume/retry/cancel semantics;
- aggregate telemetry.

### R4 — v2 evidence validation

- study completeness;
- run/checkpoint/hash provenance;
- exact expected/observed matrix reconciliation;
- scientific failure accounting;
- branch/checkpoint lineage validation;
- frozen evidence marker.

### R5 — v2 statistics

- Phase-A learning records;
- Phase-B matched branch records;
- root/layout aggregation;
- frozen confidence/sensitivity calculations;
- deterministic analysis package.

### R6 — deterministic thesis/presentation export

- figures/tables/data;
- evidence IDs;
- claim/result map;
- presentation asset map;
- export integrity manifest.

### R7 — application facade

- `StudyService` create/plan/start/resume/status/events/results/export API;
- no v1.1 DTOs in the final facade;
- legacy runs available through explicit history adapter only.

### R8 — T-528 frontend

Only after T-527 and the application facade are stable, select the replacement frontend framework and build the UI from scratch.

## 10. External-gate compatibility

T-526 remains a real external-machine evidence gate. R1-R3 may be developed without fabricating that evidence, but the existing physical pilot entrypoint must remain usable until its retained output is accepted.

T-527 remains the authority for values that the final recipe cannot know yet. The architecture can be completed before those numbers exist; the confirmatory recipe cannot.

## 11. Definition of backend redesign complete

The backend reconstruction is complete only when:

1. a study recipe can be loaded and hash-validated;
2. its complete job matrix materializes deterministically;
3. the backend can execute/resume it without UI-specific logic;
4. scientific and infrastructure failures are preserved correctly;
5. each Phase-B unit traces to its exact Phase-A checkpoint;
6. validation can reconcile planned and produced evidence;
7. v2 analysis regenerates all frozen estimates from evidence;
8. export regenerates thesis-ready figures/tables/data and presentation lineage;
9. the application-facing service exposes study-level, framework-neutral DTO/events;
10. historical v1.x evidence remains reproducible but cannot contaminate v2;
11. no final scientific parameter is supplied by frontend defaults;
12. repository tests and physical-machine gates required by the protocol pass.
