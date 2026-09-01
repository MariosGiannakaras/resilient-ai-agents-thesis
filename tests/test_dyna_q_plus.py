from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import Agent, AgentTransition  # noqa: E402
from resilient_agents.dyna_q_plus import (  # noqa: E402
    DynaQPlusAgent,
    DynaQPlusConfig,
)


def config(*, planning_steps: int = 4, kappa: float = 0.01) -> DynaQPlusConfig:
    return DynaQPlusConfig(
        agent_id="d0",
        actions=(0, 1),
        learning_rate=0.5,
        discount_factor=0.9,
        exploration_epsilon=0.0,
        planning_steps=planning_steps,
        kappa=kappa,
        bootstrap_on_truncation=False,
        initial_q_value=0.0,
    )


def transition(
    *,
    step: int,
    observation: object,
    action: object,
    reward: float,
    terminated: bool = False,
    truncated: bool = False,
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


class DynaQPlusAgentTests(unittest.TestCase):
    def test_real_q_update_matches_hand_computation_when_planning_disabled(self) -> None:
        agent = DynaQPlusAgent(config(planning_steps=0, kappa=0.0), checkpoint=None)
        agent.reset(initialization_seed=10, exploration_seed=11)
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
            (item["state"], item["action"]): item["value"]
            for item in agent.checkpoint()["q_values"]
        }
        self.assertEqual(learned[("s0", action)], 1.0)
        self.assertEqual(agent.get_state()["planning_update_count"], 0)

    def test_planning_is_deterministic_and_uses_explicit_budget(self) -> None:
        def replay() -> tuple[list[int], dict[str, object]]:
            agent = DynaQPlusAgent(config(planning_steps=5, kappa=0.02), checkpoint=None)
            agent.reset(initialization_seed=101, exploration_seed=202)
            actions: list[int] = []
            for step in range(4):
                action = agent.act([step, 0])
                actions.append(action)
                agent.observe(
                    transition(
                        step=step,
                        observation=[step + 1, 0],
                        action=action,
                        reward=-1.0 if step < 3 else 0.0,
                        terminated=step == 3,
                    )
                )
            return actions, dict(agent.get_state())

        actions_a, state_a = replay()
        actions_b, state_b = replay()
        self.assertEqual(actions_a, actions_b)
        self.assertEqual(state_a, state_b)
        self.assertEqual(state_a["planning_update_count"], 20)
        self.assertIsInstance(DynaQPlusAgent(config(), checkpoint=None), Agent)
        json.dumps(state_a, allow_nan=False, sort_keys=True)

    def test_state_round_trip_preserves_rng_model_and_next_update(self) -> None:
        cfg = config(planning_steps=7, kappa=0.03)
        original = DynaQPlusAgent(cfg, checkpoint=None)
        original.reset(initialization_seed=303, exploration_seed=404)
        for step in range(3):
            action = original.act([step, 1])
            original.observe(
                transition(
                    step=step,
                    observation=[step + 1, 1],
                    action=action,
                    reward=float(step - 1),
                )
            )

        serialized = copy.deepcopy(dict(original.get_state()))
        restored = DynaQPlusAgent(cfg, checkpoint=None)
        restored.restore_state(serialized)
        self.assertEqual(original.state_sha256(), restored.state_sha256())

        original_action = original.act([3, 1])
        restored_action = restored.act([3, 1])
        self.assertEqual(original_action, restored_action)
        next_transition = transition(
            step=3,
            observation=[4, 1],
            action=original_action,
            reward=2.0,
            terminated=True,
        )
        original.observe(next_transition)
        restored.observe(next_transition)
        self.assertEqual(original.get_state(), restored.get_state())

    def test_hidden_evaluator_information_fails_closed(self) -> None:
        agent = DynaQPlusAgent(config(), checkpoint=None)
        agent.reset(initialization_seed=1, exploration_seed=2)
        action = agent.act("s0")
        with self.assertRaises(ValueError):
            agent.observe(
                transition(
                    step=0,
                    observation="s1",
                    action=action,
                    reward=0.0,
                    optional_information={"executed_action": 1},
                )
            )

    def test_common_tabular_checkpoint_is_accepted_without_mutation(self) -> None:
        checkpoint = {
            "schema_version": 1,
            "actions": [0, 1],
            "initial_q_value": 0.0,
            "q_values": [
                {"state": "s0", "action": 0, "value": 3.0},
                {"state": "s0", "action": 1, "value": 1.0},
            ],
        }
        agent = DynaQPlusAgent(config(planning_steps=0), checkpoint=checkpoint)
        self.assertEqual(agent.checkpoint(), checkpoint)
        agent.reset(initialization_seed=8, exploration_seed=9)
        self.assertEqual(agent.act("s0"), 0)

    def test_invalid_dyna_specific_parameters_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            DynaQPlusConfig(
                agent_id="d0",
                actions=(0, 1),
                learning_rate=0.5,
                discount_factor=0.9,
                exploration_epsilon=0.1,
                planning_steps=-1,
                kappa=0.01,
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            )
        with self.assertRaises(ValueError):
            DynaQPlusConfig(
                agent_id="d0",
                actions=(0, 1),
                learning_rate=0.5,
                discount_factor=0.9,
                exploration_epsilon=0.1,
                planning_steps=5,
                kappa=-0.01,
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            )


if __name__ == "__main__":
    unittest.main()
