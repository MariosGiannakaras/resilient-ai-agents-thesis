# DEC-041: Protocol v1.0 Freeze and R0 Removal

**Date:** 2026-08-26  
**Status:** Accepted  

## Context

The pilot-v0.2 campaign diagnostics (`docs/experiments/PILOT_REPORT_V0_2.md`) confirmed that the robust agent (R0), employing a conservative rectangular transition uncertainty set, was subject to ~96% episode truncation (censoring at the 48-step horizon) under purely nominal conditions. The overly broad robust prior causes the agent to avoid goal-directed moves when anticipating worst-case out-of-set mappings. DEC-040 declared that R0 could not be frozen in its current state, requiring either a revised construction validated through tuning or removal before the protocol freeze.

## Decision

We formally remove the R0 agent role and freeze the final protocol (`protocol-v1.0`).

## Rationale

- **Informative limits**: An agent that cannot reliably reach the goal under nominal operations due to conservative priors provides no useful baseline for resilience comparisons.
- **Resource Constraints**: Revising the robust construction requires shrinking the uncertainty set, necessitating new tuning cycles to validate feasibility. This diverts quota and computational resources away from the primary scientific questions (comparing adaptive C0 to frozen F0).
- **Research Clarity**: The remaining F0/C0 contrast cleanly isolates the effect of permitting ordinary online Q-learning after the change while both roles begin from the same selected nominal Q-learning checkpoint.

## Consequences

- The final evaluation matrix in `configs/protocols/protocol-v1.0.json` contains only F0 and C0.
- The R0 uncertainty-set configuration and related parameters are absent from the frozen final protocol schema.
- Non-recovery is censored explicitly at the horizon without assigning an arbitrary penalty.
- R0 remains retained as historical negative/diagnostic pilot evidence; this decision does not erase the earlier robust-planning investigation.

## Historical count/layout reconciliation

The original prose for this decision stated that the final experiment used “16 paired roots across the 2 validated pilot layouts.” That sentence was superseded by the actual protocol that was frozen and executed. The immutable machine-readable authority is `configs/protocols/protocol-v1.0.json`, which declares:

- two held-out final layouts: `final-l01` and `final-l02`;
- **32** final evaluation root seeds;
- therefore 64 root-layout scientific cells per agent-condition pair.

`docs/experiments/PROTOCOL_V1_0.md` records the same reconciliation. This clarification repairs historical documentation only: it does **not** modify `protocol-v1.0`, any accepted `FINAL-*` evidence, or any scientific result after inspection.