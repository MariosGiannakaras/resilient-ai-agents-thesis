from __future__ import annotations

import csv
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
SOURCE_COMMIT = "a" * 40


class BibliographyImportTests(unittest.TestCase):
    def make_package(self, root: Path) -> Path:
        package = root / "package"
        (package / "catalog").mkdir(parents=True)
        (package / "analyses").mkdir()
        (package / "evidence").mkdir()
        (package / "README.md").write_text("verified package\n", encoding="utf-8")
        (package / "SOURCE_COMMIT").write_text(SOURCE_COMMIT + "\n", encoding="utf-8")

        manifest_fields = ["Κωδικός", "Ρόλος", "Κατάσταση", "Εξαγωγή"]
        with (package / "manifest.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=manifest_fields, lineterminator="\n")
            writer.writeheader()
            writer.writerow(
                {"Κωδικός": SOURCE_ID, "Ρόλος": "κύρια", "Κατάσταση": "επαληθευμένη", "Εξαγωγή": "ναι"}
            )

        with (package / "catalog" / "sources.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=["Κωδικός", "Τίτλος"], lineterminator="\n")
            writer.writeheader()
            writer.writerow({"Κωδικός": SOURCE_ID, "Τίτλος": "Example"})

        (package / "analyses" / f"{SOURCE_ID}.md").write_text(
            "# Analysis\n\nVerified scientific analysis.\n", encoding="utf-8"
        )
        (package / "evidence" / f"{SOURCE_ID}.md").write_text(
            "# Evidence\n\nStatus: verified.\n", encoding="utf-8"
        )
        return package

    def test_valid_package_installs_and_revalidates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = self.make_package(root)
            destination = root / "research" / "bibliography"

            summary = install_package(package, destination, SOURCE_COMMIT)

            self.assertEqual(summary.source_ids, (SOURCE_ID,))
            self.assertEqual(validate_installed_package(destination).source_commit, SOURCE_COMMIT)
            self.assertTrue((destination / "IMPORT_INTEGRITY.json").is_file())

    def test_source_commit_must_match_checked_out_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.make_package(Path(directory))
            with self.assertRaises(BibliographyImportError):
                validate_package(package, "b" * 40)

    def test_forbidden_pdf_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.make_package(Path(directory))
            (package / "forbidden.pdf").write_bytes(b"%PDF-1.4\n")
            with self.assertRaises(BibliographyImportError):
                validate_package(package, SOURCE_COMMIT)

    def test_manual_change_breaks_integrity_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = self.make_package(root)
            destination = root / "research" / "bibliography"
            install_package(package, destination, SOURCE_COMMIT)

            evidence = destination / "evidence" / f"{SOURCE_ID}.md"
            evidence.write_text(evidence.read_text(encoding="utf-8") + "manual edit\n", encoding="utf-8")

            with self.assertRaises(BibliographyImportError):
                validate_installed_package(destination)

    def test_manifest_and_analysis_sets_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.make_package(Path(directory))
            (package / "analyses" / f"{SOURCE_ID}.md").unlink()
            with self.assertRaises(BibliographyImportError):
                validate_package(package, SOURCE_COMMIT)


if __name__ == "__main__":
    unittest.main()
