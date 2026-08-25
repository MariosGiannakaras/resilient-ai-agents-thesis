# Model Selection Workspace

**Status:** Active post-import selection workspace; exact final algorithms are not frozen.

No model receives candidate status merely because it appeared in historical chats. Selection uses the pinned bibliography, final environment/information assumptions, actual target-machine capabilities, prototypes, and pilots.

## Current role-level direction

The project compares capability roles rather than accumulating many named methods:

| Role | Current status | Purpose / condition |
|---|---|---|
| Frozen nominal/reference behavior | RETAIN | Sanity/reference comparison for disruption impact. |
| Naive continual tabular learner | RETAIN FOR PROTOTYPE/PILOT | Useful adaptation baseline; must not be described as universally incapable under all non-stationarity. |
| Robustness-oriented comparator | CONDITIONAL | Include only if uncertainty-set assumptions fit the selected GridWorld and the exact retained claims stay within sufficient citation-ready support. |
| Explicit change/context-aware adaptive learner | LEADING ADAPTIVE ROLE | Exact algorithm remains to be selected from evidence/feasibility. |
| Detector-triggered reset/restart decomposition | OPTIONAL | Include only if it answers a distinct question after practical detector validation. |
| Deep/function-approximation methods | DEFER / EXCLUDE INITIALLY | Add only if the final environment/RQ shows tabular methods are inadequate and compute/complexity is justified. |

Decision-driving citation-ready anchors currently include `SRC-70772C0629`, `SRC-9464421E55`, `SRC-76B2247457`, `SRC-FC42D9798A`, and `SRC-3C0F7CC819`.

The two robust-MDP records support the conceptual robustness-versus-adaptation distinction. They do not select a comparator or establish faster changepoint recovery. `T-310` must test assumption fit and scientific necessity; `T-311` is needed only if the retained method or claims require evidence beyond the current verified scope.

## Required selection process

1. Use the accepted CPU-first target-machine baseline from DEC-031.
2. Complete the GridWorld prototype/ADR and final information/observability framing.
3. Finalize the bounded RQ roles that agents must answer.
4. For each retained role, verify literature assumptions and formal citation status.
5. Select the smallest exact method set that spans the required capabilities.
6. Implement every agent behind the same information-limited contract in `src/resilient_agents/`.
7. Validate correctness on tiny known-answer tasks/MDPs where possible.
8. Define fair tuning/adaptation/evaluation budgets and common final scenario access.
9. Run pilots before freezing the final set.

## Fairness invariants

- No agent receives hidden regime ID, changepoint truth, disturbance flags, or ground-truth state unless the final protocol explicitly and symmetrically justifies that signal.
- A robust method does not receive the realized post-change transition kernel merely because the evaluator knows it.
- Development/tuning/pilot/final scenario partitions remain separated.
- Common final evaluation seeds/scenario schedules are fixed after protocol freeze where pairing is scientifically valid.
- Model-specific tuning is allowed only under a documented comparable information/resource policy.
- No model is retained solely because it is popular, complex, or historically mentioned.

## Evidence matrix to complete before freeze

| Candidate ID | Exact method | Role | Citation-ready support | Environment assumptions | Information access | Adaptation mode | Compute/tuning burden | Correctness test | Inclusion status |
|---|---|---|---|---|---|---|---|---|---|
| TBD | TBD after environment/RQ gates |  |  |  |  |  |  |  | UNFROZEN |

## Exclusion principles

Exclude/defer a method when it does not answer a distinct RQ, assumptions conflict with the environment, trustworthy implementation/correctness validation is not feasible, fair comparison cannot be defined, compute/tuning burden is disproportionate, or formal evidence required for the final thesis is unavailable.

## Freeze gate

No final model set is frozen until exact methods have explicit scientific roles, source-traceable support, compatible information assumptions, correctness/feasibility evidence, fair tuning rules, and pilot evidence within the measured compute budget.
