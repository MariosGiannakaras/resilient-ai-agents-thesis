"""Subprocess entrypoint for non-final desktop Study execution."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from ..presentation_observer import bound_presentation_sink
from ..study.service import StudyService
from ..study.store import StudyStore
from .execution_policy import (
    assert_development_store_execution_allowed,
    infrastructure_failure_job_ids,
    running_job_ids,
)
from .live_events import DroppingLiveEventSink


def _load_store(*, repo_root: Path, writable_root: Path, study_id: str) -> StudyStore:
    return StudyStore.load(
        repo_root=repo_root,
        writable_root=writable_root,
        study_id=study_id,
    )


def run_development_study(
    *,
    repo_root: Path,
    writable_root: Path,
    study_id: str,
    retry_infrastructure: bool = False,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    writable_root = Path(writable_root).resolve()
    store = _load_store(
        repo_root=repo_root,
        writable_root=writable_root,
        study_id=study_id,
    )
    assert_development_store_execution_allowed(store, repo_root=repo_root)

    if (store.study_dir / "FINALIZED").is_file():
        return {
            "status": "already-finalized",
            "study_id": study_id,
            "executed_jobs": 0,
            "finalized": True,
        }

    running = running_job_ids(store)
    if running:
        raise RuntimeError(
            "study already contains RUNNING job state; worker will not assume "
            f"ownership: {running}"
        )

    failures = infrastructure_failure_job_ids(store)
    service = StudyService(repo_root=repo_root, writable_root=writable_root)
    if retry_infrastructure:
        if len(failures) != 1:
            raise RuntimeError(
                "retry requires exactly one infrastructure-failed job; "
                f"found {len(failures)}"
            )
        service.retry_infrastructure_failure(study_id, failures[0])
    elif failures:
        raise RuntimeError(
            "study has an infrastructure failure; use the explicit retry action"
        )

    # T-528 presentation is a best-effort side channel outside Study evidence.
    # The execution policy above proves this is a DEVELOPMENT Study before a
    # live sink can be bound. The sink itself is lossy and non-blocking.
    live_sink = DroppingLiveEventSink(
        writable_root=writable_root,
        study_id=study_id,
    )
    try:
        with bound_presentation_sink(live_sink):
            executed = service.run_ready(
                study_id,
                stop_on_infrastructure_failure=True,
            )
    finally:
        live_sink.close()

    status = service.status(study_id)
    progress = status.progress
    if int(progress.get("running", 0)):
        raise RuntimeError("worker returned while a Study job is still RUNNING")

    total = int(progress.get("total", 0))
    resolved = int(progress.get("resolved", 0))
    if total == resolved and not status.finalized:
        status = service.finalize(study_id)

    return {
        "status": status.status,
        "study_id": status.study_id,
        "executed_jobs": len(executed),
        "finalized": status.finalized,
        "current_stage": status.current_stage,
        "progress": dict(status.progress),
        "ready_job_ids": list(status.ready_job_ids),
        "presentation_events_dropped": live_sink.dropped_events,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run/resume a T-528 DEVELOPMENT Study outside the Qt GUI thread."
    )
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--writable-root", type=Path, required=True)
    parser.add_argument("--study-id", required=True)
    parser.add_argument(
        "--retry-infrastructure",
        action="store_true",
        help=(
            "Authorize retry of the single currently infrastructure-failed job "
            "before resuming."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        summary = run_development_study(
            repo_root=args.repo_root,
            writable_root=args.writable_root,
            study_id=args.study_id,
            retry_infrastructure=args.retry_infrastructure,
        )
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                    "study_id": args.study_id,
                },
                sort_keys=True,
            ),
            file=sys.stderr,
            flush=True,
        )
        return 1

    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
