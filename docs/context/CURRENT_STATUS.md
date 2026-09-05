# Current Project Status

**Date:** 2026-09-05  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical dependency/task ledger. Objective Git/GitHub/evidence state overrides stale prose after interruption.

## Current execution state

- `T-610` through `T-613` are **COMPLETE**. The accepted DEC-062 replacement completed 603/603 jobs with 600 scientific bundles; T-611 evidence is frozen under manifest SHA-256 `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858`; T-612 analysis under `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`; T-613 thesis assets under `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8`.
- `T-700`, `T-701`, `T-702`, `T-710`, `T-711`, `T-714` and `T-715` are **COMPLETE as their defined tasks**. T-715 is an auditable reader-scope/audit-hardening milestone, **not the final thesis**.
- The archived T-714 run #66 (`70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`) is the current full-content baseline at approximately 20.9k whole-document words. The active academic task is **T-716 — full-content evidence-aware thesis reconstruction/expansion**, integrating useful restored-draft material plus all validated T-715 scientific corrections.
- The T-715 corrections remain authoritative: 180 tuning units; selected configs `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06`, `dyna-c03`; 12 final roots with sizing max half-width 0.1428; exact action-remap semantics; action failure p=0.15 as no-op with ordinary step reward −0.1; observation corruption p=0.05 with the implemented support; RQ1/RQ2 definitions; and RQ3 32-interaction windows, directed tolerance 0.10, two-window stability and right-censoring at 256. No new experiment/reanalysis/post-hoc superiority family was introduced.
- Permanent deliverable retention applies: meaningful user-facing thesis milestones are committed under `thesis/archive/` before handoff; only genuinely accepted submission candidates belong under `thesis/final/`.

## Repository / writing maintenance completed for T-716

- The README now reflects T-716 as the current academic task and restores the full downstream lifecycle. `docs/context/POST_THESIS_LIFECYCLE.md` preserves the sequence **T-716 → actual T-712 feedback/corrections → T-713 final thesis freeze → T-720/T-721/T-722 defense work → T-800/T-801/T-802 final audits/delivery → T-803 standalone Windows package**.
- Conservative repository cleanup removed only proven-unused placeholder scaffolds: `data/raw`, `data/processed`, `data/external`, `artifacts/figures`, `artifacts/tables`, `artifacts/exports`. No docs, results, evidence, decisions, archived thesis artifacts, restored drafts or useful implementation history were deleted. See `docs/context/REPOSITORY_CLEANUP_2026-09-05.md`.
- Full repository/bibliography audits are retained under `docs/thesis/audits/`, including the 599-source/599-analysis corpus scan and the new multi-source re-audit.
- T-716 no longer uses a fixed bibliography-count target. Bibliography size is an output of validated claim coverage. Citation-ready status means **eligible for formal citation**, not “source of truth”.
- `docs/thesis/CLAIM_EVIDENCE_TREE.md` is the human-readable chapter/claim mapping; `research/bibliography/claim-evidence-map.json` is the machine registry. Claims combine all materially relevant formal sources, preserve contradictory/limiting evidence, distinguish context/informal material, and attach protocol/result statements to repository authorities. `scripts/validate_claim_evidence_map.py` plus `.github/workflows/claim-evidence-map.yml` fail closed on unknown/non-ready sources, weak single-source literature claims without exception, or missing project authority paths.
- Initial claim-map CI correctly failed on two stale decision filenames; the canonical DEC-058/DEC-060 paths were corrected and the subsequent validation run passed. Intermediate failures remain part of the audit history rather than being hidden.

## Scientific authority

DEC-058 and protocol-v2.0 remain immutable historical freeze authority. The current amendment is `docs/decisions/DEC-060_PROTOCOL_V2_1_RECOVERY_AND_COMPARISON_AMENDMENT.md` plus `configs/protocols/protocol-v2.1-final.json`: Q-Learning, SARSA, DQN, PPO and Dyna-Q+; common actual-interaction fairness; matched FN/FD/AN/AD Phase B; 12 roots, two held-out layouts, four conditions and 256-interaction horizon. RQ2 adaptation benefit remains `(FN-FD)-(AN-AD)`. RQ3 uses passive 32-interaction windows, tolerance 0.10 primary with 0.05/0.20 sensitivity, two-window stable recovery and `recovery_time=null` right-censoring. Root is the independent unit. No p-value superiority family or composite global ranking is introduced.

T-612 interpretation remains authoritative in `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`. Writing changes exposition and literature synthesis only; frozen outcomes and registered scientific media remain unchanged.

## Bibliography authority

The immutable bibliography writing-gate checkout remains `ada0d1aec7511098fd12610ae9e5abe7aea875cd`. Formal final-thesis citations must resolve to the synchronized citation-ready layer. Important analyzed records outside that layer remain visible as promotion candidates; if T-716 requires one formally, it must be promoted upstream in `ThesisBibliography` and re-synchronized rather than bypassed locally. Talks/transcripts may guide discovery/synthesis but cannot independently support exact equations, guarantees or numerical claims.

## Still intentionally gated

- `T-712` waits for **actual** supervisor/reviewer feedback; internal audits are not relabelled as external feedback.
- `T-713` waits for accepted T-716 content, resolved real feedback, authoritative person/declaration metadata and final Microsoft Word fields.
- Defense duration, slide count/template and live-demo requirements remain unfrozen until authoritative guidance is available.
- T-803 standalone Windows packaging remains post-thesis and does not block T-713.

## Exact next action

Produce T-716 from the T-714 full baseline plus reconciled restored-draft content, all T-715 scientific corrections, frozen T-611/T-612/T-613 authorities and the validated multi-source claim/evidence tree. Preserve or increase substantive academic coverage without filler, keep every result claim bounded to frozen evidence, and commit each delivered DOCX/QA milestone to `thesis/archive/` before handoff.
