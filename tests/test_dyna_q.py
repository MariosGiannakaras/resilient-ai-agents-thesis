from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import Agent, AgentTransition  # noqa: E402
from resilient_agents.dyna_q import DynaQAgent, DynaQConfig  # noqa: E402
from resilient_agents.dyna_q_deployment import DynaQDeploymentAgent  # noqa: E402
from resilient_agents.dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig  # noqa: E402


def config(*, planning_steps: int = 4) -> DynaQConfig:
    return DynaQConfig(
        agent_id="dq0",
        actions=(0, 1),
        learning_rate=0.5,
        discount_factor=0.9,
        exploration_epsilon=0.0,
        planning_steps=planning_steps,
        bootstrap_on_truncation=False,
        initial_q_value=0.0,
    )


def transition(
    *, step: int, observation: object, action: object, reward: float,
    terminated: bool = False, optional_information: dict[str, object] | None = None,
) -> AgentTransition:
    return AgentTransition(
        step=step,
        observation=observation,
        intended_action=action,
        reward=reward,
        terminated=terminated,
        truncated=False,
        optional_information=optional_information or {},
    )


class DynaQAgentTests(unittest.TestCase):
    def test_plain_dyna_models_only_experienced_pairs(self) -> None:
        agent = DynaQAgent(config(planning_steps=0), checkpoint=None)
        agent.reset(initialization_seed=1, exploration_seed=2)
        action = agent.act("s0")
        self.assertEqual(agent.get_state()["model"], [])
        agent.observe(
            transition(step=0, observation="s1", action=action, reward=-1.0)
        )
        model = agent.get_state()["model"]
        self.assertEqual(len(model), 1)
        self.assertTrue(model[0]["experienced"])
        self.assertEqual(model[0]["state"], "s0")
        self.assertEqual(model[0]["action"], action)

    def test_dyna_q_plus_has_extra_untried_action_model_even_with_zero_kappa(self) -> None:
        plain = DynaQAgent(config(planning_steps=0), checkpoint=None)
        plus = DynaQPlusAgent(
            DynaQPlusConfig(
                agent_id="d0",
                actions=(0, 1),
                learning_rate=0.5,
                discount_factor=0.9,
                exploration_epsilon=0.0,
                planning_steps=0,
                kappa=0.0,
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=None,
        )
        plain.reset(initialization_seed=7, exploration_seed=8)
        plus.reset(initialization_seed=7, exploration_seed=8)
        plain.act("s0")
        plus.act("s0")
        self.assertEqual(len(plain.get_state()["model"]), 0)
        self.assertEqual(len(plus.get_state()["model"]), 2)

    def test_planning_budget_determinism_and_state_round_trip(self) -> None:
        def run() -> DynaQAgent:
            agent = DynaQAgent(config(planning_steps=5), checkpoint=None)
            agent.reset(initialization_seed=100, exploration_seed=200)
            for step in range(3):
                action = agent.act(f"s{step}")
                agent.observe(
                    transition(
                        step=step,
                        observation=f"s{step + 1}",
                        action=action,
                        reward=-1.0 if step < 2 else 0.0,
                        terminated=step == 2,
                    )
                )
            return agent

        first = run()
        second = run()
        self.assertEqual(first.get_state(), second.get_state())
        self.assertEqual(first.get_state()["planning_update_count"], 15)
        self.assertEqual(first.get_state()["method"], "dyna_q_v1")
        self.assertIsInstance(first, Agent)
        json.dumps(first.get_state(), allow_nan=False, sort_keys=True)

        restored = DynaQAgent(config(planning_steps=5), checkpoint=None)
        restored.restore_state(copy.deepcopy(dict(first.get_state())))
        self.assertEqual(first.state_sha256(), restored.state_sha256())

    def test_hidden_evaluator_information_fails_closed(self) -> None:
        agent = DynaQAgent(config(), checkpoint=None)
        agent.reset(initialization_seed=1, exploration_seed=2)
        action = agent.act("s0")
        with self.assertRaises(ValueError):
            agent.observe(
                transition(
                    step=0,
                    observation="s1",
                    action=action,
                    reward=0.0,
                    optional_information={"true_state": [1, 1]},
                )
            )

    def test_deployment_preserves_learned_model_between_episodes(self) -> None:
        agent = DynaQDeploymentAgent(config(planning_steps=2), checkpoint=None)
        agent.start_branch(initialization_seed=10, exploration_seed=11)
        action = agent.act("s0")
        agent.observe(
            transition(
                step=0, observation="goal", action=action, reward=1.0, terminated=True
            )
        )
        agent.end_episode({})
        state_before = dict(agent.get_state())
        model_before = copy.deepcopy(state_before["model"])
        agent.start_next_episode(initialization_seed=12, exploration_seed=13)
        self.assertEqual(agent.get_state()["model"], model_before)
        self.assertEqual(agent.deployment_episode_count, 2)


if __name__ == "__main__":
    unittest.main()
