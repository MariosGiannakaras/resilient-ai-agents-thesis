# T-716 full-content evidence-aware thesis plan

**Date:** 2026-09-05  
**Status:** COMPLETE — all 11 acceptance gates passed on 2026-09-05; accepted review semantic SHA-256 `b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1`

## Objective

Produce a substantially complete Greek thesis that is fuller and better supported than the archived T-714 and T-715 Word versions while preserving frozen protocol-v2.1 science. T-715 remains an auditable reader-scope/audit-hardening milestone, not the final manuscript.

The target is meaningful academic coverage, not word-count padding.

## Controlled inputs

1. **T-714 run #66** — primary full-content Word/layout/results baseline (~20.9k whole-document words).
2. **User-restored older drafts, especially stage9** — source of explanatory material only after reconciliation with current implementation/protocol authority.
3. **T-715 audit reconciliation** — mandatory corrections to tuning, disturbance semantics, metrics, roots/seeds, recovery and limitations.
4. **T-611/T-612/T-613** — sole quantitative/result authority and registered scientific media source.
5. **Synchronized ThesisBibliography** — formal external claims may cite only citation-ready sources, with non-ready material retained as context/promotion candidates.
6. **`CLAIM_EVIDENCE_TREE.md` + `docs/thesis/claim-evidence-map.json` + `BIBLIOGRAPHY_SOURCE_SELECTION_POLICY.md`** — mandatory claim-centred source synthesis and source-ranking policy before prose enters the final document.
7. **Official guidance + thesis style guide** — structure, formatting and administrative boundaries.

## Size and chapter balance

A useful planning range is roughly **25,000–27,000 whole-document words**, but the acceptance criterion is substantive coverage. If a section is complete at a lower count, filler is forbidden; if evidence-aware explanation requires more, the upper number is not a hard cap.

Indicative main-body balance:

| Chapter | Primary role | Planning range |
|---|---|---:|
| 1 — Introduction | motivation, problem, RQs, contribution, scope | 2.0–2.3k |
| 2 — Background/Related Work | algorithms, non-stationarity, uncertainty, robustness/adaptation/recovery, empirical RL | 4.0–4.8k |
| 3 — Methodology | environment, disturbances, fairness, tuning/sizing, metrics, statistics, reproducibility | 3.3–3.8k |
| 4 — Architecture/Implementation | Study-first architecture, information firewall, checkpoints, evidence lifecycle, PySide6 | 3.0–3.5k |
| 5 — Results | full accepted T-612/T-613 coverage | 3.1–3.6k |
| 6 — Discussion | RQ synthesis, literature comparison, mechanisms, limitations/validity | 3.5–4.1k |
| 7 — Conclusions/Future Work | answers, contribution, scoped future work | 1.7–2.1k |

## Multi-source bibliography rule

There is **no fixed reference quota** and no preselected final source count.

For every substantive external statement:

- assign/use a claim ID from `docs/thesis/claim-evidence-map.json`;
- inspect all relevant sources, not only the first citation-ready hit;
- compare primary, supporting, survey and contradictory/limiting evidence;
- prefer primary work for exact algorithm/equation/empirical claims;
- rank source fitness and scientific authority before publication year;
- when two or more sources are materially comparable in relevance, scientific quality, methodological strength and depth, prefer the more recent source by default;
- permit an older source to outrank a newer one when it is clearly stronger as primary/foundational evidence, authoritative scholarly work, methodological evidence or exact claim match, and record the reason;
- do not let a newer student thesis, informal tutorial/talk/transcript or weak derivative source displace a stronger scholarly primary source or authoritative book merely because of recency;
- cite multiple independent sources where they materially strengthen or qualify the statement;
- keep a single-source exception only when the claim is inherently source-specific or no independent support exists, with an explicit reason;
- never treat citation-ready status as truth status;
- never turn a literature principle into a claim that a paper prescribed the exact thesis protocol;
- never use external literature to override project code/protocol/frozen result evidence.

The final bibliography count is therefore the number of sources actually needed by validated claims, not a target such as 30, 32, 40 or 60. The full precedence rule is authoritative in `docs/thesis/BIBLIOGRAPHY_SOURCE_SELECTION_POLICY.md`.

## Source-promotion boundary

The full-corpus audit surfaced important analyzed works that are not currently citation-ready, including primary Q-learning/Dyna records and additional continual/non-stationary reviews. These remain visible in `CLAIM_EVIDENCE_TREE.md` as promotion candidates. If the final prose truly needs them, they must be promoted/verified in `ThesisBibliography` and re-synchronized immutably; they must not be cited through a local bypass.

Informal talks such as `SRC-49A9ACCA53` may guide discovery/synthesis. Exact claims must resolve to formal evidence. The verified Ding–Lavaei AAAI 2023 non-stationary CMDP paper is an example of a primary work discovered through that path; it is not silently promoted until the bibliography lifecycle creates an independent governed record.

## Chapter-specific reconstruction

### Chapter 1

- Restore richer stage9/T-714 motivation where still accurate.
- Define robustness, adaptation and recovery separately using the multi-source tree.
- Explain why the five methods are mechanism contrasts, not a universal tournament.
- State the actual-interaction fairness principle and controlled-testbed scope.

### Chapter 2

- Deepen Q/SARSA, DQN/replay, PPO and Dyna explanations from multiple sources.
- Add explicit treatment of action uncertainty, observation uncertainty, non-stationarity types, generalization versus online adaptation and temporal resilience/recovery.
- Include negative/limiting evidence: specialized methods do not dominate universally; robustification can trade nominal utility; deep continued learning has plasticity threats without implying inevitable thesis failure.
- Delimit Safe RL from the present resilience study.

### Chapter 3

Preserve and explain all frozen T-715-corrected facts:

- six candidate configs per method × three tuning-only roots × two development layouts × five methods = 180 tuning units;
- selected configs q-c06, sarsa-c06, dqn-c05, ppo-c06, dyna-c03;
- bounded search spaces and 8192-interaction tuning budget;
- 12 final roots selected by predeclared precision sizing;
- correct root/layout/RNG semantics;
- exact two action remaps;
- action failure p=.15 -> no-op with ordinary step reward −.1 unless terminal/reward rule applies;
- observation corruption p=.05 with the exact support implemented in `gridworld.py`;
- RQ1 trapezoidal actual-interaction time average;
- RQ2 Frozen loss / Adaptive loss / adaptation benefit definitions;
- RQ3 fixed 32-interaction windows, directed gap, tolerance .10, two-window stability and right-censoring at 256.

Literature explains why fairness/uncertainty/reporting distinctions matter; repository authorities define exact project choices.

### Chapter 4

- Restore the fuller useful implementation story while describing only the accepted architecture as current.
- Explain scientific core → Study-first backend → exact checkpoints/branches → validated/frozen evidence → PySide6 stored-evidence UI.
- Keep Streamlit/React/NiceGUI only as bounded implementation history if it improves explanation.
- Explain agent-visible versus evaluator-only information, deterministic seed streams, restart/provenance and checkpoint continuation state.
- Application screenshots remain implementation illustrations, never result evidence.

### Chapter 5

- Start from full T-714 Results coverage.
- Preserve all accepted T-612 values, intervals, denominators, recovery classifications and T-613 media bytes.
- Use literature only to explain why metrics are separated, not to validate/replace observed values.
- No new p-values, survival analysis, binomial significance family, post-hoc ranking or new estimand.

### Chapter 6

- Restore full T-714 discussion and use stage9 explanations only after evidence reconciliation.
- Link each interpretation to the appropriate claim cluster and distinguish observed result from mechanism hypothesis.
- Do not claim replay caused a result without an ablation; do not claim plasticity papers directly explain a small-GridWorld outcome.
- Expand internal/construct/statistical/external/reproducibility validity.
- Preserve explicit limits: one controlled GridWorld family, compact networks, bounded tuning, finite horizon, specific perturbations, no universal ranking, no safety guarantee, no transfer claim.

### Chapter 7

- Answer RQ1/RQ2/RQ3 only from frozen result claims.
- Future work may include broader environments, explicit changepoint/context detection, specialized continual-learning mechanisms, replay management and safe-constrained adaptation, but must be labelled as future work rather than evidence produced here.

## Repository organization

- `thesis/archive/` stores T-716 review milestones and QA before handoff.
- `thesis/final/` remains reserved for an accepted T-713 submission candidate.
- `docs/thesis/audits/` stores the full repository/bibliography/corpus audits.
- `docs/thesis/CLAIM_EVIDENCE_TREE.md` is the human claim synthesis.
- `docs/thesis/claim-evidence-map.json` is the machine registry; it intentionally lives outside the immutable synchronized bibliography import.
- `docs/thesis/BIBLIOGRAPHY_SOURCE_SELECTION_POLICY.md` controls quality/authority/recency precedence.
- cleanup may remove only proven-unused placeholder scaffolds; evidence/history/docs are preserved.

## Acceptance gates

T-716 cannot be marked complete unless:

1. substantive coverage is materially fuller than the compressed T-715 and improves the T-714 baseline without filler;
2. every validated T-715 scientific correction is present;
3. no frozen scientific value/classification/media byte is altered;
4. every substantive literature claim is registered and passes claim-evidence validation;
5. every formal source is citation-ready and every bibliography entry supports at least one concrete claim;
6. materially relevant multi-source support/limitations are retained rather than arbitrarily reduced to one citation;
7. source selection follows quality/relevance/authority first and recency among materially comparable sources, with older-over-newer exceptions justified when used;
8. no unresolved `SRC-*`, drafting note or invented official/person metadata remains;
9. structural/scientific DOCX QA passes;
10. final Word output is rendered and visually checked page-by-page for clipping, overlap, broken figures/tables, glyph issues and unintended blank pages;
11. the exact DOCX and QA/report identity are committed under `thesis/archive/` before user handoff.
