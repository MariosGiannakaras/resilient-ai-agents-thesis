from __future__ import annotations

import ast
import importlib.util
import json
import unittest
from pathlib import Path

from resilient_agents.agents import TabularQLearningAgent, TabularQLearningConfig
from resilient_agents.environment import EnvironmentSeeds
from resilient_agents.gridworld import ACTION_NAMES, GridAction, GridWorldEnvironment
from resilient_agents.protocol_v2 import (
    ProtocolV2Branch,
    TabularQScientificStateAdapter,
)
from resilient_agents.protocol_v2_gridworld import GridWorldScientificStateAdapter
from resilient_agents.protocol_v2_multi_episode import reset_gridworld_branch_episode
from resilient_agents.protocol_v2_t527 import (
    CORE_METHOD_IDS,
    _horizon_256_rule_passes,
    load_plan,
)
from resilient_agents.protocol_v2_t527_sizing_v02 import (
    EXPECTED_CONFIG_IDS,
    generate_final_layouts,
    generate_final_roots,
    load_retry_plan,
    validate_historical_authority,
)
from resilient_agents.protocol_v2_t527_sizing_v03 import (
    FRESH_METHODS,
    REUSED_METHODS,
    _validate_combined_identity_coverage,
    load_completion_plan,
    validate_historical_authority as validate_dec057_authority,
)
from resilient_agents.protocol_v2_tabular_phase_b import (
    ProjectTabularPhaseBBranchDriver,
)
from tests.test_gridworld import fixture_seeds, fixture_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = REPO_ROOT / "configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json"
RETRY_PLAN_PATH = REPO_ROOT / "configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json"
COMPLETION_PLAN_PATH = (
    REPO_ROOT / "configs/protocols/protocol-v2-t527-sizing-completion-v0.3.json"
)
_SB3_AVAILABLE = importlib.util.find_spec("stable_baselines3") is not None


class ProtocolV2T527ContractTests(unittest.TestCase):
    def test_no_active_project_gridworld_direct_sb3_ingress_bypasses_wrapper(self):
        allowed = {
            ("protocol_v2_feasibility.py", "adapter"),
            ("protocol_v2_sb3.py", "self.model"),
            ("protocol_v2_sb3_driver.py", "adapter"),
            ("protocol_v2_t526_phase_b.py", "self.inner"),
        }
        found = set()
        source_root = REPO_ROOT / "src/resilient_agents"
        for path in source_root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "predict"
                ):
                    continue
                owner = ast.unparse(node.func.value)
                key = (path.name, owner)
                found.add(key)
                self.assertIn(
                    key,
                    allowed,
                    f"unclassified direct SB3 predict ingress bypasses canonical wrapper: {path}:{node.lineno}",
                )
        self.assertEqual(found, allowed)

    def test_plan_freezes_equal_opportunity_and_no_final_reserve(self):
        plan = load_plan(PLAN_PATH)
        self.assertFalse(plan["final_reserve_access"])
        self.assertEqual(set(plan["candidate_configs"]), set(CORE_METHOD_IDS))
        self.assertTrue(all(len(value) == 6 for value in plan["candidate_configs"].values()))
        self.assertEqual(plan["tuning"]["training_interaction_budget"], 8192)
        self.assertEqual(
            plan["tuning"]["probe_interaction_indices"],
            [0, 512, 1024, 2048, 4096, 8192],
        )
        self.assertEqual(plan["sizing"]["root_count_candidates"], [12, 16, 20, 24])
        self.assertEqual(plan["sizing"]["phase_b_horizon_candidates"], [256, 512])
        self.assertNotIn("a2c", json.dumps(plan).lower())

    def test_dec057_plan_freezes_structural_composition_and_fresh_three_method_scope(self):
        plan = load_completion_plan(COMPLETION_PLAN_PATH)
        self.assertFalse(plan["final_reserve_access"])
        self.assertEqual(tuple(plan["execution_scope"]["fresh_methods"]), FRESH_METHODS)
        self.assertEqual(
            tuple(plan["execution_scope"]["reused_complete_methods"]),
            REUSED_METHODS,
        )
        self.assertEqual(plan["execution_scope"]["expected_fresh_phase_a_units"], 144)
        self.assertEqual(plan["execution_scope"]["expected_fresh_matched_sets"], 288)
        self.assertFalse(plan["execution_scope"]["reuse_incomplete_dqn_v02"])
        self.assertFalse(plan["execution_scope"]["reuse_any_sizing_v01"])
        self.assertFalse(
            plan["reuse_authority"]["performance_values_permitted_for_reuse_decision"]
        )

    @unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
    def test_dec057_structurally_accepts_only_complete_q_and_sarsa_v02_strata(self):
        plan = load_completion_plan(COMPLETION_PLAN_PATH)
        validation = validate_dec057_authority(repo_root=REPO_ROOT, plan=plan)
        self.assertEqual(validation["status"], "valid-structural-composition-authority")
        self.assertFalse(validation["final_reserve_access"])
        self.assertFalse(validation["performance_values_used_for_reuse_decision"])
        self.assertEqual(set(validation["reusable_methods"]), set(REUSED_METHODS))
        for method in REUSED_METHODS:
            result = validation["reusable_methods"][method]
            self.assertEqual(result["status"], "structurally-accepted")
            self.assertEqual(result["phase_a_units"], 48)
            self.assertEqual(result["matched_sets"], 96)
            self.assertFalse(result["performance_values_used_for_decision"])
        self.assertEqual(validation["excluded_sources"]["sizing_v02_dqn_rows"], "all")

    def test_dec057_combined_guard_rejects_incomplete_v02_dqn_reference(self):
        source_plan = load_retry_plan(RETRY_PLAN_PATH)
        retained = "results/pilots/protocol-v2-t527-sizing-v0.2"
        fresh = "results/pilots/protocol-v2-t527-sizing-v0.3"
        layouts = [item["layout_id"] for item in source_plan["development_layouts"]]
        conditions = [item["condition_id"] for item in source_plan["sizing"]["conditions"]]
        phase_a = []
        phase_b = []
        phase_a_index = []
        phase_b_index = []
        methods = tuple(REUSED_METHODS) + tuple(FRESH_METHODS)
        for method in methods:
            package = retained if method in REUSED_METHODS else fresh
            for index in range(1, 25):
                root = f"t527-size-r{index:02d}"
                for layout in layouts:
                    phase_a.append({"method_id": method, "root_id": root, "layout_id": layout})
                    phase_a_index.append({
                        "method_id": method,
                        "source_package": package,
                    })
                    for condition in conditions:
                        phase_b.append({
                            "method_id": method,
                            "root_id": root,
                            "layout_id": layout,
                            "condition_id": condition,
                        })
                        phase_b_index.append({
                            "method_id": method,
                            "source_package": package,
                        })
        _validate_combined_identity_coverage(
            source_plan=source_plan,
            phase_a=phase_a,
            phase_b=phase_b,
            phase_a_index=phase_a_index,
            phase_b_index=phase_b_index,
            retained_package=retained,
        )
        dqn_entry = next(item for item in phase_a_index if item["method_id"] == "dqn")
        dqn_entry["source_package"] = retained
        with self.assertRaisesRegex(RuntimeError, "incomplete v0.2 method"):
            _validate_combined_identity_coverage(
                source_plan=source_plan,
                phase_a=phase_a,
                phase_b=phase_b,
                phase_a_index=phase_a_index,
                phase_b_index=phase_b_index,
                retained_package=retained,
            )

    @unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
    def test_dec056_validates_retained_tuning_and_failed_sizing_without_final_access(self):
        plan = load_retry_plan(RETRY_PLAN_PATH)
        validation = validate_historical_authority(repo_root=REPO_ROOT, plan=plan)
        self.assertFalse(validation["final_reserve_access"])
        self.assertEqual(validation["tuning_v01"]["status"], "valid-complete")
        self.assertEqual(validation["tuning_v01"]["units"], 180)
        self.assertEqual(validation["sizing_v01"]["status"], "valid-failed")
        self.assertEqual(validation["sizing_v01"]["phase_a_units"], 97)
        self.assertEqual(
            {method: value["config_id"] for method, value in plan["selected_configs"].items()},
            EXPECTED_CONFIG_IDS,
        )

    def test_horizon_rule_requires_native_opportunities_even_when_episodes_pass(self):
        row = {
            "horizons": {
                "256": [
                    {
                        "branch": branch,
                        "metrics": {
                            "episodes_completed": 3.0,
                            "native_update_opportunities_completed": 1.0 if branch == "AN" else 3.0,
                        },
                    }
                    for branch in ("FN", "FD", "AN", "AD")
                ]
            }
        }
        self.assertFalse(_horizon_256_rule_passes([row]))
        row["horizons"]["256"][2]["metrics"]["native_update_opportunities_completed"] = 2.0
        self.assertTrue(_horizon_256_rule_passes([row]))

    def test_final_layout_and_root_generation_is_deterministic_and_execution_free(self):
        plan = load_retry_plan(RETRY_PLAN_PATH)
        first = generate_final_layouts(plan)
        self.assertEqual(first, generate_final_layouts(plan))
        self.assertEqual(len(first), 2)
        self.assertTrue(all(item["shortest_path_length"] == 12 for item in first))
        roots = generate_final_roots(plan, 12)
        self.assertEqual(len(roots), 12)
        self.assertEqual(roots[0]["root_id"], "t527-final-r01")
        self.assertTrue(all(root["initialization_seed"] > 70000 for root in roots))

    def test_persistent_action_remap_is_active_from_later_episode_start(self):
        disturbed = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=3,
            include_change=True,
        )
        source = GridWorldEnvironment(disturbed)
        source.reset(seeds=fixture_seeds())
        source.step(GridAction.RIGHT)
        source.step(GridAction.RIGHT)
        source.step(GridAction.RIGHT)
        branch = GridWorldScientificStateAdapter(source)
        observation = reset_gridworld_branch_episode(
            branch,
            seeds=EnvironmentSeeds(101, 102, 103, 104),
        )
        self.assertEqual(
            observation,
            tuple(branch.environment.gym_env.spec.initial_state_spec["grid"]["start"]),
        )
        transition = branch.environment.step(GridAction.RIGHT)
        self.assertEqual(transition.executed_action, "down")
        self.assertTrue(transition.change_event_ids)
        branch.environment.close()

    def test_tabular_multi_episode_keeps_learning_state_and_global_clock(self):
        nominal = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=2,
            include_change=False,
        )
        source = GridWorldEnvironment(nominal)
        source.reset(seeds=fixture_seeds())
        source.step(GridAction.RIGHT)
        branch = GridWorldScientificStateAdapter(source)
        config = TabularQLearningConfig(
            agent_id="t527-multi-episode",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.95,
            exploration_epsilon=0.0,
            learning_enabled=True,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        agent = TabularQLearningAgent(config, checkpoint=None)
        agent.reset(initialization_seed=1, exploration_seed=2)
        learner = TabularQScientificStateAdapter(agent)
        driver = ProjectTabularPhaseBBranchDriver(
            branch=ProtocolV2Branch.ADAPTIVE_NOMINAL,
            adaptive=True,
            learner=learner,
            environment=branch,
            subsequent_episode_seeds=(
                EnvironmentSeeds(11, 12, 13, 14),
                EnvironmentSeeds(21, 22, 23, 24),
                EnvironmentSeeds(31, 32, 33, 34),
            ),
        )
        metrics = driver.run_to_interaction(5)
        state = learner.export_state()
        self.assertEqual(driver.interactions, 5)
        self.assertEqual(state["observed_transition_count"], 5)
        self.assertEqual(state["last_step"], 4)
        self.assertGreaterEqual(metrics["episodes_started"], 2.0)
        self.assertGreaterEqual(metrics["episodes_completed"], 2.0)
        branch.environment.close()


if __name__ == "__main__":
    unittest.main()
