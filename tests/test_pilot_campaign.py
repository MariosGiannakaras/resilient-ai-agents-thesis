from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resilient_agents.experiment_runner import HeadlessExperimentRunner
from resilient_agents.pilot_campaign import (
    QConfiguration,
    TuningScore,
    pilot_requests,
    select_tuning_winner,
    stage_one_configurations,
    stage_two_configurations,
    tuning_request,
)
from resilient_agents.pilot_protocol import load_pilot_protocol

PROTOCOL = load_pilot_protocol(ROOT / "configs" / "protocols" / "pilot-v0.1.json")


class PilotCampaignTests(unittest.TestCase):
    def test_predeclared_staged_grid_and_pilot_matrix_are_exact(self) -> None:
        stage_one = stage_one_configurations(PROTOCOL)
        self.assertEqual(len(stage_one), 16)
        self.assertTrue(all(item.discount_factor == 0.9375 for item in stage_one))
        stage_two = stage_two_configurations(PROTOCOL, stage_one[5])
        self.assertEqual(len(stage_two), 2)
        self.assertEqual({item.discount_factor for item in stage_two}, {0.875, 0.96875})
        requests = pilot_requests(
            protocol=PROTOCOL,
            configuration=stage_one[5],
            timeout_seconds=60.0,
        )
        self.assertEqual(len(requests), 14)
        self.assertEqual(len({item.run_id for item in requests}), 14)
        self.assertEqual(
            {(item.layout_id, item.condition_id) for item in requests},
            {
                (layout, condition)
                for layout in PROTOCOL.to_dict()["partitions"]["pilot"]
                for condition in PROTOCOL.to_dict()["evaluation"]["condition_ids"]
            },
        )
        self.assertTrue(all(item.auto_publish for item in requests))
        amended = load_pilot_protocol(
            ROOT / "configs" / "protocols" / "pilot-v0.2.json"
        )
        amended_requests = pilot_requests(
            protocol=amended,
            configuration=stage_one[5],
            timeout_seconds=60.0,
        )
        self.assertTrue(
            all(item.run_id.startswith("PV02-PILOT-") for item in amended_requests)
        )

    def test_tuning_selection_applies_predeclared_lexicographic_criteria(self) -> None:
        first = QConfiguration(0.125, 0.9375, 0.125)
        second = QConfiguration(0.25, 0.9375, 0.125)
        scores = (
            TuningScore(first, ("a", "b"), -13.0, -14.0, 0.03),
            TuningScore(second, ("c", "d"), -13.0, -14.0, 0.02),
        )
        self.assertEqual(select_tuning_winner(scores).configuration, second)
        tied = (
            TuningScore(first, ("a", "b"), -13.0, -14.0, 0.02),
            TuningScore(second, ("c", "d"), -13.0, -14.0, 0.02),
        )
        expected = min((first, second), key=lambda item: item.canonical_json())
        self.assertEqual(select_tuning_winner(tied).configuration, expected)

    def test_tuning_child_timeout_must_follow_protocol_bounds(self) -> None:
        request = tuning_request(
            protocol=PROTOCOL,
            configuration=stage_one_configurations(PROTOCOL)[0],
            configuration_index=0,
            layout_id="tune-l01",
            stage_label="S1",
            timeout_seconds=59.0,
        )
        with self.assertRaises(ValueError):
            HeadlessExperimentRunner(repo_root=ROOT, protocol=PROTOCOL, request=request)


if __name__ == "__main__":
    unittest.main()
