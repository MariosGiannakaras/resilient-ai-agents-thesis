"""Materialize the self-contained DEC-060 authority into one immutable StudyRecipe.

This module performs no execution and does not authorize final-reserve access.
It fails closed unless the committed authority explicitly retains the T-610 gate
and ``final_reserve_access=false``.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .model import EvidenceClass
from .recipe import StudyRecipe

_PROTOCOL_ID = "protocol-v2.1"
_STUDY_ID = "protocol-v2.1-final"
_DECISION_ID = "DEC-060"
_AMENDS_DECISION_ID = "DEC-058"
_EXECUTION_GATE = "requires-explicit-t610-gate"
_METHODS = ("q_learning", "sarsa", "dqn", "ppo", "dyna_q_plus")
_BRANCHES = ("FN", "FD", "AN", "AD")
_ACTIONS = ("up", "right", "down", "left")
_ACTION_VECTORS = {
    "up": [0, -1],
    "right": [1, 0],
    "down": [0, 1],
    "left": [-1, 0],
}


def _mapping(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return dict(value)


def _list(value: Any, *, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    return list(value)


def _authority_guard(authority: Mapping[str, Any]) -> dict[str, Any]:
    payload = dict(authority)
    if payload.get("schema_version") != 1:
        raise ValueError("protocol-v2.1 authority schema_version must be 1")
    if payload.get("decision_id") != _DECISION_ID:
        raise ValueError("protocol-v2.1 authority must be owned by DEC-060")
    if payload.get("amends_decision_id") != _AMENDS_DECISION_ID:
        raise ValueError("protocol-v2.1 authority must explicitly amend DEC-058")
    if payload.get("protocol_id") != _PROTOCOL_ID:
        raise ValueError("protocol-v2.1 authority protocol_id mismatch")
    if payload.get("study_id") != _STUDY_ID:
        raise ValueError("protocol-v2.1 authority study_id mismatch")
    if payload.get("final_reserve_access") is not False:
        raise ValueError("final reserve must remain sealed while T-530 is materialized")
    if payload.get("execution_authorization") != _EXECUTION_GATE:
        raise ValueError("protocol-v2.1 authority must retain the explicit T-610 gate")
    if tuple(_list(payload.get("retained_methods"), field="retained_methods")) != _METHODS:
        raise ValueError("protocol-v2.1 retained method set/order mismatch")
    return payload


def _scenario(layout: Mapping[str, Any], task: Mapping[str, Any]) -> dict[str, Any]:
    layout_id = str(layout["layout_id"])
    reward_spec = _mapping(task.get("reward_spec"), field="task.reward_spec")
    information_policy = _mapping(
        task.get("information_policy"), field="task.information_policy"
    )
    expected_policy = {
        "expose_executed_action": False,
        "expose_disturbance_flags": False,
        "expose_change_indicator": False,
        "expose_regime_id": False,
        "expose_true_state": False,
    }
    if information_policy != expected_policy:
        raise ValueError("protocol-v2.1 agent-visible information contract mismatch")
    if tuple(task.get("action_semantics", ())) != _ACTIONS:
        raise ValueError("protocol-v2.1 action semantics mismatch")
    if task.get("observation_semantics") != "x-y-position-only":
        raise ValueError("protocol-v2.1 observation semantics mismatch")
    return {
        "scenario_id": layout_id,
        "environment_id": task["environment_id"],
        "max_steps": int(layout["max_steps"]),
        "reward_spec": reward_spec,
        "initial_state_spec": {
            "grid": {
                "width": int(layout["width"]),
                "height": int(layout["height"]),
                "start": list(layout["start"]),
                "goal": list(layout["goal"]),
                "obstacles": [list(item) for item in layout["obstacles"]],
            }
        },
        "dynamics_spec": {"action_vectors": dict(_ACTION_VECTORS)},
        "observation_spec": {
            "type": "position",
            "coordinate_order": "x-y",
            "reset_observation": "true-state",
        },
        "action_disturbance_spec": {
            "type": "no-op-failure",
            "failure_probability": 0.0,
        },
        "observation_disturbance_spec": {
            "type": "position-mislocalization",
            "mislocalization_probability": 0.0,
        },
        "change_events": [],
        "information_policy": information_policy,
    }


def materialize_protocol_v21_recipe(authority: Mapping[str, Any]) -> StudyRecipe:
    """Convert committed DEC-060 authority data into the scheduler recipe envelope."""

    payload = _authority_guard(authority)
    task = _mapping(payload.get("task"), field="task")
    phase_a = _mapping(payload.get("phase_a"), field="phase_a")
    phase_b = _mapping(payload.get("phase_b"), field="phase_b")
    recovery = _mapping(payload.get("recovery_contract"), field="recovery_contract")
    statistics = _mapping(payload.get("statistical_contract"), field="statistical_contract")
    interval = _mapping(statistics.get("interval"), field="statistical_contract.interval")
    if phase_a.get("deployment_start_settlement") != "DEC-054":
        raise ValueError(
            "protocol-v2.1 Phase-A deployment start must retain DEC-054 settlement"
        )

    layouts_raw = _list(payload.get("final_layouts"), field="final_layouts")
    roots = _list(payload.get("final_roots"), field="final_roots")
    conditions = _list(phase_b.get("conditions"), field="phase_b.conditions")
    if len(layouts_raw) != 2 or len(roots) != 12 or len(conditions) != 4:
        raise ValueError("protocol-v2.1 final matrix dimensions no longer match DEC-060")
    if int(statistics.get("root_count", -1)) != len(roots):
        raise ValueError("statistical root_count disagrees with final roots")
    if int(statistics.get("layouts_per_root", -1)) != len(layouts_raw):
        raise ValueError("statistical layout count disagrees with final layouts")
    if int(statistics.get("conditions_per_layout", -1)) != len(conditions):
        raise ValueError("statistical condition count disagrees with Phase-B conditions")
    if int(statistics.get("methods", -1)) != len(_METHODS):
        raise ValueError("statistical method count disagrees with retained methods")
    if phase_b.get("horizon") != 256:
        raise ValueError("protocol-v2.1 Phase-B horizon must remain 256")
    if phase_b.get("common_nominal_no_learning_prefix_interactions") != 1:
        raise ValueError("protocol-v2.1 shared no-learning prefix must remain one interaction")
    if recovery.get("window_size") != 32 or recovery.get("observation_horizon") != 256:
        raise ValueError("protocol-v2.1 recovery grid must remain 32 x 8 interactions")
    if recovery.get("primary_condition_family") != "action-remap":
        raise ValueError("protocol-v2.1 primary recovery axis must remain action-remap")
    if interval.get("kind") != "student-t" or float(interval.get("confidence", 0.0)) != 0.95:
        raise ValueError("protocol-v2.1 interval contract must remain two-sided Student-t 95%")

    selected = _mapping(payload.get("selected_configs"), field="selected_configs")
    condition_ids = [str(item["condition_id"]) for item in conditions]
    methods: list[dict[str, Any]] = []
    for method_id in _METHODS:
        config = _mapping(selected.get(method_id), field=f"selected_configs.{method_id}")
        configuration_id = config.pop("config_id", None)
        implementation_id = config.pop("implementation_id", None)
        if not isinstance(configuration_id, str) or not configuration_id:
            raise ValueError(f"{method_id} config_id must be explicit")
        if not isinstance(implementation_id, str) or not implementation_id:
            raise ValueError(f"{method_id} implementation_id must be explicit")
        methods.append(
            {
                "method_id": method_id,
                "configuration_id": configuration_id,
                "implementation_id": implementation_id,
                "role": "core",
                "phase_b_condition_ids": list(condition_ids),
                "parameters": config,
            }
        )

    layouts = [
        {
            "layout_id": str(layout["layout_id"]),
            "family": "final-held-out",
            "generation_seed": int(layout["generation_seed"]),
            "spec_sha256": str(layout["spec_sha256"]),
            "scenario": _scenario(_mapping(layout, field="final layout"), task),
        }
        for layout in layouts_raw
    ]

    critical_table = _mapping(
        interval.get("critical_value_by_independent_root_count"),
        field="statistical_contract.interval.critical_value_by_independent_root_count",
    )
    analysis_spec = {
        "analysis_recipe": "protocol-v2-root-level-v2.1",
        "phase_a_metric": "return_mean",
        "phase_a_direction": "higher-is-better",
        "phase_b_metric": "return_sum",
        "phase_b_direction": "higher-is-better",
        "layout_aggregation": "equal-weight",
        "require_complete_layout_blocks": True,
        "interval": {
            "kind": "student-t",
            "confidence": 0.95,
            "critical_value_by_n": critical_table,
        },
        "recovery": {
            "window_size": int(recovery["window_size"]),
            "observation_horizon": int(recovery["observation_horizon"]),
            "tolerance": float(recovery["primary_tolerance"]),
            "sensitivity_tolerances": list(recovery["sensitivity_tolerances"]),
            "stability_windows": int(recovery["stability_windows"]),
            "primary_condition_family": str(recovery["primary_condition_family"]),
        },
    }

    return StudyRecipe(
        recipe_id=_STUDY_ID,
        protocol_version=_PROTOCOL_ID,
        evidence_class=EvidenceClass.CONFIRMATORY,
        scientific_status=str(payload["scientific_status"]),
        frozen=True,
        study={
            "matrix_schema_version": 2,
            "phase_a": {
                "execution": {
                    "training_interaction_budget": int(
                        phase_a["training_interaction_budget"]
                    ),
                    "probe_interaction_indices": list(
                        phase_a["probe_interaction_indices"]
                    ),
                    "episodes_per_probe": int(phase_a["episodes_per_probe"]),
                    "task": {
                        "gamma": float(task["gamma"]),
                        "reward_contract": dict(task["reward_spec"]),
                        "administrative_truncation": bool(
                            task["administrative_truncation"]
                        ),
                        "bootstrap_on_truncation": bool(
                            task["bootstrap_on_truncation"]
                        ),
                    },
                },
                "methods": methods,
                "references": [],
                "roots": roots,
                "layouts": layouts,
            },
            "phase_b": {
                "execution": {
                    "prefix_interactions": int(
                        phase_b["common_nominal_no_learning_prefix_interactions"]
                    ),
                    "interaction_budget_per_branch": int(phase_b["horizon"]),
                    "episode_reset_policy_id": str(
                        phase_b["episode_reset_policy_id"]
                    ),
                    "subsequent_episode_seed_count": int(
                        phase_b["subsequent_episode_seed_count"]
                    ),
                    "temporal_evidence_id": str(phase_b["temporal_evidence_id"]),
                    "temporal_window_size": int(recovery["window_size"]),
                },
                "conditions": conditions,
                "branches": list(_BRANCHES),
            },
            "postprocessing": {
                "validation": {"validator": "protocol-v2.1-study-temporal"},
                "analysis": analysis_spec,
                "exports": {
                    "package": "protocol-v2-evidence-handoff-v2",
                    "emit_csv": True,
                },
            },
        },
    )


def load_protocol_v21_final_recipe(repo_root: Path) -> StudyRecipe:
    """Load the committed authority and return its deterministic immutable recipe."""

    path = Path(repo_root) / "configs" / "protocols" / "protocol-v2.1-final.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"protocol-v2.1 final authority is unreadable: {path}") from exc
    if not isinstance(payload, Mapping):
        raise RuntimeError("protocol-v2.1 final authority must be a JSON object")
    return materialize_protocol_v21_recipe(payload)
