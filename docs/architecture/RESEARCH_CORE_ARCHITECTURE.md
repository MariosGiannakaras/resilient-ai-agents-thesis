# Research Core Architecture

**Status:** Accepted implementation boundary; scientific protocol still unfrozen.

## Boundary

The thesis uses one importable Python package under `src/resilient_agents/` as the only home of scientific execution logic. Tests, scripts, future CLI entry points, and the future Streamlit dashboard call the same package.

The UI never implements agent learning, environment transitions, disturbance logic, metric calculation, run persistence, or provenance.

## Core contracts

- `contracts.py`: common agent contract, scenario/experiment contracts, change events, retention policy, protocol stage, and the agent-information boundary.
- `environment.py`: environment protocol and explicitly separated RNG seed channels.
- `randomness.py`: deterministic independent streams for scenario generation, environment stochasticity, action disturbance, observation disturbance, agent exploration, and agent initialization.
- `metrics.py`: known-answer resilience metrics. Scientific thresholds are explicit inputs, never hidden defaults.
- `protocol.py`: non-overlapping development/tuning/pilot/final scenario partitions.
- `run_bundle.py`: filesystem-first immutable run evidence with resolved config, capability snapshot, provenance, checksums, events, traces, and summary.
- `session.py`: whole-experiment lifecycle. One experiment may contain many seeds/episodes; publication occurs once after finalization.
- `git_publish.py`: guarded one-commit/one-push publication of the finalized experiment bundle.

## Information boundary

Every environment step produces complete evaluator-visible ground truth. `project_for_agent()` exposes only what the experiment's explicit `InformationPolicy` allows. Hidden regime identifiers, realized change points, true state, executed action, and disturbance flags are not silently available to an agent.

This prevents accidental information leakage and makes agent comparisons auditable.

## Scenario versus experiment

A `ScenarioSpec` describes the world and uncertainty mechanism. An `ExperimentSpec` describes the comparison: protocol version/stage, scenario IDs, agent IDs, seeds, budgets, metrics, retention policy, and publication behavior.

Scientific quantities such as severity, change onset, seed set, budget, and recovery threshold must be explicit in a version-controlled config. Missing scientific values are validation errors rather than convenience defaults.

## Storage model

The filesystem is the source of truth. Any future SQLite/index/database is disposable and rebuildable from committed run bundles. It must never become the only copy of scientific evidence.
