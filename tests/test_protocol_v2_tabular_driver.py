from __future__ import annotations

import unittest

from resilient_agents.agents import TabularQLearningAgent, TabularQLearningConfig
from resilient_agents.dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig
from resilient_agents.gridworld import ACTION_NAMES
from resilient_agents.protocol_v2 import (
    ProtocolV2TaskSemantics,
    TabularQScientificStateAdapter,
    dyna_q_plus_state_adapter,
    sarsa_state_adapter,
)
from resilient_agents.protocol_v2_executor import execute_phase_a
from resilient_agents.protocol_v2_runtime import (
    NoLearningProbePlan,
    PhaseARequest,
    ProtocolV2MethodConfig,
    ProtocolV2RootIdentity,
)
from resilient_agents.protocol_v2_tabular_driver import (
    PROJECT_IMPLEMENTATION_ID,
    ProjectTabularNoLearningProbeEvaluator,
    ProjectTabularPhaseADriver,
)
from resilient_agents.sarsa import SarsaAgent, SarsaConfig
from tests.test_gridworld import fixture_seeds, fixture_spec


class ProtocolV2ProjectDriverTests(unittest.TestCase):
    def _root(self):
        return ProtocolV2RootIdentity(
            root_id="root-project-driver",
            initialization_seed=1001,
            exploration_seed=1002,
            scenario_seed=1003,
            environment_seed=1004,
            action_disturbance_seed=1005,
            observation_disturbance_seed=1006,
        )

    def _scenario(self):
        return fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=5,
            include_change=False,
        )

    def _request(self, method_id, parameters):
        return PhaseARequest(
            protocol_version="protocol-v2.0-candidate",
            experiment_id=f"{method_id}-phase-a",
            layout_id="tiny-project-grid",
            root=self._root(),
            task=ProtocolV2TaskSemantics(
                gamma=0.9,
                reward_contract={"step": -0.1, "collision": -0.25, "goal": 1.0},
            ),
            method=ProtocolV2MethodConfig(
                method_id=method_id,
                implementation_id=PROJECT_IMPLEMENTATION_ID,
                parameters=parameters,
            ),
            training_interaction_budget=12,
            probe_plan=NoLearningProbePlan(
                interaction_indices=(0, 6, 12),
                episodes_per_probe=2,
            ),
        )

    def _probe(self):
        return ProjectTabularNoLearningProbeEvaluator(
            scenario=self._scenario(),
            environment_seeds=(fixture_seeds(action=31, observation=41), fixture_seeds(action=32, observation=42)),
        )

    def test_q_sarsa_and_dyna_keep_full_learner_state_across_episode_resets(self):
        q_config = TabularQLearningConfig(
            agent_id="q-learning-v2",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.9,
            exploration_epsilon=0.2,
            learning_enabled=True,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        q_agent = TabularQLearningAgent(q_config, checkpoint=None)

        sarsa_config = SarsaConfig(
            agent_id="sarsa-v2",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.9,
            exploration_epsilon=0.2,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        sarsa_agent = SarsaAgent(sarsa_config, checkpoint=None)

        dyna_config = DynaQPlusConfig(
            agent_id="dyna-q-plus-v2",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.9,
            exploration_epsilon=0.2,
            planning_steps=2,
            kappa=0.001,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        dyna_agent = DynaQPlusAgent(dyna_config, checkpoint=None)

        cases = (
            (
                "q_learning",
                TabularQScientificStateAdapter(q_agent),
                {
                    "discount_factor": 0.9,
                    "bootstrap_on_truncation": True,
                    "learning_rate": 0.2,
                },
            ),
            (
                "sarsa",
                sarsa_state_adapter(sarsa_agent),
                {
                    "discount_factor": 0.9,
                    "bootstrap_on_truncation": True,
                    "learning_rate": 0.2,
                },
            ),
            (
                "dyna_q_plus",
                dyna_q_plus_state_adapter(dyna_agent),
                {
                    "discount_factor": 0.9,
                    "bootstrap_on_truncation": True,
                    "learning_rate": 0.2,
                    "planning_steps": 2,
                    "kappa": 0.001,
                },
            ),
        )

        for method_id, adapter, parameters in cases:
            with self.subTest(method_id=method_id):
                driver = ProjectTabularPhaseADriver(
                    adapter=adapter,
                    scenario=self._scenario(),
                    root=self._root(),
                )
                execution = execute_phase_a(
                    self._request(method_id, parameters),
                    driver=driver,
                    probe_evaluator=self._probe(),
                    checkpoint_provenance={"test": "persistent-project-driver"},
                )
                state = execution.final_adapter.export_state()
                self.assertEqual(execution.result.ledger.training_interactions, 12)
                self.assertGreater(execution.result.ledger.probe_interactions, 0)
                self.assertEqual(state["observed_transition_count"], 12)
                self.assertIsNotNone(state["exploration_rng_state"])
                driver.close()

    def test_probe_is_deterministic_and_does_not_call_learning_observe(self):
        config = TabularQLearningConfig(
            agent_id="q-probe",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.9,
            exploration_epsilon=1.0,
            learning_enabled=True,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        agent = TabularQLearningAgent(config, checkpoint=None)
        adapter = TabularQScientificStateAdapter(agent)
        driver = ProjectTabularPhaseADriver(
            adapter=adapter,
            scenario=self._scenario(),
            root=self._root(),
        )
        driver.train_to_interaction(6)
        before = adapter.state_sha256()
        evaluator = self._probe()
        first = evaluator(adapter.clone(), training_interaction_index=6, episodes=2)
        second = evaluator(adapter.clone(), training_interaction_index=6, episodes=2)
        self.assertEqual(first, second)
        self.assertEqual(adapter.state_sha256(), before)
        driver.close()


if __name__ == "__main__":
    unittest.main()
