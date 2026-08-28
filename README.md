# resilient-ai-agents-thesis

**Official Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

Version-controlled repository for the complete thesis lifecycle: research context, bibliography consumer, scientific implementation, controlled experiments, evidence validation, analysis, thesis assets, defense assets and final delivery.

## Project principle

The research contribution is the controlled comparison of resilient AI-agent strategies under uncertainty/change. GridWorld is the common controlled testbed and visualization surface; the application supports the research and is not the research contribution itself.

> **Polished outside, bounded inside.**

The final tool is local and single-user. Scientific validity, reproducibility and a realistic thesis scope take priority over production-platform complexity.

## Current architecture

The active scientific/backend implementation lives in:

```text
src/resilient_agents/
```

The current protocol-v2 architecture is **study-first**.

```text
immutable Study recipe
        -> deterministic job plan
        -> Phase A independent nominal learning
        -> exact scientific checkpoints
        -> Phase B FN / FD / AN / AD branches
        -> evidence validation
        -> root-level statistical analysis
        -> thesis / defense export package
```

A `Run` remains a lower-level scientific evidence unit. A `Study` is the authoritative parent lifecycle.

### Scientific core

The validated protocol-v2 scientific layer includes:

- project-owned Gymnasium-compatible GridWorld;
- strict separation of evaluator ground truth from agent-visible information;
- independent scoped RNG streams;
- actual environment-interaction accounting;
- Q-Learning, SARSA, DQN, PPO and Dyna-Q+ candidate implementations;
- isolated no-learning evaluation probes;
- exact method-specific scientific checkpoint/restore semantics;
- matched Frozen nominal / Frozen disturbed / Adaptive nominal / Adaptive disturbed Phase-B execution;
- fail-closed information, checkpoint and branch invariants.

### Study orchestration

`src/resilient_agents/study/` owns framework-neutral application/backend orchestration:

- immutable content-addressed `StudyRecipe`;
- evidence classes separating development/tuning/confirmatory/derived/history;
- deterministic recipe-to-job DAG materialization;
- scientific-vs-infrastructure failure semantics;
- restart-safe study persistence and artifact lineage;
- sequential stage barriers;
- generic executor registry/scheduler;
- framework-neutral `StudyService` facade.

### Protocol-v2 evidence and analysis

`src/resilient_agents/evidence_v2/` is the new v2-only evidence path. It remains separate from historical v1.x analysis so historical finalized evidence stays reproducible.

It owns:

- planned-vs-produced evidence validation;
- exact Phase-A checkpoint -> Phase-B lineage validation;
- standardized heterogeneous method analysis records;
- root/layout statistical primitives;
- deterministic analysis/export work as T-529 progresses.

## Legacy boundary

Historical protocol-v1.0 / v1.1 scientific code and finalized evidence remain auditable and reproducible. They are not silently reinterpreted as protocol-v2 confirmatory evidence.

The superseded NiceGUI application, v1.1 application runtime service, old native/package validation surface and UI-only tests were removed from the **active tree** during DEC-051/T-529 reconstruction. Git history remains the audit trail.

The final frontend is intentionally absent. T-528 will select a framework **different from NiceGUI** and rebuild the application from scratch only after the remaining scientific contract (T-527) and study-first backend (T-529) are stable.

## Current scientific gate

T-526 is the next external scientific evidence gate. It uses the predeclared non-final plan:

```text
configs/protocols/protocol-v2-feasibility-v0.1.json
```

On the validated physical Windows thesis machine, the committed entrypoint is:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1
```

Hosted CI does not substitute for that physical-machine evidence. T-529 backend reconstruction may continue in parallel but must not invent or consume values that remain T-526/T-527 gated.

## Repository map

```text
src/resilient_agents/                  Scientific core + study backend
src/resilient_agents/study/            Study recipe/DAG/store/scheduler/service
src/resilient_agents/evidence_v2/      Protocol-v2 validation/analysis/export

configs/                               Version-controlled protocol/scenario inputs
scripts/                               Reproducibility and maintenance utilities
tests/                                 Risk-based scientific/backend regression tests

research/bibliography/                 Immutable consumed bibliography corpus
results/runs/                          Lower-level whole-run bundles
results/studies/                       Study-level parent lifecycle/evidence bundles
results/thesis-final/                  Frozen final thesis evidence when authorized
artifacts/                             Reproducible generated figures/tables/exports

thesis/                                Source material and later thesis deliverables
presentation/                          Later defense sources/assets/final deck

docs/context/                          Current status/tasks/workflow
docs/research/                         Methodology and protocol research
docs/experiments/                      Experiment/provenance rules
docs/architecture/                     Backend/frontend architecture
docs/thesis/                           Deferred thesis/defense workflows
docs/decisions/                        Decisions and ADRs
```

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` is the canonical bibliography lifecycle repository. This repository consumes only an immutable generated snapshot. Formal automatic citation trust is limited to `research/bibliography/citation-ready/`.

The current protocol-v2 consumer snapshot is pinned to upstream SHA:

`f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`

with 597 canonical sources, 121 citation-ready sources and 19 research materials.

## Current control files

Always use these as current authority:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Important supporting decisions/specifications include:

- `docs/decisions/DEC-048_PROTOCOL_V2_INDEPENDENT_LEARNING_AND_MATCHED_RESILIENCE.md`
- `docs/decisions/DEC-049_FRONTEND_RESELECTION_AFTER_PROTOCOL_V2_BACKEND.md`
- `docs/decisions/DEC-050_PROTOCOL_V2_CLOSURE_REFINEMENTS.md`
- `docs/decisions/DEC-051_STUDY_FIRST_BACKEND_RECONSTRUCTION.md`
- `docs/architecture/STUDY_BACKEND_REDESIGN.md`

Historical bootstrap, UI and candidate-protocol documentation is context only where explicitly marked historical/superseded.

## Evidence and integrity principles

- Filesystem evidence is authoritative; indexes/databases must be rebuildable.
- Finalized evidence is immutable and checksum/provenance protected.
- Scientific failures remain outcomes and are not replaced by favorable roots.
- Infrastructure failures are distinct and may retry only under the same scientific identity/provenance rules.
- Development/tuning/custom outputs cannot silently become confirmatory evidence.
- Phase-B results must trace to the exact Phase-A scientific checkpoint that generated them.
- Final figures/tables/results are regenerated from frozen evidence, not transcribed from the UI.
- No final reserve is accessed before its protocol gate.
- No thesis writing starts before the explicit pre-WP7 user approval gate.

## End-to-end lifecycle

The intended project chain is:

> methodology/bibliography -> feasibility -> protocol freeze -> validated study backend/application -> frozen protocol-v2 final Study -> evidence validation -> predeclared analysis -> thesis evidence package -> explicit user approval -> Greek thesis/review -> defense presentation -> final audit/delivery

The application therefore becomes a client of the research backend, not the source of scientific truth.
