"""Fail-closed loader for the versioned pre-final pilot protocol."""
from __future__ import annotations

import copy
import json
import math
from collections import deque
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contracts import InformationPolicy, ScenarioSpec
from .gridworld import ACTION_NAMES, GRIDWORLD_SCHEMA_VERSION, ResolvedGridWorldScenario
from .protocol import ProtocolPartition

PILOT_PROTOCOL_SCHEMA_VERSION = 1
_STAGES = ("development", "tuning", "pilot", "final")


def _exact_keys(value: Mapping[str, Any], expected: set[str], *, field: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{field} keys mismatch; "
            f"missing={sorted(expected - actual)}, unknown={sorted(actual - expected)}"
        )


def _object(value: Any, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _sequence(value: Any, *, field: str) -> tuple[Any, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{field} must be a sequence")
    return tuple(value)


def _nonempty_string(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _positive_integer(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{field} must be a positive integer")
    return value


def _probability(value: Any, *, field: str, allow_one: bool = True) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    upper_valid = result <= 1.0 if allow_one else result < 1.0
    if not math.isfinite(result) or result < 0.0 or not upper_valid:
        boundary = "[0, 1]" if allow_one else "[0, 1)"
        raise ValueError(f"{field} must be finite and in {boundary}")
    return result


def _unique_strings(value: Any, *, field: str) -> tuple[str, ...]:
    items = _sequence(value, field=field)
    result = tuple(
        _nonempty_string(item, field=f"{field} item") for item in items
    )
    if not result or len(set(result)) != len(result):
        raise ValueError(f"{field} must be non-empty and unique")
    return result


def _seeds(value: Any, *, field: str) -> tuple[int, ...]:
    items = _sequence(value, field=field)
    if not items:
        raise ValueError(f"{field} must be non-empty")
    seeds: list[int] = []
    for item in items:
        if (
            not isinstance(item, int)
            or isinstance(item, bool)
            or not 0 <= item < 2**64
        ):
            raise ValueError(f"{field} values must be integers in [0, 2**64)")
        seeds.append(item)
    if len(set(seeds)) != len(seeds):
        raise ValueError(f"{field} values must be unique")
    return tuple(seeds)


def _shortest_path_length(scenario: ResolvedGridWorldScenario) -> int:
    frontier = deque([(scenario.start, 0)])
    visited = {scenario.start}
    while frontier:
        current, distance = frontier.popleft()
        if current == scenario.goal:
            return distance
        for dx, dy in scenario.action_vectors:
            candidate = current[0] + dx, current[1] + dy
            if (
                0 <= candidate[0] < scenario.width
                and 0 <= candidate[1] < scenario.height
                and candidate not in scenario.obstacles
                and candidate not in visited
            ):
                visited.add(candidate)
                frontier.append((candidate, distance + 1))
    raise ValueError("layout goal is unreachable")


def _mapping(value: Any, *, field: str) -> tuple[str, ...]:
    mapping = _object(value, field=field)
    if set(mapping) != set(ACTION_NAMES):
        raise ValueError(f"{field} must cover exactly {ACTION_NAMES}")
    result = tuple(mapping[name] for name in ACTION_NAMES)
    if not all(isinstance(item, str) for item in result):
        raise ValueError(f"{field} values must be action names")
    if set(result) != set(ACTION_NAMES):
        raise ValueError(f"{field} must be a permutation of {ACTION_NAMES}")
    return result


class PilotProtocol:
    """Validated immutable-by-serialization view of one pilot protocol."""

    def __init__(self, canonical_payload: str) -> None:
        self._canonical_payload = canonical_payload

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PilotProtocol":
        if not isinstance(payload, Mapping):
            raise ValueError("pilot protocol must be an object")
        _validate_payload(payload)
        try:
            canonical = json.dumps(
                payload,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("pilot protocol must be finite JSON") from exc
        return cls(canonical)

    @property
    def protocol_version(self) -> str:
        return str(self.to_dict()["protocol_version"])

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self._canonical_payload)

    def canonical_json(self) -> str:
        return self._canonical_payload

    def partition(self) -> ProtocolPartition:
        partitions = self.to_dict()["partitions"]
        return ProtocolPartition(
            development_scenarios=tuple(partitions["development"]),
            tuning_scenarios=tuple(partitions["tuning"]),
            pilot_scenarios=tuple(partitions["pilot"]),
            final_scenarios=tuple(partitions["final"]),
        )

    def layout_ids(self) -> tuple[str, ...]:
        return tuple(layout["layout_id"] for layout in self.to_dict()["layouts"])

    def condition_ids(self) -> tuple[str, ...]:
        return tuple(
            condition["condition_id"] for condition in self.to_dict()["conditions"]
        )


def _validate_payload(payload: Mapping[str, Any]) -> None:
    expected_keys = {
        "schema_version",
        "protocol_version",
        "status",
        "scientific_scope",
        "gridworld_schema_version",
        "information_policy",
        "partitions",
        "layouts",
        "reward_spec",
        "episode_horizon",
        "conditions",
        "agent_regimes",
        "tuning",
        "evaluation",
        "metric_sensitivity",
        "resource_policy",
        "stopping_policy",
        "required_artifacts",
        "failure_and_exclusion_policy",
    }
    actual_keys = set(payload.keys())
    if "robust_prior" in actual_keys:
        expected_keys.add("robust_prior")
    if "tuning_policy" in actual_keys:
        expected_keys.add("tuning_policy")
    if "pilot_analysis" in actual_keys:
        expected_keys.add("pilot_analysis")
    elif "statistical_analysis_plan" in actual_keys:
        expected_keys.add("statistical_analysis_plan")
    else:
        raise ValueError("Must have pilot_analysis or statistical_analysis_plan")

    _exact_keys(payload, expected_keys, field="pilot protocol")
    if payload["schema_version"] != PILOT_PROTOCOL_SCHEMA_VERSION:
        raise ValueError("unsupported pilot protocol schema_version")
    if payload["gridworld_schema_version"] != GRIDWORLD_SCHEMA_VERSION:
        raise ValueError("pilot protocol GridWorld schema version mismatch")
    _nonempty_string(payload["protocol_version"], field="protocol_version")
    if payload["status"] not in ("pilot-unfrozen", "frozen"):
        raise ValueError("pilot protocol status must be pilot-unfrozen or frozen")
    scope = _object(payload["scientific_scope"], field="scientific_scope")
    expected_scope_keys = {"primary_question", "final_evidence_use"}
    if "pilot_purpose" in scope:
        expected_scope_keys.add("pilot_purpose")
    _exact_keys(
        scope,
        expected_scope_keys,
        field="scientific_scope",
    )
    _nonempty_string(scope["primary_question"], field="primary_question")
    if "pilot_purpose" in scope:
        _nonempty_string(scope["pilot_purpose"], field="pilot_purpose")
    if payload["status"] == "pilot-unfrozen" and scope["final_evidence_use"] is not False:
        raise ValueError("pilot protocol cannot authorize final evidence use")
    if payload["status"] == "frozen" and scope["final_evidence_use"] is not True:
        raise ValueError("frozen protocol must authorize final evidence use")

    policy_payload = _object(payload["information_policy"], field="information_policy")
    _exact_keys(
        policy_payload,
        {
            "expose_executed_action",
            "expose_disturbance_flags",
            "expose_change_indicator",
            "expose_regime_id",
            "expose_true_state",
        },
        field="information_policy",
    )
    if any(value is not False for value in policy_payload.values()):
        raise ValueError("pilot agents must use the strict all-hidden information policy")
    information_policy = InformationPolicy(**dict(policy_payload))

    partition_payload = _object(payload["partitions"], field="partitions")
    _exact_keys(partition_payload, set(_STAGES), field="partitions")
    partition_values = {
        stage: tuple(_nonempty_string(x, field=f"partitions.{stage}") for x in partition_payload.get(stage, []))
        for stage in _STAGES
    }
    partition = ProtocolPartition(
        development_scenarios=partition_values["development"],
        tuning_scenarios=partition_values["tuning"],
        pilot_scenarios=partition_values["pilot"],
        final_scenarios=partition_values["final"],
    )
    partition.validate()

    reward_spec = _object(payload["reward_spec"], field="reward_spec")
    _exact_keys(reward_spec, {"step", "collision", "goal"}, field="reward_spec")
    horizon = _object(payload["episode_horizon"], field="episode_horizon")
    _exact_keys(
        horizon,
        {"rule", "shortest_path_multiplier", "required_shortest_path_length"},
        field="episode_horizon",
    )
    if horizon["rule"] != "shortest-path-multiple":
        raise ValueError("episode_horizon.rule must be shortest-path-multiple")
    multiplier = _positive_integer(
        horizon["shortest_path_multiplier"], field="shortest_path_multiplier"
    )
    required_distance = _positive_integer(
        horizon["required_shortest_path_length"], field="required_shortest_path_length"
    )

    layouts = _sequence(payload["layouts"], field="layouts")
    expected_layout_ids = set().union(*(set(values) for values in partition_values.values()))
    seen_layout_ids: set[str] = set()
    for index, raw_layout in enumerate(layouts):
        layout = _object(raw_layout, field=f"layouts[{index}]")
        _exact_keys(layout, {"layout_id", "stage", "grid"}, field=f"layouts[{index}]")
        layout_id = _nonempty_string(layout["layout_id"], field="layout_id")
        stage = layout["stage"]
        if stage not in _STAGES or layout_id not in partition_values[str(stage)]:
            raise ValueError("layout stage must agree with its protocol partition")
        if layout_id in seen_layout_ids:
            raise ValueError("layout_id values must be unique")
        seen_layout_ids.add(layout_id)
        grid = _object(layout["grid"], field=f"layouts[{index}].grid")
        scenario = ScenarioSpec(
            scenario_id=layout_id,
            environment_id="project-gridworld-v1",
            max_steps=required_distance * multiplier,
            reward_spec=dict(reward_spec),
            initial_state_spec={"grid": dict(grid)},
            dynamics_spec={
                "action_vectors": {
                    "up": [0, -1],
                    "right": [1, 0],
                    "down": [0, 1],
                    "left": [-1, 0],
                }
            },
            observation_spec={
                "type": "position",
                "coordinate_order": "x-y",
                "reset_observation": "true-state",
            },
            action_disturbance_spec={
                "type": "no-op-failure",
                "failure_probability": 0.0,
            },
            observation_disturbance_spec={
                "type": "position-mislocalization",
                "mislocalization_probability": 0.0,
            },
            change_events=(),
            information_policy=information_policy,
        )
        resolved = ResolvedGridWorldScenario.from_spec(scenario)
        if _shortest_path_length(resolved) != required_distance:
            raise ValueError("every layout must match required_shortest_path_length")
    if seen_layout_ids != expected_layout_ids:
        raise ValueError("layouts must exactly cover all partition identifiers")

    condition_rows = _sequence(payload["conditions"], field="conditions")
    condition_ids: set[str] = set()
    condition_mappings: dict[str, tuple[str, ...]] = {}
    identity = ACTION_NAMES
    nominal_count = 0
    for index, raw_condition in enumerate(condition_rows):
        condition = _object(raw_condition, field=f"conditions[{index}]")
        cond_expected_keys = {
            "condition_id",
            "scientific_role",
            "mechanism",
            "action_mapping",
            "remapped_actions",
            "action_failure_probability",
            "observation_corruption_probability",
        }
        if "r0_set_membership" in condition:
            cond_expected_keys.add("r0_set_membership")
        _exact_keys(
            condition,
            cond_expected_keys,
            field=f"conditions[{index}]",
        )
        condition_id = _nonempty_string(condition["condition_id"], field="condition_id")
        if condition_id in condition_ids:
            raise ValueError("condition_id values must be unique")
        condition_ids.add(condition_id)
        _nonempty_string(condition["scientific_role"], field="scientific_role")
        mechanism = condition["mechanism"]
        if mechanism not in {
            "nominal",
            "action-remap",
            "action-failure",
            "observation-corruption",
        }:
            raise ValueError("unsupported pilot condition mechanism")
        mapping = _mapping(condition["action_mapping"], field="action_mapping")
        condition_mappings[condition_id] = mapping
        remapped = condition["remapped_actions"]
        if not isinstance(remapped, int) or isinstance(remapped, bool):
            raise ValueError("remapped_actions must be an integer")
        actual_remapped = sum(left != right for left, right in zip(identity, mapping, strict=True))
        if remapped != actual_remapped:
            raise ValueError("remapped_actions must match action_mapping")
        action_failure = _probability(
            condition["action_failure_probability"], field="action_failure_probability"
        )
        observation_corruption = _probability(
            condition["observation_corruption_probability"],
            field="observation_corruption_probability",
        )
        active_factors = sum(
            (
                mapping != identity,
                action_failure > 0.0,
                observation_corruption > 0.0,
            )
        )
        r0_membership = condition.get("r0_set_membership", "not-applicable")
        if mechanism == "nominal":
            nominal_count += 1
            if active_factors != 0 or r0_membership != "not-applicable":
                raise ValueError("nominal condition must have no disturbance")
        elif active_factors != 1:
            raise ValueError("pilot conditions must perturb exactly one factor")
        if mechanism == "action-remap":
            if mapping == identity or (r0_membership not in {"in-set", "out-of-set"} and "robust_prior" in payload):
                raise ValueError("action-remap conditions require declared R0 set membership when robust_prior is active")
        elif mechanism == "action-failure" and action_failure <= 0.0:
            raise ValueError("action-failure condition requires positive failure probability")
        elif mechanism == "observation-corruption" and observation_corruption <= 0.0:
            raise ValueError(
                "observation-corruption condition requires positive corruption probability"
            )
        elif r0_membership != "not-applicable":
            raise ValueError("only action-remap conditions have R0 set membership")
    if nominal_count != 1:
        raise ValueError("conditions must contain exactly one nominal condition")

    regimes = _sequence(payload["agent_regimes"], field="agent_regimes")
    regime_ids: set[str] = set()
    expected_regimes = {
        "f0": ("tabular_q_learning_v1", False),
        "c0": ("tabular_q_learning_v1", True),
        "r0": ("rectangular_robust_value_iteration_v1", False),
    }
    for index, raw_regime in enumerate(regimes):
        regime = _object(raw_regime, field=f"agent_regimes[{index}]")
        _exact_keys(
            regime,
            {
                "agent_id",
                "method",
                "checkpoint_source",
                "post_change_learning",
                "deployment_exploration",
                "method_configuration",
            },
            field=f"agent_regimes[{index}]",
        )
        agent_id = _nonempty_string(regime["agent_id"], field="agent_id")
        if agent_id not in expected_regimes or agent_id in regime_ids:
            raise ValueError("agent_regimes must contain unique f0, c0, and r0 entries")
        regime_ids.add(agent_id)
        expected_method, expected_learning = expected_regimes[agent_id]
        if regime["method"] != expected_method:
            raise ValueError("agent regime method does not match DEC-034")
        if regime["post_change_learning"] is not expected_learning:
            raise ValueError("agent post-change learning regime does not match DEC-034")
        _nonempty_string(regime["checkpoint_source"], field="checkpoint_source")
        if regime["deployment_exploration"] != "selected-common-epsilon":
            raise ValueError("all pilot regimes must share selected deployment epsilon")
        method_configuration = _object(
            regime["method_configuration"], field="method_configuration"
        )
        if agent_id in {"f0", "c0"}:
            expected_configuration = {
                "learning_rate_policy": "selected-tuning-value",
                "discount_policy": "selected-common-discount",
                "bootstrap_on_truncation": False,
                "initial_q_value": 0.0,
            }
            if method_configuration != expected_configuration:
                raise ValueError("pilot Q-learning method configuration is inconsistent")
        else:
            expected_r0_keys = {
                "discount_policy",
                "initial_value",
                "convergence_tolerance",
                "max_iterations",
            }
            if payload["protocol_version"] == "pilot-v0.2":
                expected_r0_keys.add("active_terminal_observation_policy")
            _exact_keys(
                method_configuration,
                expected_r0_keys,
                field="R0 method_configuration",
            )
            if payload["protocol_version"] == "pilot-v0.2" and method_configuration[
                "active_terminal_observation_policy"
            ] != "zero-value-seeded-action-tie":
                raise ValueError("pilot-v0.2 requires the amended R0 alias policy")
            if method_configuration["discount_policy"] != "selected-common-discount":
                raise ValueError("R0 must use the common selected discount")
            if method_configuration["initial_value"] != 0.0:
                raise ValueError("R0 initial_value must be explicit zero")
            tolerance = method_configuration["convergence_tolerance"]
            if (
                not isinstance(tolerance, (int, float))
                or isinstance(tolerance, bool)
                or not math.isfinite(float(tolerance))
                or float(tolerance) <= 0.0
            ):
                raise ValueError("R0 convergence_tolerance must be finite and positive")
            _positive_integer(
                method_configuration["max_iterations"], field="R0 max_iterations"
            )
    if not (regime_ids == {"f0", "c0", "r0"} or regime_ids == {"f0", "c0"}):
        raise ValueError("agent_regimes must exactly cover f0, c0, and r0 (or f0, c0 for v1.0)")

    if "robust_prior" in payload:
        robust = _object(payload["robust_prior"], field="robust_prior")
        _exact_keys(
            robust,
            {
                "set_id",
                "fixed_before_pilot",
                "uncertainty_semantics",
                "candidate_action_mappings",
            },
            field="robust_prior",
        )
        _nonempty_string(robust["set_id"], field="robust_prior.set_id")
        if robust["fixed_before_pilot"] is not True:
            raise ValueError("robust uncertainty set must be fixed before pilot outcomes")
        if (
            robust["uncertainty_semantics"]
            != "state-action-rectangular-closure-of-candidate-mappings"
        ):
            raise ValueError("robust prior must declare s,a-rectangular closure semantics")
        robust_mappings = tuple(
            _mapping(item, field="robust candidate mapping")
            for item in _sequence(
                robust["candidate_action_mappings"], field="candidate_action_mappings"
            )
        )
        if not robust_mappings or len(set(robust_mappings)) != len(robust_mappings):
            raise ValueError("robust candidate mappings must be non-empty and unique")
        if identity not in robust_mappings:
            raise ValueError("robust uncertainty set must include nominal identity")
        for raw_condition in condition_rows:
            condition = _object(raw_condition, field="condition")
            if "r0_set_membership" in condition:
                membership = condition["r0_set_membership"]
                mapping = condition_mappings[str(condition["condition_id"])]
                if membership == "in-set" and mapping not in robust_mappings:
                    raise ValueError("in-set condition mapping is absent from robust prior")
                if membership == "out-of-set" and mapping in robust_mappings:
                    raise ValueError("out-of-set condition mapping appears in robust prior")

    tuning = _object(payload["tuning"], field="tuning")
    expected_tuning_keys = {
            "root_seeds",
            "training_episodes_per_layout",
            "nominal_evaluation_episodes_per_layout",
            "q_learning_search",
            "checkpoint_selection",
    }
    if "robust_set_policy" in tuning:
        expected_tuning_keys.add("robust_set_policy")
    _exact_keys(tuning, expected_tuning_keys, field="tuning")
    tuning_seeds = _seeds(tuning["root_seeds"], field="tuning.root_seeds")
    _positive_integer(
        tuning["training_episodes_per_layout"], field="training_episodes_per_layout"
    )
    _positive_integer(
        tuning["nominal_evaluation_episodes_per_layout"],
        field="nominal_evaluation_episodes_per_layout",
    )
    search = _object(tuning["q_learning_search"], field="q_learning_search")
    _exact_keys(
        search,
        {
            "strategy",
            "learning_rates",
            "exploration_epsilons",
            "discount_factors",
            "stage_one_discount_factor",
            "stage_two_rule",
            "total_unique_configurations",
        },
        field="q_learning_search",
    )
    if search["strategy"] != "staged-dyadic-grid":
        raise ValueError("q_learning_search.strategy must be staged-dyadic-grid")
    for field in ("learning_rates", "exploration_epsilons", "discount_factors"):
        candidates = _sequence(search[field], field=f"q_learning_search.{field}")
        values = tuple(_probability(item, field=field, allow_one=False) for item in candidates)
        if not values or len(set(values)) != len(values):
            raise ValueError(f"q_learning_search.{field} must be non-empty and unique")
    if search["stage_one_discount_factor"] not in search["discount_factors"]:
        raise ValueError("stage-one discount must be in discount_factors")
    if (
        search["stage_two_rule"]
        != "evaluate remaining discount factors only for the stage-one winner"
    ):
        raise ValueError("unsupported staged Q-learning search rule")
    expected_search_count = len(search["learning_rates"]) * len(
        search["exploration_epsilons"]
    ) + len(search["discount_factors"]) - 1
    if search["total_unique_configurations"] != expected_search_count:
        raise ValueError("total_unique_configurations does not match staged search")
    if "robust_set_policy" in tuning and tuning["robust_set_policy"] != "fixed-declared-set-no-pilot-outcome-tuning":
        raise ValueError("robust_set_policy must forbid pilot-outcome tuning")
    _unique_strings(tuning["checkpoint_selection"], field="checkpoint_selection")

    evaluation = _object(payload["evaluation"], field="evaluation")
    _exact_keys(
        evaluation,
        {
            "root_seeds",
            "pre_change_episodes",
            "post_change_episodes",
            "change_boundary",
            "paired_reference",
            "condition_ids",
            "retention_policy",
        },
        field="evaluation",
    )
    evaluation_seeds = _seeds(evaluation["root_seeds"], field="evaluation.root_seeds")
    if set(tuning_seeds) & set(evaluation_seeds):
        raise ValueError("tuning and pilot root seeds must be disjoint")
    _positive_integer(evaluation["pre_change_episodes"], field="pre_change_episodes")
    _positive_integer(evaluation["post_change_episodes"], field="post_change_episodes")
    if evaluation["change_boundary"] != "between-episode-blocks":
        raise ValueError("change_boundary must be between-episode-blocks")
    if evaluation["paired_reference"] != "same-checkpoint-layout-root-seed":
        raise ValueError("paired_reference must preserve matched reference inputs")
    configured_conditions = _unique_strings(
        evaluation["condition_ids"], field="evaluation.condition_ids"
    )
    if set(configured_conditions) != condition_ids:
        raise ValueError("evaluation.condition_ids must exactly cover protocol conditions")
    if evaluation["retention_policy"] != "events-plus-episode-curves":
        raise ValueError("pilot retention_policy must preserve events and episode curves")

    metrics = _object(payload["metric_sensitivity"], field="metric_sensitivity")
    _exact_keys(
        metrics,
        {
            "curve_unit",
            "immediate_windows",
            "worst_windows",
            "terminal_windows",
            "recovery_tolerances_step_reward_units",
            "recovery_stability_episodes",
            "selection_use",
        },
        field="metric_sensitivity",
    )
    if metrics["curve_unit"] != "episode-return":
        raise ValueError("pilot metric curve_unit must be episode-return")
    for field in (
        "immediate_windows",
        "worst_windows",
        "terminal_windows",
        "recovery_stability_episodes",
    ):
        values = tuple(
            _positive_integer(item, field=field)
            for item in _sequence(metrics[field], field=field)
        )
        if not values or len(set(values)) != len(values):
            raise ValueError(f"{field} must be non-empty and unique")
    raw_tolerances = _sequence(
        metrics["recovery_tolerances_step_reward_units"],
        field="recovery_tolerances_step_reward_units",
    )
    if any(
        not isinstance(item, (int, float)) or isinstance(item, bool)
        for item in raw_tolerances
    ):
        raise ValueError("recovery tolerance candidates must be numeric")
    tolerances = tuple(float(item) for item in raw_tolerances)
    if not tolerances or any(not math.isfinite(item) or item < 0.0 for item in tolerances):
        raise ValueError("recovery tolerance candidates must be finite and non-negative")
    if metrics["selection_use"] != "diagnostic-only-not-model-selection":
        raise ValueError("metric sensitivity cannot tune models on pilot outcomes")

    resources = _object(payload["resource_policy"], field="resource_policy")
    _exact_keys(
        resources,
        {
            "runtime_baseline",
            "initial_concurrency",
            "preflight_required",
            "child_timeout_rule",
            "gpu_required",
        },
        field="resource_policy",
    )
    _nonempty_string(resources["runtime_baseline"], field="runtime_baseline")
    _positive_integer(resources["initial_concurrency"], field="initial_concurrency")
    if resources["preflight_required"] is not True or resources["gpu_required"] is not False:
        raise ValueError("pilot resource policy must require CPU preflight without GPU")
    timeout = _object(resources["child_timeout_rule"], field="child_timeout_rule")
    _exact_keys(
        timeout,
        {
            "measured_preflight_multiplier",
            "minimum_seconds",
            "maximum_seconds",
            "overflow_action",
        },
        field="child_timeout_rule",
    )
    _positive_integer(
        timeout["measured_preflight_multiplier"], field="measured_preflight_multiplier"
    )
    minimum_timeout = _positive_integer(timeout["minimum_seconds"], field="minimum_seconds")
    maximum_timeout = _positive_integer(timeout["maximum_seconds"], field="maximum_seconds")
    if maximum_timeout <= minimum_timeout:
        raise ValueError("maximum timeout must exceed minimum timeout")
    if timeout["overflow_action"] not in ("protocol-amendment-before-pilot", "protocol-amendment-before-final"):
        raise ValueError("timeout overflow must require a protocol amendment")

    stopping = _object(payload["stopping_policy"], field="stopping_policy")
    _exact_keys(
        stopping,
        {
            "training",
            "evaluation",
            "early_success_stopping",
            "invalid_or_nonfinite_state",
            "timeout",
        },
        field="stopping_policy",
    )
    if stopping != {
        "training": "fixed-configured-episode-count",
        "evaluation": "fixed-pre-and-post-episode-blocks",
        "early_success_stopping": False,
        "invalid_or_nonfinite_state": "fail-immediately-and-retain",
        "timeout": "finalize-failed-and-retain-partial-output",
    }:
        raise ValueError("stopping_policy must match the bounded pilot lifecycle")

    analysis_key = "pilot_analysis" if "pilot_analysis" in payload else "statistical_analysis_plan"
    analysis = _object(payload[analysis_key], field=analysis_key)
    _exact_keys(
        analysis,
        {
            "unit_of_analysis",
            "pairing_block",
            "aggregation",
            "inferential_claims_allowed",
            "non_recovery_handling",
            "failed_or_invalid_handling",
        } | ({"estimands"} if analysis_key == "statistical_analysis_plan" else set()),
        field=analysis_key,
    )
    for field in (
        "unit_of_analysis",
        "pairing_block",
        "aggregation",
        "non_recovery_handling",
        "failed_or_invalid_handling",
    ):
        _nonempty_string(analysis[field], field=f"{analysis_key}.{field}")
    if analysis_key == "pilot_analysis" and analysis["inferential_claims_allowed"] is not False:
        raise ValueError("pilot analysis cannot authorize inferential claims")
    _unique_strings(payload["required_artifacts"], field="required_artifacts")

    failure = _object(
        payload["failure_and_exclusion_policy"], field="failure_and_exclusion_policy"
    )
    _exact_keys(
        failure,
        {
            "completed_valid_runs_included_regardless_of_outcome",
            "non_recovery_is_valid",
            "automatic_outlier_exclusion",
            "rerun_uses_new_run_id",
            "invalid_reasons",
            "analysis_exclusion_reasons",
        },
        field="failure_and_exclusion_policy",
    )
    if failure["completed_valid_runs_included_regardless_of_outcome"] is not True:
        raise ValueError("valid poor outcomes must remain included")
    if failure["non_recovery_is_valid"] is not True:
        raise ValueError("non-recovery must remain a valid outcome")
    if failure["automatic_outlier_exclusion"] is not False:
        raise ValueError("automatic outlier exclusion is forbidden")
    if failure["rerun_uses_new_run_id"] is not True:
        raise ValueError("reruns must preserve original run identity/history")
    _unique_strings(failure["invalid_reasons"], field="invalid_reasons")
    _unique_strings(
        failure["analysis_exclusion_reasons"], field="analysis_exclusion_reasons"
    )


def load_pilot_protocol(path: Path) -> PilotProtocol:
    """Read and validate a protocol JSON file without inferred defaults."""

    if not isinstance(path, Path):
        raise ValueError("path must be pathlib.Path")
    try:
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read pilot protocol: {path}") from exc
    if isinstance(payload, dict) and set(payload) == {
        "base_protocol",
        "protocol_version",
        "amendments",
    }:
        base_name = payload["base_protocol"]
        amendments = payload["amendments"]
        if (
            base_name != "pilot-v0.1.json"
            or payload["protocol_version"] != "pilot-v0.2"
            or amendments
            != {
                "r0_active_terminal_observation_policy": "zero-value-seeded-action-tie",
                "pilot_seed_policy": "retain-v0.1-seeds-for-paired-implementation-retry",
                "tuning_policy": "reuse-v0.1-f0-selection-no-retuning",
            }
        ):
            raise ValueError("unsupported pilot protocol amendment overlay")
        base = load_pilot_protocol(path.with_name(base_name)).to_dict()
        expanded = copy.deepcopy(base)
        expanded["protocol_version"] = "pilot-v0.2"
        r0 = next(
            item for item in expanded["agent_regimes"] if item["agent_id"] == "r0"
        )
        r0["method_configuration"]["active_terminal_observation_policy"] = (
            "zero-value-seeded-action-tie"
        )
        payload = expanded
    return PilotProtocol.from_dict(payload)
