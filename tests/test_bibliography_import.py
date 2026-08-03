from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from bibliography_import import (  # noqa: E402
    BibliographyImportError,
    install_package,
    validate_installed_package,
    validate_package,
)

SOURCE_ID = "SRC-0123456789"
REJECTED_ID = "SRC-AAAAAAAAAA"
MATERIAL_ID = "MAT-ABCDEF1234"
CHECKOUT_COMMIT = "f" * 40
CORPUS_COMMIT = "a" * 40
CITATION_COMMIT = "b" * 40


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def content_files(root: Path) -> list[Path]:
    excluded = {Path("catalog/package-metadata.json"), Path("catalog/SHA256SUMS")}
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.relative_to(root) not in excluded
    )


def write_integrity(root: Path, metadata: dict[str, object]) -> None:
    files = content_files(root)
    checksum = root / "catalog" / "SHA256SUMS"
    checksum.parent.mkdir(parents=True, exist_ok=True)
    checksum.write_text(
        "".join(f"{sha256(path)}  {path.relative_to(root).as_posix()}\n" for path in files),
        encoding="utf-8",
    )
    metadata = dict(metadata)
    metadata["file_count"] = len(files)
    (root / "catalog" / "package-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


class CorpusFixture:
    def __init__(self, root: Path) -> None:
        self.package = root / "research-corpus"
        self.package.mkdir()
        for directory in (
            "sources", "analyses", "evidence", "materials", "notes", "aggregates", "catalog",
            "citation-ready/analyses", "citation-ready/evidence", "citation-ready/catalog",
        ):
            (self.package / directory).mkdir(parents=True, exist_ok=True)
        (self.package / "README.md").write_text("# Complete corpus\n", encoding="utf-8")
        (self.package / "SOURCE_COMMIT").write_text(CORPUS_COMMIT + "\n", encoding="utf-8")
        (self.package / "sources" / f"{SOURCE_ID}.md").write_text("# Selected source\n", encoding="utf-8")
        (self.package / "sources" / f"{REJECTED_ID}.md").write_text("# Rejected source\n", encoding="utf-8")
        (self.package / "analyses" / "README.md").write_text("# Analyses\n", encoding="utf-8")
        (self.package / "analyses" / f"{SOURCE_ID}.md").write_text("# Analysis\n", encoding="utf-8")
        (self.package / "analyses" / f"{REJECTED_ID}.md").write_text("# Rejected analysis\n", encoding="utf-8")
        (self.package / "evidence" / f"{SOURCE_ID}.md").write_text("# Evidence\n", encoding="utf-8")
        (self.package / "materials" / f"{MATERIAL_ID}.md").write_text("# Material\n", encoding="utf-8")
        (self.package / "notes" / "README.md").write_text("# Personal note\n", encoding="utf-8")
        (self.package / "aggregates" / "USEFUL_EVIDENCE.md").write_text("# Aggregate\n", encoding="utf-8")

        source_fields = ["Κωδικός", "Τίτλος", "Θέματα"]
        write_csv(
            self.package / "catalog" / "sources.csv", source_fields,
            [
                {"Κωδικός": SOURCE_ID, "Τίτλος": "Selected source", "Θέματα": "adaptation"},
                {"Κωδικός": REJECTED_ID, "Τίτλος": "Rejected source", "Θέματα": "noise"},
            ],
        )
        write_csv(
            self.package / "catalog" / "thesis-selection.csv",
            ["Κωδικός", "Ρόλος", "Κατάσταση", "Εξαγωγή"],
            [{"Κωδικός": SOURCE_ID, "Ρόλος": "κύρια", "Κατάσταση": "επαληθευμένη", "Εξαγωγή": "ναι"}],
        )
        write_csv(
            self.package / "catalog" / "analysis-status.csv",
            ["Κωδικός", "Κατάσταση ανάλυσης", "Ρόλος", "Εξαγωγή"],
            [
                {"Κωδικός": SOURCE_ID, "Κατάσταση ανάλυσης": "πλήρης", "Ρόλος": "κύρια", "Εξαγωγή": "ναι"},
                {"Κωδικός": REJECTED_ID, "Κατάσταση ανάλυσης": "απορρίφθηκε", "Ρόλος": "απόρριψη", "Εξαγωγή": "όχι"},
            ],
        )
        write_csv(
            self.package / "catalog" / "research-materials.csv",
            ["material_id", "title_candidate", "linked_source_id", "original_path"],
            [{"material_id": MATERIAL_ID, "title_candidate": "Material", "linked_source_id": "", "original_path": "originals/x.pdf"}],
        )
        write_csv(
            self.package / "catalog" / "research-material-review.csv",
            ["material_id", "canonical_title", "identification_status", "confidence", "thesis_relevance"],
            [{"material_id": MATERIAL_ID, "canonical_title": "Material", "identification_status": "identified", "confidence": "high", "thesis_relevance": "medium"}],
        )
        write_csv(
            self.package / "catalog" / "originals-index.csv",
            ["original_path", "sha256", "linked_source_id", "research_material_id", "immutable_url", "storage"],
            [{"original_path": "originals/x.pdf", "sha256": "1" * 64, "linked_source_id": "", "research_material_id": MATERIAL_ID, "immutable_url": "https://example.invalid/x", "storage": "Git LFS"}],
        )

        citation = self.package / "citation-ready"
        (citation / "README.md").write_text("# Citation ready\n", encoding="utf-8")
        (citation / "SOURCE_COMMIT").write_text(CITATION_COMMIT + "\n", encoding="utf-8")
        write_csv(
            citation / "manifest.csv",
            ["Κωδικός", "Ρόλος", "Κατάσταση", "Εξαγωγή", "Τίτλος"],
            [{"Κωδικός": SOURCE_ID, "Ρόλος": "κύρια", "Κατάσταση": "επαληθευμένη", "Εξαγωγή": "ναι", "Τίτλος": "Selected source"}],
        )
        write_csv(citation / "catalog" / "sources.csv", source_fields, [
            {"Κωδικός": SOURCE_ID, "Τίτλος": "Selected source", "Θέματα": "adaptation"}
        ])
        (citation / "analyses" / f"{SOURCE_ID}.md").write_text("# Verified analysis\n", encoding="utf-8")
        (citation / "evidence" / f"{SOURCE_ID}.md").write_text("# Verified evidence\n", encoding="utf-8")
        write_integrity(citation, {
            "schema_version": 1,
            "package_type": "ThesisBibliography verified thesis package",
            "source_commit": CITATION_COMMIT,
            "selected_sources": 1,
            "hash_algorithm": "sha256",
            "checksum_file": "catalog/SHA256SUMS",
        })
        write_integrity(self.package, {
            "schema_version": 1,
            "package_type": "ThesisBibliography complete research corpus",
            "source_commit": CORPUS_COMMIT,
            "source_count": 2,
            "selected_source_count": 1,
            "research_material_count": 1,
            "original_pdf_count": 1,
            "hash_algorithm": "sha256",
            "checksum_file": "catalog/SHA256SUMS",
            "copied_file_counts": {"sources": 2, "analyses": 3, "evidence": 1, "materials": 1, "notes": 1},
        })

    def refresh(self) -> None:
        citation = self.package / "citation-ready"
        citation_metadata = json.loads((citation / "catalog" / "package-metadata.json").read_text(encoding="utf-8"))
        write_integrity(citation, citation_metadata)
        corpus_metadata = json.loads((self.package / "catalog" / "package-metadata.json").read_text(encoding="utf-8"))
        write_integrity(self.package, corpus_metadata)


def ancestry(ancestor: str, descendant: str) -> bool:
    return descendant == CHECKOUT_COMMIT and ancestor in {CORPUS_COMMIT, CITATION_COMMIT}


class BibliographyImportTests(unittest.TestCase):
    def test_valid_complete_corpus_installs_and_revalidates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = CorpusFixture(root)
            destination = root / "research" / "bibliography"
            summary = install_package(
                fixture.package, destination, "bibliography-integration-v2", CHECKOUT_COMMIT,
                ancestry_checker=ancestry,
                expected_source_count=2,
                expected_selected_source_count=1,
                expected_research_material_count=1,
                expected_original_pdf_count=1,
                expected_schema_version=1,
            )
            self.assertEqual(summary.corpus_source_commit, CORPUS_COMMIT)
            self.assertEqual(summary.citation_source_commit, CITATION_COMMIT)
            self.assertNotEqual(summary.checkout_commit, summary.corpus_source_commit)
            self.assertEqual(validate_installed_package(destination).selected_ids, (SOURCE_ID,))

    def test_non_ancestor_source_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            with self.assertRaises(BibliographyImportError):
                validate_package(
                    fixture.package, "tag", CHECKOUT_COMMIT,
                    ancestry_checker=lambda ancestor, descendant: ancestor == CORPUS_COMMIT,
                )

    def test_metadata_source_commit_disagreement_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            path = fixture.package / "citation-ready" / "catalog" / "package-metadata.json"
            metadata = json.loads(path.read_text(encoding="utf-8"))
            metadata["source_commit"] = "c" * 40
            path.write_text(json.dumps(metadata), encoding="utf-8")
            fixture.refresh()
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_checksum_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            (fixture.package / "sources" / f"{SOURCE_ID}.md").write_text("changed\n", encoding="utf-8")
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_checksum_path_set_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            checksums = fixture.package / "catalog" / "SHA256SUMS"
            checksums.write_text("\n".join(checksums.read_text(encoding="utf-8").splitlines()[:-1]) + "\n", encoding="utf-8")
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_duplicate_checksum_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            checksums = fixture.package / "catalog" / "SHA256SUMS"
            first = checksums.read_text(encoding="utf-8").splitlines()[0]
            checksums.write_text(checksums.read_text(encoding="utf-8") + first + "\n", encoding="utf-8")
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_path_traversal_checksum_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            checksums = fixture.package / "catalog" / "SHA256SUMS"
            checksums.write_text(checksums.read_text(encoding="utf-8") + f"{'0'*64}  ../escape\n", encoding="utf-8")
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_missing_required_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            (fixture.package / "notes" / "README.md").unlink()
            (fixture.package / "notes").rmdir()
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_missing_and_extra_material_review_rows_are_rejected(self) -> None:
        for mode in ("missing", "extra"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                fixture = CorpusFixture(Path(directory))
                review = fixture.package / "catalog" / "research-material-review.csv"
                if mode == "missing":
                    write_csv(review, ["material_id", "canonical_title", "identification_status", "confidence", "thesis_relevance"], [])
                else:
                    write_csv(review, ["material_id", "canonical_title", "identification_status", "confidence", "thesis_relevance"], [
                        {"material_id": MATERIAL_ID, "canonical_title": "Material", "identification_status": "identified", "confidence": "high", "thesis_relevance": "medium"},
                        {"material_id": "MAT-0000000000", "canonical_title": "Extra", "identification_status": "identified", "confidence": "low", "thesis_relevance": "low"},
                    ])
                fixture.refresh()
                with self.assertRaises(BibliographyImportError):
                    validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_invalid_source_and_material_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            sources = fixture.package / "catalog" / "sources.csv"
            text = sources.read_text(encoding="utf-8").replace(SOURCE_ID, "SRC-invalid")
            sources.write_text(text, encoding="utf-8")
            fixture.refresh()
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            materials = fixture.package / "catalog" / "research-materials.csv"
            materials.write_text(materials.read_text(encoding="utf-8").replace(MATERIAL_ID, "MAT-invalid"), encoding="utf-8")
            fixture.refresh()
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_forbidden_pdf_lfs_symlink_and_invalid_utf8_are_rejected(self) -> None:
        cases = ("pdf", "lfs", "symlink", "utf8")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                fixture = CorpusFixture(Path(directory))
                if case == "pdf":
                    (fixture.package / "sources" / "bad.pdf").write_bytes(b"%PDF")
                elif case == "lfs":
                    (fixture.package / "sources" / "bad.md").write_bytes(b"version https://git-lfs.github.com/spec/v1\n")
                elif case == "symlink":
                    try:
                        os.symlink(fixture.package / "README.md", fixture.package / "sources" / "link.md")
                    except (OSError, NotImplementedError):
                        self.skipTest("symlinks unavailable")
                else:
                    (fixture.package / "sources" / "bad.md").write_bytes(b"\xff\xfe")
                with self.assertRaises(BibliographyImportError):
                    validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)


    def test_well_formed_cesu8_source_markdown_is_recorded_without_rewriting(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = CorpusFixture(root)
            source = fixture.package / "sources" / f"{SOURCE_ID}.md"
            original = b"# Legacy source\n\nEquation: \xed\xa0\xb5\xed\xb1\xa2\n"
            source.write_bytes(original)
            fixture.refresh()
            destination = root / "bibliography"
            summary = install_package(
                fixture.package, destination, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry
            )
            relative = f"sources/{SOURCE_ID}.md"
            self.assertEqual(summary.legacy_text_encodings, {relative: "cesu-8"})
            self.assertEqual((destination / relative).read_bytes(), original)
            integrity = json.loads((destination / "IMPORT_INTEGRITY.json").read_text(encoding="utf-8"))
            self.assertEqual(integrity["legacy_text_encodings"], {relative: "cesu-8"})
            self.assertEqual(validate_installed_package(destination).legacy_text_encodings, {relative: "cesu-8"})

    def test_cesu8_is_rejected_outside_canonical_source_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            path = fixture.package / "analyses" / f"{SOURCE_ID}.md"
            path.write_bytes(b"# Analysis\n\xed\xa0\xb5\xed\xb1\xa2\n")
            fixture.refresh()
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_byte_preserved_controls_are_recorded_only_for_full_text_layers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = CorpusFixture(root)
            source = fixture.package / "sources" / f"{SOURCE_ID}.md"
            material = fixture.package / "materials" / f"{MATERIAL_ID}.md"
            source_bytes = b"# Selected source\n\x00alpha\x1cbeta\n"
            material_bytes = b"# Material\nleft\x14right\x1bright\n"
            source.write_bytes(source_bytes)
            material.write_bytes(material_bytes)
            fixture.refresh()
            destination = root / "bibliography"
            summary = install_package(
                fixture.package, destination, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry
            )
            expected = {
                f"materials/{MATERIAL_ID}.md": {"U+0014": 1, "U+001B": 1},
                f"sources/{SOURCE_ID}.md": {"U+0000": 1, "U+001C": 1},
            }
            self.assertEqual(summary.legacy_text_controls, expected)
            self.assertEqual((destination / "sources" / f"{SOURCE_ID}.md").read_bytes(), source_bytes)
            self.assertEqual((destination / "materials" / f"{MATERIAL_ID}.md").read_bytes(), material_bytes)
            integrity = json.loads((destination / "IMPORT_INTEGRITY.json").read_text(encoding="utf-8"))
            self.assertEqual(integrity["legacy_text_controls"], expected)
            self.assertEqual(validate_installed_package(destination).legacy_text_controls, expected)

    def test_control_characters_remain_rejected_outside_full_text_layers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = CorpusFixture(Path(directory))
            path = fixture.package / "analyses" / f"{SOURCE_ID}.md"
            path.write_bytes(b"# Analysis\nunsafe\x00control\n")
            fixture.refresh()
            with self.assertRaises(BibliographyImportError):
                validate_package(fixture.package, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)

    def test_installed_control_map_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = CorpusFixture(root)
            source = fixture.package / "sources" / f"{SOURCE_ID}.md"
            source.write_bytes(b"# Selected source\nleft\x00right\n")
            fixture.refresh()
            destination = root / "bibliography"
            install_package(fixture.package, destination, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)
            integrity_path = destination / "IMPORT_INTEGRITY.json"
            integrity = json.loads(integrity_path.read_text(encoding="utf-8"))
            integrity["legacy_text_controls"] = {}
            integrity_path.write_text(json.dumps(integrity), encoding="utf-8")
            with self.assertRaises(BibliographyImportError):
                validate_installed_package(destination)

    def test_manual_post_import_modification_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = CorpusFixture(root)
            destination = root / "bibliography"
            install_package(fixture.package, destination, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)
            path = destination / "sources" / f"{SOURCE_ID}.md"
            path.write_text(path.read_text(encoding="utf-8") + "manual\n", encoding="utf-8")
            with self.assertRaises(BibliographyImportError):
                validate_installed_package(destination)

    def test_failure_before_replacement_preserves_previous_import(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "bibliography"
            destination.mkdir()
            marker = destination / "marker.txt"
            marker.write_text("keep", encoding="utf-8")
            fixture = CorpusFixture(root)
            (fixture.package / "catalog" / "SHA256SUMS").write_text("broken\n", encoding="utf-8")
            with self.assertRaises(BibliographyImportError):
                install_package(fixture.package, destination, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_install_failure_rolls_back_previous_import(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = CorpusFixture(root)
            destination = root / "bibliography"
            destination.mkdir()
            marker = destination / "marker.txt"
            marker.write_text("keep", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                install_package(
                    fixture.package, destination, "tag", CHECKOUT_COMMIT,
                    ancestry_checker=ancestry,
                    install_hook=lambda staged, target: (_ for _ in ()).throw(RuntimeError("boom")),
                )
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
