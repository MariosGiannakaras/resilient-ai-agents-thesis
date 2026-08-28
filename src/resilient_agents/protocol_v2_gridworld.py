"""Exact protocol-v2 scientific state for the project-owned GridWorld.

The historical GridWorld implementation stays unchanged.  This compatibility
layer owns the additional state needed to fork one pre-boundary trajectory into
matched protocol-v2 post-boundary branches.

Two identities are deliberately distinct:

* ``scenario_sha256`` identifies the exact source scenario.
* ``task_sha256`` identifies the common task/information contract while
  excluding post-boundary action/observation disturbances and change events.

That second identity permits one no-learning nominal prefix to be restored into
matched nominal/disturbed branch scenarios at the fork.  The target scenario's
uncertainty mechanisms then begin on the *next* environment interaction rather
than contaminating the shared prefix.
"""
from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict
from typing import Any, Mapping

from .contracts import GroundTruthTransition, ScenarioSpec
from .environment import EnvironmentSeeds
from .gridworld import (
    GridWorldEnvironment,
    gridworld_scenario_json,
    gridworld_scenario_to_dict,
)

GRIDWORLD_SCIENTIFIC_STATE_SCHEMA_VERSION = 1


def _canonical_json(value: Any, *, field: str) -> str:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be finite JSON-compatible data") from exc


def _sha256(value: Any, *, field: str) -> str:
    return hashlib.sha256(_canonical_json(value, field=field).encode("utf-8")).hexdigest()


def _list_rng_state(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_list_rng_state(item) for item in value]
    if isinstance(value, list):
        return [_list_rng_state(item) for item in value]
    return value


def _tuple_rng_state(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_tuple_rng_state(item) for item in value)
    return value


def _task_contract(spec: ScenarioSpec) -> Mapping[str, Any]:
    """Return the branch-compatible task contract, excluding forked mechanisms."""

    payload = gridworld_scenario_to_dict(spec)
    return {
        "gridworld_schema_version": payload["gridworld_schema_version"],
        "environment_id": payload["environment_id"],
        "max_steps": payload["max_steps"],
        "reward_spec": payload["reward_spec"],
        "initial_state_spec": payload["initial_state_spec"],
        "dynamics_spec": payload["dynamics_spec"],
        "observation_spec": payload["observation_spec"],
        "information_policy": payload["information_policy"],
    }


def gridworld_task_sha256(spec: ScenarioSpec) -> str:
    return _sha256(_task_contract(spec), field="GridWorld task contract")


def gridworld_scenario_sha256(spec: ScenarioSpec) -> str:
    return hashlib.sha256(gridworld_scenario_json(spec).encode("utf-8")).hexdigest()


def _transition_to_json(value: GroundTruthTransition | None) -> Mapping[str, Any] | None:
    if value is None:
        return None
    payload = asdict(value)
    payload["change_event_ids"] = list(value.change_event_ids)
    return payload


def _transition_from_json(value: Mapping[str, Any] | None) -> GroundTruthTransition | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError("last_transition must be an object or null")
    expected = {
        "step",
        "true_state",
        "delivered_observation",
        "intended_action",
        "executed_action",
        "reward",
        "terminated",
        "truncated",
        "regime_id",
        "disturbance_flags",
        "change_event_ids",
    }
    if set(value) != expected:
        raise ValueError("last_transition keys mismatch")
    true_state = tuple(value["true_state"]) if isinstance(value["true_state"], list) else value["true_state"]
    delivered = (
        tuple(value["delivered_observation"])
        if isinstance(value["delivered_observation"], list)
        else value["delivered_observation"]
    )
    return GroundTruthTransition(
        step=int(value["step"]),
        true_state=true_state,
        delivered_observation=delivered,
        intended_action=value["intended_action"],
        executed_action=value["executed_action"],
        reward=float(value["reward"]),
        terminated=bool(value["terminated"]),
        truncated=bool(value["truncated"]),
        regime_id=value["regime_id"],
        disturbance_flags=dict(value["disturbance_flags"]),
        change_event_ids=tuple(value["change_event_ids"]),
    )


class GridWorldScientificStateAdapter:
    """Capture, restore and fork exact GridWorld trajectory/RNG state."""

    def __init__(self, environment: GridWorldEnvironment) -> None:
        if not isinstance(environment, GridWorldEnvironment):
            raise ValueError("environment must be GridWorldEnvironment")
        self.environment = environment

    @property
    def spec(self) -> ScenarioSpec:
        return self.environment.gym_env.spec

    def export_state(self) -> Mapping[str, Any]:
        gym_env = self.environment.gym_env
        if gym_env._seeds is None or gym_env._action_rng is None or gym_env._observation_rng is None:
            raise RuntimeError("GridWorld must be reset before scientific state export")
        np_rng = getattr(gym_env, "np_random", None)
        state = {
            "schema_version": GRIDWORLD_SCIENTIFIC_STATE_SCHEMA_VERSION,
            "scenario_sha256": gridworld_scenario_sha256(self.spec),
            "task_sha256": gridworld_task_sha256(self.spec),
            "environment_id": gym_env.environment_id,
            "position": list(gym_env._position),
            "step": int(gym_env._step),
            "finished": bool(gym_env._finished),
            "seeds": asdict(gym_env._seeds),
            "action_rng_state": _list_rng_state(gym_env._action_rng.getstate()),
            "observation_rng_state": _list_rng_state(gym_env._observation_rng.getstate()),
            "gym_np_random_state": None
            if np_rng is None
            else json.loads(
                json.dumps(np_rng.bit_generator.state, sort_keys=True, separators=(",", ":"))
            ),
            "last_transition": _transition_to_json(gym_env.last_transition),
        }
        # Normalize tuples from transition coordinates before returning a portable state.
        return json.loads(_canonical_json(state, field="GridWorld scientific state"))

    def state_sha256(self) -> str:
        return _sha256(self.export_state(), field="GridWorld scientific state")

    def _validate_target(self, state: Mapping[str, Any], *, branch_compatible: bool) -> None:
        expected = {
            "schema_version",
            "scenario_sha256",
            "task_sha256",
            "environment_id",
            "position",
            "step",
            "finished",
            "seeds",
            "action_rng_state",
            "observation_rng_state",
            "gym_np_random_state",
            "last_transition",
        }
        if not isinstance(state, Mapping) or set(state) != expected:
            raise ValueError("invalid GridWorld scientific state keys")
        if state["schema_version"] != GRIDWORLD_SCIENTIFIC_STATE_SCHEMA_VERSION:
            raise ValueError("unsupported GridWorld scientific state schema_version")
        if state["environment_id"] != self.environment.gym_env.environment_id:
            raise ValueError("GridWorld environment_id mismatch")
        if branch_compatible:
            if state["task_sha256"] != gridworld_task_sha256(self.spec):
                raise ValueError("target scenario changes the common task contract")
            events = tuple(self.spec.change_events)
            if events and events[0].onset_step != int(state["step"]):
                raise ValueError(
                    "a branch action-remap event must start exactly at the restored fork step"
                )
        elif state["scenario_sha256"] != gridworld_scenario_sha256(self.spec):
            raise ValueError("GridWorld exact restore requires the same scenario")

    def restore_state(
        self,
        state: Mapping[str, Any],
        *,
        branch_compatible: bool = False,
    ) -> None:
        self._validate_target(state, branch_compatible=branch_compatible)
        gym_env = self.environment.gym_env
        seeds = EnvironmentSeeds(**dict(state["seeds"]))
        # Establish Gymnasium's own seeded internals before restoring the exact
        # project-owned trajectory/RNG channels.
        gym_env.reset(seed=seeds.environment, options={"environment_seeds": seeds})
        gym_env._seeds = seeds
        gym_env._position = tuple(state["position"])
        gym_env._step = int(state["step"])
        gym_env._finished = bool(state["finished"])
        gym_env._action_rng = random.Random()
        gym_env._action_rng.setstate(_tuple_rng_state(state["action_rng_state"]))
        gym_env._observation_rng = random.Random()
        gym_env._observation_rng.setstate(_tuple_rng_state(state["observation_rng_state"]))
        if state["gym_np_random_state"] is not None:
            gym_env.np_random.bit_generator.state = json.loads(
                _canonical_json(
                    state["gym_np_random_state"], field="Gymnasium NumPy RNG state"
                )
            )
        gym_env.last_transition = _transition_from_json(state["last_transition"])

    def clone(self) -> "GridWorldScientificStateAdapter":
        target = GridWorldEnvironment(self.spec)
        clone = GridWorldScientificStateAdapter(target)
        clone.restore_state(self.export_state())
        return clone

    def fork_into(self, target_spec: ScenarioSpec) -> "GridWorldScientificStateAdapter":
        """Restore a shared prefix into a matched post-boundary branch scenario."""

        target = GridWorldEnvironment(target_spec)
        fork = GridWorldScientificStateAdapter(target)
        fork.restore_state(self.export_state(), branch_compatible=True)
        return fork
