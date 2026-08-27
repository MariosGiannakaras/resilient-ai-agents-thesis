# Codex Execution Prompt

## User entrypoint

After cloning/updating the repository on the actual thesis machine, give Codex only this Goal-mode command:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent work package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and selection of the next READY task as work to perform—not reasons to stop. Never bypass BLOCKED or DEFERRED work, fabricate evidence, cross an explicit external approval gate, or create a parallel branch when the active work package pins a branch.`

This file is the single tracked execution bootstrap. `AGENTS.md` contains the always-on rules and routing map; do not reconstruct project policy from chat history.

## Active-package override — 2026-08-27

The current package is the user-approved **pre-WP7 protocol-v1.1 + application refinement**, governed by `DEC-042` and GitHub issues #87–#91.

For this package only:

- work **only** on `feat/pre-wp7-protocol-v1.1-ui-rebuild`;
- do not create a second implementation branch or split the package into parallel PR branches;
- preserve `protocol-v1.0`, every finalized historical run, and existing frozen evidence immutably;
- `protocol-v1.1` remains candidate until D0-specific non-final tuning/pilot evidence and validation justify a freeze;
- do not run a v1.1 final campaign merely to satisfy implementation, UI, tests, or CI;
- do not start `T-700+`, thesis prose, defense work, or later writing stages;
- keep `TASKS.md`, `CURRENT_STATUS.md`, decisions, issue checklists, and this handoff synchronized at meaningful checkpoints;
- stable UI screenshots belong under repository-root `ui-screenshots/` and are review artifacts, never scientific evidence;
- `T-511` remains `USER_VALIDATION_REQUIRED` until real human E2E acceptance.

If a fresh Codex session starts while this branch is open, it must resume this package before selecting any unrelated work.

## Startup / resume

1. Inspect `git status`, current branch, recent commits, open PR/check state, and the branch diff.
2. Read exactly the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. If the current package is the DEC-042 refinement, verify the branch is exactly `feat/pre-wp7-protocol-v1.1-ui-rebuild`; switch to/update that existing branch rather than creating another one.
4. Inspect the `Resume state`, DEC-042, and issues #87–#91 only as needed to resolve current progress. Repository/Git evidence wins over stale prose.
5. Resume valid `IN_PROGRESS` work first. Otherwise select the first dependency-valid READY refinement subtask. Never start BLOCKED/DEFERRED work.
6. Read only the task-specific specifications/evidence needed for the bounded scope. Search before broad reading.
7. Preserve a recoverable checkpoint after each substantial validated slice.

Do not spend the session re-summarizing established context once dependencies and scope are clear. Execute.

## Current refinement execution order

The intended dependency order is:

1. **Governance/handoff:** canonical task/status/decision state points to this branch/package.
2. **Scientific implementation:** add deterministic information-limited D0 Dyna-Q+, a bounded D0-specific tuning surface, candidate protocol-v1.1 with four fresh held-out final layouts/fresh final seed bank/structural remap names, and paired-effect 95% CI analysis support.
3. **Runtime service:** application-facing active-run registry/status/heartbeat/events/read-only live GridWorld observation plus only lifecycle controls the backend can safely honor.
4. **UI rebuild:** Dashboard, New Experiment, Runs/live GridWorld, Compare, Artifacts using real backend/stored data; self-explanatory helper text/tooltips/units/statuses/empty-loading-error-disabled states and lightweight onboarding.
5. **UI screenshot/CI review:** repository-root `ui-screenshots/`, bounded deterministic browser/render capture, and CI diagnostics without fabricated scientific results.
6. **Human acceptance:** expose the completed screenshots/application to the user and keep T-511 open until explicit E2E acceptance.

Do not skip ahead if an earlier step supplies a contract needed by the next one.

## Scientific contract for this package

- Retain F0 frozen Q-learning and C0 continual Q-learning from the common selected nominal checkpoint.
- Add D0 Dyna-Q+ as a third scientifically distinct tabular agent. D0 learns/plans only from agent-visible interaction data; evaluator-only executed-action, disturbance, change-indicator, regime, or true-state information is prohibited.
- Preserve the validated common F0/C0 values: alpha `0.5`, gamma `0.96875`, epsilon `0.125`, training `512` episodes/layout, pre-change `16`, post-change `32`, horizon `48`, and `32` paired final roots.
- Tune only genuinely D0-specific parameters through a small predeclared development/tuning search. Never invent a selected planning-step count or kappa.
- New v1.1 final layouts/seeds must be fresh and precommitted before any new final evidence is inspected.
- New condition names are `action-remap-2-swap` and `action-remap-4-cycle`; historical v1.0 identifiers remain unchanged in old evidence.
- Primary reporting emphasizes cumulative deficit, immediate degradation, terminal gap/performance. Recovery is secondary/sensitivity; preserve explicit non-recovery and all predeclared sensitivity settings.
- Add paired agent effects and 95% confidence intervals with explicit n and layout-aware views. Do not add a composite resilience score or post-hoc favorable threshold.
- Keep R0 pilot evidence; do not reinstate the accepted R0 construction unchanged and do not add deep RL just to increase model count.

## Application/UI contract for this package

- `src/resilient_agents/` must remain functional without Streamlit.
- Put active-experiment orchestration/observation behind an application-facing service/facade; do not implement scientific execution semantics in Streamlit callbacks.
- Every status/progress/log/metric/control is backend-derived. If pause/resume or another control is unsafe/unsupported, advertise that capability truthfully and disable/omit the control.
- Live GridWorld observation is read-only and must be proved not to change scientific RNG/state/action choices.
- Visualization speed changes only rendering cadence.
- Existing finalized runs without retained step trace must display “replay unavailable”; never reconstruct a plausible path.
- Compare/Artifacts must consume real result bundles/analysis/artifacts rather than dumping raw JSON as the primary experience.
- Keep root `run_app.bat` functional and local single-user architecture; no cloud/auth/microservices/custom frontend rewrite unless a measured requirement forces an explicit amendment.

## Execution contract

For each bounded scope:

1. Confirm dependencies, acceptance conditions, scientific/provenance/UI constraints, and the smallest evidence needed.
2. Implement the smallest complete solution that satisfies the active acceptance condition.
3. Fail closed on invalid or ambiguous required state; never fabricate fallbacks or apparent success.
4. Run only targeted deterministic tests/validators while implementing.
5. Reconcile affected active source-of-truth docs and issue/task progress in the same checkpoint.
6. Before PR/checkpoint review, run the documentation consistency validator and directly affected targeted checks. Let GitHub PR CI be the canonical full-suite guard when available; do not duplicate it for reassurance.
7. Mark progress complete only when its acceptance condition is objectively satisfied.
8. Review the actual diff. Fix concrete findings before proceeding.
9. Keep the single branch recoverable with meaningful commits. Do not merge it early merely because one milestone is green.

For this user-directed package, the normal autonomous own-PR merge rule is superseded: keep the implementation branch/PR open through the integrated scientific + application + screenshot refinement and user-facing acceptance checkpoint. Do not squash-merge the branch into `main` before that package-level gate.

## Testing / quota discipline

Testing is risk-based and proportional:

- prefer known-answer, deterministic, information-boundary, serialization, configuration, lifecycle-truthfulness, artifact-loading, and representative render tests;
- no arbitrary coverage target;
- no broad mutation/fuzz/property/combinatorial/snapshot expansion without a concrete risk;
- no pilot/final experiment matrix in CI;
- do not repeatedly run the full suite locally when PR CI is available;
- screenshots validate UI rendering only and never promote fixtures to scientific evidence.

## Progress reporting and recovery

- Use `X/Y` only from finite checklist denominators in `TASKS.md`/issues #87–#91.
- Preserve intermediate branch commits after substantial validated substeps.
- If a session stops unexpectedly, inspect the existing branch diff/commits/check state before assuming work is absent.
- Never discard prior branch work solely because session memory is missing.
- Add newly discovered required work to the canonical task ledger and the relevant issue before it can be forgotten.

## Stop conditions

Continue without asking the user for routine implementation, repository reading, Git, CI, objective review, evidence retrieval, or task selection that accepted rules can resolve.

Stop/report only for a genuine blocker such as unavailable credentials/access, required execution on another physical machine, unresolved safety/privacy/legal/licensing constraints, a non-objective academic/product choice explicitly reserved for the user, or the mandatory human application/WP7 approval gates.

Technical completion, a successful test, screenshot capture, or green CI is not permission for WP7.

## Final report for this package

Report only:

- objective milestone/task progress;
- material code/scientific/UI changes;
- branch/PR/checkpoint state;
- targeted test/CI conclusions;
- protocol-v1.1 candidate/frozen state and any non-final experiment still required;
- UI screenshots/artifacts available for user review;
- remaining human E2E acceptance items;
- exact next action;
- explicit confirmation that WP7 remains blocked unless/until the user approves it.
