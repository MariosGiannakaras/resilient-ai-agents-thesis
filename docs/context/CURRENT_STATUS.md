# Current Project Status

**Date:** 2026-09-02  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Read task-specific decision/research documents progressively. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target-machine validation and `T-200` research framing are complete.
- Protocol-v1.0 / FINAL-* / R0 evidence remain immutable history; superseded `T-522` must not execute.
- Scientific/pre-final implementation through `T-533` is complete. `T-534` experiment-first PySide6 rebuild, `T-535` intended-user hardening, and `T-536` final visual polish/richer in-app result visualization are **COMPLETE**.
- `T-537` is **IN_PROGRESS** on issue #116 / `chore/t-537-final-repository-hygiene`. It is a final active-tree hygiene pass only: remove superseded non-scientific residue while keeping historical scientific protocols/configs, evidence/manifests, decisions and reproducibility-critical code intact.
- T-537 removes obsolete branch-bound T-528 workflows, the retired local bibliography-downloader compatibility shim/test, an orphan visual-reference pointer, superseded committed T-528 screenshot copies, and safe redundant scaffold placeholders. Historical T-528/T-511 visual acceptance remains recoverable through Git history and exact-head Actions artifacts.
- Generated UI review renders are now treated as CI/local QA artifacts rather than committed repository evidence. The active PySide6 acceptance workflow remains available with task-agnostic naming.
- The accepted application remains **Experiment / Run / Results / Evidence**, with `Locked Thesis experiment`, five immutable Thesis methods and simultaneous matched Frozen/Adaptive presentation.
- `docs/research/T-613_THESIS_FIGURE_INVENTORY.md` remains the downstream T-613 output contract: a rich reproducible main-thesis + appendix + defense figure/table package generated from validated stored final outputs, not quantitative UI screenshots.
- A final **read-only merged-main preflight** was completed after the T-536 merge. It confirmed `final_reserve_access=false`, `execution_authorization=requires-explicit-t610-gate`, no committed `protocol-v2.1-final` Study bundle, deny-by-default final execution, and the canonical 603-job plan with `final_execution_authorized=false`.
- `T-610` remains **BLOCKED**. T-537 must complete first; afterward it remains blocked solely by the separate explicit final-scientific-experiment authorization gate.
- Master tracker #87 remains **7/8**; milestone 8 awaits the final v2.1 evidence chain.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution or Results/Discussion writing.

## Scientific authority

DEC-058 / protocol-v2.0 remain immutable historical freeze authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` are the current pre-execution scientific authority.

Frozen protocol-v2.1 remains unchanged: Q-Learning, SARSA, DQN, PPO and Dyna-Q+; common actual-interaction fairness; Phase-A independent learning/exact checkpoints; matched FN/FD/AN/AD Phase B; 12 roots, 2 held-out layouts, four conditions and 256-interaction horizon; RQ2 adaptation benefit `(FN-FD)-(AN-AD)`; RQ3 passive 32-interaction windows, tolerance 0.10 with 0.05/0.20 sensitivity, two-window stability and `recovery_time=null` right-censoring; root as independent unit; declared root-paired direct method contrasts and Student-t intervals. No protocol-v2.1 final-reserve outcome has been generated, inspected or used.

## Pre-final backend/application readiness

The validated backend chain remains:

`Study recipe/plan -> Phase A -> exact checkpoint -> FN/FD/AN/AD -> temporal evidence -> validation -> root reduction -> RQ1/RQ2/RQ3 analysis -> recovery/direct contrasts -> deterministic exports -> stored-evidence application read model`.

Deny-by-default final execution, read-only preflight, DEVELOPMENT synthetic smoke and RQ evidence traceability are complete. None authorize T-610.

The accepted PySide6 application is experiment-first. T-535 guarantees created-record selection, Run→Results/Evidence context propagation, `Experiment record` terminology, RQ-local direct comparisons, progressive provenance disclosure, truthful retry states and actionable Evidence next steps. T-536 adds larger GridWorld emphasis, current-method/five-method lifecycle orientation, larger RQ1/RQ2 charts, stored-evidence RQ3 trajectories, improved sparse-screen use and restrained hierarchy/readability polish. The UI never recalculates scientific estimands, thresholds, recovery classification or intervals.

## Thesis/defense result assets

`T-613` remains BLOCKED behind T-612. Its inventory specifies 30 figure/asset categories plus tables across RQ1 learning, RQ2 resilience/adaptation, RQ3 recovery, methodology/evidence lineage and defense variants. Outputs are deterministic vector-first SVG/PDF plus high-resolution PNG and machine-readable tables with source artifact IDs/hashes and generator provenance. Non-recovery remains right-censored.

## Repository integration / provenance

- PR #107 / T-534 merged as `c372c581b88c63f3b07c96bd50bbc17b9b83f835` after Repository checks #864 and UI acceptance #174.
- PR #110 / T-535 merged as `225df138c5c5be0c39c9e474ef7fdbce6b11245b` after Repository checks #872 and UI acceptance #179.
- PR #113 / T-536 merged as `d16f16cef06406d8af974ef3bab5be9608d65666` after Repository checks #886, UI acceptance #190 and deterministic visual review.
- Post-T536 canonical reconciliation merged as `4ffb7bc700b3d485324c659e94823c9d2e272cba`.
- README refresh PR #115 merged as `31877a09ec2eda7852856c6c1cf7ae059bbf72ae` after Repository checks #890.
- T-537 issue #116 / `chore/t-537-final-repository-hygiene` is the active cleanup package.
- Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/`; `bibliography-integration-v3` is immutable historical terminology, not a parallel system.

## Still intentionally unfrozen

- Final-reserve execution authorization remains withheld.
- T-537 is the only active pre-T610 maintenance package.
- T-610 remains blocked by T-537 completion plus separate explicit authorization; T-611/T-612/T-613 remain downstream blocked.
- WP7 remains blocked by final evidence plus later explicit pre-WP7 approval.
- Standalone Windows packaging remains deferred to T-803 / issue #94.

## Exact next action

Complete T-537 through live-reference audit, Repository checks, current PySide6 UI acceptance, canonical reconciliation, squash merge and merged-main verification. Then stop at the separate `T-610` scientific authorization gate. Do not access or execute the final reserve, inspect final outcomes, or begin WP7/Results/Discussion without the required separate explicit authorization.
