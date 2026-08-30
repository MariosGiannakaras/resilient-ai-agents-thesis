# DEC-058 - Protocol-v2.0 final scientific freeze

- **Date:** 2026-08-30
- **Status:** Accepted
- **Decision owners:** Implementation team under the evidence-backed autonomous decision boundary
- **Related requirements:** REQ-RES-001, REQ-RES-002, REQ-RES-008, REQ-ARCH-005, REQ-TEST-001
- **Related research questions:** Provisional main RQ and secondary questions in docs/research/RESEARCH_BRIEF.md

## Context

Following the immutable valid-failed sizing-v0.2 evidence and the exact SB3 ingress boundary correction authorized by DEC-057, the T-527 fresh three-method sizing-v0.3 completion execution completed successfully on the target machine with zero failures. It produced 144 fresh Phase-A units and 288 matched sets.

The final sizing validator generated the complete combined 5-method sizing package (protocol-v2-t527-sizing-combined-v0.3) integrating the structurally unaffected complete Q-Learning and SARSA strata from sizing-v0.2 with the complete DQN, PPO, and Dyna-Q+ strata from sizing-v0.3.

The combined evidence fulfills all requirements to definitively fix the Protocol-v2.0 statistical contracts and exact denominators, and permits proceeding to the final evaluation firewall.

## Decision

This decision authorizes the formal scientific freeze of Protocol-v2.0 and the creation of protocol-v2.0-final.json.

1. **Retained Methods**: All five methods are retained with their DEC-055 optimal configurations (q-c06, sarsa-c06, dqn-c05, ppo-c06, dyna-c03). A2C and the full Dyna-Q arm remain excluded.
2. **Phase-A Budget**: Fixed at exactly 8,192 interactions per root/layout.
3. **Probe Schedule**: Probes execute precisely at interactions 0, 512, 1024, 2048, 4096, and 8192, with 12 episodes per probe.
4. **PPO Parameter**: 
_steps remains exactly 128.
5. **Phase-B Horizon**: The 256-interaction horizon is mechanically selected, as every method/root/layout pair in the combined matrix successfully completed >=2 adaptive native update opportunities and >=2 branch episodes at horizon 256.
6. **No-Learning Prefix**: Exactly one shared nominal interaction applies before branch replication.
7. **Lifecycle**: The persistent multi-episode lifecycle applies deterministically across boundaries.
8. **Final Conditions**: The final evaluated conditions are exactly four:
   - ction-remap-swap-right-down
   - ction-remap-cycle-clockwise
   - ction-failure-0.15
   - observation-corruption-0.05
9. **Final Root Count**: The mechanically selected root count is 12 (derived from the smallest candidate count achieving a Student-t 95% interval half-width < 0.20 for both Phase-A AUC and Phase-B adaptation benefit). The maximum half-width at 12 roots was 0.1428.
10. **Final Held-Out Layouts**: Exactly two 7x7 gw-l1 layouts (gw-l1-final-a, gw-l1-final-b) have been generated using the deterministic first-two-valid structural algorithm and are frozen in the final configuration.
11. **Final Roots/Seeds**: Exactly 12 final roots (	527-final-r01 through 	527-final-r12) have been generated using the DEC-056 seed-stream formula (seeds 71001-76012) and are frozen in the final configuration.
12. **Statistical Contract**: The primary uncertainty remains the root-level two-sided Student-t 95% interval with root-only bootstrap sensitivity.
13. **Final Denominators**: The final evaluation matrix spans:
    - 5 methods
    - 12 independent roots
    - 2 held-out layouts
    - Phase-A units: 5 x 12 x 2 = 120
    - Phase-B conditions: 4
    - Phase-B matched sets (FN/FD/AN/AD branches): 5 x 12 x 2 x 4 = 480
    - Branches: 480 x 4 = 1920
14. **Final Firewall**: 
    - Final reserve identities are frozen/materialized.
    - Final reserve scientific execution remains sealed.
    - inal_reserve_access=false
    - Later T-610+ explicit authorization is required. No agent parameter, statistical rule, or environment layout may be changed after this freeze. T-528 is now READY.

## Consequences

- The scientific protocol is immutable.
- T-527 is complete.
- Issue #95 can be closed.
- The T-528 application rebuild and subsequent thesis tasks are unblocked.
