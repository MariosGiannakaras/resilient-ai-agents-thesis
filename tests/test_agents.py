from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.agents import (  # noqa: E402
    RectangularRobustValueIterationAgent,
    RobustStateAction,
    RobustTransitionOutcome,
    RobustTransitionRow,
    RobustValueIterationConfig,
    TabularQLearningAgent,
    TabularQLearningConfig,
)
from resilient_agents.contracts import Agent, AgentTransition  # noqa: E402


def q_config(*, agent_id: str, learning_enabled: bool) -> TabularQLearningConfig:
    return TabularQLearningConfig(
        agent_id=agent_id,
        actions=(0, 1),
        learning_rate=0.5,
        discount_factor=0.9,
        exploration_epsilon=0.0,
        learning_enabled=learning_enabled,
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


def row(*outcomes: RobustTransitionOutcome) -> RobustTransitionRow:
    return RobustTransitionRow(outcomes=outcomes)


def outcome(
    next_state: str, probability: float, reward: float, *, terminal: bool
) -> RobustTransitionOutcome:
    return RobustTransitionOutcome(
        next_state=next_state,
        probability=probability,
        reward=reward,
        terminal=terminal,
    )


class TabularQLearningAgentTests(unittest.TestCase):
    def test_hand_computed_update_and_terminal_boundary(self) -> None:
        checkpoint = {
            "schema_version": 1,
            "actions": [0, 1],
            "initial_q_value": 0.0,
            "q_values": [
                {"state": "s1", "action": 0, "value": 2.0},
                {"state": "s1", "action": 1, "value": 4.0},
            ],
        }
        agent = TabularQLearningAgent(
            q_config(agent_id="c0", learning_enabled=True), checkpoint=checkpoint
        )
        agent.reset(initialization_seed=1, exploration_seed=2)
        selected = agent.act("s0")
        agent.observe(
            transition(step=0, observation="s1", action=selected, reward=1.0)
        )
        learned = {
            (item["state"], item["action"]): item["value"]
            for item in agent.checkpoint()["q_values"]
        }
        self.assertEqual(learned[("s0", selected)], 2.3)

        terminal_action = agent.act("s2")
        agent.observe(
            transition(
                step=1,
                observation="goal",
                action=terminal_action,
                reward=2.0,
                terminated=True,
            )
        )
        learned = {
            (item["state"], item["action"]): item["value"]
            for item in agent.checkpoint()["q_values"]
        }
        self.assertEqual(learned[("s2", terminal_action)], 1.0)

    def test_common_checkpoint_freezes_f0_and_updates_c0(self) -> None:
        trainer = TabularQLearningAgent(
            q_config(agent_id="trainer", learning_enabled=True), checkpoint=None
        )
        trainer.reset(initialization_seed=3, exploration_seed=4)
        action = trainer.act([0, 0])
        trainer.observe(
            transition(
                step=0,
                observation=[1, 0],
                action=action,
                reward=2.0,
                terminated=True,
            )
        )
        nominal = trainer.checkpoint()

        frozen = TabularQLearningAgent(
            q_config(agent_id="f0", learning_enabled=False), checkpoint=nominal
        )
        continual = TabularQLearningAgent(
            q_config(agent_id="c0", learning_enabled=True), checkpoint=nominal
        )
        self.assertEqual(frozen.checkpoint(), nominal)
        self.assertEqual(continual.checkpoint(), nominal)
        frozen.reset(initialization_seed=8, exploration_seed=9)
        continual.reset(initialization_seed=8, exploration_seed=9)
        self.assertEqual(frozen.checkpoint_sha256(), continual.checkpoint_sha256())
        frozen_before = frozen.checkpoint_sha256()

        frozen_action = frozen.act([0, 0])
        continual_action = continual.act([0, 0])
        self.assertEqual(frozen_action, continual_action)
        shifted = transition(
            step=0,
            observation=[0, 1],
            action=frozen_action,
            reward=-5.0,
            terminated=True,
        )
        frozen.observe(shifted)
        continual.observe(shifted)
        self.assertEqual(frozen_before, frozen.checkpoint_sha256())
        self.assertNotEqual(frozen.checkpoint_sha256(), continual.checkpoint_sha256())

    def test_seeded_replay_is_exact_and_checkpoint_round_trips(self) -> None:
        config = TabularQLearningConfig(
            agent_id="c0",
            actions=(0, 1, 2, 3),
            learning_rate=0.25,
            discount_factor=0.8,
            exploration_epsilon=0.3,
            learning_enabled=True,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )

        def replay() -> tuple[list[int], dict[str, object]]:
            agent = TabularQLearningAgent(config, checkpoint=None)
            agent.reset(initialization_seed=10, exploration_seed=11)
            actions = []
            for step in range(5):
                action = agent.act([step, 0])
                actions.append(action)
                agent.observe(
                    transition(
                        step=step,
                        observation=[step + 1, 0],
                        action=action,
                        reward=float(step),
                        truncated=step == 4,
                    )
                )
            return actions, agent.checkpoint()

        actions_a, checkpoint_a = replay()
        actions_b, checkpoint_b = replay()
        self.assertEqual(actions_a, actions_b)
        self.assertEqual(checkpoint_a, checkpoint_b)
        restored = TabularQLearningAgent(config, checkpoint=copy.deepcopy(checkpoint_a))
        restored.reset(initialization_seed=10, exploration_seed=11)
        self.assertEqual(restored.checkpoint(), checkpoint_a)
        self.assertIsInstance(restored, Agent)

    def test_hidden_information_and_invalid_checkpoint_fail_closed(self) -> None:
        agent = TabularQLearningAgent(
            q_config(agent_id="c0", learning_enabled=True), checkpoint=None
        )
        agent.reset(initialization_seed=0, exploration_seed=0)
        action = agent.act("s")
        with self.assertRaises(ValueError):
            agent.observe(
                transition(
                    step=0,
                    observation="next",
                    action=action,
                    reward=0.0,
                    optional_information={"regime_id": "post-change"},
                )
            )
        invalid = {
            "schema_version": 1,
            "actions": [1, 0],
            "initial_q_value": 0.0,
            "q_values": [],
        }
        with self.assertRaises(ValueError):
            TabularQLearningAgent(
                q_config(agent_id="c0", learning_enabled=True), checkpoint=invalid
            )


class RobustValueIterationAgentTests(unittest.TestCase):
    def _config(self, *, uncertain: bool) -> RobustValueIterationConfig:
        safe_rows = (
            row(outcome("goal", 1.0, 1.0, terminal=True)),
        )
        ambitious_rows = [
            row(outcome("goal", 1.0, 2.0, terminal=True)),
        ]
        if uncertain:
            ambitious_rows.append(
                row(
                    outcome("s", 0.5, 0.0, terminal=False),
                    outcome("goal", 0.5, 0.0, terminal=True),
                )
            )
        return RobustValueIterationConfig(
            agent_id="r0",
            states=("s", "goal"),
            terminal_states=("goal",),
            actions=("safe", "ambitious"),
            state_actions=(
                RobustStateAction("s", "safe", safe_rows),
                RobustStateAction("s", "ambitious", tuple(ambitious_rows)),
            ),
            discount_factor=0.5,
            convergence_tolerance=1e-10,
            max_iterations=100,
            initial_value=0.0,
            exploration_epsilon=0.0,
        )

    def test_singleton_rows_reduce_to_nominal_value_iteration(self) -> None:
        agent = RectangularRobustValueIterationAgent(self._config(uncertain=False))
        plan = agent.plan()
        self.assertEqual(plan["model"]["terminal_states"], ["goal"])
        q_values = {
            (item["state"], item["action"]): item["value"]
            for item in plan["q_values"]
        }
        values = {item["state"]: item["value"] for item in plan["values"]}
        self.assertEqual(q_values[("s", "safe")], 1.0)
        self.assertEqual(q_values[("s", "ambitious")], 2.0)
        self.assertEqual(values["s"], 2.0)
        agent.reset(initialization_seed=12, exploration_seed=13)
        self.assertEqual(agent.act("s"), "ambitious")

    def test_worst_candidate_row_changes_the_hand_computed_backup(self) -> None:
        agent = RectangularRobustValueIterationAgent(self._config(uncertain=True))
        q_values = {
            (item["state"], item["action"]): item["value"]
            for item in agent.plan()["q_values"]
        }
        self.assertEqual(q_values[("s", "safe")], 1.0)
        self.assertAlmostEqual(q_values[("s", "ambitious")], 0.25)
        agent.reset(initialization_seed=12, exploration_seed=13)
        self.assertEqual(agent.act("s"), "safe")

    def test_deployment_is_frozen_and_rejects_hidden_information(self) -> None:
        agent = RectangularRobustValueIterationAgent(self._config(uncertain=True))
        before = agent.plan_sha256()
        agent.reset(initialization_seed=1, exploration_seed=2)
        action = agent.act("s")
        agent.observe(
            transition(
                step=0,
                observation="goal",
                action=action,
                reward=-100.0,
                terminated=True,
            )
        )
        self.assertEqual(agent.plan_sha256(), before)
        action = agent.act("s")
        with self.assertRaises(ValueError):
            agent.observe(
                transition(
                    step=1,
                    observation="goal",
                    action=action,
                    reward=1.0,
                    terminated=True,
                    optional_information={"change_event_ids": ["change"]},
                )
            )

    def test_invalid_probability_row_and_incomplete_model_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            row(outcome("goal", 0.9, 1.0, terminal=True))
        with self.assertRaises(ValueError):
            RobustValueIterationConfig(
                agent_id="r0",
                states=("s", "goal"),
                terminal_states=("goal",),
                actions=("a", "b"),
                state_actions=(
                    RobustStateAction(
                        "s",
                        "a",
                        (row(outcome("goal", 1.0, 1.0, terminal=True)),),
                    ),
                ),
                discount_factor=0.5,
                convergence_tolerance=1e-8,
                max_iterations=10,
                initial_value=0.0,
                exploration_epsilon=0.0,
            )


if __name__ == "__main__":
    unittest.main()
