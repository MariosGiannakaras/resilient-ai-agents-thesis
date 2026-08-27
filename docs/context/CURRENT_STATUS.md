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
- Progress: **2/8** major milestones. `T-520`, `T-523` and **`T-521` are complete**. Current scientific task is **`T-522 READY`**.
- PR CI run **409** validated the T-521 checkpoint: documentation consistency, committed JSON validation, Python compilation, locked environment, complete tests including candidate protocol/configuration runner/fresh-reserve/paired-statistics checks, and bibliography integrity.
- Upstream `ThesisBibliography` now contains the strengthened agent-strategy theory package: Watkins–Dayan Q-learning, Sutton Dyna, Khetarpal continual RL and Padakandla dynamically varying RL are source-analysed/citation-ready; Rummery–Niranjan is retained conservatively as historical-lineage metadata where reliable complete-text verification was unavailable.

## Thesis framing

The thesis concerns **resilient AI agent strategies operating under uncertainty and environmental change**. GridWorld is the controlled experimental testbed and visualization environment used to expose mechanisms, disturbances, trajectories and comparisons reproducibly. It is not the thesis subject or the basis for choosing agent families.

## Scientific direction

DEC-047 defines five main candidate strategies:

1. **Fixed Q-Learning** — learned nominal Q-values/policy, no post-change learning; historical technical identity F0.
2. **Adaptive Q-Learning** — continual off-policy Q-learning; historical technical identity C0.
3. **SARSA** — on-policy continual model-free TD control.
4. **Dyna-Q** — online model learning plus planning over experienced state-action transitions, without Dyna-Q+ recency/untried-action bonuses.
5. **Dyna-Q+** — Dyna planning plus directed re-exploration of long-untried actions; historical technical identity D0.

**Reference only:** deterministic Random Agent is a lower scale/correctness fixture. A nominal/fully-informed planner may only be a clearly privileged analytical/debug reference. Neither belongs in fair rankings.

**Robust branch:** historical R0 remains negative/diagnostic pilot evidence. A redesigned Robust Planner can become a conditional sixth comparator only if a predeclared non-final nominal-viability/fairness/runtime gate passes; unchanged R0 is not reinstated.

## Completed T-521 candidate protocol

The checked-in `configs/protocols/protocol-v1.1.json` is an explicit **candidate**, not a frozen/final protocol. Its separate fail-closed `V11CandidateProtocol` loader preserves historical `PilotProtocol` semantics and blocks pilot/final execution.

T-521 now provides:

- the five validated main strategies with user-facing names and stable technical identities;
- preserved validated Q baseline: alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 nominal training episodes/layout;
- bounded non-final configuration catalog: two SARSA alpha candidates, two Dyna-Q planning budgets, four Dyna-Q+ planning/kappa combinations; F0/C0 remain fixed baselines;
- four structurally controlled fresh held-out v1.1 final layouts and a fresh precommitted 32-root final bank, disjoint from development/tuning and historical tuning/final reserves;
- seven single-factor conditions using structural remap IDs `action-remap-2-swap` and `action-remap-4-cycle`;
- stable per-configuration and protocol SHA-256 provenance in the candidate runner;
- tuning restricted to the complete predeclared root bank and nominal + two persistent-remap conditions, with no single-run/best-seed selection;
- primary cumulative deficit, immediate degradation and terminal performance; recovery remains secondary/sensitivity and no composite resilience score exists;
- predeclared mechanistic paired contrasts with equal-weight layout aggregation inside each root and deterministic 95% percentile-bootstrap CIs over root-level effects (10,000 resamples, fixed analysis seed);
- explicit final-outcome access block until T-522 freeze plus later application/user gates.

Candidate status **does not authorize final evidence**.

## T-522 scope

`T-522` may use only predeclared **non-final** development/tuning evidence to select/freeze/amend/reject candidate configurations. It must:

- compare complete repeated/paired configuration evidence rather than single runs or best seeds;
- retain failed/interrupted/poor/non-recovery outcomes transparently;
- measure Dyna planning update counts, wall time and artifact/runtime cost on the validated thesis machine before freeze;
- decide SARSA and Dyna/Dyna-Q+ retained configuration identities using the predeclared deterministic selection/tie rules;
- evaluate a redesigned Robust Planner only through its separate bounded gate if that gate is actually implemented and scientifically worthwhile; otherwise retain historical R0 as negative evidence only;
- inspect no v1.1 final-layout/final-seed outcomes;
- produce an explicit freeze/amend/reject record before any final-v1.1 execution can become possible.

If T-522 requires execution on the unavailable physical thesis machine in the current remote session, record that external execution boundary and continue the next dependency-valid repository task (`T-530`) rather than fabricating or moving the scientific runs into CI.

## User-facing naming and application

The primary UI concept is **Agent strategy**. Ordinary users see full names and concise mechanism explanations; F0/C0/D0, schema IDs and configuration hashes are secondary under **Technical details / Reproducibility**. The same full names propagate to Runs, Compare, charts, screenshots and later thesis/presentation-facing exports.

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services.
- Plotly = stored/final scientific figures; ECharts = real live/provisional telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- T-530 supplies truthful active-run DTOs/events/history/resources, capability-based controls and read-only live GridWorld observation.
- T-531 completes Dashboard/New Experiment/Runs/Compare/Artifacts and novice-first explanations.
- T-532 validates screenshots/browser/native Windows/PyInstaller `onedir + windowed`; root `run_app.bat` remains checkout launcher.

After acceptance, approved experiments run directly from the desktop application on the validated thesis machine without Codex/console commands merely to launch a frozen configuration.

## Bibliography and testing baseline

`MariosGiannakaras/ThesisBibliography` remains canonical. The upstream theory package has been strengthened and verified; it must enter the thesis repository only through the established versioned bibliography synchronization workflow, never by hand-copying formal citation evidence.

Testing remains risk-based/proportional; PR CI is the canonical full-suite guard. Experiment matrices are scientific work, not CI test matrices.

## Still intentionally unfrozen

T-522 retained strategy/settings outcomes, conditional Robust Planner decision, measured Dyna planning runtime, frozen v1.1 protocol, new final evidence, active-run runtime behavior, final novice-first UI/screenshots/native package, current official WP7 formatting/defense rules and final thesis/presentation deliverables remain unfrozen until their explicit gates pass.

## Exact next action

Execute **T-522** only on predeclared non-final evidence. If the validated thesis-machine execution required for that gate is unavailable in this session, do not substitute GitHub-hosted CI; record the blocker and proceed with dependency-valid **T-530** runtime-service implementation on the same branch/PR. Do not inspect/generate final-v1.1 outcomes and do not start any `T-700+` task.