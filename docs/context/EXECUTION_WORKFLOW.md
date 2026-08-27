# Execution and Review Workflow

## Operating model

The user provides goals, genuinely non-objective academic/product choices, observed application behavior, later supervisor/Department feedback and private material when actually required. The user is not the routine Git/CI/task-bookkeeping operator.

Codex executes bounded repository work from actual state, performs objective diff review, uses GitHub CI as the canonical full-suite implementation guard, fixes failures/findings and reconciles tasks/docs. This current pre-WP7 package stays on the single branch/PR declared in `TASKS.md` and must not be merged early merely because an intermediate checkpoint is green.

ChatGPT is used for independent research/review and, after the explicit WP7 approval gate, becomes the preferred Greek writing/narrative/user-instruction layer. It is not a mandatory stop after every technical checkpoint.

Normal implementation flow:

> persistent goal -> canonical task registry -> bounded dependency-valid scope -> implementation -> targeted checks -> PR CI/objective review -> corrections -> durable reconciliation -> next allowed scope

## Session continuation and quota recovery

Every Codex session starts with exactly:

1. `AGENTS.md`;
2. `docs/context/TASKS.md`;
3. `docs/context/CURRENT_STATUS.md`.

Before selecting work, inspect Git status/current branch/recent commits and PR/check state. Resume valid `IN_PROGRESS` work first. Repository evidence wins over stale/truncated session memory. Never discard useful branch/uncommitted work without inspection.

The tracked entrypoint is `docs/context/CODEX_EXECUTION_PROMPT.md`. Goal mode keeps the long-horizon objective active while `TASKS.md` controls what is actually dependency-valid. Routine task/PR/CI boundaries are not reasons to ask the user to say “continue”.

Checkpoint commits are allowed for recovery. Coherent work should still reach `main` as a small number of meaningful permanent commits when the governing acceptance/approval gates permit it.

## Testing / CI discipline

Validation is risk-based and proportional.

- During implementation, run the smallest deterministic checks that protect the changed acceptance condition or material scientific/reliability boundary.
- Add tests for known-answer behavior, information isolation, determinism/serialization, configuration validation, lifecycle truthfulness and concrete regressions.
- No arbitrary coverage target, broad fuzz/mutation project, exhaustive parameter matrix or pilot/final campaign as CI testing.
- GitHub PR CI is the canonical complete repository check. Do not repeatedly duplicate successful full-suite runs locally.
- On failure, inspect the narrowest failing step first. On success, record the result and continue.
- Required scientific/provenance/configuration state fails closed; optional unavailability is explicit and never treated as affirmative evidence.

## Bibliography flow

All new source discovery/original PDFs/OCR/conversion/scientific source analysis belong to `MariosGiannakaras/ThesisBibliography`. This repository consumes only committed immutable generated corpus versions. Formal citation trust is limited to `research/bibliography/citation-ready/`.

## Scientific implementation and model/settings flow

Current candidate-v1.1 scientific direction is maintained in `docs/research/MODEL_CANDIDATES.md`:

- F0 frozen Q-learning;
- C0 continual Q-learning;
- D0 Dyna-Q+;
- R0 preserved as historical pilot evidence only for the current direction.

Development/tuning may contain multiple **approved resolved configurations** per regime. Each configuration has stored identity/provenance and multiple predefined root seeds; single-run/best-seed selection is forbidden. F0/C0 base values remain the accepted candidate configuration unless explicitly reopened. D0-only planning settings are selected from the predeclared bounded T-521/T-522 non-final search. Final settings are frozen before final outcomes are inspected.

## Application implementation handoff

Historical Streamlit and temporary React/Vite surfaces are superseded. The authoritative application is NiceGUI native mode per DEC-044, with analytics per DEC-045 and novice-first UX per DEC-046.

The scientific core remains UI-independent. T-530 owns the Python runtime/service boundary for real active-run status/events/heartbeat/history/resources, safe control capabilities and read-only live GridWorld observation. NiceGUI consumes those contracts and must never fabricate scientific execution state.

T-531 completes Dashboard, New Experiment, Runs, Compare and Artifacts. The UI exposes protocol-approved settings and configuration variants, explains their meaning, supports multiple seeds/repetitions and compatible comparisons, and distinguishes development/tuning/live-provisional/final evidence clearly.

T-532 validates root screenshots, browser rendering, native Windows behavior and the cleaned NiceGUI/PyInstaller `onedir + windowed` delivery folder. T-511 remains a human end-to-end acceptance gate; automated rendering never substitutes for it.

## Where approved research runs execute

Once the application/runtime is complete, **ordinary approved experiments should not require Codex or console commands**. The intended path is the validated desktop application on the accepted thesis machine:

> choose approved model/configuration/condition/seeds -> review resolved configuration -> launch -> monitor real live state/GridWorld/metrics -> finalize evidence/provenance -> guarded Git publication -> compare/analyze/export

The application/backend therefore becomes the normal research execution surface after acceptance.

### GitHub-hosted Actions

GitHub remains the repository, PR, CI and evidence coordination surface. GitHub-hosted runners are suitable for:

- repository/documentation/config validators;
- deterministic unit/integration/smoke tests;
- bounded browser/render checks;
- reproducible analysis/artifact regeneration when the inputs are already frozen and the analysis contract allows it;
- packaging/build automation that does not substitute for native target-machine validation.

GitHub-hosted runners are **not automatically equivalent to the accepted thesis machine**. Final-v1.1 stochastic evidence remains on the validated thesis-machine execution path unless an explicit protocol amendment revalidates a different environment.

### Optional self-hosted GitHub runner

A self-hosted GitHub Actions runner could technically be installed on the thesis Windows machine, allowing a workflow to be triggered from GitHub while computation still occurs locally. This is optional, not the default architecture: it adds runner/service/security/update complexity without removing the need for the physical machine. The finished desktop application is the simpler user-facing run surface.

### When local Codex is still needed

Codex on the thesis machine is useful when code/protocol changes are required: debugging a real native issue, implementing a scientifically justified amendment, repairing packaging, or modifying analysis/runtime behavior. It should not be required merely to execute an already-approved configuration once the app is complete.

## Final-v1.1 evidence flow

The normal final sequence remains gated:

1. T-521 candidate-v1.1 definition/statistics.
2. T-522 bounded non-final D0 tuning/pilot and freeze/amend/reject.
3. T-530/T-531/T-532 application/runtime/delivery completion.
4. T-511 intended-user acceptance.
5. T-610 frozen v1.1 final matrix on the approved execution path.
6. T-611 evidence completeness/integrity freeze.
7. T-612 predeclared paired analysis/sensitivity diagnostics.
8. T-613 final figures/tables/exports + thesis/defense evidence package.

A run ID is one whole experiment and may contain many root seeds/episodes. Failed/cancelled/interrupted/invalid/non-recovery outcomes remain attributable. Successful finalization may create at most one guarded Git commit/push for the whole experiment.

## Mandatory pre-WP7 gate

Application/evidence completion does not authorize writing. After T-613 and T-511 are satisfactory, the assistant may ask whether WP7 may start. Only an explicit user approval unlocks T-700+.

Planning/documentation of the future workflow is allowed before that gate; thesis prose/result interpretation intended as final writing is not.

## WP7/WP8 tool and responsibility handoff

Detailed future ownership lives in `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` once present; `TASKS.md` remains the only task-status ledger.

High-level split:

- **Repository/Codex:** evidence maps, reproducible figures/tables, technical/citation/result consistency, traceable asset manifests and legitimate code/data fixes.
- **ChatGPT:** Greek thesis drafting/restructuring/review, explanatory wording, chapter coherence, slide narrative, speaker notes/full script and exact user-facing manual placement instructions.
- **Microsoft Word:** final `.docx` composition/inspection, styles/automatic TOC, captions, cross-references, lists, equations, pagination and visual QA.
- **PowerPoint:** final `.pptx` inspection/rehearsal, speaker notes/Presenter View, media/animation validation and presentation QA.
- **Canva:** optional visual-polish only; never the source of scientific claims/data and every PPTX round-trip is revalidated in PowerPoint.
- **User:** external/supervisor input, subjective academic review gates, selected real app screenshots/GIF/video capture, manual insertion where required using exact placement instructions, and final Word/PowerPoint/rehearsal inspection.

The user should not have to infer where a manually captured image belongs. For every requested screenshot/GIF/video, the repository workflow must provide: asset ID, exact app state/run/config to capture, crop/content requirements, target thesis chapter/section and/or slide, intended claim/purpose, caption, size/alignment guidance, source/evidence identifiers, and a static fallback where animation cannot be embedded reliably.

## Thesis writing/review handoff

Before T-710, T-700 rechecks current official Department/University Word/citation/submission/defense requirements and records anything that supersedes the current snapshot. T-701 may review user-supplied example theses as contextual presentation/structure references only.

T-710 drafts the Greek thesis from citation-ready bibliography plus the frozen T-613 evidence package. Quantitative/result claims must map to result/figure/table IDs and external factual claims to verified sources. Negative/null/unexpected results and limitations remain explicit.

T-711 creates the review-ready Word artifact and a placement/QA register. T-712 incorporates real supervisor/reviewer corrections and revalidates every affected claim/citation/figure/table/method description. T-713 freezes the final thesis only after Word-level cross-reference/caption/TOC/formatting and evidence checks pass.

## Defense handoff

T-720 creates the defense narrative, slide outline and evidence map from the final thesis/evidence. T-721 creates the PowerPoint, embedded speaker notes and separate full spoken Greek script. T-722 validates PowerPoint rendering, factual/numerical consistency, official timing/content requirements, rehearsal and demo/screenshot/video fallback.

See `docs/thesis/PRESENTATION_WORKFLOW.md` for the detailed presentation contract.

## Final audits

T-800 rechecks bibliography/citations/current official guidance. T-801 audits reproducibility, protocol/results, privacy/licensing, repository/docs/thesis/defense consistency. T-802 confirms final delivery readiness.

## Documentation rule

Every material architecture/science/tool/ownership/task change reconciles affected active documents in the same branch checkpoint. Historical records may remain only when clearly labelled historical/superseded. Generated bibliography content is never hand-edited for consistency.