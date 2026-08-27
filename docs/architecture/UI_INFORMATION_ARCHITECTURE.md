# UI Information Architecture

This is the bounded page map for the polished local research application. It consolidates related workflows to avoid unnecessary screens and navigation complexity. DEC-044/045/046 define the current native framework, visual analytics and novice-first UX contracts.

## Primary navigation

1. Dashboard
2. New Experiment
3. Runs
4. Compare
5. Artifacts

System information, metric definitions and advanced settings use drawers, tabs, tooltips/popovers or contextual panels rather than extra top-level products unless later evidence justifies them.

## Self-explanatory UX contract

The application must be usable by a non-programmer with no prior knowledge of the repository, RL agents, experiment settings or statistical metrics. Scientific complexity is explained, not hidden or replaced with vague language.

- Use clear plain-language primary labels, concise descriptions and visible units; technical IDs remain accessible as secondary reproducibility detail.
- Use tooltips/info icons for non-obvious scientific terms, metrics, protocol concepts and controls. Information required to complete a workflow must not exist only in a tooltip.
- Use popovers/expanders or “Learn more” detail when a tooltip is too short. Definitions must agree with the active protocol/metric definitions.
- Explain what F0/C0/D0 do, what information they observe, whether/how they adapt, and why each is scientifically included.
- Explain uncertainty conditions concretely: nominal, action remap, action failure and observation corruption, including severity/parameter meaning where applicable.
- For statistical views, explain metric directionality, units, aggregation, sample count and whether bars/intervals represent SD, CI or another declared quantity.
- Keep terminology consistent across configuration, monitoring, history, comparison and exports.
- Every important status combines text with a stable icon/symbol and semantic visual treatment. Color alone never carries essential meaning.
- Use an accessible semantic palette with sufficient contrast. Success/info/warning/error/disabled/selected and LIVE/FINALIZED/EVIDENCE classes must remain distinguishable.
- Warnings/errors state what happened, what is affected and what the user can do next; place them near the affected control/action where practical.
- Empty/loading/disabled/unavailable states explain why the state exists and the next useful action when non-obvious.
- Use confirmations only for destructive/high-impact actions; routine navigation/configuration remains friction-light.
- Show a recommended next action at important workflow boundaries when one objectively exists.
- Progressive disclosure hides irrelevant implementation detail, not scientific meaning or required decisions.

## Modern compact interaction contract

The UI is information-dense but not cryptic or oversized.

- Prefer compact cards, tables, tabs, split areas, drawers and expandable detail over large decorative surfaces and excessive scrolling.
- Use consistent icons and restrained hover/focus/selection feedback to make affordances clear.
- Smooth transitions may be used for status changes, chart updates and GridWorld movement when they improve comprehension.
- Animation speed is presentation-only and never affects experiment timing, agent decisions, RNG or stored evidence.
- Never animate fake progress or interpolate a historical trajectory that was not retained.
- Keep essential states understandable without animation; respect reduced-motion preferences where practical.
- Responsive desktop/laptop layouts are required; mobile parity is not.

## Lightweight onboarding

After the application structure is stable, provide a short first-run tutorial using the selected NiceGUI/local application primitives rather than a second frontend/tour subsystem.

- Approximately 5–7 steps: orientation, configure, validate/launch, monitor, inspect results, compare, export/help.
- Provide **Previous**, **Next**, **Skip** and **Finish**.
- Tutorial is skippable and non-blocking.
- Persistent Help/Getting Started entry can replay it.
- Store only a lightweight local completion/preference flag; no account/profile/auth system.
- Do not introduce a heavyweight separate JavaScript/DOM coach-mark framework merely for animation unless native NiceGUI primitives prove insufficient and a separate amendment justifies it.
- Final wording is written against actual implemented screens.
- Every page remains understandable if onboarding is skipped.

## 1. Dashboard

Purpose: immediate project/application status and next actions.

- Active and recent runs.
- Recent failures/warnings.
- Current candidate/frozen protocol state.
- Lightweight CPU/RAM/disk and supported GPU status.
- Quick actions: create experiment, open active run, compare results, export artifact.
- Summary of frozen thesis evidence where available.
- Clear next recommended action when the project state makes one obvious.

Keep it screenshot-ready and focused; resource status is a current snapshot, not a historical observability product.

## 2. New Experiment

Purpose: configure and launch scientifically valid work without code.

- Select validated agent(s) and environment/layout.
- Select approved uncertainty condition/severity.
- Set seed/repetition plan and approved parameters.
- Explain each agent/configuration option with concise help and units.
- Progressive disclosure for genuinely advanced/model-specific parameters.
- Preview resolved configuration, run count and relevant resource estimate.
- Pre-run review: agents, environment/layout, condition/severity, seeds/repetitions, episode budgets, relevant hyperparameters, protocol/stage, run count, retention/evidence classification and blocking issues.
- Launch single or approved batch/sweep only after validation passes.
- Save/clone a versioned configuration where supported.

The UI prevents scientifically invalid/incompatible combinations and does not expose every internal implementation switch. Failures explain the corrective action rather than exposing raw exceptions.

## 3. Runs

Unified section with Active, Run detail and History.

### Active

- Truthful status/progress/heartbeat.
- Essential lifecycle actions only when supported.
- Warnings/errors and lightweight resources.
- Stable text + icon + semantic status vocabulary.
- Compatible active agent/settings comparisons when scientifically meaningful.

### Run detail

- Smooth **live GridWorld** using real read-only observer state: grid, obstacles, start/goal, current position, action/reward, episode/step and relevant evaluator-visible disturbance/event state.
- Visualization speed controls presentation cadence only.
- Event timeline and structured logs.
- **ECharts live/provisional graphs** for real available telemetry such as episode return, rolling performance, cumulative measures/progress or other approved metrics; compatible agents/settings may share axes with clear identity/legend.
- Clear `LIVE / PROVISIONAL` labeling separate from finalized evidence.
- Resolved config and essential provenance: IDs, protocol/agent/environment versions/source commit.
- Full software/hardware/checksum/manifest detail expandable.
- Final outputs, failures and artifacts after completion.
- Actionable recovery guidance for failed/interrupted runs.

### History

- Search/filter by agent, condition, status, run type/stage, date and experiment.
- Completed/failed/cancelled/interrupted/excluded runs remain visible.
- Clone/rerun/export where safe.
- Historical run without retained step trace states **replay unavailable** rather than reconstructing a plausible path.
- Empty history guides the user to create the first experiment.

A separate queue page is unnecessary unless actual runtime requirements later prove it necessary.

## 4. Compare

Purpose: understand scientifically compatible results.

- Select runs/experiments/agent groups with compatibility checks.
- Performance, degradation, terminal behavior and secondary recovery/sensitivity views.
- Plotly distributions, paired effects/95% CIs when available, heatmaps and repetition/sample counts.
- Breakdown by layout/condition/severity/seed where approved.
- Metric definitions, directionality, units, aggregation and uncertainty/error-bar semantics adjacent or contextually accessible.
- Export comparison data/figure/artifact manifest.
- Explain why a requested comparison is invalid and how to choose compatible evidence.
- Never show a best-run-only view or unlabeled composite resilience score.

Figures should be clean enough for direct thesis/presentation screenshots while retaining titles/labels/units/n/uncertainty context needed for honest interpretation.

## 5. Artifacts

Purpose: inspect and prepare real thesis/presentation material.

- Figures, tables, CSV/JSON/HTML outputs and manifests.
- Preview stored Plotly/HTML figures and screenshot-ready analytical views.
- Friendly source-run, generation-script and metric-version summary.
- Checksums/full provenance expandable or exported.
- Approved/frozen status without deleting prior versions.
- Download/export complete evidence bundles.
- Empty state explains which compatible completed evidence is required.

## Contextual panels

Use contextual panels for:

- metric definitions/formulas,
- agent/uncertainty explanations,
- system/runtime/Git detail,
- checksums/provenance,
- raw/processed file metadata,
- advanced configuration explanations,
- storage warnings,
- application settings,
- Help / Getting Started / replay onboarding.

## Navigation and visual principles

- Keep primary navigation small/stable.
- Hide internal architecture, not scientific meaning.
- Make useful run/experiment/artifact IDs visible/copyable without making them primary labels.
- Place warnings beside affected actions/comparisons.
- Separate execution controls, live/provisional interpretation and frozen-evidence interpretation visibly.
- Use consistent compact cards, charts, filters, tables, status chips, empty/error states and typography.
- Detailed provenance stays accessible without dominating the main workflow.
- Every visible scientific value comes from real data and a versioned definition.
- UX polish, micro-interactions and animation must reduce cognitive load or improve state comprehension; decorative behavior with no concrete value is excluded.
