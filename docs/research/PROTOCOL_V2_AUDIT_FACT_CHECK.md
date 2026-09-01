# Protocol v2 audit fact-check and implementation delta

**Status:** active T-524 research record  
**Date:** 2026-08-27  
**Input:** user-provided 30-point methodology audit, treated as hypotheses rather than authority  
**Authority order:** official thesis requirements and explicit current user direction → frozen machine-readable historical protocols/evidence → canonical bibliography evidence → accepted active decisions → this fact-check

## Executive verdict

The audit is directionally strong: the thesis should compare learning methods as well as post-training resilience, preserve protocol-v1.0, separate METHOD from DEPLOYMENT REGIME, use matched own-checkpoint Frozen/Continual branches, tune methods fairly, protect the agent/evaluator information boundary, and freeze a successor protocol only after non-final pilots.

Several audit statements require material correction:

1. the exact `Q-Learning + SARSA + DQN + PPO + A2C` set is a **candidate pool**, not a scientifically mandatory final set;
2. current evidence supports `Q-Learning + SARSA + DQN + PPO + Dyna-Q+` as the stronger mechanism-spanning default confirmatory core, with A2C as a bounded promotion/fallback candidate because it overlaps strongly with PPO;
3. `root × layout × method × regime × condition` is not itself a set of independent replicates; root/run is the independent randomization unit and the other terms are experimental factors/blocks/repeated structure;
4. “same observation representation” means the same **semantic agent-visible information**, not forcing tabular and neural methods to consume the same data structure;
5. a single step-wise `act/observe` agent API must not force PPO/DQN library internals into a tabular abstraction; protocol-v2 needs capability-based adapters around a common experiment lifecycle;
6. the current 7×7 GridWorld is an anchor, not automatically final and not automatically inadequate; environment complexity must be selected by a predeclared ordered discrimination/feasibility pilot;
7. the final UI framework is no longer NiceGUI by requirement. The scientific/runtime backend remains UI-independent, while T-528 must redesign the frontend from scratch using a different framework selected only after the protocol-v2 backend contract is stable.

## Evidence base used by this pass

Canonical / citation-ready evidence already available or being promoted through ThesisBibliography includes:

- `SRC-4ED8B918E3` — Patterson et al., *Empirical Design in Reinforcement Learning*: interaction-based empirical comparison, tuning opportunity, randomness, multi-agent comparison and experimenter bias.
- `SRC-8D4F62D85D` — Henderson et al., *Deep Reinforcement Learning That Matters*: deep-RL seed/hyperparameter/implementation sensitivity and reporting.
- `SRC-0A4AFAC8E9` — Agarwal et al., *Deep RL at the Edge of the Statistical Precipice*: few-run uncertainty/effect-size reporting, with the explicit limitation that multi-task IQM is not mechanically transferred to this hierarchy.
- `SRC-32A0866AF8` — Mnih et al., *Playing Atari with Deep Reinforcement Learning*: re-evaluated for protocol-v2 as DQN foundation, not resilience evidence.
- `SRC-CD5F67F3E6` — Schulman et al., PPO foundation.
- `SRC-660560956D` — Steinparz et al., reactive exploration/non-stationary lifelong RL; reused rather than duplicated.
- `SRC-5775601BD7` and new `SRC-4C34DF3E17` — deep continual-learning plasticity/interference evidence; the latter directly includes long-horizon PPO experiments.
- `SRC-76B2247457` — lifetime tuning separation in continual RL.
- `SRC-4000D2B40A` — bsuite-style small targeted diagnostic environments.
- existing Sutton/Barto, Q-learning, SARSA, Dyna and non-stationarity sources in the canonical corpus.

External primary/source-level fact-checking during this pass additionally covered the original Dyna work, PPO/A3C lineage, current Stable-Baselines3 compatibility/serialization semantics, MiniGrid/diagnostic GridWorld precedent, and the result showing that A2C can be represented as a special case of PPO under controlled settings. External findings are not silently promoted into thesis claims: citation-ready use still goes through ThesisBibliography.

## Audit point-by-point chain

| # | Audit claim | Fact-check verdict | Current repository evidence | Accepted protocol-v2 delta |
|---:|---|---|---|---|
| 1 | Preserve v1.0 and R0 history | **Confirm** | `protocol-v1.0.json` is frozen; FINAL evidence exists; R0 pilot failure is recorded | Never mutate/pool v1.0; retain R0 as negative historical evidence |
| 2 | Separate learning performance from resilience/adaptation | **Confirm strongly** | old v1.0 measures deployment resilience only; active v2 design already separates Phase A/B | RQ-A nominal learning + RQ-B matched resilience remain separate |
| 3 | Target Q, SARSA, DQN, PPO, A2C | **Refine** | Q/SARSA/Dyna-family code exists; no DQN/PPO/A2C adapter yet | Treat all five as feasibility candidates, but do not make A2C mandatory; add Dyna-Q+ as a stronger distinct mechanism candidate |
| 4 | Separate algorithm from deployment regime | **Confirm** | v1.0 F0/C0 already isolates a deployment-regime effect within Q-learning | v2 identity = `method` plus `regime`; never encode Frozen/Continual as separate algorithms |
| 5 | Scientific unit is a predefined comparative experiment | **Confirm** | current run bundle/provenance machinery supports whole experiments; old runner is still f0/c0/r0-specific | v2 campaign/request schema declares all compared methods, budgets, partitions, metrics and contrasts before final results |
| 6 | Fairness is not identical hyperparameters | **Confirm** | existing requirements allow method-specific settings | common semantic environment/information/evaluation contract; interactions as primary resource budget; wall time separate |
| 7 | Hyperparameter tuning must be fair | **Confirm with bounded rule** | v1.0 Q tuning is mature; new methods would otherwise be asymmetric | method-specific bounded spaces + comparable number/search opportunity + same tuning roots/partitions/budget + frozen selection rule |
| 8 | Reassess 7×7 GridWorld for multiple methods | **Confirm, avoid outcome-driven escalation** | current `GridWorldEnvironment` supports arbitrary width/height/obstacles and strict semantics | predeclare a small ordered complexity ladder and choose the lowest level that avoids universal floor/ceiling while remaining CPU-feasible |
| 9 | Retain action remap/failure/observation corruption | **Confirm roles, reject gratuitous additions** | all three are already implemented/frozen historically | remap = primary persistent adaptation condition; action failure = actuation robustness; observation corruption = perceptual diagnostic; no extra uncertainty class by default |
| 10 | Collect learning data across seeds | **Confirm, refine primary measurement** | current final science largely starts from a selected checkpoint | Phase A adds interaction-indexed learning curves plus periodic standardized no-learning evaluation; raw exploratory return is not the sole cross-method policy-quality measure |
| 11 | Define exact trained scientific state | **Confirm strongly** | SARSA has fuller state restore; current Q checkpoint is mainly Q-table; deep methods absent | introduce exact method-specific scientific checkpoint contract; faithful continuation state is stricter than inference-only serialization |
| 12 | Frozen vs Continual for each method | **Confirm concept; pilot-gated feasibility** | validated by F0/C0 within Q-learning | exact own-checkpoint cloning; `Continual` means ordinary method-native continued training with a predeclared schedule; no guarantee it helps |
| 13 | Matched no-change reference branch | **Confirm strongly** | current metric contract already accepts aligned reference curves | for each regime, disturbed branch is compared to same-regime nominal reference; adaptive nominal ref also continues native training |
| 14 | Preserve component resilience metrics | **Confirm with hierarchy** | `metrics.py` already implements nominal/reference gaps, degradation, deficit and recovery | primary Phase-B: immediate degradation, cumulative deficit, terminal performance/gap; recovery/non-recovery secondary/sensitivity; no composite score |
| 15 | Statistical unit/aggregation | **Correct** | v1.1 statistics already root-block then average layouts | root/run is the independent randomization unit; method/regime/condition/layout are factors/blocks; episodes/checkpoints are nested repeated observations; paired root/layout effects where valid |
| 16 | Two GridWorlds represent selected Frozen/Continual pair | **Confirm as backend event requirement, not current UI design** | runtime telemetry is UI-independent but v1.1-specific | v2 telemetry carries method/root/layout/phase/branch/reference identities and synchronized event ordering; final UI may display selected method pair without ten simultaneous worlds |
| 17 | Protect information boundary | **Confirm non-negotiable** | `GridWorldEnvironment`/contracts already separate true/executed/change truth from delivered observation | all adapters receive only protocol-authorized semantic information; UI/evaluator truth never enters learner update path |
| 18 | Use a common agent interface | **Refine architecture** | current `Agent`-style path works well for tabular online methods but runtime/runner are protocol-specific | use project-owned capability adapters: configure/train/evaluate/checkpoint/restore/deploy/observe diagnostics; do not force PPO rollout/update internals into a Q-table-like object model |
| 19 | Algorithm-specific configuration | **Confirm** | current request exposes universal Q fields and is insufficient | discriminated method-config schemas; exact ranges/values remain tuning/pilot outputs, not hard-coded from the audit |
| 20 | Development/tuning/pilot/final separation | **Confirm strongly** | mature stage/partition/provenance controls already exist | reuse the machinery; create v2 partitions/reserve and never inspect v2 final evidence before freeze |
| 21 | New protocol generation | **Confirm** | v1.0 immutable; candidate v1.1 non-final | successor is `protocol-v2` lifecycle; do not rename/rewrite v1.0/v1.1 |
| 22 | Broaden RQs without predetermining answer | **Confirm** | active v2 design already has RQ-A/RQ-B | keep method-family-neutral main question; secondary questions limited to predeclared contrasts/sensitivity |
| 23 | Preserve negative results | **Confirm** | failure/non-recovery retention is already a repository invariant | no tuning/environment changes merely to make every method look competitive; failed/non-recovered outcomes retained under frozen validity rules |
| 24 | Measure CPU feasibility, do not assume GPU | **Confirm** | machine baseline is Ryzen 5 2600X / ~32 GiB / Radeon RX570, no validated CUDA | compact vector-state networks, sequential CPU execution, measured physical-Windows throughput before budgets/root counts freeze |
| 25 | Distinguish training/trained-state/resilience/aggregate results | **Confirm** | current run bundles are robust but schemas are v1.x-oriented | v2 result schema gets explicit artifact classes and IDs linking training root → checkpoint → branch trajectories → root-level metrics → aggregates |
| 26 | Reconcile DEC-041 historical counts | **Confirm exact inconsistency** | DEC-041 says 16 roots; machine-readable `protocol-v1.0.json` contains 32 roots and 2 final layouts; active `PROTOCOL_V1_0.md` already documents this reconciliation | amend DEC-041 with a historical clarification only; machine-readable frozen protocol remains authority and no result is changed |
| 27 | Inspect exact implementation delta | **Confirm; performed in T-524** | old `HeadlessExperimentRequest` is hard-coded to f0/c0/r0, Q fields and episode budgets; runtime launches v1.1 runner only | do not extend old request in place into an incoherent union; build bounded v2 schema/runner/adapters while reusing environment, RNG, bundles, metrics primitives and runtime process management |
| 28 | Respect methodology boundaries | **Confirm** | repository already has strict final reserve, provenance and info-boundary controls | retain all boundaries plus audit corrections above |
| 29 | Desired common GridWorld → per-method training → own checkpoint → Frozen/Adaptive architecture | **Confirm with candidate-set correction** | current backend primitives support the needed layers but not the method-generalized lifecycle | implement this architecture for retained core methods; A2C promotion remains gated; Dyna-Q+ is part of core candidate evaluation |
| 30 | Produce concrete design/repo delta/blockers | **Confirm** | this document + DEC-048/PROTOCOL_V2/TASKS are the durable output | T-524 closes only after bibliography promotion and authoritative docs reconcile all accepted deltas |

## Method-selection chain

### Q-Learning — retain as core

Scientific role: classical tabular off-policy value learning and direct continuity with v1.0. It is not labelled “weak” merely because it is tabular. It provides a low-complexity, interpretable baseline and historical bridge.

### SARSA — retain as core

Scientific role: tabular on-policy TD-control contrast against Q-learning under identical state/action semantics. The repository already has a strict information-limited implementation and full-state restore path. This contrast is compact and interpretable.

### DQN — retain as core

Scientific role: neural off-policy value learning with function approximation, replay and target/update machinery. It tests whether representation/generalization and replay-driven learning produce different nominal/resilience behavior without changing the action space. Replay state is part of the scientific continuation state.

### PPO — retain as core

Scientific role: neural on-policy policy optimization / actor-critic contrast. It adds a materially different update family from DQN and tabular TD control. Checkpointing must occur at a completed rollout/update boundary.

### Dyna-Q+ — retain as core candidate

Scientific role: learned-model planning plus recency-directed re-exploration. Dyna-style planning is mechanistically different from pure model-free learning, and Dyna-Q+ is specifically relevant to changed environments because its exploration bonus encourages testing long-untried actions. Plain Dyna-Q remains a targeted planning-versus-recency ablation, not an automatic full final arm.

### A2C — feasibility/promotion candidate, not default final arm

A2C is technically compatible with discrete actions and CPU execution. However, it overlaps with PPO as an on-policy actor-critic family, and controlled analysis in the literature shows that A2C can be expressed as a special case of PPO under corresponding settings. For a bounded thesis whose confirmed requirement is the **minimum scientifically sufficient set**, adding a full A2C Frozen/Continual/reference matrix is not justified merely for algorithm-name coverage.

Promotion gate: A2C enters the confirmatory core only if a bounded non-final pilot/evidence pass shows a distinct, thesis-relevant contrast that PPO does not already cover and the resulting matrix remains feasible without weakening roots/statistical rigor. Otherwise its exclusion is documented as redundancy/scope control, not technical inability.

### Random and historical R0

Random remains a reference/correctness floor and is never fair-ranked as a learned method. R0 remains immutable historical negative evidence from the earlier robust-planning construction; it is not silently revived as a v2 final method.

## GridWorld verdict

Do **not** replace the environment engine merely to accommodate neural methods. The existing project-owned Gymnasium-compatible environment already has the critical semantics:

- finite discrete action space;
- deterministic discrete true state and delivered observation contract;
- configurable grid dimensions/obstacles;
- action-remap, action-failure and observation-corruption mechanisms;
- strict evaluator/agent information separation;
- deterministic scoped randomness/provenance.

The open scientific question is complexity/discrimination, not engine capability. T-526 therefore uses an ordered ladder of small structural variants. Neural agents receive a deterministic vector/one-hot encoding of the same delivered state semantics; no pixels, hidden maps or change indicators are introduced to manufacture a neural advantage.

## Protocol-v2 execution architecture

```text
ProtocolV2ExperimentSpec
  ├─ partitions / roots / layouts / uncertainty conditions
  ├─ method configurations
  ├─ common interaction and evaluation budgets
  ├─ metric/statistical contract
  └─ retained method set
        |
        v
MethodAdapter registry
  ├─ QLearningAdapter
  ├─ SarsaAdapter
  ├─ DqnAdapter (library wrapped)
  ├─ PpoAdapter (library wrapped)
  ├─ DynaQPlusAdapter
  └─ A2cAdapter only when promotion gate requires it
        |
        +-- train(method-native, fixed interaction budget)
        +-- standardized no-learning evaluation
        +-- exact scientific checkpoint
        +-- restore exact clone
        +-- deploy Frozen or Continual
        v
RunBundle / provenance / runtime observer
        |
        +-- training artifacts
        +-- trained-state identity
        +-- matched resilience branch trajectories
        +-- root-level metrics
        +-- aggregate comparison artifacts
```

The adapter boundary is deliberately above low-level `act/observe`: simple online tabular agents can keep that implementation internally, while SB3-style algorithms can own rollout, replay and optimizer cadence without violating the shared experiment contract.

## Checkpoint corrections required in implementation

The v2 scientific checkpoint is not merely a deployable policy file.

- **Q-Learning/SARSA:** Q values, exploration/schedule state, counters and behavior-relevant RNG state required for exact continuation.
- **Dyna-Q(+):** Q values, learned model, planning/recency state, planning/exploration RNG and counters.
- **DQN:** online/target networks, optimizer, replay contents/capacity/logical position, exploration schedule/counters, preprocessing/normalization if used and relevant RNG/state. A library model save alone is not assumed to preserve replay.
- **PPO/A2C:** policy/value/shared feature parameters, optimizer and learning schedule/counters, normalization if used and relevant RNG/state; clone at completed rollout/update boundary.

A replay reset, optimizer reset or special plasticity intervention is a different scientific intervention and cannot be smuggled into “restore”.

## Statistical correction

For confirmatory inference the root/run remains the independent randomization unit. A complete root may contain multiple matched layouts, methods, regimes and conditions, but those cells are not re-labelled as independent samples merely to increase `n`.

Primary Phase-B contrast family remains bounded:

1. within each method: `Continual − Frozen` adaptation benefit;
2. Frozen cross-method resistance under matched conditions;
3. only predeclared mechanism-motivated cross-method Continual/adaptation-benefit contrasts.

Episodes/checkpoints are longitudinal observations used to construct root-level estimands. Layout handling is frozen as blocking/equal aggregation or another justified hierarchical rule before final access. Effect sizes and 95% uncertainty intervals are primary reporting; any formal p-value family requires a frozen multiplicity rule.

## UI/backend consequence of the latest explicit requirement

The prior repository requirement to keep NiceGUI as the final application framework is superseded by the current explicit direction: **after the backend/scientific redesign, the UI is redesigned from scratch with a different framework.**

This does not invalidate the completed NiceGUI work. It becomes prototype/feasibility history demonstrating required workflows, native-window expectations, truthful telemetry and visualization needs.

Protocol-v2 therefore requires the backend to expose framework-neutral application contracts:

- validated experiment/spec DTOs;
- run lifecycle and capability state;
- append-only/provisional telemetry events;
- synchronized branch/method/root/layout identifiers;
- comparison/result DTOs;
- read-only evaluator visualization state separated from agent input;
- export/history/resource snapshots.

T-528, not T-524/T-525, selects the new frontend framework after the v2 backend contract is stable. Framework selection must be based on the local desktop requirement, live dual-GridWorld rendering, charting, packaging, accessibility, maintainability and absence of duplicated scientific logic.

## Historical reconciliation: DEC-041

`DEC-041_PROTOCOL_V1_0_FREEZE.md` currently says “16 paired roots across the 2 validated pilot layouts”. That prose is stale. The frozen machine-readable `configs/protocols/protocol-v1.0.json` contains:

- final layouts `final-l01`, `final-l02`;
- **32** evaluation root seeds;
- 64 root-layout scientific cells per agent-condition pair.

`docs/experiments/PROTOCOL_V1_0.md` already records that its older 16-root wording was reconciled to the actual machine-readable authority. DEC-041 requires the same clarification. This is historical documentation repair only; no frozen config, FINAL evidence or result is changed.

## Immediate implementation order

1. Finish canonical protocol-v2 bibliography analysis/evidence/selection; merge only after duplicate/content checks.
2. Reconcile active docs and DEC-041; record the final candidate/core distinction and the new frontend-framework requirement.
3. Close T-524 only when the source-backed research contract and bibliography sync are complete.
4. T-525: implement the **bounded infrastructure only** — v2 spec/result schemas, method adapters, standardized no-learning evaluation, exact checkpoint round-trip and branch cloning. No tuning/final matrix/UI.
5. T-526: physical-Windows discrimination/CPU/checkpoint pilot, including A2C promotion evidence if still needed.
6. T-527: fair bounded tuning, final method retention, precision/root review and frozen `protocol-v2` statistical plan.
7. T-528: choose a **different** UI framework and rebuild the UI from scratch against the now-stable backend contracts.
8. No v2 final reserve access or thesis WP7 execution before explicit freeze/approval gates.
