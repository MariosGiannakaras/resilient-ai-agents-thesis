# Current Project Status

**Date:** 2026-09-01  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Read task-specific decision/research documents **progressively**. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, historical application baseline `T-528`, `T-529`, historical `T-530`, `T-531`, `T-532`, historical intended-user acceptance `T-511`, and `T-533` are COMPLETE.
- `T-534` is the active dependency-valid application task: a clean protocol-v2.1 PySide6 rebuild from fresh current `main`. The paused/pre-v2.1 UI branch/worktree is not an implementation base.
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

Pre-final readiness additionally includes:

- deny-by-default final execution in `StudyService`;
- read-only final preflight that verifies the frozen v2.1 matrix while making zero final attempts/artifacts;
- DEVELOPMENT-only synthetic end-to-end smoke through validation, v2.1 analysis, deterministic export and finalized/reloaded StudyStore;
- `docs/research/RQ_EVIDENCE_TRACEABILITY.md`;
- focused Protocol-v2 CI coverage for v2.1 temporal/recovery/analysis/export/preflight contracts.

These checks do not authorize `T-610`.

## Application state

DEC-059 selects PySide6 / Qt 6 Widgets over the framework-neutral Study backend. `T-528` remains historically COMPLETE and records the previous architecture/workflow/read-model/application baseline; `T-511` remains its historical intended-user acceptance record.

DEC-061 now controls the T-534 **product model and information architecture**. The application is experiment-first, not StudyStore/job/artifact-first. Primary navigation is **Experiment / Run / Results / Evidence**; Help/onboarding and technical/reproducibility details are contextual/secondary.

The rebuild must start from current `main`, audit `src/resilient_agents/desktop/`, preserve still-correct UI-neutral Study/evidence/provenance/execution contracts, and freely replace historical presentation windows/pages/widgets/styles/navigation where appropriate.

The current desktop audit identified real migration targets: active presentation code still contains protocol-v2.0/DEC-058/T-528-specific root discovery, protocol loading, shell/status/help and desktop execution-policy wording. These are not current v2.1 presentation authority.

The rebuilt UI must:

- make the scientific experiment understandable before backend administration;
- keep all five final methods fixed in the Thesis experiment; method selection is DEVELOPMENT-only where backend-supported;
- present Frozen and Adaptive as simultaneous matched Phase-B regimes, never algorithms or mutually exclusive choices;
- make one large Phase-A GridWorld or two exact-matched Phase-B Frozen/Adaptive GridWorlds the dominant Run visualization, with compact five-method status;
- keep primary live facts to method/phase/condition/interaction/intended→executed action/reward and move roots/states/observations/IDs/flags/hashes to technical disclosure;
- organize Results explicitly by **RQ1 Learning / RQ2 Resilience & Adaptation / RQ3 Recovery**;
- use real stored Phase-A trajectory/probe information for RQ1 when scientifically supported, never a UI-invented aggregate;
- preserve RQ2 adaptation-benefit and Frozen/Adaptive-loss separation;
- preserve RQ3 trajectory/status/conditional observed time/restricted-delay/right-censoring semantics, never showing 256 as observed recovery time for a censored root;
- make Evidence user-friendly first and provenance-rich on demand;
- present only validated stored scientific outputs and keep historical schema-v1 truthful;
- never recompute scientific thresholds, root reductions, estimands, intervals, recovery, conclusions, RNG/checkpoints or evidence finalization in Qt;
- never grant/bypass final-experiment authorization;
- remain novice-first, compact, self-explanatory and accessible with truthful locked/error/loading/empty states;
- use DEVELOPMENT/synthetic fixtures for implementation tests/screenshots.

## Repository integration / provenance

PR #92 is historical and was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`; there is no remaining PR #92 integration step. Protocol-v2.1 readiness and pre-UI context cleanup were subsequently merged as well.

Only deliberate provenance archive refs remain alongside `main`; they are not active implementation branches and must not be merged into current development merely to reduce branch count.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system exists.

## Still intentionally unfrozen

- Final-reserve **execution authorization** remains withheld even though the protocol recipe is frozen.
- `T-610` remains BLOCKED by the separate explicit scientific authorization gate.
- `T-611`/`T-612`/`T-613` remain blocked downstream of `T-610`.
- WP7 remains blocked by final evidence plus later explicit pre-WP7 user approval.
- Final standalone Windows packaging remains deferred to `T-803` / issue #94.

## Exact next action

Execute `T-534` as the active application package from one fresh implementation branch created from the latest current `main`. First read `AGENTS.md`, `docs/context/TASKS.md` and this file, then DEC-059/DEC-060/DEC-061, the protocol-v2.1 config, RQ evidence traceability and current UI information architecture. Implement the experiment-first **Experiment / Run / Results / Evidence** application from the merged protocol-v2.1/Study/evidence contracts rather than inheriting pre-v2.1 presentation assumptions.

Scientifically, stop at the separate `T-610` authorization gate: do not access final roots/layouts/seeds, execute the protocol-v2.1 final matrix, inspect final outcomes, or begin Results/Discussion without explicit authorization.
