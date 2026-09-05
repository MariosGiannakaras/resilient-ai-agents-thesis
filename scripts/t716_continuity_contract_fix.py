#!/usr/bin/env python3
"""Keep the interrupted-session reconciliation compatible with durable bootstrap contracts."""
from pathlib import Path

SEMANTIC = "b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1"
BIB = "27674a566ab55e4491b74243fe077a31ef81ae73"

PROMPT = f"""# Codex Execution Prompt

## User entrypoint

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely.`

Complete the canonical project task registry autonomously within repository permissions and the explicit scientific/external-input gates below.

## Startup / resume

1. Recover actual state first: inspect git status/current branch/recent commits, open PRs, CI, issues and any unmerged or `IN_PROGRESS` work. Preserve unique partial work; repository/Git/GitHub evidence wins over stale chat memory.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Read further authorities only for the selected task. Prefer targeted search and direct dependencies over broad repository rereads.
4. Select one bounded scope that is dependency-valid. In-progress/failed work never counts as complete.

## Durable current state

- T-610 final protocol-v2.1 execution, T-611 evidence freeze, T-612 predeclared analysis and T-613 scientific thesis/defense assets are COMPLETE. Preserve the failed 216-job predecessor and accepted 603/603 DEC-062 replacement as distinct immutable histories.
- The accepted PySide6 **Experiment / Run / Results / Evidence** application is complete through T-537. T-538 is optional/deferred presentation polish, not a thesis blocker.
- T-700, T-701, T-702, T-710, T-711, T-714, T-715 and T-716 are COMPLETE.
- Accepted T-716 review authority: `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic OOXML SHA-256 `{SEMANTIC}`; 11/11 final acceptance gates PASS.
- Current bibliography consumer authority: immutable upstream SHA `{BIB}` (601 canonical / 129 citation-ready / 19 research-material records / 281 indexed originals).
- The current task ID is T-712, but it is DEFERRED until actual supervisor/reviewer feedback exists. Internal review is never relabelled as external feedback.
- T-713 remains DEFERRED until T-712 is resolved where applicable plus authoritative official person/declaration metadata and final Word/submission checks.
- T-720/T-721/T-722 and T-800/T-801/T-802 are downstream of T-713. T-803 standalone Windows packaging remains post-thesis under issue #94.

## Execution / Git / CI discipline

Use targeted checks during implementation; PR CI is the canonical full-suite pre-merge check. Handle routine Git, PR creation, CI, objective diff review, correction and merge without pushing bookkeeping back to the user when tools permit it.

Do not submit an `APPROVE` review on your own PR. An own-PR squash merge is allowed only after required checks/objective review pass and repository rules permit it. Preserve unrelated changes and avoid destructive Git operations.

At coherent checkpoints report objective progress only as `Project: X/Y` when `TASKS.md` defines a real denominator. In-progress/failed work never counts as complete.

Scientific/bibliographic state fails closed: do not change frozen protocol choices, roots/seeds, estimands, evidence, final interpretation or registered quantitative assets; do not hand-edit generated bibliography content; do not invent official metadata, feedback, deadlines or defense rules.

## Stop conditions

If T-712 has no actual supervisor/reviewer feedback, do not reopen T-716 or manufacture a correction cycle. Record the external-input gate and stop. Likewise do not start T-713/T-720+ until their explicit dependencies and official-input gates are satisfied.
"""


def main() -> None:
    prompt = Path("docs/context/CODEX_EXECUTION_PROMPT.md")
    if prompt.read_text(encoding="utf-8") != PROMPT.rstrip() + "\n":
        prompt.write_text(PROMPT.rstrip() + "\n", encoding="utf-8")

    tasks = Path("docs/context/TASKS.md")
    text = tasks.read_text(encoding="utf-8")
    old = "- **Current academic state:** `T-716` is **COMPLETE**."
    new = "- **Current task:** `T-712` is **DEFERRED** pending actual supervisor/reviewer feedback; `T-716` is **COMPLETE**."
    if new not in text:
        if old not in text:
            raise RuntimeError("TASKS.md current-state prefix is neither expected old nor canonical new form")
        text = text.replace(old, new, 1)
        tasks.write_text(text, encoding="utf-8")

    print("T-716 continuity bootstrap-contract reconciliation complete")


if __name__ == "__main__":
    main()
