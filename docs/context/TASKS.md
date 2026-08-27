# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Preserve exact task/dependency/resume state across Codex sessions, quota interruptions, restarts and chat changes.

`CURRENT_STATUS.md` is the compact status summary. This file is the canonical task/dependency checklist.

## Mandatory session rule

Every Codex session MUST read the three-file session-start core:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Use session memory together with repository/Git/GitHub/evidence. Repository evidence wins when memory or prose is stale. Inspect `git status`, branch, recent commits, PR #92 and any `IN_PROGRESS` work before modifying anything.

Status: `[x]` complete; `READY` dependency-valid; `IN_PROGRESS` active; `BLOCKED` gate/dependency unmet; `DEFERRED` intentionally later. In-progress/failed work never counts as complete.

## Resume state

- **Package:** DEC-042 + DEC-044 + DEC-045 + DEC-046 + DEC-047. DEC-043 is historical/superseded.
- **Project:** **5/8** major refinement milestones complete (#87 milestones 1, 2, 4, 5 and 6).
- **Current task:** `T-532`.
- **State:** `READY`; dependency `T-531` is complete.
- **External scientific gate:** `T-522` remains READY only on the validated thesis machine. It is not replaced by hosted CI.
- **Branch / PR:** `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; no second implementation branch.
- **Trackers:** #87 master (**5/8**); #88 scientific (**9/12**); #89 runtime (**6/6 complete/closed**); #90 UI (**8/9**); #91 screenshots/CI/packaging (**0/6**, active next).
- **Validation authority:** inspect PR #92's current-head CI live; historical run 425 remains the T-530 checkpoint but is not a substitute for the current head.
- **Completed refinement tasks:** `T-520`, `T-523`, `T-521`, `T-530`, `T-531`.
- **Pre-WP7 approval:** NOT APPROVED; `T-700+` execution remains blocked.
- **Exact next action:** continue `T-532` on this branch: root screenshots, bounded browser/CI capture and actual Windows native/onedir validation. If a session has access to the validated thesis machine, `T-522` may run in parallel only as the predeclared non-final external evidence gate; never inspect/generate final-v1.1 reserve outcomes.

## Quota/interruption resilience

1. Resume valid unfinished local/remote work before starting something new.
2. Never discard uncommitted/pushed/partial experiment evidence without inspection.
3. Reconcile this ledger at coherent checkpoints, not after every command/run child.
4. Preserve stable task/requirement/decision IDs; supersede explicitly rather than renumbering.
5. Use `Project: X/Y` only from finite canonical denominators.
6. Testing is risk-based/proportional; scientific experiment matrices are not CI test matrices.
7. Never create another implementation branch for this package.

## WP0 — Repository/research infrastructure

- [x] `T-001` — Repository/project identity and controlled Git/PR workflow.
- [x] `T-002` — Immutable `ThesisBibliography` integration/provenance.
- [x] `T-003` — Python 3.12 + `uv` locked environment/importable core.
- [x] `T-004` — Information/RNG/scenario/experiment/stage contracts.
- [x] `T-005` — Run bundles/provenance/checksums/metrics/publication safeguards.
- [x] `T-006` — Documentation reconciliation/canonical execution prompt.
- [x] `T-007` — End-to-end lifecycle/user/Codex/defense handoffs.
- [x] `T-008` — Lean three-file session-start core and resumable execution.
- [x] `T-009` — Project-scoped OpenAI developer-documentation configuration.

## WP1 — Target-machine baseline

- [x] `T-100` — Actual-machine hardware/software/storage inventory.
- [x] `T-101` — Compute-dependent dependency/runtime constraints.
- [x] `T-102` — Durable capability-provenance reconciliation.

## WP2 — Research framing and controlled testbed

- [x] `T-200` — Source-traceable RQ/hypothesis framing.
- [x] `T-210` — GridWorld implementation comparison.
- [x] `T-211` — GridWorld ADR.
- [x] `T-212` — Project-owned Gymnasium GridWorld.
- [x] `T-213` — Known-answer/determinism/disturbance/information tests.

GridWorld is the controlled experimental/visualization testbed, not the thesis subject.

## WP3 — Historical metrics/agent selection

- [x] `T-300` — Resilience/degradation/recovery estimands.
- [x] `T-301` — Known-answer metric validation.
- [x] `T-310` — Historical bounded agent-role comparison.
- [x] `T-311` — Robust-MDP citation decision.
- [x] `T-312` — Historical F0/C0/R0-capable implementation.

## WP4 — Historical pilot/protocol system

- [x] `T-400` — Partitions and pilot protocol.
- [x] `T-401` — Headless runner/orchestration.
- [x] `T-402` — Reproducible analysis pipeline.
- [x] `T-410` — Pilot diagnostics/R0 amendment evidence.
- [x] `T-411` — Pre-freeze bibliography freshness review.
- [x] `T-412` — Immutable historical `protocol-v1.0` freeze/statistical plan.

## WP5 — Application baseline and active refinement

- [x] `T-500` — Historical experiment-manager baseline.
- [x] `T-510` — Historical Streamlit dashboard baseline.
- [x] `T-512` — Historical self-explanatory UX/onboarding pass.
- [x] `T-513` — Refinement governance, single branch/PR, Codex handoff.

- [x] `T-520` — Information-limited deterministic Dyna-Q+ integration.
  - Depends on: `T-513`.
  - Evidence: separate development-only path, deterministic state/model/RNG, episode persistence, no evaluator leakage; historical protocol semantics unchanged.

- [x] `T-523` — Broaden main strategy set to Fixed Q-Learning, Adaptive Q-Learning, SARSA, Dyna-Q and Dyna-Q+.
  - Depends on: `T-520`.
  - Evidence: SARSA/Dyna-Q implementations, five-strategy runner, Random reference fixture, human-readable identities and feasibility; CI run 396.

- [x] `T-521` — Authoritative **candidate** `protocol-v1.1`, bounded tuning/settings, fresh reserves, configuration identity/provenance and paired statistics.
  - Depends on: `T-523`.
  - Evidence: separate fail-closed schema/loader/runner; five strategies; preserved Q baseline alpha `.5`, gamma `.96875`, epsilon `.125`; 2 SARSA + 2 Dyna-Q + 4 Dyna-Q+ bounded candidate configurations; four fresh held-out layouts; fresh/disjoint 32-root final bank; seven structural single-factor conditions; stable SHA-256 configuration/protocol identities; complete-root tuning/no best-seed; cumulative deficit/immediate degradation/terminal performance primary; recovery secondary/sensitivity; root-blocked equal-layout paired effects with deterministic 95% percentile-bootstrap CI; pilot/final candidate execution blocked. CI run 409/425.
  - Robust gate: historical R0 remains negative/diagnostic; a redesigned Robust Planner is conditional/non-main unless a separate non-final viability/fairness/runtime gate passes.

- [ ] READY `T-522` — Execute bounded non-final tuning/resource evaluation and freeze/amend/reject v1.1.
  - Depends on: `T-521`.
  - Acceptance: use only complete predeclared non-final roots/layouts/conditions/configurations; retain failed/interrupted/poor/non-recovery outcomes; apply deterministic selection/tie rules; measure Dyna planning wall time/update/artifact cost on the validated thesis machine; resolve conditional Robust Planner explicitly; freeze retained configuration IDs before any final reserve access.
  - External boundary: do not substitute GitHub-hosted CI for the validated thesis machine.

- [x] `T-530` — Truthful UI-independent Python runtime service for live experiments.
  - Depends on: `T-520`.
  - Evidence: schema-v1 queued/running/completed/failed/cancelled/interrupted DTOs; persisted runtime registry; activity heartbeat; persisted root progress plus latest real phase/episode/step; telemetry tail; canonical resources; unfinished/finalized history reconciliation; capability-based cancel/restart; pause/resume explicitly unsupported; owned candidate subprocess entrypoint only; pre-queue protocol/request validation; read-only live GridWorld observer; observer ON/OFF produces identical scientific root results. Tracker #89 6/6; CI run 425.

- [x] `T-531` — Complete native NiceGUI application.
  - Depends on: `T-521`, `T-530`.
  - Acceptance: Dashboard/New Experiment/Runs/Compare/Artifacts; approved Agent strategy/configuration/repetitions; smooth truthful live GridWorld; ECharts live telemetry; Plotly final/comparison figures; Mermaid explanations; AG Grid tables; tooltips/helper text/progressive disclosure; accessible text+icon+color status; compact modern micro-interactions/animations; technical IDs only under Reproducibility; no fake data/progress/replay.
  - Evidence: all five NiceGUI routes consume the validated read/runtime/core contracts; five human-readable strategy flows and bounded settings; truthful lifecycle/history/no-trace states; stored-only v1.0 distributions/counts/layout breakdowns with SD never relabelled CI; exact stored artifact preview/download/provenance; 15 focused application tests; import/compile and five-route browser-mode render checks; tall visual inspection corrected Plotly/artifact clipping. Tracker #90 8/9; its remaining native/onedir item belongs to T-532.

- [ ] READY `T-532` — Root screenshots, bounded UI validation and Windows standalone packaging.
  - Depends on: `T-531`.
  - Acceptance: root `ui-screenshots/`, deterministic CI/browser captures, useful help/status/error/empty states, no fixture-as-evidence, native NiceGUI/PyInstaller `onedir + windowed` launch/close/restart with safe writable paths.

- [ ] USER_VALIDATION_REQUIRED `T-511` — Intended-user application workflow/self-explanatory UX acceptance.
  - Depends on: `T-512`, `T-531`, `T-532`.
  - Acceptance: a non-technical user can understand strategies/settings/metrics, configure an approved experiment, monitor real GridWorld/charts, compare/export/screenshot evidence and understand help/errors/status. Automated checks never close this gate.

## WP6 — Historical and future final evidence

- [x] `T-600` — Historical frozen v1.0 final matrix.
- [x] `T-601` — Historical v1.0 evidence validation/freeze.
- [x] `T-602` — Historical v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical thesis/defense evidence package.

- [ ] BLOCKED `T-610` — Execute frozen v1.1 final matrix through accepted thesis-machine/application path.
  - Depends on: `T-522`, `T-511`.
- [ ] BLOCKED `T-611` — Validate/freeze v1.1 final evidence.
  - Depends on: `T-610`.
- [ ] BLOCKED `T-612` — Predeclared paired statistical analysis/sensitivity diagnostics.
  - Depends on: `T-611`.
- [ ] BLOCKED `T-613` — Final v1.1 figures/tables/exports and thesis/defense evidence package.
  - Depends on: `T-612`.

## Mandatory pre-WP7 user approval gate

**NOT APPROVED.** Completion of science, CI, screenshots, packaging or `T-613` does not authorize thesis writing. Only explicit user approval after accepted evidence/application can unlock WP7.

## WP7 — Thesis writing/review/defense

- [ ] BLOCKED `T-700` — Recheck current Department/University submission/formatting/defense rules and current tool assumptions.
  - Depends on: `T-613`, `T-511` and explicit pre-WP7 user approval.
- [ ] DEFERRED `T-701` — Review later supplied completed theses as contextual examples only.
- [ ] DEFERRED `T-710` — Draft complete Greek thesis from accepted evidence.
  - Depends on: `T-700`.
- [ ] DEFERRED `T-711` — Produce review-ready Word thesis + manual `ASSET-*` placement register.
  - Depends on: `T-710`.
- [ ] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate.
  - Depends on: `T-711`.
- [ ] DEFERRED `T-713` — Freeze final thesis deliverable.
  - Depends on: `T-712`.
- [ ] DEFERRED `T-720` — Defense narrative/slide outline/evidence map.
  - Depends on: `T-713`.
- [ ] DEFERRED `T-721` — Final PowerPoint + speaker material per `docs/thesis/PRESENTATION_WORKFLOW.md`.
  - Depends on: `T-720`.
- [ ] DEFERRED `T-722` — Validate/rehearse defense package/demo fallback.
  - Depends on: `T-721`.

## WP8 — Final audits/completion

- [ ] DEFERRED `T-800` — Final bibliography/citation/official-guidance audit.
  - Depends on: `T-713`, `T-722`.
- [ ] DEFERRED `T-801` — Final reproducibility/privacy/licensing/docs/thesis/defense/application-asset audit.
  - Depends on: `T-800`.
- [ ] DEFERRED `T-802` — Final delivery readiness.
  - Depends on: `T-801`.

## Task maintenance rule

Every material checkpoint reconciles this registry. GitHub issues are tracking views, not a competing task list. In-progress/failed work never counts as complete.
