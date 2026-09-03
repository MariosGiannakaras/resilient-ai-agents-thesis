# WP7 / WP8 Thesis, Defense, and Delivery Tool Workflow

**Status:** Active post-evidence workflow. The explicit pre-WP7 user approval gate was satisfied on 2026-09-03. T-700, T-701, T-702 and T-710 are complete. `docs/context/TASKS.md` remains the only task-status/dependency ledger.

**Current next task:** T-711 review-ready Microsoft Word thesis composition is READY from the merged evidence-grounded T-710 manuscript.

## Purpose

Define how repository evidence, `ThesisBibliography`, ChatGPT, Codex/repository automation, Microsoft Word, PowerPoint, optional Canva, official ICE guidance, contextual example theses and manual application captures are used from the start of WP7 through final delivery.

The workflow prevents two common failure modes:

1. turning the repository into prose without adequate academic synthesis; and
2. producing polished prose/figures that no longer map to accepted evidence.

No writing or presentation tool may turn provisional/live/tuning values into final thesis results.

## Current completed prerequisites

The following prerequisites are objectively satisfied:

- intended application workflow accepted;
- final protocol-v2.1 execution complete under DEC-062 replacement;
- accepted final evidence validated/frozen by T-611;
- predeclared RQ1/RQ2/RQ3 analysis finalized by T-612;
- deterministic thesis/appendix/defense quantitative asset package finalized by T-613;
- explicit pre-WP7 user approval granted on 2026-09-03;
- current public academic-guidance recheck completed by T-700;
- contextual example-thesis review and structure/style guide completed by T-701;
- dated major-writing-gate bibliography freshness review, immutable consumer snapshot and integrated citation-ready validation completed by T-702;
- complete evidence-grounded Greek manuscript, summaries, evidence map, glossary, appendices and handoff register completed by T-710 and merged through PR #132.

No remaining prerequisite blocks T-711.

## Source and authority hierarchy for WP7

When drafting, composing or reviewing a claim, use the narrowest appropriate authority:

1. **T-611/T-612/T-613 accepted evidence** — final experimental/result claims;
2. **synchronized citation-ready `ThesisBibliography` evidence** — external scientific/factual claims;
3. **accepted repository decisions/configs/code/test records** — exact project methodology/implementation claims;
4. **T-700 official academic guidance** — required structure/format/submission rules;
5. **actual supervisor instructions** — when supplied;
6. **T-701 structure/style guide** — contextual architecture/presentation decisions;
7. **merged T-710 manuscript/handoff** — accepted prose/composition input, subordinate to the authorities above;
8. **individual example theses** — context only, never scientific authority.

Chat memory is never sufficient authority for a technical, bibliographic or numerical claim.

## T-700 — COMPLETE: current academic requirements

Output: `docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`.

T-700 re-verified current public ICE/UNIWA thesis-writing/regulation/deposit guidance. The current public ICE writing guide remains the principal structural/format reference found. No public ICE-specific mandatory defense duration, slide count, PowerPoint template or live-demo rule was found; these remain future T-720/T-722 recheck items.

T-700/T-701 select IEEE numeric referencing as the project WP7 default because ICE permits multiple consistent styles and the technically closest contextual examples predominantly use numeric references. A later explicit supervisor/Department instruction supersedes this project choice.

## T-701 — COMPLETE: contextual example-thesis review

Output: `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`.

The user supplied 22 files representing 21 unique completed theses because two PDF files are byte-identical. The review covered front matter, chapter hierarchy, methodology/implementation/experiment separation, evidence presentation, code/screenshots, references, appendices, limitations, academic register and Word/layout conventions. The examples are never used for scientific subject-matter claims.

The final manuscript architecture is seven substantive chapters: Introduction; Background and Related Work; Methodology and Experimental Design; Research-System Architecture and Implementation; Results; Discussion; Conclusions and Future Work. Results and Discussion remain separate by design.

## T-702 — COMPLETE: major-writing-gate bibliography freshness and re-sync

The dated writing-gate review was completed on 2026-09-03 in canonical `MariosGiannakaras/ThesisBibliography`. It screened recent work against the actual final RQs/methods/non-stationarity/recovery/adaptation needs rather than expanding scope for recency alone.

Two non-redundant 2025 peer-reviewed supporting sources were promoted through the normal upstream lifecycle: `SRC-6F4F8BE003` and `SRC-D38364B32C`.

The accepted immutable consumer checkout is `ada0d1aec7511098fd12610ae9e5abe7aea875cd`. It was synchronized through PR #130. Integrated validation records 599 canonical sources, 123 citation-ready sources, 19 research materials, 281 indexed originals and 1,634 integrity-covered corpus files.

The review found no evidence requiring protocol amendment, re-analysis, new roots/methods, changed estimands or changed recovery thresholds. Newer literature may inform context/limitations but cannot rewrite experimental history.

## T-710 — COMPLETE: Draft the complete Greek thesis

T-710 executed only after T-702 was objectively complete, synchronized and validated.

### Evidence-first preparation

Chapter-level evidence maps were built before prose. Major subsections were tied to purpose, repository fact authority, citation-ready sources, registered result/table/figure IDs, terminology/equations, out-of-scope claims and appendix material.

### Completed drafting sequence

The evidence-driven sequence was executed as planned:

1. Chapter 3 — Methodology and Experimental Design;
2. Chapter 4 — Architecture and Implementation;
3. Chapter 5 — Results;
4. Chapter 6 — Discussion, threats and limitations;
5. Chapter 7 — Conclusions and Future Work;
6. Chapter 2 — Background and Related Work;
7. Chapter 1 — Introduction;
8. Greek summary / English abstract.

### Merged manuscript package

The authoritative Markdown manuscript input is `docs/thesis/draft/` and includes:

- `FRONT_MATTER_SUMMARIES.md`;
- Chapters 1–7;
- `T710_EVIDENCE_MAP.md`;
- `GLOSSARY_ACRONYMS.md`;
- `APPENDIX_DRAFT.md`;
- `MANUSCRIPT_INDEX.md`.

Formal external citations use stable citation-ready `SRC-*` placeholders for deterministic IEEE conversion at T-711. During PR #132, installed-bibliography validation caught a corpus-only Dyna reference residue in the formal handoff register; it was removed. Corrected exact head `e62ea790f16ab87622c1a9cc1102d5bdb1aceaa5` passed Repository checks #929, including 427 tests and installed-bibliography validation, and PR #132 was squash-merged as `b8019ece98b9f6a89350b8aa52c205b20225f013`.

### Results/Discussion firewall preserved

Results state only accepted estimates, uncertainty, denominators, censoring and predeclared sensitivity. Discussion handles meaning, literature context, plausible mechanism-level interpretation, limitations and generalization boundaries. No new statistical result, estimand, threshold, p-value family, ranking or post-hoc analysis was introduced.

## T-711 — READY: Produce review-ready Microsoft Word thesis

T-711 composes, rather than scientifically rewrites, the merged T-710 manuscript.

### Input authority

Use:

- merged T-710 manuscript/handoff at `docs/thesis/draft/`;
- citation-ready bibliography metadata under `research/bibliography/citation-ready/`;
- finalized T-613 assets under `results/thesis-assets/protocol-v2.1-final/`;
- T-700/T-701 Word/structure rules;
- T-611/T-612/T-613 whenever a composition choice touches a scientific claim.

### Word features

Use:

- A4 page and the current official-guidance-derived typography/spacing contract;
- real numbered Heading styles;
- automatic Table of Contents;
- Word caption fields for figures/tables/equations where practical;
- automatic figure/table lists;
- Word cross-references rather than manually typed numbering/page references;
- controlled styles for body, headings, captions, bibliography and appendices;
- deterministic conversion of validated `SRC-*` placeholders to IEEE numeric citations;
- formatted reference list built from canonical bibliography metadata;
- registered T-613 figure/table insertion without manually retyping result values;
- glossary/front matter and controlled section/page breaks;
- final field update before each review export where the tooling supports it.

### Scientific firewall

T-711 must not:

- change any T-612 estimate, interval, denominator or interpretation boundary;
- replace right-censored `recovery_time=null` with horizon 256 as an observed recovery time;
- derive new statistical values from raw evidence;
- substitute screenshots for T-613 quantitative evidence;
- add a source outside the citation-ready layer without upstream bibliography governance;
- invent supervisor details, acknowledgements, dedication or official declaration wording that has not actually been supplied.

### Review-ready outputs

- review-ready thesis `.docx`;
- PDF/render preview for visual QA where feasible;
- citation/reference traceability result;
- figure/table placement register;
- manual application-asset placement register;
- unresolved authoritative-input list, if any.

The `.docx` should be structurally inspectable automatically and visually reviewed to the extent available in this environment. Final Microsoft Word inspection after field updates remains required before T-713 freeze.

## Manual application screenshot / GIF / video workflow

The user captures real application media only when requested through a precise `ASSET-*` instruction. Each requested capture records stable asset ID, type, exact surface/state, visible/hide requirements, purpose, thesis placement, Word treatment, defense use, static fallback and evidence link.

Static-thesis rules:

- the thesis argument must remain understandable in static print/PDF;
- animated material is supplemental;
- quantitative result claims use T-613 figures/tables, not screenshots;
- a screenshot of Results does not become scientific evidence merely because the UI displays stored results.

## T-712 — Supervisor/reviewer correction cycle

When real feedback arrives:

1. classify each correction as wording/structure, formatting, citation, method, result interpretation, figure/table or scientific/protocol-impacting;
2. make the smallest evidence-supported correction;
3. revalidate every affected citation/result/figure/table/cross-reference;
4. if a requested change would alter frozen scientific evidence/protocol semantics, reopen the appropriate technical/evidence governance path rather than editing prose to contradict the repository;
5. preserve a revision map from feedback to change and validation.

## T-713 — Freeze final thesis

Before freeze:

- update all Word fields, TOC, lists, captions and cross-references;
- validate headings/page breaks/page numbering;
- validate figure/table legibility/source attribution;
- validate Greek/English front matter and keywords;
- validate IEEE citation/reference consistency unless superseded by a higher-authority style instruction;
- validate the claim-to-evidence register;
- perform spelling/grammar/terminology review;
- confirm no provisional/tuning/private/debug material is presented as final evidence;
- save the controlled final `.docx` and required PDF/export copies;
- visually inspect the final `.docx` in Microsoft Word after all fields are updated.

## T-720 — Defense narrative and evidence map

The defense is derived from the accepted final thesis and frozen evidence, not written independently. Outputs include examiner-facing narrative, slide outline, slide-to-evidence map, asset list, live-demo/static-fallback plan and likely examiner questions. Recheck current ICE-specific duration/content/file/demo rules before fixing deck length.

## T-721 — Final PowerPoint and speaker material

ChatGPT is preferred for slide narrative/order, concise Greek slide copy, speaker notes, full spoken script, transitions/pacing and exact capture guidance. PowerPoint is the final deck inspection/rehearsal surface. Canva is optional visual polish only and must never be used to rebuild scientific figures or retype results.

## T-722 — Presentation validation and rehearsal

Validate current official rules, every numerical/external claim, terminology/settings, slide/notes synchronization, rendering, chart/table readability, media behavior, rehearsal duration and live-demo/static-fallback behavior. A live demo is never the only way to communicate an essential result.

## T-800 — Final bibliography / official-guidance audit

Recheck bibliography freshness/citation-ready status, every final thesis/presentation citation, current official thesis/submission/defense requirements and administrative metadata/files.

## T-801 — Final consistency / reproducibility / privacy audit

Audit protocol/final-run identities, evidence/checksums/provenance, analysis/asset regeneration, thesis/slide numerical consistency, citations/source attribution, documentation/current-status consistency, media provenance, privacy/secrets/personal data and licensing/copyright boundaries.

## T-802 — Final delivery readiness

Confirm the accepted package contains the then-required versions of final thesis `.docx`/PDF, final `.pptx`, notes/script, reproducibility evidence/artifacts, official forms/files, demo/static fallback and standalone application package if/when T-803 is required.

## Direct user tools

The normal user-facing tools remain deliberately few:

1. finished thesis application — run/inspect and capture precisely requested real UI media;
2. Microsoft Word — final thesis inspection/composition;
3. Microsoft PowerPoint — final defense inspection/rehearsal;
4. ChatGPT — drafting/review/placement/narrative collaboration;
5. Canva — optional visual polish only.

The user should not need routine Git commands, manual result aggregation, manual statistical calculation, manual citation-number maintenance or manual reconstruction of evidence provenance.

## Non-negotiable integrity rules

- No tool may invent a citation, DOI, page number, result, run, metric or interval.
- No example thesis may supply a scientific claim for this thesis.
- No manual screenshot may substitute for quantitative evidence.
- No Word/PowerPoint/Canva visual edit may change scientific meaning.
- No provisional/tuning/live value becomes final evidence by copying it into a document.
- No new literature source bypasses `ThesisBibliography` governance for formal citation.
- Every scientific/application asset remains traceable to a real source or is explicitly labelled as a non-scientific illustration.
- Final thesis and defense must remain correct even if every animation/live demo fails.