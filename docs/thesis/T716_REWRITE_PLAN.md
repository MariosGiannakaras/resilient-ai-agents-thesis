# T-716 full-content thesis rewrite plan

**Date:** 2026-09-05  
**Status:** controlled composition plan before the new DOCX build

## Objective

Produce a new full-content Greek thesis that is materially fuller and better supported than both the T-714 and T-715 Word versions, while preserving the frozen protocol-v2.1 evidence and every validated T-715 scientific correction. The target is substantive academic coverage, not word-count padding.

## Controlled composition inputs

1. **T-714 run #66** — full evidence-grounded review-ready composition (~20.9k whole-document words). This is the primary document/layout/results baseline.
2. **User-restored stage9** — representative old full-draft lineage (~19.8k words). Use only for explanatory content that survives reconciliation with current implementation/protocol authority.
3. **T-715 audit reconciliation** — mandatory scientific corrections/clarifications for tuning, disturbance semantics, metric definitions, root sizing, seed streams, recovery interpretation and limitations.
4. **Frozen T-611/T-612/T-613 authorities** — sole quantitative/scientific result source.
5. **Citation-ready ThesisBibliography** — sole formal external scientific citation source unless a separate bibliography-governance change promotes another source.
6. **Official guidance + T-701 style guide** — structure, formatting and reader-facing academic style.

## Target size and chapter balance

The target is approximately **25,000–27,000 whole-document words**, with no requirement to hit an exact number if additional text would be filler. Planned main-body coverage:

| Chapter | Target role | Approx. target words |
|---|---|---:|
| 1 — Introduction | motivation, problem, RQs, contribution, scope, roadmap | 2,000–2,300 |
| 2 — Background/Related Work | RL foundations, methods, non-stationarity, robustness/resilience/recovery, related evaluation literature | 4,000–4,600 |
| 3 — Methodology | environment, disturbances, fairness, tuning/sizing, seeds, metrics, statistical design, reproducibility | 3,300–3,700 |
| 4 — Architecture/Implementation | Study-first architecture, information firewall, checkpoints/branches, PySide6 application, evidence lifecycle | 3,000–3,400 |
| 5 — Results | preserve full accepted T-612/T-613 coverage and careful interpretation | 3,100–3,500 |
| 6 — Discussion | RQ synthesis, mechanisms, literature linkage, limitations, validity, transfer boundaries | 3,400–3,900 |
| 7 — Conclusions/Future Work | conclusions, contribution recap, bounded future work | 1,700–2,000 |

Front matter, glossary, bibliography and appendices bring the whole-document target above the main-body total.

## Content restoration/expansion by chapter

### Chapter 1

- Restore the fuller stage9/T-714 problem motivation instead of the compressed T-715 opening.
- Make explicit the distinction among static robustness, adaptation and temporal resilience/recovery.
- Explain why the five methods are mechanism contrasts rather than a universal ranking tournament.
- State the common actual-interaction fairness principle and why GridWorld is a controlled testbed, not the thesis subject.
- Keep contribution claims strictly project-scoped.

### Chapter 2

- Retain the mature T-714 related-work structure but deepen algorithm explanations using stage9 where accurate.
- Add direct literature support for action uncertainty, noisy/partial observations, generalization/OOD and process-based resilience.
- Add a short distinction between resilience, robustness, continual adaptation, generalization and safe RL; do not collapse them into synonyms.
- Explain DQN replay/target-network sensitivity and PPO implementation sensitivity without treating these mechanisms as robustness guarantees.
- Expand the Dyna/Dyna-Q+ mechanism discussion and why recency-driven exploration is relevant in changing environments.

### Chapter 3

- Preserve all T-714 protocol/evidence details.
- Integrate the complete T-715 audit hardening: exactly 180 tuning units; correct selected configs; bounded search spaces; 12-root precision sizing; six RNG streams; exact remappings; action failure p=0.15/no-op/−0.1 reward; observation corruption p=0.05 with correct support; RQ1/RQ2/RQ3 formulas; two-window stable recovery and right-censoring at 256.
- Add literature-backed explanation of why tuning opportunity, seeds and actual interactions are fairness concerns.
- Keep every protocol-specific numerical choice clearly identified as a thesis design decision rather than something prescribed by a paper.

### Chapter 4

- Restore the fuller implementation story from stage9 where it matches the accepted architecture.
- Explain the final implementation evolution only to the extent useful to the reader: scientific core → Study-first backend → immutable evidence → PySide6 presentation layer.
- Clarify exact checkpoint/branch semantics, agent-visible vs evaluator-only information, restart/reproducibility guarantees and why the UI never recomputes estimands.
- Include the two application screenshots only as explanatory implementation illustrations, never scientific evidence.

### Chapter 5

- Start from the full T-714 Results text, not T-715 compression.
- Preserve every accepted value, interval, denominator, recovery/non-recovery classification and figure/table identity.
- Do not introduce new p-values, new rankings, new post-hoc estimands or survival analysis.
- Improve reader guidance around what each figure establishes and what it does not establish.

### Chapter 6

- Restore the fuller T-714 discussion and integrate stage9 explanatory distinctions only after scientific reconciliation.
- Add stronger literature linkage for non-stationarity, replay/history, directed re-exploration, generalization and recovery concepts.
- Separate observed project results from plausible mechanism interpretation.
- Expand limitations: single GridWorld family, compact architectures, bounded tuning, finite horizon, no universal ranking, no direct safety claim, no transfer claim to robotics/Atari/continuous control.
- Use the safe non-stationary seminar only as a discovery/theory aid; exact statements on variation budgets/restarts must be tied to formal literature if formally cited.

### Chapter 7

- Restore a full contribution and answer-to-RQ recap.
- Keep future work explicitly downstream: broader environments, alternative changepoint models/detection, specialized continual-learning mechanisms, safety-constrained extensions and larger-scale evaluation.
- Do not rewrite future work as evidence already produced by this thesis.

## Formal bibliography plan

The current 17 references remain because all are actually used and verified. The next composition will add a bounded set of high-value citation-ready sources. The planned formal set is **32 references** (17 current + 15 additions), subject to final per-claim validation during composition.

### Existing 17 source identities

`SRC-701E163AC8`, `SRC-660560956D`, `SRC-4C34DF3E17`, `SRC-46CF36BC1E`, `SRC-4ED8B918E3`, `SRC-8D4F62D85D`, `SRC-6F4F8BE003`, `SRC-D38364B32C`, `SRC-D52DF7B9A4`, `SRC-32A0866AF8`, `SRC-CBA29E303A`, `SRC-CD5F67F3E6`, `SRC-5D0E7E5BD7`, `SRC-F909CABDEB`, `SRC-95C9DAEE68`, `SRC-0A4AFAC8E9`, `SRC-69D02D7E25`.

### Planned additions and writing role

| Source | Primary writing role |
|---|---|
| `SRC-01BBBA7EAB` | noisy/incomplete observations; observation uncertainty boundary |
| `SRC-0406E13B97` | safe continual RL under non-stationarity; useful contrast, not a safety claim for this thesis |
| `SRC-0882A9B2B0` | controlled generalization and train/test shift framing |
| `SRC-09DD20BA85` | bounded robustness and nominal-vs-robust trade-off framing |
| `SRC-0AEF7EF16A` | Bayesian robust RL and conservativeness/uncertainty framing |
| `SRC-0A594EACC0` | temporal/process-based resilience and recovery-curve framing |
| `SRC-0F8A6588DC` | controlled novelty/change injection and separate post-change metrics |
| `SRC-19C2E91926` | OOD/dynamics/observation-shift diagnostic framing |
| `SRC-21EBE15D15` | zero-shot generalization vs online adaptation distinction |
| `SRC-3A5E2C9E2C` | established Safe RL taxonomy used only to delimit safety vs resilience |
| `SRC-4000D2B40A` | diagnostic RL benchmark / behavioural test design |
| `SRC-70772C0629` | switching non-stationary MDP theory/context |
| `SRC-81A15E6905` | action replacement/failure and action-noise robustness models |
| `SRC-BE53B7970E` | Double-Q/maximization-bias context for deep value learning |
| `SRC-DBDFB80961` | Bayesian RL uncertainty/exploration background |

Every added reference must appear in at least one concrete literature-supported claim. Sources will not be added merely to increase the bibliography count.

## Informal material / YouTube policy

`SRC-49A9ACCA53` (safe RL in non-stationary environments seminar) is retained as useful theory/discovery material. Its valuable concepts include forgetting stale experience, variation-budget/restart trade-offs, adaptive change detection, joint utility/safety accounting and the distinction between within-task non-stationarity and explicit task boundaries. Because the stored source is an unstable automatic transcript, it will not be used alone for exact equations, guarantees or numerical claims. Formal claims use verified primary/citation-ready literature.

## Repository organization decisions

- Keep `artifacts/` as a generated-output contract even when its generic subfolders are currently sparse.
- Keep historical implementation/decision material; it explains superseded Streamlit/React/NiceGUI paths and prevents accidental architectural regression.
- Treat `docs/thesis/draft/` as the historical T-710/T-714 source lineage; T-716 output provenance will be recorded explicitly rather than silently overwriting archive artifacts.
- `thesis/archive/` stores the new T-716 review milestone and QA before handoff.
- `thesis/final/` remains reserved for the later accepted T-713 submission candidate.
- After T-716, a bounded cleanup may remove/rewrite placeholder-only scaffold READMEs that have no consumer, but no scientific/history/provenance artifact is removed during manuscript composition.

## Acceptance gates

T-716 is complete only if all are satisfied:

1. whole-document content is materially fuller than T-714 and near the 25k–27k target without filler;
2. all T-715 scientific corrections are present;
3. no frozen scientific value or registered scientific media byte is changed;
4. at least 30 formal references are verified and every bibliography entry is cited;
5. no unresolved `SRC-*`, drafting note or invented official/person metadata remains;
6. structural DOCX QA passes;
7. the final Word document is rendered page-by-page and visually inspected with no clipping/overlap/broken figures/tables/missing glyphs/unintended blank pages;
8. DOCX + QA/report are committed under `thesis/archive/` before user handoff.
