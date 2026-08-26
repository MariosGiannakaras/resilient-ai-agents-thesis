# Post-import Evidence Synthesis

**Status:** Active source-traceable workspace; not a frozen protocol  
**Pinned baseline:** accepted v3 import at upstream checkout `71995373ae0da64149583cae8d7a2c17e5ab1a0a`; corpus source `e46693d4201cf47c118eb61c216243f3c5798e28`; citation-ready source `822891fb585c98dbe4464602e97998704d1609c5`

## Evidence layers

1. **Citation-ready evidence:** 113 selected `SRC-*` records under `citation-ready/`; these alone may support formal thesis claims.
2. **Complete source context:** all 585 canonical sources and analyses remain searchable for interpretation, terminology, comparison, and limitations.
3. **Research materials:** 19 `MAT-*` files may support internal research and provenance but are not formal citations.
4. **Author notes:** searchable without mandatory bibliographic identity; factual final claims still require citation-ready support.
5. **Rejected/theory-only records:** accessible for negative evidence and scope context without automatic promotion.
6. **Unresolved decisions:** final post-pilot role retention/hyperparameters, scenario severities/matrix, metric parameters/roles, tuning boundary, seeds, budgets, and statistical plan remain open.

## Decision-driving citation-ready anchors

- `SRC-70772C0629`: structured switching non-stationarity means ordinary Q-learning must not be described as universally incapable; theoretical results depend on assumptions that must be made explicit and tested in the thesis regime.
- `SRC-9464421E55`: prior-free black-box non-stationary RL and detector/restart ideas motivate finite-horizon validation of activation, delay, and error rather than assumed practical recovery.
- `SRC-76B2247457`: continual-RL evaluation requires a leakage-free boundary between tuning, pilots, and final trajectories; no universal tuning fraction is adopted.
- `SRC-FC42D9798A`: robust-MDP policy optimization assumes a known structured uncertainty set and does not provide change detection or explicit recovery.
- `SRC-3C0F7CC819`: online robust Q-learning supports an incremental tabular feasibility concept under model uncertainty but does not establish faster changepoint recovery.

## Robust-MDP evidence boundary after v3 promotion

- `SRC-FC42D9798A` and `SRC-3C0F7CC819` are citation-ready in the accepted v3 baseline. They may formally support the conceptual distinction between robustness within a declared uncertainty set and recovery after an unknown change.
- Their promotion removed the earlier source-status blocker but still does not support a claim of changepoint-recovery superiority.
- DEC-034 retains finite rectangular robust value iteration only for declared-set frozen robustness. Citation-ready `SRC-52E62452B8` provides the exact robust-DP support required by that bounded role, so `T-311` is complete without upstream promotion; in-set/out-of-set assumptions and conservativeness remain explicit.

## Current synthesis

The bounded direction remains persistent rule/dynamics change as the primary recovery axis, with observation corruption and action-execution failure as supporting robustness diagnostics. DEC-034 selects two implementations in three capability regimes: common tabular Q-learning as F0 frozen and C0 continual, plus R0 frozen rectangular robust value iteration. Context-memory and detector/reset methods are excluded unless a distinct RQ and their recorded reopening conditions arise before freeze.

DEC-023 now provides the implementation infrastructure for information isolation, deterministic RNG streams, protocol partitions, run bundles, and known-answer metric primitives. Those engineering decisions do not freeze the scientific model/metric/protocol choices above.

## Promotion rule

When a `MAT-*`, rejected, theory-only, full-corpus non-citation-ready source, or note item becomes necessary for a final claim, create an upstream promotion task containing the missing bibliographic identity/evidence requirement. Do not promote it locally. A later verified export and synchronization is required before formal citation.
