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

- Decisions: `DEC-042` scientific refinement; `DEC-043` historical/superseded React/Vite exploration; authoritative `DEC-044` NiceGUI native application; `DEC-045` visual analytics; `DEC-046` novice-first compact UX.
- Single branch/PR: `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft #92. No parallel implementation branch or early merge.
- Trackers: #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/packaging.
- Project refinement progress: **2/8**. `T-520` is complete; current task is `T-521 READY`.
- PR CI run **346** validated the D0/NiceGUI checkpoint through documentation consistency, JSON validation, Python compile, locked environment, complete tests including `test_v11_runner.py`, and bibliography integrity.

## Continuity / interrupted-work audit

Known stale/interrupted areas have been reconciled rather than left only in chat:

- D0 runner integration is complete and focused-tested; historical `PilotProtocol` semantics remain unchanged.
- Active application direction is NiceGUI native; React/Vite and Streamlit are historical/superseded only.
- `PROJECT_CONTEXT`, `EXECUTION_WORKFLOW`, DEC-042, `MODEL_CANDIDATES`, requirements/decisions/constraints/open questions/roadmap/definition-of-done and thesis/application workflow docs now use the current scientific/application/delivery direction.
- `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` durably records the future Word/PowerPoint/ChatGPT/Codex/optional-Canva/manual-asset workflow without unlocking WP7.

## Scientific direction

Current candidate-v1.1 agents:

- **F0:** frozen Q-learning;
- **C0:** continual Q-learning from the same selected nominal checkpoint/base configuration;
- **D0:** information-limited Dyna-Q+ with learned model/planning/recency-directed re-exploration;
- R0 remains historical pilot evidence only for the current direction.

Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.

T-521 candidate v1.1 requires seven single-factor conditions, structural remap IDs, four fresh held-out final layouts, fresh precommitted final seeds, exact bounded D0-only `planning_steps`/`kappa` search, stable resolved-configuration identity/provenance and paired statistical support.

Multiple **approved** development/tuning configurations are allowed where the protocol declares them, always with multiple predefined roots and no single-run/best-seed cherry-picking. F0/C0 remain fixed unless explicitly reopened; D0 gets the bounded T-521/T-522 search. Final retained settings freeze before final outcomes are inspected.

Primary reporting: cumulative deficit, immediate degradation and terminal gap/performance. Recovery remains secondary/sensitivity. Paired effects + 95% CIs + explicit n/layout-aware views required; no composite resilience score/post-hoc favorable threshold.

## Application / experiment execution direction

- NiceGUI 3.16 native mode (`pywebview`) over UI-independent Python scientific/runtime services.
- Plotly = stored/final scientific figures; ECharts = real live/provisional telemetry; Mermaid = explanatory diagrams; AG Grid Community = analytical tables.
- T-530 provides truthful active-run DTOs/events/heartbeat/history/resources, safe control capabilities and read-only live GridWorld observation; visualization never changes scientific timing/actions/RNG.
- T-531 completes Dashboard/New Experiment/Runs/Compare/Artifacts with protocol-approved multiple configurations/settings, multiple seeds/repetitions, real live overlays and novice-first explanations.
- T-532 validates screenshots/browser/native Windows/PyInstaller `onedir + windowed`; root `run_app.bat` remains repository-checkout launcher.

After application acceptance, ordinary approved experiments should run directly from the finished application on the validated thesis machine without Codex/console commands. The backend owns resolved config, seeds, execution, persistence/provenance, finalization and guarded Git publication.

GitHub remains source of truth/PR/CI/evidence coordination. GitHub-hosted Actions are not automatically the validated final scientific execution machine. A self-hosted runner on the thesis machine is technically possible but optional and adds operational complexity; local Codex remains for code/protocol/debugging changes, not routine approved runs.

## WP7/WP8 future workflow

After T-610–T-613, T-511 acceptance and explicit user approval:

- Codex/repository automation owns traceable evidence maps, reproducible figures/tables and technical consistency.
- ChatGPT is preferred for Greek thesis drafting/review, slide narrative, notes/script and exact manual asset-placement instructions.
- Microsoft Word is the final `.docx` composition/inspection surface using styles, automatic TOC, caption fields, lists and cross-references.
- PowerPoint is the final `.pptx` inspection/rehearsal surface with speaker notes/Presenter View/media validation.
- Canva is optional visual polish only and any PPTX round-trip must be rechecked in PowerPoint.
- User captures selected real screenshots/GIF/video when requested; every capture receives an `ASSET-*` record specifying exact page/state/run/config, crop, target chapter/section/slide, caption/placement/size, evidence ID and static fallback.

## Accepted baseline

Python 3.12 + `uv`, project GridWorld, information boundary, deterministic RNG, filesystem run bundles, provenance/checksums and guarded publication remain authoritative. Testing stays risk-based/proportional; PR CI is the canonical full-suite guard.

`MariosGiannakaras/ThesisBibliography` remains canonical; accepted immutable import: `bibliography-integration-v3`.

## Still intentionally unfrozen

Exact D0 planning grid/selection, candidate-v1.1 freeze, exact fresh layouts/seeds, new final evidence, active-run runtime behavior, final novice-first UI/screenshots/native package, current official WP7 formatting/defense rules and final thesis/presentation deliverables remain unfrozen until their explicit gates pass.

## Exact next action

Execute `T-521`: implement the authoritative candidate-v1.1 schema, exact bounded D0-only tuning plan, fresh held-out layouts/seeds, structural condition IDs, resolved configuration/settings identity rules and paired effect/95% CI support. Keep final evidence and every `T-700+` task blocked.