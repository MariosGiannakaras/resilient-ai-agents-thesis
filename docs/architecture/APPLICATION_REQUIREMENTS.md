# Application Requirements

**Purpose:** A polished local control, monitoring, comparison and export layer over the validated research core.

The application is an important thesis deliverable, but not a production-grade platform. Its feature set must be bounded by the actual experiment and thesis workflows.

## Required workflows

### 1. Project overview

- Show active, recent and failed runs.
- Show critical warnings and storage/system status.
- Provide direct actions to create a run, continue monitoring or open results.
- Keep the overview visually clean and useful for screenshots.

### 2. Experiment configuration and launch

- Select only validated models, environment versions and uncertainty scenarios.
- Edit schema-validated parameters with defaults, units, ranges and explanations.
- Support single runs and the approved seed/repetition batch design.
- Preview the resolved configuration and estimated run count before launch.
- Save or clone versioned configurations.
- Prevent invalid or scientifically incompatible combinations.

The UI must not expose an uncontrolled research sandbox containing every internal parameter. Advanced parameters may use clearly labeled progressive disclosure.

### 3. Active run and GridWorld monitoring

- Display truthful run status and progress based on real work units.
- Use indeterminate progress when a reliable total is unavailable.
- Show useful logs, warnings and errors with timestamps and run identity.
- Visualize agent, goal, obstacles, actions, rewards and disturbance events.
- Clearly identify training, evaluation and adaptation state.
- Allow visualization speed/pause independent of the scientific runner where feasible.
- Show CPU/RAM and supported GPU/VRAM telemetry from real sources.
- Provide only lifecycle controls supported safely by the runner.

### 4. Run history and details

- Search and filter runs by model, scenario, status, run type, date and experiment.
- Keep completed, failed, cancelled, interrupted and excluded runs visible.
- Show resolved config, status history, logs, metrics and provenance.
- Show source Git commit, software environment and hardware snapshot.
- Support clone/rerun and export without overwriting previous evidence.

### 5. Comparison and results

- Compare compatible models, seeds, settings and uncertainty conditions.
- Warn when protocols, environments or metric versions are incompatible.
- Show distributions and independent repetition counts, not only best or mean values.
- Provide clear charts and tables for performance, disruption, recovery and variability.
- Support scenario/severity breakdowns when required by the approved protocol.
- Trace every figure/table back to source runs and metric definitions.

### 6. Thesis artifact export

- Export real CSV/JSON data and metadata.
- Export Word-ready figures and reproducible tables.
- Generate artifact manifests with source runs, configs, versions and checksums.
- Preview approved/frozen thesis artifacts.
- Never export mock values as scientific results.

## UI quality requirements

- Modern, consistent and visually polished design.
- Clear hierarchy, spacing, typography and status communication.
- Appropriate use of dashboards, cards, charts, filters and tables.
- Responsive layouts for common desktop and laptop resolutions.
- Keyboard-accessible essential workflows.
- Actionable errors and visible recovery guidance.
- Screenshot-ready views without hiding scientific labels or provenance.
- Consistent loading, empty, warning, failure and unsupported states.

## Scientific information integrity

The application must not contain:

- fake or timer-driven progress,
- fabricated scientific metrics or logs,
- success state before outputs and manifests finalize,
- hidden filtering of failures or excluded runs,
- silent config changes,
- unlabeled synthetic/demo data,
- misleading comparisons across incompatible protocols.

Synthetic fixtures are allowed only in isolated tests or clearly labeled UI development mode.

## Feature tiers

### Required for thesis completion

- configuration and run launch,
- truthful active-run monitoring,
- GridWorld visualization,
- run history and details,
- comparison charts/tables,
- real artifact export,
- basic local resource/status visibility.

### Add only when justified

- pause/resume and checkpoint selection,
- parameter sweeps beyond the frozen design,
- queue ordering or priorities,
- bulk operations,
- advanced saved views,
- automated report generation,
- optional AI assistance.

### Out of scope

- authentication and permissions,
- multi-user collaboration,
- public/cloud deployment,
- remote/distributed workers,
- complex orchestration,
- production incident tooling,
- plugin marketplaces,
- mobile application.

## Non-functional requirements

- Local single-user operation.
- Core runs safely if the UI closes.
- Normal workflows work offline after dependencies are installed.
- Stable IDs remain visible and copyable.
- Performance overhead from visualization is measurable and optional.
- Architecture and feature count remain compatible with thesis completion.
