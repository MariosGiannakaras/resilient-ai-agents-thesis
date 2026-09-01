# Current Project Status

**Date:** 2026-09-01  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Read task-specific decision/research documents **progressively**. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, historical application baseline `T-528`, `T-529`, historical `T-530`, `T-531`, `T-532`, historical intended-user acceptance `T-511`, and `T-533` are COMPLETE.
- `T-534` is the active dependency-valid application task: a clean protocol-v2.1 PySide6 rebuild from fresh current `main`.
- **GitHub issue #104 is the operational implementation/acceptance checklist for T-534.** It is deliberately detailed so a short instruction such as “start the UI” does not require inventing product behavior. It is a tracking/execution view, not a competing authority; canonical repository decisions/configs/docs win if any wording diverges.
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

DEC-061 and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md` define the current experiment-first product model. The detailed operational sequence, component reuse/redesign checklist, UX/scientific invariants, representative tests/screenshots and Definition of Complete are tracked in **issue #104**.

The implementation must still preserve these top-level boundaries: final Thesis mode keeps all five methods fixed; Frozen/Adaptive are matched regimes rather than algorithms; Run prioritizes truthful GridWorld presentation; Results are RQ1/RQ2/RQ3 and use validated stored outputs only; Evidence is user-friendly first with provenance under progressive disclosure; Qt does not recompute scientific estimands/recovery/intervals or authorize final execution.

The current desktop code contains known protocol-v2.0/DEC-058/T-528 presentation assumptions. Issue #104 explicitly tracks their protocol-v2.1 migration rather than treating existing screens as design authority.

## Repository integration / provenance

PR #92 is historical and was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`; there is no remaining PR #92 integration step. PR #103 subsequently merged DEC-061 and the experiment-first T-534 UI specification into `main` as `f960991c3ba71130178946fbc8051875b9fecac6`.

Only deliberate provenance archive refs remain alongside `main`; they are not active implementation branches and must not be merged merely to reduce branch count.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system exists.

## Still intentionally unfrozen

- Final-reserve **execution authorization** remains withheld even though the protocol recipe is frozen.
- `T-610` remains BLOCKED by the separate explicit scientific authorization gate.
- `T-611`/`T-612`/`T-613` remain blocked downstream of `T-610`.
- WP7 remains blocked by final evidence plus later explicit pre-WP7 user approval.
- Final standalone Windows packaging remains deferred to `T-803` / issue #94.

## Exact next action

Execute `T-534` from one fresh implementation branch created from the latest current `main`. After the mandatory three-file session-start core, read **GitHub issue #104 in full** and use its unchecked items as the operational implementation/validation/acceptance checklist, with DEC-059/060/061, protocol-v2.1, RQ evidence traceability and the UI information architecture as canonical authority.

Scientifically, stop at the separate `T-610` authorization gate: do not access final roots/layouts/seeds, execute the protocol-v2.1 final matrix, inspect final outcomes, or begin Results/Discussion without explicit authorization.
