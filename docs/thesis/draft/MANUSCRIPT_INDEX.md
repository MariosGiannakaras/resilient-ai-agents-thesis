# T-710 Manuscript Index and Handoff Register

**Task:** T-710 — Draft complete Greek thesis from accepted evidence  
**Draft branch:** `thesis/t710-draft`  
**Scientific authority:** accepted T-611/T-612/T-613 chain only  
**Bibliography snapshot:** `ada0d1aec7511098fd12610ae9e5abe7aea875cd`  
**Final editable composition:** T-711, not this task

## Manuscript order

1. `FRONT_MATTER_SUMMARIES.md` — Greek summary/keywords and English abstract/keywords.
2. `CHAPTER_01_INTRODUCTION.md` — Εισαγωγή.
3. `CHAPTER_02_BACKGROUND_RELATED_WORK.md` — Θεωρητικό Υπόβαθρο και Σχετική Βιβλιογραφία.
4. `CHAPTER_03_METHODOLOGY.md` — Μεθοδολογία και Πειραματικός Σχεδιασμός.
5. `CHAPTER_04_SYSTEM_ARCHITECTURE.md` — Αρχιτεκτονική και Υλοποίηση του Ερευνητικού Συστήματος.
6. `CHAPTER_05_RESULTS.md` — Πειραματικά Αποτελέσματα.
7. `CHAPTER_06_DISCUSSION.md` — Συζήτηση.
8. `CHAPTER_07_CONCLUSIONS.md` — Συμπεράσματα και Μελλοντική Εργασία.
9. `GLOSSARY_ACRONYMS.md` — glossary/acronym source for the final alphabetical terminology section.
10. `APPENDIX_DRAFT.md` — appendix narrative and artifact-placement authority.

`T710_EVIDENCE_MAP.md` is a drafting control and is not itself a thesis chapter.

## Citation placeholder contract

During T-710, formal external citations use stable placeholders of the form:

`[@SRC-XXXXXXXXXX]`

Multiple sources may appear in one bracket separated by semicolons. These placeholders are not the final visible citation format. T-711 converts the validated IDs to consistent IEEE numeric citations and builds the formatted reference list from canonical bibliography metadata.

No final prose may cite a source merely because it exists in the full research corpus. Every `SRC-*` placeholder used by the manuscript must resolve in `research/bibliography/citation-ready/manifest.csv`.

## Validated citation-ready IDs used in the manuscript

The following IDs were checked against the imported citation-ready manifest from bibliography source commit `84d62ec3eb18e1d3565625bc02c289131282ea27`:

- `SRC-701E163AC8` — RL/TD/Q-Learning/SARSA/Dyna foundations.
- `SRC-D52DF7B9A4` — focused Q-Learning/SARSA TD-control support.
- `SRC-32A0866AF8` — DQN foundation.
- `SRC-CBA29E303A` — experience-replay design sensitivity.
- `SRC-CD5F67F3E6` — PPO foundation and clipped objective.
- `SRC-5D0E7E5BD7` — PPO/deep-policy-gradient implementation sensitivity.
- `SRC-660560956D` — non-stationarity and reactive adaptation/replay context.
- `SRC-4C34DF3E17` — loss of plasticity in deep continual learning.
- `SRC-46CF36BC1E` — primacy bias in deep RL.
- `SRC-6F4F8BE003` — ICLR 2025 online non-stationary context-driven RL; observed-context boundary retained.
- `SRC-D38364B32C` — 2025 partial-model adaptation in deep model-based RL; direct-transfer limits retained.
- `SRC-4ED8B918E3` — empirical design in RL.
- `SRC-8D4F62D85D` — deep-RL empirical/reproducibility sensitivity.
- `SRC-69D02D7E25` — time-limit termination/truncation semantics.

### Explicitly excluded from formal citation

`SRC-F6BD3A6B18` is verified in the full corpus but is **not present in the citation-ready manifest**. An early T-710 draft used it for Dyna background; the citation was removed during manuscript validation. Dyna claims now rely on citation-ready `SRC-701E163AC8`. This exclusion must remain unless that source is formally promoted upstream and a later immutable bibliography sync is accepted.

## T-613 quantitative asset placement register

The manuscript refers only to finalized T-613 asset IDs. Primary planned placements are:

### Methodology / architecture
- `FIG-METHOD-026-EXPERIMENT-FLOW` — experiment flow and exact checkpoint before FN/FD/AN/AD.
- `FIG-METHOD-027-RQ-MAP` — RQ-to-estimand/output map.
- `FIG-METHOD-028-LINEAGE` — accepted evidence lineage and explicit failed-attempt exclusion.

### RQ1
- `FIG-RQ1-002-FINAL` — final nominal return.
- `FIG-RQ1-003-TIME-AVERAGE` — interaction-axis time-average return.
- `FIG-RQ1-004-FINAL-ROOTS` — root-level final nominal distribution.
- `FIG-RQ1-005-TIME-ROOTS` — root-level time-average distribution.
- `FIG-RQ1-007-CONTRASTS` — declared paired method contrasts.

### RQ2
- `FIG-RQ2-008-ADAPTATION` — adaptation benefit.
- `FIG-RQ2-009-LOSSES` — Frozen versus Adaptive loss.
- `FIG-RQ2-010-CONDITIONS` — condition-specific adaptation view.
- `FIG-RQ2-012-BENEFIT-ROOTS` — root-level benefit distribution.
- `FIG-RQ2-013-HEATMAP` — stored mean adaptation benefit heatmap.
- `FIG-RQ2-014-CONTRASTS` — declared RQ2 paired contrasts.
- `FIG-RQ2-015-PAIRED-ROOTS` — Frozen-to-Adaptive root diagnostics.

### RQ3
- `FIG-RQ3-016-TRAJECTORIES` — directed-gap trajectories at primary tolerance.
- `FIG-RQ3-017-RECOVERED` — recovered roots and right-censoring.
- `FIG-RQ3-018-RESTRICTED` — censoring-aware restricted recovery delay.
- `FIG-RQ3-019-CONDITIONAL` — conditional observed recovery time; must display recovered n.
- `FIG-RQ3-021-ROOT-TRAJECTORIES` — detailed stored root trajectories.
- `FIG-RQ3-022-CENSORING` — recovered/right-censored composition.
- `FIG-RQ3-023-SENSITIVITY` — predeclared tolerance sensitivity.
- `FIG-RQ3-024-CONTRASTS` — recovery-status and restricted-delay paired contrasts.
- `FIG-RQ3-025-TIMELINE` — recovery/confirmation timeline without fake recovery times.

All IDs above exist in `results/thesis-assets/protocol-v2.1-final/captions.md`. T-711 chooses the exact main-text versus appendix placement and inserts the corresponding registered SVG/PDF/PNG/table asset without retyping numerical values.

## Unresolved optional front matter

These items are intentionally not invented during T-710:

- dedication;
- acknowledgements;
- any supervisor identity or supervisor-specific wording not supplied by the user;
- final copyright/plagiarism declaration wording when exact institutional text is required;
- final page numbering and layout.

Their absence does not change the scientific manuscript. T-711 incorporates only authoritative text actually available at composition time.

## T-711 boundary

T-711 owns:

- final `.docx` construction;
- Times New Roman/A4/spacing and real Word Heading styles;
- automatic TOC and lists of figures/tables;
- caption fields and Word cross-references;
- final IEEE numeric numbering/reference formatting from the validated `SRC-*` set;
- equation numbering where useful;
- exact T-613 asset insertion and layout;
- final appendix ordering and pagination;
- field updates and visual QA.

T-711 must not alter T-612 values, derive new statistical results, replace right-censored `null` recovery times with 256, or use application screenshots as quantitative evidence.