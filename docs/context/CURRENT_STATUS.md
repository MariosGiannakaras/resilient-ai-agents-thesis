# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative current-state summary

This file is intentionally short. Detailed policy/history live in the routed source-of-truth documents; use progressive disclosure rather than growing this into a second manual.

## Current execution state

- Canonical ledger: `docs/context/TASKS.md`.
- Historical milestones remain accepted and preserved, including `T-100` target-machine baseline and `T-200` research framing through completed WP6 evidence production.
- `T-511` remains **USER_VALIDATION_REQUIRED**. Automated checks/screenshots never substitute for intended-user E2E acceptance.
- **Pre-WP7 user approval: NOT APPROVED.** All `T-700+` WP7/WP8 work remains blocked.
- Existing `protocol-v1.0`, every finalized `FINAL-*` bundle, and the current thesis-final evidence package remain immutable historical baseline evidence.

## Active pre-WP7 refinement

- Accepted decision: `DEC-042`.
- Single implementation branch: `feat/pre-wp7-protocol-v1.1-ui-rebuild`.
- Single draft integration PR: #92.
- Trackers: master #87; scientific #88; runtime #89; UI #90; screenshots/CI/Codex handoff #91.
- Do not create a parallel implementation branch for this work package.
- `T-513` governance/Codex handoff is complete. Master tracker #87 is **1/8**.
- Current task: `T-520 IN_PROGRESS` — integrate D0 into the headless runner/agent-construction path.
- Standalone D0 implementation and focused tests are committed. PR CI run 266 on branch head `e4b95c24cb191233b6a82190dcb81d0a3b4bcd57` completed successfully after the canonical task-ledger reconciliation.

### Scientific direction

- Retain F0 frozen Q-learning and C0 continual Q-learning from their common selected nominal checkpoint.
- Add D0 Dyna-Q+ as a third scientifically distinct tabular agent using only agent-visible interaction data; evaluator-only information remains forbidden.
- Keep the existing validated F0/C0 values: alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, 48-step horizon, and 32 paired final roots.
- `protocol-v1.1` is a **candidate**, not frozen. D0-specific planning parameters require bounded development/tuning selection and non-final validation before any freeze.
- Candidate v1.1 keeps seven single-factor conditions, structurally renames the remaps to `action-remap-2-swap` and `action-remap-4-cycle`, and must use four fresh held-out final layouts plus a fresh precommitted final seed bank because v1.0 final outcomes have already been inspected.
- Primary reporting: cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity with explicit `NOT_RECOVERED`; paired effects and 95% CIs are required. No composite resilience score or post-hoc favorable threshold.
- Preserve R0 pilot evidence; do not reinstate the accepted R0 construction unchanged and do not add deep RL merely to increase model count.

### Application direction

- Keep `src/resilient_agents/` headless and UI-independent.
- Add an application/runtime service for truthful active-run state, heartbeat/progress/events, read-only live GridWorld observation, history, and only lifecycle controls that can actually be honored safely.
- Rebuild Streamlit around Dashboard → New Experiment → Runs/live GridWorld → Compare → Artifacts. Current page code may be substantially replaced.
- Status/progress/logs/metrics are backend-derived; unsupported controls remain explicit.
- Visualization speed changes presentation cadence only, never experiment timing/RNG.
- Historical finalized runs without retained step trace display replay unavailable; never synthesize a path.
- Keep root `run_app.bat` functional.
- Create repository-root `ui-screenshots/` for stable CI-rendered review screenshots; screenshot fixtures are not scientific evidence.

## Accepted repository / Codex baseline

- Python 3.12 + `uv`, project-owned Gymnasium GridWorld, explicit agent/evaluator information boundary, deterministic RNG streams, filesystem-first finalized run bundles, provenance/checksums, and guarded publication remain authoritative.
- Native Windows CPU execution remains the required scientific baseline; the Radeon RX 570 is not a validated scientific-compute backend.
- Invalid/ambiguous required scientific, provenance, or lifecycle state fails closed. Never fabricate data, evidence, state, progress, logs, metrics, protocol status, or results.
- Testing remains risk-based and proportional; PR CI is the full-suite guard when available and pilot/final matrices are never CI tests.
- Codex session startup remains exactly `AGENTS.md`, `docs/context/TASKS.md`, and this file, followed by progressive task-specific reading. Bootstrap: `docs/context/CODEX_EXECUTION_PROMPT.md`.

## Bibliography baseline

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable thesis import remains `bibliography-integration-v3`; bibliography originals are not edited in this repository.

## Still intentionally unfrozen

The v1.1 D0-specific planning parameters, final v1.1 freeze, and any new v1.1 final evidence remain intentionally unfrozen until the bounded non-final tuning/pilot and protocol acceptance gates are satisfied. Later supervisor/deadline/template/defense inputs remain deferred and do not block this package.

## Exact next action

Continue `T-520` on the existing branch: integrate D0 into the headless runner while preserving learned Q/model/recency state across evaluation episodes and reseeding only agent RNG streams at episode boundaries; add focused integration tests proving deterministic matched pre-change behavior and no evaluator-information leakage. Then advance to `T-521` only after `T-520` acceptance passes. No `T-700+` action is permitted.

After technical refinement and user review are complete, explicitly ask whether the user approves starting WP7. Only a direct affirmative answer unlocks writing/defense work.
