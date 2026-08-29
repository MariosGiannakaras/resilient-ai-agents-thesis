# Protocol v2 Backend Contract

**Status:** T-525 implementation-complete contract; DEC-054 boundary settlement physically validated; final numeric protocol remains T-527 gated
**Research authority:** DEC-048 / DEC-050 / `PROTOCOL_V2_RESEARCH_DESIGN.md`  
**Implementation branch:** `feat/pre-wp7-protocol-v1.1-ui-rebuild`

## 1. Purpose and boundary

Protocol v2 is implemented beside the historical v1.x experiment path. The legacy `HeadlessExperimentRequest` and frozen v1.0/v1.1 evidence semantics are not extended with neural-method flags and are not rewritten.

The v2 backend owns a framework-neutral scientific lifecycle:

1. method-native Phase-A nominal learning;
2. actual environment-interaction accounting;
3. isolated interaction-indexed no-learning probes;
4. exact method-specific scientific checkpoints;
5. exact GridWorld branch-point state;
6. matched Frozen nominal / Frozen disturbed / Adaptive nominal / Adaptive disturbed execution;
7. fail-closed information and lifecycle boundaries.

T-525 does **not** freeze final methods, environment complexity, numeric budgets, hyperparameters, probe cadence, uncertainty severities, roots, final Phase-B multi-episode reset semantics, statistics, final evidence or UI behavior. Those remain T-526/T-527 decisions.

## 2. Core implementation map

| Concern | Implementation |
|---|---|
| v2 scientific primitives / method capabilities / interaction ledger / checkpoint envelope | `src/resilient_agents/protocol_v2.py` |
| run/root/method/probe/failure schemas and four-branch plan | `src/resilient_agents/protocol_v2_runtime.py` |
| framework-neutral Phase-A / Phase-B executor | `src/resilient_agents/protocol_v2_executor.py` |
| exact GridWorld trajectory/RNG state and branch-compatible restore | `src/resilient_agents/protocol_v2_gridworld.py` |
| resolved implementation registry | `src/resilient_agents/protocol_v2_implementations.py` |
| persistent project-native Phase-A drivers and no-learning probes | `src/resilient_agents/protocol_v2_tabular_driver.py` |
| project-native Phase-B Frozen/Adaptive semantics | `src/resilient_agents/protocol_v2_tabular_phase_b.py` |
| exact SB3 DQN/PPO scientific-state bundles | `src/resilient_agents/protocol_v2_sb3.py` |
| SB3 Phase-A driver / no-learning probes | `src/resilient_agents/protocol_v2_sb3_driver.py` |
| SB3-to-project-GridWorld Gymnasium facades | `src/resilient_agents/protocol_v2_sb3_gridworld.py` |
| SB3 Phase-B Frozen/Adaptive driver | `src/resilient_agents/protocol_v2_sb3_phase_b.py` |

## 3. Resolved pilot implementations

The T-525 minimum core candidate set has concrete implementations:

- **Q-Learning** — project-owned tabular learner + exact scientific-state compatibility adapter.
- **SARSA** — project-owned on-policy tabular learner with exact pending/deferred/RNG state.
- **Dyna-Q+** — project-owned learned-model planner with exact model/recency/planning/RNG state.
- **DQN** — Stable-Baselines3 2.9.0 CPU scientific-state adapter.
- **PPO** — Stable-Baselines3 2.9.0 CPU scientific-state adapter at legal completed rollout/update boundaries.

Dyna-Q remains an ablation rather than a required full arm. A2C remains promotion/diagnostic only and is not part of the T-525 minimum implementation requirement.

The optional `protocol-v2-pilot` environment is locked to CPU-only PyTorch 2.9.0 and Stable-Baselines3 2.9.0. Hosted CI verifies that CUDA is unavailable in that environment; physical Windows performance remains T-526 evidence.

## 4. Phase-A execution invariant

A method driver receives **absolute actual environment-interaction targets**. Library-requested timesteps, episode counts and optimizer-update counts cannot substitute for the project ledger.

At every predeclared probe index:

1. training stops exactly at the requested interaction count or fails;
2. the scientific learner state is cloned;
3. standardized evaluation runs only on that clone;
4. probe interactions are recorded separately;
5. the source training state is proven unchanged;
6. training resumes from the exact pre-probe state.

Project tabular learners remain persistent across episode resets so Q/SARSA/Dyna-Q+ RNG/model/recency state is not silently reset by episode lifecycle. SB3 methods retain their native update/replay/rollout semantics rather than being forced into a tabular `Agent.observe()` abstraction.

## 5. Scientific checkpoint invariant

A checkpoint means faithful continuation state, not inference-only serialization.

### Q-Learning

Preserves Q values, immutable baseline, behavior RNG, pending action, seeds and counters while leaving the historical v1.x Q-only checkpoint artifact unchanged.

### SARSA

Preserves Q values, behavior RNG, pending action, deferred on-policy backup state, seeds and counters.

### Dyna-Q+

Preserves Q values, empirical model, experienced pairs, recency/tau state, planning state/RNG, behavior RNG and counters.

### DQN

Preserves online/target/optimizer state through the model bundle plus full replay buffer, logical replay position/fullness, exploration/update/warm-up counters, configuration, algorithm/action-space/global RNG state and continuation schedule.

### PPO

Preserves policy/value/optimizer/configuration/counters/schedules/RNG state. A scientific checkpoint is legal only before training or after a completed rollout/update boundary; mid-rollout snapshots fail closed.

Conformance covers state round-trip, destruction/reconstruction or equivalent exact restore, continuation equality and four-way clone equality.

## 6. Exact GridWorld branch point

The project GridWorld scientific state contains:

- position and environment interaction index;
- finished state;
- explicit `EnvironmentSeeds`;
- action-disturbance RNG state;
- observation-disturbance RNG state;
- Gymnasium NumPy RNG state;
- last evaluator transition, including the **delivered observation** required to continue agent interaction.

Full scenario identity and branch-compatible task identity are distinct. The branch-compatible identity keeps grid/action/reward/observation/information semantics fixed while allowing only declared post-boundary uncertainty/change mechanisms to differ.

A Phase-B branch must have a delivered pre-change prefix observation. Evaluator truth (`debug_state`, true state, hidden mapping/change information) is never a fallback.

## 7. Frozen versus Adaptive semantics

All four branches begin from exact learner-state clones and exact shared GridWorld prefix state.

**Frozen:** scientific learning state cannot mutate after the branch point. Behavior RNG and inference-only bookkeeping may advance when required for behavior, but Q/model/recency/planning/optimizer/replay/update state cannot change.

**Adaptive:** ordinary method-native training resumes from the exact checkpoint. No exploration/replay/model/optimizer/target/LR/warm-up/recency reset occurs at the change boundary.

Special handling is explicit where method semantics require it:

- SARSA branches require a quiescent fork with no unresolved deferred backup.
- Frozen Dyna-Q+ does not call the historical learning `act()` path because that path can create model entries; its Frozen inference path avoids hidden model learning.
- Frozen DQN/PPO perform inference without mutating model/optimizer/replay/update counters.
- Adaptive DQN/PPO attach method-native SB3 training to the exact already-restored project GridWorld branch.

## 8. Phase-B lifecycle boundary intentionally left for T-526/T-527

T-525 validates one exact post-boundary environment segment. If termination/truncation occurs before the requested branch target and another episode reset would be required, the implementation fails closed.

This is intentional. The final protocol must explicitly decide how a persistent action remap and other uncertainty mechanisms behave across later episode resets. That decision depends on the selected GridWorld level, horizon, feasible interaction budget and final estimand schedule and therefore belongs to T-526/T-527 rather than being hidden in backend code.

### T-526 exact Phase-A budget settlement

DEC-054 narrowly resolves the separate pre-prefix case where a method-native learner has completed the fixed actual-interaction budget but retains algorithmic bookkeeping attributable to the final consumed transition. The immutable historical checkpoint remains the source identity. A deterministic derived deployment-start state may complete that bookkeeping with zero environment interactions before constructing the fresh Phase-B environment.

For the retained implementation matrix, Q-Learning, DQN, PPO and Dyna-Q+ are already quiescent. SARSA may carry one deferred nonterminal backup; settlement selects the required bootstrap-only action from the deferred Phase-A `next_state` under the exact restored behavior policy/RNG, applies the update once and discards the action. It never uses or executes a Phase-B observation/action. All 30 derived states must be quiescent and validated before the common no-learning prefix.

## 9. Information and randomness invariants

- Neural and tabular methods receive the same semantic agent-visible information; representation may differ deterministically.
- Evaluator-only truth never enters the learner transition or policy input.
- Algorithm/behavior RNG and environment/disturbance RNG remain separate scientific streams.
- SB3's algorithm seed is not silently reused as the project environment seed.
- Probes do not consume or overwrite source learner state.
- Scientific failure identities are retained; infrastructure retries preserve the same root identity.

## 10. Conformance gate

The dedicated `Protocol-v2 pilot checks` workflow installs the locked CPU pilot group, verifies CPU-only PyTorch, and executes all protocol-v2 conformance modules covering:

- task/runtime schemas and actual-interaction accounting;
- exact native/SB3 checkpoints;
- GridWorld exact restore/fork;
- resolved implementation registry;
- generic Phase-A/Phase-B executor;
- project-native Phase-A and Phase-B drivers;
- DQN/PPO Phase-A drivers and probes;
- real project-GridWorld DQN/PPO Phase-B continuation;
- Frozen-state invariants;
- evaluator-information fail-closed behavior.

At T-525 closure, both repository-wide checks and the complete dedicated protocol-v2 conformance gate are required to be green on the same PR head.

## 11. Next gate

T-526 is the first physical-machine evidence gate. It must run on the validated Windows thesis machine and cannot be replaced by hosted CI. It will determine the usable ordered GridWorld complexity level, method/runtime feasibility and non-degenerate uncertainty settings without accessing the final reserve.

Only after T-526 and T-527 freeze the remaining scientific/runtime choices may T-528 select a **different framework from NiceGUI** and rebuild the final application UI from scratch against this framework-neutral backend contract.
