#!/usr/bin/env python3
"""Focused T-534 exact-matched Phase-B render validation without execution."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "0")

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtCore import QSize  # noqa: E402

from resilient_agents.desktop.app import create_application  # noqa: E402
from resilient_agents.desktop.exploratory_study import DesktopExploratoryStudyModel  # noqa: E402
from resilient_agents.desktop.live_events import DroppingLiveEventSink  # noqa: E402
from resilient_agents.desktop.main_window import MainWindow  # noqa: E402
from resilient_agents.study import StudyStage, StudyStore  # noqa: E402
from render_ui_screenshots import capture  # noqa: E402


def _grid_context(writable_root: Path, study_id: str) -> tuple[dict, str, str, str]:
    store = StudyStore.load(
        repo_root=REPO_ROOT,
        writable_root=writable_root,
        study_id=study_id,
    )
    phase_b = next(job for job in store.plan.jobs if job.stage is StudyStage.PHASE_B)
    layout = dict(phase_b.payload["layout"])
    root = dict(phase_b.payload["root"])
    condition = dict(phase_b.payload["condition"])
    grid = dict(dict(layout["scenario"])["initial_state_spec"])["grid"]
    return (
        grid,
        str(layout["layout_id"]),
        str(root["root_id"]),
        str(condition["condition_id"]),
    )


def _free_neighbor(start: tuple[int, int], grid: dict) -> tuple[int, int]:
    obstacles = {tuple(item) for item in grid["obstacles"]}
    for candidate in (
        (start[0] + 1, start[1]),
        (start[0], start[1] + 1),
        (start[0] - 1, start[1]),
        (start[0], start[1] - 1),
    ):
        x, y = candidate
        if (
            0 <= x < int(grid["width"])
            and 0 <= y < int(grid["height"])
            and candidate not in obstacles
        ):
            return candidate
    return start


def _event(
    *,
    branch: str,
    state: tuple[int, int],
    grid: dict,
    root_id: str,
    layout_id: str,
    condition_id: str,
) -> dict:
    return {
        "schema_version": 1,
        "event_type": "gridworld-transition",
        "stream_id": (
            f"phase-b:q_learning:{root_id}:{layout_id}:{condition_id}:{branch}"
        ),
        "phase": "phase-b",
        "method_id": "q_learning",
        "root_id": root_id,
        "layout_id": layout_id,
        "condition_id": condition_id,
        "branch": branch,
        "episode_index": 0,
        "interaction_index": 1,
        "environment_step": 1,
        "grid": {
            "width": int(grid["width"]),
            "height": int(grid["height"]),
            "start": list(grid["start"]),
            "goal": list(grid["goal"]),
            "obstacles": [list(item) for item in grid["obstacles"]],
        },
        "true_state": list(state),
        "delivered_observation": list(state),
        "intended_action": "right",
        "executed_action": "down" if branch == "FD" else "right",
        "reward": -1.0 if branch == "FD" else -0.5,
        "terminated": False,
        "truncated": False,
        "regime_id": "presentation-qa-only",
        "disturbance_flags": {
            "action_failure": branch == "FD",
            "observation_corruption": False,
        },
        "change_event_ids": ["presentation-qa-action-remap"],
    }


def write_condition_aware_pair(*, writable_root: Path, study_id: str) -> str:
    grid, layout_id, root_id, condition_id = _grid_context(writable_root, study_id)
    start = tuple(grid["start"])
    adaptive = _free_neighbor(start, grid)
    sink = DroppingLiveEventSink(
        writable_root=writable_root,
        study_id=study_id,
        flush_interval_seconds=0.01,
    )
    sink.emit(
        _event(
            branch="FD",
            state=start,
            grid=grid,
            root_id=root_id,
            layout_id=layout_id,
            condition_id=condition_id,
        )
    )
    sink.emit(
        _event(
            branch="AD",
            state=adaptive,
            grid=grid,
            root_id=root_id,
            layout_id=layout_id,
            condition_id=condition_id,
        )
    )
    sink.close()
    return condition_id


def _project_phase_b_render_state(window: MainWindow, study_id: str) -> None:
    """Adjust only the in-memory QA read projection; never mutate Study lifecycle."""

    item = next(entry for entry in window.runs_page._items if entry.study_id == study_id)
    projected = replace(
        item,
        current_stage="phase-b",
        resolved_jobs=1,
        completed_jobs=1,
        running_jobs=1,
        method_statuses=(("q_learning", "Running"),),
    )
    window.runs_page._items = tuple(
        projected if entry.study_id == study_id else entry
        for entry in window.runs_page._items
    )
    window.runs_page._render_status(projected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="t534-ui-pair-") as directory:
        writable_root = Path(directory).resolve()
        study_id = "t534-dev-ui-review-pair"
        DesktopExploratoryStudyModel(
            repo_root=REPO_ROOT,
            writable_root=writable_root,
        ).create(
            selected_method_ids=("q_learning",),
            root_count=1,
            layout_count=1,
            study_label="Matched presentation QA",
            study_id=study_id,
        )
        condition_id = write_condition_aware_pair(
            writable_root=writable_root,
            study_id=study_id,
        )
        if (writable_root / "results" / "runs").exists():
            raise RuntimeError("pair fixture unexpectedly executed a scientific run")

        app = create_application([])
        window = MainWindow(repo_root=REPO_ROOT, writable_root=writable_root)
        window.show()
        window.set_page(1)
        window.runs_page.refresh()
        window.runs_page.study_combo.setCurrentIndex(
            window.runs_page.study_combo.findData(study_id)
        )
        _project_phase_b_render_state(window, study_id)
        window.runs_page.refresh_live()
        frame = window.runs_page._latest_frame
        if frame is None or frame.comparison is None:
            raise RuntimeError("exact FD/AD comparison was not exposed")
        pair = frame.comparison
        if (
            pair.frozen.method_id != pair.adaptive.method_id
            or pair.frozen.root_id != pair.adaptive.root_id
            or pair.frozen.layout_id != pair.adaptive.layout_id
            or pair.frozen.condition_id != pair.adaptive.condition_id
            or pair.frozen.interaction_index != pair.adaptive.interaction_index
            or pair.adaptive.condition_id != condition_id
        ):
            raise RuntimeError(
                "render attempted with a mismatched Phase-B method/root/layout/"
                "condition/interaction pair"
            )
        if condition_id not in window.runs_page.frame_summary.text():
            raise RuntimeError("Phase-B condition is not prominent in the Run summary")
        if "Frozen — learning off" not in window.runs_page.frame_summary.text():
            raise RuntimeError("Frozen learning-off meaning is missing from Run summary")
        if "Adaptive — learning continues" not in window.runs_page.frame_summary.text():
            raise RuntimeError("Adaptive learning-continuation meaning is missing")
        if window.runs_page.stage_label.text() != "Phase B — Frozen vs Adaptive":
            raise RuntimeError("focused Phase-B QA render has contradictory stage text")

        records = []
        for size, suffix in (
            (QSize(1440, 900), "1440x900"),
            (QSize(1366, 768), "1366x768"),
        ):
            window.resize(size)
            app.processEvents()
            records.append(
                capture(window, output, f"phase-b-exact-pair-{suffix}.png")
            )
        (output / "matched-resilience-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 4,
                    "purpose": (
                        "T-534 exact matched Phase-B presentation QA; not scientific evidence"
                    ),
                    "scientific_jobs_executed": 0,
                    "environment_steps_executed": 0,
                    "durable_job_state_mutated": False,
                    "final_reserve_accessed": False,
                    "condition_id": condition_id,
                    "pairing": (
                        "exact method/root/layout/condition/interaction FD/AD "
                        "transient presentation"
                    ),
                    "screenshots": records,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
