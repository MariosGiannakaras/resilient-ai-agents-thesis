# Current Project Status

**Date:** 2026-09-01  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Read task-specific decision/research documents **progressively**. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, historical application baseline `T-528`, `T-529`, historical `T-530`, `T-531`, `T-532`, historical intended-user acceptance `T-511`, and `T-533` are COMPLETE.
- `T-534` is **IN_PROGRESS / pre-merge reconciliation** on PR #107 (`feat/t-534-experiment-first-ui`), created from the then-current `main` and still zero commits behind current `main`. The experiment-first implementation, targeted validation and deterministic laptop/desktop render review are objectively accepted; merge/post-merge verification remains.
- **GitHub issue #104 is the operational implementation/acceptance checklist for T-534.** It is deliberately detailed so a short instruction such as “start the UI” does not require inventing product behavior. It is a tracking/execution view, not a competing authority; canonical repository decisions/configs/docs win if any wording diverges.
- **T-534 execution cadence:** implement the largest safe coherent batches, use targeted deterministic checks during development, avoid CI for every small edit/checklist item, and require full repository CI at meaningful checkpoints plus one final exact-head pre-merge pass. Reconcile issue #104 from objective implementation/test/render evidence; do not estimate checklist completion or conflate it with the separate master-project milestone count.
- DEC-061 is the current T-534 product/UX amendment: it preserves DEC-059's PySide6/runtime boundary but replaces the old Study/Runs/Results/Artifacts product model with **Experiment / Run / Results / Evidence**.
- `T-610` remains a separate **BLOCKED** scientific task. Its dependencies and methodology are unchanged; `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain mandatory.
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

Pre-final readiness includes deny-by-default final execution in `StudyService`, read-only final preflight, DEVELOPMENT-only synthetic end-to-end smoke, `docs/research/RQ_EVIDENCE_TRACEABILITY.md`, and focused protocol-v2.1 CI coverage. None of these authorize `T-610`.

## Application state

DEC-059 selects PySide6 / Qt 6 Widgets over the framework-neutral Study backend. `T-528` and `T-511` remain historical completed application/acceptance records; their presentation is not the implementation authority for T-534.

PR #107 implements DEC-061 and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md` as the experiment-first **Experiment / Run / Results / Evidence** application. The active UI now projects protocol-v2.1 fail-closed; the final Thesis experiment is immutable with all five methods; DEVELOPMENT uses backend-constrained Configure → Review → Create; Run uses truthful durable method status plus presentation-only GridWorld frames; Phase B requires exact method/root/layout/condition/interaction FD/AD pairing; Results remain RQ1/RQ2/RQ3 projections of stored validated outputs; Evidence leads with readiness and exposes backend-registered lineage on demand.

Active protocol-v2.0/DEC-058/T-528 presentation assumptions discovered during T-534 have been removed from current user-facing behavior. Historical decisions, compatibility support for historical DEVELOPMENT records and explicitly historical documentation remain intact rather than being rewritten.

The deterministic T-534 review set covers 1366×768 and 1440×900 Experiment, DEVELOPMENT review, Phase-A GridWorld, exact Phase-B Frozen/Adaptive pairing, RQ1, RQ2, recovered/right-censored RQ3, Evidence readiness/technical lineage and onboarding/final-lock states. Fixtures are DEVELOPMENT/synthetic only; render manifests assert zero scientific jobs/environment steps and no final-reserve access.

## Repository integration / provenance

PR #92 is historical and was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`; there is no remaining PR #92 integration step. PR #103 subsequently merged DEC-061 and the experiment-first T-534 UI specification into `main` as `f960991c3ba71130178946fbc8051875b9fecac6`.

PR #107 is the single coherent T-534 implementation PR. Its implementation heads have repeatedly passed Repository checks and the T-534 PySide6 UI acceptance workflow while objective render findings were fixed narrowly. The final pre-merge exact-head CI pass must include this documentation reconciliation before squash merge.

Only deliberate provenance archive refs remain alongside `main`; they are not active implementation branches and must not be merged merely to reduce branch count.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system exists.

## Still intentionally unfrozen

- Final-reserve **execution authorization** remains withheld even though the protocol recipe is frozen.
- `T-610` remains BLOCKED by the separate explicit scientific authorization gate.
- `T-611`/`T-612`/`T-613` remain blocked downstream of `T-610`.
- WP7 remains blocked by final evidence plus later explicit pre-WP7 user approval.
- Final standalone Windows packaging remains deferred to `T-803` / issue #94.

## Exact next action

Finish T-534 pre-merge reconciliation on PR #107: align issue #104 with objective implementation/test/render evidence, run the final exact-head repository/UI CI after canonical documentation changes, confirm current `main` has not advanced, perform the final PR diff/mergeability review, then squash-merge only if all objective gates remain green. After merge, verify the accepted implementation on `main` and only then mark `T-534` complete in canonical status/docs and close issue #104.

Scientifically, stop at the separate `T-610` authorization gate: do not access final roots/layouts/seeds, execute the protocol-v2.1 final matrix, inspect final outcomes, or begin Results/Discussion without explicit authorization.