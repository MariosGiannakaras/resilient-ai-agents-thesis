from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

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


class DesktopStudyReadModelTests(unittest.TestCase):
    def test_empty_writable_root_has_no_synthetic_studies(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            read_model = DesktopStudyReadModel(repo_root=REPO_ROOT, writable_root=Path(temp))
            self.assertEqual(read_model.studies(), ())

    def test_read_model_uses_empty_executor_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            read_model = DesktopStudyReadModel(repo_root=REPO_ROOT, writable_root=Path(temp))
            self.assertEqual(read_model._service.executors.job_types(), ())

    def test_artifact_projection_preserves_exact_lineage_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            writable = Path(temp).resolve()
            study_id = "desktop-artifact-lineage-test"
            recipe = StudyRecipe(
                recipe_id=study_id,
                protocol_version="protocol-v2.0-development",
                evidence_class=EvidenceClass.DEVELOPMENT,
                scientific_status="desktop-read-model-test",
                frozen=False,
                study={"purpose": "artifact-lineage-projection"},
            )
            job = StudyJobSpec(
                job_id="phase-a-test-job",
                stage=StudyStage.PHASE_A,
                evidence_class=EvidenceClass.DEVELOPMENT,
                payload={"job_type": "test-only"},
            )
            store = StudyStore.create(
                repo_root=REPO_ROOT,
                writable_root=writable,
                recipe=recipe,
                plan=StudyPlan(study_id=study_id, jobs=(job,)),
            )

            source_path = store.study_dir / "derived" / "source.txt"
            source_path.parent.mkdir(parents=True, exist_ok=True)
            source_path.write_text("source\n", encoding="utf-8")
            store.record_artifact(
                StudyArtifact(
                    artifact_id="source-artifact",
                    role=ArtifactRole.PROVENANCE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=source_path.resolve().relative_to(writable).as_posix(),
                    sha256=_sha256(source_path),
                )
            )

            derived_path = store.study_dir / "derived" / "derived.txt"
            derived_path.write_text("derived\n", encoding="utf-8")
            store.record_artifact(
                StudyArtifact(
                    artifact_id="derived-artifact",
                    role=ArtifactRole.PRESENTATION_ASSET,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=derived_path.resolve().relative_to(writable).as_posix(),
                    sha256=_sha256(derived_path),
                    source_job_ids=(job.job_id,),
                    source_artifact_ids=("source-artifact",),
                )
            )

            items = DesktopStudyReadModel(
                repo_root=REPO_ROOT,
                writable_root=writable,
            ).artifacts(study_id)
            derived = next(item for item in items if item.artifact_id == "derived-artifact")
            self.assertEqual(derived.source_job_ids, (job.job_id,))
            self.assertEqual(derived.source_artifact_ids, ("source-artifact",))
            self.assertEqual(derived.source_job_count, 1)
            self.assertEqual(derived.source_artifact_count, 1)


if __name__ == "__main__":
    unittest.main()
