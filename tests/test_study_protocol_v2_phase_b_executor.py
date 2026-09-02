from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from resilient_agents.evidence_v2 import StudyEvidenceValidator, StudyExportExecutor
from resilient_agents.evidence_v2.executors import (
    StudyAnalysisExecutor,
    StudyValidationExecutor,
)
from resilient_agents.study import (
    ArtifactRole,
    EvidenceClass,
    JobState,
    JobOutcomeKind,
    StudyExecutorCrashed,
    StudyExecutorRegistry,
    StudyPlanner,
    StudyRecipe,
    StudyScheduler,
    StudyStore,
)
from resilient_agents.study.protocol_v2_executors import ProtocolV2PhaseAStudyExecutor
from resilient_agents.study import protocol_v2_executors as phase_a_executors
from resilient_agents.study.protocol_v2_phase_b_executor import ProtocolV2PhaseBStudyExecutor


class StudyProtocolV2PhaseBExecutorTests(unittest.TestCase):
    def _recipe(self, *, method_id: str = "q_learning") -> StudyRecipe:
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
                            "method_id": method_id,
                            "configuration_id": f"{method_id}-test",
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
                    "analysis": {
                        "analysis_recipe": "protocol-v2-root-level-v1",
                        "phase_a_metric": "terminated_rate",
                        "phase_a_direction": "higher-is-better",
                        "phase_b_metric": "return_sum",
                        "phase_b_direction": "higher-is-better",
                        "layout_aggregation": "equal-weight",
                        "require_complete_layout_blocks": True,
                        "interval": {"kind": "none"},
                    },
                    "exports": {
                        "package": "protocol-v2-evidence-handoff-v1",
                        "emit_csv": True,
                    },
                },
            },
        )

    def test_real_q_study_runs_through_deterministic_evidence_handoff(self) -> None:
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
                        StudyValidationExecutor(),
                        StudyAnalysisExecutor(),
                        StudyExportExecutor(),
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
            checkpoint_artifact = next(
                item
                for item in store.artifacts()
                if item.artifact_id == checkpoint_id
            )
            checkpoint_payload = json.loads(
                (root / checkpoint_artifact.relative_path).read_text(encoding="utf-8")
            )
            q_settlement = checkpoint_payload["provenance"]["boundary_settlement"]
            self.assertTrue(q_settlement["no_op"])
            self.assertEqual(q_settlement["environment_interactions_consumed"], 0)
            self.assertEqual(
                q_settlement["pre_learner_state_sha256"],
                q_settlement["post_learner_state_sha256"],
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

            validation = scheduler.run_job("validate-study")
            self.assertIs(validation.outcome.kind, JobOutcomeKind.COMPLETED)
            analyzed = scheduler.run_job("analyze-study")
            self.assertIs(analyzed.outcome.kind, JobOutcomeKind.COMPLETED)
            packages = [
                item
                for item in store.artifacts()
                if item.artifact_id == "analysis-package"
            ]
            self.assertEqual(len(packages), 1)
            package = json.loads((root / packages[0].relative_path).read_text())
            self.assertEqual(package["analysis_recipe"], "protocol-v2-root-level-v1")
            self.assertEqual(len(package["phase_a"]["unit_records"]), 1)
            self.assertEqual(len(package["phase_a"]["root_records"]), 1)
            self.assertEqual(len(package["phase_b"]["unit_records"]), 1)
            self.assertEqual(len(package["phase_b"]["root_records"]), 1)
            effect = package["phase_b"]["unit_records"][0]
            self.assertIn("frozen_loss", effect)
            self.assertIn("adaptive_loss", effect)
            self.assertIn("adaptation_benefit", effect)

            exported = scheduler.run_job("export-study")
            self.assertIs(exported.outcome.kind, JobOutcomeKind.COMPLETED)
            self.assertEqual(exported.outcome.measurements["exported_files"], 6)
            handoff = next(
                item
                for item in store.artifacts()
                if item.artifact_id == "evidence-handoff-package"
            )
            manifest = json.loads((root / handoff.relative_path).read_text())
            self.assertEqual(manifest["package"], "protocol-v2-evidence-handoff-v1")
            self.assertEqual(
                manifest["figure_rendering_status"],
                "deferred-until-frozen-figure-recipe",
            )
            self.assertEqual(manifest["source_analysis_artifact_id"], "analysis-package")

            result_index = json.loads(
                (
                    root
                    / "results/studies/phase-b-integration-study/derived/export/result-index.json"
                ).read_text()
            )
            self.assertEqual(
                [item["result_id"] for item in result_index["results"]],
                ["RESULT-PA-q_learning", "RESULT-PB-q_learning-remap-swap"],
            )
            with (
                root
                / "results/studies/phase-b-integration-study/derived/export/phase-b-method-condition-summary.csv"
            ).open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["method_id"], "q_learning")
            self.assertEqual(rows[0]["condition_id"], "remap-swap")
            self.assertIn("adaptation_benefit_mean", rows[0])

    def test_real_sarsa_study_settles_phase_a_boundary_before_phase_b(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = self._recipe(method_id="sarsa")
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

            phase_a_id = "pa__sarsa__root-01__layout-a"
            phase_b_id = "pb__sarsa__root-01__layout-a__remap-swap"
            phase_a = scheduler.run_job(phase_a_id)
            self.assertIs(phase_a.outcome.kind, JobOutcomeKind.COMPLETED)
            phase_b = scheduler.run_job(phase_b_id)
            self.assertIs(phase_b.outcome.kind, JobOutcomeKind.COMPLETED)

            checkpoint_artifact = next(
                item
                for item in store.artifacts()
                if item.role is ArtifactRole.SCIENTIFIC_CHECKPOINT
            )
            checkpoint = json.loads(
                (root / checkpoint_artifact.relative_path).read_text(encoding="utf-8")
            )
            settlement = checkpoint["provenance"]["boundary_settlement"]
            self.assertEqual(
                settlement["policy_id"],
                "dec-054-phase-a-budget-boundary-settlement-v1",
            )
            self.assertEqual(settlement["environment_interactions_consumed"], 0)
            self.assertFalse(settlement["no_op"])
            self.assertNotEqual(
                settlement["pre_learner_state_sha256"],
                settlement["post_learner_state_sha256"],
            )
            self.assertEqual(
                settlement["pre_counters"], settlement["post_counters"]
            )
            self.assertEqual(settlement["post_counters"]["observed_transition_count"], 4)
            self.assertIsNone(checkpoint["state"]["pending_action"])
            self.assertIsNone(checkpoint["state"]["deferred_update"])
            self.assertEqual(phase_a.outcome.measurements["training_interactions"], 4)
            self.assertIn(
                "boundary_settlement_source_checkpoint_sha256",
                checkpoint["provenance"],
            )

    def test_study_phase_a_fails_closed_on_unexpected_unfinished_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = self._recipe(method_id="sarsa")
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=recipe,
                plan=StudyPlanner(recipe).materialize(),
            )
            scheduler = StudyScheduler(
                store=store,
                executors=StudyExecutorRegistry([ProtocolV2PhaseAStudyExecutor()]),
            )
            real_execute_phase_a = phase_a_executors.execute_phase_a

            def execute_with_invalid_pending_state(*args, **kwargs):
                result = real_execute_phase_a(*args, **kwargs)
                result.final_adapter.agent._pending_action = ('[0,0]', '"up"')
                return result

            with patch.object(
                phase_a_executors,
                "execute_phase_a",
                side_effect=execute_with_invalid_pending_state,
            ):
                with self.assertRaisesRegex(StudyExecutorCrashed, "pending_action"):
                    scheduler.run_job("pa__sarsa__root-01__layout-a")

            self.assertIs(
                store.lifecycle.state_for("pa__sarsa__root-01__layout-a"),
                JobState.INFRASTRUCTURE_FAILED,
            )
            self.assertFalse(
                any(
                    artifact.role is ArtifactRole.SCIENTIFIC_CHECKPOINT
                    for artifact in store.artifacts()
                )
            )


if __name__ == "__main__":
    unittest.main()
