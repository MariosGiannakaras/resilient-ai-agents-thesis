import unittest

from resilient_agents.evidence_v2.final_assets import (
    CONDITIONS,
    METHODS,
    _figure_specs,
)


class FinalAssetContractTests(unittest.TestCase):
    def test_inventory_has_explicit_supported_and_unavailable_categories(self) -> None:
        supported = {spec.category for spec in _figure_specs()}
        self.assertEqual(supported, set(range(2, 31)) - {6})
        self.assertNotIn(1, supported)
        self.assertNotIn(6, supported)

    def test_visual_order_is_frozen(self) -> None:
        self.assertEqual(
            METHODS, ["q_learning", "sarsa", "dyna_q_plus", "dqn", "ppo"]
        )
        self.assertEqual(
            CONDITIONS,
            [
                "action-remap-cycle-clockwise",
                "action-remap-swap-right-down",
                "action-failure-0.15",
                "observation-corruption-0.05",
            ],
        )

    def test_asset_ids_are_unique_and_defense_variants_keep_rq_scope(self) -> None:
        specs = _figure_specs()
        self.assertEqual(len({spec.asset_id for spec in specs}), len(specs))
        defense = [spec for spec in specs if spec.category == 30]
        self.assertEqual({spec.rq for spec in defense}, {"RQ1", "RQ2", "RQ3"})
        self.assertTrue(all("defense" in spec.use for spec in defense))
