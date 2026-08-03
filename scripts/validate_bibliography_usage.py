#!/usr/bin/env python3
"""Validate SRC-* and MAT-* references according to document trust context."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from bibliography_catalog import CatalogIndex, load_catalog
from bibliography_import import BibliographyImportError, validate_installed_package

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMPORT_DIR = ROOT / "research" / "bibliography"
REFERENCE_RE = re.compile(r"\b(?:SRC|MAT)-[A-F0-9]{10}\b")
TEXT_SUFFIXES = {".md", ".txt", ".rst", ".tex", ".py", ".yaml", ".yml", ".json", ".csv"}
SCAN_ROOTS = (ROOT / "docs", ROOT / "thesis", ROOT / "results" / "thesis-final")
SCAN_FILES = (ROOT / "README.md", ROOT / "AGENTS.md")
EXCLUDED_NAMES = {".git", ".venv", "venv", "node_modules", "__pycache__"}


@dataclass(frozen=True)
class ReferenceUse:
    identifier: str
    path: str
    context: str
    trust: str


def _is_formal_path(root: Path, path: Path, text: str) -> bool:
    relative = path.relative_to(root).as_posix()
    formal_prefixes = (
        "thesis/chapters/", "thesis/final/", "docs/thesis/", "results/thesis-final/",
    )
    if relative.startswith(formal_prefixes):
        return True
    if relative.startswith("docs/experiments/"):
        name = path.stem.casefold()
        if any(token in name for token in ("final", "frozen", "protocol", "methodology")):
            return True
    header = "\n".join(text.splitlines()[:40]).casefold()
    return "status: frozen" in header or "status:** frozen" in header or "status: final" in header


def _candidate_files(root: Path) -> list[Path]:
    candidates = [path for path in SCAN_FILES if path.is_file()]
    for scan_root in SCAN_ROOTS:
        if scan_root.exists():
            candidates.extend(path for path in scan_root.rglob("*") if path.is_file())
    unique = sorted(set(candidates), key=lambda path: path.relative_to(root).as_posix())
    return [
        path for path in unique
        if path.suffix.casefold() in TEXT_SUFFIXES
        and not any(part in EXCLUDED_NAMES for part in path.parts)
    ]


def validate_references(
    root: Path,
    import_dir: Path,
    paths: list[Path] | None = None,
) -> tuple[list[ReferenceUse], list[str]]:
    root = root.resolve()
    validate_installed_package(import_dir)
    catalog: CatalogIndex = load_catalog(import_dir)
    uses: list[ReferenceUse] = []
    errors: list[str] = []
    for path in paths or _candidate_files(root):
        resolved = path.resolve()
        if import_dir.resolve() in resolved.parents:
            continue
        try:
            text = resolved.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        context = "formal" if _is_formal_path(root, resolved, text) else "internal"
        relative = resolved.relative_to(root).as_posix()
        for identifier in REFERENCE_RE.findall(text):
            if identifier.startswith("SRC-"):
                record = catalog.sources.get(identifier)
                if record is None:
                    errors.append(f"Unknown source ID {identifier} in {relative}")
                    continue
                uses.append(ReferenceUse(identifier, relative, context, record.trust))
                if context == "formal" and not record.citation_ready:
                    errors.append(
                        f"Formal document {relative} references non-citation-ready source "
                        f"{identifier} ({record.trust})"
                    )
            else:
                material = catalog.materials.get(identifier)
                if material is None:
                    errors.append(f"Unknown research-material ID {identifier} in {relative}")
                    continue
                uses.append(ReferenceUse(identifier, relative, context, "research-material"))
                if context == "formal":
                    errors.append(
                        f"Formal document {relative} uses {identifier} as a citation; MAT-* is not a formal citation"
                    )
    return uses, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--import-dir", type=Path, default=DEFAULT_IMPORT_DIR)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    try:
        paths = [path if path.is_absolute() else args.root / path for path in args.paths] or None
        uses, errors = validate_references(args.root, args.import_dir, paths)
    except BibliographyImportError as exc:
        print(f"Bibliography usage validation failed: {exc}")
        return 1
    if errors:
        print("Bibliography reference validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    by_trust: dict[str, int] = {}
    for use in uses:
        by_trust[use.trust] = by_trust.get(use.trust, 0) + 1
    trust_summary = ", ".join(f"{key}={value}" for key, value in sorted(by_trust.items())) or "none"
    print(f"Bibliography usage valid: {len(uses)} references ({trust_summary}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
