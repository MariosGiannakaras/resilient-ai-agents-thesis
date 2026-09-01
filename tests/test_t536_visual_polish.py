from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6.QtWidgets import QApplication, QLabel
except ImportError:
    QApplication = None  # type: ignore[assignment]
    QLabel = None  # type: ignore[assignment]

from resilient_agents.desktop.results_read_model import (
    RecoveryEvidence,
    RecoverySummary,
    RecoveryTrajectoryPoint,
    StoredAnalysisPackage,
    StoredSummary,
)
from resilient_agents.desktop.study_read_model import StudyListItem

REPO_ROOT = Path(__file__).resolve().parents[1]


def _stored(mean: float | None, *, n: int = 4) -> StoredSummary:
    if mean is None:
        return StoredSummary(
            n=0,
            mean=None,
            interval_lower=None,
            interval_upper=None,
            interval_status="unavailable",
        )
    return StoredSummary(
        n=n,
        mean=mean,
        interval_lower=mean - 4.0,
        interval_upper=mean + 4.0,
        interval_status=None,
    )


def _recovery_package(*, recovered: bool) -> StoredAnalysisPackage:
    condition = "action-remap-swap-right-down"
    method = "q_learning"
    summary = RecoverySummary(
        method_id=method,
        condition_id=condition,
        condition_family="action-remap",
        primary_recovery_axis=True,
        included_root_count=4,
        recovered_root_count=3 if recovered else 0,
        right_censored_root_count=1 if recovered else 4,
        recovered_proportion=0.75 if recovered else 0.0,
        recovery_time_conditional_on_recovery=_stored(96.0, n=3) if recovered else _stored(None, n=0),
        restricted_recovery_delay_through_horizon=_stored(136.0 if recovered else 256.0),
    )
    points = tuple(
        RecoveryTrajectoryPoint(
            method_id=method,
            root_id=root_id,
            condition_id=condition,
            condition_family="action-remap",
            primary_recovery_axis=True,
            window_index=index - 1,
            window_start=(index - 1) * 32 + 1,
            window_end=index * 32,
            nominal_value=0.70,
            disturbed_value=0.48 + 0.04 * index,
            directed_gap=max(0.0, 0.22 - 0.04 * index),
            within_tolerance=(recovered and index >= 4),
        )
        for root_id in ("r01", "r02", "r03", "r04")
        for index in range(1, 9)
    )
    recovery = RecoveryEvidence(
        metric="mean-reward-per-actual-environment-interaction",
        direction="higher-is-better",
        window_size=32,
        observation_horizon=256,
        primary_tolerance=0.10,
        stability_windows=2,
        primary_condition_family="action-remap",
        summaries=(summary,),
        trajectories=points,
        method_contrasts=(),
    )
    return StoredAnalysisPackage(
        study_id="t536-results",
        recipe_sha256="1" * 64,
        analysis_recipe="protocol-v2-root-level-v2.1",
        artifact_sha256="2" * 64,
        relative_path="results/studies/t536-results/analysis-package.json",
        phase_a_metric="return_mean",
        phase_a_direction="higher-is-better",
        phase_b_metric="return_sum",
        phase_b_direction="higher-is-better",
        learning=(),
        resilience=(),
        recovery=recovery,
    )


class _FakeResultsModel:
    def __init__(self, package: StoredAnalysisPackage) -> None:
        self.package = package

    def study_ids(self) -> tuple[str, ...]:
        return (self.package.study_id,)

    def load(self, study_id: str) -> StoredAnalysisPackage:
        if study_id != self.package.study_id:
            raise KeyError(study_id)
        return self.package


@unittest.skipIf(QApplication is None, "PySide6 application overlay is not installed")
class T536VisualPolishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        assert QApplication is not None
        cls.app = QApplication.instance() or QApplication([])

    def test_run_orientation_keeps_five_method_strip_and_marks_current_method(self) -> None:
        from resilient_agents.desktop.protocol import load_frozen_protocol
        from resilient_agents.desktop.run_workspace_user import RunWorkspacePage
        from resilient_agents.desktop.study_read_model import DesktopStudyReadModel

        with tempfile.TemporaryDirectory() as directory:
            model = DesktopStudyReadModel(repo_root=REPO_ROOT, writable_root=Path(directory))
            page = RunWorkspacePage(model, load_frozen_protocol(REPO_ROOT))
            item = StudyListItem(
                study_id="t536-dev",
                protocol_version="protocol-v2.1-development",
                evidence_class="development",
                status="running",
                current_stage="phase-a",
                total_jobs=10,
                resolved_jobs=2,
                completed_jobs=2,
                running_jobs=1,
                scientific_failures=0,
                infrastructure_failures=0,
                finalized=False,
                method_ids=("q_learning", "sarsa"),
                method_statuses=(("q_learning", "Running"), ("sarsa", "Pending")),
            )
            page._refresh_method_orientation(item, current_method_id="q_learning")
            labels = [
                label
                for label in page.method_overview.findChildren(QLabel)
                if label.objectName() in {"MethodStatus", "CurrentMethodStatus"}
            ]
            self.assertEqual(len(labels), 5)
            self.assertEqual(page.current_method_label.text(), "Method 1 of 5 · Q-Learning")
            self.assertEqual(
                len([label for label in labels if label.objectName() == "CurrentMethodStatus"]),
                1,
            )
            self.assertTrue(any("Dyna-Q+ · Not selected" in label.text() for label in labels))
            self.assertEqual(page.method_strip.count(), 0)
            self.assertGreaterEqual(page.grid.minimumHeight(), 260)
            page.close()

    def test_results_charts_have_more_visual_weight_and_rq3_uses_stored_trajectory_chart(self) -> None:
        from resilient_agents.desktop.protocol import load_frozen_protocol
        from resilient_agents.desktop.results_workspace import ResultsWorkspacePage

        page = ResultsWorkspacePage(
            _FakeResultsModel(_recovery_package(recovered=True)),  # type: ignore[arg-type]
            load_frozen_protocol(REPO_ROOT),
        )
        self.assertGreaterEqual(page.learning_chart.minimumHeight(), 215)
        self.assertGreaterEqual(page.resilience_chart.minimumHeight(), 215)
        description = page.recovery_chart.accessibleDescription()
        self.assertIn("3 recovered roots", description)
        self.assertIn("1 right-censored roots", description)
        self.assertIn("Stored tolerance 0.1", description)
        self.assertIn("stored conditional recovery-time mean 96", description)
        self.assertIn("no UI aggregation is performed", description)
        page.close()

    def test_rq3_non_recovery_is_explicitly_right_censored_without_fake_recovery_time(self) -> None:
        from resilient_agents.desktop.protocol import load_frozen_protocol
        from resilient_agents.desktop.results_workspace import ResultsWorkspacePage

        page = ResultsWorkspacePage(
            _FakeResultsModel(_recovery_package(recovered=False)),  # type: ignore[arg-type]
            load_frozen_protocol(REPO_ROOT),
        )
        description = page.recovery_chart.accessibleDescription()
        self.assertIn("0 recovered roots", description)
        self.assertIn("4 right-censored roots", description)
        self.assertIn("no observed recovery-time summary", description)
        self.assertIn("right-censored through 256", description)
        page.close()

    def test_sparse_review_and_evidence_surfaces_use_more_available_space(self) -> None:
        from resilient_agents.desktop.main_window import MainWindow

        with tempfile.TemporaryDirectory() as directory:
            window = MainWindow(repo_root=REPO_ROOT, writable_root=Path(directory))
            self.assertGreaterEqual(window.experiment_page.review_surface.minimumHeight(), 178)
            for frame, _state, _detail in (
                window.evidence_page.validation_card,
                window.evidence_page.analysis_card,
                window.evidence_page.export_card,
            ):
                self.assertGreaterEqual(frame.minimumHeight(), 142)
            window.close()


if __name__ == "__main__":
    unittest.main()
