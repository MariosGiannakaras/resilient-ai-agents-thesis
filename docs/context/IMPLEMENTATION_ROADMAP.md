# Implementation Roadmap

The roadmap is phase-gated and optimized for thesis completion, scientific adequacy, reproducibility, and bounded engineering complexity.

## Working rule

Phases are checkpoints, not the concrete execution checklist and not mandatory separate PRs. `docs/context/TASKS.md` is the canonical task/status/resume registry. Combine adjacent work when it remains reviewable, but do not skip task acceptance conditions or scientific gates merely because infrastructure already exists.

## Phase 1 — Context, bibliography, and target machine

- Confirm the immutable bibliography baseline and current project context.
- Run/accept the privacy-minimal system inventory on the actual experiment machine.
- **Gate:** no compute-dependent dependency, model-budget, or acceleration decision before the real inventory.

## Phase 2 — Research framing

- Define the bounded main research question, minimal secondary questions, and hypotheses from citation-ready evidence.
- Keep final model/environment/protocol choices unfrozen until feasibility evidence exists.

## Phase 3 — Environment contract and GridWorld decision

- Use the common environment/ground-truth contracts in `src/resilient_agents/`.
- DEC-032's project-owned Gymnasium path and explicit schema-v1 contracts are implemented.
- **Gate passed:** deterministic known-answer transition/reference-trace and information-boundary tests pass.

## Phase 4 — Reproducibility and metric fixtures

- Validate independent RNG streams, deterministic replay, provenance, run bundles, and storage.
- Operational metric schema v1 and synthetic hand-calculated tests are complete; pilot-derived numeric/statistical choices remain later freeze inputs.
- Explicitly represent non-recovery rather than substituting the horizon.

## Phase 5 — Small model-role selection

- F0/C0 common tabular Q-learning and R0 rectangular robust value iteration are implemented with versioned state and focused correctness tests; final retention follows pilots.
- All selected agents use the same strict information-limited contract.
- **Gate:** no privileged ground truth and no model without a distinct research role.

## Phase 6 — Pilot protocol

- `pilot-v0.1` defines explicit disjoint development/tuning/pilot/final-reserve layouts and a validated stage firewall.
- Precommitted seeds, bounded diagnostic budgets/severities, tuning/checkpoint rules, metric sensitivity, resources, failures, exclusions, and preliminary analysis units are explicit; pilots determine later final values.
- Refresh relevant literature in `ThesisBibliography` before freeze.

## Phase 7 — Headless experiment core

- Complete the environment, agent implementations, orchestration, persistence, manifests, and recovery behavior inside `src/resilient_agents/`.
- A whole experiment may contain many seeds; it finalizes once and optionally creates one automatic Git commit/push.
- **Gate:** full experiments run without the UI and produce auditable bundles.

## Phase 8 — Pilots and protocol freeze

- Measure runtime, variance, detector/adaptation behavior, failure modes, storage volume, and metric behavior.
- Freeze `protocol-v1.0` only after pilot questions are answered.
- Any later scientific change requires an explicit protocol amendment/version.

## Phase 9 — Minimal experiment management

- Add only the run registry, truthful lifecycle state, interruption/recovery, batch support, and current resource snapshot required by the frozen workflow.
- Filesystem run bundles remain the source of truth; any database/index is rebuildable cache.

## Phase 10 — Polished bounded application

- Implement the final dashboard as a thin local Streamlit layer unless a concrete pilot-derived requirement disproves that choice.
- Required workflows: New Experiment, Run/Monitor, History, Compare, Detailed Analysis, and Artifacts/Export.
- Make the UI self-explanatory using clear labels/helper text/units, concise tooltips and contextual help for non-obvious scientific concepts, consistent text+icon+semantic-color statuses, actionable empty/warning/error states, and clear next actions where useful.
- Add a concise pre-run resolved-configuration/validation summary so the user knows what will actually execute.
- After the final dashboard structure is stable, add lightweight first-run onboarding for the essential flow with Previous/Next/Skip/Finish plus replay from Help/Getting Started. Prefer native/lightweight Streamlit mechanisms and a local completion flag; do not add a heavyweight custom frontend tour framework without demonstrated need.
- Use proportionate confirmation only for destructive/high-impact actions and keep routine navigation/configuration friction low.
- Validate a real end-to-end multi-seed workflow through the user-facing application before the final experiment campaign.
- No scientific logic may be duplicated in Streamlit callbacks.
- **Gate:** application completion means the intended user workflow is truthful, tested, self-explanatory, accessible in normal use, polished, and uses the same frozen scientific core.

## Phase 11 — Final experiment campaign

- Execute the frozen matrix only after `protocol-v1.0` and the validated application workflow are ready.
- Use automatic provenance, storage, checksums, and one commit/push per whole experiment.
- Retain failed/cancelled/invalid/excluded runs with reasons.
- Large thesis-produced artifacts may use Git LFS; bibliography LFS/PDF objects remain upstream.

## Phase 12 — Statistical analysis and frozen evidence package

- Freeze the accepted final run set under `results/thesis-final/`.
- Produce reproducible summaries, intervals/effect sizes/diagnostics as justified, figures, tables, captions, and exports from frozen evidence only.
- Produce a versioned thesis/defense evidence package mapping RQs, protocol/method references, source IDs, result/run IDs, figures/tables, and planned claims.
- **Gate:** writing/presentation must not require ad-hoc reinterpretation of raw final runs.

## Phase 13 — Thesis writing and review

- Refresh current official thesis/template/submission guidance.
- Write the Greek Word thesis from citation-ready bibliography evidence and the frozen evidence package.
- Produce a review-ready `.docx`, incorporate supervisor/reviewer corrections when received, and revalidate affected claims/figures/citations.
- Perform final bibliography/guidance audit and freeze the final thesis deliverable.

## Phase 14 — Defense presentation

- Follow `docs/thesis/PRESENTATION_WORKFLOW.md` only after the final thesis is stable.
- Build the defense narrative and slide evidence map from the final thesis and frozen evidence.
- Produce the final PowerPoint `.pptx`, embedded speaker notes, and a separate full spoken Greek script.
- Validate application screenshots/demo fallback, factual consistency, PowerPoint rendering, and rehearsal timing.

## Phase 15 — Final audit and delivery

- Audit claims, citations, protocol versions, included/excluded runs, figures, cross-references, privacy, licensing, reproducibility, thesis/presentation consistency, and official required files.
- Confirm the final repository/application, thesis, PowerPoint, speaker material, and demo/delivery package are ready.

## Completion rule

The project is complete when the research question is answered with reliable reproducible evidence, the bounded local application supports the real experiment workflow, and the final thesis and defense package faithfully communicate the same frozen evidence. Production-platform engineering is not required. Concrete completion is tracked through task acceptance conditions in `TASKS.md`.
