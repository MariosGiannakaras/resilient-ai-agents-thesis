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
    StoredAnalysisPackage,
    StoredMethodContrast,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _contrast(source: str, estimand: str, condition_id: str | None = None) -> StoredMethodContrast:
    return StoredMethodContrast(
        source=source,
        estimand=estimand,
        condition_id=condition_id,
        primary_recovery_axis=True if source == "recovery" else None,
        method_a="q_learning",
        method_b="sarsa",
        difference_orientation="method_a-minus-method_b",
        root_ids=("r01", "r02"),
        mean_difference=0.125,
        interval_lower=0.05,
        interval_upper=0.2,
    )


def _package(study_id: str) -> StoredAnalysisPackage:
    phase_a = _contrast("phase-a", "final_value")
    phase_b = _contrast("phase-b", "adaptation_benefit", "action-failure-0.15")
    recovery_contrast = _contrast(
        "recovery",
        "restricted_recovery_delay_through_horizon",
        "action-remap-swap-right-down",
    )
    recovery = RecoveryEvidence(
        metric="return_sum",
        direction="higher-is-better",
        window_size=32,
        observation_horizon=256,
        primary_tolerance=0.1,
        stability_windows=2,
        primary_condition_family="action-remap",
        summaries=(),
        trajectories=(),
        method_contrasts=(recovery_contrast,),
    )
    return StoredAnalysisPackage(
        study_id=study_id,
        recipe_sha256="1" * 64,
        analysis_recipe="protocol-v2-root-level-v2.1",
        artifact_sha256="2" * 64,
        relative_path=f"results/studies/{study_id}/analysis-package.json",
        phase_a_metric="return_mean",
        phase_a_direction="higher-is-better",
        phase_b_metric="return_sum",
        phase_b_direction="higher-is-better",
        learning=(),
        resilience=(),
        method_contrasts=(phase_a, phase_b, recovery_contrast),
        recovery=recovery,
    )


class _FakeResultsModel:
    def __init__(self, study_ids: tuple[str, ...]) -> None:
        self._study_ids = study_ids
        self._packages = {study_id: _package(study_id) for study_id in study_ids}

    def study_ids(self) -> tuple[str, ...]:
        return self._study_ids

    def load(self, study_id: str) -> StoredAnalysisPackage:
        return self._packages[study_id]


@unittest.skipIf(QApplication is None, "PySide6 application overlay is not installed")
class T535IntendedUserWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        assert QApplication is not None
        cls.app = QApplication.instance() or QApplication([])

    def test_created_experiment_opens_run_with_new_record_selected(self) -> None:
        from resilient_agents.desktop.exploratory_study import DesktopExploratoryStudyModel
        from resilient_agents.desktop.main_window import MainWindow

        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            model = DesktopExploratoryStudyModel(repo_root=REPO_ROOT, writable_root=writable)
            model.create(
                selected_method_ids=("q_learning",),
                root_count=1,
                layout_count=1,
                study_id="t535-dev-older",
            )
            created = model.create(
                selected_method_ids=("q_learning",),
                root_count=1,
                layout_count=1,
                study_id="t535-dev-new",
            )

            window = MainWindow(repo_root=REPO_ROOT, writable_root=writable)
            window.experiment_page.study_created.emit(created.study_id)
            self.app.processEvents()

            self.assertEqual(window.stack.currentIndex(), 1)
            self.assertEqual(window.runs_page.selected_study_id(), created.study_id)
            self.assertEqual(window.evidence_page.selected_study_id(), created.study_id)
            window.close()

    def test_results_follow_available_run_context(self) -> None:
        from resilient_agents.desktop.protocol import load_frozen_protocol
        from resilient_agents.desktop.results_workspace import ResultsWorkspacePage

        page = ResultsWorkspacePage(
            _FakeResultsModel(("analysis-a", "analysis-b")),  # type: ignore[arg-type]
            load_frozen_protocol(REPO_ROOT),
        )
        page.set_study("analysis-b")
        self.assertEqual(page.study_combo.currentData(), "analysis-b")
        self.assertTrue(page.context_notice.isHidden())
        page.close()

    def test_results_warn_when_current_run_has_no_analysis_instead_of_implying_old_results(self) -> None:
        from resilient_agents.desktop.protocol import load_frozen_protocol
        from resilient_agents.desktop.results_workspace import ResultsWorkspacePage

        page = ResultsWorkspacePage(
            _FakeResultsModel(("older-analysis",)),  # type: ignore[arg-type]
            load_frozen_protocol(REPO_ROOT),
        )
        page.set_study("current-run-without-analysis")
        self.assertFalse(page.context_notice.isHidden())
        self.assertIn("has no stored validated analysis yet", page.context_notice.text())
        self.assertIn("not to the current Run experiment", page.context_notice.text())
        page.close()

    def test_direct_method_comparisons_are_partitioned_by_research_question(self) -> None:
        from resilient_agents.desktop.protocol import load_frozen_protocol
        from resilient_agents.desktop.results_workspace import ResultsWorkspacePage

        page = ResultsWorkspacePage(
            _FakeResultsModel(("analysis-a",)),  # type: ignore[arg-type]
            load_frozen_protocol(REPO_ROOT),
        )
        self.assertEqual(page.learning_contrast_table.rowCount(), 1)
        self.assertEqual(page.resilience_contrast_table.rowCount(), 1)
        self.assertEqual(page.method_contrast_table.rowCount(), 1)
        self.assertEqual(page.recovery_view.itemText(2), "Recovery method contrasts")
        self.assertTrue(page.provenance.isHidden())
        self.assertTrue(page.learning_contrast_table.isHidden())
        self.assertTrue(page.resilience_contrast_table.isHidden())
        labels = [label.text() for label in page.findChildren(QLabel)]
        self.assertIn("Experiment record", labels)
        page.close()

    def test_retry_is_hidden_without_infrastructure_failure(self) -> None:
        from resilient_agents.desktop.main_window import MainWindow

        with tempfile.TemporaryDirectory() as directory:
            window = MainWindow(repo_root=REPO_ROOT, writable_root=Path(directory))
            self.assertTrue(window.runs_page.retry_button.isHidden())
            window.close()

    def test_evidence_empty_state_names_the_user_actions(self) -> None:
        from resilient_agents.desktop.main_window import MainWindow

        with tempfile.TemporaryDirectory() as directory:
            window = MainWindow(repo_root=REPO_ROOT, writable_root=Path(directory))
            text = window.evidence_page.next_action.text()
            self.assertIn("open Experiment", text)
            self.assertIn("Run", text)
            self.assertIn("Start / resume DEVELOPMENT", text)
            window.close()

    def test_onboarding_final_gate_copy_is_task_agnostic(self) -> None:
        from resilient_agents.desktop.onboarding import _STEPS

        title, body = _STEPS[-1]
        self.assertEqual(title, "Final execution gate")
        self.assertIn("backend authorization gate", body)
        self.assertNotIn("T-534", body)
        self.assertNotIn("T-610", body)


if __name__ == "__main__":
    unittest.main()
