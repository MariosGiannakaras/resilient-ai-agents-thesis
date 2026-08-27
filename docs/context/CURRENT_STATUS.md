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
- Upstream `ThesisBibliography` now contains strengthened agent-strategy theory: Watkins–Dayan Q-learning, Sutton Dyna, Khetarpal continual RL and Padakandla dynamically varying RL are source-analysed/citation-ready; Rummery–Niranjan is retained conservatively as historical-lineage metadata where reliable complete-text verification was unavailable.

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

T-521 provides:

- five validated strategies with user-facing names and stable technical identities;
- preserved Q baseline: alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 nominal training episodes/layout;
- bounded non-final catalog: two SARSA alpha candidates, two Dyna-Q planning budgets, four Dyna-Q+ planning/kappa combinations;
- four fresh held-out layouts and a fresh 32-root final bank, disjoint from development/tuning and historical reserves;
- seven single-factor conditions with `action-remap-2-swap` and `action-remap-4-cycle`;
- stable configuration/protocol SHA-256 provenance;
- tuning restricted to the full predeclared tuning root bank and nominal + two persistent-remap conditions, with no best-seed/single-run selection;
- primary cumulative deficit, immediate degradation and terminal performance; recovery secondary/sensitivity; no composite score;
- predeclared paired contrasts with equal-weight layout aggregation inside roots and deterministic 95% percentile-bootstrap CIs over root effects (10,000 resamples, fixed seed);
- explicit final-outcome access block until T-522 freeze plus later application/user gates.

Candidate status **does not authorize final evidence**.

## T-522 scope

`T-522` may use only predeclared **non-final** development/tuning evidence to select/freeze/amend/reject candidate configurations. It must compare complete repeated/paired evidence, retain failures/poor/non-recovery outcomes, measure Dyna planning cost on the validated thesis machine, apply the predeclared deterministic selection/tie rules, and inspect no v1.1 final-layout/final-seed outcomes.

If the physical thesis machine is unavailable in the current remote session, record that external execution boundary and continue dependency-valid `T-530`; do not move the scientific matrix into GitHub-hosted CI.

## User-facing naming and application

The primary UI concept is **Agent strategy**. Ordinary users see full names and concise mechanism explanations; F0/C0/D0, schema IDs and configuration hashes are secondary under **Technical details / Reproducibility**.

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services.
- Plotly = stored/final scientific figures; ECharts = real live/provisional telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- T-530 supplies truthful active-run DTOs/events/history/resources, controls and read-only live GridWorld observation.
- T-531 completes Dashboard/New Experiment/Runs/Compare/Artifacts and novice-first explanations.
- T-532 validates screenshots/browser/native Windows/PyInstaller `onedir + windowed`; root `run_app.bat` remains checkout launcher.

After acceptance, approved experiments run directly from the desktop application on the validated thesis machine without Codex/console commands merely to launch a frozen configuration.

## Bibliography and testing baseline

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable thesis-repository import remains **`bibliography-integration-v3`**. The newer upstream theory package must enter this repository only through the established later versioned bibliography synchronization workflow; never hand-copy formal citation evidence.

Testing remains risk-based/proportional; PR CI is the canonical full-suite guard. Experiment matrices are scientific work, not CI test matrices.

## Still intentionally unfrozen

T-522 retained settings, conditional Robust Planner decision, measured Dyna planning runtime, frozen v1.1 protocol, new final evidence, active-run runtime behavior, final novice-first UI/screenshots/native package, current official WP7 rules and final thesis/presentation deliverables remain unfrozen until their explicit gates pass.

## Exact next action

Execute **T-522** only on predeclared non-final evidence. If validated thesis-machine execution is unavailable, do not substitute GitHub-hosted CI; record the blocker and proceed with dependency-valid **T-530** on the same branch/PR. Do not inspect/generate final-v1.1 outcomes and do not start `T-700+`.