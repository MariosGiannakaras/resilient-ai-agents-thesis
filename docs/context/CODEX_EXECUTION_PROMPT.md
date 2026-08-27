# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED/SUPERSEDED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

Repository evidence beats stale chat/session memory.

## Active package

DEC-048 / issue #95 supersedes future execution of the unfrozen protocol-v1.1 candidate.

- Use `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92 until explicitly superseded; do not create a parallel implementation branch or merge early.
- Preserve protocol-v1.0, FINAL-* and historical R0 evidence immutably.
- Candidate v1.1 remains auditable non-final history; **do not execute old T-522 or inspect/generate its final reserve**.
- Current task: **`T-524` IN_PROGRESS** — source-backed protocol-v2 RQ/estimand/method-role freeze.
- #93 radical UI redesign is PAUSED until the v2 scientific contract stabilizes.
- Final standalone Windows packaging is post-thesis #94 / T-803.
- `T-511` remains USER_VALIDATION_REQUIRED; `T-700+` remains blocked until all science/application gates and explicit user approval.

## Startup / resume

1. Inspect `git status`, branch, recent commits and PR #92/current-head CI.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Inspect/resume IN_PROGRESS work before READY work.
4. Read DEC-048, `docs/research/PROTOCOL_V2_RESEARCH_DESIGN.md` and issue #95 for current science.
5. Preserve validated predecessor work; supersession changes future use, not historical facts.

## Protocol-v2 scientific contract

The thesis compares resilient RL agents under uncertainty/change. GridWorld is the controlled experimental/visualization testbed, not the thesis subject.

### Phase A — nominal learning

Retained methods train independently from method-appropriate fresh initialization under the same semantic environment, agent-visible information, action/reward contract and main **environment-interaction/timestep budget**. Do not force equal episode counts, optimizer updates or universal hyperparameters.

Use periodic standardized no-learning evaluation checkpoints so exploratory/stochastic training returns are not treated as directly comparable policy quality.

### Phase B — resilience/adaptation

For each retained method/root/layout, clone the same trained scientific state into matched:
- **Frozen** — no learning-state updates during deployment;
- **Continual** — ordinary method-native continued learning under a predeclared update schedule.

Each regime also has a matched no-change reference. `Continual` is a continued-training baseline, not automatically a specialized continual-RL algorithm.

Method checkpoints include all state needed for exact continuation. DQN includes online/target networks, optimizer, replay contents/cursor/policy, exploration schedule/counters and RNG. Actor-critic methods clone policy/value/optimizer/schedule/normalization/counter/RNG state only at completed rollout/update boundaries. Replay reset or plasticity-preserving interventions are separate scientific interventions, not implementation conveniences.

### Candidate method roles — pilot-gated

Strong core candidates: **Q-Learning, SARSA, DQN, PPO, Dyna-Q+**.

**Dyna-Q** is a targeted planning-vs-recency ablation, not an automatic full final arm. **A2C is not retained as a full final arm by default** because its mechanism-level contrast substantially overlaps PPO; use it only as a bounded fallback/diagnostic if pilot evidence establishes distinct value. Historical R0 remains negative/diagnostic. Do not freeze the final method count before pilots.

Use maintained deep-RL library adapters where scientifically appropriate; do not reimplement DQN/PPO merely for ownership. The project wrapper must preserve provenance, RNG, checkpoint and information boundaries.

## Fairness / environment / statistics

- Bounded method-specific tuning uses predeclared literature-backed ranges, tuning-only roots/partitions, a common configuration/search opportunity and a frozen selection metric/tie rule. Seeds are randomization units, never tunable parameters; library defaults are not automatically fair.
- Pilot a small **ordered** set of project-owned GridWorld complexity levels. Predeclare the discrimination rule and retain the simplest level that is not universally trivial or universally unsolved, supports the uncertainty contract and remains CPU-feasible. Do not choose a level because it favors a method; do not add pixels/partial observability merely to favor deep RL.
- Persistent action remapping is the primary adaptation claim. Action-execution failure is a stochastic actuation-robustness diagnostic; observation corruption is a perceptual-uncertainty diagnostic and may create POMDP-like ambiguity. Do not pool these into one undifferentiated claim.
- Phase-B primary components are immediate degradation, cumulative deficit versus matched same-regime nominal reference, and terminal performance/gap. Recovery remains secondary/sensitivity; no composite resilience score.
- Episodes are nested observations, not independent replicates. Use paired root-level comparisons where common randomness is valid, effect sizes and 95% intervals, and only predeclared primary contrasts. If p-values are used, multiplicity handling must be frozen first.
- Final methods, environment, roots, budgets and contrasts freeze from non-final variance/precision/runtime evidence before final access. Historical v1.0/v1.1 evidence is reported separately and never numerically pooled into v2 confirmatory estimates.

## Task order

`T-524` research/source freeze -> `T-525` common multimethod/pilot foundation -> `T-526` validated-Windows environment/method feasibility pilots -> `T-527` fair tuning/statistics/protocol-v2 freeze -> `T-528` UI redesign -> `T-511` human acceptance -> `T-610..T-613` v2 final evidence -> explicit approval -> WP7.

Do not use hosted CI as a substitute for T-526's required physical-machine runtime evidence.

## Validation and Git

For each **one bounded scope**, validate dependencies/acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, inspect the diff, reconcile docs/issues and push coherent checkpoints.

Testing is proportional: information boundaries, determinism, serialization/checkpoint fidelity, configuration, statistical known answers and representative integration. Scientific pilot/final matrices are not CI tests. PR CI is the canonical full-suite guard.

Do not submit an `APPROVE` review on your own PR. The historical workflow may permit an **own-PR squash merge**, but this package remains draft/unmerged until integrated gates allow it.

Report `Project: X/Y` only from the canonical finite checklist. In-progress/failed work never counts as complete.

## Stop conditions

Continue repository reading, implementation, routine Git, PR creation, CI diagnosis, objective review and dependency-valid next-task selection autonomously. Stop only for access/credentials, required external-machine evidence, safety/privacy/legal/licensing blockers, a genuinely user-reserved subjective choice, mandatory human application acceptance or explicit pre-WP7 approval.
