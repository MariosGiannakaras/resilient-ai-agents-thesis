# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical task registry autonomously, one bounded dependency-valid task or coherent package at a time. Never bypass BLOCKED/DEFERRED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

This is the tracked bootstrap. `AGENTS.md` owns always-on rules; do not rebuild policy from chat history.

## Active package override — 2026-08-27

The current package is the user-approved pre-WP7 protocol-v1.1 + application refinement governed by DEC-042 and issues #87–#91.

- Work only on `feat/pre-wp7-protocol-v1.1-ui-rebuild`; do not create another implementation branch for this package.
- Keep draft PR #92 open through integrated scientific/runtime/UI/screenshots and user-facing acceptance; do not merge early.
- Preserve `protocol-v1.0`, finalized historical runs, and frozen evidence immutably.
- `protocol-v1.1` remains candidate until D0-specific non-final tuning/pilot evidence and validation justify freeze. Never run a v1.1 final campaign for CI/UI convenience.
- Keep `TASKS.md`, `CURRENT_STATUS.md`, decisions and #87–#91 synchronized at checkpoints.
- Root `ui-screenshots/` contains stable UI review screenshots; screenshots/fixtures are never scientific evidence.
- `T-511` remains USER_VALIDATION_REQUIRED and all `T-700+` WP7/WP8 work remains blocked until explicit user approval.

## Startup / resume

Use the explicit three-file session-start core and nothing else before selecting work:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Then inspect `git status`, current branch, recent commits, PR #92/check state, and the current Resume state. For DEC-042 work verify the branch is exactly `feat/pre-wp7-protocol-v1.1-ui-rebuild`; switch/update that existing branch rather than creating another one. Resume valid IN_PROGRESS work first, otherwise the first dependency-valid READY refinement task. Read only task-specific evidence after that.

## Current execution order

1. Governance/task handoff.
2. D0 + candidate protocol-v1.1 + paired statistical support.
3. Truthful application runtime/service layer.
4. Streamlit Dashboard → New Experiment → Runs/live GridWorld → Compare → Artifacts rebuild.
5. Root UI screenshots + bounded CI capture/validation.
6. Human E2E acceptance; only afterward ask explicitly whether WP7 may begin.

Work one bounded scope at a time and preserve recoverable checkpoint commits after substantial validated slices.

## Scientific package contract

- Retain F0 frozen Q-learning and C0 continual Q-learning from the common selected checkpoint.
- Add D0 Dyna-Q+ using only agent-visible observations, intended actions and rewards. Evaluator-only executed action, change/disturbance flags, regime and true state remain forbidden.
- Preserve F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48, and 32 paired final roots.
- Tune only D0-specific planning parameters through a small predeclared development/tuning search; never invent the selected planning budget/kappa.
- Use four fresh held-out v1.1 final layouts and a fresh precommitted final seed bank before any new final evidence is inspected.
- New remap IDs are `action-remap-2-swap` and `action-remap-4-cycle`; historical IDs remain unchanged.
- Primary reporting: cumulative deficit, immediate degradation and terminal gap/performance. Recovery remains secondary/sensitivity with explicit non-recovery. Add paired effects + 95% CIs, explicit n and layout-aware views. No composite resilience score or post-hoc favorable threshold.
- Keep R0 pilot evidence; do not reinstate its accepted construction unchanged or add deep RL merely to increase model count.

## Application package contract

- `src/resilient_agents/` works without UI. Streamlit never reimplements scientific execution.
- Put active orchestration/observation in an application-facing service: backend-derived queued/running/completed/failed/cancelled/interrupted state, heartbeat/progress/events, read-only live GridWorld observation, history and only safe lifecycle capabilities.
- Unsupported controls are explicitly unsupported; no fake state/progress/logs/metrics.
- Live observation must not change scientific RNG/actions. Visualization speed affects rendering cadence only.
- Historical runs without retained step trace display replay unavailable; never reconstruct a plausible trajectory.
- Compare/Artifacts consume real stored analysis/results. Keep root `run_app.bat` functional and the accepted local single-user/Streamlit baseline unless measured evidence forces an amendment.

## Execution / validation contract

For each scope, confirm dependencies and acceptance, implement the smallest complete solution, fail closed on invalid required state, run the smallest relevant deterministic checks, reconcile docs/tasks/issues, and review the actual diff.

Testing is proportional: known-answer, determinism, information-boundary, serialization, configuration, lifecycle-truthfulness, artifact-loading and representative render checks. No arbitrary coverage target, no broad fuzz/mutation/combinatorial expansion without a concrete risk, and no pilot/final matrices in CI. PR CI is the canonical full-suite guard when available; do not duplicate it merely for reassurance.

Do not submit an `APPROVE` review on your own PR. The repository normally permits an objective own-PR squash merge after green CI/review, but this package explicitly defers that own-PR squash merge until the integrated user-facing acceptance checkpoint.

Progress uses real finite denominators only. Report `Project: X/Y` only from canonical `T-*` entries, with issue/milestone X/Y when useful. In-progress/failed work never counts as complete.

## Stop conditions

Continue routine repository reading, implementation, Git, CI diagnosis, objective review and task selection without asking the user when accepted rules resolve them. Stop only for a genuine access/credential, external-machine, safety/privacy/legal/licensing blocker, a non-objective choice explicitly reserved for the user, or the mandatory human application/WP7 approval gate.

Technical completion, screenshots or green CI are not WP7 approval.

## Final report

Report objective progress; changed scientific/runtime/UI behavior; branch/PR/CI state; protocol-v1.1 candidate/frozen state; UI screenshots available for review; remaining human acceptance; exact next action; and explicit confirmation that WP7 is still blocked unless the user has directly approved it.
