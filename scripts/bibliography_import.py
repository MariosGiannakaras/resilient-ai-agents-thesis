#!/usr/bin/env python3
"""Validate and transactionally install a complete ThesisBibliography research corpus."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable

from bibliography_text import BibliographyTextError, read_corpus_text

SOURCE_ID_RE = re.compile(r"^SRC-[A-F0-9]{10}$")
MATERIAL_ID_RE = re.compile(r"^MAT-[A-F0-9]{10}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CHECKSUM_RE = re.compile(r"^([0-9a-f]{64})  (.+)$")
LFS_PREFIX = b"version https://git-lfs.github.com/spec/v1"
TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".rst", ".tex"}
TEXT_FILENAMES = {"SOURCE_COMMIT", "SHA256SUMS"}
FORBIDDEN_SUFFIXES = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip",
    ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".png", ".jpg",
    ".jpeg", ".gif", ".webp", ".svgz", ".bin", ".exe", ".dll", ".so",
    ".dylib", ".pt", ".pth", ".pkl", ".pickle", ".npy", ".npz", ".db",
    ".sqlite", ".sqlite3",
}
FORBIDDEN_DIRECTORY_NAMES = {
    ".git", ".github", "originals", "new-originals", "intake", "incoming",
    "conversion", "conversions", "conversion-workspace", "ocr-workspace", "cache",
    "caches", "tmp", "temp", "__pycache__",
}
CONSUMER_INTEGRITY = Path("IMPORT_INTEGRITY.json")
CORPUS_METADATA = Path("catalog/package-metadata.json")
CORPUS_CHECKSUMS = Path("catalog/SHA256SUMS")
CITATION_ROOT = Path("citation-ready")
CITATION_METADATA = CITATION_ROOT / "catalog/package-metadata.json"
CITATION_CHECKSUMS = CITATION_ROOT / "catalog/SHA256SUMS"

CORPUS_REQUIRED_FILES = {
    Path("README.md"), Path("SOURCE_COMMIT"), CORPUS_METADATA, CORPUS_CHECKSUMS,
    Path("catalog/sources.csv"), Path("catalog/thesis-selection.csv"),
    Path("catalog/research-materials.csv"), Path("catalog/research-material-review.csv"),
    Path("catalog/originals-index.csv"),
}
CORPUS_REQUIRED_DIRS = {
    CITATION_ROOT, Path("sources"), Path("analyses"), Path("evidence"),
    Path("materials"), Path("notes"), Path("aggregates"), Path("catalog"),
}
CITATION_REQUIRED_FILES = {
    Path("README.md"), Path("SOURCE_COMMIT"), Path("manifest.csv"),
    Path("catalog/sources.csv"), Path("catalog/package-metadata.json"),
    Path("catalog/SHA256SUMS"),
}
CITATION_REQUIRED_DIRS = {Path("analyses"), Path("evidence"), Path("catalog")}


class BibliographyImportError(RuntimeError):
    """Raised when a bibliography corpus violates the consumer contract."""


@dataclass(frozen=True)
class PackageSummary:
    requested_ref: str
    checkout_commit: str
    corpus_source_commit: str
    citation_source_commit: str
    source_ids: tuple[str, ...]
    selected_ids: tuple[str, ...]
    material_ids: tuple[str, ...]
    file_hashes: dict[str, str]
    corpus_file_count: int
    original_pdf_count: int
    corpus_schema_version: int
    corpus_metadata_sha256: str
    corpus_checksums_sha256: str
    citation_metadata_sha256: str
    citation_checksums_sha256: str
    legacy_text_encodings: dict[str, str]
    legacy_text_controls: dict[str, dict[str, int]]

    @property
    def source_count(self) -> int:
        return len(self.source_ids)

    @property
    def selected_source_count(self) -> int:
        return len(self.selected_ids)

    @property
    def research_material_count(self) -> int:
        return len(self.material_ids)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_commit(value: str, label: str) -> str:
    normalized = value.strip().lower()
    if not COMMIT_RE.fullmatch(normalized):
        raise BibliographyImportError(f"{label} must be a full lowercase 40-character Git SHA: {value!r}")
    return normalized


def _read_commit(path: Path, label: str) -> str:
    try:
        value = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as exc:
        raise BibliographyImportError(f"Cannot read {label}: {exc}") from exc
    return _require_commit(value, label)


def _load_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BibliographyImportError(f"Invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise BibliographyImportError(f"{label} must be a JSON object")
    return value


def _safe_checksum_path(raw: str, manifest_relative: Path) -> str:
    candidate = PurePosixPath(raw)
    if not raw or candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        raise BibliographyImportError(
            f"Unsafe checksum path in {manifest_relative.as_posix()}: {raw!r}"
        )
    normalized = candidate.as_posix()
    if normalized in {
        "catalog/package-metadata.json", "catalog/SHA256SUMS", CONSUMER_INTEGRITY.as_posix()
    }:
        raise BibliographyImportError(
            f"Checksum manifest includes an excluded path in {manifest_relative.as_posix()}: {raw!r}"
        )
    return normalized


def _parse_checksums(root: Path, relative: Path) -> dict[str, str]:
    path = root / relative
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise BibliographyImportError(f"Cannot read checksum manifest {relative}: {exc}") from exc
    checksums: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        match = CHECKSUM_RE.fullmatch(line)
        if not match:
            raise BibliographyImportError(
                f"Malformed checksum line {number} in {relative.as_posix()}"
            )
        digest, raw_path = match.groups()
        normalized = _safe_checksum_path(raw_path, relative)
        if normalized in checksums:
            raise BibliographyImportError(
                f"Duplicate checksum path in {relative.as_posix()}: {normalized}"
            )
        checksums[normalized] = digest
    return checksums


def _validate_text(path: Path, relative: Path) -> tuple[str, dict[str, int]]:
    if path.suffix.casefold() not in TEXT_EXTENSIONS and path.name not in TEXT_FILENAMES:
        raise BibliographyImportError(f"Unexpected non-text file in research corpus: {relative}")
    try:
        _, encoding, controls = read_corpus_text(path, relative)
    except BibliographyTextError as exc:
        raise BibliographyImportError(str(exc)) from exc
    return encoding, controls


def _walk_files(
    root: Path,
    *,
    ignore_consumer_integrity: bool = False,
    legacy_text_encodings: dict[str, str] | None = None,
    legacy_text_controls: dict[str, dict[str, int]] | None = None,
) -> dict[str, Path]:
    files: dict[str, Path] = {}
    resolved_root = root.resolve()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        rel_posix = relative.as_posix()
        if ignore_consumer_integrity and relative == CONSUMER_INTEGRITY:
            continue
        if path.is_symlink():
            raise BibliographyImportError(f"Symlinks are not permitted: {rel_posix}")
        try:
            resolved = path.resolve(strict=True)
        except OSError as exc:
            raise BibliographyImportError(f"Cannot resolve imported path {rel_posix}: {exc}") from exc
        try:
            resolved.relative_to(resolved_root)
        except ValueError as exc:
            raise BibliographyImportError(f"Path escapes research corpus: {rel_posix}") from exc
        if path.is_dir():
            if path.name.casefold() in FORBIDDEN_DIRECTORY_NAMES:
                raise BibliographyImportError(f"Forbidden directory in research corpus: {rel_posix}")
            continue
        if not path.is_file():
            raise BibliographyImportError(f"Unsupported filesystem entry in research corpus: {rel_posix}")
        if path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            raise BibliographyImportError(f"Forbidden binary/archive file in research corpus: {rel_posix}")
        with path.open("rb") as handle:
            prefix = handle.read(max(len(LFS_PREFIX), 256))
        if prefix.startswith(LFS_PREFIX):
            raise BibliographyImportError(f"Git LFS pointer is not permitted: {rel_posix}")
        encoding, controls = _validate_text(path, relative)
        if encoding != "utf-8" and legacy_text_encodings is not None:
            legacy_text_encodings[rel_posix] = encoding
        if controls and legacy_text_controls is not None:
            legacy_text_controls[rel_posix] = controls
        files[rel_posix] = path
    return files


def _validate_structure(package: Path) -> None:
    missing_files = sorted(
        path.as_posix() for path in CORPUS_REQUIRED_FILES if not (package / path).is_file()
    )
    missing_dirs = sorted(
        path.as_posix() for path in CORPUS_REQUIRED_DIRS if not (package / path).is_dir()
    )
    citation = package / CITATION_ROOT
    missing_files.extend(
        f"citation-ready/{path.as_posix()}"
        for path in sorted(CITATION_REQUIRED_FILES)
        if not (citation / path).is_file()
    )
    missing_dirs.extend(
        f"citation-ready/{path.as_posix()}"
        for path in sorted(CITATION_REQUIRED_DIRS)
        if not (citation / path).is_dir()
    )
    if missing_files or missing_dirs:
        details: list[str] = []
        if missing_files:
            details.append("missing files: " + ", ".join(missing_files))
        if missing_dirs:
            details.append("missing directories: " + ", ".join(missing_dirs))
        raise BibliographyImportError("Invalid complete research corpus (" + "; ".join(details) + ")")


def _content_file_map(root: Path, files: dict[str, Path]) -> dict[str, Path]:
    excluded = {"catalog/package-metadata.json", "catalog/SHA256SUMS"}
    return {relative: path for relative, path in files.items() if relative not in excluded}


def _validate_checksum_scope(
    root: Path,
    files: dict[str, Path],
    checksum_relative: Path,
) -> dict[str, str]:
    recorded = _parse_checksums(root, checksum_relative)
    actual = _content_file_map(root, files)
    actual_paths = set(actual)
    recorded_paths = set(recorded)
    if actual_paths != recorded_paths:
        missing = sorted(actual_paths - recorded_paths)
        extra = sorted(recorded_paths - actual_paths)
        raise BibliographyImportError(
            f"Checksum path-set mismatch in {checksum_relative.as_posix()} "
            f"(missing={missing[:10]}, extra={extra[:10]})"
        )
    changed = sorted(
        relative for relative, path in actual.items() if sha256(path) != recorded[relative]
    )
    if changed:
        raise BibliographyImportError(
            f"Checksum mismatch in {checksum_relative.as_posix()}: {changed[:10]}"
        )
    return recorded


def _read_csv(path: Path, label: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = list(reader.fieldnames or [])
            rows = [dict(row) for row in reader]
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise BibliographyImportError(f"Invalid {label}: {exc}") from exc
    if not fields:
        raise BibliographyImportError(f"{label} has no header")
    return fields, rows


def _find_column(fields: Iterable[str], candidates: Iterable[str], label: str) -> str:
    field_set = set(fields)
    for candidate in candidates:
        if candidate in field_set:
            return candidate
    raise BibliographyImportError(f"{label} has no recognized identifier column")


def _read_ids(
    path: Path,
    candidates: Iterable[str],
    pattern: re.Pattern[str],
    label: str,
) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    fields, rows = _read_csv(path, label)
    key = _find_column(fields, candidates, label)
    values = tuple((row.get(key) or "").strip() for row in rows)
    if any(not value for value in values):
        raise BibliographyImportError(f"{label} contains a blank identifier")
    if len(values) != len(set(values)):
        raise BibliographyImportError(f"{label} contains duplicate identifiers")
    invalid = sorted(value for value in values if not pattern.fullmatch(value))
    if invalid:
        raise BibliographyImportError(f"{label} contains invalid identifiers: {invalid[:10]}")
    return rows, values


def _markdown_ids(directory: Path, pattern: re.Pattern[str]) -> set[str]:
    ids: set[str] = set()
    for path in directory.glob("*.md"):
        if path.name == "README.md":
            continue
        if not pattern.fullmatch(path.stem):
            raise BibliographyImportError(f"Unexpected Markdown identifier file: {path.relative_to(directory.parent)}")
        ids.add(path.stem)
    return ids


def _validate_metadata(
    package: Path,
    corpus_files: dict[str, Path],
    citation_files: dict[str, Path],
) -> tuple[dict[str, object], dict[str, object], str, str]:
    corpus_metadata = _load_json(package / CORPUS_METADATA, CORPUS_METADATA.as_posix())
    citation_metadata = _load_json(package / CITATION_METADATA, CITATION_METADATA.as_posix())
    corpus_commit = _read_commit(package / "SOURCE_COMMIT", "corpus SOURCE_COMMIT")
    citation_commit = _read_commit(
        package / CITATION_ROOT / "SOURCE_COMMIT", "citation-ready SOURCE_COMMIT"
    )
    if corpus_metadata.get("schema_version") != 1:
        raise BibliographyImportError("Unsupported complete research-corpus schema_version")
    if corpus_metadata.get("package_type") != "ThesisBibliography complete research corpus":
        raise BibliographyImportError("Unexpected complete research-corpus package_type")
    if corpus_metadata.get("source_commit") != corpus_commit:
        raise BibliographyImportError("Complete-corpus metadata source_commit differs from SOURCE_COMMIT")
    if corpus_metadata.get("hash_algorithm") != "sha256":
        raise BibliographyImportError("Complete-corpus hash_algorithm must be sha256")
    if corpus_metadata.get("checksum_file") != CORPUS_CHECKSUMS.as_posix():
        raise BibliographyImportError("Complete-corpus checksum_file is inconsistent")
    corpus_content_count = len(_content_file_map(package, corpus_files))
    if corpus_metadata.get("file_count") != corpus_content_count:
        raise BibliographyImportError("Complete-corpus metadata file_count mismatch")

    if citation_metadata.get("schema_version") != 1:
        raise BibliographyImportError("Unsupported citation-ready schema_version")
    if citation_metadata.get("package_type") != "ThesisBibliography verified thesis package":
        raise BibliographyImportError("Unexpected citation-ready package_type")
    if citation_metadata.get("source_commit") != citation_commit:
        raise BibliographyImportError("Citation-ready metadata source_commit differs from SOURCE_COMMIT")
    if citation_metadata.get("hash_algorithm") != "sha256":
        raise BibliographyImportError("Citation-ready hash_algorithm must be sha256")
    if citation_metadata.get("checksum_file") != "catalog/SHA256SUMS":
        raise BibliographyImportError("Citation-ready checksum_file is inconsistent")
    citation_root = package / CITATION_ROOT
    citation_content_count = len(_content_file_map(citation_root, citation_files))
    if citation_metadata.get("file_count") != citation_content_count:
        raise BibliographyImportError("Citation-ready metadata file_count mismatch")
    return corpus_metadata, citation_metadata, corpus_commit, citation_commit


def _validate_identifiers_and_counts(
    package: Path,
    corpus_metadata: dict[str, object],
    citation_metadata: dict[str, object],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    _source_rows, source_ids = _read_ids(
        package / "catalog/sources.csv", ("Κωδικός", "Source ID", "source_id"),
        SOURCE_ID_RE, "catalog/sources.csv",
    )
    source_set = set(source_ids)
    if not source_ids:
        raise BibliographyImportError("catalog/sources.csv contains no canonical sources")
    if corpus_metadata.get("source_count") != len(source_ids):
        raise BibliographyImportError("Complete-corpus source_count differs from catalog/sources.csv")
    source_files = _markdown_ids(package / "sources", SOURCE_ID_RE)
    if source_files != source_set:
        raise BibliographyImportError(
            "sources/ does not exactly cover catalog/sources.csv "
            f"(missing={sorted(source_set-source_files)[:10]}, extra={sorted(source_files-source_set)[:10]})"
        )
    analysis_files = _markdown_ids(package / "analyses", SOURCE_ID_RE)
    if analysis_files != source_set:
        raise BibliographyImportError(
            "analyses/ does not exactly cover catalog/sources.csv "
            f"(missing={sorted(source_set-analysis_files)[:10]}, extra={sorted(analysis_files-source_set)[:10]})"
        )
    evidence_files = _markdown_ids(package / "evidence", SOURCE_ID_RE)
    if not evidence_files <= source_set:
        raise BibliographyImportError(
            f"evidence/ contains unknown source IDs: {sorted(evidence_files-source_set)[:10]}"
        )

    _manifest_rows, selected_ids = _read_ids(
        package / CITATION_ROOT / "manifest.csv",
        ("Κωδικός", "Source ID", "source_id"), SOURCE_ID_RE,
        "citation-ready/manifest.csv",
    )
    selected_set = set(selected_ids)
    if not selected_set <= source_set:
        raise BibliographyImportError(
            f"Citation-ready manifest contains non-canonical sources: {sorted(selected_set-source_set)[:10]}"
        )
    if citation_metadata.get("selected_sources") != len(selected_ids):
        raise BibliographyImportError("Citation-ready selected_sources differs from manifest.csv")
    if corpus_metadata.get("selected_source_count") != len(selected_ids):
        raise BibliographyImportError("Complete-corpus selected_source_count differs from citation-ready manifest")
    for dirname in ("analyses", "evidence"):
        found = _markdown_ids(package / CITATION_ROOT / dirname, SOURCE_ID_RE)
        if found != selected_set:
            raise BibliographyImportError(
                f"citation-ready/{dirname}/ does not match manifest.csv "
                f"(missing={sorted(selected_set-found)[:10]}, extra={sorted(found-selected_set)[:10]})"
            )

    selection_path = package / "catalog/thesis-selection.csv"
    fields, selection_rows = _read_csv(selection_path, "catalog/thesis-selection.csv")
    selection_key = _find_column(fields, ("Κωδικός", "Source ID", "source_id"), "catalog/thesis-selection.csv")
    export_key = "Εξαγωγή" if "Εξαγωγή" in fields else None
    exported = {
        (row.get(selection_key) or "").strip()
        for row in selection_rows
        if export_key is None or (row.get(export_key) or "").strip().casefold() in {"ναι", "yes", "true", "1"}
    }
    invalid_selection = sorted(value for value in exported if not SOURCE_ID_RE.fullmatch(value))
    if invalid_selection:
        raise BibliographyImportError(f"Invalid source IDs in thesis-selection.csv: {invalid_selection[:10]}")
    if exported != selected_set:
        raise BibliographyImportError(
            "catalog/thesis-selection.csv exported set differs from citation-ready manifest "
            f"(missing={sorted(selected_set-exported)[:10]}, extra={sorted(exported-selected_set)[:10]})"
        )

    _material_rows, material_ids = _read_ids(
        package / "catalog/research-materials.csv", ("material_id",), MATERIAL_ID_RE,
        "catalog/research-materials.csv",
    )
    _review_rows, review_ids = _read_ids(
        package / "catalog/research-material-review.csv", ("material_id",), MATERIAL_ID_RE,
        "catalog/research-material-review.csv",
    )
    material_set = set(material_ids)
    review_set = set(review_ids)
    material_files = _markdown_ids(package / "materials", MATERIAL_ID_RE)
    if material_set != review_set or material_set != material_files:
        raise BibliographyImportError(
            "Research-material coverage mismatch "
            f"(missing_review={sorted(material_set-review_set)[:10]}, "
            f"extra_review={sorted(review_set-material_set)[:10]}, "
            f"missing_files={sorted(material_set-material_files)[:10]}, "
            f"extra_files={sorted(material_files-material_set)[:10]})"
        )
    if corpus_metadata.get("research_material_count") != len(material_ids):
        raise BibliographyImportError("Complete-corpus research_material_count mismatch")

    _original_rows, original_ids = _read_originals_index(package / "catalog/originals-index.csv")
    if corpus_metadata.get("original_pdf_count") != len(original_ids):
        raise BibliographyImportError("Complete-corpus original_pdf_count differs from originals-index.csv")
    return source_ids, selected_ids, material_ids


def _read_originals_index(path: Path) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    fields, rows = _read_csv(path, "catalog/originals-index.csv")
    required = {"original_path", "sha256", "linked_source_id", "research_material_id", "immutable_url"}
    if not required <= set(fields):
        raise BibliographyImportError(
            "catalog/originals-index.csv is missing columns: " + ", ".join(sorted(required-set(fields)))
        )
    identities: list[str] = []
    seen_paths: set[str] = set()
    for row in rows:
        original_path = (row.get("original_path") or "").strip()
        digest = (row.get("sha256") or "").strip().lower()
        if not original_path or PurePosixPath(original_path).is_absolute() or ".." in PurePosixPath(original_path).parts:
            raise BibliographyImportError(f"Unsafe original_path in originals-index.csv: {original_path!r}")
        if original_path in seen_paths:
            raise BibliographyImportError(f"Duplicate original_path in originals-index.csv: {original_path}")
        seen_paths.add(original_path)
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise BibliographyImportError(f"Invalid original SHA-256 for {original_path}")
        linked = (row.get("linked_source_id") or "").strip()
        material = (row.get("research_material_id") or "").strip()
        if linked and not SOURCE_ID_RE.fullmatch(linked):
            raise BibliographyImportError(f"Invalid linked_source_id in originals-index.csv: {linked}")
        if material and not MATERIAL_ID_RE.fullmatch(material):
            raise BibliographyImportError(f"Invalid research_material_id in originals-index.csv: {material}")
        identities.append(original_path)
    return rows, tuple(identities)


def _git_is_ancestor(repository: Path, ancestor: str, descendant: str) -> bool:
    try:
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=repository,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise BibliographyImportError(f"Cannot execute Git ancestry check: {exc}") from exc
    if completed.returncode == 0:
        return True
    if completed.returncode == 1:
        return False
    raise BibliographyImportError(
        "Git ancestry check failed: " + (completed.stderr.strip() or f"exit {completed.returncode}")
    )


def _validate_ancestry(
    corpus_commit: str,
    citation_commit: str,
    checkout_commit: str,
    source_repository: Path | None,
    ancestry_checker: Callable[[str, str], bool] | None,
) -> None:
    if ancestry_checker is None:
        if source_repository is None:
            raise BibliographyImportError(
                "A source repository checkout is required to validate source-commit ancestry"
            )
        repository = source_repository.resolve()
        ancestry_checker = lambda ancestor, descendant: _git_is_ancestor(repository, ancestor, descendant)
    for label, source_commit in (
        ("complete-corpus", corpus_commit), ("citation-ready", citation_commit)
    ):
        if not ancestry_checker(source_commit, checkout_commit):
            raise BibliographyImportError(
                f"{label} source commit {source_commit} is not an ancestor of checkout {checkout_commit}"
            )


def _assert_expectation(label: str, actual: int, expected: int | None) -> None:
    if expected is not None and actual != expected:
        raise BibliographyImportError(f"Unexpected {label}: {actual}; expected {expected}")


def validate_package(
    package: Path,
    requested_ref: str,
    checkout_commit: str,
    source_repository: Path | None = None,
    *,
    ancestry_checker: Callable[[str, str], bool] | None = None,
    expected_source_count: int | None = None,
    expected_selected_source_count: int | None = None,
    expected_research_material_count: int | None = None,
    expected_original_pdf_count: int | None = None,
    expected_schema_version: int | None = None,
    installed: bool = False,
) -> PackageSummary:
    package = package.resolve()
    if not package.is_dir():
        raise BibliographyImportError(f"Research-corpus directory does not exist: {package}")
    if not requested_ref.strip():
        raise BibliographyImportError("requested_ref must not be empty")
    checkout = _require_commit(checkout_commit, "checkout_commit")
    _validate_structure(package)
    legacy_text_encodings: dict[str, str] = {}
    legacy_text_controls: dict[str, dict[str, int]] = {}
    corpus_files = _walk_files(
        package,
        ignore_consumer_integrity=installed,
        legacy_text_encodings=legacy_text_encodings,
        legacy_text_controls=legacy_text_controls,
    )
    citation_root = package / CITATION_ROOT
    citation_files = _walk_files(citation_root)
    _validate_checksum_scope(package, corpus_files, CORPUS_CHECKSUMS)
    _validate_checksum_scope(citation_root, citation_files, Path("catalog/SHA256SUMS"))
    corpus_metadata, citation_metadata, corpus_commit, citation_commit = _validate_metadata(
        package, corpus_files, citation_files
    )
    source_ids, selected_ids, material_ids = _validate_identifiers_and_counts(
        package, corpus_metadata, citation_metadata
    )
    if not installed:
        _validate_ancestry(
            corpus_commit, citation_commit, checkout, source_repository, ancestry_checker
        )
    schema_version = int(corpus_metadata.get("schema_version", -1))
    original_pdf_count = int(corpus_metadata.get("original_pdf_count", -1))
    _assert_expectation("source_count", len(source_ids), expected_source_count)
    _assert_expectation("selected_source_count", len(selected_ids), expected_selected_source_count)
    _assert_expectation("research_material_count", len(material_ids), expected_research_material_count)
    _assert_expectation("original_pdf_count", original_pdf_count, expected_original_pdf_count)
    _assert_expectation("schema_version", schema_version, expected_schema_version)
    file_hashes = {relative: sha256(path) for relative, path in corpus_files.items()}
    return PackageSummary(
        requested_ref=requested_ref.strip(),
        checkout_commit=checkout,
        corpus_source_commit=corpus_commit,
        citation_source_commit=citation_commit,
        source_ids=source_ids,
        selected_ids=selected_ids,
        material_ids=material_ids,
        file_hashes=file_hashes,
        corpus_file_count=int(corpus_metadata["file_count"]),
        original_pdf_count=original_pdf_count,
        corpus_schema_version=schema_version,
        corpus_metadata_sha256=sha256(package / CORPUS_METADATA),
        corpus_checksums_sha256=sha256(package / CORPUS_CHECKSUMS),
        citation_metadata_sha256=sha256(package / CITATION_METADATA),
        citation_checksums_sha256=sha256(package / CITATION_CHECKSUMS),
        legacy_text_encodings=legacy_text_encodings,
        legacy_text_controls=legacy_text_controls,
    )


def _integrity_payload(summary: PackageSummary) -> dict[str, object]:
    return {
        "schema_version": 2,
        "source_repository": "MariosGiannakaras/ThesisBibliography",
        "requested_ref": summary.requested_ref,
        "checkout_commit": summary.checkout_commit,
        "corpus_source_commit": summary.corpus_source_commit,
        "citation_source_commit": summary.citation_source_commit,
        "imported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "consumer_importer_schema_version": 2,
        "corpus_file_count": summary.corpus_file_count,
        "imported_file_count": len(summary.file_hashes),
        "source_count": summary.source_count,
        "selected_source_count": summary.selected_source_count,
        "research_material_count": summary.research_material_count,
        "original_pdf_count": summary.original_pdf_count,
        "upstream_corpus_schema_version": summary.corpus_schema_version,
        "upstream_metadata_sha256": summary.corpus_metadata_sha256,
        "upstream_checksum_manifest_sha256": summary.corpus_checksums_sha256,
        "citation_metadata_sha256": summary.citation_metadata_sha256,
        "citation_checksum_manifest_sha256": summary.citation_checksums_sha256,
        "ancestry_validated": True,
        "legacy_text_encodings": summary.legacy_text_encodings,
        "legacy_text_controls": summary.legacy_text_controls,
        "files": summary.file_hashes,
    }


def write_integrity_manifest(destination: Path, summary: PackageSummary) -> None:
    (destination / CONSUMER_INTEGRITY).write_text(
        json.dumps(_integrity_payload(summary), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _summary_from_integrity(destination: Path, integrity: dict[str, object]) -> PackageSummary:
    required_strings = (
        "requested_ref", "checkout_commit", "corpus_source_commit", "citation_source_commit",
        "upstream_metadata_sha256", "upstream_checksum_manifest_sha256",
        "citation_metadata_sha256", "citation_checksum_manifest_sha256",
    )
    for key in required_strings:
        if not isinstance(integrity.get(key), str) or not str(integrity[key]):
            raise BibliographyImportError(f"IMPORT_INTEGRITY.json has invalid {key}")
    checkout = _require_commit(str(integrity["checkout_commit"]), "checkout_commit")
    corpus = _require_commit(str(integrity["corpus_source_commit"]), "corpus_source_commit")
    citation = _require_commit(str(integrity["citation_source_commit"]), "citation_source_commit")
    summary = validate_package(
        destination,
        requested_ref=str(integrity["requested_ref"]),
        checkout_commit=checkout,
        installed=True,
    )
    if summary.corpus_source_commit != corpus or summary.citation_source_commit != citation:
        raise BibliographyImportError("IMPORT_INTEGRITY.json source commits differ from installed package")
    recorded_encodings = integrity.get("legacy_text_encodings", {})
    if not isinstance(recorded_encodings, dict):
        raise BibliographyImportError("IMPORT_INTEGRITY.json has invalid legacy_text_encodings")
    normalized_encodings = {str(key): str(value) for key, value in recorded_encodings.items()}
    if normalized_encodings != summary.legacy_text_encodings:
        raise BibliographyImportError(
            "IMPORT_INTEGRITY.json legacy text encoding map differs from installed package"
        )
    recorded_controls = integrity.get("legacy_text_controls", {})
    if not isinstance(recorded_controls, dict):
        raise BibliographyImportError("IMPORT_INTEGRITY.json has invalid legacy_text_controls")
    normalized_controls: dict[str, dict[str, int]] = {}
    for path, counts in recorded_controls.items():
        if not isinstance(counts, dict):
            raise BibliographyImportError("IMPORT_INTEGRITY.json has invalid legacy_text_controls")
        normalized_controls[str(path)] = {str(key): int(value) for key, value in counts.items()}
    if normalized_controls != summary.legacy_text_controls:
        raise BibliographyImportError(
            "IMPORT_INTEGRITY.json legacy text control map differs from installed package"
        )
    return summary


def validate_installed_package(destination: Path) -> PackageSummary:
    destination = destination.resolve()
    integrity_path = destination / CONSUMER_INTEGRITY
    if not integrity_path.is_file():
        raise BibliographyImportError("Imported bibliography is missing IMPORT_INTEGRITY.json")
    integrity = _load_json(integrity_path, "IMPORT_INTEGRITY.json")
    if integrity.get("schema_version") != 2 or integrity.get("consumer_importer_schema_version") != 2:
        raise BibliographyImportError("Unsupported IMPORT_INTEGRITY.json schema version")
    if integrity.get("source_repository") != "MariosGiannakaras/ThesisBibliography":
        raise BibliographyImportError("Unexpected bibliography source repository")
    if integrity.get("ancestry_validated") is not True:
        raise BibliographyImportError("IMPORT_INTEGRITY.json does not record successful ancestry validation")
    summary = _summary_from_integrity(destination, integrity)
    expected_files = integrity.get("files")
    if not isinstance(expected_files, dict):
        raise BibliographyImportError("IMPORT_INTEGRITY.json has no file hash map")
    normalized_expected = {str(key): str(value) for key, value in expected_files.items()}
    actual_files = _walk_files(destination, ignore_consumer_integrity=True)
    actual_hashes = {relative: sha256(path) for relative, path in actual_files.items()}
    if normalized_expected != actual_hashes:
        missing = sorted(set(normalized_expected) - set(actual_hashes))
        extra = sorted(set(actual_hashes) - set(normalized_expected))
        changed = sorted(
            key for key in set(actual_hashes) & set(normalized_expected)
            if actual_hashes[key] != normalized_expected[key]
        )
        raise BibliographyImportError(
            "Generated bibliography was modified outside the sync workflow "
            f"(missing={missing[:10]}, extra={extra[:10]}, changed={changed[:10]})"
        )
    expected_scalars = {
        "corpus_file_count": summary.corpus_file_count,
        "imported_file_count": len(summary.file_hashes),
        "source_count": summary.source_count,
        "selected_source_count": summary.selected_source_count,
        "research_material_count": summary.research_material_count,
        "original_pdf_count": summary.original_pdf_count,
        "upstream_corpus_schema_version": summary.corpus_schema_version,
        "upstream_metadata_sha256": summary.corpus_metadata_sha256,
        "upstream_checksum_manifest_sha256": summary.corpus_checksums_sha256,
        "citation_metadata_sha256": summary.citation_metadata_sha256,
        "citation_checksum_manifest_sha256": summary.citation_checksums_sha256,
    }
    for key, expected in expected_scalars.items():
        if integrity.get(key) != expected:
            raise BibliographyImportError(f"IMPORT_INTEGRITY.json {key} does not match installed package")
    return summary


def install_package(
    package: Path,
    destination: Path,
    requested_ref: str,
    checkout_commit: str,
    source_repository: Path | None = None,
    *,
    ancestry_checker: Callable[[str, str], bool] | None = None,
    expected_source_count: int | None = None,
    expected_selected_source_count: int | None = None,
    expected_research_material_count: int | None = None,
    expected_original_pdf_count: int | None = None,
    expected_schema_version: int | None = None,
    install_hook: Callable[[Path, Path], None] | None = None,
) -> PackageSummary:
    summary = validate_package(
        package,
        requested_ref,
        checkout_commit,
        source_repository,
        ancestry_checker=ancestry_checker,
        expected_source_count=expected_source_count,
        expected_selected_source_count=expected_selected_source_count,
        expected_research_material_count=expected_research_material_count,
        expected_original_pdf_count=expected_original_pdf_count,
        expected_schema_version=expected_schema_version,
    )
    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bibliography-import-", dir=destination.parent) as temporary:
        staged = Path(temporary) / "bibliography"
        shutil.copytree(package, staged, copy_function=shutil.copy2)
        write_integrity_manifest(staged, summary)
        validate_installed_package(staged)
        backup = destination.with_name(destination.name + ".previous")
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            destination.replace(backup)
        try:
            if install_hook is not None:
                install_hook(staged, destination)
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


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("expected a non-negative integer")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path)
    parser.add_argument("--requested-ref")
    parser.add_argument("--checkout-commit")
    parser.add_argument("--source-repository", type=Path)
    parser.add_argument(
        "--destination", type=Path,
        default=Path(__file__).resolve().parents[1] / "research" / "bibliography",
    )
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--expect-source-count", type=_positive_int)
    parser.add_argument("--expect-selected-source-count", type=_positive_int)
    parser.add_argument("--expect-research-material-count", type=_positive_int)
    parser.add_argument("--expect-original-pdf-count", type=_positive_int)
    parser.add_argument("--expect-schema-version", type=_positive_int)
    args = parser.parse_args()
    try:
        if args.validate_only:
            summary = validate_installed_package(args.destination)
        else:
            missing = [
                name for name, value in (
                    ("--package", args.package), ("--requested-ref", args.requested_ref),
                    ("--checkout-commit", args.checkout_commit),
                    ("--source-repository", args.source_repository),
                ) if value is None
            ]
            if missing:
                parser.error("installation requires " + ", ".join(missing))
            summary = install_package(
                args.package,
                args.destination,
                args.requested_ref,
                args.checkout_commit,
                args.source_repository,
                expected_source_count=args.expect_source_count,
                expected_selected_source_count=args.expect_selected_source_count,
                expected_research_material_count=args.expect_research_material_count,
                expected_original_pdf_count=args.expect_original_pdf_count,
                expected_schema_version=args.expect_schema_version,
            )
    except BibliographyImportError as exc:
        print(f"Bibliography import validation failed: {exc}")
        return 1
    print(
        "Bibliography corpus valid: "
        f"{summary.source_count} canonical sources, "
        f"{summary.selected_source_count} citation-ready sources, "
        f"{summary.research_material_count} research materials; "
        f"checkout={summary.checkout_commit}, corpus={summary.corpus_source_commit}, "
        f"citation={summary.citation_source_commit}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
