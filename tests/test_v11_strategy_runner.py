from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.contracts import ProtocolStage, RetentionPolicy  # noqa: E402
from resilient_agents.pilot_protocol import load_pilot_protocol  # noqa: E402
from resilient_agents.v11_strategy_runner import (  # noqa: E402
    MAIN_STRATEGY_IDS,
    BroadenedV11DevelopmentProtocol,
    BroadenedV11ExperimentRequest,
    BroadenedV11ExperimentRunner,
)

BASE_PROTOCOL = load_pilot_protocol(ROOT / "configs" / "protocols" / "pilot-v0.1.json")


def request(
    *,
    run_id: str,
    agent_ids: tuple[str, ...] = MAIN_STRATEGY_IDS,
    dyna_planning_steps: int | None = 1,
    dyna_kappa: float | None = 0.001,
) -> BroadenedV11ExperimentRequest:
    return BroadenedV11ExperimentRequest(
        run_id=run_id,
        stage=ProtocolStage.DEVELOPMENT,
        layout_id="dev-l01",
        condition_id="remap-min-in-set",
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


class BroadenedV11RunnerTests(unittest.TestCase):
    def test_protocol_declares_five_main_strategies_without_mutating_base(self) -> None:
        before = BASE_PROTOCOL.canonical_json()
        protocol = BroadenedV11DevelopmentProtocol.from_validated_base(BASE_PROTOCOL)
        self.assertEqual(BASE_PROTOCOL.canonical_json(), before)
        regimes = protocol.to_dict()["agent_regimes"]
        self.assertEqual(tuple(item["agent_id"] for item in regimes), MAIN_STRATEGY_IDS)
        methods = {item["agent_id"]: item["method"] for item in regimes}
        self.assertEqual(methods["s0"], "sarsa_v1")
        self.assertEqual(methods["dq0"], "dyna_q_v1")
        self.assertEqual(methods["d0"], "dyna_q_plus_v1")

    def test_request_applies_dyna_parameters_only_to_planning_strategies(self) -> None:
        with self.assertRaises(ValueError):
            request(
                run_id="DEV-DQ-MISSING-PLANNING",
                agent_ids=("dq0",),
                dyna_planning_steps=None,
                dyna_kappa=None,
            )
        dq_only = request(
            run_id="DEV-DQ-ONLY",
            agent_ids=("dq0",),
            dyna_planning_steps=2,
            dyna_kappa=None,
        )
        self.assertEqual(dq_only.dyna_planning_steps, 2)
        with self.assertRaises(ValueError):
            request(
                run_id="DEV-DQ-WITH-KAPPA",
                agent_ids=("dq0",),
                dyna_planning_steps=2,
                dyna_kappa=0.001,
            )
        with self.assertRaises(ValueError):
            request(
                run_id="DEV-DPLUS-MISSING-KAPPA",
                agent_ids=("d0",),
                dyna_planning_steps=2,
                dyna_kappa=None,
            )
        sarsa_only = request(
            run_id="DEV-SARSA-ONLY",
            agent_ids=("s0",),
            dyna_planning_steps=None,
            dyna_kappa=None,
        )
        self.assertEqual(
            BroadenedV11ExperimentRequest.from_dict(sarsa_only.to_dict()),
            sarsa_only,
        )

    def test_five_strategy_runner_executes_matched_pre_change_and_is_deterministic(self) -> None:
        protocol = BroadenedV11DevelopmentProtocol.from_validated_base(BASE_PROTOCOL)

        with tempfile.TemporaryDirectory() as first_directory:
            first = BroadenedV11ExperimentRunner(
                repo_root=Path(first_directory),
                protocol=protocol,
                request=request(run_id="DEV-FIVE-FIRST"),
            ).run()
            first_summary = json.loads(
                (first.run_dir / "summary.json").read_text(encoding="utf-8")
            )
            first_config = json.loads(
                (first.run_dir / "resolved-config.json").read_text(encoding="utf-8")
            )

        with tempfile.TemporaryDirectory() as second_directory:
            second = BroadenedV11ExperimentRunner(
                repo_root=Path(second_directory),
                protocol=protocol,
                request=request(run_id="DEV-FIVE-SECOND"),
            ).run()
            second_summary = json.loads(
                (second.run_dir / "summary.json").read_text(encoding="utf-8")
            )

        agent_results = first_summary["root_results"][0]["agent_results"]
        self.assertEqual(tuple(item["agent_id"] for item in agent_results), MAIN_STRATEGY_IDS)
        for result in agent_results:
            self.assertEqual(
                result["observed_episode_returns"][:2],
                result["reference_episode_returns"][:2],
            )
        self.assertEqual(
            first_config["agent_strategy_names"],
            {
                "f0": "Fixed Q-Learning",
                "c0": "Adaptive Q-Learning",
                "s0": "SARSA",
                "dq0": "Dyna-Q",
                "d0": "Dyna-Q+",
            },
        )
        self.assertEqual(
            first_summary["root_results"], second_summary["root_results"]
        )


if __name__ == "__main__":
    unittest.main()
