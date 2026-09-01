from __future__ import annotations

import unittest

from resilient_agents.evidence_v2.records import (
    ANALYSIS_RECORD_SCHEMA_VERSION,
    PHASE_B_TEMPORAL_SCHEMA_VERSION,
    PhaseBAnalysisRecord,
)
from resilient_agents.protocol_v2 import ProtocolV2Branch
from resilient_agents.protocol_v2_temporal import RewardWindow


def _windows() -> tuple[RewardWindow, ...]:
    return tuple(
        RewardWindow(
            start_interaction=index + 1,
            end_interaction=index + 32,
            interaction_count=32,
            mean_reward=-0.1,
        )
        for index in range(0, 256, 32)
    )


def _base(**overrides):
    values = {
        "study_id": "study",
        "job_id": "job",
        "method_id": "q_learning",
        "root_id": "root-1",
        "layout_id": "layout-a",
        "condition_id": "action-remap-swap-right-down",
        "branch": ProtocolV2Branch.ADAPTIVE_NOMINAL,
        "checkpoint_artifact_id": "checkpoint",
        "metrics": {"return_sum": -25.6},
        "resource_metrics": {"environment_interactions": 256.0},
    }
    values.update(overrides)
    return values


class PhaseBTemporalRecordTests(unittest.TestCase):
    def test_historical_schema_v1_round_trip_remains_supported(self) -> None:
        record = PhaseBAnalysisRecord(**_base())
        self.assertEqual(record.schema_version, ANALYSIS_RECORD_SCHEMA_VERSION)
        payload = record.to_dict()
        self.assertNotIn("reward_windows", payload)
        self.assertEqual(PhaseBAnalysisRecord.from_dict(payload), record)

    def test_schema_v2_requires_and_round_trips_complete_windows(self) -> None:
        record = PhaseBAnalysisRecord(
            **_base(),
            schema_version=PHASE_B_TEMPORAL_SCHEMA_VERSION,
            reward_windows=_windows(),
        )
        payload = record.to_dict()
        self.assertEqual(len(payload["reward_windows"]), 8)
        restored = PhaseBAnalysisRecord.from_dict(payload)
        self.assertEqual(restored, record)
        self.assertEqual(restored.reward_windows[-1].end_interaction, 256)

    def test_schema_v1_cannot_masquerade_as_temporal(self) -> None:
        with self.assertRaisesRegex(ValueError, "v1"):
            PhaseBAnalysisRecord(**_base(), reward_windows=_windows())

    def test_schema_v2_fails_when_windows_do_not_cover_resource_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "cover all"):
            PhaseBAnalysisRecord(
                **_base(),
                schema_version=PHASE_B_TEMPORAL_SCHEMA_VERSION,
                reward_windows=_windows()[:-1],
            )

    def test_schema_v2_fails_on_nonfixed_window_width(self) -> None:
        windows = list(_windows())
        windows[-1] = RewardWindow(225, 255, 31, -0.1)
        with self.assertRaisesRegex(ValueError, "fixed width"):
            PhaseBAnalysisRecord(
                **_base(resource_metrics={"environment_interactions": 255.0}),
                schema_version=PHASE_B_TEMPORAL_SCHEMA_VERSION,
                reward_windows=tuple(windows),
            )


if __name__ == "__main__":
    unittest.main()
