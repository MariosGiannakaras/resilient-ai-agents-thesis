# Pre-Import Freshness Implications — August 2026

**Status:** `PROPOSED / PRE-IMPORT / NON-BINDING`  
**Date:** 2026-08-03

## Purpose

A targeted literature freshness pass was performed while the first controlled bibliography import remained blocked by the invalid cross-repository credential. Three recent sources were then ingested, archived, converted, scientifically reviewed, and selected in the canonical `ThesisBibliography` repository. The canonical bibliography now contains 583 definitive source decisions and 112 selected/verified sources.

This consumer-repository note records only the **design implications** that can safely guide preparatory work before synchronization. It deliberately does not use canonical `SRC-*` identifiers because `research/bibliography/manifest.csv` has not yet been installed and consumer-repository source-ID references are validated against that imported manifest.

After controlled import succeeds, each retained statement in this note must be replaced or linked with the exact imported source identifiers and original-language verified evidence.

## 1. Plain Q-learning is not intrinsically invalid under every form of non-stationarity

The 2026 extended version of *Reinforcement Learning in Switching Non-Stationary Markov Decision Processes: Algorithms and Convergence Analysis* studies a structured non-stationary process in which a hidden environmental mode switches among a finite collection of MDPs according to a Markov chain.

Under that specific structure and its formal conditions, the paper proves convergence results for TD learning, policy iteration, and tabular Q-learning. Its Q-learning result requires the stated step-size conditions, sufficient visitation of state–action–environment combinations, and the behavioral-policy conditions used by the analysis.

### Thesis implication

The thesis must not justify the naive continual Q-learning comparator using a blanket statement such as “ordinary Q-learning cannot work in non-stationary environments.” That claim would be too broad.

Instead:

- the exact non-stationarity class must be defined;
- the primary thesis experiment should remain focused on an **unannounced persistent rule/dynamics change and its degradation–recovery trajectory**;
- Q-learning should be judged empirically in that finite-budget recovery setting;
- structured Markov switching with a long-run convergence target should be treated as a different non-stationarity regime from a one-time persistent changepoint;
- observed slow recovery, interference, or forgetting in the thesis experiment must be reported as an empirical result under the frozen protocol, not assumed in advance from algorithm name alone.

This strengthens, rather than removes, the value of a naive continual baseline: it becomes a legitimate comparator whose actual recovery behavior must be measured.

## 2. Non-stationarity detection needs practical-horizon validation

*Is Prior-Free Black-Box Non-Stationary Reinforcement Learning Feasible?* (AISTATS 2025) examines the gap between theoretical non-stationary regret guarantees and the practical behavior of a detector/restart framework. The paper shows that, under the analyzed conditions, the MASTER non-stationarity tests may fail to trigger at practical horizons even though the broader method has order-optimal theoretical guarantees.

Its empirical comparison is specifically conducted in **piecewise-stationary multi-armed bandits**, where quickest-change-detection restart methods perform more robustly than the tested MASTER/random-restart alternatives.

### Thesis implication

Any detector-based GridWorld agent or optional detector-reset baseline must be validated as an operational component, not accepted merely because a paper provides a non-stationary guarantee.

Before final protocol freeze, detector prototypes should expose at least:

- whether and when a detector activates after a known experimental changepoint;
- detection delay;
- false-positive and false-negative behavior where definable;
- sensitivity to the detector's tuning parameters;
- what learner state is reset, retained, or recalled after detection;
- whether detector behavior is still meaningful at the actual pilot/final interaction horizon.

The AISTATS bandit result must **not** be rewritten as evidence that quickest change detection is universally superior in finite-state GridWorld MDPs. Its role is methodological: it justifies practical detector tests and cautions against equating asymptotic theory with useful finite-budget change detection.

## 3. Final-lifetime tuning should not leak the non-stationary evaluation schedule

*Position: Lifetime tuning is incompatible with continual reinforcement learning* (ICML 2025) argues that repeatedly tuning hyperparameters against an agent's complete deployment lifetime can compromise continual-learning evaluation. In non-stationary benchmarks, full-lifetime tuning can allow the researcher to adapt algorithm settings to information about hidden dynamics, change schedules, and the finite evaluation horizon.

The paper proposes `k`-percent tuning as one possible constrained methodology: use only an initial fraction for hyperparameter selection, then freeze the selected hyperparameters for the full evaluation lifetime. Its empirical studies show that the useful value of `k` can be agent–environment dependent; therefore no single percentage should be copied as a universal default.

### Thesis implication

The final experiment protocol should establish a hard boundary between:

1. implementation debugging;
2. hyperparameter search/tuning;
3. pilot protocol design;
4. frozen final evaluation.

The final non-stationary trajectories and change schedules must not become an iterative hyperparameter-selection surface. A practical thesis-specific policy may use separate tuning scenarios, an explicitly bounded tuning budget, or another predeclared separation scheme, but it must be fixed **before** inspecting final results.

The exact fraction, tuning budget, search method, and scenario split remain open until the target-system inventory and pilots exist.

## 4. Impact on the provisional agent-family review

The new evidence changes the interpretation of existing proposed capability roles without selecting final algorithms.

### Frozen nominal reference

Unchanged. A no-update evaluation remains necessary to separate zero-shot resistance from post-change learning.

### Naive continual Q-learning

Strengthened as a legitimate prototype comparator. It must no longer be framed as an obviously inadequate straw baseline. The thesis should test how one shared learner state behaves after the specific persistent change used in the experiment.

### Robust uncertainty-aware comparator

Unchanged in scientific role. It represents pre-deployment robustness under an explicit uncertainty-set assumption and must be interpreted separately from recovery through online updates.

### Explicit change/context-aware learner

Still the strongest provisional structured-adaptation role, but detector behavior must be validated independently from reward performance. Any context-pattern assumptions must remain explicit.

### Detector-triggered restart/reset comparator

The freshness evidence makes this decomposition more scientifically plausible, but it remains **optional**. It should only be added if pilots show that separating detection from context-memory/recall is needed to answer a retained research question without expanding the experiment matrix disproportionately.

## 5. Impact on the primary research framing

The current narrow scope remains supported:

- **Primary resilience/recovery axis:** persistent environment/rule/dynamics change.
- **Supporting diagnostics:** observation corruption and action-execution disturbance.
- **Primary temporal constructs:** nominal performance, immediate degradation, failure depth/duration, recovery trajectory, recovery time where operationally valid, post-change performance, and non-recovery.

The freshness evidence adds two safeguards:

1. comparisons must be phrased for the **specific non-stationarity regime** actually implemented rather than for “non-stationary RL” generically;
2. tuning and detector design must not use information from the final evaluation trajectory in a way that makes the purported adaptation problem easier for the researcher than for the agent.

## 6. Promotion gate

This note remains `PROPOSED` until:

1. the verified bibliography package is imported through the controlled synchronization workflow;
2. the exact three selected freshness records are present in the imported manifest;
3. their original-language evidence is available under `research/bibliography/evidence/`;
4. the target-system inventory is accepted;
5. GridWorld prototypes and the final environment ADR are completed;
6. agent feasibility prototypes confirm which capability roles are implementable and comparable;
7. the final tuning/evaluation boundary is frozen before final runs.

Only then should these implications be integrated into the final research brief, model matrix, and experimental protocol with canonical source traceability.
