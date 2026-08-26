# DEC-041: Protocol v1.0 Freeze and R0 Removal

**Date:** 2026-08-26  
**Status:** Accepted  

## Context

The pilot-v0.2 campaign diagnostics (docs/experiments/PILOT_REPORT_V0_2.md) confirmed that the robust agent (R0), employing a conservative rectangular transition uncertainty set, was subject to ~96% episode truncation (censoring at the 48-step horizon) under purely nominal conditions. The overly broad robust prior causes the agent to avoid goal-directed moves when anticipating worst-case out-of-set mappings. DEC-040 declared that R0 could not be frozen in its current state, requiring either a revised construction validated through tuning or removal before the protocol freeze.

## Decision

We formally remove the R0 agent role and freeze the final protocol (protocol-v1.0). 

## Rationale

- **Informative limits**: An agent that cannot reliably reach the goal under nominal operations due to conservative priors provides no useful baseline for resilience comparisons.
- **Resource Constraints**: Revising the robust construction requires shrinking the uncertainty set, necessitating new tuning cycles to validate feasibility. This diverts quota and computational resources away from the primary scientific questions (comparing adaptive C0 to frozen F0).
- **Research Clarity**: The remaining contrast (online sample-driven adaptation vs stronger-prior frozen behavior) is objectively robust and addresses the core operational definitions in the thesis.

## Consequences

- The final evaluation matrix (protocol-v1.0.json) contains only F0 and C0.
- The 0_set_membership configuration and related parameters have been pruned from the protocol schema.
- The experiment matrix uses 16 paired roots across the 2 validated pilot layouts for F0 and C0.
- Non-recovery is censored explicitly at the horizon without attempting to assign arbitrary penalties.
