#!/usr/bin/env python3
"""Validate the generated bibliography import and canonical SRC-* usage in thesis text."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bibliography_import import BibliographyImportError, validate_installed_package

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "research" / "bibliography"
SOURCE_ID_RE = re.compile(r"\bSRC-[A-F0-9]{10}\b")
TEXT_SUFFIXES = {".md", ".txt", ".rst", ".tex", ".py", ".yaml", ".yml", ".json", ".csv"}
SCAN_ROOTS = (ROOT / "docs", ROOT / "thesis")
SCAN_FILES = (ROOT / "README.md", ROOT / "AGENTS.md")
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "research/bibliography",
}


def scan_source_references() -> dict[str, set[str]]:
    references: dict[str, set[str]] = {}
    candidates: list[Path] = [path for path in SCAN_FILES if path.is_file()]
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        candidates.extend(path for path in root.rglob("*") if path.is_file())

    for path in candidates:
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith("research/bibliography/"):
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.suffix.casefold() not in TEXT_SUFFIXES and path.name not in {"README.md", "AGENTS.md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for source_id in SOURCE_ID_RE.findall(text):
            references.setdefault(source_id, set()).add(relative)
    return references


def main() -> int:
    try:
        summary = validate_installed_package(IMPORT_DIR)
    except BibliographyImportError as error:
        print(f"Bibliography import validation failed: {error}")
        return 1

    imported = set(summary.source_ids)
    references = scan_source_references()
    unknown = sorted(set(references) - imported)
    if unknown:
        print("Canonical source IDs are referenced outside the import but missing from manifest.csv:")
        for source_id in unknown:
            print(f"- {source_id}: {', '.join(sorted(references[source_id]))}")
        return 1

    print(
        f"Bibliography usage valid: {len(imported)} imported sources; "
        f"{len(references)} canonical source IDs referenced by repository text."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
