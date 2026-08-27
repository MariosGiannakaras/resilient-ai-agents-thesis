# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger; use progressive task-specific reading for detailed decisions/evidence.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine validation and `T-200` research framing through completed historical WP6 v1.0 evidence.
- `protocol-v1.0`, finalized `FINAL-*`, frozen historical analysis and R0 pilot evidence remain immutable.
- **Project: 4/8** master milestones complete (#87: 1, 2, 4, 5).
- **Current task:** `T-524` IN_PROGRESS — source-backed protocol-v2 research contract.
- Active tracker: #95 **2/10**. Historical #88 closed/superseded at 9/12; its unfinished T-522/v1.1 tuning/freeze work must not execute.
- #93 radical UI redesign is PAUSED until the v2 scientific workflow stabilizes. The current NiceGUI UI/runtime is a technical prototype/foundation, not the accepted final interface.
- Final standalone `.exe` packaging is post-thesis #94 / `T-803`, not a pre-WP7 gate.
- **Pre-WP7 approval: NOT APPROVED.** All `T-700+` execution remains blocked.

## Protocol-v2 methodology verdict

The 2026-08-27 chained methodology pass supports the two-phase decomposition with refinements:

1. **Nominal learning:** independently trained methods under a common semantic environment/information and environment-interaction budget, with periodic standardized no-learning evaluation.
2. **Resilience/adaptation:** each method/root's own trained scientific checkpoint cloned into matched **Frozen** and ordinary-training **Continual** regimes, each with a same-regime no-change reference.

The exact four-branch Phase-B construction is a project experimental design for isolating change and continued-learning effects; literature supports the component principles but does not make this exact layout a universal standard.

Strong core candidates remain **Q-Learning, SARSA, DQN, PPO and Dyna-Q+**. **Dyna-Q** is a targeted planning-vs-recency ablation, not an automatic full arm. **A2C is not retained as a full final arm by default** because its mechanism-level contrast substantially overlaps PPO; it is only a bounded fallback/diagnostic if later pilot evidence establishes distinct value. Historical R0 remains negative/diagnostic.

## Fair-learning and evaluation contract

- Principal common training budget: **environment interactions/timesteps**, not equal episodes, optimizer updates or wall-clock time.
- Tuning uses method-specific literature-backed ranges but a predeclared equivalent search/configuration opportunity, common tuning-only roots/partitions, fixed selection metric and deterministic tie rule. Seeds are randomization units, never tuning parameters; library defaults are not automatically fair.
- Periodic standardized **no-learning evaluation** checkpoints separate learned policy quality from exploratory/stochastic training return. Evaluation interactions never update the learner and are accounted separately from the training budget.
- Episodes nested in a run are not independent replicates. Use root-level paired differences where common randomness is scientifically valid, effect sizes and 95% intervals, and only limited predeclared primary contrasts.
- Final root/layout/matrix size is selected from non-final variance/precision/runtime evidence rather than copied automatically from v1.1. No best-seed selection and no mechanical use of multi-task IQM as the single-testbed estimand.

## Continual-deployment and checkpoint contract

`Continual` means ordinary method-native continued training, not a claim that DQN/PPO/etc. are specialized continual-learning algorithms. Deep agents can lose plasticity or interfere with prior learning under non-stationarity; that is an interpretation/diagnostic issue, not justification to add continual-learning mitigations without a separate RQ.

Frozen and Continual branches for one method/root start from the exact same trained scientific state. DQN continuation includes online/target networks, optimizer, replay contents/capacity/cursor/sampling policy, exploration schedule/counters and RNG; replay reset/recency weighting is a separate intervention. PPO-like continuation includes policy/value parameters, optimizer/LR schedule, normalization state when used, counters/RNG and clones only at completed rollout/update boundaries. Tabular/planning agents similarly preserve Q/model/recency/schedule/counter/RNG state required for exact continuation.

## Environment and uncertainty

Do not add pixels, partial observability or a large external benchmark merely to justify deep RL. `T-526` uses a small **ordered, predeclared** set of project-owned GridWorld complexity levels and a frozen discrimination rule. Retain the simplest level that is not universally trivial or universally unsolved, preserves the information/uncertainty contract and is CPU-feasible; do not select environment complexity because it produces a preferred method ranking.

The uncertainty conditions support separate claims:

- **action remapping:** abrupt persistent transition/action-semantics change; primary adaptation condition;
- **action-execution failure:** stationary/stochastic actuation uncertainty; robustness diagnostic;
- **observation corruption:** perceptual/information uncertainty that may introduce POMDP-like ambiguity; supporting diagnostic.

Do not pool these into a single undifferentiated resilience claim. Additional drift/dynamic-obstacle/reward-change conditions are not added for variety.

## Metrics and historical evidence

Phase A retains standardized final nominal evaluation, learning curves/checkpoints, learning efficiency/AUC only alongside curves, variability and CPU/wall cost. Phase B primaries are immediate degradation, cumulative deficit versus the matched same-regime nominal reference, and terminal performance/gap. Recovery remains secondary/sensitivity; there is no composite resilience score.

Protocol-v1.0 remains separately reportable foundational evidence. Candidate v1.1 remains auditable non-final adaptation-mechanism evidence. Neither is numerically pooled into protocol-v2 confirmatory estimates because the training provenance, estimands and protocol differ.

## Bibliography and provenance

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable consumer snapshot is still **`bibliography-integration-v3`**. Bibliography issue #135 owns the v2 methodology refresh. Content/identifier deduplication found four genuine methodology gaps — Patterson et al. (2024), Henderson et al. (2018), Steinparz et al. (2022), and Dohare et al. (2024) — and they have entered the upstream canonical intake workflow. Existing bsuite and DQN records are re-evaluated rather than duplicated. A later versioned bibliography sync is required after upstream analysis/evidence/selection is complete.

## Still intentionally unfrozen

Exact v2 final methods after pilot gates, environment complexity, interaction budget, hyperparameters, update schedules, final roots/layouts, exact primary contrast family, final evidence, redesigned UI and final thesis/presentation remain intentionally unfrozen until their declared gates pass.

## Exact next action

Complete `T-524` by finishing ThesisBibliography #135 canonical intake/re-evaluation and citation-ready evidence, then close the source-backed v2 RQ/method-role freeze. `T-525` is the next bounded implementation package: only the common multimethod training/evaluation/checkpoint/clone infrastructure and minimum pilot adapters, not final tuning or matrix expansion. `T-526` then requires the validated Windows CPU/environment/method pilot, followed by `T-527` fair tuning/statistics/protocol-v2 freeze. Do not run old T-522, access any final reserve, resume UI redesign #93, or start WP7.
