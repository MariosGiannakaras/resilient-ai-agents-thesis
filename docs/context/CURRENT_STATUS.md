# Current Project Status

**Date:** 2026-09-01  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` remains the canonical dependency/task ledger. Read task-specific decision/research documents **progressively**. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, `T-528`, `T-529`, historical `T-530`, `T-531`, `T-532`, `T-511` and `T-533` are COMPLETE. The final pre-experiment readiness hardening described below does not change task dependencies or create a new scientific work package.
- DEC-058 and `configs/protocols/protocol-v2.0-final.json` remain immutable historical protocol-v2.0 authority. DEC-060 and `configs/protocols/protocol-v2.1-final.json` remain the current pre-execution authority; no methodology, estimand, root/layout, hyperparameter, condition, budget or recovery-rule change was made by the readiness pass.
- PR #92 was squash-merged into `main` as `feb8c70395d13f506dad2ab60f4a71d4405f6298`; the post-merge status reconciliation was merged as `ae51d9cca36ab2e41f7a8f7e9a2407c8ab56c481`. Historical pre-squash provenance remains reachable through `archive/pre-squash-protocol-v2-lineage`.
- `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain mandatory. **The protocol-v2.1 final matrix has not been authorized or executed, and no final-reserve outcome has been generated, inspected or used.**
- Master tracker #87 remains **7/8** complete; milestone 8 depends on the final v2.1 evidence chain.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution or Results/Discussion writing.

## Protocol-v2.1 scientific contract

### Research questions

- **RQ1 — Nominal learning:** compare Q-Learning, SARSA, DQN, PPO and Dyna-Q+ nominal performance and learning efficiency under the common actual-environment-interaction budget and information contract.
- **RQ2 — Resilience/adaptation:** quantify Frozen/Adaptive loss and matched adaptation benefit `(FN-FD)-(AN-AD)`.
- **RQ3 — Recovery speed:** quantify adaptive recovery trajectory, stable recovery and non-recovery after persistent unannounced change; persistent action-remap is the primary RQ3 family.

Frozen and Adaptive/Continual remain deployment regimes, not distinct algorithms. Root is the independent unit; layouts, episodes, probes and windows are repeated/nested observations. Direct method contrasts are root-paired A-minus-B after equal-layout reduction. Two-sided 95% Student-t pointwise intervals use the predeclared critical value for the actual independent-root count `n=2..12`; no p-value superiority family is authorized.

Recovery remains AN versus AD after equal layout weighting within root, using passive 32-interaction windows over the unchanged 256-interaction horizon. Primary tolerance is `0.10`, sensitivities are `0.05`/`0.20`, stable recovery requires two consecutive in-tolerance windows, and non-recovery is right-censored with `recovery_time=null`. The restricted fixed-horizon recovery delay remains a separately named censored-comparison estimand; 256 is never fabricated as observed recovery time.

## Completed implementation and pre-final readiness

The scientific path remains:

`Phase-B execution -> passive temporal windows -> schema-v2 records -> structural validation -> root reduction -> recovery/direct contrasts -> deterministic exports -> stored-evidence presentation`.

The final readiness pass added only operational safeguards and validation:

- framework-neutral `StudyService` now denies protocol-v2.1 frozen confirmatory execution by default; both `run_ready` and direct `run_job` require the later explicit scientific authorization capability before any final job can start;
- `scripts/check_protocol_v2_1_pre_t610.py` performs fail-closed preflight checks: final lock/gate identity, exact 5-method/12-root/2-layout/4-condition frozen plan, 120 Phase-A jobs, 480 Phase-B matched-set jobs and 603 total Study jobs, no committed final Study bundle, and zero final job attempts/artifacts when execution is unauthorized;
- a synthetic **DEVELOPMENT-only** scientific smoke uses synthetic methods/roots/layout/condition evidence and exercises standardized Phase-A/Phase-B records through real validation -> protocol-v2.1 analysis -> deterministic v2 evidence handoff -> finalized/reloaded StudyStore. It exercises both recovered and right-censored recovery outcomes and never uses final identities;
- `docs/research/RQ_EVIDENCE_TRACEABILITY.md` maps each RQ to its primary evidence, root-level estimands and stored analysis/CSV outputs without defining new methodology;
- the focused Protocol-v2 workflow now explicitly watches/tests protocol-v2.1 authority, temporal/recovery, analysis/export and preflight paths instead of relying only on the full repository suite.

Validation on readiness head `d5e84287652289e0e429402a8bc255c1193b897c`: Repository checks #804 **green** and Protocol-v2 pilot checks #317 **green**. The first smoke attempt exposed only an incorrect test expectation for registered export artifact IDs; the assertion was corrected to the existing canonical `thesis-table-*` / `analysis-table-*` IDs without changing the pipeline.

## Application / UI boundary

PySide6 remains the accepted application architecture over the Python Study backend. Results may present validated stored learning, resilience, recovery and direct-comparison evidence, but the UI must never choose scientific thresholds, aggregate roots/layouts, derive recovery, compute contrasts or supply the final-execution authorization capability.

Any paused Codex UI implementation that began before protocol-v2.1 is non-authoritative partial work. Restart from current `main`; read `AGENTS.md`, `docs/context/TASKS.md` and this file first, then derive UI behavior from DEC-059, DEC-060, `configs/protocols/protocol-v2.1-final.json`, `docs/research/RQ_EVIDENCE_TRACEABILITY.md` and the current backend/evidence contracts rather than carrying forward pre-v2.1 assumptions.

## Documentation / thesis preparation

DEC-060, the decision index, `RESEARCH_BRIEF.md`, `MODEL_CANDIDATES.md`, `docs/experiments/EXPERIMENTAL_REQUIREMENTS.md`, `RQ_EVIDENCE_TRACEABILITY.md` and the structure-only `THESIS_STRUCTURE_DRAFT.md` are consistent with protocol-v2.1. Results, Discussion and conclusion claims remain evidence-gated.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system was created. The repository remains public and `thesis/source-material/ThesisApplication.pdf` remains unchanged.

## Still intentionally unfrozen

- Final-reserve **execution authorization** remains withheld even though the protocol recipe is frozen: `final_reserve_access=false`.
- T-610 remains **BLOCKED by the separate explicit scientific authorization gate**; T-611/T-612/T-613 remain blocked downstream.
- WP7 remains blocked by final evidence plus the later explicit pre-WP7 user-approval gate.
- Final Windows standalone packaging remains deferred to `T-803` / issue #94.

## Exact next action

For application work, restart the paused Codex UI implementation cleanly from the latest `main` and the merged protocol-v2.1 contracts. Scientifically, stop at the separate explicit authorization gate: do not access final roots/layouts/seeds, execute the protocol-v2.1 final matrix, or begin Results/Discussion writing without that authorization.
