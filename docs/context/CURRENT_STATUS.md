# Current Project Status

**Date:** 2026-09-05  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Objective Git/GitHub/evidence state overrides stale prose after interruption.

## Current execution state

- Historical baseline invariants remain complete: `T-100` target-machine validation and `T-200` source-traceable research framing are not reopened by WP7 writing work. The accepted PySide6 application remains the experiment-first **Experiment / Run / Results / Evidence** system; the UI is presentation/control only and never recomputes frozen estimands.
- `T-610` through `T-613` are **COMPLETE**. The accepted DEC-062 replacement completed 603/603 jobs with 600 scientific bundles; T-611 evidence is frozen under manifest SHA-256 `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858`; T-612 analysis under `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`; T-613 thesis assets under `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8`.
- `T-700`, `T-701`, `T-702`, `T-710`, `T-711`, `T-714` and `T-715` are **COMPLETE as their defined tasks**. T-714 was squash-merged through PR #136 as `42afba20fd5a7e9d3912418d0847b42e566aaca0`. T-715 was squash-merged through PR #138 as `35c5367f075a2f3af0bb6d40d9db08cfc484419c` after Repository checks, DOCX QA and rewrite-workbook checks passed.
- The T-715 v27 DOCX SHA-256 is `e06a466e667359486a86f30c561c42b74b4e209ea28bb8d94c2652c9d36616d1`; it has 59 rendered pages, 446 paragraphs, 17 verified references, all 24 registered scientific figures, four Word tables, 27 inline shapes and exactly three intentional review placeholders. Its 59/59-page visual QA passed.
- **T-715 is not the final thesis manuscript.** On 2026-09-05 the user explicitly rejected the reader-scope compression because it reduced a previously full ~20k-word manuscript to roughly 12–13k whole-document words. Passing scientific/structural/visual QA does not satisfy the required content/coverage target.
- The recovered T-714 run #66 DOCX (`70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`) is the current full-content baseline at approximately 20,925 whole-document words. The next complete thesis must restore and expand that fuller academic coverage while integrating the validated T-715 audit corrections rather than padding the compressed T-715 text.
- The T-715 audit corrections remain authoritative for scientific wording: 180 tuning units; selected configs `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06`, `dyna-c03`; 12 final roots with sizing max half-width 0.1428; exact action-remap semantics; action-failure p=0.15 with no-op step reward −0.1; observation-corruption p=0.05 excluding the current true state but not goal as a category; RQ1/RQ2 definitions; and RQ3 32-interaction windows, directed tolerance 0.10, two-window stability and right-censoring at 256. No new experiment/reanalysis/post-hoc superiority family was introduced.
- A permanent deliverable-retention rule now applies: `/mnt/data` and Actions artifacts are transient only. Meaningful user-facing deliverables must be committed to the repository. Historical/superseded review versions live under `thesis/archive/`; only genuinely accepted submission candidates belong under `thesis/final/`. See `docs/context/DELIVERABLE_RETENTION_POLICY.md` and `thesis/archive/README.md`.
- Recovered permanent milestones include T-711 run #22, T-711 run #27, T-714 run #66, T-715 pre-audit run #90 and T-715 audit-reconciled run #98, each with its QA report and recorded SHA-256.
- `T-712` remains **DEFERRED / WAITING FOR ACTUAL SUPERVISOR OR REVIEWER FEEDBACK**. The internal audit is not relabelled as supervisor feedback. `T-713` remains **DEFERRED** until the full-content manuscript is accepted, real feedback is resolved, official person/declaration placeholders are supplied, and final Microsoft Word fields are updated. `T-538` remains deferred non-scientific application polish.

## Scientific authority

DEC-058/protocol-v2.0 remain immutable historical freeze authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the accepted protocol-v2.1 design: Q-Learning, SARSA, DQN, PPO and Dyna-Q+; common actual-interaction fairness; matched FN/FD/AN/AD Phase B; 12 roots, two held-out layouts, four conditions and 256-interaction horizon. RQ2 adaptation benefit remains `(FN-FD)-(AN-AD)`. RQ3 uses passive 32-interaction windows, tolerance 0.10 primary with 0.05/0.20 sensitivity, two-window stable recovery and `recovery_time=null` right-censoring. Root is the independent unit; declared root-paired contrasts and Student-t intervals use the actual root count. No p-value superiority family or composite ranking is introduced.

T-612 interpretation remains authoritative in `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`. Writing work changes exposition and structure only; frozen outcomes and registered scientific media remain unchanged.

## WP7 writing authority

Current official Department/University guidance and actual supervisor instructions outrank project writing conventions. `docs/thesis/THESIS_REQUIREMENTS.md`, `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`, the T-710 manuscript, frozen T-611/T-612/T-613 evidence, synchronized citation-ready bibliography, the T-714 full-content baseline and the T-715 audit reconciliation are the controlled inputs. Example theses provide structure/style context only.

## Still intentionally unfrozen / externally gated

- Exact official student/person metadata and declaration wording must not be invented.
- Optional acknowledgements/dedication remain unset unless supplied by the user.
- Final Microsoft Word field updates remain required before submission.
- Defense duration, slide count/template and live-demo requirements remain unfrozen until an authoritative rule is available.
- T-803 standalone Windows packaging remains post-thesis and does not block WP7.

## Exact next action

Produce the next **full-content thesis manuscript** from the T-714 full baseline plus all validated T-715 corrections and current repository authorities, preserving or increasing substantive academic coverage rather than simplifying it. Commit every delivered DOCX/QA milestone to the repository before handoff. Keep T-712 deferred until real supervisor/reviewer feedback exists and do not start T-713 until the full-content manuscript plus official finalization gates are satisfied.
