# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Preserve concrete task/dependency/resume state across Codex sessions, quota interruptions, machine restarts, and context changes.

`IMPLEMENTATION_ROADMAP.md` defines phase intent. `EXECUTION_WORKFLOW.md` defines responsibilities/handoffs. `CURRENT_STATUS.md` summarizes the current state. This file is the canonical checklist. Historical detail remains in Git history, decisions, PRs, and task-specific evidence; completed task IDs remain here for auditability.

## Mandatory session rule

Every Codex session MUST read the three-file session-start core before selecting work:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Use current session memory together with durable repository evidence. Git/repository state wins when session memory is missing, truncated, stale, or conflicting.

Status syntax:

- `[x]` completed and validated.
- `[ ] READY` dependency-valid and may start.
- `[ ] IN_PROGRESS` active; Resume state must explain continuation.
- `[ ] BLOCKED` cannot proceed until the stated dependency/gate resolves.
- `[ ] DEFERRED` intentionally later.

In-progress/failed work never counts as complete. Newly discovered required work gets a stable `T-*` ID here rather than living only in chat/issues.

## Resume state

- **Current work package:** DEC-042 pre-WP7 protocol-v1.1 scientific + application refinement.
- **Current task:** `T-513`
- **State:** `IN_PROGRESS`
- **Active branch / PR:** `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92. This is the single implementation branch/PR for this package; do not create a parallel implementation branch.
- **Trackers:** #87 master; #88 scientific; #89 runtime; #90 UI; #91 screenshots/CI/Codex handoff.
- **Last validated point:** DEC-042, branch-pinned `CURRENT_STATUS.md`, branch-pinned Codex bootstrap, initial D0 implementation and focused D0 tests are committed. First PR CI failed at documentation consistency before compile/tests; the concrete validator findings are being reconciled in this checkpoint.
- **Tests already run:** PR #92 CI run 261 reached documentation validation only and failed there; Python compile/tests were skipped, so D0 is not yet counted validated.
- **Uncommitted work:** unknown to remote handoff; next session must inspect `git status` before assuming clean state.
- **Exact next action:** finish `T-513` by making documentation consistency green and reconciling #87/#91 progress; then start `T-520` on this same branch. Do not start `T-700+`.

## Quota/interruption resilience

1. At session start inspect `git status`, current branch, recent commits, PR #92/check state, this Resume state, and any `IN_PROGRESS` task.
2. Resume an `IN_PROGRESS` task before selecting new work unless genuinely blocked.
3. Never discard useful prior branch/uncommitted work without inspecting it.
4. Preserve a recoverable checkpoint after substantial validated substeps when practical.
5. Update this Resume state when the next action would otherwise be ambiguous.
6. Use issue `X/Y` and task status only from real finite denominators; failed/partial work does not count.
7. Testing remains risk-based/proportional; pilot/final experiment matrices are never CI tests.

## WP0 — Completed repository/research infrastructure

- [x] `T-001` — Repository/project identity and controlled Git/PR workflow.
- [x] `T-002` — Immutable `ThesisBibliography` corpus integration and provenance validation.
- [x] `T-003` — Python 3.12 + `uv` locked environment and importable scientific package.
- [x] `T-004` — Information/RNG/scenario/experiment/stage contracts.
- [x] `T-005` — Filesystem run bundles, provenance/checksums, metrics primitives, guarded publication.
- [x] `T-006` — Active-document reconciliation and canonical Codex prompt.
- [x] `T-007` — End-to-end lifecycle/user/Codex/defense handoffs.
- [x] `T-008` — Lean three-file session-start core and resumable Goal-mode execution.
- [x] `T-009` — Project-scoped OpenAI developer-documentation MCP configuration.

## WP1 — Completed target-machine baseline

- [x] `T-100` — Actual-machine hardware/software/storage inventory.
- [x] `T-101` — Resolve compute-dependent dependency/runtime constraints.
- [x] `T-102` — Reconcile durable merged-main capability provenance.

## WP2 — Completed research framing and GridWorld

- [x] `T-200` — Source-traceable research-question/hypothesis framing.
- [x] `T-210` — Bounded GridWorld implementation comparison.
- [x] `T-211` — GridWorld ADR.
- [x] `T-212` — Project-owned Gymnasium GridWorld implementation.
- [x] `T-213` — Known-answer/determinism/disturbance/information-boundary GridWorld tests.

## WP3 — Completed original metrics and agent selection

- [x] `T-300` — Operational resilience/degradation/recovery estimands.
- [x] `T-301` — Known-answer metric validation.
- [x] `T-310` — Original bounded agent-role comparison.
- [x] `T-311` — Robust-MDP citation support decision.
- [x] `T-312` — Original F0/C0/R0-capable common agent implementation.

## WP4 — Completed original pilot/protocol system

- [x] `T-400` — Development/tuning/pilot/final partitions and pilot protocol.
- [x] `T-401` — Headless experiment runner/orchestration.
- [x] `T-402` — Reproducible analysis pipeline.
- [x] `T-410` — Pilot execution/diagnostics including retained R0 failure/amendment evidence.
- [x] `T-411` — Pre-freeze bibliography freshness review.
- [x] `T-412` — Historical `protocol-v1.0` freeze/statistical plan. This remains immutable baseline evidence, not a prohibition on DEC-042 versioned refinement.

## WP5 — Historical application baseline and active DEC-042 refinement

Historical baseline:

- [x] `T-500` — Historical experiment-manager baseline.
- [x] `T-510` — Historical bounded Streamlit dashboard baseline.
- [x] `T-512` — Historical self-explanatory UX/onboarding pass.

Active refinement tasks:

- [ ] IN_PROGRESS `T-513` — Reconcile DEC-042 governance, single-branch/PR tracking, Codex handoff, and canonical task/status state.
  - Acceptance: DEC-042/current status/Codex prompt/this ledger/issues #87–#91 agree; PR documentation validator passes; branch/PR/resume state is recoverable without chat history; WP7 hard gate remains explicit.

- [ ] BLOCKED `T-520` — Implement/integrate D0 Dyna-Q+ as an information-limited deterministic third tabular agent.
  - Depends on: `T-513`.
  - Acceptance: D0 uses only agent-visible observations/intended actions/rewards; common selected Q checkpoint is supported; stochastic learned model + Dyna-Q+ planning/recency bonus are explicit; state/RNG/model serialization is deterministic; focused known-answer/information-boundary/round-trip tests pass; runner can execute D0 without special evaluator access.

- [ ] BLOCKED `T-521` — Implement candidate `protocol-v1.1` design, bounded D0-specific tuning plan, fresh held-out layouts/seeds, and paired statistical support.
  - Depends on: `T-520`.
  - Acceptance: v1.0/final evidence unchanged; candidate v1.1 contains F0/C0/D0; preserves F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48, 32 paired final roots; uses four fresh held-out final layouts + fresh precommitted final seeds; structural remap IDs; small predeclared D0-only planning search; primary component metrics + secondary recovery sensitivity; paired effects + 95% CIs; candidate status cannot authorize final evidence.

- [ ] BLOCKED `T-522` — Execute bounded non-final D0 tuning/pilot validation and freeze `protocol-v1.1` only if acceptance gates pass.
  - Depends on: `T-521`; execution on the actual thesis machine when required.
  - Acceptance: D0 planning parameters are selected from predeclared development/tuning evidence only; non-final pilot confirms execution/informativeness/runtime bounds; failed/non-recovery outcomes retained; no final-v1.1 evidence inspected; freeze/amend/reject decision is evidence-backed and versioned.

- [ ] BLOCKED `T-530` — Add truthful application runtime/service layer independent of Streamlit.
  - Depends on: `T-520`.
  - Acceptance: real queued/running/completed/failed/cancelled/interrupted state; heartbeat/progress/events; read-only live GridWorld observation proven not to alter scientific RNG/actions; unfinished runs visible; stop/cancel/restart only when safe; unsupported pause/resume/control capabilities explicit.

- [ ] BLOCKED `T-531` — Rebuild the Streamlit research application on the validated core/runtime service.
  - Depends on: `T-530`, `T-521`.
  - Acceptance: Dashboard; real New Experiment configuration/resolved-config review; Runs active/history/detail with live GridWorld/event timeline/metrics/logs; Compare with compatibility checks/distributions/paired CIs/counts/layout-condition breakdowns; Artifacts real CSV/JSON/HTML/provenance preview/export; self-explanatory UX/help/tooltips/units/status semantics/accessibility/empty-loading-error-disabled states and lightweight onboarding; root `run_app.bat` remains functional; no fabricated state/data/replay.

- [ ] BLOCKED `T-532` — Add repository-root UI screenshots and bounded CI browser/render validation.
  - Depends on: `T-531`.
  - Acceptance: root `ui-screenshots/` documents committed stable page screenshots; CI capture is deterministic and bounded; diagnostic artifacts may be uploaded; fixtures never masquerade as scientific results; historical no-trace runs show replay unavailable.

- [ ] USER_VALIDATION_REQUIRED `T-511` — Validate the complete intended application workflow and UX.
  - Depends on: `T-512`, `T-531`, `T-532`.
  - Acceptance: intended user can configure an approved multi-seed experiment, launch/monitor truthful state and live GridWorld, inspect history/results, compare agents, export artifacts, understand help/status/error/disabled states, and complete/skip/replay onboarding; UI is coherent and presentation-ready; no fake progress/metrics/logs. Automated render/screenshot checks never close this task.

## WP6 — Historical v1.0 evidence plus future v1.1 evidence

Historical immutable baseline:

- [x] `T-600` — Execute historical frozen `protocol-v1.0` final matrix.
- [x] `T-601` — Validate/freeze historical v1.0 evidence.
- [x] `T-602` — Historical frozen v1.0 statistical analysis.
- [x] `T-603` — Historical v1.0 figures/tables/artifacts.
- [x] `T-604` — Historical thesis/defense evidence package.

DEC-042 replacement evidence path:

- [ ] BLOCKED `T-610` — Execute frozen `protocol-v1.1` final matrix with new run IDs after protocol freeze and application acceptance.
  - Depends on: `T-522`, `T-511`.
  - Acceptance: all predeclared v1.1 runs execute through the validated core/application path on the target machine; no cherry-picking; failed/interrupted/invalid outcomes retained with reasons; v1.0 evidence untouched.

- [ ] BLOCKED `T-611` — Validate and freeze accepted v1.1 final evidence.
  - Depends on: `T-610`.
  - Acceptance: exact run/file/provenance/checksum inclusion set is frozen with exclusions/reasons explicit.

- [ ] BLOCKED `T-612` — Run predeclared v1.1 paired statistical analysis and sensitivity diagnostics.
  - Depends on: `T-611`.
  - Acceptance: paired effects, 95% CIs, explicit n, per-layout/aggregate views, primary component estimands and secondary recovery sensitivity reproduce from frozen v1.1 evidence only.

- [ ] BLOCKED `T-613` — Generate v1.1 figures/tables/exports and superseding thesis/defense evidence package.
  - Depends on: `T-612`.
  - Acceptance: version-controlled rebuild produces final result artifacts and traceable claim/result/run mapping; historical v1.0 package remains archived rather than rewritten.

## Mandatory pre-WP7 user approval gate

**Current gate state: NOT APPROVED.** Existing technical/final evidence, a green PR, screenshots, or completed `T-613` do not authorize writing.

Only after the requested scientific/application refinement, new evidence path where applicable, and `T-511` human acceptance are satisfactory may the assistant explicitly ask: **“Do you approve starting WP7 thesis-writing/defense work now?”** Only a direct affirmative answer in the current conversation unlocks `T-700+`.

## WP7 — Thesis writing, review, and defense presentation

- [ ] BLOCKED `T-700` — Recheck current Department/University thesis/Word/citation/submission/defense rules.
  - Depends on: mandatory pre-WP7 user approval gate and the accepted final evidence state.
- [ ] DEFERRED `T-701` — Review completed theses later supplied by the user as contextual examples only.
- [ ] DEFERRED `T-710` — Draft the complete Greek thesis from citation-ready bibliography and accepted frozen evidence.
- [ ] DEFERRED `T-711` — Produce review-ready Word thesis with validated figures/tables/cross-references/citations.
- [ ] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate affected evidence.
- [ ] DEFERRED `T-713` — Freeze final thesis deliverable and required submission copies.
- [ ] DEFERRED `T-720` — Build defense narrative/slide outline/evidence map.
- [ ] DEFERRED `T-721` — Produce final PowerPoint plus speaker material per `docs/thesis/PRESENTATION_WORKFLOW.md`.
- [ ] DEFERRED `T-722` — Validate/rehearse defense package and tested demo/screenshot fallback.

## WP8 — Final audits and completion

- [ ] DEFERRED `T-800` — Final bibliography freshness/citation and official-guidance audit.
- [ ] DEFERRED `T-801` — Final reproducibility/protocol/results/privacy/licensing/docs/thesis/defense audit.
- [ ] DEFERRED `T-802` — Final delivery readiness.

## Task maintenance rule

Every material checkpoint/PR must review this registry. If it starts/completes/blocks/unblocks/supersedes/discovers work, reconcile the task and Resume state in the same branch checkpoint. Do not create a competing task list elsewhere; GitHub issues are tracking views, while this file remains canonical.
