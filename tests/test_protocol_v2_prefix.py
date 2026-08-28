from __future__ import annotations

import unittest

from resilient_agents.agents import TabularQLearningAgent, TabularQLearningConfig
from resilient_agents.contracts import project_for_agent
from resilient_agents.gridworld import ACTION_NAMES, GridAction, GridWorldEnvironment
from resilient_agents.protocol_v2 import TabularQScientificStateAdapter, sarsa_state_adapter
from resilient_agents.protocol_v2_prefix import prepare_shared_no_learning_prefix
from resilient_agents.sarsa import SarsaAgent, SarsaConfig
from tests.test_gridworld import fixture_seeds, fixture_spec


class ProtocolV2SharedPrefixTests(unittest.TestCase):
    def _nominal(self):
        return fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=20,
            include_change=False,
        )

    def test_q_prefix_advances_behavior_state_without_learning(self):
        agent = TabularQLearningAgent(
            TabularQLearningConfig(
                agent_id="prefix-q",
                actions=ACTION_NAMES,
                learning_rate=0.2,
                discount_factor=0.9,
                exploration_epsilon=0.2,
                learning_enabled=True,
                bootstrap_on_truncation=True,
                initial_q_value=0.0,
            ),
            checkpoint=None,
        )
        agent.reset(initialization_seed=11, exploration_seed=12)
        adapter = TabularQScientificStateAdapter(agent)
        checkpoint_before = agent.checkpoint()
        digest_before = adapter.state_sha256()

        prefix = prepare_shared_no_learning_prefix(
            learner=adapter,
            nominal_spec=self._nominal(),
            environment_seeds=fixture_seeds(),
            interactions=1,
        )
        try:
            self.assertEqual(agent.checkpoint(), checkpoint_before)
            self.assertNotEqual(adapter.state_sha256(), digest_before)
            self.assertEqual(prefix.interactions, 1)
            self.assertEqual(prefix.environment.environment.gym_env._step, 1)
            self.assertIsNotNone(prefix.environment.environment.gym_env.last_transition)
        finally:
            prefix.environment.environment.close()

    def test_sarsa_prefix_rejects_unresolved_phase_a_backup(self):
        scenario = self._nominal()
        environment = GridWorldEnvironment(scenario)
        try:
            observation = environment.reset(seeds=fixture_seeds())
            agent = SarsaAgent(
                SarsaConfig(
                    agent_id="prefix-sarsa",
                    actions=ACTION_NAMES,
                    learning_rate=0.2,
                    discount_factor=0.9,
                    exploration_epsilon=0.1,
                    bootstrap_on_truncation=True,
                    initial_q_value=0.0,
                ),
                checkpoint=None,
            )
            agent.reset(initialization_seed=21, exploration_seed=22)
            action_name = agent.act(observation)
            truth = environment.step(int(GridAction[str(action_name).upper()]))
            agent.observe(project_for_agent(truth, environment.information_policy))
            self.assertIsNotNone(agent.get_state()["deferred_update"])
            adapter = sarsa_state_adapter(agent)

            with self.assertRaisesRegex(ValueError, "quiescent project learner"):
                prepare_shared_no_learning_prefix(
                    learner=adapter,
                    nominal_spec=scenario,
                    environment_seeds=fixture_seeds(),
                    interactions=1,
                )
        finally:
            environment.close()

    def test_prefix_fails_closed_when_branch_point_would_be_after_episode_end(self):
        scenario = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=1,
            include_change=False,
        )
        agent = TabularQLearningAgent(
            TabularQLearningConfig(
                agent_id="prefix-end",
                actions=ACTION_NAMES,
                learning_rate=0.2,
                discount_factor=0.9,
                exploration_epsilon=0.0,
                learning_enabled=True,
                bootstrap_on_truncation=True,
                initial_q_value=0.0,
            ),
            checkpoint=None,
        )
        agent.reset(initialization_seed=31, exploration_seed=32)
        adapter = TabularQScientificStateAdapter(agent)
        with self.assertRaisesRegex(RuntimeError, "multi-episode prefix semantics"):
            prepare_shared_no_learning_prefix(
                learner=adapter,
                nominal_spec=scenario,
                environment_seeds=fixture_seeds(),
                interactions=1,
            )


if __name__ == "__main__":
    unittest.main()
