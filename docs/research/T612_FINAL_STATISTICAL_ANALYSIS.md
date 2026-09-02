# T-612 — Final protocol-v2.1 statistical analysis

**Status:** Final interpretation of the T-611 frozen accepted evidence

**Scientific recipe:** `protocol-v2.1-final`

**Accepted execution:** `protocol-v2.1-final--t610-recovery-01`

**T-611 freeze manifest SHA-256:** `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858`

## Analysis boundary

This report interprets only the predeclared protocol-v2.1 analysis. The independent unit is the root, the two held-out layouts are reduced with equal weight within each root, and all scalar uncertainty intervals are two-sided pointwise 95% Student-t intervals using the actual independent-root count. Direct contrasts are A-minus-B on shared roots after layout reduction. The analysis defines no p-value family, simultaneous inference, composite ranking, or universal winner claim.

All 12 planned roots and both layouts were complete for every RQ1, RQ2 and RQ3 method/condition block. The canonical analysis package and all 12 deterministic exports reproduced byte-for-byte twice from the T-611 accepted Study and matched the mechanical T-610 artifacts exactly. The historical 216-job failed attempt was not an input.

## RQ1 — Nominal learning

### Observed result

Higher Phase-A mean return is better. At the final 8,192-interaction probe, Q-Learning, SARSA and Dyna-Q+ each reached a root mean of -0.100 with no between-root variation (n=12; 95% CI [-0.100, -0.100]). DQN and PPO each averaged -1.862; their intervals were [-2.988, -0.737] and [-3.156, -0.569], with root SD 1.771 and 2.035 respectively.

The trajectory/time-average estimand separated learning efficiency more strongly. Dyna-Q+ was highest at -0.485 (95% CI [-0.512, -0.458], SD 0.042), followed by SARSA at -1.611 ([-1.792, -1.430], SD 0.285) and Q-Learning at -1.628 ([-1.831, -1.425], SD 0.320). DQN (-2.862, [-3.811, -1.914], SD 1.493) and PPO (-2.904, [-3.965, -1.844], SD 1.669) were lower and more heterogeneous across roots.

### Statistical uncertainty and direct comparisons

The paired final-performance contrasts were exactly zero among Q-Learning, SARSA and Dyna-Q+. Each of these methods exceeded DQN by 1.762 return units; the paired intervals were [0.637, 2.888] when expressed as method-minus-DQN. They also exceeded PPO by 1.762, with intervals [0.469, 3.056]. DQN versus PPO was 0.000 with a wide paired interval [-2.112, 2.112].

For time-average performance, Dyna-Q+ exceeded Q-Learning by 1.143 [0.936, 1.350], SARSA by 1.126 [0.949, 1.303], DQN by 2.377 [1.441, 3.314], and PPO by 2.419 [1.352, 3.486]. Q-Learning versus SARSA was -0.017 [-0.294, 0.260], and DQN versus PPO was 0.042 [-1.763, 1.847].

### Scientific interpretation

Under this task and fixed interaction budget, the three tabular/planning methods converged to the same final nominal level, while Dyna-Q+ learned that level substantially earlier on average. Q-Learning and SARSA showed similar learning efficiency. DQN and PPO did not reach the same final nominal performance reliably within the frozen budget and displayed materially greater root-to-root variability. These are controlled-task capability and sample-efficiency findings, not a general ranking of algorithm families.

## RQ2 — Resilience and adaptation benefit

### Observed result

Positive loss means worse disturbed than matched nominal performance; positive adaptation benefit means online learning reduced that disturbance-associated loss relative to frozen deployment.

| Condition | DQN | Dyna-Q+ | PPO | Q-Learning | SARSA |
|---|---:|---:|---:|---:|---:|
| Action-remap cycle | 6.623 [3.798, 9.448] | 26.102 [25.344, 26.860] | 0.060 [-1.552, 1.673] | 32.269 [28.910, 35.628] | 31.127 [28.796, 33.458] |
| Action-remap swap | 1.723 [-3.524, 6.969] | 9.712 [6.500, 12.925] | -0.515 [-1.864, 0.835] | 22.665 [18.078, 27.251] | 13.785 [9.904, 17.667] |
| Action failure 0.15 | -0.194 [-0.770, 0.382] | 0.117 [-0.227, 0.460] | -1.108 [-2.914, 0.697] | -0.175 [-0.451, 0.101] | -0.485 [-1.209, 0.238] |
| Observation corruption 0.05 | 0.323 [-0.719, 1.365] | -0.387 [-0.816, 0.041] | -0.498 [-1.276, 0.280] | -2.698 [-3.880, -1.516] | -3.165 [-4.917, -1.412] |

All cells use n=12 roots and show mean adaptation benefit with its pointwise 95% interval. The canonical machine-readable summary also preserves Frozen and Adaptive losses separately. Action-remap Frozen losses were large for every method (means 28.585–52.921 across the two remaps). Adaptive losses fell sharply for Q-Learning, SARSA and Dyna-Q+, remained high for PPO, and fell more modestly and variably for DQN. The two milder stochastic conditions produced much smaller absolute losses.

### Statistical uncertainty and direct comparisons

On the cycle remap, Q-Learning and SARSA had similar adaptation benefit (Q-Learning-minus-SARSA 1.142 [-3.584, 5.867]); both exceeded Dyna-Q+, while Dyna-Q+ exceeded DQN and PPO. On the swap remap, Q-Learning exceeded SARSA by 8.879 [3.432, 14.327], SARSA exceeded PPO by 14.300 [10.146, 18.454], and Dyna-Q+ versus SARSA remained uncertain at -4.073 [-9.528, 1.382]. DQN versus PPO on the swap was also uncertain at 2.237 [-3.639, 8.114].

No action-failure adaptation-benefit contrast had an interval wholly on one side of zero. Under observation corruption, Q-Learning and SARSA had more negative adaptation benefit than DQN, Dyna-Q+ and PPO in several paired contrasts; Q-Learning versus SARSA remained uncertain at 0.467 [-1.492, 2.425].

### Scientific interpretation

Continued online learning delivered a large, consistent aggregate benefit for the tabular methods under persistent action remapping, with Dyna-Q+ also benefiting but less than Q-Learning and SARSA on the cycle and less than Q-Learning on the swap. DQN showed a smaller cycle benefit and an uncertain swap benefit; PPO showed essentially no aggregate remap benefit. Online learning did not provide a clear aggregate advantage under 15% action failure. For observation corruption, Q-Learning and SARSA were harmed on this estimand, showing that adaptation is condition-dependent rather than uniformly protective. Adaptation benefit is not recovery speed and does not establish universal method superiority.

## RQ3 — Recovery

### Observed result at the primary tolerance

Recovery uses Adaptive-Nominal versus Adaptive-Disturbed mean reward per interaction in passive 32-interaction windows, tolerance 0.10, two consecutive qualifying windows, and a 256-interaction horizon. Non-recovery remains right-censored with null observed recovery time.

| Action-remap condition | Method | Recovered roots | Recovered proportion | Conditional recovery time | Restricted delay through 256 |
|---|---|---:|---:|---:|---:|
| Cycle | DQN | 2/12 | 0.167 | 80.0 [-529.9, 689.9], n=2 | 226.7 [181.2, 272.1] |
| Cycle | Dyna-Q+ | 12/12 | 1.000 | 176.0 [155.7, 196.3], n=12 | 176.0 [155.7, 196.3] |
| Cycle | PPO | 1/12 | 0.083 | 128.0, n=1; no interval | 245.3 [221.9, 268.8] |
| Cycle | Q-Learning | 12/12 | 1.000 | 98.7 [72.0, 125.3], n=12 | 98.7 [72.0, 125.3] |
| Cycle | SARSA | 12/12 | 1.000 | 136.0 [111.3, 160.7], n=12 | 136.0 [111.3, 160.7] |
| Swap | DQN | 8/12 | 0.667 | 68.0 [11.8, 124.2], n=8 | 130.7 [62.7, 198.6] |
| Swap | Dyna-Q+ | 8/12 | 0.667 | 72.0 [8.4, 135.6], n=8 | 133.3 [64.1, 202.6] |
| Swap | PPO | 4/12 | 0.333 | 56.0 [-20.4, 132.4], n=4 | 189.3 [124.8, 253.9] |
| Swap | Q-Learning | 12/12 | 1.000 | 106.7 [63.0, 150.3], n=12 | 106.7 [63.0, 150.3] |
| Swap | SARSA | 12/12 | 1.000 | 98.7 [76.6, 120.7], n=12 | 98.7 [76.6, 120.7] |

### Statistical uncertainty and direct comparisons

On the cycle remap, recovery-status estimates were 1.0 for Q-Learning, SARSA and Dyna-Q+, 0.167 for DQN and 0.083 for PPO. Restricted-delay paired contrasts placed Q-Learning 37.3 interactions below SARSA [-64.5, -10.1], 77.3 below Dyna-Q+ [-106.7, -48.0], 128.0 below DQN [-168.7, -87.3], and 146.7 below PPO [-185.9, -107.5]. SARSA was 40.0 below Dyna-Q+ [-64.7, -15.3].

On the swap remap, Q-Learning and SARSA recovered in every root; DQN and Dyna-Q+ each recovered in eight roots, and PPO in four. Most restricted-delay paired intervals were wide and crossed zero. The clearest separation was SARSA versus PPO: SARSA was 90.7 interactions lower [-161.5, -19.8]. Q-Learning versus SARSA was 8.0 [-32.8, 48.8].

The apparently shorter conditional recovery times for the small recovered subsets of PPO and DQN must not be interpreted as faster overall recovery: those means condition on recovery and omit censored roots. The separately named restricted-delay estimand and the recovery-status indicator carry the censoring-aware direct comparison.

### Tolerance sensitivity

Recovered roots out of 12 at tolerances 0.05 / 0.10 / 0.20 were:

| Method | Cycle | Swap |
|---|---:|---:|
| DQN | 0 / 2 / 12 | 2 / 8 / 12 |
| Dyna-Q+ | 0 / 12 / 12 | 0 / 8 / 12 |
| PPO | 0 / 1 / 6 | 2 / 4 / 7 |
| Q-Learning | 11 / 12 / 12 | 10 / 12 / 12 |
| SARSA | 8 / 12 / 12 | 5 / 12 / 12 |

The broad ordering is robust: Q-Learning and SARSA recover most consistently, especially under the strict threshold, while PPO is least consistent. Exact recovery incidence is threshold-sensitive, particularly for Dyna-Q+, DQN and PPO. The primary conclusions remain anchored to 0.10; the 0.05 and 0.20 results diagnose robustness and are not alternative thresholds selected after outcomes.

### Scientific interpretation

Q-Learning and SARSA showed the most consistent stable recovery across both persistent remaps. Q-Learning recovered earlier than SARSA on the more severe cycle remap, while their swap-remap restricted delays were not clearly separated. Dyna-Q+ eventually recovered in every cycle root but later than the two tabular temporal-difference methods; on the swap it had substantial non-recovery. DQN and especially PPO had frequent right-censoring, so their recovery behavior was less reliable within the fixed horizon. These findings describe recovery at 32-interaction resolution under the frozen neighborhood rule, not an exact latent time-to-recovery process.

## Limitations and claim boundary

- The experiment covers one controlled GridWorld task, two held-out layouts, twelve independent roots, one interaction budget, and the five frozen implementations/configurations. External validity to other tasks, budgets or implementations is not established.
- Layouts, windows and episodes are not independent replicates. Inference uses roots only; pointwise intervals are estimation summaries and are not simultaneous or multiplicity-adjusted tests.
- No formal null-hypothesis p-value superiority family was predeclared. Intervals and numerical ordering must not be relabelled as statistical significance or a league table.
- RQ3 is window-resolved and threshold-sensitive. Conditional recovery-time estimates can have very small denominators and must be read alongside recovered proportions and restricted delays.
- The experiment supports controlled comparative associations under randomized seeds and matched branches. It does not establish universal or real-world causal superiority.

No T-613 polished figure/table asset production, WP7 work, thesis Results/Discussion chapter prose, or defense material is included here.
