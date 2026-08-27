from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from resilient_agents.contracts import ProtocolStage  # noqa: E402
from resilient_agents.v11_protocol import (  # noqa: E402
    V11_CONDITION_IDS,
    V11_FINAL_LAYOUT_IDS,
    V11_STRATEGY_IDS,
    V11CandidateProtocol,
    load_v11_candidate_protocol,
)


ROOT = Path(__file__).resolve().parents[1]
V11_PATH = ROOT / "configs" / "protocols" / "protocol-v1.1.json"
V10_PATH = ROOT / "configs" / "protocols" / "protocol-v1.0.json"


class V11ProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.protocol = load_v11_candidate_protocol(V11_PATH)

    def test_checked_in_candidate_is_fail_closed_and_complete(self) -> None:
        payload = self.protocol.to_dict()
        self.assertEqual(self.protocol.status, "candidate")
        self.assertFalse(payload["scientific_scope"]["final_evidence_use"])
        self.assertEqual(self.protocol.strategy_ids(), V11_STRATEGY_IDS)
        self.assertEqual(tuple(payload["evaluation"]["condition_ids"]), V11_CONDITION_IDS)
        self.assertEqual(tuple(payload["evaluation"]["final_layout_ids"]), V11_FINAL_LAYOUT_IDS)
        self.assertEqual(len(payload["evaluation"]["root_seeds"]), 32)
        self.assertTrue(all(value is False for value in payload["information_policy"].values()))

    def test_candidate_execution_blocks_pilot_and_final(self) -> None:
        self.protocol.assert_execution_allowed(ProtocolStage.DEVELOPMENT)
        self.protocol.assert_execution_allowed(ProtocolStage.TUNING)
        with self.assertRaises(ValueError):
            self.protocol.assert_execution_allowed(ProtocolStage.PILOT)
        with self.assertRaises(ValueError):
            self.protocol.assert_execution_allowed(ProtocolStage.FINAL)

    def test_configuration_identity_is_stable_and_agent_specific(self) -> None:
        first = self.protocol.configuration_sha256("dq0-p05-v1")
        second = self.protocol.configuration_sha256("dq0-p05-v1")
        other = self.protocol.configuration_sha256("dq0-p10-v1")
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)
        self.assertNotEqual(first, other)
        self.assertEqual(
            self.protocol.configuration("d0-p10-k0010-v1")["agent_id"], "d0"
        )
        with self.assertRaises(ValueError):
            self.protocol.configuration("unknown-config")

    def test_candidate_final_reserve_is_fresh_against_protocol_v1_0(self) -> None:
        v10 = json.loads(V10_PATH.read_text(encoding="utf-8"))
        v11 = self.protocol.to_dict()
        old_final_ids = set(v10["partitions"]["final"])
        old_signatures = {
            json.dumps(row["grid"], sort_keys=True, separators=(",", ":"))
            for row in v10["layouts"]
            if row["layout_id"] in old_final_ids
        }
        new_signatures = {
            json.dumps(row["grid"], sort_keys=True, separators=(",", ":"))
            for row in v11["layouts"]
            if row["layout_id"] in set(V11_FINAL_LAYOUT_IDS)
        }
        self.assertTrue(old_signatures.isdisjoint(new_signatures))

        old_seeds = set(v10["evaluation"]["root_seeds"]) | set(v10["tuning"]["root_seeds"])
        new_seeds = set(v11["evaluation"]["root_seeds"]) | set(v11["tuning"]["root_seeds"])
        self.assertTrue(old_seeds.isdisjoint(new_seeds))

    def test_seed_partitions_are_disjoint(self) -> None:
        payload = self.protocol.to_dict()
        development = set(payload["development"]["root_seeds"])
        tuning = set(payload["tuning"]["root_seeds"])
        final = set(payload["evaluation"]["root_seeds"])
        self.assertTrue(development.isdisjoint(tuning))
        self.assertTrue(development.isdisjoint(final))
        self.assertTrue(tuning.isdisjoint(final))

    def test_candidate_rejects_final_evidence_authorization(self) -> None:
        payload = copy.deepcopy(self.protocol.to_dict())
        payload["scientific_scope"]["final_evidence_use"] = True
        with self.assertRaises(ValueError):
            V11CandidateProtocol.from_dict(payload)

    def test_candidate_rejects_information_leak_and_unbounded_tuning(self) -> None:
        leaked = copy.deepcopy(self.protocol.to_dict())
        leaked["information_policy"]["expose_change_indicator"] = True
        with self.assertRaises(ValueError):
            V11CandidateProtocol.from_dict(leaked)

        expanded = copy.deepcopy(self.protocol.to_dict())
        expanded["tuning"]["candidate_configuration_ids"]["s0"].append("s0-a050-v1")
        with self.assertRaises(ValueError):
            V11CandidateProtocol.from_dict(expanded)


if __name__ == "__main__":
    unittest.main()
