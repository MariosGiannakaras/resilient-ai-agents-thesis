# Current Project Status

**Date:** 2026-08-28  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use **progressive** task-specific reading of DEC-048/049/050/051 and `docs/research/` / `docs/architecture/` only as needed.

## Current execution state

- Historical accepted baseline includes completed `T-100` target-machine validation and `T-200` research framing through protocol-v1.0 WP6 evidence. Frozen protocol-v1.0, `FINAL-*` and R0 evidence remain immutable. Candidate v1.1 is auditable non-final history; old `T-522` must not execute.
- `T-524` and `T-525` are COMPLETE. The validated protocol-v2 scientific core supports Q-Learning, SARSA, DQN, PPO and Dyna-Q+ with exact scientific continuation, actual-interaction accounting, isolated probes and matched FN/FD/AN/AD Phase-B semantics.
- **Current implementation task: `T-529` IN_PROGRESS.** DEC-051 reconstructs the backend around one study-first lifecycle: immutable recipe -> deterministic plan -> scientific jobs/checkpoints -> validation -> analysis -> thesis/presentation exports.
- **External scientific gate: `T-526` READY.** The predeclared non-final Windows feasibility pilot still has to run on the validated physical thesis machine. T-529 may continue without fabricating or consuming T-526/T-527 outcomes.
- `T-527` remains BLOCKED on T-526. Final methods/layouts/budgets/hyperparameters/severities/roots/statistics remain unfrozen.
- #93 / `T-528` remains PAUSED/BLOCKED. The final UI is rebuilt from scratch with a different framework from NiceGUI only after both T-527 and T-529 are complete.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution.

## Study-first backend reconstruction

The final application/backend aggregate is now `Study`, not a flat `Run`. Individual runs/checkpoints remain lower-level immutable evidence units.

Implemented under `src/resilient_agents/study/`:

- immutable content-addressed `StudyRecipe` with evidence classes and a frozen-confirmatory firewall;
- ordered study stages and deterministic job DAG;
- explicit scientific failure vs infrastructure failure vs downstream skip semantics;
- durable `StudyStore` with recipe/plan/lifecycle/events/artifact lineage and finalized tamper checks;
- deterministic planner with stable Phase-A/Phase-B IDs, exact Phase-A producer dependencies and method-specific Phase-B condition eligibility;
- generic executor ports/scheduler;
- restart-safe framework-neutral `StudyService` that reloads filesystem evidence rather than relying on UI session memory.

Implemented under `src/resilient_agents/evidence_v2/`:

- structural evidence validation from planned job to run/checkpoint/artifact lineage;
- validation-stage executor;
- standardized Phase-A/Phase-B analysis records;
- root/layout statistical primitives including interaction-axis learning summaries, paired effects, matched four-branch adaptation benefit and Student-t intervals driven by frozen recipe inputs.

Still active in T-529:

- real protocol-v2 Phase-A/Phase-B study executor bridge over validated method-native drivers;
- complete v2 analysis engine and explicit failure denominators;
- deterministic thesis/defense data/table/figure/evidence export package;
- final active-document/legacy-boundary reconciliation.

## Cleanup boundary

The superseded NiceGUI `src/app` implementation, v1.1 application `RuntimeService`/observer, NiceGUI-only tests, old runtime launcher and NiceGUI packaging/screenshot/validation scripts have been removed from the active tree. Their history remains in Git; historical scientific runners and finalized evidence are not deleted or rewritten.

`pyproject.toml` no longer exposes the old application entrypoint and packages only `src/resilient_agents`. NiceGUI/PyInstaller dependency-lock entries remain temporarily until the lock can be safely regenerated; they no longer define the active architecture.

## Protocol-v2 scientific invariants

### Phase A

- Train every retained method independently under common task/reward/action semantics, common semantic information and task-level `gamma`.
- Fairness resource = actual environment interactions, not episodes, optimizer updates or wall time.
- Standardized interaction-indexed no-learning probes operate only on cloned learner state.

### Phase B

Each `method × root × layout` originates from its own exact Phase-A checkpoint. The exact branch point is cloned into Frozen nominal, Frozen disturbed, Adaptive nominal and Adaptive disturbed branches. Adaptive updates begin only after the boundary and do not reset replay, optimizer, epsilon, warm-up, recency or schedules.

Primary adaptation benefit remains the matched four-branch difference-in-differences. T-525 validates one exact post-boundary segment; T-526/T-527 still own the final multi-episode reset/regime lifecycle decision.

## T-526 physical gate

Committed plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`.  
Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`.  
Entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`.

First pass remains the predeclared ordered 7×7 -> 10×10 -> 14×14 ladder, two layouts/level, three roots, five core methods, 2048 actual Phase-A training interactions and probes at 0/512/1024/2048. Hosted CI does not substitute for this machine evidence.

## Statistics / provenance

Root/run is the independent randomization unit; layouts are blocked/repeated observations. Scientific failures remain outcomes; infrastructure retries retain the same scientific identity. Final statistical values and contrast family are frozen only in T-527. Filesystem evidence remains authoritative; any future index/database must be rebuildable.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography`, immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources and 19 research materials.

## Still intentionally unfrozen

Final retained methods/A2C decision, selected GridWorld level/layouts, final budgets/gamma/reward/horizon, method hyperparameters, probe cadence, Phase-B reset lifecycle, uncertainty settings, roots/statistics, confirmatory Study recipe values, final frontend framework and final evidence remain T-526/T-527 gated.

## Exact next actions

Backend work: continue `T-529` with the real protocol-v2 Study executor bridge, then complete v2 analysis/export and repository reconciliation. Do not start UI.

User-machine scientific gate: from a clean reviewed branch checkout on the validated native Windows thesis machine, execute exactly once:

`powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1`

Retain `results/pilots/protocol-v2-feasibility-v0.1/` unchanged for review. Do not rerun/overwrite it, access final reserve or tune methods from final outcomes.
