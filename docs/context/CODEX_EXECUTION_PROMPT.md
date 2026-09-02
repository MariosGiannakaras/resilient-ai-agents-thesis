# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Preserve both T-610 histories, resume only the next dependency-valid task, and honor all downstream gates.`

## Startup / resume

1. Inspect Git/local/remote/PR/CI state and preserve any partial Study/evidence before synchronization.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Confirm the committed protocol-v2.1 authority and backend guard are unchanged. Never edit the immutable gate fields or weaken/hard-code around the guard.
4. Verify `protocol-v2.1-final--t610-recovery-01` remains the finalized 603/603 replacement from clean source commit `86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730` and verify the T-611 freeze manifest before any T-612 work.
5. Verify `results/studies/protocol-v2.1-final` remains the exact immutable 216-job failed/incomplete attempt defined by DEC-062. Never retry, resume, finalize, copy or mix it.

## Execution discipline

The persistent invariant is **Complete the canonical project task registry autonomously**, subject to dependency/approval gates and the explicit stop boundary of the active goal. Resume valid `IN_PROGRESS` work first and work on one bounded scope at a time.

Use native Windows CPython 3.12, the locked `uv` environment, CPU execution, the frozen recipe loader, `StudyService`, default executors, sequential scheduler, durable `StudyStore`, and `PROTOCOL_V21_FINAL_EXECUTION_AUTHORIZATION` exactly as implemented.

Preserve scientific failures as outcomes. DEC-062 recovery, T-610 execution and T-611 replacement-evidence validation/freeze are complete; the predecessor is permanently ineligible. T-612 is next and may analyze only the T-611 frozen evidence. Never replace roots/seeds, alter protocol choices, delete failed evidence, or mix execution instances.

Report only durable operational progress and infrastructure state during execution. Do not inspect or interpret method rankings, RQ outcomes, distributions, final conclusions, or post-hoc analyses.

The routine Git, PR creation, CI, objective review, corrections, and reconciliation flow remains autonomous. Do not submit an `APPROVE` review on your own PR. Perform a permitted own-PR squash merge when scope/evidence/checks are sound, but do not terminate healthy scientific execution merely to update documentation.

Report `Project: X/Y` only from a canonical finite denominator. In-progress/failed work never counts as complete.

## Stop conditions

T-611 is complete and this execution stops at its boundary. Preserve the original failed attempt, finalized replacement and frozen final-evidence package. T-612 is the next dependency-valid task; T-613 remains blocked by dependency and WP7 remains separately approval-gated.
