from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app.state import (  # noqa: E402
    AGENT_PROFILES,
    ApplicationReadModel,
    CandidateConfigurationOption,
    CandidateExperimentForm,
    layout_label,
    setting_rows,
)
from resilient_agents.contracts import ProtocolStage  # noqa: E402


class ApplicationStateTests(unittest.TestCase):
    def _model(self, root: Path) -> ApplicationReadModel:
        target = root / "configs" / "protocols" / "protocol-v1.1.json"
        target.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "configs" / "protocols" / "protocol-v1.1.json", target)
        return ApplicationReadModel(root)

    def test_primary_strategy_profiles_use_five_human_readable_names(self) -> None:
        self.assertEqual(
            tuple(profile.name for profile in AGENT_PROFILES),
            (
                "Fixed Q-Learning",
                "Adaptive Q-Learning",
                "SARSA",
                "Dyna-Q",
                "Dyna-Q+",
            ),
        )
        for profile in AGENT_PROFILES:
            self.assertNotIn("F0", profile.name)
            self.assertNotIn("C0", profile.name)
            self.assertNotIn("D0", profile.name)
            self.assertTrue(profile.mechanism_badge)
            self.assertTrue(profile.description)

    def test_candidate_catalog_exposes_only_bounded_protocol_configurations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            model = self._model(Path(temporary))
            options = model.candidate_configuration_options(
                stage=ProtocolStage.TUNING
            )
            self.assertEqual(tuple(options), ("f0", "c0", "s0", "dq0", "d0"))
            self.assertEqual(len(options["f0"]), 1)
            self.assertEqual(len(options["c0"]), 1)
            self.assertEqual(len(options["s0"]), 2)
            self.assertEqual(len(options["dq0"]), 2)
            self.assertEqual(len(options["d0"]), 4)
            for agent_id, values in options.items():
                for option in values:
                    self.assertEqual(option.agent_id, agent_id)
                    self.assertEqual(len(option.sha256), 64)

    def test_resolved_request_uses_complete_stage_root_bank_and_common_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            model = self._model(Path(temporary))
            request = model.resolved_candidate_request(
                CandidateExperimentForm(
                    run_id="APP-STATE-TEST",
                    stage=ProtocolStage.DEVELOPMENT,
                    layout_id="dev-l01",
                    condition_id="action-remap-2-swap",
                    agent_configuration_ids={
                        "f0": "f0-base-v1",
                        "s0": "s0-a025-v1",
                        "d0": "d0-p05-k0005-v1",
                    },
                )
            )
            self.assertEqual(
                tuple(request.root_seeds),
                model.stage_root_seeds(ProtocolStage.DEVELOPMENT),
            )
            self.assertEqual(request.agent_ids, ("f0", "s0", "d0"))
            self.assertEqual(request.q_learning_rate, 0.5)
            self.assertEqual(request.discount_factor, 0.96875)
            self.assertEqual(request.exploration_epsilon, 0.125)
            self.assertEqual(request.training_episodes_per_layout, 512)
            self.assertEqual(request.pre_change_episodes, 16)
            self.assertEqual(request.post_change_episodes, 32)

    def test_final_stage_and_invalid_configuration_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            model = self._model(Path(temporary))
            with self.assertRaisesRegex(ValueError, "development/tuning"):
                model.resolved_candidate_request(
                    CandidateExperimentForm(
                        run_id="APP-FINAL-BLOCKED",
                        stage=ProtocolStage.FINAL,
                        layout_id="v11-final-l01",
                        condition_id="nominal",
                        agent_configuration_ids={"f0": "f0-base-v1"},
                    )
                )
            invalid = model.resolved_candidate_request(
                CandidateExperimentForm(
                    run_id="APP-CONFIG-BAD",
                    stage=ProtocolStage.DEVELOPMENT,
                    layout_id="dev-l01",
                    condition_id="nominal",
                    agent_configuration_ids={"s0": "c0-base-v1"},
                )
            )
            with self.assertRaisesRegex(ValueError, "does not belong"):
                model.runtime.enqueue_v11_candidate(
                    protocol_path=model.v11_protocol_path,
                    request=invalid.to_dict(),
                )

    def test_plain_layout_and_setting_presentations_keep_ids_secondary(self) -> None:
        self.assertEqual(layout_label("dev-l01"), "Development layout 1")
        first = CandidateConfigurationOption(
            configuration_id="internal-a",
            agent_id="s0",
            strategy_name="SARSA",
            settings={"learning_rate": 0.25, "discount_factor": 0.96875},
            sha256="a" * 64,
        )
        second = CandidateConfigurationOption(
            configuration_id="internal-b",
            agent_id="s0",
            strategy_name="SARSA",
            settings={"learning_rate": 0.5, "discount_factor": 0.96875},
            sha256="b" * 64,
        )
        rows = setting_rows(first, (first, second))
        self.assertEqual(rows[0]["setting"], "Learning responsiveness")
        self.assertEqual(rows[0]["availability"], "Tunable across approved choices")
        self.assertEqual(rows[1]["availability"], "Fixed by protocol")
        self.assertNotIn("internal-a", str(rows))

    def test_artifact_preview_reads_exact_stored_csv_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model = self._model(root)
            artifact = root / "results" / "thesis-final" / "artifacts" / "stored.csv"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("name,value\nFixed Q-Learning,3\n", encoding="utf-8")
            manifest = artifact.parent.parent / "freeze-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "protocol_version": "protocol-v1.0",
                        "freeze_time_utc": "2026-01-01T00:00:00+00:00",
                        "included_runs": 1,
                        "total_final_runs_found": 1,
                        "provenance_archive_ref": "archive",
                    }
                ),
                encoding="utf-8",
            )
            inventory = {item["name"]: item for item in model.thesis_final_artifacts()}
            self.assertEqual(len(inventory["stored.csv"]["sha256"]), 64)
            preview = model.artifact_preview("stored.csv")
            self.assertEqual(preview["kind"], "csv")
            self.assertEqual(preview["rows"], [{"name": "Fixed Q-Learning", "value": 3}])

    def test_historical_trace_never_promotes_episode_summaries_to_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model = self._model(root)
            first = root / "results" / "runs" / "NO-TRACE" / "events.jsonl"
            first.parent.mkdir(parents=True)
            first.write_text('{"event":"episode_completed"}\n', encoding="utf-8")
            second = root / "results" / "runs" / "REAL-TRACE" / "events.jsonl"
            second.parent.mkdir(parents=True)
            second.write_text('{"event": "gridworld_step", "sequence": 1}\n', encoding="utf-8")
            self.assertFalse(model.historical_trace_available("NO-TRACE"))
            self.assertTrue(model.historical_trace_available("REAL-TRACE"))

    def test_historical_identity_uses_full_strategy_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model = self._model(root)
            run = root / "results" / "runs" / "FINAL-TEST"
            run.mkdir(parents=True)
            (run / "manifest.json").write_text(
                json.dumps(
                    {
                        "run_id": "FINAL-TEST",
                        "protocol_version": "protocol-v1.0",
                        "stage": "final",
                        "source": {"git_commit": "abc"},
                    }
                ),
                encoding="utf-8",
            )
            (run / "resolved-config.json").write_text(
                json.dumps(
                    {
                        "request": {
                            "run_id": "FINAL-TEST",
                            "stage": "final",
                            "layout_id": "final-l01",
                            "condition_id": "nominal",
                            "agent_ids": ["f0", "c0"],
                            "retention_policy": "events",
                        }
                    }
                ),
                encoding="utf-8",
            )
            identity = model.run_identity("FINAL-TEST")
            assert identity is not None
            self.assertEqual(identity["strategy_names"], ("Fixed Q-Learning", "Adaptive Q-Learning"))


if __name__ == "__main__":
    unittest.main()
