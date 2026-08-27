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
from resilient_agents.runtime_observer import (  # noqa: E402
    ObservedV11DevelopmentRunner,
    RuntimeTelemetrySink,
)
from resilient_agents.v11_runner import (  # noqa: E402
    V11DevelopmentProtocol,
    V11ExperimentRequest,
    V11ExperimentRunner,
)

BASE = load_pilot_protocol(ROOT / "configs" / "protocols" / "pilot-v0.1.json")
PROTOCOL = V11DevelopmentProtocol.from_validated_base(BASE)


def request(run_id: str) -> V11ExperimentRequest:
    return V11ExperimentRequest(
        run_id=run_id,
        stage=ProtocolStage.DEVELOPMENT,
        layout_id="dev-l01",
        condition_id="remap-min-in-set",
        root_seeds=(12345,),
        agent_ids=("f0", "c0", "d0"),
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
        dyna_planning_steps=2,
        dyna_kappa=0.001,
    )


class RuntimeObserverTests(unittest.TestCase):
    def test_observer_on_off_produces_identical_scientific_root_results(self) -> None:
        with tempfile.TemporaryDirectory() as plain_dir:
            plain = V11ExperimentRunner(
                repo_root=Path(plain_dir),
                protocol=PROTOCOL,
                request=request("PLAIN"),
            ).run()
            plain_summary = json.loads(
                (plain.run_dir / "summary.json").read_text(encoding="utf-8")
            )

        with tempfile.TemporaryDirectory() as observed_dir:
            root = Path(observed_dir)
            telemetry = root / "runtime.ndjson"
            observed = ObservedV11DevelopmentRunner(
                repo_root=root,
                protocol=PROTOCOL,
                request=request("OBSERVED"),
                runtime_telemetry_sink=RuntimeTelemetrySink(telemetry),
            ).run()
            observed_summary = json.loads(
                (observed.run_dir / "summary.json").read_text(encoding="utf-8")
            )
            rows = [
                json.loads(line)
                for line in telemetry.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]

        self.assertEqual(plain_summary["root_results"], observed_summary["root_results"])
        self.assertGreater(len(rows), 0)
        self.assertEqual([row["sequence"] for row in rows], list(range(len(rows))))
        step_rows = [row for row in rows if row["event"] == "gridworld_step"]
        self.assertGreater(len(step_rows), 0)
        first = step_rows[0]
        self.assertIn("true_state", first)
        self.assertIn("delivered_observation", first)
        self.assertIn("intended_action", first)
        self.assertIn("executed_action", first)
        self.assertIn("disturbance_flags", first)

    def test_live_telemetry_is_separate_from_scientific_retention(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            telemetry = root / "runtime.ndjson"
            result = ObservedV11DevelopmentRunner(
                repo_root=root,
                protocol=PROTOCOL,
                request=request("EVENTS-ONLY"),
                runtime_telemetry_sink=RuntimeTelemetrySink(telemetry),
            ).run()
            self.assertTrue(telemetry.is_file())
            self.assertFalse((result.run_dir / "trace.jsonl").exists())

    def test_telemetry_writer_rejects_non_json_finite_values(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            sink = RuntimeTelemetrySink(Path(temporary) / "events.ndjson")
            with self.assertRaises(ValueError):
                sink.emit({"event": "bad", "value": float("nan")})


if __name__ == "__main__":
    unittest.main()
