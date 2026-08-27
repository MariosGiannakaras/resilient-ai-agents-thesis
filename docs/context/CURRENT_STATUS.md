# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger; use progressive task-specific reading for detailed decisions/evidence.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine capability validation and `T-200` research framing through completed historical WP6 v1.0 evidence.
- Existing `protocol-v1.0`, finalized `FINAL-*` bundles, R0 pilot evidence and historical thesis-final evidence are immutable baseline evidence.
- `T-511` remains **USER_VALIDATION_REQUIRED**; automated screenshots/package checks do not replace intended-user E2E acceptance.
- **Pre-WP7 approval: NOT APPROVED.** All `T-700+` execution remains blocked.

## Active refinement

- Decisions: DEC-042 scientific refinement; DEC-043 historical/superseded React/Vite exploration; DEC-044 NiceGUI native application; DEC-045 visual analytics; DEC-046 novice-first compact UX; DEC-047 broadened agent comparison and human-readable naming.
- Single branch/PR: `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft #92. No parallel implementation branch or early merge.
- Trackers: #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/packaging.
- Progress: **2/8** major milestones. `T-520` and `T-523` are complete. Current scientific task is **`T-521 READY`**; `T-522` remains blocked on T-521.
- PR CI run **396** validated the broadened agent implementation checkpoint: documentation consistency, committed JSON validation, Python compile, locked environment, complete **143-test** suite including SARSA/Dyna-Q/five-strategy/reference tests, and bibliography integrity.

## Thesis framing

The thesis concerns **resilient AI agent strategies operating under uncertainty and environmental change**. GridWorld is the controlled experimental testbed and visualization environment used to expose mechanisms, disturbances, trajectories and comparisons reproducibly. It is not the thesis subject or the basis for choosing agent families.

## Scientific direction

DEC-047 defines five main candidate strategies:

1. **Fixed Q-Learning** — learned nominal Q-values/policy, no post-change learning; historical technical identity F0.
2. **Adaptive Q-Learning** — continual off-policy Q-learning; historical technical identity C0.
3. **SARSA** — on-policy continual model-free TD control.
4. **Dyna-Q** — online model learning plus planning over experienced state-action transitions, without Dyna-Q+ recency/untried-action bonuses.
5. **Dyna-Q+** — Dyna planning plus directed re-exploration of long-untried actions; historical technical identity D0.

The set isolates no adaptation, off-policy model-free adaptation, on-policy model-free adaptation, learned-model planning, and planning plus explicit change-seeking re-exploration. `T-523` implemented and validated SARSA and plain Dyna-Q with deterministic/serializable state, the same agent-visible information boundary, episode persistence, focused algorithmic tests and five-strategy runner/configuration identities.

**Reference only:** deterministic Random Agent is a lower scale/correctness fixture. A nominal/fully-informed planner may only be a clearly privileged analytical/debug reference. Neither belongs in fair rankings.

**Robust branch:** historical R0 remains negative/diagnostic pilot evidence. A redesigned Robust Planner can become a conditional sixth comparator only if a predeclared non-final nominal-viability/fairness/runtime gate passes; unchanged R0 is not reinstated.

Preserve the validated Fixed/Adaptive Q-Learning base values unless an explicit evidence-backed amendment is made: alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 nominal training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and current target 32 paired final roots.

Five-strategy matrix feasibility is bounded but not yet a runtime claim: 888,832 environment episodes for 4 layouts × 7 conditions × 32 roots versus 315,392 historical v1.0 episodes, about 2.82× before Dyna planning overhead. Real planning cost must be measured on non-final runs before freeze.

## T-521 scope

T-521 now owns the authoritative candidate `protocol-v1.1` definition before any selection evidence is inspected:

- five validated main strategies and stable human-readable/technical configuration identities;
- exact small predeclared SARSA fairness-tuning and Dyna/Dyna-Q+ planning surfaces only where scientifically justified;
- four fresh held-out final layouts and a fresh precommitted final seed bank;
- seven single-factor conditions with structural remap IDs `action-remap-2-swap` and `action-remap-4-cycle`;
- paired effects, 95% confidence intervals, explicit n and layout-aware aggregation;
- primary cumulative deficit, immediate degradation and terminal performance/gap; recovery secondary/sensitivity;
- no best-seed, best-final switching, opaque composite score or post-hoc favorable threshold.

Candidate status never authorizes final evidence. T-522 later uses only predeclared non-final evidence to freeze/amend/reject strategies and settings.

## User-facing naming and application

The primary UI concept is **Agent strategy**. Ordinary users see full names and concise mechanism explanations; F0/C0/D0, schema IDs and configuration hashes are secondary under **Technical details / Reproducibility**. The same full names propagate to Runs, Compare, charts, screenshots and later thesis/presentation-facing exports.

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services.
- Plotly = stored/final scientific figures; ECharts = real live/provisional telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- T-530 supplies truthful active-run DTOs/events/history/resources, capability-based controls and read-only live GridWorld observation.
- T-531 completes Dashboard/New Experiment/Runs/Compare/Artifacts and novice-first explanations.
- T-532 validates screenshots/browser/native Windows/PyInstaller `onedir + windowed`; root `run_app.bat` remains checkout launcher.

After acceptance, approved experiments run directly from the desktop application on the validated thesis machine without Codex/console commands merely to launch a frozen configuration.

## Bibliography and testing baseline

`MariosGiannakaras/ThesisBibliography` remains canonical; accepted immutable thesis-repo import is `bibliography-integration-v3`. New research sources continue through the bibliography repository's canonical intake and are imported only through a later versioned synchronization.

Testing remains risk-based/proportional; PR CI is the canonical full-suite guard. Use progressive reading and targeted checks during implementation rather than coverage expansion.

## Still intentionally unfrozen

Exact T-521 tuning/fairness surfaces, candidate-v1.1 schema/fresh layouts/seeds/statistical implementation, T-522 retained strategy/settings outcome, conditional Robust Planner decision, actual Dyna planning runtime, new final evidence, active-run runtime behavior, final novice-first UI/screenshots/native package, current official WP7 formatting/defense rules and final thesis/presentation deliverables remain unfrozen until their explicit gates pass.

## Exact next action

Execute **T-521** as one bounded scientific scope. Define and implement the authoritative five-strategy candidate `protocol-v1.1`, predeclared bounded settings/fairness rules, fresh held-out layouts/seeds, configuration identity/provenance and paired statistical support. Do not inspect/generate final-v1.1 outcomes and do not start any `T-700+` task.