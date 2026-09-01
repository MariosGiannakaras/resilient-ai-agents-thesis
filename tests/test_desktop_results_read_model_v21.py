from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.results_read_model import DesktopResultsReadModel
from resilient_agents.desktop.study_read_model import DesktopStudyReadModel
from resilient_agents.study import (
    ArtifactRole,
    EvidenceClass,
    StudyArtifact,
    StudyJobSpec,
    StudyPlan,
    StudyRecipe,
    StudyStage,
    StudyStore,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _interval(mean: float) -> dict:
    return {
        "n": 2,
        "mean": mean,
        "standard_deviation": 0.1,
        "standard_error": 0.070710678,
        "lower": mean - 0.2,
        "upper": mean + 0.2,
        "critical_value": 12.706,
        "confidence": 0.95,
    }


def _summary(mean: float) -> dict:
    return {"n": 2, "mean": mean, "interval": _interval(mean)}


def _contrast(estimand: str, *, condition_id: str | None = None, primary: bool | None = None) -> dict:
    payload = {
        "estimand": estimand,
        "method_a": "q_learning",
        "method_b": "sarsa",
        "difference_orientation": "method_a-minus-method_b",
        "root_ids": ["r1", "r2"],
        "differences": [0.1, 0.2],
        "interval": _interval(0.15),
    }
    if condition_id is not None:
        payload["condition_id"] = condition_id
    if primary is not None:
        payload["primary_recovery_axis"] = primary
    return payload


class DesktopResultsReadModelV21Tests(unittest.TestCase):
    def test_projects_stored_recovery_trajectories_and_direct_contrasts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            study_id = "results-v21-test"
            recipe = StudyRecipe(
                recipe_id=study_id,
                protocol_version="protocol-v2.1",
                evidence_class=EvidenceClass.DEVELOPMENT,
                scientific_status="synthetic-results-v21-test",
                frozen=False,
                study={"purpose": "synthetic-stored-results-test"},
            )
            job = StudyJobSpec(
                job_id="analysis",
                stage=StudyStage.ANALYSIS,
                evidence_class=EvidenceClass.DERIVED,
                payload={"job_type": "study-analysis"},
            )
            store = StudyStore.create(
                repo_root=REPO_ROOT,
                writable_root=writable,
                recipe=recipe,
                plan=StudyPlan(study_id=study_id, jobs=(job,)),
            )
            condition = "action-remap-swap-right-down"
            trajectories = []
            for root_id in ("r1", "r2"):
                for window_index in range(8):
                    end = (window_index + 1) * 32
                    trajectories.append(
                        {
                            "method_id": "q_learning",
                            "root_id": root_id,
                            "condition_id": condition,
                            "condition_family": "action-remap",
                            "primary_recovery_axis": True,
                            "window_index": window_index,
                            "window_start": window_index * 32 + 1,
                            "window_end": end,
                            "nominal_value": 0.5,
                            "disturbed_value": 0.45,
                            "directed_gap": 0.05,
                            "within_tolerance": True,
                        }
                    )
            package = {
                "schema_version": 2,
                "analysis_recipe": "protocol-v2-root-level-v2.1",
                "study_id": study_id,
                "recipe_sha256": recipe.sha256(),
                "specification": {},
                "phase_a": {
                    "metric": "return_mean",
                    "direction": "higher-is-better",
                    "unit_records": [],
                    "root_records": [],
                    "method_summaries": [
                        {
                            "method_id": "q_learning",
                            "metric": "return_mean",
                            "direction": "higher-is-better",
                            "planned_root_count": 2,
                            "included_root_count": 2,
                            "final_value": _summary(0.8),
                            "time_average": _summary(0.7),
                        }
                    ],
                    "method_contrasts": [_contrast("phase-a-final-value")],
                },
                "phase_b": {
                    "metric": "return_sum",
                    "direction": "higher-is-better",
                    "unit_records": [],
                    "root_records": [],
                    "method_condition_summaries": [
                        {
                            "method_id": "q_learning",
                            "condition_id": condition,
                            "metric": "return_sum",
                            "direction": "higher-is-better",
                            "planned_root_count": 2,
                            "included_root_count": 2,
                            "frozen_loss": _summary(1.0),
                            "adaptive_loss": _summary(0.6),
                            "adaptation_benefit": _summary(0.4),
                        }
                    ],
                    "method_contrasts": [
                        _contrast("phase-b-adaptation-benefit", condition_id=condition)
                    ],
                    "recovery": {
                        "metric": "mean-reward-per-actual-environment-interaction",
                        "direction": "higher-is-better",
                        "window_size": 32,
                        "observation_horizon": 256,
                        "primary_tolerance": 0.1,
                        "stability_windows": 2,
                        "primary_condition_family": "action-remap",
                        "sensitivity_tolerances": [0.05, 0.2],
                        "censoring_policy": "right-censored-at-fixed-horizon; recovery_time-remains-null",
                        "restricted_delay_policy": "recovery_time-if-observed-else-fixed-horizon; separate estimand, not recovery_time",
                        "root_records": [],
                        "trajectory_records": trajectories,
                        "method_condition_summaries": [
                            {
                                "method_id": "q_learning",
                                "condition_id": condition,
                                "condition_family": "action-remap",
                                "primary_recovery_axis": True,
                                "included_root_count": 2,
                                "recovered_root_count": 2,
                                "right_censored_root_count": 0,
                                "recovered_proportion": 1.0,
                                "recovery_time_conditional_on_recovery": _summary(32.0),
                                "restricted_recovery_delay_through_horizon": _summary(32.0),
                            }
                        ],
                        "method_contrasts": [
                            _contrast(
                                "restricted-recovery-delay-through-horizon",
                                condition_id=condition,
                                primary=True,
                            )
                        ],
                        "sensitivity_root_records": [],
                    },
                },
                "scientific_denominators": {},
                "interval_policy": {
                    "kind": "student-t",
                    "confidence": 0.95,
                    "selection": "actual-independent-root-count",
                },
            }
            path = store.study_dir / "derived" / "analysis" / "analysis-package.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(package, allow_nan=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="analysis-package",
                    role=ArtifactRole.ANALYSIS_DATA,
                    evidence_class=EvidenceClass.DERIVED,
                    relative_path=path.resolve().relative_to(writable.resolve()).as_posix(),
                    sha256=_sha256(path),
                    source_job_ids=(job.job_id,),
                    metadata={"record_type": "protocol-v2-analysis-package"},
                )
            )

            model = DesktopResultsReadModel(
                DesktopStudyReadModel(repo_root=REPO_ROOT, writable_root=writable)
            )
            projected = model.load(study_id)
            self.assertEqual(projected.analysis_recipe, "protocol-v2-root-level-v2.1")
            self.assertIsNotNone(projected.recovery)
            assert projected.recovery is not None
            self.assertEqual(projected.recovery.window_size, 32)
            self.assertEqual(projected.recovery.observation_horizon, 256)
            self.assertEqual(projected.recovery.primary_tolerance, 0.1)
            self.assertEqual(len(projected.recovery.trajectories), 16)
            self.assertEqual(projected.recovery.trajectories[-1].window_end, 256)
            self.assertTrue(projected.recovery.trajectories[-1].within_tolerance)
            self.assertEqual(projected.recovery.summaries[0].recovered_root_count, 2)
            self.assertEqual(
                projected.recovery.summaries[0].restricted_recovery_delay_through_horizon.mean,
                32.0,
            )
            self.assertEqual(len(projected.method_contrasts), 3)
            self.assertEqual(projected.method_contrasts[-1].source, "recovery")
            self.assertEqual(projected.method_contrasts[-1].mean_difference, 0.15)


if __name__ == "__main__":
    unittest.main()
