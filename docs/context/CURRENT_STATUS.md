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
- Master progress: **5/8** milestones complete (#87 milestones 1, 2, 4, 5 and 6).
- Completed refinement tasks: `T-520`, `T-523`, `T-521`, `T-530`, `T-531`.
- Current repository task: **`T-532 READY`**.
- External scientific gate: **`T-522 READY` only on the validated thesis machine**; hosted CI is not a substitute.
- Trackers: #87 master 5/8; #88 scientific 9/12; #89 runtime 6/6 complete/closed; #90 UI 8/9; #91 screenshots/CI/packaging 0/6 active next.
- PR #92's current-head CI is the canonical full-suite guard and must be inspected live; historical run 425 remains only the completed T-530 checkpoint.

## Thesis framing and scientific direction

The thesis concerns **resilient AI agent strategies operating under uncertainty and environmental change**. GridWorld is the controlled experimental testbed and visualization environment, not the thesis subject.

Main candidate strategies:

1. **Fixed Q-Learning** — learned nominal Q-values/policy, no post-change learning.
2. **Adaptive Q-Learning** — continual off-policy Q-learning.
3. **SARSA** — on-policy continual model-free TD control.
4. **Dyna-Q** — online model learning plus planning over experienced state-action transitions.
5. **Dyna-Q+** — Dyna planning plus directed re-exploration of long-untried actions.

Random Agent and any nominal/fully-informed planner are reference-only. Historical R0 remains negative/diagnostic pilot evidence; a redesigned Robust Planner is conditional on the predeclared non-final gate.

## Completed candidate protocol / statistics

`configs/protocols/protocol-v1.1.json` remains an explicit **candidate**, not a frozen/final protocol. T-521 provides the five strategies, preserved Q baseline (`alpha=.5`, `gamma=.96875`, `epsilon=.125`, 512 training episodes/layout), bounded SARSA/Dyna settings, four fresh held-out layouts, fresh/disjoint seed banks, seven structural single-factor conditions, stable configuration/protocol SHA-256 provenance, and fail-closed final access.

Primary metrics are cumulative deficit, immediate degradation and terminal performance. Recovery remains secondary/sensitivity. `v11_statistics.py` implements predeclared root-blocked paired effects with equal layout weighting and deterministic 95% percentile-bootstrap CIs. No composite resilience score or post-hoc favorable threshold is allowed.

## T-522 external scientific gate

T-522 may use only the complete predeclared **non-final** development/tuning evidence on the validated thesis machine. It must retain failures/poor outcomes, measure Dyna planning runtime/cost, apply predeclared selection/tie rules, resolve the optional Robust Planner gate, and freeze/amend/reject retained configuration IDs before any v1.1 final reserve access.

This remote GitHub-connected session does not substitute hosted runners for that physical-machine evidence.

## Completed T-530 runtime service

T-530 is complete and tracker #89 is closed 6/6.

- `RuntimeService` is UI-independent and exposes schema-v1 queued/running/completed/failed/cancelled/interrupted snapshots.
- Persisted runtime metadata is separate from scientific run bundles.
- Heartbeat derives from real telemetry activity; progress uses persisted root completion plus latest real phase/episode/step.
- Candidate requests are validated against the protocol before queue creation.
- Runtime execution uses only the owned candidate entrypoint; arbitrary shell commands are not exposed.
- Cancel/restart are capability-based; pause/resume are explicitly unsupported.
- Historical unfinished runs remain visible without being falsely restartable; finalized scientific status remains authoritative.
- Live GridWorld telemetry is evaluator-side operational/provisional data, separate from scientific retention.
- Observer ON versus OFF is regression-tested to produce identical scientific root results.
- Canonical resource snapshots and live telemetry tailing are exposed for NiceGUI.

## Completed T-531 application

NiceGUI 3.16 native/pywebview remains the single active frontend over the UI-independent Python runtime/scientific services.

T-531 now provides:

- Dashboard with real recent/active run status, resources and navigation;
- New Experiment with human-readable **Agent strategy** selection, approved configuration variants, repetitions/root seeds, bounded settings/sweeps, fixed-vs-tunable explanations and resolved-config review;
- Runs with active/history/detail, real lifecycle/progress/events/logs and smooth read-only live GridWorld driven only by runtime telemetry;
- Compare with compatible agent/configuration comparisons, distributions, paired CIs/counts and layout/condition views;
- Artifacts with real CSV/JSON/HTML/provenance preview/export;
- Plotly for stored/final scientific figures, ECharts for live/provisional telemetry, Mermaid for explanations and AG Grid Community for analytical tables;
- novice-first compact UX: plain labels, accurate tooltips/help, units/consequences, progressive disclosure, semantic text+icon+color status and actionable invalid/empty/loading/error/disabled states;
- no fake progress, fabricated metrics/logs or synthesized historical trajectory replay.

Focused application tests validate bounded protocol/configuration choices, plain-language identities/settings, truthful no-trace history, exact stored artifact reads and live telemetry parsing. Browser-mode rendering of all five routes and a tall Compare visual pass confirmed the compact layout; Plotly title/legend and Artifact-index clipping found during that pass were corrected. Issue #90 is 8/9 because its remaining native-window/onedir packaging item is the T-532 boundary.

Technical IDs (`F0/C0/D0`, schema/config hashes) belong under **Technical details / Reproducibility**, not ordinary strategy names.

## Bibliography and testing baseline

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable thesis-repository import remains **`bibliography-integration-v3`**. Newer upstream theory records enter only through a later versioned synchronization; do not hand-copy formal citation evidence.

Testing remains risk-based/proportional; PR CI is the canonical full-suite guard. Scientific experiment matrices are not CI tests.

## Still intentionally unfrozen

T-522 retained settings, optional Robust Planner decision, measured thesis-machine planning runtime, frozen v1.1 protocol, new final evidence, accepted screenshots/native package, intended-user validation, current official WP7 rules and final thesis/presentation deliverables remain unfrozen until their explicit gates pass.

## Exact next action

Continue **T-532** on the existing branch/PR: create accepted root screenshots, add bounded deterministic NiceGUI browser/CI capture, and validate actual Windows native-window plus `onedir + windowed` delivery behavior and safe writable paths. Keep T-522 reserved for the validated thesis machine. Do not inspect/generate final-v1.1 outcomes and do not start `T-700+`.
