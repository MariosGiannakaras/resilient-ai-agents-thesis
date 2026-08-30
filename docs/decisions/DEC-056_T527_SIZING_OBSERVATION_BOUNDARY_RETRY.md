# DEC-056 — T-527 sizing observation-boundary correction and retry authority

**Status:** accepted pre-outcome authority; awaits one physical sizing-v0.2 validation  
**Date:** 2026-08-30  
**Task:** T-527  
**Configuration:** `configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json`  
**Entrypoint:** `scripts/run_protocol_v2_t527_sizing_v02_windows.ps1`

## Decision

Authorize one fresh sizing-only attempt after a project-owned, representation-only adapter correction at the SB3 GridWorld facade. Tuning-v0.1 remains immutable and is not rerun. Sizing-v0.1 remains immutable valid-failed evidence and is neither resumed nor copied. The new attempt starts all 240 Phase-A units and 480 Phase-B matched sets from unit one, using the exact DEC-055 winners, 8,192-interaction budget, development layouts, 24 sizing roots/seeds, two action remaps, 256/512 horizons, one-interaction prefix, lifecycle and precision rule.

DEC-055 anticipated DEC-056 as a possible final freeze, but the incomplete sizing matrix could not justify that decision. DEC-056 is therefore consumed by this required pre-outcome correction authority. A successful complete sizing-v0.2 result may support the next free decision, DEC-057, as the final protocol-v2.0 scientific freeze. This numbering preserves rather than rewrites DEC-055 history.

## Exact infrastructure diagnosis

The retained DQN failure is caused by an SB3 2.9.0 call-path asymmetry, not a different scientific observation. `SB3PhaseBBranchDriver._run_frozen_to()` passed the project coordinate tuple to `SB3ScientificStateAdapter.predict()`, then `DQN.predict(deterministic=False)` took its exploration branch and called `BasePolicy.is_vectorized_observation()` before policy tensor conversion. The MultiDiscrete validator in `stable_baselines3.common.utils.is_vectorized_multidiscrete_observation()` accessed `observation.shape`; a tuple has no such attribute. The deterministic policy path instead enters `BasePolicy.predict()` and `obs_to_tensor()`, which converts with NumPy before validation. Phase-A SB3 learning already ran through Gym/SB3 vector-environment buffering, and standardized tuning probes used deterministic inference. The failure was isolated to the newly introduced direct stochastic Frozen multi-episode reset path.

The correction keeps the project scientific state exactly `(x, y)` under `MultiDiscrete([width, height])`. `as_sb3_gridworld_observation()` converts only the direct multi-episode SB3 continuation container to an ndarray with the declared dtype and exact shape, verifies exact integer-value preservation, and requires observation-space membership. It rejects malformed, fractional, overflowed or out-of-space coordinates. It consumes no RNG, adds no information, and changes no environment, learner, reward, transition, exploration or schedule state. Branch attachment, branch steps, later-episode resets and progressive Frozen calls use it. The framework-neutral GridWorld and historical Phase-A facade remain tuple-based; the unchanged SB3 VecEnv buffer already converted Phase-A facade output to arrays. This narrower boundary preserves the original T-526 source-compatibility audit exactly.

## Existing horizon-rule enforcement

DEC-055 already required both at least two completed branch episodes and at least two completed Adaptive method-native update opportunities in every 256-interaction sizing unit. The prior selector checked only episodes. DEC-056 corrects that conformance gap before new outcomes and records cumulative method-aware counts at both horizons:

- Q-Learning: completed observed-transition backups;
- SARSA: completed on-policy backups, excluding a final observed transition whose deferred backup still awaits the next behavior action;
- DQN: completed SB3 gradient updates under the selected `train_freq=1`, `gradient_steps=1` schedule;
- PPO: completed 128-interaction rollout/update opportunities, distinct from optimizer epochs;
- Dyna-Q+: completed direct transition opportunities, with planning-update counts retained separately.

Frozen branches report zero Adaptive opportunities. The 256 horizon is selected only if both original criteria pass everywhere; otherwise 512 is selected. Root-count selection remains the exact DEC-055 Student-t rule.

## Outcome-independent final-freeze rules

Before sizing-v0.2 outcomes, this authority also fixes the remaining mechanical inputs that DEC-057 must use if sizing validates:

- retain Q-Learning `q-c06`, SARSA `sarsa-c06`, DQN `dqn-c05`, PPO `ppo-c06` and Dyna-Q+ `dyna-c03` unless an existing scientific-validity failure applies; no A2C and no full Dyna-Q arm;
- final conditions are the two categorical persistent remaps, action failure `0.15`, and observation corruption `0.05` with `uniform-valid-non-obstacle-excluding-true-state` support;
- generate exactly two 7×7 held-out `gw-l1` inputs using the configuration's deterministic first-two-valid structural algorithm, without constructing or executing an agent;
- generate the mechanically selected number of final roots as `t527-final-rNN` with the distinct fixed 71,000–76,000 seed-stream formulas, without executing them;
- root is the independent unit; layouts are equal-weight repeated/block observations within root; primary uncertainty is a root-level two-sided Student-t 95% interval with root-only bootstrap sensitivity; formal p-values are excluded, so multiplicity correction is not applicable.

## Evidence and failure policy

The committed entrypoint requires native Windows CPython 3.12 CPU execution, a clean local/remote/PR head, both required green checks, immutable T-526 validation, tuning-v0.1 valid-complete integrity and exact selection, and sizing-v0.1 valid-failed integrity and exact failure. It creates only `results/pilots/protocol-v2-t527-sizing-v0.2/`.

Any failure is retained and stops the authority. There is no resume, second retry, seed replacement, tuning rerun, rule change or final-reserve access. Only 240/240 Phase-A units, 480/480 matched sets, 1,920 branches, 3,840 branch-horizon evaluations, complete update-opportunity accounting and full integrity validation can authorize DEC-057.
