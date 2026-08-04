# UI Information Architecture

This is a bounded page map for a polished local research dashboard. It intentionally consolidates related workflows to avoid unnecessary screens and navigation complexity.

## Primary navigation

1. Dashboard
2. New Experiment
3. Runs
4. Compare
5. Artifacts

System information, metric definitions and advanced settings should use drawers, tabs or contextual panels rather than separate top-level products unless later evidence justifies them.

## Self-explanatory UX contract

The application should be understandable without requiring the user to read a separate manual before normal use. Scientific complexity must be explained, not hidden or replaced with vague UI language.

- Use clear human-readable labels, short descriptions and visible units. Internal identifiers/codes may remain available as secondary technical detail but should not replace understandable names.
- Use tooltips for non-obvious scientific/technical terms, metrics, protocol concepts and controls. Tooltips should be concise and supplemental rather than carrying information required to complete the workflow.
- Use contextual help/popovers or expandable explanations when a tooltip would be too short. Definitions must agree with the frozen protocol and metric definitions.
- Use consistent terminology across configuration, run monitoring, history, comparison and exports. Do not call the same scientific concept by different names on different pages.
- Every important status must combine understandable text with a consistent symbol/icon and semantic visual treatment. Color alone must never carry essential meaning.
- Use an accessible semantic palette with sufficient contrast for normal desktop/laptop use. Success, information, warning, error, disabled and selected states must be visually distinct and used consistently; exact palette values are finalized during implementation rather than hard-coded prematurely here.
- Icons/symbols must be familiar and consistent. Ambiguous icons require text labels or accessible explanations.
- Warnings/errors should state what happened, what is affected and what the user can do next. Put messages next to the affected control/action whenever possible.
- Empty states should explain why no content exists and offer the relevant next action instead of showing unexplained blank tables/panels.
- Loading and disabled states should explain what is happening or why an action is unavailable when that is not obvious.
- Use confirmations only for destructive/high-impact actions such as cancelling an active experiment or removing non-evidence local material; do not interrupt harmless navigation/configuration with unnecessary confirmations.
- At key workflow boundaries, show a clear next recommended action when one exists, while preserving the user's ability to navigate elsewhere.
- Progressive disclosure should hide irrelevant implementation detail, not scientific meaning or required decisions.

## Lightweight onboarding

After the final dashboard structure is stable, add a small first-run tutorial/onboarding layer rather than a heavy frontend tour framework.

- Keep it short: approximately 5–7 steps covering the essential flow (orientation, create/configure experiment, validate/launch, monitor, inspect results, compare, export/help).
- Provide **Previous**, **Next**, **Skip** and **Finish** actions (wording may be localized appropriately in the final UI).
- The tutorial must be skippable and non-blocking.
- Provide a persistent Help/Getting Started entry that can replay the tutorial later.
- Store only a lightweight local completion/preference flag; no account/profile/authentication system is introduced.
- Prefer native Streamlit/session-state/dialog/popover capabilities or similarly lightweight primitives available in the selected final stack.
- Do not introduce a custom JavaScript/DOM coach-mark framework merely for animation/highlighting unless the final UI proves that native components are genuinely insufficient and the added complexity is separately justified.
- Final tutorial wording and exact steps are written against the actual implemented screens so they cannot become stale instructions for a UI that changed.

## 1. Dashboard

Purpose: immediate project status and next actions.

- Active and recent runs.
- Recent failures and warnings.
- Current experiment/protocol version.
- Lightweight current CPU/RAM/disk and supported GPU status.
- Quick actions: create experiment, open active run, compare results, export artifact.
- Summary of frozen thesis evidence where available.
- Clear next recommended action when the project state makes one obvious.

The dashboard must remain readable and screenshot-ready, not overloaded with every available metric. Resource status is a current snapshot, not a historical monitoring product.

## 2. New Experiment

Purpose: configure and launch scientifically valid work without code.

- Select validated model and environment version.
- Select uncertainty scenario and severity allowed by the protocol.
- Set seed/repetition plan and approved parameters.
- Show defaults, units, validation, helper text and explanations.
- Use progressive disclosure for genuinely advanced parameters.
- Preview resolved configuration, run count and estimated resources.
- Present a clear pre-run review before launch: selected agents/models, environment/scenario/severity, seeds/repetitions, expected run count, protocol version, relevant estimated resources, and blocking validation issues.
- Launch single or approved batch run only after validation passes.
- Save/clone a versioned configuration.

The page must prevent incompatible model/environment/metric combinations and must not expose every internal implementation option. Validation failures should explain both the problem and the corrective action.

## 3. Runs

A unified section with three views:

### Active

- Run cards or table with truthful status and progress.
- Essential lifecycle actions when supported.
- Warnings, errors, heartbeat and lightweight current resource use.
- Stable status vocabulary with text + icon/symbol + semantic visual treatment.

### Run detail

- Live GridWorld visualization and event timeline.
- Current action, reward, episode/step and disturbance state.
- Structured logs and provisional live metrics.
- Resolved config and essential provenance: IDs, protocol/model/environment versions and source commit.
- Full software environment, hardware snapshot, checksums and manifests in expandable technical details.
- Final outputs, warnings, failures and artifacts after completion.
- Actionable recovery guidance when a run fails or is interrupted.

### History

- Search/filter by model, scenario, status, run type, date and experiment.
- Completed, failed, cancelled, interrupted and excluded runs remain visible.
- Clone/rerun/export actions.
- Empty history states guide the user to create the first experiment rather than showing an unexplained empty table.

A separate queue page is unnecessary unless the implemented runner proves that queue management needs more than the Active view.

## 4. Compare

Purpose: understand scientifically compatible results.

- Select runs, experiments or model groups.
- Compatibility checks and visible warnings.
- Performance, degradation, recovery and variability views.
- Distribution plots, confidence/uncertainty views and repetition counts.
- Breakdown by seed, severity, scenario or environment where approved.
- Clear tables with metric definitions and aggregation level.
- Export comparison data and artifact manifest.
- If no valid comparison can be made, explain what is missing/incompatible and how to choose compatible evidence.

No best-run-only view and no unlabeled composite score.

## 5. Artifacts

Purpose: prepare material for the thesis.

- Figures, tables, CSV/JSON exports and manifests.
- Preview Word-ready output.
- Friendly summary of source runs, generation script and metric version.
- Checksums, full provenance chain and complete manifest in expandable details or the export bundle.
- Approved/frozen status without deleting prior versions.
- Download/export complete evidence bundles.
- Empty states explain which completed/compatible results are required before an artifact can be produced.

## Contextual panels

Use contextual panels instead of top-level pages for:

- metric definitions and formulas,
- system/runtime/Git details,
- checksums and complete provenance manifests,
- raw/processed data file metadata,
- advanced config explanations,
- storage warnings,
- application settings,
- Help / Getting Started / replay onboarding.

## Navigation and visual principles

- Keep the main navigation small and stable.
- Hide internal architecture, not scientific meaning.
- Make run, experiment and artifact IDs visible and copyable where useful.
- Place warnings next to the affected action or comparison.
- Separate execution controls from frozen-result interpretation.
- Use consistent cards, charts, filters, tables, empty states and error states.
- Use clear visual hierarchy, spacing and typography so primary actions/statuses are distinguishable without decoration-heavy UI.
- Do not depend on color alone for status, validation or comparison meaning; combine color with text/symbol/shape where relevant.
- Responsive desktop/laptop layouts are required; mobile application parity is not.
- Every visible scientific value must come from real data and a versioned definition.
- Detailed provenance must remain accessible without dominating the primary workflow.
- UX polish must reduce cognitive load, not add animations, custom frontend machinery or decorative interactions without a concrete usability benefit.