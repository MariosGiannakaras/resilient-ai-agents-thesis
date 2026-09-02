from resilient_agents.evidence_v2.final_assets import (
    CONDITIONS,
    METHODS,
    _figure_specs,
)


def test_t613_inventory_has_explicit_supported_and_unavailable_categories() -> None:
    supported = {spec.category for spec in _figure_specs()}
    assert supported == set(range(2, 31)) - {6}
    assert 1 not in supported
    assert 6 not in supported


def test_t613_visual_order_is_frozen() -> None:
    assert METHODS == ["q_learning", "sarsa", "dyna_q_plus", "dqn", "ppo"]
    assert CONDITIONS == [
        "action-remap-cycle-clockwise",
        "action-remap-swap-right-down",
        "action-failure-0.15",
        "observation-corruption-0.05",
    ]


def test_t613_asset_ids_are_unique_and_defense_variants_are_data_identical_scope() -> None:
    specs = _figure_specs()
    assert len({spec.asset_id for spec in specs}) == len(specs)
    defense = [spec for spec in specs if spec.category == 30]
    assert {spec.rq for spec in defense} == {"RQ1", "RQ2", "RQ3"}
    assert all("defense" in spec.use for spec in defense)
