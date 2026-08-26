import sys

with open('src/resilient_agents/experiment_manager.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# We will replace the launch_batch method.
old_launch_batch = """    def launch_batch(self, protocol_path: Path, requests: list[dict[str, Any]]) -> None:
        \"\"\"
        Executes a batch of headless run requests.
        Ensures execution and publication uses single-writer locking to prevent race conditions.
        \"\"\"
        runner_script = self.repo_root / "scripts" / "run_headless_experiment.py"
        
        for req in requests:
            run_id = req["run_id"]
            finalized_marker = self.repo_root / "results" / "runs" / run_id / ".finalized"
            if finalized_marker.exists():
                logger.info("Run %s is already finalized, skipping.", run_id)
                continue
            
            with acquire_single_writer_lock(self.repo_root):
                cmd = [
                    sys.executable,
                    str(runner_script),
                    "--repo-root", str(self.repo_root),
                    "--protocol", str(protocol_path),
                    "--publish"
                ]
                req_json = json.dumps(req)
                
                logger.info("Launching run %s", run_id)
                try:
                    subprocess.run(cmd, input=req_json, encoding="utf-8", check=True)
                except subprocess.CalledProcessError as e:
                    logger.error("Run %s failed with code %d", run_id, e.returncode)
                    raise"""

new_launch_batch = """    def launch_batch(self, protocol_path: Path, requests: list[dict[str, Any]]) -> None:
        \"\"\"
        Executes a batch of headless run requests.
        Ensures execution and publication uses single-writer locking to prevent race conditions.
        \"\"\"
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
                        os.unlink(req_path)"""

code = code.replace(old_launch_batch, new_launch_batch)

with open('src/resilient_agents/experiment_manager.py', 'w', encoding='utf-8') as f:
    f.write(code)
