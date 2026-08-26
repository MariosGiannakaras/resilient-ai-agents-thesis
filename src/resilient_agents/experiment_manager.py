import json
import logging
import subprocess
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

@contextmanager
def acquire_single_writer_lock(repo_root: Path, timeout: float = 300.0) -> Iterator[None]:
    """Provides a safe single-writer boundary using a directory lock."""
    lock_path = repo_root / "results" / ".publish.lock"
    start = time.monotonic()
    while True:
        try:
            lock_path.mkdir(parents=True, exist_ok=False)
            break
        except FileExistsError:
            if time.monotonic() - start > timeout:
                raise TimeoutError("Could not acquire publication single-writer lock")
            time.sleep(1.0)
    try:
        yield
    finally:
        try:
            lock_path.rmdir()
        except OSError:
            pass

class ExperimentRegistry:
    """Provides access to historical runs and rebuilds the index safely."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.runs_dir = self.repo_root / "results" / "runs"
        self.index_path = self.repo_root / "results" / "run-index.jsonl"

    def rebuild_index(self) -> None:
        """Rebuilds the index from individual run bundles."""
        entries = []
        if self.runs_dir.exists():
            for run_dir in sorted(self.runs_dir.iterdir()):
                if run_dir.is_dir():
                    manifest_path = run_dir / "manifest.json"
                    finalized_marker = run_dir / ".finalized"
                    
                    if not finalized_marker.exists():
                        continue # Incomplete or interrupted run
                    
                    if not manifest_path.exists():
                        raise ValueError(f"Finalized run {run_dir.name} is missing manifest.json")
                        
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    
                    if "status" not in manifest or manifest.get("run_id") != run_dir.name:
                        raise ValueError(f"Malformed manifest in {run_dir.name}")
                        
                    entries.append(manifest)
        
        with acquire_single_writer_lock(self.repo_root):
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.index_path, "w", encoding="utf-8") as f:
                for entry in entries:
                    f.write(json.dumps(entry, sort_keys=True) + "\n")

    def list_runs(self) -> list[dict[str, Any]]:
        """Returns a list of all finalized runs from the index."""
        if not self.index_path.exists():
            self.rebuild_index()
        runs = []
        with open(self.index_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    runs.append(json.loads(line))
        return runs

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        """Loads a specific run manifest and configuration."""
        manifest_path = self.runs_dir / run_id / "manifest.json"
        config_path = self.runs_dir / run_id / "config.json"
        if not manifest_path.exists():
            return None
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        config = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        return {"manifest": manifest, "config": config}

def get_resource_snapshot(repo_root: Path) -> dict[str, Any]:
    """Returns a snapshot of current system resources."""
    script_path = repo_root / "scripts" / "system_inventory.py"
    result = subprocess.check_output(
        [sys.executable, str(script_path)],
        encoding="utf-8"
    )
    return json.loads(result)

class CampaignManager:
    """Batch executes experiments using a single-writer boundary."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.registry = ExperimentRegistry(repo_root)

    def launch_batch(self, protocol_path: Path, requests: list[dict[str, Any]]) -> None:
        """
        Executes a batch of headless run requests.
        Ensures execution and publication uses single-writer locking to prevent race conditions.
        """
        import tempfile
        runner_script = self.repo_root / "scripts" / "run_headless_experiment.py"
        
        for req in requests:
            run_id = req["run_id"]
            finalized_marker = self.repo_root / "results" / "runs" / run_id / ".finalized"
            if finalized_marker.exists():
                logger.info("Run %s is already finalized, skipping.", run_id)
                continue
            
            with acquire_single_writer_lock(self.repo_root):
                with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                    json.dump(req, f)
                    req_path = f.name
                
                cmd = [
                    sys.executable,
                    str(runner_script),
                    "--repo-root", str(self.repo_root),
                    "--protocol", str(protocol_path),
                    "--request", req_path
                ]
                
                logger.info("Launching run %s", run_id)
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    logger.error("Run %s failed with code %d", run_id, e.returncode)
                    raise
                finally:
                    import os
                    if os.path.exists(req_path):
                        os.unlink(req_path)
