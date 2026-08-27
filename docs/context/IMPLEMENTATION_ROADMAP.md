# Implementation Roadmap

The roadmap is phase-gated for thesis completion, scientific adequacy, reproducibility and bounded engineering. `TASKS.md` is the concrete task/status/resume registry; roadmap phases do not override its current state.

## Completed foundation

The following baseline is already implemented/validated and remains reusable:

1. Project/bibliography ownership, immutable corpus consumer and provenance.
2. Actual-machine capability inventory; Python 3.12 + `uv` locked environment.
3. Source-traceable research framing and project-owned Gymnasium GridWorld with deterministic information/RNG contracts.
4. Resilience/degradation/recovery metric primitives and known-answer fixtures.
5. Historical F0/C0/R0 implementation, pilot protocols, headless runner and reproducible analysis.
6. Historical frozen `protocol-v1.0` final evidence and thesis-final artifact package.
7. Canonical Codex task registry, documentation governance and interruption recovery.

Historical v1.0 evidence remains immutable; current refinement is versioned rather than retroactively rewriting it.

## Current pre-WP7 refinement

### Phase R1 — D0 integration — COMPLETE

- Add D0 Dyna-Q+ as the third scientifically distinct current comparator beside F0 frozen and C0 continual Q-learning.
- Preserve strict agent-visible/evaluator-only information boundary and deterministic state/RNG serialization.
- Preserve learned Dyna state across evaluation episodes while reseeding episode-local RNG correctly.
- Keep historical `PilotProtocol` semantics unchanged; use a versioned development-only v1.1 adapter until the real candidate schema exists.
- **Gate passed:** focused F0/C0/D0 runner tests + PR CI run 346 are green (`T-520`).

### Phase R2 — Candidate protocol-v1.1 and statistics — CURRENT

- Build authoritative candidate `protocol-v1.1`; it must not authorize final evidence.
- Keep validated F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.
- Define a small predeclared search only for D0-specific `planning_steps`/`kappa`.
- Keep seven single-factor conditions; structural remap IDs are `action-remap-2-swap` and `action-remap-4-cycle`.
- Generate/validate four fresh held-out final layouts and a fresh precommitted final seed bank before any new final outcomes can be inspected.
- Primary analysis: cumulative deficit, immediate degradation, terminal performance/gap. Recovery remains secondary/sensitivity.
- Implement paired effects + 95% confidence intervals, explicit n and layout-aware views; no unlabeled composite resilience score or post-hoc favorable threshold.
- **Gate:** T-521 complete before non-final tuning/pilot.

### Phase R3 — Non-final D0 tuning and v1.1 freeze

- Execute only bounded development/tuning/pilot evidence defined by candidate v1.1.
- Select D0-specific parameters from predeclared non-final evidence only.
- Validate runtime/informativeness/failure/non-recovery behavior and retain unsuccessful outcomes.
- Freeze, amend or reject candidate v1.1 before any final reserve is executed.
- **Gate:** T-522.

### Phase A1 — Truthful active-run runtime service

- Add a UI-independent Python runtime registry/service, separate from NiceGUI and scientific execution.
- Expose real queued/running/completed/failed/cancelled/interrupted state, heartbeat/progress/events/history/resources.
- Provide a read-only live GridWorld observer proven not to alter agent information, actions, timing or RNG.
- Support stop/cancel/restart only where safe; unsupported pause/resume/control capabilities remain explicit.
- Preserve unfinished/failed/cancelled/interrupted runs without corrupting finalized registry semantics.
- **Gate:** T-530.

### Phase A2 — Native polished thesis application

DEC-044/045/046 are authoritative.

- **Framework:** NiceGUI 3.16 native mode (`pywebview`) over the same Python core/runtime services. No active Streamlit or React/Vite frontend.
- **Navigation:** Dashboard, New Experiment, Runs, Compare, Artifacts.
- Dashboard: active/recent state, warnings, protocol status, resource snapshot, quick actions.
- New Experiment: F0/C0/D0 explanations; approved layout/condition/seeds/repetitions/settings; progressive advanced options; readable resolved-config review before launch.
- Runs: active/history/detail, smooth live GridWorld, event timeline, real logs/metrics and compatible live model/settings overlays.
- Compare: scientifically compatible selection, distributions, paired effects/CIs, counts and condition/layout breakdowns.
- Artifacts: real figures/tables/CSV/JSON/HTML/provenance preview/export and thesis/presentation-ready views.

Visual roles:

- Plotly — stored scientific/thesis-ready figures.
- ECharts — live/provisional animated telemetry.
- Mermaid — agent/experiment/information-flow infographics.
- AG Grid Community — analytical tables.

Novice-first UX:

- Plain-language primary labels; technical IDs secondary.
- Tooltips/info icons/contextual explanations, visible units/ranges/consequences, progressive disclosure.
- Explain agents, uncertainty conditions, metrics, aggregation and error-bar/CI semantics.
- Semantic text + icon + accessible color statuses; color never sole signal.
- Actionable empty/loading/error/disabled/unavailable states.
- Modern compact hierarchy rather than oversized decorative layouts.
- Restrained hover/focus/selection micro-interactions and purposeful GridWorld/chart/status animations; animation never fabricates scientific progress and remains understandable with reduced motion where practical.
- Short skippable/replayable onboarding, but normal pages remain understandable without it.
- **Gate:** T-531 and later T-511 intended-user validation.

### Phase A3 — Screenshots and standalone Windows delivery

- Root `ui-screenshots/` stores stable accepted review screenshots, including useful help/status/empty/error states; screenshots are not scientific evidence.
- Bounded CI browser rendering uses the same NiceGUI pages and deterministic labelled fixtures only where needed for chrome/state validation.
- Validate native Windows launch/close/restart and pywebview/WebView2 behavior on the target machine.
- Produce/validate NiceGUI/PyInstaller `onedir + windowed` cleaned application folder with safe writable data paths.
- Recipient should not need Python/Node/browser/visible terminal interaction.
- Root `run_app.bat` remains the repository-checkout launcher.
- **Gate:** T-532 followed by T-511 human E2E.

## New final evidence path

Only after frozen v1.1 and application acceptance:

1. `T-610` execute the frozen v1.1 final matrix with new run IDs.
2. `T-611` validate/freeze accepted final evidence.
3. `T-612` execute predeclared paired statistical analysis/sensitivity diagnostics.
4. `T-613` generate final v1.1 figures/tables/exports and the superseding thesis/defense evidence package.

Failed/cancelled/invalid/excluded runs remain visible and attributable. Final figures/tables derive only from frozen real data.

## Mandatory pre-WP7 approval

Completing application/evidence does **not** authorize thesis writing. T-511 must be accepted and the user must explicitly approve starting WP7. Until then all `T-700+` work remains blocked.

## Deferred downstream phases

After explicit approval:

- Recheck current official thesis/Word/submission/defense requirements.
- Draft/review/freeze the Greek Word thesis from citation-ready bibliography + frozen evidence.
- Incorporate supervisor/reviewer corrections with affected-evidence revalidation.
- Build the final PowerPoint defense narrative/deck/evidence map, embedded speaker notes and separate full spoken Greek script per `docs/thesis/PRESENTATION_WORKFLOW.md`.
- Validate PowerPoint rendering, factual consistency, rehearsal timing and demo/screenshot fallback.
- Final bibliography/reproducibility/privacy/licensing/delivery audits.

## Completion rule

The project is complete only when the research question is answered with reliable reproducible evidence, the bounded standalone application supports the real experiment workflow, and the final thesis/defense package communicates the same frozen evidence. Production-platform engineering is not required; concrete progress is governed by `TASKS.md`.
