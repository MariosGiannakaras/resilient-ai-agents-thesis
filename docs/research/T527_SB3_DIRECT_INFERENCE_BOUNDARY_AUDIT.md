# T-527 SB3 direct-inference boundary and sizing-v0.2 reuse audit

**Status:** pre-outcome DEC-057 audit complete; physical validation pending
**Baseline:** `fbb5a7abda5444aebb12569e5e83b07df89b49ee`
**Scope:** project GridWorld representation ingress and structural reuse only; no final-reserve outcomes

## Direct-inference inventory

The project scientific observation remains the framework-neutral integer coordinate `(x, y)` under `MultiDiscrete([width, height])`. SB3 training through Gym/VecEnv may use the array container supplied by that library boundary. Every direct project-GridWorld inference call now uses `predict_sb3_gridworld_action()`, which delegates only after `as_sb3_gridworld_observation()` proves exact dtype, shape, values and observation-space membership.

| File / function | Classification | Source representation | Conversion owner | Stochastic DQN path? | Coverage |
|---|---|---|---|---|---|
| `protocol_v2_sb3.py / SB3ScientificStateAdapter.predict` | adapter-internal delegation, not GridWorld ingress | caller-owned | caller must use canonical ingress | possible | adapter/state tests |
| `protocol_v2_sb3_gridworld.py / ExplicitSeededGridWorldEnv` | SB3 training through Gym/VecEnv | project tuple returned by facade | SB3 VecEnv buffer | yes, inside `learn()` | Phase-A DQN/PPO driver tests |
| `protocol_v2_sb3_driver.py / SB3NoLearningProbeEvaluator` | generic non-project evaluator | environment-native Box fixture | generic evaluator/environment | possible | generic SB3 driver tests; explicitly outside project-GridWorld ingress rule |
| `protocol_v2_feasibility.py / SB3ProjectGridWorldProbeEvaluator` | historical-only T-526 Phase-A probe; excluded from current T-527/Study execution | project tuple | retained historical implementation at its source commit | no stochastic exploration | T-526 recovery source-identity tests; deliberately unchanged |
| `study/protocol_v2_executors.py / _SB3ProjectProbeEvaluator` | direct deterministic Study project probe | project tuple | canonical wrapper | no exploration branch, but same strict boundary | Study executor suite plus ingress guard |
| `protocol_v2_prefix.py / prepare_shared_no_learning_prefix` | direct stochastic shared prefix | project tuple on reset and after every step | canonical wrapper on every iteration | yes | forced `exploration_rate=1.0` DQN public-prefix regression and PPO public-prefix regression |
| `protocol_v2_sb3_phase_b.py / SB3PhaseBBranchDriver._run_frozen_to` | direct stochastic/deterministic Frozen deployment | attachment/reset/step observation | continuation facade plus canonical wrapper | yes | forced raw-tuple reproduction; 256→512 progressive reset regression |
| `protocol_v2_sb3_phase_b.py / _run_adaptive_to` | Adaptive SB3 learning through Gym/VecEnv | strict continuation arrays | persistent continuation facade | yes, inside `learn()` | Adaptive DQN/PPO reset, clock, replay/update tests |
| `protocol_v2_t526_phase_b.py / T526PPOPhaseBBranchDriver._run_frozen` | reachable historical T-526 compatibility helper | project branch tuple | canonical wrapper | PPO only | T-526 compatibility suite plus ingress guard |
| T-526 recovery/settlement and Study Phase-B orchestrators | composed surface | inherited from prefix/driver | canonical prefix and branch drivers | yes for DQN | recovery/settlement/Study suites |

The newly identified active uncentralized surfaces beyond the known shared prefix were the Study deterministic project probe evaluator and the retained T-526 PPO Frozen compatibility helper. They did not cause the DEC-056 failure, but leaving active paths ad hoc would violate one auditable representation boundary. The historical T-526 Phase-A probe is classified historical-only and kept source-compatible with its immutable recovery authority. The generic Box-space `SB3NoLearningProbeEvaluator`, SB3 adapter delegation and the transient PPO adapter delegation are not project-GridWorld ingress surfaces.

## Representation contract

`predict_sb3_gridworld_action()`:

1. accepts the unchanged project coordinate and declared `MultiDiscrete` space;
2. rejects non-coordinate, fractional, wrong-shape, overflowed or out-of-space values;
3. creates an ndarray of exactly the declared observation dtype and shape;
4. proves integer-value preservation and observation-space membership;
5. delegates once to the exact scientific-state adapter;
6. performs no normalization, scaling, clipping, RNG draw, state reset or information addition.

Only stochastic prediction itself may advance the already-restored behavior/global/action-space RNG state. The wrapper does not create a new RNG. A source-level AST guard permits direct `.predict()` only inside the immutable historical T-526 Phase-A probe, generic non-GridWorld evaluator, SB3 adapter's internal model delegation and T-526 transient-adapter delegation.

## Q-Learning/SARSA compositional reuse decision

Reuse is accepted before new physical outcomes for structural reasons only.

Both retained sizing-v0.2 strata satisfy all required identities:

| Method | Phase A | Matched sets | Roots/layouts/remaps/horizons | Phase-A rows SHA | Phase-B rows SHA | Checkpoint-index SHA |
|---|---:|---:|---|---|---|---|
| Q-Learning | 48/48 | 96/96 | 24 × 2 × 2 × {256,512} | `8b710d864ccb1ff6698f24fb792d7a2ec3cb31f9e353725af9ab0af582b9a28d` | `8cceb2bb605886a1cbfc93becd962f04d7d7d0d2f2f6dbfbd1bdbbceae849ab2` | `fd9dcc87fae617445d914be778b0d3f50275dd7984a7e9500fa3d3eac9939e30` |
| SARSA | 48/48 | 96/96 | 24 × 2 × 2 × {256,512} | `5097ef276ae136f07c9bcc2e8d382d164793c34b7d8c53dbf72fe4069673be5d` | `15ca15c33d1b0b157940b1fbc51d065a8061bf3e8d943cce1d634375cdd085ba` | `c0188f17251047653347357d6ddac5f5a15f64406fd3d2e395f942c048dbd2dc` |

The validator additionally requires exact v0.2 integrity, configurations `q-c06`/`sarsa-c06`, 8,192 interactions, all six probes, the frozen roots/seeds/layouts/remaps/horizons, one prefix interaction, complete native-update fields, four branches per horizon, no method-local failure and exact checkpoint-file hashes.

Code-lineage validation requires the tabular learners/drivers, environment, randomness, scenario, settlement, sizing orchestration and DEC-056 scientific plan to have no diff from the retained baseline. It compares a normalized AST of `prepare_shared_no_learning_prefix()` in which only the SB3-specific `else` bodies are removed; the full shared and project-method semantics must remain identical. Focused prefix tests protect the tabular path.

No Q-Learning/SARSA return, success, episode or precision value was consulted to choose reuse. Runtime savings are not the decision basis. Incomplete DQN v0.2 rows and every sizing-v0.1 row are prohibited from the composition.

## DEC-057 scope

The only new physical strata are complete fresh DQN, PPO and Dyna-Q+ executions from `dqn / t527-size-r01 / gw-l1-a`: 144 Phase-A units, 288 matched sets, 1,152 branches and 2,304 branch-horizon evaluations. If and only if they validate, a reference-only combined package resolves the two exact retained strata plus the three exact fresh strata into the original 240/480/1,920/3,840 matrix and mechanically applies the unchanged DEC-055/056 selection rules.

No final layout, final root or final agent execution occurs during this audit or sizing completion.
