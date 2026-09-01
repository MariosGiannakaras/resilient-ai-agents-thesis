from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.contracts import ProtocolStage, RetentionPolicy  # noqa: E402
from resilient_agents.pilot_protocol import load_pilot_protocol  # noqa: E402
from resilient_agents.v11_runner import (  # noqa: E402
    V11DevelopmentProtocol,
    V11ExperimentRequest,
    V11ExperimentRunner,
)

BASE_PROTOCOL = load_pilot_protocol(ROOT / "configs" / "protocols" / "pilot-v0.1.json")


def request(
    *,
    run_id: str,
    stage: ProtocolStage = ProtocolStage.DEVELOPMENT,
    layout_id: str = "dev-l01",
    condition_id: str = "remap-min-in-set",
    agent_ids: tuple[str, ...] = ("f0", "c0", "d0"),
    dyna_planning_steps: int | None = 2,
    dyna_kappa: float | None = 0.001,
) -> V11ExperimentRequest:
    return V11ExperimentRequest(
        run_id=run_id,
        stage=stage,
        layout_id=layout_id,
        condition_id=condition_id,
        root_seeds=(12345,),
        agent_ids=agent_ids,
        q_learning_rate=0.5,
        discount_factor=0.96875,
        exploration_epsilon=0.125,
        training_episodes_per_layout=2,
        pre_change_episodes=2,
        post_change_episodes=3,
        immediate_window=1,
        worst_window=2,
        terminal_window=2,
        recovery_tolerance=1.0,
        recovery_stability_episodes=2,
        retention_policy=RetentionPolicy.EVENTS,
        auto_publish=False,
        execution_timeout_seconds=None,
        dyna_planning_steps=dyna_planning_steps,
        dyna_kappa=dyna_kappa,
    )


class V11RunnerTests(unittest.TestCase):
    def test_development_adapter_preserves_historical_protocol_and_declares_d0(self) -> None:
        before = BASE_PROTOCOL.canonical_json()
        protocol = V11DevelopmentProtocol.from_validated_base(BASE_PROTOCOL)

        self.assertEqual(BASE_PROTOCOL.canonical_json(), before)
        payload = protocol.to_dict()
        self.assertFalse(payload["scientific_scope"]["final_evidence_use"])
        self.assertTrue(protocol.protocol_version.startswith("v1.1-development-fixture-"))
        self.assertEqual(
            [item["agent_id"] for item in payload["agent_regimes"]],
            ["f0", "c0", "d0"],
        )
        d0 = payload["agent_regimes"][-1]
        self.assertEqual(d0["method"], "dyna_q_plus_v1")
        self.assertTrue(d0["post_change_learning"])

    def test_request_requires_dyna_parameters_exactly_when_d0_is_requested(self) -> None:
        with self.assertRaises(ValueError):
            request(run_id="DEV-MISSING-DYNA", dyna_planning_steps=None)
        with self.assertRaises(ValueError):
            request(run_id="DEV-MISSING-KAPPA", dyna_kappa=None)
        with self.assertRaises(ValueError):
            request(
                run_id="DEV-IRRELEVANT-DYNA",
                agent_ids=("f0",),
                dyna_planning_steps=2,
                dyna_kappa=0.001,
            )

        f0_only = request(
            run_id="DEV-F0-ONLY",
            agent_ids=("f0",),
            dyna_planning_steps=None,
            dyna_kappa=None,
        )
        self.assertEqual(V11ExperimentRequest.from_dict(f0_only.to_dict()), f0_only)

    def test_non_development_execution_fails_closed_before_run(self) -> None:
        protocol = V11DevelopmentProtocol.from_validated_base(BASE_PROTOCOL)
        tuning = request(
            run_id="TUNE-D0-BLOCKED",
            stage=ProtocolStage.TUNING,
            layout_id="tune-l01",
            condition_id="nominal",
        )
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "non-development execution is blocked"):
                V11ExperimentRunner(
                    repo_root=Path(temporary),
                    protocol=protocol,
                    request=tuning,
                )

    def test_d0_runner_executes_all_agents_and_is_deterministic(self) -> None:
        protocol = V11DevelopmentProtocol.from_validated_base(BASE_PROTOCOL)

        with tempfile.TemporaryDirectory() as first_directory:
            first = V11ExperimentRunner(
                repo_root=Path(first_directory),
                protocol=protocol,
                request=request(run_id="DEV-V11-FIRST"),
            ).run()
            first_summary = json.loads(
                (first.run_dir / "summary.json").read_text(encoding="utf-8")
            )
            first_config = json.loads(
                (first.run_dir / "resolved-config.json").read_text(encoding="utf-8")
            )

        with tempfile.TemporaryDirectory() as second_directory:
            second = V11ExperimentRunner(
                repo_root=Path(second_directory),
                protocol=protocol,
                request=request(run_id="DEV-V11-SECOND"),
            ).run()
            second_summary = json.loads(
                (second.run_dir / "summary.json").read_text(encoding="utf-8")
            )

        self.assertEqual(first_summary["status"], "completed")
        self.assertEqual(first_summary["completed_root_count"], 1)
        agent_results = first_summary["root_results"][0]["agent_results"]
        self.assertEqual([item["agent_id"] for item in agent_results], ["f0", "c0", "d0"])
        for result in agent_results:
            self.assertEqual(
                result["observed_episode_returns"][:2],
                result["reference_episode_returns"][:2],
            )
        self.assertEqual(first_config["entrypoint"], "resilient_agents.v11_runner.v1")
        self.assertEqual(first_config["protocol_lifecycle"], "development-fixture-only")
        self.assertEqual(first_config["request"]["dyna_planning_steps"], 2)
        self.assertEqual(first_config["request"]["dyna_kappa"], 0.001)

        comparable_first = first_summary["root_results"]
        comparable_second = second_summary["root_results"]
        self.assertEqual(comparable_first, comparable_second)

    def test_request_round_trip_rejects_unknown_keys(self) -> None:
        run_request = request(run_id="DEV-V11-ROUNDTRIP")
        self.assertEqual(
            V11ExperimentRequest.from_dict(run_request.to_dict()),
            run_request,
        )
        with self.assertRaises(ValueError):
            V11ExperimentRequest.from_dict(run_request.to_dict() | {"extra": True})


if __name__ == "__main__":
    unittest.main()
