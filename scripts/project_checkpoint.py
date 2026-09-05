#!/usr/bin/env python3
"""Update the repository operational resume pointer without creating a second task ledger."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "docs/context/WORK_STATE.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    state["updated_at_utc"] = now_utc()
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_validation(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"validation must be KEY=VALUE, got: {item}")
        key, value = item.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def checkpoint(args: argparse.Namespace) -> None:
    state = load_state()
    if args.phase:
        state["phase"] = args.phase
    if args.status:
        state["task_status"] = args.status
    if args.next_action:
        state["next_action"] = args.next_action
    if args.last_checkpoint:
        state["last_completed_checkpoint"] = args.last_checkpoint
    if args.completed:
        completed = state.setdefault("completed_substeps", [])
        for item in args.completed:
            if item not in completed:
                completed.append(item)
        pending = state.setdefault("pending_substeps", [])
        state["pending_substeps"] = [item for item in pending if item not in args.completed]
    if args.pending:
        pending = state.setdefault("pending_substeps", [])
        for item in args.pending:
            if item not in pending:
                pending.append(item)
    if args.clear_blockers:
        state["blockers"] = []
    if args.blocker:
        blockers = state.setdefault("blockers", [])
        for item in args.blocker:
            if item not in blockers:
                blockers.append(item)
    state.setdefault("validation", {}).update(parse_validation(args.validation))
    save_state(state)


def set_state(args: argparse.Namespace) -> None:
    state = load_state()
    state.update(
        {
            "active_task": args.task,
            "task_status": args.status,
            "work_package": args.work_package,
            "branch": args.branch,
            "base_branch": args.base_branch,
            "pull_request": args.pr,
            "phase": args.phase,
            "last_completed_checkpoint": args.last_checkpoint,
            "next_action": args.next_action,
            "blockers": args.blocker or [],
            "completed_substeps": args.completed or [],
            "pending_substeps": args.pending or [],
            "validation": parse_validation(args.validation),
        }
    )
    save_state(state)


def show(_: argparse.Namespace) -> None:
    print(STATE_PATH.read_text(encoding="utf-8"), end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_show = sub.add_parser("show")
    p_show.set_defaults(func=show)

    p_checkpoint = sub.add_parser("checkpoint")
    p_checkpoint.add_argument("--phase")
    p_checkpoint.add_argument("--status")
    p_checkpoint.add_argument("--last-checkpoint")
    p_checkpoint.add_argument("--next-action")
    p_checkpoint.add_argument("--completed", action="append", default=[])
    p_checkpoint.add_argument("--pending", action="append", default=[])
    p_checkpoint.add_argument("--blocker", action="append", default=[])
    p_checkpoint.add_argument("--clear-blockers", action="store_true")
    p_checkpoint.add_argument("--validation", action="append", default=[])
    p_checkpoint.set_defaults(func=checkpoint)

    p_set = sub.add_parser("set")
    p_set.add_argument("--task", required=True)
    p_set.add_argument("--status", required=True)
    p_set.add_argument("--work-package", required=True)
    p_set.add_argument("--branch", required=True)
    p_set.add_argument("--base-branch", default="main")
    p_set.add_argument("--pr", type=int)
    p_set.add_argument("--phase", required=True)
    p_set.add_argument("--last-checkpoint", required=True)
    p_set.add_argument("--next-action", required=True)
    p_set.add_argument("--blocker", action="append", default=[])
    p_set.add_argument("--completed", action="append", default=[])
    p_set.add_argument("--pending", action="append", default=[])
    p_set.add_argument("--validation", action="append", default=[])
    p_set.set_defaults(func=set_state)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
