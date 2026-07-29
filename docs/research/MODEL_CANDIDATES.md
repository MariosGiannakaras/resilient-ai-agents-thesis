# Model Candidates

No model is final. Selection must follow the research question, final environment class, literature, pilots and actual hardware.

## Selection criteria

- Clear role in answering a research question.
- Compatibility with state/action/observability assumptions.
- Fair training/evaluation protocol.
- Feasible local compute and implementation complexity.
- Availability of a trustworthy implementation or ability to validate it.
- Complementarity rather than redundant model count.
- Ability to checkpoint, reproduce and expose actual state.
- Appropriate baseline or upper-bound interpretation.

## Candidate catalog

| Candidate | Historical status | Possible role | Advantages | Limitations / risks | Expected cost | Fit conditions |
|---|---|---|---|---|---|---|
| Random policy | Repeatedly mentioned | Sanity lower baseline | Trivial, detects environment/metric errors | Not an intelligent comparator | Very low | Any discrete action space |
| Shortest-path/A* planner | Mentioned | Deterministic oracle/planning baseline when map/rules known | Strong calibration; interpretable | Unfair if given information agents do not have; replanning assumptions matter | Low | Known fully observable map |
| Tabular Q-learning | Repeatedly mentioned | Simple model-free RL baseline | Interpretable, feasible, easy to validate | Scales poorly; adaptation depends on continued learning | Low | Small discrete fully observable state |
| SARSA | Repeatedly mentioned | On-policy tabular comparator | Captures behavior-policy effects; simple | Similar scope limitations to Q-learning | Low | Small discrete environment |
| Dyna-Q / tabular model-based RL | Repeatedly mentioned | Planning/adaptation comparator | Explicit learning plus planning; plausible recovery benefit | Planning budget creates fairness issue | Low–medium | Small discrete MDP |
| Custom “resilient Q-learning” | Historical proposal | Potential algorithmic contribution | Could target disturbance detection/adaptation | High risk of ad hoc novelty and biased comparison; requires formal definition | Low–medium | Only with literature gap and supervisor approval |
| MCTS | Historical proposal | Online planning comparator | Responds to known/current model changes | Needs simulator/model access; per-step compute fairness | Medium–high | Generative model available |
| PPO | Repeatedly mentioned | Neural model-free baseline | Common continuous training pipeline; handles larger encodings | Likely unnecessary for tiny tabular grids; variance/compute | Medium–high CPU | Larger state representation or benchmark rationale |
| Frame-stack PPO | Historical proposal | Limited-memory heuristic | Simple way to expose recent observations | Arbitrary memory horizon; not truly recurrent | High | Partial/noisy observations justified |
| Recurrent PPO/LSTM | Historical proposal | Memory-based POMDP agent | Can integrate history | More variance, tuning and compute; difficult fair comparison | High | Partial observability is central |
| Dreamer/world-model agent | Historical proposal | Learned-model/world-model comparator | Potential adaptation/planning insight | Excessive complexity/compute for simple GridWorld; implementation validity risk | Very high | Only if RQ specifically targets learned world models |
| POMCP | Historical mention | Planning under partial observability | Principled POMDP baseline | Requires model and belief machinery; computationally expensive | High | Explicit small POMDP |
| Oracle/full-state policy | Historical proposal | Upper bound under hidden information or changed rules | Clarifies information cost | Not a deployable peer model; must be labeled upper bound | Low–medium | Partial observability/change-detection analysis |
| ReAct/LLM agent | Historical proposal | Optional exploratory comparator | Language-based reasoning/log interpretability | Weak fit, nondeterminism, API/local-model constraints, cost and reproducibility | High/uncertain | Only if task exposes semantic instructions and literature justifies |
| Rule-based reactive policy | Implied candidate | Simple interpretable baseline | Low cost and predictable | May be handcrafted to scenarios | Low | Useful behavior can be specified without privileged information |

## Provisional minimal comparison ladder

Not a final selection:

1. Random/sanity baseline.
2. Planning or oracle calibration baseline, with explicitly privileged information.
3. One or two validated tabular RL methods for small fully observable GridWorld.
4. One model-based/planning or memory-enabled method only if the uncertainty class makes it scientifically necessary.
5. Neural methods only when environment representation/RQ requires them and pilots prove feasibility.

## Fair-comparison requirements

- Same final evaluation scenarios, disturbance schedules and episode counts.
- Separate model-specific tuning from common final evaluation.
- Comparable budget must be defined by the estimand: environment interactions, wall-clock, planning calls or a reported multi-resource profile.
- Privileged-information baselines clearly labeled.
- Online adaptation permission identical or stratified as a separate experimental regime.
- Training checkpoint selection rule fixed before final evaluation.
- Multiple seeds and independent repetitions.
- Implementation/source/version recorded.
- Failed or unstable methods are reported, not silently removed.

## Final decision record must include

- Research question served.
- Environment assumptions.
- Inclusion and rejected alternatives.
- Expected evidence gain.
- Tuning/search space and budget.
- Hardware benchmark.
- Implementation source/license/version.
- Validation tests.
- Checkpoint/recovery feasibility.
