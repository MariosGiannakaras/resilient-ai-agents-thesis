import os
import subprocess
import time
import urllib.request
import signal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_APP = ROOT / "dist" / "thesis-app" / "thesis-app.exe"

def validate_packaging():
    if not DIST_APP.exists():
        print(f"FAIL: Packaged app not found at {DIST_APP}")
        exit(1)

    print(f"Testing packaged app: {DIST_APP}")
    
    env = os.environ.copy()
    env["THESIS_APP_BROWSER_MODE"] = "1"
    env["THESIS_APP_PORT"] = "9999"
    env["THESIS_WRITABLE_ROOT"] = str(ROOT / "dist" / "test-workspace")
    
    print("Starting packaged executable in background...")
    process = subprocess.Popen([str(DIST_APP)], env=env)
    
    try:
        # Give it up to 60 seconds to start
        print("Waiting for server to start...")
        for _ in range(60):
            try:
                urllib.request.urlopen("http://127.0.0.1:9999/")
                break
            except Exception:
                time.sleep(1)
        else:
            print("FAIL: Timeout waiting for server to start.")
            exit(1)
            
        # Test 1: Check HTTP response
        print("Testing HTTP connection to packaged app...")
        req = urllib.request.urlopen("http://127.0.0.1:9999/")
        assert req.getcode() == 200, f"Expected 200, got {req.getcode()}"
        html = req.read().decode("utf-8")
        assert "Resilient AI Agents Lab" in html, "App title not found in HTML"
        print("HTTP connection successful!")
        
        # Test 2: Check writable root creation
        test_workspace = ROOT / "dist" / "test-workspace"
        print(f"Testing writable root creation at {test_workspace} ...")
        req_runs = urllib.request.urlopen("http://127.0.0.1:9999/runs")
        assert req_runs.getcode() == 200
        time.sleep(2)
        assert (test_workspace / "results" / "runtime").is_dir(), "Writable root runtime directory not created!"
        print("Writable root validation successful!")
        
        print("\nALL PACKAGING TESTS PASSED!")

    finally:
        print("Terminating packaged app...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    validate_packaging()
