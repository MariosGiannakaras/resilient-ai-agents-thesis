# Protocol v2 deep-chain validity audit — pass 2

**Status:** active `T-524` research record  
**Date:** 2026-08-28  
**Scope:** second chained pass over the already accepted protocol-v2 methodology, current implementation, canonical bibliography, and primary external evidence  
**Rule:** this document records additional validity gaps and accepted deltas; it does not authorize final tuning, final-reserve access, UI implementation, or thesis writing.

## Executive verdict

The first protocol-v2 methodology pass remains directionally correct, but it was not yet sufficiently specific to guarantee that two independently reasonable implementations would estimate the same scientific quantities. The second pass therefore audits the full chain

`estimand -> environment -> training -> evaluation -> checkpoint -> branch point -> change -> adaptation -> statistics -> compute -> reproducibility`.

Twenty bounded checks were completed. The most important new conclusion is that the final design must distinguish **policy quality**, **online deployed utility**, and **disturbance-specific adaptation benefit**. It must also make the branch point, time-limit semantics, interaction accounting, learning-state continuation, and deep-RL update clocks explicit.

The stronger primary Phase-B causal design is now:

1. independently train each method/root/layout under Phase A;
2. take the method's exact own scientific checkpoint at a valid update boundary;
3. execute one shared nominal, no-learning deployment prefix when a pre-change prefix is required;
4. at the declared boundary, clone the same learner/deployment state into four post-boundary branches;
5. keep learning disabled in both Frozen branches;
6. enable ordinary method-native updates in both Adaptive/Continual branches **from the boundary onward**, not before it;
7. compare disturbed against matched nominal branches inside each regime;
8. estimate disturbance-specific adaptation with a difference-in-differences contrast rather than raw Continual-minus-Frozen alone.

This cleanly separates post-boundary learning from pre-boundary policy improvement and keeps all four branches identical at the causal branch point. An always-learning-from-deployment-start regime would answer a different question and may only be added later as a secondary sensitivity design if its value justifies the matrix cost.

## Evidence classes

### Canonical evidence already available

- `SRC-4ED8B918E3` — Patterson et al., *Empirical Design in Reinforcement Learning*: interaction accounting, online/offline evaluation distinctions, stochastic comparison, tuning opportunity, paired design, baselines, experimenter bias and failure-handling principles.
- `SRC-8D4F62D85D` — Henderson et al., *Deep Reinforcement Learning That Matters*: implementation/hyperparameter/seed sensitivity.
- `SRC-660560956D` — Steinparz et al., reactive exploration under non-stationarity: decayed exploration and stale replay can impede adaptation; replay/exploration interventions are separate mechanisms.
- `SRC-4C34DF3E17` and `SRC-5775601BD7` — continual deep-RL plasticity/interference evidence.
- `SRC-620F17076C` — Zhang et al., observation perturbation/robustness: true state and observed state are distinct, perturbation support/budget matters, and unconstrained perturbation can make the problem qualitatively different.
- `SRC-32A0866AF8` — DQN foundation, used as algorithm background rather than resilience evidence.
- `SRC-CD5F67F3E6` — PPO foundation.

### Genuine bibliography gaps found in this second pass

Content/title/identifier searches of `ThesisBibliography` did not find canonical records for these four primary works. They should be upstreamed before `T-524` closes:

1. Pardo et al. (2018), *Time Limits in Reinforcement Learning* — finite-horizon time-awareness versus administrative truncation/bootstrapping.
2. Engstrom et al. (2020), *Implementation Matters in Deep Policy Gradients: A Case Study on PPO and TRPO* — material effect of code-level PPO/TRPO implementation choices.
3. Fedus et al. (2020), *Revisiting Fundamentals of Experience Replay* — replay capacity and replay ratio as material DQN/Q-learning-system variables.
4. Nikishin et al. (2022), *The Primacy Bias in Deep Reinforcement Learning* — early-data bias and reset-based mitigation, used here to justify diagnosis/caution rather than importing reset interventions.

These are new gaps, not permission to add four more algorithm arms. Their role is methodology/implementation validity.

## Deep chain 2 — twenty checks

### 1. RQ and estimand separation — PASS WITH SHARPENING

The Phase-A/Phase-B split remains correct. Phase A asks about nominal learning and attained policy quality. Phase B asks about resistance and post-boundary adaptation. CPU cost, failure rate and artifact cost are reported resource outcomes, not silently folded into learning quality or resilience.

**Delta:** every result artifact must identify whether it is a training-process measure, no-learning policy-quality probe, online deployment outcome, resilience gap, or compute/provenance measure.

### 2. Four-branch matched-reference logic — PASS, BUT RAW `Continual - Frozen` IS INSUFFICIENT

For a larger-is-better root-level metric `Y`, define

- `D_F = Y(Frozen, disturbed) - Y(Frozen, nominal)`;
- `D_A = Y(Adaptive, disturbed) - Y(Adaptive, nominal)`;
- `AB = D_A - D_F`.

`AB` is the primary disturbance-specific adaptation-benefit contrast. Raw `Adaptive_disturbed - Frozen_disturbed` remains descriptive absolute deployed performance because it can include regime-level differences unrelated to the disturbance itself.

**Delta:** Phase-B statistics must implement the matched difference-in-differences estimand explicitly and preserve its component cells.

### 3. Online deployment versus no-learning policy probes — NEW CRITICAL GAP

Training/deployment return and offline test return answer different questions. Exploration and other behavioral stochasticity cost real reward online but can be removed or standardized during an offline probe.

**Delta:** report both:

- **online deployed utility**, measured on the actual Frozen/Adaptive branches and counting exploration/adaptation costs; and
- **standardized no-learning policy probes**, run at fixed interaction checkpoints in isolated evaluator environments/RNG streams without learner updates.

Neither surface is allowed to substitute for the other.

### 4. Phase-A fairness budget — CONFIRMED

The common sample budget remains environment interactions/timesteps. Equal episode counts are not a fair main cross-family budget when episode lengths differ.

**Delta:** resolved configs store requested and actual training interactions; completed episodes remain descriptive.

### 5. Phase-B adaptation budget — NEW CRITICAL GAP

The earlier design still described post-change windows mainly in episodes. That can give different methods different amounts of post-change experience.

**Delta:** the primary post-boundary horizon is an exact common **environment-interaction budget**. Episode counts, success counts and truncations are recorded, but they do not define the adaptation opportunity. If the interaction budget ends mid-episode, this is a measurement/campaign stop, not an artificial MDP terminal transition.

### 6. Termination versus truncation/time limits — NEW CRITICAL GAP

The GridWorld correctly exposes `terminated` separately from `truncated`, but legacy tabular/v1.1 agents currently use `bootstrap_on_truncation=False` while the observation contains position and not remaining episode time.

Primary evidence distinguishes two cases:

- if the horizon is intrinsic to the task, remaining time belongs in the agent-visible state to preserve Markov semantics;
- if the horizon is an administrative training/evaluation cutoff, it is truncation and value learners should bootstrap from the final observed state.

**Accepted v2 default:** treat `max_steps` as an **administrative cutoff**, preserve the position-state semantics, and bootstrap on truncation. A true finite-horizon task would be a different explicit protocol because it would require time-awareness in the observation.

**Historical limitation:** protocol-v1.0/v1.1 used the common fixed implementation with no bootstrap on truncation. Their frozen evidence is not altered or discarded, but v2 documentation must record this as a methodological limitation and must not inherit it silently.

### 7. Exact change onset and algorithm update boundary — NEW HIGH-IMPORTANCE GAP

A change can occur at an environment step while PPO updates only after a rollout and DQN/tabular methods update at different cadences. A mid-rollout/mid-update clone creates method-specific ambiguity.

**Delta:** the primary abrupt-change design uses a fresh episode boundary and a method-valid completed update boundary. Phase-A checkpointing finishes all updates due for the declared interaction count. Phase B starts a fresh environment episode. The disturbance is active before the first action of the first post-boundary episode. No confirmatory mid-rollout change is used.

### 8. General scientific checkpoint semantics — CONFIRMED AND STRENGTHENED

Inference serialization is not enough. A scientific checkpoint is the state needed to continue the same learning process under the declared software contract.

**Delta:** round-trip tests must verify continuation behavior/counters/state, not merely equal inference output immediately after load. Environment episode state is intentionally fresh at the Phase-B boundary; learner state is preserved.

### 9. DQN replay and schedule state — NEW HIGH-IMPORTANCE DETAIL

Replay capacity and replay ratio materially affect deep Q-learning systems. `learning_starts`, `train_freq`, `gradient_steps`, target-update cadence and epsilon schedule also change the realized algorithm.

**Delta:** DQN scientific configuration/checkpoint/provenance must include online and target networks, optimizer, replay buffer contents/capacity/logical position/sampling semantics, `learning_starts`, batch size, `train_freq`, `gradient_steps`, target cadence, exploration schedule/progress counters, preprocessing state if used, and relevant RNG. Replay ratio is derived/reported explicitly. Default Continual never clears replay, restarts warm-up, or resets epsilon merely because the environment changed.

### 10. PPO is an implementation system, not only an algorithm name — NEW HIGH-IMPORTANCE DETAIL

Primary evidence shows code-level PPO implementation choices can materially change behavior. Therefore cross-method conclusions cannot be reproduced from the word `PPO` plus a few headline hyperparameters.

**Delta:** record/freeze the maintained-library version, Torch version, policy/value architecture, activation/initialization choices, optimizer, learning-rate/progress schedule, rollout length, batch size, epochs, GAE/discount parameters, clipping/value/entropy coefficients, normalization, max-gradient rule, device and relevant thread/determinism settings.

### 11. Dyna-Q+ own scientific checkpoint — NEW CRITICAL REPOSITORY GAP

The current v1.1 `DynaQPlusAgent.get_state()` already serializes learned model, recency clock, Q values, planning/exploration RNG and counters. However `checkpoint()` serializes only the tabular Q values, and the v1.1 deployment path deliberately starts Dyna variants from the common Q-learning checkpoint and clears their model/recency state at a fresh branch.

That was valid for the v1.1 adaptation-mechanism candidate, but it is not valid for v2 independent-method training.

**Delta:** v2 Dyna-Q+ Phase A trains Dyna-Q+ independently and Phase B clones its **full own Dyna scientific state**. Plain Dyna-Q, if used for the targeted ablation, likewise preserves its learned model/planning RNG/counters. v1.1 Dyna outcomes are never relabelled as v2 independent-training evidence.

### 12. Frozen/Adaptive behavioral semantics — NEW CRITICAL GAP

`Frozen` cannot simply mean “greedy inference” while `Adaptive` continues an epsilon/stochastic behavior policy, because the comparison would confound learning permission with action-selection policy.

**Delta:** both regimes inherit the same predeclared deployment behavior-policy class and schedule/clock state at the branch point. Frozen disables learner/model/optimizer/planning updates; Adaptive enables native updates. Non-learning behavior clocks may advance in both regimes when they are part of the declared deployment policy. No schedule is reset at the change boundary.

If an implementation cannot make update permission the only material regime difference, the online contrast must be named a **deployment-regime effect**, not a pure effect of learning. Standardized no-learning probe DiD remains the cleaner learned-policy adaptation estimand.

### 13. Learning starts at the causal boundary — NEW CRITICAL GAP

If the Adaptive/Continual branch learns during a pre-change deployment block while Frozen does not, their learned states differ before the disturbance arrives. A matched nominal reference helps but does not restore identical state at the change point, and nonlinear interactions can remain.

**Primary v2 design delta:** when a pre-change prefix is used, execute it once with learning disabled and then fork exact state at the declared boundary. Enable updates only in both Adaptive branches from that boundary onward. This is an **adaptive-after-boundary** estimand, not autonomous change detection and not a claim of lifetime continual-learning capability.

An always-on continual-learning deployment is a different estimand and is not added to the default matrix merely for terminology.

### 14. Exact interaction accounting under SB3 update quanta — NEW CRITICAL IMPLEMENTATION GAP

Current Stable-Baselines3 documents that `total_timesteps` is a lower bound: PPO/A2C collect `n_steps × n_envs` rollouts, while DQN/off-policy algorithms collect `train_freq × n_envs` before updates.

**Delta:** project-owned accounting, not the `learn(total_timesteps=...)` argument, is scientific authority. The resolved budget and probe points must be compatible with method update quanta or an explicit common overshoot rule must be frozen. The preferred pilot baseline is `n_envs=1` for this small CPU GridWorld because it makes interaction counts, causal ordering and paired RNG semantics auditable; vectorization remains pilot-gated rather than silently enabled.

### 15. Common probe grid and partial-episode semantics — NEW HIGH-IMPORTANCE GAP

Methods can only expose a scientifically coherent learner state after different update units. A common checkpoint grid must not force PPO to checkpoint mid-rollout or permit DQN to receive extra samples.

**Delta:** freeze a shared interaction-indexed probe grid that is compatible with the retained methods' update quanta. At a probe point, finish only updates due for the already-counted interactions, then evaluate a copied/no-learning policy state. Probe interactions are isolated and never enter training/replay. Learning-curve AUC/time-average is computed on the same declared interaction grid/rule; no method-specific interpolation selected after seeing outcomes.

### 16. RNG, common random numbers and reproducibility scope — STRENGTHENED

Paired designs benefit from controlled shared randomness, but deep-framework randomness and branch execution can leak through global RNG state. PyTorch also does not guarantee bit-identical results across arbitrary releases/platforms/devices.

**Delta:**

- keep project-scoped independent environment, disturbance, action-selection, planning/replay and probe RNG streams;
- clone learner RNG state at the branch point where relevant;
- isolate branch execution so one branch cannot consume a global RNG sequence needed by another;
- use common exogenous root/layout/episode randomness where the counterfactual comparison remains meaningful;
- record Python/NumPy/Torch/library/software/platform identity and determinism settings;
- claim deterministic replay only within the validated software/platform contract, while final scientific inference still uses repeated roots.

### 17. Tuning, checkpoint-selection and final-reserve leakage — STRENGTHENED

Selecting the best checkpoint on the final curve or escalating environment/severity until a desired ranking appears is another form of test-set adaptation.

**Delta:**

- final Phase-A score uses the frozen fixed interaction-budget endpoint/probe rule;
- any early-stopping or checkpoint-selection rule is selected only from development/tuning evidence and then frozen;
- environment complexity and uncertainty severities are fixed from pilot/development evidence before confirmatory results;
- final roots/layouts remain a fresh reserve and are accessed once under the frozen protocol;
- no “rerun until the method wins” iteration on final evidence.

### 18. Held-out layouts and generalization semantics — NEW HIGH-IMPORTANCE GAP

A layout held out from experimenter tuning is not automatically a layout the agent must never train on. If v2 trains on development layouts and evaluates zero-shot on final layouts, the experiment silently becomes a generalization benchmark.

**Delta:** final confirmatory layouts are hidden from hyperparameter/environment/severity selection, but **Phase-A training on each final layout is part of the frozen final experiment** when the target estimand is learning/resilience on that layout. Phase B uses that method/root/layout's own checkpoint. Zero-shot layout generalization remains out of scope unless promoted to a separate RQ before freeze.

### 19. Uncertainty severity and observation-corruption support — NEW HIGH-IMPORTANCE GAP

The current GridWorld observation-corruption implementation does not merely add small sensor noise: when corruption occurs it samples another valid non-obstacle grid coordinate, potentially anywhere in the layout. Thus probability controls corruption **frequency**, while the spatial support implicitly controls **magnitude**.

**Delta:** do not describe the existing condition generically as local sensor noise. Before v2 freeze, define a predeclared observation-corruption family with both frequency and support/magnitude semantics. A bounded local mislocalization rule is a candidate for a more interpretable primary perceptual diagnostic; the current global-random mislocalization can instead remain a harsh supporting diagnostic if retained. The choice is made on scientific semantics/pilot adequacy, never method ranking.

For action remapping, mappings are categorical transformations rather than an automatically ordered scalar severity. Different permutations can have different structural effects despite remapping the same number of actions. Preserve mapping identity and avoid false severity ordering.

### 20. Failure policy, resource accounting and decomposable outcomes — STRENGTHENED

A final method/root that diverges or fails is itself evidence when the failure is algorithmic. Replacing it with a different seed biases results. Conversely, a disk/power/runner failure is not an algorithmic scientific outcome.

**Delta:** pre-register root identities and classify attempts:

- **scientific/algorithmic failure:** retain as method failure evidence; do not replace with another seed;
- **external infrastructure invalidation:** rerun the **same root identity**, retaining the invalid attempt provenance.

Report failure rate explicitly. Any conditional-on-completion estimate must be accompanied by failure-aware reporting/sensitivity; do not invent a numeric worst-case penalty before the metric scale/floor is frozen.

In addition to environment interactions and task outcomes, record method-native compute counters such as real TD updates, planning backups, gradient steps/minibatch updates/epochs, plus wall/CPU time and practical peak memory/artifact size when cheap. These are secondary resource outcomes, not alternative primary fairness currencies.

Finally, episodic return remains the main task-utility outcome but must be accompanied by interpretable components: goal success, truncation, episode/path length, and collision/disturbance-event counts where applicable. A deterministic evaluator-only shortest-path/solvability baseline may be used during environment pilots as a sanity/ceiling reference, never as a fair-ranked learned method and never as learner-visible information.

## Consequences for the primary v2 Phase-B construction

The preferred bounded construction is now:

```text
Phase-A own method/root/layout training
        |
        +-- fixed interaction-budget endpoint at valid update boundary
        +-- standardized no-learning final nominal probe
        |
        v
exact scientific checkpoint
        |
        +-- optional shared nominal pre-boundary prefix, learning disabled
        |
        v
exact common branch-point state
        |
        +-- Frozen nominal      (updates disabled)
        +-- Frozen disturbed    (updates disabled)
        +-- Adaptive nominal    (updates enabled from boundary)
        +-- Adaptive disturbed  (updates enabled from boundary)
```

All four post-boundary branches have the same interaction horizon. Online deployed-utility trajectories and standardized no-learning policy probes are stored separately.

For a larger-is-better metric, the primary within-method disturbance-specific adaptation estimand is

`[(Adaptive disturbed - Adaptive nominal) - (Frozen disturbed - Frozen nominal)]`.

The corresponding raw four cell outcomes and regime-specific disturbance effects remain mandatory so the interaction contrast is never reported without interpretable components.

## Consequences for `T-525`

The bounded implementation task must now additionally prove:

1. explicit `terminated` versus administrative `truncated` handling, with bootstrap-on-truncation under the accepted v2 semantics;
2. exact requested-versus-actual interaction accounting and update-quantum compatibility;
3. shared pre-boundary state and four exact post-boundary clones;
4. updates disabled before the branch point and enabled only for Adaptive post-boundary branches;
5. online deployment outcomes separated from no-learning probes;
6. difference-in-differences component data are retained rather than reconstructing from lossy aggregates;
7. full Dyna-Q(+) continuation state, not Q-table-only v1.1 checkpoint semantics;
8. DQN replay/schedule/warm-up continuation without hidden resets;
9. PPO continuation without hidden timestep/LR/progress-schedule restart;
10. branch-local framework RNG isolation and explicit software/runtime provenance;
11. interpretable component outcomes and method-native update/resource counters.

These are correctness/validity tests with tiny deterministic fixtures. They are not a request to run the pilot/final experiment matrix in CI.

## Consequences for `T-526` and `T-527`

`T-526` must measure, on the physical Windows thesis machine, not only throughput but whether the proposed update quanta/probe cadence, single-environment baseline, checkpoint fidelity and memory/artifact footprint are feasible.

`T-527` must freeze before final access:

- exact interaction budgets for Phase A and Phase B;
- update/probe grid and action-selection rule for standardized probes;
- administrative truncation semantics;
- exact branch-point/change-onset semantics;
- exact Frozen/Adaptive behavior/update rules;
- DQN replay/update settings and PPO implementation settings;
- environment complexity and uncertainty severities/support;
- failure classification/sensitivity policy;
- primary DiD estimand and limited contrast family;
- root count from pilot precision/runtime evidence.

## Historical evidence amendment required

Protocol-v1.0 remains immutable and reportable for its original within-Q-learning estimands. The second audit found an additional limitation: the historical runner treated GridWorld `max_steps` truncation as terminal for value bootstrapping while the agent observation did not include remaining time. This limitation must be disclosed in the historical methodology/threats-to-validity record. It does **not** authorize rewriting old configs, rerunning or replacing accepted FINAL evidence, or numerically pooling old results with v2.

## What this pass explicitly does not add

- no new final algorithm merely because a paper exists;
- no mandatory A2C arm;
- no replay reset, network reset, continual-backprop or primacy-bias reset intervention in the default final matrix;
- no pixel observations;
- no automatic unseen-layout generalization RQ;
- no mid-rollout abrupt-change design;
- no best-checkpoint-on-final selection;
- no fixed root count copied from prior experiments or literature;
- no composite resilience score;
- no new UI work.

## Completion state

**Deep chain 2: 20/20 checks completed.**

The research pass found four genuine new bibliography gaps and multiple protocol/implementation gaps. `T-524` remains `IN_PROGRESS` until those sources are processed through the canonical bibliography workflow, active protocol/decision/task/status documents are reconciled, a new immutable bibliography consumer sync is accepted, and the latest PR #92 head passes its required checks.
