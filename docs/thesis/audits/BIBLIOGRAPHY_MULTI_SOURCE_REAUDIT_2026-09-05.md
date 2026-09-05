# Bibliography multi-source re-audit — 2026-09-05

## Purpose

This audit replaces the earlier “choose a bounded shortlist and write from it” mindset with **claim-centred evidence synthesis**. A source being citation-ready means it is eligible for formal use; it does not make that source authoritative by itself.

The audit is grounded in the synchronized `ThesisBibliography` snapshot consumed by this repository and in its canonical analyses/evidence records. It does not promote sources locally or invent new bibliographic authority.

## Corpus rechecked

The synchronized corpus contains:

- **599 canonical source records**;
- **599 analysis records**;
- **147 evidence records**;
- **123 citation-ready records**;
- **19 extracted research-material files**;
- **5 working/research-note files**;
- **39 talk/seminar/transcript/workshop analysis records**.

The previous final-thesis bibliography used only 17 formal sources. Those 17 were real and all were cited, but they represented a narrow slice of the available evidence and concentrated most external citation support in the Introduction, Background and Discussion.

The earlier metadata ranking surfaced 57 additional citation-ready records relevant to one or more thesis themes. That ranking is a discovery aid, **not a 57-source inclusion list**.

## New source-selection rule

There is no longer a fixed “32 references” target. Reference count is an output of claim coverage. For every literature claim:

1. identify all materially relevant records in the synchronized corpus;
2. separate primary evidence, replications/related empirical work, surveys/reviews and informal/context material;
3. compare what the sources actually agree on;
4. preserve incompatible assumptions, task domains and negative/limiting evidence;
5. write only the strongest statement supported by the intersection or clearly attributed differences;
6. cite more than one independent source where that materially improves support;
7. prefer a primary paper for exact algorithm/equation/empirical claims;
8. never convert a literature principle into a claim that a paper prescribed this thesis's exact protocol;
9. never use an external source to override frozen project evidence/results;
10. record a single-source exception only when the claim is inherently source-specific (for example, the definition of that paper's own algorithm) or no independent corroborating source is available.

## Evidence classes

### A — Formal citation-ready

Sources under `research/bibliography/citation-ready/` may support final-thesis literature claims after claim-level comparison.

### B — Verified/analyzed but not citation-ready

These are useful discovery/corroboration candidates but may not appear as formal thesis citations until bibliography governance promotes them upstream and a new immutable sync is consumed. Important examples found by the full-corpus audit include primary/major works such as Watkins & Dayan on Q-learning (`SRC-AD8A2E9A85`), Sutton's 1990 Dyna paper (`SRC-F6BD3A6B18`), Khetarpal et al.'s continual-RL review (`SRC-39696F490F`) and Padakandla's dynamically-varying-environment survey (`SRC-8025C139CE`). Their presence prevents us from pretending the current citation-ready shortlist is exhaustive.

### C — Informal/context/discovery material

Talks, seminars and transcripts may contribute terminology, questions and pointers to primary work, but not exact equations/theorems/numerical claims unless those claims are independently verified.

`SRC-49A9ACCA53` is the main example: its non-stationary safe-RL seminar is valuable for stale-experience/forgetting, variation-budget, restart-vs-detection, utility-plus-safety and within-task-vs-multitask distinctions. Its automatic transcript is not stable formal evidence.

### D — Rejected or unsuitable as formal evidence

Rejected records remain visible in corpus/history but cannot be used to support formal thesis claims. They may only explain why a candidate was excluded.

## Multi-source thematic comparison

### 1. RL foundations, Q-Learning and SARSA

**Formal cluster:** `SRC-701E163AC8`, `SRC-D52DF7B9A4`.  
**Important non-citation-ready corroboration candidate:** `SRC-AD8A2E9A85` (Watkins & Dayan primary Q-learning paper).

Use the textbook/focused citation-ready material for the standard MDP/TD/Q/SARSA mechanism explanation. The Watkins–Dayan record should remain visible as a primary-source promotion candidate rather than being silently ignored. Do not state that Q-learning is inherently unable to operate under all non-stationarity; recent structured-switching work (`SRC-70772C0629`) supplies an explicit counter-boundary under strong assumptions.

### 2. DQN, replay and value-estimation effects

**Formal cluster:** `SRC-32A0866AF8` (DQN foundation), `SRC-CBA29E303A` (experience replay), `SRC-BE53B7970E` (Double-Q / maximization-bias context), plus `SRC-8D4F62D85D`/`SRC-4ED8B918E3` for empirical-design sensitivity.

Synthesis: DQN's replay and target-network mechanisms are part of its learning dynamics; replay settings and implementation choices can materially change outcomes. Double-Q literature contextualizes overestimation but does not imply that Double DQN was tested here. None of these sources establishes DQN as inherently robust or non-resilient under the thesis disturbances.

### 3. PPO and implementation sensitivity

**Formal cluster:** `SRC-CD5F67F3E6` + `SRC-5D0E7E5BD7` + empirical-design sources `SRC-4ED8B918E3`/`SRC-8D4F62D85D`.

Synthesis: PPO's clipped objective constrains policy-update magnitude in its optimization formulation, while implementation details materially affect observed performance. Clipping is not an environmental-robustness guarantee; the thesis must not use it as one.

### 4. Dyna / model-based adaptation

**Formal cluster:** `SRC-701E163AC8` plus current model-based/adaptive sources such as `SRC-D38364B32C`.  
**Primary promotion candidate:** `SRC-F6BD3A6B18` (Sutton 1990).

Synthesis: Dyna combines direct experience and planning from a learned model; under change, stale model content and directed re-exploration are distinct mechanisms worth discussing. The thesis's Dyna-Q+ result is project evidence, not proof that model-based planning is generally better/worse.

### 5. Non-stationarity and continual adaptation

**Formal cluster:** `SRC-660560956D`, `SRC-F909CABDEB`, `SRC-95C9DAEE68`, `SRC-70772C0629`, with `SRC-4C34DF3E17`/`SRC-46CF36BC1E` as plasticity/primacy threat literature.  
**Additional analyzed candidates:** `SRC-39696F490F`, `SRC-8025C139CE`.

Synthesis: “non-stationarity” covers multiple processes and assumptions. Reactive re-exploration, continual-learning plasticity threats, structured hidden-mode switching and arbitrary persistent changepoints are not interchangeable. The thesis studies a predeclared controlled family; broader papers bound interpretation rather than predict the winner.

### 6. Action uncertainty

**Formal cluster:** `SRC-81A15E6905` plus the thesis's own protocol authority for the actual no-op failure mechanism.

Action-robust RL distinguishes probabilistic action replacement from continuous action perturbation and demonstrates robustness/nominal-performance trade-offs. The thesis condition is a **project-specific stochastic no-op with p=0.15**, not the adversarial PR-MDP itself. Literature motivates the distinction; repository code/protocol defines the tested mechanism.

### 7. Observation uncertainty / partial observability / OOD

**Formal cluster:** `SRC-01BBBA7EAB`, `SRC-09DD20BA85`, `SRC-19C2E91926`, `SRC-21EBE15D15`.

Synthesis: incomplete/noisy observation, an observation-corruption kernel, static OOD detection and zero-shot generalization are related but different constructs. Observation corruption in this thesis changes the delivered observation only; it is not automatically a POMDP benchmark, detector study or zero-shot-generalization study. These sources support the conceptual boundaries and trade-offs, not a claim that the thesis implemented their methods.

### 8. Generalization versus online adaptation

**Formal cluster:** `SRC-0882A9B2B0`, `SRC-21EBE15D15`, `SRC-0F8A6588DC`.

Synthesis: train/test interpolation/extrapolation and zero-shot testing prohibit or delimit test-time learning, whereas the thesis explicitly compares Frozen and Adaptive branches after a changepoint. NovGrid adds a closely related controlled-novelty perspective with separate post-change metrics. Therefore generalization, immediate robustness, adaptation benefit and recovery must stay separate in the prose.

### 9. Resilience and recovery

**Formal cluster:** `SRC-0A594EACC0`, `SRC-0F8A6588DC`, plus the project's own predeclared recovery authority.

Both external sources motivate time-resolved disturbance/recovery analysis and separation of degradation from recovery/final performance. Their metric definitions are not imported wholesale. The thesis recovery rule — directed AN−AD gap, fixed 32-interaction windows, tolerance 0.10, two-window stability and right-censoring at 256 — is a project-specific frozen definition.

### 10. Empirical design, statistics and reproducibility

**Formal cluster:** `SRC-4ED8B918E3`, `SRC-8D4F62D85D`, `SRC-0A4AFAC8E9`, `SRC-69D02D7E25`, `SRC-4000D2B40A`.

Synthesis: repeated seeds/roots, hyperparameter opportunity, environment-interaction budgets, implementation variation, reporting uncertainty and termination/truncation semantics can all affect RL conclusions. Bsuite adds the diagnostic-experiment argument that a benchmark is environment + interaction regime + analysis, not a single global score. These principles motivate the thesis design but do not prescribe its exact root count, 8192 budget, four Phase-B branches or Student-t threshold.

### 11. Safety versus resilience

**Formal cluster:** `SRC-3A5E2C9E2C`, `SRC-0406E13B97`, with runtime/safety records where a specific claim requires them.

Synthesis: safe RL introduces constraints/costs beyond task return; safe continual RL additionally raises safety during adaptation and possibly changing constraints. The current thesis does **not** experimentally establish safety guarantees. Safety literature is used to delimit future work and prevent “resilience” from being misreported as “safe RL”.

### 12. Informal seminar: stale experience, restarts and detection

**Context record:** `SRC-49A9ACCA53`.

The seminar's useful ideas are retained as a discovery map. It points toward restart/sliding-window/discounting and variation-budget literature and distinguishes restart schedules from adaptive detection. Exact formal claims require the underlying primary papers. The synchronized corpus currently contains Ding & Lavaei's non-stationary CMDP paper as a cited work inside `SRC-0406E13B97`, not as an independently governed citation-ready record; therefore it must not be silently promoted locally.

## Contradiction and limitation handling

The writing process must actively preserve evidence that weakens over-simple statements. Examples:

- specialized robust/generalization methods do not dominate vanilla baselines in every environment (`SRC-0882A9B2B0`);
- robust action training can trade nominal utility for disturbance robustness and is domain-sensitive (`SRC-81A15E6905`);
- observation-robust methods operate under assumptions that do not transfer automatically to transition/action change (`SRC-01BBBA7EAB`, `SRC-09DD20BA85`);
- continued deep RL can exhibit primacy/plasticity problems, but these papers do not predict failure in this small GridWorld (`SRC-46CF36BC1E`, `SRC-4C34DF3E17`);
- structured non-stationary Q-learning convergence results do not imply rapid recovery after an abrupt persistent remap (`SRC-70772C0629`);
- resilience papers use metric definitions specific to their domains; the thesis's recovery definition remains its own frozen protocol (`SRC-0A594EACC0`, `SRC-0F8A6588DC`).

## Writing consequence

The final bibliography should be expected to grow beyond the current 17 entries, but **no numerical quota is a quality criterion**. A source enters the formal bibliography only when it supports at least one final literature claim and passes the claim-evidence registry. Conversely, if multiple independent sources materially support the same claim, the registry should preserve them rather than arbitrarily choosing one.

The authoritative working artifacts are:

- `docs/thesis/CLAIM_EVIDENCE_TREE.md` — human-readable claim-by-claim synthesis;
- `research/bibliography/claim-evidence-map.json` — machine-readable registry;
- `scripts/validate_claim_evidence_map.py` — fail-closed validation.

The map is expected to evolve with T-716. It is not frozen merely because this initial re-audit is complete.
