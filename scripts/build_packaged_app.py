"""PyInstaller build script for the Resilient AI Agents Lab application.

Creates a --onedir --windowed distribution of the native application.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import nicegui

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
NICEGUI_PATH = Path(nicegui.__file__).parent


def clean_build_dirs() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)


def build() -> None:
    print("=== Building Thesis Application with PyInstaller ===")
    clean_build_dirs()
    
    # We include configs and the read-only final thesis evidence
    # We do NOT include runtime state or temporary logs
    
    args = [
        "uv", "run", "--locked", "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "thesis-app",
        "--add-data", f"{NICEGUI_PATH}{os.pathsep}nicegui",
        "--add-data", f"{ROOT / 'configs'}{os.pathsep}configs",
        "--add-data", f"{ROOT / 'results' / 'thesis-final'}{os.pathsep}results/thesis-final",
        "--add-data", f"{ROOT / 'scripts'}{os.pathsep}scripts",
        "--hidden-import", "socketio",
        "--hidden-import", "engineio",
        "--hidden-import", "fastapi",
        "--hidden-import", "uvicorn",
        "--collect-all", "plotly",
        "--collect-all", "pandas",
        "--collect-all", "gymnasium",
        "--collect-all", "minigrid",
        str(ROOT / "src" / "app" / "main.py"),
    ]
    
    print("Running PyInstaller...")
    subprocess.check_call(args, cwd=str(ROOT))
    
    print("\n=== Build Complete ===")
    print(f"Output directory: {DIST_DIR / 'thesis-app'}")


if __name__ == "__main__":
    build()
