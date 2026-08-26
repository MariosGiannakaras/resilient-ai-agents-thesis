# GridWorld Prototype Comparison

**Status:** Completed evidence for `T-210`; implementation selection remains the `T-211` ADR.
**Comparison date:** 2026-08-26
**Validated source:** `a22508dc3c78fd1af0729737234b31736dc1e87b` (clean working tree)

## Scope

Two deliberately bounded candidates implement the same explicit fixture and expose the same accepted `ResearchEnvironment` and `GroundTruthTransition` contracts:

1. a small project-owned `gymnasium.Env` mechanics layer;
2. a MiniGrid mechanics adaptation with project-owned translation around MiniGrid's orientation, mission, observation, action, and reward conventions.

The prototypes are feasibility evidence only. Their fixture seeds and benchmark are not experiment evidence and do not freeze scientific GridWorld parameters.

## Semantic and validation comparison

| Criterion | Project-owned Gymnasium mechanics | MiniGrid adaptation | Result |
|---|---|---|---|
| Four-neighbor state/action semantics | Expressed directly in 28 candidate-owned source lines. | Requires 60 candidate-owned source lines and bypasses/translates MiniGrid orientation, mission, object encoding, seven-action, and reward conventions. | Both match the fixture; custom is more direct. |
| Accepted project contracts | Uses the common adapter and evaluator ground-truth record. | Uses the same adapter and record. | Equivalent external contract. |
| Determinism and seeding | Explicit action and observation RNG channels; reset fails without them. | Same project-owned channels; MiniGrid reset is contained behind the adapter. | Equivalent under tests. |
| Persistent change and disturbances | Exact-step persistent action remap, action-execution failure, and observation corruption are explicit. | Same behavior is supplied by project-owned adaptation rather than MiniGrid's native research semantics. | Equivalent output; no reuse advantage. |
| Information boundary | True state, delivered observation, intended action, and executed action remain distinct. | Same boundary because project code owns it. | Equivalent under tests. |
| Termination and truncation | Explicit and independently tested. | Translated to the same explicit contract. | Equivalent under tests. |
| Testability | Direct mechanics support hand-checkable traces. | Parity is testable but additionally depends on the translation layer. | Custom has the smaller reasoning surface. |
| Disturbance extensibility | New thesis mechanisms can remain named project-owned transitions/processes. | The same extensions still require project code and may interact with inherited MiniGrid conventions. | Custom is clearer for the RQ. |

Nine deterministic tests passed on native Windows CPython 3.12.13 for exact change onset, replay and RNG isolation, intended/executed action separation, observation isolation, boundary/obstacle collisions, goal termination versus truncation, serialization, debug/trace parity, and fail-closed reset seeding.

## Dependency, maintenance, and licensing audit

The locked custom candidate uses Gymnasium 1.3.0 and its normal runtime dependencies. The MiniGrid candidate additionally introduces MiniGrid 3.1.0 and Pygame, while its relevant thesis semantics still reside in project code.

Both tagged packages imported and passed the prototype suite on the accepted native Windows baseline. MiniGrid's documentation does not treat Windows as an officially supported platform, so this successful local prototype does not remove the upstream support risk.

Gymnasium 1.3.0 declares MIT consistently in its tagged project metadata and license. MiniGrid 3.1.0 has a material tag-level licensing inconsistency: its `pyproject.toml` declares MIT, while the tagged root `LICENSE` identifies Apache License 2.0 and appears malformed/truncated. The prototype copies no MiniGrid source, but the inconsistency increases dependency/reuse risk and must not be silently resolved by assumption.

Authoritative technical artifacts checked for the pinned tags:

- [Gymnasium 1.3.0 project metadata](https://github.com/Farama-Foundation/Gymnasium/blob/v1.3.0/pyproject.toml) and [license](https://github.com/Farama-Foundation/Gymnasium/blob/v1.3.0/LICENSE);
- [MiniGrid 3.1.0 project metadata](https://github.com/Farama-Foundation/Minigrid/blob/v3.1.0/pyproject.toml) and [root license](https://github.com/Farama-Foundation/Minigrid/blob/v3.1.0/LICENSE).

## Native target-machine feasibility result

The clean-source command was:

```text
uv run --locked --group gridworld-prototype python -m prototypes.gridworld.compare --episodes 1000 --repeats 5
```

Each repeat executed 4,000 transitions on the fixed test fixture. Median time was 26,621.2 ns/transition for the custom candidate and 264,943.6 ns/transition for the MiniGrid adaptation (minimum/maximum: 26,514.1/27,127.6 and 264,501.0/265,725.8 respectively). This small engineering smoke benchmark demonstrates adequate headless feasibility for both candidates; it is neither a scientific performance result nor the sole selection criterion.

The benchmark recorded Windows 10, AMD64, CPython 3.12.13, Gymnasium 1.3.0, MiniGrid 3.1.0, a clean source tree, and fixture SHA-256 `4b118e8b6f28900af30351462c7f92ca27b202df2d58e1f7e511c9ea6ffc3e2f`.

## Evidence available to the ADR

Both candidates can satisfy the accepted external contract. The project-owned Gymnasium mechanics are smaller, faster in this bounded smoke check, semantically direct, and avoid MiniGrid's extra dependency/support/license uncertainty. The MiniGrid adaptation supplies no demonstrated scientific capability that the retained RQ needs and still requires project-owned code to neutralize inherited semantics.

This comparison does not itself select the implementation. `T-211` applies the accepted simplicity-under-scientific-equivalence rule, records consequences and reopening conditions, and is the formal selection gate.
