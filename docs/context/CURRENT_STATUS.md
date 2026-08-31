# Current Project Status

**Date:** 2026-08-31
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use **progressive** task-specific reading of DEC-048/049/050/051/052/053/054/055/056/057/058/059 and `docs/research/` / `docs/architecture/` only as needed.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, `T-528` and `T-529` are COMPLETE.
- `T-529` completed DEC-051's framework-neutral Study lifecycle from immutable recipe through real execution, validation, root/layout analysis and deterministic evidence export.
- `T-527` is COMPLETE under DEC-058. DEC-055 tuning is immutable valid-complete; sizing-v0.1 and v0.2 are immutable valid-failed and cannot be resumed/rerun. DEC-057 sizing-v0.3 and the combined five-method sizing package are valid-complete.
- DEC-058 accepts the final protocol-v2.0 scientific freeze. `configs/protocols/protocol-v2.0-final.json` retains `final_reserve_access=false`; issue #95 is 10/10 and CLOSED. No final-reserve scientific outcome was generated, and T-610+ remains unauthorized/unexecuted.
- **`T-528 — Final Application / Frontend Rebuild` is COMPLETE under DEC-059.** The final application is Python-native PySide6 / Qt 6 Widgets over the framework-neutral Study backend; NiceGUI remains historical prototype only.
- T-528 implements the recipe-first Thesis Study review path, clearly separated DEVELOPMENT/Exploratory Study flow, durable Study creation, non-blocking worker/supervisor execution, truthful Runs progress, matched Frozen/Adaptive live GridWorld presentation, stored-evidence Results (Compare Learning / Test Resilience), registered-artifact provenance, accessibility/help/empty/error/locked states and deterministic CI screenshot review artifacts.
- T-528's bounded DEVELOPMENT application smoke completed the complete create -> execute -> validate -> analyze -> evidence-handoff lifecycle without final identities. The accepted implementation head before screenshot curation (`15fe9598955df1fa5fecff86fa1d9a80767045f6`) had Repository checks, Protocol-v2 checks and PySide6 UI screenshot checks all green.
- The curated `ui-screenshots/pyside6/` review set is current; `ui-screenshots/historical-nicegui/` is historical-only. CI remains the authoritative full screenshot bundle, including laptop-width sanity renders and historical side-by-side references.
- **`T-511 — Intended-user application workflow/self-explanatory UX acceptance` is READY and is the next application gate.** It requires explicit user acceptance; automated checks cannot close it.
- Master tracker #87 is now **6/8** objectively complete: milestones 1, 2, 3, 4, 5 and 7. Milestone 6 awaits T-511 human acceptance; milestone 8 additionally depends on the final v2 evidence chain.
- PR #92 remains OPEN, DRAFT and UNMERGED.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution.

## Completed Study-first backend

Current reusable backend/evidence foundation includes:

- immutable recipes/evidence, stable-ID DAG barriers and restart-safe `StudyStore`/`StudyService`;
- real Q-Learning/SARSA/DQN/PPO/Dyna-Q+ execution with exact checkpoints and explicit failure semantics;
- shared-prefix atomic FN/FD/AN/AD branching, structural validation and root/layout analysis;
- explicit status denominators and deterministic lineage-preserving CSV/JSON export.

## Completed final application foundation

DEC-059 selects PySide6 / Qt 6 Widgets for the final local desktop application. The UI consumes application/read-model boundaries and does not own or reimplement scientific protocol logic.

Application behavior now includes:

- read-only frozen Thesis Study review while `final_reserve_access=false`;
- DEVELOPMENT-only Exploratory Study creation using non-final layouts/root namespaces;
- server/application-side execution policy that rejects final identities and non-DEVELOPMENT study execution;
- `QProcess`-based non-blocking local worker supervision over durable Study state;
- Runs progress derived from `StudyStore`, with scientific/infrastructure failure distinction retained;
- presentation-only dropping live-event sink/read model and matched FD/AD visualization that cannot feed back into action selection, RNG, checkpoints or evidence;
- stored `analysis-package` rendering with integrity/provenance checks rather than UI-side estimand recomputation;
- registered artifact lineage/provenance presentation without arbitrary filesystem browsing;
- deterministic PySide6 screenshot CI plus curated review set and 1366×768 / 1440×900 visual sanity coverage.

## Protocol-v2 invariants

Phase A independently trains each retained method under common semantic task/information/action/reward/gamma semantics and a principal actual-environment-interaction budget, with isolated no-learning probes.

Each Phase-B `method × root × layout` starts from its own exact Phase-A checkpoint. The exact branch point is cloned into FN/FD/AN/AD. Adaptive updates begin only after the boundary; replay, optimizer, exploration, warm-up, model/recency, schedules, counters and RNG state are not silently reset.

Primary adaptation benefit remains matched four-branch DiD. Root/run is the independent unit; layouts/episodes/checkpoints are blocked/repeated observations. Scientific failures remain retained outcomes and seeds are not replaced from outcomes.

## T-526 physical gate

Plan: `configs/protocols/protocol-v2-feasibility-v0.1.json`  
Runbook: `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`  
Entrypoint: `scripts/run_protocol_v2_feasibility_windows.ps1`

Historical failed recovery authority/config/entrypoint: `docs/decisions/DEC-052_T526_CHECKPOINT_MATERIALIZATION_AND_PHASE_B.md`, `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.1.json`, `scripts/run_protocol_v2_t526_recovery_phase_b_windows.ps1`.

DEC-053 recovery and DEC-054 boundary-settlement evidence remain immutable historical/accepted scientific evidence. DEC-055/056 failed sizing attempts remain immutable failed evidence. DEC-057 sizing-v0.3 and the combined five-method matrix remain the accepted non-final sizing authority. No scientific package was rerun by T-528.

## Statistics / provenance

Final statistical values and the contrast family are frozen by T-527 in DEC-058. Filesystem evidence remains authoritative and any future index/database must be rebuildable.

DEC-058 authority/firewall: `docs/decisions/DEC-058_PROTOCOL_V2_FINAL_SCIENTIFIC_FREEZE.md` and `configs/protocols/protocol-v2.0-final.json`. The protocol is frozen with `final_reserve_access=false`; explicit later T-610+ authorization is required for final-reserve scientific execution.

DEC-059 application authority: `docs/decisions/DEC-059_PYSIDE6_FINAL_APPLICATION_ARCHITECTURE.md`. T-528 application presentation and DEVELOPMENT smoke evidence do not authorize final scientific execution.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography`, immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources and 19 research materials. `bibliography-integration-v3` remains immutable historical terminology.

## Still intentionally gated

- Final-reserve execution remains sealed: `final_reserve_access=false`.
- `T-511 — Intended-user application workflow/self-explanatory UX acceptance` requires explicit user acceptance.
- `T-610+` remains blocked until its dependencies and explicit scientific authorization are satisfied.
- WP7 remains blocked by the mandatory explicit pre-WP7 user-approval gate.
- Final Windows standalone packaging remains deferred to `T-803` / issue #94.

## Exact next action

Perform `T-511 — Intended-user application workflow/self-explanatory UX acceptance` using the accepted PySide6 screenshots/application workflow. Do not execute T-610+, do not access the final reserve and do not start WP7 merely because T-528 is complete.
