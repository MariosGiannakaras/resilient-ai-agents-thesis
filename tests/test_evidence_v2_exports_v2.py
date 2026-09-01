from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2.exports import StudyExportEngine


class EvidenceV2ExportV2Tests(unittest.TestCase):
    def _package(self):
        interval = {
            "n": 2,
            "mean": 0.1,
            "sample_std": 0.01,
            "standard_error": 0.01,
            "critical_value": 12.706,
            "lower": -0.02,
            "upper": 0.22,
        }
        summary = {"n": 2, "mean": 0.1, "interval": interval}
        contrast = {
            "estimand": "phase-a-final-value",
            "method_a": "q_learning",
            "method_b": "sarsa",
            "difference_orientation": "method_a-minus-method_b",
            "root_ids": ["r1", "r2"],
            "differences": [0.0, 0.2],
            "interval": interval,
        }
        phase_b_contrast = {
            **contrast,
            "estimand": "phase-b-adaptation-benefit",
            "condition_id": "action-remap-swap-right-down",
        }
        recovery_contrast = {
            **contrast,
            "estimand": "restricted-recovery-delay-through-horizon",
            "condition_id": "action-remap-swap-right-down",
            "primary_recovery_axis": True,
        }
        return {
            "schema_version": 2,
            "analysis_recipe": "protocol-v2-root-level-v2",
            "study_id": "protocol-v2.1-final",
            "recipe_sha256": "a" * 64,
            "phase_a": {
                "method_summaries": [
                    {
                        "method_id": "q_learning",
                        "metric": "mean_return",
                        "direction": "higher-is-better",
                        "planned_root_count": 2,
                        "included_root_count": 2,
                        "final_value": summary,
                        "time_average": summary,
                    }
                ],
                "root_records": [
                    {
                        "method_id": "q_learning",
                        "root_id": "r1",
                        "planned_layout_count": 2,
                        "observed_layout_count": 2,
                        "missing_layout_ids": [],
                        "complete_layout_block": True,
                        "included_in_primary_summary": True,
                        "final_value": 0.1,
                        "time_average": 0.1,
                    }
                ],
                "method_contrasts": [contrast],
            },
            "phase_b": {
                "method_condition_summaries": [
                    {
                        "method_id": "q_learning",
                        "condition_id": "action-remap-swap-right-down",
                        "metric": "return_sum",
                        "direction": "higher-is-better",
                        "planned_root_count": 2,
                        "included_root_count": 2,
                        "frozen_loss": summary,
                        "adaptive_loss": summary,
                        "adaptation_benefit": summary,
                    }
                ],
                "root_records": [
                    {
                        "method_id": "q_learning",
                        "root_id": "r1",
                        "condition_id": "action-remap-swap-right-down",
                        "planned_layout_count": 2,
                        "observed_layout_count": 2,
                        "missing_layout_ids": [],
                        "complete_layout_block": True,
                        "included_in_primary_summary": True,
                        "frozen_loss": 0.2,
                        "adaptive_loss": 0.1,
                        "adaptation_benefit": 0.1,
                    }
                ],
                "method_contrasts": [phase_b_contrast],
                "recovery": {
                    "root_records": [
                        {
                            "method_id": "q_learning",
                            "root_id": "r1",
                            "condition_id": "action-remap-swap-right-down",
                            "condition_family": "action-remap",
                            "primary_recovery_axis": True,
                            "planned_layout_count": 2,
                            "observed_layout_count": 2,
                            "missing_layout_ids": [],
                            "complete_layout_block": True,
                            "included_in_recovery_summary": True,
                            "status": "recovered",
                            "recovery_time": 64,
                            "confirmation_time": 96,
                            "censoring_time": 256,
                            "restricted_recovery_delay_through_horizon": 64.0,
                        }
                    ],
                    "trajectory_records": [
                        {
                            "method_id": "q_learning",
                            "root_id": "r1",
                            "condition_id": "action-remap-swap-right-down",
                            "condition_family": "action-remap",
                            "primary_recovery_axis": True,
                            "window_index": 0,
                            "window_start": 1,
                            "window_end": 32,
                            "nominal_value": 0.2,
                            "disturbed_value": 0.0,
                            "directed_gap": 0.2,
                            "within_tolerance": False,
                        }
                    ],
                    "method_condition_summaries": [
                        {
                            "method_id": "q_learning",
                            "condition_id": "action-remap-swap-right-down",
                            "condition_family": "action-remap",
                            "primary_recovery_axis": True,
                            "included_root_count": 2,
                            "recovered_root_count": 1,
                            "right_censored_root_count": 1,
                            "recovered_proportion": 0.5,
                            "recovery_time_conditional_on_recovery": {
                                "n": 1,
                                "mean": 64.0,
                                "interval": None,
                            },
                            "restricted_recovery_delay_through_horizon": summary,
                        }
                    ],
                    "method_contrasts": [recovery_contrast],
                    "sensitivity_root_records": [
                        {
                            "method_id": "q_learning",
                            "root_id": "r1",
                            "condition_id": "action-remap-swap-right-down",
                            "condition_family": "action-remap",
                            "primary_recovery_axis": True,
                            "tolerance": 0.05,
                            "status": "right-censored",
                            "recovery_time": None,
                            "confirmation_time": None,
                            "censoring_time": 256,
                        }
                    ],
                },
            },
        }

    def test_v2_emits_full_recovery_and_comparison_handoff_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            kwargs = {
                "analysis_package": self._package(),
                "specification": {
                    "package": "protocol-v2-evidence-handoff-v2",
                    "emit_csv": True,
                },
                "source_analysis_artifact_id": "analysis-package",
                "source_analysis_sha256": "b" * 64,
            }
            result_a = StudyExportEngine().export(output_dir=first, **kwargs)
            result_b = StudyExportEngine().export(output_dir=second, **kwargs)

            expected = {
                "phase-a-method-summary.csv",
                "phase-b-method-condition-summary.csv",
                "phase-a-root-records.csv",
                "phase-b-root-records.csv",
                "phase-a-method-contrasts.csv",
                "phase-b-method-contrasts.csv",
                "recovery-root-records.csv",
                "recovery-trajectory-records.csv",
                "recovery-method-condition-summary.csv",
                "recovery-method-contrasts.csv",
                "recovery-sensitivity-root-records.csv",
                "result-index.json",
            }
            self.assertEqual({item["filename"] for item in result_a["files"]}, expected)
            self.assertEqual(result_a["manifest"], result_b["manifest"])
            self.assertEqual(
                {item["filename"]: item["sha256"] for item in result_a["files"]},
                {item["filename"]: item["sha256"] for item in result_b["files"]},
            )
            self.assertIn(
                "right-censored",
                (first / "recovery-sensitivity-root-records.csv").read_text(
                    encoding="utf-8"
                ),
            )

    def test_v1_export_contract_remains_available(self) -> None:
        package = self._package()
        package["schema_version"] = 1
        package["analysis_recipe"] = "protocol-v2-root-level-v1"
        with tempfile.TemporaryDirectory() as directory:
            result = StudyExportEngine().export(
                analysis_package=package,
                specification={
                    "package": "protocol-v2-evidence-handoff-v1",
                    "emit_csv": True,
                },
                output_dir=Path(directory),
                source_analysis_artifact_id="analysis-package",
                source_analysis_sha256="c" * 64,
            )
        self.assertEqual(len(result["files"]), 5)


if __name__ == "__main__":
    unittest.main()
