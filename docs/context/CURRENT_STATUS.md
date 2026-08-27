# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative current-state summary

This file is intentionally short. Detailed policy, history, requirements, and design rationale live in the source-of-truth documents routed by `AGENTS.md`; do not grow this file into a second project manual.

## Current execution state

- Canonical concrete ledger: `docs/context/TASKS.md`.
- Existing WP0–WP6 work remains preserved, including the validated research core, `protocol-v1.0`, all finalized `FINAL-*` runs, and the existing thesis-final evidence package.
- `T-511` remains **USER_VALIDATION_REQUIRED**. Automated render/tests never substitute for the intended user's end-to-end application acceptance.
- **Pre-WP7 user approval: NOT APPROVED.** WP7/WP8 and all `T-700+` work remain blocked.
- The user explicitly reopened the pre-writing scientific/application state on 2026-08-27 and requested direct implementation of the approved refinement rather than thesis writing.

### Active refinement package

- **Decision:** `DEC-042` — pre-WP7 protocol v1.1 and application refinement.
- **Single implementation branch:** `feat/pre-wp7-protocol-v1.1-ui-rebuild`.
- **GitHub trackers:** master #87; scientific #88; runtime #89; UI #90; screenshots/CI/Codex handoff #91.
- **Branch policy for this package:** continue only on the branch above; do not open a parallel implementation branch. Intermediate commits are recovery checkpoints. The branch is not merged merely because automated checks pass; user-facing application acceptance remains an explicit gate.
- **Current milestone:** 1/8 governance/handoff checkpoint in progress. `DEC-042` is committed; canonical task-ledger reconciliation and the first implementation checkpoint follow on the same branch.

### Accepted scientific direction for v1.1 candidate

- Preserve `protocol-v1.0`, historical finalized runs, frozen evidence, and R0 pilot evidence immutably.
- Retain F0 frozen Q-learning and C0 continual Q-learning from the common nominal checkpoint.
- Add D0 Dyna-Q+ as a third scientifically distinct tabular agent using only agent-visible interaction data; no evaluator information leakage.
- Do not add deep RL merely to increase model count and do not reinstate the accepted R0 construction unchanged.
- Preserve the existing validated F0/C0 base configuration: learning rate `0.5`, discount `0.96875`, exploration epsilon `0.125`, 512 training episodes/layout, 16 pre-change episodes, 32 post-change episodes, 48-step horizon, and 32 paired final roots.
- Candidate v1.1 retains seven single-factor conditions but structurally renames the remaps to `action-remap-2-swap` and `action-remap-4-cycle`.
- Candidate v1.1 uses four **new held-out final layouts** and a **fresh precommitted final seed bank** because v1.0 final outcomes have already been inspected.
- D0-specific planning parameters require a bounded development/tuning selection and non-final validation. **`protocol-v1.1` is not frozen and no v1.1 final campaign may run until that evidence exists.**
- Primary reporting: cumulative deficit, immediate degradation, and terminal gap/performance. Recovery remains secondary/sensitivity with explicit non-recovery. Add paired agent effects and 95% confidence intervals; no post-hoc favorable threshold selection and no composite resilience score.

### Accepted application direction

- Keep `src/resilient_agents/` headless and UI-independent.
- Add an application/runtime service layer for truthful active-run registry, heartbeat/progress/events, read-only live GridWorld state, history, and capability-based controls.
- Rebuild the Streamlit surface around Dashboard → New Experiment → Runs/live GridWorld → Compare → Artifacts. The current page implementation is not a design baseline and may be replaced substantially.
- UI controls, progress, logs, metrics, and lifecycle state must be backend-derived. Unsupported controls remain explicitly unsupported.
- Visualization speed changes presentation cadence only and never scientific timing/RNG.
- Historical finalized runs without a retained step trace show replay unavailable; never synthesize or reconstruct a trajectory.
- Keep root `run_app.bat` working.
- Create root `ui-screenshots/` and commit stable CI-rendered screenshots there for review once the relevant UI milestone is stable. Screenshot fixtures are UI-only and never scientific evidence.

## Accepted repository / Codex baseline

- Python 3.12 + `uv` + committed lockfile; native Windows CPU execution is the required supported scientific baseline.
- Project-owned Gymnasium GridWorld, explicit agent/evaluator information boundary, independent deterministic RNG streams, filesystem-first finalized run bundles, provenance/checksums, and guarded publication remain authoritative.
- UI/application code consumes the validated scientific core; it never reimplements experiment semantics.
- Invalid or ambiguous required scientific/provenance/lifecycle state fails closed. Never fabricate data, evidence, progress, logs, metrics, results, protocol state, or apparent success.
- Testing is risk-based and proportional: targeted checks during implementation and PR CI as the canonical full-suite guard when available. No arbitrary coverage target and no pilot/final experiment matrix in CI.

Codex session startup remains exactly `AGENTS.md`, `docs/context/TASKS.md`, and this file, followed by only task-specific evidence. The tracked bootstrap is `docs/context/CODEX_EXECUTION_PROMPT.md`.

## Exact continuation rule

On this work package, Codex must first verify that it is on `feat/pre-wp7-protocol-v1.1-ui-rebuild`, inspect #87–#91/current branch commits, and resume the first incomplete dependency-valid refinement subtask. It must keep repository status/task/decision files synchronized at checkpoints and must not create another implementation branch for this package.

The intended execution order is:

1. durable governance/task handoff;
2. D0 + candidate protocol-v1.1 + statistical support;
3. truthful application runtime/service layer;
4. Streamlit workflow/live GridWorld rebuild;
5. root UI screenshot capture + bounded CI validation;
6. real user E2E review/acceptance.

No `T-700+` action is permitted. After all pre-WP7 refinements are technically complete and the user has reviewed the resulting application/screenshots, explicitly ask whether they approve starting WP7. Only a direct affirmative answer unlocks writing/defense work.

## Bibliography and target-machine boundaries

`MariosGiannakaras/ThesisBibliography` remains the canonical bibliography source of truth. Scientific source originals are not edited here. The accepted target-machine baseline remains native Windows CPython 3.12 via `uv`, Ryzen 5 2600X / ~31.9 GiB RAM, CPU-required execution; the Radeon RX 570 is not a validated scientific-compute backend.

Supervisor identity, future corrections, deadlines, example theses, final Word formatting, and exact defense/submission rules remain later-stage inputs and do not block this pre-WP7 refinement.
