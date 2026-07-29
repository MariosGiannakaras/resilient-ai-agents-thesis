# Experimental Requirements

## Run classes

### Baseline runs
- Validate environment and metric behavior.
- Include at least sanity/random and any justified planning/oracle calibration.
- Must not receive hidden advantages without explicit labeling.

### Pilot runs
- Small, cheap and diagnostic.
- Estimate runtime, variance, instability, checkpoint behavior and metric sensitivity.
- May change the protocol.
- Never mixed with final evidence.

### Exploratory runs
- Used for model debugging, hypothesis refinement and hyperparameter search.
- Conditions and outcomes remain logged.
- Must not silently become final runs.

### Final runs
- Executed only after protocol and analysis plan freeze.
- Use predeclared configs, seeds/repetitions, evaluation scenarios and exclusions.
- Form the immutable evidence set for thesis figures/tables.

## Experiment matrix

Each experiment must define:
- research question and estimand,
- environment version and layout/configuration set,
- disturbance type, severity, onset, duration and schedule,
- model/implementation/version,
- training and evaluation regime,
- hyperparameter source/range,
- tuning policy and tuning dataset/scenarios,
- evaluation budget,
- seeds and repeat indices,
- checkpoint selection rule,
- metrics and aggregation,
- resource limits,
- stopping/early-stop criteria,
- failure and exclusion policy,
- statistical comparison plan,
- expected artifacts.

## Hyperparameters and sweeps

- No arbitrary “standard” values without source or pilot evidence.
- Search spaces must be bounded and recorded before execution.
- Model-specific ranges are allowed when justified.
- Search effort/budget per model must be reported.
- Final evaluation scenarios cannot drive hyperparameter selection.
- Sweeps use explicit experiment IDs and child run IDs.
- Failed configurations remain in the registry.
- Adaptive search methods, if used, need deterministic seeds and complete search history.

## Seeds and repetitions

- Separate environment, agent initialization, sampling and disturbance RNG streams where practical.
- Derive component seeds from a recorded root seed using a documented method.
- Do not reuse a random global state implicitly.
- Number of repetitions is chosen from pilot variance, desired precision and compute budget.
- Use common random numbers/paired scenarios only when the design and analysis account for dependence.
- Report seed sensitivity and all excluded seeds with reasons.

## Stopping criteria

Candidates include:
- fixed environment-interaction budget,
- fixed training episodes,
- fixed wall-clock/resource budget,
- convergence/plateau rule defined before final runs,
- safety/failure cutoff,
- maximum episode length,
- early termination for invalid/numerically unstable configuration.

The criterion must not selectively favor a model family without being part of the intended comparison. Training stop and evaluation horizon are distinct.

## Common evaluation conditions

- Same frozen environment and disturbance scenario set.
- Same outcome definitions and metric implementation.
- Same evaluation episode count/horizon.
- Same permitted adaptation regime.
- Same access to information, unless a baseline is explicitly privileged.
- Same checkpoint selection rule or model-appropriate rule documented in advance.
- Timing comparisons run under controlled machine-load procedures.

## GridWorld coverage

Final design should consider, subject to RQs and compute:
- nominal/no-disturbance condition,
- multiple severity levels,
- more than one layout or held-out layout,
- single disturbances before compound disturbances,
- reachable and intentionally impossible scenarios labeled separately,
- early/late or abrupt/gradual changes only if scientifically useful,
- robustness/generalization tests separated from training conditions.

## Robustness tests

- Perturb one factor at a time for interpretability before interactions.
- Check sensitivity to metric thresholds/windowing.
- Check sensitivity to seeds and selected layouts.
- Validate that conclusions are not determined by one pathological run.
- Repeat critical comparisons under at least one reasonable alternative analysis when predeclared.

## Run lifecycle

Required statuses:
`queued`, `preparing`, `running`, `pausing`, `paused`, `resuming`, `stopping`, `stopped`, `cancelling`, `cancelled`, `completed`, `failed`, `interrupted`, `invalid`, `excluded`.

- Status transitions must be explicit and timestamped.
- “Progress” must be derived from measurable work units or declared indeterminate.
- Pause/resume is supported only when state can be checkpointed safely.
- Restart creates a new run linked to the parent; it does not overwrite history.
- Resume from checkpoint records checkpoint ID and source run.
- Cancellation reason and failure stack/context are retained.

## Computational budget

Before final matrix:
- benchmark environment step throughput,
- benchmark each candidate family on minimal configs,
- estimate total wall-clock, storage and memory,
- include failed/retry allowance,
- define concurrency consistent with CPU/RAM,
- avoid assuming usable GPU acceleration,
- document which compute dimension is equalized and which is merely reported.

## Data outputs

At minimum:
- run manifest and resolved config,
- event/status log,
- raw episode/step metrics at justified granularity,
- summary metrics,
- checkpoints where enabled,
- environment/scenario identifiers,
- warnings/errors/failure reason,
- system/software snapshot,
- checksums,
- artifact references.

## Statistical analysis

Before final results:
- define unit of analysis,
- define primary and secondary estimands,
- define pairing/blocking structure,
- define aggregation across episodes, seeds, layouts and severities,
- define interval/effect-size procedure,
- define multiple-comparison strategy where relevant,
- define missing/failed/censored handling,
- define outlier and exclusion rules,
- define sensitivity analyses.

## Links to thesis evidence

Every final figure/table must identify:
- experiment IDs,
- included/excluded run IDs,
- raw and processed source paths,
- analysis script/version,
- metric/config version,
- Git commit,
- generation date,
- caption claim scope.
