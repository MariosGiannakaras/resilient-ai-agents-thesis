# Open Questions

This file contains only issues that are genuinely unresolved after current repository evidence and accepted decisions. Superseded historical questions are not carried forward as active uncertainty.

## Resolved and no longer open

The following are already decided or completed:

- bibliography ownership/import/provenance boundary;
- Python 3.12 + `uv`, project-owned Gymnasium GridWorld, deterministic RNG and evaluator/agent information boundary;
- target-machine CPU baseline and protocol-v2 feasibility/tuning/sizing;
- retained final methods: Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
- selected method-specific configurations and protocol-v2.1 final matrix dimensions;
- final Phase-A budget/probe/checkpoint semantics;
- final Phase-B matched FN/FD/AN/AD contract and 256-interaction horizon;
- protocol-v2.1 RQ1/RQ2/RQ3 estimands, direct comparisons, recovery definition/censoring and actual-root Student-t interval policy;
- application framework: PySide6 / Qt 6 Widgets under DEC-059;
- framework-neutral Study backend and stored-evidence read-model boundary;
- novice-first/self-explanatory UI requirements;
- final-reserve execution remains separately authorization-gated, and T-610 plus DEC-062 recovery are now authorized without weakening that gate;
- standalone Windows packaging is intentionally deferred until after the thesis.

Historical v1.0/v1.1/pilot evidence remains auditable history; resolving current questions never relabels old evidence.

## Current open questions

| ID | Open issue | Why open | Needed by | Blocks now? | Resolver / safe rule |
|---|---|---|---|---|---|
| OQ-ACA-001 | Are supervisor-specific corrections introduced later? | None currently exist. | When feedback arrives. | No. | User/supervisor; record as an explicit change when received. |
| OQ-ACA-002 | What is the eventual submission/presentation schedule? | No verified date has been provided. | Delivery planning. | No. | User/Department; never invent dates. |
| OQ-ACA-003 | Is there a current official Word template/submission package? | Not required for current implementation and may change. | Thesis composition/final QA. | No. | Recheck official sources near writing/submission. |
| OQ-ACA-004 | What are the exact current defense duration/language/file/template/live-demo/submission rules? | They have not been verified for final delivery and may change. | Defense freeze. | No. | Recheck official guidance near defense; do not invent slide count/duration. |
| OQ-UI-001 | What exact visual composition survives the clean protocol-v2.1 UI rebuild? | Architecture and UX constraints are frozen, but page composition can be improved during implementation. | Current UI rebuild. | No scientific block. | Start from fresh `main`; preserve backend/read-model contracts, replace presentation code where useful, and validate with representative DEVELOPMENT/synthetic states. |
| OQ-PKG-001 | What exact post-thesis standalone Windows packaging recipe is finally delivered? | Packaging is intentionally deferred and should target the finally accepted rebuilt UI. | Post-thesis delivery. | No. | Resolve in issue #94 after thesis/UI freeze; validate on the actual Windows machine. |
| OQ-AI-001 | Is any optional AI feature useful inside the application? | No demonstrated need. | Late UI only, if ever. | No. | Do not integrate unless a concrete measurable benefit appears. |
| OQ-PRIV-001 | Are any additional privacy/licensing/copyright changes required before deliberate wider distribution? | Repository is public, but final distribution packaging has its own audit. | Final delivery. | No. | Run final secret/privacy/license/copyright audit before release packaging. |

## Current authority

Concrete status/dependencies are in `TASKS.md`; compact current state is in `CURRENT_STATUS.md`. The final scientific experiment and DEC-062 recovery are not open design questions: the frozen replacement execution is in progress, while T-611 and later work remain blocked by task dependencies.
