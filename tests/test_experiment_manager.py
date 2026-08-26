"""Tests for the experiment manager."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.experiment_manager import (
    CampaignManager,
    ExperimentRegistry,
    acquire_single_writer_lock,
    get_resource_snapshot,
)

def test_acquire_single_writer_lock(tmp_path: Path):
    """Tests that the directory lock works and can be acquired and released."""
    repo_root = tmp_path
    with acquire_single_writer_lock(repo_root):
        assert (repo_root / "results" / ".publish.lock").is_dir()
    
    # Should be released
    assert not (repo_root / "results" / ".publish.lock").exists()

def test_experiment_registry_rebuild(tmp_path: Path):
    """Tests rebuilding the run-index.jsonl from bundles."""
    repo_root = tmp_path
    runs_dir = repo_root / "results" / "runs"
    runs_dir.mkdir(parents=True)
    
    # Create fake run 1
    run1 = runs_dir / "RUN-01"
    run1.mkdir()
    (run1 / "manifest.json").write_text(json.dumps({"run_id": "RUN-01", "status": "completed"}))
    (run1 / "config.json").write_text(json.dumps({"agent": "c0"}))
    
    # Create fake run 2
    run2 = runs_dir / "RUN-02"
    run2.mkdir()
    (run2 / "manifest.json").write_text(json.dumps({"run_id": "RUN-02", "status": "failed"}))
    
    registry = ExperimentRegistry(repo_root)
    registry.rebuild_index()
    
    index_path = repo_root / "results" / "run-index.jsonl"
    assert index_path.exists()
    
    runs = registry.list_runs()
    assert len(runs) == 2
    assert runs[0]["run_id"] == "RUN-01"
    assert runs[1]["run_id"] == "RUN-02"
    
    run1_details = registry.get_run("RUN-01")
    assert run1_details is not None
    assert run1_details["manifest"]["status"] == "completed"
    assert run1_details["config"]["agent"] == "c0"
