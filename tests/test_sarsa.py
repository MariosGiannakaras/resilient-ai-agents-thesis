from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import Agent, AgentTransition  # noqa: E402
from resilient_agents.sarsa import SarsaAgent, SarsaConfig  # noqa: E402
from resilient_agents.sarsa_deployment import SarsaDeploymentAgent  # noqa: E402


def config(*, epsilon: float = 0.0) -> SarsaConfig:
    return SarsaConfig(
        agent_id="s0",
        actions=(0, 1),
        learning_rate=0.5,
        discount_factor=0.9,
        exploration_epsilon=epsilon,
        bootstrap_on_truncation=False,
        initial_q_value=0.0,
    )


def transition(
    *, step: int, observation: object, action: object, reward: float,
    terminated: bool = False, truncated: bool = False,
    optional_information: dict[str, object] | None = None,
) -> AgentTransition:
    return AgentTransition(
        step=step,
        observation=observation,
        intended_action=action,
        reward=reward,
        terminated=terminated,
        truncated=truncated,
        optional_information=optional_information or {},
    )


class SarsaAgentTests(unittest.TestCase):
    def test_on_policy_backup_waits_for_next_selected_action(self) -> None:
        checkpoint = {
            "schema_version": 1,
            "actions": [0, 1],
            "initial_q_value": 0.0,
            "q_values": [
                {"state": "s1", "action": 0, "value": 0.5},
                {"state": "s1", "action": 1, "value": 2.0},
            ],
        }
        agent = SarsaAgent(config(), checkpoint=checkpoint)
        agent.reset(initialization_seed=1, exploration_seed=2)
        first_action = agent.act("s0")
        agent.observe(
            transition(
                step=0,
                observation="s1",
                action=first_action,
                reward=1.0,
            )
        )
        before_next_action = {
            (row["state"], row["action"]): row["value"]
            for row in agent.checkpoint()["q_values"]
        }
        self.assertNotIn(("s0", first_action), before_next_action)

        next_action = agent.act("s1")
        self.assertEqual(next_action, 1)
        after = {
            (row["state"], row["action"]): row["value"]
            for row in agent.checkpoint()["q_values"]
        }
        # 0 + 0.5 * (1 + 0.9 * Q(s1,1=2) - 0) = 1.4
        self.assertAlmostEqual(after[("s0", first_action)], 1.4)

    def test_terminal_backup_is_immediate_and_exact(self) -> None:
        agent = SarsaAgent(config(), checkpoint=None)
        agent.reset(initialization_seed=3, exploration_seed=4)
        action = agent.act("s0")
        agent.observe(
            transition(
                step=0,
                observation="goal",
                action=action,
                reward=2.0,
                terminated=True,
            )
        )
        learned = {
            (row["state"], row["action"]): row["value"]
            for row in agent.checkpoint()["q_values"]
        }
        self.assertEqual(learned[("s0", action)], 1.0)
        agent.end_episode({})

    def test_determinism_state_round_trip_and_agent_contract(self) -> None:
        cfg = config(epsilon=0.25)
        original = SarsaAgent(cfg, checkpoint=None)
        original.reset(initialization_seed=100, exploration_seed=200)
        action = original.act("s0")
        original.observe(
            transition(step=0, observation="s1", action=action, reward=-1.0)
        )
        serialized = copy.deepcopy(dict(original.get_state()))
        restored = SarsaAgent(cfg, checkpoint=None)
        restored.restore_state(serialized)
        self.assertEqual(original.state_sha256(), restored.state_sha256())
        self.assertEqual(original.act("s1"), restored.act("s1"))
        self.assertEqual(original.get_state(), restored.get_state())
        self.assertIsInstance(original, Agent)
        json.dumps(original.get_state(), allow_nan=False, sort_keys=True)

    def test_hidden_evaluator_information_fails_closed(self) -> None:
        agent = SarsaAgent(config(), checkpoint=None)
        agent.reset(initialization_seed=1, exploration_seed=2)
        action = agent.act("s0")
        with self.assertRaises(ValueError):
            agent.observe(
                transition(
                    step=0,
                    observation="s1",
                    action=action,
                    reward=0.0,
                    optional_information={"change_event_ids": ["hidden"]},
                )
            )

    def test_deployment_preserves_learning_but_resets_episode_step_guard(self) -> None:
        agent = SarsaDeploymentAgent(config(), checkpoint=None)
        agent.start_branch(initialization_seed=10, exploration_seed=11)
        action = agent.act("s0")
        agent.observe(
            transition(
                step=0, observation="goal", action=action, reward=2.0, terminated=True
            )
        )
        learned_sha = agent.checkpoint_sha256()
        agent.end_episode({})
        agent.start_next_episode(initialization_seed=12, exploration_seed=13)
        self.assertEqual(agent.checkpoint_sha256(), learned_sha)
        next_action = agent.act("s0")
        agent.observe(
            transition(
                step=0, observation="goal", action=next_action, reward=0.0, terminated=True
            )
        )
        self.assertEqual(agent.deployment_episode_count, 2)


if __name__ == "__main__":
    unittest.main()
