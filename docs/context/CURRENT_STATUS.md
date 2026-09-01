# Current Project Status

**Date:** 2026-09-01  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Read task-specific decision/research documents **progressively**. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, historical application baseline `T-528`, `T-529`, historical `T-530`, `T-531`, `T-532`, historical intended-user acceptance `T-511`, `T-533`, and `T-534` are COMPLETE.
- `T-534` remains **COMPLETE**. PR #107 was squash-merged into `main` as `c372c581b88c63f3b07c96bd50bbc17b9b83f835` after exact-head Repository checks #864 and T-534 PySide6 UI acceptance #174 passed, deterministic 1366×768/1440×900 renders were visually reviewed, and the merged `main` was verified to contain the accepted experiment-first implementation.
- `T-535` is **IN_PROGRESS** on issue #109 / PR #110. It is a bounded pre-T610 intended-user UX/workflow hardening package discovered by a post-T-534 workflow and exact-head screenshot review; it does not reopen or invalidate T-534.
- `T-535` scope is presentation-only: created-record context propagation, RQ-local direct-comparison placement, progressive Results provenance/comparison detail, actionable Run/Evidence states, and task-agnostic final-gate copy. It does not modify the Study backend, scientific estimands, analysis outputs or protocol-v2.1 authority.
- DEC-061 remains the accepted product/UX authority: it preserves DEC-059's PySide6/runtime boundary and defines the experiment-first **Experiment / Run / Results / Evidence** application model.
- `T-610` remains a separate **BLOCKED** scientific task. T-535 must complete first, and `final_reserve_access=false` plus `execution_authorization=requires-explicit-t610-gate` remain mandatory until a separate explicit final-scientific-experiment authorization is granted.
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

DEC-059 selects PySide6 / Qt 6 Widgets over the framework-neutral Study backend. `T-528` and `T-511` remain historical completed application/acceptance records; their presentation is not the implementation authority for T-534/T-535.

T-534 is complete on `main` through squash merge commit `c372c581b88c63f3b07c96bd50bbc17b9b83f835`. The accepted application implements DEC-061 and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md` as the experiment-first **Experiment / Run / Results / Evidence** workflow. The active UI projects protocol-v2.1 fail-closed; the final Thesis experiment is immutable with all five methods; DEVELOPMENT uses backend-constrained Configure → Review → Create; Run uses truthful durable method status plus presentation-only GridWorld frames; Phase B requires exact method/root/layout/condition/interaction FD/AD pairing; Results remain RQ1/RQ2/RQ3 projections of stored validated outputs; Evidence leads with readiness and exposes backend-registered lineage on demand.

T-535 hardens the intended-user transitions without changing those accepted scientific/application invariants. The active PR makes the newly created DEVELOPMENT record the selected Run context, propagates compatible context to Results/Evidence, warns when the current run has no stored analysis instead of silently implying an older package is current, uses `Experiment record` terminology, keeps Phase-A/Phase-B/recovery direct comparisons within RQ1/RQ2/RQ3 respectively, hides Results provenance/comparison detail behind disclosure, hides unavailable infrastructure retry, and makes Evidence next actions operational.

The deterministic T-534 review set remains the regression visual baseline for 1366×768 and 1440×900 Experiment, DEVELOPMENT review, Phase-A GridWorld, exact Phase-B Frozen/Adaptive pairing, RQ1, RQ2, recovered/right-censored RQ3, Evidence readiness/technical lineage and onboarding/final-gate states. T-535 must rerun and visually review that exact-head render workflow before merge. Fixtures remain DEVELOPMENT/synthetic only; no scientific jobs, environment steps or final-reserve access are permitted for UI QA.

## Repository integration / provenance

PR #92 is historical and was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`; there is no remaining PR #92 integration step. PR #103 subsequently merged DEC-061 and the experiment-first T-534 UI specification into `main` as `f960991c3ba71130178946fbc8051875b9fecac6`.

PR #107 was the single coherent T-534 implementation PR and was squash-merged into `main` as `c372c581b88c63f3b07c96bd50bbc17b9b83f835`. Its exact head `0fff019d8bd1b90bd1809f2c2f5b0c0662d743da` passed Repository checks #864 and T-534 PySide6 UI acceptance #174 before merge. Merged-state verification confirmed the accepted protocol-v2.1 four-surface application on `main`.

PR #110 / `feat/t-535-intended-user-ux-hardening` is the current bounded presentation/workflow hardening branch from `main`; issue #109 is its operational tracking view. T-535 must be merged and verified before the project returns to the separate T-610 authorization gate.

Only deliberate provenance archive refs remain alongside `main`; they are not active implementation branches and must not be merged merely to reduce branch count.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system exists.

## Still intentionally unfrozen

- Final-reserve **execution authorization** remains withheld even though the protocol recipe is frozen.
- `T-535` is the only active pre-T610 application hardening package.
- `T-610` remains BLOCKED by T-535 completion plus the separate explicit scientific authorization gate.
- `T-611`/`T-612`/`T-613` remain blocked downstream of `T-610`.
- WP7 remains blocked by final evidence plus later explicit pre-WP7 user approval.
- Final standalone Windows packaging remains deferred to `T-803` / issue #94.

## Exact next action

Complete T-535 through focused tests, exact-head Repository checks and PySide6 render CI, deterministic 1366×768/1440×900 screenshot review, canonical reconciliation, squash merge and merged-main verification. Then stop at the separate `T-610` scientific authorization gate. Do not access final roots/layouts/seeds, execute the protocol-v2.1 final matrix, inspect final outcomes, or begin Results/Discussion unless the user separately and explicitly authorizes the final scientific experiment.