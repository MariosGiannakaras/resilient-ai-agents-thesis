# Execution and Review Workflow

## Operating model

The user provides goals, genuinely non-objective academic/product choices, observed target-machine/application behavior, later supervisor/Department feedback and private material when actually required. The user is not the routine Git/CI/task-bookkeeping operator.

Codex executes bounded repository work from actual state, performs objective diff review, uses GitHub CI as the canonical full-suite implementation guard, fixes failures/findings and reconciles tasks/docs. The active pre-WP7 package stays on the single branch/PR declared in `TASKS.md` and is not merged merely because an intermediate checkpoint is green.

ChatGPT is used for independent research/review and, only after the explicit WP7 approval gate, becomes the preferred Greek writing/narrative/user-instruction layer.

Normal implementation flow:

> persistent goal -> canonical task registry -> bounded dependency-valid scope -> implementation -> targeted checks -> PR CI/objective review -> corrections -> durable reconciliation -> next allowed scope

## Session continuation and quota recovery

Every Codex session starts with exactly:

1. `AGENTS.md`;
2. `docs/context/TASKS.md`;
3. `docs/context/CURRENT_STATUS.md`.

Before selecting work, inspect Git status/current branch/recent commits and PR/check state. Resume valid `IN_PROGRESS` work first. Repository evidence wins over stale/truncated session memory. Never discard useful branch/uncommitted work without inspection.

## Testing / CI discipline

Validation is risk-based and proportional.

- Use the smallest deterministic checks that protect the changed scientific/reliability boundary during implementation.
- Add tests for known-answer behavior, information isolation, determinism/serialization, configuration validation, lifecycle truthfulness, provenance and concrete regressions.
- Do not turn experiment matrices into CI tests or pursue arbitrary coverage/fuzzing projects.
- GitHub PR CI is the canonical complete repository check.
- Required scientific/provenance/configuration state fails closed.

## Bibliography flow

All new source discovery/original PDFs/OCR/conversion/scientific source analysis belongs to `MariosGiannakaras/ThesisBibliography`. This repository consumes only committed immutable generated corpus versions. Formal citation trust is limited to `research/bibliography/citation-ready/`.

## Scientific workflow authority

Protocol-v2, controlled by DEC-048/050, separates:

1. **Phase A — nominal learning:** every retained method trains independently under common semantic task/information and actual-environment-interaction accounting, with isolated no-learning probes.
2. **Phase B — resilience/adaptation:** each method/root/layout starts from its own exact Phase-A scientific checkpoint and branches into FN/FD/AN/AD with Adaptive learning beginning only after the change boundary.

Q-Learning, SARSA, DQN, PPO and Dyna-Q+ are the current feasibility core; final retention remains T-526/T-527 gated. Dyna-Q is a targeted ablation and A2C remains conditional. Historical v1.0/v1.1 evidence is not pooled into v2 confirmatory estimates.

## Study-first backend workflow

DEC-051/T-529 makes `Study`, not an individual run, the final backend aggregate.

The authoritative implemented chain is:

> immutable recipe -> deterministic study plan -> scientific jobs/checkpoints -> validation -> analysis -> export

A lower-level `RunBundle` remains the provenance/checksum evidence unit for one scientific execution. `StudyStore` is the parent lifecycle that records recipe/plan identity, job states, artifact lineage and finalization.

### Evidence classes

Every study/job/artifact is explicitly classified as development, tuning, confirmatory, derived, exploratory or historical.

A confirmatory Study recipe must already be frozen. Development/custom output cannot be promoted by UI action or filename changes.

### Failure semantics

- **Scientific failure:** retained outcome; do not replace with another favorable root.
- **Infrastructure failure:** not a scientific outcome; may retry only with the same scientific identity/provenance rules.
- **Skipped downstream unit:** explicit when a required scientific checkpoint does not exist because its producer failed scientifically.

### Stage barriers

Later stages do not execute while an earlier stage remains unresolved. Direct artifact dependencies are stricter: a Phase-B matched set requires the exact successful Phase-A checkpoint producer.

## T-529 completion boundary

T-529 is complete. The framework-neutral backend now provides:

1. immutable Study recipe/lifecycle/store contracts;
2. deterministic Phase-A/Phase-B job DAGs from explicit execution settings;
3. real recipe-materialized execution over the validated protocol-v2 method-native drivers;
4. exact scientific checkpoint lineage and a shared no-learning prefix primitive;
5. one atomic matched FN/FD/AN/AD Phase-B execution unit;
6. structural evidence validation and planned-vs-produced reconciliation;
7. root/layout-aware analysis with matched adaptation-benefit estimands and explicit outcome denominators;
8. deterministic machine-readable CSV/JSON/result-ID/provenance export for later scientific/thesis tooling;
9. framework-neutral `StudyService` as the application-facing service boundary.

T-529 does **not** generate thesis prose, final thesis figures or PPTX. Those remain later evidence/writing deliverables after T-527/T-610..T-613 and the explicit WP7 gate.

No final scientific parameter is supplied by frontend defaults.

## External T-526 / T-527 gates

T-529 is complete without consuming or inventing T-526/T-527 outcomes.

T-526 remains the predeclared non-final feasibility/environment/severity/runtime gate on the physical Windows thesis machine. Hosted CI cannot substitute for it. A repository-preflight failure before the runner starts is infrastructure state, not a scientific outcome.

The latest physical attempt stopped before execution because the local checkout was stale and contained untracked `temp_body.md`. Before retrying, inspect/preserve that draft as appropriate, fast-forward the clean checkout to the reviewed remote branch head and rerun the predeclared entrypoint only after preflight passes. No T-526 scientific evidence exists from the aborted attempt.

T-527 then freezes retained methods, layouts, budgets, hyperparameters, severities, roots, statistics and the remaining Phase-B lifecycle. Only after this can a confirmatory Study recipe be materialized with final values.

## Application handoff

Historical Streamlit/React/NiceGUI implementations are not the final application architecture. The active NiceGUI source/runtime/package surface has been removed from the active tree under DEC-049/051; Git history preserves it as prototype evidence.

The future application is a client of `StudyService`. It may request/observe:

- recipe validation and deterministic plan preview;
- study create/start/resume/status;
- aggregate and per-job progress;
- truthful live/provisional events when implemented;
- finalized results/history/artifacts;
- validation/analysis/export outputs.

It must not construct roots, branch IDs, checkpoint paths, SB3 objects or scientific execution commands itself.

T-528 remains blocked on T-527. Its T-529 backend dependency is satisfied. It must select a framework different from NiceGUI and rebuild the frontend from scratch.

## Intended user workflow after T-528

The default thesis-valid path should be conceptually simple:

> Run Thesis Study -> Monitor -> Validate -> Results -> Export

A separate exploratory/custom path may expose model/settings choices, but it remains permanently distinguishable from confirmatory thesis evidence.

The general exploratory UX remains:

> Mode -> Model(s) -> Settings -> Review -> Run -> Live Monitor -> Results/Compare -> History/Artifacts/Export

Backend orchestration creates FN/FD/AN/AD and scientific bookkeeping automatically.

## Where approved research executes

Final stochastic scientific evidence remains on the validated thesis-machine execution path unless an explicit protocol amendment validates another environment. GitHub-hosted Actions remain suitable for repository checks, deterministic tests and allowed reproducible analysis/artifact regeneration, but are not automatically equivalent to the thesis machine.

Once the final application is accepted, ordinary execution of an already-frozen Study should not require Codex or manual console construction. Codex remains relevant for code/protocol changes, debugging, justified amendments and repository/evidence maintenance.

## Remaining protocol-v2 evidence flow

T-529's backend prerequisite is complete. The remaining sequence is:

1. T-526 physical feasibility/severity/runtime evidence.
2. T-527 fair tuning, precision/runtime sizing and machine-readable protocol freeze.
3. T-528 new-framework frontend rebuild against the completed StudyService contract.
4. T-511 intended-user acceptance.
5. T-610 execute the frozen protocol-v2 final Study.
6. T-611 validate/freeze final evidence.
7. T-612 execute the predeclared root-level analysis/sensitivity diagnostics.
8. T-613 generate final figures/tables/data and thesis/defense evidence package.

No final-reserve inspection occurs before the frozen protocol authorizes it.

## Mandatory pre-WP7 gate

Application/evidence completion does not authorize writing. Only explicit user approval after T-613/T-511 unlocks T-700+.

## WP7/WP8 handoff

After approval:

- **Repository/Codex:** evidence maps, reproducible figures/tables, technical/citation/result consistency and traceable asset manifests.
- **ChatGPT:** Greek thesis drafting/restructuring/review, explanatory wording, slide narrative, speaker notes/script and exact user-facing manual placement instructions.
- **Microsoft Word:** authoritative final `.docx` composition/inspection.
- **PowerPoint:** authoritative final `.pptx` inspection/rehearsal.
- **Canva:** optional bounded visual polish only; never a scientific data source.
- **User:** supervisor/private input, subjective academic review gates, selected real app media capture and final Word/PowerPoint/rehearsal inspection.

Quantitative thesis/presentation assets derive from frozen repository evidence, never manually retyped from the UI.

## Documentation rule

Every material architecture/science/tool/ownership/task change reconciles affected active documents in the same branch checkpoint. Historical records remain only when clearly labelled historical/superseded. Generated bibliography content is never hand-edited for consistency.