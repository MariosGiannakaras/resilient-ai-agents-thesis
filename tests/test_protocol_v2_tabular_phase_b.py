from __future__ import annotations

import unittest

from resilient_agents.agents import TabularQLearningAgent, TabularQLearningConfig
from resilient_agents.dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig
from resilient_agents.gridworld import ACTION_NAMES, GridAction, GridWorldEnvironment
from resilient_agents.protocol_v2 import (
    ProtocolV2Branch,
    TabularQScientificStateAdapter,
    dyna_q_plus_state_adapter,
    sarsa_state_adapter,
)
from resilient_agents.protocol_v2_executor import execute_phase_b
from resilient_agents.protocol_v2_gridworld import GridWorldScientificStateAdapter
from resilient_agents.protocol_v2_tabular_phase_b import (
    ProjectTabularPhaseBBranchDriver,
)
from resilient_agents.sarsa import SarsaAgent, SarsaConfig
from tests.test_gridworld import fixture_seeds, fixture_spec


class ProtocolV2TabularPhaseBTests(unittest.TestCase):
    def _specs(self):
        nominal = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=False,
        )
        disturbed = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=True,
        )
        return nominal, disturbed

    def _branch_point(self):
        nominal, disturbed = self._specs()
        source = GridWorldEnvironment(nominal)
        source.reset(seeds=fixture_seeds(action=51, observation=61))
        source.step(GridAction.RIGHT)
        source.step(GridAction.RIGHT)
        return source, GridWorldScientificStateAdapter(source), nominal, disturbed

    def _q_adapter(self):
        config = TabularQLearningConfig(
            agent_id="q-phase-b",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.9,
            exploration_epsilon=0.0,
            learning_enabled=True,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        checkpoint = {
            "schema_version": 1,
            "actions": list(ACTION_NAMES),
            "initial_q_value": 0.0,
            "q_values": [
                {"state": [2, 1], "action": "right", "value": 10.0},
            ],
        }
        agent = TabularQLearningAgent(config, checkpoint=checkpoint)
        agent.reset(initialization_seed=71, exploration_seed=72)
        return TabularQScientificStateAdapter(agent)

    def test_frozen_q_preserves_q_values_while_inference_state_advances(self):
        source, branch_point, nominal, _ = self._branch_point()
        learner = self._q_adapter()
        before = learner.export_state()
        environment = branch_point.fork_into(nominal)
        driver = ProjectTabularPhaseBBranchDriver(
            branch=ProtocolV2Branch.FROZEN_NOMINAL,
            adaptive=False,
            learner=learner,
            environment=environment,
        )
        driver.run_to_interaction(1)
        after = learner.export_state()
        self.assertEqual(after["checkpoint"], before["checkpoint"])
        self.assertEqual(
            after["observed_transition_count"],
            before["observed_transition_count"] + 1,
        )
        self.assertNotEqual(after["exploration_rng_state"], before["exploration_rng_state"])
        source.close()
        environment.environment.close()

    def test_frozen_dyna_does_not_create_model_or_recency_state(self):
        source, branch_point, nominal, _ = self._branch_point()
        config = DynaQPlusConfig(
            agent_id="dyna-phase-b",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.9,
            exploration_epsilon=0.0,
            planning_steps=2,
            kappa=0.001,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        agent = DynaQPlusAgent(config, checkpoint=None)
        agent.reset(initialization_seed=81, exploration_seed=82)
        learner = dyna_q_plus_state_adapter(agent)
        before = learner.export_state()
        environment = branch_point.fork_into(nominal)
        driver = ProjectTabularPhaseBBranchDriver(
            branch=ProtocolV2Branch.FROZEN_NOMINAL,
            adaptive=False,
            learner=learner,
            environment=environment,
        )
        driver.run_to_interaction(1)
        after = learner.export_state()
        for key in (
            "checkpoint",
            "model",
            "time",
            "planning_update_count",
            "planning_rng_state",
        ):
            self.assertEqual(after[key], before[key])
        source.close()
        environment.environment.close()

    def test_sarsa_branch_rejects_unresolved_behavior_or_deferred_state(self):
        source, branch_point, nominal, _ = self._branch_point()
        config = SarsaConfig(
            agent_id="sarsa-phase-b",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.9,
            exploration_epsilon=0.0,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        agent = SarsaAgent(config, checkpoint=None)
        agent.reset(initialization_seed=91, exploration_seed=92)
        agent.act((2, 1))
        learner = sarsa_state_adapter(agent)
        environment = branch_point.fork_into(nominal)
        with self.assertRaisesRegex(ValueError, "quiescent learner fork"):
            ProjectTabularPhaseBBranchDriver(
                branch=ProtocolV2Branch.FROZEN_NOMINAL,
                adaptive=False,
                learner=learner,
                environment=environment,
            )
        source.close()
        environment.environment.close()

    def test_four_branch_executor_preserves_factor_assignment_and_disturbed_dynamics(self):
        source, branch_point, nominal, disturbed = self._branch_point()
        execution = execute_phase_b(
            learner=self._q_adapter(),
            shared_environment=branch_point,
            nominal_spec=nominal,
            disturbed_spec=disturbed,
            interaction_budget_per_branch=1,
            driver_factory=lambda branch, adaptive, learner, environment: (
                ProjectTabularPhaseBBranchDriver(
                    branch=branch,
                    adaptive=adaptive,
                    learner=learner,
                    environment=environment,
                )
            ),
        )
        results = {item.branch: item for item in execution.results}
        self.assertEqual(set(results), set(ProtocolV2Branch))
        self.assertEqual(results[ProtocolV2Branch.FROZEN_NOMINAL].metrics["adaptive"], 0.0)
        self.assertEqual(results[ProtocolV2Branch.FROZEN_DISTURBED].metrics["adaptive"], 0.0)
        self.assertEqual(results[ProtocolV2Branch.ADAPTIVE_NOMINAL].metrics["adaptive"], 1.0)
        self.assertEqual(results[ProtocolV2Branch.ADAPTIVE_DISTURBED].metrics["adaptive"], 1.0)
        self.assertNotEqual(
            results[ProtocolV2Branch.FROZEN_NOMINAL].final_environment_state_sha256,
            results[ProtocolV2Branch.FROZEN_DISTURBED].final_environment_state_sha256,
        )
        self.assertNotEqual(
            results[ProtocolV2Branch.ADAPTIVE_NOMINAL].final_environment_state_sha256,
            results[ProtocolV2Branch.ADAPTIVE_DISTURBED].final_environment_state_sha256,
        )
        source.close()

    def test_branch_without_delivered_prefix_fails_closed(self):
        nominal, _ = self._specs()
        source = GridWorldEnvironment(nominal)
        source.reset(seeds=fixture_seeds())
        environment = GridWorldScientificStateAdapter(source)
        driver = ProjectTabularPhaseBBranchDriver(
            branch=ProtocolV2Branch.FROZEN_NOMINAL,
            adaptive=False,
            learner=self._q_adapter(),
            environment=environment,
        )
        with self.assertRaisesRegex(RuntimeError, "delivered pre-change prefix observation"):
            driver.run_to_interaction(1)
        source.close()


if __name__ == "__main__":
    unittest.main()
