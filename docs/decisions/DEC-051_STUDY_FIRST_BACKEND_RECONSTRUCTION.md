# DEC-051 — Study-First Backend Reconstruction

**Date:** 2026-08-28  
**Status:** Accepted by explicit user direction; implementation in progress  
**Scope:** backend/domain/orchestration/evidence/analysis/export architecture only; frontend remains deferred to T-528

## Context

Protocol-v2 now has a validated framework-neutral scientific execution foundation for Q-Learning, SARSA, DQN, PPO and Dyna-Q+, including exact scientific continuation, interaction accounting, isolated no-learning probes and matched Frozen/Adaptive branch semantics.

However, the repository still contains two generations of application/backend architecture:

- historical run-centric `experiment_manager`, `experiment_runner`, `analysis`, `runtime_service` and NiceGUI application models built around protocol-v1.x;
- protocol-v2 scientific adapters/executors built correctly beside the legacy path but not yet unified into one end-to-end study service.

The final thesis workflow is no longer "choose one agent/config -> run one experiment". It is one controlled research program whose final confirmatory recipe automatically materializes all required method/root/layout/condition/branch units, validates them, analyzes the frozen evidence and exports thesis/presentation-ready artifacts.

## Decision

### 1. The primary backend aggregate becomes `Study`, not `Run`

A run remains a lower-level scientific execution/evidence unit. A `Study` is the authoritative parent lifecycle that owns:

`immutable recipe -> materialized plan -> jobs -> scientific run/checkpoint lineage -> validation -> analysis -> thesis/presentation exports`.

The UI will later operate on studies and study jobs. It will not construct protocol internals manually.

### 2. Preserve validated scientific code; reconstruct orchestration around it

Keep and reuse the validated protocol-v2 scientific assets:

- project GridWorld and information/RNG boundaries;
- Q-Learning/SARSA/Dyna-Q+ implementations and exact state adapters;
- Stable-Baselines3 DQN/PPO scientific-state adapters;
- protocol-v2 Phase-A/Phase-B executors and conformance invariants;
- existing run-bundle provenance/checksum/finalization primitives where they remain valid.

Do not rewrite algorithms merely to fit a new service API. The new orchestration layer adapts to method-native execution.

### 3. Freeze legacy application/runtime APIs as compatibility/history

The existing v1.x `ExperimentRegistry`, `RuntimeService`, legacy analysis path and NiceGUI `ApplicationReadModel` may remain temporarily for historical evidence/prototype compatibility, but they are not the final application-facing architecture.

No new protocol-v2 product behavior should be added by extending v1.1-specific DTOs, F0/C0/D0 forms or the old single-run launcher.

### 4. New backend layers

The final backend is organized conceptually as:

1. **Scientific Core** — agents, GridWorld, method-native protocol-v2 adapters/executors.
2. **Study Domain** — recipes, evidence classes, stages, jobs, dependencies, failures and artifact lineage.
3. **Study Orchestration** — plan materialization, sequential stage barriers, bounded local scheduling, resume/retry rules and external gates.
4. **Evidence Store** — study-level manifests and lineage above immutable individual run bundles.
5. **Analysis / Export** — protocol-v2 validation, root-level analysis and deterministic thesis/defense artifact production from frozen evidence.
6. **Application API** — framework-neutral read/control DTOs/events. The later frontend is a client only.

### 5. Recipe-first thesis-valid operation

After T-527 freezes protocol-v2.0, the thesis-valid application path loads one immutable machine-readable study recipe. It automatically owns:

- retained methods/configurations;
- final layouts and root identities;
- Phase-A budgets/probe grid;
- Phase-B condition matrix and FN/FD/AN/AD materialization;
- checkpoint origins and branch lineage;
- validation requirements;
- analysis contrasts/statistics;
- required tables/figures/exports.

Manual configuration is a separate exploratory/custom mode and can never silently become confirmatory thesis evidence.

### 6. Stage sequencing and failure semantics

A later stage cannot start until the earlier stage is scientifically resolved.

Scientific failures are retained outcomes and are never replaced with favorable seeds. A downstream unit that requires an unavailable checkpoint is explicitly skipped with lineage to the upstream scientific failure. Infrastructure failures are distinct and may be retried only under the same scientific identity/provenance policy.

### 7. Evidence lineage reaches thesis and defense assets

Every generated artifact receives a stable role and lineage to source jobs/artifacts. The chain must support:

`run/checkpoint -> validation record -> root-level analysis row -> table/figure -> thesis evidence package -> presentation asset/evidence map`.

Quantitative thesis or slide assets are generated from frozen evidence, never manually retyped by the UI or presentation tooling.

### 8. Filesystem evidence remains authoritative

Continue the repository rule that filesystem evidence is the source of truth. Any future index/database is rebuildable. Study-level state uses atomic files, content hashes, append-only events/lineage and a finalization boundary so partial work cannot masquerade as complete evidence.

### 9. Physical-machine and protocol gates remain intact

This reconstruction does not bypass T-526 or T-527 and does not authorize final reserve access. The already-predeclared physical T-526 Windows pilot remains executable and its evidence must not be invalidated by unrelated orchestration refactoring.

The final recipe values remain intentionally unresolved until T-526/T-527 evidence freezes them.

### 10. Frontend remains deferred

No new frontend implementation is part of this decision. T-528 begins only after the new application API and T-527 scientific contract are stable. DEC-049 continues to require a different final framework from NiceGUI.

## Migration strategy

### Slice A — domain and durable study envelope

- immutable recipe envelope/hash;
- ordered study stages and job DAG;
- explicit scientific/infrastructure failure semantics;
- study-level filesystem bundle and artifact lineage;
- focused lifecycle/lineage tests.

### Slice B — protocol-v2 plan materialization

- materialize development and frozen confirmatory matrices from machine-readable recipe axes;
- stable IDs for method/root/layout/condition/branch jobs;
- explicit Phase-A checkpoint -> Phase-B branch dependencies;
- Random/oracle/reference units remain non-ranked supporting jobs.

### Slice C — execution ports and scheduler

- method-native execution ports over existing protocol-v2 drivers;
- local CPU scheduler with deterministic stage barriers and bounded concurrency;
- restart/resume/infrastructure retry semantics;
- truthful event/telemetry stream.

### Slice D — validation and analysis

- v2 evidence completeness/integrity validator;
- root-level Phase-A learning and Phase-B matched-DiD datasets;
- frozen statistical recipe execution;
- explicit failure denominators and sensitivity outputs.

### Slice E — export/handoff

- deterministic thesis tables/figures/data manifests;
- claim/result/figure/table IDs;
- presentation evidence/asset manifest;
- UI-neutral export APIs.

### Slice F — legacy quarantine/application facade

- final `StudyService` read/control API;
- old v1.x application/runtime path clearly namespaced/deprecated as history;
- T-528 consumes only the new facade.

## Supersession boundary

This decision supersedes the final-architecture assumption that the existing v1.x run-centric runtime service and NiceGUI-era application read model should be incrementally extended for protocol-v2.

It does **not** supersede historical evidence, the validated scientific execution invariants, run-bundle provenance principles, DEC-048/050 methodology or DEC-049 frontend reselection.
