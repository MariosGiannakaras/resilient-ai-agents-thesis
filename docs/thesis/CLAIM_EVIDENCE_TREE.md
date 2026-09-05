# T-716 claim → evidence tree

**Status:** living pre-writing authority  
**Date:** 2026-09-05  
**Machine registry:** `research/bibliography/claim-evidence-map.json`

## How to use this tree

The unit of writing is the **claim**, not the source. For each claim below:

1. inspect every listed formal source analysis/evidence record;
2. inspect relevant context-only or informal records for contradictory material and discovery leads;
3. prefer primary evidence for exact algorithms/equations/results;
4. combine only statements that are compatible in assumptions and scope;
5. retain limitations and negative evidence;
6. write the narrowest statement supported by the combined evidence;
7. for protocol/result claims, use repository authority for the exact tested definition/value and literature only for motivation/context.

No source in this tree is individually a “source of truth”. A formal source can be correct about its own setting while still being insufficient for the thesis claim.

---

## Chapter 1 — Introduction

### 1.1 RL as sequential decision-making — `LIT-001`

**Formal evidence:** `SRC-701E163AC8`, `SRC-D52DF7B9A4`.  
**Primary promotion candidate/context:** `SRC-AD8A2E9A85`.

**Combined use:** define agent/state/action/reward/policy/value and the Q/SARSA family without overloading the Introduction with algorithm detail.  
**Boundary:** convergence statements belong to their assumptions; stationary Q-learning theory is not evidence of recovery after the thesis changepoint.

### 1.2 Why “robustness”, “adaptation” and “recovery” are not synonyms — `LIT-002`

**Formal evidence:** `SRC-21EBE15D15`, `SRC-0A594EACC0`, `SRC-0F8A6588DC`.  
**Comparison:** zero-shot/no-update capability versus online updating; reference/performance curves versus novelty response; immediate degradation versus recovery/final performance.  
**Write:** the thesis intentionally separates nominal learning, adaptation benefit and temporal recovery.  
**Do not write:** that one external resilience metric is the universal definition adopted here.

### 1.3 Why a small GridWorld can still support a controlled research question — `LIT-003`

**Formal evidence:** `SRC-4000D2B40A`, `SRC-21EBE15D15`, `SRC-4ED8B918E3`.  
**Combined use:** controlled factors, explicit interaction regime and predefined analysis can improve diagnostic interpretability.  
**Boundary:** GridWorld remains a controlled testbed; no transfer claim to robotics/Atari/continuous control.

### 1.4 No universal “best algorithm” framing — `DISC-002`, `DISC-004`

**Formal evidence:** `SRC-0882A9B2B0`, `SRC-81A15E6905`, `SRC-09DD20BA85`, `SRC-4ED8B918E3`.  
**Combined use:** method performance depends on perturbation family, training regime, architecture/implementation and evaluation design.  
**Write:** mechanism comparison under a bounded protocol.  
**Do not write:** a global leaderboard claim.

---

## Chapter 2 — Theoretical background and related work

### 2.1 Q-Learning versus SARSA — `LIT-004`

**Formal:** `SRC-701E163AC8`, `SRC-D52DF7B9A4`.  
**Context/primary candidate:** `SRC-AD8A2E9A85`.  
**Synthesis:** off-policy greedy target versus on-policy next-action target under exploratory behavior.  
**Limit:** no intrinsic-resilience ranking follows from this mechanism difference.

### 2.2 DQN foundation, replay and value-estimation sensitivity — `LIT-005`

**Formal:** `SRC-32A0866AF8`, `SRC-CBA29E303A`, `SRC-BE53B7970E`, `SRC-8D4F62D85D`.  
**Synthesis path:** DQN architecture → replay/target-network role → replay-design sensitivity → Double-Q overestimation context → implementation/reproducibility sensitivity.  
**Limit:** Double DQN was not tested; replay effects after the thesis change remain empirical rather than assumed.

### 2.3 PPO mechanism and implementation sensitivity — `LIT-006`

**Formal:** `SRC-CD5F67F3E6`, `SRC-5D0E7E5BD7`, `SRC-8D4F62D85D`.  
**Synthesis:** clipped surrogate objective plus evidence that implementation details materially affect policy-gradient results.  
**Limit:** clipping is an optimization mechanism, not an environmental robustness guarantee.

### 2.4 Dyna and Dyna-Q+ — `LIT-007`

**Formal:** `SRC-701E163AC8`, `SRC-D38364B32C`.  
**Primary context candidate:** `SRC-F6BD3A6B18`.  
**Synthesis:** direct learning + learned model + planning; under change, stale model information and directed re-exploration are distinct effects.  
**Limit:** project results do not establish a universal model-based advantage.

### 2.5 What “non-stationary” can mean — `LIT-008`

**Formal:** `SRC-660560956D`, `SRC-F909CABDEB`, `SRC-95C9DAEE68`, `SRC-70772C0629`.  
**Additional analyzed context:** `SRC-39696F490F`, `SRC-8025C139CE`.  
**Compare explicitly:** abrupt persistent changepoint; recurring/structured hidden regimes; continual task streams; re-exploration/forgetting assumptions.  
**Limit:** the thesis implements a declared persistent-remap/noise family, not a generic model of all non-stationarity.

### 2.6 Plasticity and primacy as threats to continued deep learning — `LIT-009`

**Formal:** `SRC-4C34DF3E17`, `SRC-46CF36BC1E`, `SRC-F909CABDEB`.  
**Synthesis:** continued learning can face interference/primacy/plasticity problems over long horizons.  
**Limit:** these sources do not predict that DQN/PPO must fail in the thesis's small GridWorld.

### 2.7 Action uncertainty — `LIT-010`

**Formal:** `SRC-81A15E6905`, `SRC-21EBE15D15`.  
**Compare:** discrete probabilistic action replacement, continuous action perturbation, context/dynamics change and persistent action-semantic remap.  
**Limit:** the thesis action-failure condition is a project-specific stochastic no-op, not an adversarial action policy.

### 2.8 Observation uncertainty, POMDP-like ambiguity and OOD detection — `LIT-011`

**Formal:** `SRC-01BBBA7EAB`, `SRC-09DD20BA85`, `SRC-19C2E91926`, `SRC-21EBE15D15`.  
**Compare:** incomplete/noisy observation; observation-kernel robustness; static OOD detector scores; zero-shot context shift.  
**Limit:** the thesis implements none of the cited detector/belief/robust-policy algorithms; they establish conceptual boundaries only.

### 2.9 Generalization is not online adaptation — `LIT-012`

**Formal:** `SRC-0882A9B2B0`, `SRC-21EBE15D15`, `SRC-0F8A6588DC`.  
**Synthesis:** interpolation/extrapolation and strict zero-shot testing differ from online learning after a changepoint; NovGrid provides controlled novelty/post-change metric context.  
**Limit:** FN/FD/AN/AD must not be relabelled as a standard zero-shot benchmark.

### 2.10 Resilience as a temporal process — `LIT-013`

**Formal:** `SRC-0A594EACC0`, `SRC-0F8A6588DC`, `SRC-4000D2B40A`.  
**Synthesis:** reference/performance trajectories, degradation, recovery and diagnostic metrics should remain separate.  
**Limit:** exact thesis recovery semantics come from project authority, not these formulas.

### 2.11 Safety versus resilience — `LIT-014`

**Formal:** `SRC-3A5E2C9E2C`, `SRC-0406E13B97`.  
**Synthesis:** safe RL adds explicit cost/constraint objectives; safe continual RL raises constraint validity during adaptation.  
**Limit:** the present thesis does not demonstrate a safety guarantee. Use this literature to delimit scope and future work.

### 2.12 Fair empirical RL — `LIT-015`, `LIT-016`

**Formal:** `SRC-4ED8B918E3`, `SRC-8D4F62D85D`, `SRC-0A4AFAC8E9`, `SRC-4000D2B40A`, `SRC-69D02D7E25`.  
**Synthesis:** stochastic variation, tuning opportunity, experience budgets, implementation choices, termination/truncation and uncertainty reporting can all change conclusions.  
**Limit:** literature motivates design principles; it does not prescribe this project's exact 180 tuning units, n=12 or recovery rule.

### 2.13 Forgetting/restarts versus adaptive detection — `LIT-017`

**Formal:** `SRC-0406E13B97`, `SRC-660560956D`.  
**Informal discovery:** `SRC-49A9ACCA53`.  
**Verified external primary pointer:** Ding & Lavaei (AAAI 2023) exists and studies known variation budgets with a periodically restarted primal-dual method, but it is not currently an independent citation-ready `SRC-*` record in the synchronized corpus.  
**Rule:** do not silently promote it locally; request upstream bibliography governance if it becomes necessary for formal T-716 prose.

---

## Chapter 3 — Methodology and experimental design

### 3.1 Common actual-interaction fairness — `PROJ-001`

**Literature motivation:** `SRC-4ED8B918E3`, `SRC-8D4F62D85D`.  
**Project authority:** `configs/protocols/protocol-v2.1-final.json`, DEC-055.  
**Write:** why actual interactions are the common experience currency.  
**Exact budget/value:** project authority only.

### 3.2 Tuning opportunity and seed discipline — `PROJ-002`

**Literature motivation:** `SRC-4ED8B918E3`, `SRC-8D4F62D85D`.  
**Project authority:** DEC-055 and `protocol-v2-t527-tuning-sizing-v0.1.json`.  
**Exact facts:** six candidates/method × three tuning-only roots × two dev layouts × five methods = 180 units; 8192 interactions; seeds not tuned; winners q-c06/sarsa-c06/dqn-c05/ppo-c06/dyna-c03.  
**Limit:** none of these exact choices is prescribed by a paper.

### 3.3 Independent roots and precision sizing — `PROJ-003`

**Literature motivation:** `SRC-0A4AFAC8E9`, `SRC-4ED8B918E3`.  
**Project authority:** DEC-058 sizing/freeze evidence.  
**Write:** root is the independent unit; layouts are paired/repeated structure.  
**Exact fact:** smallest candidate n satisfying the predeclared t-interval half-width criterion was 12; observed maximum sizing half-width 0.1428.

### 3.4 Exact matched FN/FD/AN/AD branches — `PROJ-004`

**Literature motivation:** `SRC-4ED8B918E3`, `SRC-8D4F62D85D`.  
**Project authority:** final protocol + Phase-B executor.  
**Write:** matching controls ordinary nominal continued-learning drift.  
**Limit:** this four-branch estimand is our design, not a published universal standard.

### 3.5 Disturbance semantics — `PROJ-005`

**Literature categories:** action `SRC-81A15E6905`; observation `SRC-01BBBA7EAB`, `SRC-09DD20BA85`.  
**Only exact authority:** `protocol_v2_phase_b_executor.py`, `gridworld.py`, final protocol.

Exact project facts that must survive writing:

- swap-right-down: up→up, right→down, down→right, left→left;
- cycle-clockwise: up→right, right→down, down→left, left→up;
- action failure p=.15 -> no-op, position unchanged, collision false, ordinary step reward −.1 unless another terminal/reward rule applies;
- observation corruption p=.05 after true transition; sample valid non-obstacle coordinate excluding current true position; goal/start are not categorically excluded;
- agent receives no true-state/disturbance/executed-action flag.

### 3.6 RQ1 metric — `PROJ-006`

**Literature motivation:** `SRC-4ED8B918E3`, `SRC-4000D2B40A`.  
**Project authority:** `evidence_v2/statistics.py`, `RQ_EVIDENCE_TRACEABILITY.md`.  
**Exact:** final no-learning probe plus trapezoidal time-average over actual interaction axis.

### 3.7 RQ2 metric — `PROJ-007`

**Literature motivation:** diagnostic/matched comparison principles.  
**Project authority:** statistics code + traceability + T-612.  
**Exact:** Frozen loss = FN−FD; Adaptive loss = AN−AD; adaptation benefit = (FN−FD)−(AN−AD).  
**Limit:** positive benefit does not mean disturbed Adaptive exceeds nominal performance.

### 3.8 RQ3 recovery — `PROJ-008`

**External context:** `SRC-0A594EACC0`, `SRC-0F8A6588DC`.  
**Project authority:** `evidence_v2/recovery.py`, traceability, T-612.  
**Exact:** 32-interaction windows; eight windows over 256; directed gap nominal−disturbed; tolerance .10; two consecutive qualifying windows; recovery_time=end of first window of first stable pair; confirmation_time=end of second; otherwise right-censored with `null` recovery time.  
**Forbidden regression:** absolute gap, three-window criterion or converting 256 into a fabricated observed recovery time.

### 3.9 Time-limit semantics — `LIT-016` + project implementation

**Formal:** `SRC-69D02D7E25`, `SRC-701E163AC8`.  
**Project:** final environment/adapter semantics.  
**Write:** termination and administrative truncation are distinct.  
**Limit:** literature does not determine the numerical horizon.

---

## Chapter 4 — Architecture and implementation

### 4.1 Study-first architecture — `PROJ-009`

**Project-only authority:** `src/resilient_agents/study/`, `evidence_v2/`, `desktop/`, `EXECUTION_WORKFLOW.md`.  
**Write:** immutable recipe → deterministic plan → Phase A → checkpoint → matched Phase B → validation/freeze → analysis → assets → stored-evidence UI.  
**Historical note:** Streamlit/React/NiceGUI are superseded architecture history, not current implementation.

### 4.2 Information firewall — `PROJ-010`

**Literature motivation:** `SRC-21EBE15D15` for explicit context/information protocol.  
**Project authority:** `gridworld.py`, Phase-B executor.  
**Write:** evaluator truth may exist for analysis/UI but is not agent-visible learning input.

### 4.3 Exact continuation checkpoints — `PROJ-011`

**Literature motivation:** `SRC-CBA29E303A` for replay state and `SRC-5D0E7E5BD7` for implementation state sensitivity.  
**Project authority:** Study/checkpoint code and DEC-060.  
**Write:** continuation state is method-specific and branch identity is exact.  
**Limit:** external papers do not prescribe the repository serialization format.

### 4.4 RNG/provenance/evidence integrity

**Project authority only:** final protocol seed streams, Study/run-bundle manifests, T-611 freeze, evidence validators.  
**Rule:** external sources may motivate reproducibility but never override recorded seed/provenance values.

### 4.5 PySide6 application boundary

**Project authority only:** `src/resilient_agents/desktop/`, relevant architecture/decision docs.  
**Write:** Experiment → Run → Results → Evidence; live visualization and result display are presentation paths.  
**Do not write:** that the UI is scientific evidence or recomputes estimands.

---

## Chapter 5 — Results

### 5.1 RQ1 — `RES-001`

**Only numerical authority:** T-612 analysis + accepted analysis artifacts + T-613 figures/tables.  
**Literature role:** `SRC-4ED8B918E3`, `SRC-4000D2B40A` justify separating final performance from learning trajectory/sample efficiency.  
**Rule:** no external paper predicts or validates the actual method ordering.

### 5.2 RQ2 — `RES-002`

**Only numerical authority:** T-612/T-613.  
**Literature context:** `SRC-0F8A6588DC`, `SRC-4000D2B40A`, `SRC-0882A9B2B0`.  
**Write:** condition-specific losses/benefit.  
**Do not:** pool action-remap, action-failure and observation-corruption evidence into one global resilience score.

### 5.3 RQ3 — `RES-003`

**Only classification/time authority:** T-612 + `recovery.py` + accepted result artifacts.  
**Literature context:** temporal recovery sources.  
**Write:** recovered x/12, right-censored roots, observed recovery time only among actual events, tolerance sensitivity.  
**Do not:** add post-hoc binomial intervals/significance or survival analysis not in the frozen plan.

---

## Chapter 6 — Discussion

### 6.1 Final nominal performance ≠ learning efficiency ≠ recovery speed — `RES-001`, `DISC-001`

**Formal context:** `SRC-0F8A6588DC`, `SRC-0A594EACC0`, `SRC-4000D2B40A`.  
**Use:** explain why the three thesis RQs cannot be collapsed.  
**Project result:** interpret Dyna-Q+ only from its actual T-612 trajectories.

### 6.2 Adaptation depends on perturbation family — `RES-002`, `DISC-002`

**Formal:** generalization/action/observation robustness sources.  
**Use:** compare known trade-offs and domain dependence with thesis condition-specific observations.  
**Boundary:** mechanism interpretation must be marked as interpretation unless directly measured.

### 6.3 Replay/history under change — `DISC-003`

**Formal:** `SRC-CBA29E303A`, `SRC-660560956D`, `SRC-F909CABDEB`.  
**Use:** motivate a plausible stale-history issue.  
**Critical limit:** without a replay-clearing/reweighting ablation, do not claim replay *caused* a DQN result.

### 6.4 Plasticity/primacy — `LIT-009`

**Formal:** `SRC-4C34DF3E17`, `SRC-46CF36BC1E`, continual-RL survey.  
**Use:** threat/interpretation framework.  
**Limit:** different domains/timescales prevent direct causal attribution.

### 6.5 External validity — `DISC-004`

**Formal:** `SRC-4ED8B918E3`, `SRC-8D4F62D85D`, `SRC-21EBE15D15`, `SRC-4000D2B40A`.  
**Write:** controlled internal validity versus bounded generalizability.  
**Explicit bounds:** one GridWorld family, compact networks, bounded tuning, finite horizon, specific remaps/noise, CPU-feasible study.

### 6.6 Safety boundary — `LIT-014`

**Formal:** established SafeRL + recent safe-continual survey.  
**Write:** safety is a separate research objective requiring costs/constraints and adaptation-time safety evidence.  
**Do not:** claim the present work proves safety.

---

## Chapter 7 — Conclusions and future work

### 7.1 Conclusions

Every conclusion sentence referring to observed method performance must trace to `RES-001`, `RES-002` or `RES-003` and therefore to frozen T-612/T-613 evidence. Literature may contextualize but cannot strengthen the empirical claim beyond the tested protocol.

### 7.2 Explicit changepoint/context mechanisms — `FUT-001`

**Formal:** `SRC-660560956D`, `SRC-0406E13B97`, `SRC-19C2E91926`.  
**Informal discovery:** `SRC-49A9ACCA53`.  
**Write:** detector-triggered reset, context inference and recency mechanisms are future experimental branches distinct from ordinary continued learning.

### 7.3 Broader environments/generalization — `FUT-002`

**Formal:** `SRC-0882A9B2B0`, `SRC-21EBE15D15`, `SRC-4000D2B40A`.  
**Write:** controlled interpolation/extrapolation and broader testbeds as external-validity tests.  
**Do not:** imply current transfer.

### 7.4 Safety-constrained continual adaptation — `FUT-003`

**Formal:** `SRC-3A5E2C9E2C`, `SRC-0406E13B97`.  
**Write:** future extension needs explicit cost/constraint metrics during adaptation.  
**Do not:** retrofit a safety claim onto current return/recovery evidence.

---

## Cross-cutting contradiction register

The following evidence must remain visible when writing apparently simple claims:

| Topic | Evidence that prevents overclaiming |
|---|---|
| Specialized methods are “better” | `SRC-0882A9B2B0` reports domain/algorithm sensitivity and no universal specialized-method dominance. |
| Robust training has no cost | `SRC-81A15E6905` and `SRC-09DD20BA85` explicitly expose robustness/nominal-utility trade-offs and domain dependence. |
| Observation robustness = dynamics adaptation | `SRC-01BBBA7EAB`, `SRC-09DD20BA85`, `SRC-19C2E91926` operate on different information/detection assumptions. |
| Continued deep learning always adapts | `SRC-4C34DF3E17` and `SRC-46CF36BC1E` establish plasticity/primacy concerns, but do not predict this thesis outcome. |
| Q-learning cannot handle any non-stationarity | `SRC-70772C0629` provides a structured switching setting with convergence under strong assumptions. |
| One resilience number is sufficient | `SRC-0A594EACC0`, `SRC-0F8A6588DC`, `SRC-4000D2B40A` motivate decomposed temporal/diagnostic views. |
| Safe adaptation is demonstrated here | `SRC-3A5E2C9E2C`, `SRC-0406E13B97` show that safety requires explicit constraints/costs not measured as a primary thesis outcome. |

## Promotion/discovery queue

The corpus audit identified important analyzed records that are not currently formal citation-ready sources. They should not be lost simply because the current citation layer excluded them:

- `SRC-AD8A2E9A85` — Watkins & Dayan, primary Q-learning paper;
- `SRC-F6BD3A6B18` — Sutton 1990 Dyna primary paper;
- `SRC-39696F490F` — Khetarpal et al., continual-RL review;
- `SRC-8025C139CE` — Padakandla, dynamically varying RL survey;
- Ding & Lavaei AAAI 2023 non-stationary CMDP paper — verified externally and present as a cited work inside the synchronized survey record, but not yet an independently governed `SRC-*` formal record.

If T-716 needs one of these for a formal claim, the correct action is upstream bibliography promotion/verification and a new immutable consumer sync — not a local workaround.

## Completion rule for T-716

Before a T-716 DOCX can pass:

- every substantive external claim must have a claim ID in the machine registry;
- every formal `SRC-*` used by the prose must be citation-ready;
- multi-source claims should retain all materially relevant support rather than arbitrarily selecting one source;
- contradictions/limitations above must remain represented where relevant;
- protocol/project/result facts must resolve to repository authorities;
- bibliography count is not a quota; every listed reference must support at least one concrete final claim.
