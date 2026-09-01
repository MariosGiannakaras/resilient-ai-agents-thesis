from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import AgentTransition  # noqa: E402
from resilient_agents.dyna_deployment import DynaQPlusDeploymentAgent  # noqa: E402
from resilient_agents.dyna_q_plus import DynaQPlusConfig  # noqa: E402


def config() -> DynaQPlusConfig:
    return DynaQPlusConfig(
        agent_id="d0",
        actions=(0, 1),
        learning_rate=0.5,
        discount_factor=0.9,
        exploration_epsilon=0.0,
        planning_steps=3,
        kappa=0.01,
        bootstrap_on_truncation=False,
        initial_q_value=0.0,
    )


def observe_once(
    agent: DynaQPlusDeploymentAgent,
    *,
    step: int,
    state: str,
    next_state: str,
    reward: float,
) -> None:
    action = agent.act(state)
    agent.observe(
        AgentTransition(
            step=step,
            observation=next_state,
            intended_action=action,
            reward=reward,
            terminated=False,
            truncated=False,
            optional_information={},
        )
    )


class DynaQPlusDeploymentTests(unittest.TestCase):
    def test_next_episode_preserves_learning_and_restarts_step_guard(self) -> None:
        agent = DynaQPlusDeploymentAgent(config(), checkpoint=None)
        agent.start_branch(initialization_seed=11, exploration_seed=22)
        observe_once(agent, step=0, state="s0", next_state="s1", reward=2.0)
        before = copy.deepcopy(dict(agent.get_state()))
        self.assertEqual(agent.deployment_episode_count, 1)
        self.assertGreater(before["observed_transition_count"], 0)
        self.assertGreater(before["planning_update_count"], 0)
        self.assertTrue(before["model"])

        agent.start_next_episode(initialization_seed=33, exploration_seed=44)
        after_boundary = dict(agent.get_state())
        self.assertEqual(agent.deployment_episode_count, 2)
        self.assertEqual(after_boundary["checkpoint"], before["checkpoint"])
        self.assertEqual(after_boundary["model"], before["model"])
        self.assertEqual(after_boundary["time"], before["time"])
        self.assertEqual(
            after_boundary["observed_transition_count"],
            before["observed_transition_count"],
        )
        self.assertEqual(
            after_boundary["planning_update_count"], before["planning_update_count"]
        )
        self.assertEqual(after_boundary["initialization_seed"], 33)
        self.assertEqual(after_boundary["exploration_seed"], 44)
        self.assertIsNone(after_boundary["last_step"])

        # Environment step numbering restarts at zero in the new episode and
        # must be accepted without erasing the learned Dyna state.
        observe_once(agent, step=0, state="s1", next_state="s2", reward=-1.0)
        self.assertEqual(agent.get_state()["observed_transition_count"], 2)
        self.assertGreater(agent.get_state()["time"], before["time"])

    def test_episode_reseed_is_deterministic_for_equal_learned_state(self) -> None:
        left = DynaQPlusDeploymentAgent(config(), checkpoint=None)
        right = DynaQPlusDeploymentAgent(config(), checkpoint=None)
        for agent in (left, right):
            agent.start_branch(initialization_seed=101, exploration_seed=202)
            observe_once(agent, step=0, state="s0", next_state="s1", reward=1.0)
            agent.start_next_episode(initialization_seed=303, exploration_seed=404)

        self.assertEqual(left.get_state(), right.get_state())
        self.assertEqual(left.act("s1"), right.act("s1"))

    def test_new_branch_clears_prior_dyna_learning(self) -> None:
        agent = DynaQPlusDeploymentAgent(config(), checkpoint=None)
        agent.start_branch(initialization_seed=1, exploration_seed=2)
        observe_once(agent, step=0, state="s0", next_state="s1", reward=5.0)
        self.assertTrue(agent.get_state()["model"])
        self.assertTrue(agent.checkpoint()["q_values"])

        agent.start_branch(initialization_seed=3, exploration_seed=4)
        state = agent.get_state()
        self.assertEqual(agent.deployment_episode_count, 1)
        self.assertEqual(state["model"], [])
        self.assertEqual(state["time"], 0)
        self.assertEqual(state["observed_transition_count"], 0)
        self.assertEqual(agent.checkpoint()["q_values"], [])

    def test_cannot_cross_episode_with_unobserved_action(self) -> None:
        agent = DynaQPlusDeploymentAgent(config(), checkpoint=None)
        agent.start_branch(initialization_seed=1, exploration_seed=2)
        agent.act("s0")
        with self.assertRaises(RuntimeError):
            agent.start_next_episode(initialization_seed=3, exploration_seed=4)


if __name__ == "__main__":
    unittest.main()
