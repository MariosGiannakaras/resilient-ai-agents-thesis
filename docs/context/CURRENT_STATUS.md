# Current Project Status

**Date:** 2026-09-02  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Read task-specific decision/research documents **progressively**. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, historical application baseline `T-528`, `T-529`, historical `T-530`, `T-531`, `T-532`, historical intended-user acceptance `T-511`, `T-533`, `T-534`, and `T-535` are COMPLETE.
- `T-534` remains **COMPLETE**. PR #107 was squash-merged into `main` as `c372c581b88c63f3b07c96bd50bbc17b9b83f835` after exact-head Repository checks #864 and T-534 PySide6 UI acceptance #174 passed, deterministic 1366×768/1440×900 renders were visually reviewed, and the merged `main` was verified to contain the accepted experiment-first implementation.
- `T-535` remains **COMPLETE**. PR #110 was squash-merged into `main` as `225df138c5c5be0c39c9e474ef7fdbce6b11245b` after exact head `710f7f4290b07dba682db2f1c548d19ec43c1876` passed Repository checks #872 and PySide6 UI acceptance #179, and merged-state verification confirmed the intended-user hardening on `main`.
- `T-536` is **IN_PROGRESS** on issue #112 / PR #113. It is the final bounded visual-polish/richer-result-visualization package requested after T-535; it does not reopen or invalidate the accepted T-534/T-535 workflow.
- T-536 preserves the **Experiment / Run / Results / Evidence** information architecture, the five immutable Thesis methods, simultaneous exact Frozen/Adaptive Phase-B presentation, Study/read-model authority and protocol-v2.1 scientific semantics. It adds presentation geometry/hierarchy only: larger GridWorld emphasis, explicit current-method/five-method lifecycle orientation, larger RQ1/RQ2 charts, stored-evidence RQ3 trajectory visualization and less sparse DEVELOPMENT/Evidence presentation.
- `docs/research/T-613_THESIS_FIGURE_INVENTORY.md` now defines the downstream T-613 figure/table contract: a rich reproducible main-thesis + appendix + defense asset package generated from validated stored final outputs, not quantitative screenshots of the application.
- `T-610` remains a separate **BLOCKED** scientific task. T-536 must complete first; afterward `final_reserve_access=false` plus `execution_authorization=requires-explicit-t610-gate` remain mandatory until a separate explicit final-scientific-experiment authorization is granted.
- Master tracker #87 remains **7/8** complete. Milestone 8 awaits the final v2.1 evidence chain.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution or Results/Discussion writing.

## Scientific authority

DEC-058 and `configs/protocols/protocol-v2.0-final.json` remain immutable historical protocol-v2.0 freeze authority. DEC-060 is the explicit pre-outcome amendment. `configs/protocols/protocol-v2.1-final.json` is the current self-contained pre-execution scientific authority.

The frozen design remains unchanged:

- methods: Q-Learning, SARSA, DQN, PPO, Dyna-Q+;
- common actual-environment-interaction fairness budget and information/reward/gamma semantics;
- Phase-A independent learning and exact checkpoints;
- Phase-B matched FN/FD/AN/AD branches;
- 12 final roots, 2 held-out final layouts, four Phase-B conditions, 256-interaction horizon;
- RQ2 primary adaptation benefit `(FN-FD)-(AN-AD)`;
- RQ3 AN-vs-AD passive 32-interaction windows, primary tolerance 0.10, sensitivity 0.05/0.20, two-window stable recovery and right-censoring with `recovery_time=null`;
- root as independent statistical unit, direct root-paired method contrasts after equal layout reduction, and pointwise Student-t intervals using the predeclared actual-root-count critical value;
- no outcome-driven seed/root replacement and no formal p-value superiority family.

No protocol-v2.1 final-reserve outcome has been generated, inspected or used.

## Completed pre-final implementation/readiness

The current Study/backend/evidence chain is implemented and validated:

`Study recipe/plan -> Phase A -> exact checkpoint -> FN/FD/AN/AD -> passive temporal evidence -> validation -> root reduction -> RQ1/RQ2/RQ3 analysis -> recovery/direct contrasts -> deterministic exports -> stored-evidence application read model`.

Pre-final scientific readiness includes deny-by-default final execution in `StudyService`, read-only final preflight, DEVELOPMENT-only synthetic end-to-end smoke, `docs/research/RQ_EVIDENCE_TRACEABILITY.md`, and focused protocol-v2.1 CI coverage. None of these authorize `T-610`.

## Application state

DEC-059 selects PySide6 / Qt 6 Widgets over the framework-neutral Study backend. `T-528` and `T-511` remain historical completed application/acceptance records; their presentation is not the implementation authority for T-534/T-535/T-536.

T-534 is complete on `main` through squash merge commit `c372c581b88c63f3b07c96bd50bbc17b9b83f835`. The accepted application implements DEC-061 and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md` as the experiment-first **Experiment / Run / Results / Evidence** workflow. The active UI projects protocol-v2.1 fail-closed; the final Thesis experiment is immutable with all five methods; DEVELOPMENT uses backend-constrained Configure → Review → Create; Run uses truthful durable method status plus presentation-only GridWorld frames; Phase B requires exact method/root/layout/condition/interaction FD/AD pairing; Results remain RQ1/RQ2/RQ3 projections of stored validated outputs; Evidence leads with readiness and exposes backend-registered lineage on demand.

T-535 completed the intended-user hardening without changing those accepted scientific/application invariants. Newly created DEVELOPMENT records become the selected Run context; compatible context propagates to Results/Evidence; Results explicitly warn when the current run has no stored analysis instead of silently implying an older package is current; primary terminology is `Experiment record`; Phase-A/Phase-B/recovery direct comparisons remain inside RQ1/RQ2/RQ3 respectively; Results provenance/comparison detail is progressively disclosed; unavailable infrastructure retry is hidden; Evidence next actions name the operational surface/action; final-gate wording is task-agnostic while authorization remains backend-owned.

T-536 is a presentation-only successor polish pass. Run keeps simultaneous Frozen/Adaptive comparison and uses durable method lifecycle state plus live-frame method identity only for orientation; it does not rank methods or alter execution. RQ3 reads already-stored per-root directed-gap trajectories, stored tolerance/window/horizon values and stored method/condition recovery summaries. The chart performs only visual scaling/positioning; recovery classification, right-censoring, root reduction, thresholds, intervals and estimands remain backend-owned.

The first T-536 exact head passed Repository checks #876 and PySide6 UI acceptance #180, and visual inspection identified one 1366×768 Run height regression despite green CI. That regression is being corrected before final acceptance by compacting current-method/status presentation rather than reducing scientific content or relaxing screenshot criteria. Final exact-head CI and renders remain required before merge.

## Thesis/defense result assets

T-613 remains the canonical final figure/table/export task after T-612. Its pre-execution contract is `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`, which specifies 30 figure/asset categories plus thesis tables and provenance across RQ1 learning, RQ2 resilience/adaptation, RQ3 recovery, methodology/evidence lineage and defense variants. T-613 must generate deterministic vector-first `SVG`/`PDF`, high-resolution `PNG` and machine-readable table outputs from validated stored final evidence, with source artifact IDs/hashes and generator provenance. Application screenshots remain illustrative workflow assets rather than quantitative sources for thesis claims.

## Repository integration / provenance

PR #92 is historical and was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`; there is no remaining PR #92 integration step. PR #103 subsequently merged DEC-061 and the experiment-first T-534 UI specification into `main` as `f960991c3ba71130178946fbc8051875b9fecac6`.

PR #107 was the single coherent T-534 implementation PR and was squash-merged into `main` as `c372c581b88c63f3b07c96bd50bbc17b9b83f835`. Its exact head `0fff019d8bd1b90bd1809f2c2f5b0c0662d743da` passed Repository checks #864 and T-534 PySide6 UI acceptance #174 before merge. Merged-state verification confirmed the accepted protocol-v2.1 four-surface application on `main`.

PR #110 / `feat/t-535-intended-user-ux-hardening` was squash-merged into `main` as `225df138c5c5be0c39c9e474ef7fdbce6b11245b`. Its exact head `710f7f4290b07dba682db2f1c548d19ec43c1876` passed Repository checks #872 and PySide6 UI acceptance #179; deterministic artifact `9818821831` was reviewed before merge. Merged-state verification confirmed the accepted T-535 presentation/workflow hardening on `main`.

PR #113 / `feat/t-536-final-visual-polish` is the active final visual-polish/richer-results branch. Issue #112 is its operational checklist; canonical repository science and execution authorization remain unchanged.

Only deliberate provenance archive refs remain alongside `main`; they are not active implementation branches and must not be merged merely to reduce branch count.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system exists.

## Still intentionally unfrozen

- Final-reserve **execution authorization** remains withheld even though the protocol recipe is frozen.
- `T-536` is the only active pre-T610 application/presentation package.
- `T-610` remains BLOCKED by T-536 completion plus the separate explicit scientific authorization gate.
- `T-611`/`T-612`/`T-613` remain blocked downstream of `T-610`.
- WP7 remains blocked by final evidence plus later explicit pre-WP7 user approval.
- Final standalone Windows packaging remains deferred to `T-803` / issue #94.

## Exact next action

Complete T-536 through focused tests, exact-head Repository checks and PySide6 render CI, deterministic 1366×768/1440×900 screenshot review, canonical reconciliation, squash merge and merged-main verification. Then stop at the separate `T-610` scientific authorization gate. Do not access final roots/layouts/seeds, execute the protocol-v2.1 final matrix, inspect final outcomes, or begin Results/Discussion unless the user separately and explicitly authorizes the final scientific experiment.