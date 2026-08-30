from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.study_read_model import DesktopStudyReadModel


REPO_ROOT = Path(__file__).resolve().parents[1]


class DesktopStudyReadModelTests(unittest.TestCase):
    def test_empty_writable_root_has_no_synthetic_studies(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            read_model = DesktopStudyReadModel(repo_root=REPO_ROOT, writable_root=Path(temp))
            self.assertEqual(read_model.studies(), ())

    def test_read_model_uses_empty_executor_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            read_model = DesktopStudyReadModel(repo_root=REPO_ROOT, writable_root=Path(temp))
            self.assertEqual(read_model._service.executors.job_types(), ())


if __name__ == "__main__":
    unittest.main()
