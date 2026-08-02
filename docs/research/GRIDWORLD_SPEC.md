# GridWorld Specification Workspace

**Status:** `RESEARCH_REQUIRED`. No implementation has been selected and there is no legacy-code requirement.

## Confirmed purpose

The environment must be simple, controlled, and suitable for comparative evaluation of decision agents under uncertainty and dynamic change. It must support repeatable episodes, explicit disturbance parameters, trace capture, metric validation, and execution without the dashboard.

The official application gives examples including:

- data/observation noise,
- rule changes,
- action-execution failures.

These are scope examples, not a frozen taxonomy or factorial design.

## Implementation strategy to decide

The final decision will compare:

| Strategy | Description | Required evidence before selection |
|---|---|---|
| Reuse | Use a current GridWorld package/framework largely as provided. | Current maintenance, compatible license/API, deterministic seeding, required disturbance support, tests, low integration risk. |
| Adapt/wrap | Use a package for base mechanics with project-owned wrappers/extensions. | Clear boundary, pinned source, provenance, test parity, no hidden semantics, manageable upgrade policy. |
| Custom minimal implementation | Project-owned environment designed for the exact protocol. | Small scope, complete known-answer tests, explicit semantics, lower total complexity than adapting a framework. |

There is no preselected repository. Codex must perform a fresh landscape review and small prototype before an ADR. Any external code requires a pinned version/commit, license review, and attribution.

## Evaluation matrix for candidate frameworks

- Last meaningful release/commit and maintenance activity.
- License compatibility and redistribution obligations.
- Python/runtime and Gymnasium/API compatibility.
- Explicit `terminated`/`truncated` semantics.
- Seed ownership and deterministic replay.
- Extensibility for the official uncertainty examples.
- Observation/action/state configurability.
- Layout/config serialization and checksums.
- Headless speed and batch execution.
- Test coverage/source readability.
- Rendering separation from environment logic.
- Dependency size, security, and maintenance risk.
- Ability to run on the actual local system.
- Ease of provenance and version pinning.

## Specification decisions required after research

1. Grid dimensions and coordinate convention.
2. Start and goal distribution/fixed sets.
3. Obstacle representation and collision semantics.
4. Action set and nominal transition.
5. Reward/penalty semantics and scaling.
6. Episode terminal/truncation conditions.
7. Observation schema and observability class.
8. Reset behavior and scenario generation.
9. RNG streams and seed derivation.
10. Disturbance types, severity, onset, duration, and combinations.
11. Online-adaptation/frozen-policy regimes.
12. Serialization/version identifiers.
13. Trace/event schema independent of UI.
14. Validation fixtures with hand-calculated trajectories and returns.

## Required validation suite

- Nominal deterministic trace.
- Boundary and invalid-action behavior.
- Obstacle collision semantics.
- Goal reward and exact termination.
- Step-limit truncation.
- Seed replay for each stochastic mechanism.
- Scheduled rule/action/noise change at the exact step.
- Serialization round trip.
- Reachability/solvability classification where applicable.
- State isolation between episodes.
- Renderer/trace parity.
- Library-wrapper parity tests if third-party code is used.
- Performance smoke benchmark in headless mode.

## Current non-decisions

- No grid size is selected.
- No action set is selected.
- No reward values are selected.
- No partial-observability design is selected.
- No disturbance severity levels are selected.
- No framework/repository/package is selected.
- No old-conversation example is considered a default.