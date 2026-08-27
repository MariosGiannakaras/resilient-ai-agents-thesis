# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Preserve exact task/dependency/resume state across Codex sessions, quota interruptions, restarts, and chat changes.

`CURRENT_STATUS.md` is the compact status summary; decisions/evidence are read progressively. This file is the canonical checklist.

## Mandatory session rule

Every Codex session MUST read the three-file session-start core before selecting work:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Use current session memory together with durable Git/repository evidence. Repository state wins when memory is missing, stale, truncated, or conflicting.

Status: `[x]` complete; `READY` dependency-valid; `IN_PROGRESS` active; `BLOCKED` dependency/gate unmet; `DEFERRED` intentionally later. In-progress/failed work never counts as complete.

## Resume state

- **Package:** DEC-042 + DEC-044 + DEC-045 + DEC-046 + DEC-047 pre-WP7 scientific/application refinement. DEC-043 is historical/superseded.
- **Project:** **2/8** major refinement milestones complete.
- **Current task:** `T-523`
- **State:** `READY`
- **Branch / PR:** `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; this is the single implementation branch/PR.
- **Trackers:** #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/packaging.
- **Last validated checkpoint:** PR CI run **376** passed documentation consistency, JSON validation, Python compile, locked environment, complete tests and bibliography integrity before DEC-047 broadened the candidate agent set.
- **Continuity reconciliation:** known stale architecture/delivery/workflow areas are reconciled. DEC-047 now supersedes the three-agent candidate direction with five mechanism-distinct user-facing strategies while preserving historical IDs/evidence.
- **Downstream planning:** `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` records future Word/PowerPoint/ChatGPT/Codex/optional-Canva/manual-screenshot ownership without unlocking WP7.
- **Uncommitted work:** unknown from remote handoff; every new session must inspect `git status` before assuming clean state.
- **Exact next action:** execute `T-523`: implement/validate information-limited SARSA and plain Dyna-Q, add clearly labelled reference fixtures where useful, integrate runner/config identities, and measure bounded runtime feasibility. Then execute `T-521`; do not start final-v1.1 evidence or `T-700+`.

## Quota/interruption resilience

1. Inspect `git status`, branch, recent commits, PR #92/check state, and every `IN_PROGRESS` task at session start.
2. Resume `IN_PROGRESS` work first unless genuinely blocked.
3. Never discard branch/uncommitted work before inspection.
4. Preserve recoverable checkpoint commits for substantial validated slices.
5. Reconcile this Resume state whenever a newer instruction supersedes architecture, research design, UI behavior, tool ownership, or next action.
6. Preserve stable task/requirement/decision identifiers; append or supersede explicitly rather than silently renumbering durable references.
7. Use `Project: X/Y` and issue X/Y only from finite canonical denominators.
8. Testing remains risk-based/proportional; pilot/final matrices are never CI tests.
9. Do not create another implementation branch for this package.

## WP0 — Completed repository/research infrastructure

- [x] `T-001` — Repository/project identity and controlled Git/PR workflow.
- [x] `T-002` — Immutable `ThesisBibliography` integration/provenance.
- [x] `T-003` — Python 3.12 + `uv` locked environment/importable core.
- [x] `T-004` — Information/RNG/scenario/experiment/stage contracts.
- [x] `T-005` — Run bundles/provenance/checksums/metrics/publication safeguards.
- [x] `T-006` — Active-document reconciliation/canonical Codex prompt.
- [x] `T-007` — End-to-end lifecycle/user/Codex/defense handoffs.
- [x] `T-008` — Lean three-file session-start core and resumable Goal execution.
- [x] `T-009` — Project-scoped OpenAI developer-documentation MCP configuration.

## WP1 — Completed target-machine baseline

- [x] `T-100` — Actual-machine hardware/software/storage inventory.
- [x] `T-101` — Compute-dependent dependency/runtime constraints.
- [x] `T-102` — Durable capability-provenance reconciliation.

## WP2 — Completed research framing and controlled testbed

- [x] `T-200` — Source-traceable RQ/hypothesis framing.
- [x] `T-210` — GridWorld implementation comparison.
- [x] `T-211` — GridWorld ADR.
- [x] `T-212` — Project-owned Gymnasium GridWorld.
- [x] `T-213` — GridWorld known-answer/determinism/disturbance/information tests.

GridWorld is the controlled experimental/visualization testbed, not the thesis subject. The thesis compares resilient agent strategies under uncertainty/change.

## WP3 — Completed historical metrics/agent selection

- [x] `T-300` — Resilience/degradation/recovery estimands.
- [x] `T-301` — Known-answer metric validation.
- [x] `T-310` — Historical bounded agent-role comparison.
- [x] `T-311` — Robust-MDP citation decision.
- [x] `T-312` — Historical F0/C0/R0-capable implementation.

## WP4 — Completed historical pilot/protocol system

- [x] `T-400` — Partitions and pilot protocol.
- [x] `T-401` — Headless runner/orchestration.
- [x] `T-402` — Reproducible analysis pipeline.
- [x] `T-410` — Pilot diagnostics/R0 amendment evidence.
- [x] `T-411` — Pre-freeze bibliography freshness review.
- [x] `T-412` — Immutable historical `protocol-v1.0` freeze/statistical plan.

## WP5 — Application baseline and active refinement

Historical baseline:

- [x] `T-500` — Historical experiment-manager baseline.
- [x] `T-510` — Historical Streamlit dashboard baseline.
- [x] `T-512` — Historical self-explanatory UX/onboarding pass.
- [x] `T-513` — Refinement governance, single branch/PR, Codex handoff and canonical state.

Current refinement:

- [x] `T-520` — Implement/integrate information-limited deterministic Dyna-Q+ (`D0` historical technical identity).
  - Depends on: `T-513`.
  - Validated: uses only agent-visible observations/intended actions/rewards; deterministic Q/model/RNG serialization; common checkpoint; episode-preserving deployment; historical `PilotProtocol` unchanged; development-only `V11DevelopmentProtocol`; F0/C0/D0 runner deterministic; missing/irrelevant Dyna-specific parameters and non-development use fail closed.

- [ ] READY `T-523` — Implement/validate the broadened DEC-047 agent strategy set before candidate-v1.1 freeze.
  - Depends on: `T-520`.
  - Acceptance: deterministic information-limited **SARSA** implementation with explicit/versioned config/state and exact update tests; deterministic **Dyna-Q** implementation reusing the Dyna learned-model/planning machinery without recency bonus; focused test proving Dyna-Q vs Dyna-Q+ intended difference; runner/configuration identity integration for Fixed Q-Learning, Adaptive Q-Learning, SARSA, Dyna-Q and Dyna-Q+; Random Agent and nominal/fully-informed planner only as clearly labelled non-ranked reference fixtures where useful; user-facing names/descriptions independent of opaque F0/C0/D0 IDs; measured bounded runtime/matrix-size feasibility; historical v1.0/R0 evidence untouched.
  - Fairness: same online information boundary for five scientific agents; no changepoint/evaluator truth; SARSA tuning surface is predeclared/minimal if fairness requires it; Dyna-Q/Dyna-Q+ planning budgets matched where appropriate; no final evidence inspected.

- [ ] BLOCKED `T-521` — Implement authoritative candidate `protocol-v1.1`, bounded tuning design, fresh held-out layouts/seeds, approved configuration identity/settings policy, and paired statistical support.
  - Depends on: `T-523`.
  - Acceptance: v1.0/final evidence untouched; candidate v1.1 contains the five validated main strategies **Fixed Q-Learning, Adaptive Q-Learning, SARSA, Dyna-Q, Dyna-Q+**; validated Q-learning budgets preserved; exact small predeclared SARSA fairness-tuning and Dyna planning/Dyna-Q+ `kappa` search only where justified; four fresh held-out final layouts + fresh precommitted final seeds; seven single-factor conditions with `action-remap-2-swap` / `action-remap-4-cycle`; stable resolved-configuration identity/provenance; multiple approved development/tuning configurations use multiple predefined roots and no single-run/best-seed cherry-picking; primary cumulative deficit/immediate degradation/terminal performance; recovery secondary/sensitivity; paired effects + 95% CIs with explicit n/layout aggregation; candidate status cannot authorize final evidence.
  - Conditional robust gate: a redesigned Robust Planner becomes a sixth main comparator only if a small predeclared non-final nominal-viability/fairness/runtime gate passes; otherwise historical R0 remains negative pilot evidence only.

- [ ] BLOCKED `T-522` — Execute bounded non-final tuning/pilot and freeze/amend/reject v1.1.
  - Depends on: `T-521`.
  - Acceptance: candidate settings selected only from predeclared non-final evidence; all retained strategies pass correctness/runtime/informativeness criteria; configurations compared using approved repeated/paired design and predeclared selection/tie rules; failed/interrupted/non-recovery/poor configurations retained; optional Robust Planner either passes its explicit gate or remains excluded with documented evidence; no final-v1.1 outcomes inspected before freeze; final retained configuration for each scientific agent is explicit/versioned.

- [ ] READY `T-530` — Add truthful UI-independent Python runtime service for live experiments.
  - Depends on: `T-520`.
  - Acceptance: versioned DTO/service contracts for queued/running/completed/failed/cancelled/interrupted state, heartbeat/progress/events/history/resources, unfinished runs, read-only live GridWorld observer proven not to alter RNG/actions, safe stop/cancel/restart only, unsupported controls explicit. NiceGUI framework plumbing is not the scientific runtime contract.
  - Execution order: remain secondary to current scientific T-523/T-521 sequence; do not split into a parallel branch.

- [ ] BLOCKED `T-531` — Complete native NiceGUI application with DEC-045 analytics, DEC-046 novice-first UX and DEC-047 human-readable agent strategies.
  - Depends on: `T-521`, `T-530`.
  - Existing early work: NiceGUI shell/read model/visualization builders/onboarding; historical v1.0 Plotly views; intentionally empty live ECharts surface.
  - Functional acceptance: Dashboard; New Experiment supports protocol-approved agent/configuration variants, multiple seeds/repetitions and bounded settings/sweeps with resolved-config review; Runs active/history/detail with smooth live GridWorld, event timeline, real metrics/logs and compatible live agent/configuration overlays; Compare supports compatible agents/settings/config identities with distributions/paired CIs/counts/layout-condition views; Artifacts real CSV/JSON/HTML/provenance preview/export; Plotly/ECharts/Mermaid/AG Grid integration.
  - Naming acceptance: primary selector is **Agent strategy**; ordinary users see Fixed Q-Learning, Adaptive Q-Learning, SARSA, Dyna-Q and Dyna-Q+ with plain one-sentence explanations/mechanism badges. Historical/internal IDs such as F0/C0/D0/config hashes appear only under Technical details / Reproducibility.
  - Self-explanatory UX acceptance: non-programmer/non-RL user understands agents, conditions, settings, fixed-vs-tunable configuration, units, metrics, repetition meaning and statuses via plain-language labels, helper text, info icons/tooltips, progressive disclosure, metric/uncertainty explanations and actionable invalid/empty/loading/error/disabled states.
  - Visual acceptance: modern compact hierarchy; consistent icons; accessible semantic text+icon+color states; restrained hover/focus/selection micro-interactions; purposeful chart/status/GridWorld animations; reduced-motion-safe where practical; skippable/replayable onboarding. Animation never implies fake progress.
  - Runtime acceptance: root `run_app.bat` opens the NiceGUI native desktop window; same pages work in CI browser mode; no active Node/Vite/Streamlit stack; no fabricated state/data/replay.

- [ ] BLOCKED `T-532` — Root UI screenshots, bounded render validation and Windows packaging.
  - Depends on: `T-531`.
  - Acceptance: root `ui-screenshots/` with stable pages plus useful help/tooltip/status/empty/error examples; deterministic bounded CI capture; no fixture presented as evidence; historical no-trace replay unavailable; Windows native launch/close/restart; validated NiceGUI/PyInstaller `onedir + windowed` folder requiring no Python/Node/browser interaction and using safe writable data paths.

- [ ] USER_VALIDATION_REQUIRED `T-511` — Validate the complete intended application workflow and self-explanatory UX.
  - Depends on: `T-512`, `T-531`, `T-532`.
  - Acceptance: a non-technical intended user can understand the human-readable agent strategies, configure an approved experiment/configuration set, launch/monitor truthful live GridWorld/charts, compare compatible live/finalized agent/settings behavior, inspect/export/screenshot results, understand help/status/errors/disabled states/onboarding, and use the standalone app. Automated screenshots/package checks never close this gate.

## WP6 — Historical v1.0 evidence and future v1.1 evidence

- [x] `T-600` — Historical frozen v1.0 final matrix.
- [x] `T-601` — Historical v1.0 evidence validation/freeze.
- [x] `T-602` — Historical v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical thesis/defense evidence package.

- [ ] BLOCKED `T-610` — Execute frozen v1.1 final matrix with new run IDs through the accepted thesis-machine/application execution path.
  - Depends on: `T-522`, `T-511`.
  - Acceptance: frozen retained scientific-agent settings/config IDs only; all required fresh layouts/conditions/paired roots executed or transparently accounted for; reference fixtures not mixed into fair rankings; no post-final configuration switching; ordinary approved execution requires no Codex/console intervention.
- [ ] BLOCKED `T-611` — Validate/freeze v1.1 final evidence.
  - Depends on: `T-610`.
- [ ] BLOCKED `T-612` — Predeclared v1.1 paired statistical analysis/sensitivity diagnostics.
  - Depends on: `T-611`.
- [ ] BLOCKED `T-613` — v1.1 figures/tables/exports and superseding thesis/defense evidence package.
  - Depends on: `T-612`.
  - Acceptance: claim-ready evidence map includes final human-readable agent/config identities, technical IDs, runs, paired statistics, figures/tables/captions and source/protocol references; no provisional/tuning values promoted to final evidence.

## Mandatory pre-WP7 user approval gate

**NOT APPROVED.** Technical completion, green CI, screenshots, packaged app or completed `T-613` do not authorize writing. Only after refinement/evidence and `T-511` acceptance may the assistant ask whether WP7 may begin; only a direct affirmative unlocks it.

Planning files such as `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` may be prepared before the gate so future execution is unambiguous; final thesis prose/defense production remains blocked.

## WP7 — Thesis writing/review/defense

- [ ] BLOCKED `T-700` — Recheck current Department/University thesis/submission/defense rules and current tool assumptions.
  - Depends on: mandatory pre-WP7 approval gate and accepted final evidence state.
  - Acceptance: dated authoritative guidance snapshot; current Word/template/citation/submission/defense requirements; explicit differences from historical snapshot; `WP7_WP8_TOOL_WORKFLOW.md` revalidated against current Word/PowerPoint/ChatGPT/Canva capabilities where material.
- [ ] DEFERRED `T-701` — Review later supplied completed theses as contextual examples only.
  - Acceptance: structural/presentation observations only; never scientific/official authority.
- [ ] DEFERRED `T-710` — Draft complete Greek thesis from accepted evidence.
  - Depends on: `T-700`; final evidence package.
  - Acceptance: chapter evidence maps; every quantitative/result claim maps to frozen result/figure/table IDs; external claims map to citation-ready evidence; negative/null/unexpected results and limitations retained; full human-readable agent strategy names introduced before any stable abbreviations/technical IDs; settings/protocol terminology used consistently.
- [ ] DEFERRED `T-711` — Produce review-ready Word thesis and manual asset-placement register.
  - Depends on: `T-710`.
  - Acceptance: `.docx` uses Word heading styles/automatic TOC/caption fields/cross-references/lists; validated figures/tables; every user-captured screenshot/GIF/video request has an `ASSET-*` record with exact page/state/run/config/crop, target chapter/section, caption, placement/size guidance, evidence identity and static fallback.
- [ ] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate.
  - Depends on: `T-711` and actual feedback when provided.
  - Acceptance: feedback-to-change register; every affected citation/result/figure/table/method statement revalidated; scientific changes reopen the proper evidence/protocol task rather than being hidden in prose.
- [ ] DEFERRED `T-713` — Freeze final thesis deliverable.
  - Depends on: `T-712` or documented absence/completion of required review cycle.
  - Acceptance: Word fields/TOC/captions/cross-references/lists updated; final formatting/evidence/citation/asset QA passed; controlled `.docx` + required exports frozen.
- [ ] DEFERRED `T-720` — Defense narrative/slide outline/evidence map.
  - Depends on: stable/final thesis.
  - Acceptance: examiner-facing narrative; slide-to-thesis/result/source map; generated-vs-user-captured asset plan; live-demo/static fallback plan.
- [ ] DEFERRED `T-721` — Final PowerPoint + speaker material per `docs/thesis/PRESENTATION_WORKFLOW.md`.
  - Depends on: `T-720`.
  - Acceptance: final `.pptx`, embedded notes, separate full spoken Greek script, evidence IDs preserved, exact `ASSET-*` instructions for manual app media; Canva optional only; PowerPoint remains final inspection surface.
- [ ] DEFERRED `T-722` — Validate/rehearse defense package/demo fallback.
  - Depends on: `T-721`.
  - Acceptance: current official duration/content/file rules; numerical/citation consistency; PowerPoint rendering/media/notes/Presenter View; rehearsal timing; live demo plus tested static/screenshot/GIF/video fallback.

## WP8 — Final audits/completion

- [ ] DEFERRED `T-800` — Final bibliography/citation/official-guidance audit.
- [ ] DEFERRED `T-801` — Final reproducibility/privacy/licensing/docs/thesis/defense/application-asset audit.
- [ ] DEFERRED `T-802` — Final delivery readiness.

## Task maintenance rule

Every material checkpoint must reconcile this registry if work starts/completes/blocks/unblocks/is superseded or new required work is discovered. GitHub issues are tracking views, not a competing task list.