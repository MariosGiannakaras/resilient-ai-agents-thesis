# Related-Work Evidence Matrix

**Status:** Initial verified research seed, not a final literature review and not a model/metric decision.

**Last search:** 2026-07-29

## Purpose

This file records closely related primary studies and the specific evidence they provide for the thesis. It must be refreshed before protocol freeze, before drafting Related Work/Methodology/Discussion, and shortly before submission.

Do not cite a row from this matrix without reading and checking the full paper. Abstract-level evidence is marked accordingly.

## Core directly related studies

| ID | Study | Setting and method | Reported result | Relevance to this thesis | Limits / status |
|---|---|---|---|---|---|
| RW-001 | Balloch et al. (2022), *NovGrid: A Flexible Grid World for Evaluating Agent Response to Novelty* | MiniGrid-based novelty injection framework. Defines object/action novelties and barrier/delta/shortcut effects. Provides resilience, asymptotic adaptive performance, adaptive efficiency and one-shot adaptive performance metrics. | PPO baseline on a 6×6 DoorKeyChange task showed a sharp post-novelty drop; reported resilience 0.0531, one-shot performance 0.22, recovery/convergence around 300k post-change steps and lower post-change asymptotic reward around 0.8. | Closest methodological analogue. Supports explicit change injection, pre/post performance curves and separate degradation/recovery outcomes. | Benchmark/tool paper with one illustrative baseline; do not copy its full ontology or large training budget automatically. Open preprint: `https://arxiv.org/abs/2203.12117` |
| RW-002 | Luo et al. (2022), *Adapt to Environment Sudden Changes by Learning a Context Sensitive Policy* | Context-based meta-RL with variance minimization, context-separation objective and history-truncated RNN. Evaluated in one grid-world and five changing locomotion tasks. | Authors report better context recovery and approximately 10× faster post-change adaptation in the grid-world while maintaining or improving return versus selected meta-RL baselines. | Demonstrates that recovery speed after abrupt transition changes is a legitimate primary outcome and that recent interaction history can matter. | Method is substantially more complex than likely needed for this thesis; useful as high-complexity reference, not an automatic candidate. Peer-reviewed AAAI 2022: `https://doi.org/10.1609/aaai.v36i7.20730` |
| RW-003 | Leike et al. (2017), *AI Safety Gridworlds* | Suite of small GridWorlds isolating safety/robustness problems, including distributional shift and adversaries. Uses observed reward plus a separate hidden performance function for evaluation. | A2C and Rainbow did not solve the suite satisfactorily; the authors specifically report poor generalization in the distributional-shift environment. | Supports using small controlled environments to isolate one failure mode and separating the agent objective from independent evaluation where justified. | Focus is AI safety/specification rather than recovery dynamics. Hidden performance function is optional, not required by the thesis. Open preprint: `https://arxiv.org/abs/1711.09883` |
| RW-004 | Sutton (1990), *Integrated Modeling and Control Based on Reinforcement Learning and Dynamic Programming* | Dyna architectures combine direct RL, learned world models and planning. Navigation examples include changing environments. | The paper reports that Dyna-Q architectures can be adapted easily for changing environments and that planning with a learned model accelerates navigation learning. | Establishes a classic low-complexity model-based comparison category for dynamic GridWorlds. | Historical foundational evidence; exact modern implementation and fairness policy still require fresh selection and testing. NeurIPS paper: `https://papers.nips.cc/paper/1990/hash/d9fc5b73a8d78fad3d6dffe419384e70-Abstract.html` |
| RW-005 | Steinparz et al. (2022), *Reactive Exploration to Cope With Non-Stationarity in Lifelong Reinforcement Learning* | Reactive exploration for continual domain shifts in lifelong RL; compares exploration strategies and algorithm families. | Authors report policy-gradient methods adapted faster to distribution shifts than Q-learning and benefited most from reactive exploration. | Warns that adaptation ranking may depend on algorithm family and exploration behavior; motivates measuring both final performance and adaptation path. | Lifelong continuous shifts are broader than the planned bounded abrupt-change setting. PMLR: `https://proceedings.mlr.press/v199/steinparz22a.html` |
| RW-006 | Benjamins et al. (2021), *CARL: A Benchmark for Contextual and Adaptive Reinforcement Learning* | Controlled context variables alter goals/dynamics across established RL environments; benchmark targets generalization and adaptation. | Even simple toy environments became challenging across contextual instances; authors report initial evidence that separating state representation learning from context-conditioned policy learning improves generalization. | Supports explicit, versioned context parameters and controlled variation rather than many unrelated environments. | Not centered on GridWorld novelty recovery and published as a NeurIPS workshop paper. Open preprint: `https://arxiv.org/abs/2110.02102` |
| RW-007 | de la Rosa, Dusparic and Cardozo (2025/2026), *Adapting the Behavior of Reinforcement Learning Agents to Changing Action Spaces and Reward Functions* | MORPHIN combines concept-drift detection with dynamic learning/exploration adjustment and preserves prior Q-learning knowledge. Gridworld plus traffic-signal simulation. | Authors report continuous adaptation and up to 1.7× improved learning efficiency over standard Q-learning. | Recent direct analogue for rule/reward/action changes and a simple tabular adaptive baseline category. | Short IEEE ACSOS Companion paper; recent and less established than foundational work. Treat as emerging evidence. Open author preprint: `https://arxiv.org/abs/2601.20714` |

## Supporting theoretical studies

| ID | Study | Contribution | Use in the thesis | Limit |
|---|---|---|---|---|
| RW-008 | Cheung, Simchi-Levi and Zhu (2020), *Reinforcement Learning for Non-Stationary Markov Decision Processes: The Blessing of (More) Optimism* | Formalizes drifting reward/transition changes with variation budgets and proposes sliding-window/parameter-free algorithms with dynamic-regret guarantees. | Vocabulary and theory for non-stationarity, variation and adaptive windows. | Theory-heavy; not a direct GridWorld empirical template. `https://proceedings.mlr.press/v119/cheung20a.html` |
| RW-009 | Wei and Luo (2021), *Non-stationary Reinforcement Learning without Prior Knowledge: an Optimal Black-box Approach* | Black-box reduction for optimal dynamic regret without prior knowledge of change count/amount. | Supports careful distinction between stationary return and adaptation under changing MDPs. | Not a practical small-thesis implementation target. `https://proceedings.mlr.press/v134/wei21b.html` |

## Preliminary synthesis — implications, not decisions

The literature supports the following design principles:

1. **Small controlled GridWorlds are scientifically legitimate** when each environment/change isolates a defined robustness or adaptation question.
2. **Abrupt change should have an explicit injection point** so pre-change performance, immediate degradation, recovery path and post-change performance can be measured.
3. **A single final score is insufficient.** Comparable work separates immediate resilience, adaptation efficiency/recovery speed and asymptotic post-change performance.
4. **Model diversity should be conceptual, not numerical.** A minimal comparison may include a standard model-free baseline, a model-based or explicitly adaptive category and, only if justified by state representation/hardware, one function-approximation baseline.
5. **The uncertainty taxonomy should remain bounded.** NovGrid demonstrates many novelty types, but this thesis should select only the few that map directly to the official examples and research question.
6. **Algorithm complexity is not automatically scientific value.** ESCP and non-stationary regret algorithms establish upper-end references; they do not require reproduction in a bounded undergraduate thesis.
7. **Report distributions and repeated runs.** Adaptation trajectories can be noisy and algorithm rankings can depend on exploration and change type.

## Candidate evidence gaps for the first Codex mission

- Find peer-reviewed empirical comparisons using simple tabular agents under action failure/slip, observation corruption and abrupt rule/goal changes.
- Verify whether NovGrid code remains maintained and compatible with current Gymnasium/MiniGrid before considering it technically.
- Find validated operational definitions for recovery time, cumulative post-change loss, resilience and post-change asymptote.
- Check whether a small model set can answer the official topic without deep/meta-RL.
- Identify recent theses or dissertations with a comparable theory–experiment–dashboard structure; use them only as structural examples, not as authoritative methods.

## Required refresh during writing

Before writing Related Work, Methodology or Discussion:

- rerun focused searches with current dates,
- read full text of all decision-driving sources,
- add exact experimental details, sample counts/seeds and limitations,
- verify every DOI and publication status,
- distinguish peer-reviewed sources, workshop papers, preprints and software/benchmark papers,
- connect each thesis claim to a source or to the project’s own frozen evidence.