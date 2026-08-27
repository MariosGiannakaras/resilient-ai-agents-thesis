# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` is the canonical ledger; use progressive task-specific reading for detailed decisions/evidence.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine capability validation and `T-200` research framing through completed historical WP6 v1.0 evidence.
- Existing `protocol-v1.0`, finalized `FINAL-*` bundles, R0 pilot evidence and historical thesis-final evidence are immutable baseline evidence.
- `T-511` remains **USER_VALIDATION_REQUIRED**; automated screenshots/package checks do not replace intended-user E2E acceptance.
- **Pre-WP7 approval: NOT APPROVED.** All `T-700+` execution remains blocked.

## Active refinement

- Decisions: DEC-042 scientific refinement; DEC-043 historical/superseded React/Vite exploration; authoritative DEC-044 NiceGUI native application; DEC-045 visual analytics; DEC-046 novice-first compact UX.
- Single branch/PR: `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft #92. No parallel implementation branch or early merge.
- Trackers: #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/packaging.
- Progress: **2/8** major milestones. `T-520` complete; current task `T-521 READY`.
- PR CI run **346** validated the T-520 D0 code checkpoint. PR CI run **376** validated the subsequent continuity/documentation reconciliation: documentation consistency, JSON validation, Python compile, locked environment, complete tests and bibliography integrity all passed.

## Continuity / interruption audit

Known interrupted/stale areas are now durably reconciled:

- D0 runner integration is complete; historical `PilotProtocol` semantics remain unchanged.
- NiceGUI native is the active application; React/Vite and Streamlit are historical/superseded only.
- `PROJECT_CONTEXT`, `EXECUTION_WORKFLOW`, DEC-042, `MODEL_CANDIDATES`, requirements/decisions/constraints/open questions/roadmap/definition-of-done, UI architecture and thesis/application workflow docs use the current scientific/application/delivery direction.
- Stable requirement IDs remain stable; current requirements append new IDs rather than silently repurposing old references.
- `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` records future Word/PowerPoint/ChatGPT/Codex/optional-Canva/manual-asset ownership without unlocking WP7.

## Scientific direction

Candidate v1.1 agents: F0 frozen Q-learning; C0 continual Q-learning from the same selected checkpoint/base configuration; D0 information-limited Dyna-Q+ learned-model/planning/recency-directed re-exploration. R0 remains historical pilot evidence only.

Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.

T-521 requires seven single-factor conditions, structural remap IDs, four fresh held-out final layouts, fresh precommitted final seeds, exact bounded D0 `planning_steps`/`kappa` search, stable resolved-configuration identity/provenance and paired statistical support.

Multiple **approved** development/tuning configurations are allowed where predeclared, always with multiple predefined roots and no single-run/best-seed cherry-picking. F0/C0 stay fixed unless explicitly reopened; final retained settings freeze before final outcomes.

Primary reporting: cumulative deficit, immediate degradation and terminal gap/performance. Recovery secondary/sensitivity. Paired effects + 95% CIs + explicit n/layout-aware views required; no composite resilience score/post-hoc favorable threshold.

## Application / execution direction

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services.
- Plotly = stored/final figures; ECharts = real live/provisional telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- T-530 supplies truthful active-run DTOs/events/history/resources, safe controls and read-only live GridWorld; visualization never changes scientific timing/actions/RNG.
- T-531 completes Dashboard/New Experiment/Runs/Compare/Artifacts with approved multiple configurations/settings, repetitions, live overlays and novice-first explanations.
- T-532 validates screenshots/browser/native Windows/PyInstaller `onedir + windowed`; root `run_app.bat` remains checkout launcher.

After acceptance, ordinary approved experiments run directly from the desktop application on the validated thesis machine without Codex/console commands. Backend owns resolved config, seeds, execution, persistence/provenance, finalization and guarded Git publication.

GitHub remains source-of-truth/PR/CI/evidence coordination. GitHub-hosted Actions are not automatically the validated final stochastic experiment machine. A thesis-machine self-hosted runner is optional and adds operational complexity; local Codex remains for code/protocol/debugging changes, not routine frozen runs.

## WP7/WP8 future workflow

After final evidence, T-511 acceptance and explicit approval: Codex/repository automation owns traceable evidence/assets/technical checks; ChatGPT is preferred for Greek thesis/slide drafting and placement guidance; Word is final `.docx` QA; PowerPoint is final `.pptx` QA/rehearsal; Canva is optional polish. Every user-captured screenshot/GIF/video receives an exact `ASSET-*` record with state/run/config, crop, target section/slide, caption/placement/size, evidence ID and static fallback.

## Accepted baseline

Python 3.12 + `uv`, project GridWorld, information boundary, deterministic RNG, filesystem run bundles, provenance/checksums and guarded publication remain authoritative. Testing stays risk-based/proportional; PR CI is the canonical full-suite guard.

`MariosGiannakaras/ThesisBibliography` remains canonical; accepted immutable import: `bibliography-integration-v3`.

## Still intentionally unfrozen

Exact D0 planning grid/selection, candidate-v1.1 freeze, exact fresh layouts/seeds, new final evidence, active-run runtime behavior, final novice-first UI/screenshots/native package, current official WP7 formatting/defense rules and final thesis/presentation deliverables remain unfrozen until explicit gates pass.

## Exact next action

Execute `T-521`: authoritative candidate-v1.1 schema, exact bounded D0 tuning plan, fresh layouts/seeds, structural condition IDs, resolved configuration identity rules and paired effect/95% CI support. Keep final evidence and every `T-700+` task blocked.