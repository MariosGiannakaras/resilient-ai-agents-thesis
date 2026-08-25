from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import (  # noqa: E402
    ChangeEvent,
    GroundTruthTransition,
    InformationPolicy,
    ProtocolStage,
    project_for_agent,
)
from resilient_agents.git_publish import PublishError, publish_finalized_run  # noqa: E402
from resilient_agents.metrics import compute_resilience_metrics  # noqa: E402
from resilient_agents.protocol import ProtocolPartition, assert_stage_access  # noqa: E402
from resilient_agents.randomness import RandomStreams, derive_seed  # noqa: E402
from resilient_agents.run_bundle import RunBundle  # noqa: E402


class InformationBoundaryTests(unittest.TestCase):
    def test_hidden_ground_truth_is_not_exposed_by_strict_policy(self) -> None:
        policy = InformationPolicy(False, False, False, False, False)
        truth = GroundTruthTransition(
            step=4,
            true_state=(3, 2),
            delivered_observation=(2, 2),
            intended_action="right",
            executed_action="up",
            reward=-1.0,
            terminated=False,
            truncated=False,
            regime_id="post-change",
            disturbance_flags={"action_failure": True},
            change_event_ids=("change-1",),
        )
        visible = project_for_agent(truth, policy)
        self.assertEqual(visible.observation, (2, 2))
        self.assertEqual(visible.optional_information, {})

    def test_explicit_policy_exposes_only_requested_information(self) -> None:
        policy = InformationPolicy(True, True, False, False, False)
        truth = GroundTruthTransition(
            step=1,
            true_state=2,
            delivered_observation=1,
            intended_action=0,
            executed_action=1,
            reward=0.0,
            terminated=False,
            truncated=False,
            regime_id="r1",
            disturbance_flags={"action_failure": True},
        )
        visible = project_for_agent(truth, policy)
        self.assertEqual(visible.optional_information["executed_action"], 1)
        self.assertIn("disturbance_flags", visible.optional_information)
        self.assertNotIn("true_state", visible.optional_information)


class ChangeEventTests(unittest.TestCase):
    def test_change_event_rejects_negative_onset(self) -> None:
        with self.assertRaises(ValueError):
            ChangeEvent("c", "dynamics", -1, True, "transition", {}, {}, {})


class RandomStreamTests(unittest.TestCase):
    def test_streams_are_deterministic_and_independent(self) -> None:
        first = RandomStreams(42)
        second = RandomStreams(42)
        self.assertEqual(first.derived_seeds(), second.derived_seeds())
        seeds = list(first.derived_seeds().values())
        self.assertEqual(len(seeds), len(set(seeds)))
        self.assertEqual(derive_seed(42, "environment"), second.derived_seeds()["environment"])

    def test_unknown_stream_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            derive_seed(1, "shared-randomness")


class MetricTests(unittest.TestCase):
    def test_known_answer_recovery(self) -> None:
        metrics = compute_resilience_metrics(
            [10.0, 10.0, 4.0, 7.0, 9.0, 10.0],
            change_index=2,
            recovery_fraction=0.9,
            reference_value=None,
        )
        self.assertEqual(metrics.nominal_mean, 10.0)
        self.assertEqual(metrics.immediate_degradation, 6.0)
        self.assertEqual(metrics.worst_degradation, 6.0)
        self.assertEqual(metrics.recovery_step, 4)

    def test_non_recovery_is_none_not_horizon(self) -> None:
        metrics = compute_resilience_metrics(
            [10.0, 10.0, 4.0, 5.0, 6.0],
            change_index=2,
            recovery_fraction=0.9,
            reference_value=None,
        )
        self.assertIsNone(metrics.recovery_step)


class ProtocolFirewallTests(unittest.TestCase):
    def test_partitions_must_not_overlap(self) -> None:
        partition = ProtocolPartition(["d"], ["t"], ["p"], ["p"])
        with self.assertRaises(ValueError):
            partition.validate()

    def test_final_stage_cannot_access_tuning_scenario(self) -> None:
        partition = ProtocolPartition(["d"], ["t"], ["p"], ["f"])
        with self.assertRaises(ValueError):
            assert_stage_access(stage=ProtocolStage.FINAL, scenario_ids=["t"], partition=partition)


class RunBundleTests(unittest.TestCase):
    def test_completed_bundle_contains_provenance_and_checksums(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "results" / "runs").mkdir(parents=True)
            bundle = RunBundle(
                repo_root=root,
                run_id="EXP-TEST-001",
                resolved_config={"seed": 1},
                protocol_version="protocol-v0.1",
                stage="development",
                retention_policy="full-trace",
            )
            bundle.append_event({"step": 1, "event": "change"})
            bundle.append_trace({"step": 1, "state": [0, 0]})
            run_dir = bundle.finalize(status="completed", summary={"return": 1.0})
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "completed")
            self.assertIn("resolved-config.json", manifest["files"])
            self.assertIn("system-capability.json", manifest["files"])
            self.assertTrue((run_dir / "checksums.sha256").is_file())
            self.assertTrue((run_dir / "FINALIZED").is_file())
            index = (root / "results" / "run-index.jsonl").read_text(encoding="utf-8")
            self.assertIn("EXP-TEST-001", index)

            with self.assertRaises(RuntimeError):
                bundle.append_event({"step": 2, "event": "late-mutation"})

    def test_noncanonical_complete_alias_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = RunBundle(
                repo_root=root,
                run_id="EXP-OLD-STATUS",
                resolved_config={"seed": 1},
                protocol_version="protocol-v0.1",
                stage="development",
                retention_policy="events",
            )
            with self.assertRaises(ValueError):
                bundle.finalize(status="complete", summary={"return": 1.0})


class GitPublicationTests(unittest.TestCase):
    def _git(self, root: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def _initialize_repo(self, base: Path) -> tuple[Path, str]:
        remote = base / "remote.git"
        repo = base / "repo"
        subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
        subprocess.run(["git", "init", "-b", "main", str(repo)], check=True, capture_output=True)
        self._git(repo, "config", "user.email", "test@example.invalid")
        self._git(repo, "config", "user.name", "Test Runner")
        self._git(repo, "remote", "add", "origin", str(remote))
        (repo / "README.md").write_text("test\n", encoding="utf-8")
        self._git(repo, "add", "README.md")
        self._git(repo, "commit", "-m", "initial")
        self._git(repo, "push", "-u", "origin", "main")
        return repo, self._git(repo, "rev-parse", "HEAD")

    def test_finalized_experiment_creates_one_commit_and_push(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, source_commit = self._initialize_repo(Path(temporary))

            bundle = RunBundle(
                repo_root=repo,
                run_id="EXP-001",
                resolved_config={"seeds": [1, 2, 3]},
                protocol_version="protocol-v0.1",
                stage="pilot",
                retention_policy="events",
            )
            for seed in (1, 2, 3):
                bundle.append_event({"seed": seed, "event": "completed"})
            bundle.finalize(status="completed", summary={"seeds_completed": 3})
            result = publish_finalized_run(repo_root=repo, run_id="EXP-001")

            self.assertNotEqual(result.commit, source_commit)
            self.assertEqual(self._git(repo, "rev-list", "--count", f"{source_commit}..HEAD"), "1")
            self.assertEqual(self._git(repo, "rev-parse", "origin/main"), result.commit)
            message = self._git(repo, "log", "-1", "--pretty=%B")
            self.assertIn("experiment: completed EXP-001", message)
            self.assertIn("Run-ID: EXP-001", message)
            self.assertIn(f"Source-Commit: {source_commit}", message)

    def test_corrupted_finalized_bundle_is_not_published(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, source_commit = self._initialize_repo(Path(temporary))
            bundle = RunBundle(
                repo_root=repo,
                run_id="EXP-CORRUPT",
                resolved_config={"seeds": [1]},
                protocol_version="protocol-v0.1",
                stage="pilot",
                retention_policy="events",
            )
            bundle.append_event({"seed": 1, "event": "completed"})
            run_dir = bundle.finalize(status="completed", summary={"seeds_completed": 1})
            (run_dir / "summary.json").write_text('{"seeds_completed": 999}\n', encoding="utf-8")

            with self.assertRaises(PublishError):
                publish_finalized_run(repo_root=repo, run_id="EXP-CORRUPT")

            self.assertEqual(self._git(repo, "rev-parse", "HEAD"), source_commit)
            self.assertEqual(self._git(repo, "rev-parse", "origin/main"), source_commit)

    def test_finalization_marker_and_index_must_match_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, source_commit = self._initialize_repo(Path(temporary))
            bundle = RunBundle(
                repo_root=repo,
                run_id="EXP-FINALIZATION",
                resolved_config={"seeds": [1]},
                protocol_version="protocol-v0.1",
                stage="pilot",
                retention_policy="events",
            )
            bundle.append_event({"seed": 1, "event": "completed"})
            run_dir = bundle.finalize(status="completed", summary={"seeds_completed": 1})

            marker = run_dir / "FINALIZED"
            marker.write_text("schema_version=1\nstatus=failed\n", encoding="utf-8")
            with self.assertRaises(PublishError):
                publish_finalized_run(repo_root=repo, run_id="EXP-FINALIZATION")

            marker.write_text("schema_version=1\nstatus=completed\n", encoding="utf-8")
            index_path = repo / "results" / "run-index.jsonl"
            index = index_path.read_text(encoding="utf-8")
            index_path.write_text(
                index.replace('"status": "completed"', '"status": "failed"'),
                encoding="utf-8",
            )
            with self.assertRaises(PublishError):
                publish_finalized_run(repo_root=repo, run_id="EXP-FINALIZATION")

            self.assertEqual(self._git(repo, "rev-parse", "HEAD"), source_commit)
            self.assertEqual(self._git(repo, "rev-parse", "origin/main"), source_commit)


if __name__ == "__main__":
    unittest.main()
