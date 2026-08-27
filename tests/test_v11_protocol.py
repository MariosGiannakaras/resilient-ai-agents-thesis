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
        self.assertIn("not the thesis subject", payload["scientific_scope"]["testbed_role"])

    def test_candidate_execution_blocks_pilot_and_final(self) -> None:
        self.protocol.assert_execution_allowed(ProtocolStage.DEVELOPMENT)
        self.protocol.assert_execution_allowed(ProtocolStage.TUNING)
        with self.assertRaises(ValueError):
            self.protocol.assert_execution_allowed(ProtocolStage.PILOT)
        with self.assertRaises(ValueError):
            self.protocol.assert_execution_allowed(ProtocolStage.FINAL)

    def test_configuration_identity_and_bounded_surface_are_stable(self) -> None:
        self.assertEqual(self.protocol.candidate_configuration_ids("f0"), ("f0-base-v1",))
        self.assertEqual(self.protocol.candidate_configuration_ids("c0"), ("c0-base-v1",))
        self.assertEqual(
            self.protocol.candidate_configuration_ids("s0"),
            ("s0-a025-v1", "s0-a050-v1"),
        )
        self.assertEqual(
            self.protocol.candidate_configuration_ids("dq0"),
            ("dq0-p05-v1", "dq0-p10-v1"),
        )
        self.assertEqual(
            self.protocol.candidate_configuration_ids("d0"),
            (
                "d0-p05-k0005-v1",
                "d0-p05-k0010-v1",
                "d0-p10-k0005-v1",
                "d0-p10-k0010-v1",
            ),
        )

        sarsa_alphas = {
            self.protocol.configuration(config_id)["settings"]["learning_rate"]
            for config_id in self.protocol.candidate_configuration_ids("s0")
        }
        dyna_steps = {
            self.protocol.configuration(config_id)["settings"]["planning_steps"]
            for config_id in self.protocol.candidate_configuration_ids("dq0")
        }
        dyna_plus = {
            (
                self.protocol.configuration(config_id)["settings"]["planning_steps"],
                self.protocol.configuration(config_id)["settings"]["kappa"],
            )
            for config_id in self.protocol.candidate_configuration_ids("d0")
        }
        self.assertEqual(sarsa_alphas, {0.25, 0.5})
        self.assertEqual(dyna_steps, {5, 10})
        self.assertEqual(dyna_plus, {(5, 0.0005), (5, 0.001), (10, 0.0005), (10, 0.001)})

        all_ids = list(self.protocol.to_dict()["configuration_catalog"])
        hashes = [self.protocol.configuration_sha256(config_id) for config_id in all_ids]
        self.assertEqual(hashes, [self.protocol.configuration_sha256(config_id) for config_id in all_ids])
        self.assertEqual(len(hashes), len(set(hashes)))
        self.assertEqual(len(self.protocol.protocol_sha256()), 64)
        with self.assertRaises(ValueError):
            self.protocol.configuration("unknown-config")

    def test_candidate_final_reserve_is_fresh_against_all_historical_v10_layouts(self) -> None:
        v10 = json.loads(V10_PATH.read_text(encoding="utf-8"))
        v11 = self.protocol.to_dict()
        old_signatures = {
            json.dumps(row["grid"], sort_keys=True, separators=(",", ":"))
            for row in v10["layouts"]
        }
        new_final_signatures = {
            json.dumps(row["grid"], sort_keys=True, separators=(",", ":"))
            for row in v11["layouts"]
            if row["layout_id"] in set(V11_FINAL_LAYOUT_IDS)
        }
        self.assertEqual(len(new_final_signatures), 4)
        self.assertTrue(old_signatures.isdisjoint(new_final_signatures))

    def test_v11_seed_banks_are_disjoint_from_historical_and_each_other(self) -> None:
        v10 = json.loads(V10_PATH.read_text(encoding="utf-8"))
        payload = self.protocol.to_dict()
        historical = set(v10["evaluation"]["root_seeds"]) | set(v10["tuning"]["root_seeds"])
        development = set(payload["development"]["root_seeds"])
        tuning = set(payload["tuning"]["root_seeds"])
        final = set(payload["evaluation"]["root_seeds"])
        self.assertTrue(historical.isdisjoint(development))
        self.assertTrue(historical.isdisjoint(tuning))
        self.assertTrue(historical.isdisjoint(final))
        self.assertTrue(development.isdisjoint(tuning))
        self.assertTrue(development.isdisjoint(final))
        self.assertTrue(tuning.isdisjoint(final))
        self.assertEqual(len(final), 32)

    def test_metric_windows_effect_direction_and_robust_gate_are_machine_readable(self) -> None:
        payload = self.protocol.to_dict()
        metrics = payload["metric_policy"]
        self.assertEqual(
            metrics["primary"],
            ["cumulative_deficit", "immediate_degradation", "terminal_performance"],
        )
        self.assertEqual(
            metrics["primary_windows"],
            {
                "immediate_window": 1,
                "worst_window": 2,
                "terminal_window": 4,
                "recovery_tolerance": 0.0,
                "recovery_stability_episodes": 2,
            },
        )
        self.assertEqual(metrics["definitions"]["terminal_performance"]["source_field"], "post_change_mean")
        self.assertEqual(metrics["definitions"]["terminal_performance"]["orientation"], "higher-is-better")
        self.assertTrue(metrics["recovery_is_sensitivity"])
        self.assertFalse(metrics["composite_resilience_score"])

        plan = payload["statistical_analysis_plan"]
        self.assertEqual(plan["confidence_interval"]["level"], 0.95)
        self.assertEqual(plan["confidence_interval"]["resamples"], 10000)
        self.assertIn("positive effect values always favor", plan["effect_direction"])
        self.assertIn("32 root-level paired effects", plan["primary_n"])
        self.assertIn("four held-out layout effects equally", plan["layout_aggregation"])

        gate = payload["robust_planner_gate"]
        self.assertFalse(gate["evidence_partition"]["final_access"])
        self.assertEqual(gate["nominal_viability"]["minimum_overall_goal_rate"], 0.80)
        self.assertEqual(gate["nominal_viability"]["minimum_each_layout_goal_rate"], 0.70)
        self.assertEqual(gate["runtime"]["maximum_complete_gate_wall_seconds"], 600)
        self.assertTrue(gate["information_fairness"]["same_all_hidden_policy"])

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

    def test_structural_duplicate_or_condition_drift_fails_closed(self) -> None:
        duplicated = copy.deepcopy(self.protocol.to_dict())
        final_rows = [
            row for row in duplicated["layouts"] if row["layout_id"] in set(V11_FINAL_LAYOUT_IDS)
        ]
        final_rows[1]["grid"] = copy.deepcopy(final_rows[0]["grid"])
        with self.assertRaises(ValueError):
            V11CandidateProtocol.from_dict(duplicated)

        renamed = copy.deepcopy(self.protocol.to_dict())
        renamed["conditions"][1]["condition_id"] = "old-r0-relative-label"
        with self.assertRaises(ValueError):
            V11CandidateProtocol.from_dict(renamed)


if __name__ == "__main__":
    unittest.main()
