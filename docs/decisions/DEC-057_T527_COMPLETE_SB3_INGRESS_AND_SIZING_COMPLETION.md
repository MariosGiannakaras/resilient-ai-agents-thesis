# DEC-057 — T-527 complete SB3 direct-inference boundary correction and final sizing completion authority

**Status:** accepted pre-outcome authority; one physical sizing-v0.3 completion attempt pending
**Date:** 2026-08-30
**Task:** T-527
**Configuration:** `configs/protocols/protocol-v2-t527-sizing-completion-v0.3.json`
**Entrypoint:** `scripts/run_protocol_v2_t527_sizing_v03_windows.ps1`

## Context

DEC-055 tuning remains immutable valid-complete. DEC-055 sizing-v0.1 and DEC-056 sizing-v0.2 remain immutable valid-failed. DEC-056 corrected the new multi-episode continuation facade but its one authorized run exposed a separate direct stochastic ingress in `prepare_shared_no_learning_prefix()`. Earlier DQN prefix calls passed only when the stochastic exploration branch was not selected.

DEC-056 is not rewritten and authorizes no rerun. This decision consumes DEC-057 as the next pre-outcome correction/completion authority. The eventual final scientific freeze therefore moves to DEC-058 and is permitted only after one objectively complete five-method sizing matrix.

## Decision

### 1. Central direct-inference boundary

All active direct project-GridWorld SB3 prediction surfaces use `predict_sb3_gridworld_action()`. It converts only the `(x, y)` container through `as_sb3_gridworld_observation()` and proves exact declared dtype, shape, integer values and space membership. It adds no information, normalization, clipping or RNG. Stochastic prediction retains exactly the restored adapter RNG semantics.

The exhaustive inventory and callsite classifications are frozen in `docs/research/T527_SB3_DIRECT_INFERENCE_BOUNDARY_AUDIT.md`. The shared prefix applies the boundary before every SB3 prediction, not only its first interaction. Training/Adaptive paths continue through the declared Gym/VecEnv interface. A maintainability guard fails if a new active direct `.predict()` call bypasses the canonical boundary.

### 2. Structural reuse of complete unaffected strata

Q-Learning and SARSA sizing-v0.2 are accepted as immutable sizing components solely because all structural, integrity and code-lineage conditions pass before new outcomes:

- each contains 48/48 Phase-A units and 96/96 matched sets over the exact 24 roots, two layouts, two remaps and both horizons;
- all update-opportunity fields, branch identities, budgets, probes, prefix/lifecycle and configurations are exact;
- every source row and deployment checkpoint is hash-identified and integrity-valid;
- neither method has a retained failure;
- tabular learner/driver, environment, randomness, scenario, settlement and sizing paths are unchanged;
- the normalized shared-prefix project-method AST is identical to the retained baseline;
- the new correction is selected by learner type and changes only SB3 representation ingress;
- no performance value or runtime preference is used for reuse.

This is not a resume of sizing-v0.2. That package remains valid-failed. Its incomplete DQN stratum is prohibited. Every sizing-v0.1 row is prohibited.

### 3. One fresh three-method completion

The one authorized physical run starts from the first DQN unit and executes from scratch:

- DQN: 48 Phase-A units / 96 matched sets;
- PPO: 48 / 96;
- Dyna-Q+: 48 / 96.

The total fresh scope is 144 Phase-A units, 288 matched sets, 1,152 branches and 2,304 branch-horizon evaluations. It uses the unchanged DEC-055 winners, 8,192 budget, six probes, 24 sizing roots/seeds, two development layouts, two action remaps, 256/512 horizons, one nominal no-learning prefix and persistent multi-episode lifecycle.

Output is only `results/pilots/protocol-v2-t527-sizing-v0.3/`. Any failure is retained and stops DEC-057. There is no resume, second execution, seed replacement, scope change or tuning rerun.

### 4. Derived complete matrix

Only a valid-complete fresh package may create `results/pilots/protocol-v2-t527-sizing-combined-v0.3/`. The package stores source references, exact row numbers/hashes and checkpoint hashes rather than duplicating checkpoint payloads. It must prove exactly five methods, 240 Phase-A units, 480 matched sets, 1,920 branches and 3,840 branch-horizon evaluations with no missing/duplicate cell, no sizing-v0.1 row and no incomplete v0.2 DQN row.

The unchanged horizon rule selects 256 only when every Adaptive branch has at least two native update opportunities and two completed episodes; otherwise it selects 512. Root candidates remain exactly 12/16/20/24 with the frozen Student-t 95% half-width target 0.20 and frozen critical values.

## Authority gate and firewall

Before execution, implementation, tests, configuration, audit and canonical reconciliation must be committed and pushed; Repository and Protocol-v2 checks must be green on the exact PR #92 head; the PR must remain open/draft; and native Windows Git must be clean/current.

The entrypoint validates immutable T-526, tuning-v0.1, sizing-v0.1, sizing-v0.2 and the complete Q-Learning/SARSA reuse barrier before writing. It executes no tuning, held-out layout, final root or final-reserve agent.

DEC-058, final layouts/roots and `protocol-v2.0-final` may be materialized only after the combined matrix validates. T-528, T-610+, WP7 and PR merge remain prohibited here.
