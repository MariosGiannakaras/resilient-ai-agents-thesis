# Open Questions

This file contains only unresolved issues that cannot be considered completed from the current repository, accepted decisions, verified bibliography, or actual system evidence.

## Resolved since earlier versions

The following are **not open questions anymore**:

- complete bibliography consumer migration/import;
- private bibliography read/authentication verification;
- bibliography provenance/integrity baseline;
- Python/runtime project baseline;
- package/environment-information/RNG/run-bundle architecture;
- filesystem-first storage and guarded one-commit/one-push publication;
- selective Git LFS policy for large thesis-produced artifacts;
- final-dashboard architectural direction as a thin local Streamlit layer after core/pilots;
- resumable Codex task/checkpoint workflow;
- overall application -> final experiments -> analysis/evidence -> thesis/review -> defense presentation -> delivery handoff model;
- requirement for a final PowerPoint, embedded speaker notes, separate full spoken Greek script, and evidence/rehearsal validation.

They are governed by DEC-021 through DEC-026 as applicable. Exact scientific choices and future official delivery requirements remain open below.

| ID | Open issue | Why open / missing information | Needed by | Blocks next phase? | Resolver | Safe temporary rule |
|---|---|---|---|---|---|---|
| OQ-ACA-001 | Are any supervisor-specific corrections introduced later? | The topic is approved and no current special instructions exist. | When feedback is actually received. | No. | User / supervisor. | Continue current work; record later feedback as an explicit change. |
| OQ-ACA-002 | What is the eventual submission/presentation schedule? | No verified date/procedure has been provided. | Delivery planning. | No for research/program work. | User / Department. | Do not invent dates. |
| OQ-ACA-003 | Is there a current official Word template/submission package? | Not needed for current implementation/experiments. | Final writing/submission QA. | No. | User / Department / supervisor. | Recheck near writing/submission; example theses are contextual only. |
| OQ-ACA-004 | What are the exact current defense requirements: duration, presentation language, required/allowed file format or template, mandatory content, live-demo rules, and submission procedure? | The presentation workflow is defined, but current official defense specifics have not been verified and may change. | Before final slide outline/deck freeze. | No for current research/program work. | Department / supervisor / user-provided current guidance. | Prepare for a Greek PowerPoint with speaker notes/script and evidence-backed demo fallback; do not assume duration/slide count/template. |
| OQ-HW-001 | What are the accepted capabilities of the actual experiment machine? | The collector exists and is tested, but the actual thesis machine has not yet produced an accepted inventory. | Before compute-dependent dependency/model/budget choices. | Yes for compute-dependent choices. | Local Codex/system inventory + review. | Remain CPU-compatible; make no CUDA/GPU assumption. |
| OQ-RES-001 | What is the final main research question and minimal secondary questions? | Post-import evidence framing exists, but the final environment/model/metric feasibility chain is not complete. | Before pilot/final protocol freeze. | Yes. | Research decision from citation-ready evidence + prototypes/pilots. | Keep the bounded persistent-change direction as a proposal, not final methodology. |
| OQ-RES-002 | Which hypotheses are theoretically/statistically justified? | Depends on final RQ, environment, model roles, and estimands. | Before final protocol. | Yes. | Research decision. | Keep exploratory questions separate; do not invent directional hypotheses. |
| OQ-ENV-001 | Which GridWorld implementation is selected? | Technical pre-screen retained project-owned Gymnasium-compatible and thin MiniGrid prototype paths; final prototype/ADR is pending. | Before full environment implementation. | Yes. | Prototype + ADR. | Use shared contracts in `src/resilient_agents/`; do not create a second environment interface. |
| OQ-ENV-002 | What exact uncertainty mechanisms, severities, onset/timing, duration, and combinations are used? | Official examples and evidence-led hierarchy exist, but scientific parameters require environment validation/pilots. | Pilot/final protocol. | Yes. | Literature + prototypes + pilots. | Persistent rule/dynamics change remains leading recovery axis; observation/action disturbances are supporting diagnostics unless evidence/RQ changes this. |
| OQ-ENV-003 | Is formal partial observability required? | Observation corruption is relevant, but full POMDP/belief-state complexity may be unnecessary and would alter the model class. | Environment/model freeze. | Yes. | Research/environment decision. | Keep true state separate from delivered observation; do not add POMDP machinery without a distinct RQ need. |
| OQ-MOD-001 | Which exact models/baselines are in the final comparison? | Role-level direction exists, but exact methods depend on final environment, evidence, machine inventory, and pilots. | Agent implementation/final protocol. | Yes. | Verified evidence + feasibility + pilots. | Keep the set small and role-based; no algorithm is included merely for breadth. |
| OQ-MOD-002 | Is a robust-MDP comparator retained? | Relevant full-corpus evidence exists, but formal citation-ready support/assumption fit is not yet sufficient for a final inclusion decision. | Final model set. | Only for that comparator. | Upstream evidence verification/promotion + environment fit. | Treat as conditional internal candidate, not formally supported final baseline. |
| OQ-MET-001 | Which resilience/recovery metrics are primary, secondary, and diagnostic? | Metric primitives exist, but exact estimands, thresholds, windows, censoring, and aggregation are not frozen. | Pilot/final protocol. | Yes. | Literature + known-answer fixtures + pilots. | Preserve full degradation/recovery trajectory and explicit non-recovery; no arbitrary threshold. |
| OQ-EXP-001 | How many seeds/repetitions are required? | Depends on measured variance, precision needs, and compute budget. | Final experiment matrix. | Yes for final runs. | Pilot/statistical decision. | Never use single-run comparison. |
| OQ-EXP-002 | What model-specific tuning budgets/stopping rules are fair? | Depends on selected models and actual hardware/runtime. | Pilot/final protocol. | Yes. | Inventory + prototypes + pilots. | Record interactions/wall-clock/resource use without hard-coding final budgets early. |
| OQ-EXP-003 | What exact final statistical plan is appropriate? | Depends on estimands, nesting, censoring/non-recovery, paired scenario structure, and pilot distributions. | Before final result inspection. | Yes. | Statistical/protocol decision. | Freeze analysis roles before final evidence is inspected. |
| OQ-UI-001 | Which optional dashboard controls/views survive after pilots? | Core architecture and Streamlit direction are accepted, but the exact feature budget should follow the real experiment workflow. | Dashboard implementation. | No now. | Pilot-derived workflow + user/product decision where needed. | Build no speculative advanced features. |
| OQ-AI-001 | Is any optional AI feature useful in the dashboard? | No demonstrated need exists. | Late dashboard phase only. | No. | User + measured value. | Do not integrate it. |
| OQ-PRIV-001 | What must be redacted before any possible public release? | Repository currently remains private. | Only if public release is considered. | No. | User/privacy audit. | Keep repository private. |
