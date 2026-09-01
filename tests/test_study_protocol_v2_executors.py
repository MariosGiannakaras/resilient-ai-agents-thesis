from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2.records import PhaseAAnalysisRecord
from resilient_agents.protocol_v2_tabular_driver import PROJECT_IMPLEMENTATION_ID
from resilient_agents.study import (
    ArtifactRole,
    EvidenceClass,
    StudyExecutorRegistry,
    StudyJobSpec,
    StudyPlan,
    StudyRecipe,
    StudyScheduler,
    StudyStage,
    StudyStore,
)
from resilient_agents.study.protocol_v2_executors import ProtocolV2PhaseAStudyExecutor


class ProtocolV2PhaseAStudyExecutorTests(unittest.TestCase):
    def _recipe(self) -> StudyRecipe:
        return StudyRecipe(
            recipe_id="study-executor-test",
            protocol_version="protocol-v2.0-candidate",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="executor-test",
            frozen=False,
            study={"purpose": "executor-test"},
        )

    @staticmethod
    def _scenario() -> dict:
        return {
            "scenario_id": "layout-a",
            "environment_id": "project-gridworld-v1",
            "max_steps": 12,
            "reward_spec": {"step": -0.1, "collision": -0.25, "goal": 1.0},
            "initial_state_spec": {
                "grid": {
                    "width": 3,
                    "height": 3,
                    "start": [0, 0],
                    "goal": [2, 0],
                    "obstacles": [],
                }
            },
            "dynamics_spec": {
                "action_vectors": {
                    "up": [0, -1],
                    "right": [1, 0],
                    "down": [0, 1],
                    "left": [-1, 0],
                }
            },
            "observation_spec": {
                "type": "position",
                "coordinate_order": "x-y",
                "reset_observation": "true-state",
            },
            "action_disturbance_spec": {
                "type": "no-op-failure",
                "failure_probability": 0.0,
            },
            "observation_disturbance_spec": {
                "type": "position-mislocalization",
                "mislocalization_probability": 0.0,
            },
            "change_events": [],
            "information_policy": {
                "expose_executed_action": False,
                "expose_disturbance_flags": False,
                "expose_change_indicator": False,
                "expose_regime_id": False,
                "expose_true_state": False,
            },
        }

    def _job(self, recipe: StudyRecipe) -> StudyJobSpec:
        return StudyJobSpec(
            job_id="pa__q_learning__root-01__layout-a",
            stage=StudyStage.PHASE_A,
            evidence_class=recipe.evidence_class,
            payload={
                "job_type": "phase-a-training",
                "recipe_sha256": recipe.sha256(),
                "execution": {
                    "training_interaction_budget": 16,
                    "probe_interaction_indices": [0, 16],
                    "episodes_per_probe": 1,
                    "task": {
                        "gamma": 0.95,
                        "reward_contract": {
                            "step": -0.1,
                            "collision": -0.25,
                            "goal": 1.0,
                        },
                        "administrative_truncation": True,
                        "bootstrap_on_truncation": True,
                    },
                },
                "method": {
                    "method_id": "q_learning",
                    "configuration_id": "q-test",
                    "implementation_id": PROJECT_IMPLEMENTATION_ID,
                    "role": "core",
                    "phase_b_condition_ids": ["remap"],
                    "parameters": {
                        "learning_rate": 0.2,
                        "discount_factor": 0.95,
                        "exploration_epsilon": 0.1,
                        "bootstrap_on_truncation": True,
                        "initial_q_value": 0.0,
                    },
                },
                "root": {
                    "root_id": "root-01",
                    "initialization_seed": 11,
                    "exploration_seed": 12,
                    "scenario_seed": 13,
                    "environment_seed": 14,
                    "action_disturbance_seed": 15,
                    "observation_disturbance_seed": 16,
                },
                "layout": {
                    "layout_id": "layout-a",
                    "scenario": self._scenario(),
                },
            },
        )

    def test_real_q_phase_a_job_emits_bundle_checkpoint_and_standardized_analysis(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = self._recipe()
            job = self._job(recipe)
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=recipe,
                plan=StudyPlan(study_id=recipe.recipe_id, jobs=(job,)),
            )
            scheduler = StudyScheduler(
                store=store,
                executors=StudyExecutorRegistry([ProtocolV2PhaseAStudyExecutor()]),
            )
            result = scheduler.run_job(job.job_id)
            self.assertEqual(result.outcome.kind.value, "completed")
            self.assertEqual(result.outcome.measurements["training_interactions"], 16)

            artifacts = store.artifacts()
            self.assertEqual(
                [item.role for item in artifacts],
                [
                    ArtifactRole.RUN_BUNDLE,
                    ArtifactRole.SCIENTIFIC_CHECKPOINT,
                    ArtifactRole.ANALYSIS_DATA,
                ],
            )
            checkpoint = next(
                item for item in artifacts if item.role is ArtifactRole.SCIENTIFIC_CHECKPOINT
            )
            analysis = next(
                item for item in artifacts if item.role is ArtifactRole.ANALYSIS_DATA
            )
            self.assertIn(checkpoint.artifact_id, analysis.source_artifact_ids)

            analysis_payload = json.loads(
                (root / analysis.relative_path).read_text(encoding="utf-8")
            )
            record = PhaseAAnalysisRecord.from_dict(analysis_payload)
            self.assertEqual(record.method_id, "q_learning")
            self.assertEqual([item.interaction_index for item in record.probes], [0, 16])
            self.assertEqual(
                record.resource_metrics["training_environment_interactions"], 16.0
            )

            run_manifest = next(
                item for item in artifacts if item.role is ArtifactRole.RUN_BUNDLE
            )
            manifest_payload = json.loads(
                (root / run_manifest.relative_path).read_text(encoding="utf-8")
            )
            self.assertEqual(manifest_payload["status"], "completed")
            self.assertEqual(manifest_payload["protocol_version"], recipe.protocol_version)


if __name__ == "__main__":
    unittest.main()
