# GridWorld Specification Workspace

**Status:** Schema-v1 core/invariants and validated `pilot-v0.1` diagnostic scenarios implemented; final experiment values remain unfrozen.

The technical pre-screen in `docs/research/GRIDWORLD_LANDSCAPE_REVIEW.md` and completed comparison in `docs/research/GRIDWORLD_PROTOTYPE_COMPARISON.md` support DEC-032's selection of a small project-owned Gymnasium environment. DEC-023 already establishes the shared environment/information/randomness/run architecture in `src/resilient_agents/`; GridWorld work must use those contracts rather than create parallel interfaces.

## Confirmed purpose

The environment must be simple, controlled, and suitable for comparative evaluation of decision agents under uncertainty and dynamic change. It must support repeatable episodes, explicit disturbance parameters, trace capture, metric validation, and headless execution independent of the dashboard.

Official examples include observation/data noise, rule changes, and action-execution failures. These remain scope examples rather than a frozen factorial design.

## Evaluated implementation candidates

The completed bounded comparison evaluated:

| Strategy | Current role | Required evidence before selection |
|---|---|---|
| Project-owned Gymnasium-compatible environment | **Selected by DEC-032** | Direct accepted semantics, smaller dependency/reasoning surface, deterministic tests, and target-machine feasibility. |
| Thin MiniGrid adaptation | Rejected for the core path | Equivalent fixture behavior required project translation/bypass and added dependency/platform/tag-license uncertainty without a required capability advantage. |

Gymnasium Toy Text environments may serve as reference fixtures. Other engines/frameworks are not added unless they solve a concrete requirement the retained prototype paths cannot satisfy.

## Shared architecture already decided

The final GridWorld must integrate with the accepted core contracts:

- evaluator ground truth is distinct from delivered agent observation;
- agent-visible optional information is explicitly policy-controlled;
- intended and executed actions are separately representable;
- change/disturbance events are structured rather than hidden `if step == ...` behavior;
- independent RNG streams isolate environment, observation disturbance, action disturbance, exploration, and initialization randomness;
- scenario/experiment/protocol configs do not contain hidden scientific defaults;
- traces/run bundles are UI-independent and provenance-bound.

These are implementation invariants, not final scientific parameter choices.

## Implemented schema-v1 semantics

- State is an explicit `(x, y)` coordinate in a rectangular grid with explicit start, goal, and obstacle cells; nominal reachability is validated.
- Actions are the stable `up`, `right`, `down`, and `left` identifiers with explicit canonical cardinal vectors; persistent remapping is represented only by a change event.
- Boundaries and obstacles are collisions that preserve position. Explicit finite `step`, `collision`, and `goal` rewards apply with goal precedence.
- Reaching the goal terminates; exhausting the explicit positive `max_steps` truncates only when the goal was not reached.
- Reset returns the explicit true start state. Transition observations are explicit positions and may undergo a separately seeded position-mislocalization process that never changes truth.
- No-op action-execution failure is separately seeded and preserves intended versus executed action.
- Schema v1 supports zero or one exact-step persistent action-remap event. Its declared remap count must match the mapping; onset is emitted once and the regime persists.
- Evaluator truth is stored as `GroundTruthTransition`; Gymnasium `info` stays empty and agent visibility is controlled only by `InformationPolicy`.
- Reset requires all `EnvironmentSeeds` channels. Resolved fixed layouts retain the scenario seed for provenance/future versioned generation, Gymnasium receives the environment seed, and the two disturbance seeds drive only their named streams. Episodes cannot be stepped before reset or after termination/truncation.
- Canonical serialization carries `gridworld_schema_version: 1`, rejects missing/unknown state, and round-trips the resolved scenario.
- The environment is headless. Evaluator-only debug state exists for trace parity and is not an agent or UI execution path.

## Pilot-v0.1 diagnostic specification

The pre-final pilot protocol now fixes eight disjoint same-scale 7x7 layouts (two per lifecycle stage), six obstacles, shortest-path length 12, step/collision/goal rewards `-1/-2/0`, and a 48-step episode cap. Its primary episode-block change uses minimal in-set and maximal out-of-set action remaps; dyadic action/observation disturbances remain supporting single-factor diagnostics. Exact layouts and rationale are validated from `configs/protocols/pilot-v0.1.json` and documented in `docs/experiments/PILOT_PROTOCOL_V0_1.md`. These values are pilot inputs, not final thesis parameters.

## Final scientific specification decisions still required

1. Final grid dimensions, layout/scenario families, and concrete start/goal instances or distributions.
2. Final reward values, horizons, and comparability rules across retained changes.
3. Which supported disturbance/change conditions enter primary versus supporting analyses.
4. Final probabilities, severities, onset, persistence/combination matrix, and whether the pilot partitions survive freeze.
5. Whether formal partial observability is scientifically required; schema v1 otherwise retains position observation plus controlled corruption.
6. Any versioned scenario generator needed beyond explicit resolved layouts.
7. Training/adaptation/evaluation regime and final experiment reference scenarios.

No grid size, reward value, severity, changepoint, horizon, or recovery threshold is accepted merely as a convenient default.

## Completed implementation validation

- nominal deterministic reference trace;
- boundary/invalid-action behavior;
- obstacle collision semantics;
- goal reward and exact termination;
- step-limit truncation;
- independent seeded replay for each stochastic mechanism;
- exact scheduled change onset and persistence;
- observation corruption does not mutate true state;
- action-execution failure preserves intended versus executed action distinction;
- hidden regime/change metadata is not exposed to agents unless explicitly permitted;
- serialization round trip;
- state isolation between episodes;
- evaluator debug-state/trace parity (no renderer is implemented);
- prototype wrapper parity for the rejected MiniGrid alternative;
- headless performance smoke benchmark on the actual target machine.

The 10 deterministic core tests in `tests/test_gridworld.py` cover these applicable conditions. The fixed fixture values are test evidence only, not experiment defaults.

## ADR gate

DEC-032 satisfies the implementation ADR gate, and `T-212`/`T-213` implement and validate the selected path. Later scientific parameter selection must use explicit schema-v1 scenarios and may reopen the decision only under DEC-032's recorded triggers.
