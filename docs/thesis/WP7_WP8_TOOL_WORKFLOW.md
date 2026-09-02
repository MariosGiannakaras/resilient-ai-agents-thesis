# WP7 / WP8 Thesis, Defense, and Delivery Tool Workflow

**Status:** Active post-evidence workflow. The explicit pre-WP7 user approval gate was satisfied on 2026-09-03. T-700 and T-701 are complete. `docs/context/TASKS.md` remains the only task-status/dependency ledger.

**Current next gate:** T-702 bibliography freshness/re-sync must complete before T-710 full drafting.

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
- contextual example-thesis review and structure/style guide completed by T-701.

The remaining gate before full thesis drafting is T-702.

## Source and authority hierarchy for WP7

When drafting or reviewing a claim, use the narrowest appropriate authority:

1. **T-611/T-612/T-613 accepted evidence** — final experimental/result claims;
2. **citation-ready `ThesisBibliography` evidence** — external scientific/factual claims;
3. **accepted repository decisions/configs/code/test records** — exact project methodology/implementation claims;
4. **T-700 official academic guidance** — required structure/format/submission rules;
5. **actual supervisor instructions** — when supplied;
6. **T-701 structure/style guide** — contextual architecture/presentation decisions;
7. **individual example theses** — context only, never scientific authority.

Chat memory is never sufficient authority for a technical, bibliographic or numerical claim.

## T-700 — COMPLETE: current academic requirements

Output:

`docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`

T-700 re-verified current public ICE/UNIWA thesis-writing/regulation/deposit guidance. The current public ICE writing guide remains the principal structural/format reference found. No public ICE-specific mandatory defense duration, slide count, PowerPoint template or live-demo rule was found; these remain future T-720/T-722 recheck items.

T-700/T-701 select IEEE numeric referencing as the project WP7 default because ICE permits multiple consistent styles and the technically closest contextual examples predominantly use numeric references. A later explicit supervisor/Department instruction supersedes this project choice.

## T-701 — COMPLETE: contextual example-thesis review

Output:

`docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`

The user supplied 22 files representing 21 unique completed theses because two PDF files are byte-identical. The review covered front matter, chapter hierarchy, methodology/implementation/experiment separation, evidence presentation, code/screenshots, references, appendices, limitations, academic register and Word/layout conventions.

The examples are never used for scientific subject-matter claims.

The final manuscript architecture is seven substantive chapters:

1. Introduction;
2. Background and Related Work;
3. Methodology and Experimental Design;
4. Research-System Architecture and Implementation;
5. Results;
6. Discussion;
7. Conclusions and Future Work.

Results and Discussion remain separate by design.

## T-702 — READY: major-writing-gate bibliography freshness and re-sync

### Why this task exists

REQ-RES-012 requires a literature refresh before major writing gates. The existing immutable consumer snapshot was sufficient for the earlier protocol/research stage, but its August 2026 freshness review was targeted at protocol-freeze decisions and cannot serve as dated evidence that the final writing literature was rechecked.

### Canonical ownership

The work occurs in:

`MariosGiannakaras/ThesisBibliography`

Do not bypass that repository by adding ad-hoc primary sources or manually curated references directly to this thesis repository.

### T-702 work

1. Recover actual current `ThesisBibliography` Git/GitHub state and read its own current authorities.
2. Run a bounded current-literature search aligned to the **actual final thesis**, especially:
   - resilient/adaptive reinforcement learning under nonstationarity/change;
   - robustness/adaptation under action remapping, action failure and observation corruption where directly relevant;
   - recovery/resilience measurement in sequential decision agents;
   - Dyna/Dyna-Q+ and planning under environmental change;
   - relevant comparative evidence involving tabular RL, DQN/PPO or model-based/planning methods;
   - methodological evidence needed for the final Discussion/limitations.
3. Deduplicate against the existing corpus by content/identity, not filename alone.
4. Process genuinely useful additions through the existing upstream intake → conversion/OCR where needed → scientific analysis → evidence/excerpts → metadata verification → selection/citation-ready workflow.
5. Record a dated writing-gate freshness report, including searches that found no decision-relevant new evidence.
6. Produce a new immutable consumer snapshot identity even when no source changes the selected citation-ready set; the snapshot proves the writing gate itself was checked.
7. Sync the accepted new snapshot into this repository through the existing controlled consumer mechanism.
8. Verify integrity, provenance and citation-ready status.

### Scientific firewall

T-702 may improve/refresh literature coverage for writing. It may **not**:

- retune methods;
- change roots/layouts/conditions/budgets;
- redefine RQs/estimands;
- change T-612 values or interpretations merely because a newer paper is interesting;
- regenerate T-613 quantitative results under another analysis;
- retrospectively change the frozen protocol.

If newer literature materially challenges interpretation, it is discussed as context/limitation in Chapter 6, not used to rewrite experimental history.

## T-710 — Draft the complete Greek thesis

T-710 begins only after T-702 is objectively complete and merged/synchronized.

### Required preparation before prose generation

Build/validate chapter-level evidence maps first. For every major subsection, identify:

- purpose/question answered;
- repository source of project facts;
- citation-ready external sources required;
- final result/table/figure IDs where applicable;
- key terminology/equations;
- claims that are explicitly out of scope;
- appendix material that supports but should not interrupt the main narrative.

This prevents unsupported “smooth prose”.

### Tool split

#### Codex / repository automation

Own or verify:

- chapter evidence maps;
- claim-to-source/result/figure/table registers;
- protocol/method/settings summaries from accepted authority;
- exact run/config/evidence IDs;
- deterministic figure/table assets and their hashes;
- candidate glossary/acronym register;
- bibliography/citation consistency inputs;
- technical corrections discovered during writing through explicit revalidation paths.

Codex should not independently invent polished Greek scientific interpretation where evidence is ambiguous.

#### ChatGPT

Preferred for:

- full Greek academic drafting from verified evidence maps;
- argument structure and cross-chapter coherence;
- accurate translation/explanation of technical concepts;
- literature synthesis rather than paper-by-paper listing;
- Results narration that does not exceed T-612;
- Discussion, limitations and future-work synthesis grounded in accepted evidence and refreshed literature;
- academic-register editing, terminology control and repetition reduction;
- exact figure/table/screenshot placement guidance;
- claim-level support review.

#### Microsoft Word

Authoritative final composition/inspection surface:

- real Heading styles;
- automatic TOC;
- caption fields;
- cross-references;
- automatic lists of figures/tables;
- equation tooling;
- section/page breaks and pagination;
- final field update and visual inspection.

### Evidence-driven drafting sequence

Draft in this order, not final-document order:

1. Chapter 3 — Methodology and Experimental Design;
2. Chapter 4 — Architecture and Implementation;
3. Chapter 5 — Results;
4. Chapter 6 — Discussion, threats and limitations;
5. Chapter 7 — Conclusions and Future Work;
6. Chapter 2 — Background and Related Work using refreshed citation-ready evidence;
7. Chapter 1 — Introduction after the result/contribution story is stable;
8. Greek summary / English abstract near review-ready freeze.

### Results/Discussion firewall

**Results** state what the accepted analysis shows: estimates, uncertainty, denominators, censoring and predeclared sensitivity.

**Discussion** explains meaning, relation to literature, plausible mechanism-level interpretation, limitations and generalization boundaries.

Do not use Discussion to create a new statistical result.

## T-711 — Produce review-ready Microsoft Word thesis

### Word features

Use:

- numbered Heading styles;
- automatic Table of Contents;
- Word caption fields for figures/tables/equations;
- automatic figure/table lists;
- Word cross-references rather than manually typed numbering/page references;
- controlled document styles for body, headings, captions, bibliography and appendices;
- final update of fields before each review export.

### Review-ready outputs

- thesis `.docx`;
- PDF/render preview for visual QA where useful;
- claim/citation/result traceability report;
- figure/table register;
- manual application-asset placement register;
- unresolved reviewer/supervisor questions list, if any.

## Manual application screenshot / GIF / video workflow

The user captures real application media only when requested through a precise `ASSET-*` instruction.

Every requested capture records:

| Field | Required content |
|---|---|
| Asset ID | Stable `ASSET-APP-*` identifier |
| Capture type | Screenshot / GIF / short video |
| Exact app surface | Experiment / Run / Results / Evidence |
| Exact state | protocol, record/run/config, method, condition and live/final context where relevant |
| What must be visible | specific controls/GridWorld/chart/tooltip/status |
| What to hide/crop | unrelated/private/noisy UI |
| Purpose | exact implementation/workflow explanation supported |
| Thesis placement | chapter/section and surrounding text |
| Word treatment | target size/alignment/caption/provenance note |
| Defense use | slide/role if reused |
| Static fallback | mandatory when animation adds value |
| Evidence link | source run/config/artifact/protocol IDs when applicable |

### Static-thesis rule

- The thesis argument must remain understandable in static print/PDF.
- Animated material is supplemental.
- Quantitative result claims use T-613 figures/tables, not screenshots.
- A screenshot of the Results UI does not become scientific evidence merely because the UI displays stored results.

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

The defense is derived from the accepted final thesis and frozen evidence, not written independently.

Outputs:

- examiner-facing narrative;
- slide outline with one primary message per slide;
- slide-to-thesis/result/source evidence map;
- asset list distinguishing generated figures from application media;
- planned live-demo path and static fallback where useful;
- likely examiner questions and evidence-grounded answer notes.

Recheck current ICE-specific duration/content/file/demo rules before fixing the deck length.

## T-721 — Final PowerPoint and speaker material

### ChatGPT

Preferred for:

- slide narrative/order;
- concise Greek slide copy;
- speaker notes;
- separate full spoken Greek script synchronized slide-by-slide;
- transitions and pacing;
- visual-content recommendations and exact user-capture instructions.

### PowerPoint

Authoritative final deck inspection/rehearsal surface:

- layout/font/media compatibility;
- speaker notes/Presenter View;
- transitions/animations/media;
- actual presentation-machine testing where practical;
- any officially required export.

### Canva — optional only

Use only if it provides a concrete visual-polish benefit. Never rebuild scientific figures manually or retype result values. Revalidate any Canva → PPTX round trip in PowerPoint. Skip Canva if it adds no value.

## T-722 — Presentation validation and rehearsal

Validate:

- current official duration/content/file rules;
- every numerical claim against frozen evidence;
- external claims against final thesis/citation-ready evidence;
- terminology/settings against final thesis/application;
- slide order and notes/script synchronization;
- PowerPoint rendering on target setup;
- chart/table readability;
- media behavior;
- rehearsal duration with safety margin;
- any live demo plus tested static fallback.

A live demo is never the only way to communicate an essential result.

## T-800 — Final bibliography / official-guidance audit

Recheck:

- bibliography freshness/citation-ready status;
- every final thesis/presentation citation;
- current official thesis/submission/defense requirements;
- administrative metadata/files.

## T-801 — Final consistency / reproducibility / privacy audit

Audit as one package:

- protocol/final run identities;
- evidence/checksums/provenance;
- analysis/figure/table regeneration;
- thesis-result and slide-result numerical consistency;
- citations/source attribution;
- repository documentation/current-status consistency;
- application media provenance;
- privacy/secrets/personal data;
- licences/copyright/redistribution boundaries.

## T-802 — Final delivery readiness

Confirm the accepted package contains the then-required versions of:

- final thesis `.docx` and officially required PDF/export;
- final PowerPoint `.pptx`;
- embedded notes and separate spoken Greek script;
- required reproducibility evidence/artifacts;
- any official forms/files;
- documented demo/static fallback;
- standalone application package if/when T-803 is required by the chosen delivery scope.

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