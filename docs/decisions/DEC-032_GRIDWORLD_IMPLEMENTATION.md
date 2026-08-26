# DEC-032 — Project-Owned Gymnasium GridWorld Implementation

- **Date:** 2026-08-26
- **Status:** Accepted
- **Decision owners:** Implementation team under the evidence-backed autonomous decision boundary
- **Related requirements:** REQ-RES-002, REQ-RES-008, REQ-ARCH-005, REQ-TEST-001
- **Related research questions:** Provisional main RQ and secondary questions in `docs/research/RESEARCH_BRIEF.md`

## Context

The thesis needs a small, controlled GridWorld whose evaluator truth, agent-visible observation, intended/executed actions, persistent change, disturbance streams, termination, and traces are explicit and reproducible. DEC-023 already fixes the shared research contracts, and DEC-031 fixes native Windows CPython 3.12 with CPU execution as the supported baseline.

`T-210` compared a project-owned `gymnasium.Env` mechanics layer and a MiniGrid adaptation against the same fixed fixture and accepted adapter. Both passed the same nine deterministic parity/invariant tests and were feasible on the target machine. The comparison is recorded in `docs/research/GRIDWORLD_PROTOTYPE_COMPARISON.md`.

## Decision

Implement the thesis GridWorld as a small project-owned environment using the locked Gymnasium 1.3.0 API in `src/resilient_agents/`, together with the existing project environment, information, randomness, configuration, and trace contracts. Later Gymnasium upgrades require the normal locked dependency validation but do not reopen the strategy decision unless semantics or compatibility change materially.

Gymnasium supplies the maintained environment API, spaces, seeding integration, and `terminated`/`truncated` convention. The project owns the scientific state/action/reward/change/disturbance/observation semantics and validates them with hand-checkable reference traces. MiniGrid is not a core dependency.

This selects the implementation strategy only. It does not freeze grid dimensions, layouts, rewards, horizons, severities, changepoints, scenario partitions, seeds, repetitions, metrics, agents, or protocol values.

## Evidence and assumptions

- **Verified technical sources:** pinned Gymnasium 1.3.0 metadata/license and API guidance; pinned MiniGrid 3.1.0 metadata/license and platform guidance, as linked from the comparison.
- **Prototype evidence:** identical external contract and fixture behavior for both candidates; nine deterministic native-Windows tests passed.
- **Measured feasibility:** clean-source benchmark at `a22508d` completed five repeats of 4,000 transitions per candidate; both were adequate, while the project-owned mechanics had the smaller/faster measured surface.
- **Implementation surface:** 28 candidate-owned source lines for custom mechanics versus 60 for the MiniGrid translation, excluding their shared 238-line feasibility harness.
- **Dependency/licensing evidence:** MiniGrid additionally brings Pygame, is not officially supported on Windows, and its v3.1.0 tag has conflicting MIT project metadata versus a malformed/truncated root Apache-2.0 license artifact.
- **Assumption:** the final bounded research design continues to require transparent four-neighbor controlled mechanics rather than MiniGrid-native orientation, mission, object, or partial-view semantics.
- **Open uncertainties:** scientific environment parameters remain subject to `T-212`/`T-213`, metrics/agent work, and pilots.

## Alternatives considered

### MiniGrid adaptation

- **Benefits:** maintained grid-focused ecosystem, built-in rendering, objects, partial views, wrappers, and existing environments.
- **Costs/risks:** the accepted four-neighbor contract requires translation or bypass of its orientation, mission, object encoding, action, observation, and reward conventions; thesis disturbances still remain project code; it adds Pygame plus upstream Windows-support and tag-license uncertainty.
- **Reason rejected:** it demonstrated no required RQ capability advantage and increased the semantic/dependency surface under the accepted simplicity-under-scientific-equivalence rule.

### Direct reuse of Gymnasium Toy Text environments

- **Benefits:** maintained, tiny, known-behavior reference environments.
- **Costs/risks:** their fixed task semantics do not natively represent explicit scheduled persistent changes, separate observation/action disturbance processes, or the required ground-truth trace contract.
- **Reason rejected:** retain as optional agent/metric reference fixtures, not the final research environment.

### Griddly or another larger engine

- **Benefits:** expressive game definition and rendering capabilities.
- **Costs/risks:** unnecessary native/build/rendering surface and more inherited behavior than the bounded thesis requires.
- **Reason rejected:** no accepted scientific requirement justifies the additional complexity.

## Consequences

### Positive

- Scientific mechanics remain directly inspectable and independently testable.
- The environment uses a standard maintained API without inheriting unrelated MiniGrid semantics.
- Independent RNG and evaluator/agent information boundaries stay project-controlled.
- The core dependency surface remains smaller and avoids the identified MiniGrid risks.
- Dashboard rendering can remain a trace consumer and cannot alter experiments.

### Negative / trade-offs

- The project must implement and maintain collision, reachability where required, transition, reward, termination, change, disturbance, serialization, and rendering/trace-parity invariants.
- Built-in MiniGrid layouts, objects, wrappers, and rendering are not available automatically.

### Follow-up actions

- `T-212`: implement the selected environment in `src/resilient_agents/`, promote only Gymnasium to the justified core runtime dependencies, and remove prototype-only MiniGrid/Pygame dependency use from the production path.
- `T-213`: validate reference traces, deterministic replay, disturbance isolation, termination/truncation, serialization, state isolation, and information non-leakage.
- Keep Toy Text environments optional and test-only if later agent/metric validation benefits from them.

## Validation / review trigger

Validate this decision through `T-212`/`T-213` known-answer and invariant tests and later pilot feasibility. Reopen only if:

1. an accepted scientific requirement needs orientation, object interaction, formal partial views, or another capability that a maintained reuse candidate supplies more transparently;
2. the project-owned mechanics cannot meet deterministic reference-trace, information-isolation, or performance requirements without disproportionate complexity;
3. Gymnasium 1.3 compatibility becomes unmaintainable on the accepted runtime; or
4. the target runtime materially changes and invalidates the dependency/feasibility evidence.

Resolution of MiniGrid's license inconsistency alone is not a reopening reason unless MiniGrid also gains a demonstrated scientific or maintenance advantage.

## Supersedes / superseded by

- Implements the final selection gate required by DEC-010; does not supersede DEC-023 or DEC-031.
- No superseding decision.
