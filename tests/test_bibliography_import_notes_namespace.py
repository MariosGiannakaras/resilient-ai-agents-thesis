from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from bibliography_import import BibliographyImportError, _walk_files  # noqa: E402


class BibliographyImportNotesNamespaceTests(unittest.TestCase):
    def test_reviewed_notes_intake_namespace_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = root / "notes" / "intake" / "NOTE-TEST.md"
            note.parent.mkdir(parents=True)
            note.write_text("# Reviewed intake note\n", encoding="utf-8")

            files = _walk_files(root)

            self.assertIn("notes/intake/NOTE-TEST.md", files)

    def test_arbitrary_intake_directory_remains_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = root / "intake" / "raw.md"
            note.parent.mkdir(parents=True)
            note.write_text("raw\n", encoding="utf-8")

            with self.assertRaisesRegex(BibliographyImportError, "Forbidden directory"):
                _walk_files(root)


if __name__ == "__main__":
    unittest.main()
