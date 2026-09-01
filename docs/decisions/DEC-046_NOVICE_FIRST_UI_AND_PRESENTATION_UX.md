# DEC-046 — Novice-first compact UI and presentation-quality interaction design

**Status:** Accepted  
**Date:** 2026-08-27  
**Applies to:** pre-WP7 application refinement on `feat/pre-wp7-protocol-v1.1-ui-rebuild`

## Decision

The thesis application is not designed only for the author or for users who already understand reinforcement learning, experiment configuration, metrics, or the repository. The primary UI must be usable by a non-programmer with no prior knowledge of the specific agents, uncertainty conditions, run stages, statistical metrics, or controls.

The accepted visual direction is **modern, compact, information-dense without being cryptic, and self-explanatory**. NiceGUI native mode remains the application framework selected by DEC-044; Plotly/ECharts/Mermaid/AG Grid roles remain as selected by DEC-045.

## UX contract

1. **Plain-language first, technical precision preserved.**
   - Every scientific control or metric has a concise human-readable label.
   - Technical names/IDs remain available as secondary detail where useful for reproducibility.
   - Units, valid ranges and consequences of a setting are shown where ambiguity is plausible.

2. **Progressive disclosure instead of a wall of text.**
   - The default view exposes the information required to make a safe decision.
   - Helper text, info icons, tooltips, expandable “Learn more” sections and advanced settings reveal deeper detail without cluttering the main workflow.
   - Advanced controls are grouped and visually separated from ordinary experiment choices.

3. **Contextual scientific explanation.**
   - Agent cards explain what F0, C0 and D0 do, what information they can observe, how they adapt, and what scientific role each agent serves.
   - Environment/condition controls explain nominal, action remap, action failure and observation corruption in concrete language.
   - Statistical views explain metric directionality, uncertainty/error bars, sample count, aggregation scope and whether a value is LIVE/PROVISIONAL, FINALIZED RUN or versioned ANALYSIS/EVIDENCE.
   - Recovery remains visibly secondary/sensitivity and is not presented as an unexplained binary headline.

4. **Resolved configuration before launch.**
   - Before launching an experiment, the user sees a readable summary of agents, layout, condition/severity, seeds/repetitions, episode budgets, relevant hyperparameters, retention/evidence status and estimated run count.
   - Invalid or scientifically disallowed combinations fail closed with an actionable explanation, not a raw exception.

5. **Semantic visual language.**
   - Use consistent icons plus text plus color; color is never the sole signal.
   - Statuses such as queued/running/completed/failed/cancelled/interrupted, live/provisional/finalized/evidence and supported/unsupported controls have stable visual semantics.
   - Agent identities remain visually consistent across GridWorld, live charts, comparison figures and tables.

6. **Micro-interactions and purposeful animation.**
   - Use restrained hover/focus/selection feedback, button state transitions, animated progress/status changes, chart transitions and smooth GridWorld movement where they improve comprehension.
   - Animations must not obscure data, delay scientific interaction, imply progress that did not occur, or alter experiment timing/RNG/actions.
   - Respect reduced-motion accessibility where practical; essential state changes remain understandable without animation.

7. **Compact desktop layout.**
   - Prefer clear hierarchy, tight but readable spacing, compact cards/tables and progressive detail over oversized decorative surfaces.
   - Primary pages remain usable on ordinary thesis laptop/desktop resolutions without excessive scrolling.
   - Dense analytical screens may use tabs, split panes, filters, drawers and expandable detail instead of hiding useful information.

8. **Actionable states.**
   - Empty, loading, disabled, unavailable, warning and error states explain what the state means and what the user can do next.
   - Historical runs without a retained trace explicitly say replay is unavailable; no trajectory is synthesized.
   - Unsupported lifecycle actions are shown as unavailable with an explanation rather than simulated.

9. **Onboarding without dependency on onboarding.**
   - A short skippable/replayable onboarding may orient the user to Dashboard → New Experiment → Runs → Compare → Artifacts.
   - Every page must still be understandable if onboarding is skipped.

10. **Screenshot/presentation readiness.**
    - Comparison figures, metric cards and explanatory infographics should be visually clean enough for direct screenshot use in the thesis or defense when the underlying data is appropriate.
    - Presentation polish never overrides statistical truthfulness, labels, uncertainty, provenance or sample-count context.

## Acceptance implications

T-531 cannot be considered complete merely because all pages render. Human-facing acceptance must demonstrate that a user without code/RL knowledge can understand what the main controls and metrics mean, configure an approved experiment, distinguish live from final evidence, interpret comparison views, and recover from common invalid/empty/error states without repository knowledge.

T-532 screenshots must include representative tooltip/help/empty/error/status states in addition to clean default pages where useful. T-511 remains the final intended-user E2E gate.

## Non-goals

- Do not turn every label into a paragraph or expose implementation internals by default.
- Do not add decorative animation, dashboards, metrics or controls without real user/scientific value.
- Do not simplify terminology by changing the underlying scientific meaning.
- Do not introduce a second frontend framework merely for visual effects.
