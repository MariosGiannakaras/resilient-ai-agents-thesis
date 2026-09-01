# DEC-042 — Pre-WP7 protocol v1.1 and application refinement

**Date:** 2026-08-27  
**Status:** Accepted user-directed scientific/application refinement; implementation in progress. Application-framework details in the original decision are superseded by DEC-044/045/046.

## Context

The user has not accepted the historical application, agent set, experiment design, runs/results, or UI as the final thesis state. `protocol-v1.0`, finalized `FINAL-*` run bundles and existing thesis-final evidence are real immutable historical evidence, but they do not satisfy the current pre-WP7 acceptance gate.

Repository review identified two material refinements:

1. the v1.0 comparison is controlled but narrow because F0 and C0 are two deployment regimes of one tabular Q-learning implementation; and
2. the historical Streamlit application did not implement the intended configure -> launch -> live GridWorld -> inspect -> compare -> export journey, while the validated headless scientific core is reusable and must remain UI-independent.

Historical R0 robust-value-iteration pilot evidence remains useful but its accepted configuration exhibited approximately 96% nominal truncation and must not be reinstated unchanged.

## Decision

### Evidence preservation and versioning

- Preserve `protocol-v1.0`, every finalized historical run, and existing frozen analysis/artifacts unchanged.
- Revised primary evidence uses a new protocol version, new run identities, fresh held-out final layouts and a fresh precommitted final seed bank.
- `protocol-v1.1` begins as **candidate**, not frozen. It may freeze only after D0 implementation, bounded non-final tuning/pilot validation, protocol/statistical validation and the explicit pre-final gates pass.
- Never launch a final-v1.1 run merely for CI/UI convenience.

### Agent set

Retain:

- **F0 — Frozen Q-learning:** common nominal checkpoint, no post-change updates.
- **C0 — Continual Q-learning:** same common checkpoint/base configuration, online post-change Q-learning updates.

Add:

- **D0 — Dyna-Q+:** tabular learned-model planning on the same information-limited interaction surface. It learns transition/reward behavior only from agent-visible experience, performs bounded planning updates and uses Dyna-Q+ recency bonus for directed re-exploration.

D0 must remain deterministic under established RNG/seed contracts and serializable/resumable according to the validated agent/runner contract. D0-only planning parameters are selected only from a small predeclared development/tuning search. No D0 parameter is selected from final evidence.

Do not add deep RL merely to increase model count. Do not reinstate R0 unchanged.

### Multiple-settings policy

Development/tuning may execute multiple **protocol-approved resolved configurations** for a model/regime. Each configuration has stable identity/provenance and multiple predefined root seeds; single-run/best-seed ranking is forbidden.

- F0/C0 retain the accepted candidate-v1.1 base configuration unless an explicit scientific amendment reopens it.
- D0 receives only the bounded D0-specific planning search declared by T-521.
- Tuning/pilot/final stages remain separated and stage-validated.
- Failed, interrupted, cancelled, invalid and poor-performing configuration attempts remain recorded.
- Final model settings are frozen before final outcomes are inspected; final evidence cannot cherry-pick a development/tuning configuration after seeing final results.

Detailed current model/settings authority is `docs/research/MODEL_CANDIDATES.md`.

### Candidate protocol v1.1

Preserve accepted F0/C0 base values:

- learning rate `0.5`;
- discount factor `0.96875`;
- exploration epsilon `0.125`;
- `512` nominal training episodes per layout;
- `16` pre-change episodes;
- `32` post-change episodes;
- `48`-step evaluation horizon;
- `32` paired final root seeds.

Retain seven single-factor conditions with structural names:

1. `nominal`;
2. `action-remap-2-swap`;
3. `action-remap-4-cycle`;
4. `action-failure-1of8`;
5. `action-failure-1of4`;
6. `observation-corruption-1of8`;
7. `observation-corruption-1of4`.

Use four fresh held-out final layouts under the accepted GridWorld scale/structural constraints. Do not reuse already-inspected v1.0 final layouts as the new primary held-out set.

T-521 owns the authoritative candidate schema, exact fresh layouts/seeds, bounded D0 search and paired-statistics implementation. T-522 owns non-final selection and freeze/amend/reject evidence.

### Statistical roles

Primary outcome reporting keeps separate component estimands:

- cumulative deficit;
- immediate degradation;
- terminal gap/performance.

Recovery remains explicit secondary/sensitivity because accepted pilot evidence showed material threshold/stability sensitivity. Preserve `NO_DEGRADATION`, `RECOVERED` and `NOT_RECOVERED`; never encode non-recovery as artificial horizon recovery time.

Add paired agent-effect reporting and 95% confidence intervals using the paired root/layout design, with explicit `n`, per-layout views and aggregate views. Do not select favorable thresholds, settings or interval methods after inspecting final outcomes. No composite resilience score.

### Application architecture — superseded details reconciled

DEC-044 is the current framework authority and supersedes the temporary React/Vite exploration and historical Streamlit application direction.

Current stack:

- **NiceGUI 3.16 native mode** (`pywebview`) as the Python-only local desktop UI;
- UI-independent Python application/runtime service between NiceGUI and the validated scientific runner;
- Plotly for stored/final scientific figures;
- ECharts for real live/provisional telemetry;
- Mermaid for explanatory model/experiment diagrams;
- AG Grid Community for analytical tables;
- final Windows NiceGUI/PyInstaller `onedir + windowed` delivery plus root `run_app.bat` for repository-checkout launch.

T-530 provides truthful active-run state, heartbeat/progress/events/history/resources, read-only live GridWorld observation and capability-based lifecycle controls. Unsupported controls remain explicitly unsupported.

T-531 implements Dashboard, New Experiment, Runs/live GridWorld, Compare and Artifacts using the same scientific/runtime contracts. It may substantially replace historical application code but never duplicate scientific execution logic or fabricate status/metrics/logs/progress/replay.

Historical finalized runs without retained step traces show replay unavailable. Visualization speed/interpolation affects presentation cadence only, never scientific execution timing/actions/seeds/RNG.

DEC-046 additionally requires novice-first, compact, self-explanatory UX with accurate helper text/tooltips, progressive disclosure, semantic icon+text+color statuses, actionable states, modern micro-interactions/animations and reduced-motion-safe behavior where practical.

### Normal experiment execution after application completion

Once T-530/T-531/T-532/T-511 are complete, an already-approved experiment should be executable directly from the finished application on the validated thesis machine without Codex or console commands. The backend owns resolved config, seeds, execution, persistence/provenance, finalization, guarded Git publication and result availability for comparison/analysis.

GitHub remains source of truth and CI/evidence coordination surface. GitHub-hosted CI does not automatically become the validated final scientific execution machine. A self-hosted runner on the thesis machine is technically possible but is not required by this architecture.

### UI review artifacts

Create repository-root `ui-screenshots/`. Stable rendered screenshots are review artifacts, not scientific evidence. Deterministic UI fixtures may illustrate chrome/empty/error states only when clearly labelled and never as experiment results.

Real user-captured screenshots/GIF/video for thesis/defense later follow the exact `ASSET-*` placement/provenance workflow in `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md`; essential claims always retain a static evidence fallback.

### Work branch and tracking

All work uses:

`feat/pre-wp7-protocol-v1.1-ui-rebuild`

Master tracker #87; component trackers #88–#91. Do not create a parallel implementation branch. Keep canonical task/status/docs synchronized so another Codex/chat session can resume from repository state alone.

### Testing and completion

Testing remains risk-based and proportional: scientific/information-boundary/determinism/configuration/runtime-truthfulness regressions plus small representative UI/render/native-package checks. Never run pilot/final matrices as CI tests and do not create a quota-expanding coverage project.

Automated UI rendering/screenshots do not satisfy T-511. The application remains `USER_VALIDATION_REQUIRED` until intended-user E2E acceptance.

WP7/WP8 remain blocked. Technical completion of this package does not authorize thesis writing; explicit user approval is still required after pre-WP7 refinement and final evidence/application acceptance.