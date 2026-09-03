# T-710 Chapter Evidence Map

**Task:** T-710 — complete Greek thesis drafting  
**Status:** active drafting authority for the manuscript checkpoint  
**Language:** Greek main text  
**Bibliography snapshot:** `ada0d1aec7511098fd12610ae9e5abe7aea875cd`  
**Scientific result authority:** T-611/T-612/T-613 only

This map is a drafting control, not a new scientific source. It records where every chapter obtains project facts, external scientific support, quantitative results and figures/tables. It must remain narrower than the canonical authorities and must never redefine an estimand, protocol parameter or result.

## Global claim rules

- External scientific/factual claims: use only verified `research/bibliography/citation-ready/` sources.
- Project methodology/configuration claims: use accepted repository decisions, frozen protocol/configuration and implementation records.
- Numerical/result claims: use only T-612 accepted analysis and T-613 registered assets derived from the T-611 freeze.
- Example theses: structure/presentation context only; never scientific support.
- Application screenshots: implementation/workflow illustration only; never quantitative evidence.
- Right-censored RQ3 roots retain `recovery_time=null`; the horizon value 256 is not an observed recovery time.
- No p-value superiority language, composite ranking, universal-winner claim or post-hoc threshold selection.

## Chapter 1 — Εισαγωγή

**Purpose:** define the uncertainty/non-stationarity problem, exact thesis objective, RQs, contribution and scope.

**Project authorities:** approved Greek/English title; `docs/context/PROJECT_CONTEXT.md`; `docs/research/RQ_EVIDENCE_TRACEABILITY.md`; `configs/protocols/protocol-v2.1-final.json`; T-612 for a bounded contribution summary only.

**External support:** citation-ready sources on non-stationarity, continual/adaptive RL, robustness/resilience and the recent 2025 writing-gate additions. Do not front-load algorithm detail.

**Result boundary:** at most a concise high-level contribution statement; detailed values belong in Chapters 5–6.

## Chapter 2 — Θεωρητικό Υπόβαθρο και Σχετική Βιβλιογραφία

**Purpose:** provide only the theory and related work required to understand the five retained methods, uncertainty mechanisms, resilience/adaptation and recovery.

**Primary external evidence:** `research/bibliography/citation-ready/` plus the writing-oriented upstream notes imported under `research/bibliography/notes/`.

**Required concepts:** MDP/RL; Q-Learning; SARSA; DQN; PPO; Dyna/Dyna-Q+; non-stationary environments; action/observation uncertainty; continual/adaptive RL; resilience/adaptation/recovery; related empirical comparison methodology.

**Freshness additions:**
- `SRC-6F4F8BE003` — online RL in non-stationary context-driven environments; use for stability/plasticity and recurring-context discussion, preserving its observed-context limitation.
- `SRC-D38364B32C` — partial models for adaptive model-based RL; use for local change, stale information/model organization and modular adaptation, without equating its deep Dyna-Q setting to the thesis's bounded tabular Dyna-Q+.

**Boundary:** do not use the literature to retroactively change protocol-v2.1 or to claim that one algorithm family is generally superior.

## Chapter 3 — Μεθοδολογία και Πειραματικός Σχεδιασμός

**Primary authorities:**
- `configs/protocols/protocol-v2.1-final.json`;
- DEC-058 historical protocol-v2.0 freeze;
- DEC-060 protocol-v2.1 recovery/direct-comparison amendment;
- `docs/research/RQ_EVIDENCE_TRACEABILITY.md`;
- DEC-062 only where execution lineage/failure-recovery provenance must be explained.

**Must state exactly:**
- five methods: Q-Learning, SARSA, DQN, PPO, Dyna-Q+;
- common actual-environment-interaction fairness axis;
- two 7×7 held-out layouts, 12 independent roots;
- Phase A budget 8,192 interactions and probes at 0/512/1024/2048/4096/8192;
- matched Phase B FN/FD/AN/AD with four conditions and 256-interaction horizon;
- RQ1 final nominal + time-average estimands;
- RQ2 Frozen loss, Adaptive loss, adaptation benefit `(FN-FD)-(AN-AD)`;
- RQ3 passive 32-interaction windows, tolerance 0.10, sensitivity 0.05/0.20, two-window stability, right-censoring;
- root as independent unit; equal layout reduction; pointwise 95% Student-t intervals by actual root n; root-paired A-minus-B contrasts;
- no p-value family, no multiplicity correction, no composite resilience score.

**Figures/tables:** T-613 experiment-flow and RQ/evidence schematics where registered; exact placement deferred to T-711.

## Chapter 4 — Αρχιτεκτονική και Υλοποίηση του Ερευνητικού Συστήματος

**Primary authorities:** `src/resilient_agents/`; `docs/context/PROJECT_CONTEXT.md`; DEC-059; DEC-061; `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`; Study/evidence implementation and accepted task records T-529/T-534/T-535/T-536.

**Core narrative:** framework-neutral Study backend is scientific authority; PySide6/Qt is a thin experiment-first presentation/control layer. Filesystem evidence is authoritative; indexes are rebuildable caches. RNG, checkpoints, branch construction, metrics, reduction, recovery classification, validation and finalization remain backend-owned.

**Application surfaces:** Experiment / Run / Results / Evidence. Live GridWorld is lossy, non-blocking and presentation-only. Frozen/Adaptive are simultaneous matched deployment regimes, not algorithms.

**Boundary:** avoid code-listing/tutorial content; implementation detail is included only when it explains reproducibility, scientific isolation or user-facing evidence inspection.

## Chapter 5 — Πειραματικά Αποτελέσματα

**Primary authority:** `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md` and machine-readable T-612 exports. Figures/tables only from `results/thesis-assets/protocol-v2.1-final/` and `asset-manifest.json`.

**RQ1 facts to preserve:** final probe: Q-Learning/SARSA/Dyna-Q+ = -0.100 with zero between-root variation; DQN/PPO = -1.862 means with wider intervals. Time-average: Dyna-Q+ -0.485, SARSA -1.611, Q-Learning -1.628, DQN -2.862, PPO -2.904.

**RQ2 facts to preserve:** large positive adaptation benefit for tabular methods under persistent action remapping; Dyna-Q+ positive but smaller in key remap comparisons; DQN smaller/uncertain; PPO approximately no aggregate remap benefit; no clear aggregate advantage under 15% action failure; Q-Learning/SARSA negative adaptation benefit under observation corruption.

**RQ3 facts to preserve:** at tolerance 0.10, Q-Learning and SARSA recover 12/12 roots for both remaps; cycle Dyna-Q+ 12/12, DQN 2/12, PPO 1/12; swap Dyna-Q+ 8/12, DQN 8/12, PPO 4/12. Conditional recovery time must always be paired with recovered proportion/censoring context.

**Boundary:** report values and uncertainty first; defer mechanism-level interpretation and literature comparison to Chapter 6.

## Chapter 6 — Συζήτηση

**Authorities:** T-612 interpretation/limitations; refreshed citation-ready literature; protocol and implementation boundaries.

**Required themes:**
- sample-efficiency versus final nominal performance;
- condition-dependent value of continued adaptation;
- distinction between adaptation benefit and recovery speed;
- right-censoring and threshold sensitivity;
- why Dyna-Q+ planning does not imply universal adaptation superiority;
- observed-context versus hidden-change assumptions;
- stale information/model organization as a plausible literature-grounded mechanism, not a causal result of this experiment;
- internal/external/construct/statistical validity boundaries.

**Boundary:** no new estimand, significance test or post-hoc mechanism claim.

## Chapter 7 — Συμπεράσματα και Μελλοντική Εργασία

**Authorities:** accepted RQ1/RQ2/RQ3 findings and Chapter 6 limitations.

**Required output:** answer each RQ directly; summarize contribution; state bounded implications; propose future work that follows from limitations rather than pretending untested claims were established.

Potential future-work classes: broader tasks/layout families and budgets; other non-stationarity/change mechanisms; explicit change detection/context inference; richer model-based modular adaptation; additional independent roots when justified; real-world or higher-dimensional environments; safe/constraint-aware adaptation as a distinct future problem.

## T-711 handoff boundary

T-710 produces the complete evidence-grounded Greek manuscript and stable placement intentions. T-711, not T-710, owns final `.docx` composition, Word styles/fields, automatic TOC/lists, final pagination, cross-references and manual `ASSET-*` placement register.