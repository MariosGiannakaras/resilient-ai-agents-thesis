from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "download_open_access_bibliography.py"
SPEC = importlib.util.spec_from_file_location("bibliography_downloader", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def write_pdf(path: Path, marker: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"%PDF-1.7\n" + marker + b"x" * 2048)


class BibliographyDownloaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.original = self.root / "bibliography" / "original"
        self.manifest = self.root / "bibliography" / "source_manifest.json"
        self.source = MODULE.Source(
            "SRC-TEST-001",
            "related-work",
            "test.pdf",
            "Test source",
            "Test Author",
            2026,
            "Test publication",
            "https://example.invalid/test.pdf",
            "Test access",
        )
        self.patchers = [
            patch.object(MODULE, "REPOSITORY_ROOT", self.root),
            patch.object(MODULE, "ORIGINAL_DIR", self.original),
            patch.object(MODULE, "MANIFEST_PATH", self.manifest),
            patch.object(MODULE, "SOURCES", (self.source,)),
            patch.object(MODULE, "MANUAL_ACQUISITION", ()),
        ]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patchers):
            patcher.stop()
        self.tempdir.cleanup()

    def load_output(self) -> dict[str, object]:
        return json.loads(self.manifest.read_text(encoding="utf-8"))

    def test_unchanged_pdf_preserves_retrieval_and_review_status(self) -> None:
        pdf = self.original / "related-work" / "test.pdf"
        write_pdf(pdf, b"stable")
        checksum = MODULE.sha256_file(pdf)
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        self.manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "sources": [
                        {
                            "source_id": self.source.source_id,
                            "sha256": checksum,
                            "retrieved_at_utc": "2026-01-01T00:00:00+00:00",
                            "full_text_review_complete": True,
                        }
                    ],
                    "manual_acquisition": [],
                }
            ),
            encoding="utf-8",
        )
        with patch.object(MODULE, "download") as download_mock:
            self.assertEqual(MODULE.main(), 0)
        download_mock.assert_not_called()
        record = self.load_output()["sources"][0]
        self.assertEqual(record["retrieved_at_utc"], "2026-01-01T00:00:00+00:00")
        self.assertTrue(record["full_text_review_complete"])

    def test_checksum_change_quarantines_redownloads_and_resets_review(self) -> None:
        pdf = self.original / "related-work" / "test.pdf"
        write_pdf(pdf, b"old-local")
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        self.manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "sources": [
                        {
                            "source_id": self.source.source_id,
                            "sha256": "0" * 64,
                            "retrieved_at_utc": "2026-01-01T00:00:00+00:00",
                            "full_text_review_complete": True,
                        }
                    ],
                    "manual_acquisition": [],
                }
            ),
            encoding="utf-8",
        )

        def fake_download(_source: object, destination: Path) -> None:
            write_pdf(destination, b"authoritative")

        with patch.object(MODULE, "download", side_effect=fake_download):
            self.assertEqual(MODULE.main(), 0)
        record = self.load_output()["sources"][0]
        self.assertFalse(record["full_text_review_complete"])
        self.assertNotEqual(record["retrieved_at_utc"], "2026-01-01T00:00:00+00:00")
        self.assertTrue(list(pdf.parent.glob("test.pdf.checksum-mismatch.*.quarantine")))

    def test_manual_source_records_survive_manifest_refresh(self) -> None:
        manual_record = {
            "source_id": "SRC-MANUAL-001",
            "title": "Lawfully acquired paper",
            "local_path": "bibliography/original/related-work/manual.pdf",
            "sha256": "a" * 64,
            "retrieved_at_utc": "2026-02-02T00:00:00+00:00",
            "full_text_review_complete": False,
        }
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        self.manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "sources": [manual_record],
                    "manual_acquisition": [
                        {
                            "source_id": "SRC-MANUAL-001",
                            "title": "Lawfully acquired paper",
                            "official_url": "https://example.invalid/manual",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

        def fake_download(_source: object, destination: Path) -> None:
            write_pdf(destination, b"curated")

        with patch.object(MODULE, "download", side_effect=fake_download):
            self.assertEqual(MODULE.main(), 0)
        output = self.load_output()
        records = {record["source_id"]: record for record in output["sources"]}
        self.assertEqual(records["SRC-MANUAL-001"], manual_record)
        manual_entries = {record["source_id"]: record for record in output["manual_acquisition"]}
        self.assertIn("SRC-MANUAL-001", manual_entries)


if __name__ == "__main__":
    unittest.main()
