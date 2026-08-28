from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2 import StudyEvidenceValidator
from resilient_agents.study import (
    ArtifactRole,
    EvidenceClass,
    JobOutcomeKind,
    StudyExecutorRegistry,
    StudyPlanner,
    StudyRecipe,
    StudyScheduler,
    StudyStore,
)
from resilient_agents.study.protocol_v2_executors import ProtocolV2PhaseAStudyExecutor
from resilient_agents.study.protocol_v2_phase_b_executor import ProtocolV2PhaseBStudyExecutor


class StudyProtocolV2PhaseBExecutorTests(unittest.TestCase):
    def _recipe(self) -> StudyRecipe:
        scenario = {
            "scenario_id": "layout-a",
            "environment_id": "project-gridworld-v1",
            "max_steps": 20,
            "reward_spec": {"step": -0.1, "collision": -0.25, "goal": 1.0},
            "initial_state_spec": {
                "grid": {
                    "width": 10,
                    "height": 10,
                    "start": [0, 0],
                    "goal": [9, 9],
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
        return StudyRecipe(
            recipe_id="phase-b-integration-study",
            protocol_version="protocol-v2.0-candidate",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="phase-b-integration-test",
            frozen=False,
            study={
                "matrix_schema_version": 2,
                "phase_a": {
                    "execution": {
                        "training_interaction_budget": 4,
                        "probe_interaction_indices": [0, 4],
                        "episodes_per_probe": 1,
                        "task": {
                            "gamma": 0.9,
                            "reward_contract": {
                                "step": -0.1,
                                "collision": -0.25,
                                "goal": 1.0,
                            },
                            "administrative_truncation": True,
                            "bootstrap_on_truncation": True,
                        },
                    },
                    "methods": [
                        {
                            "method_id": "q_learning",
                            "configuration_id": "q-test",
                            "implementation_id": "project-protocol-v2-state-adapter",
                            "role": "core",
                            "parameters": {
                                "learning_rate": 0.2,
                                "discount_factor": 0.9,
                                "exploration_epsilon": 0.1,
                                "bootstrap_on_truncation": True,
                                "initial_q_value": 0.0,
                            },
                            "phase_b_condition_ids": ["remap-swap"],
                        }
                    ],
                    "references": [],
                    "roots": [
                        {
                            "root_id": "root-01",
                            "initialization_seed": 101,
                            "exploration_seed": 102,
                            "scenario_seed": 103,
                            "environment_seed": 104,
                            "action_disturbance_seed": 105,
                            "observation_disturbance_seed": 106,
                        }
                    ],
                    "layouts": [
                        {
                            "layout_id": "layout-a",
                            "family": "test",
                            "scenario": scenario,
                        }
                    ],
                },
                "phase_b": {
                    "execution": {
                        "interaction_budget_per_branch": 1,
                        "prefix_interactions": 1,
                    },
                    "conditions": [
                        {
                            "condition_id": "remap-swap",
                            "family": "action-remap",
                            "specification": {"mapping_id": "swap-right-down"},
                        }
                    ],
                    "branches": ["FN", "FD", "AN", "AD"],
                },
                "postprocessing": {
                    "validation": {"validator": "protocol-v2-study"},
                    "analysis": {"analysis_recipe": "root-level-did"},
                    "exports": {"package": "thesis-evidence"},
                },
            },
        )

    def test_real_q_phase_a_checkpoint_drives_atomic_four_branch_phase_b(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = self._recipe()
            plan = StudyPlanner(recipe).materialize()
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=recipe,
                plan=plan,
            )
            scheduler = StudyScheduler(
                store=store,
                executors=StudyExecutorRegistry(
                    [
                        ProtocolV2PhaseAStudyExecutor(),
                        ProtocolV2PhaseBStudyExecutor(),
                    ]
                ),
            )

            phase_a_id = "pa__q_learning__root-01__layout-a"
            phase_b_id = "pb__q_learning__root-01__layout-a__remap-swap"
            phase_a = scheduler.run_job(phase_a_id)
            self.assertIs(phase_a.outcome.kind, JobOutcomeKind.COMPLETED)
            phase_b = scheduler.run_job(phase_b_id)
            self.assertIs(phase_b.outcome.kind, JobOutcomeKind.COMPLETED)
            self.assertEqual(phase_b.outcome.measurements["post_boundary_interactions"], 4)

            artifacts = [
                item for item in store.artifacts() if phase_b_id in item.source_job_ids
            ]
            self.assertEqual(
                len([item for item in artifacts if item.role is ArtifactRole.RUN_BUNDLE]),
                1,
            )
            analysis = [
                item for item in artifacts if item.role is ArtifactRole.ANALYSIS_DATA
            ]
            self.assertEqual(len(analysis), 5)
            checkpoint_id = f"checkpoint__{phase_a_id}"
            self.assertTrue(
                all(checkpoint_id in item.source_artifact_ids for item in artifacts)
            )

            matched_artifact = next(
                item
                for item in analysis
                if item.metadata.get("record_type") == "phase-b-matched-set"
            )
            matched = json.loads((root / matched_artifact.relative_path).read_text())
            self.assertEqual(
                [item["branch"] for item in matched["branches"]],
                ["FN", "FD", "AN", "AD"],
            )
            self.assertEqual(matched["prefix_interactions"], 1)
            self.assertEqual(
                matched["phase_a_checkpoint_artifact_id"],
                checkpoint_id,
            )

            report = StudyEvidenceValidator().validate(store)
            self.assertTrue(report.valid, report.to_dict())
            self.assertEqual(report.planned_scientific_jobs, 2)
            self.assertEqual(report.completed_scientific_jobs, 2)


if __name__ == "__main__":
    unittest.main()
