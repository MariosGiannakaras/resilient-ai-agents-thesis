"""Tests for the experiment manager."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.experiment_manager import (
    CampaignManager,
    ExperimentRegistry,
    acquire_single_writer_lock,
    get_resource_snapshot,
)


class TestExperimentManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)
        self.runs_dir = self.repo_root / "results" / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_acquire_single_writer_lock(self):
        """Tests that the directory lock works and can be acquired and released."""
        with acquire_single_writer_lock(self.repo_root):
            self.assertTrue((self.repo_root / "results" / ".publish.lock").is_dir())
        
        # Should be released
        self.assertFalse((self.repo_root / "results" / ".publish.lock").exists())

    def test_experiment_registry_rebuild(self):
        """Tests rebuilding the run-index.jsonl from bundles."""
        # Create fake run 1
        run1 = self.runs_dir / "RUN-01"
        run1.mkdir()
        (run1 / "manifest.json").write_text(json.dumps({"run_id": "RUN-01", "status": "completed"}))
        (run1 / "config.json").write_text(json.dumps({"agent": "c0"}))
        (run1 / ".finalized").write_text("")
        
        # Create fake run 2
        run2 = self.runs_dir / "RUN-02"
        run2.mkdir()
        (run2 / "manifest.json").write_text(json.dumps({"run_id": "RUN-02", "status": "failed"}))
        (run2 / ".finalized").write_text("")
        
        registry = ExperimentRegistry(self.repo_root)
        registry.rebuild_index()
        
        index_path = self.repo_root / "results" / "run-index.jsonl"
        self.assertTrue(index_path.exists())
        
        runs = registry.list_runs()
        self.assertEqual(len(runs), 2)
        self.assertEqual(runs[0]["run_id"], "RUN-01")
        self.assertEqual(runs[1]["run_id"], "RUN-02")
        
        run1_details = registry.get_run("RUN-01")
        self.assertIsNotNone(run1_details)
        self.assertEqual(run1_details["manifest"]["status"], "completed")
        self.assertEqual(run1_details["config"]["agent"], "c0")

if __name__ == "__main__":
    unittest.main()
