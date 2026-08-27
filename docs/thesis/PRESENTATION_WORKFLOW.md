# Thesis Defense Presentation Workflow

**Status:** Deferred active workflow specification. Planning only; do not build the final presentation until `TASKS.md` prerequisites and explicit pre-WP7 approval are satisfied.

## Purpose

Produce a complete evidence-consistent PowerPoint defense package from the final thesis, frozen experiment evidence, reproducible figures/tables, and validated application/demo assets.

The presentation is not an independent scientific source. Important factual/result statements remain traceable to the final thesis, citation-ready bibliography or frozen experiment evidence.

Detailed WP7/WP8 ownership and manual-asset rules are in `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md`.

## Preferred tool split

### Codex / repository automation — evidence and assets

Codex should:

- verify final thesis/evidence/protocol versions used by the deck;
- prepare the slide evidence map and stable IDs for figures/tables/results;
- regenerate charts/tables from repository-backed frozen data when needed;
- prepare technical architecture/experiment diagrams from the actual implementation;
- validate result values, model/settings names, condition/protocol terms and captions;
- prepare exact capture instructions and provenance records for user-created application screenshots/GIF/video;
- automate repetitive export/asset validation where useful.

Codex does not invent presentation conclusions or silently convert a provisional/live/tuning value into final evidence.

### ChatGPT — narrative, Greek copy, notes and script

ChatGPT is the preferred layer for:

- selecting the defense narrative from the final thesis;
- deciding what belongs on each slide versus in speech;
- writing concise Greek slide copy;
- writing embedded speaker-note content and a separate natural spoken Greek script;
- compressing the thesis to the officially allowed duration once known;
- improving transitions, explanation order and examiner-facing clarity;
- preparing likely-question material where useful;
- giving the user exact instructions for any manual screenshot/GIF/video capture and slide placement;
- checking consistency between thesis, slides and script.

Where presentation artifact generation is available, ChatGPT may produce the `.pptx`; the final file still requires Microsoft PowerPoint validation.

### Microsoft PowerPoint — authoritative final presentation surface

PowerPoint is the preferred final inspection/rehearsal surface because the required deck is `.pptx` and the actual presentation behavior matters.

Use it to:

- inspect layouts/fonts/media after generation or any Canva round trip;
- verify embedded speaker notes;
- use Presenter View during rehearsal/presentation so notes remain private;
- validate animations/transitions/video/GIF behavior;
- run the deck on the actual presentation setup when practical;
- export PDF/video/GIF only when useful or officially required.

Current PowerPoint versions support speaker notes/Presenter View and animated-GIF export, but these convenience features never become the evidence source.

### Canva — optional visual-polish stage only

Canva is not required. It may be used only if a bounded visual-polish pass clearly improves the deck.

Canva currently supports presentation export to PPTX. If used:

- never recreate scientific plots by typing values manually;
- preserve repository-generated figures and evidence IDs;
- do not let Canva become the source of result values/citations;
- revalidate the exported PPTX in Microsoft PowerPoint, especially fonts/layouts/media/animations and speaker-note preservation;
- skip Canva when the PowerPoint artifact is already coherent and polished.

## Inputs

Before final deck generation, stabilize:

- final/review-approved thesis;
- current official defense duration/content/file requirements;
- frozen final-v1.1 evidence package;
- final paired statistical outputs;
- final figures/tables/captions;
- validated application screenshots/demo path;
- thesis/defense evidence package with claim/result/source mappings;
- `ASSET-*` capture/placement register for manually captured application media.

## Expected content

Exact slide count follows official duration and rehearsal, but the narrative normally covers only what is needed to defend the work:

- problem/motivation/research question;
- only the required related-work/conceptual context;
- methodology and experimental design;
- GridWorld and uncertainty setup;
- F0/C0/D0 roles and fairness/information boundaries;
- model/settings selection and repetition protocol at an explainable level;
- resilience/degradation/recovery metrics;
- application/reproducibility workflow where useful;
- main final results and statistical interpretation;
- limitations/threats to validity;
- conclusions/direct answer to the research question;
- optional live demo or carefully selected real app screenshots/GIF/video;
- brief future work only if justified.

Do not turn the deck into a chapter-by-chapter thesis copy.

## Application screenshots / GIF / video

The user will capture selected real application media. Every requested capture must have an `ASSET-APP-*` instruction from the WP7/WP8 workflow specifying:

- exact page and application state;
- protocol/run/config/agent/condition context;
- controls/GridWorld/chart/tooltip/status that must be visible;
- crop/hide requirements;
- intended slide and purpose;
- caption/label and evidence identifiers;
- whether animation is necessary;
- required static fallback.

Animated/live media is useful for demonstrating agent movement, real-time charts and application interaction, but **no key scientific conclusion may depend on animation or a live demo**. Quantitative claims use repository-generated final statistical figures/tables; app media illustrates execution/UX/workflow.

## Speaker material

Produce both:

1. **embedded PowerPoint speaker notes**, concise and synchronized slide-by-slide;
2. **separate full spoken Greek script**, with slide numbers/headings and complete natural wording suitable for rehearsal/following during preparation.

The script may be more detailed than the notes but should sound spoken, not like pasted thesis prose.

## Repository output contract

When eventually executed, use a structure equivalent to:

```text
presentation/
  source/
    slide-evidence-map.md
    outline.md
    speaker-script.md
    asset-placement-register.md
  assets/
    figures/
    screenshots/
    demo/
  final/
    thesis-defense.pptx
    speaker-script.docx        # optional convenience export
    defense-export.pdf         # only if required/useful
```

Names may change with official requirements; the separation between source/evidence, assets and final deliverables remains.

## Validation gates

Before final freeze:

- every numerical/result claim matches frozen evidence;
- literature claims map to final thesis/citation-ready evidence;
- model/settings/protocol terminology matches the final research state;
- app screenshots/media map to real runs/configurations or are explicitly labelled as non-scientific UI illustrations;
- notes/script match final slide order;
- PPTX opens correctly in PowerPoint with no broken fonts/layouts/media;
- graphs/tables remain legible at presentation distance;
- animation/media behavior is verified;
- no essential slide requires live internet/cloud access;
- any live demo has tested static/screenshot/GIF/video fallback;
- rehearsal fits the official duration with deliberate safety margin;
- likely examiner questions and concise evidence-grounded answers are prepared when useful.

The presentation freezes only after these checks pass.