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
- #93 final UI redesign is PAUSED until the v2 scientific/backend workflow stabilizes. The current NiceGUI application is retained only as prototype/implementation history. Per the latest explicit requirement, the final frontend will be rebuilt from scratch with a **different framework**, selected after the framework-neutral v2 backend contract is stable.
- Final standalone packaging is post-thesis #94 / `T-803`, not a pre-WP7 gate; its packaging technology must follow the later selected frontend rather than assuming NiceGUI/PyInstaller.
- **Pre-WP7 approval: NOT APPROVED.** All `T-700+` execution remains blocked.

## Protocol-v2 methodology verdict

The 2026-08-27 chained methodology pass and the 30-point audit fact-check in `docs/research/PROTOCOL_V2_AUDIT_FACT_CHECK.md` support the two-phase decomposition with refinements:

1. **Nominal learning:** independently trained methods under a common semantic environment/information and environment-interaction budget, with periodic standardized no-learning evaluation.
2. **Resilience/adaptation:** each method/root's own trained scientific checkpoint cloned into matched **Frozen** and ordinary-training **Continual** regimes, each with a same-regime no-change reference.

The exact four-branch Phase-B construction is a project experimental design for isolating change and continued-learning effects; literature supports the component principles but does not make this exact layout a universal standard.

The broader feasibility candidate pool includes the audit-requested **Q-Learning, SARSA, DQN, PPO and A2C**, plus **Dyna-Q+** because it adds a distinct learned-model planning and recency-directed re-exploration mechanism. The stronger bounded confirmatory-core candidates are currently **Q-Learning, SARSA, DQN, PPO and Dyna-Q+**. **Dyna-Q** is a targeted planning-vs-recency ablation, not an automatic full arm. **A2C is technically feasible but is not a default full final arm** because its mechanism-level contrast substantially overlaps PPO; it remains a bounded promotion/diagnostic candidate if later non-final evidence establishes distinct thesis value without weakening statistical rigor. Historical R0 remains negative/diagnostic.

No final method retention decision is frozen until the declared pilot/feasibility gate closes.

## Fair-learning and evaluation contract

- Principal common training budget: **environment interactions/timesteps**, not equal episodes, optimizer updates or wall-clock time.
- Fairness means the same semantic agent-visible information, not necessarily the same data structure. Tabular agents may consume the canonical discrete state while neural agents receive a deterministic vector/one-hot encoding of exactly the same semantics; no pixels, hidden map information or change indicators are added to favor deep methods.
- Tuning uses method-specific literature-backed ranges but a predeclared equivalent search/configuration opportunity, common tuning-only roots/partitions, fixed selection metric and deterministic tie rule. Seeds are randomization units, never tuning parameters; library defaults are not automatically fair.
- Periodic standardized **no-learning evaluation** checkpoints separate learned policy quality from exploratory/stochastic training return. Evaluation interactions never update the learner and are accounted separately from the training budget.
- Root/run is the independent randomization unit. Episodes/checkpoints within a root are nested repeated observations; method/regime/condition/layout cells are experimental factors/blocks rather than newly invented independent replicates. Use root-level paired differences where common randomness is scientifically valid, effect sizes and 95% intervals, and only limited predeclared primary contrasts.
- Final root/layout/matrix size is selected from non-final variance/precision/runtime evidence rather than copied automatically from v1.1. No best-seed selection and no mechanical use of multi-task IQM as the single-testbed estimand.

## Continual-deployment and checkpoint contract

`Continual` means ordinary method-native continued training, not a claim that DQN/PPO/etc. are specialized continual-learning algorithms. Deep agents can lose plasticity or interfere with prior learning under non-stationarity; that is an interpretation/diagnostic issue, not justification to add continual-learning mitigations without a separate RQ.

Frozen and Continual branches for one method/root start from the exact same trained scientific state. DQN continuation includes online/target networks, optimizer, replay contents/capacity/cursor/sampling policy, exploration schedule/counters and behavior-relevant RNG/state; replay reset/recency weighting is a separate intervention. PPO-like continuation includes policy/value parameters, optimizer/LR schedule, normalization state when used, counters/RNG and clones only at completed rollout/update boundaries. Tabular/planning agents similarly preserve Q/model/recency/schedule/counter/RNG state required for exact continuation.

The common v2 implementation boundary is an experiment-lifecycle/capability adapter, not a forced Q-table-shaped low-level interface. Tabular learners may keep `act/observe` internally; DQN/PPO library adapters retain method-native replay/rollout/update semantics behind project-owned training/evaluation/checkpoint/provenance contracts.

## Environment and uncertainty

The current project-owned GridWorld engine remains a valid low-complexity anchor because it already supports configurable dimensions/obstacles, discrete actions, the required uncertainty mechanisms, Gymnasium-compatible semantics, deterministic scoped randomness and strict agent/evaluator information separation. The open issue is **discrimination/complexity**, not an automatic need for a different engine.

Do not add pixels, partial observability or a large external benchmark merely to justify deep RL. `T-526` uses a small **ordered, predeclared** set of project-owned GridWorld complexity levels and a frozen discrimination rule. Retain the simplest level that is not universally trivial or universally unsolved, preserves the information/uncertainty contract and is CPU-feasible; do not select environment complexity because it produces a preferred method ranking.

The uncertainty conditions support separate claims:

- **action remapping:** abrupt persistent transition/action-semantics change; primary adaptation condition;
- **action-execution failure:** stationary/stochastic actuation uncertainty; robustness diagnostic;
- **observation corruption:** perceptual/information uncertainty that may introduce POMDP-like ambiguity; supporting diagnostic.

Do not pool these into a single undifferentiated resilience claim. Additional drift/dynamic-obstacle/reward-change conditions are not added for variety.

## Metrics and historical evidence

Phase A retains standardized final nominal evaluation, learning curves/checkpoints, learning efficiency/AUC only alongside curves, variability and CPU/wall cost. Phase B primaries are immediate degradation, cumulative deficit versus the matched same-regime nominal reference, and terminal performance/gap. Recovery remains secondary/sensitivity; there is no composite resilience score.

Protocol-v1.0 remains separately reportable foundational evidence. Candidate v1.1 remains auditable non-final adaptation-mechanism evidence. Neither is numerically pooled into protocol-v2 confirmatory estimates because the training provenance, estimands and protocol differ.

The historical DEC-041 16-root wording has been explicitly reconciled without touching frozen evidence: the actual machine-readable `protocol-v1.0.json` authority contains 32 final roots across `final-l01`/`final-l02`, i.e. 64 root-layout cells per agent-condition pair.

## Bibliography and provenance

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable consumer snapshot is still **`bibliography-integration-v3`**. Bibliography issue #135 owns the v2 methodology refresh.

Content/identifier deduplication found **three genuinely new methodology gaps**, now represented in upstream intake PR #139:

- Patterson et al. (2024), `SRC-4ED8B918E3`;
- Henderson et al. (2018), `SRC-8D4F62D85D`;
- Dohare et al. (2024), `SRC-4C34DF3E17`.

Steinparz et al. (2022) was correctly deduplicated against the already canonical and selected `SRC-660560956D`. Existing DQN `SRC-32A0866AF8` is being re-evaluated/promoted for protocol-v2 nominal-learning foundations rather than duplicated. The new sources now have scientific analysis/evidence on the upstream PR; canonical thesis-selection, validation/merge and a later versioned bibliography sync remain required before T-524 closes.

## Frontend/backend boundary

The v2 scientific/runtime backend must remain frontend-framework neutral. Required backend surfaces include validated experiment/config DTOs, lifecycle/capability state, truthful provisional telemetry, synchronized method/root/layout/branch identities, read-only evaluator visualization state, final comparison/result DTOs, history/export and lightweight resource snapshots.

The current NiceGUI frontend and its framework-specific chart/table choices are not the final architecture. `T-528` will select a **different** framework based on the stable backend contract, local desktop workflow, live dual-GridWorld rendering, scientific chart/table needs, accessibility, maintainability and later standalone-delivery constraints. Scientific logic must not be duplicated in the new frontend.

## Still intentionally unfrozen

Exact v2 final methods after pilot gates, A2C promotion/exclusion, environment complexity, interaction budget, hyperparameters, update schedules, final roots/layouts, exact primary contrast family, final evidence, new frontend framework, redesigned UI and final thesis/presentation remain intentionally unfrozen until their declared gates pass.

## Exact next action

Complete `T-524` by finishing ThesisBibliography #135 canonical analysis/evidence/selection and versioned sync, then close the source-backed v2 RQ/method-role contract. `T-525` is the next bounded implementation package: only the framework-neutral multimethod experiment schemas/adapters, independent nominal training, standardized no-learning evaluation, exact scientific checkpoint/restore and Frozen/Continual clone infrastructure — not final tuning, final matrix or UI. `T-526` then requires the validated Windows CPU/environment/method discrimination pilot, including the A2C promotion decision if still unresolved, followed by `T-527` fair tuning/statistics/protocol-v2 freeze. `T-528` then performs the new-framework frontend rebuild. Do not run old T-522, access any final reserve, resume UI implementation early, or start WP7.
