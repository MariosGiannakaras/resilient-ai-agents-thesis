"""Fail-closed loader for the authoritative pre-freeze protocol-v1.1 candidate.

This module is intentionally separate from ``pilot_protocol.py``.  Historical
pilot/v1.0 validation semantics are immutable; v1.1 adds five strategy/config
identities, fresh held-out layouts/seeds and a candidate lifecycle that permits
only non-final development/tuning execution until T-522 freezes or amends it.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

from .contracts import InformationPolicy, ProtocolStage, ScenarioSpec
from .gridworld import ACTION_NAMES, GRIDWORLD_SCHEMA_VERSION, ResolvedGridWorldScenario
from .pilot_protocol import (
    PilotProtocol,
    _mapping,
    _object,
    _positive_integer,
    _probability,
    _seeds,
    _shortest_path_length,
)
from .protocol import ProtocolPartition

V11_PROTOCOL_SCHEMA_VERSION = 2
V11_STRATEGY_IDS = ("f0", "c0", "s0", "dq0", "d0")
V11_CONDITION_IDS = (
    "nominal",
    "action-remap-2-swap",
    "action-remap-4-cycle",
    "action-failure-1of8",
    "action-failure-1of4",
    "observation-corruption-1of8",
    "observation-corruption-1of4",
)
V11_FINAL_LAYOUT_IDS = (
    "v11-final-l01",
    "v11-final-l02",
    "v11-final-l03",
    "v11-final-l04",
)
_EXPECTED_METHODS = {
    "f0": "tabular_q_learning_v1",
    "c0": "tabular_q_learning_v1",
    "s0": "sarsa_v1",
    "dq0": "dyna_q_v1",
    "d0": "dyna_q_plus_v1",
}


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("protocol values must be finite JSON") from exc


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _exact_keys(value: Mapping[str, Any], expected: set[str], *, field: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{field} keys mismatch; missing={sorted(expected-actual)}, "
            f"unknown={sorted(actual-expected)}"
        )


def _nonempty(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _sequence(value: Any, *, field: str) -> tuple[Any, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{field} must be a sequence")
    return tuple(value)


def _finite_nonnegative(value: Any, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{field} must be finite and non-negative")
    return result


def _validate_layouts(
    payload: Mapping[str, Any], *, information_policy: InformationPolicy
) -> None:
    partitions = _object(payload["partitions"], field="partitions")
    expected_partition_keys = {"development", "tuning", "pilot", "final"}
    _exact_keys(partitions, expected_partition_keys, field="partitions")
    values = {
        key: tuple(_nonempty(item, field=f"partitions.{key}") for item in _sequence(partitions[key], field=f"partitions.{key}"))
        for key in expected_partition_keys
    }
    partition = ProtocolPartition(
        development_scenarios=values["development"],
        tuning_scenarios=values["tuning"],
        pilot_scenarios=values["pilot"],
        final_scenarios=values["final"],
    )
    partition.validate()
    if values["final"] != V11_FINAL_LAYOUT_IDS:
        raise ValueError("protocol-v1.1 must declare exactly four fresh final layouts")

    reward = _object(payload["reward_spec"], field="reward_spec")
    _exact_keys(reward, {"step", "collision", "goal"}, field="reward_spec")
    horizon = _object(payload["episode_horizon"], field="episode_horizon")
    _exact_keys(
        horizon,
        {"rule", "shortest_path_multiplier", "required_shortest_path_length"},
        field="episode_horizon",
    )
    if horizon["rule"] != "shortest-path-multiple":
        raise ValueError("episode_horizon.rule must be shortest-path-multiple")
    multiplier = _positive_integer(horizon["shortest_path_multiplier"], field="shortest_path_multiplier")
    distance = _positive_integer(horizon["required_shortest_path_length"], field="required_shortest_path_length")

    expected_ids = set().union(*(set(group) for group in values.values()))
    seen: set[str] = set()
    signatures: set[str] = set()
    for index, raw_layout in enumerate(_sequence(payload["layouts"], field="layouts")):
        layout = _object(raw_layout, field=f"layouts[{index}]")
        _exact_keys(layout, {"layout_id", "stage", "grid"}, field=f"layouts[{index}]")
        layout_id = _nonempty(layout["layout_id"], field="layout_id")
        stage = _nonempty(layout["stage"], field="layout stage")
        if stage not in values or layout_id not in values[stage]:
            raise ValueError("layout stage must agree with its partition")
        if layout_id in seen:
            raise ValueError("layout_id values must be unique")
        seen.add(layout_id)
        grid = _object(layout["grid"], field=f"layouts[{index}].grid")
        signature = _canonical_json(grid)
        if signature in signatures:
            raise ValueError("v1.1 layouts must be structurally distinct")
        signatures.add(signature)
        spec = ScenarioSpec(
            scenario_id=layout_id,
            environment_id="project-gridworld-v1",
            max_steps=distance * multiplier,
            reward_spec=dict(reward),
            initial_state_spec={"grid": dict(grid)},
            dynamics_spec={
                "action_vectors": {
                    "up": [0, -1], "right": [1, 0],
                    "down": [0, 1], "left": [-1, 0],
                }
            },
            observation_spec={
                "type": "position", "coordinate_order": "x-y",
                "reset_observation": "true-state",
            },
            action_disturbance_spec={"type": "no-op-failure", "failure_probability": 0.0},
            observation_disturbance_spec={"type": "position-mislocalization", "mislocalization_probability": 0.0},
            change_events=(),
            information_policy=information_policy,
        )
        resolved = ResolvedGridWorldScenario.from_spec(spec)
        if _shortest_path_length(resolved) != distance:
            raise ValueError("every v1.1 layout must match required shortest-path length")
    if seen != expected_ids:
        raise ValueError("layouts must exactly cover all partition identifiers")


def _validate_conditions(payload: Mapping[str, Any]) -> None:
    rows = _sequence(payload["conditions"], field="conditions")
    if tuple(str(row.get("condition_id")) for row in rows if isinstance(row, Mapping)) != V11_CONDITION_IDS:
        raise ValueError("protocol-v1.1 condition IDs/order do not match the predeclared seven-condition design")
    identity = tuple(ACTION_NAMES)
    for index, raw in enumerate(rows):
        row = _object(raw, field=f"conditions[{index}]")
        _exact_keys(
            row,
            {
                "condition_id", "scientific_role", "mechanism", "action_mapping",
                "remapped_actions", "action_failure_probability",
                "observation_corruption_probability",
            },
            field=f"conditions[{index}]",
        )
        _nonempty(row["scientific_role"], field="scientific_role")
        mechanism = row["mechanism"]
        if mechanism not in {"nominal", "action-remap", "action-failure", "observation-corruption"}:
            raise ValueError("unsupported v1.1 condition mechanism")
        mapping = _mapping(row["action_mapping"], field="action_mapping")
        remapped = row["remapped_actions"]
        if not isinstance(remapped, int) or isinstance(remapped, bool):
            raise ValueError("remapped_actions must be an integer")
        if remapped != sum(left != right for left, right in zip(identity, mapping, strict=True)):
            raise ValueError("remapped_actions must match action_mapping")
        failure = _probability(row["action_failure_probability"], field="action_failure_probability")
        corruption = _probability(row["observation_corruption_probability"], field="observation_corruption_probability")
        factors = int(mapping != identity) + int(failure > 0.0) + int(corruption > 0.0)
        if mechanism == "nominal" and factors != 0:
            raise ValueError("nominal must have no disturbance")
        if mechanism != "nominal" and factors != 1:
            raise ValueError("each non-nominal condition must perturb exactly one factor")
    if rows[1]["remapped_actions"] != 2 or rows[2]["remapped_actions"] != 4:
        raise ValueError("structural remap severities must be two-action swap and four-action cycle")


def _validate_agent_and_configuration_policy(payload: Mapping[str, Any]) -> None:
    regimes = _sequence(payload["agent_regimes"], field="agent_regimes")
    if tuple(str(row.get("agent_id")) for row in regimes if isinstance(row, Mapping)) != V11_STRATEGY_IDS:
        raise ValueError("agent_regimes must exactly cover f0/c0/s0/dq0/d0")
    for raw in regimes:
        row = _object(raw, field="agent regime")
        _exact_keys(row, {"agent_id", "method", "user_facing_name", "mechanism_badge", "post_change_learning"}, field="agent regime")
        agent_id = str(row["agent_id"])
        if row["method"] != _EXPECTED_METHODS[agent_id]:
            raise ValueError(f"unexpected method for {agent_id}")
        _nonempty(row["user_facing_name"], field="user_facing_name")
        _nonempty(row["mechanism_badge"], field="mechanism_badge")
        if row["post_change_learning"] is not (agent_id != "f0"):
            raise ValueError("post_change_learning declaration is inconsistent")

    checkpoint = _object(payload["checkpoint_training"], field="checkpoint_training")
    _exact_keys(
        checkpoint,
        {
            "configuration_id", "method", "learning_rate", "discount_factor",
            "exploration_epsilon", "training_episodes_per_layout",
            "bootstrap_on_truncation", "initial_q_value",
        },
        field="checkpoint_training",
    )
    if checkpoint != {
        "configuration_id": "common-q-checkpoint-v1",
        "method": "tabular_q_learning_v1",
        "learning_rate": 0.5,
        "discount_factor": 0.96875,
        "exploration_epsilon": 0.125,
        "training_episodes_per_layout": 512,
        "bootstrap_on_truncation": False,
        "initial_q_value": 0.0,
    }:
        raise ValueError("validated common Q-learning checkpoint budget must remain frozen")

    catalog = _object(payload["configuration_catalog"], field="configuration_catalog")
    if not catalog:
        raise ValueError("configuration_catalog must be non-empty")
    by_agent: dict[str, set[str]] = {agent: set() for agent in V11_STRATEGY_IDS}
    for config_id, raw in catalog.items():
        _nonempty(config_id, field="configuration_id")
        row = _object(raw, field=f"configuration_catalog.{config_id}")
        _exact_keys(row, {"agent_id", "method", "settings"}, field=f"configuration_catalog.{config_id}")
        agent_id = _nonempty(row["agent_id"], field="configuration agent_id")
        if agent_id not in _EXPECTED_METHODS or row["method"] != _EXPECTED_METHODS[agent_id]:
            raise ValueError("configuration method/agent identity mismatch")
        settings = _object(row["settings"], field=f"{config_id}.settings")
        base_keys = {
            "learning_rate", "discount_factor", "exploration_epsilon",
            "bootstrap_on_truncation", "initial_q_value",
        }
        extra = set()
        if agent_id in {"dq0", "d0"}:
            extra.add("planning_steps")
        if agent_id == "d0":
            extra.add("kappa")
        _exact_keys(settings, base_keys | extra, field=f"{config_id}.settings")
        _probability(settings["learning_rate"], field="learning_rate")
        _probability(settings["discount_factor"], field="discount_factor", allow_one=False)
        _probability(settings["exploration_epsilon"], field="exploration_epsilon")
        if settings["bootstrap_on_truncation"] is not False or settings["initial_q_value"] != 0.0:
            raise ValueError("v1.1 configurations require zero initial Q and no truncation bootstrap")
        if "planning_steps" in settings:
            _positive_integer(settings["planning_steps"], field="planning_steps")
        if "kappa" in settings and _finite_nonnegative(settings["kappa"], field="kappa") <= 0.0:
            raise ValueError("Dyna-Q+ kappa must be positive")
        by_agent[agent_id].add(config_id)

    tuning = _object(payload["tuning"], field="tuning")
    candidates = _object(tuning["candidate_configuration_ids"], field="candidate_configuration_ids")
    if set(candidates) != set(V11_STRATEGY_IDS):
        raise ValueError("tuning configuration map must cover all five strategies")
    for agent_id, values in candidates.items():
        ids = tuple(_nonempty(item, field="candidate configuration id") for item in _sequence(values, field=f"candidate_configuration_ids.{agent_id}"))
        if not ids or len(set(ids)) != len(ids) or any(item not in by_agent[agent_id] for item in ids):
            raise ValueError("candidate configuration IDs must be unique and agent-compatible")
    if len(tuple(candidates["s0"])) != 2 or len(tuple(candidates["dq0"])) != 2 or len(tuple(candidates["d0"])) != 4:
        raise ValueError("v1.1 tuning surface must remain bounded at 2 SARSA, 2 Dyna-Q and 4 Dyna-Q+ configurations")
    if tuning["single_run_or_best_seed_selection"] is not False:
        raise ValueError("single-run/best-seed configuration selection is forbidden")


def _validate_seed_and_analysis_policy(payload: Mapping[str, Any]) -> None:
    development = _object(payload["development"], field="development")
    tuning = _object(payload["tuning"], field="tuning")
    evaluation = _object(payload["evaluation"], field="evaluation")
    dev = _seeds(development["root_seeds"], field="development.root_seeds")
    tune = _seeds(tuning["root_seeds"], field="tuning.root_seeds")
    final = _seeds(evaluation["root_seeds"], field="evaluation.root_seeds")
    if len(dev) < 2 or len(tune) < 4 or len(final) != 32:
        raise ValueError("v1.1 requires multiple development/tuning roots and exactly 32 final roots")
    if set(dev) & set(tune) or set(dev) & set(final) or set(tune) & set(final):
        raise ValueError("development, tuning and final seed banks must be disjoint")
    if tuning["training_episodes_per_layout"] != 512 or tuning["evaluation_pre_change_episodes"] != 16 or tuning["evaluation_post_change_episodes"] != 32:
        raise ValueError("validated tuning episode budgets must remain 512/16/32")
    if tuple(tuning["condition_ids"]) != V11_CONDITION_IDS[:3]:
        raise ValueError("tuning is predeclared on nominal and the two primary remaps only")
    if evaluation["pre_change_episodes"] != 16 or evaluation["post_change_episodes"] != 32:
        raise ValueError("final evaluation episode budgets must remain 16/32")
    if tuple(evaluation["condition_ids"]) != V11_CONDITION_IDS or tuple(evaluation["final_layout_ids"]) != V11_FINAL_LAYOUT_IDS:
        raise ValueError("final evaluation must use the seven conditions and four held-out layouts")

    metrics = _object(payload["metric_policy"], field="metric_policy")
    if tuple(metrics["primary"]) != ("cumulative_deficit", "immediate_degradation", "terminal_performance"):
        raise ValueError("primary metric order is predeclared")
    if metrics["composite_resilience_score"] is not False or metrics["recovery_is_sensitivity"] is not True:
        raise ValueError("recovery must remain secondary and no composite score is allowed")

    analysis = _object(payload["statistical_analysis_plan"], field="statistical_analysis_plan")
    ci = _object(analysis["confidence_interval"], field="confidence_interval")
    if ci.get("level") != 0.95 or ci.get("method") != "percentile-bootstrap-over-root-level-paired-effects" or ci.get("resamples") != 10000:
        raise ValueError("paired 95% bootstrap CI plan must be fixed before final outcomes")
    _seeds([ci.get("analysis_seed")], field="analysis_seed")
    contrasts = tuple(tuple(item) for item in _sequence(analysis["predeclared_contrasts"], field="predeclared_contrasts"))
    expected = (("c0","f0"),("s0","f0"),("dq0","f0"),("d0","f0"),("s0","c0"),("dq0","c0"),("d0","dq0"))
    if contrasts != expected:
        raise ValueError("mechanistic paired contrasts must remain predeclared")


def _validate_payload(payload: Mapping[str, Any]) -> None:
    expected = {
        "schema_version", "protocol_version", "status", "scientific_scope",
        "gridworld_schema_version", "information_policy", "partitions", "layouts",
        "reward_spec", "episode_horizon", "conditions", "agent_regimes",
        "checkpoint_training", "configuration_catalog", "development", "tuning",
        "evaluation", "metric_policy", "statistical_analysis_plan",
        "robust_planner_gate", "resource_policy", "stopping_policy",
        "required_artifacts", "failure_and_exclusion_policy",
    }
    _exact_keys(payload, expected, field="protocol-v1.1")
    if payload["schema_version"] != V11_PROTOCOL_SCHEMA_VERSION:
        raise ValueError("unsupported protocol-v1.1 schema_version")
    if payload["gridworld_schema_version"] != GRIDWORLD_SCHEMA_VERSION:
        raise ValueError("GridWorld schema version mismatch")
    if payload["protocol_version"] != "protocol-v1.1-candidate" or payload["status"] != "candidate":
        raise ValueError("T-521 protocol must remain an explicit candidate")
    scope = _object(payload["scientific_scope"], field="scientific_scope")
    _exact_keys(scope, {"primary_question", "final_evidence_use", "testbed_role"}, field="scientific_scope")
    _nonempty(scope["primary_question"], field="primary_question")
    _nonempty(scope["testbed_role"], field="testbed_role")
    if scope["final_evidence_use"] is not False:
        raise ValueError("candidate protocol cannot authorize final evidence")

    policy_payload = _object(payload["information_policy"], field="information_policy")
    _exact_keys(policy_payload, {"expose_executed_action", "expose_disturbance_flags", "expose_change_indicator", "expose_regime_id", "expose_true_state"}, field="information_policy")
    if any(value is not False for value in policy_payload.values()):
        raise ValueError("all evaluator-only information must remain hidden")
    information_policy = InformationPolicy(**dict(policy_payload))

    _validate_layouts(payload, information_policy=information_policy)
    _validate_conditions(payload)
    _validate_agent_and_configuration_policy(payload)
    _validate_seed_and_analysis_policy(payload)
    failure = _object(payload["failure_and_exclusion_policy"], field="failure_and_exclusion_policy")
    if failure.get("final_evidence_allowed") is not False or failure.get("post_final_configuration_switching") is not False:
        raise ValueError("candidate protocol must block final evidence and post-final switching")
    _canonical_json(payload)


class V11CandidateProtocol(PilotProtocol):
    """Validated candidate v1.1 protocol with configuration identities."""

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "V11CandidateProtocol":
        if not isinstance(payload, Mapping):
            raise ValueError("protocol-v1.1 must be an object")
        _validate_payload(payload)
        return cls(_canonical_json(payload))

    @property
    def status(self) -> str:
        return str(self.to_dict()["status"])

    def protocol_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    def strategy_ids(self) -> tuple[str, ...]:
        return V11_STRATEGY_IDS

    def configuration(self, configuration_id: str) -> dict[str, Any]:
        catalog = self.to_dict()["configuration_catalog"]
        if configuration_id not in catalog:
            raise ValueError(f"unknown protocol-v1.1 configuration_id: {configuration_id}")
        return json.loads(_canonical_json(catalog[configuration_id]))

    def configuration_sha256(self, configuration_id: str) -> str:
        return _sha256({"configuration_id": configuration_id, **self.configuration(configuration_id)})

    def candidate_configuration_ids(self, agent_id: str) -> tuple[str, ...]:
        if agent_id not in V11_STRATEGY_IDS:
            raise ValueError("unknown v1.1 agent strategy")
        values = self.to_dict()["tuning"]["candidate_configuration_ids"][agent_id]
        return tuple(str(value) for value in values)

    def root_seeds_for(self, stage: ProtocolStage) -> tuple[int, ...]:
        payload = self.to_dict()
        if stage is ProtocolStage.DEVELOPMENT:
            return tuple(payload["development"]["root_seeds"])
        if stage is ProtocolStage.TUNING:
            return tuple(payload["tuning"]["root_seeds"])
        if stage is ProtocolStage.FINAL:
            return tuple(payload["evaluation"]["root_seeds"])
        return ()

    def assert_execution_allowed(self, stage: ProtocolStage) -> None:
        if stage not in {ProtocolStage.DEVELOPMENT, ProtocolStage.TUNING}:
            raise ValueError("candidate protocol-v1.1 permits non-final development/tuning execution only")


def load_v11_candidate_protocol(path: Path) -> V11CandidateProtocol:
    if not isinstance(path, Path):
        path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load protocol-v1.1: {path}") from exc
    return V11CandidateProtocol.from_dict(payload)


__all__ = [
    "V11_CONDITION_IDS",
    "V11_FINAL_LAYOUT_IDS",
    "V11_PROTOCOL_SCHEMA_VERSION",
    "V11_STRATEGY_IDS",
    "V11CandidateProtocol",
    "load_v11_candidate_protocol",
]
