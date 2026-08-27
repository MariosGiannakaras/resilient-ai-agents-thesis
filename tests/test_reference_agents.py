from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import AgentTransition  # noqa: E402
from resilient_agents.reference_agents import (  # noqa: E402
    RandomReferenceAgent,
    RandomReferenceConfig,
)


class RandomReferenceAgentTests(unittest.TestCase):
    def test_reference_is_deterministic_and_explicitly_not_ranked(self) -> None:
        def actions() -> tuple[list[int], dict[str, object]]:
            agent = RandomReferenceAgent(
                RandomReferenceConfig(agent_id="random-reference", actions=(0, 1, 2, 3))
            )
            agent.reset(initialization_seed=1, exploration_seed=99)
            sequence: list[int] = []
            for step in range(5):
                action = agent.act([step, 0])
                sequence.append(action)
                agent.observe(
                    AgentTransition(
                        step=step,
                        observation=[step + 1, 0],
                        intended_action=action,
                        reward=-1.0,
                        terminated=step == 4,
                        truncated=False,
                        optional_information={},
                    )
                )
            agent.end_episode({})
            return sequence, dict(agent.get_state())

        first_actions, first_state = actions()
        second_actions, second_state = actions()
        self.assertEqual(first_actions, second_actions)
        self.assertEqual(first_state, second_state)
        self.assertEqual(first_state["classification"], "reference-only-not-ranked")

    def test_reference_rejects_hidden_evaluator_information(self) -> None:
        agent = RandomReferenceAgent(
            RandomReferenceConfig(agent_id="random-reference", actions=(0, 1))
        )
        agent.reset(initialization_seed=1, exploration_seed=2)
        action = agent.act("s0")
        with self.assertRaises(ValueError):
            agent.observe(
                AgentTransition(
                    step=0,
                    observation="s1",
                    intended_action=action,
                    reward=0.0,
                    terminated=False,
                    truncated=False,
                    optional_information={"true_state": "hidden"},
                )
            )


if __name__ == "__main__":
    unittest.main()
