from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.contracts import ProtocolStage, RetentionPolicy  # noqa: E402
from resilient_agents.v11_candidate_runner import (  # noqa: E402
    V11CandidateExperimentRequest,
    V11CandidateExperimentRunner,
)
from resilient_agents.v11_protocol import load_v11_candidate_protocol  # noqa: E402

PROTOCOL = load_v11_candidate_protocol(ROOT / "configs" / "protocols" / "protocol-v1.1.json")


def request(
    *,
    run_id: str = "DEV-V11-CANDIDATE",
    stage: ProtocolStage = ProtocolStage.DEVELOPMENT,
    layout_id: str = "dev-l01",
    condition_id: str = "action-remap-2-swap",
    agent_ids: tuple[str, ...] = ("f0", "c0", "s0", "dq0", "d0"),
    configuration_ids: dict[str, str] | None = None,
) -> V11CandidateExperimentRequest:
    if configuration_ids is None:
        configuration_ids = {
            "f0": "f0-base-v1",
            "c0": "c0-base-v1",
            "s0": "s0-a025-v1",
            "dq0": "dq0-p05-v1",
            "d0": "d0-p05-k0005-v1",
        }
    return V11CandidateExperimentRequest(
        run_id=run_id,
        stage=stage,
        layout_id=layout_id,
        condition_id=condition_id,
        root_seeds=PROTOCOL.root_seeds_for(stage),
        agent_ids=agent_ids,
        q_learning_rate=0.5,
        discount_factor=0.96875,
        exploration_epsilon=0.125,
        training_episodes_per_layout=512,
        pre_change_episodes=16,
        post_change_episodes=32,
        immediate_window=1,
        worst_window=2,
        terminal_window=4,
        recovery_tolerance=0.0,
        recovery_stability_episodes=2,
        retention_policy=RetentionPolicy.EVENTS,
        auto_publish=False,
        execution_timeout_seconds=None,
        agent_configuration_ids=configuration_ids,
    )


class V11CandidateRunnerTests(unittest.TestCase):
    def test_request_round_trip_preserves_configuration_identity(self) -> None:
        original = request()
        restored = V11CandidateExperimentRequest.from_dict(original.to_dict())
        self.assertEqual(restored, original)
        self.assertEqual(restored.agent_configuration_ids["d0"], "d0-p05-k0005-v1")

    def test_resolved_config_records_protocol_and_configuration_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runner = V11CandidateExperimentRunner(
                repo_root=Path(temporary), protocol=PROTOCOL, request=request()
            )
            resolved = runner._resolved_config()
        identities = resolved["agent_configuration_identities"]
        self.assertEqual(set(identities), {"f0", "c0", "s0", "dq0", "d0"})
        self.assertEqual(identities["s0"]["configuration_id"], "s0-a025-v1")
        self.assertEqual(identities["dq0"]["configuration"]["settings"]["planning_steps"], 5)
        self.assertEqual(identities["d0"]["configuration"]["settings"]["kappa"], 0.0005)
        self.assertEqual(len(resolved["protocol_sha256"]), 64)
        self.assertEqual(len(resolved["configuration_set_sha256"]), 64)
        self.assertEqual(resolved["protocol_lifecycle"], "candidate-non-final")

    def test_configuration_must_belong_to_selected_agent(self) -> None:
        invalid = request(
            agent_ids=("s0",),
            configuration_ids={"s0": "c0-base-v1"},
        )
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "does not belong"):
                V11CandidateExperimentRunner(
                    repo_root=Path(temporary), protocol=PROTOCOL, request=invalid
                )

    def test_tuning_accepts_only_predeclared_conditions(self) -> None:
        valid = request(
            run_id="TUNE-V11-VALID",
            stage=ProtocolStage.TUNING,
            layout_id="tune-l01",
            condition_id="nominal",
            agent_ids=("s0",),
            configuration_ids={"s0": "s0-a025-v1"},
        )
        with tempfile.TemporaryDirectory() as temporary:
            V11CandidateExperimentRunner(
                repo_root=Path(temporary), protocol=PROTOCOL, request=valid
            )

        invalid = replace(valid, run_id="TUNE-V11-UNDECLARED-CONDITION", condition_id="action-failure-1of8")
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "outside the bounded predeclared tuning design"):
                V11CandidateExperimentRunner(
                    repo_root=Path(temporary), protocol=PROTOCOL, request=invalid
                )

    def test_final_execution_is_blocked_before_any_run_bundle_is_created(self) -> None:
        final_request = replace(
            request(),
            run_id="FINAL-V11-BLOCKED",
            stage=ProtocolStage.FINAL,
            layout_id="v11-final-l01",
            condition_id="nominal",
            root_seeds=PROTOCOL.root_seeds_for(ProtocolStage.FINAL),
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(ValueError, "non-final"):
                V11CandidateExperimentRunner(
                    repo_root=root, protocol=PROTOCOL, request=final_request
                )
            self.assertFalse((root / "results" / "runs" / "FINAL-V11-BLOCKED").exists())

    def test_common_checkpoint_budget_cannot_be_silently_changed(self) -> None:
        invalid = replace(request(), q_learning_rate=0.25)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "common checkpoint budget"):
                V11CandidateExperimentRunner(
                    repo_root=Path(temporary), protocol=PROTOCOL, request=invalid
                )

    def test_stage_root_bank_must_be_complete_and_predeclared(self) -> None:
        invalid = replace(request(), root_seeds=PROTOCOL.root_seeds_for(ProtocolStage.DEVELOPMENT)[:-1])
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "complete predeclared stage root bank"):
                V11CandidateExperimentRunner(
                    repo_root=Path(temporary), protocol=PROTOCOL, request=invalid
                )


if __name__ == "__main__":
    unittest.main()
