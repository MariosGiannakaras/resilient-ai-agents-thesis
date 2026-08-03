from __future__ import annotations

import hashlib
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
from search_bibliography import build_index, search_documents  # noqa: E402
from test_bibliography_import import (  # noqa: E402
    CHECKOUT_COMMIT,
    MATERIAL_ID,
    REJECTED_ID,
    SOURCE_ID,
    CorpusFixture,
    ancestry,
)


class BibliographySearchTests(unittest.TestCase):
    def setup_corpus(self, root: Path):
        fixture = CorpusFixture(root)
        (fixture.package / "notes" / "README.md").write_text(
            "# Personal note\n\nA metadata-free note about recovery latency.\n", encoding="utf-8"
        )
        fixture.refresh()
        destination = root / "research" / "bibliography"
        install_package(fixture.package, destination, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)
        return destination

    def test_note_is_searchable_without_bibliographic_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setup_corpus(root)
            documents = build_index(import_dir, root / "index.json")
            results = search_documents(documents, "recovery latency", include_rejected=True)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][0].trust, "author-note")
            self.assertEqual(results[0][0].identifier, "")

    def test_search_results_expose_trust_labels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setup_corpus(root)
            documents = build_index(import_dir, root / "index.json")
            selected = search_documents(documents, "Selected source", identifier=SOURCE_ID)
            rejected = search_documents(documents, "Rejected source", identifier=REJECTED_ID)
            material = search_documents(documents, "Material", identifier=MATERIAL_ID)
            self.assertTrue(selected)
            self.assertEqual({item[0].trust for item in selected}, {"citation-ready"})
            self.assertTrue(rejected)
            self.assertEqual({item[0].trust for item in rejected}, {"rejected"})
            self.assertTrue(material)
            self.assertEqual({item[0].trust for item in material}, {"research-material"})


    def test_cesu8_source_is_searchable_with_recorded_encoding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = CorpusFixture(root)
            source = fixture.package / "sources" / f"{SOURCE_ID}.md"
            source.write_bytes(b"# Legacy source\n\nEquation marker \xed\xa0\xb5\xed\xb1\xa2\n")
            fixture.refresh()
            import_dir = root / "research" / "bibliography"
            install_package(fixture.package, import_dir, "tag", CHECKOUT_COMMIT, ancestry_checker=ancestry)
            documents = build_index(import_dir, root / "index.json")
            results = search_documents(documents, "Equation marker", identifier=SOURCE_ID)
            self.assertTrue(results)
            self.assertEqual(results[0][0].text_encoding, "cesu-8")
            self.assertIn("𝑢", results[0][0].text)

    def test_rebuilding_search_index_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setup_corpus(root)
            index = root / "index.json"
            build_index(import_dir, index)
            first = hashlib.sha256(index.read_bytes()).hexdigest()
            build_index(import_dir, index)
            second = hashlib.sha256(index.read_bytes()).hexdigest()
            self.assertEqual(first, second)

    def test_rejected_sources_require_explicit_inclusion_for_free_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import_dir = self.setup_corpus(root)
            documents = build_index(import_dir, root / "index.json")
            self.assertFalse(search_documents(documents, "Rejected source"))
            self.assertTrue(search_documents(documents, "Rejected source", include_rejected=True))


if __name__ == "__main__":
    unittest.main()
