# T-527 Physical Windows Tuning and Sizing Runbook

**Status:** DEC-055 and DEC-056 physical sizing attempts retained valid-failed; no resume/rerun authorized
**Decision:** `docs/decisions/DEC-055_PROTOCOL_V2_FAIR_TUNING_AND_SIZING_AUTHORITY.md`  
**Plan:** `configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json`  
**Entrypoint:** `scripts/run_protocol_v2_t527_tuning_sizing_windows.ps1`

## Purpose and boundary

This runbook executes the single reviewed T-527 non-final development program on the authoritative native Windows thesis PC. It performs fair six-candidate tuning for each of Q-Learning, SARSA, DQN, PPO and Dyna-Q+, selects one configuration per method mechanically, selects the common Phase-A budget from the declared 4,096/8,192 rule, and performs fresh 24-root precision/runtime sizing on the two development layouts and two primary action remaps.

It never executes T-526 again, never accesses final reserve, never creates final layouts/roots, and never generates confirmatory outcomes. Tuning and sizing evidence are not final thesis evidence.

## Reviewed-head gate

Before execution, the committed entrypoint requires:

- native Windows CPython 3.12 and the locked CPU-only protocol-v2 environment;
- branch `feat/pre-wp7-protocol-v1.1-ui-rebuild`;
- a clean native-Windows worktree;
- local HEAD equal to the fetched remote branch and draft PR #92 head;
- both `Repository checks / sanity` and `Protocol-v2 pilot checks / focused-conformance` green on that exact head;
- successful integrity/lineage validation of every immutable T-526 evidence package;
- the committed deterministic input-diagnostics package;
- absent/empty new tuning and sizing output directories.

## Command

From the repository root in native Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_t527_tuning_sizing_windows.ps1
```

The entrypoint may execute once. Do not resume or rerun a partial/failed package. A failure is retained and requires explicit scientific or infrastructure review without seed/config replacement.

## Expected evidence

- `results/pilots/protocol-v2-t527-input-diagnostics-v0.1/` — deterministic descriptive T-526 input audit;
- `results/pilots/protocol-v2-t527-tuning-v0.1/` — 180 candidate units, selection scores, runtimes, failures and integrity;
- `results/pilots/protocol-v2-t527-sizing-v0.1/` — 240 selected-config Phase-A sizing units, 480 action-remap matched sets evaluated at both 256 and 512 interactions, deployment-start checkpoints, root precision, runtime and integrity.

Only after these packages validate may DEC-056 freeze the final held-out layouts, final root reserve, final statistics, retained configurations/budgets/conditions and the machine-readable protocol-v2.0 firewall. DEC-056 does not execute that reserve.

## Retained execution result

Authority commit `357c38cc5effafbb7fd45e464b37cd3e22eef84b` passed the reviewed-head gate. Native Windows CPython 3.12.13, Stable-Baselines3 2.9.0 and CPU-only Torch executed the entrypoint once. The focused pre-run suite passed 30 tests and immutable-input validation passed.

- tuning: 180/180 complete, zero failures, 1,474,560 training interactions and 417,408 isolated probe interactions;
- selected development configurations: `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06`, `dyna-c03`;
- selected development Phase-A budget: 8,192 interactions under the frozen rule;
- sizing retained: 97/240 Phase-A units, 192/480 matched sets, 1,536 branch-horizon evaluations, 192 common-prefix interactions and 393,216 completed recorded branch interactions;
- runtime through failure: 2,894.3 seconds from scientific-program start to retained integrity finalization (2,346.8 seconds through completed tuning and approximately 547.5 seconds in partial sizing);
- failure: `dqn / t527-size-r01 / gw-l1-a`, `AttributeError: 'tuple' object has no attribute 'shape'` at the Frozen SB3 post-reset inference boundary;
- classification: infrastructure/type-boundary failure; zero scientific failures;
- integrity: tuning 4 hash-covered files/287,709 bytes and sizing 101 hash-covered files/3,911,282 bytes, with zero recomputed hash/size mismatches;
- final reserve: not accessed.

Do not resume or rerun these directories. No sizing selection or DEC-056 final freeze is valid from the partial evidence.

## DEC-056 sizing-only v0.2

DEC-056 is the new correction/retry authority, not the final freeze. It preserves tuning-v0.1 and sizing-v0.1 immutably, validates both before execution, and starts a new complete sizing matrix from unit one. The project scientific observation remains `(x, y)`; the SB3 facade alone emits the same coordinates as a strict declared-dtype MultiDiscrete ndarray. Adaptive method-native update opportunities are recorded at 256 and 512 and are now enforced together with the original completed-episode criterion.

- Authority: `docs/decisions/DEC-056_T527_SIZING_OBSERVATION_BOUNDARY_RETRY.md`
- Configuration: `configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json`
- Entrypoint: `scripts/run_protocol_v2_t527_sizing_v02_windows.ps1`
New evidence: `results/pilots/protocol-v2-t527-sizing-v0.2/`

After the committed authority matches local/remote/draft PR #92, both required checks are green and the native worktree is clean, execute exactly once:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_t527_sizing_v02_windows.ps1
```

The entrypoint does not execute tuning. Expected valid-complete denominators are 240 Phase-A units, 480 matched sets, 1,920 branches and 3,840 branch-horizon evaluations. Any failure is retained with no resume or second DEC-056 retry. Final reserve remains inaccessible. Only a valid-complete result may support DEC-057 and the machine-readable protocol-v2.0 freeze.

## Retained DEC-056 result

Authority commit `51612fe3ca216280d19afb69cd48f594e6ca2290` passed both checks and clean native preflight. The one fresh run retained 137/240 Phase-A units, 272/480 matched sets, 1,088 branch executions and 2,176 branch-horizon evaluations before `dqn / t527-size-r21 / gw-l1-a` failed. It accounts for 272 common-prefix interactions and 557,056 post-boundary branch interactions. The integrity manifest covers 142 files / 57,135,229 bytes with zero recomputed mismatches. There were zero scientific failures, one infrastructure failure and no final-reserve access.

The adapter correctly covered persistent continuation attachment/step/reset and progressive 256→512 Frozen execution. The shared no-learning prefix was a separate direct stochastic inference surface: it reset the project environment to a tuple and called DQN prediction before converting the MultiDiscrete container. Root 21's exploration draw entered SB3 2.9.0's pre-policy vectorization branch, which accessed `.shape` and raised `AttributeError`. Earlier completed roots do not validate that missing surface because their stochastic draws bypassed it.

Do not resume, rerun, copy, delete, replace or hand-edit sizing-v0.2. It cannot support horizon/root-count selection or DEC-057. T-527/T-528 remain blocked and #95 remains 7/10.
