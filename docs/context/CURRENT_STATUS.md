# Current Project Status

**Date:** 2026-08-29  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use **progressive** task-specific reading of DEC-048/049/050/051 and `docs/research/` / `docs/architecture/` only as needed.

## Current execution state

- Historical accepted baseline includes completed `T-100` target-machine validation and `T-200` research framing through protocol-v1.0 WP6 evidence. Protocol-v1.0, FINAL-* and R0 evidence remain immutable. Candidate v1.1 is non-final history; old `T-522` must not execute.
- `T-524`, `T-525` and `T-529` are COMPLETE.
- `T-529` completed DEC-051's framework-neutral Study lifecycle: immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis with explicit denominators -> deterministic machine-readable evidence export. No final frontend, thesis prose, final thesis figures or PPTX were generated.
- **Current dependency-valid gate: `T-526` READY.** It still requires the predeclared non-final pilot on the validated physical Windows thesis machine. Hosted CI cannot substitute for it.
- The latest physical T-526 attempt stopped before the runner started because repository preflight failed. The checkout reported local HEAD `6aacd40332fe8578ab5e1c9a34bae30d4e321688`, stale relative to remote, plus untracked prior PR draft `temp_body.md`. No T-526 result directory, selected level, runtime data, checkpoints, scientific outcomes or validation evidence were produced. The reported WSL change to `results/thesis_evidence_package.zip` was verified as Git LFS hydration with matching committed content and native Windows Git clean.
- `T-527` is BLOCKED on T-526. Final methods/layouts/budgets/hyperparameters/severities/roots/statistics remain unfrozen.
- `T-528` / #93 is PAUSED/BLOCKED on T-527; its T-529 backend dependency is satisfied. The final frontend must use a framework different from NiceGUI.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution.

## Completed Study-first backend

Current reusable backend/evidence foundation includes:

- immutable content-addressed `StudyRecipe`, evidence classes and frozen-confirmatory firewall;
- deterministic stable-ID job DAG with stage barriers and exact Phase-A producer dependencies;
- durable restart-safe `StudyStore`/`StudyService` with artifact lineage/finalization integrity;
- explicit scientific failure, infrastructure failure and downstream skip semantics;
- real Q-Learning/SARSA/DQN/PPO/Dyna-Q+ Phase-A Study execution and explicit Random supporting reference execution;
- method-native exact scientific checkpoints and fail-closed checkpoint integrity checks;
- one shared no-learning Phase-B prefix and atomic matched FN/FD/AN/AD execution from the exact same branch point;
- structural evidence validation;
- Phase-A interaction-axis learning summaries and root/layout blocked Phase-B matched adaptation effects;
- explicit planned/completed/scientific-failure/skipped/infrastructure-failure/cancelled/pending/running denominators;
- deterministic analysis/export lineage with machine-readable CSV/JSON, stable `RESULT-*` IDs and integrity/provenance manifests;
- default concrete protocol-v2 executor registry behind the framework-neutral StudyService.

The reviewed implementation head had repository-wide `sanity` and dedicated protocol-v2 `focused-conformance` checks green before the documentation closure checkpoint. Documentation-only follow-up CI must remain green before the checkpoint is considered fully reconciled.

## Protocol-v2 invariants

Phase A independently trains each retained method under common semantic task/information/action/reward/gamma semantics and a principal actual-environment-interaction budget, with isolated no-learning probes.

Each Phase-B `method × root × layout` starts from its own exact Phase-A checkpoint. The exact branch point is cloned into FN/FD/AN/AD. Adaptive updates begin only after the boundary; replay, optimizer, exploration, warm-up, model/recency, schedules, counters and RNG state are not silently reset.

Primary adaptation benefit remains matched four-branch DiD. Root/run is the independent unit; layouts/episodes/checkpoints are blocked/repeated observations. Scientific failures remain retained outcomes and seeds are not replaced from outcomes.

## T-526 physical gate

Plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`  
Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`  
Entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`

The predeclared first pass remains ordered 7×7 -> 10×10 -> 14×14, two layouts/level, three roots, five core methods, 2048 actual Phase-A training interactions and probes at 0/512/1024/2048.

Before retrying, inspect `temp_body.md` and preserve any unique content; remove it from the repository working tree only if confirmed obsolete. Then fast-forward the active physical branch to the reviewed current remote head and require a clean native-Windows Git preflight. This is repository/infrastructure repair, not a scientific protocol amendment or scientific failure.

## Statistics / provenance

Final statistical values and the contrast family freeze only in T-527. Filesystem evidence remains authoritative and any future index/database must be rebuildable.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography`, immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources and 19 research materials. `bibliography-integration-v3` remains immutable historical terminology.

## Still intentionally unfrozen

Final retained methods/A2C decision, selected GridWorld level/layouts, final budgets/gamma/reward/horizon, method hyperparameters, probe cadence, Phase-B reset lifecycle, uncertainty settings, roots/statistics, confirmatory Study recipe values, final frontend framework and final evidence remain T-526/T-527 gated.

## Exact next action

All dependency-valid in-repository T-529 work is complete. On the validated physical thesis machine:

1. inspect/preserve or explicitly discard only the confirmed-obsolete untracked `temp_body.md`;
2. fast-forward `feat/pre-wp7-protocol-v1.1-ui-rebuild` to the reviewed current remote head and verify clean native-Windows Git status;
3. execute exactly once:

`powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1`

Retain `results/pilots/protocol-v2-feasibility-v0.1/` unchanged for review. Do not rerun/overwrite scientific failures, access final reserve or tune methods from final outcomes.