# Model Selection Workspace

**Status:** `RESEARCH_REQUIRED`. There is no model shortlist.

The old conversation exports included many model names, but the user clarified that those conversations were examples/context only. Therefore, no model receives candidate status merely because it appeared there.

## Required selection process

1. Freeze provisional research questions and environment class.
2. Conduct a fresh literature review using verified primary/peer-reviewed sources.
3. Define the capability dimensions that need comparison only after they map to an approved research question and environment assumption.
4. Identify the smallest set of baselines and agents that can answer those questions.
5. Inspect trustworthy implementations, licenses, testability and maintenance.
6. Run minimal feasibility/correctness prototypes on the actual hardware.
7. Define fair tuning/evaluation budgets and information access.
8. Record inclusion/exclusion rationale in a decision/ADR.
9. Run pilots before freezing the final set.

## Evidence matrix to populate

| Candidate ID | Model/family | RQ role | Primary literature | Implementation source/version/license | Environment assumptions | Information access | Adaptation mode | Expected compute | Validation plan | Inclusion status |
|---|---|---|---|---|---|---|---|---|---|---|
| TBD | TBD after fresh research |  |  |  |  |  |  |  |  | RESEARCH_REQUIRED |

## Baseline and comparison questions

The literature review must determine, rather than assume:

- What minimum sanity checks are needed to validate the environment and metrics?
- Which comparison points are scientifically legitimate under equal or explicitly different information access?
- Which agent capabilities are required by the approved research questions?
- Which alternatives would be redundant rather than informative?
- Can every selected method be implemented, validated and evaluated fairly within the measured compute budget?

## Exclusion principles

Exclude or defer a model when:

- it does not answer a distinct research question,
- its assumptions conflict with the environment,
- a trustworthy implementation cannot be validated,
- fair comparison cannot be defined,
- compute/variance/tuning burden is disproportionate,
- it is included only because it is fashionable or appeared in an old chat,
- its claimed novelty would be ad hoc and unsupported by a literature gap.

## Decision gate

No model code is implemented beyond small research prototypes until the model matrix has verified sources, explicit roles, feasibility evidence and an accepted decision entry.
