# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Preserve the failed T-610 attempt, execute the authorized DEC-062 clean replacement recovery, and stop before T-611 or interpretation.`

## Startup / resume

1. Inspect Git/local/remote/PR/CI state and preserve any partial Study/evidence before synchronization.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Confirm the committed protocol-v2.1 authority and backend guard are unchanged. Never edit the immutable gate fields or weaken/hard-code around the guard.
4. Run the native Windows read-only preflight and fail closed unless the frozen invariants and canonical 603-job plan reproduce.
5. Verify `results/studies/protocol-v2.1-final` and its 216 completed jobs remain the exact immutable failed/incomplete attempt defined by DEC-062. Never retry, resume, finalize, copy or mix it. Create only the distinct replacement instance after the correction is merged and the clean preflight passes.

## Execution discipline

The persistent invariant is **Complete the canonical project task registry autonomously**, subject to dependency/approval gates and this run's explicit T-610 stop boundary. Resume valid `IN_PROGRESS` work first and work on one bounded scope at a time.

Use native Windows CPython 3.12, the locked `uv` environment, CPU execution, the frozen recipe loader, `StudyService`, default executors, sequential scheduler, durable `StudyStore`, and `PROTOCOL_V21_FINAL_EXECUTION_AUTHORIZATION` exactly as implemented.

Preserve scientific failures as outcomes. DEC-062 is the accepted recovery path: apply the existing DEC-054 settlement at the missing Study Phase-A boundary, merge through normal CI/review, run the clean preflight, and execute `protocol-v2.1-final--t610-recovery-01` from zero. Retry only recorded infrastructure failures in that replacement when the accepted lifecycle permits it. Never replace roots/seeds, alter protocol choices, delete partial evidence, or mix source commits.

Report only durable operational progress and infrastructure state during execution. Do not inspect or interpret method rankings, RQ outcomes, distributions, final conclusions, or post-hoc analyses.

The routine Git, PR creation, CI, objective review, corrections, and reconciliation flow remains autonomous. Do not submit an `APPROVE` review on your own PR. Perform a permitted own-PR squash merge when scope/evidence/checks are sound, but do not terminate healthy scientific execution merely to update documentation.

Report `Project: X/Y` only from a canonical finite denominator. In-progress/failed work never counts as complete.

## Stop conditions

Preserve the original unfinalized Study, 216 completed jobs, run-index records and exact failure event. T-610 completes only when the fresh DEC-062 replacement from one corrected merged commit accounts for all 603 planned jobs and is durably finalized with coherent lifecycle/provenance/checksum state. Then reconcile canonical status, make T-611 next and stop. Do not inspect outcomes for interpretation or begin T-611/T-612/T-613/WP7.
