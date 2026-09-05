#!/usr/bin/env python3
"""Temporary branch-only T-010 post-merge state normalizer; delete before merge."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "docs/context/TASKS.md"
STATUS = ROOT / "docs/context/CURRENT_STATUS.md"
WORK = ROOT / "docs/context/WORK_STATE.json"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}")
    return text.replace(old, new, 1)


def normalize_tasks() -> None:
    text = TASKS.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "- **Current task:** `T-010` is **IN_PROGRESS** on PR #146: install the prompt-free self-resuming repository workflow and durable operational checkpoint contract. T-716 remains COMPLETE. T-712 remains DEFERRED until actual supervisor/reviewer feedback; T-713 remains downstream of T-712 plus authoritative official metadata/declaration and final Word/submission gates.",
        "- **Current task:** `T-712` is **DEFERRED** pending actual supervisor/reviewer feedback. T-010 and T-716 are COMPLETE. T-713 remains downstream of resolved real feedback plus authoritative official metadata/declaration and final Word/submission gates.",
        "TASKS current task",
    )
    text = replace_once(
        text,
        "- **Exact next action:** finish `T-010`: make `AGENTS.md` the no-prompt entrypoint, require `WORK_STATE.json` checkpoints, add continuity validation/CI, retire `CODEX_EXECUTION_PROMPT.md`, reconcile active workflow/governance docs, then merge PR #146 only after required checks pass.",
        "- **Exact next action:** wait for actual supervisor/reviewer feedback for `T-712`; do not fabricate or substitute internal review for external feedback. When real feedback arrives, record it durably, move T-712 to IN_PROGRESS, incorporate the corrections and revalidate before T-713.",
        "TASKS exact next action",
    )
    text = replace_once(
        text,
        "- [ ] IN_PROGRESS `T-010` — **Prompt-free self-resuming repository workflow and durable work-state checkpoints.**",
        "- [x] `T-010` — **Prompt-free self-resuming repository workflow and durable work-state checkpoints.** COMPLETE.",
        "TASKS T-010 line",
    )
    TASKS.write_text(text, encoding="utf-8")


def normalize_status() -> None:
    text = STATUS.read_text(encoding="utf-8")
    old = """## Active repository continuity work\n\n- `T-010` is **IN_PROGRESS** on PR #146. Its purpose is to make repository continuation independent of chat/model memory: `AGENTS.md` is the no-prompt entrypoint, `docs/context/WORK_STATE.json` is the operational resume pointer, and every material change/checkpoint must update that pointer before work proceeds.\n- Recovery order is: working-tree work -> open PR -> unmerged pushed branch -> `WORK_STATE` -> `TASKS` `IN_PROGRESS` -> first dependency-valid `READY` task -> exact external gate.\n- T-716 remains COMPLETE and immutable as the accepted review-ready thesis milestone. T-010 changes workflow/governance only; it does not change the thesis DOCX, protocol, frozen evidence, analysis or scientific assets.\n"""
    new = """## Repository continuity state\n\n- `T-010` is **COMPLETE** and was squash-merged through PR #146 as `bac999ce0bd32220ddf7e5112978a2035759970b`. `AGENTS.md` is the prompt-free entrypoint and `docs/context/WORK_STATE.json` is the operational resume pointer.\n- Recovery order remains: working-tree work -> open PR -> unmerged pushed branch -> `WORK_STATE` -> `TASKS` `IN_PROGRESS` -> first dependency-valid `READY` task -> exact external gate.\n- `T-716` remains COMPLETE and immutable as the accepted review-ready thesis milestone. The current academic gate is `T-712`, intentionally DEFERRED until actual supervisor/reviewer feedback exists.\n"""
    text = replace_once(text, old, new, "CURRENT_STATUS continuity section")
    text = replace_once(
        text,
        "Finish T-010 on PR #146, validate the prompt-free recovery/checkpoint workflow, and merge only when continuity/documentation/required PR CI is green. After merge, normalize `WORK_STATE.json` on `main` to T-712 DEFERRED unless real supervisor/reviewer feedback has arrived.",
        "Wait for actual supervisor/reviewer feedback for `T-712`. Do not relabel internal audits as external feedback. When real feedback arrives, record it in the repository, move T-712 to IN_PROGRESS, incorporate the corrections and revalidate before T-713 finalization.",
        "CURRENT_STATUS exact next action",
    )
    STATUS.write_text(text, encoding="utf-8")


def normalize_work_state() -> None:
    state = json.loads(WORK.read_text(encoding="utf-8"))
    if state.get("active_task") == "T-712" and state.get("task_status") == "DEFERRED":
        return
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    final = {
        "schema_version": 1,
        "updated_at_utc": now,
        "authority": "repository-operational-resume-state",
        "active_task": "T-712",
        "task_status": "DEFERRED",
        "work_package": "Supervisor/reviewer feedback incorporation gate",
        "branch": "main-after-merge",
        "base_branch": "main",
        "pull_request": None,
        "phase": "EXTERNAL_GATE",
        "last_completed_checkpoint": "T-010 prompt-free self-resuming repository workflow completed and squash-merged through PR #146 as bac999ce0bd32220ddf7e5112978a2035759970b. Post-merge normalization sets the repository to the next real academic gate without inventing external feedback.",
        "next_action": "Wait for actual supervisor/reviewer feedback. When it arrives, record the feedback durably, move T-712 to IN_PROGRESS, incorporate the corrections and revalidate. Do not start T-713 finalization before T-712 and its remaining official-input gates are satisfied.",
        "blockers": ["Actual supervisor/reviewer feedback has not yet been received."],
        "completed_substeps": [
            "T-716 final thesis acceptance completed with 11/11 gates PASS",
            "T-010 prompt-free self-resuming workflow merged through PR #146",
            "Generic Project continuity CI installed",
            "Legacy tracked execution prompt and dangerous one-shot migration paths retired",
            "Repository state normalized to the real post-T-010 external gate",
        ],
        "pending_substeps": [
            "Receive actual supervisor/reviewer feedback",
            "Record feedback durably and move T-712 to IN_PROGRESS",
            "Incorporate corrections and revalidate",
            "Proceed to T-713 only after T-712 and official finalization inputs are satisfied",
        ],
        "validation": {
            "t010": "COMPLETE_MERGED_bac999ce0bd32220ddf7e5112978a2035759970b",
            "t716_final_acceptance": "PASS_11_OF_11",
            "project_continuity": "REQUIRED_ON_NORMALIZATION_PR",
            "documentation_consistency": "REQUIRED_ON_NORMALIZATION_PR",
        },
        "resume_rule": "Repository/Git/GitHub evidence overrides chat or model memory. T-712 is intentionally deferred; do not create substitute work for the missing external feedback.",
        "notes": [
            "TASKS.md remains the canonical task/dependency ledger; this file is only the operational resume pointer.",
            "If real supervisor/reviewer feedback is later available in connected evidence, recover it before asking the user to restate it.",
        ],
    }
    WORK.write_text(json.dumps(final, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    normalize_tasks()
    normalize_status()
    normalize_work_state()
    print("T-010 post-merge normalization complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
