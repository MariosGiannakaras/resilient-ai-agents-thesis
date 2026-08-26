from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.contracts import ProtocolStage, RetentionPolicy  # noqa: E402
from resilient_agents.experiment_runner import (  # noqa: E402
    HeadlessExperimentRequest,
    HeadlessExperimentRunner,
)
from resilient_agents.git_publish import PublishResult  # noqa: E402
from resilient_agents.pilot_protocol import load_pilot_protocol  # noqa: E402

PROTOCOL = load_pilot_protocol(ROOT / "configs" / "protocols" / "pilot-v0.1.json")


def request(
    *,
    run_id: str,
    root_seeds: tuple[int, ...],
    agent_ids: tuple[str, ...] = ("f0", "c0", "r0"),
    auto_publish: bool = False,
) -> HeadlessExperimentRequest:
    return HeadlessExperimentRequest(
        run_id=run_id,
        stage=ProtocolStage.DEVELOPMENT,
        layout_id="dev-l01",
        condition_id="remap-min-in-set",
        root_seeds=root_seeds,
        agent_ids=agent_ids,
        q_learning_rate=0.25,
        discount_factor=0.875,
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
        auto_publish=auto_publish,
    )


class HeadlessExperimentRunnerTests(unittest.TestCase):
    def test_multi_seed_all_agent_experiment_finalizes_one_auditable_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            result = HeadlessExperimentRunner(
                repo_root=repo,
                protocol=PROTOCOL,
                request=request(run_id="DEV-MULTI", root_seeds=(101, 202)),
            ).run()

            self.assertIsNone(result.publication_commit)
            self.assertTrue((result.run_dir / "FINALIZED").is_file())
            manifest = json.loads(
                (result.run_dir / "manifest.json").read_text(encoding="utf-8")
            )
            summary = json.loads(
                (result.run_dir / "summary.json").read_text(encoding="utf-8")
            )
            state = json.loads(
                (result.run_dir / "runner-state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual(summary["completed_root_count"], 2)
            self.assertEqual(state["completed_root_seeds"], [101, 202])
            for root_result in summary["root_results"]:
                self.assertEqual(
                    [item["agent_id"] for item in root_result["agent_results"]],
                    ["f0", "c0", "r0"],
                )
                for agent_result in root_result["agent_results"]:
                    self.assertEqual(
                        agent_result["observed_episode_returns"][:2],
                        agent_result["reference_episode_returns"][:2],
                    )
                    self.assertIn(
                        agent_result["metrics"]["recovery_status"],
                        {"no_degradation", "recovered", "not_recovered"},
                    )
            index_lines = (
                repo / "results" / "run-index.jsonl"
            ).read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(index_lines), 1)
            events_text = (result.run_dir / "events.jsonl").read_text()
            self.assertIn("root_completed", events_text)
            first_episode = next(
                json.loads(line)
                for line in events_text.splitlines()
                if json.loads(line).get("event") == "episode_completed"
            )
            self.assertIn("agent_exploration_seed", first_episode)
            self.assertEqual(
                set(first_episode["environment_seeds"]),
                {
                    "scenario",
                    "environment",
                    "action_disturbance",
                    "observation_disturbance",
                },
            )

            with tempfile.TemporaryDirectory() as repeat_temporary:
                repeated = HeadlessExperimentRunner(
                    repo_root=Path(repeat_temporary),
                    protocol=PROTOCOL,
                    request=request(run_id="DEV-REPEAT", root_seeds=(101, 202)),
                ).run()
                repeated_summary = json.loads(
                    (repeated.run_dir / "summary.json").read_text(encoding="utf-8")
                )
            self.assertEqual(summary["root_results"], repeated_summary["root_results"])

    def test_interruption_resumes_only_incomplete_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            run_request = request(
                run_id="DEV-RESUME",
                root_seeds=(303, 404),
                agent_ids=("f0",),
            )
            interrupted = HeadlessExperimentRunner(
                repo_root=repo, protocol=PROTOCOL, request=run_request
            )
            original = interrupted._run_root
            calls = 0

            def interrupt_second_root(*, bundle: object, root_seed: int) -> object:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise KeyboardInterrupt("simulated interruption")
                return original(bundle=bundle, root_seed=root_seed)  # type: ignore[arg-type]

            with patch.object(interrupted, "_run_root", side_effect=interrupt_second_root):
                with self.assertRaises(KeyboardInterrupt):
                    interrupted.run()

            run_dir = repo / "results" / "runs" / "DEV-RESUME"
            partial = json.loads(
                (run_dir / "runner-state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(partial["completed_root_seeds"], [303])
            self.assertFalse((run_dir / "FINALIZED").exists())

            completed = HeadlessExperimentRunner(
                repo_root=repo, protocol=PROTOCOL, request=run_request
            ).run()
            summary = json.loads(
                (completed.run_dir / "summary.json").read_text(encoding="utf-8")
            )
            state = json.loads(
                (completed.run_dir / "runner-state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["completed_root_count"], 2)
            self.assertEqual(state["completed_root_seeds"], [303, 404])
            self.assertEqual(state["resume_generation"], 1)
            self.assertIn(
                "experiment_resumed", (completed.run_dir / "events.jsonl").read_text()
            )

    def test_whole_experiment_publication_is_called_once_after_all_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            with patch(
                "resilient_agents.session.publish_finalized_run",
                return_value=PublishResult("abc123", "main", "origin"),
            ) as publisher:
                result = HeadlessExperimentRunner(
                    repo_root=repo,
                    protocol=PROTOCOL,
                    request=request(
                        run_id="DEV-PUBLISH",
                        root_seeds=(505, 606),
                        agent_ids=("f0",),
                        auto_publish=True,
                    ),
                ).run()
            self.assertEqual(result.publication_commit, "abc123")
            publisher.assert_called_once_with(repo_root=repo.resolve(), run_id="DEV-PUBLISH")
            self.assertTrue((result.run_dir / "FINALIZED").is_file())

    def test_final_stage_and_mismatched_resume_fail_closed(self) -> None:
        round_trip = request(run_id="ROUND-TRIP", root_seeds=(1,))
        self.assertEqual(
            HeadlessExperimentRequest.from_dict(round_trip.to_dict()), round_trip
        )
        with self.assertRaises(ValueError):
            HeadlessExperimentRequest.from_dict(round_trip.to_dict() | {"extra": True})

        with self.assertRaises(ValueError):
            HeadlessExperimentRunner(
                repo_root=ROOT,
                protocol=PROTOCOL,
                request=HeadlessExperimentRequest(
                    **(
                        request(run_id="FINAL-BLOCKED", root_seeds=(1,)).to_dict()
                        | {
                            "stage": ProtocolStage.FINAL,
                            "layout_id": "final-l01",
                            "retention_policy": RetentionPolicy.EVENTS,
                        }
                    )
                ),
            )

        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            first = request(
                run_id="DEV-MISMATCH", root_seeds=(707, 808), agent_ids=("f0",)
            )
            runner = HeadlessExperimentRunner(
                repo_root=repo, protocol=PROTOCOL, request=first
            )
            with patch.object(runner, "_run_root", side_effect=KeyboardInterrupt()):
                with self.assertRaises(KeyboardInterrupt):
                    runner.run()
            changed = request(
                run_id="DEV-MISMATCH", root_seeds=(707, 909), agent_ids=("f0",)
            )
            with self.assertRaises(RuntimeError):
                HeadlessExperimentRunner(
                    repo_root=repo, protocol=PROTOCOL, request=changed
                ).run()

    def test_corrupted_resume_log_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            run_request = request(
                run_id="DEV-CORRUPT", root_seeds=(1001,), agent_ids=("f0",)
            )
            runner = HeadlessExperimentRunner(
                repo_root=repo, protocol=PROTOCOL, request=run_request
            )
            with patch.object(runner, "_run_root", side_effect=KeyboardInterrupt()):
                with self.assertRaises(KeyboardInterrupt):
                    runner.run()
            events = repo / "results" / "runs" / "DEV-CORRUPT" / "events.jsonl"
            with events.open("a", encoding="utf-8") as handle:
                handle.write("{incomplete")
            with self.assertRaises(RuntimeError):
                HeadlessExperimentRunner(
                    repo_root=repo, protocol=PROTOCOL, request=run_request
                ).run()


if __name__ == "__main__":
    unittest.main()
