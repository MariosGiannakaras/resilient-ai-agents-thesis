# Thesis Defense Presentation Workflow

**Status:** Deferred active workflow specification. Do not build the presentation until the final thesis/evidence prerequisites in `TASKS.md` are satisfied.

## Purpose

Produce a complete, evidence-consistent PowerPoint defense package from the final thesis, frozen experiment evidence, reproducible figures/tables, and validated application/demo assets.

The presentation is not an independent source of scientific claims. Every important factual/result statement must remain traceable to the final thesis, citation-ready bibliography, or frozen experiment evidence.

## Preferred tool split

### Codex — evidence and asset preparation

Codex should:

- verify the final evidence/thesis versions used by the deck;
- prepare the slide evidence map and stable IDs for figures/tables/results;
- regenerate charts/tables/screenshots from repository-backed data when needed;
- prepare demo/fallback assets and technical architecture diagrams from the actual implementation;
- validate that slide numbers, result values, model names, protocol terms, and captions match the repository/final thesis;
- automate repetitive asset/export work where useful.

Codex should not invent presentation conclusions or silently simplify a result into a different scientific claim.

### ChatGPT — narrative, slide copy, and speaking script

ChatGPT is the preferred layer for:

- selecting the defense narrative from the final thesis;
- deciding what belongs on each slide and what should be spoken instead of displayed;
- writing concise Greek slide copy;
- writing speaker notes and a separate natural spoken Greek script;
- compressing the thesis into the allowed presentation duration;
- improving transitions, explanation order, clarity, and likely question preparation;
- checking consistency between thesis, slides, and script.

### Presentation tooling — final `.pptx`

Default final workflow: use ChatGPT's presentation-generation capability or equivalent PowerPoint-capable tooling to produce the `.pptx`, then validate the file in Microsoft PowerPoint.

Microsoft PowerPoint is the preferred final inspection/rehearsal surface because the required deliverable is a PowerPoint deck and speaker notes must be checked in the actual target format.

Canva or another design tool may be used only as an optional visual-polish stage if it adds value. It must not become the scientific source of truth, and any export back to `.pptx` must be rechecked for fonts, layouts, charts, animations, and speaker-note preservation.

## Inputs

Before final deck generation, the following should be stable:

- final/review-approved thesis version;
- current official presentation/defense requirements, especially duration and required content;
- frozen `results/thesis-final/` evidence;
- final statistical outputs;
- final figures/tables and captions;
- application screenshots/demo path validated against real state;
- thesis evidence package with claim/result/source mappings.

## Expected presentation content

The exact slide count follows the official duration and rehearsal, but the narrative should normally cover only what is needed to defend the work:

- problem, motivation, and research question;
- relevant concepts/related-work context only to the degree needed;
- methodology and experimental design;
- GridWorld/uncertainty setup;
- compared agent roles and fairness controls;
- resilience/recovery metrics;
- application/reproducibility workflow where useful;
- main experiment results and statistical interpretation;
- limitations/threats to validity;
- conclusions and direct answer to the research question;
- optional demo or carefully selected screenshots;
- brief future work only if justified.

Do not turn the deck into a chapter-by-chapter copy of the thesis.

## Speaker material

Produce both:

1. **embedded speaker notes** in the PowerPoint, concise and synchronized slide by slide;
2. **separate full spoken script**, in Greek, with slide numbers/headings and complete wording detailed enough for the user to rehearse from or read/follow when preparing the defense.

The full script may be more detailed than the embedded notes. It should sound spoken rather than like thesis prose.

## Repository output contract

When this phase is eventually executed, use a structure equivalent to:

```text
presentation/
  source/
    slide-evidence-map.md
    outline.md
    speaker-script.md
  assets/
    figures/
    screenshots/
    demo/
  final/
    thesis-defense.pptx
    speaker-script.docx        # optional convenience export when useful
    defense-export.pdf         # only if required/useful
```

Names may change to match official requirements, but the separation between source/evidence, assets, and final deliverables should remain.

## Validation gates

Before the presentation is final:

- every numerical/result claim matches frozen evidence;
- every literature claim is supported by the final thesis/citation-ready evidence;
- slide terminology matches the final thesis and actual application;
- notes/script match the final slide order;
- deck opens correctly in PowerPoint with no broken fonts/layouts/media;
- graphs/tables are legible at presentation distance;
- no slide depends on live internet/cloud access;
- any live demo has a tested screenshot/video/static fallback;
- rehearsal fits the official time with a deliberate safety margin;
- likely examiner questions and concise evidence-grounded answers are prepared separately if useful.

The final presentation is frozen only after these checks pass.