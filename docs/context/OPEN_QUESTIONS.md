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
- baseline self-explanatory dashboard UX requirements: clear labels/messages/units, contextual tooltips/help, semantic text+icon+color status treatment, actionable states, pre-run review, and lightweight skippable/replayable onboarding;
- resumable Codex task/checkpoint workflow;
- overall application -> final experiments -> analysis/evidence -> thesis/review -> defense presentation -> delivery handoff model;
- requirement for a final PowerPoint, embedded speaker notes, separate full spoken Greek script, and evidence/rehearsal validation.
- actual target-machine CPU/RAM/storage/GPU/runtime baseline and current acceleration support.
- project-owned Gymnasium GridWorld implementation strategy (scientific parameters remain open).

They are governed by DEC-021 through DEC-032 as applicable. Exact scientific choices, pilot-derived optional UI controls, and future official delivery requirements remain open below.

| ID | Open issue | Why open / missing information | Needed by | Blocks next phase? | Resolver | Safe temporary rule |
|---|---|---|---|---|---|---|
| OQ-ACA-001 | Are any supervisor-specific corrections introduced later? | The topic is approved and no current special instructions exist. | When feedback is actually received. | No. | User / supervisor. | Continue current work; record later feedback as an explicit change. |
| OQ-ACA-002 | What is the eventual submission/presentation schedule? | No verified date/procedure has been provided. | Delivery planning. | No for research/program work. | User / Department. | Do not invent dates. |
| OQ-ACA-003 | Is there a current official Word template/submission package? | Not needed for current implementation/experiments. | Final writing/submission QA. | No. | User / Department / supervisor. | Recheck near writing/submission; example theses are contextual only. |
| OQ-ACA-004 | What are the exact current defense requirements: duration, presentation language, required/allowed file format or template, mandatory content, live-demo rules, and submission procedure? | The presentation workflow is defined, but current official defense specifics have not been verified and may change. | Before final slide outline/deck freeze. | No for current research/program work. | Department / supervisor / user-provided current guidance. | Prepare for a Greek PowerPoint with speaker notes/script and evidence-backed demo fallback; do not assume duration/slide count/template. |
| OQ-RES-001 | What is the final main research question and minimal secondary questions? | Post-import evidence framing exists, but the final environment/model/metric feasibility chain is not complete. | Before pilot/final protocol freeze. | Yes. | Research decision from citation-ready evidence + prototypes/pilots. | Keep the bounded persistent-change direction as a proposal, not final methodology. |
| OQ-RES-002 | Which hypotheses are theoretically/statistically justified? | Depends on final RQ, environment, model roles, and estimands. | Before final protocol. | Yes. | Research decision. | Keep exploratory questions separate; do not invent directional hypotheses. |
| OQ-ENV-002 | What exact uncertainty mechanisms, severities, onset/timing, duration, and combinations are used? | Official examples and evidence-led hierarchy exist, but scientific parameters require environment validation/pilots. | Pilot/final protocol. | Yes. | Literature + prototypes + pilots. | Persistent rule/dynamics change remains leading recovery axis; observation/action disturbances are supporting diagnostics unless evidence/RQ changes this. |
| OQ-ENV-003 | Is formal partial observability required? | Observation corruption is relevant, but full POMDP/belief-state complexity may be unnecessary and would alter the model class. | Environment/model freeze. | Yes. | Research/environment decision. | Keep true state separate from delivered observation; do not add POMDP machinery without a distinct RQ need. |
| OQ-MOD-001 | Do all three selected capability regimes survive final post-pilot freeze? | T-312 implements and correctness-validates F0 frozen/C0 continual common tabular Q-learning plus R0 frozen rectangular robust value iteration; tuning, repeated-run feasibility, and distinct empirical value still require pilots. | Final model set/protocol. | Yes. | Pilots + T-412 freeze. | Pilot only the selected bounded set; remove a role if its documented gate fails. |
| OQ-MET-001 | Which operational metrics receive final primary, secondary, and diagnostic roles and parameter values? | Schema-v1 estimands/formulas and outcome states are implemented and known-answer validated; exact windows, tolerance, stabilization, roles, aggregation, censoring analysis, and intervals require pilots/final freeze. | Pilot/final protocol. | Yes. | `T-400` pilots plus `T-412` freeze. | Preserve full curves and all schema-v1 components; no arbitrary parameter or composite score. |
| OQ-EXP-001 | How many seeds/repetitions are required? | Depends on measured variance, precision needs, and compute budget. | Final experiment matrix. | Yes for final runs. | Pilot/statistical decision. | Never use single-run comparison. |
| OQ-EXP-002 | What model-specific tuning budgets/stopping rules are fair? | Depends on selected models and actual hardware/runtime. | Pilot/final protocol. | Yes. | Inventory + prototypes + pilots. | Record interactions/wall-clock/resource use without hard-coding final budgets early. |
| OQ-EXP-003 | What exact final statistical plan is appropriate? | Depends on estimands, nesting, censoring/non-recovery, paired scenario structure, and pilot distributions. | Before final result inspection. | Yes. | Statistical/protocol decision. | Freeze analysis roles before final evidence is inspected. |
| OQ-UI-001 | Which optional dashboard controls/views survive after pilots? | The self-explanatory UX baseline and lightweight onboarding are confirmed, but optional controls/views still depend on the real experiment workflow and feature budget. | Dashboard implementation. | No now. | Pilot-derived workflow + user/product decision where needed. | Always implement the confirmed UX baseline; add no speculative advanced controls/views. |
| OQ-AI-001 | Is any optional AI feature useful in the dashboard? | No demonstrated need exists. | Late dashboard phase only. | No. | User + measured value. | Do not integrate it. |
| OQ-PRIV-001 | What must be redacted or licensed differently before a deliberate public release/distribution? | Temporary public repository visibility may be used explicitly for GitHub Actions/CI, but that operational choice is not a decision to publish the thesis package or redistribute every contained artifact permanently. | Before any intentional public release/distribution. | No for current research/program work. | User + final privacy/licensing audit. | Temporary CI visibility does not waive the final privacy, secret, copyright, or licensing audit. |
