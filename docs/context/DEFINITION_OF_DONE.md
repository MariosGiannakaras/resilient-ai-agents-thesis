# Definition of Done

Project-level completion conditions only. Concrete task IDs/status/dependencies/resume state live in `docs/context/TASKS.md`; phase intent lives in `IMPLEMENTATION_ROADMAP.md`.

## Foundation and bibliography

- [x] Official application examined; exact titles/context recorded.
- [x] Raw chat exports excluded and historical chats removed from decision authority.
- [x] `ThesisBibliography` ownership boundary, complete immutable consumer, provenance and citation-ready trust established.
- [x] Confirmed requirements/decisions/constraints/contradictions/open questions documented with stale-state validation.

## Scientific/reproducibility infrastructure

- [x] Python 3.12 + `uv` locked environment and independent `src/resilient_agents/` core.
- [x] Evaluator/agent information boundary and independent deterministic RNG streams.
- [x] Project-owned Gymnasium GridWorld and known-answer/determinism/disturbance tests.
- [x] Filesystem run bundles, provenance/checksums, multi-seed persistence/resume and guarded whole-experiment publication.
- [x] Historical pilot/v1.0 analysis and immutable final evidence baseline.
- [x] Canonical resumable Codex task/interruption workflow and documentation governance.

## Current protocol-v1.1 refinement

- [x] D0 Dyna-Q+ implemented with deterministic/serializable learned model/RNG state and no evaluator-information leakage.
- [x] D0 episode-preserving deployment and F0/C0/D0 development runner integration validated without weakening historical `PilotProtocol` semantics; CI run 346 green.
- [ ] Authoritative candidate `protocol-v1.1` defines F0/C0/D0, validated common F0/C0 budgets, bounded D0-only tuning, seven single-factor conditions, structural remap IDs, four fresh held-out final layouts and fresh precommitted final seeds.
- [ ] Candidate statistical plan fixes primary component metrics, secondary recovery sensitivity, paired effects, 95% CIs, explicit n/layout handling and no post-hoc favorable threshold/composite resilience score.
- [ ] Bounded non-final D0 tuning/pilot selects planning parameters and justifies freeze/amend/reject before any v1.1 final reserve is inspected.

## Runtime/application service

- [ ] UI-independent Python runtime service exposes truthful queued/running/completed/failed/cancelled/interrupted state, heartbeat/progress/events, unfinished history and resource snapshots.
- [ ] Read-only live GridWorld observer is proven not to alter agent-visible information, actions, timing or RNG.
- [ ] Lifecycle actions are capability-based; unsupported pause/resume/stop/cancel/restart behavior is explicit rather than simulated.

## Native application completion

- [ ] NiceGUI 3.16 native mode is the single authoritative application surface; no active Streamlit/React/Vite frontend remains.
- [ ] Dashboard, New Experiment, Runs, Compare and Artifacts implement the real configure → validate → launch → monitor → history → compare → export journey.
- [ ] A real approved multi-seed experiment executes end to end through the application using the same scientific core.
- [ ] Runs includes smooth truthful live GridWorld, event timeline/logs and real ECharts live/provisional metrics/compatible overlays.
- [ ] Compare uses real stored evidence with Plotly distributions/heatmaps/paired effects/CIs/counts/layout-condition views as available; error bars are accurately labelled (e.g. SD vs CI).
- [ ] Artifacts previews/exports real CSV/JSON/HTML/figures/provenance and provides clean thesis/presentation-ready views.
- [ ] Mermaid agent/experiment infographics and AG Grid Community analytical tables are integrated where useful without adding a second frontend stack.

### Self-explanatory UX

- [ ] A non-programmer with no RL/model/config/repository knowledge can understand the main workflow without a separate manual.
- [ ] Plain-language labels, secondary technical IDs, helper text, visible units/ranges/consequences, tooltips/info icons and contextual explanations accurately describe agents, conditions, settings and metrics.
- [ ] Advanced settings use progressive disclosure; pre-run review shows readable resolved configuration, protocol/stage, run count and blocking issues.
- [ ] Status/loading/empty/warning/error/disabled/unavailable states use understandable text + stable icons/symbols + semantic accessible visual treatment; color is never the sole signal.
- [ ] Modern compact desktop/laptop hierarchy is consistent across cards/charts/tables/filters rather than oversized/decorative.
- [ ] Restrained hover/focus/selection micro-interactions and purposeful GridWorld/chart/status animations improve comprehension, never fabricate progress/data, never alter scientific execution, and remain understandable with reduced motion where practical.
- [ ] Destructive/high-impact actions use proportionate confirmation; routine interactions remain friction-light.
- [ ] Short first-run onboarding supports Previous/Next/Skip/Finish, is replayable and local/skippable; every page remains understandable if onboarding is skipped.

## Screenshots and standalone delivery

- [ ] Root `ui-screenshots/` contains stable accepted screenshots based on real data/state or explicitly labelled diagnostic fixtures, including useful help/status/empty/error states.
- [ ] Bounded CI browser/render checks exercise the same NiceGUI pages; automated screenshots do not close human acceptance.
- [ ] Root `run_app.bat` remains a working one-click repository-checkout launcher.
- [ ] Native Windows NiceGUI/pywebview launch, close and restart are validated on the target path.
- [ ] NiceGUI/PyInstaller `onedir + windowed` build produces a cleaned application folder that opens its own window without requiring recipient-installed Python/Node/browser interaction and uses safe writable data paths.
- [ ] Intended-user T-511 E2E acceptance is complete; rendered screens/package checks alone are insufficient.

## Final v1.1 experimental/evidence phase

- [ ] Frozen v1.1 final matrix executes only after protocol freeze + application acceptance.
- [ ] Required final runs complete or are transparently accounted for; failed/cancelled/invalid/excluded runs remain attributable.
- [ ] Finalized raw results immutable/checksummed and accepted final run set frozen.
- [ ] Predeclared paired analysis/sensitivity diagnostics reproducible from frozen evidence.
- [ ] Every final figure/table has machine-readable provenance.
- [ ] Superseding thesis/defense evidence package maps RQs, protocol/methods, source IDs, run/result IDs, figures/tables/captions and planned claims.

## Mandatory writing gate

- [ ] User explicitly approves starting WP7 **after** scientific/application refinement and T-511 acceptance. No technical milestone, green CI, screenshot or package substitutes for this approval.

## Thesis phase

- [ ] Current official thesis/template/submission/defense rules reverified.
- [ ] Bibliography freshness/evidence sync complete.
- [ ] Complete Greek thesis drafted from citation-ready sources + frozen evidence package.
- [ ] Review-ready Word document includes bilingual front matter and validated figures/tables/cross-references.
- [ ] Supervisor/reviewer corrections incorporated and affected evidence/citations revalidated.
- [ ] Final thesis `.docx`/required exports frozen/versioned.

## Defense phase

- [ ] Current official defense requirements reverified.
- [ ] Slide narrative/evidence map complete; final `.pptx` grounded in final thesis/frozen evidence.
- [ ] Embedded speaker notes and separate full spoken Greek script synchronized with slide order.
- [ ] Real application screenshots/demo assets and non-live fallback validated.
- [ ] PowerPoint rendering, legibility, factual consistency and timing rehearsal pass.

## Final repository/delivery

- [ ] Privacy/secret/license audit passed.
- [ ] Reproduction guide validated on a clean environment.
- [ ] Thesis, presentation, speaker material, standalone application and frozen evidence agree.
- [ ] Required final delivery files are present, validated and frozen.
