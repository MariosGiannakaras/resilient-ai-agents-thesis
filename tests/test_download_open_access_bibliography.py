from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "download_open_access_bibliography.py"
SPEC = importlib.util.spec_from_file_location("bibliography_downloader", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class RetiredBibliographyDownloaderTests(unittest.TestCase):
    def test_module_entrypoint_is_explicitly_blocked(self) -> None:
        with patch("builtins.print") as print_mock:
            self.assertEqual(MODULE.main(), 2)

        rendered = "\n".join(
            " ".join(str(argument) for argument in call.args)
            for call in print_mock.call_args_list
        )
        self.assertIn("This command is retired", rendered)
        self.assertIn("MariosGiannakaras/ThesisBibliography", rendered)
        self.assertIn("research/bibliography", rendered)

    def test_cli_exits_nonzero_without_creating_local_bibliography_state(self) -> None:
        before = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
        }

        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        after = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(result.returncode, 2)
        self.assertIn("This command is retired", result.stderr)
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
