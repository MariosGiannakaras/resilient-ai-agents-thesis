# Pilot Protocol v0.1

**Protocol identity:** `pilot-v0.1`  
**Lifecycle state:** pilot-unfrozen; amendable before `protocol-v1.0`  
**Machine-readable authority:** `configs/protocols/pilot-v0.1.json`  
**Validator:** `src/resilient_agents/pilot_protocol.py`

This protocol controls tuning and diagnostic pilots only. Its outputs may inform a later protocol version but are never final thesis evidence. Any material change creates a new pilot protocol version, preserves earlier runs under their original identity, and requires the affected pilot checks to be rerun.

## Pilot questions

The bounded pilot asks whether F0 frozen nominal Q-learning, C0 continual Q-learning, and R0 declared-set robust planning can be executed reproducibly and remain scientifically distinct under:

1. an unannounced persistent action remap represented in R0's declared uncertainty set;
2. a maximal remap deliberately outside that set;
3. supporting single-factor action-failure and observation-corruption diagnostics.

The pilot measures runtime, storage, failures, seed/layout sensitivity, nominal cost, degradation, recovery/non-recovery, terminal behavior, metric-parameter sensitivity, and whether the retained roles remain informative. Eight diagnostic seeds do not authorize inferential or final comparative claims.

## Evidence firewall and partitions

All layouts are explicit 7x7 grids with six obstacles, the same `(0,0)` start, `(6,6)` goal, and nominal shortest-path length 12. Holding grid size, obstacle count, and shortest-path length fixed prevents stage identity from being confounded with nominal path scale while still changing topology.

| Stage | Layout IDs | Permitted use |
|---|---|---|
| development | `dev-l01`, `dev-l02` | implementation, deterministic debugging, preflight |
| tuning | `tune-l01`, `tune-l02` | Q hyperparameter and common checkpoint selection |
| pilot | `pilot-l01`, `pilot-l02` | predefined diagnostic pilot outcomes only |
| final reserve | `final-l01`, `final-l02` | structural validation only before final freeze; no tuning, pilot, or outcome inspection |

The validator rejects duplicate IDs, overlap, missing stages, layout/partition drift, reachability changes, or shortest-path drift. A runtime request must pass the existing stage-access firewall. Final-reserve definitions may be structurally/schema validated because that does not inspect agent outcomes; executing them is forbidden until the later frozen-protocol and application gates permit it.

## Environment and performance unit

- Reward is `-1` for a valid non-goal step, `-2` for a collision, and `0` on reaching the goal. Higher episode return therefore directly represents fewer navigation steps/collisions without an arbitrary goal bonus.
- Episode horizon is four times the shared nominal shortest path: `4 x 12 = 48` transitions. This topology-normalized diagnostic cap provides three shortest-path lengths of detour allowance beyond an optimal route; pilot truncation/censoring determines whether a later amendment is needed.
- The agent sees only delivered position, intended action lifecycle, and reward through the strict all-hidden `InformationPolicy`. Executed action, disturbance flags, change truth, regime ID, and true state remain evaluator-only.
- The curve unit is episode return. Episodes nested within one root-seed/layout/agent/condition unit are repeated measurements, not independent replicates.

## Persistent-change lifecycle

The scientific changepoint is between episode blocks, not late within one goal-terminating episode:

1. load the selected nominal checkpoint (F0/C0) or precomputed robust plan (R0);
2. execute 16 nominal pre-change episodes;
3. switch the evaluator's scenario at the episode boundary without resetting agent learning state;
4. execute 32 post-change episodes under the selected condition;
5. run a matched nominal reference branch for all 48 episodes from the same checkpoint, layout, root seed, and derived episode-seed schedule.

Each post-change GridWorld episode encodes an action remap at local step zero, so the new dynamics remain active throughout every post-change episode. The runner records one global changepoint at episode index 16 for metric computation; repeated local environment event emission is provenance, not a sequence of new scientific changes. This design gives a meaningful pre/post episode-return curve while preserving the GridWorld's correct goal termination semantics.

For each root seed, nominal training produces a root-specific checkpoint so training variability remains part of the independent unit. F0 and C0 use that identical checkpoint/checksum and deployment exploration schedule within the root. F0 never updates after checkpoint load; C0 continues its standard update across episode boundaries. R0 is planned from the recorded nominal model and fixed uncertainty set, uses the common deployment epsilon, and never replans or learns from pilot outcomes.

## Conditions and severity rationale

Only one factor changes at a time; compound disturbances are excluded from v0.1.

| Condition | Role | Severity rationale |
|---|---|---|
| `nominal` | matched reference / nominal cost | identity dynamics, no disturbance |
| `remap-min-in-set` | primary in-set persistent change | one transposition remaps two actions, the smallest possible non-identity action permutation |
| `remap-max-out-of-set` | primary out-of-set persistent change | four-action derangement changes every action and is excluded from R0's prior |
| `action-failure-1of8`, `action-failure-1of4` | supporting action diagnostic | dyadic 1/8 and 1/4 probabilities provide separated low/higher incidence without claiming final severity |
| `observation-corruption-1of8`, `observation-corruption-1of4` | supporting observation diagnostic | the same dyadic incidence levels isolate mechanism rather than severity-grid differences |

R0's set `rectangular-remap-prior-v0.1` is frozen before pilots and contains only identity plus the minimal transposition. The planner uses the state-action-rectangular closure of the transition rows induced by those mappings, rather than pretending the two global mappings are one coupled uncertainty draw. It therefore receives a declared stronger prior in the in-set condition but never the realized active kernel or changepoint. The out-of-set condition tests the limitation of that prior rather than being silently added after outcomes are seen.

## Tuning and checkpoint rule

The four tuning roots and eight pilot roots are disjoint and committed before outcomes. Each is the unsigned big-endian integer from the first eight bytes of SHA-256 over `pilot-v0.1`, the stage, and the zero-based index separated by NUL bytes; component RNG streams continue to use the accepted independent derivation function.

Tuning is bounded engineering selection, not statistical evidence:

- train for 512 episodes per tuning layout and evaluate nominally for 64 episodes per tuning layout/root;
- stage one evaluates the 4 x 4 dyadic learning-rate/exploration grid at discount `15/16`;
- stage two evaluates the two remaining discounts (`7/8`, `31/32`) only for the stage-one winner, for 18 unique Q configurations total;
- select by highest mean nominal return, then highest worst-layout mean, then lowest collision rate, then canonical hyperparameter JSON order;
- preserve every tried configuration and outcome;
- create one common selected nominal Q checkpoint for F0/C0 and record its checksum;
- keep the R0 uncertainty set fixed; pilot outcomes cannot tune it.

The dyadic candidates span materially different update, exploration, and effective-horizon regimes with a small reproducible search rather than importing unexplained library defaults. If pilot behavior exposes a boundary failure, a new tuning/protocol version is created; pilot outcomes are not directly searched as an extra tuning set.

## Metrics and preliminary analysis

Every disrupted branch is matched to its nominal reference curve. Schema-v1 estimands are computed over episode returns with:

- immediate window: 1 episode;
- worst-window sensitivity: 2, 4, and 8 episodes;
- terminal-window sensitivity: 4 and 8 episodes;
- recovery tolerance sensitivity: 0, 1, and 2 step-reward units;
- recovery stabilization sensitivity: 2, 4, and 8 episodes.

These are a predeclared sensitivity grid, not multiple opportunities to choose the most favorable result. They diagnose identifiability/censoring and inform `protocol-v1.0`; they cannot select agents or create final claims. Non-recovery remains `NOT_RECOVERED` with null recovery time. The pilot unit is root-seed x layout x agent x condition, paired by the identical root/layout/checkpoint/episode-seed schedule. Report raw unit distributions and recovery-status counts; no inferential claim is allowed from v0.1.

## Resource and stopping policy

- Native Windows CPython 3.12 in the locked `uv` environment and CPU execution are required; GPU is neither required nor assumed.
- Start with concurrency one so timing and memory evidence are interpretable. Pilot evidence may justify a later bounded concurrency change.
- A preflight measures one representative child configuration. Timeout is `20 x` its estimate, floored at 60 seconds. If the estimate would exceed the 7,200-second ceiling, do not truncate science silently: amend the protocol before pilots.
- Training and evaluation use their fixed episode counts. There is no early success stopping.
- Invalid/non-finite state fails immediately and is retained. Timeout finalizes the child as failed with partial output retained.

## Failure, exclusion, and artifacts

Every valid completed run is included regardless of poor return, truncation, or non-recovery. No automatic outlier exclusion exists. A retry uses a new linked run ID and never overwrites the original.

Invalid execution is limited to recorded schema/contract, provenance, checksum/finalization, information-boundary, or non-finite-state violations. Later analysis exclusion requires a confirmed implementation defect, confirmed external interference affecting scientific validity, or a predeclared scenario/agent contract violation. Execution outcome remains unchanged and visible when an analysis exclusion is added.

Each child/whole experiment preserves the resolved protocol/scenario, all root/derived seeds, source/runtime provenance, Q checkpoint or robust-plan checksum, event log, episode-return curves, execution outcome/reason, metric sensitivity summaries, manifest, and checksums. `T-401` now enforces this protocol through the resumable CLI/core path documented in `HEADLESS_RUNNER.md`; `T-402` must derive reproducible summaries before `T-410` pilots execute.
