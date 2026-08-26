# Final Protocol v1.0

**Protocol identity:** protocol-v1.0

**Lifecycle state:** frozen final evaluation protocol
**Machine-readable authority:** configs/protocols/protocol-v1.0.json

## R0 Removal and Role Reframing

Following the results in docs/experiments/PILOT_REPORT_V0_2.md and the formal decision in DEC-041, the robust planner role (R0) has been completely removed from this final protocol. Pilot diagnostics demonstrated that R0's prior/policy/horizon combination suffered ~96% truncation in nominal conditions due to overly conservative in-set action remapping assumptions. Rather than undertaking an extensive and scientifically uninformative re-tuning of the robust construction, the protocol focuses on the objective contrast between the frozen baseline (F0) and the adaptive role (C0). 

## Protocol Definition

- **Agent Regimes**: 
  - F0 (frozen reference)
  - C0 (adaptive role with online post-change learning)
- **Conditions**: 7 conditions (nominal, 2 action remaps, 2 action failures, 2 observation corruptions)
- **GridWorld Layouts**: 2 distinct layouts (pilot-l01, pilot-l02), retaining layout blocking due to observed F0 variance.
- **Evaluation Matrix**: 16 distinct root seeds per condition per layout, totaling 32 scientific units per agent-condition pair.
- **Tuning**: Reuses the validated F0 tuning configuration from pilot-v0.1; no final tuning is performed.
- **Recovery & Metrics**: Recovery is defined without a single binary cutoff. Non-recovery is censored at the horizon with a null recovery time. The primary analysis will report component curve estimands and operational stability rather than a single collapsed resilience score.
