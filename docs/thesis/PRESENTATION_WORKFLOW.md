# Thesis Defense Presentation Workflow

**Status:** Deferred active specification. Do not build the final deck before T-713 final-thesis freeze and T-720's current defense-guidance/evidence-map gate. The pre-WP7 approval gate is already satisfied and T-716 is complete.

## Purpose

Produce an evidence-consistent PowerPoint defense package from the frozen final thesis, accepted protocol-v2.1 evidence/analysis/assets and validated application illustrations. The deck is not an independent scientific source.

## Inputs before final deck generation

- T-713 final Word/PDF thesis identity;
- current verified ICE/UNIWA defense duration/language/file/template/live-demo rules;
- T-611 frozen protocol-v2.1 evidence and T-612 final statistical interpretation;
- T-613 registered figures/tables/exports and any later verified final-thesis assets;
- slide-level claim/result/source evidence map from T-720;
- validated application screenshots/demo path only where useful, each with `ASSET-APP-*` provenance and static fallback.

## Narrative scope

The deck should defend the work rather than reproduce chapters. It normally covers:

- problem, motivation, research questions and bounded contribution;
- only the related-work concepts needed to understand the comparison;
- controlled GridWorld/uncertainty design and information/fairness boundaries;
- retained methods: Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
- Phase-A nominal learning and matched Phase-B FN/FD/AN/AD Frozen-versus-Adaptive regimes;
- RQ1 nominal learning, RQ2 matched adaptation benefit/losses and RQ3 temporal recovery/right-censoring;
- principal frozen results with uncertainty and denominators;
- limitations/threats to validity and direct conclusions;
- architecture/application workflow only where it helps explain reproducibility or demonstration;
- concise future work where justified.

No slide may introduce a new estimand, post-hoc ranking, p-value superiority family or uncited factual claim.

## Tool split

- **Repository/Codex:** evidence map, frozen figures/tables, exact technical diagrams, app-media provenance and mechanical consistency checks.
- **ChatGPT:** defense narrative, concise Greek slide copy, transitions, embedded speaker notes, separate spoken Greek script and likely-question preparation.
- **Microsoft PowerPoint:** authoritative final `.pptx` inspection, Presenter View, media/animation/font/layout validation and rehearsal.
- **Canva:** optional bounded visual polish only; any exported PPTX must be revalidated in PowerPoint and Canva never becomes a data/citation source.

## Application screenshots / GIF / video

Animated/live media is supplemental. Every manual capture must state exact page/state/context, crop/hide requirements, slide purpose, caption/evidence identity and static fallback. No essential scientific conclusion may depend on live software or animation. Quantitative claims use repository-generated evidence assets.

## Speaker material

Produce both embedded PowerPoint speaker notes and a separate complete natural Greek spoken script synchronized to slide numbers/headings. Final length follows the verified official duration and rehearsal, not an invented slide-count rule.

## Validation gates

Before T-722 completion:

- every numerical/result claim matches frozen T-612/T-613 evidence and the final thesis;
- literature claims resolve through the final governed bibliography;
- method/condition/protocol terminology matches protocol-v2.1 and the final thesis;
- right-censored recovery remains explicit and horizon 256 is never presented as an observed recovery time;
- app media are authentic or explicitly labelled non-scientific illustrations;
- notes/script match final slide order;
- PPTX opens correctly in PowerPoint with readable layouts/fonts/tables/graphs and working media;
- no essential slide requires internet/cloud/live demo;
- tested static fallback exists for any live/animated element;
- rehearsal fits the verified official duration with safety margin.
