from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.pilot_protocol import (  # noqa: E402
    PilotProtocol,
    load_pilot_protocol,
)

PROTOCOL_PATH = ROOT / "configs" / "protocols" / "pilot-v0.1.json"
AMENDED_PROTOCOL_PATH = ROOT / "configs" / "protocols" / "pilot-v0.2.json"


class PilotProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))

    def test_committed_protocol_is_complete_disjoint_and_canonical(self) -> None:
        protocol = load_pilot_protocol(PROTOCOL_PATH)
        self.assertEqual(protocol.protocol_version, "pilot-v0.1")
        self.assertEqual(len(protocol.layout_ids()), 8)
        self.assertEqual(len(protocol.condition_ids()), 7)
        partition = protocol.partition()
        partition.validate()
        groups = [
            partition.development_scenarios,
            partition.tuning_scenarios,
            partition.pilot_scenarios,
            partition.final_scenarios,
        ]
        self.assertEqual(len(set().union(*(set(group) for group in groups))), 8)
        self.assertEqual(
            PilotProtocol.from_dict(protocol.to_dict()).canonical_json(),
            protocol.canonical_json(),
        )

    def test_v02_overlay_is_bounded_and_expands_to_a_complete_protocol(self) -> None:
        protocol = load_pilot_protocol(AMENDED_PROTOCOL_PATH)
        self.assertEqual(protocol.protocol_version, "pilot-v0.2")
        r0 = next(
            item for item in protocol.to_dict()["agent_regimes"] if item["agent_id"] == "r0"
        )
        self.assertEqual(
            r0["method_configuration"]["active_terminal_observation_policy"],
            "zero-value-seeded-action-tie",
        )
        self.assertEqual(
            protocol.to_dict()["evaluation"]["root_seeds"],
            self.payload["evaluation"]["root_seeds"],
        )

    def test_partition_overlap_and_privileged_information_fail_closed(self) -> None:
        overlap = copy.deepcopy(self.payload)
        overlap["partitions"]["final"][0] = overlap["partitions"]["pilot"][0]
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(overlap)

        privileged = copy.deepcopy(self.payload)
        privileged["information_policy"]["expose_regime_id"] = True
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(privileged)

    def test_layout_drift_and_seed_reuse_fail_closed(self) -> None:
        changed_path = copy.deepcopy(self.payload)
        changed_path["layouts"][0]["grid"]["goal"] = [5, 6]
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(changed_path)

        reused_seed = copy.deepcopy(self.payload)
        reused_seed["evaluation"]["root_seeds"][0] = reused_seed["tuning"][
            "root_seeds"
        ][0]
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(reused_seed)

    def test_condition_and_robust_membership_drift_fail_closed(self) -> None:
        compound = copy.deepcopy(self.payload)
        compound["conditions"][1]["action_failure_probability"] = 0.125
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(compound)

        leaked_prior = copy.deepcopy(self.payload)
        leaked_prior["robust_prior"]["candidate_action_mappings"].append(
            copy.deepcopy(leaked_prior["conditions"][2]["action_mapping"])
        )
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(leaked_prior)

    def test_unknown_or_missing_required_state_fails_closed(self) -> None:
        unknown = copy.deepcopy(self.payload)
        unknown["unexpected"] = "value"
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(unknown)

        missing = copy.deepcopy(self.payload)
        del missing["failure_and_exclusion_policy"]
        with self.assertRaises(ValueError):
            PilotProtocol.from_dict(missing)


if __name__ == "__main__":
    unittest.main()
