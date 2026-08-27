from __future__ import annotations

import unittest

from resilient_agents.protocol_v2 import (
    InteractionLedger,
    ProtocolV2Branch,
    ProtocolV2Phase,
    ProtocolV2TaskSemantics,
    ScientificCheckpoint,
)
from resilient_agents.protocol_v2_runtime import (
    FOUR_BRANCH_PLAN,
    NoLearningProbePlan,
    PhaseARequest,
    PhaseAResult,
    PhaseBInteractionLedger,
    ProbeResult,
    ProtocolV2MethodConfig,
    ProtocolV2RootIdentity,
    RunFailureKind,
    RunFailureRecord,
    require_same_branch_opportunity,
)


class ProtocolV2RuntimeSchemaTests(unittest.TestCase):
    def _root(self) -> ProtocolV2RootIdentity:
        return ProtocolV2RootIdentity(
            root_id="root-01",
            initialization_seed=1,
            exploration_seed=2,
            scenario_seed=3,
            environment_seed=4,
            action_disturbance_seed=5,
            observation_disturbance_seed=6,
        )

    def _request(self) -> PhaseARequest:
        task = ProtocolV2TaskSemantics(
            gamma=0.9,
            reward_contract={"step": -1.0, "collision": -1.0, "goal": 10.0},
        )
        method = ProtocolV2MethodConfig(
            method_id="q_learning",
            implementation_id="project-tabular",
            parameters={
                "discount_factor": 0.9,
                "bootstrap_on_truncation": True,
                "learning_rate": 0.2,
            },
        )
        return PhaseARequest(
            protocol_version="protocol-v2.0-candidate",
            experiment_id="phase-a-test",
            layout_id="layout-a",
            root=self._root(),
            task=task,
            method=method,
            training_interaction_budget=100,
            probe_plan=NoLearningProbePlan(
                interaction_indices=(0, 50, 100),
                episodes_per_probe=2,
            ),
        )

    def test_phase_a_rejects_method_specific_objective_drift(self) -> None:
        task = ProtocolV2TaskSemantics(
            gamma=0.9,
            reward_contract={"step": -1.0},
        )
        with self.assertRaisesRegex(ValueError, "common task-level gamma"):
            PhaseARequest(
                protocol_version="protocol-v2.0-candidate",
                experiment_id="bad-gamma",
                layout_id="layout-a",
                root=self._root(),
                task=task,
                method=ProtocolV2MethodConfig(
                    method_id="q_learning",
                    implementation_id="project-tabular",
                    parameters={"discount_factor": 0.8},
                ),
                training_interaction_budget=100,
                probe_plan=NoLearningProbePlan(
                    interaction_indices=(0, 100), episodes_per_probe=1
                ),
            )

    def test_probe_schedule_is_interaction_indexed_and_bounded(self) -> None:
        with self.assertRaisesRegex(ValueError, "sorted and unique"):
            NoLearningProbePlan(
                interaction_indices=(0, 50, 50), episodes_per_probe=1
            )
        with self.assertRaisesRegex(ValueError, "extends beyond"):
            NoLearningProbePlan(
                interaction_indices=(0, 101), episodes_per_probe=1
            ).validate_against_training_budget(100)

    def test_completed_phase_a_requires_exact_actual_budget_and_probe_reconciliation(self) -> None:
        request = self._request()
        ledger = InteractionLedger(training_interactions=100, probe_interactions=6)
        checkpoint = ScientificCheckpoint(
            method_id="q_learning",
            root_id="root-01",
            layout_id="layout-a",
            phase=ProtocolV2Phase.NOMINAL_TRAINING,
            training_interaction_index=100,
            state={"scientific_state": "opaque-test-value"},
            provenance={"implementation": "project-tabular"},
        )
        result = PhaseAResult(
            request=request,
            ledger=ledger,
            probes=(
                ProbeResult(
                    training_interaction_index=0,
                    probe_environment_interactions=2,
                    episodes=2,
                    metrics={"return_mean": 0.0},
                ),
                ProbeResult(
                    training_interaction_index=50,
                    probe_environment_interactions=2,
                    episodes=2,
                    metrics={"return_mean": 1.0},
                ),
                ProbeResult(
                    training_interaction_index=100,
                    probe_environment_interactions=2,
                    episodes=2,
                    metrics={"return_mean": 2.0},
                ),
            ),
            final_checkpoint=checkpoint,
            completed=True,
        )
        self.assertTrue(result.completed)

        short_ledger = InteractionLedger(training_interactions=99, probe_interactions=6)
        short_checkpoint = ScientificCheckpoint(
            method_id="q_learning",
            root_id="root-01",
            layout_id="layout-a",
            phase=ProtocolV2Phase.NOMINAL_TRAINING,
            training_interaction_index=99,
            state={"scientific_state": "opaque-test-value"},
            provenance={"implementation": "project-tabular"},
        )
        with self.assertRaisesRegex(ValueError, "exact training budget"):
            PhaseAResult(
                request=request,
                ledger=short_ledger,
                probes=result.probes,
                final_checkpoint=short_checkpoint,
                completed=True,
            )

    def test_four_branch_plan_has_exact_nominal_disturbed_frozen_adaptive_factorial(self) -> None:
        self.assertEqual({item.branch for item in FOUR_BRANCH_PLAN}, set(ProtocolV2Branch))
        self.assertEqual(
            {(item.disturbed, item.adaptive) for item in FOUR_BRANCH_PLAN},
            {(False, False), (True, False), (False, True), (True, True)},
        )

    def test_phase_b_ledger_enforces_equal_exact_opportunity(self) -> None:
        ledger = PhaseBInteractionLedger(interaction_budget_per_branch=10)
        for branch in ProtocolV2Branch:
            ledger.record(branch, 10)
        ledger.require_complete()
        self.assertEqual(require_same_branch_opportunity(ledger.counts), 10)

        with self.assertRaisesRegex(RuntimeError, "exceeded"):
            ledger.record(ProtocolV2Branch.FROZEN_NOMINAL)

        unequal = dict(ledger.counts)
        unequal[ProtocolV2Branch.ADAPTIVE_DISTURBED] = 9
        with self.assertRaisesRegex(ValueError, "equal interaction opportunity"):
            require_same_branch_opportunity(unequal)

    def test_scientific_failure_cannot_be_replaced_by_retry_root(self) -> None:
        with self.assertRaisesRegex(ValueError, "scientific failures"):
            RunFailureRecord(
                failure_id="failure-1",
                kind=RunFailureKind.SCIENTIFIC,
                root_id="root-01",
                method_id="ppo",
                layout_id="layout-a",
                branch=ProtocolV2Branch.ADAPTIVE_DISTURBED,
                interaction_index=123,
                exception_type="FloatingPointError",
                message="non-finite loss",
                retry_of_failure_id="failure-0",
            )

        retry = RunFailureRecord(
            failure_id="infra-retry-1",
            kind=RunFailureKind.INFRASTRUCTURE,
            root_id="root-01",
            method_id="ppo",
            layout_id="layout-a",
            branch=None,
            interaction_index=0,
            exception_type="OSError",
            message="worker interrupted",
            retry_of_failure_id="infra-failure-0",
        )
        self.assertEqual(retry.root_id, "root-01")


if __name__ == "__main__":
    unittest.main()
