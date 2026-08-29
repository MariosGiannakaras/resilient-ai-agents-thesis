from __future__ import annotations

import unittest
import json
from pathlib import Path

from resilient_agents.protocol_v2_feasibility import load_plan
from resilient_agents.protocol_v2_t526_recovery import verify_original_bundle, verify_source_compatibility
from resilient_agents.protocol_v2_t526_recovery_v02 import (
    NATIVE_METHOD_IDS,
    SB3_METHOD_IDS,
    _identity_evidence,
    load_amendment,
    validate_phase_b_attempt_evidence,
    validate_recovery_attempt_evidence,
    verify_prior_failed_recovery,
)

try:
    import stable_baselines3  # noqa: F401

    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False


REPO_ROOT = Path(__file__).resolve().parents[1]
AMENDMENT_PATH = (
    REPO_ROOT
    / "configs"
    / "protocols"
    / "protocol-v2-t526-recovery-phase-b-v0.2.json"
)


class T526RecoveryV02ContractTests(unittest.TestCase):
    def test_dec053_preserves_both_historical_evidence_trees_and_phase_a_sources(self):
        amendment = load_amendment(AMENDMENT_PATH)
        self.assertEqual(amendment["amendment_id"], "DEC-053")
        self.assertEqual(
            verify_original_bundle(repo_root=REPO_ROOT, amendment=amendment),
            amendment["original_phase_a"]["evidence_file_sha256"],
        )
        self.assertEqual(
            verify_prior_failed_recovery(repo_root=REPO_ROOT, amendment=amendment),
            amendment["prior_failed_recovery"]["evidence_file_sha256"],
        )
        self.assertGreater(
            len(verify_source_compatibility(repo_root=REPO_ROOT, amendment=amendment)),
            10,
        )

    def test_identity_policy_is_method_specific_and_keeps_phase_b_unchanged(self):
        amendment = load_amendment(AMENDMENT_PATH)
        policy = amendment["identity_policy"]
        self.assertEqual(tuple(policy["native_methods"]), NATIVE_METHOD_IDS)
        self.assertEqual(tuple(policy["sb3_methods"]), SB3_METHOD_IDS)
        self.assertTrue(policy["native_require_raw_checkpoint_envelope_sha256"])
        self.assertFalse(policy["sb3_require_raw_checkpoint_envelope_sha256"])
        self.assertTrue(policy["sb3_require_historical_learner_state_sha256"])
        self.assertEqual(amendment["phase_b"]["expected_matched_sets"], 240)
        self.assertEqual(amendment["phase_b"]["expected_branch_executions"], 960)
        self.assertEqual(
            amendment["phase_b"]["expected_post_boundary_interactions"], 9600
        )
        self.assertEqual(len(amendment["phase_b"]["conditions"]), 8)

    def test_physical_v02_attempt_validates_when_present(self):
        amendment = load_amendment(AMENDMENT_PATH)
        attempt = REPO_ROOT / amendment["recovery"]["output_directory"]
        if not attempt.exists():
            self.skipTest("DEC-053 physical recovery evidence is not present yet")
        result = validate_recovery_attempt_evidence(
            repo_root=REPO_ROOT, amendment=amendment
        )
        self.assertIn(result["status"], {"valid-complete", "valid-failed-barrier"})
        phase_b = REPO_ROOT / amendment["phase_b"]["output_directory"]
        if phase_b.exists():
            phase_b_result = validate_phase_b_attempt_evidence(
                repo_root=REPO_ROOT, amendment=amendment
            )
            self.assertIn(phase_b_result["status"], {"valid", "valid-failed"})

    @unittest.skipUnless(
        _SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed"
    )
    def test_retained_dec052_dqn_passes_the_new_restore_and_derived_barrier(self):
        amendment = load_amendment(AMENDMENT_PATH)
        plan = load_plan(
            REPO_ROOT / amendment["original_phase_a"]["plan_path"]
        )
        layout = next(
            level for level in plan["ordered_gridworld_ladder"]
            if level["level_id"] == "gw-l1"
        )["layouts"][0]
        root = plan["roots"][0]
        checkpoint = json.loads(
            (
                REPO_ROOT
                / amendment["prior_failed_recovery"]["evidence_directory"]
                / "checkpoints"
                / "dqn"
                / "t526-r01"
                / "gw-l1-a.json"
            ).read_text(encoding="utf-8")
        )
        authoritative = next(
            json.loads(line)
            for line in (
                REPO_ROOT
                / amendment["original_phase_a"]["evidence_directory"]
                / "phase-a-runs.jsonl"
            ).read_text(encoding="utf-8").splitlines()
            if '"method_id":"dqn"' in line
            and '"root_id":"t526-r01"' in line
            and '"layout_id":"gw-l1-a"' in line
        )
        evidence = _identity_evidence(
            plan=plan,
            layout=layout,
            root_data=root,
            method_id="dqn",
            checkpoint_value=checkpoint,
            authoritative=authoritative,
        )
        self.assertTrue(evidence["adapter_restore_passed"])
        self.assertTrue(evidence["round_trip_historical_identity_passed"])
        self.assertTrue(evidence["derived_round_trip_passed"])
        self.assertEqual(
            evidence["post_restore_learner_state_sha256"],
            authoritative["learner_state_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
