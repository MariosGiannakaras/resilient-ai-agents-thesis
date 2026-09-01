# DEC-051 — Study-First Backend Reconstruction

**Date:** 2026-08-28  
**Status:** Accepted by explicit user direction; T-529 backend reconstruction implemented and closed  
**Scope:** backend/domain/orchestration/evidence/analysis/export architecture only; frontend remains deferred to T-528

## Context

Protocol-v2 now has a validated framework-neutral scientific execution foundation for Q-Learning, SARSA, DQN, PPO and Dyna-Q+, including exact scientific continuation, interaction accounting, isolated no-learning probes and matched Frozen/Adaptive branch semantics.

At the time of this decision, the repository still contained two generations of application/backend architecture:

- historical run-centric `experiment_manager`, `experiment_runner`, `analysis`, `runtime_service` and NiceGUI application models built around protocol-v1.x;
- protocol-v2 scientific adapters/executors built correctly beside the legacy path but not yet unified into one end-to-end study service.

T-529 subsequently removed the superseded active NiceGUI/runtime application path and completed the study-first service described below while preserving historical scientific reproducibility in Git/history.

The final thesis workflow is no longer "choose one agent/config -> run one experiment". It is one controlled research program whose final confirmatory recipe automatically materializes all required method/root/layout/condition/branch units, validates them, analyzes the frozen evidence and exports deterministic evidence for later thesis/presentation tooling.

## Decision

### 1. The primary backend aggregate becomes `Study`, not `Run`

A run remains a lower-level scientific execution/evidence unit. A `Study` is the authoritative parent lifecycle that owns:

`immutable recipe -> materialized plan -> jobs -> scientific run/checkpoint lineage -> validation -> analysis -> deterministic evidence export`.

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

The v1.x `ExperimentRegistry`, `RuntimeService`, legacy analysis path and NiceGUI `ApplicationReadModel` are historical/prototype architecture, not the final application-facing architecture. T-529 removed their superseded active application/runtime surface while retaining Git history and historical scientific evidence/runners where required for reproducibility.

No new protocol-v2 product behavior is added by extending v1.1-specific DTOs, F0/C0/D0 forms or the old single-run launcher.

### 4. New backend layers

The final backend is organized conceptually as:

1. **Scientific Core** — agents, GridWorld, method-native protocol-v2 adapters/executors.
2. **Study Domain** — recipes, evidence classes, stages, jobs, dependencies, failures and artifact lineage.
3. **Study Orchestration** — plan materialization, sequential stage barriers, bounded local scheduling, resume/retry rules and external gates.
4. **Evidence Store** — study-level manifests and lineage above immutable individual run bundles.
5. **Analysis / Export** — protocol-v2 validation, root-level analysis and deterministic machine-readable evidence handoff from validated evidence.
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
- required downstream result/export identities.

Manual configuration is a separate exploratory/custom mode and can never silently become confirmatory thesis evidence.

### 6. Stage sequencing and failure semantics

A later stage cannot start until the earlier stage is scientifically resolved.

Scientific failures are retained outcomes and are never replaced with favorable seeds. A downstream unit that requires an unavailable checkpoint is explicitly skipped with lineage to the upstream scientific failure. Infrastructure failures are distinct and may be retried only under the same scientific identity/provenance policy.

### 7. Evidence lineage reaches later thesis and defense assets

Every generated artifact receives a stable role and lineage to source jobs/artifacts. T-529 establishes the machine-readable chain through validated analysis/result identities. Later T-613/WP7 tooling may extend that lineage into final tables/figures/thesis/defense assets:

`run/checkpoint -> validation record -> root-level analysis/result row -> deterministic evidence handoff -> later table/figure -> thesis evidence package -> presentation asset/evidence map`.

Quantitative thesis or slide assets must derive from frozen evidence, never be manually retyped by the UI or presentation tooling. T-529 itself does not generate thesis prose, final thesis figures or PPTX.

### 8. Filesystem evidence remains authoritative

Continue the repository rule that filesystem evidence is the source of truth. Any future index/database is rebuildable. Study-level state uses atomic files, content hashes, append-only events/lineage and a finalization boundary so partial work cannot masquerade as complete evidence.

### 9. Physical-machine and protocol gates remain intact

This reconstruction does not bypass T-526 or T-527 and does not authorize final reserve access. The already-predeclared physical T-526 Windows pilot remains executable and its evidence must not be invalidated by unrelated orchestration refactoring.

The final recipe values remain intentionally unresolved until T-526/T-527 evidence freezes them.

### 10. Frontend remains deferred

No new frontend implementation is part of this decision. T-528 begins only after T-527 freezes the remaining scientific/runtime contract. T-529's application API/backend dependency is complete. DEC-049 continues to require a different final framework from NiceGUI.

## Implemented migration slices

### Slice A — domain and durable study envelope

- immutable recipe envelope/hash;
- ordered study stages and job DAG;
- explicit scientific/infrastructure failure semantics;
- study-level filesystem bundle and artifact lineage;
- focused lifecycle/lineage tests.

### Slice B — protocol-v2 plan materialization

- materialize development and frozen-confirmatory matrices from machine-readable recipe axes;
- stable IDs for method/root/layout/condition/branch jobs;
- explicit Phase-A checkpoint -> Phase-B dependencies;
- Random/reference units remain non-ranked supporting jobs and unknown identities fail closed.

### Slice C — execution ports and scheduler

- method-native execution ports over existing protocol-v2 drivers;
- deterministic stage barriers and restart-safe local execution;
- resume/infrastructure retry semantics;
- concrete default protocol-v2 executor registry behind `StudyService`.

### Slice D — validation and analysis

- v2 evidence completeness/integrity validator;
- root/layout Phase-A learning and Phase-B matched-DiD datasets;
- explicit recipe-driven statistical inputs;
- explicit planned/observed/scientific-failure/skipped/infrastructure denominators.

### Slice E — export/handoff

- deterministic machine-readable CSV/JSON root/summary/result tables;
- stable evidence/result IDs and result index;
- integrity/provenance manifests and source-artifact lineage;
- UI-neutral export APIs for later T-613/WP7 asset generation.

### Slice F — legacy quarantine/application facade

- final framework-neutral `StudyService` read/control API;
- old v1.x/NiceGUI application/runtime path removed from the active product architecture while history remains auditable;
- T-528 must consume the new facade rather than reconstruct scientific orchestration in frontend state.

## T-529 closure

T-529 is complete. Repository evidence covers one immutable Study recipe through deterministic planning, restart-safe execution, real Phase A, exact finalized checkpoint consumption, common no-learning prefix, atomic FN/FD/AN/AD execution, retained scientific failure/skip semantics, structural validation, root/layout analysis, explicit denominators and deterministic lineage-preserving export without UI logic. Dedicated protocol-v2 and repository-wide CI were green on the reviewed implementation head before the documentation-only closure checkpoint.

No unresolved T-526/T-527 scientific value was invented or consumed to close T-529.

## Supersession boundary

This decision supersedes the final-architecture assumption that the existing v1.x run-centric runtime service and NiceGUI-era application read model should be incrementally extended for protocol-v2.

It does **not** supersede historical evidence, the validated scientific execution invariants, run-bundle provenance principles, DEC-048/050 methodology or DEC-049 frontend reselection.