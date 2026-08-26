from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.analysis import (
    build_analysis_payload,
    derive_completed_run_records,
    validate_analysis,
    write_analysis,
)
from resilient_agents.contracts import ProtocolStage, RetentionPolicy
from resilient_agents.experiment_runner import (
    HeadlessExperimentRequest,
    HeadlessExperimentRunner,
)
from resilient_agents.git_publish import PublishError
from resilient_agents.pilot_protocol import load_pilot_protocol
from resilient_agents.run_bundle import RunBundle

PROTOCOL = load_pilot_protocol(ROOT / "configs" / "protocols" / "pilot-v0.1.json")


def development_request(run_id: str) -> HeadlessExperimentRequest:
    return HeadlessExperimentRequest(
        run_id=run_id,
        stage=ProtocolStage.DEVELOPMENT,
        layout_id="dev-l02",
        condition_id="remap-max-out-of-set",
        root_seeds=(11, 22),
        agent_ids=("f0", "c0", "r0"),
        q_learning_rate=0.25,
        discount_factor=0.875,
        exploration_epsilon=0.125,
        training_episodes_per_layout=2,
        pre_change_episodes=2,
        post_change_episodes=8,
        immediate_window=1,
        worst_window=2,
        terminal_window=4,
        recovery_tolerance=1.0,
        recovery_stability_episodes=2,
        retention_policy=RetentionPolicy.EVENTS,
        auto_publish=False,
    )


class ReproducibleAnalysisTests(unittest.TestCase):
    def _run(self, repo: Path, run_id: str = "DEV-ANALYSIS") -> Path:
        return (
            HeadlessExperimentRunner(
                repo_root=repo,
                protocol=PROTOCOL,
                request=development_request(run_id),
            )
            .run()
            .run_dir
        )

    def test_finalized_bundle_produces_deterministic_units_and_sensitivity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._run(repo)
            first = build_analysis_payload(
                repo_root=repo,
                analysis_id="ANALYSIS-DEV",
                run_ids=("DEV-ANALYSIS",),
            )
            second = build_analysis_payload(
                repo_root=repo,
                analysis_id="ANALYSIS-DEV",
                run_ids=("DEV-ANALYSIS",),
            )
            self.assertEqual(first, second)
            payload, units, sensitivity = first
            self.assertEqual(payload["valid_unit_count"], 6)
            self.assertEqual(len(units), 6)
            self.assertEqual(len(sensitivity), 6 * 54)
            self.assertEqual(payload["sensitivity_record_count"], 324)
            self.assertEqual(len(payload["sensitivity_aggregates"]), 3 * 54)
            self.assertEqual(
                [item["agent_id"] for item in payload["primary_aggregates"]],
                ["c0", "f0", "r0"],
            )
            self.assertTrue(
                all(
                    unit["observed_episode_returns"][:2]
                    == unit["reference_episode_returns"][:2]
                    for unit in units
                )
            )
            frozen_units = [unit for unit in units if unit["agent_id"] == "f0"]
            self.assertTrue(
                all(
                    unit["starting_scientific_state_sha256"]
                    == unit["reference_final_state_sha256"]
                    == unit["observed_final_state_sha256"]
                    for unit in frozen_units
                )
            )
            self.assertTrue(
                all(
                    aggregate["metric_sample_standard_deviations"]["cumulative_deficit"]
                    is not None
                    for aggregate in payload["primary_aggregates"]
                )
            )
            self.assertGreaterEqual(
                payload["operational_diagnostics"][0]["wall_clock_seconds"], 0.0
            )

            result = write_analysis(
                repo_root=repo,
                analysis_id="ANALYSIS-DEV",
                run_ids=("DEV-ANALYSIS",),
            )
            self.assertEqual(result.unit_count, 6)
            self.assertEqual(result.sensitivity_record_count, 324)
            self.assertTrue((result.analysis_dir / "FINALIZED").is_file())
            self.assertTrue((result.analysis_dir / "manifest.json").is_file())
            validated = validate_analysis(analysis_dir=result.analysis_dir)
            self.assertEqual(validated["analysis_id"], "ANALYSIS-DEV")
            self.assertEqual(
                len((result.analysis_dir / "units.jsonl").read_text().splitlines()), 6
            )
            self.assertEqual(
                len(
                    (result.analysis_dir / "sensitivity.jsonl").read_text().splitlines()
                ),
                324,
            )
            with self.assertRaises(FileExistsError):
                write_analysis(
                    repo_root=repo,
                    analysis_id="ANALYSIS-DEV",
                    run_ids=("DEV-ANALYSIS",),
                )
            (result.analysis_dir / "units.jsonl").write_text("{}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_analysis(analysis_dir=result.analysis_dir)

    def test_stored_metric_drift_fails_semantic_reproduction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            run_dir = self._run(repo)
            manifest = json.loads((run_dir / "manifest.json").read_text())
            resolved = json.loads((run_dir / "resolved-config.json").read_text())
            summary = json.loads((run_dir / "summary.json").read_text())
            changed = copy.deepcopy(summary)
            changed["root_results"][0]["agent_results"][0]["metrics"][
                "cumulative_deficit"
            ] += 1.0
            with self.assertRaises(ValueError):
                derive_completed_run_records(
                    run_id="DEV-ANALYSIS",
                    manifest=manifest,
                    resolved_config=resolved,
                    summary=changed,
                    repo_root=repo,
                )

    def test_bundle_integrity_corruption_is_rejected_before_analysis(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            run_dir = self._run(repo)
            (run_dir / "summary.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaises(PublishError):
                build_analysis_payload(
                    repo_root=repo,
                    analysis_id="ANALYSIS-CORRUPT",
                    run_ids=("DEV-ANALYSIS",),
                )

    def test_failed_runs_remain_visible_but_create_no_scientific_units(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._run(repo)
            failed = RunBundle(
                repo_root=repo,
                run_id="DEV-FAILED",
                resolved_config={"fixture": "explicit failure"},
                protocol_version="pilot-v0.1",
                stage="development",
                retention_policy="events",
            )
            failed.finalize(
                status="failed",
                summary={
                    "failure": {
                        "type": "FixtureFailure",
                        "message": "retained test failure",
                    }
                },
            )
            payload, units, sensitivity = build_analysis_payload(
                repo_root=repo,
                analysis_id="ANALYSIS-WITH-FAILURE",
                run_ids=("DEV-FAILED", "DEV-ANALYSIS"),
            )
            self.assertEqual(payload["completed_run_count"], 1)
            self.assertEqual(payload["noncompleted_run_count"], 1)
            self.assertEqual(len(units), 6)
            self.assertEqual(len(sensitivity), 324)
            failed_inventory = next(
                item
                for item in payload["run_inventory"]
                if item["run_id"] == "DEV-FAILED"
            )
            self.assertEqual(failed_inventory["status"], "failed")
            self.assertEqual(failed_inventory["unit_count"], 0)
            self.assertEqual(failed_inventory["failure"]["type"], "FixtureFailure")


if __name__ == "__main__":
    unittest.main()
