# Current Project Status

**Date:** 2026-09-05  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Objective Git/GitHub/evidence state overrides stale prose after interruption.

## Active repository continuity work

- `T-010` is **IN_PROGRESS** on PR #146. Its purpose is to make repository continuation independent of chat/model memory: `AGENTS.md` is the no-prompt entrypoint, `docs/context/WORK_STATE.json` is the operational resume pointer, and every material change/checkpoint must update that pointer before work proceeds.
- Recovery order is: working-tree work -> open PR -> unmerged pushed branch -> `WORK_STATE` -> `TASKS` `IN_PROGRESS` -> first dependency-valid `READY` task -> exact external gate.
- T-716 remains COMPLETE and immutable as the accepted review-ready thesis milestone. T-010 changes workflow/governance only; it does not change the thesis DOCX, protocol, frozen evidence, analysis or scientific assets.

## Current execution state

- Historical baseline invariants remain complete: `T-100` target-machine validation and `T-200` source-traceable research framing are not reopened by WP7 writing work. The accepted PySide6 application remains the experiment-first **Experiment / Run / Results / Evidence** system; the UI is presentation/control only and retains progressive disclosure for technical/provenance detail.
- `T-610` through `T-613` are **COMPLETE**. The accepted DEC-062 replacement completed 603/603 jobs with 600 scientific bundles; T-611 evidence is frozen under manifest SHA-256 `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858`; T-612 analysis under `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`; T-613 thesis assets under `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8`.
- `T-700`, `T-701`, `T-702`, `T-710`, `T-711`, `T-714` and `T-715` are **COMPLETE as their defined tasks**. T-715 is an auditable reader-scope/audit-hardening milestone, **not the final thesis**.
- **T-716 is COMPLETE.** Final acceptance is recorded in `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md`: all 11 rewrite-plan gates pass. The accepted review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx` with 25,327 whole-document words, 23,273 main-body words to bibliography, 766 paragraphs, 31/31 governed references used, 25/25 scientific media preserved and 92-page visual QA. Semantic package SHA-256 `b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1`; CI archive raw SHA-256 `08992272e90b0cae6b457a3f4ce66511cc7c337aeea0b6d3645d632f8d66a7f7`. T-714 remains the historical full-content provenance baseline and T-715 the scientific-correction overlay.
- The T-715 corrections remain authoritative: 180 tuning units; selected configs `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06`, `dyna-c03`; 12 final roots with sizing max half-width 0.1428; exact action-remap semantics; action failure p=0.15 as no-op with ordinary step reward −0.1; observation corruption p=0.05 with the implemented support; RQ1/RQ2 definitions; and RQ3 32-interaction windows, directed tolerance 0.10, two-window stability and right-censoring at 256. No new experiment/reanalysis/post-hoc superiority family was introduced.
- Permanent deliverable retention applies: meaningful user-facing thesis milestones are committed under `thesis/archive/` before handoff; only genuinely accepted submission candidates belong under `thesis/final/`.

## Repository / writing maintenance completed for T-716

- The README now reflects T-716 as COMPLETE, T-712 as the current externally gated academic task, and the full downstream lifecycle. `docs/context/POST_THESIS_LIFECYCLE.md` preserves the sequence **T-716 → actual T-712 feedback/corrections → T-713 final thesis freeze → T-720/T-721/T-722 defense work → T-800/T-801/T-802 final audits/delivery → T-803 standalone Windows package**.
- Conservative repository cleanup removed only proven-unused placeholder scaffolds: `data/raw`, `data/processed`, `data/external`, `artifacts/figures`, `artifacts/tables`, `artifacts/exports`. No docs, results, evidence, decisions, archived thesis artifacts, restored drafts or useful implementation history were deleted. See `docs/context/REPOSITORY_CLEANUP_2026-09-05.md`.
- Full repository/bibliography audits are retained under `docs/thesis/audits/`. The earlier 599-source/599-analysis scan remains historical audit evidence; the final synchronized consumer corpus now contains 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals.
- T-716 no longer uses a fixed bibliography-count target. Bibliography size is an output of validated claim coverage. Citation-ready status means **eligible for formal citation**, not “source of truth”.
- Source selection is now governed by `docs/thesis/BIBLIOGRAPHY_SOURCE_SELECTION_POLICY.md`: exact claim fitness, scientific authority, primary/foundational value and methodological strength are evaluated before publication year; among materially comparable sources, the newer source is preferred by default; an older source may outrank a newer one when it is clearly stronger, with the reason kept explicit. Student/informal/derivative material does not outrank stronger scholarly primary evidence or authoritative books merely because it is newer.
- `docs/thesis/CLAIM_EVIDENCE_TREE.md` is the human-readable chapter/claim mapping; `docs/thesis/claim-evidence-map.json` is the machine registry outside the immutable synchronized bibliography import. Claims combine materially relevant formal sources, preserve contradictory/limiting evidence, distinguish context/informal material, and attach protocol/result statements to repository authorities. `scripts/validate_claim_evidence_map.py` plus `.github/workflows/claim-evidence-map.yml` fail closed on unknown/non-ready sources, weak single-source literature claims without exception, missing project authority paths or loss of the source-selection policy contract.
- Initial claim-map CI correctly failed on two stale decision filenames; the canonical DEC-058/DEC-060 paths were corrected and the subsequent validation run passed. Intermediate failures remain part of the audit history rather than being hidden.

## Scientific authority

DEC-058 and protocol-v2.0 remain immutable historical freeze authority. The current amendment is `docs/decisions/DEC-060_PROTOCOL_V2_1_RECOVERY_AND_COMPARISON_AMENDMENT.md` plus `configs/protocols/protocol-v2.1-final.json`: Q-Learning, SARSA, DQN, PPO and Dyna-Q+; common actual-interaction fairness; matched FN/FD/AN/AD Phase B; 12 roots, two held-out layouts, four conditions and 256-interaction horizon. RQ2 adaptation benefit remains `(FN-FD)-(AN-AD)`. RQ3 uses passive 32-interaction windows, tolerance 0.10 primary with 0.05/0.20 sensitivity, two-window stable recovery and `recovery_time=null` right-censoring. Root is the independent unit. No p-value superiority family or composite global ranking is introduced.

T-612 interpretation remains authoritative in `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`. Writing changes exposition and literature synthesis only; frozen outcomes and registered scientific media remain unchanged.

## Bibliography authority

The immutable bibliography writing-gate consumer snapshot is `27674a566ab55e4491b74243fe077a31ef81ae73`, synchronized and validated at 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals. The earlier `ada0d1aec7511098fd12610ae9e5abe7aea875cd` / `bibliography-integration-v3` state is prior-snapshot provenance only. Watkins–Dayan, Sutton 1990, Khetarpal and Padakandla are now formal citation-ready sources; Liu 2025 and Cadet 2025 are scoped supporting formal sources. Talks/transcripts remain discovery/synthesis material only and cannot independently support exact equations, guarantees or numerical claims.

## Still intentionally unfrozen / externally gated

- `T-712` waits for **actual** supervisor/reviewer feedback; internal audits are not relabelled as external feedback. T-716 acceptance satisfies the composition prerequisite but does not fabricate external feedback.
- `T-713` now has accepted T-716 content but still waits for resolved real feedback, authoritative person/declaration metadata and final Microsoft Word fields/submission-format checks.
- Defense duration, slide count/template and live-demo requirements remain unfrozen until authoritative guidance is available.
- T-803 standalone Windows packaging remains post-thesis and does not block T-713.

## Exact next action

Finish T-010 on PR #146, validate the prompt-free recovery/checkpoint workflow, and merge only when continuity/documentation/required PR CI is green. After merge, normalize `WORK_STATE.json` on `main` to T-712 DEFERRED unless real supervisor/reviewer feedback has arrived.
