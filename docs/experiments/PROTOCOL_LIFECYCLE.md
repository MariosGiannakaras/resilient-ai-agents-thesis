# Protocol Lifecycle and Evidence Firewall

Protocol stages are explicit: `development`, `tuning`, `pilot`, and `final`. Their scenario partitions must not overlap, and a run is rejected when it requests a scenario outside its assigned stage.

Protocol versions progress from exploratory/pilot versions to a frozen final version. After final freeze, changes to scenarios, information access, model configuration, metrics, seed policy, tuning procedure, budgets, severity definitions, or statistical estimands require a new protocol version or amendment.

Pilot and tuning outputs remain useful for feasibility/protocol design but are never silently relabelled as final thesis evidence.

The active pre-final design is `pilot-v0.1`, specified in `PILOT_PROTOCOL_V0_1.md` and validated from `configs/protocols/pilot-v0.1.json`. It uses disjoint development/tuning/pilot/final-reserve layouts and an episode-block changepoint; it does not authorize execution of final-reserve scenarios or final claims.

## Metrics before complex agents

Metric primitives are implemented and tested before model-specific implementations. Recovery thresholds are explicit protocol inputs. If recovery is not observed within the available horizon, recovery time is represented as `None`, not as the final timestep.

The current primitives cover matched-reference nominal/post-change performance, signed immediate/worst/terminal gaps, cumulative deficit, and explicit no-degradation/recovered/non-recovered outcomes. Their final parameters and scientific roles remain subject to pilot validation and final freeze.

## Matrix bound

The final matrix remains intentionally small: a few scientifically distinct agent roles, one primary GridWorld family, a primary persistent-change axis, limited supporting robustness diagnostics, justified severities, and enough seeds for reliable estimates. Algorithm count is not a success criterion.
