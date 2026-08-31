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


def _summary(mean: float) -> dict:
    return {
        "n": 1,
        "mean": mean,
        "interval": None,
        "interval_status": "insufficient-independent-roots",
    }


class DesktopResultsReadModelTests(unittest.TestCase):
    def _store_with_analysis(
        self,
        writable: Path,
        *,
        study_id: str = "results-read-model-test",
        recipe_sha_override: str | None = None,
    ) -> tuple[StudyStore, Path]:
        recipe = StudyRecipe(
            recipe_id=study_id,
            protocol_version="protocol-v2.0-development",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="results-read-model-test",
            frozen=False,
            study={"purpose": "stored-results-test"},
        )
        analysis_job = StudyJobSpec(
            job_id="analysis",
            stage=StudyStage.ANALYSIS,
            evidence_class=EvidenceClass.DERIVED,
            payload={"job_type": "study-analysis"},
        )
        store = StudyStore.create(
            repo_root=REPO_ROOT,
            writable_root=writable,
            recipe=recipe,
            plan=StudyPlan(study_id=study_id, jobs=(analysis_job,)),
        )
        package = {
            "schema_version": 1,
            "analysis_recipe": "protocol-v2-root-level-v1",
            "study_id": study_id,
            "recipe_sha256": recipe_sha_override or recipe.sha256(),
            "specification": {
                "analysis_recipe": "protocol-v2-root-level-v1",
                "phase_a_metric": "terminated_rate",
                "phase_a_direction": "higher-is-better",
                "phase_b_metric": "return_sum",
                "phase_b_direction": "higher-is-better",
                "layout_aggregation": "equal-weight",
                "require_complete_layout_blocks": True,
                "interval": {"kind": "student-t", "critical_value": 12.706},
            },
            "phase_a": {
                "metric": "terminated_rate",
                "direction": "higher-is-better",
                "unit_records": [],
                "root_records": [],
                "method_summaries": [
                    {
                        "method_id": "q_learning",
                        "metric": "terminated_rate",
                        "direction": "higher-is-better",
                        "planned_root_count": 1,
                        "included_root_count": 1,
                        "final_value": _summary(0.75),
                        "time_average": _summary(0.5),
                    }
                ],
            },
            "phase_b": {
                "metric": "return_sum",
                "direction": "higher-is-better",
                "unit_records": [],
                "root_records": [],
                "method_condition_summaries": [
                    {
                        "method_id": "q_learning",
                        "condition_id": "action-remap-swap-right-down",
                        "metric": "return_sum",
                        "direction": "higher-is-better",
                        "planned_root_count": 1,
                        "included_root_count": 1,
                        "frozen_loss": _summary(1.2),
                        "adaptive_loss": _summary(0.8),
                        "adaptation_benefit": _summary(0.4),
                    }
                ],
            },
            "scientific_denominators": {},
        }
        path = store.study_dir / "derived" / "analysis" / "analysis-package.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(package, allow_nan=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        relative = path.resolve().relative_to(writable.resolve()).as_posix()
        store.record_artifact(
            StudyArtifact(
                artifact_id="analysis-package",
                role=ArtifactRole.ANALYSIS_DATA,
                evidence_class=EvidenceClass.DERIVED,
                relative_path=relative,
                sha256=_sha256(path),
                source_job_ids=(analysis_job.job_id,),
                metadata={"record_type": "protocol-v2-analysis-package"},
            )
        )
        return store, path

    def _model(self, writable: Path) -> DesktopResultsReadModel:
        return DesktopResultsReadModel(
            DesktopStudyReadModel(repo_root=REPO_ROOT, writable_root=writable)
        )

    def test_reads_registered_backend_summaries_without_replacing_missing_interval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            store, _ = self._store_with_analysis(writable)
            model = self._model(writable)
            self.assertEqual(model.study_ids(), (store.plan.study_id,))

            package = model.load(store.plan.study_id)
            self.assertEqual(package.learning[0].final_value.mean, 0.75)
            self.assertEqual(package.learning[0].time_average.mean, 0.5)
            self.assertIsNone(package.learning[0].final_value.interval_lower)
            self.assertEqual(
                package.learning[0].final_value.interval_status,
                "insufficient-independent-roots",
            )
            self.assertEqual(package.resilience[0].frozen_loss.mean, 1.2)
            self.assertEqual(package.resilience[0].adaptive_loss.mean, 0.8)
            self.assertEqual(package.resilience[0].adaptation_benefit.mean, 0.4)

    def test_refuses_analysis_file_after_registered_sha_is_changed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            store, path = self._store_with_analysis(writable)
            path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "SHA-256"):
                self._model(writable).load(store.plan.study_id)

    def test_refuses_analysis_from_different_recipe_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            store, _ = self._store_with_analysis(
                writable,
                recipe_sha_override="0" * 64,
            )
            with self.assertRaisesRegex(RuntimeError, "recipe SHA-256"):
                self._model(writable).load(store.plan.study_id)


if __name__ == "__main__":
    unittest.main()
