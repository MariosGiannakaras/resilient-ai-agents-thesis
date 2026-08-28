from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2 import StudyValidationExecutor
from resilient_agents.study import (
    ArtifactRole,
    EvidenceClass,
    JobOutcomeKind,
    JobState,
    StudyArtifact,
    StudyExecutorRegistry,
    StudyJobSpec,
    StudyPlan,
    StudyRecipe,
    StudyScheduler,
    StudyStage,
    StudyStore,
)


class EvidenceV2ExecutorTests(unittest.TestCase):
    def _store(self, root: Path) -> StudyStore:
        recipe = StudyRecipe(
            recipe_id="validation-executor-study",
            protocol_version="protocol-v2.0-candidate",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="test",
            frozen=False,
            study={"purpose": "validation-executor"},
        )
        plan = StudyPlan(
            study_id=recipe.recipe_id,
            jobs=(
                StudyJobSpec(
                    job_id="pa",
                    stage=StudyStage.PHASE_A,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    payload={"job_type": "phase-a-training"},
                ),
                StudyJobSpec(
                    job_id="pb",
                    stage=StudyStage.PHASE_B,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    dependencies=("pa",),
                    payload={"job_type": "phase-b-matched-set"},
                ),
                StudyJobSpec(
                    job_id="validate",
                    stage=StudyStage.VALIDATION,
                    evidence_class=EvidenceClass.DERIVED,
                    payload={"job_type": "study-validation"},
                ),
            ),
        )
        return StudyStore.create(
            repo_root=root,
            writable_root=root,
            recipe=recipe,
            plan=plan,
        )

    @staticmethod
    def _file(root: Path, relative: str, content: bytes) -> tuple[str, str]:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return relative, hashlib.sha256(content).hexdigest()

    def _analysis_artifact(
        self,
        *,
        store: StudyStore,
        root: Path,
        job_id: str,
        artifact_id: str,
        source_artifact_ids: tuple[str, ...],
    ) -> None:
        path, digest = self._file(
            root,
            f"results/runs/{job_id}/analysis.json",
            b'{"record_type":"test"}\n',
        )
        store.record_artifact(
            StudyArtifact(
                artifact_id=artifact_id,
                role=ArtifactRole.ANALYSIS_DATA,
                evidence_class=EvidenceClass.DEVELOPMENT,
                relative_path=path,
                sha256=digest,
                source_job_ids=(job_id,),
                source_artifact_ids=source_artifact_ids,
            )
        )

    def test_validation_executor_records_report_and_completes_valid_study(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = self._store(root)
            store.start_job("pa")
            pa_run_path, pa_run_sha = self._file(root, "results/runs/pa/run.json", b"{}")
            cp_path, cp_sha = self._file(root, "results/runs/pa/cp.bin", b"cp")
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pa-run",
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=pa_run_path,
                    sha256=pa_run_sha,
                    source_job_ids=("pa",),
                )
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pa-cp",
                    role=ArtifactRole.SCIENTIFIC_CHECKPOINT,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=cp_path,
                    sha256=cp_sha,
                    source_job_ids=("pa",),
                    source_artifact_ids=("pa-run",),
                )
            )
            self._analysis_artifact(
                store=store,
                root=root,
                job_id="pa",
                artifact_id="pa-analysis",
                source_artifact_ids=("pa-run", "pa-cp"),
            )
            store.complete_job("pa")
            store.start_job("pb")
            pb_path, pb_sha = self._file(root, "results/runs/pb/run.json", b"{}")
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pb-run",
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=pb_path,
                    sha256=pb_sha,
                    source_job_ids=("pb",),
                    source_artifact_ids=("pa-cp",),
                )
            )
            self._analysis_artifact(
                store=store,
                root=root,
                job_id="pb",
                artifact_id="pb-analysis",
                source_artifact_ids=("pa-cp", "pb-run"),
            )
            store.complete_job("pb")

            scheduler = StudyScheduler(
                store=store,
                executors=StudyExecutorRegistry([StudyValidationExecutor()]),
            )
            result = scheduler.run_job("validate")
            self.assertIs(result.outcome.kind, JobOutcomeKind.COMPLETED)
            self.assertIs(store.lifecycle.state_for("validate"), JobState.COMPLETED)
            reports = [
                item for item in store.artifacts() if item.role is ArtifactRole.VALIDATION_REPORT
            ]
            self.assertEqual(len(reports), 1)
            report_path = root / reports[0].relative_path
            self.assertTrue(report_path.is_file())

    def test_validation_integrity_error_becomes_retryable_infrastructure_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = self._store(root)
            store.start_job("pa")
            path, digest = self._file(root, "results/runs/pa/run.json", b"{}")
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pa-run",
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=path,
                    sha256=digest,
                    source_job_ids=("pa",),
                )
            )
            store.complete_job("pa")
            store.start_job("pb")
            fail_path, fail_sha = self._file(
                root, "results/runs/pb/failure.json", b'{"kind":"scientific"}'
            )
            store.record_artifact(
                StudyArtifact(
                    artifact_id="pb-failure",
                    role=ArtifactRole.FAILURE_RECORD,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=fail_path,
                    sha256=fail_sha,
                    source_job_ids=("pb",),
                )
            )
            store.fail_job_scientifically("pb", reason="scientific failure")

            scheduler = StudyScheduler(
                store=store,
                executors=StudyExecutorRegistry([StudyValidationExecutor()]),
            )
            result = scheduler.run_job("validate")
            self.assertIs(result.outcome.kind, JobOutcomeKind.INFRASTRUCTURE_FAILURE)
            self.assertIs(
                store.lifecycle.state_for("validate"),
                JobState.INFRASTRUCTURE_FAILED,
            )
            self.assertEqual(
                len(
                    [
                        item
                        for item in store.artifacts()
                        if item.role is ArtifactRole.VALIDATION_REPORT
                    ]
                ),
                1,
            )


if __name__ == "__main__":
    unittest.main()
