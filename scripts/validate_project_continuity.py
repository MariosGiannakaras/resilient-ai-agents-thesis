#!/usr/bin/env python3
"""Fail closed when the repository cannot be resumed safely without conversation memory."""
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "docs/context/WORK_STATE.json"
TASKS_PATH = ROOT / "docs/context/TASKS.md"
AGENTS_PATH = ROOT / "AGENTS.md"
CURRENT_STATUS_PATH = ROOT / "docs/context/CURRENT_STATUS.md"
LEGACY_PROMPT = ROOT / "docs/context/CODEX_EXECUTION_PROMPT.md"

REQUIRED_STATE_KEYS = {
    "schema_version",
    "updated_at_utc",
    "authority",
    "active_task",
    "task_status",
    "work_package",
    "branch",
    "base_branch",
    "pull_request",
    "phase",
    "last_completed_checkpoint",
    "next_action",
    "blockers",
    "completed_substeps",
    "pending_substeps",
    "validation",
    "resume_rule",
    "notes",
}

ALLOWED_STATUS = {"IN_PROGRESS", "READY_TO_MERGE", "BLOCKED", "DEFERRED", "READY", "COMPLETE"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def changed_files(base: str) -> list[str]:
    subprocess.run(
        ["git", "fetch", "origin", base, "--depth=1"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    result = subprocess.run(
        ["git", "diff", "--name-only", f"origin/{base}...HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def task_id_pattern(task: str) -> str:
    """Match a backticked task ID followed by whitespace or end-of-line."""
    return rf"`{re.escape(task)}`(?=\s|$)"


def main() -> int:
    errors: list[str] = []

    for required_path in (STATE_PATH, TASKS_PATH, AGENTS_PATH, CURRENT_STATUS_PATH):
        if not required_path.is_file():
            fail(errors, f"missing required continuity authority: {required_path.relative_to(ROOT)}")
    if LEGACY_PROMPT.exists():
        fail(errors, "legacy CODEX_EXECUTION_PROMPT.md must not be an active repository dependency")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: WORK_STATE.json invalid JSON: {exc}")
        return 1

    missing = sorted(REQUIRED_STATE_KEYS - set(state))
    if missing:
        fail(errors, "WORK_STATE.json missing keys: " + ", ".join(missing))
    if state.get("schema_version") != 1:
        fail(errors, "WORK_STATE.json schema_version must be 1")
    try:
        datetime.fromisoformat(str(state.get("updated_at_utc", "")).replace("Z", "+00:00"))
    except ValueError:
        fail(errors, "WORK_STATE.json updated_at_utc must be ISO-8601")

    task = str(state.get("active_task", ""))
    status = str(state.get("task_status", ""))
    if not re.fullmatch(r"T-\d+", task):
        fail(errors, f"WORK_STATE active_task is invalid: {task!r}")
    if status not in ALLOWED_STATUS:
        fail(errors, f"WORK_STATE task_status is invalid: {status!r}")
    if not str(state.get("next_action", "")).strip():
        fail(errors, "WORK_STATE next_action must be explicit")
    if not str(state.get("last_completed_checkpoint", "")).strip():
        fail(errors, "WORK_STATE last_completed_checkpoint must be explicit")
    if not isinstance(state.get("blockers"), list) or not isinstance(state.get("pending_substeps"), list):
        fail(errors, "WORK_STATE blockers and pending_substeps must be arrays")
    if status == "BLOCKED" and not state.get("blockers"):
        fail(errors, "BLOCKED WORK_STATE requires at least one blocker")
    if status in {"IN_PROGRESS", "READY_TO_MERGE"} and not state.get("pending_substeps"):
        fail(errors, f"{status} WORK_STATE requires pending_substeps")

    tasks = TASKS_PATH.read_text(encoding="utf-8")
    task_pattern = task_id_pattern(task)
    if task and not re.search(task_pattern, tasks):
        fail(errors, f"WORK_STATE active_task {task} is absent from TASKS.md")

    if status in {"IN_PROGRESS", "READY_TO_MERGE"}:
        if not re.search(rf"^- \[ \] IN_PROGRESS {task_pattern}", tasks, re.MULTILINE):
            fail(errors, f"WORK_STATE {status} requires TASKS.md to mark {task} IN_PROGRESS")
    elif status == "COMPLETE":
        if not re.search(rf"^- \[x\].*{task_pattern}", tasks, re.MULTILINE):
            fail(errors, f"WORK_STATE COMPLETE requires {task} completed in TASKS.md")
    elif status in {"DEFERRED", "BLOCKED", "READY"}:
        if not re.search(rf"^- \[ \] {status} {task_pattern}", tasks, re.MULTILINE):
            fail(errors, f"WORK_STATE {status} requires matching {status} task line for {task}")

    agents = AGENTS_PATH.read_text(encoding="utf-8")
    for required in (
        "docs/context/WORK_STATE.json",
        "continue implementation",
        "Repository/Git/GitHub evidence overrides",
        "before every material change",
        "after every material validated checkpoint",
        "resume unfinished work",
        "open a draft PR",
    ):
        if required.casefold() not in agents.casefold():
            fail(errors, f"AGENTS.md missing continuity invariant: {required}")

    event = os.environ.get("GITHUB_EVENT_NAME", "")
    if event == "pull_request":
        base = os.environ.get("GITHUB_BASE_REF", "main")
        head = os.environ.get("GITHUB_HEAD_REF", "")
        pr_number = os.environ.get("PR_NUMBER") or os.environ.get("GITHUB_PR_NUMBER")
        files = changed_files(base)
        automated_generated_only = bool(files) and all(
            changed.startswith("research/bibliography/") or changed == ".bibliography-sync-trigger"
            for changed in files
        )
        if not automated_generated_only and "docs/context/WORK_STATE.json" not in files:
            fail(errors, "every material PR must update docs/context/WORK_STATE.json")
        if head and state.get("branch") not in {head, "main-after-merge"}:
            fail(errors, f"WORK_STATE branch {state.get('branch')!r} does not match PR head {head!r}")
        if pr_number and state.get("pull_request") not in {None, int(pr_number)}:
            fail(errors, "WORK_STATE pull_request does not match the active PR")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Project continuity validation passed: "
        f"task={task} status={status} phase={state.get('phase')} next={state.get('next_action')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
