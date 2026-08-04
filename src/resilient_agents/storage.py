"""Filesystem-first result storage rules."""
from __future__ import annotations

from pathlib import Path


def run_directory(repo_root: Path, run_id: str) -> Path:
    if not run_id or any(part in {"..", "."} for part in Path(run_id).parts):
        raise ValueError("invalid run_id")
    return repo_root / "results" / "runs" / run_id


def cache_directory(repo_root: Path) -> Path:
    """Return a disposable, rebuildable local index location."""
    return repo_root / ".cache" / "runs"
