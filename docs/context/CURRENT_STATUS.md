# Current Project Status

**Date:** 2026-09-01  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` remains the canonical dependency/task ledger. Read task-specific decision/research documents **progressively**. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, `T-528`, `T-529`, historical `T-530`, `T-531`, `T-532`, `T-511` and **`T-533` are COMPLETE**.
- DEC-058 and `configs/protocols/protocol-v2.0-final.json` remain immutable historical protocol-v2.0 freeze authority. DEC-060 is the explicit pre-outcome amendment; it does not rewrite DEC-058 history.
- `configs/protocols/protocol-v2.1-final.json` is the self-contained current scientific authority. It preserves the five methods, selected hyperparameters, Phase-A budget/probes, 12 final roots, 2 held-out final layouts, four Phase-B conditions and the 256-interaction horizon from DEC-058.
- PR #92 was squash-merged into `main` as commit `feb8c70395d13f506dad2ab60f4a71d4405f6298`. Issue #98 is CLOSED/COMPLETE.
- Exact final PR head `b722c3065368557ca06b46b1c2a374aa5f3cd085` passed Repository checks #799, Protocol-v2 pilot checks #314 and T-528 PySide6 UI screenshot checks #140 before merge. The squash merge preserves that exact tree.
- `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain mandatory. **T-610 has not been authorized or executed. No protocol-v2 final-reserve outcome was generated, inspected or used by T-533.**
- Master tracker #87 remains **7/8** complete; milestone 8 depends on the final v2.1 evidence chain.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution or Results/Discussion writing.

## Completed T-533 / DEC-060 amendment

### Final research questions

- **RQ1 — Nominal learning:** compare Q-Learning, SARSA, DQN, PPO and Dyna-Q+ nominal performance and learning efficiency under the common actual-environment-interaction budget and information contract.
- **RQ2 — Resilience/adaptation:** quantify directed Frozen/Adaptive loss and preserve matched adaptation benefit `(FN-FD)-(AN-AD)`.
- **RQ3 — Recovery speed:** quantify adaptive recovery trajectory, stable recovery and non-recovery after persistent unannounced change.

Frozen and Adaptive/Continual remain deployment regimes, not distinct algorithms.

### Recovery-speed contract

- Primary RQ3 family: persistent `action-remap/*`; action-failure and observation-corruption remain supporting diagnostics.
- Metric: mean reward per actual environment interaction.
- Passive fixed windows: 32 interactions across the unchanged 256-interaction horizon, crossing episode boundaries without reset/realignment.
- Reference: Adaptive-Nominal (`AN`) versus Adaptive-Disturbed (`AD`), equal layout weighting inside each independent root.
- Higher-is-better gap: `AN - AD`; primary tolerance `0.10`, sensitivity `0.05`/`0.20`.
- Stable recovery: two consecutive in-tolerance windows.
- Non-recovery: right-censored at 256 with `recovery_time=null`; 256 is never fabricated as recovery time.
- Censoring-aware method comparison uses recovery status plus the separately named restricted fixed-horizon recovery delay. Observed recovery-time summaries remain conditional on recovery.

### Statistics and computation

- Root is the independent unit; layouts, episodes, probes and windows are repeated/nested observations.
- Direct method contrasts are root-paired A-minus-B on shared roots after equal layout reduction.
- Two-sided 95% Student-t pointwise intervals select the predeclared critical value for the actual independent-root count `n=2..12`.
- No formal p-value superiority family or post-hoc “statistically significant” relabeling is authorized.
- Actual environment interactions remain the primary fairness axis. Wall-clock/process CPU and interpretable method-native update counts are secondary descriptive evidence.

## Completed implementation chain

The complete pre-final path is versioned and isolated from historical v2.0/T-526/T-527 code:

`Phase-B execution -> passive temporal windows -> schema-v2 records -> structural validation -> root reduction -> recovery/direct contrasts -> deterministic exports -> stored-evidence PySide6 presentation`.

The v2.1 Study recipe materializer fails closed if the final-reserve lock or explicit T-610 gate is altered. PPO/DQN temporal capture does not impose artificial 32-step learning boundaries. A numerical `1e-12` guard only prevents binary floating-point representation from changing an exact frozen tolerance-boundary classification.

PySide6 Results supports stored Recovery & Comparisons summaries, AN-vs-AD trajectory rows and direct method contrasts for schema-v2/v2.1 packages. Legacy schema-v1 packages remain supported and do not expose recovery. The UI never chooses thresholds, reduces roots or recomputes scientific estimands.

Any separately paused Codex UI working copy that started before the protocol-v2.1 merge must be treated as non-authoritative partial work. Restart UI implementation from current `main`, read `AGENTS.md`, `docs/context/TASKS.md` and this file first, and re-derive UI behavior from the merged v2.1 backend/evidence contracts rather than carrying forward pre-v2.1 assumptions.

## Documentation / thesis preparation

`TASKS.md`, DEC-060, the decision index, `RESEARCH_BRIEF.md`, `MODEL_CANDIDATES.md`, `docs/experiments/EXPERIMENTAL_REQUIREMENTS.md` and the structure-only `THESIS_STRUCTURE_DRAFT.md` are reconciled to protocol-v2.1. Results, Discussion and conclusion claims remain explicitly evidence-gated.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system was created.

The repository remains public by explicit user decision. `thesis/source-material/ThesisApplication.pdf` and the existing source-material structure remain unchanged; privacy migration/history rewrite is not a scientific blocker.

## Still intentionally unfrozen

- Final-reserve **execution authorization** remains unfrozen/withheld even though the protocol recipe is frozen: `final_reserve_access=false`.
- T-610 is dependency-valid after T-533 but remains **BLOCKED by the separate explicit scientific authorization gate**.
- T-611/T-612/T-613 remain blocked downstream of T-610.
- WP7 remains blocked by final evidence plus the later explicit pre-WP7 user-approval gate.
- Final Windows standalone packaging remains deferred to `T-803` / issue #94.

## Exact next action

For application work, a paused pre-v2.1 Codex UI implementation may now restart cleanly from current `main` using the merged protocol-v2.1 contracts as authority. Scientifically, stop at the **separate explicit authorization gate for T-610**: do not access final roots/layouts/seeds, execute the protocol-v2.1 final matrix, or begin Results/Discussion writing without that authorization.
