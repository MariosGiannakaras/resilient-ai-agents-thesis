from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.gridworld import gridworld_scenario_to_dict
from resilient_agents.study import (
    ArtifactRole,
    EvidenceClass,
    JobOutcomeKind,
    StudyJobContext,
    StudyJobSpec,
    StudyRecipe,
    StudyStage,
)
from resilient_agents.study.reference_executors import ProtocolV2PhaseAReferenceExecutor
from tests.test_gridworld import fixture_spec


class StudyReferenceExecutorTests(unittest.TestCase):
    def _job(self, recipe: StudyRecipe) -> StudyJobSpec:
        scenario = gridworld_scenario_to_dict(
            fixture_spec(
                action_failure=0.0,
                observation_corruption=0.0,
                max_steps=8,
                include_change=False,
            )
        )
        scenario.pop("gridworld_schema_version")
        return StudyJobSpec(
            job_id="ref__random__root-01__layout-a",
            stage=StudyStage.PHASE_A,
            evidence_class=EvidenceClass.DEVELOPMENT,
            payload={
                "job_type": "phase-a-reference",
                "recipe_sha256": recipe.sha256(),
                "execution": {
                    "probe_interaction_indices": [0, 4],
                    "episodes_per_probe": 2,
                },
                "reference": {
                    "reference_id": "random",
                    "role": "calibration-floor",
                },
                "root": {
                    "root_id": "root-01",
                    "initialization_seed": 101,
                    "exploration_seed": 102,
                    "scenario_seed": 103,
                    "environment_seed": 104,
                    "action_disturbance_seed": 105,
                    "observation_disturbance_seed": 106,
                },
                "layout": {
                    "layout_id": "layout-a",
                    "scenario": scenario,
                },
            },
        )

    def test_random_reference_is_real_reproducible_nonlearning_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = StudyRecipe(
                recipe_id="reference-study",
                protocol_version="protocol-v2.0-candidate",
                evidence_class=EvidenceClass.DEVELOPMENT,
                scientific_status="reference-test",
                frozen=False,
                study={"purpose": "reference-test"},
            )
            context = StudyJobContext(
                study_id=recipe.recipe_id,
                recipe=recipe,
                recipe_sha256=recipe.sha256(),
                repo_root=root,
                writable_root=root,
                study_dir=root / "results" / "studies" / recipe.recipe_id,
                attempt=1,
            )
            outcome = ProtocolV2PhaseAReferenceExecutor().execute(
                self._job(recipe),
                context=context,
            )
            self.assertIs(outcome.kind, JobOutcomeKind.COMPLETED)
            self.assertEqual(outcome.measurements["probe_count"], 2)
            self.assertGreater(outcome.measurements["probe_environment_interactions"], 0)
            self.assertEqual(
                {artifact.role for artifact in outcome.artifacts},
                {ArtifactRole.RUN_BUNDLE, ArtifactRole.ANALYSIS_DATA},
            )
            analysis = next(
                artifact
                for artifact in outcome.artifacts
                if artifact.role is ArtifactRole.ANALYSIS_DATA
            )
            payload = json.loads((root / analysis.relative_path).read_text())
            self.assertEqual(payload["record_type"], "phase-a-reference")
            self.assertEqual(payload["reference_id"], "random")
            self.assertEqual([item["interaction_index"] for item in payload["probes"]], [0, 4])

    def test_unknown_reference_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = StudyRecipe(
                recipe_id="reference-reject-study",
                protocol_version="protocol-v2.0-candidate",
                evidence_class=EvidenceClass.DEVELOPMENT,
                scientific_status="reference-test",
                frozen=False,
                study={"purpose": "reference-test"},
            )
            job = self._job(recipe)
            payload = dict(job.payload)
            payload["reference"] = {"reference_id": "oracle", "role": "upper-bound"}
            rejected = StudyJobSpec(
                job_id=job.job_id,
                stage=job.stage,
                evidence_class=job.evidence_class,
                payload=payload,
            )
            context = StudyJobContext(
                study_id=recipe.recipe_id,
                recipe=recipe,
                recipe_sha256=recipe.sha256(),
                repo_root=root,
                writable_root=root,
                study_dir=root / "results" / "studies" / recipe.recipe_id,
                attempt=1,
            )
            with self.assertRaisesRegex(ValueError, "only 'random' is explicit"):
                ProtocolV2PhaseAReferenceExecutor().execute(rejected, context=context)


if __name__ == "__main__":
    unittest.main()
