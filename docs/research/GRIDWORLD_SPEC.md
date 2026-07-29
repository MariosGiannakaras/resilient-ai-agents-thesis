# GridWorld Specification

**Status:** Incomplete; this file separates confirmed requirements from historical candidates. No missing rule is invented.

## Confirmed purpose

The environment must be a simple, controlled simulation for comparing decision agents under uncertainty and dynamic change. It must support repeatable episodes, explicit disturbance parameters, trace capture and independent execution without the dashboard.

## Specification status table

| Element | Status | Current knowledge |
|---|---|---|
| State representation | OPEN | Must be explicit and versioned; full vs partial observability unresolved. |
| Action set | PROVISIONAL | Historical discussions assume cardinal movement; exact actions and no-op behavior not confirmed. |
| Transition model | OPEN | Must define boundaries, obstacles and failed/slipped actions precisely. |
| Reward function | OPEN | Goal reward, step cost, collision/invalid-action penalty and change behavior are not final. |
| Obstacles | CONFIRMED AT CONCEPT LEVEL | GridWorld is expected to contain obstacles; static/dynamic behavior not final. |
| Goal | CONFIRMED AT CONCEPT LEVEL | Agent navigates toward a task goal; placement and relocation rules open. |
| Episode termination | OPEN | Goal, max steps and unrecoverable states must be specified. |
| Randomness | CONFIRMED REQUIREMENT | Every stochastic mechanism needs seeded RNG and logged resolved parameters. |
| Grid configurations | CONFIRMED REQUIREMENT | Multiple layouts/configurations are expected for robustness/generalization. |
| Dynamic changes | CONFIRMED REQUIREMENT | Rule/environment changes must be representable and scheduled. |
| Observation noise | OFFICIAL EXAMPLE | Exact channel, distribution and severity open. |
| Action execution failure | OFFICIAL EXAMPLE | Exact failure/slip model open. |
| Partial observability | HISTORICAL CANDIDATE | Not confirmed. |
| Online adaptation after disruption | OPEN | Must be defined per evaluation regime and agent capability. |

## Required base-environment decisions

Before implementation/freeze, specify:

1. Grid dimensions and coordinate convention.
2. Start and goal distributions or fixed sets.
3. Obstacle representation and collision semantics.
4. Action set and deterministic nominal transition.
5. Reward/penalty values and scaling.
6. Maximum episode steps and all terminal/truncated conditions.
7. Observation schema and encoding.
8. Reset behavior.
9. RNG ownership and seeding.
10. Serialization/version identifier.
11. Render/trace schema independent of UI.
12. Validation examples with expected trajectories and returns.

## Candidate uncertainty taxonomy

These are candidates, not a final factorial design.

### U1 — Action uncertainty
- Intended action replaced, dropped, delayed or converted to no-op.
- Candidate parameters: failure probability, slip distribution, burst length, onset.
- Must distinguish stochastic transitions from software execution failure.

### U2 — Observation/data noise
- Corruption, missingness, delayed observation or position ambiguity.
- Candidate parameters: noise rate/distribution, affected fields, persistence.
- Only appropriate if observation semantics support it.

### U3 — Dynamic topology
- Obstacles appear/disappear/move or passages become blocked.
- Candidate parameters: change time, number/location, reversibility.
- Requires reachability validation to avoid accidental impossible tasks unless impossibility is intentional and labeled.

### U4 — Rule/reward changes
- Goal, costs, penalties or transition rules change.
- Candidate parameters: changed component, magnitude, onset/duration.
- Must avoid changing reward scale in a way that makes raw return comparisons meaningless without normalization.

### U5 — Goal relocation or task change
- Goal changes after learning or during an episode.
- Candidate parameters: relocation policy, notice/observation, frequency.
- Research value must be justified separately from generic non-stationarity.

### U6 — Partial observability
- Limited field of view, hidden map features or aliased states.
- Introduces POMDP requirements and may justify memory-based agents.
- Must not be added solely to justify a preferred model.

### U7 — Compound disturbance
- Multiple single factors combined.
- Consider only after single-factor effects are understood and compute budget is feasible.

## Existing implementation evidence

### User-owned source
- No dedicated GridWorld repository was found among the accessible user-owned repositories during bootstrap.
- The exact local or remote source remains `OQ-SRC-001`.

### Historical local scaffold
- Conversation exports refer to a local `THESISnew` project and generated components.
- The code is unavailable for audit.
- Historical descriptions mention proxy/placeholder outputs; nothing from it is accepted as scientifically valid without recovery and tests.

### Public candidate/reference
- `https://github.com/prasenjit52282/GridWorld`
- Historical discussions referenced a repository consistent with this project.
- Its README describes custom ASCII grids, agent/goal/holes/walls, stochastic slip behavior and RL examples.
- It is a third-party reference only until identity, license, commit and suitability are audited.
- No code has been copied into this repository.

## Known risks and likely bugs to test

- Off-by-one coordinates or inconsistent row/column ordering.
- Boundary/obstacle behavior differing between transition model and rendered state.
- Multiple RNGs not seeded from the run seed.
- Goal/terminal reward applied twice or omitted.
- `terminated` vs `truncated` confusion.
- Dynamic changes creating unreachable goals without explicit labeling.
- Observation showing information that an intended partially observable agent should not receive.
- Reward-scale changes invalidating cross-condition return comparison.
- State mutation leaking between episodes.
- Evaluation agents learning when protocol says frozen, or not learning when adaptation is intended.
- Visualization running different logic from the environment.

## Required validation examples

1. **Nominal deterministic trace:** fixed 3×3 or similarly minimal grid with hand-calculated states/rewards.
2. **Boundary case:** attempted movement outside grid.
3. **Obstacle case:** collision/blocked transition semantics.
4. **Goal termination:** exact final reward and terminal flag.
5. **Step-limit truncation:** exact number of transitions.
6. **Action-failure seed replay:** same seed reproduces failure sequence.
7. **Dynamic-change event:** rule/topology changes at exact scheduled step.
8. **Serialization round trip:** config produces same resolved environment.
9. **Reachability check:** valid configurations have intended solvability status.
10. **Trace/UI parity:** rendered frames correspond to recorded states, not a separate simulator.
