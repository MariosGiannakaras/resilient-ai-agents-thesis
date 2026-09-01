# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Start the active T-534 UI implementation from latest current main and follow GitHub issue #104 as the operational checklist. Preserve the canonical scientific/application authorities and stop before the separate BLOCKED T-610 final-experiment gate.`

The repository's persistent execution invariant is **Complete the canonical project task registry autonomously**, but only through dependency-valid, non-gated work. For this run the active bounded package is T-534.

## Startup / resume

1. Inspect Git status, current branch, recent commits, upstream/ahead-behind state, open PR and CI. Resume `IN_PROGRESS` work only if it belongs to the current T-534 implementation package.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Confirm T-534 is still the active task and recover the objective GitHub state for **issue #104 — T-534 Clean protocol-v2.1 PySide6 experiment-first UI rebuild**.
4. Read issue #104 completely and execute its unchecked implementation/validation/acceptance items. The issue is an operational checklist, not a competing authority: when in doubt, follow the canonical files it names, especially DEC-059, DEC-060, DEC-061, `configs/protocols/protocol-v2.1-final.json`, `docs/research/RQ_EVIDENCE_TRACEABILITY.md` and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`.
5. Work on **one bounded scope** at a time inside one coherent T-534 branch/PR. Start from latest current `main`; do not continue a paused/pre-v2.1 UI branch/worktree.

Repository/Git/GitHub/evidence state beats stale memory or stale prose. Do not invent UI behavior, scientific semantics, acceptance criteria, or completion state when the canonical docs/issue provide them.

## Execution discipline

Issue #104 owns the detailed implementation checklist: desktop reuse/redesign boundaries, protocol-v2.1 migration, Experiment/Run/Results/Evidence behavior, Frozen/Adaptive live presentation, RQ1/RQ2/RQ3 results semantics, Evidence UX, scientific thin-client invariants, accessibility/polish, DEVELOPMENT fixtures, targeted tests, screenshots, launcher validation, documentation reconciliation, PR/CI and Definition of Complete.

Use DEVELOPMENT/synthetic fixtures for UI implementation/testing. Final-reserve execution, final outcomes and thesis Results/Discussion remain outside this package.

Perform routine Git, PR creation, CI, objective diff review, corrections and documentation reconciliation as work to do, not reasons to stop. Repository CI is the canonical full-suite pre-merge check.

Do not submit an `APPROVE` review on your own PR. When issue #104 acceptance is objectively satisfied and exact-head CI is green, perform the permitted own-PR squash merge and verify the merged `main` before marking T-534 complete.

Report `Project: X/Y` only from a real canonical finite denominator in `TASKS.md`. In-progress/failed work never counts as complete.

## Stop conditions

Complete T-534 through implementation, targeted validation, issue-checklist reconciliation, PR/CI correction, documentation reconciliation and permitted merge. Stop before T-610 unless separate explicit scientific authorization is supplied.
