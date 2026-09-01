"""DEC-053 audit helpers for SB3 scientific continuation identity.

The historical protocol-v2 learner fingerprint remains immutable.  This module
does not replace or reinterpret it.  It makes the continuation invariants that
are independently implied by the frozen construction/execution path explicit,
and separates them from SB3's transport archive metadata.
"""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from typing import Any, Mapping

from .protocol_v2_sb3 import (
    SB3ScientificStateAdapter,
    _digest_value,
    _replay_fingerprint,
)


SCIENTIFIC_CONTINUATION_IDENTITY_SCHEMA_VERSION = 1


def _state_dict_digest(value: Any) -> str:
    return _digest_value(value)


def _schedule_descriptor(schedule: Any) -> Mapping[str, Any]:
    """Return the numeric definition of the frozen SB3 schedules we use."""

    descriptor: dict[str, Any] = {
        "class_module": type(schedule).__module__,
        "class_name": type(schedule).__qualname__,
    }
    for name in ("start", "end", "end_fraction", "val", "value_schedule"):
        if hasattr(schedule, name):
            value = getattr(schedule, name)
            if callable(value):
                descriptor[name] = _schedule_descriptor(value)
            elif isinstance(value, (int, float, str, bool)) or value is None:
                descriptor[name] = value
            else:
                descriptor[name] = repr(value)
    return descriptor


def _optimizer_learning_rates(model: Any) -> list[float]:
    return [float(group["lr"]) for group in model.policy.optimizer.param_groups]


def scientific_continuation_components(
    adapter: SB3ScientificStateAdapter,
) -> Mapping[str, Any]:
    """Describe all continuation-relevant state and frozen derivation invariants.

    ``historical_learner_state_sha256`` is the physically recorded Phase-A
    identity.  The remaining fields are a DEC-053 audit/round-trip identity;
    they were not physically recorded during the original Phase-A run.
    """

    if not isinstance(adapter, SB3ScientificStateAdapter):
        raise TypeError("scientific continuation identity requires the project SB3 adapter")
    adapter._validate_boundary()
    model = adapter.model
    parameters = model.get_parameters()
    progress = float(model._current_progress_remaining)
    configured_learning_rate = float(adapter.configuration["learning_rate"])
    scheduled_learning_rate = float(model.lr_schedule(progress))
    optimizer_learning_rates = _optimizer_learning_rates(model)
    common_invariants = {
        "cpu_device": str(model.device) == "cpu",
        "single_environment": int(model.n_envs) == 1,
        "no_vec_normalization": model._vec_normalize_env is None,
        "configuration_is_finite_json": adapter.configuration
        == json.loads(json.dumps(adapter.configuration, allow_nan=False, sort_keys=True)),
        "constant_learning_rate_matches_configuration": scheduled_learning_rate
        == configured_learning_rate,
        "optimizer_learning_rate_matches_schedule": all(
            value == scheduled_learning_rate for value in optimizer_learning_rates
        ),
    }
    components: dict[str, Any] = {
        "schema_version": SCIENTIFIC_CONTINUATION_IDENTITY_SCHEMA_VERSION,
        "identity_name": "dec-053-derived-scientific-continuation-v1",
        "historical_learner_state_sha256": adapter.state_sha256(),
        "method_id": adapter.method_id,
        "provenance": adapter.provenance.__dict__,
        "configuration": adapter.configuration,
        "policy_state_sha256": _state_dict_digest(parameters["policy"]),
        "optimizer_state_sha256": _state_dict_digest(parameters["policy.optimizer"]),
        "counters": {
            "num_timesteps": int(model.num_timesteps),
            "n_updates": int(model._n_updates),
            "current_progress_remaining": progress,
            "total_timesteps": int(model._total_timesteps),
            "n_envs": int(model.n_envs),
        },
        "learning_rate_schedule": _schedule_descriptor(model.lr_schedule),
        "learning_rate_at_current_progress": scheduled_learning_rate,
        "optimizer_learning_rates": optimizer_learning_rates,
        "rng_state_sha256": _digest_value(adapter._rng_state),
        "action_space_rng_state_sha256": _digest_value(
            adapter._action_space_rng_state
        ),
        "invariants": common_invariants,
    }

    if adapter.method_id == "dqn":
        replay = model.replay_buffer
        unit = getattr(model.train_freq.unit, "value", model.train_freq.unit)
        exploration_at_progress = float(model.exploration_schedule(progress))
        components.update(
            {
                "online_network_sha256": _state_dict_digest(
                    model.q_net.state_dict()
                ),
                "target_network_sha256": _state_dict_digest(
                    model.q_net_target.state_dict()
                ),
                "replay_scientific_state_sha256": _digest_value(
                    _replay_fingerprint(model)
                ),
                "replay_operational_state": {
                    "class_module": type(replay).__module__,
                    "class_name": type(replay).__qualname__,
                    "buffer_size": int(replay.buffer_size),
                    "pos": int(replay.pos),
                    "full": bool(replay.full),
                    "n_envs": int(replay.n_envs),
                    "optimize_memory_usage": bool(model.optimize_memory_usage),
                    "handle_timeout_termination": bool(
                        replay.handle_timeout_termination
                    ),
                },
                "target_and_schedule_state": {
                    "n_calls": int(model._n_calls),
                    "target_update_interval": int(model.target_update_interval),
                    "tau": float(model.tau),
                    "train_frequency": int(model.train_freq.frequency),
                    "train_frequency_unit": str(unit),
                    "gradient_steps": int(model.gradient_steps),
                    "learning_starts": int(model.learning_starts),
                    "exploration_rate": float(model.exploration_rate),
                    "exploration_schedule": _schedule_descriptor(
                        model.exploration_schedule
                    ),
                    "exploration_at_current_progress": exploration_at_progress,
                },
            }
        )
        common_invariants.update(
            {
                # With n_envs=1, fresh construction, and one _on_step call per
                # environment step, this omitted historical counter is exactly
                # determined by the retained num_timesteps value.
                "dqn_n_calls_equals_num_timesteps": int(model._n_calls)
                == int(model.num_timesteps),
                "dqn_step_train_frequency": str(unit) == "step",
                "dqn_exploration_matches_frozen_schedule": float(
                    model.exploration_rate
                )
                == exploration_at_progress,
                "dqn_no_memory_optimized_replay": model.optimize_memory_usage
                is False,
                "dqn_timeout_termination_is_explicit": replay.handle_timeout_termination
                is True,
                "dqn_no_action_noise": model.action_noise is None,
                "dqn_no_sde": model.use_sde is False,
                "dqn_model_matches_frozen_configuration": (
                    float(model.gamma)
                    == float(adapter.configuration["discount_factor"])
                    and int(model.buffer_size)
                    == int(adapter.configuration["buffer_size"])
                    and int(model.learning_starts)
                    == int(adapter.configuration["learning_starts"])
                    and int(model.batch_size)
                    == int(adapter.configuration["batch_size"])
                    and int(model.train_freq.frequency)
                    == int(adapter.configuration["train_freq"])
                    and int(model.gradient_steps)
                    == int(adapter.configuration["gradient_steps"])
                    and int(model.target_update_interval)
                    == int(adapter.configuration["target_update_interval"])
                    and float(model.exploration_fraction)
                    == float(adapter.configuration["exploration_fraction"])
                    and float(model.exploration_initial_eps)
                    == float(adapter.configuration["exploration_initial_eps"])
                    and float(model.exploration_final_eps)
                    == float(adapter.configuration["exploration_final_eps"])
                    and float(model.tau) == 1.0
                    and int(model.n_steps) == 1
                ),
            }
        )
    else:
        rollout = model.rollout_buffer
        boundary = (
            "initial"
            if int(model.num_timesteps) == 0
            else "completed-update"
        )
        clip_vf = (
            None
            if model.clip_range_vf is None
            else float(model.clip_range_vf(progress))
        )
        components.update(
            {
                "ppo_boundary_state": {
                    "boundary": boundary,
                    "rollout_buffer_size": int(rollout.buffer_size),
                    "rollout_pos": int(rollout.pos),
                    "rollout_full": bool(rollout.full),
                    "n_steps": int(model.n_steps),
                    "n_epochs": int(model.n_epochs),
                    "batch_size": int(model.batch_size),
                },
                "ppo_schedule_state": {
                    "clip_range": _schedule_descriptor(model.clip_range),
                    "clip_range_at_current_progress": float(
                        model.clip_range(progress)
                    ),
                    "clip_range_vf_at_current_progress": clip_vf,
                },
            }
        )
        common_invariants.update(
            {
                "ppo_legal_completed_boundary": (
                    int(model.num_timesteps) == 0
                    and int(rollout.pos) == 0
                    and not bool(rollout.full)
                )
                or (
                    bool(rollout.full)
                    and int(rollout.pos) == int(rollout.buffer_size)
                ),
                # OnPolicyAlgorithm.collect_rollouts() resets this buffer before
                # any next collection, so completed-buffer payload values cannot
                # affect continuation from the legal boundary.
                "ppo_completed_rollout_is_consumed_before_checkpoint": int(
                    model.num_timesteps
                )
                == 0
                or (
                    bool(rollout.full)
                    and int(rollout.pos) == int(rollout.buffer_size)
                ),
                "ppo_no_sde": model.use_sde is False,
                "ppo_no_action_noise": model.action_noise is None,
                "ppo_model_matches_frozen_configuration": (
                    float(model.gamma)
                    == float(adapter.configuration["discount_factor"])
                    and int(model.n_steps) == int(adapter.configuration["n_steps"])
                    and int(model.batch_size)
                    == int(adapter.configuration["batch_size"])
                    and int(model.n_epochs) == int(adapter.configuration["n_epochs"])
                    and float(model.gae_lambda)
                    == float(adapter.configuration["gae_lambda"])
                    and float(model.clip_range(progress))
                    == float(adapter.configuration["clip_range"])
                    and float(model.ent_coef)
                    == float(adapter.configuration["ent_coef"])
                    and float(model.vf_coef)
                    == float(adapter.configuration["vf_coef"])
                    and float(model.max_grad_norm)
                    == float(adapter.configuration["max_grad_norm"])
                ),
            }
        )
    return components


def require_scientific_continuation_invariants(
    adapter: SB3ScientificStateAdapter,
) -> Mapping[str, Any]:
    components = scientific_continuation_components(adapter)
    failed = sorted(
        name for name, passed in components["invariants"].items() if passed is not True
    )
    if failed:
        raise ValueError(
            "SB3 scientific continuation invariants failed: " + ", ".join(failed)
        )
    return components


def scientific_continuation_sha256(adapter: SB3ScientificStateAdapter) -> str:
    """Return the DEC-053 derived audit identity, not an original Phase-A hash."""

    return _digest_value(require_scientific_continuation_invariants(adapter))


def _summary(value: Any) -> Mapping[str, Any]:
    if isinstance(value, str) and len(value) > 160:
        encoded = value.encode("utf-8")
        return {
            "kind": "long-string",
            "characters": len(value),
            "sha256": hashlib.sha256(encoded).hexdigest(),
        }
    return {"kind": type(value).__name__, "value": value}


def _json_differences(first: Any, second: Any, *, path: str = "") -> list[Mapping[str, Any]]:
    differences: list[Mapping[str, Any]] = []
    if isinstance(first, Mapping) and isinstance(second, Mapping):
        for key in sorted(set(first) | set(second)):
            child = f"{path}.{key}" if path else str(key)
            if key not in first or key not in second:
                differences.append(
                    {
                        "path": child,
                        "first": {"kind": "missing"}
                        if key not in first
                        else _summary(first[key]),
                        "second": {"kind": "missing"}
                        if key not in second
                        else _summary(second[key]),
                    }
                )
            else:
                differences.extend(
                    _json_differences(first[key], second[key], path=child)
                )
    elif isinstance(first, list) and isinstance(second, list):
        if len(first) != len(second):
            differences.append(
                {
                    "path": f"{path}.length",
                    "first": _summary(len(first)),
                    "second": _summary(len(second)),
                }
            )
        for index, (left, right) in enumerate(zip(first, second)):
            differences.extend(
                _json_differences(left, right, path=f"{path}[{index}]")
            )
    elif first != second:
        differences.append(
            {"path": path, "first": _summary(first), "second": _summary(second)}
        )
    return differences


def _classification(path: str) -> str:
    if path in {"start_time", "_num_timesteps_at_start"}:
        return "serialization-runtime-metadata-only"
    if path.startswith(("policy_class.", "replay_buffer_class.")) and not path.endswith(
        ":serialized:"
    ):
        return "serialization-human-readable-metadata-only"
    return "requires-scientific-review"


def diff_canonical_sb3_archives(
    first: bytes, second: bytes
) -> Mapping[str, Any]:
    """Return a deterministic member/data-field diff for canonical SB3 archives."""

    def read(value: bytes) -> Mapping[str, bytes]:
        with zipfile.ZipFile(io.BytesIO(value), "r") as archive:
            return {name: archive.read(name) for name in sorted(archive.namelist())}

    left = read(first)
    right = read(second)
    member_differences = []
    for name in sorted(set(left) | set(right)):
        left_value = left.get(name)
        right_value = right.get(name)
        if left_value == right_value:
            continue
        member_differences.append(
            {
                "path": name,
                "first_bytes": None if left_value is None else len(left_value),
                "second_bytes": None if right_value is None else len(right_value),
                "first_sha256": None
                if left_value is None
                else hashlib.sha256(left_value).hexdigest(),
                "second_sha256": None
                if right_value is None
                else hashlib.sha256(right_value).hexdigest(),
            }
        )
    data_differences: list[Mapping[str, Any]] = []
    if "data" in left and "data" in right and left["data"] != right["data"]:
        data_differences = [
            {**item, "classification": _classification(str(item["path"]))}
            for item in _json_differences(
                json.loads(left["data"]), json.loads(right["data"])
            )
        ]
    return {
        "schema_version": 1,
        "first_archive_sha256": hashlib.sha256(first).hexdigest(),
        "second_archive_sha256": hashlib.sha256(second).hexdigest(),
        "archives_equal": first == second,
        "member_differences": member_differences,
        "data_field_differences": data_differences,
    }
