# Protocol v2 methodology closure audit

**Status:** accepted T-524 closure research record; bibliography promotion still pending  
**Date:** 2026-08-28  
**Builds on:** `PROTOCOL_V2_AUDIT_FACT_CHECK.md`, `PROTOCOL_V2_DEEP_CHAIN_2.md`, DEC-048  
**Boundary:** no final reserve, final tuning, final matrix, UI implementation, or thesis writing is authorized by this document.

## Executive closure verdict

Broad methodology exploration is now considered saturated for the current thesis scope. The remaining work is implementation and non-final empirical validation of a finite contract, not open-ended search for more algorithms or benchmarks.

The closure audit resolves eight targeted items: formal estimands; horizon/reward semantics; statistical inference stress-testing; uncertainty severity; deployment-policy semantics; scientific-checkpoint conformance; experimenter/final-reserve leakage; and threats to validity.

The primary Phase-B causal structure is:

`own Phase-A scientific checkpoint -> optional shared no-learning nominal prefix -> exact branch point -> Frozen nominal / Frozen disturbed / Adaptive nominal / Adaptive disturbed`.

Adaptive learning begins only at the declared branch/change boundary. Frozen and Adaptive inherit the same pre-boundary learner and behavior state. The primary disturbance-specific adaptation estimands are matched difference-in-differences effects on degradation/deficit/gap, not raw Adaptive-minus-Frozen alone.

## 1. Formal estimand audit

### 1.1 Indexing and independent unit

Let:

- `m` = retained method;
- `r` = independent root/run identity;
- `l` = final layout/block;
- `t` = predeclared environment-interaction checkpoint;
- `b` = Phase-B branch in `{FN, FD, AN, AD}` for Frozen nominal, Frozen disturbed, Adaptive nominal, Adaptive disturbed.

`r` is the independent randomization unit. Layouts, checkpoints, methods, branches, uncertainty conditions and episodes are repeated/block/factor structure within a root, not additional independent replicates.

### 1.2 Phase-A nominal-learning estimands

At each interaction checkpoint `t`, the learner is copied at a valid method-native update boundary and evaluated in an isolated no-learning evaluator using the same semantic observation/action/reward contract. Evaluator interactions never enter replay, rollout buffers, planning models or training counters.

Primary Phase-A quantities:

1. **Fixed-budget nominal policy quality** at the final predeclared interaction budget `T`: root/layout no-learning evaluation mean return (and success/episode-length diagnostics).
2. **Learning trajectory** over the common interaction-indexed probe grid.
3. **Learning efficiency/AUC** only as a secondary summary over that frozen probe grid and always reported with the curve.
4. **Failure probability and CPU/wall/resource cost** as separate outcomes, never folded into a single score.

No best checkpoint is selected from final evidence. The primary endpoint is the frozen fixed-budget endpoint/probe rule.

### 1.3 Phase-B component estimands

For a higher-is-better online or probe performance series, define within each regime the disturbed-vs-nominal loss. For the three primary resilience roles, use positive-is-worse component measures:

- `G_R^F` / `G_R^A`: Frozen/Adaptive immediate degradation relative to the same-regime nominal branch;
- `C_R^F` / `C_R^A`: Frozen/Adaptive cumulative deficit over the exact post-boundary interaction horizon;
- `T_R^F` / `T_R^A`: Frozen/Adaptive terminal gap over the frozen terminal interaction window.

The primary **adaptation benefit** for each component is:

- `AB_G = G_R^F - G_R^A`;
- `AB_C = C_R^F - C_R^A`;
- `AB_T = T_R^F - T_R^A`.

Positive values indicate that allowing ordinary post-boundary learning reduced the disturbance-specific loss. Algebraically this is the matched difference-in-differences interaction between regime and disturbance.

Raw `Adaptive disturbed - Frozen disturbed` remains an important absolute online deployed-performance contrast, but it is not the sole causal adaptation estimand.

### 1.4 Frozen cross-method resistance

Cross-method resistance is compared using Frozen disturbed-vs-nominal losses on the same root/layout blocks. Smaller degradation/deficit/gap means stronger resistance. Cross-method adaptation comparisons use the `AB_*` estimands only for a small predeclared mechanism-motivated contrast family.

## 2. Horizon, truncation, reward and task-objective semantics

### 2.1 `max_steps`

Protocol v2 treats GridWorld `max_steps` as an **administrative episode cutoff**, not a hidden finite-horizon objective. The agent-visible state remains the controlled position-state semantics; remaining time is not added merely because the runner needs a safety/reset horizon.

Consequences:

- goal arrival is `terminated=True`;
- the administrative cutoff is `truncated=True`;
- value learners bootstrap through truncation;
- a campaign interaction budget ending mid-episode is a measurement stop and must not be injected into the MDP as a terminal transition.

A future true finite-horizon task would be a different protocol and would require time-awareness in the observation.

Historical v1.0/v1.1 evidence used `bootstrap_on_truncation=False` without time in the observation. That evidence remains immutable and reportable for its original estimands, but this is now an explicit historical methodological limitation and is not inherited by v2.

### 2.2 Reward contract

The project-owned reward semantics remain task-level and common across methods. No method receives hidden reward shaping, method-specific reward scale, success bonus or wrapper that changes the scientific reward stream.

The current negative step/collision cost structure is compatible with shortest-path navigation and preserves an interpretable cost objective. Exact v2 reward values remain subject to the environment-discrimination pilot only if the ladder changes structural scale; they are selected for task semantics/floor-ceiling adequacy, never to improve a preferred method ranking.

### 2.3 Discount factor

`gamma` changes the return objective and therefore is a **common protocol/task parameter**, not an independently tuned optimizer hyperparameter. Q-Learning, SARSA, DQN, PPO and Dyna-Q+ use the same frozen discount factor unless a later explicit RQ justifies comparing different objectives. Method-specific tuning remains available for genuinely algorithmic optimization/configuration parameters.

### 2.4 Layout comparability

Raw return depends on unavoidable path length and layout geometry. Therefore the protocol must not average incomparable raw returns across heterogeneous complexity levels and call the result method quality.

- Environment-ladder selection is performed level-by-level with predeclared floor/ceiling/discrimination rules.
- Final layouts belong to one frozen task family/complexity level with comparable reward/horizon semantics.
- Primary method contrasts are paired/blocked within layout before root-level aggregation.
- Oracle/reference-relative path-cost or success/efficiency diagnostics may be reported to aid cross-layout interpretation; they do not replace the raw outcomes or create a composite score.

## 3. Statistical-plan stress test

A synthetic coverage check was run for the intended root-level paired/DiD estimator. Each synthetic root contained two correlated layout observations with a root latent effect. Three root-effect/noise families were tested: approximately normal, lognormal-skewed and Student-t heavy-tailed. Candidate root counts were 16, 24, 32 and 48.

Observed empirical 95% coverage across 400 Monte Carlo repetitions per cell:

| root n | Normal t-CI | Normal percentile bootstrap | Skew t-CI | Skew percentile bootstrap | Heavy-tail t-CI | Heavy-tail percentile bootstrap |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 0.952 | 0.920 | 0.968 | 0.930 | 0.952 | 0.915 |
| 24 | 0.950 | 0.932 | 0.952 | 0.915 | 0.968 | 0.930 |
| 32 | 0.950 | 0.935 | 0.948 | 0.930 | 0.942 | 0.925 |
| 48 | 0.945 | 0.935 | 0.955 | 0.928 | 0.940 | 0.925 |

This is a design stress test, not final power analysis. It rejects a mechanical assumption that a simple percentile bootstrap is automatically safer for the small root counts anticipated here.

**Accepted inference direction for T-527:**

1. compute the predeclared paired/DiD effect within each root after equal/block-aware layout handling;
2. use the mean root effect as the primary estimand;
3. use a Student-t 95% CI for the root-level mean as the default primary candidate when the final pilot-sized `n` and diagnostics support it;
4. report root-resampling/bootstrap and robust descriptive sensitivity rather than replacing the primary interval ad hoc;
5. perform final precision/coverage/runtime sizing using non-final pilot variance and the actual retained matrix before protocol freeze.

Episodes/checkpoints are never bootstrapped as independent observations.

### Failure-aware inference

Scientific/algorithmic failures are not silently dropped or replaced by favorable seeds. Report:

- planned-root denominator;
- scientific failure count/rate by method/condition;
- performance estimands conditional on protocol-valid completed roots with the denominator explicit;
- sensitivity/interpretation when failures are differential enough to undermine an unconditional superiority claim.

No arbitrary numeric penalty is invented merely to force failed runs into a scalar aggregate. Infrastructure failures may rerun only the same registered root identity and retain the failed attempt in provenance.

## 4. Uncertainty severity calibration

Severity is frozen from semantics and non-final pilot adequacy, never from desired method ordering.

### Action remapping

Action permutations are categorical structural changes. `remapped_actions` alone is not a valid scalar severity ordering: two permutations with the same count can differ materially by layout. Persist the exact mapping identity and describe conditions by mapping class rather than claiming universal low/high severity from count alone.

### Action-execution failure

No-op action failure has an interpretable scalar frequency `p`. Candidate frequencies are checked on development/pilot roots for nontrivial but non-degenerate behavior. The accepted values are then frozen before final reserve access.

### Observation corruption

Frequency alone is insufficient. The current implementation can replace the true position with any other valid non-obstacle coordinate, so a single corruption event can be globally large.

Protocol-v2 observation corruption therefore has two explicit dimensions:

- **frequency/probability**;
- **support/magnitude rule**.

Primary perceptual diagnostics should prefer a bounded, semantically interpretable local mislocalization support (for example a frozen Manhattan-radius neighborhood) if the pilot shows it is informative. The historical/global-random valid-cell corruption may be retained as a clearly labelled harsh supporting diagnostic. The exact radius/probability pair remains T-526/T-527 pilot-gated.

## 5. Deployment-policy semantics

### Shared branch point

Frozen and Adaptive branches clone the same learner state, behavior-policy state, counters/schedules and relevant RNG state at the boundary. Adaptive updates begin only from the first post-boundary transition. No epsilon/LR/replay/optimizer reset occurs because a change occurred.

### Value-based methods

Q-Learning, SARSA, DQN and Dyna-Q+ use the same predeclared deployment behavior-policy class in Frozen and Adaptive branches. If epsilon or another behavior clock is part of deployment, both branches start from the same value and the non-learning clock advances under the same interaction rule. Frozen blocks learned-state/model/optimizer/planning updates; Adaptive permits native updates.

### PPO

Online PPO deployment uses the same policy-sampling semantics in Frozen and Adaptive branches at the branch point. Adaptive PPO collects native on-policy experience and updates only at legal rollout/update boundaries; Frozen never updates its policy/value/optimizer state.

### Standardized no-learning probes

Primary policy-quality probes remove training exploration and learning updates:

- value-based methods use their frozen greedy/exploitation action rule with a predeclared deterministic tie rule;
- PPO uses a predeclared deterministic modal action rule as the cross-method exploitation probe;
- native stochastic-policy performance/entropy may be reported as a secondary PPO diagnostic.

The online branch remains authoritative for the real cost of exploration/adaptation; the deterministic probe is authoritative only for the defined exploitation-policy-quality estimand.

## 6. Scientific-checkpoint conformance audit

The scientific branch checkpoint and an operational mid-run resume checkpoint are distinct concepts.

### Required round-trip conformance test

For every retained method:

1. train to a legal method-native boundary;
2. serialize the full scientific continuation state plus schema/version/checksum;
3. continue clone A in memory;
4. destroy the original object/process, instantiate clone B and restore from bytes/artifacts;
5. feed A and B identical scoped learner/environment RNG streams and transitions for a bounded validation continuation;
6. compare actions, update counters, schedules, learned parameters/tables, replay/model state and final scientific-state checksums at legal boundaries;
7. fail the adapter gate if a material continuation field is missing.

### Method-specific closure

- **Q-Learning:** current Q-only checkpoint is insufficient for v2 exact continuation; full exploration/schedule/RNG/counter state must be added.
- **SARSA:** reuse the existing fuller state/restore design, adapted to the v2 common contract.
- **Dyna-Q+:** use the existing full `get_state()/restore_state()` capability as the basis; v2 must not use the Q-table-only `checkpoint()` as its scientific Phase-A checkpoint.
- **DQN:** online/target networks, optimizer, full replay state, replay sampling RNG, learning/exploration schedules, target/update counters, preprocessing state and software identity are required.
- **PPO:** policy/value/shared parameters, optimizer, progress/LR schedules, normalization state, counters/RNG and completed rollout/update-boundary identity are required.

Library `save()` convenience files are never assumed to satisfy this contract without an explicit conformance test.

## 7. Experimenter leakage and reserve audit

The following decision/evidence firewall is mandatory:

| Stage | May influence | Must not access/use |
|---|---|---|
| Development | adapter correctness, candidate ranges, ladder construction, severity semantics | final reserve outcomes |
| T-526 feasibility/discrimination | method feasibility, simplest informative environment level, candidate severity adequacy, runtime | final layouts/roots/results; preferred final ranking |
| T-527 tuning/sizing | method-specific tuning selection, common gamma/reward/horizon freeze, root-count precision/runtime sizing, final contrast/CI rules | final outcome curves or best final checkpoints |
| Protocol-v2 freeze | immutable retained method/environment/condition/root/probe/statistical contract | any final result |
| Final execution | execute frozen Phase A/B exactly once per planned root identity subject to declared infrastructure retry rule | post-hoc redesign/tuning based on final outcome |

Additional safeguards:

- final scenario/layout reserve is not inspected for manual tuning or severity design before freeze;
- final Phase-A training may use each final layout after reserve opening because the target RQ is learning/resilience on that task, not zero-shot generalization;
- root identities are never treated as tunable seeds;
- exact fixed-budget endpoint replaces best-final-checkpoint selection;
- failures/null/non-recovery outcomes remain visible.

## 8. Threats-to-validity closure matrix

### Construct validity

- "Resilience" is operationalized only through resistance/degradation, cumulative deficit, terminal gap and secondary recovery under declared GridWorld uncertainties; it is not a universal measure of AI resilience.
- "Adaptive/Continual" in the primary v2 contrast means ordinary method-native learning enabled after an externally defined boundary, not autonomous change detection and not a specialized continual-learning algorithm.
- observation corruption, actuation failure and persistent action remapping are distinct constructs and support distinct claims.

### Internal validity

Principal controlled threats: branch-state mismatch, behavior-policy mismatch, hidden evaluator information, time-limit handling, method-specific reward/objective changes, replay/reset interventions, RNG cross-talk and unequal interaction opportunity. The closure contract addresses each explicitly.

### Statistical-conclusion validity

Threats: finite root count, correlated repeated observations, skew/heavy tails, multiplicity, informative algorithmic failures and post-hoc selection. Controls: root-level estimands, paired blocking/DiD, precision-based sizing, limited primary contrast family, frozen multiplicity rule if p-values are used, failure-rate reporting and final-reserve firewall.

### External validity

The final evidence is intentionally bounded to a project-owned low-dimensional discrete GridWorld family on the validated thesis Windows/CPU environment. It does not establish performance for pixels, continuous control, large-scale benchmarks, real robots, arbitrary POMDPs or production systems. Those are limitations/future work, not hidden claims.

### Reproducibility validity

Deep-framework bitwise reproducibility is claimed only within the validated software/platform/device contract. Record Python, NumPy, PyTorch, Stable-Baselines3, OS, CPU/device, determinism flags, thread settings, code commit and complete resolved configuration. Repeated roots remain necessary even when deterministic mode is enabled.

## Closure decision

No third open-ended methodology search is required before implementation. New evidence should be added only when a concrete implementation/pilot observation exposes a specific unresolved methodological question.

The remaining T-524 bibliography gap is finite: promote/analyze/select the four newly identified methodology sources through `ThesisBibliography`, complete generated package/corpus convergence, synchronize one new immutable bibliography snapshot into this repository, and reconcile active requirements/status. After that, T-525 may begin the bounded framework-neutral v2 adapter/checkpoint foundation.
