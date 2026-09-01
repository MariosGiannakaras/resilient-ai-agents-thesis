# DEC-050 — Protocol v2 methodology closure refinements

**Status:** Accepted  
**Date:** 2026-08-28  
**Refines:** DEC-048 and `docs/research/PROTOCOL_V2_RESEARCH_DESIGN.md`  
**Research record:** `docs/research/PROTOCOL_V2_CLOSURE_AUDIT.md`

## Decision

The second deep-chain pass and targeted closure audit are accepted as binding refinements for protocol v2. Where this decision conflicts with earlier DEC-048 wording, this decision is newer and controls the successor protocol.

## Accepted refinements

1. **Phase-B causal branch point:** when a pre-change prefix is used, it is shared and no-learning. Frozen and Adaptive branches fork from the exact same state at the declared boundary. Adaptive updates begin only from the first post-boundary transition.
2. **Four branches:** every retained method/root/layout uses Frozen nominal, Frozen disturbed, Adaptive nominal and Adaptive disturbed post-boundary branches from the same branch-point state.
3. **Primary adaptation estimand:** disturbance-specific adaptation benefit is the matched difference-in-differences reduction in immediate degradation, cumulative deficit and terminal gap. Raw Adaptive-disturbed minus Frozen-disturbed remains descriptive deployed performance, not the sole causal adaptation effect.
4. **Interaction budgets:** Phase-A training and Phase-B adaptation opportunities are defined in actual environment interactions. Episode counts are descriptive. A campaign budget ending mid-episode is not converted into a terminal MDP transition.
5. **Time-limit semantics:** GridWorld `max_steps` is administrative truncation in v2. Remaining time is not added to the position observation. Value-based methods bootstrap through truncation. A true finite-horizon task would require an explicit different protocol with time-aware state.
6. **Historical boundary:** v1.0/v1.1 use of `bootstrap_on_truncation=False` without remaining time is retained as an immutable historical methodological limitation, not rewritten evidence.
7. **Common task objective:** reward semantics and discount factor `gamma` are protocol/task-level and common across retained methods. `gamma` is not independently tuned per method because doing so changes the objective being compared.
8. **Deep-library accounting:** project-owned actual interaction counters are scientific authority. Library `total_timesteps` arguments are not assumed to equal exact collected interactions. Probe/budget boundaries must respect method-native update quanta.
9. **DQN identity/state:** replay capacity, replay ratio/update cadence, warm-up, target cadence, exploration schedule and full replay/optimizer/network state are scientific configuration/continuation state, not invisible defaults.
10. **PPO identity/state:** maintained-library and PyTorch versions plus code-level configuration are scientific provenance; scientific checkpoints occur only at completed rollout/update boundaries and preserve optimizer/schedule/RNG state needed for continuation.
11. **Dyna-Q+ state:** protocol v2 trains Dyna-Q+ independently and clones its full learned model, Q values, recency state, planning/exploration RNG and counters. The v1.1 Q-table-only common-checkpoint deployment design remains historical and is not reused as v2 independent-training evidence.
12. **Frozen/Adaptive behavior:** both regimes inherit the same behavior-policy class and branch-point clock/state. Frozen disables learning/model/planning/optimizer updates; Adaptive enables native updates. No epsilon, replay, optimizer, warm-up or schedule reset occurs at change onset.
13. **Online versus probe outcomes:** online deployed utility includes real exploration/adaptation costs. Separate standardized no-learning probes measure exploitation-policy quality at common interaction checkpoints and never update or contaminate the learner.
14. **Uncertainty severity:** action mappings are categorical identities, not universally ordered by remapped-action count. Action-failure frequency is explicit. Observation corruption must freeze both frequency and spatial support/magnitude; global-random mislocalization is not described as generic local sensor noise.
15. **Statistical hierarchy:** root remains the independent unit. Primary root-level paired/DiD mean effects use a predeclared interval procedure; current synthetic stress testing supports Student-t intervals as the default candidate, with root-bootstrap/robust sensitivity and final precision sizing at T-527. Episodes/layout cells are not resampled as independent units.
16. **Failures:** scientific/algorithmic failures remain outcomes and are never replaced by another seed. Infrastructure failures may retry only the same registered root and retain attempt provenance.
17. **Final-layout semantics:** final layouts are held out from experimenter tuning/selection before freeze, but final Phase-A may train on each final layout after reserve opening because zero-shot layout generalization is not the primary RQ.
18. **Frontend remains downstream:** none of these refinements changes the accepted DEC-049 direction. The final UI is rebuilt from scratch using a different framework only after the v2 scientific/backend contract is stable.

## Consequences for T-525

The framework-neutral adapter foundation must expose exact interaction accounting, legal update boundaries, full scientific-state serialization/restore, behavior-policy state, separate online/probe modes, and branch cloning. It must not simply wrap legacy episode-based v1.x execution or rely on library save files without round-trip conformance tests.

## Consequences for T-526/T-527

The physical-machine pilot must calibrate the environment ladder and uncertainty support without selecting preferred rankings. T-527 freezes common gamma/reward/horizon semantics, exact interaction/probe grids, retained methods, method-specific optimization settings, final severity values, root count, failure policy, interval/multiplicity rules and the machine-readable final firewall before any final reserve access.

## Scope control

This closure does not add new algorithm arms, pixels, large external benchmarks, specialized continual-learning mitigations, dynamic obstacles, reward shifts or a composite resilience score. New methodology research is reopened only if a concrete implementation or non-final pilot exposes a specific unresolved validity problem.
