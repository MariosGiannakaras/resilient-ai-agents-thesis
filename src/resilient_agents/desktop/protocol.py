"""Read-only presentation projection of the frozen protocol-v2.0 authority."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


_METHOD_PRESENTATION: dict[str, tuple[str, str]] = {
    "q_learning": (
        "Q-Learning",
        "Off-policy tabular control that learns action values from experienced transitions.",
    ),
    "sarsa": (
        "SARSA",
        "On-policy tabular control that updates values using the action actually selected next.",
    ),
    "dqn": (
        "DQN",
        "Neural Q-learning with experience replay and a target network.",
    ),
    "ppo": (
        "PPO",
        "Policy-gradient learning with clipped policy updates for stable optimization.",
    ),
    "dyna_q_plus": (
        "Dyna-Q+",
        "Tabular learning combined with model-based planning and a change-aware exploration bonus.",
    ),
}


@dataclass(frozen=True)
class MethodSummary:
    method_id: str
    name: str
    config_id: str
    description: str


@dataclass(frozen=True)
class FrozenProtocolSummary:
    study_id: str
    decision_id: str
    scientific_status: str
    final_reserve_access: bool
    execution_authorization: str
    methods: tuple[MethodSummary, ...]
    root_count: int
    layout_count: int
    condition_count: int
    phase_a_units: int
    phase_a_training_interactions: int
    phase_b_matched_sets: int
    phase_b_branches: int
    phase_b_prefix_interactions: int
    phase_b_post_boundary_interactions: int
    phase_b_horizon: int
    probe_indices: tuple[int, ...]
    probe_episodes: int

    @property
    def final_execution_locked(self) -> bool:
        return not self.final_reserve_access


def _mapping(value: Any, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def load_frozen_protocol(repo_root: Path) -> FrozenProtocolSummary:
    """Load only display/guard metadata from the accepted machine-readable freeze.

    This projection deliberately does not materialize a StudyRecipe or execute a
    planner.  It is a read-only application view over DEC-058 authority.
    """

    path = Path(repo_root) / "configs" / "protocols" / "protocol-v2.0-final.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"frozen protocol is unreadable: {path}") from exc
    if not isinstance(payload, Mapping):
        raise RuntimeError("frozen protocol root must be an object")

    if payload.get("decision_id") != "DEC-058":
        raise RuntimeError("desktop application requires the accepted DEC-058 protocol")
    if payload.get("study_id") != "protocol-v2.0-final":
        raise RuntimeError("unexpected frozen protocol study_id")

    reserve_access = payload.get("final_reserve_access")
    if reserve_access is not False:
        # T-528 is not a final-execution authority.  Fail closed even if the
        # visual layer were accidentally pointed at an amended config.
        raise RuntimeError(
            "T-528 desktop application refuses a protocol with final_reserve_access enabled"
        )
    authorization = payload.get("execution_authorization")
    if authorization != "requires-explicit-t610-gate":
        raise RuntimeError("unexpected final execution authorization contract")

    retained = payload.get("retained_methods")
    configs = _mapping(payload.get("selected_configs"), field="selected_configs")
    if not isinstance(retained, list) or not retained:
        raise RuntimeError("retained_methods must be a non-empty list")
    methods: list[MethodSummary] = []
    for method_id in retained:
        if not isinstance(method_id, str) or method_id not in _METHOD_PRESENTATION:
            raise RuntimeError(f"unsupported retained method identity: {method_id!r}")
        config = _mapping(configs.get(method_id), field=f"selected_configs.{method_id}")
        config_id = config.get("config_id")
        if not isinstance(config_id, str) or not config_id:
            raise RuntimeError(f"missing config_id for {method_id}")
        name, description = _METHOD_PRESENTATION[method_id]
        methods.append(MethodSummary(method_id, name, config_id, description))

    roots = payload.get("final_roots")
    layouts = payload.get("final_layouts")
    phase_a = _mapping(payload.get("phase_a"), field="phase_a")
    phase_b = _mapping(payload.get("phase_b"), field="phase_b")
    stats = _mapping(payload.get("statistical_contract"), field="statistical_contract")
    conditions = phase_b.get("conditions")
    if not isinstance(roots, list) or not isinstance(layouts, list):
        raise RuntimeError("final roots/layouts must be lists")
    if not isinstance(conditions, list):
        raise RuntimeError("phase_b.conditions must be a list")

    probe_indices = phase_a.get("probe_interaction_indices")
    if not isinstance(probe_indices, list) or not all(
        isinstance(value, int) and not isinstance(value, bool) for value in probe_indices
    ):
        raise RuntimeError("phase_a probe indices are invalid")

    def required_int(container: Mapping[str, Any], key: str) -> int:
        value = container.get(key)
        if not isinstance(value, int) or isinstance(value, bool):
            raise RuntimeError(f"{key} must be an integer")
        return value

    summary = FrozenProtocolSummary(
        study_id=str(payload["study_id"]),
        decision_id=str(payload["decision_id"]),
        scientific_status=str(payload.get("scientific_status", "")),
        final_reserve_access=False,
        execution_authorization=str(authorization),
        methods=tuple(methods),
        root_count=len(roots),
        layout_count=len(layouts),
        condition_count=len(conditions),
        phase_a_units=required_int(stats, "expected_phase_a_units"),
        phase_a_training_interactions=required_int(
            stats, "expected_phase_a_training_interactions"
        ),
        phase_b_matched_sets=required_int(stats, "expected_phase_b_matched_sets"),
        phase_b_branches=required_int(stats, "expected_phase_b_branches"),
        phase_b_prefix_interactions=required_int(
            stats, "expected_phase_b_prefix_interactions"
        ),
        phase_b_post_boundary_interactions=required_int(
            stats, "expected_phase_b_post_boundary_interactions"
        ),
        phase_b_horizon=required_int(phase_b, "horizon"),
        probe_indices=tuple(probe_indices),
        probe_episodes=required_int(phase_a, "episodes_per_probe"),
    )

    # Presentation consistency checks protect against showing a convincing but
    # internally contradictory frozen-plan summary.
    if summary.phase_a_units != len(methods) * len(roots) * len(layouts):
        raise RuntimeError("Phase-A denominator disagrees with frozen protocol dimensions")
    expected_sets = len(methods) * len(roots) * len(layouts) * len(conditions)
    if summary.phase_b_matched_sets != expected_sets:
        raise RuntimeError("Phase-B matched-set denominator disagrees with dimensions")
    if summary.phase_b_branches != expected_sets * 4:
        raise RuntimeError("Phase-B branch denominator disagrees with FN/FD/AN/AD design")
    return summary
