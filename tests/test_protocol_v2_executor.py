from __future__ import annotations

import hashlib
import json
import unittest

from resilient_agents.gridworld import GridAction, GridWorldEnvironment
from resilient_agents.protocol_v2 import ProtocolV2Branch, ProtocolV2TaskSemantics
from resilient_agents.protocol_v2_executor import execute_phase_a, execute_phase_b
from resilient_agents.protocol_v2_gridworld import GridWorldScientificStateAdapter
from resilient_agents.protocol_v2_runtime import (
    NoLearningProbePlan,
    PhaseARequest,
    ProbeResult,
    ProtocolV2MethodConfig,
    ProtocolV2RootIdentity,
)
from tests.test_gridworld import fixture_seeds, fixture_spec


class _CounterAdapter:
    method_id = "q_learning"

    def __init__(self, state=None):
        self.state = dict(state or {"trained": 0, "probe_mutations": 0, "adaptive_updates": 0})

    def export_state(self):
        return dict(self.state)

    def restore_state(self, state):
        self.state = dict(state)

    def clone(self):
        return _CounterAdapter(self.state)

    def state_sha256(self):
        encoded = json.dumps(
            self.state,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class _PhaseADriver:
    method_id = "q_learning"
    implementation_id = "project-tabular"

    def __init__(self):
        self.state_adapter = _CounterAdapter()
        self._interactions = 0
        self.targets = []

    @property
    def training_interactions(self):
        return self._interactions

    def train_to_interaction(self, target_interaction):
        if target_interaction < self._interactions:
            raise ValueError("target moved backwards")
        self.targets.append(target_interaction)
        self._interactions = target_interaction
        self.state_adapter.state["trained"] = target_interaction


class _BranchDriver:
    def __init__(self, branch, adaptive, learner, environment):
        self.branch = branch
        self.adaptive = adaptive
        self.learner = learner
        self.environment = environment
        self._interactions = 0

    @property
    def interactions(self):
        return self._interactions

    def run_to_interaction(self, target_interaction):
        rewards = []
        while self._interactions < target_interaction:
            transition = self.environment.environment.step(GridAction.RIGHT)
            rewards.append(float(transition.reward))
            self._interactions += 1
            if self.adaptive:
                self.learner.state["adaptive_updates"] += 1
        return {
            "return_sum": float(sum(rewards)),
            "adaptive_updates": float(self.learner.state["adaptive_updates"]),
        }


class ProtocolV2ExecutorTests(unittest.TestCase):
    def _request(self):
        return PhaseARequest(
            protocol_version="protocol-v2.0-candidate",
            experiment_id="executor-test",
            layout_id="layout-a",
            root=ProtocolV2RootIdentity(
                root_id="root-01",
                initialization_seed=1,
                exploration_seed=2,
                scenario_seed=3,
                environment_seed=4,
                action_disturbance_seed=5,
                observation_disturbance_seed=6,
            ),
            task=ProtocolV2TaskSemantics(
                gamma=0.9,
                reward_contract={"step": -0.1, "collision": -0.25, "goal": 1.0},
            ),
            method=ProtocolV2MethodConfig(
                method_id="q_learning",
                implementation_id="project-tabular",
                parameters={
                    "discount_factor": 0.9,
                    "bootstrap_on_truncation": True,
                },
            ),
            training_interaction_budget=10,
            probe_plan=NoLearningProbePlan(
                interaction_indices=(0, 4, 10),
                episodes_per_probe=2,
            ),
        )

    def test_phase_a_uses_absolute_interaction_targets_and_isolated_probes(self):
        driver = _PhaseADriver()
        source_probe_digests = []

        def probe(adapter, *, training_interaction_index, episodes):
            source_probe_digests.append(driver.state_adapter.state_sha256())
            adapter.state["probe_mutations"] += 1
            return ProbeResult(
                training_interaction_index=training_interaction_index,
                probe_environment_interactions=episodes * 3,
                episodes=episodes,
                metrics={"return_mean": float(training_interaction_index)},
            )

        execution = execute_phase_a(
            self._request(),
            driver=driver,
            probe_evaluator=probe,
            checkpoint_provenance={"test": "executor"},
        )
        self.assertEqual(driver.targets, [4, 10])
        self.assertEqual(execution.result.ledger.training_interactions, 10)
        self.assertEqual(execution.result.ledger.probe_interactions, 18)
        self.assertEqual(driver.state_adapter.state["probe_mutations"], 0)
        self.assertEqual(
            [item.training_interaction_index for item in execution.result.probes],
            [0, 4, 10],
        )
        self.assertEqual(
            execution.final_adapter.state_sha256(),
            driver.state_adapter.state_sha256(),
        )
        self.assertEqual(len(source_probe_digests), 3)

    def test_phase_a_rejects_driver_that_overshoots_actual_budget(self):
        driver = _PhaseADriver()

        def overshoot(target):
            driver._interactions = target + 1
            driver.state_adapter.state["trained"] = target + 1

        driver.train_to_interaction = overshoot

        def probe(adapter, *, training_interaction_index, episodes):
            return ProbeResult(
                training_interaction_index=training_interaction_index,
                probe_environment_interactions=episodes,
                episodes=episodes,
                metrics={"return_mean": 0.0},
            )

        with self.assertRaisesRegex(RuntimeError, "exact actual-interaction target"):
            execute_phase_a(
                self._request(),
                driver=driver,
                probe_evaluator=probe,
                checkpoint_provenance={"test": "overshoot"},
            )

    def test_phase_b_clones_identical_fork_then_separates_factors(self):
        nominal_spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=False,
        )
        disturbed_spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=True,
        )
        shared = GridWorldEnvironment(nominal_spec)
        shared.reset(seeds=fixture_seeds())
        shared.step(GridAction.RIGHT)
        shared.step(GridAction.RIGHT)
        environment_adapter = GridWorldScientificStateAdapter(shared)
        learner = _CounterAdapter({"trained": 10, "probe_mutations": 0, "adaptive_updates": 0})
        fork_digest = learner.state_sha256()

        execution = execute_phase_b(
            learner=learner,
            shared_environment=environment_adapter,
            nominal_spec=nominal_spec,
            disturbed_spec=disturbed_spec,
            interaction_budget_per_branch=1,
            driver_factory=lambda branch, adaptive, clone, environment: _BranchDriver(
                branch, adaptive, clone, environment
            ),
        )
        self.assertEqual(execution.branch_point_learner_sha256, fork_digest)
        self.assertEqual({item.branch for item in execution.results}, set(ProtocolV2Branch))
        by_branch = {item.branch: item for item in execution.results}
        self.assertEqual(
            by_branch[ProtocolV2Branch.FROZEN_NOMINAL].final_learner_state_sha256,
            fork_digest,
        )
        self.assertEqual(
            by_branch[ProtocolV2Branch.FROZEN_DISTURBED].final_learner_state_sha256,
            fork_digest,
        )
        self.assertNotEqual(
            by_branch[ProtocolV2Branch.ADAPTIVE_NOMINAL].final_learner_state_sha256,
            fork_digest,
        )
        self.assertNotEqual(
            by_branch[ProtocolV2Branch.ADAPTIVE_DISTURBED].final_learner_state_sha256,
            fork_digest,
        )
        # Nominal and disturbed branches share the fork but diverge on the first
        # post-boundary transition because the disturbed scenario remaps RIGHT.
        self.assertNotEqual(
            by_branch[ProtocolV2Branch.FROZEN_NOMINAL].final_environment_state_sha256,
            by_branch[ProtocolV2Branch.FROZEN_DISTURBED].final_environment_state_sha256,
        )
        shared.close()


if __name__ == "__main__":
    unittest.main()
