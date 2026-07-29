# UI Information Architecture

This is a requirements-level page map, not a final visual design.

## 1. Overview
- Project/repository/environment version.
- Active and queued runs.
- Recent completions/failures.
- System status.
- Frozen experiment/artifact summary.
- Critical warnings and blockers.

## 2. Experiment configuration
- Research/experiment context.
- Model and environment selection.
- Disturbance configuration.
- Hyperparameters and seed/repetition plan.
- Validation issues and estimated cost.
- Resolved-config preview.
- Save, launch, batch or sweep.

## 3. Live GridWorld
- Environment viewport.
- Current state/observation distinction.
- Agent action and reward.
- Disturbance event timeline.
- Episode/step controls and visualization speed.
- Live provisional metrics/logs.

## 4. Active runs
- Run cards/table with real status.
- Progress mode and heartbeat.
- Lifecycle controls based on capability.
- Resource use and warnings.

## 5. Queue
- Ordered pending runs.
- Priority/order controls only if runner supports them.
- Batch/experiment grouping.
- Estimated—not guaranteed—work remaining, clearly labeled.

## 6. Run details
- Identity, lineage and status history.
- Resolved config.
- Model/environment/protocol metadata.
- Metrics, logs, errors and checkpoints.
- Raw/processed outputs and artifacts.
- Clone/rerun/restart/export.

## 7. Run history
- Search, filtering, saved views.
- Completed/failed/cancelled/interrupted/excluded visibility.
- Bulk selection for valid comparison/export.

## 8. Comparison
- Compatibility checks.
- Distribution and uncertainty views.
- Performance, degradation and recovery.
- Breakdown by severity/layout/scenario.
- Resource/efficiency trade-offs.
- Export and artifact-generation action.

## 9. Metrics
- Definitions, units, versions and formulas.
- Run/experiment aggregation hierarchy.
- Diagnostic and sensitivity views.
- No unlabeled composite scores.

## 10. Logs
- Cross-run or single-run structured log viewer.
- Filters by level/component/event.
- Link events to lifecycle transitions and artifacts.

## 11. Results explorer
- Raw/processed/summary dataset hierarchy.
- Read-only raw-data browsing.
- Provenance and checksum display.
- Processing history.

## 12. Artifact viewer
- Figures/tables/exports.
- Source runs and generation manifest.
- Approved/frozen status.
- Word-ready preview.

## 13. System status
- Runner/service health.
- CPU/RAM/disk and supported GPU telemetry.
- Dependency/runtime/Git details.
- Storage retention warnings.

## 14. Export
- Dataset/artifact selection.
- Format/options.
- Complete bundle manifest.
- Destination and checksum verification.

## Navigation principles
- Stable experiment/run/artifact IDs visible and copyable.
- Execution controls separated from analysis/frozen-results views.
- “Final” status reserved for protocol/frozen-evidence meaning, not UI decoration.
- Warnings shown near the action they affect.
- Scientific metadata not hidden behind aesthetic simplification.
