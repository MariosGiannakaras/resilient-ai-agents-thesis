# Protocol Lifecycle and Evidence Firewall

Protocol stages are explicit: `development`, `tuning`, `pilot`, and `final`. Their scenario partitions must not overlap, and a run is rejected when it requests a scenario outside its assigned stage.

Protocol versions progress from exploratory/pilot versions to a frozen final version. After final freeze, changes to scenarios, information access, model configuration, metrics, seed policy, tuning procedure, budgets, severity definitions, or statistical estimands require a new protocol version or amendment.

Pilot and tuning outputs remain useful for feasibility/protocol design but are never silently relabelled as final thesis evidence.

## Metrics before complex agents

Metric primitives are implemented and tested before model-specific implementations. Recovery thresholds are explicit protocol inputs. If recovery is not observed within the available horizon, recovery time is represented as `None`, not as the final timestep.

The current primitives cover nominal mean, immediate degradation, worst degradation, post-change mean, cumulative loss, and observed recovery step. Their final scientific use remains subject to research/pilot validation.

## Matrix bound

The final matrix remains intentionally small: a few scientifically distinct agent roles, one primary GridWorld family, a primary persistent-change axis, limited supporting robustness diagnostics, justified severities, and enough seeds for reliable estimates. Algorithm count is not a success criterion.
