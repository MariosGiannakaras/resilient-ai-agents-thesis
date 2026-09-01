# Current Project Status

**Date:** 2026-09-02  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Read task-specific decision/research documents progressively. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target-machine validation and `T-200` research framing are complete.
- Protocol-v1.0 / FINAL-* / R0 evidence remain immutable history; superseded `T-522` must not execute.
- Scientific/pre-final implementation through `T-533` is complete. `T-534` experiment-first PySide6 rebuild and `T-535` intended-user workflow hardening are COMPLETE and remain historical accepted records.
- `T-536` is **IN_PROGRESS** on issue #112 / PR #113. It is the final bounded UI/UX visual-polish and richer in-app result-visualization package; it does not reopen T-534/T-535 or amend science.
- T-536 preserves **Experiment / Run / Results / Evidence**, the five immutable Thesis methods and simultaneous exact Frozen/Adaptive Phase-B presentation. It changes presentation geometry/hierarchy only: larger GridWorld emphasis, current-method/five-method lifecycle orientation, larger RQ1/RQ2 charts, stored-evidence RQ3 trajectory visualization and denser use of DEVELOPMENT/Evidence space.
- `docs/research/T-613_THESIS_FIGURE_INVENTORY.md` is the pre-execution downstream T-613 output contract: a broad reproducible main-thesis + appendix + defense figure/table package generated from validated stored final outputs, not quantitative UI screenshots.
- `T-610` remains **BLOCKED**. T-536 must complete first; afterward a separate explicit final-scientific-experiment authorization is still mandatory. `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain unchanged.
- Master tracker #87 remains **7/8**; milestone 8 awaits the final v2.1 evidence chain.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution or Results/Discussion writing.

## Scientific authority

DEC-058 / protocol-v2.0 remain immutable historical freeze authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` are the current pre-execution scientific authority.

Frozen protocol-v2.1 remains unchanged: Q-Learning, SARSA, DQN, PPO and Dyna-Q+; common actual-interaction fairness; Phase-A independent learning/exact checkpoints; matched FN/FD/AN/AD Phase B; 12 roots, 2 held-out layouts, four conditions and 256-interaction horizon; RQ2 adaptation benefit `(FN-FD)-(AN-AD)`; RQ3 passive 32-interaction windows, tolerance 0.10 with 0.05/0.20 sensitivity, two-window stability and `recovery_time=null` right-censoring; root as independent unit; declared root-paired direct method contrasts and Student-t intervals. No protocol-v2.1 final-reserve outcome has been generated, inspected or used.

## Pre-final backend/application readiness

The validated backend chain remains:

`Study recipe/plan -> Phase A -> exact checkpoint -> FN/FD/AN/AD -> temporal evidence -> validation -> root reduction -> RQ1/RQ2/RQ3 analysis -> recovery/direct contrasts -> deterministic exports -> stored-evidence application read model`.

Deny-by-default final execution, read-only preflight, DEVELOPMENT synthetic smoke and RQ evidence traceability are complete. None authorize T-610.

The accepted PySide6 application remains experiment-first. T-535 already guarantees created-record selection, Run→Results/Evidence context propagation, `Experiment record` terminology, RQ-local direct comparisons, progressive provenance disclosure, truthful retry states and actionable Evidence next steps.

T-536 adds presentation only. Run orientation uses durable method lifecycle state and live-frame method identity, never a score/ranking. RQ3 reads already-stored per-root directed-gap trajectories, stored tolerance/window/horizon and stored recovery summaries; the UI performs visual scaling only and does not reduce roots, derive thresholds, classify recovery, replace right-censoring or recompute estimands/intervals.

The first T-536 candidate passed Repository checks #876 and UI acceptance #180, but visual review found a 1366×768 Run height regression despite green CI. The branch was corrected by compacting method orientation so larger GridWorlds do not clip. Exact-final-head CI and renders remain required before merge.

## Thesis/defense result assets

`T-613` remains BLOCKED behind T-612. Its new inventory specifies 30 figure/asset categories plus tables across RQ1 learning, RQ2 resilience/adaptation, RQ3 recovery, methodology/evidence lineage and defense variants. T-613 must produce deterministic vector-first SVG/PDF, high-resolution PNG and machine-readable tables with source artifact IDs/hashes and generator provenance. Non-recovery must remain right-censored; application screenshots are illustrative workflow assets only.

## Repository integration / provenance

- PR #107 / T-534 merged as `c372c581b88c63f3b07c96bd50bbc17b9b83f835` after Repository checks #864 and UI acceptance #174.
- PR #110 / T-535 merged as `225df138c5c5be0c39c9e474ef7fdbce6b11245b` after Repository checks #872 and UI acceptance #179; merged-state verification completed.
- Post-T-535 canonical reconciliation is on `main` as `3cc4728aee0e3ca4efe6dd86b6b7ce6b58e05100`.
- PR #113 / `feat/t-536-final-visual-polish` is the active package; #112 is its operational checklist.
- Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`; `bibliography-integration-v3` is immutable historical terminology, not a parallel system.

## Still intentionally unfrozen

- Final-reserve execution authorization remains withheld.
- T-536 is the only active pre-T610 presentation package.
- T-610 remains blocked by T-536 completion plus separate explicit authorization; T-611/T-612/T-613 remain downstream blocked.
- WP7 remains blocked by final evidence plus later explicit pre-WP7 approval.
- Standalone Windows packaging remains deferred to T-803 / issue #94.

## Exact next action

Complete T-536 through focused tests, exact-head Repository checks and PySide6 render CI, deterministic 1366×768/1440×900 visual review, canonical reconciliation, squash merge and merged-main verification. Then stop at the separate T-610 scientific authorization gate. Do not access final roots/layouts/seeds, execute the final matrix, inspect final outcomes, or begin Results/Discussion without separate explicit authorization.