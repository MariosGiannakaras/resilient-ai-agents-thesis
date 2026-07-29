# UI Information Architecture

This is a bounded page map for a polished local research dashboard. It intentionally consolidates related workflows to avoid unnecessary screens and navigation complexity.

## Primary navigation

1. Dashboard
2. New Experiment
3. Runs
4. Compare
5. Artifacts

System information, metric definitions and advanced settings should use drawers, tabs or contextual panels rather than separate top-level products unless later evidence justifies them.

## 1. Dashboard

Purpose: immediate project status and next actions.

- Active and recent runs.
- Recent failures and warnings.
- Current experiment/protocol version.
- Lightweight current CPU/RAM/disk and supported GPU status.
- Quick actions: create experiment, open active run, compare results, export artifact.
- Summary of frozen thesis evidence where available.

The dashboard must remain readable and screenshot-ready, not overloaded with every available metric. Resource status is a current snapshot, not a historical monitoring product.

## 2. New Experiment

Purpose: configure and launch scientifically valid work without code.

- Select validated model and environment version.
- Select uncertainty scenario and severity allowed by the protocol.
- Set seed/repetition plan and approved parameters.
- Show defaults, units, validation and explanations.
- Use progressive disclosure for genuinely advanced parameters.
- Preview resolved configuration, run count and estimated resources.
- Launch single or approved batch run.
- Save/clone a versioned configuration.

The page must prevent incompatible model/environment/metric combinations and must not expose every internal implementation option.

## 3. Runs

A unified section with three views:

### Active

- Run cards or table with truthful status and progress.
- Essential lifecycle actions when supported.
- Warnings, errors, heartbeat and lightweight current resource use.

### Run detail

- Live GridWorld visualization and event timeline.
- Current action, reward, episode/step and disturbance state.
- Structured logs and provisional live metrics.
- Resolved config and essential provenance: IDs, protocol/model/environment versions and source commit.
- Full software environment, hardware snapshot, checksums and manifests in expandable technical details.
- Final outputs, warnings, failures and artifacts after completion.

### History

- Search/filter by model, scenario, status, run type, date and experiment.
- Completed, failed, cancelled, interrupted and excluded runs remain visible.
- Clone/rerun/export actions.

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

No best-run-only view and no unlabeled composite score.

## 5. Artifacts

Purpose: prepare material for the thesis.

- Figures, tables, CSV/JSON exports and manifests.
- Preview Word-ready output.
- Friendly summary of source runs, generation script and metric version.
- Checksums, full provenance chain and complete manifest in expandable details or the export bundle.
- Approved/frozen status without deleting prior versions.
- Download/export complete evidence bundles.

## Contextual panels

Use contextual panels instead of top-level pages for:

- metric definitions and formulas,
- system/runtime/Git details,
- checksums and complete provenance manifests,
- raw/processed data file metadata,
- advanced config explanations,
- storage warnings,
- application settings.

## Navigation and visual principles

- Keep the main navigation small and stable.
- Hide internal architecture, not scientific meaning.
- Make run, experiment and artifact IDs visible and copyable where useful.
- Place warnings next to the affected action or comparison.
- Separate execution controls from frozen-result interpretation.
- Use consistent cards, charts, filters, tables, empty states and error states.
- Responsive desktop/laptop layouts are required; mobile application parity is not.
- Every visible scientific value must come from real data and a versioned definition.
- Detailed provenance must remain accessible without dominating the primary workflow.