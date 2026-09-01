# DEC-047 — Broader agent comparison and user-facing names

**Date:** 2026-08-27  
**Status:** Accepted pre-v1.1 scientific/UI refinement

## Context

The thesis is about comparing and evaluating resilient AI agent strategies in uncertain/changing environments. GridWorld is the controlled experimental testbed and visualization surface; it is not the thesis subject itself. The agent selection therefore needs to cover a useful cross-section of resilience/adaptation mechanisms while remaining fair, explainable, reproducible, and realistically executable in the same finite decision environment.

The earlier candidate set F0/C0/D0 was scientifically controlled but still narrow: F0 and C0 are two deployment regimes of the same Q-learning implementation, while D0 is Dyna-Q+. External research on non-stationary/continual reinforcement learning and classical changing-environment experiments commonly compares ordinary TD learners and planning learners rather than relying on one family alone. Sutton and Barto's changing-environment Dyna examples specifically compare Dyna-Q with Dyna-Q+ so that the contribution of directed re-exploration can be separated from planning itself. Related non-stationary empirical work has compared Sarsa, Expected Sarsa, Q-learning, Dyna-Q and Dyna-Q+ over many independent runs.

Robust-MDP/robust-RL literature remains a distinct conceptual branch because it optimizes against model uncertainty rather than relying only on online adaptation. The historical R0 pilot is therefore scientifically useful negative evidence, but its accepted construction cannot be reinstated unchanged after severe nominal truncation.

## Decision

### Main candidate agent strategies

Candidate v1.1 should target five main strategies, subject to implementation and non-final validation gates:

1. **Fixed Q-Learning** — reuse the learned nominal Q policy without post-change updates. Historical technical identity: F0.
2. **Adaptive Q-Learning** — continue ordinary off-policy Q-learning after change. Historical technical identity: C0.
3. **SARSA** — on-policy model-free continual adaptation, learning from the action actually selected by the behavior policy.
4. **Dyna-Q** — continual Q-learning plus an empirical learned model and planning updates, without the Dyna-Q+ recency exploration bonus.
5. **Dyna-Q+** — Dyna-Q plus recency-directed re-exploration of long-untried state/action pairs. Historical technical identity: D0.

This set is selected by mechanism, not by desired model count. It isolates:

- no online adaptation;
- ordinary off-policy model-free adaptation;
- on-policy model-free adaptation;
- model-based planning;
- model-based planning plus explicit re-exploration for change discovery.

### Reference strategies

The following may be implemented as clearly labelled reference/debug bounds but are not ranked as equivalent resilience agents:

- **Random Agent** — lower behavioral reference/correctness fixture.
- **Nominal / fully informed planner** — scale/debug upper reference when useful; any privileged model/evaluator information must be explicit and excludes it from fair agent rankings.

### Robust-planning branch

Historical R0 remains immutable pilot evidence. A **revised Robust Planner** may become a sixth main comparator only if a small predeclared non-final redesign passes all of:

- nominal viability without the previous severe truncation;
- explicit uncertainty-set construction and information-prior disclosure;
- fair interpretation relative to learning agents despite stronger prior model assumptions;
- bounded tuning/runtime cost;
- distinct empirical role not already answered by the five main strategies.

Failure of this gate is a valid negative result; it does not block the five-agent v1.1 design.

### Exclusions

Do not add Expected SARSA merely to increase count unless SARSA-specific non-final evidence shows a material variance/stability question that requires it. Do not add DQN, PPO, SAC, deep actor-critic, meta-learning, or neural robust methods unless the accepted research question/environment representation later requires function approximation. The finite observable testbed does not justify that complexity by itself.

## Fairness and tuning

- All scientific agents use the same agent-visible information boundary. No changepoint truth, executed-action truth, disturbance flags, regime ID, or true evaluator state may leak into adaptive logic.
- Fixed/Adaptive Q-Learning retain the validated common checkpoint/base configuration unless explicitly reopened by evidence.
- SARSA must receive a bounded, predeclared non-final tuning policy appropriate to its on-policy update rather than blindly inheriting a value known to be optimal for Q-learning if evidence shows that would be unfair.
- Dyna-Q and Dyna-Q+ should share the same learned-model/planning machinery where possible; their key planned contrast is `kappa = 0`/no recency bonus versus a predeclared Dyna-Q+ bonus, with planning-step budgets matched when scientifically appropriate.
- Every configuration is evaluated with multiple predefined roots; single-run/best-seed selection is forbidden.
- Final settings and retained agents freeze before final outcomes are inspected.

## User-facing naming and explanation

The primary UI must **not** present opaque technical IDs such as F0/C0/D0 as the names users are expected to understand.

Primary selector label: **Agent strategy**.

Recommended user-facing cards:

- **Fixed Q-Learning** — "Uses what it learned before the change; it does not learn during evaluation."
- **Adaptive Q-Learning** — "Keeps updating its learned action values from new experience."
- **SARSA** — "Learns from the actions it actually follows, including exploratory actions."
- **Dyna-Q** — "Learns from real experience and also plans using an internal model it learns."
- **Dyna-Q+** — "Plans like Dyna-Q and deliberately re-checks actions that have not been tried recently."

Each card/view should provide concise mechanism, adaptation behavior, model-free/model-based classification, key trade-off, and when useful a small explanatory infographic. Technical IDs/method schema/config hash belong in secondary **Technical details / Reproducibility** disclosure only.

The same human-readable names must be used in Compare, Runs, charts, legends, artifacts, screenshots, thesis-facing exports, and presentation assets. The thesis may introduce stable abbreviations after the full names, but must not rely on unexplained internal repository IDs.

## Implementation consequences

- Add a bounded task before candidate-v1.1 freeze to implement deterministic information-limited SARSA and plain Dyna-Q, plus reference fixtures where useful.
- Candidate-v1.1 schema/runner must support the five main strategies only after their focused correctness/determinism/fairness tests pass.
- Update UI architecture/help/agent infographics to human-readable strategy names.
- Update candidate matrix size/runtime feasibility before freeze; keep the existing four-layout/32-root target unless measured non-final runtime requires a documented adjustment.
- Preserve protocol-v1.0, old F0/C0/R0 results and all historical IDs unchanged.

## Evidence basis

This decision uses external research as design evidence, not as final thesis citation promotion. Formal thesis citations still follow the `ThesisBibliography` citation-ready workflow. Relevant external evidence includes continual/non-stationary RL surveys, classical Dyna-Q/Dyna-Q+ changing-environment experiments, robust-RL surveys, and empirical comparisons of Sarsa/Q-learning/Dyna variants. The corresponding formal sources should be verified/promoted through `ThesisBibliography` before WP7 claims depend on them.