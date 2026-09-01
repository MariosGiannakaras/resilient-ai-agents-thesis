# UI Information Architecture

**Status:** framework-neutral contract for the future T-528 rebuild. No final frontend framework, component library, chart library or packaging technology is selected here.

The final application is a client of the study-first `StudyService` backend. It exposes research intent and results while the backend owns scientific mechanics such as roots, exact checkpoints, FN/FD/AN/AD branch construction, validation and evidence lineage.

## Primary workflow

Default user journey:

> **Choose study → Choose method(s) → Review → Run → Monitor → Results → Export**

The simplest valid path should feel closer to:

> **Choose study → Choose methods → Run → Results**

because frozen scientific settings, root construction, Phase-A/Phase-B orchestration and validation are backend recipe responsibilities rather than manual UI plumbing.

Two high-level study intents are expected unless T-528 evidence supports a clearer wording:

1. **Compare Learning** — nominal Phase-A learning/performance comparison.
2. **Test Resilience** — matched Frozen versus Adaptive resilience/adaptation study.

Advanced/custom exploratory workflows may expose more controls, but they remain permanently distinguishable from thesis-valid frozen studies.

## Candidate primary navigation

T-528 may refine labels/layout, but the information model should cover:

1. Home / Studies
2. New Study
3. Active / History
4. Results / Compare
5. Evidence / Export
6. Help / Getting Started as contextual utility rather than a scientific product area

Do not restore historical Dashboard/New Experiment/Runs/Compare/Artifacts labels merely for continuity if a cleaner study-first structure is better.

## Self-explanatory UX contract

The application must be usable without reading a separate manual. Scientific complexity is explained rather than hidden behind unexplained IDs.

- Use human-readable primary labels; technical IDs remain secondary reproducibility detail.
- Explain retained methods, uncertainty conditions, study modes, metrics, aggregation and interval/error semantics; exact roots/internal IDs stay under Reproducibility.
- Use concise info-icon/tooltips for non-obvious concepts and contextual/expandable help for longer explanations.
- Tooltips supplement rather than replace information required to make a scientifically safe choice.
- Use consistent terminology across planning, execution, history, results and exports.
- Every important status combines understandable text + stable icon/symbol + semantic visual treatment; **color alone** never carries essential meaning.
- Warnings/errors state what happened, what is affected and the useful next action.
- Empty/loading/disabled/unavailable states explain why and what can be done next.
- Use confirmations only for destructive or scientifically high-impact actions.
- Progressive disclosure hides irrelevant implementation detail, not scientific meaning or required decisions.
- Never fabricate telemetry, trajectory motion, progress, metrics, comparisons or completed artifacts.

## Scientific configuration contract

### Thesis-valid/frozen mode

The UI loads an immutable recipe and may not silently alter:

- task/reward/gamma semantics;
- retained method configurations;
- roots/seeds;
- final layouts;
- uncertainty severities/mappings;
- learning/deployment budgets;
- probe cadence;
- Phase-B branch combinations;
- exact checkpoint origins;
- statistical recipe/contrast family.

The backend resolves those values from the frozen Study recipe. The UI shows them readably and explains why they are locked.

### Development/tuning/exploratory mode

Only stage-authorized settings are editable. Every variant receives stable configuration identity/provenance and cannot later masquerade as confirmatory evidence.

- Show fixed, editable, advanced and unavailable settings with reasons.
- Validate method-specific settings and scientific compatibility before run creation.
- Avoid a generic free-form settings panel that lets the user construct invalid protocol combinations.
- Seeds/roots are not “try another seed” controls for replacing poor outcomes.

## Pre-run review

Before launch, present a **pre-run review** derived from the resolved Study plan:

- study/evidence class and protocol version;
- selected methods and roles;
- layouts/conditions at a human-readable level;
- planned independent roots and scientific unit counts;
- Phase-A/Phase-B stages that will run;
- estimated/known resource implications when evidence supports them;
- locked versus user-selected settings;
- blocking validation issues;
- explicit note when a run is exploratory/non-thesis evidence.

The user should not need to enumerate FN/FD/AN/AD manually. In resilience mode, the primary conceptual comparison may be shown as **Frozen vs Adaptive** while technical branch details remain available under methodology/reproducibility.

## Lightweight onboarding

After the final T-528 screen structure is stable, provide a short first-run flow of roughly 5–7 steps: orientation, choose study, review, run/monitor, inspect results, compare, export/help.

- **Previous / Next / Skip / Finish**.
- Skippable and non-blocking.
- Replayable from Help / Getting Started.
- Local lightweight state only; no account/profile subsystem without a demonstrated need.
- Do not add a heavyweight tour framework unless it materially improves the selected frontend implementation.
- Every page remains understandable when onboarding is skipped.

## Studies / Home

Purpose: show durable study state and objective next actions.

- Current/ready/running/recent studies from `StudyService`.
- Evidence class and frozen/exploratory status.
- Current stage and truthful completed/failed/skipped/pending counts.
- External/blocking gates where relevant.
- Recent actionable failures/warnings.
- Quick actions: create/choose study, open active study, inspect results/evidence.
- Recommended next action only when objectively derivable from backend state.

Resource status should remain a lightweight current snapshot, not a monitoring platform.

## New Study

Purpose: express research intent without requiring scientific orchestration knowledge.

- Choose a permitted study mode/recipe.
- Choose method(s) only where the recipe/stage permits selection.
- Show recommended/frozen presets and why they are valid.
- Provide optional **Customize** progressive disclosure only for authorized exploratory/tuning parameters.
- Preview materialized job/root/layout/condition counts from the backend planner.
- Show pre-run review and validation before launch.
- Do not expose manual checkpoint IDs, branch cloning, root generation or internal executor choices as normal controls.

Invalid/incompatible combinations are blocked with an actionable explanation from backend validation.

## Active study / Monitor

Purpose: observe real execution without influencing scientific behavior.

- Truthful Study stage/job status from durable backend state.
- Method/root/layout/condition currently executing where useful.
- Real progress counters based on scientific interaction/job state, never elapsed-time animation pretending to be progress.
- Read-only GridWorld/trajectory view only where the backend provides scientifically isolated observation data.
- Real warnings/errors/events/resources.
- Supported cancellation/retry controls only where lifecycle semantics permit them; unsupported pause/resume remains explicit.
- Frozen vs Adaptive views may be synchronized conceptually, but the UI must not inject information into agents or alter timing/RNG.

If step-level replay is unavailable for retained historical evidence, say so rather than fabricating it.

## History

- Search/filter by study, method, root/configuration identity, layout, condition, state, evidence class and date where available.
- Completed/scientific-failed/infrastructure-failed/skipped/cancelled/interrupted units remain attributable.
- History is study-first, with drill-down to jobs/runs rather than a flat run list as the primary mental model.
- Rerun/retry controls must respect scientific identity; no “rerun bad seed” shortcut.

## Results / Compare

Purpose: interpret scientifically compatible evidence.

### Phase A — learning

Show, when the analysis recipe supports them:

- standardized final no-learning evaluation;
- equal-grid learning time-average/AUC-style summaries;
- root/layout distributions and explicit included/planned denominators;
- runtime/resource cost separately from policy quality.

### Phase B — resilience/adaptation

Show component results rather than a composite score:

- Frozen disturbed-vs-nominal loss;
- Adaptive disturbed-vs-nominal loss;
- matched adaptation benefit / DiD;
- branch-level FN/FD/AN/AD detail on demand;
- condition-family separation;
- failure/skipped denominators.

### Comparison rules

- Compare only scientifically compatible protocol/evidence definitions.
- Show effect sizes/intervals only when emitted by the frozen analysis package.
- Historical SD is labelled SD; do not relabel it as CI.
- No best-run-only view, no unlabeled composite score, no post-hoc best-setting cherry-picking.
- Explain incomplete layout/root blocks and retained failures rather than silently dropping them.

Exact chart types and visualization libraries are selected at T-528/T-613 after the statistical/output contract is frozen.

## Evidence / Export

Purpose: inspect and hand off reproducible evidence.

- Study evidence-handoff manifest and result index.
- Deterministic analysis/root-level CSV/JSON outputs.
- Stable result/evidence IDs.
- Thesis-ready tables/figures only after their downstream frozen recipe generates them.
- Friendly source-study/recipe/protocol/evidence-class summary.
- Full checksums/provenance/lineage expandable.
- Clear separation of scientific evidence from illustrative application screenshots/GIF/video.
- Empty states explain which upstream stage is required.

The UI never treats whatever happens to be visible on screen as the authoritative export source.

## Contextual panels

Use contextual/help surfaces for:

- method/role explanations;
- Frozen/Adaptive and FN/FD/AN/AD methodology;
- metric/estimand/interval definitions;
- system/runtime details;
- checksums/provenance/recipe hashes;
- raw/derived data metadata;
- advanced configuration explanations;
- storage warnings;
- application settings;
- Help / Getting Started / onboarding replay.

## Navigation and visual principles

- Stable small navigation and clear hierarchy.
- Modern compact desktop/laptop density rather than oversized decoration.
- Consistent typography, spacing, icons, tables and charts within the T-528 design system.
- Method identity stays consistent across GridWorld/charts/tables without relying on color alone.
- Restrained hover/focus/selection feedback and purposeful state/chart/GridWorld animation may improve comprehension.
- Animation never fabricates progress/trajectory/metrics and must remain understandable with reduced motion.
- Separate execution controls, live/provisional interpretation and frozen-result interpretation.
- Every visible scientific value comes from real backend data and a versioned definition.
- Provenance remains accessible without dominating the primary workflow.
- UX polish reduces cognitive load; it does not add decorative machinery without a concrete usability benefit.
