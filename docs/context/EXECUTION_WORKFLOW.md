# Execution and Review Workflow

## Operating model

The user provides goals, genuinely subjective academic/product choices, observed target-machine/application behavior, later supervisor/Department feedback and private material when actually required. Routine Git/CI/task bookkeeping should not be pushed back to the user when repository tooling can perform it.

Codex executes bounded repository work from actual state, performs objective diff review, uses GitHub CI as the canonical full-suite implementation guard, fixes failures/findings and reconciles affected active docs. ChatGPT remains the preferred later Greek writing/review/narrative layer after the explicit writing gate.

Normal implementation flow:

> persistent goal -> recover current repository state -> bounded allowed scope -> implementation -> targeted checks -> PR CI/objective review -> corrections -> durable reconciliation -> next allowed scope

## Session continuation

Every Codex session starts with exactly:

1. `AGENTS.md`;
2. `docs/context/TASKS.md`;
3. `docs/context/CURRENT_STATUS.md`.

Before selecting work, inspect Git status/current branch/recent commits and PR/check state. Repository evidence wins over stale/truncated session memory. Never discard unique branch/uncommitted work without inspection.

## Testing / CI discipline

Validation is risk-based and proportional.

- Use the smallest deterministic checks that protect the changed scientific/reliability boundary during implementation.
- Add tests for known-answer behavior, information isolation, determinism/serialization, configuration validation, lifecycle truthfulness, provenance and concrete regressions.
- Do not turn pilot/final experiment matrices into CI tests or pursue arbitrary coverage/fuzzing projects.
- GitHub PR CI is the canonical complete repository check.
- Required scientific/provenance/configuration state fails closed.

## Bibliography flow

All new source discovery/original PDFs/OCR/conversion/scientific source analysis belongs to `MariosGiannakaras/ThesisBibliography`. This repository consumes committed immutable generated corpus versions. Formal citation trust is limited to `research/bibliography/citation-ready/` unless upstream verification/promotion creates a new trusted snapshot.

## Current scientific workflow authority

Protocol-v2.1 is frozen pre-execution scientific authority under DEC-058 + DEC-060.

### Phase A — nominal learning

Each retained method trains independently under the same semantic task/information/reward contract and principal actual-environment-interaction budget. Standardized no-learning probes remain separate from deployed online utility.

### Phase B — resilience/adaptation

Each method/root/layout starts from its own exact successful Phase-A scientific checkpoint and exact branch point. The matched branches are FN, FD, AN and AD. Frozen learning state does not mutate; Adaptive learning follows the frozen method-native continuation contract.

### Recovery/direct comparison

Protocol-v2.1 additionally records passive 32-interaction reward windows across the unchanged 256-interaction Phase-B horizon. Recovery compares AN versus AD after equal layout reduction inside each root, with the frozen tolerance/stability/right-censoring semantics. Direct method contrasts are root-paired on common independent roots.

See `docs/research/RQ_EVIDENCE_TRACEABILITY.md` for final RQ/estimand/output mapping.

Historical v1.0/v1.1/pilot evidence remains separate and is never pooled into protocol-v2.1 confirmatory estimates.

## Study-first backend workflow

`Study`, not a UI screen or individual run, is the application-facing aggregate.

The implemented chain is:

> immutable recipe -> deterministic study plan -> scientific jobs/checkpoints -> validation -> root-level analysis -> deterministic evidence export

A lower-level `RunBundle` remains a provenance/checksum evidence unit. `StudyStore` records recipe/plan identity, job states, artifact lineage and finalization.

### Evidence classes

Every study/job/artifact has an explicit evidence class. DEVELOPMENT/custom output cannot be promoted to confirmatory evidence by UI action, filename changes or manual copying.

### Failure semantics

- **Scientific failure:** retained outcome; never replace with another favorable root.
- **Infrastructure failure:** not a scientific outcome; retry only with the same scientific identity/provenance rules.
- **Skipped downstream unit:** explicit when a required scientific producer is scientifically unavailable.

### Stage barriers

Later stages do not execute while an earlier stage remains unresolved. Phase-B matched sets require the exact successful Phase-A checkpoint producer.

### Final-execution authorization

The framework-neutral Study service denies confirmatory/final execution by default. The final protocol-v2.1 Study may run only after a separate explicit scientific authorization supplies the required execution token. UI code may not bypass or reimplement this guard.

DEC-062 governs the current authorized recovery: the first attempt is immutable failed/incomplete history, and the same frozen recipe must restart from zero in a distinct execution instance created from one clean corrected merged commit. Execution-instance lineage prevents storage collision without changing scientific or statistical identity. The existing authorization token remains mandatory.

## Clean application restart

DEC-059 selects PySide6 / Qt 6 Widgets as the application architecture. Historical Streamlit/React/NiceGUI implementations are superseded.

The current user direction is to restart UI implementation cleanly from current `main`, not continue the paused/pre-v2.1 presentation implementation.

The workflow for the new UI branch is:

1. create one fresh branch from current `main`;
2. read DEC-059, DEC-060, protocol-v2.1 authority and RQ traceability before editing UI;
3. classify existing `src/resilient_agents/desktop/` files;
4. preserve UI-neutral read-model/evidence/provenance/execution-policy contracts;
5. replace presentation windows/pages/widgets/styles from scratch where that produces a clearer implementation;
6. validate with DEVELOPMENT/synthetic fixtures and stored evidence only;
7. run targeted UI/backend contract checks and representative screenshot/render checks;
8. reconcile active UI docs and squash-merge one coherent PR when green.

The UI may request/observe backend state but must not construct scientific roots, branch IDs, checkpoint identities, recovery thresholds or analysis estimands itself.

## Intended application workflow

The confirmatory/frozen-study experience should remain conceptually simple and locked:

> Review Thesis Study -> authorization/lock state -> Run/Monitor only when allowed -> Validate -> Results -> Export

Before explicit final authorization, the confirmatory path is review/read-only and clearly explains why execution is locked.

A separate DEVELOPMENT/Exploratory path may expose approved configurable choices:

> Configure -> Review -> Create -> Run -> Live Monitor -> Results/Compare -> History/Artifacts/Export

Development output remains visibly non-confirmatory.

## Results and presentation boundary

The UI reads validated stored evidence/read models. It does not:

- recompute root reductions or scientific intervals from raw evidence;
- decide recovery thresholds or stability rules;
- convert censored roots to fake observed recovery times;
- relabel historical schema-v1 evidence with v2.1 semantics;
- fabricate live/provisional progress or trajectories.

Technical provenance remains available with progressive disclosure.

## Where final research executes

Final stochastic scientific evidence remains on the protocol-approved thesis-machine execution path unless an explicit amendment validates another environment. GitHub-hosted Actions are suitable for repository checks, deterministic tests and allowed reproducible postprocessing, but are not automatically the final stochastic experiment machine.

## Remaining scientific evidence flow

The protocol/backend/pre-final readiness, T-610 execution and T-611 validation/freeze work are complete. Scientifically the remaining sequence is:

1. execute the predeclared root-level analysis/sensitivity diagnostics from the T-611 frozen evidence;
2. generate final figures/tables/data and evidence handoff;
3. obtain explicit user approval before Results/Discussion/WP7 writing.

Repository cleanup and UI rebuilding are allowed before step 1 and do not authorize it.

## Downstream handoff

After explicit writing approval:

- **Repository/Codex:** reproducible evidence maps, figures/tables, technical/citation/result consistency and traceable assets.
- **ChatGPT:** Greek thesis drafting/restructuring/review, explanatory wording, slide narrative, speaker material and user-facing placement guidance.
- **Microsoft Word:** authoritative final `.docx` composition/inspection.
- **PowerPoint:** authoritative final `.pptx` inspection/rehearsal.
- **Canva:** optional bounded visual polish only; never a scientific data source.
- **User:** supervisor/private input, subjective academic review gates, selected real app media capture and final Word/PowerPoint/rehearsal inspection.

Quantitative thesis/presentation assets derive from frozen repository evidence, never manually retyped from the UI.

## Documentation rule

Every material architecture/science/tool/ownership/task change reconciles affected active documents in the same branch checkpoint. Historical records remain when clearly historical/superseded. Generated bibliography content is never hand-edited for consistency.
