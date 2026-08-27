# Protocol-v1.1 Candidate Design Rationale

**Status:** T-521 candidate design; non-final and amendable only before freeze  
**Machine-readable authority:** `configs/protocols/protocol-v1.1.json`  
**Historical evidence:** protocol-v1.0 and all `FINAL-*` bundles remain immutable

## Research framing

The thesis compares agent strategies for acting under uncertainty and unannounced environmental change. GridWorld is the common controlled testbed and visualization surface; it is not the thesis subject.

The five main candidate strategies are deliberately mechanism-distinct:

1. **Fixed Q-Learning** — learned action values are retained but no longer updated after deployment;
2. **Adaptive Q-Learning** — model-free off-policy value updates continue online;
3. **SARSA** — model-free on-policy value updates continue online;
4. **Dyna-Q** — real updates are augmented with planning over an empirical learned model;
5. **Dyna-Q+** — Dyna-Q planning is augmented with recency-driven re-exploration for possible change.

The formal/theoretical basis is maintained in `ThesisBibliography`, including the primary Q-learning source (`SRC-AD8A2E9A85`), the primary Dyna source (`SRC-F6BD3A6B18`), the continual-RL review (`SRC-39696F490F`), the dynamically-varying-environment survey (`SRC-8025C139CE`), the Sutton–Barto full-text source (`SRC-701E163AC8`), and the partially verified historical SARSA-lineage record (`SRC-D20C157084`). The partially verified record is not used as sole citation support for claims that require checked full text.

## Controlled initial-knowledge policy

This is an adaptation-mechanism experiment, not an end-to-end training benchmark.

All five main strategies therefore begin evaluation from the same selected nominal tabular-Q checkpoint produced with the already validated Q-learning budget:

- learning rate `0.5`;
- discount factor `0.96875`;
- exploration epsilon `0.125`;
- `512` nominal training episodes per layout;
- no bootstrap on truncation;
- zero initial Q value.

This controls initial nominal action-value knowledge instead of allowing a different pretraining procedure to become an additional confound. Fixed Q-Learning freezes that learned value function. The four adaptive strategies may change their internal state online using only the information visible to every agent.

The `16` pre-change evaluation episodes are intentionally retained. They serve two purposes:

- adaptive value-based strategies can settle under their own update rule before the change boundary;
- Dyna-Q and Dyna-Q+ can populate their empirical model from actual pre-change interaction rather than receiving a privileged world model.

Reference and disrupted branches use the same root/layout/episode seed schedule and are identical before the change boundary. Therefore agent-specific resilience metrics remain paired against that agent's own matched no-change reference even when adaptive strategies update during the pre-change block.

This design must be described explicitly in the thesis. It would be misleading to describe SARSA/Dyna-Q/Dyna-Q+ as independently pretrained end-to-end algorithms in v1.1.

## Bounded non-final configuration surface

The already selected Q-learning settings are not reopened.

Only mechanism-relevant settings that were not previously selected are varied:

### SARSA

- `alpha = 0.25`;
- `alpha = 0.5`.

`gamma = 0.96875` and `epsilon = 0.125` remain common. The two-point alpha check is a bounded fairness/stability check, not a general SARSA hyperparameter search.

### Dyna-Q

- `planning_steps = 5`;
- `planning_steps = 10`.

Base Q-update settings remain common. This isolates the additional planning budget while keeping CPU cost bounded.

### Dyna-Q+

Cartesian product of:

- `planning_steps in {5, 10}`;
- `kappa in {0.0005, 0.001}`.

The planning-step surface is shared with Dyna-Q so the Dyna-Q versus Dyna-Q+ comparison is not confounded by a systematically larger planning budget. The small positive kappa values probe recency exploration without opening a broad search.

Every configuration has a stable human-readable configuration ID and canonical SHA-256 identity. Selection uses all required tuning roots/layouts/conditions; a single run, best seed, or visually attractive trajectory can never select a configuration.

## Tuning conditions

Configuration selection uses only:

- nominal;
- `action-remap-2-swap`;
- `action-remap-4-cycle`.

The two persistent remaps are the primary adaptation mechanism test and nominal performance prevents selecting a configuration that adapts only by becoming unusably poor under normal operation. Action-failure and observation-corruption remain supporting final diagnostics and are not used to tune the candidate agents.

T-522 must execute the complete predeclared tuning matrix or retain/identify every failed or incomplete unit. It must apply the selection/tie rule in the machine-readable candidate protocol without post-hoc metric switching.

## Fresh final reserve

The candidate creates four new final layouts `v11-final-l01..l04` with the same controlled structural constraints as the historical experiment:

- `7 x 7` grid;
- start `(0,0)`;
- goal `(6,6)`;
- six obstacles;
- required shortest-path length `12`;
- horizon multiplier `4`, therefore `48` steps.

Focused tests compare their canonical grid definitions with historical v1.0 layouts so an old final layout cannot silently be reused. The v1.1 development/tuning/final seed banks are mutually disjoint, and the new reserve is checked for overlap with historical v1.0 tuning/final root seeds.

The final reserve is configuration-selection forbidden. Candidate/final execution is fail-closed until T-522 freezes the protocol and the later application/user gates permit final evidence generation.

## Primary estimands and executable paired statistics

The primary metrics remain deliberately non-composite:

- **cumulative deficit** — lower is better;
- **immediate degradation** — lower is better;
- **terminal performance** — higher is better; operationally the existing `ResilienceMetrics.post_change_mean`, which is the mean observed return over the configured terminal window.

The primary metric windows retained for protocol execution are:

- immediate window: `1` post-change episode;
- worst-window diagnostic: `2` episodes;
- terminal window: `4` episodes;
- recovery tolerance: `0` step-reward units;
- recovery stability: `2` consecutive episodes.

Recovery status/time remains secondary and must be accompanied by the already planned sensitivity settings; no threshold is allowed to be selected after looking at final results. No single composite resilience score is permitted.

`src/resilient_agents/v11_statistics.py` implements the predeclared final contrast logic:

1. calculate the first-agent versus second-agent effect inside each root/layout pair;
2. orient the sign so **positive always favors the first-listed agent**;
3. average the four held-out layout effects equally inside each root;
4. use the resulting `32` root-level paired effects as the independent bootstrap units;
5. report the mean effect and deterministic `95%` percentile-bootstrap CI using `10,000` resamples and the predeclared analysis seed;
6. also report layout-specific paired effects;
7. retain negative, null, unexpected and non-recovery results.

This prevents treating four layouts or many episodes from the same root as independent replicates.

## Conditional Robust Planner gate

The historical R0 remains immutable negative/diagnostic pilot evidence and is **not** one of the five default v1.1 competitors.

A redesigned Robust Planner may be promoted as a sixth main comparator only if a separate non-final gate is run before protocol freeze. The gate is predeclared as follows:

### Evidence reserve

- tuning layouts only: `tune-l01`, `tune-l02`;
- the complete eight-root v1.1 tuning seed bank;
- nominal condition only for the viability decision;
- no final layout or final root may be loaded or executed.

### Information/fairness gate

- same all-hidden information policy as the five main strategies;
- no executed action, disturbance flag, change indicator, regime ID or true state;
- any uncertainty set/model prior must be written and hashed **before** gate outcomes are generated;
- no outcome-dependent enlargement, narrowing or relabeling of that uncertainty set.

### Nominal-viability gate

Across all gate episodes:

- overall goal-reaching rate must be at least `0.80`;
- goal-reaching rate on each tuning layout must be at least `0.70`;
- no non-finite/invalid policy/value state is permitted.

These are operational inclusion thresholds, not claims that 0.80/0.70 are universal robustness standards. Their purpose is to prevent a repeat of the historical R0 failure mode in which nominal behavior was dominated by truncation.

### Runtime gate

On the validated thesis machine:

- the complete two-layout/eight-root nominal gate must finish without timeout;
- wall time for that complete gate must not exceed `600` seconds;
- all runtime/provenance artifacts must be retained.

The 600-second bound is an engineering scope limit for this thesis, not a scientific performance metric.

### Promotion rule

The redesigned Robust Planner becomes a sixth final comparator only if **all** information/fairness, nominal-viability and runtime criteria pass. Any failed criterion leaves it excluded from the final ranked set; the failure remains reportable methodological evidence rather than being hidden or retuned after the gate.

Any change to these thresholds before execution requires an explicit candidate-protocol amendment. Changing them after gate outcomes have been observed is forbidden.

## T-522 decision boundary

T-521 defines the candidate design; it does not select final configurations and does not run final evidence.

T-522 may, using only the declared non-final evidence:

- choose one SARSA configuration;
- choose one Dyna-Q configuration;
- choose one Dyna-Q+ configuration;
- keep the fixed Q-learning configurations unchanged;
- accept or reject the optional Robust Planner through the gate above;
- amend resource parameters only before any final reserve access;
- freeze a final v1.1 protocol with explicit selected configuration IDs/hashes.

Only that frozen protocol can later authorize the T-610 final matrix after the application and intended-user acceptance gates are satisfied.
