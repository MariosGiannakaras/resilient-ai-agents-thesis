# WP7 / WP8 Thesis, Defense, and Delivery Tool Workflow

**Status:** Deferred workflow specification. This file plans future execution only; it does **not** authorize or start T-700+ work. `docs/context/TASKS.md` remains the only task-status ledger and the explicit pre-WP7 user approval gate remains mandatory.

**Planning snapshot:** 2026-08-27. Current product/tool capabilities and official Department requirements must be rechecked when T-700 actually starts.

## Purpose

Define exactly how repository evidence, ChatGPT, Codex, Microsoft Word, PowerPoint, optional Canva, and manual application captures will be used after the research/application/evidence gates are complete.

The workflow is designed so the user does not have to reconstruct the thesis from repository internals or guess where screenshots/figures belong. Scientific claims remain grounded in citation-ready bibliography and frozen experiment evidence.

## Preconditions before WP7

WP7 stays blocked until all controlling gates in `TASKS.md` pass, including:

- candidate v1.1 is frozen through the non-final protocol/tuning gate;
- complete intended application is validated and T-511 receives human acceptance;
- frozen v1.1 final runs are complete/accounted for;
- final evidence is integrity-validated/frozen;
- predeclared paired analysis is complete;
- T-613 produces the superseding thesis/defense evidence package;
- the user explicitly approves starting WP7.

No writing tool may turn provisional/live/tuning values into final thesis results.

## T-700 — Recheck official academic requirements

### Primary tools

- current official Department/University web/PDF guidance;
- repository evidence register;
- ChatGPT/web research for current verification and synthesis;
- Codex only for updating repository requirements/checklists after the verified guidance is known.

### Outputs

- dated official-guidance snapshot;
- exact current thesis/submission/defense requirements;
- Word template/style requirements if available;
- current citation style requirement/decision;
- exact defense duration/file/template/live-demo rules if officially specified;
- recorded differences from the historical requirements snapshot.

### User role

Provide any private/current supervisor instruction or template that cannot be obtained from public/connected sources. Do not manually research details the tools can verify directly.

## T-701 — Optional example-thesis review

If the user later supplies two or three completed theses, use them only for contextual structure/presentation conventions.

- They are not official requirements.
- They are not scientific sources.
- They cannot override current Department guidance.
- Useful observations are recorded as presentation/structure preferences only.

## T-710 — Draft the Greek thesis

### Scientific source hierarchy

1. frozen T-613 thesis/defense evidence package for experiment/results claims;
2. citation-ready `ThesisBibliography` evidence for external scientific claims;
3. accepted repository decisions/method/protocol documents for implementation/methodology descriptions;
4. official academic guidance for required structure/format.

Chat memory is never the authority for a technical/result claim.

### Recommended tool split

#### Codex / repository automation

Prepare and validate:

- chapter evidence maps;
- claim-to-source/result/figure/table registers;
- reproducible figure/table exports;
- protocol/method/model/settings summaries from accepted configs;
- exact run/config IDs behind reported results;
- figure/table captions from evidence metadata where deterministic;
- glossary/acronym candidate register;
- bibliography/citation consistency inputs;
- legitimate code/data corrections discovered during writing, through explicit task/revalidation paths.

Codex should not independently invent polished Greek interpretation or silently resolve an ambiguous academic claim.

#### ChatGPT

Preferred for:

- complete Greek chapter drafting from the supplied evidence map;
- restructuring and coherence across chapters;
- translating technical source meaning into accurate Greek while preserving the original scientific meaning;
- explaining F0/C0/D0, GridWorld, uncertainty mechanisms, settings and metrics at the appropriate academic level;
- writing discussion/limitations/future-work text grounded in frozen evidence;
- language/academic-register editing;
- reducing repetition and improving transitions;
- preparing exact manual-placement instructions for screenshots/assets;
- checking that a paragraph does not claim more than its citations/results support.

Where ChatGPT document-generation capability is available, it may create/edit document artifacts; the final thesis remains a Microsoft Word deliverable and must still be inspected in Word.

### Writing sequence

Recommended chapter order is evidence-driven rather than necessarily final-document order:

1. methodology / environment / agents / protocol / implementation from frozen technical records;
2. results from frozen evidence only;
3. discussion / limitations / conclusions after result claims are mapped;
4. related work/background from citation-ready evidence;
5. introduction after the final contribution/result story is stable;
6. Greek summary/English abstract near final freeze.

This reduces rewriting and prevents early prose from dictating the results.

## T-711 — Produce review-ready Microsoft Word thesis

Microsoft Word is the authoritative final composition/inspection surface because the required deliverable is `.docx`.

### Word features to use deliberately

- Heading styles for numbered chapter/subchapter hierarchy;
- automatic Table of Contents generated from headings;
- Word caption fields for figures/tables/equations rather than manually typed numbering;
- automatic list/table of figures and tables from captions;
- cross-references to headings/figures/tables/equations rather than hard-coded page/figure numbers;
- equation tooling where required;
- section/page breaks and page numbering;
- consistent styles for body text, captions, headings, bibliography and appendices;
- final field update before freeze.

### Review-ready outputs

- `.docx` thesis;
- PDF/render preview if useful for visual QA, not as a replacement for the required Word source;
- claim/citation/result traceability report;
- figure/table register;
- manual application-asset placement register;
- unresolved reviewer questions list, if any.

## Manual application screenshot / GIF / video workflow

The user has reserved capture of real screenshots, GIFs and similar animated application material.

The user must **not** be given a vague instruction such as “add a screenshot of the app”. Every requested capture receives an `ASSET-*` instruction record with:

| Field | Required content |
|---|---|
| Asset ID | Stable `ASSET-APP-*` identifier |
| Capture type | Screenshot / GIF / short video / static chart export |
| Exact app page | Dashboard / New Experiment / Runs / Compare / Artifacts |
| Exact state | protocol, run/config ID, agent(s), condition, seed/configuration context and live/final status as applicable |
| What must be visible | specific controls/GridWorld/chart/tooltip/status to include |
| What to hide/crop | unrelated/private/noisy UI elements |
| Purpose | exact claim or explanation the asset supports |
| Thesis placement | chapter -> section/subsection -> after which paragraph/table/figure |
| Word treatment | target width/alignment/wrapping, caption text, source/provenance note |
| Presentation placement | slide number/role if also used in defense |
| Animation rule | whether animation adds explanatory value and required static fallback |
| Evidence link | source run/config/artifact/protocol IDs |

### Static thesis rule

The core thesis argument must remain understandable in a static/printed/PDF form. Therefore:

- use a representative static screenshot/figure in the Word thesis for any scientifically relevant animated view;
- keep GIF/video as supplemental/demo/defense material unless current official delivery rules explicitly support and justify animated thesis media;
- never make a result claim depend only on an animation;
- prefer repository-generated Plotly/static figure exports for quantitative result claims; application screenshots illustrate the application/workflow, not replace statistical figures.

## T-712 — Supervisor/reviewer correction cycle

When real feedback arrives:

1. classify each correction as wording/structure, formatting, citation, method, result interpretation, figure/table, or scientific/protocol-impacting;
2. make the smallest supported correction;
3. revalidate every affected citation/result/figure/table/cross-reference;
4. if a requested change would alter frozen scientific evidence or protocol interpretation, reopen the appropriate technical/evidence task rather than editing prose to contradict the repository;
5. keep a revision log mapping feedback to changes and validation.

ChatGPT may rewrite/restructure; Codex/repository tooling verifies technical/evidence consequences; Word is used for final document-level inspection.

## T-713 — Freeze final thesis

Before freeze:

- update all Word fields/TOC/lists/caption numbering/cross-references;
- verify headings/page breaks/page numbering;
- validate figure/table legibility and source attribution;
- validate Greek/English front matter and keywords;
- validate bibliography/citation consistency;
- validate claim-to-evidence register;
- spell/grammar/terminology review;
- check no provisional/tuning/private/debug content is accidentally presented as final evidence;
- save the final controlled `.docx` and required exports.

## T-720 — Defense narrative and evidence map

The defense is derived from the final thesis/frozen evidence, not written independently.

Outputs:

- presentation purpose and examiner-facing narrative;
- slide outline with one primary message per slide;
- slide-to-thesis/result/source evidence map;
- asset list distinguishing generated figures from user-captured app screenshots/GIF/video;
- planned live-demo path and static fallback;
- likely examiner questions/evidence-grounded answer notes where useful.

ChatGPT is the preferred narrative/Greek explanation layer. Codex verifies every technical/result value and prepares reproducible assets.

## T-721 — Final PowerPoint and speaker material

### Preferred tool split

#### ChatGPT

- slide narrative and ordering;
- concise Greek slide copy;
- speaker notes;
- separate full spoken Greek script synchronized to slide order;
- transitions and explanation pacing;
- visual-content recommendations;
- exact instructions for user-captured app media.

ChatGPT may generate a `.pptx` artifact where the active product/tool surface supports presentation generation, but the workflow does not assume direct Microsoft PowerPoint control through ChatGPT Work.

#### PowerPoint

PowerPoint is the authoritative final presentation inspection/rehearsal surface:

- verify slide layout/font/media compatibility;
- inspect embedded speaker notes;
- use Presenter View for private notes during rehearsal/presentation;
- verify transitions/animations and any embedded media;
- run the deck on the actual presentation hardware/setup where practical;
- export any required PDF/video/GIF only when useful/officially required.

Current Microsoft PowerPoint versions support speaker notes/Presenter View and can export a slide show as an animated GIF. These capabilities are useful for defense assets but do not replace the repository evidence contract.

#### Canva — optional only

Canva can be used for a bounded visual-polish pass when it provides a clear benefit. Current Canva presentation tooling supports PPTX export. However:

- do not rebuild scientific figures manually in Canva;
- do not type result values manually when repository-generated assets exist;
- preserve slide evidence IDs outside Canva;
- after any Canva -> PPTX round trip, revalidate fonts/layouts/charts/media/animations and speaker notes in Microsoft PowerPoint;
- skip Canva entirely if the generated PowerPoint is already coherent and polished.

Canva is therefore **optional, not required**.

## T-722 — Presentation validation and rehearsal

Validate:

- current official duration/content/file rules;
- every numerical/result claim against frozen evidence;
- every external factual claim against final thesis/citation-ready evidence;
- terminology/model/settings names against final thesis/application;
- slide order and notes/script synchronization;
- PowerPoint rendering on the target machine;
- chart/table readability at presentation distance;
- animation/media behavior;
- Presenter View/speaker-note usability;
- rehearsal duration with safety margin;
- live demo plus tested screenshot/GIF/video/static fallback.

A live demo is never the only way to communicate a key result.

## T-800 — Final bibliography / official-guidance audit

Recheck:

- bibliography freshness and citation-ready status;
- citations used in final thesis/presentation;
- current official thesis/submission/defense requirements;
- any required administrative metadata/files.

## T-801 — Final consistency / reproducibility / privacy audit

Audit as one package:

- protocol version and final run set;
- reproducibility/provenance/checksums;
- analysis/figure/table regeneration;
- thesis-result numerical consistency;
- slide-result numerical consistency;
- citations/source attribution;
- repository documentation/current-status consistency;
- application screenshot/media provenance;
- privacy/secrets/personal data;
- licenses/copyright/redistribution boundaries.

## T-802 — Final delivery readiness

Confirm that the required final package contains the accepted versions of:

- thesis `.docx` and any officially required exports;
- final PowerPoint `.pptx`;
- embedded notes and separate spoken Greek script;
- final application/delivery folder where required;
- frozen evidence/artifacts required for reproducibility;
- any officially required forms/files;
- documented demo/static fallback.

## Tools the user is expected to use directly

The normal expected direct user tools are deliberately few:

1. **Finished thesis application** — execute/inspect approved experiments and capture requested real UI media.
2. **Microsoft Word** — final thesis visual inspection and any deliberate manual insertion/adjustment specified by the placement register.
3. **Microsoft PowerPoint** — final deck inspection, notes/Presenter View, rehearsal and media/animation QA.
4. **ChatGPT** — review/drafting/placement guidance and later slide/script collaboration.
5. **Canva** — optional only if a visual-polish pass is genuinely useful.

The user should not need routine Git commands, manual result aggregation, manual statistical calculation, manual citation-number maintenance, or manual reconstruction of evidence provenance.

## Current external-tool capability notes

These are planning notes, not permanent assumptions:

- Microsoft Word builds an automatic TOC from heading styles and supports captions, cross-references and automatic lists of figures/tables; use those native mechanisms rather than manual numbering.
- Microsoft PowerPoint supports embedded speaker notes and Presenter View; current versions also support animated GIF export.
- Canva currently supports presentation export to PPTX and may be useful for optional design polish.
- ChatGPT can work with uploaded files and, depending on the active surface/plan, create/edit document/presentation artifacts. Current ChatGPT Work documentation should be rechecked at T-700/T-721 rather than assuming direct PowerPoint desktop integration.
- GitHub Actions can use GitHub-hosted or self-hosted runners, but final scientific execution remains governed by the validated protocol/machine boundary rather than by tool convenience.

## Non-negotiable integrity rules

- No tool may invent a citation, DOI, page number, result, run, metric or confidence interval.
- No manual screenshot may substitute for quantitative analysis evidence.
- No Canva/PowerPoint/Word visual edit may change the scientific meaning of a figure/table.
- No provisional/tuning/live value becomes final evidence by copying it into Word/PowerPoint.
- Every manually inserted scientific/application asset remains traceable to a real run/config/artifact or is explicitly labelled as a non-scientific UI illustration.
- Final thesis and defense must remain correct even if every animation/live demo fails; static evidence/fallbacks are mandatory for essential content.