# GridWorld Landscape Review

**Status:** Technical pre-screen and bounded comparison complete; DEC-032 selects the project-owned Gymnasium strategy.
**Review date:** 2026-08-03  
**Scope:** current technical candidates for the controlled uncertainty/resilience environment required by the thesis.

## Purpose

This review narrows the implementation space before any prototype or ADR. It evaluates current environment frameworks against the requirements already defined in `GRIDWORLD_SPEC.md`: explicit mechanics, deterministic seeding, controlled uncertainty and scheduled change, clean `terminated`/`truncated` semantics, headless execution, traceability, testability, and bounded implementation cost.

This is a **technical landscape review**, not the final scientific environment decision. The imported `ThesisBibliography` evidence must still be mapped to the final uncertainty taxonomy and benchmark design after the first controlled bibliography synchronization succeeds.

## Sources checked

Authoritative/current technical sources checked on 2026-08-03:

- Gymnasium documentation: https://gymnasium.farama.org/
- Gymnasium repository and releases: https://github.com/Farama-Foundation/Gymnasium
- MiniGrid documentation: https://minigrid.farama.org/
- MiniGrid repository, release notes, and root license: https://github.com/Farama-Foundation/Minigrid
- Griddly repository and documentation: https://github.com/Bam4d/Griddly and https://griddly.readthedocs.io/
- Griddly PyPI release history: https://pypi.org/project/griddly/

Versions and maintenance status must be rechecked immediately before dependency pinning.

## Candidate summary

| Candidate | Current evidence | Fit for this thesis | Main risk | Pre-screen result |
|---|---|---|---|---|
| Project-owned custom `gymnasium.Env` | Gymnasium 1.3.0 is current in 2026; official API supports explicit spaces, `terminated`/`truncated`, environment-owned RNG and deterministic `reset(seed=...)`; official custom-environment guidance exists. | Very high control over exact state/action/reward/change semantics and trace schema; minimal hidden behavior; naturally CPU-friendly. | We own all environment invariants and must test them thoroughly. | **Prototype A — retain** |
| MiniGrid 3.1.x + thin project wrappers/subclass | MiniGrid 3.1.0 released 2026-05-11; active Farama project; Gymnasium API; wrappers include stochastic actions, observation transforms, full/partial observability and reseeding; dynamic-obstacle environments exist. The v3.1.0 project metadata declares MIT while its root license identifies Apache-2.0 and appears malformed/truncated. | Strong ready-made grid mechanics and rendering; usable as the strongest bounded reuse candidate. | Built-in orientation, mission strings, object encoding and broader action semantics require translation/bypass for the accepted thesis contract; mid-episode changes remain project code; Windows is not an officially supported upstream platform; tagged license evidence conflicts. | **Prototype B — completed** |
| Gymnasium FrozenLake / CliffWalking reused directly | Maintained Toy Text environments with small discrete spaces; FrozenLake supports custom maps, configurable slipperiness/success probability and reward schedule; CliffWalking has simple known semantics. | Excellent known-behavior fixtures and smoke-test references for tabular agents and stochastic actions. | Too narrow as the final environment: not designed around scheduled dynamic rule/topology changes, observation corruption, multiple disturbance mechanisms, or explicit recovery-event traces. | **Reference fixtures only** |
| Griddly 1.6.x | Flexible YAML/GDY game definition, stochastic mechanics, configurable partial observability, event history, fast C++ engine; MIT license. Public release line is from 2023. Native development involves C++/CMake/Conan and Vulkan-related dependencies. | Technically expressive enough for complex grid research. | Much larger engine/dependency surface than the thesis requires; maintenance/release recency is weaker; more build/platform risk and more hidden engine semantics to validate. | **Do not prototype unless a later requirement demands it** |

## Candidate A: minimal project-owned Gymnasium environment

### Why it remains a strong candidate

Gymnasium provides the interface contract without forcing a specific GridWorld design. The current API gives us:

- explicit `observation_space` and `action_space`,
- separate `terminated` and `truncated` outputs,
- environment-owned `np_random`, initialized correctly through `super().reset(seed=seed)`,
- environment checking utilities,
- wrappers when a transformation genuinely belongs outside the base environment,
- a stable single-agent ecosystem and familiar integration surface for RL implementations.

A custom environment therefore does **not** mean inventing an RL API. It means implementing only the small grid mechanics and disturbance state machine that are specific to this thesis on top of the current Gymnasium contract.

### Expected advantages

- The nominal transition function can remain small enough to inspect manually.
- Observation noise, action failure and rule/topology changes can be represented as explicit named mechanisms instead of inferred through framework behavior.
- Change onset, duration and severity can be stored as first-class scenario configuration.
- The environment can emit exact disturbance/change events in `info` and the project trace schema.
- Fully observable tabular state can coexist with derived partial/noisy observation views without changing the underlying ground-truth state.
- Serialization and checksums can cover the exact environment/scenario definition used by each run.
- Tests can use hand-calculated trajectories and returns.

### Main cost

The project must own and test collision semantics, reachability checks where needed, transition stochasticity, reward/termination logic, RNG separation and scenario scheduling. This is acceptable only if the final GridWorld remains intentionally small.

## Candidate B: MiniGrid with thin extensions

### Current strengths

MiniGrid is a current Farama project designed specifically for lightweight configurable grid-world RL. The 3.1.0 release on 2026-05-11 added current Python support and maintenance fixes. Its documented wrappers already cover several mechanisms relevant to the thesis:

- `StochasticActionWrapper` for action stochasticity,
- `ObservationWrapper` as an extension point for observation corruption/transformation,
- `FullyObsWrapper`, `SymbolicObsWrapper`, and partial-view wrappers for observability choices,
- `ReseedWrapper` for controlled environment regeneration,
- configurable view sizes,
- built-in dynamic-obstacle environments.

MiniGrid also provides rendering and a known external research codebase, reducing the amount of low-level environment/UI work.

### Main concerns for this thesis

MiniGrid's defaults are not neutral with respect to the research design:

- the agent has orientation and turn/forward semantics,
- many environments expose a seven-action family even when some actions are unused,
- observations include a compact object-state encoding plus mission/direction fields,
- default observation is partially observable,
- built-in reward shaping/episode conventions differ across tasks.

Those features are useful research features in MiniGrid, but they can become confounders if the thesis only needs a four-direction controlled decision process with explicit disturbances. We should not inherit them merely because they are already implemented.

A MiniGrid solution is acceptable only if the prototype shows that project-owned changes remain thin, testable, and semantically transparent.

## Reference candidates: FrozenLake and CliffWalking

Gymnasium's Toy Text environments are deliberately small and suitable for debugging RL implementations. They are useful here as **known-behavior fixtures**:

- FrozenLake provides a discrete grid and configurable stochastic action success through `is_slippery` / `success_rate`.
- CliffWalking provides deterministic movement, explicit large failure penalty, and simple terminal semantics.

They can be used to validate tabular-agent implementations, seeding expectations, metric code and environment adapters. They should not define the final research environment because the thesis needs scheduled environmental change and multiple distinct uncertainty mechanisms whose timing and ground-truth state must be recorded explicitly.

## Rejected at this stage: Griddly

Griddly is expressive and technically capable. It supports a YAML-based game description language, stochastic mechanics, partial observability, event history, rendering and a high-performance native engine.

For this thesis, those strengths do not currently outweigh the additional surface area:

- C++/Python codebase rather than a small pure-Python environment,
- CMake/Conan/native build concerns for development,
- Vulkan-related rendering/development dependencies,
- public release line last updated in 2023,
- substantially more engine behavior to understand and validate than the proposed controlled GridWorld requires.

Griddly should be reconsidered only if the frozen research design later demands capabilities that cannot be represented cleanly in a small Gymnasium/MiniGrid implementation.

## Prototype gate

No third-party environment code should be integrated into the thesis core before a bounded prototype comparison.

### Prototype A — custom Gymnasium

Implement the smallest possible environment skeleton sufficient to test:

1. deterministic nominal four-neighbor motion,
2. seeded probabilistic action failure/slip,
3. deterministic scheduled rule or transition change at an exact step,
4. deterministic seeded observation corruption as a separate observation process,
5. goal termination versus time-limit truncation,
6. ground-truth event/trace output,
7. scenario serialization and replay.

### Prototype B — MiniGrid adaptation

Implement the same externally observable test cases with the thinnest possible MiniGrid subclass/wrapper stack. Do not add model training or dashboard work.

### Required comparison tests

Both prototypes must run the same conceptual fixtures:

- fixed seed produces identical episode trace,
- different disturbance seed can change only the intended stochastic stream,
- action-failure event occurs at the expected probability mechanism without silently changing the nominal action definition,
- scheduled change occurs on the exact configured step,
- observation corruption does not mutate the hidden ground-truth state,
- terminal goal and time-limit truncation are distinguishable,
- serialized scenario reproduces the same resolved configuration,
- renderer/debug view agrees with recorded state,
- headless smoke benchmark is adequate for repeated local experiments.

## Selection rule after prototype

The default decision rule is simplicity under scientific equivalence:

1. Prefer MiniGrid only if the required experimental semantics can be expressed with a thin, explicit wrapper/subclass layer and parity tests without inheriting unwanted observation/action/reward semantics.
2. Prefer a project-owned Gymnasium environment if it produces clearer disturbance semantics, easier known-answer tests and a smaller total code/dependency surface.
3. Do not choose on rendering quality or number of built-in environments; the final dashboard can render the project state independently.
4. Do not select Griddly unless a frozen scientific requirement makes its engine capabilities necessary.

## Current proposal

**Prototype order:** custom Gymnasium first, MiniGrid second.

This ordering is not a final selection. It reflects current technical evidence: a minimal Gymnasium environment appears most likely to match the thesis requirement for a deliberately small, explicit, reproducible dynamic GridWorld, while MiniGrid remains the strongest maintained reuse/adaptation alternative.

## Prototype outcome and remaining ADR gate

The controlled bibliography baseline, construct-level research framing, accepted native-Windows inventory, bounded implementations, deterministic parity suite, and clean-source headless benchmark are complete. `GRIDWORLD_PROTOTYPE_COMPARISON.md` records the measured result and the MiniGrid tag-level license conflict.

DEC-032 applies the selection rule and chooses the small project-owned Gymnasium path. `T-212` promotes locked Gymnasium 1.3.0 to the core runtime and implements schema v1; MiniGrid and Pygame remain confined to the reproducible prototype dependency group.
