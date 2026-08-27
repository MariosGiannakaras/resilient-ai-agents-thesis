# Project Context

## Status taxonomy

- **CONFIRMED:** established by the approved application, current explicit user direction, accepted repository decision, or validated evidence.
- **RESEARCH_REQUIRED:** requires current evidence before selection.
- **PROPOSED / CANDIDATE:** defined but not yet frozen for final evidence.
- **OPEN:** unresolved and genuinely needed later.
- **DEFERRED:** intentionally later and non-blocking now.
- **HISTORICAL_CONTEXT_ONLY:** retained for auditability, not active guidance.

## Project identity

This repository is the permanent source of truth for the thesis lifecycle:

> **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**

Official English title: **Comparison and Evaluation of Resilient AI Agents in Uncertain Environments**.

Confirmed academic context:

- University of West Attica, School of Engineering, Department of Informatics and Computer Engineering.
- Topic approved.
- Final thesis language is Greek and the required final thesis artifact is Microsoft Word (`.docx`) unless current official guidance later changes this.
- No current supervisor-specific correction or submission deadline blocks research/application work.
- WP7/WP8 thesis-writing/defense work remains blocked until the explicit pre-WP7 user approval gate in `TASKS.md` is satisfied.

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` is canonical for source discovery, originals/PDFs, OCR/conversion, canonical Markdown, scientific analysis, evidence verification, source selection and generated corpus exports.

This thesis repository consumes the verified generated corpus read-only. `research/bibliography/citation-ready/` is the formal automatic citation surface; other imported material remains internal research context unless promoted upstream and resynchronized.

Current accepted immutable consumer baseline: `bibliography-integration-v3`. Bibliography originals/PDF/LFS objects are not copied into this repository and generated bibliography content is never edited here for convenience.

## Scientific core — accepted baseline

The accepted implementation baseline remains:

- Python 3.12;
- `uv`, `pyproject.toml`, `.python-version`, committed `uv.lock`;
- UI-independent package `src/resilient_agents/`;
- project-owned Gymnasium-compatible GridWorld;
- explicit separation of evaluator ground truth from agent-visible information;
- independently derived deterministic RNG streams;
- versioned configuration/protocol contracts with fail-closed validation;
- filesystem-first run bundles with resolved config, provenance, checksums, events/results and lifecycle state;
- at most one guarded automatic Git commit/push per finalized whole experiment, never one per seed;
- large thesis-produced artifacts retained when useful under the configured Git LFS policy.

The user should not manually stage/move/publish routine experiment evidence.

## Historical v1.0 evidence

Historical `protocol-v1.0`, all finalized `FINAL-*` bundles, frozen v1.0 analysis and thesis-final evidence remain immutable real evidence. They are not deleted or rewritten by the current refinement.

Historical R0 robust-value-iteration pilot evidence is also preserved. Its accepted configuration showed approximately 96% nominal truncation, so it must not be reinstated unchanged in the new primary protocol.

## Current pre-WP7 scientific refinement

DEC-042 defines a versioned candidate `protocol-v1.1` path. `T-520` is complete; `T-521` is the current READY scientific task.

### Current candidate agent set

- **F0 — Frozen Q-learning:** common selected nominal checkpoint; post-change updates disabled.
- **C0 — Continual Q-learning:** same checkpoint/base configuration; online Q updates continue.
- **D0 — Dyna-Q+:** information-limited tabular learned-model planning with recency-directed re-exploration; no evaluator/change oracle.

R0 is historical pilot evidence only for the current direction.

Candidate-v1.1 preserves the accepted F0/C0 base configuration:

- alpha `0.5`;
- gamma `0.96875`;
- epsilon `0.125`;
- 512 nominal training episodes/layout;
- 16 pre-change episodes;
- 32 post-change episodes;
- evaluation horizon 48;
- 32 paired final root seeds.

D0-only `planning_steps` and `kappa` require a small predeclared development/tuning search in T-521 and non-final selection in T-522. Final settings are frozen before final outcomes are inspected.

The runner/application may execute multiple **approved** settings/configuration variants during development/tuning. Every configuration has a complete resolved identity/provenance and multiple predefined repetitions; single-run/best-seed cherry-picking is forbidden. Final evidence uses only the frozen configuration per retained regime.

### Candidate-v1.1 conditions and design

Seven single-factor conditions:

1. `nominal`;
2. `action-remap-2-swap`;
3. `action-remap-4-cycle`;
4. `action-failure-1of8`;
5. `action-failure-1of4`;
6. `observation-corruption-1of8`;
7. `observation-corruption-1of4`.

T-521 owns four fresh held-out final layouts, a fresh precommitted final seed bank, exact bounded D0 tuning values, protocol schema/firewall and paired statistical implementation.

Primary reporting: cumulative deficit, immediate degradation and terminal gap/performance. Recovery remains secondary/sensitivity with explicit `NO_DEGRADATION`, `RECOVERED` and `NOT_RECOVERED`. Paired effects, 95% CIs, explicit n and layout-aware views are required. No composite resilience score or post-hoc favorable threshold.

## Application architecture — current authority

DEC-044 supersedes the temporary React/Vite exploration and the historical Streamlit UI implementation.

Current application stack:

- **NiceGUI 3.16 native mode** (`pywebview`) as the Python-only desktop UI;
- Python application/runtime service between UI and scientific runner;
- Plotly for stored/final scientific figures;
- ECharts for real live/provisional telemetry;
- Mermaid for explanatory agent/experiment diagrams;
- AG Grid Community for analytical tables;
- root `run_app.bat` for repository-checkout launch;
- final Windows delivery target: validated NiceGUI/PyInstaller `onedir + windowed` folder requiring no Python/Node/browser interaction from the recipient.

`src/resilient_agents/` remains headless and usable without NiceGUI. No scientific execution logic belongs in UI callbacks.

T-530 must provide real active-run DTOs/status/events/heartbeat/history/resources, capability-based controls and a read-only live GridWorld observer proven not to alter actions/RNG. Historical runs without retained step traces display replay unavailable rather than synthetic reconstruction.

## Novice-first UI contract

DEC-046 requires the application to be understandable by a non-programmer with no prior RL/model/configuration knowledge while remaining scientifically precise.

Required behavior includes:

- human-readable primary labels and secondary technical IDs;
- concise helper text and info-icon/tooltips for non-obvious concepts;
- explanations of agents, uncertainty conditions, settings, units/ranges/consequences, metrics, aggregation and CI/error-bar semantics;
- approved-setting controls only, with progressive disclosure for advanced settings;
- readable resolved-configuration review before launch;
- truthful live GridWorld, event timeline, logs/metrics and compatible live model/settings overlays;
- semantic status using text + icon + accessible color, never color alone;
- actionable empty/loading/error/disabled/unavailable states;
- modern compact desktop/laptop density, consistent icons, restrained micro-interactions and purposeful animations;
- visualization animation/speed affects presentation only and never scientific timing, actions, seeds or RNG;
- short skippable/replayable onboarding, while every page remains usable without it.

The active navigation remains Dashboard, New Experiment, Runs, Compare and Artifacts.

## Experiment execution and GitHub boundary

The finished application is the normal user-facing execution surface for approved experiments on the validated thesis machine. A standard research/final run should not require Codex or console commands once the app/runtime path is complete.

Expected normal flow:

> select approved configuration in app -> review resolved config -> launch -> monitor real run/GridWorld/metrics -> persist provenance/results -> finalize whole experiment -> guarded Git commit/push -> compare/analyze/export

GitHub remains the repository/PR/CI/evidence source of truth. GitHub-hosted Actions are appropriate for deterministic CI, validators, small fixtures, analysis/artifact regeneration where scientifically valid and documentation checks, but they are **not automatically the validated machine for final stochastic evidence**. Final-v1.1 execution remains on the accepted thesis-machine path unless an explicit protocol amendment validates another execution environment.

A GitHub self-hosted runner on the thesis machine is technically possible, but it would still compute on that machine and adds runner/security/maintenance complexity; it is not the default requirement. The completed application is the simpler normal execution surface.

Codex on the thesis machine remains useful for code/protocol fixes, debugging, migrations or a scientifically required amendment. It should not be required merely to press Run for an already-approved experiment.

## Current lifecycle

Canonical task state is only in `docs/context/TASKS.md`.

Current refinement progress: **5/8** major milestones. Current repository task: `T-532 READY`; `T-522` remains the separate validated-thesis-machine scientific gate.

High-level order:

1. T-521 candidate-v1.1 schema/tuning/statistics (complete).
2. T-522 bounded non-final D0 tuning/pilot and freeze/amend/reject decision.
3. T-530 truthful active-run runtime service (complete).
4. T-531 complete NiceGUI research application (complete).
5. T-532 screenshots/render/native Windows packaging validation.
6. T-511 intended-user human E2E acceptance.
7. T-610–T-613 frozen v1.1 final execution, evidence freeze, paired analysis and final evidence package.
8. Explicit user approval before any T-700+ work.

No green CI, screenshot, packaged app or completed final analysis alone authorizes WP7.

## WP7/WP8 downstream ownership model

After explicit approval, current official thesis/submission/defense guidance is rechecked before writing. The frozen thesis/defense evidence package — not chat memory or ad-hoc raw-run browsing — becomes the scientific source for prose and presentation claims.

Planned responsibilities:

- **Codex/repository automation:** evidence maps, reproducible figures/tables, technical consistency, citation/result IDs, generated asset validation and legitimate code/data corrections.
- **ChatGPT:** Greek thesis drafting/restructuring/review, explanations, chapter coherence, slide narrative, Greek slide copy, speaker notes/full script and user-facing placement instructions.
- **Microsoft Word:** final thesis composition/inspection with heading styles, automatic TOC, captions, cross-references, lists of figures/tables, equations, pagination and final visual QA.
- **PowerPoint:** final defense inspection/rehearsal, embedded notes, Presenter View, animation/media validation and final `.pptx` QA.
- **Canva:** optional visual-polish tool only when it adds value; never scientific source of truth and any PPTX export is revalidated in PowerPoint.
- **User:** provide genuine external/supervisor input, review subjective academic wording/interpretation at explicit gates, capture selected real app screenshots/GIF/video when requested, place/approve them using an exact repository-generated placement guide, and perform final Word/PowerPoint visual/rehearsal checks.

The user should receive exact placement instructions for every manually captured application asset: target chapter/section or slide, intended purpose, crop/state to capture, caption/label, size/alignment guidance, evidence/run/config identity, and whether a static figure or animation fallback is required.

## Current authority

Use:

- `AGENTS.md` — project/Codex policy;
- `docs/context/TASKS.md` — concrete task/resume state;
- `docs/context/CURRENT_STATUS.md` — compact current status;
- `docs/context/CODEX_EXECUTION_PROMPT.md` — Goal-mode bootstrap;
- `docs/research/MODEL_CANDIDATES.md` — current F0/C0/D0/settings policy;
- `docs/context/IMPLEMENTATION_ROADMAP.md` — phase order;
- `docs/context/EXECUTION_WORKFLOW.md` — responsibility/handoff model;
- `docs/architecture/UI_INFORMATION_ARCHITECTURE.md` — application information/UX contract;
- `docs/thesis/THESIS_REQUIREMENTS.md` — thesis format/evidence requirements;
- `docs/thesis/PRESENTATION_WORKFLOW.md` — defense workflow;
- dedicated `DEC-*` files — accepted decisions and supersession history.

Historical documents remain useful for auditability only where their status explicitly says historical/superseded.
