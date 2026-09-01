# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Resume T-610 from actual repository and durable Study state, use only the accepted protocol-v2.1 backend authorization path, and stop after objective T-610 completion without beginning T-611 or interpretation.`

## Startup / resume

1. Inspect Git/local/remote/PR/CI state and preserve any partial Study/evidence before synchronization.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Confirm the committed protocol-v2.1 authority and backend guard are unchanged. Never edit the immutable gate fields or weaken/hard-code around the guard.
4. Run the native Windows read-only preflight and fail closed unless the frozen invariants and canonical 603-job plan reproduce.
5. Inspect `results/studies/protocol-v2.1-final` and related evidence before creation. Create exactly once if absent; otherwise resume only genuinely outstanding jobs through validated lifecycle semantics.

## Execution discipline

The persistent invariant is **Complete the canonical project task registry autonomously**, subject to dependency/approval gates and this run's explicit T-610 stop boundary. Resume valid `IN_PROGRESS` work first and work on one bounded scope at a time.

Use native Windows CPython 3.12, the locked `uv` environment, CPU execution, the frozen recipe loader, `StudyService`, default executors, sequential scheduler, durable `StudyStore`, and `PROTOCOL_V21_FINAL_EXECUTION_AUTHORIZATION` exactly as implemented.

Preserve scientific failures as outcomes. Retry only recorded infrastructure failures, with the same scientific identity, when the accepted lifecycle permits it. Never replace roots/seeds, alter protocol choices, delete partial evidence, or mix source commits.

Report only durable operational progress and infrastructure state during execution. Do not inspect or interpret method rankings, RQ outcomes, distributions, final conclusions, or post-hoc analyses.

The routine Git, PR creation, CI, objective review, corrections, and reconciliation flow remains autonomous. Do not submit an `APPROVE` review on your own PR. Perform a permitted own-PR squash merge when scope/evidence/checks are sound, but do not terminate healthy scientific execution merely to update documentation.

Report `Project: X/Y` only from a canonical finite denominator. In-progress/failed work never counts as complete.

## Stop conditions

Stop after every planned T-610 job reaches an allowed terminal state, the Study is durably finalized with coherent lifecycle/provenance/checksum state, and canonical task/status/tracker state records objective T-610 completion. T-611 becomes next dependency-valid but must not start. If safe continuation becomes impossible, preserve all state and record the exact blocker rather than improvising a protocol amendment.
