from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PYSIDE6_AVAILABLE = importlib.util.find_spec("PySide6") is not None

if PYSIDE6_AVAILABLE:
    from resilient_agents.desktop.app import create_application
    from resilient_agents.desktop.protocol import load_frozen_protocol
    from resilient_agents.desktop.results_page import ResultsPage
    from resilient_agents.desktop.results_read_model import (
        RecoveryEvidence,
        RecoverySummary,
        RecoveryTrajectoryPoint,
        StoredAnalysisPackage,
        StoredMethodContrast,
        StoredSummary,
    )

REPO_ROOT = Path(__file__).resolve().parents[1]


class _EmptyResultsReadModel:
    def study_ids(self) -> tuple[str, ...]:
        return ()


def _stored(value: float) -> "StoredSummary":
    return StoredSummary(
        n=2,
        mean=value,
        interval_lower=value - 1.0,
        interval_upper=value + 1.0,
        interval_status=None,
    )


@unittest.skipUnless(PYSIDE6_AVAILABLE, "PySide6 is an application-only dependency")
class DesktopRecoveryPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_application([])
        cls.protocol = load_frozen_protocol(REPO_ROOT)

    def test_recovery_tab_presents_only_stored_summary_trajectory_and_contrast_values(self) -> None:
        condition = "action-remap-swap-right-down"
        recovery = RecoveryEvidence(
            metric="mean-reward-per-actual-environment-interaction",
            direction="higher-is-better",
            window_size=32,
            observation_horizon=256,
            primary_tolerance=0.1,
            stability_windows=2,
            primary_condition_family="action-remap",
            summaries=(
                RecoverySummary(
                    method_id="q_learning",
                    condition_id=condition,
                    condition_family="action-remap",
                    primary_recovery_axis=True,
                    included_root_count=2,
                    recovered_root_count=1,
                    right_censored_root_count=1,
                    recovered_proportion=0.5,
                    recovery_time_conditional_on_recovery=_stored(64.0),
                    restricted_recovery_delay_through_horizon=_stored(160.0),
                ),
            ),
            trajectories=(
                RecoveryTrajectoryPoint(
                    method_id="q_learning",
                    root_id="r1",
                    condition_id=condition,
                    condition_family="action-remap",
                    primary_recovery_axis=True,
                    window_index=0,
                    window_start=1,
                    window_end=32,
                    nominal_value=0.5,
                    disturbed_value=0.3,
                    directed_gap=0.2,
                    within_tolerance=False,
                ),
                RecoveryTrajectoryPoint(
                    method_id="q_learning",
                    root_id="r1",
                    condition_id=condition,
                    condition_family="action-remap",
                    primary_recovery_axis=True,
                    window_index=1,
                    window_start=33,
                    window_end=64,
                    nominal_value=0.5,
                    disturbed_value=0.45,
                    directed_gap=0.05,
                    within_tolerance=True,
                ),
            ),
            method_contrasts=(
                StoredMethodContrast(
                    source="recovery",
                    estimand="restricted-recovery-delay-through-horizon",
                    condition_id=condition,
                    primary_recovery_axis=True,
                    method_a="q_learning",
                    method_b="sarsa",
                    difference_orientation="method_a-minus-method_b",
                    root_ids=("r1", "r2"),
                    mean_difference=-32.0,
                    interval_lower=-64.0,
                    interval_upper=0.0,
                ),
            ),
        )
        package = StoredAnalysisPackage(
            study_id="recovery-presentation-test",
            recipe_sha256="1" * 64,
            analysis_recipe="protocol-v2-root-level-v2.1",
            artifact_sha256="2" * 64,
            relative_path="results/studies/recovery-presentation-test/analysis-package.json",
            phase_a_metric="return_mean",
            phase_a_direction="higher-is-better",
            phase_b_metric="return_sum",
            phase_b_direction="higher-is-better",
            learning=(),
            resilience=(),
            method_contrasts=recovery.method_contrasts,
            recovery=recovery,
        )

        page = ResultsPage(_EmptyResultsReadModel(), self.protocol)
        page.current_package = package
        page._populate(package)

        self.assertTrue(page.recovery_button.isEnabled())
        self.assertIn("32-interaction windows", page.recovery_guidance.text())
        self.assertIn("right-censored", page.recovery_guidance.text())
        self.assertEqual(page.recovery_summary_table.rowCount(), 1)
        self.assertEqual(page.recovery_summary_table.item(0, 2).text(), "1")
        self.assertEqual(page.recovery_summary_table.item(0, 3).text(), "1")
        self.assertEqual(page.recovery_summary_table.item(0, 5).text(), "64")
        self.assertEqual(page.recovery_summary_table.item(0, 6).text(), "160")

        page.recovery_view.setCurrentIndex(1)
        self.assertEqual(page.recovery_trajectory_table.rowCount(), 2)
        self.assertEqual(page.recovery_trajectory_table.item(0, 4).text(), "0.2")
        self.assertEqual(page.recovery_trajectory_table.item(1, 5).text(), "Yes")

        page.recovery_view.setCurrentIndex(2)
        self.assertEqual(page.method_contrast_table.rowCount(), 1)
        self.assertEqual(page.method_contrast_table.item(0, 5).text(), "-32")
        self.assertEqual(page.method_contrast_table.item(0, 7).text(), "2")
        page.close()

    def test_schema_v1_package_keeps_recovery_tab_disabled(self) -> None:
        package = StoredAnalysisPackage(
            study_id="legacy-presentation-test",
            recipe_sha256="1" * 64,
            analysis_recipe="protocol-v2-root-level-v1",
            artifact_sha256="2" * 64,
            relative_path="results/studies/legacy/analysis-package.json",
            phase_a_metric="return_mean",
            phase_a_direction="higher-is-better",
            phase_b_metric="return_sum",
            phase_b_direction="higher-is-better",
            learning=(),
            resilience=(),
        )
        page = ResultsPage(_EmptyResultsReadModel(), self.protocol)
        page.current_package = package
        page._populate(package)
        self.assertFalse(page.recovery_button.isEnabled())
        self.assertIn("No protocol-v2.1 recovery evidence", page.recovery_guidance.text())
        page.close()


if __name__ == "__main__":
    unittest.main()
