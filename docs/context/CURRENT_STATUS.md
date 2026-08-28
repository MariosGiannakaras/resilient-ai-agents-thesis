# Current Project Status

**Date:** 2026-08-28  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use **progressive** task-specific reading of DEC-048/049/050 and `docs/research/` only as needed.

## Current execution state

- Historical accepted baseline includes completed `T-100` target-machine validation and `T-200` research framing through protocol-v1.0 WP6 evidence. Frozen protocol-v1.0, `FINAL-*` and R0 evidence remain immutable. Candidate v1.1 is auditable non-final history; old `T-522` must not execute.
- **Project: 4/8** master milestones complete (#87: 1, 2, 4, 5). **`T-524` and `T-525` are COMPLETE; current task: `T-526` READY for physical Windows evidence.** Protocol-v2 tracker #95 is 4/10.
- T-525 closure is documented in `docs/research/PROTOCOL_V2_BACKEND_CONTRACT.md`.
- #93 final UI rebuild remains PAUSED. T-528 will rebuild from scratch with a **different framework from NiceGUI** only after T-527 freezes the remaining scientific/runtime contract.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` work.

## Protocol-v2 scientific contract

### Phase A

- Train every retained method independently under common task/reward/action semantics, common semantic agent-visible information and common task-level `gamma`.
- Fairness resource = **actual environment interactions**, not episodes, optimizer updates, wall time or requested library timesteps.
- Run standardized interaction-indexed no-learning probes only on cloned learner state; probe interactions remain outside the training budget/state.
- Core feasibility candidates: Q-Learning, SARSA, DQN, PPO, Dyna-Q+. Dyna-Q is ablation-only; A2C remains promotion/diagnostic only.

### Phase B

Each `method × root × layout` begins from its own exact Phase-A scientific checkpoint. At the exact branch point, clone identical learner/behavior/RNG state into Frozen nominal, Frozen disturbed, Adaptive nominal and Adaptive disturbed branches. Adaptive updates begin only after the boundary and do not reset replay, optimizer, epsilon, warm-up, recency or schedules.

Primary losses are immediate degradation, cumulative deficit and terminal gap against the same-regime nominal reference. Primary adaptation benefit is the matched four-branch difference-in-differences. Recovery remains secondary; no composite resilience score.

T-525 validates one exact post-boundary segment and fails closed if another environment reset is required. T-526/T-527 must explicitly freeze the final multi-episode post-boundary reset/regime semantics.

## Backend invariants and T-525 closure

- `max_steps` is administrative truncation in v2; goal arrival is termination; value learners bootstrap through truncation.
- Scientific checkpoints preserve exact continuation state: Q/SARSA schedules/RNG/counters; Dyna-Q+ learned model/recency/planning; DQN networks/optimizer/full replay/update/exploration state; PPO policy/value/optimizer/schedules/RNG at legal rollout/update boundaries.
- Exact GridWorld state includes trajectory position, seeds, disturbance RNGs, Gym RNG and last transition. Evaluator truth never substitutes for delivered observation.
- Neural initialization and later stochastic behavior/update RNG are separately rooted. SB3 algorithm RNG and project environment/disturbance RNG streams remain independent.
- Frozen branches cannot mutate learning state. SARSA requires a quiescent fork; Frozen Dyna-Q+ avoids its model-mutating learning `act()` path; DQN/PPO attach to exact restored project-GridWorld branches.
- The v2 lifecycle is separate from legacy `HeadlessExperimentRequest`; historical execution/evidence semantics were not rewritten.

Concrete pilot implementations exist for Q-Learning, SARSA, Dyna-Q+, DQN and PPO. Stable-Baselines3 2.9.0 / CPU-only PyTorch 2.9.0 is the neural pilot stack.

Closure evidence on the reviewed PR #92 implementation head: the dedicated CPU-only protocol-v2 gate passed **55 conformance tests**; repository-wide tests, documentation/JSON checks and installed-bibliography validation also passed.

## T-526 physical gate

The committed non-final plan is `configs/protocols/protocol-v2-feasibility-v0.1.json`; runbook is `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`; user-machine entrypoint is `scripts/run_protocol_v2_feasibility_windows.ps1`.

First physical pass:

- ordered GridWorld ladder: 7×7 → 10×10 → 14×14;
- two layouts/level, three roots, five core methods;
- provisional common Phase-A budget: 2048 actual interactions;
- probes: 0/512/1024/2048;
- record training/probe interactions, wall/process CPU time, checkpoint size and failures;
- select the first complete level that is neither a universal early ceiling nor a universal final floor; never select by preferred method ranking.

After the selected level is reviewed, T-526 continues with already-predeclared Phase-B calibration candidates: two categorical action-remap mappings, bounded action-failure probabilities and bounded observation-corruption probabilities with explicit global valid-cell support. A2C promotion remains conditional on distinct thesis value and acceptable matrix cost.

Hosted CI does **not** substitute for this physical-machine gate.

## Statistics / provenance

Root/run is the independent randomization unit; layouts, checkpoints and episodes are blocks/repeated observations. Student-t root-level 95% intervals remain the current primary candidate, with bootstrap/robust sensitivity and final precision/runtime sizing deferred to T-527. Scientific failures remain outcomes; infrastructure retries keep the same root identity.

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography`, immutable upstream SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`: 597 canonical sources, 121 citation-ready sources, 19 research materials. Thesis sync PR #96 is merged; `bibliography-integration-v3` remains immutable history.

## Still intentionally unfrozen

Final retained methods/A2C decision, selected GridWorld level/layouts, final budgets/gamma/reward/horizon, method hyperparameters, probe cadence, Phase-B reset lifecycle, uncertainty settings, roots/statistics, final frontend framework and final evidence remain T-526/T-527 gated.

## Exact next action

From a clean reviewed `feat/pre-wp7-protocol-v1.1-ui-rebuild` checkout on the validated native Windows thesis machine, execute exactly once:

`powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1`

Retain `results/pilots/protocol-v2-feasibility-v0.1/` unchanged for review. Do not rerun/overwrite it, access final reserve, tune methods or resume UI. After T-526 evidence is complete, T-527 freezes the remaining protocol; then T-528 starts the new-framework UI rebuild.
