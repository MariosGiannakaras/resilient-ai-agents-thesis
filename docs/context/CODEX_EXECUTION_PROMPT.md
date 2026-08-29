# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Complete the canonical project task registry autonomously, one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR creation, CI, objective diff review, corrections, task reconciliation, and next-task selection as work to perform, not reasons to stop. Recover actual repository/Git/GitHub/evidence state before acting. Never bypass BLOCKED/DEFERRED/SUPERSEDED work, fabricate evidence, cross an external approval gate, or create a parallel branch when the active package pins one.`

Repository/Git/GitHub/evidence state beats stale chat/session memory or stale prose.

## Active package

DEC-048/050 controls protocol-v2 methodology, DEC-051 controls the completed Study-first backend, and issue #95 tracks the scientific successor.

- Use `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92; no parallel main-repo implementation branch and no early merge.
- Preserve protocol-v1.0, FINAL-* and historical R0 evidence immutably.
- Candidate v1.1 remains auditable non-final history; do not execute old T-522 or inspect/generate its final reserve.
- T-524, T-525 and T-529 are COMPLETE.
- T-526 is READY and is the next dependency-valid scientific gate on the validated physical Windows thesis machine.
- T-527 is BLOCKED on T-526; final methods/layouts/budgets/hyperparameters/severities/roots/statistics remain unfrozen.
- T-528 is BLOCKED on T-527; its T-529 backend dependency is satisfied. The final frontend must use a framework different from NiceGUI.
- T-511 remains later intended-user acceptance; T-700+ remains blocked until accepted final evidence/application and explicit user approval.

## Startup / resume

1. Inspect `git status`, staged/unstaged/untracked work, branch, recent commits, upstream/ahead-behind state and current remote head.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Inspect PR #92/current-head CI and resume valid `IN_PROGRESS` work before READY work.
4. Preserve interrupted work; never use destructive cleanup merely to obtain a clean tree.
5. Read only task-specific decisions/research required by the recovered active task.

When objective Git/GitHub/finalized-evidence state proves prose stale, preserve completed work, reconcile the docs at the next coherent checkpoint and continue. Never repeat completed work solely because a resume note is stale.

## Current T-526 physical gate

T-526 may execute only on the validated physical Windows thesis machine through:

`powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1`

The latest physical attempt did not execute scientific work: repository preflight failed because the checkout was stale and contained untracked prior PR draft `temp_body.md`. No T-526 output directory or scientific evidence was produced.

Before retrying:

1. inspect `temp_body.md` and preserve any unique content; remove it from the working tree only if confirmed obsolete;
2. fetch and fast-forward the physical active branch to the reviewed current remote head without destructive reset/force operations;
3. verify native-Windows Git is clean and the committed plan/runbook/entrypoint are present;
4. execute the predeclared runner exactly once;
5. retain all scientific failures/evidence as-is and never replace roots based on outcomes.

Hosted CI/WSL/another machine cannot substitute for T-526 runtime evidence.

## Protocol-v2 scientific contract

Phase A independently trains every retained method under the same semantic environment/information/action/reward/gamma contract and principal actual-environment-interaction budget, with isolated no-learning probes.

For each method/root/layout, Phase B starts from that unit's own exact Phase-A scientific checkpoint. Any common prefix is no-learning. At the exact boundary clone identical scientific state into FN, FD, AN and AD. Adaptive updates begin only on the first post-boundary transition; Frozen learning state cannot mutate. Do not reset replay, optimizer, exploration, warm-up, model/recency, schedules, counters or RNG state at change unless a later frozen protocol explicitly defines it.

Primary adaptation benefit is matched four-branch DiD. Root/run is the independent unit; layouts/checkpoints/episodes are blocked/repeated measurements. Scientific failures remain outcomes and seeds are never replaced from outcomes.

Pilot-gated core candidates are Q-Learning, SARSA, DQN, PPO and Dyna-Q+. Dyna-Q is an ablation; A2C remains conditional; Random is a supporting reference. Do not freeze final scientific choices before T-527.

## Completed T-529 boundary

DEC-051/T-529 makes `Study` the application-facing aggregate. The implemented UI-independent chain is:

> immutable recipe -> deterministic plan -> real Phase A -> exact checkpoint -> optional common no-learning prefix -> atomic FN/FD/AN/AD -> validation -> root/layout analysis -> deterministic evidence export

It includes restart-safe `StudyStore`/`StudyService`, stable identities/lineage, scientific-vs-infrastructure failure semantics, explicit outcome denominators, default real protocol-v2 executors and machine-readable CSV/JSON/result-ID/provenance handoff. T-529 generates no thesis prose, final thesis figures or PPTX. Do not re-audit/rebuild it without new objective regression evidence.

## Task order

Remaining dependency chain:

`T-526 -> T-527 -> T-528 -> T-511 -> T-610..T-613 -> explicit user approval -> WP7`.

T-529 is already a satisfied dependency. Do not access final reserve early or use hosted CI as a physical-pilot substitute.

## Validation and Git

For each **one bounded scope**, validate acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, inspect the diff, reconcile docs/issues and push a coherent recoverable checkpoint.

Testing is proportional: scientific invariants, information boundaries, determinism, checkpoint fidelity, configuration, lifecycle/provenance, statistical known answers and representative integration. Scientific experiment matrices are not CI tests. PR CI is the canonical full-repository guard.

Do not submit an `APPROVE` review on your own PR. Historical workflow may permit an **own-PR squash merge**, but this active draft PR remains unmerged until its integration gates allow it.

Report `Project: X/Y` only from a real canonical finite denominator. In-progress/failed work never counts as complete.

## Stop conditions

Continue routine repository work, Git/GitHub, CI diagnosis, objective review, reconciliation and dependency-valid next-task selection autonomously. Stop only when the next valid action genuinely requires unavailable physical-machine evidence, access/credentials, a safety/privacy/legal/licensing boundary, a user-reserved subjective choice, mandatory intended-user/supervisor acceptance or explicit pre-WP7 approval.