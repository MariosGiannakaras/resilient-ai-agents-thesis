# Headless Experiment Runner

`src/resilient_agents/experiment_runner.py` is the UI-independent execution path for the validated protocol, GridWorld, F0/C0/R0 agents, schema-v1 metrics, run bundles, interruption recovery, and optional whole-experiment publication. The CLI is `scripts/run_headless_experiment.py`; future dashboard actions must construct the same request and call the same core path.

## Invocation

```text
uv run python scripts/run_headless_experiment.py \
  --repo-root <repository-root> \
  --protocol configs/protocols/pilot-v0.1.json \
  --request <explicit-request.json>
```

All three paths are required. The request is exact-key/fail-closed JSON with:

| Field | Meaning |
|---|---|
| `run_id` | New whole-experiment identity; never reused after finalization |
| `stage`, `layout_id`, `condition_id` | Protocol-controlled stage/scenario identity |
| `root_seeds`, `agent_ids` | Explicit multi-root and selected-agent set |
| `q_learning_rate`, `discount_factor`, `exploration_epsilon` | Resolved selected tabular/deployment parameters |
| `training_episodes_per_layout` | Fixed nominal checkpoint-training budget |
| `pre_change_episodes`, `post_change_episodes` | Episode-block curve budget |
| metric window/tolerance/stability fields | One explicit schema-v1 summary setting; the analysis pipeline derives the full predeclared sensitivity grid from stored curves |
| `retention_policy` | `events` or `full-trace`; pilot-v0.1 requires events plus persisted episode curves |
| `auto_publish` | One optional publication only after whole-experiment finalization |
| `execution_timeout_seconds` | Optional positive wall-clock deadline; mandatory within the protocol bounds for tuning/pilot children |

For tuning/pilot stages the runner rejects dirty/uncommitted source, out-of-partition layouts, non-precommitted seed banks, budgets or hyperparameters outside `pilot-v0.1`, incomplete agent sets, or final-reserve access. Development requests may use smaller explicit fixtures but receive no final/pilot evidentiary status.

## Scientific execution

For every root seed, the runner trains a root-specific nominal Q checkpoint on the permitted training layouts. F0 and C0 share that exact checkpoint/checksum within the root block; this preserves training variability across independent roots without giving either regime a different nominal start. R0 builds the deterministic layout-specific state-action-rectangular plan from the declared pre-pilot model/uncertainty set.

Each agent then executes two independent branches from identical starting scientific state:

- matched nominal reference for all episodes;
- disrupted branch, nominal before the global episode boundary and under the requested condition afterward.

Reference/disrupted branches reuse the same root/layout and per-episode environment and exploration seed schedule. A mismatch in their pre-change curves is a hard invariant failure. Agent learning state persists across episodes: F0 remains unchanged, C0 checkpoints each episode and continues learning, and R0 remains frozen. Agents receive only the strict projected `AgentTransition`; evaluator truth may be retained only in explicit full traces.

## Persistence, interruption, and finalization

`events.jsonl` is appended after every completed episode and records the actual derived agent/environment/disturbance seeds. `runner-state.json` is atomically replaced only after a whole root (training plus all requested agents/branches) completes and contains the completed roots, common Q checkpoint/checksum, curves, agent-state checksums, and metrics. The summary is finalized from this state, not inferred from possibly repeated partial-attempt events.

An external interruption such as process termination or `KeyboardInterrupt` leaves the bundle in `running` state without `FINALIZED`. Reinvoking the exact request resumes only at a verified root boundary. Source commit/content fingerprints, resolved config, manifest identity, checkpoint schema, and complete valid JSONL logs must still agree. A partially attempted root is deterministically rerun and its earlier events remain visible; completed roots are never rerun. Unsupported mid-root state mutation is not advertised as resumable.

Ordinary execution exceptions finalize the one bundle as `failed` with type, message, traceback, partial events, and the last atomic runner state. A predeclared deadline is checked between roots, episodes, and transitions and produces an explicit `ExperimentTimeoutError`; it never converts partial work into completion. Provenance-invalid tuning/pilot starts finalize as `invalid`. Execution finalizes exactly one auditable bundle and updates the run index once. If `auto_publish` is true, the existing guarded publisher is called once after completed or failed whole-experiment finalization; no seed or episode can publish independently.

## T-401 validation

Tiny deterministic integration tests execute two roots across all F0/C0/R0 regimes, reproduce identical scientific root results in a second repository, verify matched pre-change curves and real metric outcomes, interrupt/resume at a root boundary, reject mismatched requests and corrupted logs, and confirm one mocked publisher call only after all roots. Pilot/final matrices remain outside CI.

Finalized bundles are consumed read-only by the deterministic pipeline in `ANALYSIS_PIPELINE.md`; analysis independently revalidates the bundle and recomputes metrics rather than trusting stored summaries as derived ground truth.
