from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLICATION = ROOT / "thesis" / "source-material" / "ThesisApplication.pdf"
EXPECTED_SHA256 = "6f2026c7582e4ac396261b7686e799317515542c59c0ac505da11bf7611de4b5"
EXPECTED_SIZE_BYTES = 395338


class SourceMaterialIntegrityTests(unittest.TestCase):
    def test_official_application_repository_copy_is_unchanged(self) -> None:
        payload = APPLICATION.read_bytes()

        self.assertTrue(payload.startswith(b"%PDF-"))
        self.assertEqual(len(payload), EXPECTED_SIZE_BYTES)
        self.assertEqual(hashlib.sha256(payload).hexdigest(), EXPECTED_SHA256)


if __name__ == "__main__":
    unittest.main()
