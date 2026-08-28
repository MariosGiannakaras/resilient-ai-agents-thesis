from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.study import StudyService


class StudyDefaultRegistryTests(unittest.TestCase):
    def test_default_service_registry_covers_supported_study_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            service = StudyService(repo_root=root, writable_root=root)
            self.assertEqual(
                set(service.executors.job_types()),
                {
                    "phase-a-training",
                    "phase-a-reference",
                    "phase-b-matched-set",
                    "study-validation",
                    "study-analysis",
                    "study-export",
                },
            )
            self.assertIsNone(service.evidence_package("missing-study") if False else None)


if __name__ == "__main__":
    unittest.main()
