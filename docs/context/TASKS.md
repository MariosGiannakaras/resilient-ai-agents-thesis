# Thesis Task Registry

**Status:** Active canonical execution ledger  
**Purpose:** Prevent task loss across Codex sessions, model-quota interruptions, machine restarts, or context changes.

`IMPLEMENTATION_ROADMAP.md` defines phase/dependency intent. `CURRENT_STATUS.md` summarizes current state. `END_TO_END_JOURNEY.md` defines lifecycle handoffs and user/Codex responsibilities. This file is the canonical checklist of concrete remaining work and resumable progress. If these active files disagree, reconcile them in the same PR before continuing.

## Mandatory session rule

Every Codex session MUST inspect this registry before selecting or resuming work. Do not rely only on chat/session memory and do not ignore valid current-session memory either.

Use both:

1. current Codex/session memory and context, when available;
2. durable repository evidence: this registry, Git branch/commits/diff, PR state, tests, and current-status files.

Repository evidence is the recovery authority when memory is missing, truncated, ambiguous, or conflicts with committed state.

## Status syntax

- `[x]` — completed and validated.
- `[ ] READY` — all required dependencies are complete and the task may be started now.
- `[ ] BLOCKED` — cannot proceed until the stated dependency/condition is resolved.
- `[ ] DEFERRED` — intentionally later; not a current blocker.
- `[ ] IN_PROGRESS` — actively being worked on; must have a resume note below.

A task is checked only when its acceptance condition is satisfied. Partial work remains unchecked. Whenever completing a task makes downstream dependencies valid, reconcile the downstream task status in the same change.

## Resume state

- **Current work package:** WP1 — Target-machine baseline
- **Current task:** `T-100`
- **State:** `BLOCKED until executed on the actual thesis experiment machine`
- **Active branch / PR:** none for `T-100`.
- **Last validated point:** `T-007` end-to-end lifecycle audit is complete and passed full repository CI in PR #38.
- **Exact next action:** clone/update current `main` on the actual thesis machine, start Codex from `CODEX_EXECUTION_PROMPT.md`, change `T-100` to `READY/IN_PROGRESS` after confirming it is the actual experiment machine, and execute it.

Whenever a task becomes `IN_PROGRESS`, replace this section with:

- task ID;
- branch and PR number if one exists;
- last completed/validated substep;
- tests already run and their result;
- relevant files changed;
- uncommitted work that exists, if any;
- exact next action.

## Quota/interruption resilience

Codex must assume a session can stop unexpectedly.

1. At session start inspect `git status`, current branch, recent commits, open PR state when relevant, this `Resume state`, and any `IN_PROGRESS` task.
2. If an `IN_PROGRESS` task exists, resume it before starting another task unless it has become genuinely blocked.
3. Use current-session memory to continue efficiently, but verify memory against repository state before changing task status.
4. Keep each work package on a descriptive branch. Intermediate branch commits are recovery checkpoints and are allowed even though the PR will normally be squash-merged to `main`.
5. Do not go through more than one substantial logical substep without preserving a recoverable checkpoint when practical. Good checkpoint boundaries include: a validated implementation slice, passing tests, a completed research decision draft, before/after a long experiment, or before moving to another major subtask.
6. At a checkpoint, update task/resume state when the next action is not obvious from the commit itself.
7. If quota ends abruptly before a registry update, the next session must inspect the existing working tree/diff and branch history before assuming the task was not started.
8. Never discard useful uncommitted work merely because the previous session ended. Validate it first.
9. Newly discovered required work gets a stable task ID and dependency in this registry before it can be forgotten. Do not hide required work only in prose, comments, or chat.
10. Completed tasks remain checked for auditability; do not delete them just to shorten the file.

## WP0 — Completed repository/research infrastructure

- [x] `T-001` — Establish private thesis repository, official project identity, core context, and controlled Git/PR workflow.
  - Acceptance: authoritative context and Git workflow are committed and validated.
- [x] `T-002` — Integrate the complete immutable `ThesisBibliography` research corpus with nested citation-ready trust, provenance, and integrity validation.
  - Acceptance: accepted full-corpus baseline and consumer validators pass.
- [x] `T-003` — Establish Python 3.12, `uv`, committed lockfile, and importable `src/resilient_agents/` research core.
  - Acceptance: locked environment and package tests pass in CI.
- [x] `T-004` — Establish scientific infrastructure contracts: ground-truth/agent-visible boundary, independent RNG streams, scenario/experiment/change/protocol contracts, and stage separation.
  - Acceptance: contract/invariant tests pass.
- [x] `T-005` — Establish filesystem-first run bundles, provenance/checksums, metric primitives, selective Git LFS, and guarded one-commit/one-push publication per whole experiment.
  - Acceptance: integration tests verify safe whole-experiment publication and retained evidence.
- [x] `T-006` — Reconcile active documentation, create the directly executable canonical Codex prompt, and enforce documentation consistency in CI.
  - Acceptance: stale bootstrap instructions are retired and documentation validator passes.
- [x] `T-007` — Audit the full Codex/user journey and define reliable handoffs from application completion through final experiments, analysis, thesis review/freeze, defense presentation, and delivery.
  - Depends on: `T-006`.
  - Acceptance: lifecycle/user/Codex handoffs, application-to-final-experiment dependency, frozen thesis/defense evidence package, thesis review cycle, PowerPoint/speaker-material workflow, task-status semantics, governance/requirements/decisions, and consistency validation are reconciled; full repository CI passes.

## WP1 — Target-machine baseline

- [ ] BLOCKED `T-100` — Run the privacy-minimal hardware/software/storage inventory on the actual thesis experiment machine.
  - Depends on: `T-006` plus execution on the actual thesis experiment machine.
  - Output: versioned accepted capability report with CPU, RAM, OS, Python/tooling, storage, GPU/VRAM/driver/runtime when present, and supported acceleration.
  - Acceptance: report is generated automatically on the actual machine, privacy-reviewed, tests/validation pass, and current docs/tasks are reconciled.
- [ ] BLOCKED `T-101` — Use the accepted inventory to resolve compute-dependent dependency/tooling constraints without freezing unsupported scientific choices.
  - Depends on: `T-100`.
  - Acceptance: dependency/runtime decisions that actually depend on hardware are documented and reproducible; CPU-compatible fallback remains clear where needed.

## WP2 — Research framing and GridWorld

- [ ] BLOCKED `T-200` — Complete source-traceable research-question and hypothesis framing from citation-ready evidence, while keeping feasibility-dependent choices provisional.
  - Depends on: `T-100` for feasibility-sensitive scope; bibliography baseline already complete.
  - Acceptance: bounded main RQ, minimal secondary RQs/hypotheses, evidence mapping, limitations, and open feasibility gates are documented.
- [ ] BLOCKED `T-210` — Complete bounded GridWorld prototype comparison (minimal custom implementation versus justified reuse/adaptation candidates).
  - Depends on: `T-100`.
  - Acceptance: prototypes/audit compare semantics, determinism, seeding, disturbance extensibility, testability, maintenance/license/dependency cost, and fit to the RQ.
- [ ] BLOCKED `T-211` — Record the final GridWorld implementation ADR.
  - Depends on: `T-210` and current research framing from `T-200`.
  - Acceptance: one option is selected with evidence, alternatives, consequences, and reopening conditions.
- [ ] BLOCKED `T-212` — Implement the selected GridWorld in `src/resilient_agents/` using the existing environment/information contracts.
  - Depends on: `T-211`.
  - Acceptance: explicit state/action/reward/termination/change/disturbance semantics; no UI dependency.
- [ ] BLOCKED `T-213` — Add known-answer, reference-trace, deterministic replay, disturbance-isolation, termination, and information-leakage tests for the GridWorld.
  - Depends on: `T-212`.
  - Acceptance: environment scientific invariants pass reproducibly.

## WP3 — Metrics and agent/model selection

- [ ] BLOCKED `T-300` — Finalize operational definitions/estimands for resilience, degradation, recovery, post-change performance, non-recovery, and supporting diagnostics.
  - Depends on: `T-200`, `T-212`.
  - Acceptance: every metric has a clear estimand, interpretation, required inputs, edge-case behavior, and RQ mapping.
- [ ] BLOCKED `T-301` — Validate all selected metrics against synthetic known-answer trajectories.
  - Depends on: `T-300`.
  - Acceptance: hand-checkable fixtures verify values and non-recovery is never converted into artificial horizon recovery.
- [ ] BLOCKED `T-310` — Complete source-traceable comparison of scientifically distinct agent/model roles.
  - Depends on: `T-100`, `T-200`, `T-212`.
  - Acceptance: inclusion/exclusion matrix covers nominal baseline, continual/adaptive roles, robustness role, and any optional detector/reset decomposition only when scientifically distinct.
- [ ] BLOCKED `T-311` — Resolve formal citation support for any robust-MDP comparator retained for final use.
  - Depends on: `T-310` deciding that robust MDP remains necessary.
  - External action if required: verify/promote appropriate robust-MDP evidence upstream in `ThesisBibliography`, then perform a new immutable bibliography synchronization.
  - Acceptance: final robust-MDP claims/selection are supported by citation-ready evidence, or the comparator is explicitly excluded.
- [ ] BLOCKED `T-312` — Implement the selected small agent set behind the common information-limited `Agent` contract.
  - Depends on: `T-310`; `T-311` if robust MDP is retained.
  - Acceptance: agent contract tests and tiny known-MDP/reference tests pass; no privileged hidden information.

## WP4 — Pilot protocol and headless experiment system

- [ ] BLOCKED `T-400` — Define development/tuning/pilot/final scenario partitions and versioned pilot protocol.
  - Depends on: `T-213`, `T-301`, `T-312`.
  - Acceptance: partitions do not overlap; seeds/budgets/severities/tuning/failure/exclusion rules are explicit and justified rather than convenience defaults.
- [ ] BLOCKED `T-401` — Complete the headless experiment runner/orchestration path for the selected environment/agents/metrics.
  - Depends on: `T-400`.
  - Acceptance: a full experiment with multiple seeds runs without UI, persists continuously, resumes safely where supported, finalizes one auditable bundle, and uses the existing publisher correctly.
- [ ] BLOCKED `T-402` — Complete reproducible analysis pipeline for experiment summaries and pilot diagnostics.
  - Depends on: `T-401`.
  - Acceptance: stored run bundles deterministically produce validated summaries/diagnostics through version-controlled code.
- [ ] BLOCKED `T-410` — Execute pilots and record runtime, variance, failures, recovery/metric behavior, storage volume, and agent-specific issues.
  - Depends on: `T-401`, `T-402`.
  - Acceptance: pilot evidence answers the predefined feasibility/protocol questions without contaminating final evaluation.
- [ ] BLOCKED `T-411` — Refresh decision-driving bibliography before final protocol freeze.
  - Depends on: `T-410`.
  - Acceptance: freshness review occurs in `ThesisBibliography`; any required promotion/new evidence is synchronized immutably before freeze.
- [ ] BLOCKED `T-412` — Freeze `protocol-v1.0` and the statistical analysis plan.
  - Depends on: `T-410`, `T-411`.
  - Acceptance: final RQs/hypotheses, model set, scenario matrix, severities, seeds/repetitions, budgets, tuning rules, primary/secondary metrics, recovery definition, exclusions, and statistical estimands are versioned before final results are inspected.

## WP5 — Experiment management and dashboard

- [ ] BLOCKED `T-500` — Implement only the pilot-proven experiment-management features needed for final work: truthful lifecycle state, history/registry, batch execution, interruption/recovery where safe, and current resource snapshot.
  - Depends on: `T-412`.
  - Acceptance: features use filesystem run bundles as source of truth; any index/database is rebuildable.
- [ ] BLOCKED `T-510` — Implement the bounded local Streamlit dashboard as a thin layer over the same validated core.
  - Depends on: `T-500`.
  - Acceptance: New Experiment, Run/Monitor, History, Compare, Detailed Analysis, and Artifacts/Export workflows operate on real core data with no duplicated scientific logic.
- [ ] BLOCKED `T-511` — Validate the complete application/user workflow, UX, truthful state, screenshots, exports, and end-to-end consistency.
  - Depends on: `T-510`.
  - Acceptance: the intended user can configure and execute an approved multi-seed experiment, monitor it, inspect history/results, compare agents, and export artifacts through the local application; no fake progress/metrics/logs; desktop/laptop workflows are coherent, polished, and presentation-ready.
  - Handoff: satisfying this task marks the application complete for the intended thesis workflow and unlocks the frozen final experiment campaign.

## WP6 — Final experiments, frozen evidence, and writing package

- [ ] BLOCKED `T-600` — Execute the frozen final experiment matrix under `protocol-v1.0` using the validated application/core workflow.
  - Depends on: `T-412`, `T-511`.
  - Acceptance: all predefined final runs are retained with provenance/status/reasons; the final campaign uses the validated workflow and one automatic publication commit/push occurs per whole experiment. Any necessary headless fallback is documented and uses the identical scientific core/configuration path.
- [ ] BLOCKED `T-601` — Validate final-run completeness and freeze the accepted final evidence set under `results/thesis-final/`.
  - Depends on: `T-600`.
  - Acceptance: included/excluded/failed runs and reasons are explicit; checksums/protocol/config/commit links are complete; no cherry-picking.
- [ ] BLOCKED `T-602` — Run the frozen statistical analysis and robustness/sensitivity diagnostics exactly as specified.
  - Depends on: `T-601`.
  - Acceptance: reproducible outputs come only from frozen evidence and frozen analysis definitions.
- [ ] BLOCKED `T-603` — Generate final figures, tables, summaries, and export artifacts from frozen evidence.
  - Depends on: `T-602`.
  - Acceptance: version-controlled rebuild reproduces thesis artifacts from stored final data.
- [ ] BLOCKED `T-604` — Freeze the thesis/defense evidence package used by downstream writing and presentation work.
  - Depends on: `T-603`.
  - Output: versioned RQ/protocol summary, method/config references, included/excluded run manifest, statistical outputs, figure/table/caption registry, and claim-to-result/source/run mapping.
  - Acceptance: a future writer/presentation builder can trace every planned method/result claim to citation-ready literature or frozen experiment evidence without reinterpreting raw runs ad hoc.

## WP7 — Thesis writing, review, and defense presentation

- [ ] DEFERRED `T-700` — Recheck current Department/University thesis, Word template, citation, submission, defense/presentation, duration, and required-file rules.
  - Depends on: research sufficiently mature for writing; must be repeated near submission/defense.
  - Acceptance: current official guidance is recorded and supersedes examples/historical guidance.
- [ ] DEFERRED `T-701` — Review any completed theses later supplied by the user as contextual structure/presentation examples only.
  - Depends on: user supplying them near writing phase.
  - Acceptance: useful conventions are identified without treating examples as scientific or official authority.
- [ ] DEFERRED `T-710` — Draft the complete Greek thesis from citation-ready bibliography and the frozen evidence package.
  - Depends on: `T-604`, `T-700`.
  - Acceptance: every material scientific claim traces to citation-ready evidence or frozen experiment artifacts; methodology matches the executed protocol; no result is reconstructed from memory or ad-hoc raw-run inspection.
- [ ] DEFERRED `T-711` — Produce a review-ready Word thesis with validated figures/tables/cross-references, bilingual front matter, citations, and current required formatting.
  - Depends on: `T-710`.
  - Acceptance: coherent `.docx` suitable for supervisor/reviewer review and current official requirements.
- [ ] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate affected claims, citations, figures, tables, and methodology.
  - Depends on: `T-711` plus actual feedback if a review cycle is requested.
  - Acceptance: received feedback is dispositioned and implemented where appropriate, or the absence of a required review cycle is explicitly recorded; no correction silently breaks evidence/protocol consistency.
- [ ] DEFERRED `T-713` — Freeze the final thesis deliverable and required submission copies.
  - Depends on: `T-711`, `T-800`, and `T-712` when feedback exists.
  - Acceptance: final `.docx` and any officially required exports are validated, versioned, and tied to the final evidence/citation state.
- [ ] DEFERRED `T-720` — Build the defense narrative, slide outline, and slide-to-thesis/result/source evidence map.
  - Depends on: `T-713`, `T-604`, `T-511`.
  - Acceptance: slide plan covers only the material required to defend the thesis within the official duration and every substantive claim/visual has a traceable source.
- [ ] DEFERRED `T-721` — Produce the final PowerPoint deck plus speaker material according to `docs/thesis/PRESENTATION_WORKFLOW.md`.
  - Depends on: `T-720`.
  - Output: final `.pptx`, embedded slide speaker notes, separate full spoken Greek script, and repository-backed presentation assets.
  - Acceptance: slides and spoken script agree with the final thesis and frozen evidence; the script is detailed enough for rehearsal/following/reading during preparation.
- [ ] DEFERRED `T-722` — Validate and rehearse the defense package.
  - Depends on: `T-721`.
  - Acceptance: PowerPoint rendering/media/notes are correct; timing fits official limits with margin; graphs/text are legible; demo/screenshots have a tested fallback; thesis/slides/script numerical and factual consistency checks pass.

## WP8 — Final audits and completion

- [ ] DEFERRED `T-800` — Perform final bibliography freshness/citation and official-guidance audit before thesis freeze.
  - Depends on: `T-711` nearing final form.
  - Acceptance: citations/claims map to current verified citation-ready evidence; any approved bibliography update is synchronized immutably; current submission/defense guidance has been rechecked.
- [ ] DEFERRED `T-801` — Perform final reproducibility, protocol, results, privacy, licensing, documentation, thesis, and defense-package audit.
  - Depends on: `T-713`, `T-722`, `T-800`.
  - Acceptance: no unresolved scientific/provenance/privacy/licensing/delivery blocker remains; active docs agree; thesis and presentation agree with frozen evidence.
- [ ] DEFERRED `T-802` — Final delivery readiness.
  - Depends on: `T-801`.
  - Acceptance: thesis answers the approved research question with reproducible evidence; the application supports the real workflow; final thesis, PowerPoint, speaker script/notes, and required delivery/demo materials are ready.

## Task maintenance rule

Every material PR must review this registry. If it completes, starts, blocks, unblocks, supersedes, or discovers a task, update the corresponding checkbox/status/dependencies/resume state in the same PR.

Do not duplicate a second competing task list elsewhere. Roadmaps may explain phases; lifecycle docs may explain handoffs; issue/PR descriptions may describe a work package; this file remains the canonical execution checklist.