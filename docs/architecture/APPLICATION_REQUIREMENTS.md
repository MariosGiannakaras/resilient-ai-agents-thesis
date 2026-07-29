# Application Requirements

**Purpose:** Local control, monitoring, exploration and export layer over the validated research core.

## Essential capabilities

### Overview
- Active/queued/recent run summary.
- Experiment counts by real status.
- Current system resource snapshot.
- Warnings requiring attention.
- Links to frozen thesis artifacts.

### Experiment configuration
- Select model and validated model version.
- Select GridWorld configuration and disturbance scenario.
- Edit only schema-validated parameters.
- Show defaults, ranges, units and source/rationale where available.
- Preview resolved config before launch.
- Save/reuse versioned configurations.
- Prevent final-tagged runs from dirty/uncommitted code unless explicitly permitted by policy.

### Run creation and batches
- Single run.
- Batch over seeds/repetitions.
- Explicit parameter sweeps.
- Estimated run count, storage and compute before submission.
- Immutable experiment ID and child run IDs.
- Duplicate/clone a prior run without overwriting it.

### Queue and lifecycle
- Real queue position/status where queueing exists.
- Start, pause, resume, stop, cancel and restart capability matrix.
- Confirmation for destructive/expensive operations.
- Checkpoint selection on resume.
- Structured failure/cancellation reasons.
- Recovery after application restart.

### Live GridWorld
- Current agent, goal, obstacles and visible disturbance state.
- Trace step/episode controls.
- Speed control and pause of visualization independent from scientific runner where possible.
- Clear indication of training vs evaluation and online adaptation state.
- Source run ID, environment version and scenario ID.
- Visualization can be disabled to reduce overhead.

### Real progress, logs and metrics
- Progress based on real work units, with “indeterminate” when total is unknown.
- Structured logs with time, level, component and run ID.
- Warnings and errors separated from normal logs.
- Live metrics labeled as provisional until run completion.
- No silent smoothing or aggregation.
- Link from displayed metric to definition/version.

### Run history and details
- Search/filter by model, run type, status, experiment, config, date and tags.
- Full resolved configuration.
- Status history and lineage.
- Hardware/software/Git provenance.
- Logs, warnings, errors and failure context.
- Raw/processed file and artifact links.
- Rerun/clone/restart actions.

### Comparison
- Select compatible runs/models/experiments.
- Warn when environment, metric or evaluation protocols differ.
- Show distributions, not only point estimates.
- Display number of independent repetitions and excluded runs.
- Support severity/layout breakdowns and recovery curves.
- Export comparison data and generated artifact manifest.

### Results explorer and artifact viewer
- Browse raw and processed result sets without modifying raw data.
- Preview figures, tables, traces and manifests.
- Trace figure/table back to source runs.
- Mark approved/frozen thesis artifacts without deleting earlier versions.

### Export
- CSV/JSON for data and metadata.
- Figure formats suitable for Word and archival use.
- Tables in reproducible formats.
- Complete export bundle with manifest/checksums.
- Never export invented placeholder values as scientific results.

### System status
- CPU/RAM metrics.
- GPU/VRAM only when supported and accurately sourced.
- Disk usage/free space for run paths.
- Runner process/heartbeat status.
- Software and Git version.
- Unsupported telemetry shown explicitly as unavailable.

## UI information integrity

The final application must not contain:
- fake progress bars,
- timer-driven statuses unrelated to runner state,
- random/mock scientific metrics,
- fabricated logs,
- “success” before outputs and checksums finalize,
- UI-only changes to resolved configs,
- hidden filtering of failed/excluded runs,
- unlabeled demo data.

Synthetic fixtures are allowed only in isolated tests/storybook/demo mode, clearly labeled and impossible to confuse with the final result registry.

## Non-functional requirements

- Local single-user operation.
- Core execution survives or fails safely if UI closes.
- Keyboard-accessible essential workflows.
- Readable tables/plots at common desktop resolutions.
- Clear error recovery and actionable messages.
- No mandatory cloud/network dependency for normal use.
- Stable IDs visible for runs/experiments/artifacts.
- Audit trail for lifecycle actions.
- Performance overhead measurable and optional for live visualization.
