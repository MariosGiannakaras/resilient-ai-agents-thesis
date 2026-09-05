from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(Path(__file__).parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent))

from bibliography_import import install_package  # noqa: E402
from validate_bibliography_usage import validate_references  # noqa: E402
from test_bibliography_import import (  # noqa: E402
    CHECKOUT_COMMIT,
    MATERIAL_ID,
    REJECTED_ID,
    SOURCE_ID,
    CorpusFixture,
    ancestry,
)


class BibliographyUsageTests(unittest.TestCase):
    def setUpCorpus(self, root: Path) -> Path:
        fixture = CorpusFixture(root)
        destination = root / "research" / "bibliography"
        install_package(fixture.package, destination, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)
        return destination

    def validate_text(self, root: Path, import_dir: Path, relative: str, text: str):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return validate_references(root, import_dir, [path])

    def test_citation_ready_source_is_accepted_in_formal_thesis_prose(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setUpCorpus(root)
            uses, errors = self.validate_text(root, import_dir, "thesis/chapters/method.md", SOURCE_ID)
            self.assertFalse(errors)
            self.assertEqual(uses[0].trust, "citation-ready")
            self.assertEqual(uses[0].context, "formal")

    def test_rejected_source_is_rejected_as_formal_citation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setUpCorpus(root)
            _uses, errors = self.validate_text(root, import_dir, "thesis/chapters/results.md", REJECTED_ID)
            self.assertTrue(any("non-citation-ready" in error for error in errors))

    def test_full_corpus_source_is_accepted_in_internal_research_notes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setUpCorpus(root)
            uses, errors = self.validate_text(root, import_dir, "docs/research/workspace.md", REJECTED_ID)
            self.assertFalse(errors)
            self.assertEqual(uses[0].trust, "rejected")
            self.assertEqual(uses[0].context, "internal")

    def test_docs_thesis_audit_and_mapping_are_internal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setUpCorpus(root)
            for relative in (
                "docs/thesis/audits/full-corpus-audit.md",
                "docs/thesis/CLAIM_EVIDENCE_TREE.md",
                "docs/thesis/claim-evidence-map.json",
                "docs/thesis/T716_REWRITE_PLAN.md",
            ):
                uses, errors = self.validate_text(root, import_dir, relative, REJECTED_ID)
                self.assertFalse(errors, relative)
                self.assertEqual(uses[0].context, "internal", relative)

    def test_material_is_valid_internal_but_not_in_explicit_final_or_manuscript_prose(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setUpCorpus(root)

            uses, errors = self.validate_text(root, import_dir, "docs/research/material-notes.md", MATERIAL_ID)
            self.assertFalse(errors)
            self.assertEqual(uses[0].trust, "research-material")
            self.assertEqual(uses[0].context, "internal")

            uses, errors = self.validate_text(root, import_dir, "docs/thesis/draft.md", MATERIAL_ID)
            self.assertFalse(errors)
            self.assertEqual(uses[0].context, "internal")

            _uses, errors = self.validate_text(root, import_dir, "thesis/chapters/method.md", MATERIAL_ID)
            self.assertTrue(any("MAT-* is not a formal citation" in error for error in errors))

            _uses, errors = self.validate_text(
                root,
                import_dir,
                "docs/thesis/frozen-methodology.md",
                f"Status: Frozen\n\n{MATERIAL_ID}",
            )
            self.assertTrue(any("MAT-* is not a formal citation" in error for error in errors))

    def test_non_ready_source_rejected_in_explicit_final_docs_thesis_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setUpCorpus(root)
            uses, errors = self.validate_text(
                root,
                import_dir,
                "docs/thesis/submission-record.md",
                f"Status: Final\n\n{REJECTED_ID}",
            )
            self.assertEqual(uses[0].context, "formal")
            self.assertTrue(any("non-citation-ready" in error for error in errors))

    def test_unknown_identifiers_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setUpCorpus(root)
            _uses, errors = self.validate_text(
                root, import_dir, "docs/research/unknown.md", "SRC-FFFFFFFFFF MAT-FFFFFFFFFF"
            )
            self.assertEqual(len(errors), 2)


if __name__ == "__main__":
    unittest.main()
