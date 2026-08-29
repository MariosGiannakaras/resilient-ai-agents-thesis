from __future__ import annotations

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
from resilient_agents.protocol_v2_gridworld import (
    GridWorldScientificStateAdapter,
    reset_gridworld_branch_episode,
)
from resilient_agents.protocol_v2_t527 import CORE_METHOD_IDS, load_plan
from resilient_agents.protocol_v2_tabular_phase_b import (
    ProjectTabularPhaseBBranchDriver,
)
from tests.test_gridworld import fixture_seeds, fixture_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = REPO_ROOT / "configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json"


class ProtocolV2T527ContractTests(unittest.TestCase):
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
