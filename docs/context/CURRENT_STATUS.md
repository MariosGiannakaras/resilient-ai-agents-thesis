# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger; use progressive task-specific reading for detailed decisions/evidence.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine validation and `T-200` research framing through completed historical WP6 v1.0 evidence.
- `protocol-v1.0`, finalized `FINAL-*`, frozen historical analysis and R0 pilot evidence remain immutable.
- **Project: 4/8** master milestones complete (#87: 1, 2, 4, 5).
- **Current task:** `T-524 IN_PROGRESS` — source-backed protocol-v2 research contract.
- Active tracker: #95 **1/10**. Historical #88 closed/superseded at 9/12; its unfinished T-522/v1.1 tuning/freeze work must not execute.
- #93 radical UI redesign is PAUSED until the v2 scientific workflow stabilizes. The current NiceGUI UI/runtime is a technical prototype/foundation, not the accepted final interface.
- Final standalone `.exe` packaging is post-thesis #94 / `T-803`, not a pre-WP7 gate.
- **Pre-WP7 approval: NOT APPROVED.** All `T-700+` execution remains blocked.

## Why protocol v2

Candidate v1.1 is a valid adaptation-mechanism experiment, but its strategies begin evaluation from the same selected tabular Q-learning checkpoint. It therefore cannot support genuine end-to-end claims about how different RL algorithms learn. DEC-048 supersedes future v1.1 final execution while preserving v1.1 as auditable non-final history.

Protocol v2 separates two questions:

1. **Nominal learning:** independently trained methods under a common semantic environment/information/resource contract.
2. **Resilience/adaptation:** each method/root's trained checkpoint cloned into matched **Frozen** and **Continual** deployment regimes, each with a same-regime no-change reference.

GridWorld remains the controlled testbed/visualization environment, not the thesis subject.

## Candidate method roles

Strong core candidates, still pilot-gated:

- **Q-Learning** — tabular off-policy value learning;
- **SARSA** — tabular on-policy value learning;
- **DQN** — neural off-policy value approximation;
- **PPO** — neural on-policy policy-gradient/actor-critic optimization;
- **Dyna-Q+** — learned-model planning plus directed re-exploration for change.

**Dyna-Q** is a useful Dyna-Q+ planning ablation. **A2C** is a secondary actor-critic candidate; full final inclusion requires distinct-value evidence because it overlaps mechanistically with PPO. Historical R0 remains negative/diagnostic. No final method count is frozen yet.

## Fair-learning contract

- Principal common training budget: **environment interactions/timesteps**, not equal episodes or equal optimizer updates.
- Each algorithm gets a small literature-backed configuration set and equivalent tuning opportunity on tuning-only partitions; library defaults are not automatically fair final settings.
- Periodic standardized **no-learning evaluation** checkpoints separate learned policy quality from exploratory/stochastic training return.
- Roots/seeds are randomization units, never tunable parameters; nested episodes are not independent replicates.
- Final root/layout/matrix size is selected from non-final variance/precision/runtime evidence rather than copied automatically from v1.1.
- Preserve effect sizes/95% intervals, negative/null/failed/non-recovery outcomes, paired designs where valid, recovery as secondary/sensitivity and no composite resilience score.

## Continual-deployment contract

`Continual` means ordinary method-native continued training, not a claim that DQN/PPO/etc. are specialized continual-learning algorithms. Deep RL can suffer forgetting/plasticity limitations under non-stationarity, so these effects are part of interpretation rather than hidden.

Frozen and Continual branches for one method/root start from the exact same trained scientific state. Checkpoint semantics are algorithm-specific: DQN continuation includes network/target/optimizer/replay/exploration/RNG state; actor-critic continuation includes policy/value/optimizer/schedule/RNG state and clones only at valid update boundaries.

## Environment and uncertainty

Do not add pixels, partial observability or a large external benchmark merely to justify deep RL. `T-526` will pilot only a small bounded set of project-owned GridWorld complexity levels and keep the simplest one that avoids clear floor/ceiling effects while remaining CPU-feasible on the validated Windows thesis machine.

Current uncertainty taxonomy remains strong unless pilots justify amendment:

- primary persistent change: action remapping;
- supporting actuation uncertainty: action-execution failure;
- supporting perceptual uncertainty: observation corruption.

Additional drift/dynamic-obstacle/reward-change conditions are not added for variety.

## Bibliography and provenance

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable consumer snapshot is still **`bibliography-integration-v3`**. Bibliography issue #135 now owns the v2 methodology refresh: re-evaluate existing DQN/plasticity/PPO/statistical records first, add only missing primary/methodology sources, then enter this repo through a later versioned synchronization.

## Still intentionally unfrozen

Exact v2 final methods, environment complexity, interaction budget, hyperparameters, checkpoint/update schedules, final roots/layouts, primary contrast set, final evidence, redesigned UI and final thesis/presentation remain intentionally unfrozen until their declared gates pass.

## Exact next action

Complete `T-524`: finish the canonical bibliography refresh and freeze the source-backed v2 RQs, estimand roles and method-role gates. Then `T-525` implements the common multimethod training/checkpoint foundation, followed by `T-526` Windows CPU/environment/method pilots and `T-527` fair tuning/statistics/protocol-v2 freeze. Do not run old T-522, access any final reserve, resume UI redesign #93, or start WP7.
