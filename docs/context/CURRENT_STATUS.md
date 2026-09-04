# Current Project Status

**Date:** 2026-09-05  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Objective Git/GitHub/evidence state overrides stale prose after interruption.

## Current execution state

- Historical baseline invariants remain complete: `T-100` target-machine validation and `T-200` source-traceable research framing are not reopened by WP7 writing work. The accepted PySide6 application remains the experiment-first **Experiment / Run / Results / Evidence** system; the UI is presentation/control only, never recomputes frozen estimands, and keeps progressive disclosure for technical/provenance detail.
- `T-610` through `T-613` are **COMPLETE**. The accepted DEC-062 replacement completed 603/603 jobs with 600 scientific bundles; T-611 evidence is frozen under manifest SHA-256 `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858`; T-612 analysis under `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`; T-613 thesis assets under `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8`. The historical failed 216-job predecessor remains excluded.
- `T-700`, `T-701` and `T-702` are **COMPLETE**. Current ICE/UNIWA guidance was rechecked; 22 supplied files were reviewed as 21 unique completed theses; the bibliography writing gate was refreshed. The current immutable bibliography consumer checkout is `ada0d1aec7511098fd12610ae9e5abe7aea875cd`; historical label `bibliography-integration-v3` remains prior-snapshot provenance only.
- `T-710`, `T-711` and `T-714` are **COMPLETE**. T-714 was squash-merged through PR #136 as `42afba20fd5a7e9d3912418d0847b42e566aaca0`; its accepted review DOCX SHA-256 is `70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`. Exactly three official-person/declaration placeholders remain intentionally unresolved for review mode.
- `T-715` is **IN_PROGRESS** on PR #138 / branch `thesis/t715-reader-scope-simplification`. The user explicitly authorized/resumed this bounded internal reader-scope and audit-reconciliation cycle on 2026-09-05. It is not supervisor feedback and does not reopen `T-712`.
- T-715 keeps the complete frozen evidence package while shortening the reader-facing main narrative: 10 registered scientific figures remain in the main body and 14 in appendices, alongside the existing synthesis graphic and two deterministic DEVELOPMENT-only PySide6 screenshots that are explanatory, not scientific evidence.
- The supplied audit/prior answer was reconciled against repository authorities before implementation. The v27 composition carries the frozen facts: 180 tuning units; selected configs `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06`, `dyna-c03`; 12 final roots with sizing max half-width 0.1428; exact action-remap semantics; action-failure p=0.15 with no-op step reward −0.1; observation-corruption p=0.05 excluding the current true state but not goal as a category; final layout/seed streams; RQ1/RQ2 definitions; and RQ3 32-interaction windows, directed tolerance 0.10, two-window stability and right-censoring at 256.
- `scripts/t715_audit_hardening.py` plus `scripts/t711_build_entry_v27.py` add 26 bounded clarification paragraphs, including three Heading-3 subsections, after the accepted v26 composition. QA requires exact sentinels, unchanged inline-shape/media hashes, `scientific_values_modified=false`, `registered_asset_bytes_modified=false`, and no new experiment/reanalysis or post-hoc binomial test. `docs/thesis/T715_AUDIT_RECONCILIATION.md` records the authority boundary.
- `T-712` remains **DEFERRED** for actual supervisor/reviewer corrections only. `T-713` remains **DEFERRED** until real feedback is resolved and final Microsoft Word field/update plus placeholder/person-metadata gates pass. `T-538` remains deferred non-scientific application polish.

## Scientific authority

DEC-058/protocol-v2.0 remain immutable historical freeze authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the accepted protocol-v2.1 design: Q-Learning, SARSA, DQN, PPO and Dyna-Q+; common actual-interaction fairness; matched FN/FD/AN/AD Phase B; 12 roots, two held-out layouts, four conditions and 256-interaction horizon. RQ2 adaptation benefit remains `(FN-FD)-(AN-AD)`. RQ3 uses passive 32-interaction windows, tolerance 0.10 primary with 0.05/0.20 sensitivity, two-window stable recovery and `recovery_time=null` right-censoring. Root is the independent unit; declared root-paired contrasts and Student-t intervals use the actual root count. No p-value superiority family or composite ranking is introduced.

T-612 interpretation remains authoritative in `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`. WP7 writing tasks through T-715 alter structure/presentation only and do not reinterpret frozen outcomes.

## WP7 writing authority

Current official Department/University guidance and actual supervisor instructions outrank project writing conventions. `docs/thesis/THESIS_REQUIREMENTS.md`, `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`, the T-710 manuscript, frozen T-611/T-612/T-613 evidence and synchronized citation-ready bibliography remain the controlled writing sources; example theses provide structure/style context only.

## Still intentionally unfrozen / externally gated

- Exact official student/person metadata and declaration wording must not be invented; review builds may retain placeholders but T-713 final mode must reject them.
- Optional acknowledgements/dedication remain unset unless supplied by the user.
- Final Microsoft Word field updates remain required before submission.
- Defense duration, slide count/template and live-demo requirements remain unfrozen until an authoritative rule is available.
- T-803 standalone Windows packaging remains post-thesis and does not block WP7.

## Exact next action

Finish T-715 on PR #138: obtain green checks for the audit-reconciled v27 head, download the CI-produced DOCX/QA artifact, render and inspect every final page, reconcile the PR body with the validated artifact SHA/page count, and merge only if all gates remain green. Keep T-712 deferred for actual supervisor/reviewer feedback and do not start T-713 while official placeholders or final Word field updates remain unresolved.
