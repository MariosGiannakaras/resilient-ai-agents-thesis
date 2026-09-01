#!/usr/bin/env python3
"""Render deterministic T-534 experiment-first UI review screenshots.

All populated states are DEVELOPMENT or in-memory presentation fixtures. The
script never starts a Study worker, steps an environment, accesses final-reserve
identities/outcomes, or writes scientific run evidence.
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
from resilient_agents.desktop.onboarding import OnboardingDialog  # noqa: E402
from resilient_agents.desktop.results_read_model import (  # noqa: E402
    LearningSummary,
    RecoveryEvidence,
    RecoverySummary,
    RecoveryTrajectoryPoint,
    ResilienceSummary,
    StoredAnalysisPackage,
    StoredSummary,
)
from resilient_agents.study import ArtifactRole, EvidenceClass, StudyArtifact, StudyStage, StudyStore  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def capture(widget, output: Path, filename: str) -> dict[str, object]:
    app = create_application([])
    app.processEvents()
    image = QPixmap(widget.size())
    image.fill(Qt.GlobalColor.white)
    widget.render(image)
    target = output / filename
    if not image.save(str(target), "PNG"):
        raise RuntimeError(f"failed to save screenshot: {target}")
    return {"file": filename, "width": image.width(), "height": image.height(), "sha256": sha256(target)}


def _grid_from_study(writable_root: Path, study_id: str) -> tuple[dict, str, str]:
    store = StudyStore.load(repo_root=REPO_ROOT, writable_root=writable_root, study_id=study_id)
    job = next(job for job in store.plan.jobs if job.stage is StudyStage.PHASE_A)
    layout = dict(job.payload["layout"])
    grid = dict(dict(layout["scenario"])["initial_state_spec"])["grid"]
    root = dict(store.recipe.study["phase_a"]["roots"][0])
    return grid, str(layout["layout_id"]), str(root["root_id"])


def _live_event(
    *,
    phase: str,
    method_id: str,
    root_id: str,
    layout_id: str,
    grid: dict,
    branch: str | None,
    interaction_index: int,
    true_state: tuple[int, int],
) -> dict:
    return {
        "schema_version": 1,
        "event_type": "gridworld-transition",
        "stream_id": f"{phase}:{method_id}:{root_id}:{layout_id}:{branch or 'nominal'}",
        "phase": phase,
        "method_id": method_id,
        "root_id": root_id,
        "layout_id": layout_id,
        "branch": branch,
        "episode_index": 0,
        "interaction_index": interaction_index,
        "environment_step": interaction_index,
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
        "regime_id": "presentation-qa-only",
        "disturbance_flags": {"action_failure": False, "observation_corruption": False},
        "change_event_ids": ["presentation-qa-only"] if phase == "phase-b" else [],
    }


def write_phase_a_fixture(*, writable_root: Path, study_id: str) -> None:
    grid, layout_id, root_id = _grid_from_study(writable_root, study_id)
    start = tuple(grid["start"])
    sink = DroppingLiveEventSink(writable_root=writable_root, study_id=study_id, flush_interval_seconds=0.01)
    sink.emit(_live_event(
        phase="phase-a", method_id="q_learning", root_id=root_id, layout_id=layout_id,
        grid=grid, branch=None, interaction_index=0, true_state=start,
    ))
    sink.close()


def _free_neighbor(start: tuple[int, int], grid: dict) -> tuple[int, int]:
    obstacles = {tuple(item) for item in grid["obstacles"]}
    for candidate in ((start[0] + 1, start[1]), (start[0], start[1] + 1), (start[0] - 1, start[1]), (start[0], start[1] - 1)):
        x, y = candidate
        if 0 <= x < int(grid["width"]) and 0 <= y < int(grid["height"]) and candidate not in obstacles:
            return candidate
    return start


def write_phase_b_pair_fixture(*, writable_root: Path, study_id: str) -> None:
    grid, layout_id, root_id = _grid_from_study(writable_root, study_id)
    start = tuple(grid["start"])
    adaptive = _free_neighbor(start, grid)
    sink = DroppingLiveEventSink(writable_root=writable_root, study_id=study_id, flush_interval_seconds=0.01)
    sink.emit(_live_event(
        phase="phase-b", method_id="q_learning", root_id=root_id, layout_id=layout_id,
        grid=grid, branch="FD", interaction_index=1, true_state=start,
    ))
    sink.emit(_live_event(
        phase="phase-b", method_id="q_learning", root_id=root_id, layout_id=layout_id,
        grid=grid, branch="AD", interaction_index=1, true_state=adaptive,
    ))
    sink.close()


def add_evidence_fixture(*, writable_root: Path, study_id: str) -> None:
    store = StudyStore.load(repo_root=REPO_ROOT, writable_root=writable_root, study_id=study_id)
    fixture_dir = store.study_dir / "presentation-qa"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    previous: str | None = None
    for artifact_id, role in (
        ("ui-review-validation", ArtifactRole.VALIDATION_REPORT),
        ("ui-review-analysis", ArtifactRole.ANALYSIS_DATA),
        ("ui-review-evidence-package", ArtifactRole.EVIDENCE_PACKAGE),
        ("ui-review-provenance", ArtifactRole.PROVENANCE),
    ):
        path = fixture_dir / f"{artifact_id}.txt"
        path.write_text(
            "T-534 presentation-QA fixture only. No scientific job or final-reserve outcome produced this artifact.\n",
            encoding="utf-8",
        )
        artifact = StudyArtifact(
            artifact_id=artifact_id,
            role=role,
            evidence_class=EvidenceClass.DEVELOPMENT,
            relative_path=path.resolve().relative_to(writable_root).as_posix(),
            sha256=sha256(path),
            source_artifact_ids=() if previous is None else (previous,),
            metadata={"purpose": "presentation-qa-only", "scientific_evidence": False},
        )
        store.record_artifact(artifact)
        previous = artifact_id


def _stored(mean: float | None, half_width: float = 0.0, *, n: int = 4) -> StoredSummary:
    if mean is None:
        return StoredSummary(n=n, mean=None, interval_lower=None, interval_upper=None, interval_status="unavailable")
    return StoredSummary(n=n, mean=mean, interval_lower=mean - half_width, interval_upper=mean + half_width, interval_status=None)


def presentation_results_fixture() -> StoredAnalysisPackage:
    learning_values = (
        ("q_learning", 0.72, 0.58), ("sarsa", 0.69, 0.56), ("dqn", 0.81, 0.65),
        ("ppo", 0.77, 0.63), ("dyna_q_plus", 0.75, 0.61),
    )
    learning = tuple(
        LearningSummary(
            method_id=method_id, metric="presentation-qa-value", direction="higher-is-better",
            planned_root_count=4, included_root_count=4,
            final_value=_stored(final_value, 0.04), time_average=_stored(time_average, 0.035),
        )
        for method_id, final_value, time_average in learning_values
    )
    conditions = ("action-remap-swap-right-down", "action-remap-cycle-clockwise")
    resilience = tuple(
        ResilienceSummary(
            method_id=method_id, condition_id=condition_id, metric="presentation-qa-value",
            direction="higher-is-better", planned_root_count=4, included_root_count=4,
            frozen_loss=_stored(0.42 + 0.02 * method_index, 0.03),
            adaptive_loss=_stored(0.27 + 0.015 * method_index, 0.025),
            adaptation_benefit=_stored(0.15 + 0.005 * method_index, 0.02),
        )
        for condition_id in conditions
        for method_index, (method_id, _, _) in enumerate(learning_values)
    )
    summaries = (
        RecoverySummary(
            method_id="q_learning", condition_id=conditions[0], condition_family="action-remap",
            primary_recovery_axis=True, included_root_count=4, recovered_root_count=3,
            right_censored_root_count=1, recovered_proportion=0.75,
            recovery_time_conditional_on_recovery=_stored(96.0, 16.0, n=3),
            restricted_recovery_delay_through_horizon=_stored(136.0, 22.0, n=4),
        ),
        RecoverySummary(
            method_id="dqn", condition_id=conditions[1], condition_family="action-remap",
            primary_recovery_axis=True, included_root_count=4, recovered_root_count=0,
            right_censored_root_count=4, recovered_proportion=0.0,
            recovery_time_conditional_on_recovery=_stored(None, n=0),
            restricted_recovery_delay_through_horizon=_stored(256.0, 0.0, n=4),
        ),
    )
    trajectories = tuple(
        RecoveryTrajectoryPoint(
            method_id="q_learning", root_id="presentation-root-a", condition_id=conditions[0],
            condition_family="action-remap", primary_recovery_axis=True,
            window_index=index, window_start=(index - 1) * 32 + 1, window_end=index * 32,
            nominal_value=0.70, disturbed_value=0.50 + 0.04 * index,
            directed_gap=max(0.0, 0.20 - 0.04 * index), within_tolerance=index >= 3,
        )
        for index in range(1, 5)
    ) + tuple(
        RecoveryTrajectoryPoint(
            method_id="dqn", root_id="presentation-root-b", condition_id=conditions[1],
            condition_family="action-remap", primary_recovery_axis=True,
            window_index=index, window_start=(index - 1) * 32 + 1, window_end=index * 32,
            nominal_value=0.78, disturbed_value=0.48 + 0.01 * index,
            directed_gap=0.30 - 0.01 * index, within_tolerance=False,
        )
        for index in range(1, 9)
    )
    recovery = RecoveryEvidence(
        metric="presentation-qa-value", direction="higher-is-better", window_size=32,
        observation_horizon=256, primary_tolerance=0.1, stability_windows=2,
        primary_condition_family="action-remap", summaries=summaries,
        trajectories=trajectories, method_contrasts=(),
    )
    return StoredAnalysisPackage(
        study_id="ui-review-in-memory-not-a-study", recipe_sha256="1" * 64,
        analysis_recipe="presentation-qa-only-not-scientific", artifact_sha256="0" * 64,
        relative_path="<in-memory-presentation-fixture>", phase_a_metric="presentation-qa-value",
        phase_a_direction="higher-is-better", phase_b_metric="presentation-qa-value",
        phase_b_direction="higher-is-better", learning=learning, resilience=resilience, recovery=recovery,
    )


def show_presentation_results_fixture(window: MainWindow) -> None:
    page = window.results_page
    package = presentation_results_fixture()
    page.study_combo.blockSignals(True)
    page.study_combo.clear()
    page.study_combo.addItem("UI REVIEW · NOT SCIENTIFIC EVIDENCE", package.study_id)
    page.study_combo.blockSignals(False)
    page.selector_surface.show()
    page.empty.hide()
    page.content.show()
    page.current_package = package
    page._populate(package)
    page.provenance_title.setText("UI REVIEW FIXTURE · PRESENTATION ONLY")
    page.provenance_detail.setText(
        "Synthetic in-memory values for layout QA only · not stored evidence · not produced by a Study or scientific run.\n"
        "The application never recomputes these displayed values."
    )


def _prepare_development_review(window: MainWindow) -> None:
    page = window.experiment_page
    page.set_mode(page.DEVELOPMENT)
    page.study_label.setText("UI review · non-scientific")
    page.root_count.setValue(1)
    page.layout_count.setValue(1)
    page.review_development()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="t534-ui-review-") as directory:
        writable_root = Path(directory).resolve()
        app = create_application([])
        window = MainWindow(repo_root=REPO_ROOT, writable_root=writable_root)
        window.show()
        records: list[dict[str, object]] = []

        fixture_id = "t534-dev-ui-review"
        DesktopExploratoryStudyModel(repo_root=REPO_ROOT, writable_root=writable_root).create(
            selected_method_ids=("q_learning",), root_count=1, layout_count=1,
            study_label="T-534 UI review", study_id=fixture_id,
        )
        add_evidence_fixture(writable_root=writable_root, study_id=fixture_id)
        if (writable_root / "results" / "runs").exists():
            raise RuntimeError("T-534 UI fixture unexpectedly executed a scientific run")

        for size, suffix in ((QSize(1440, 900), "1440x900"), (QSize(1366, 768), "1366x768")):
            window.resize(size)
            window.set_page(0)
            window.experiment_page.set_mode(window.experiment_page.THESIS)
            app.processEvents()
            records.append(capture(window, output, f"01-experiment-thesis-{suffix}.png"))

            _prepare_development_review(window)
            app.processEvents()
            records.append(capture(window, output, f"02-experiment-development-review-{suffix}.png"))

            write_phase_a_fixture(writable_root=writable_root, study_id=fixture_id)
            window.set_page(1)
            window.runs_page.refresh()
            window.runs_page.study_combo.setCurrentIndex(window.runs_page.study_combo.findData(fixture_id))
            window.runs_page.refresh_live()
            app.processEvents()
            records.append(capture(window, output, f"03-run-phase-a-{suffix}.png"))

            write_phase_b_pair_fixture(writable_root=writable_root, study_id=fixture_id)
            window.runs_page.refresh_live()
            if window.runs_page._latest_frame is None or window.runs_page._latest_frame.comparison is None:
                raise RuntimeError("T-534 exact matched FD/AD presentation pair was not exposed")
            app.processEvents()
            records.append(capture(window, output, f"04-run-phase-b-frozen-adaptive-{suffix}.png"))

            window.set_page(2)
            show_presentation_results_fixture(window)
            window.results_page._show_tab(0)
            app.processEvents()
            records.append(capture(window, output, f"05-results-rq1-learning-{suffix}.png"))

            window.results_page._show_tab(1)
            window.results_page.resilience_condition.setCurrentIndex(0)
            app.processEvents()
            records.append(capture(window, output, f"06-results-rq2-resilience-{suffix}.png"))

            window.results_page._show_tab(2)
            window.results_page.recovery_view.setCurrentIndex(0)
            window.results_page.recovery_condition.setCurrentIndex(0)
            app.processEvents()
            records.append(capture(window, output, f"07-results-rq3-recovered-{suffix}.png"))

            window.results_page.recovery_condition.setCurrentIndex(1)
            app.processEvents()
            records.append(capture(window, output, f"08-results-rq3-right-censored-{suffix}.png"))

            window.set_page(3)
            window.evidence_page.refresh()
            window.evidence_page.set_study(fixture_id)
            app.processEvents()
            records.append(capture(window, output, f"09-evidence-readiness-{suffix}.png"))

            window.evidence_page.technical_button.setChecked(True)
            app.processEvents()
            records.append(capture(window, output, f"10-evidence-technical-{suffix}.png"))
            window.evidence_page.technical_button.setChecked(False)

        guide = OnboardingDialog(window)
        guide.resize(QSize(640, 440))
        guide.show()
        app.processEvents()
        records.append(capture(guide, output, "11-onboarding-final-lock.png"))
        guide.close()

        protocol_path = REPO_ROOT / "configs" / "protocols" / "protocol-v2.1-final.json"
        manifest = {
            "schema_version": 1,
            "purpose": "T-534 deterministic experiment-first presentation review; not scientific evidence",
            "viewports": [[1440, 900], [1366, 768]],
            "protocol_projection": "protocol-v2.1",
            "protocol_file_sha256": sha256(protocol_path),
            "development_fixture_created_only": True,
            "scientific_jobs_executed": 0,
            "environment_steps_executed": 0,
            "final_reserve_accessed": False,
            "final_experiment_authorized": False,
            "stored_results_fixture": "in-memory-synthetic-presentation-only-never-registered",
            "screenshots": records,
        }
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
