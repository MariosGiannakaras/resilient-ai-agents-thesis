from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2 import StudyEvidenceValidator
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


class EvidenceV2ValidationTests(unittest.TestCase):
    def _recipe(self, recipe_id: str = "evidence-study") -> StudyRecipe:
        return StudyRecipe(
            recipe_id=recipe_id,
            protocol_version="protocol-v2.0-candidate",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="validation-test",
            frozen=False,
            study={"purpose": "evidence-validation"},
        )

    def _plan(self, recipe: StudyRecipe) -> StudyPlan:
        digest = recipe.sha256()
        return StudyPlan(
            study_id=recipe.recipe_id,
            jobs=(
                StudyJobSpec(
                    job_id="pa",
                    stage=StudyStage.PHASE_A,
                    evidence_class=recipe.evidence_class,
                    payload={
                        "job_type": "phase-a-training",
                        "recipe_sha256": digest,
                    },
                ),
                StudyJobSpec(
                    job_id="pb",
                    stage=StudyStage.PHASE_B,
                    evidence_class=recipe.evidence_class,
                    dependencies=("pa",),
                    payload={
                        "job_type": "phase-b-matched-set",
                        "recipe_sha256": digest,
                        "branches": ["FN", "FD", "AN", "AD"],
                    },
                ),
                StudyJobSpec(
                    job_id="validate",
                    stage=StudyStage.VALIDATION,
                    evidence_class=EvidenceClass.DERIVED,
                    payload={
                        "job_type": "study-validation",
                        "recipe_sha256": digest,
                    },
                ),
            ),
        )

    def _store(self, root: Path) -> StudyStore:
        recipe = self._recipe()
        return StudyStore.create(
            repo_root=root,
            writable_root=root,
            recipe=recipe,
            plan=self._plan(recipe),
        )

    @staticmethod
    def _write(root: Path, relative: str, data: bytes) -> tuple[str, str]:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return relative, hashlib.sha256(data).hexdigest()

    def _record_phase_a_success(self, store: StudyStore, root: Path) -> str:
        store.start_job("pa")
        run_path, run_sha = self._write(
            root, "results/runs/pa/summary.json", b'{"status":"completed"}\n'
        )
        checkpoint_path, checkpoint_sha = self._write(
            root, "results/runs/pa/checkpoint.bin", b"checkpoint"
        )
        analysis_path, analysis_sha = self._write(
            root, "results/runs/pa/analysis.json", b'{"record_type":"phase-a"}\n'
        )
        store.record_artifact(
            StudyArtifact(
                artifact_id="pa-run",
                role=ArtifactRole.RUN_BUNDLE,
                evidence_class=EvidenceClass.DEVELOPMENT,
                relative_path=run_path,
                sha256=run_sha,
                source_job_ids=("pa",),
            )
        )
        store.record_artifact(
            StudyArtifact(
                artifact_id="pa-checkpoint",
                role=ArtifactRole.SCIENTIFIC_CHECKPOINT,
                evidence_class=EvidenceClass.DEVELOPMENT,
                relative_path=checkpoint_path,
                sha256=checkpoint_sha,
                source_job_ids=("pa",),
                source_artifact_ids=("pa-run",),
            )
        )
        store.record_artifact(
            StudyArtifact(
                artifact_id="pa-analysis",
                role=ArtifactRole.ANALYSIS_DATA,
                evidence_class=EvidenceClass.DEVELOPMENT,
                relative_path=analysis_path,
                sha256=analysis_sha,
                source_job_ids=("pa",),
                source_artifact_ids=("pa-run", "pa-checkpoint"),
            )
        )
        store.complete_job("pa")
        return "pa-checkpoint"

    def _record_phase_b_success(
        self,
        store: StudyStore,
        root: Path,
        *,
        checkpoint_id: str,
    ) -> None:
        store.start_job("pb")
        run_path, run_sha = self._write(
            root, "results/runs/pb/summary.json", b'{"status":"completed"}\n'
        )
        analysis_path, analysis_sha = self._write(
            root, "results/runs/pb/analysis.json", b'{"record_type":"phase-b-matched-set"}\n'
        )
        store.record_artifact(
            StudyArtifact(
                artifact_id="pb-run",
                role=ArtifactRole.RUN_BUNDLE,
                evidence_class=EvidenceClass.DEVELOPMENT,
                relative_path=run_path,
                sha256=run_sha,
                source_job_ids=("pb",),
                source_artifact_ids=(checkpoint_id,),
            )
        )
        store.record_artifact(
            StudyArtifact(
                artifact_id="pb-analysis",
                role=ArtifactRole.ANALYSIS_DATA,
                evidence_class=EvidenceClass.DEVELOPMENT,
                relative_path=analysis_path,
                sha256=analysis_sha,
                source_job_ids=("pb",),
                source_artifact_ids=(checkpoint_id, "pb-run"),
            )
        )
        store.complete_job("pb")

    def test_valid_completed_evidence_traces_phase_b_to_exact_phase_a_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = self._store(root)
            checkpoint_id = self._record_phase_a_success(store, root)
            self._record_phase_b_success(store, root, checkpoint_id=checkpoint_id)

            report = StudyEvidenceValidator().validate(store)
            self.assertTrue(report.valid)
            self.assertTrue(report.ready_for_analysis)
            self.assertEqual(report.planned_scientific_jobs, 2)
            self.assertEqual(report.completed_scientific_jobs, 2)
            self.assertEqual(report.checkpoint_count, 1)
            self.assertEqual(report.run_bundle_count, 2)
            self.assertEqual(report.findings, ())

    def test_completed_phase_a_without_checkpoint_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = self._store(root)
            store.start_job("pa")
            run_path, run_sha = self._write(root, "results/runs/pa/summary.json", b"{}")
            analysis_path, analysis_sha = self._write(
                root, "results/runs/pa/analysis.json", b"{}"
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pa-run",
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=run_path,
                    sha256=run_sha,
                    source_job_ids=("pa",),
                )
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pa-analysis",
                    role=ArtifactRole.ANALYSIS_DATA,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=analysis_path,
                    sha256=analysis_sha,
                    source_job_ids=("pa",),
                    source_artifact_ids=("pa-run",),
                )
            )
            store.complete_job("pa")
            store.start_job("pb")
            failure_path, failure_sha = self._write(
                root, "results/runs/pb/failure.json", b'{"kind":"scientific"}'
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pb-failure",
                    role=ArtifactRole.FAILURE_RECORD,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=failure_path,
                    sha256=failure_sha,
                    source_job_ids=("pb",),
                )
            )
            store.fail_job_scientifically("pb", reason="scientific failure")

            report = StudyEvidenceValidator().validate(store)
            self.assertFalse(report.valid)
            self.assertIn(
                "REQUIRED_ARTIFACT_MISSING",
                {item.code for item in report.findings},
            )
            self.assertIn(
                "PHASE_A_CHECKPOINT_AMBIGUOUS",
                {item.code for item in report.findings},
            )

    def test_scientific_phase_a_failure_is_valid_when_recorded_and_matched_set_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = self._store(root)
            store.start_job("pa")
            failure_path, failure_sha = self._write(
                root, "results/runs/pa/failure.json", b'{"kind":"scientific"}'
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pa-failure",
                    role=ArtifactRole.FAILURE_RECORD,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=failure_path,
                    sha256=failure_sha,
                    source_job_ids=("pa",),
                )
            )
            store.fail_job_scientifically("pa", reason="non-finite update")

            report = StudyEvidenceValidator().validate(store)
            self.assertTrue(report.valid)
            self.assertEqual(report.scientific_failures, 1)
            self.assertEqual(report.skipped_scientific_jobs, 1)
            self.assertEqual(report.failure_record_count, 1)

    def test_phase_b_evidence_without_exact_checkpoint_lineage_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = self._store(root)
            self._record_phase_a_success(store, root)
            store.start_job("pb")
            run_path, run_sha = self._write(root, "results/runs/pb/summary.json", b"{}")
            analysis_path, analysis_sha = self._write(
                root, "results/runs/pb/analysis.json", b"{}"
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pb-run",
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=run_path,
                    sha256=run_sha,
                    source_job_ids=("pb",),
                )
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pb-analysis",
                    role=ArtifactRole.ANALYSIS_DATA,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=analysis_path,
                    sha256=analysis_sha,
                    source_job_ids=("pb",),
                    source_artifact_ids=("pb-run",),
                )
            )
            store.complete_job("pb")

            report = StudyEvidenceValidator().validate(store)
            self.assertFalse(report.valid)
            self.assertIn(
                "PHASE_B_CHECKPOINT_LINEAGE_MISSING",
                {item.code for item in report.findings},
            )

    def test_unresolved_infrastructure_state_is_not_analysis_ready(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = self._store(root)
            store.start_job("pa")
            store.fail_job_infrastructure("pa", reason="disk interrupted")
            report = StudyEvidenceValidator().validate(store)
            self.assertFalse(report.ready_for_analysis)
            self.assertIn(
                "SCIENTIFIC_JOB_UNRESOLVED",
                {item.code for item in report.findings},
            )


if __name__ == "__main__":
    unittest.main()
