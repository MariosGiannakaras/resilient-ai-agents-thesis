from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2.final_analysis import (
    T612_PACKAGE_SCHEMA_VERSION,
    _sensitivity_diagnostics,
    _write_package_atomic,
)


class EvidenceV2FinalAnalysisTests(unittest.TestCase):
    def test_sensitivity_diagnostics_combines_primary_and_declared_thresholds(
        self,
    ) -> None:
        roots = [
            {
                "method_id": "method",
                "condition_id": "action-remap-a",
                "primary_recovery_axis": True,
                "status": status,
            }
            for status in ("recovered", "right-censored") * 6
        ]
        sensitivity = [
            {
                **row,
                "tolerance": tolerance,
                "status": "recovered" if tolerance == 0.2 else "right-censored",
            }
            for tolerance in (0.05, 0.2)
            for row in roots
        ]
        package = {
            "phase_b": {
                "recovery": {
                    "root_records": roots,
                    "sensitivity_root_records": sensitivity,
                }
            }
        }

        with self.assertRaisesRegex(RuntimeError, "coverage is incomplete"):
            _sensitivity_diagnostics(package)

    def test_atomic_package_refuses_overwrite_and_marker_pins_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "analysis"
            digest = _write_package_atomic(
                output,
                manifest={"status": "finalized"},
                diagnostics={"valid": True},
            )
            self.assertEqual(
                (output / "FINALIZED").read_text(encoding="utf-8"),
                f"schema_version={T612_PACKAGE_SCHEMA_VERSION}\n"
                "status=finalized\n"
                f"manifest_sha256={digest}\n",
            )
            self.assertTrue(
                json.loads((output / "diagnostics.json").read_text())["valid"]
            )
            with self.assertRaisesRegex(RuntimeError, "refusing overwrite"):
                _write_package_atomic(
                    output,
                    manifest={"status": "finalized"},
                    diagnostics={"valid": True},
                )


if __name__ == "__main__":
    unittest.main()
