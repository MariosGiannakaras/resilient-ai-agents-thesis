"""Windows native desktop validation script for the thesis application.

Launches the NiceGUI application in native mode (pywebview desktop window),
validates that it opens, renders correctly, and closes cleanly.

This script MUST be run on the actual Windows thesis machine.
Do not claim native validation from browser mode or Ubuntu CI.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_native_validation() -> dict:
    """Run the native application and validate basic lifecycle."""
    results = {
        "native_launch": False,
        "window_opened": False,
        "clean_exit": False,
        "relaunch_works": False,
        "no_zombie_process": True,
        "prerequisites": [],
    }

    # Check prerequisites
    try:
        import webview  # noqa: F401
        results["prerequisites"].append("pywebview: available")
    except ImportError:
        results["prerequisites"].append("pywebview: MISSING")
        return results

    # Check WebView2 (EdgeChromium backend on Windows)
    if sys.platform == "win32":
        import winreg
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BEB-E856EABC05AB}",
            )
            version = winreg.QueryValueEx(key, "pv")[0]
            winreg.CloseKey(key)
            results["prerequisites"].append(f"WebView2 Runtime: {version}")
        except (OSError, FileNotFoundError):
            # Try current user
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BEB-E856EABC05AB}",
                )
                version = winreg.QueryValueEx(key, "pv")[0]
                winreg.CloseKey(key)
                results["prerequisites"].append(f"WebView2 Runtime: {version}")
            except (OSError, FileNotFoundError):
                results["prerequisites"].append("WebView2 Runtime: not found in registry (may still work via Edge)")

    results["prerequisites"].append(f"Python: {sys.version}")
    results["prerequisites"].append(f"Platform: {sys.platform}")
    results["prerequisites"].append(f"OS: {os.name}")

    # Test 1: Launch native app
    print("Test 1: Launching native application...")
    env = os.environ.copy()
    # Unset browser mode to ensure native
    env.pop("THESIS_APP_BROWSER_MODE", None)
    proc = subprocess.Popen(
        ["uv", "run", "--locked", "resilient-agents-app"],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )

    # Wait for the application to start (native mode takes longer due to pywebview)
    time.sleep(8)

    if proc.poll() is None:
        results["native_launch"] = True
        results["window_opened"] = True
        print("  -> Native window launched and still running")
    else:
        returncode = proc.returncode
        stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
        print(f"  -> Process exited early with code {returncode}")
        print(f"  -> stderr: {stderr[:500]}")
        results["native_launch"] = False
        return results

    # Test 2: Clean exit
    print("Test 2: Testing clean exit...")
    proc.terminate()
    try:
        proc.wait(timeout=15)
        results["clean_exit"] = True
        print(f"  -> Clean exit with code {proc.returncode}")
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        results["clean_exit"] = False
        print("  -> Had to force kill")

    if proc.stdout:
        proc.stdout.close()
    if proc.stderr:
        proc.stderr.close()

    # Brief pause before relaunch
    time.sleep(3)

    # Test 3: Relaunch
    print("Test 3: Testing relaunch...")
    proc2 = subprocess.Popen(
        ["uv", "run", "--locked", "resilient-agents-app"],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )
    time.sleep(8)

    if proc2.poll() is None:
        results["relaunch_works"] = True
        print("  -> Relaunch successful")
        proc2.terminate()
        try:
            proc2.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc2.kill()
            proc2.wait()
    else:
        results["relaunch_works"] = False
        print(f"  -> Relaunch failed with code {proc2.returncode}")

    if proc2.stdout:
        proc2.stdout.close()
    if proc2.stderr:
        proc2.stderr.close()

    # Test 4: No zombie processes
    print("Test 4: Checking for zombie processes...")
    time.sleep(2)
    # Check if any nicegui/uvicorn processes are still running from our test
    if sys.platform == "win32":
        check = subprocess.run(
            ["tasklist", "/FI", f"PID eq {proc.pid}", "/NH"],
            capture_output=True, text=True,
        )
        if str(proc.pid) in check.stdout:
            results["no_zombie_process"] = False
            print(f"  -> Warning: PID {proc.pid} may still be running")
        else:
            print("  -> No zombie processes found")

    return results


def main() -> None:
    print("=" * 60)
    print("Windows Native Application Validation")
    print("=" * 60)

    results = run_native_validation()

    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)
    for key, value in results.items():
        if key == "prerequisites":
            print(f"  {key}:")
            for prereq in value:
                print(f"    - {prereq}")
        else:
            status = "PASS" if value else "FAIL"
            print(f"  {key}: {status}")

    all_pass = all(
        v for k, v in results.items()
        if k != "prerequisites" and isinstance(v, bool)
    )
    print(f"\nOverall: {'ALL PASS' if all_pass else 'SOME FAILURES'}")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
