#!/usr/bin/env python3
"""Validate and install the generated bibliography package from ThesisBibliography."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

SOURCE_ID_RE = re.compile(r"^SRC-[A-F0-9]{10}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
LFS_PREFIX = b"version https://git-lfs.github.com/spec/v1"
TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml"}
FORBIDDEN_SUFFIXES = {
    ".pdf", ".doc", ".docx", ".zip", ".tar", ".gz", ".7z",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bin", ".pt", ".pth",
}
REQUIRED_FILES = {
    Path("README.md"),
    Path("SOURCE_COMMIT"),
    Path("manifest.csv"),
    Path("catalog/sources.csv"),
}
REQUIRED_DIRS = {Path("analyses"), Path("evidence")}


class BibliographyImportError(RuntimeError):
    """Raised when an imported bibliography package violates the contract."""


@dataclass(frozen=True)
class PackageSummary:
    source_commit: str
    source_ids: tuple[str, ...]
    file_hashes: dict[str, str]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_source_commit(package: Path) -> str:
    value = (package / "SOURCE_COMMIT").read_text(encoding="utf-8").strip()
    if not COMMIT_RE.fullmatch(value):
        raise BibliographyImportError(f"Invalid SOURCE_COMMIT: {value!r}")
    return value


def _source_id_column(fieldnames: list[str]) -> str:
    for candidate in ("Κωδικός", "Source ID", "source_id"):
        if candidate in fieldnames:
            return candidate
    raise BibliographyImportError("manifest.csv has no recognized source-id column")


def read_manifest_ids(package: Path) -> list[str]:
    manifest = package / "manifest.csv"
    with manifest.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        key = _source_id_column(fieldnames)
        ids = [(row.get(key) or "").strip() for row in reader]

    if not ids:
        raise BibliographyImportError("manifest.csv contains no exported sources")
    if len(ids) != len(set(ids)):
        raise BibliographyImportError("manifest.csv contains duplicate source IDs")
    invalid = sorted(source_id for source_id in ids if not SOURCE_ID_RE.fullmatch(source_id))
    if invalid:
        raise BibliographyImportError("Invalid source IDs in manifest.csv: " + ", ".join(invalid[:10]))
    return ids


def _catalog_ids(package: Path) -> set[str]:
    path = package / "catalog" / "sources.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        key = _source_id_column(fieldnames)
        return {(row.get(key) or "").strip() for row in reader if (row.get(key) or "").strip()}


def _check_paths(package: Path) -> dict[str, str]:
    file_hashes: dict[str, str] = {}
    for path in sorted(package.rglob("*")):
        relative = path.relative_to(package)
        if path.is_symlink():
            raise BibliographyImportError(f"Symlinks are not permitted in imported package: {relative}")
        if path.is_dir():
            if path.name in {"originals", "new-originals", ".git", ".github"}:
                raise BibliographyImportError(f"Forbidden directory in imported package: {relative}")
            continue
        if path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            raise BibliographyImportError(f"Forbidden binary/archive file in imported package: {relative}")
        with path.open("rb") as handle:
            prefix = handle.read(len(LFS_PREFIX))
        if prefix == LFS_PREFIX:
            raise BibliographyImportError(f"Git LFS pointer is not permitted in imported package: {relative}")
        file_hashes[relative.as_posix()] = sha256(path)
    return file_hashes


def validate_package(package: Path, expected_source_commit: str | None = None) -> PackageSummary:
    package = package.resolve()
    if not package.is_dir():
        raise BibliographyImportError(f"Package directory does not exist: {package}")

    missing_files = sorted(str(path) for path in REQUIRED_FILES if not (package / path).is_file())
    missing_dirs = sorted(str(path) for path in REQUIRED_DIRS if not (package / path).is_dir())
    if missing_files or missing_dirs:
        details = []
        if missing_files:
            details.append("missing files: " + ", ".join(missing_files))
        if missing_dirs:
            details.append("missing directories: " + ", ".join(missing_dirs))
        raise BibliographyImportError("Invalid bibliography package (" + "; ".join(details) + ")")

    source_commit = read_source_commit(package)
    if expected_source_commit is not None:
        expected = expected_source_commit.strip().lower()
        if not COMMIT_RE.fullmatch(expected):
            raise BibliographyImportError(f"Invalid expected source commit: {expected!r}")
        if source_commit != expected:
            raise BibliographyImportError(
                f"Package SOURCE_COMMIT {source_commit} does not match checked-out bibliography commit {expected}"
            )

    source_ids = read_manifest_ids(package)
    source_id_set = set(source_ids)
    catalog_ids = _catalog_ids(package)
    if catalog_ids != source_id_set:
        missing = sorted(source_id_set - catalog_ids)
        extra = sorted(catalog_ids - source_id_set)
        raise BibliographyImportError(
            "catalog/sources.csv does not match manifest.csv "
            f"(missing={missing[:10]}, extra={extra[:10]})"
        )

    for dirname in ("analyses", "evidence"):
        directory = package / dirname
        found_ids = {path.stem for path in directory.glob("SRC-*.md")}
        if found_ids != source_id_set:
            missing = sorted(source_id_set - found_ids)
            extra = sorted(found_ids - source_id_set)
            raise BibliographyImportError(
                f"{dirname}/ does not match manifest.csv (missing={missing[:10]}, extra={extra[:10]})"
            )

    file_hashes = _check_paths(package)
    return PackageSummary(source_commit, tuple(source_ids), file_hashes)


def write_integrity_manifest(destination: Path, summary: PackageSummary) -> None:
    payload = {
        "schema_version": 1,
        "source_repository": "MariosGiannakaras/ThesisBibliography",
        "source_commit": summary.source_commit,
        "exported_source_count": len(summary.source_ids),
        "source_ids": list(summary.source_ids),
        "files": summary.file_hashes,
    }
    (destination / "IMPORT_INTEGRITY.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def install_package(package: Path, destination: Path, expected_source_commit: str) -> PackageSummary:
    summary = validate_package(package, expected_source_commit)
    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="bibliography-import-", dir=destination.parent) as temporary:
        staged = Path(temporary) / "bibliography"
        shutil.copytree(package, staged)
        write_integrity_manifest(staged, summary)
        validate_installed_package(staged)

        backup = destination.with_name(destination.name + ".previous")
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            destination.replace(backup)
        try:
            staged.replace(destination)
        except Exception:
            if destination.exists():
                shutil.rmtree(destination)
            if backup.exists():
                backup.replace(destination)
            raise
        else:
            if backup.exists():
                shutil.rmtree(backup)

    return summary


def validate_installed_package(destination: Path) -> PackageSummary:
    integrity_path = destination / "IMPORT_INTEGRITY.json"
    if not integrity_path.is_file():
        raise BibliographyImportError("Imported bibliography is missing IMPORT_INTEGRITY.json")
    try:
        integrity = json.loads(integrity_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise BibliographyImportError(f"Invalid IMPORT_INTEGRITY.json: {error}") from error

    source_commit = str(integrity.get("source_commit", ""))
    summary = validate_package(destination, source_commit)
    expected_files = integrity.get("files")
    if not isinstance(expected_files, dict):
        raise BibliographyImportError("IMPORT_INTEGRITY.json has no file hash map")

    actual_files = {
        path.relative_to(destination).as_posix(): sha256(path)
        for path in destination.rglob("*")
        if path.is_file() and path.name != "IMPORT_INTEGRITY.json"
    }
    normalized_expected = {str(key): str(value) for key, value in expected_files.items()}
    if actual_files != normalized_expected:
        missing = sorted(set(normalized_expected) - set(actual_files))
        extra = sorted(set(actual_files) - set(normalized_expected))
        changed = sorted(
            key for key in set(actual_files) & set(normalized_expected)
            if actual_files[key] != normalized_expected[key]
        )
        raise BibliographyImportError(
            "Generated bibliography was modified outside the sync workflow "
            f"(missing={missing[:10]}, extra={extra[:10]}, changed={changed[:10]})"
        )

    integrity_ids = tuple(str(value) for value in integrity.get("source_ids", []))
    if integrity_ids != summary.source_ids:
        raise BibliographyImportError("IMPORT_INTEGRITY.json source_ids do not match manifest.csv")
    if int(integrity.get("exported_source_count", -1)) != len(summary.source_ids):
        raise BibliographyImportError("IMPORT_INTEGRITY.json source count does not match manifest.csv")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "research" / "bibliography",
    )
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    try:
        if args.validate_only:
            summary = validate_installed_package(args.destination.resolve())
        else:
            summary = install_package(args.package, args.destination, args.source_commit)
    except BibliographyImportError as error:
        print(f"Bibliography import validation failed: {error}")
        return 1

    print(
        f"Bibliography package valid: {len(summary.source_ids)} sources from {summary.source_commit}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
