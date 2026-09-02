from __future__ import annotations

import unittest
from pathlib import Path

from resilient_agents.study.pre_t610 import (
    run_protocol_v21_preflight,
    run_synthetic_protocol_v21_pipeline_smoke,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class ProtocolV21PreT610ReadinessTests(unittest.TestCase):
    def test_recovery_preflight_preserves_failed_attempt_and_gate(self) -> None:
        report = run_protocol_v21_preflight(REPO_ROOT)
        self.assertTrue(report["ready_for_recovery_execution_authorization"])
        self.assertFalse(report["final_execution_authorized"])
        self.assertFalse(report["final_reserve_access"])
        self.assertTrue(report["backend_default_execution_blocked"])
        self.assertFalse(report["replacement_bundle_present"])
        self.assertEqual(
            report["replacement_execution_instance_id"],
            "protocol-v2.1-final--t610-recovery-01",
        )
        self.assertEqual(report["recovery_decision_id"], "DEC-062")
        self.assertEqual(report["preserved_failed_attempt"]["run_bundle_count"], 216)
        self.assertFalse(
            report["preserved_failed_attempt"]["eligible_for_replacement_evidence"]
        )
        self.assertFalse(
            report["preserved_failed_attempt"]["eligible_for_t611_or_later"]
        )
        self.assertEqual(report["plan_preview"]["total_jobs"], 603)

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
