# Pilot Protocol v0.2 Amendment

**Protocol identity:** `pilot-v0.2`

**Lifecycle state:** pilot-unfrozen amendment; diagnostic evidence only
**Machine-readable authority:** `configs/protocols/pilot-v0.2.json`

## Trigger and preserved evidence

The real `pilot-v0.1` campaign completed all 36 F0-only tuning runs and began its fixed pilot matrix. `PV01-PILOT-L01-C06` then failed under `observation-corruption-1of8`: R0 received an active delivered observation equal to the modeled goal while evaluator truth correctly showed that the episode had not terminated. R0 rejected the observation as terminal and could not act. The failed bundle and the five earlier completed pilot attempts remain finalized, indexed, and published under their original identities.

This is a confirmed implementation/information-boundary defect, not poor resilience or non-recovery. Treating the delivered observation as proof of true termination would leak evaluator truth. `pilot-v0.2` therefore makes one bounded amendment: while the runner requests an action in an active episode, a terminal-like R0 observation assigns the absorbing value zero to every action and applies the existing seeded tie rule. Robust-plan schema v2 records `active_terminal_observation_policy=zero-value-seeded-action-tie`.

## Amendment boundaries

- All GridWorld layouts, conditions, severities, budgets, metric definitions, resources, stopping rules, and the R0 uncertainty set remain unchanged.
- The 36 completed `pilot-v0.1` tuning runs are reused because they execute F0 only; the R0 defect cannot affect their selection evidence.
- The selected Q configuration is recomputed from those immutable tuning bundles through the same semantic reproduction and predeclared score.
- The complete 14-run pilot matrix is rerun under `PV02-*` identities so every included pilot unit uses one consistent fixed agent implementation.
- The eight pilot root seeds are deliberately retained for a paired implementation retry. This is diagnostic pilot evidence, not a new search over seeds or final evidence.
- Earlier `PV01-PILOT-*` attempts are listed as superseded in campaign state, never deleted or relabeled.
- `PV02-PILOT-ANALYSIS` consumes only the complete amended matrix. The v0.1 failure remains explicit operational evidence in the pilot report.

The compact machine-readable v0.2 file is a validated bounded overlay on the full v0.1 protocol. Loading expands it to a complete self-contained resolved protocol before validation and persistence in every run bundle.
