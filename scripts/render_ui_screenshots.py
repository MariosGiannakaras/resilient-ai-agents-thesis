#!/usr/bin/env python3
"""Render deterministic PySide6 T-528 review screenshots in offscreen mode.

These screenshots are presentation QA artifacts, never scientific evidence. The
script may create one deterministic DEVELOPMENT Study fixture in a temporary
writable workspace so Runs controls, live-presentation layout and provenance can
be reviewed, but it never executes, resumes or finalizes a Study.
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

from PySide6.QtCore import QSize  # noqa: E402

from resilient_agents.desktop.app import create_application  # noqa: E402
from resilient_agents.desktop.exploratory_study import (  # noqa: E402
    DesktopExploratoryStudyModel,
)
from resilient_agents.desktop.live_events import DroppingLiveEventSink  # noqa: E402
from resilient_agents.desktop.main_window import MainWindow  # noqa: E402
from resilient_agents.study import (  # noqa: E402
    ArtifactRole,
    EvidenceClass,
    StudyArtifact,
    StudyStage,
    StudyStore,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def capture(window: MainWindow, output: Path, filename: str) -> dict[str, object]:
    app = create_application([])
    app.processEvents()
    image = window.grab()
    target = output / filename
    if not image.save(str(target), "PNG"):
        raise RuntimeError(f"failed to save screenshot: {target}")
    return {
        "file": filename,
        "width": image.width(),
        "height": image.height(),
        "sha256": sha256(target),
    }


def prepare_review(study) -> None:
    study.show_customize()
    study.customize.study_label.setText("GridWorld adaptation check")
    study.customize.root_count.setCurrentIndex(1)
    study.customize.layout_count.setCurrentIndex(1)
    study._show_review()


def add_presentation_provenance_fixture(
    *, writable_root: Path, study_id: str
) -> None:
    """Record non-scientific QA lineage without executing any Study job."""

    store = StudyStore.load(
        repo_root=REPO_ROOT,
        writable_root=writable_root,
        study_id=study_id,
    )
    fixture_dir = store.study_dir / "presentation-qa"
    fixture_dir.mkdir(parents=True, exist_ok=True)

    provenance_path = fixture_dir / "ui-review-provenance.txt"
    provenance_path.write_text(
        "Presentation-only provenance fixture for T-528 UI review.\n"
        "No scientific job produced this file and no scientific metric is represented.\n",
        encoding="utf-8",
    )
    provenance = StudyArtifact(
        artifact_id="ui-review-provenance",
        role=ArtifactRole.PROVENANCE,
        evidence_class=EvidenceClass.DEVELOPMENT,
        relative_path=provenance_path.resolve().relative_to(writable_root).as_posix(),
        sha256=sha256(provenance_path),
        metadata={"purpose": "presentation-qa-only", "scientific_evidence": False},
    )
    store.record_artifact(provenance)

    asset_path = fixture_dir / "ui-review-asset.txt"
    asset_path.write_text(
        "Presentation-only derived asset used to exercise artifact lineage UI.\n",
        encoding="utf-8",
    )
    store.record_artifact(
        StudyArtifact(
            artifact_id="ui-review-presentation-asset",
            role=ArtifactRole.PRESENTATION_ASSET,
            evidence_class=EvidenceClass.DEVELOPMENT,
            relative_path=asset_path.resolve().relative_to(writable_root).as_posix(),
            sha256=sha256(asset_path),
            source_artifact_ids=(provenance.artifact_id,),
            metadata={"purpose": "presentation-qa-only", "scientific_evidence": False},
        )
    )


def add_live_layout_fixture(*, writable_root: Path, study_id: str) -> None:
    """Write one static presentation frame from the real DEVELOPMENT layout only.

    No environment is reset or stepped. The frame is intentionally labelled
    ``presentation-qa`` / ``not-executed`` so the screenshot cannot be mistaken
    for an experimental outcome.
    """

    store = StudyStore.load(
        repo_root=REPO_ROOT,
        writable_root=writable_root,
        study_id=study_id,
    )
    phase_a_job = next(job for job in store.plan.jobs if job.stage is StudyStage.PHASE_A)
    layout = dict(phase_a_job.payload["layout"])
    scenario = dict(layout["scenario"])
    grid = dict(scenario["initial_state_spec"])["grid"]
    start = list(grid["start"])
    sink = DroppingLiveEventSink(
        writable_root=writable_root,
        study_id=study_id,
        flush_interval_seconds=0.01,
    )
    sink.emit(
        {
            "schema_version": 1,
            "event_type": "gridworld-transition",
            "stream_id": f"presentation-qa:ui_fixture:not-executed:{layout['layout_id']}:nominal",
            "phase": "presentation-qa",
            "method_id": "ui_fixture",
            "root_id": "not-executed",
            "layout_id": str(layout["layout_id"]),
            "branch": None,
            "episode_index": 0,
            "interaction_index": 0,
            "environment_step": 0,
            "grid": {
                "width": int(grid["width"]),
                "height": int(grid["height"]),
                "start": start,
                "goal": list(grid["goal"]),
                "obstacles": [list(item) for item in grid["obstacles"]],
            },
            "true_state": start,
            "delivered_observation": start,
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
            "change_event_ids": [],
        }
    )
    sink.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="t528-ui-review-") as directory:
        writable_root = Path(directory).resolve()
        app = create_application([])
        window = MainWindow(repo_root=REPO_ROOT, writable_root=writable_root)
        window.show()
        app.processEvents()

        records: list[dict[str, object]] = []
        study = window.study_page

        # Historical accepted references are 1480x920. Capture the key Study journey
        # states at this exact viewport so visual review is not confounded by size.
        window.resize(QSize(1480, 920))
        window.set_page(0)

        study.show_home()
        app.processEvents()
        records.append(capture(window, output, "reference-size-choose-study.png"))

        study.show_thesis()
        app.processEvents()
        records.append(capture(window, output, "reference-size-thesis-study.png"))

        study.show_exploratory()
        app.processEvents()
        records.append(capture(window, output, "reference-size-exploratory-models.png"))

        study.show_customize()
        app.processEvents()
        records.append(capture(window, output, "reference-size-exploratory-customize.png"))

        prepare_review(study)
        app.processEvents()
        records.append(capture(window, output, "reference-size-exploratory-review.png"))

        window.set_page(2)
        app.processEvents()
        records.append(capture(window, output, "reference-size-results-empty.png"))

        window.resize(QSize(1440, 900))
        window.set_page(0)
        study.show_home()
        app.processEvents()
        records.append(capture(window, output, "01-choose-study.png"))

        study.show_thesis()
        app.processEvents()
        records.append(capture(window, output, "02-thesis-study.png"))

        study.show_exploratory()
        app.processEvents()
        records.append(capture(window, output, "03-exploratory-models.png"))

        study.show_customize()
        app.processEvents()
        records.append(capture(window, output, "04-exploratory-customize.png"))

        prepare_review(study)
        app.processEvents()
        records.append(capture(window, output, "05-exploratory-review.png"))

        window.set_page(1)
        app.processEvents()
        records.append(capture(window, output, "06-runs-empty.png"))

        window.set_page(2)
        app.processEvents()
        records.append(capture(window, output, "07-results-empty.png"))

        window.set_page(3)
        app.processEvents()
        records.append(capture(window, output, "08-artifacts-empty.png"))

        # Create exactly one deterministic DEVELOPMENT Study fixture. Creation only
        # materializes durable recipe/plan state; no worker or scientific job runs.
        fixture = DesktopExploratoryStudyModel(
            repo_root=REPO_ROOT,
            writable_root=writable_root,
        )
        fixture_study_id = "t528-dev-ui-review-gridworld"
        fixture.create(
            selected_method_ids=("q_learning",),
            root_count=1,
            layout_count=1,
            study_label="UI review",
            study_id=fixture_study_id,
        )
        if (writable_root / "results" / "runs").exists():
            raise RuntimeError("UI screenshot fixture unexpectedly executed a scientific run")

        add_presentation_provenance_fixture(
            writable_root=writable_root,
            study_id=fixture_study_id,
        )
        add_live_layout_fixture(
            writable_root=writable_root,
            study_id=fixture_study_id,
        )
        if (writable_root / "results" / "runs").exists():
            raise RuntimeError("presentation fixtures unexpectedly executed a scientific run")

        window.set_page(1)
        window.runs_page.refresh()
        window.runs_page.table.selectRow(0)
        window.runs_page.worker_message.setText(
            "UI REVIEW FIXTURE · Static DEVELOPMENT layout only · no environment step or scientific job executed."
        )
        window.runs_page.worker_message.show()
        window.runs_page._refresh_live()
        app.processEvents()
        records.append(capture(window, output, "06b-runs-development-ready.png"))
        records.append(capture(window, output, "06c-runs-live-presentation.png"))

        window.set_page(3)
        window.artifacts_page.refresh()
        window.artifacts_page.set_study(fixture_study_id)
        if window.artifacts_page.table.rowCount() > 1:
            window.artifacts_page.table.selectRow(1)
        app.processEvents()
        records.append(capture(window, output, "08b-artifacts-provenance.png"))

        window.resize(QSize(1366, 768))
        window.set_page(0)
        study.show_home()
        app.processEvents()
        records.append(capture(window, output, "09-choose-study-1366x768.png"))

        study.show_exploratory()
        app.processEvents()
        records.append(capture(window, output, "10-exploratory-models-1366x768.png"))

        study.show_customize()
        app.processEvents()
        records.append(capture(window, output, "11-exploratory-customize-1366x768.png"))

        prepare_review(study)
        app.processEvents()
        records.append(capture(window, output, "12-exploratory-review-1366x768.png"))

        window.set_page(1)
        window.runs_page.table.selectRow(0)
        window.runs_page.worker_message.setText(
            "UI REVIEW FIXTURE · Static DEVELOPMENT layout only · no environment step or scientific job executed."
        )
        window.runs_page.worker_message.show()
        window.runs_page._refresh_live()
        app.processEvents()
        records.append(capture(window, output, "13-runs-development-ready-1366x768.png"))
        records.append(capture(window, output, "13b-runs-live-presentation-1366x768.png"))

        window.set_page(2)
        app.processEvents()
        records.append(capture(window, output, "14-results-empty-1366x768.png"))

        window.set_page(3)
        window.artifacts_page.set_study(fixture_study_id)
        if window.artifacts_page.table.rowCount() > 1:
            window.artifacts_page.table.selectRow(1)
        app.processEvents()
        records.append(capture(window, output, "15-artifacts-provenance-1366x768.png"))

        protocol_path = REPO_ROOT / "configs" / "protocols" / "protocol-v2.0-final.json"
        manifest = {
            "schema_version": 8,
            "purpose": "T-528 deterministic presentation review; not scientific evidence",
            "visual_reference_viewport": [1480, 920],
            "final_reserve_execution": "not-authorized-and-not-executed",
            "development_fixture_created_only": True,
            "development_fixture_scientific_runs": 0,
            "presentation_provenance_fixture": "development-only-no-scientific-metrics",
            "presentation_live_fixture": "static-development-layout-no-environment-step",
            "stored_results_fixture": "none-no-scientific-metrics-fabricated",
            "protocol_file_sha256": sha256(protocol_path),
            "screenshots": records,
        }
        (output / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
