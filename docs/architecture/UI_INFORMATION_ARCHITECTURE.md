# UI Information Architecture

This is the bounded page map for the native NiceGUI research application. It keeps navigation small while exposing enough scientific context for a non-programmer/non-RL user to configure, observe and understand the research workflow.

## Primary navigation

1. Dashboard
2. New Experiment
3. Runs
4. Compare
5. Artifacts

System details, metric definitions and advanced settings use drawers/tabs/contextual panels rather than extra top-level products unless later evidence requires otherwise.

## Self-explanatory UX contract

The application must be usable without reading a separate manual. Scientific complexity is explained rather than hidden behind unexplained IDs.

- Use human-readable primary labels; technical IDs remain secondary reproducibility detail.
- Explain F0/C0/D0 roles, uncertainty conditions, settings, repetitions/seeds, metrics, aggregation and SD/CI/error semantics.
- Use concise info-icon/tooltips for non-obvious concepts and contextual/expandable help for longer explanations.
- Tooltips supplement rather than replace information required to make a safe configuration decision.
- Use consistent terminology across configuration, live runs, history, comparison and exports.
- Every important status combines understandable text + stable icon/symbol + semantic visual treatment; color alone never carries essential meaning.
- Warnings/errors state what happened, what is affected and the useful next action.
- Empty/loading/disabled/unavailable states explain why and what can be done next.
- Use confirmations only for destructive/high-impact actions.
- Progressive disclosure hides irrelevant implementation detail, not scientific meaning or required decisions.

## Configuration-identity and multiple-settings contract

The application supports multiple **protocol-approved resolved configurations/settings** where the active stage declares them.

- Every resolved configuration has a stable identity/hash and stored provenance.
- Show which settings are fixed, tunable, advanced or unavailable and why.
- Development/tuning may expose multiple approved variants; final-evidence mode exposes only frozen allowed configurations.
- Every compared setting/configuration is backed by the required predefined repetitions/seeds; no single-run “best setting” ranking.
- New Experiment previews the number of whole experiments/roots implied by the selected configuration plan.
- Runs and Compare carry the configuration identity alongside agent, layout, condition and stage.
- Compatibility logic prevents or clearly warns about scientifically invalid cross-protocol/stage/configuration comparisons.
- Technical parameter differences can be expanded without cluttering the primary comparison view.

## Lightweight onboarding

After the final screen structure is stable, provide a short first-run flow (approximately 5–7 steps): orientation, configure, validate/launch, monitor, inspect results, compare, export/help.

- Previous / Next / Skip / Finish.
- Skippable and non-blocking.
- Replayable from Help / Getting Started.
- Lightweight local NiceGUI/application state only; no account/profile/persistence subsystem.
- Do not add a separate heavyweight JS/DOM tour framework without demonstrated need.
- Every page remains understandable when onboarding is skipped.

## 1. Dashboard

Purpose: immediate project/application state and next actions.

- Active and recent runs.
- Recent failures/warnings.
- Current protocol/stage and evidence state.
- Lightweight current CPU/RAM/disk/supported-GPU snapshot.
- Quick actions: create experiment, open active run, compare results, export artifact.
- Summary of accepted/frozen evidence where relevant.
- Clear recommended next action when objectively defined.

Keep the page compact and screenshot-ready; resource status is a current snapshot, not a monitoring product.

## 2. New Experiment

Purpose: configure and launch scientifically valid work without code.

- Select protocol/stage.
- Select permitted agent regime(s): F0/C0/D0 as defined by the active protocol.
- Select one or more protocol-approved configuration/settings variants where the stage permits them.
- Explain fixed vs tunable parameters and model-specific settings; hide invalid/unapproved internal switches.
- Select environment/layout and uncertainty condition/severity allowed by the protocol.
- Select or resolve the approved seed/repetition plan.
- Show defaults, units, range/meaning/consequences and validation.
- Progressive disclosure for advanced parameters.
- Preview resolved configuration identity, run/root count, evidence class/retention and relevant estimated resources.
- Present a pre-run review: agents, configuration IDs/settings, environment/condition, seeds/repetitions, protocol/stage, expected run count and blocking issues.
- Launch single or approved batch/tuning plan only after validation passes.
- Save/clone/version configuration only where the scientific workflow allows it.

Invalid/incompatible combinations are blocked with an actionable explanation.

## 3. Runs

Unified section with Active, Run Detail and History.

### Active

- Truthful queued/running/status/progress from T-530 runtime DTOs.
- Essential lifecycle actions only when supported.
- Warnings/errors/heartbeat/current resource snapshot.
- Agent + configuration identity visible.
- Compatible multi-agent/configuration live overlays only when the scientific comparison is meaningful.

### Run detail

- Smooth live GridWorld driven by read-only observer state.
- Current episode/step/action/reward and relevant evaluator-labelled disturbance state without leaking it back to agents.
- Real event timeline, logs and `LIVE / PROVISIONAL` metrics.
- ECharts live curves/overlays for compatible agents/settings.
- Resolved configuration identity and readable primary settings; full technical config/provenance expandable.
- Final outputs/artifacts after completion.
- Actionable recovery guidance after failure/interruption.
- Historical finalized runs without retained step trace explicitly show replay unavailable.

Visualization speed/interpolation is presentation-only and never affects execution actions/timing/seeds/RNG.

### History

- Search/filter by agent, configuration/settings identity, layout, condition, status, stage/evidence class, date and experiment.
- Completed/failed/cancelled/interrupted/excluded runs remain visible.
- Clone/rerun/export where scientifically valid.
- Empty state directs the user to create an experiment.

## 4. Compare

Purpose: understand compatible scientific results and configuration effects.

- Select runs/experiments/agent groups/configuration identities.
- Show compatibility status and reasons for incompatibility.
- Performance, immediate degradation, cumulative deficit, terminal performance/gap and secondary recovery/sensitivity views as permitted by the evidence version.
- Distribution plots, paired effects/95% CIs and explicit n where the final analysis supports them.
- Layout/condition/seed breakdowns where approved.
- Clear table of what differs between selected configurations/settings.
- Plotly for stored/final scientific figures; historical v1.0 SD remains labelled SD rather than CI.
- No best-run-only view, no unlabeled composite score and no post-hoc best-setting cherry-picking.
- Export comparison data/artifact manifest.

If no valid comparison exists, explain what is incompatible and how to choose compatible evidence.

## 5. Artifacts

Purpose: inspect/export thesis-ready evidence and application assets.

- Real figures/tables/CSV/JSON/HTML outputs and manifests.
- Preview/download stored Plotly/static scientific figures.
- Friendly summary of source runs/configuration identities/generation script/metric version.
- Full checksums/provenance expandable.
- Frozen/approved/provisional classification visible.
- Complete evidence-bundle export.
- Empty states explain what results are required first.

## Contextual panels

Use contextual panels for:

- agent/configuration explanations;
- metric definitions/formulas/CI semantics;
- system/runtime/Git details;
- checksums/provenance manifests;
- raw/processed data metadata;
- advanced config explanations;
- storage warnings;
- application settings;
- Help / Getting Started / onboarding replay.

## Navigation and visual principles

- Stable small navigation.
- Modern compact desktop/laptop density rather than oversized decorative sections.
- Consistent typography, spacing, iconography, cards, filters, tables and charts.
- Agent identity remains visually consistent across GridWorld/charts/tables without relying on color alone.
- Restrained hover/focus/selection micro-interactions and purposeful state/chart/GridWorld animations improve comprehension.
- Animation never fabricates progress/trajectory/metrics and remains understandable with reduced motion where practical.
- Separate execution controls, live/provisional interpretation and frozen-result interpretation.
- Every visible scientific value comes from real data and a versioned definition.
- Provenance remains accessible without dominating primary workflows.
- UX polish reduces cognitive load; it does not add decorative machinery without a concrete usability benefit.