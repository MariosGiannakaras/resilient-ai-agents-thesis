from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PYSIDE6_AVAILABLE = importlib.util.find_spec("PySide6") is not None

if PYSIDE6_AVAILABLE:
    from PySide6.QtWidgets import QMessageBox

    from resilient_agents.desktop.app import create_application
    from resilient_agents.desktop.live_events import LiveGridComparison, LiveGridFrame
    from resilient_agents.desktop.main_window import MainWindow
    from resilient_agents.desktop.protocol import load_frozen_protocol
    from resilient_agents.desktop.results_page import ResultsPage
    from resilient_agents.desktop.results_read_model import (
        LearningSummary,
        ResilienceSummary,
        StoredAnalysisPackage,
        StoredSummary,
    )
    from resilient_agents.desktop.runs_page import RunsPage
    from resilient_agents.desktop.study_read_model import DesktopStudyReadModel


REPO_ROOT = Path(__file__).resolve().parents[1]


def _stored(value: float) -> "StoredSummary":
    return StoredSummary(
        n=4,
        mean=value,
        interval_lower=value - 0.05,
        interval_upper=value + 0.05,
        interval_status=None,
    )


def _frame(*, branch: str, state: tuple[int, int], action: str, reward: float) -> "LiveGridFrame":
    return LiveGridFrame(
        stream_id=f"test:{branch}",
        phase="phase-b",
        method_id="q_learning",
        root_id="dev-root",
        layout_id="gw-l1-a",
        branch=branch,
        episode_index=0,
        interaction_index=7,
        environment_step=7,
        width=3,
        height=3,
        start=(0, 0),
        goal=(2, 2),
        obstacles=((1, 1),),
        true_state=state,
        delivered_observation=state,
        intended_action=action,
        executed_action=action,
        reward=reward,
        terminated=False,
        truncated=False,
        regime_id="changed",
        disturbance_flags={"action_failure": False},
        change_event_ids=("change-1",),
        presentation_sequence=7,
    )


class _EmptyResultsReadModel:
    def study_ids(self) -> tuple[str, ...]:
        return ()


@unittest.skipUnless(PYSIDE6_AVAILABLE, "PySide6 is an application-only dependency")
class DesktopResearchPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_application([])
        cls.protocol = load_frozen_protocol(REPO_ROOT)

    def test_matched_gridworld_text_describes_both_branches_and_change_context(self) -> None:
        frozen = _frame(branch="FD", state=(0, 0), action="right", reward=-1.0)
        adaptive = _frame(branch="AD", state=(1, 0), action="down", reward=-0.5)
        frame = LiveGridFrame(
            **{
                **adaptive.__dict__,
                "comparison": LiveGridComparison(frozen=frozen, adaptive=adaptive),
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            read_model = DesktopStudyReadModel(
                repo_root=REPO_ROOT,
                writable_root=Path(directory),
            )
            page = RunsPage(read_model)
            page._show_live_frame(frame, is_running=True)

            self.assertIn("Exact FD/AD match", page.live_interaction.text())
            self.assertIn("Frozen — action right", page.live_transition.text())
            self.assertIn("Adaptive — action down", page.live_transition.text())
            self.assertIn("change-1", page.live_observation.text())
            self.assertIn("Frozen and Adaptive", page.live_grid.accessibleDescription())
            page.close()

    def test_results_offer_stored_loss_comparison_and_research_guidance(self) -> None:
        page = ResultsPage(_EmptyResultsReadModel(), self.protocol)
        package = StoredAnalysisPackage(
            study_id="presentation-test",
            recipe_sha256="1" * 64,
            analysis_recipe="protocol-v2-root-level-v1",
            artifact_sha256="2" * 64,
            relative_path="results/studies/presentation-test/analysis-package.json",
            phase_a_metric="terminated_rate",
            phase_a_direction="higher-is-better",
            phase_b_metric="return_sum",
            phase_b_direction="higher-is-better",
            learning=(
                LearningSummary(
                    method_id="q_learning",
                    metric="terminated_rate",
                    direction="higher-is-better",
                    planned_root_count=4,
                    included_root_count=4,
                    final_value=_stored(0.8),
                    time_average=_stored(0.7),
                ),
            ),
            resilience=(
                ResilienceSummary(
                    method_id="q_learning",
                    condition_id="action-remap-swap-right-down",
                    metric="return_sum",
                    direction="higher-is-better",
                    planned_root_count=4,
                    included_root_count=4,
                    frozen_loss=_stored(0.5),
                    adaptive_loss=_stored(0.3),
                    adaptation_benefit=_stored(0.2),
                ),
            ),
        )
        page.current_package = package
        page._populate(package)

        self.assertEqual(len(page.resilience_chart._bars), 1)
        self.assertEqual(len(page.resilience_loss_chart._bars), 2)
        self.assertEqual(page.resilience_chart._zero_label, "No matched benefit")
        self.assertIn("Positive adaptation benefit", page.resilience_guidance.text())
        self.assertIn("not screenshots", page.provenance_detail.text())
        page._show_resilience_chart(1)
        self.assertEqual(page.resilience_chart_stack.currentIndex(), 1)
        page.close()

    def test_getting_started_explains_full_research_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            window = MainWindow(repo_root=REPO_ROOT, writable_root=Path(directory))
            with patch.object(QMessageBox, "information") as information:
                window._show_getting_started()
            message = information.call_args.args[2]
            self.assertIn("1. Choose Study", message)
            self.assertIn("7. Verify Artifacts", message)
            self.assertIn("cannot be presented as final thesis evidence", message)
            window.close()


if __name__ == "__main__":
    unittest.main()
