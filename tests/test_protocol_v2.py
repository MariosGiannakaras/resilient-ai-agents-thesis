from __future__ import annotations

import unittest

from resilient_agents.agents import TabularQLearningAgent, TabularQLearningConfig
from resilient_agents.contracts import AgentTransition
from resilient_agents.dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig
from resilient_agents.protocol_v2 import (
    CORE_METHOD_CAPABILITIES,
    InteractionLedger,
    MethodRegistration,
    MethodRegistry,
    ProtocolV2Branch,
    ProtocolV2Phase,
    ProtocolV2TaskSemantics,
    ScientificCheckpoint,
    TabularQScientificStateAdapter,
    dyna_q_plus_state_adapter,
    fork_four_branches,
    make_scientific_checkpoint,
    require_information_limited_transition,
    run_isolated_probe,
    sarsa_state_adapter,
)
from resilient_agents.sarsa import SarsaAgent, SarsaConfig


ACTIONS = ("left", "right")


def transition(
    *,
    step: int,
    observation: tuple[int, int],
    intended_action: str,
    reward: float = 0.0,
    terminated: bool = False,
    truncated: bool = False,
    optional_information: dict[str, object] | None = None,
) -> AgentTransition:
    return AgentTransition(
        step=step,
        observation=observation,
        intended_action=intended_action,
        reward=reward,
        terminated=terminated,
        truncated=truncated,
        optional_information=optional_information or {},
    )


class ProtocolV2TaskSemanticsTests(unittest.TestCase):
    def test_administrative_truncation_requires_bootstrap(self) -> None:
        semantics = ProtocolV2TaskSemantics(
            gamma=0.95,
            reward_contract={"step": -1.0, "goal": 10.0},
            administrative_truncation=True,
            bootstrap_on_truncation=True,
        )
        self.assertEqual(semantics.gamma, 0.95)
        self.assertEqual(len(semantics.reward_contract_sha256), 64)

        with self.assertRaisesRegex(ValueError, "requires bootstrap_on_truncation"):
            ProtocolV2TaskSemantics(
                gamma=0.95,
                reward_contract={"step": -1.0},
                administrative_truncation=True,
                bootstrap_on_truncation=False,
            )


class MethodRegistryTests(unittest.TestCase):
    def test_core_registry_contains_bounded_candidate_pool(self) -> None:
        registry = MethodRegistry.core_candidates()
        self.assertEqual(
            registry.method_ids(),
            ("dqn", "dyna_q_plus", "ppo", "q_learning", "sarsa"),
        )
        self.assertEqual(len(CORE_METHOD_CAPABILITIES), 5)
        self.assertIn(
            "replay_buffer_contents",
            registry.get("dqn").capabilities.required_checkpoint_components,
        )
        self.assertIn(
            "rollout_update_counters",
            registry.get("ppo").capabilities.required_checkpoint_components,
        )

    def test_duplicate_method_registration_is_rejected(self) -> None:
        registry = MethodRegistry.core_candidates()
        existing = registry.get("q_learning")
        with self.assertRaisesRegex(ValueError, "already registered"):
            registry.register(
                MethodRegistration(
                    capabilities=existing.capabilities,
                    implementation_id="duplicate",
                )
            )


class InteractionLedgerTests(unittest.TestCase):
    def test_actual_interactions_are_separated_by_scientific_role(self) -> None:
        ledger = InteractionLedger()
        ledger.record_training(7)
        ledger.record_probe(3)
        ledger.record_deployment(ProtocolV2Branch.FROZEN_NOMINAL, 2)
        ledger.record_deployment(ProtocolV2Branch.ADAPTIVE_DISTURBED, 5)

        self.assertEqual(ledger.training_interactions, 7)
        self.assertEqual(ledger.probe_interactions, 3)
        self.assertEqual(ledger.deployment_total, 7)
        self.assertEqual(ledger.all_environment_interactions, 17)
        ledger.require_training_budget(7)
        with self.assertRaisesRegex(RuntimeError, "exceeded"):
            ledger.require_training_budget(6)


class ScientificCheckpointTests(unittest.TestCase):
    def _q_adapter(self) -> TabularQScientificStateAdapter:
        config = TabularQLearningConfig(
            agent_id="q-v2",
            actions=ACTIONS,
            learning_rate=0.5,
            discount_factor=0.9,
            exploration_epsilon=1.0,
            learning_enabled=True,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        agent = TabularQLearningAgent(config, checkpoint=None)
        agent.reset(initialization_seed=11, exploration_seed=22)
        first_action = agent.act((0, 0))
        agent.observe(
            transition(
                step=1,
                observation=(1, 0),
                intended_action=first_action,
                reward=0.25,
            )
        )
        return TabularQScientificStateAdapter(agent)

    def test_checkpoint_digest_is_deterministic_and_provenance_sensitive(self) -> None:
        adapter = self._q_adapter()
        first = make_scientific_checkpoint(
            adapter=adapter,
            root_id="root-001",
            layout_id="layout-a",
            phase=ProtocolV2Phase.NOMINAL_TRAINING,
            training_interaction_index=1,
            provenance={"python": "3.12", "implementation": "project-tabular"},
        )
        second = ScientificCheckpoint(
            method_id=first.method_id,
            root_id=first.root_id,
            layout_id=first.layout_id,
            phase=first.phase,
            training_interaction_index=first.training_interaction_index,
            state=first.state,
            provenance={"implementation": "project-tabular", "python": "3.12"},
        )
        self.assertEqual(first.sha256, second.sha256)
        self.assertEqual(len(first.sha256), 64)

        changed = ScientificCheckpoint(
            method_id=first.method_id,
            root_id=first.root_id,
            layout_id=first.layout_id,
            phase=first.phase,
            training_interaction_index=first.training_interaction_index,
            state=first.state,
            provenance={"implementation": "project-tabular", "python": "3.13"},
        )
        self.assertNotEqual(first.sha256, changed.sha256)

    def test_q_state_survives_destroy_restore_and_continues_exactly(self) -> None:
        original = self._q_adapter()
        saved = original.export_state()
        config = original.config

        restored_agent = TabularQLearningAgent(config, checkpoint=None)
        restored = TabularQScientificStateAdapter(restored_agent)
        restored.restore_state(saved)
        self.assertEqual(original.state_sha256(), restored.state_sha256())

        original_action = original.agent.act((1, 0))
        restored_action = restored.agent.act((1, 0))
        self.assertEqual(original_action, restored_action)

        next_transition = transition(
            step=2,
            observation=(2, 0),
            intended_action=original_action,
            reward=1.0,
        )
        original.agent.observe(next_transition)
        restored.agent.observe(next_transition)
        self.assertEqual(original.export_state(), restored.export_state())

    def test_four_branch_fork_has_exact_state_equality(self) -> None:
        adapter = self._q_adapter()
        source_digest = adapter.state_sha256()
        branches = fork_four_branches(adapter)
        self.assertEqual(set(branches), set(ProtocolV2Branch))
        self.assertEqual(
            {branch.state_sha256() for branch in branches.values()},
            {source_digest},
        )

    def test_isolated_probe_cannot_mutate_training_state(self) -> None:
        adapter = self._q_adapter()
        before = adapter.state_sha256()

        def probe(clone: object) -> str:
            assert isinstance(clone, TabularQScientificStateAdapter)
            return clone.agent.act((1, 0))

        selected_action = run_isolated_probe(adapter, probe)
        self.assertIn(selected_action, ACTIONS)
        self.assertEqual(adapter.state_sha256(), before)


class NativeProjectAdapterTests(unittest.TestCase):
    def test_sarsa_clone_preserves_deferred_update_and_rng(self) -> None:
        config = SarsaConfig(
            agent_id="sarsa-v2",
            actions=ACTIONS,
            learning_rate=0.5,
            discount_factor=0.9,
            exploration_epsilon=1.0,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        agent = SarsaAgent(config, checkpoint=None)
        agent.reset(initialization_seed=101, exploration_seed=202)
        first_action = agent.act((0, 0))
        agent.observe(
            transition(
                step=1,
                observation=(1, 0),
                intended_action=first_action,
                reward=0.4,
            )
        )
        adapter = sarsa_state_adapter(agent)
        clone = adapter.clone()
        self.assertEqual(adapter.state_sha256(), clone.state_sha256())

        original_action = adapter.agent.act((1, 0))
        clone_action = clone.agent.act((1, 0))
        self.assertEqual(original_action, clone_action)
        self.assertEqual(adapter.export_state(), clone.export_state())

    def test_dyna_q_plus_clone_preserves_model_recency_and_rng(self) -> None:
        config = DynaQPlusConfig(
            agent_id="dyna-v2",
            actions=ACTIONS,
            learning_rate=0.5,
            discount_factor=0.9,
            exploration_epsilon=1.0,
            planning_steps=3,
            kappa=0.01,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )
        agent = DynaQPlusAgent(config, checkpoint=None)
        agent.reset(initialization_seed=303, exploration_seed=404)
        first_action = agent.act((0, 0))
        agent.observe(
            transition(
                step=1,
                observation=(1, 0),
                intended_action=first_action,
                reward=0.5,
            )
        )
        adapter = dyna_q_plus_state_adapter(agent)
        clone = adapter.clone()
        self.assertEqual(adapter.export_state(), clone.export_state())
        self.assertEqual(adapter.state_sha256(), clone.state_sha256())


class InformationBoundaryTests(unittest.TestCase):
    def test_evaluator_only_information_is_rejected(self) -> None:
        clean = transition(step=1, observation=(0, 0), intended_action="left")
        require_information_limited_transition(clean)

        leaked = transition(
            step=1,
            observation=(0, 0),
            intended_action="left",
            optional_information={"true_state": (9, 9)},
        )
        with self.assertRaisesRegex(ValueError, "evaluator-only"):
            require_information_limited_transition(leaked)


if __name__ == "__main__":
    unittest.main()
