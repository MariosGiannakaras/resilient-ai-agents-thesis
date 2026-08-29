# Current Project Status

**Date:** 2026-08-29  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use **progressive** task-specific reading of DEC-048/049/050/051 and `docs/research/` / `docs/architecture/` only as needed.

## Current execution state

- Historical accepted baseline includes completed `T-100` target-machine validation and `T-200` research framing through protocol-v1.0 WP6 evidence. Frozen protocol-v1.0, `FINAL-*` and R0 evidence remain immutable. Candidate v1.1 is auditable non-final history; old `T-522` must not execute.
- `T-524` and `T-525` are COMPLETE. The validated protocol-v2 scientific core supports Q-Learning, SARSA, DQN, PPO and Dyna-Q+ with exact scientific continuation, actual-interaction accounting, isolated probes and matched FN/FD/AN/AD Phase-B semantics.
- **`T-529` is COMPLETE.** DEC-051's framework-neutral Study lifecycle is implemented from immutable recipe through deterministic plan, real scientific execution/checkpoint lineage, validation, root/layout analysis, explicit denominators and deterministic machine-readable evidence export. No final frontend was implemented.
- **Current dependency-valid scientific gate: `T-526` READY.** The predeclared non-final Windows feasibility pilot still requires execution on the validated physical thesis machine. Hosted CI cannot substitute for it.
- The latest physical T-526 attempt stopped at mandatory repository preflight before the runner started. The physical checkout reported local HEAD `6aacd40332fe8578ab5e1c9a34bae30d4e321688`, stale relative to the remote branch, plus untracked prior PR draft `temp_body.md`. No `results/pilots/protocol-v2-feasibility-v0.1/` directory, selected level, scientific outcomes, runtime data, checkpoints or validation evidence were produced. The reported WSL change to `results/thesis_evidence_package.zip` was verified as Git LFS hydration with matching committed content and native Windows Git clean.
- `T-527` remains BLOCKED on T-526. Final methods/layouts/budgets/hyperparameters/severities/roots/statistics remain unfrozen.
- #93 / `T-528` remains PAUSED/BLOCKED on T-527. Its T-529 backend dependency is now satisfied. The final UI must be rebuilt from scratch with a framework different from NiceGUI.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution.

## Completed Study-first backend

The final application/backend aggregate is `Study`, not a flat `Run`. Individual runs/checkpoints remain lower-level immutable evidence units.

Implemented under `src/resilient_agents/study/`:

- immutable content-addressed `StudyRecipe` with evidence classes and a frozen-confirmatory firewall;
- ordered study stages and deterministic job DAG;
- explicit scientific failure vs infrastructure failure vs downstream skip semantics;
- durable `StudyStore` with recipe/plan/lifecycle/events/artifact lineage and finalized tamper checks;
- deterministic planner with stable Phase-A/Phase-B IDs, exact Phase-A producer dependencies and method-specific Phase-B condition eligibility;
- generic executor ports/scheduler;
- restart-safe framework-neutral `StudyService` that reloads filesystem evidence rather than relying on UI session memory;
- concrete default protocol-v2 executor registry;
- real Q-Learning/SARSA/DQN/PPO/Dyna-Q+ Phase-A execution that emits finalized scientific evidence and exact method-native checkpoints;
- explicit Random supporting-reference Phase-A execution with unknown reference identities failing closed;
- exact Phase-B checkpoint consumption, common no-learning prefix and one atomic matched FN/FD/AN/AD execution unit from the same branch point.

Implemented under `src/resilient_agents/evidence_v2/`:

- structural evidence validation from planned job to run/checkpoint/artifact lineage;
- validation-stage executor;
- standardized Phase-A/Phase-B analysis records;
- root/layout analysis with interaction-axis learning summaries and matched four-branch adaptation benefit;
- explicit planned/completed/scientific-failure/skipped/infrastructure-failure/cancelled/pending/running denominators;
- deterministic analysis-package lineage;
- deterministic export/handoff with machine-readable CSV/JSON root/summary tables, stable `RESULT-*` identities and integrity/provenance manifests.

T-529 intentionally does not generate thesis prose, final thesis figures or PPTX. Those later assets remain downstream of frozen final evidence and the T-612/T-613/WP7 gates.

## T-529 closure validation

Repository evidence at the reviewed implementation head demonstrated the complete acceptance chain: one immutable Study recipe can be planned, executed/resumed, run through real Phase A, consume the exact finalized checkpoint, create a common no-learning prefix, atomically execute FN/FD/AN/AD, retain scientific failures and downstream skips, validate evidence, analyze at root/layout level with explicit denominators and deterministically export a lineage-preserving package without UI logic.

The latest implementation head before this documentation reconciliation had both repository-wide `sanity` CI and dedicated `focused-conformance` protocol-v2 checks green. The final reconciliation changes active documentation/tracker state only; no protocol-v2 scientific implementation or pilot plan is modified.

## Cleanup boundary

The superseded NiceGUI `src/app` implementation, v1.1 application `RuntimeService`/observer, NiceGUI-only tests, old runtime launcher and NiceGUI packaging/screenshot/validation scripts have been removed from the active tree. Their history remains in Git; historical scientific runners and finalized evidence are not deleted or rewritten.

`pyproject.toml` no longer exposes the old application entrypoint and packages only `src/resilient_agents`. Legacy dependency-lock entries do not define the active architecture.

## Protocol-v2 scientific invariants

### Phase A

- Train every retained method independently under common task/reward/action semantics, common semantic information and task-level `gamma`.
- Fairness resource = actual environment interactions, not episodes, optimizer updates or wall time.
- Standardized interaction-indexed no-learning probes operate only on cloned learner state.

### Phase B

Each `method × root × layout` originates from its own exact Phase-A checkpoint. The exact branch point is cloned into Frozen nominal, Frozen disturbed, Adaptive nominal and Adaptive disturbed branches. Adaptive updates begin only after the boundary and do not reset replay, optimizer, epsilon, warm-up, recency or schedules.

Primary adaptation benefit remains the matched four-branch difference-in-differences. T-525/T-529 validate exact current execution semantics; T-526/T-527 still own the final multi-episode reset/regime lifecycle decision.

## T-526 physical gate

Committed plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`.  
Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`.  
Entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`.

First pass remains the predeclared ordered 7×7 -> 10×10 -> 14×14 ladder, two layouts/level, three roots, five core methods, 2048 actual Phase-A training interactions and probes at 0/512/1024/2048. Hosted CI does not substitute for this machine evidence.

Before the one-time physical run, inspect the untracked `temp_body.md` and preserve any unique content; if it is confirmed as an obsolete PR-body draft, remove it from the repository working tree. Then fast-forward the physical branch to the reviewed current remote head and require a clean native-Windows Git preflight. This repository-state repair is infrastructure handling, not a scientific protocol amendment and not a scientific failure.

## Statistics / provenance

Root/run is the independent randomization unit; layouts are blocked/repeated observations. Scientific failures remain outcomes; infrastructure retries retain the same scientific identity. Final statistical values and contrast family are frozen only in T-527. Filesystem evidence remains authoritative; any future index/database must be rebuildable.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography`, immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources and 19 research materials. The synchronized consumer history label `bibliography-integration-v3` remains immutable.

## Still intentionally unfrozen

Final retained methods/A2C decision, selected GridWorld level/layouts, final budgets/gamma/reward/horizon, method hyperparameters, probe cadence, Phase-B reset lifecycle, uncertainty settings, roots/statistics, confirmatory Study recipe values, final frontend framework and final evidence remain T-526/T-527 gated.

## Exact next action

All dependency-valid in-repository T-529 work is exhausted. The next gate is the physical Windows T-526 pilot.

On the validated thesis machine:

1. inspect/preserve or explicitly discard only the confirmed-obsolete untracked `temp_body.md` draft;
2. fast-forward `feat/pre-wp7-protocol-v1.1-ui-rebuild` to the reviewed current remote branch head and verify the native-Windows working tree is clean;
3. execute exactly once:

`powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1`

Retain `results/pilots/protocol-v2-feasibility-v0.1/` unchanged for review. Do not rerun/overwrite scientific failures, access final reserve or tune methods from final outcomes.