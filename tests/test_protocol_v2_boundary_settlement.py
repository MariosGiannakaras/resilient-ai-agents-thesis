from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest import mock

from resilient_agents.contracts import AgentTransition
from resilient_agents.gridworld import ACTION_NAMES, GridWorldEnvironment
from resilient_agents.protocol_v2 import sarsa_state_adapter
from resilient_agents.protocol_v2_boundary_settlement import (
    SETTLEMENT_POLICY_ID,
    settle_phase_a_interaction_boundary,
)
from resilient_agents.protocol_v2_prefix import prepare_shared_no_learning_prefix
from resilient_agents.protocol_v2_runtime import ProtocolV2RootIdentity
from resilient_agents.protocol_v2_tabular_driver import ProjectTabularPhaseADriver
from resilient_agents.protocol_v2_t526_boundary_phase_b_v03 import (
    _selected_inputs,
    _settle_source,
    load_config,
    run_phase_b_v03,
    validate_phase_b_v03_attempt,
    validate_settlement_evidence,
    verify_immutable_inputs,
)
from resilient_agents.sarsa import SarsaAgent, SarsaConfig
from tests.test_gridworld import fixture_seeds, fixture_spec

try:
    import stable_baselines3  # noqa: F401

    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    REPO_ROOT
    / "configs"
    / "protocols"
    / "protocol-v2-t526-boundary-settlement-phase-b-v0.3.json"
)


def _valid_observations(scenario):
    grid = scenario.initial_state_spec["grid"]
    obstacles = {tuple(item) for item in grid["obstacles"]}
    return frozenset(
        (x, y)
        for x in range(grid["width"])
        for y in range(grid["height"])
        if (x, y) not in obstacles
    )


class ProtocolV2BoundarySettlementTests(unittest.TestCase):
    def _config(self, *, epsilon: float = 0.1) -> SarsaConfig:
        return SarsaConfig(
            agent_id="dec054-sarsa",
            actions=ACTION_NAMES,
            learning_rate=0.2,
            discount_factor=0.95,
            exploration_epsilon=epsilon,
            bootstrap_on_truncation=True,
            initial_q_value=0.0,
        )

    def _root(self) -> ProtocolV2RootIdentity:
        return ProtocolV2RootIdentity(
            root_id="dec054-root",
            initialization_seed=101,
            exploration_seed=102,
            scenario_seed=103,
            environment_seed=104,
            action_disturbance_seed=105,
            observation_disturbance_seed=106,
        )

    def _driver_state(self):
        scenario = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=20,
            include_change=False,
        )
        agent = SarsaAgent(self._config(), checkpoint=None)
        adapter = sarsa_state_adapter(agent)
        driver = ProjectTabularPhaseADriver(
            adapter=adapter,
            scenario=scenario,
            root=self._root(),
        )
        driver.train_to_interaction(1)
        return scenario, agent, adapter, driver

    def test_phase_a_stops_exactly_after_nonterminal_interaction_with_deferred_backup(self):
        scenario, agent, adapter, driver = self._driver_state()
        try:
            state = adapter.export_state()
            self.assertEqual(driver.training_interactions, 1)
            self.assertEqual(state["observed_transition_count"], 1)
            self.assertEqual(state["last_step"], 0)
            self.assertIsNone(state["pending_action"])
            self.assertIsNotNone(state["deferred_update"])
            before = adapter.state_sha256()
            driver.train_to_interaction(1)
            self.assertEqual(adapter.state_sha256(), before)
            self.assertEqual(driver.training_interactions, 1)
            self.assertIn(
                tuple(state["deferred_update"]["next_state"]),
                _valid_observations(scenario),
            )
        finally:
            driver.close()

    def test_settlement_uses_restored_behavior_policy_applies_once_and_keeps_accounting(self):
        scenario, agent, adapter, driver = self._driver_state()
        try:
            pre = adapter.export_state()
            pre_sha = adapter.state_sha256()
            result = settle_phase_a_interaction_boundary(
                adapter,
                expected_source_learner_sha256=pre_sha,
                expected_interactions=1,
                valid_observations=_valid_observations(scenario),
            )
            self.assertEqual(result.policy_id, SETTLEMENT_POLICY_ID)
            self.assertFalse(result.no_op)
            self.assertEqual(result.environment_interactions_consumed, 0)
            self.assertEqual(result.pre_counters, result.post_counters)
            self.assertEqual(result.post_counters["observed_transition_count"], 1)
            self.assertEqual(result.post_counters["last_step"], 0)
            self.assertEqual(
                result.details["deferred_transition"], pre["deferred_update"]
            )
            self.assertIn(
                result.details["selected_bootstrap_action"], ACTION_NAMES
            )
            self.assertAlmostEqual(
                result.details["q_value_after"],
                result.details["q_value_before"]
                + self._config().learning_rate
                * (result.details["target"] - result.details["q_value_before"]),
            )
            post = adapter.export_state()
            self.assertIsNone(post["pending_action"])
            self.assertIsNone(post["deferred_update"])

            post_sha = adapter.state_sha256()
            repeated = settle_phase_a_interaction_boundary(
                adapter,
                expected_source_learner_sha256=post_sha,
                expected_interactions=1,
                valid_observations=_valid_observations(scenario),
            )
            self.assertTrue(repeated.no_op)
            self.assertEqual(adapter.state_sha256(), post_sha)
        finally:
            driver.close()

    def test_settlement_matches_existing_bootstrapped_truncation_semantics(self):
        checkpoint = {
            "schema_version": 1,
            "actions": list(ACTION_NAMES),
            "initial_q_value": 0.0,
            "q_values": [
                {"state": [0, 1], "action": "right", "value": 3.0}
            ],
        }
        settled_agent = SarsaAgent(self._config(epsilon=0.0), checkpoint=checkpoint)
        truncated_agent = SarsaAgent(self._config(epsilon=0.0), checkpoint=checkpoint)
        for agent in (settled_agent, truncated_agent):
            agent.reset(initialization_seed=11, exploration_seed=12)
        first_settled = settled_agent.act([0, 0])
        first_truncated = truncated_agent.act([0, 0])
        self.assertEqual(first_settled, first_truncated)
        settled_agent.observe(
            AgentTransition(
                step=0,
                observation=[0, 1],
                intended_action=first_settled,
                reward=-0.1,
                terminated=False,
                truncated=False,
                optional_information={},
            )
        )
        truncated_agent.observe(
            AgentTransition(
                step=0,
                observation=[0, 1],
                intended_action=first_truncated,
                reward=-0.1,
                terminated=False,
                truncated=True,
                optional_information={},
            )
        )
        adapter = sarsa_state_adapter(settled_agent)
        result = settle_phase_a_interaction_boundary(
            adapter,
            expected_source_learner_sha256=adapter.state_sha256(),
            expected_interactions=1,
            valid_observations={(0, 0), (0, 1)},
        )
        self.assertEqual(result.details["selected_bootstrap_action"], "right")
        self.assertEqual(settled_agent.get_state(), truncated_agent.get_state())

    def test_settled_sarsa_enters_fresh_prefix_without_forcing_bootstrap_action(self):
        scenario, agent, adapter, driver = self._driver_state()
        try:
            result = settle_phase_a_interaction_boundary(
                adapter,
                expected_source_learner_sha256=adapter.state_sha256(),
                expected_interactions=1,
                valid_observations=_valid_observations(scenario),
            )
            settled_checkpoint = copy.deepcopy(agent.checkpoint())
            settled_sha = adapter.state_sha256()

            expected_clone = adapter.clone()
            expected_env = GridWorldEnvironment(scenario)
            try:
                start_observation = expected_env.reset(seeds=fixture_seeds())
                expected_prefix_action = expected_clone.agent.act(start_observation)
            finally:
                expected_env.close()

            prefix = prepare_shared_no_learning_prefix(
                learner=adapter,
                nominal_spec=scenario,
                environment_seeds=fixture_seeds(),
                interactions=1,
            )
            try:
                transition = prefix.environment.environment.gym_env.last_transition
                self.assertIsNotNone(transition)
                self.assertEqual(transition.intended_action, expected_prefix_action)
                self.assertEqual(agent.checkpoint(), settled_checkpoint)
                self.assertNotEqual(adapter.state_sha256(), settled_sha)
                self.assertFalse(
                    result.details["bootstrap_action_executed_in_environment"]
                )
            finally:
                prefix.environment.environment.close()
        finally:
            driver.close()

    def test_changed_q_rng_or_deferred_provenance_and_malformed_pending_fail_closed(self):
        scenario, agent, adapter, driver = self._driver_state()
        try:
            authoritative_sha = adapter.state_sha256()
            mutations = []
            q_mutated = adapter.clone()
            q_mutated.agent._q_values[("[99,99]", '"up"')] = 1.0
            mutations.append(q_mutated)
            rng_mutated = adapter.clone()
            rng_mutated.agent._exploration_rng.random()
            mutations.append(rng_mutated)
            deferred_mutated = adapter.clone()
            prior = deferred_mutated.agent._deferred_update
            deferred_mutated.agent._deferred_update = (
                prior[0], prior[1], prior[2] - 0.01, prior[3]
            )
            mutations.append(deferred_mutated)
            for mutation in mutations:
                with self.subTest(mutation=mutation.state_sha256()):
                    with self.assertRaisesRegex(ValueError, "source learner SHA"):
                        settle_phase_a_interaction_boundary(
                            mutation,
                            expected_source_learner_sha256=authoritative_sha,
                            expected_interactions=1,
                            valid_observations=_valid_observations(scenario),
                        )

            pending = adapter.clone()
            pending.agent._pending_action = ('[0,0]', '"up"')
            with self.assertRaisesRegex(ValueError, "pending_action"):
                settle_phase_a_interaction_boundary(
                    pending,
                    expected_source_learner_sha256=pending.state_sha256(),
                    expected_interactions=1,
                    valid_observations=_valid_observations(scenario),
                )
            invalid_state = copy.deepcopy(dict(adapter.export_state()))
            invalid_state["pending_action"] = {"state": [0, 0], "action": "up"}
            with self.assertRaisesRegex(ValueError, "both pending action and deferred"):
                SarsaAgent(self._config(), checkpoint=None).restore_state(invalid_state)
        finally:
            driver.close()

    @unittest.skipUnless(
        _SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed"
    )
    def test_all_retained_methods_settle_deterministically_without_environment_use(self):
        config = load_config(CONFIG_PATH)
        verified = verify_immutable_inputs(repo_root=REPO_ROOT, config=config)
        self.assertEqual(
            verified["recovery"]["accepted_scientific_continuation_states"], 30
        )
        _, plan, layouts, roots, recovery_rows = _selected_inputs(
            repo_root=REPO_ROOT, config=config
        )
        no_op_by_method = {method: 0 for method in ACTION_METHODS}
        non_noop_sarsa = 0
        for key, recovery_row in recovery_rows.items():
            method_id, root_id, layout_id = key
            learner, settlement = _settle_source(
                repo_root=REPO_ROOT,
                config=config,
                plan=plan,
                layout=layouts[layout_id],
                root_data=roots[root_id],
                method_id=method_id,
                recovery_row=recovery_row,
            )
            self.assertEqual(settlement["environment_interactions_consumed"], 0)
            self.assertIsNone(learner.export_state().get("pending_action"))
            no_op_by_method[method_id] += int(settlement["no_op"])
            non_noop_sarsa += int(method_id == "sarsa" and not settlement["no_op"])
        self.assertEqual(no_op_by_method["q_learning"], 6)
        self.assertEqual(no_op_by_method["dqn"], 6)
        self.assertEqual(no_op_by_method["ppo"], 6)
        self.assertEqual(no_op_by_method["dyna_q_plus"], 6)
        self.assertEqual(no_op_by_method["sarsa"], 1)
        self.assertEqual(non_noop_sarsa, 5)
        self.assertFalse(config["final_reserve_access"])

    @unittest.skipUnless(
        _SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed"
    )
    def test_versioned_evidence_validators_run_only_when_outputs_exist(self):
        config = load_config(CONFIG_PATH)
        settlement = REPO_ROOT / config["settlement"]["output_directory"]
        phase_b = REPO_ROOT / config["phase_b"]["output_directory"]
        if settlement.exists():
            self.assertEqual(
                validate_settlement_evidence(
                    repo_root=REPO_ROOT, config=config
                )["status"],
                "valid-complete",
            )
        if phase_b.exists():
            self.assertIn(
                validate_phase_b_v03_attempt(
                    repo_root=REPO_ROOT, config=config
                )["status"],
                {"valid-complete", "valid-failed"},
            )

    def test_phase_b_cannot_create_output_before_complete_settlement_barrier(self):
        config = load_config(CONFIG_PATH)
        phase_b = REPO_ROOT / config["phase_b"]["output_directory"]
        self.assertFalse(phase_b.exists())
        with (
            mock.patch(
                "resilient_agents.protocol_v2_t526_boundary_phase_b_v03.verify_immutable_inputs"
            ),
            mock.patch(
                "resilient_agents.protocol_v2_t526_boundary_phase_b_v03.validate_settlement_evidence",
                return_value={"accepted_states": 29},
            ),
        ):
            with self.assertRaisesRegex(RuntimeError, "incomplete settlement barrier"):
                run_phase_b_v03(repo_root=REPO_ROOT, config=config)
        self.assertFalse(phase_b.exists())


ACTION_METHODS = ("q_learning", "sarsa", "dqn", "ppo", "dyna_q_plus")


if __name__ == "__main__":
    unittest.main()
