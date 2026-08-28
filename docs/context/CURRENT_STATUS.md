# Current Project Status

**Date:** 2026-08-28  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use progressive task-specific reading of DEC-048/049/050 and `docs/research/` for detail.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine validation and `T-200` research framing through completed protocol-v1.0 WP6 evidence. Frozen `protocol-v1.0`, `FINAL-*` and R0 pilot evidence remain immutable.
- **Project: 4/8** master milestones complete (#87: 1, 2, 4, 5). **`T-524` and `T-525` are COMPLETE; current task: `T-526` READY for physical Windows evidence.** Protocol-v2 tracker #95 advances to 4/10. Old `T-522` is superseded and must not execute.
- T-525 closure is recorded in `docs/research/PROTOCOL_V2_BACKEND_CONTRACT.md`. The framework-neutral v2 implementation now has concrete Q-Learning, SARSA, DQN, PPO and Dyna-Q+ pilot adapters, exact learner/GridWorld checkpointing, isolated no-learning probes, actual-interaction accounting and matched four-branch execution.
- #93 final UI redesign remains PAUSED. Per DEC-049, the final frontend is rebuilt from scratch with a **different framework from NiceGUI** only after T-527 freezes the remaining v2 scientific/runtime choices. #94 / `T-803` packaging remains post-thesis and follows that later framework.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` work.

## Protocol-v2 methodology closure

Open-ended methodology exploration is saturated after the 30-point audit fact-check, 20-check deep-chain pass, targeted closure audit and accepted DEC-050. New literature work reopens only for a concrete implementation/pilot validity problem.

### Phase A

- Independently train each retained method under the same task/reward/action semantics, same semantic agent-visible information and a common task-level `gamma`.
- Common learning resource = **actual environment interactions**, not episodes, optimizer updates, wall time or a library `total_timesteps` request.
- Use isolated no-learning policy-quality probes on a common interaction-indexed grid compatible with method-native update boundaries. Probe interactions never enter training state/replay/model.
- Feasibility pool: Q-Learning, SARSA, DQN, PPO, A2C, Dyna-Q+. Current core candidates: Q-Learning, SARSA, DQN, PPO, Dyna-Q+. Dyna-Q is ablation-only; A2C remains promotion/diagnostic only.

### Phase B

Each `method × root × layout` starts from its own exact Phase-A scientific checkpoint. If a pre-change prefix is needed, it is shared and no-learning. At the exact boundary clone identical learner/behavior/RNG state into Frozen nominal, Frozen disturbed, Adaptive nominal and Adaptive disturbed branches. Adaptive updates begin only from the first post-boundary transition; no epsilon/replay/optimizer/warm-up/recency/LR reset occurs at change onset.

Primary post-boundary opportunity is an exact common interaction budget. Primary component losses are immediate degradation, cumulative deficit and terminal gap relative to the same-regime nominal reference. Primary adaptation benefit is **Frozen loss − Adaptive loss**, i.e. the matched four-branch difference-in-differences interaction. Raw Adaptive-disturbed vs Frozen-disturbed performance remains a separate deployed-utility contrast. Recovery stays secondary/sensitivity; no composite resilience score.

T-525 validates one exact post-boundary segment and fails closed if an additional environment reset would be required. The final multi-episode post-boundary reset/regime semantics are deliberately owned by T-526/T-527 rather than hidden in backend code.

## Objective, time-limit, RNG and checkpoint invariants

- GridWorld `max_steps` is administrative **truncation** in v2; goal arrival is termination. Value learners bootstrap through truncation. Remaining time is not added to the controlled position observation. Historical v1.x `bootstrap_on_truncation=False` without time in state is an explicit immutable limitation.
- Reward semantics and `gamma` are common task-level parameters; no method-specific reward objective/shaping.
- Scientific checkpoint = exact continuation state, not inference serialization. Q/SARSA preserve schedules/RNG/counters; Dyna-Q+ preserves its own learned model/recency/planning state; DQN preserves networks/optimizer/full replay/update/exploration state; PPO preserves policy/value/optimizer/schedules/RNG at legal rollout/update boundaries.
- Every retained adapter passes exact save/restore/continuation and branch-clone equality conformance. DQN replay and PPO rollout/update boundaries are explicit.
- Neural model initialization and post-initialization stochastic behavior/update RNG are separately rooted; environment/action-disturbance/observation-disturbance RNG streams remain independent. SB3 algorithm seeds are not reused as project environment seeds.
- Evaluator truth is never a fallback for agent-visible state. Phase-B continuation requires the delivered pre-change observation.

## T-525 implementation closure and validation

The new protocol-v2 lifecycle lives beside, not inside, the legacy v1.x `HeadlessExperimentRequest` path, preserving historical execution/evidence semantics.

Implemented modules cover:

- method/run/root/probe/failure schemas and concrete implementation registry;
- actual interaction-ledger enforcement and common task-level objective/truncation semantics;
- persistent project-native Phase-A learners plus deterministic no-learning probes;
- CPU-only Stable-Baselines3 2.9.0 DQN/PPO exact-state adapters;
- exact GridWorld trajectory/RNG snapshot, restore and branch-compatible fork;
- generic Phase-A and Phase-B executor;
- Frozen/Adaptive project-native and SB3 branch drivers;
- Frozen-state mutation guards, SARSA quiescent-fork requirement and Dyna-Q+ hidden-model-learning avoidance;
- explicit post-initialization SB3 behavior/update RNG reseeding from the independent root exploration stream.

Closure evidence on the reviewed PR #92 implementation head: the dedicated CPU-only protocol-v2 gate passed **55 conformance tests**, and the repository-wide gate passed tests, documentation consistency, committed JSON validation and installed-bibliography validation.

## T-526 physical feasibility gate

The first physical pass is fully predeclared in `configs/protocols/protocol-v2-feasibility-v0.1.json` and documented in `docs/research/T526_WINDOWS_FEASIBILITY_RUNBOOK.md`. The only user-machine entrypoint is:

`scripts/run_protocol_v2_feasibility_windows.ps1`

It requires a clean native-Windows branch state and performs dependency/CPU/conformance preflight before producing retained non-final evidence under `results/pilots/protocol-v2-feasibility-v0.1/`.

The ordered ladder is 7×7 → 10×10 → 14×14, with two layouts per level and three roots. Core methods receive the same provisional 2048-interaction Phase-A budget and probes at 0/512/1024/2048. The runner stops at the first complete level that is neither a universal early ceiling nor a universal final floor. It records actual training/probe interactions, wall/process CPU time, checkpoint size and failures. The rule never selects by preferred method ranking.

After a usable level is identified and the retained physical artifacts are reviewed, T-526 continues with the already-predeclared Phase-B candidates: two categorical action-remap mappings, bounded action-failure probabilities and bounded observation-corruption probabilities with explicit global valid-cell support. A2C promotion remains conditional on distinct thesis value versus PPO and acceptable matrix cost.

Hosted CI does **not** substitute for this physical-machine evidence gate.

## Statistics, environment and uncertainty

Root/run is the independent randomization unit; layouts/checkpoints/episodes are blocks/repeated observations. A synthetic closure stress test found root-level Student-t 95% intervals near nominal coverage across normal/skew/heavy-tail scenarios at indicative n=16–48, while simple percentile bootstrap under-covered; therefore t-CI is the current primary candidate, with root-bootstrap/robust sensitivity and final precision/runtime sizing deferred to `T-527`. No final root count is frozen yet.

Scientific failures remain outcomes and are never replaced by another seed. Infrastructure retries use the same root identity and retain provenance.

Uncertainty claims remain separate: action remaps are categorical exact mappings; action-failure has explicit frequency; observation corruption requires both frequency **and support/magnitude**. The current global-random valid-cell corruption is explicitly a harsh perceptual diagnostic, not generic local sensor noise.

## Bibliography/provenance

`MariosGiannakaras/ThesisBibliography` remains canonical. Protocol-v2 methodology issue #135 is complete. The converged upstream corpus is pinned by immutable full SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5` and contains **597 canonical sources, 121 citation-ready sources and 19 research materials**, including `research-notes/protocol-v2-writing-crosswalk-2026-08-28.md` for later claim-to-source drafting discipline.

The generated consumer sync was validated upstream and in this repository, merged through PR #96, and synchronized into the single pre-WP7 integration branch. `bibliography-integration-v3` remains immutable historical provenance; it was not moved.

## Still intentionally unfrozen

Final retained methods/A2C decision, selected GridWorld level/layouts, final numeric interaction budgets, common gamma/reward/horizon values, method-specific optimization settings, probe/update cadence, Phase-B multi-episode reset/regime semantics, uncertainty probabilities/support, final root count, multiplicity rule, final frontend framework and final evidence remain pilot/freeze-gated. Claims remain bounded to the controlled low-dimensional GridWorld and validated Windows/CPU contract; no universal resilience, autonomous change-detection, specialized continual-RL, real-robot or cross-platform bitwise claim is authorized.

## Exact next action

Execute the committed T-526 Phase-A physical gate **once** on the validated native Windows thesis machine from a clean reviewed `feat/pre-wp7-protocol-v1.1-ui-rebuild` state:

`powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1`

Retain the generated output directory unchanged for review. Do not rerun/overwrite it, access a final reserve, begin tuning, or resume the UI. After T-526 evidence is complete, T-527 freezes the remaining protocol/runtime/statistical choices; only then does T-528 start the different-framework UI rebuild.
