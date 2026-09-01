"""Read-only presentation projection of the current protocol-v2.1 authority.

The desktop application deliberately projects only information needed to explain
and guard the experiment.  It never materializes final roots, layout identities,
seed streams, checkpoints, or execution authorization into a UI recipe.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


_METHOD_PRESENTATION: dict[str, tuple[str, str]] = {
    "q_learning": (
        "Q-Learning",
        "Tabular off-policy control that learns action values from experienced transitions.",
    ),
    "sarsa": (
        "SARSA",
        "Tabular on-policy control that learns from the action actually selected next.",
    ),
    "dqn": (
        "DQN",
        "Neural Q-learning with experience replay and a target network.",
    ),
    "ppo": (
        "PPO",
        "Policy-gradient learning with clipped updates for stable optimization.",
    ),
    "dyna_q_plus": (
        "Dyna-Q+",
        "Tabular learning with model-based planning and a change-aware exploration bonus.",
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
    protocol_id: str
    study_id: str
    decision_id: str
    amended_decision_id: str
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
    recovery_window_size: int
    recovery_observation_horizon: int
    recovery_primary_condition_family: str
    recovery_primary_tolerance: float
    recovery_stability_windows: int

    @property
    def final_execution_locked(self) -> bool:
        return not self.final_reserve_access


class ProtocolProjectionError(RuntimeError):
    """The current protocol cannot be represented safely by the UI."""


def _mapping(value: Any, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ProtocolProjectionError(f"{field} must be an object")
    return value


def _required_int(container: Mapping[str, Any], key: str) -> int:
    value = container.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ProtocolProjectionError(f"{key} must be an integer")
    return value


def load_frozen_protocol(repo_root: Path) -> FrozenProtocolSummary:
    """Load a fail-closed, read-only presentation summary of protocol-v2.1."""

    path = Path(repo_root) / "configs" / "protocols" / "protocol-v2.1-final.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProtocolProjectionError(f"current protocol is unreadable: {path}") from exc
    if not isinstance(payload, Mapping):
        raise ProtocolProjectionError("current protocol root must be an object")

    if payload.get("decision_id") != "DEC-060":
        raise ProtocolProjectionError("desktop application requires DEC-060 protocol authority")
    if payload.get("amends_decision_id") != "DEC-058":
        raise ProtocolProjectionError("protocol-v2.1 amendment lineage is invalid")
    if payload.get("protocol_id") != "protocol-v2.1":
        raise ProtocolProjectionError("unexpected current protocol_id")
    if payload.get("study_id") != "protocol-v2.1-final":
        raise ProtocolProjectionError("unexpected current protocol study_id")

    reserve_access = payload.get("final_reserve_access")
    if reserve_access is not False:
        raise ProtocolProjectionError(
            "T-534 desktop application refuses a protocol with final_reserve_access enabled"
        )
    authorization = payload.get("execution_authorization")
    if authorization != "requires-explicit-t610-gate":
        raise ProtocolProjectionError("unexpected final execution authorization contract")

    retained = payload.get("retained_methods")
    configs = _mapping(payload.get("selected_configs"), field="selected_configs")
    if not isinstance(retained, list) or not retained:
        raise ProtocolProjectionError("retained_methods must be a non-empty list")
    if tuple(retained) != tuple(_METHOD_PRESENTATION):
        raise ProtocolProjectionError("protocol-v2.1 retained-method identity/order is unexpected")

    methods: list[MethodSummary] = []
    for method_id in retained:
        if not isinstance(method_id, str) or method_id not in _METHOD_PRESENTATION:
            raise ProtocolProjectionError(f"unsupported retained method identity: {method_id!r}")
        config = _mapping(configs.get(method_id), field=f"selected_configs.{method_id}")
        config_id = config.get("config_id")
        if not isinstance(config_id, str) or not config_id:
            raise ProtocolProjectionError(f"missing config_id for {method_id}")
        name, description = _METHOD_PRESENTATION[method_id]
        methods.append(MethodSummary(method_id, name, config_id, description))

    # These arrays are consulted only for cardinality checks. Their identities and
    # values are intentionally not projected into the presentation model.
    roots = payload.get("final_roots")
    layouts = payload.get("final_layouts")
    phase_a = _mapping(payload.get("phase_a"), field="phase_a")
    phase_b = _mapping(payload.get("phase_b"), field="phase_b")
    stats = _mapping(payload.get("statistical_contract"), field="statistical_contract")
    recovery = _mapping(payload.get("recovery_contract"), field="recovery_contract")
    conditions = phase_b.get("conditions")
    if not isinstance(roots, list) or not isinstance(layouts, list):
        raise ProtocolProjectionError("final protocol dimensions must be lists")
    if not isinstance(conditions, list):
        raise ProtocolProjectionError("phase_b.conditions must be a list")

    probe_indices = phase_a.get("probe_interaction_indices")
    if not isinstance(probe_indices, list) or not all(
        isinstance(value, int) and not isinstance(value, bool) for value in probe_indices
    ):
        raise ProtocolProjectionError("phase_a probe indices are invalid")

    tolerance = recovery.get("primary_tolerance")
    if not isinstance(tolerance, (int, float)) or isinstance(tolerance, bool):
        raise ProtocolProjectionError("recovery primary_tolerance must be numeric")
    family = recovery.get("primary_condition_family")
    if not isinstance(family, str) or not family:
        raise ProtocolProjectionError("recovery primary_condition_family is invalid")

    summary = FrozenProtocolSummary(
        protocol_id=str(payload["protocol_id"]),
        study_id=str(payload["study_id"]),
        decision_id=str(payload["decision_id"]),
        amended_decision_id=str(payload["amends_decision_id"]),
        scientific_status=str(payload.get("scientific_status", "")),
        final_reserve_access=False,
        execution_authorization=str(authorization),
        methods=tuple(methods),
        root_count=len(roots),
        layout_count=len(layouts),
        condition_count=len(conditions),
        phase_a_units=_required_int(stats, "expected_phase_a_units"),
        phase_a_training_interactions=_required_int(stats, "expected_phase_a_training_interactions"),
        phase_b_matched_sets=_required_int(stats, "expected_matched_sets"),
        phase_b_branches=_required_int(stats, "expected_phase_b_branches"),
        phase_b_prefix_interactions=_required_int(stats, "expected_phase_b_prefix_interactions"),
        phase_b_post_boundary_interactions=_required_int(stats, "expected_phase_b_post_boundary_interactions"),
        phase_b_horizon=_required_int(phase_b, "horizon"),
        probe_indices=tuple(probe_indices),
        probe_episodes=_required_int(phase_a, "episodes_per_probe"),
        recovery_window_size=_required_int(recovery, "window_size"),
        recovery_observation_horizon=_required_int(recovery, "observation_horizon"),
        recovery_primary_condition_family=family,
        recovery_primary_tolerance=float(tolerance),
        recovery_stability_windows=_required_int(recovery, "stability_windows"),
    )

    if summary.phase_a_units != len(methods) * len(roots) * len(layouts):
        raise ProtocolProjectionError("Phase-A denominator disagrees with protocol dimensions")
    expected_sets = len(methods) * len(roots) * len(layouts) * len(conditions)
    if summary.phase_b_matched_sets != expected_sets:
        raise ProtocolProjectionError("Phase-B matched-set denominator disagrees with dimensions")
    if summary.phase_b_branches != expected_sets * 4:
        raise ProtocolProjectionError("Phase-B branch denominator disagrees with FN/FD/AN/AD design")
    if summary.recovery_observation_horizon != summary.phase_b_horizon:
        raise ProtocolProjectionError("RQ3 recovery horizon disagrees with Phase-B horizon")
    return summary
