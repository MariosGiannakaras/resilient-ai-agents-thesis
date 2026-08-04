# Post-import Evidence Synthesis

**Status:** Active source-traceable workspace; not a frozen protocol  
**Pinned baseline:** `bibliography-integration-v2` / `27e325a74722b8f80643e6d1902e4bf3847036f5`

## Evidence layers

1. **Citation-ready evidence:** 112 selected `SRC-*` records under `citation-ready/`; these alone may support formal thesis claims.
2. **Complete source context:** all 583 canonical sources and analyses remain searchable for interpretation, terminology, comparison, and limitations.
3. **Research materials:** 19 `MAT-*` files may support internal research and provenance but are not formal citations.
4. **Author notes:** searchable without mandatory bibliographic identity; factual final claims still require citation-ready support.
5. **Rejected/theory-only records:** accessible for negative evidence and scope context without automatic promotion.
6. **Unresolved decisions:** exact model set, environment implementation, severities, final metrics, tuning boundary, seeds, budgets, thresholds, and statistical plan remain open.

## Decision-driving citation-ready anchors

- `SRC-70772C0629`: structured switching non-stationarity means ordinary Q-learning must not be described as universally incapable; theoretical results depend on assumptions that must be made explicit and tested in the thesis regime.
- `SRC-9464421E55`: prior-free black-box non-stationary RL and detector/restart ideas motivate finite-horizon validation of activation, delay, and error rather than assumed practical recovery.
- `SRC-76B2247457`: continual-RL evaluation requires a leakage-free boundary between tuning, pilots, and final trajectories; no universal tuning fraction is adopted.

## Full-corpus internal candidates requiring formal-evidence resolution

- `SRC-FC42D9798A` and `SRC-3C0F7CC819` contain robust-MDP context that may motivate a robustness-oriented comparator when its uncertainty assumptions match the final GridWorld semantics and information-access contract.
- These records are **not citation-ready in the pinned baseline** and must not be presented as formal citation-ready support.
- If a robust-MDP comparator is retained for the final model set, create a precise upstream verification/promotion task in `ThesisBibliography`, then synchronize a later immutable baseline before using the evidence in a final thesis claim.

## Current synthesis

The bounded direction remains persistent rule/dynamics change as the primary recovery axis, with observation corruption and action-execution failure as supporting robustness diagnostics. Candidate agents are compared by capability role rather than algorithm count: frozen nominal reference, naive continual learner, conditional robustness-oriented comparator, explicit change/context-aware adaptive comparator, and an optional detector/reset decomposition only if prototypes establish a distinct research question.

DEC-023 now provides the implementation infrastructure for information isolation, deterministic RNG streams, protocol partitions, run bundles, and known-answer metric primitives. Those engineering decisions do not freeze the scientific model/metric/protocol choices above.

## Promotion rule

When a `MAT-*`, rejected, theory-only, full-corpus non-citation-ready source, or note item becomes necessary for a final claim, create an upstream promotion task containing the missing bibliographic identity/evidence requirement. Do not promote it locally. A later verified export and synchronization is required before formal citation.
