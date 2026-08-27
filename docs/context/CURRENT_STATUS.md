# Current Project Status

**Date:** 2026-08-28  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger. Use progressive task-specific reading of DEC-048/049/050 and `docs/research/` for detail.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine validation and `T-200` research framing through completed protocol-v1.0 WP6 evidence. Frozen `protocol-v1.0`, `FINAL-*` and R0 pilot evidence remain immutable.
- **Project: 4/8** master milestones complete (#87: 1, 2, 4, 5). **Current task: `T-524` IN_PROGRESS.** Protocol-v2 tracker #95 remains 2/10 until bibliography convergence/sync closes T-524. Old `T-522` is superseded and must not execute.
- #93 final UI redesign remains PAUSED. Per DEC-049, the final frontend is rebuilt from scratch with a **different framework from NiceGUI** only after the framework-neutral v2 backend is stable. #94 / `T-803` packaging remains post-thesis and follows that later framework.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` work.

## Methodology closure

Open-ended methodology exploration is considered saturated after the 30-point audit fact-check, 20-check deep-chain pass, targeted closure audit and accepted DEC-050. New research reopens only for a concrete implementation/pilot validity problem.

### Phase A

- Independently train each retained method under the same task/reward/action semantics, same semantic agent-visible information and a common task-level `gamma`.
- Common learning resource = **actual environment interactions**, not episodes, optimizer updates, wall time or a library `total_timesteps` request.
- Use isolated no-learning policy-quality probes on a common interaction-indexed grid compatible with method-native update boundaries. Probe interactions never enter training state/replay/model.
- Feasibility pool: Q-Learning, SARSA, DQN, PPO, A2C, Dyna-Q+. Current core candidates: Q-Learning, SARSA, DQN, PPO, Dyna-Q+. Dyna-Q is ablation-only; A2C remains promotion/diagnostic only.

### Phase B

Each `method × root × layout` starts from its own exact Phase-A scientific checkpoint. If a pre-change prefix is needed, it is shared and no-learning. At the exact boundary clone identical learner/behavior/RNG state into Frozen nominal, Frozen disturbed, Adaptive nominal and Adaptive disturbed branches. Adaptive updates begin only from the first post-boundary transition; no epsilon/replay/optimizer/warm-up/recency/LR reset occurs at change onset.

Primary post-boundary opportunity is an exact common interaction budget. Primary component losses are immediate degradation, cumulative deficit and terminal gap relative to the same-regime nominal reference. Primary adaptation benefit is **Frozen loss − Adaptive loss**, i.e. the matched four-branch difference-in-differences interaction. Raw Adaptive-disturbed vs Frozen-disturbed performance remains a separate deployed-utility contrast. Recovery stays secondary/sensitivity; no composite resilience score.

## Objective, time-limit and checkpoint invariants

- GridWorld `max_steps` is administrative **truncation** in v2; goal arrival is termination. Value learners bootstrap through truncation. Remaining time is not added to the controlled position observation. Historical v1.x `bootstrap_on_truncation=False` without time in state is an explicit immutable limitation.
- Reward semantics and `gamma` are common task-level parameters; no method-specific reward objective/shaping.
- Scientific checkpoint = exact continuation state, not inference serialization. Q/SARSA preserve schedules/RNG/counters; Dyna-Q+ preserves its own learned model/recency/planning state; DQN preserves networks/optimizer/full replay/update/exploration state; PPO preserves policy/value/optimizer/schedules/RNG at legal rollout/update boundaries.
- Every retained adapter must pass `train -> serialize -> destroy -> restore -> continue` plus exact branch-clone equality.

## Statistics, environment and uncertainty

Root/run is the independent randomization unit; layouts/checkpoints/episodes are blocks/repeated observations. A synthetic closure stress test found root-level Student-t 95% intervals near nominal coverage across normal/skew/heavy-tail scenarios at indicative n=16–48, while simple percentile bootstrap under-covered; therefore t-CI is the current primary candidate, with root-bootstrap/robust sensitivity and final precision/runtime sizing deferred to `T-527`. No root count is frozen yet.

Scientific failures remain outcomes and are never replaced by another seed. Infrastructure retries use the same root identity and retain provenance.

`T-526` selects the simplest predeclared GridWorld complexity level avoiding universal floor/ceiling behavior without using preferred method ranking. Final layouts are hidden from experimenter tuning but Phase-A may train on them after reserve opening because zero-shot layout generalization is not the RQ.

Uncertainty claims remain separate: action remaps are categorical exact mappings; action-failure has explicit frequency; observation corruption requires both frequency **and support/magnitude**. The historical global-random valid-cell corruption is a harsh diagnostic, not generic local sensor noise.

## Bibliography/provenance

`MariosGiannakaras/ThesisBibliography` is canonical. The currently accepted immutable consumer snapshot remains `bibliography-integration-v3` until a new validated sync is merged. Earlier protocol-v2 sources (Patterson, Henderson, Dohare, DQN re-evaluation, existing Steinparz) are upstream; package/corpus convergence is still active.

Closure intake PR #143 was merged and triggered canonical processing for four additional methodology sources: Pardo (time limits), Engstrom (implementation sensitivity), Fedus (experience replay) and Nikishin (primacy bias). They are methodology sources, not new algorithm arms. T-524 remains open until canonical `SRC-*` IDs, analysis/evidence/selection, package/corpus convergence, all upstream validators and a new immutable consumer sync are complete.

## Still intentionally unfrozen

Exact retained methods/A2C decision, final GridWorld level/layouts, numeric interaction budgets, common gamma/reward values, method-specific optimization settings, probe/update cadence, uncertainty probabilities/support, final root count, multiplicity rule, final frontend framework and final evidence remain pilot/freeze-gated. Claims remain bounded to the controlled low-dimensional GridWorld and validated Windows/CPU contract; no universal resilience, autonomous change-detection, specialized continual-RL, real-robot or cross-platform bitwise claim is authorized.

## Exact next action

Finish the finite T-524 bibliography/convergence/sync work. Then T-525 implements the bounded v2 adapters/checkpoints/branching; T-526 runs the physical Windows feasibility/severity pilot; T-527 freezes tuning/statistics/protocol; T-528 performs the new-framework UI rebuild.
