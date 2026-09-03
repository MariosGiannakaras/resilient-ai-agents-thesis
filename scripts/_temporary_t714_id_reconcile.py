#!/usr/bin/env python3
from pathlib import Path

paths = [
    Path("docs/context/TASKS.md"),
    Path("docs/context/CURRENT_STATUS.md"),
]
for path in paths:
    text = path.read_text(encoding="utf-8")
    count = text.count("T-711A")
    if count < 1:
        raise RuntimeError(f"Expected T-711A in {path}, found {count}")
    updated = text.replace("T-711A", "T-714")
    if "T-711A" in updated:
        raise RuntimeError(f"T-711A residue in {path}")
    path.write_text(updated, encoding="utf-8")
