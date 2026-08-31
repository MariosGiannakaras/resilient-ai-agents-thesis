#!/usr/bin/env python3
"""Render the T-528 matched FD/AD live layout without scientific execution.

The fixture is presentation-only. It creates one DEVELOPMENT Study plan, writes
static transient FD/AD frames from an already materialized development layout,
and never resets/steps an environment or starts a Study worker.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "0")

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtCore import QSize, Qt  # noqa: E402
from PySide6.QtGui import QPixmap  # noqa: E402

from resilient_agents.desktop.app import create_application  # noqa: E402
from resilient_agents.desktop.exploratory_study import DesktopExploratoryStudyModel  # noqa: E402
from resilient_agents.desktop.live_events import DroppingLiveEventSink  # noqa: E402
from resilient_agents.desktop.main_window import MainWindow  # noqa: E402
from resilient_agents.study import StudyStage, StudyStore  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def capture(window: MainWindow, output: Path, filename: str) -> dict[str, object]:
    app = create_application([])
    app.processEvents()
    image = QPixmap(window.size())
    image.fill(Qt.GlobalColor.white)
    window.render(image)
    target = output / filename
    if not image.save(str(target), "PNG"):
        raise RuntimeError(f"failed to save screenshot: {target}")
    return {
        "file": filename,
        "width": image.width(),
        "height": image.height(),
        "sha256": sha256(target),
    }


def _free_neighbor(start: tuple[int, int], grid: dict) -> tuple[int, int]:
    width = int(grid["width"])
    height = int(grid["height"])
    obstacles = {tuple(item) for item in grid["obstacles"]}
    candidates = (
        (start[0] + 1, start[1]),
        (start[0], start[1] + 1),
        (start[0] - 1, start[1]),
        (start[0], start[1] - 1),
    )
    for x, y in candidates:
        if 0 <= x < width and 0 <= y < height and (x, y) not in obstacles:
            return x, y
    return start


def _event(
    *,
    branch: str,
    layout_id: str,
    grid: dict,
    true_state: tuple[int, int],
) -> dict:
    return {
        "schema_version": 1,
        "event_type": "gridworld-transition",
        "stream_id": f"phase-b:ui_fixture:not-executed:{layout_id}:{branch}",
        "phase": "phase-b",
        "method_id": "ui_fixture",
        "root_id": "not-executed",
        "layout_id": layout_id,
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
        "true_state": list(true_state),
        "delivered_observation": list(true_state),
        "intended_action": "not-executed",
        "executed_action": "not-executed",
        "reward": 0.0,
        "terminated": False,
        "truncated": False,
        "regime_id": "presentation-qa",
        "disturbance_flags": {
            "action_failure": False,
            "observation_corruption": False,
        },
        "change_event_ids": ["presentation-qa-only"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="t528-ui-resilience-pair-") as directory:
        writable_root = Path(directory).resolve()
        fixture_study_id = "t528-dev-ui-review-resilience-pair"
        DesktopExploratoryStudyModel(
            repo_root=REPO_ROOT,
            writable_root=writable_root,
        ).create(
            selected_method_ids=("q_learning",),
            root_count=1,
            layout_count=1,
            study_label="Matched live presentation QA",
            study_id=fixture_study_id,
        )

        store = StudyStore.load(
            repo_root=REPO_ROOT,
            writable_root=writable_root,
            study_id=fixture_study_id,
        )
        phase_a_job = next(job for job in store.plan.jobs if job.stage is StudyStage.PHASE_A)
        layout = dict(phase_a_job.payload["layout"])
        grid = dict(dict(layout["scenario"])["initial_state_spec"])["grid"]
        start = tuple(grid["start"])
        adaptive_state = _free_neighbor(start, grid)

        sink = DroppingLiveEventSink(
            writable_root=writable_root,
            study_id=fixture_study_id,
            flush_interval_seconds=0.01,
        )
        sink.emit(
            _event(
                branch="FD",
                layout_id=str(layout["layout_id"]),
                grid=grid,
                true_state=start,
            )
        )
        sink.emit(
            _event(
                branch="AD",
                layout_id=str(layout["layout_id"]),
                grid=grid,
                true_state=adaptive_state,
            )
        )
        sink.close()

        if (writable_root / "results" / "runs").exists():
            raise RuntimeError("matched live screenshot fixture unexpectedly executed a scientific run")

        app = create_application([])
        window = MainWindow(repo_root=REPO_ROOT, writable_root=writable_root)
        window.show()
        window.set_page(1)
        window.runs_page.refresh()
        window.runs_page.table.selectRow(0)
        window.runs_page.worker_message.setText(
            "UI REVIEW FIXTURE · Matched FD/AD static presentation only · no environment step or scientific job executed."
        )
        window.runs_page.worker_message.show()
        window.runs_page._refresh_live()
        app.processEvents()

        frames = window.runs_page.live_read_model.latest(fixture_study_id)
        if not frames or frames[0].comparison is None:
            raise RuntimeError("matched FD/AD presentation pair was not exposed to the Runs UI")

        records: list[dict[str, object]] = []
        window.resize(QSize(1440, 900))
        app.processEvents()
        records.append(capture(window, output, "16-runs-matched-resilience.png"))

        window.resize(QSize(1366, 768))
        app.processEvents()
        records.append(capture(window, output, "16b-runs-matched-resilience-1366x768.png"))

        manifest = {
            "schema_version": 1,
            "purpose": "T-528 matched FD/AD presentation layout QA; not scientific evidence",
            "development_fixture_created_only": True,
            "environment_steps_executed": 0,
            "scientific_jobs_executed": 0,
            "final_reserve_execution": "not-authorized-and-not-executed",
            "pairing": "exact interaction-index FD/AD transient presentation",
            "screenshots": records,
        }
        (output / "matched-resilience-manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
