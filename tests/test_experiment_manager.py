"""Tests for the experiment manager using real RunBundle finalization semantics."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.experiment_manager import (
    ExperimentRegistry,
    acquire_single_writer_lock,
    _validate_bundle_integrity,
)
from resilient_agents.run_bundle import FINALIZATION_MARKER, RunBundle


def _create_finalized_bundle(
    repo_root: Path,
    run_id: str,
    *,
    status: str = "completed",
    protocol_version: str = "test-v1",
    stage: str = "development",
) -> Path:
    """Create a real finalized bundle using RunBundle.finalize."""
    bundle = RunBundle(
        repo_root=repo_root,
        run_id=run_id,
        resolved_config={"test": True, "agent": "c0"},
        protocol_version=protocol_version,
        stage=stage,
        retention_policy="events-plus-episode-curves",
    )
    bundle.append_event({"step": 1, "reward": -1.0})
    return bundle.finalize(
        status=status,
        summary={"total_reward": -1.0, "episodes": 1},
    )


class TestSingleWriterLock(unittest.TestCase):
    def test_acquire_and_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            with acquire_single_writer_lock(repo_root):
                self.assertTrue(
                    (repo_root / "results" / ".publish.lock").is_dir()
                )
            self.assertFalse(
                (repo_root / "results" / ".publish.lock").exists()
            )


class TestBundleIntegrity(unittest.TestCase):
    def test_valid_finalized_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            run_dir = _create_finalized_bundle(repo_root, "TEST-RUN-01")
            manifest = _validate_bundle_integrity(run_dir, "TEST-RUN-01")
            self.assertEqual(manifest["run_id"], "TEST-RUN-01")
            self.assertEqual(manifest["status"], "completed")

    def test_unfinished_bundle_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            # Create a bundle but don't finalize it
            bundle = RunBundle(
                repo_root=repo_root,
                run_id="TEST-UNFIN",
                resolved_config={"test": True},
                protocol_version="test-v1",
                stage="development",
                retention_policy="events-plus-episode-curves",
            )
            run_dir = bundle.run_dir
            with self.assertRaises(ValueError) as ctx:
                _validate_bundle_integrity(run_dir, "TEST-UNFIN")
            self.assertIn("no finalization marker", str(ctx.exception))

    def test_tampered_manifest_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            run_dir = _create_finalized_bundle(repo_root, "TEST-TAMPER")
            # Tamper with the manifest
            manifest_path = run_dir / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["run_id"] = "WRONG-ID"
            manifest_path.write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            with self.assertRaises(ValueError) as ctx:
                _validate_bundle_integrity(run_dir, "TEST-TAMPER")
            self.assertIn("run_id mismatch", str(ctx.exception))


class TestExperimentRegistry(unittest.TestCase):
    def test_rebuild_with_finalized_and_unfinished(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)

            # Finalized run
            _create_finalized_bundle(repo_root, "TEST-FIN-01")

            # Unfinished run (no finalization marker)
            RunBundle(
                repo_root=repo_root,
                run_id="TEST-UNFIN-01",
                resolved_config={"test": True},
                protocol_version="test-v1",
                stage="development",
                retention_policy="events-plus-episode-curves",
            )

            registry = ExperimentRegistry(repo_root)
            registry.rebuild_index()

            runs = registry.list_runs()
            self.assertEqual(len(runs), 1)
            self.assertEqual(runs[0]["run_id"], "TEST-FIN-01")
            self.assertEqual(runs[0]["status"], "completed")

            # Verify canonical index record keys
            for key in (
                "run_id",
                "status",
                "protocol_version",
                "stage",
                "started_at_utc",
                "finished_at_utc",
                "source_git_commit",
            ):
                self.assertIn(key, runs[0])

    def test_get_run_returns_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            _create_finalized_bundle(repo_root, "TEST-GET-01")

            registry = ExperimentRegistry(repo_root)
            details = registry.get_run("TEST-GET-01")
            self.assertIsNotNone(details)
            self.assertEqual(details["manifest"]["status"], "completed")
            self.assertEqual(details["config"]["agent"], "c0")

    def test_get_run_missing_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = ExperimentRegistry(Path(tmp))
            self.assertIsNone(registry.get_run("NONEXISTENT"))


if __name__ == "__main__":
    unittest.main()
