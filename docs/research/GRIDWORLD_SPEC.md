# GridWorld Specification Workspace

**Status:** Active; DEC-032 selects a project-owned environment using the locked Gymnasium 1.3.0 API, while scientific parameters remain unfrozen.

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

## Scientific specification decisions still required

1. Grid dimensions/layout family and coordinate convention.
2. Start/goal distribution or fixed scenario sets.
3. Obstacle/collision semantics.
4. Final action set and nominal transition semantics.
5. Reward/penalty semantics and comparability across changes.
6. Episode termination/truncation rules.
7. Observation schema and final observability class.
8. Reset/scenario-generation behavior.
9. Exact disturbance/change mechanisms.
10. Severity, onset, duration, persistence, and combination rules.
11. Training/adaptation/evaluation regime.
12. Serialization/version identifiers.
13. Reference traces/known-answer fixtures.

No grid size, reward value, severity, changepoint, horizon, or recovery threshold is accepted merely as a convenient default.

## Required validation suite

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
- renderer/trace parity where rendering exists;
- wrapper parity tests if third-party code is used;
- headless performance smoke benchmark on the actual target machine before final matrix freeze.

## ADR gate

DEC-032 satisfies the implementation ADR gate after both retained paths were compared on scientific semantic transparency, implementation/dependency cost, deterministic testability, disturbance extensibility, information-access correctness, and measured feasibility. `T-212`/`T-213` must now implement and validate the selected path without treating the prototype fixture as frozen scientific configuration.
