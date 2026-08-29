from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from resilient_agents.environment import EnvironmentSeeds
from resilient_agents.gridworld import GridAction, GridWorldEnvironment, ResolvedGridWorldScenario
from resilient_agents.protocol_v2 import ProtocolV2Branch
from resilient_agents.protocol_v2_executor import execute_phase_b
from resilient_agents.protocol_v2_feasibility import _scenario, load_plan
from resilient_agents.protocol_v2_gridworld import GridWorldScientificStateAdapter
from resilient_agents.protocol_v2_t526_recovery import (
    _file_sha256,
    _write_json,
    compare_reconstruction_row,
    load_amendment,
    require_complete_recovery_barrier,
    validate_recovery_attempt_evidence,
    verify_original_bundle,
    verify_source_compatibility,
)

try:
    from stable_baselines3 import PPO

    from resilient_agents.protocol_v2_sb3 import ppo_state_adapter
    from resilient_agents.protocol_v2_sb3_gridworld import ExplicitSeededGridWorldEnv
    from resilient_agents.protocol_v2_t526_phase_b import (
        T526PPOTransientStateAdapter,
        t526_branch_driver,
    )
    from resilient_agents.study.protocol_v2_phase_b_executor import _disturbed_spec
    from tests.test_gridworld import fixture_spec

    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False


REPO_ROOT = Path(__file__).resolve().parents[1]
AMENDMENT_PATH = (
    REPO_ROOT
    / "configs"
    / "protocols"
    / "protocol-v2-t526-recovery-phase-b-v0.1.json"
)
ORIGINAL_PLAN_PATH = (
    REPO_ROOT / "configs" / "protocols" / "protocol-v2-feasibility-v0.1.json"
)


class T526RecoveryContractTests(unittest.TestCase):
    def test_original_bundle_is_byte_exact_and_phase_a_sources_are_compatible(self):
        amendment = load_amendment(AMENDMENT_PATH)
        self.assertEqual(
            verify_original_bundle(repo_root=REPO_ROOT, amendment=amendment),
            amendment["original_phase_a"]["evidence_file_sha256"],
        )
        self.assertGreater(
            len(verify_source_compatibility(repo_root=REPO_ROOT, amendment=amendment)),
            10,
        )

    def test_amendment_freezes_level_candidates_lifecycle_and_final_reserve_firewall(self):
        amendment = load_amendment(AMENDMENT_PATH)
        self.assertFalse(amendment["final_reserve_access"])
        self.assertEqual(amendment["original_phase_a"]["selected_level_id"], "gw-l1")
        self.assertEqual(len(amendment["phase_b"]["conditions"]), 8)
        self.assertEqual(
            amendment["phase_b"]["common_nominal_no_learning_prefix_interactions"],
            1,
        )
        self.assertEqual(
            amendment["phase_b"]["post_boundary_interactions_per_branch"], 10
        )
        self.assertFalse(amendment["phase_b"]["episode_resets"])
        self.assertEqual(amendment["phase_b"]["expected_matched_sets"], 240)

    def test_both_selected_layouts_prove_no_reset_segment_is_shorter_than_path(self):
        plan = load_plan(ORIGINAL_PLAN_PATH)
        level = next(
            item for item in plan["ordered_gridworld_ladder"] if item["level_id"] == "gw-l1"
        )
        self.assertEqual([layout["shortest_path_length"] for layout in level["layouts"]], [12, 12])
        for layout in level["layouts"]:
            resolved = ResolvedGridWorldScenario.from_spec(_scenario(plan, layout))
            self.assertEqual(resolved.max_steps, 48)
            self.assertLess(1 + 10, int(layout["shortest_path_length"]))

    def test_exact_row_matching_fails_checkpoint_and_learner_mismatches(self):
        expected = {
            "checkpoint_sha256": "checkpoint",
            "learner_state_sha256": "learner",
            "probes": [{"interaction_index": 0, "metrics": {"x": 1.0}}],
        }
        exact = compare_reconstruction_row(
            authoritative=expected,
            reconstructed=dict(expected),
            fields=tuple(expected),
        )
        self.assertTrue(exact["exact_match"])
        for field in ("checkpoint_sha256", "learner_state_sha256"):
            changed = dict(expected)
            changed[field] = "mismatch"
            comparison = compare_reconstruction_row(
                authoritative=expected,
                reconstructed=changed,
                fields=tuple(expected),
            )
            self.assertFalse(comparison["exact_match"])
            self.assertEqual(set(comparison["mismatches"]), {field})

    def test_recovery_barrier_cannot_be_bypassed_by_partial_matches(self):
        for manifest in (
            {"status": "complete-barrier-passed", "exact_matches": 29},
            {"status": "failed-barrier-blocks-phase-b", "exact_matches": 30},
        ):
            with self.assertRaisesRegex(RuntimeError, "30/30"):
                require_complete_recovery_barrier(manifest)
        require_complete_recovery_barrier(
            {"status": "complete-barrier-passed", "exact_matches": 30}
        )

    def test_checkpoint_file_serialization_has_deterministic_identity(self):
        value = {"z": [2, 1], "a": {"state": "exact"}}
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.json"
            second = Path(directory) / "second.json"
            _write_json(first, value)
            _write_json(second, value)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(_file_sha256(first), _file_sha256(second))

    def test_retained_physical_recovery_attempt_validates_when_present(self):
        amendment = load_amendment(AMENDMENT_PATH)
        attempt = REPO_ROOT / amendment["recovery"]["output_directory"]
        if not attempt.exists():
            self.skipTest("physical recovery evidence is not present in this checkout")
        result = validate_recovery_attempt_evidence(
            repo_root=REPO_ROOT, amendment=amendment
        )
        self.assertIn(result["status"], {"valid-complete", "valid-failed-barrier"})

    def test_candidate_or_level_mutation_is_rejected(self):
        value = json.loads(AMENDMENT_PATH.read_text(encoding="utf-8"))
        value["phase_b"]["conditions"][2]["specification"]["probability"] = 0.07
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "candidate"):
                load_amendment(path)


@unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
class T526PPOPartialLifecycleTests(unittest.TestCase):
    @staticmethod
    def _episode_seeds(count: int = 24):
        return tuple(
            EnvironmentSeeds(
                scenario=1000 + index,
                environment=2000 + index,
                action_disturbance=3000 + index,
                observation_disturbance=4000 + index,
            )
            for index in range(count)
        )

    def _scenarios(self):
        base = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=30,
            include_change=False,
        )
        grid = {
            "grid": {
                "width": 10,
                "height": 10,
                "start": [0, 0],
                "goal": [9, 9],
                "obstacles": [],
            }
        }
        nominal = replace(base, scenario_id="t526-test-nominal", initial_state_spec=grid)
        disturbed = _disturbed_spec(
            nominal=nominal,
            condition={
                "condition_id": "test-swap",
                "family": "action-remap",
                "specification": {
                    "mapping": {
                        "up": "up",
                        "right": "down",
                        "down": "right",
                        "left": "left",
                    }
                },
            },
            onset_step=1,
        )
        return nominal, disturbed

    def _adapter(self):
        nominal, _ = self._scenarios()
        environment = ExplicitSeededGridWorldEnv(
            scenario=nominal, episode_seeds=self._episode_seeds()
        )
        model = PPO(
            "MlpPolicy",
            environment,
            learning_rate=1e-3,
            n_steps=16,
            batch_size=8,
            n_epochs=1,
            gamma=0.9,
            policy_kwargs={"net_arch": {"pi": [8], "vf": [8]}},
            seed=201,
            device="cpu",
            verbose=0,
        )
        adapter = ppo_state_adapter(
            model,
            configuration={
                "learning_rate": 1e-3,
                "n_steps": 16,
                "batch_size": 8,
                "n_epochs": 1,
                "discount_factor": 0.9,
                "net_arch": {"pi": [8], "vf": [8]},
                "seed": 201,
            },
            environment_factory=lambda: ExplicitSeededGridWorldEnv(
                scenario=nominal, episode_seeds=self._episode_seeds()
            ),
        )
        adapter.learn_to_total_interactions(16)
        attached = adapter.model.get_env()
        if attached is not None:
            attached.close()
        # Loading a legal checkpoint is the same detached state consumed by T-526.
        state = adapter.export_state()
        detached = adapter.clone()
        detached.restore_state(state)
        return detached

    def test_partial_ppo_starts_adaptive_collection_at_one_without_early_update(self):
        nominal, disturbed = self._scenarios()
        source = GridWorldEnvironment(nominal)
        source.reset(seeds=EnvironmentSeeds(1, 2, 3, 4))
        source.step(GridAction.RIGHT)
        branch_point = GridWorldScientificStateAdapter(source)
        learner = self._adapter()
        self.assertIsNone(learner.model.get_env())
        execution = execute_phase_b(
            learner=T526PPOTransientStateAdapter(learner),
            shared_environment=branch_point,
            nominal_spec=nominal,
            disturbed_spec=disturbed,
            interaction_budget_per_branch=3,
            driver_factory=lambda branch, adaptive, branch_learner, environment: (
                t526_branch_driver(
                    branch=branch,
                    adaptive=adaptive,
                    learner=branch_learner,
                    environment=environment,
                )
            ),
        )
        results = {item.branch: item for item in execution.results}
        self.assertEqual(set(results), set(ProtocolV2Branch))
        for result in results.values():
            self.assertEqual(result.interactions, 3)
            self.assertEqual(result.metrics["diagnostic_interactions"], 3.0)
        for branch in (
            ProtocolV2Branch.ADAPTIVE_NOMINAL,
            ProtocolV2Branch.ADAPTIVE_DISTURBED,
        ):
            metrics = results[branch].metrics
            self.assertEqual(metrics["adaptive_collection_started_at_interaction"], 1.0)
            self.assertEqual(metrics["optimizer_updates_during_branch"], 0.0)
            self.assertEqual(metrics["partial_rollout_interactions"], 3.0)
        source.close()


if __name__ == "__main__":
    unittest.main()
