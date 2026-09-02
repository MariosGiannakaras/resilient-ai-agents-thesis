# Thesis Structure and Style Guide

**Task:** T-701  
**Derived:** 2026-09-03  
**Status:** canonical WP7 structure/presentation guide after T-700 verification and comparative review of user-supplied ICE thesis examples  
**Scientific authority:** none; this document controls structure, writing and presentation only

## 1. Authority and scope

This guide combines three distinct evidence classes without conflating them:

1. **OFFICIAL** — current Department/University guidance re-verified in T-700. This is mandatory unless a later official/supervisor instruction supersedes it.
2. **EXAMPLE** — contextual patterns observed across user-supplied completed theses from the same Department. These are descriptive, not authoritative.
3. **PROJECT** — decisions required by the scientific design, frozen protocol, T-612 analysis and T-613 evidence package of this thesis. These may deliberately be stricter than typical example-thesis practice.

Scientific claims, citations, numerical results and interpretations never come from the example theses. They come from citation-ready `ThesisBibliography` evidence, accepted repository decisions/configurations and the frozen T-611/T-612/T-613 evidence chain.

## 2. Example corpus and review method

### 2.1 Corpus identity

The user supplied 22 files labelled `example-theses 1` through `example-theses 22`.

Integrity review found that `example-theses 1.pdf` and `example-theses 10.pdf` are byte-for-byte identical. Therefore:

- uploaded files: **22**;
- unique completed-thesis documents: **21**;
- duplicate documents are counted once in comparative observations.

The examples span older and newer Department practice, including documents dated from the 2020–2021 period through 2025. The corpus covers theoretical surveys, software-engineering projects, hardware/embedded projects, machine-learning/computer-vision implementations, simulations and experimental model comparisons.

The examples are not equally relevant to this project. More weight is placed on examples that share one or more of the following characteristics:

- explicit research question or comparative aim;
- machine learning / artificial intelligence;
- experimental or simulation evidence;
- multiple methods/models compared under common metrics;
- clear separation of literature, methods, experiment and conclusions;
- recent Department formatting practice.

### 2.2 High-value structural analogues

The following anonymized labels are used only to describe structural observations:

| Example | Why it is useful | Limitations as a model for this thesis |
|---|---|---|
| E02 (2025, ML/CV) | Recent Department practice; explicit training, performance evaluation, metrics, limitations and conclusions/future work. | Code/implementation detail is much heavier than appropriate for this research-first thesis; evaluation is less statistically rigorous than T-612. |
| E03 (2025, DOCX, CV) | Direct evidence of modern Word styling; clean literature → methods → implementation → conclusions sequence; rich front matter. | Implementation chapter is dominated by code, tool installation and packaging detail; no standalone experimental Discussion. |
| E05 (2021, ML model comparison) | Compact example of theory → methods/models → experiments/evaluation → conclusions. | Uses a simplified “best model” conclusion that would exceed this project’s predeclared statistical claims. |
| E09 (2022, ML/simulation) | Distinct simulation and results treatment; technical/theoretical depth before empirical results. | Background is broader and more domain-survey-heavy than needed here. |
| E19 (2023, mobile ML) | Clear application/model-training/implementation separation and extensive UI material. | Application-first organization would wrongly make software the main thesis contribution here. |
| E22 (2020–2021, experimental autonomous system) | Strongest general structural analogue: Introduction → Literature Review → Materials and Methods → Experimental Study → Conclusions/Future Work; rich lists/glossary/appendix. | This thesis needs a separate Discussion because its three RQs, paired contrasts, sensitivity analysis and right-censoring create a more complex interpretation layer. |

### 2.3 Review dimensions

The comparative review considered:

- front-matter ordering;
- title/committee/declaration practice;
- summaries/abstracts and keywords;
- TOC, figures/tables lists, abbreviations/glossary;
- number and purpose of top-level chapters;
- separation of background/related work, methodology, implementation, experiments, results, discussion and conclusions;
- treatment of limitations and future work;
- code/pseudocode/equation treatment;
- figure/table/screenshot usage;
- citation/reference style;
- appendix usage;
- Word/layout conventions where inspectable;
- academic register and common weak patterns that should not be copied.

No example prose, image, figure, table, code or scientific result is reused.

## 3. Cross-example findings

### 3.1 Front matter

**Observation:** Greek summary material is effectively universal across the unique examples, and English abstract material is present in nearly all modern/technical examples. Author declarations are also a strong Department convention. Acknowledgements are common but not universal. Lists of figures/tables, abbreviation lists and appendices vary substantially between individual works.

**Decision:** do not use majority voting for front matter. Follow the current official T-700 ordering in full, because official guidance is stronger than inconsistent historical practice.

**Traceability:** OFFICIAL > EXAMPLE.

### 3.2 Number of substantive chapters

The corpus ranges from compact 4–5 chapter works to highly fragmented 10+ chapter hardware/application reports. The research-oriented analogues cluster more naturally around approximately 5–7 substantive chapters, with detail expressed through subsection hierarchy rather than a separate top-level chapter for every technical component.

**Decision:** use seven substantive chapters. This is enough to separate distinct scientific functions while avoiding fragmentation.

**Traceability:** EXAMPLE + PROJECT.

### 3.3 Introduction pattern

Across useful examples, the Introduction typically contains some combination of:

- motivation/context;
- thesis objective;
- scope/problem statement;
- methodology at a high level;
- contribution/innovation;
- document structure.

Recent/research-oriented examples are strongest when they state purpose and structure explicitly rather than beginning with many pages of generic domain history.

**Decision:** Chapter 1 must define the exact problem, RQs, contribution and scope early. Generic “history of AI” material is excluded unless it directly supports a later technical concept.

**Traceability:** EXAMPLE + PROJECT.

### 3.4 Related work / theoretical background

The examples vary considerably. Some create a dedicated literature-review chapter; others distribute background across several technology chapters; application-heavy works often provide generic introductions to programming languages/frameworks.

The strongest analogue, E22, explicitly separates `Βιβλιογραφική Ανασκόπηση` from `Υλικά και Μέθοδοι`. E03 also uses a dedicated `Βιβλιογραφική Ανασκόπηση` chapter.

**Decision:** combine theoretical background and related research in one coherent Chapter 2, but internally distinguish foundational concepts from empirical related work. Do not create filler sections such as “What is Python”, “What is GitHub”, a broad history of AI, or generic software-library descriptions unless they are scientifically necessary.

**Traceability:** EXAMPLE + PROJECT + citation-ready bibliography.

### 3.5 Methodology versus implementation

Application-centric examples frequently blur scientific method and software implementation or allocate very large sections to code listings, installation instructions, database tables and screenshots. E02/E03/E19 demonstrate this pattern clearly. E22 more cleanly places system construction inside Materials and Methods and then creates a separate experimental study.

**Decision:** keep two distinct top-level functions:

- Chapter 3 — scientific methodology and experimental design;
- Chapter 4 — architecture and implementation of the research system.

This prevents implementation detail from obscuring the experimental contract and lets the reader reproduce the science independently of the UI.

**Traceability:** PROJECT, supported by EXAMPLE.

### 3.6 Experimental evidence and Results

ML/simulation examples that perform real empirical comparison usually allocate a distinct experiment/evaluation/results section or chapter. E05 has `Πειράματα – Αξιολόγηση`; E09 has a distinct Results chapter; E22 has a separate `Πειραματική Μελέτη` with an `Αποτελέσματα` section; E02 has a full `Αξιολόγηση Απόδοσης` chapter.

**Decision:** Chapter 5 is a dedicated Results chapter organized by frozen RQ/estimand, not by software component or chronological implementation history.

**Traceability:** EXAMPLE + PROJECT/T-612.

### 3.7 Discussion

A standalone Discussion chapter is uncommon in the supplied examples. Most works move from experiments/results directly to conclusions, or interpret results inside the evaluation chapter.

For this project that convention is insufficient. T-612 contains:

- three conceptually distinct RQs;
- different estimands for nominal learning, adaptation benefit and recovery;
- root-paired method contrasts;
- Student-t uncertainty intervals;
- sensitivity thresholds;
- explicit right-censoring;
- disturbance-specific and method-specific heterogeneity.

**Decision:** create a standalone Chapter 6, `Συζήτηση`. Results report what the accepted analysis shows; Discussion explains what those results mean, relates them to literature, evaluates limitations and avoids overclaiming.

**Traceability:** PROJECT. This is an intentional improvement over common example practice.

### 3.8 Limitations / threats to validity

Limitations appear inconsistently across examples. E02 explicitly includes implementation limitations; many others mention limitations informally in conclusions or future work. Systematic validity-threat treatment is not a strong historical consensus.

**Decision:** include explicit `Απειλές προς την εγκυρότητα` and `Περιορισμοί / όρια γενίκευσης` subsections in Chapter 6. Negative/null/nonuniform results must not be hidden.

**Traceability:** PROJECT scientific-integrity requirements; examples provide only secondary support.

### 3.9 Conclusions and future work

Future-work material is common across the corpus and is frequently coupled with final conclusions. Research-oriented examples typically summarize the work and then identify extensions.

**Decision:** Chapter 7 contains final RQ answers, contribution recap, bounded implications and future work. It must not introduce new analysis or new evidence.

**Traceability:** OFFICIAL + EXAMPLE + PROJECT.

### 3.10 Figures, tables and screenshots

The examples vary from sparse figures to extremely screenshot-heavy application/hardware documents. Application-first theses often devote many pages to UI screenshots or code images. Research-oriented works use figures more selectively to explain method and experiment.

**Decision:**

- quantitative claims use T-613 reproducible figures/tables, never UI screenshots;
- application screenshots are illustrative implementation/workflow evidence only;
- main text includes only the figures/tables needed for the argument;
- root-level diagnostics, complete contrast matrices, secondary sensitivity views and extended provenance are moved to appendices where appropriate;
- avoid screenshots of source code when pseudocode, equations or brief textual snippets communicate the idea more clearly.

**Traceability:** PROJECT/T-613; EXAMPLE used mainly to identify overuse patterns to reject.

### 3.11 Citation practice

Numeric bracket referencing is the dominant convention among the technically closest engineering/ML examples inspected in depth. The current Department guide accepts multiple consistent systems rather than mandating a single one.

**Decision:** use IEEE numeric references for WP7, subject to later explicit supervisor override.

**Traceability:** OFFICIAL permissibility + EXAMPLE convention + PROJECT engineering fit.

### 3.12 Word presentation

E03 provides direct recent DOCX evidence consistent with the official guide: A4, Times New Roman 11 pt main text, 1.5 line spacing, larger bold heading styles and structured heading hierarchy. Historical examples vary in margins, headers/footers, page-number placement and cosmetic spacing.

**Decision:** official T-700 Word rules control; recent example formatting is used only to confirm practical feasibility. The final document uses real Word styles/fields rather than visual imitation through manual formatting.

**Traceability:** OFFICIAL; recent EXAMPLE corroboration.

## 4. Final chapter architecture

The final manuscript architecture is seven substantive chapters.

### Chapter 1 — Εισαγωγή

**Purpose:** establish the research problem and contribution without preloading the reader with unnecessary implementation detail.

Planned subsections:

1.1 Αντικείμενο και κίνητρο  
1.2 Πρόβλημα και ερευνητικό πλαίσιο  
1.3 Σκοπός και στόχοι  
1.4 Ερευνητικά ερωτήματα  
1.5 Συνεισφορά της εργασίας  
1.6 Πεδίο, παραδοχές και οριοθέτηση  
1.7 Δομή της διπλωματικής

**Evidence role:** official approved topic; project RQ authority; high-level citation-ready motivation evidence; no final-result detail beyond concise contribution framing.

**Avoid:** generic AI history, broad unsupported claims, final-result cherry-picking, implementation chronology.

### Chapter 2 — Θεωρητικό Υπόβαθρο και Σχετική Βιβλιογραφία

**Purpose:** provide exactly the concepts and prior evidence necessary to understand the five methods, uncertainty/resilience problem and research gap.

Planned subsections:

2.1 Πράκτορες και διαδοχική λήψη αποφάσεων  
2.2 Markov Decision Processes και Reinforcement Learning  
2.3 Q-Learning και SARSA  
2.4 Deep Q-Network  
2.5 Proximal Policy Optimization  
2.6 Dyna-Q και Dyna-Q+  
2.7 Αβεβαιότητα και δυναμικές μεταβολές περιβάλλοντος  
2.8 Ανθεκτικότητα, προσαρμογή και ανάκαμψη  
2.9 Σχετικές εμπειρικές εργασίες και πειραματικές προσεγγίσεις  
2.10 Ερευνητικό κενό και θέση της παρούσας εργασίας

**Evidence role:** citation-ready `ThesisBibliography` only for external scientific claims. Repository design history may explain project choices but cannot substitute for literature evidence.

**Avoid:** textbook-length introductions to programming languages/libraries; unrelated AI taxonomy; sources outside the verified citation-ready layer unless first promoted through bibliography governance.

### Chapter 3 — Μεθοδολογία και Πειραματικός Σχεδιασμός

**Purpose:** make the experiment scientifically reproducible and separate predeclared design from implementation mechanics.

Planned subsections:

3.1 Ερευνητική προσέγγιση και αρχές συγκρισιμότητας  
3.2 GridWorld ως ελεγχόμενο πειραματικό testbed  
3.3 Τελικές μέθοδοι και fairness boundaries  
3.4 Phase A: ανεξάρτητη ονομαστική μάθηση και checkpoints  
3.5 Phase B: matched FN/FD/AN/AD design  
3.6 Μηχανισμοί αβεβαιότητας / disturbance conditions  
3.7 RQ1: nominal-learning estimands  
3.8 RQ2: resilience και adaptation-benefit estimand  
3.9 RQ3: recovery definition, passive windows και right-censoring  
3.10 Roots, layouts, interaction budgets και πειραματικός πίνακας  
3.11 Στατιστική ανάλυση, paired contrasts και uncertainty intervals  
3.12 Reproducibility, provenance, exclusions και scientific firewall

**Evidence role:** DEC-060/frozen protocol-v2.1, accepted configs, predeclared analysis contract, T-611 provenance; bibliography where methodological rationale needs external support.

**Critical wording:** describe the design as frozen/predeclared where that is objectively true. The failed 216-job attempt may be documented as provenance/recovery history but never mixed into accepted results.

### Chapter 4 — Αρχιτεκτονική και Υλοποίηση του Ερευνητικού Συστήματος

**Purpose:** explain how the research design was realized faithfully in software and how the user-facing application supports inspection without becoming the scientific authority.

Planned subsections:

4.1 Συνολική αρχιτεκτονική  
4.2 GridWorld/environment και scientific core  
4.3 Υλοποίηση των πέντε agent strategies  
4.4 Study lifecycle και deterministic planning/execution  
4.5 Checkpoints, continuation state, settlement και recovery boundaries  
4.6 Evidence bundles, manifests, integrity validation και provenance  
4.7 PySide6 desktop research application  
4.8 Experiment → Run → Results → Evidence user workflow  
4.9 Scientific firewall μεταξύ UI και execution/analysis  
4.10 Software validation και reproducibility controls

**Evidence role:** accepted code/ADR/architecture/test records. Use diagrams and selective pseudocode. Full code remains in repository.

**Main-text asset rule:** a small number of architecture/workflow/application images only. Detailed UI walkthroughs and code listings belong in appendix or are omitted.

### Chapter 5 — Πειραματικά Αποτελέσματα

**Purpose:** present accepted final outcomes exactly as T-612/T-613 define them, without changing estimands or adding post-hoc analysis.

Planned subsections:

5.1 Δομή παρουσίασης και κανόνες ανάγνωσης  
5.2 RQ1 — Ονομαστική μάθηση  
5.3 RQ2 — Ανθεκτικότητα και όφελος προσαρμογής  
5.4 RQ3 — Ανάκαμψη μετά τη μεταβολή  
5.5 Προδηλωμένες άμεσες συγκρίσεις μεθόδων  
5.6 Sensitivity analysis για tolerances 0.05 / 0.10 / 0.20  
5.7 Συνοπτική εμπειρική απάντηση στα RQ1–RQ3

**Evidence role:** T-612 analysis package and T-613 quantitative assets exclusively for final numeric claims.

**Hard restrictions:**

- no global composite winner score;
- no formal significance claim not present in T-612;
- no replacement of right-censored `recovery_time=null` by 256;
- no sensitivity threshold selected because it gives a preferred result;
- no historical failed-attempt outcomes.

### Chapter 6 — Συζήτηση

**Purpose:** interpret, contextualize and delimit the results without repeating the entire Results chapter.

Planned subsections:

6.1 Ερμηνεία RQ1  
6.2 Ερμηνεία RQ2  
6.3 Ερμηνεία RQ3  
6.4 Συγκριτικές παρατηρήσεις για tabular, model-based και deep-RL συμπεριφορά  
6.5 Συσχέτιση με τη σχετική βιβλιογραφία  
6.6 Μη ομοιόμορφα, αρνητικά ή μη αναμενόμενα ευρήματα  
6.7 Απειλές προς την εγκυρότητα  
6.8 Περιορισμοί και όρια γενίκευσης

**Evidence role:** T-612 bounded interpretation + refreshed citation-ready bibliography.

**Critical distinction:** observations, uncertainty, interpretation and limitations must remain distinguishable. A numerical ordering is not automatically a superiority conclusion.

### Chapter 7 — Συμπεράσματα και Μελλοντική Εργασία

**Purpose:** close the research argument, answer the RQs concisely and identify defensible extensions.

Planned subsections:

7.1 Συνολική αποτίμηση  
7.2 Κύριες συνεισφορές  
7.3 Τελικές απαντήσεις στα RQ1–RQ3  
7.4 Πρακτικές και ερευνητικές προεκτάσεις  
7.5 Μελλοντική εργασία

**Evidence role:** synthesis only; no new experiment, metric or citation-dependent claim introduced without support.

## 5. Front and final matter contract

The review-ready Word thesis will contain, in the official T-700 order:

- Greek cover/title page;
- English title page;
- current official copyright/plagiarism declarations;
- optional dedication only if the user chooses one;
- optional acknowledgements only if the user chooses them;
- Greek summary and keywords;
- English abstract and keywords;
- automatic Table of Contents;
- automatic List of Figures;
- automatic List of Tables;
- controlled glossary / alphabetical term index;
- abbreviation/acronym list integrated with the term-index strategy;
- Chapters 1–7;
- IEEE-style bibliography/references;
- appendices.

Supervisor/examining-committee fields remain placeholders until real information/instructions are available; no identity is fabricated.

## 6. Main text versus appendices

### 6.1 Main text

Main text prioritizes the scientific argument. It should contain:

- essential conceptual diagrams;
- the experiment design and primary methodology visuals;
- approximately the key subset of T-613 figures/tables needed to answer the RQs;
- only a small number of application/workflow screenshots that explain implementation or reproducibility;
- equations/pseudocode central to understanding the experiment.

A provisional design target is roughly **12–16 primary quantitative figures** and **5–8 primary tables**, to be selected from T-613 by evidence role rather than by visual appeal. This is a planning target, not a quota.

### 6.2 Appendices

Appendices are the preferred location for:

- complete protocol/configuration details that would interrupt the main narrative;
- exhaustive root-level diagnostics;
- full direct-contrast matrices;
- secondary sensitivity views;
- extended provenance/integrity information;
- supplementary T-613 figures/tables;
- optional code/pseudocode detail not essential to the main argument;
- additional application captures or operational instructions if academically useful.

No appendix is used to hide a result necessary to understand a main-text conclusion.

## 7. Figure and table conventions

1. Every figure/table is introduced and interpreted in text; it is never left as unexplained decoration.
2. Captions identify the represented quantity, unit/direction and important uncertainty/censoring semantics where needed.
3. Original T-613 scientific assets are treated as primary quantitative evidence and retain their provenance IDs.
4. External figures are avoided where an original explanatory diagram can be produced; if an external figure is genuinely needed, source/copyright requirements are respected.
5. Application screenshots are labelled as implementation/workflow illustrations and never as quantitative scientific evidence.
6. Do not reproduce the same information simultaneously as a large table and a redundant figure unless each serves a distinct reading purpose.
7. Main-text figures must remain legible in the final Word/PDF page size; appendix figures may be denser but still readable.
8. Right-censoring must be visually/textually explicit; non-recovery is not plotted as observed recovery at the horizon.

## 8. Code, algorithms and equations

- Prefer mathematical definition for estimands and metrics.
- Prefer pseudocode for algorithmic logic that matters scientifically.
- Use short source-code excerpts only when exact implementation semantics cannot be communicated more clearly otherwise.
- Never use screenshots of long source files as a substitute for explanation.
- Full repository paths/commit identities may be cited in reproducibility notes but should not dominate the prose.
- Equations receive stable numbering only when referenced later or when the formal definition materially matters.

## 9. Academic Greek style

The target register is a research-engineering thesis, not a chronological project diary.

### Preferred properties

- precise, formal Greek;
- paragraphs organized around one claim or explanatory function;
- explicit transitions between motivation, method, observation and interpretation;
- stable terminology across Greek text, English terms, protocol and application;
- first-use Greek/English pairing for technical terms where it improves precision;
- evidence/citation attached to the claim it supports;
- uncertainty and scope stated explicitly;
- negative/null results reported normally rather than apologetically.

### Avoid

- conversational fillers such as “όπως όλοι γνωρίζουμε”;
- generic technology enthusiasm;
- unsupported statements such as “είναι ξεκάθαρα η καλύτερη μέθοδος”;
- anthropomorphic or promotional language about algorithms;
- excessive first-person chronological narration (“μετά κάναμε…”, “έπειτα δοκιμάσαμε…”);
- raw implementation diary detail;
- needless English jargon when an established Greek technical term is clear;
- forced literal translation where the English term is the standard unambiguous form.

The Department guide’s preference for formal/passive academic phrasing is respected, but passive voice is not used mechanically when it would make a sentence obscure.

## 10. Citation and source-writing rules

- Citation style: IEEE numeric by T-700/T-701 project decision, unless a later explicit supervisor instruction supersedes it.
- External scientific claims use citation-ready `ThesisBibliography` evidence.
- A citation must support the exact nearby claim; citations are not placed at paragraph ends as vague decoration for several unrelated statements.
- Related work compares research question, method, setting, evidence and limitations rather than listing papers one by one.
- Direct quotations are rare; paraphrase is preferred when scientifically faithful.
- Bibliography freshness must pass the writing gate before drafting citation-dependent Related Work and Discussion.

## 11. Length and balance

The official 70–140 page / 20,000–40,000 word range is indicative only. The example corpus itself demonstrates substantial legitimate variation.

For this project, a reasonable working content range is approximately **28,000–36,000 main-text words**, likely yielding roughly **90–120 pages** after figures/tables and the official Word formatting are applied. This is not an acceptance threshold.

The priority order is:

1. complete scientific argument;
2. sufficient reproducibility detail;
3. readable balance;
4. no unnecessary padding.

Expected relative emphasis:

- Chapters 2–4: substantial foundation/method/implementation detail;
- Chapters 5–6: the scientific center of gravity of the final thesis;
- Chapters 1 and 7: concise synthesis rather than repetition.

## 12. Rejected example-thesis conventions

The following observed patterns are explicitly **not** adopted merely because they occur in prior Department theses:

- treating an individual prior thesis as a template;
- generic multi-page descriptions of Python/HTML/CSS/Git/tool installation;
- line-by-line source-code walkthroughs in the main body;
- screenshot-heavy UI documentation as the main contribution;
- selecting a “best method” from simple mean ordering without the declared uncertainty/contrast contract;
- using the 256-interaction horizon as fake observed recovery time;
- burying limitations in one sentence of the conclusion;
- merging scientific method and implementation so tightly that the experiment cannot be understood independently of the software;
- manual TOC/figure/table numbering when Word fields/styles can provide stable numbering;
- excessive blank pages/manual spacing used to imitate old layouts;
- obsolete or inconsistent front-matter choices that conflict with current official guidance.

## 13. Writing sequence

The final document order is not the drafting order.

The evidence-driven drafting sequence is:

1. Chapter 3 — Methodology and Experimental Design;
2. Chapter 4 — Architecture and Implementation;
3. Chapter 5 — Results;
4. Chapter 6 — Discussion / validity / limitations;
5. Chapter 7 — Conclusions;
6. Chapter 2 — Background and Related Work after the required writing-gate bibliography refresh;
7. Chapter 1 — Introduction after the contribution/result story is stable;
8. Greek summary / English abstract near review-ready freeze.

This sequence minimizes rewriting and prevents introductory prose from constraining or overstating the accepted findings.

## 14. Required evidence gates before drafting

T-701 structure completion does **not** itself authorize citation-dependent drafting from the existing old bibliography snapshot.

Before T-710:

- execute the required major-writing-gate literature freshness review in the canonical `ThesisBibliography` repository;
- process any genuinely relevant new evidence through its normal analysis/verification/selection lifecycle;
- produce a new immutable consumer snapshot even if the scientific selected set remains unchanged, so the writing gate has dated provenance;
- synchronize that snapshot into this thesis repository through the controlled bibliography integration workflow;
- verify citation-ready integrity.

Only then is the full T-710 drafting task dependency-valid.

## 15. Traceability summary

| Decision | Authority |
|---|---|
| Greek main text, Word source | CONFIRMED USER / OFFICIAL workflow |
| Front-matter order | OFFICIAL T-700 |
| A4 / TNR 11 / 1.5 / heading sizes | OFFICIAL T-700 |
| IEEE numeric citations | PROJECT decision permitted by OFFICIAL guidance and supported by EXAMPLE convention |
| Seven substantive chapters | PROJECT + EXAMPLE synthesis |
| Dedicated Background/Related Work | PROJECT + strongest research EXAMPLES |
| Separate Methodology and Implementation chapters | PROJECT + EXAMPLE synthesis |
| Dedicated Results chapter | PROJECT/T-612 + experimental EXAMPLES |
| Dedicated Discussion chapter | PROJECT scientific need; intentionally stricter than common EXAMPLE practice |
| Explicit threats/limitations | PROJECT scientific integrity |
| Conclusions + future work | OFFICIAL + EXAMPLE + PROJECT |
| Quantitative figures from T-613, not UI | PROJECT/T-613 |
| Main/appendix evidence split | PROJECT + OFFICIAL appendix guidance |
| Literature refresh before T-710 | CONFIRMED REQ-RES-012 / REQ-THESIS-007 |

## 16. T-701 disposition

T-701 is complete when this guide is merged with:

- the T-700 dated official-guidance snapshot;
- canonical task/status reconciliation;
- the explicit pre-WP7 approval record;
- the writing-gate bibliography freshness task recorded as the next dependency.

This guide may later be revised only when a higher-authority requirement changes (official Department/University guidance or supervisor instruction) or when a demonstrable document-composition problem requires a bounded presentation adjustment. Such a revision must not alter frozen scientific evidence or retroactively redefine T-612/T-613 results.