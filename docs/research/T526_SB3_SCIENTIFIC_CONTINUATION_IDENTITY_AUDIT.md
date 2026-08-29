# T-526 SB3 Scientific-Continuation Identity Audit

**Date:** 2026-08-29
**Scope:** historical protocol-v2 DQN/PPO fingerprints, SB3 2.9.0 persistence, and the retained DEC-052 DQN mismatch
**Conclusion:** diagnosis B is established; the retained DQN learner fingerprint is exact scientific continuation state, while the nonidentical raw checkpoint envelope contains runtime/serialization metadata that is not part of that state

## Evidence boundary

The audit did not rerun Phase A, create a scientific outcome, inspect final reserve, or write either historical directory. The original Phase-A five-file bundle and the failed DEC-052 recovery bundle are verified against their committed SHA-256 inventories. The original run retained the DQN checkpoint-envelope SHA and learner-state SHA, but not the original checkpoint payload. Therefore an internal member-by-member diff against that unavailable original archive cannot be manufactured. The analysis instead combines:

1. the exact historical/reconstructed learner-state SHA match;
2. the immutable original source/configuration/dependency path;
3. direct SB3 2.9.0 save/load/learn source inspection;
4. the retained reconstructed archive;
5. a controlled same-scientific-state archive diff; and
6. perturbation and restore proof tests.

## Raw archive mismatch

`_save_model_bytes()` calls SB3 `model.save()` and then `_canonicalize_zip()`. Canonicalization sorts members and normalizes ZIP timestamps, compression and permissions, but deliberately preserves every member byte. SB3's `data` member serializes the algorithm object's remaining attributes. It includes `start_time`, which `BaseAlgorithm._setup_learn()` assigns from `time.time_ns()` on every learning call and later uses only to report elapsed time/FPS. The original Phase-A run began at Unix time `1788013562.109377`; the DEC-052 recovery began at `1788016464.4321978`, and its retained DQN archive records `data.start_time = 1788016475939752700`. The original and recovery `data.start_time` values therefore cannot be equal. This alone guarantees nonidentical raw archives without implying a learner difference.

The reconstructed model ZIP has these canonical members:

| Member | Bytes | Role |
| --- | ---: | --- |
| `_stable_baselines3_version` | 5 | dependency provenance |
| `data` | 10,833 | algorithm configuration, counters, runtime/logging fields and cloudpickle metadata |
| `policy.pth` | 47,743 | DQN online and target network state |
| `policy.optimizer.pth` | 48,621 | optimizer state |
| `pytorch_variables.pth` | 1,261 | SB3 torch-variable container |
| `system_info.txt` | 185 | runtime provenance |

SB3 `data_to_json()` also adds human-readable first-level attributes beside `:serialized:` cloudpickle payloads. For class objects such as `policy_class` and `replay_buffer_class`, those display attributes contain function/object representations with process memory addresses. They are ignored by `json_to_data()`, which restores only `:serialized:`, but they make a raw archive process-sensitive. A controlled load/resave of the retained state exhibited such address-only display differences. They are serialization metadata, not executable parameter state.

The focused proof fixture changes only `model.start_time` by one nanosecond. Its exact field-level diff is:

| Archive member | Data path | Classification |
| --- | --- | --- |
| `data` | `start_time` | serialization/runtime metadata only |

The raw archive bytes differ, both states keep the same historical learner SHA and DEC-053 derived continuation SHA, and both restore to those exact identities. This proves that raw SB3 archive equality is stronger than, and not equivalent to, scientific continuation equality.

## Historical DQN fingerprint coverage

The historical `state_sha256()` hashes a canonical structural payload. Tensor dtype, shape and bytes are included; mappings are key ordered; numeric values use exact representations.

| Continuation component | Historical coverage | Independent audit |
| --- | --- | --- |
| Online Q network | `model.get_parameters()["policy"]` | direct perturbation changes the historical hash |
| Target Q network | same policy state dict; SB3 DQN policy owns `q_net_target` | direct target-only perturbation changes the historical hash |
| Optimizer state | `model.get_parameters()["policy.optimizer"]` | momentum/step perturbation changes the historical hash |
| Replay observations/actions/rewards/dones/next observations/timeouts | `_replay_fingerprint()` | content perturbation changes the historical hash |
| Replay capacity, logical position, full flag and environment count | `_replay_fingerprint()` plus counters | position/full perturbations change the historical hash |
| Training/update/progress/total counters | counter snapshot | direct perturbations change the historical hash |
| Exploration rate | counter snapshot | direct perturbation changes the historical hash |
| Exploration schedule definition | frozen configuration and SB3 2.9.0 `LinearSchedule` construction | DEC-053 derived identity records class/start/end/fraction and current value; perturbation fails the barrier |
| Learning-rate schedule definition/current value | frozen numeric configuration and SB3 2.9.0 `FloatSchedule(ConstantSchedule)` construction; optimizer current LR is already in optimizer state | DEC-053 derived identity records schedule definition/current value and optimizer group LR |
| DQN `_n_calls` target-update counter | not a direct historical field | independently exact: the adapter requires `n_envs=1`, the frozen run starts at zero, and SB3 increments `_n_calls` and `num_timesteps` once per environment step; retained `num_timesteps=2048` therefore proves `_n_calls=2048`; DEC-053 rejects any inequality |
| Python/NumPy/Torch CPU RNG | adapter-owned global RNG snapshot | RNG perturbation changes the historical hash |
| Action-space RNG | exact Gymnasium bit-generator state | perturbation changes the historical hash |
| Replay sampling mode | frozen constructor/source (`optimize_memory_usage=False`, standard ReplayBuffer, timeout handling enabled) | DEC-053 asserts these actual operational fields |
| Normalization/preprocessing | none used; `_vec_normalize_env is None`; fixed project observation space/network construction | DEC-053 asserts no VecNormalize state |
| Attached environment observation/episode flags | excluded intentionally | project continuation detaches learner state and `set_env(..., force_reset=True)` attaches the exact Phase-B branch point; environment state is separately cloned/fingerprinted |
| Episode/logging buffers, episode count, start time and timing baseline | excluded intentionally | affect logs/FPS only, not action selection, replay sampling, targets or optimizer updates |

No continuation-relevant DQN state remains unknown. The only continuation-relevant historical omission, `_n_calls`, is independently and uniquely determined from retained `num_timesteps` plus the frozen one-environment SB3 transition invariant.

## Historical PPO fingerprint coverage

| Continuation component | Historical coverage | Independent audit |
| --- | --- | --- |
| Policy/value networks | policy state dict | direct perturbation changes historical hash |
| Optimizer | policy optimizer state dict | optimizer perturbation changes historical hash |
| Timesteps, updates, progress and total target | counter snapshot | direct perturbation changes historical hash |
| Learning-rate and clipping schedules | frozen numeric configuration and SB3 2.9.0 `FloatSchedule` construction; current LR also resides in optimizer state | derived audit records definitions and evaluated current values; schedule perturbation fails derived identity |
| Python/NumPy/Torch/action-space RNG | exact adapter snapshots | perturbations change historical hash |
| Rollout lifecycle | legal boundary and buffer size | only initial or completed rollout/update boundaries are accepted |
| Completed rollout payload | intentionally excluded | `OnPolicyAlgorithm.collect_rollouts()` calls `rollout_buffer.reset()` before the next collection, so consumed buffer values cannot affect subsequent behavior or learning |
| Attached environment state | intentionally separate | exact Phase-B prefix/environment is cloned independently and attachment forces reset to that branch point |
| SDE/normalization | not used | derived audit requires `use_sde=False` and no VecNormalize state |

No continuation-relevant PPO state remains unknown at the legal completed-update boundary.

## Identity policy consequence

The historical learner SHA remains the primary physically recorded SB3 barrier. `scientific_continuation_sha256` is a DEC-053 derived audit identity computed only for reconstructed/round-tripped states; it is not represented as an original measurement. SB3 acceptance requires the historical SHA exactly, exact method/root/layout/configuration/source/accounting/probes, exact restore and post-restore historical SHA, all explicit continuation invariants, and an exact derived round trip. Both original and reconstructed raw checkpoint-envelope hashes are retained and never described as byte-identical.

Q-Learning, SARSA and Dyna-Q+ keep raw checkpoint-envelope equality because their canonical project serialization is deterministic and scientifically meaningful.
