# Run Schema

The canonical machine-readable format should be versioned JSON or another schema-validated format. Field names below are conceptual until an implementation ADR freezes them.

## Identity and lineage

| Field | Required | Description |
|---|---:|---|
| `schema_version` | yes | Run-manifest schema version. |
| `run_id` | yes | Globally unique immutable identifier. |
| `experiment_id` | yes | Parent experiment/protocol identifier. |
| `name` | yes | Human-readable short name. |
| `description` | no | Purpose or condition description. |
| `run_type` | yes | `baseline`, `pilot`, `exploratory`, `final`, `validation`. |
| `parent_run_id` | no | Clone/restart/resume source. |
| `lineage_relation` | no | `clone`, `restart`, `resume`, `rerun`, `derived`. |
| `repeat_index` | yes | Independent repetition index within condition. |

## Model

| Field | Required | Description |
|---|---:|---|
| `model.name` | yes | Canonical model/agent name. |
| `model.family` | yes | Baseline/tabular/model-based/neural/planning/etc. |
| `model.version` | yes | Implementation version or package/source commit. |
| `model.adapter_version` | yes | Common-interface adapter version. |
| `model.hyperparameters.requested` | yes | User/config requested values. |
| `model.hyperparameters.resolved` | yes | Actual values used after defaults/derivations. |
| `model.checkpoint_in` | no | Initial checkpoint reference and checksum. |
| `model.information_access` | yes | Observation/privileged information declaration. |
| `model.adaptation_mode` | yes | Frozen, online learning, replanning, detector, etc. |

## Environment and scenario

| Field | Required | Description |
|---|---:|---|
| `environment.name` | yes | Environment implementation name. |
| `environment.version` | yes | Semantic/config schema version. |
| `environment.config_path` | yes | Version-controlled source config. |
| `environment.config_resolved` | yes | Full actual config. |
| `environment.layout_id` | yes | Stable layout/map identifier and checksum. |
| `environment.disturbances` | yes | Type, severity, onset, duration, schedule, seed. |
| `environment.termination` | yes | Terminal/truncation conditions. |
| `evaluation.scenario_set_id` | yes for evaluation | Frozen scenario manifest. |

## Randomness

| Field | Required | Description |
|---|---:|---|
| `seed.root` | yes | Root seed. |
| `seed.environment` | yes | Environment RNG seed. |
| `seed.agent` | yes | Agent/init/sampling seed. |
| `seed.disturbance` | yes | Disturbance RNG seed. |
| `seed.framework` | no | Framework/device-specific seeds. |
| `determinism.mode` | yes | Exact, best-effort or statistical. |
| `determinism.notes` | no | Known nondeterministic operations. |

## Lifecycle

| Field | Required | Description |
|---|---:|---|
| `status.current` | yes | Current/final state. |
| `status.history` | yes | Ordered state changes with timestamps/reasons. |
| `queue.position_history` | no | Queue changes if used. |
| `progress.mode` | yes | Determinate with unit/total or indeterminate. |
| `progress.completed_units` | no | Real completed work units. |
| `progress.total_units` | no | Real expected units. |
| `started_at` | no | UTC timestamp. |
| `ended_at` | no | UTC timestamp. |
| `duration_seconds` | no | Monotonic measured duration. |
| `heartbeat_at` | no | Last runner heartbeat. |
| `failure_reason` | no | Structured failure type/message/context. |
| `cancellation_reason` | no | User/system cancellation reason. |
| `exclusion_reason` | no | Analysis exclusion rule/reference. |

## Outputs

| Field | Required | Description |
|---|---:|---|
| `paths.run_root` | yes | Immutable run directory. |
| `paths.logs` | yes | Structured and human-readable logs. |
| `paths.raw_results` | yes | Raw result files with checksums. |
| `paths.processed_results` | no | Run-local processed outputs, if any. |
| `paths.checkpoints` | no | Checkpoint manifest. |
| `metrics.schema_version` | yes | Metric schema/code version. |
| `metrics.summary` | yes on completion | Final run-level summaries. |
| `warnings` | yes | Zero or more structured warnings. |
| `errors` | yes | Zero or more structured errors. |
| `artifacts` | yes | Artifact IDs/paths/checksums. |

## Execution environment

| Field | Required | Description |
|---|---:|---|
| `git.repository` | yes | Repository identifier. |
| `git.commit` | yes | Exact commit hash. |
| `git.dirty` | yes | Whether uncommitted changes existed. Final runs should be false. |
| `software.os` | yes | OS and version. |
| `software.runtime` | yes | Language/runtime version. |
| `software.dependencies` | yes | Lockfile or package snapshot/checksum. |
| `hardware.cpu` | yes | Model/core count. |
| `hardware.ram` | yes | Total/available snapshot. |
| `hardware.gpu` | no | Model/driver/backend if present. |
| `hardware.storage` | no | Relevant disk/path/free-space snapshot. |
| `command` | yes | Reproduction command or entrypoint. |
| `config_file` | yes | Source config and checksum. |

## Integrity

| Field | Required | Description |
|---|---:|---|
| `created_at` | yes | Manifest creation time. |
| `finalized_at` | no | Lock/finalization time. |
| `checksums` | yes | Hashes for raw results/config/checkpoints/artifacts. |
| `provenance_version` | yes | Provenance-policy version. |
| `notes` | no | Non-authoritative annotation. |

## Example lifecycle rules

- `completed` requires final metrics, output checksums and finalized manifest.
- `failed` requires failure reason and retained partial outputs.
- `cancelled` requires cancellation reason.
- `excluded` is an analysis status layered over the execution outcome; original execution status is retained.
- Restart/rerun never reuses the old `run_id`.
- Mutable operational state may be stored separately while running, but completion produces an immutable snapshot.
