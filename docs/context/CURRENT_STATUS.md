# Current Project Status

**Date:** 2026-08-27  
**Status:** Authoritative current-state summary

This file is intentionally compact. `docs/context/TASKS.md` is the canonical task ledger; detailed policy/history lives in routed decisions and evidence.

## Current execution state

- Historical accepted baseline includes `T-100` target-machine capability validation and `T-200` research framing through completed historical WP6 v1.0 evidence.
- `T-511` remains **USER_VALIDATION_REQUIRED**. Automated checks/screenshots/package validation never substitute for intended-user E2E acceptance.
- **Pre-WP7 user approval: NOT APPROVED.** Every `T-700+` WP7/WP8 task remains blocked.
- Existing `protocol-v1.0`, all finalized `FINAL-*` bundles and the current thesis-final evidence package are immutable historical baseline evidence.

## Active pre-WP7 refinement

- Decisions: `DEC-042` scientific refinement; historical `DEC-043` web-frontend exploration; superseding `DEC-044` native NiceGUI application; `DEC-045` visual analytics; `DEC-046` novice-first compact UX/presentation contract.
- Single branch: `feat/pre-wp7-protocol-v1.1-ui-rebuild`.
- Single draft integration PR: #92. Do not create parallel implementation branches or merge early.
- Trackers: #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/packaging.
- `T-513` governance is complete; master tracker remains **1/8** until another whole milestone satisfies acceptance.
- Current task: `T-520 IN_PROGRESS` — complete and validate D0 integration into the versioned headless runner path.
- NiceGUI migration work exists early on the same branch but does not make blocked T-530/T-531/T-532 complete.

## Continuity / interruption audit

A repository audit was performed specifically to detect work left half-finished by chat interruption or later instructions. Current findings are now durable in #87 and this file:

1. **D0 runner integration is unfinished, not lost.** Standalone D0, serialization, episode-preserving deployment and an initial v1.1 runner exist. A development-only `V11DevelopmentProtocol` adapter was added because the historical `PilotProtocol` correctly rejects D0; the historical validator must not be weakened. Focused v1.1 runner tests and a current-head green CI run are still required before T-520 can close.
2. **The framework migration is superseded cleanly at the source level.** The temporary React/Vite direction is retained only in DEC-043 history; active application files are NiceGUI. Historical Streamlit page files are removed from the active implementation. Any stale wording in docs/issues is cleanup work, not an alternative implementation path.
3. **The NiceGUI shell is intentionally incomplete.** It already contains a read model, five-page shell, historical v1.0 Plotly views, agent infographics and an empty ECharts live surface. Real runtime DTOs, live GridWorld, real live charts, full experiment configurator, final novice-first help/error states, screenshots and packaging remain explicit future acceptance work.
4. **Latest current-head CI did not reach Python compile/tests.** It failed at documentation validation because the compact Codex prompt lost required literal execution invariants. The prompt has now been repaired; a new current-head CI result must prove the scientific/application checkpoint rather than relying on earlier run 266.
5. **Master issue #87 had stale Streamlit wording.** It has been reconciled to NiceGUI/DEC-044/045/046 and now contains a dedicated continuity checklist so future sessions cannot silently skip these unfinished items.

No evidence was found of a second active React/Vite frontend project remaining in the branch. The remaining incomplete work is tracked explicitly rather than being assumed complete.

### Scientific direction

- Retain F0 frozen Q-learning and C0 continual Q-learning from the common selected nominal checkpoint.
- Add D0 Dyna-Q+ using only agent-visible interaction information; evaluator-only information remains forbidden.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.
- Candidate v1.1 keeps seven single-factor conditions, uses `action-remap-2-swap` and `action-remap-4-cycle`, four fresh held-out final layouts and a fresh precommitted final seed bank.
- D0-only planning parameters require bounded development/tuning selection and non-final validation before freeze.
- Primary reporting: cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity; paired effects + 95% CIs are required. No composite resilience score or post-hoc favorable threshold.
- Preserve R0 pilot evidence; do not reinstate its accepted construction unchanged and do not add deep RL merely to increase model count.

### Application direction

- `DEC-044` supersedes the React/Vite application choice after standalone delivery became a first-class requirement.
- Framework: **NiceGUI 3.16 native mode** (`pywebview`) over the Python scientific/runtime layers. No active Node/npm/Vite or Streamlit application remains.
- Root `run_app.bat` launches the locked Python entry point in its own native window. `THESIS_APP_BROWSER_MODE=1` is CI/browser-render mode only.
- Final delivery target: validated NiceGUI/PyInstaller **onedir + windowed** Windows folder requiring no Python/Node/browser interaction from the recipient.
- `src/resilient_agents/` stays headless/UI-independent. T-530 provides the truthful Python active-run/runtime service and read-only GridWorld observer.
- Unsupported lifecycle controls remain explicit. Visualization cadence never changes scientific timing/actions/RNG.
- Historical runs without retained step trace display replay unavailable; never synthesize a trajectory.

### Novice-first UX direction

Per `DEC-046`, the application must be understandable by a non-programmer with no prior RL/model/configuration knowledge while remaining scientifically precise.

- Use plain-language labels with technical IDs as secondary reproducibility detail.
- Explain agents, uncertainty conditions, metrics, units, ranges and setting consequences through concise helper text, info icons/tooltips and progressive disclosure.
- Show a readable resolved configuration before launch and actionable explanations for invalid/disallowed combinations.
- Use consistent text + icon + semantic color statuses; color is never the sole signal.
- Keep the interface modern and compact rather than sparse/oversized; use cards/tables/tabs/drawers/expanders to preserve density without hiding required information.
- Use restrained micro-interactions and purposeful animations for hover/focus/selection/status/chart/GridWorld feedback; animation must never imply scientific progress or alter execution timing.
- Keep onboarding skippable/replayable, but every page must remain understandable without it.
- Empty/loading/error/disabled/unavailable states must say what happened and what the user can do next.

### Visual analytics direction

Per `DEC-045`:

- **Plotly:** stored scientific comparisons and thesis/presentation-ready figures. Historical v1.0 error bars remain labelled SD until real paired CI artifacts exist.
- **ECharts:** real live/provisional telemetry and compatible multi-agent/settings overlays.
- **Mermaid:** F0/C0/D0 and experiment/information-boundary infographics.
- **AG Grid Community:** run/result/artifact inspection tables.

Live/provisional telemetry, finalized runs and versioned analysis/evidence are distinct data classes; the UI never promotes live values into final evidence.

## Current application checkpoint

Committed but not yet accepted:

- NiceGUI native dependency/application entry point and Python-only lock workflow;
- `src/app/state.py` truthful read-only workspace facade;
- `src/app/visualizations.py` Plotly/ECharts/Mermaid builders;
- NiceGUI Dashboard/New Experiment/Runs/Compare/Artifacts shell;
- real historical v1.0 comparisons from stored `aggregated_summary.csv`;
- F0/C0/D0 explanatory infographics and migrated onboarding;
- live telemetry surface intentionally empty until T-530 provides real DTOs;
- historical Streamlit pages and temporary React/Vite scaffold removed.

Current-head lock/import/tests/browser render must pass before this checkpoint is called validated. Live GridWorld/runtime integration, screenshots and Windows onedir packaging remain incomplete.

## Accepted repository / Codex baseline

- Python 3.12 + `uv`, project-owned Gymnasium GridWorld, explicit information boundary, deterministic RNG streams, filesystem-first finalized run bundles, provenance/checksums and guarded publication remain authoritative.
- Native Windows CPU execution remains the required scientific baseline; the Radeon RX 570 is not a validated scientific-compute backend.
- Invalid/ambiguous required scientific, provenance or lifecycle state fails closed. Never fabricate data, state, progress, logs, metrics or evidence.
- Testing remains risk-based/proportional; PR CI is the canonical full-suite guard and pilot/final matrices are never CI tests.
- Codex startup: `AGENTS.md`, `docs/context/TASKS.md`, this file; then task-specific progressive reading. Bootstrap: `docs/context/CODEX_EXECUTION_PROMPT.md`.

## Bibliography baseline

`MariosGiannakaras/ThesisBibliography` remains canonical. The accepted immutable import is `bibliography-integration-v3`; bibliography originals are not edited here.

## Still intentionally unfrozen

D0 planning parameters, candidate `protocol-v1.1` freeze, fresh v1.1 final layouts/seeds, new final evidence, full active-run runtime behavior, final novice-first UI/screenshots and Windows packaged delivery remain intentionally unfrozen/unaccepted until their explicit dependency and validation gates pass.

## Exact next action

1. Obtain a current-head CI run after the repaired Codex prompt and confirm documentation validation now reaches compile/locked environment/tests.
2. Add focused `V11DevelopmentProtocol`/`V11ExperimentRunner` tests and complete T-520 acceptance without changing historical `PilotProtocol` semantics.
3. Reconcile #88/TASKS after T-520 evidence is green, then proceed dependency-valid T-521/T-530.
4. Live GridWorld/charts may attach only to real T-530 runtime observer data.
5. Do not start `T-700+`.
