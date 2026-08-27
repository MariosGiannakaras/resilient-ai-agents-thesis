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

- Decisions: DEC-042 scientific refinement; DEC-043 historical/superseded React/Vite exploration; DEC-044 NiceGUI native application; DEC-045 visual analytics; DEC-046 novice-first compact UX; **DEC-047 broader agent comparison + human-readable agent naming**.
- Single branch/PR: `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft #92. No parallel implementation branch or early merge.
- Trackers: #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/packaging.
- Progress: **2/8** major milestones. `T-520` complete; current task is now **`T-523 READY`**. `T-521` is blocked on T-523.
- PR CI run **376** validated the pre-DEC-047 continuity/documentation reconciliation: documentation consistency, JSON validation, Python compile, locked environment, complete tests and bibliography integrity passed. DEC-047/T-523 changes require a new current-head CI before their checkpoint is called validated.

## Thesis framing correction

The thesis is about **resilient AI agent strategies operating under uncertainty and environmental change**. GridWorld is the controlled experimental testbed and visualization environment used to make mechanisms, disturbances, trajectories and comparisons reproducible/understandable. It is not the thesis subject or the reason the agent set is selected.

## Scientific direction

DEC-047 broadens the candidate v1.1 comparison from three technical roles to **five main user-facing agent strategies**:

1. **Fixed Q-Learning** — learned nominal policy, no post-change learning (historical technical identity F0).
2. **Adaptive Q-Learning** — ordinary off-policy continual Q-learning (historical technical identity C0).
3. **SARSA** — on-policy continual model-free learning.
4. **Dyna-Q** — online learning plus an empirical learned model and planning, without recency bonus.
5. **Dyna-Q+** — learned-model planning plus directed re-exploration of long-untried actions (historical technical identity D0).

Why these five: they isolate no adaptation, off-policy model-free adaptation, on-policy model-free adaptation, learned-model planning, and planning plus explicit change-seeking re-exploration. Plain Dyna-Q is required to separate the contribution of planning from Dyna-Q+'s recency bonus.

**Reference-only strategies:** Random Agent may be used as a lower scale/correctness fixture; a nominal/fully-informed planner may be used as a clearly privileged scale/debug reference. They are not equivalent scientific agents and are excluded from fair rankings.

**Robust-planning branch:** historical R0 remains negative/diagnostic pilot evidence. A redesigned Robust Planner may become a conditional sixth comparator only if a small predeclared non-final nominal-viability/fairness/runtime gate passes. Do not reinstate R0 unchanged.

Preserve Fixed/Adaptive Q-Learning alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and current target 32 paired final roots unless an explicit later evidence-backed amendment changes the matrix.

T-523 must implement/validate SARSA and plain Dyna-Q with the same agent-visible information boundary, deterministic/serializable state and focused correctness tests, then integrate them into the versioned runner/configuration identity surface. T-521 then owns the authoritative five-agent candidate-v1.1 schema, bounded tuning, fresh layouts/seeds and paired statistics.

Multiple approved development/tuning configurations remain stage-controlled: stable identity/hash/provenance, multiple predefined roots, no single-run/best-seed selection, final retained settings frozen before final outcomes.

Primary reporting remains cumulative deficit, immediate degradation and terminal gap/performance. Recovery remains secondary/sensitivity. Paired effects + 95% CIs + explicit n/layout-aware views required; no composite resilience score/post-hoc favorable threshold.

## User-facing naming

Opaque technical IDs are not primary UI terminology. The selector is **Agent strategy** and ordinary users see the five full names above plus one-sentence explanations and mechanism badges such as `Does not adapt`, `Model-free`, `On-policy`, `Uses planning`, `Re-explores for change`.

Historical/internal IDs such as F0/C0/D0, method schema IDs and configuration hashes appear only in **Technical details / Reproducibility**. The same human-readable names must propagate to Runs, Compare, chart legends, screenshots, thesis-facing exports and presentation assets.

## Application / execution direction

- NiceGUI 3.16 native/pywebview over UI-independent Python runtime/scientific services.
- Plotly = stored/final figures; ECharts = real live/provisional telemetry; Mermaid = explanations; AG Grid Community = analytical tables.
- T-530 supplies truthful active-run DTOs/events/history/resources, safe controls and read-only live GridWorld; visualization never changes scientific timing/actions/RNG.
- T-531 completes Dashboard/New Experiment/Runs/Compare/Artifacts with approved configurations/settings, repetitions, live overlays and novice-first explanations using the new human-readable agent strategy names.
- T-532 validates screenshots/browser/native Windows/PyInstaller `onedir + windowed`; root `run_app.bat` remains checkout launcher.

After acceptance, ordinary approved experiments run directly from the desktop application on the validated thesis machine without Codex/console commands. Backend owns resolved config, seeds, execution, persistence/provenance, finalization and guarded Git publication.

GitHub remains source-of-truth/PR/CI/evidence coordination. GitHub-hosted Actions are not automatically the validated final stochastic experiment machine. A thesis-machine self-hosted runner is optional; local Codex remains for code/protocol/debugging changes, not routine frozen runs.

## WP7/WP8 future workflow

After final evidence, T-511 acceptance and explicit approval: Codex/repository automation owns traceable evidence/assets/technical checks; ChatGPT is preferred for Greek thesis/slide drafting and placement guidance; Word is final `.docx` QA; PowerPoint is final `.pptx` QA/rehearsal; Canva is optional polish. Every user-captured screenshot/GIF/video receives an exact `ASSET-*` record with state/run/config, crop, target section/slide, caption/placement/size, evidence ID and static fallback.

## Accepted baseline

Python 3.12 + `uv`, project GridWorld testbed, strict information boundary, deterministic RNG, filesystem run bundles, provenance/checksums and guarded publication remain authoritative. Testing stays risk-based/proportional; PR CI is the canonical full-suite guard.

`MariosGiannakaras/ThesisBibliography` remains canonical; accepted immutable import: `bibliography-integration-v3`.

## Still intentionally unfrozen

SARSA/Dyna-Q implementation checkpoint, exact SARSA/Dyna planning tuning surfaces, candidate-v1.1 freeze, conditional Robust Planner decision, exact fresh layouts/seeds, new final evidence, active-run runtime behavior, final novice-first UI/screenshots/native package, current official WP7 formatting/defense rules and final thesis/presentation deliverables remain unfrozen until explicit gates pass.

## Exact next action

Execute **T-523**: implement/validate SARSA and Dyna-Q, integrate five main agent strategies/reference fixtures/user-facing identities, and measure bounded runtime feasibility. Then execute T-521. Keep final evidence and every `T-700+` task blocked.