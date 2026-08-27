# Current Project Status

**Date:** 2026-08-28  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical execution ledger. Use DEC-048, DEC-049, DEC-050 and the protocol-v2 research records for detailed methodology/UI decisions.

## Current execution state

- Historical accepted baseline through protocol-v1.0 and completed historical WP6 evidence remains immutable.
- **Project: 4/8** master milestones complete (#87: 1, 2, 4, 5).
- **Current task:** `T-524` IN_PROGRESS — source-backed protocol-v2 research contract and bibliography convergence.
- Active protocol-v2 tracker #95 remains **2/10** until the bibliography/source-backed closure is actually complete. Historical #88 is closed/superseded; old `T-522` must not execute.
- #93 final UI redesign remains PAUSED. Final frontend is rebuilt from scratch with a **different framework from NiceGUI** only after the framework-neutral v2 backend/scientific contract is stable.
- Final standalone packaging remains post-thesis #94 / `T-803` and follows the later selected frontend rather than assuming NiceGUI/PyInstaller.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` work.

## Methodology closure state

The open-ended methodology exploration is considered saturated for the current thesis scope after:

1. the 30-point audit fact-check (`PROTOCOL_V2_AUDIT_FACT_CHECK.md`);
2. the second 20-check deep-chain validity pass (`PROTOCOL_V2_DEEP_CHAIN_2.md`);
3. the targeted eight-part closure audit (`PROTOCOL_V2_CLOSURE_AUDIT.md`);
4. accepted refinement decision DEC-050.

New methodology research is reopened only if implementation or a non-final pilot exposes a concrete unresolved validity problem.

## Protocol-v2 core design

### Phase A — nominal learning

Each retained method trains independently using:

- the same project-owned task/reward/action semantics;
- the same semantic agent-visible information;
- a common task-level discount factor `gamma`;
- actual environment interactions as the primary common learning budget;
- algorithm-specific optimization/configuration settings under equivalent predeclared tuning opportunity;
- periodic isolated no-learning policy-quality probes on a common interaction-indexed grid compatible with method-native update boundaries.

Library `total_timesteps` is not scientific authority. Project-owned counters record requested and actual interactions.

The broader feasibility pool includes Q-Learning, SARSA, DQN, PPO, A2C and Dyna-Q+. Current bounded core candidates are Q-Learning, SARSA, DQN, PPO and Dyna-Q+. Dyna-Q is a targeted planning-vs-recency ablation. A2C remains promotion/diagnostic only unless the pilot establishes distinct thesis value at acceptable matrix cost.

### Phase B — resilience/adaptation

For each retained `method × root × layout`, Phase B starts from that method/root/layout's own exact scientific checkpoint.

If a pre-change prefix is required, it is executed once with learning disabled. At the declared change/branch boundary the exact learner/behavior/RNG state is cloned into:

- Frozen nominal;
- Frozen disturbed;
- Adaptive nominal;
- Adaptive disturbed.

Adaptive updates begin only from the first post-boundary transition. Frozen and Adaptive inherit the same behavior-policy class/clock at the branch point. No epsilon, replay, optimizer, warm-up, recency or learning-rate schedule reset occurs merely because a change occurred.

Primary post-boundary opportunity is an exact common environment-interaction budget, not equal episode count.

### Primary Phase-B estimands

Within each regime, disturbance is measured relative to its matched nominal branch. Primary component measures remain:

- immediate degradation;
- cumulative deficit;
- terminal gap/performance.

For each component, the primary disturbance-specific adaptation benefit is the **Frozen loss minus Adaptive loss**, i.e. the four-branch matched difference-in-differences interaction. Positive adaptation benefit means online learning reduced the disturbance-specific loss.

Raw Adaptive-disturbed minus Frozen-disturbed online performance is retained as an absolute deployment contrast but is not the sole causal adaptation estimand. Recovery remains secondary/sensitivity; no composite resilience score is used.

## Time-limit and objective semantics

- GridWorld `max_steps` is an **administrative truncation** in v2, not a hidden finite-horizon task objective.
- Goal arrival is termination; administrative cutoff is truncation.
- Value learners bootstrap through truncation.
- Remaining time is not added to the controlled position observation.
- A campaign interaction budget ending mid-episode is a measurement stop, not an injected terminal MDP transition.
- Historical v1.0/v1.1 `bootstrap_on_truncation=False` without time in state is now an explicit immutable historical limitation, not a reason to alter frozen results.
- Reward semantics and `gamma` are common task-level parameters; no method-specific reward shaping/objective is allowed.

## Deep-method scientific identity/checkpoint contract

A scientific checkpoint means exact continuation state, not inference serialization.

- Q-Learning: Q values plus exploration/schedule/RNG/counters required for continuation.
- SARSA: full corresponding state/restore semantics.
- Dyna-Q(+): Q values, learned model, planning state/RNG, recency state, behavior state and counters. v2 Dyna-Q+ uses its full own Phase-A state; the historical v1.1 Q-table-only common-checkpoint path is not v2 evidence.
- DQN: online/target networks, optimizer, replay contents/capacity/logical position/sampling RNG, `learning_starts`, batch/update/replay ratio, target cadence, exploration schedule/counters and preprocessing/software state.
- PPO: policy/value/shared parameters, optimizer, LR/progress schedule, rollout/update-boundary state, normalization if used, RNG/counters and full implementation/library provenance.

Every retained adapter must pass `train -> serialize -> destroy -> restore -> continue` conformance plus exact branch-point clone tests at legal method-native boundaries.

## Online deployment versus no-learning probes

Two evidence surfaces are mandatory:

1. **online deployed utility**, including real exploration/adaptation costs;
2. **standardized no-learning policy-quality probes**, isolated from training state/RNG and forbidden from entering replay/rollout/model updates.

Value-based exploitation probes use the frozen greedy rule with deterministic tie semantics. PPO uses a frozen deterministic modal-action exploitation probe for the primary cross-method policy-quality surface; native stochastic-policy behavior/entropy may be reported secondarily. Online PPO deployment retains its actual policy-sampling semantics.

## Statistical closure

Root/run remains the independent randomization unit. Layouts/methods/branches/checkpoints/episodes are blocked/repeated/factor structure.

A synthetic coverage stress test of root-level paired/DiD mean effects at indicative `n=16,24,32,48` found Student-t 95% intervals near nominal coverage across normal, skewed and heavy-tailed synthetic root effects (~0.94–0.97), while simple percentile bootstrap intervals systematically under-covered (~0.91–0.94). Therefore a root-level Student-t interval is the current default primary candidate, with root-bootstrap/robust sensitivity and final precision/runtime sizing frozen later at `T-527`. This is not final power analysis and does not freeze a root count.

Scientific/algorithmic failures remain outcomes and are never replaced by another seed. Infrastructure failures may retry only the same registered root identity and retain attempt provenance. Performance denominators and failure rates remain explicit.

## Environment and uncertainty closure

The current project-owned GridWorld engine remains the controlled testbed. T-526 selects the simplest predeclared complexity level that avoids universal floor/ceiling behavior and remains CPU-feasible without using preferred method ordering.

Final layouts are held out from experimenter tuning/selection before freeze. After reserve opening, Phase-A may train on each final layout because the target RQ is learning/resilience on that task, not zero-shot layout generalization.

Uncertainty claims remain separate:

- action remapping: categorical persistent dynamics/action-semantics change; exact mapping identity is retained and remapped-action count is not treated as a universal scalar severity;
- action-execution failure: stochastic no-op actuation uncertainty with explicit frequency;
- observation corruption: perceptual uncertainty with both explicit frequency **and support/magnitude**. The historical global-random valid-cell corruption is a harsh diagnostic, not generic local sensor noise. A bounded local mislocalization support is a pilot candidate for the primary perceptual diagnostic.

No extra change classes are added merely for variety.

## Threats-to-validity boundary

The final thesis may claim only what the controlled design supports. It does not establish universal AI resilience, autonomous change detection, specialized continual-learning competence, pixel/continuous-control benchmark superiority, real-world robotic transfer, arbitrary POMDP robustness or cross-platform bitwise deep-learning reproducibility.

The experiment intentionally targets low-dimensional discrete GridWorld behavior on the validated Windows/CPU thesis machine. Deep-framework reproducibility claims are scoped to the frozen software/platform/device contract; repeated roots remain necessary.

## Bibliography/provenance state

`MariosGiannakaras/ThesisBibliography` remains canonical. Earlier protocol-v2 methodology additions (Patterson `SRC-4ED8B918E3`, Henderson `SRC-8D4F62D85D`, Dohare `SRC-4C34DF3E17`, DQN re-evaluation, existing Steinparz `SRC-660560956D`) were promoted/selected in the upstream repository, but generated package/corpus convergence and the next immutable consumer sync are not yet complete.

The methodology-closure pass found four further genuine source gaps and opened clean intake PR #143 from current bibliography `main`:

- Pardo et al. (2018), *Time Limits in Reinforcement Learning*;
- Engstrom et al. (2020), *Implementation Matters in Deep Policy Gradients*;
- Fedus et al. (2020), *Revisiting Fundamentals of Experience Replay*;
- Nikishin et al. (2022), *The Primacy Bias in Deep Reinforcement Learning*.

These are methodology/implementation-validity sources, not new algorithm arms. They still require canonical intake IDs, analysis, evidence, selection, package/corpus convergence and later immutable thesis-repo sync before T-524 can close.

The accidental temporary bibliography file created during branch setup has been removed from `main`; it contains no scientific content.

## Frontend/backend boundary

DEC-049 remains controlling: the final frontend is selected later and must be **different from NiceGUI**. Existing NiceGUI/Plotly/ECharts/Mermaid/AG Grid/PyInstaller assumptions are prototype/history, not final requirements. Scientific logic remains framework-neutral and backend-owned.

## Still intentionally unfrozen

Exact retained methods, A2C promotion/exclusion, final GridWorld complexity/layouts, interaction budgets, common gamma/reward numerical values, method-specific optimization settings, update/probe cadence, uncertainty probabilities/support radius, final root count, primary contrast subset/multiplicity rule, final frontend framework and final evidence remain pilot/freeze-gated.

## Exact next action

Finish `T-524` upstream bibliography convergence and immutable consumer sync, then mark the source-backed methodology contract complete. `T-525` then implements only the bounded v2 experiment schemas/adapters, exact interaction accounting, independent nominal learning, isolated probes, scientific checkpoint/restore and four-branch clone infrastructure. `T-526` runs the physical Windows feasibility/environment/severity pilot; `T-527` freezes tuning/statistics/machine-readable protocol before final reserve access; `T-528` then rebuilds the UI with the newly selected framework.
