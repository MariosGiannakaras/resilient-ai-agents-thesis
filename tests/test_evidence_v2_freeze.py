from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2 import StudyEvidenceValidator
from resilient_agents.evidence_v2.freeze import (
    _validate_freeze_time,
    _write_package_atomic,
)
from resilient_agents.study import StudyStore
from resilient_agents.study.pre_t610 import (
    _record_synthetic_scientific_evidence,
    _synthetic_recipe_and_plan,
)


class EvidenceV2FreezeTests(unittest.TestCase):
    def test_v21_validation_rejects_plan_record_identity_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe, plan = _synthetic_recipe_and_plan()
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=recipe,
                plan=plan,
            )
            _record_synthetic_scientific_evidence(store)
            artifact = next(
                item
                for item in store.artifacts()
                if item.metadata.get("record_type") == "phase-a"
            )
            path = root / artifact.relative_path
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["method_id"] = "wrong-method"
            path.write_text(json.dumps(payload), encoding="utf-8")

            report = StudyEvidenceValidator().validate(store)

            self.assertFalse(report.valid)
            self.assertIn(
                "PHASE_A_SCIENTIFIC_IDENTITY_MISMATCH",
                {finding.code for finding in report.findings},
            )

    def test_freeze_time_requires_utc_and_is_normalized(self) -> None:
        self.assertEqual(
            _validate_freeze_time("2026-09-02T12:34:56+00:00"),
            "2026-09-02T12:34:56Z",
        )
        with self.assertRaisesRegex(ValueError, "must be UTC"):
            _validate_freeze_time("2026-09-02T15:34:56+03:00")
        with self.assertRaisesRegex(ValueError, "must include a UTC offset"):
            _validate_freeze_time("2026-09-02T12:34:56")

    def test_atomic_freeze_refuses_to_overwrite_finalized_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "final-evidence"
            manifest = b'{"status":"frozen"}\n'
            inventory = b'{"run_id":"run-1"}\n'
            digest = _write_package_atomic(
                output_dir,
                manifest_bytes=manifest,
                inventory_bytes=inventory,
            )
            marker = (output_dir / "FINALIZED").read_text(encoding="utf-8")
            self.assertIn(f"manifest_sha256={digest}", marker)
            self.assertEqual(
                (output_dir / "run-manifest-inventory.jsonl").read_bytes(),
                inventory,
            )
            self.assertEqual(
                json.loads(
                    (output_dir / "run-manifest-inventory.jsonl").read_text(
                        encoding="utf-8"
                    )
                )["run_id"],
                "run-1",
            )
            with self.assertRaisesRegex(RuntimeError, "refusing overwrite"):
                _write_package_atomic(
                    output_dir,
                    manifest_bytes=manifest,
                    inventory_bytes=inventory,
                )


if __name__ == "__main__":
    unittest.main()
