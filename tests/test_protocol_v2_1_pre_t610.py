from __future__ import annotations

import unittest
from pathlib import Path

from resilient_agents.study.pre_t610 import (
    run_synthetic_protocol_v21_pipeline_smoke,
    validate_protocol_v21_t610_completion,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class ProtocolV21PreT610ReadinessTests(unittest.TestCase):
    def test_completed_replacement_preserves_failed_attempt_and_lineage(self) -> None:
        report = validate_protocol_v21_t610_completion(REPO_ROOT)
        self.assertTrue(report["finalized"])
        self.assertEqual(report["progress"]["completed"], 603)
        self.assertEqual(report["run_bundle_count"], 600)
        self.assertEqual(report["source_git_commit"], "86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730")
        self.assertEqual(report["failed_attempt"]["run_bundle_count"], 216)
        self.assertFalse(
            report["failed_attempt"]["eligible_for_replacement_evidence"]
        )
        self.assertFalse(
            report["failed_attempt"]["eligible_for_t611_or_later"]
        )
        self.assertFalse(report["outcomes_interpreted"])

    def test_synthetic_pipeline_reaches_validated_v21_evidence_handoff(self) -> None:
        report = run_synthetic_protocol_v21_pipeline_smoke(REPO_ROOT)
        self.assertEqual(report["evidence_class"], "development")
        self.assertFalse(report["final_identities_used"])
        self.assertEqual(report["analysis_recipe"], "protocol-v2-root-level-v2.1")
        self.assertEqual(report["evidence_package"], "protocol-v2-evidence-handoff-v2")
        self.assertEqual(
            report["recovery_statuses_exercised"],
            ["recovered", "right-censored"],
        )
        self.assertTrue(report["finalized"])


if __name__ == "__main__":
    unittest.main()
