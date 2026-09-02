# Current Project Status

**Date:** 2026-09-03  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Objective Git/GitHub/evidence state overrides stale prose after interruption.

## Current execution state

- The scientific/application programme through `T-613` is **COMPLETE**. Master tracker #87 reached **8/8** and was closed completed.
- The accepted PySide6 application remains the experiment-first **Experiment / Run / Results / Evidence** system. The UI is presentation/control only and never recomputes frozen scientific estimands.
- `T-610` is COMPLETE. The DEC-062 replacement execution `protocol-v2.1-final--t610-recovery-01` completed/finalized 603/603 jobs with 600 scientific run bundles and zero infrastructure/scientific failures. The first 216-job attempt remains immutable failed/incomplete historical evidence and is permanently excluded from accepted final outcomes.
- `T-611` is COMPLETE. Accepted evidence is frozen at `results/final-evidence/protocol-v2.1-final/` under manifest SHA-256 `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858` and 600-record inventory SHA-256 `0c2b352b88045951d32e58ee3479656dce00e35d55899bcdea65dc07604d8045`.
- `T-612` is COMPLETE. The canonical predeclared RQ1/RQ2/RQ3 analysis is finalized at `results/analysis/protocol-v2.1-final/` under analysis manifest SHA-256 `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`.
- `T-613` is COMPLETE. The deterministic thesis/appendix/defense evidence package at `results/thesis-assets/protocol-v2.1-final/` contains 31 figures, 12 table assets and 117 registered output variants under asset manifest SHA-256 `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8`. Inventory categories 1 and 6 remain explicitly unavailable because T-612 registered no probe/checkpoint-series values; no post-hoc reconstruction is allowed.
- **Pre-WP7 approval: APPROVED.** After T-613 completion, the user explicitly directed the project on 2026-09-03 to begin the required next work and to request the example theses when needed.
- `T-700` is **COMPLETE**. Current public ICE/UNIWA thesis-writing/regulation/deposit guidance was rechecked and recorded in `docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`. No newer public ICE replacement was identified for the writing guide; no public ICE-specific defense duration/slide-count/PowerPoint-template/live-demo rule was found.
- `T-701` is **COMPLETE**. Twenty-two supplied example files were reviewed as 21 unique completed theses because `example-theses 1.pdf` and `example-theses 10.pdf` are byte-identical. The canonical derived structure/style guide is `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`. Examples remain contextual structure/presentation evidence only, never scientific sources.
- The final writing architecture is seven substantive chapters: **Introduction; Background and Related Work; Methodology and Experimental Design; Research-System Architecture and Implementation; Results; Discussion; Conclusions and Future Work**, followed by references and appendices. Results and Discussion are intentionally separate because the frozen analysis contains three distinct RQs/estimands, paired contrasts, uncertainty intervals, sensitivity analysis and right-censoring.
- T-700/T-701 select **IEEE numeric citations** as the project WP7 default because ICE permits multiple consistent styles and the technically closest contextual examples predominantly use numeric references. This is not represented as an ICE mandate and is superseded by any later explicit supervisor/Department instruction.
- The existing bibliography consumer snapshot remains the immutable upstream `ThesisBibliography` SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`. It is still valid as the previously accepted imported snapshot, but it does **not** by itself satisfy the required major-writing-gate freshness control in REQ-RES-012.
- `T-702` is the **next READY task**. It must perform a new dated writing-gate literature freshness review in canonical `MariosGiannakaras/ThesisBibliography`, process any genuinely relevant additions through normal source governance, create a new immutable consumer identity even if the selected set does not change, sync it into this repository and validate citation-ready integrity.
- `T-710` is **BLOCKED by T-702**. Full thesis drafting must not begin before the bibliography freshness/re-sync gate is closed.

## Scientific authority

DEC-058/protocol-v2.0 remain immutable historical freeze authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the accepted final protocol-v2.1 scientific design.

Frozen protocol-v2.1 remains unchanged: Q-Learning, SARSA, DQN, PPO and Dyna-Q+; common actual-environment-interaction fairness; Phase-A independent learning/exact checkpoints; matched FN/FD/AN/AD Phase B; 12 roots, 2 held-out layouts, four conditions and 256-interaction horizon; RQ2 adaptation benefit `(FN-FD)-(AN-AD)`; RQ3 passive 32-interaction windows, tolerance 0.10 primary with 0.05/0.20 sensitivity, two-window stable recovery and `recovery_time=null` right-censoring; root as independent unit; declared root-paired direct contrasts and Student-t intervals using actual root count. No formal p-value superiority family or composite method ranking was introduced.

T-612 scientific interpretation remains authoritative in `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`. T-700/T-701 change only writing/structure/presentation governance and do not reinterpret scientific outcomes.

## WP7 writing authority

The current writing hierarchy is:

1. current official Department/University guidance (`T-700` snapshot);
2. actual supervisor instructions when supplied;
3. `docs/thesis/THESIS_REQUIREMENTS.md`;
4. `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md` for derived structure/presentation;
5. frozen T-611/T-612/T-613 evidence for scientific/result claims;
6. citation-ready `ThesisBibliography` evidence for external scientific claims;
7. contextual example theses only for structure/style patterns.

The planned final editable thesis is Greek Microsoft Word (`.docx`) using real Heading styles, automatic TOC, caption fields, cross-references and automatic figure/table lists. The institutional deposit copy may additionally be PDF.

## Exact next action

Execute `T-702` only. Refresh the literature at the major-writing gate in `MariosGiannakaras/ThesisBibliography`, freeze a new immutable consumer snapshot, synchronize/validate it here, then reconcile canonical state. **Do not start T-710 chapter drafting until T-702 is objectively complete.**