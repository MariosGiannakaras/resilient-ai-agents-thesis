"""Read-only live telemetry for application-run GridWorld experiments.

This module is intentionally outside the agent information path.  The observer
receives evaluator-visible copies only *after* the environment transition and
after the projected transition has been delivered to the agent.  It never owns
or consumes experiment RNGs and cannot alter actions, rewards or checkpoints.

The application/runtime service may tail the NDJSON sink for smooth GridWorld
and chart updates.  Scientific retention remains controlled independently by
the run bundle's RetentionPolicy; live telemetry is operational/provisional,
not final evidence.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from threading import Lock
from typing import Any, Mapping

from .contracts import RetentionPolicy, ScenarioSpec, project_for_agent
from .environment import EnvironmentSeeds
from .gridworld import ACTION_NAMES, GridAction, GridWorldEnvironment
from .randomness import RandomStreams, derive_scoped_seed
from .v11_candidate_runner import V11CandidateExperimentRunner
from .v11_runner import V11ExperimentRunner

RUNTIME_TELEMETRY_SCHEMA_VERSION = 1


class RuntimeTelemetrySink:
    """Append-only NDJSON sink with one process-local writer lock."""

    def __init__(self, path: Path) -> None:
        if not isinstance(path, Path):
            raise ValueError("telemetry path must be pathlib.Path")
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._sequence = 0

    def emit(self, payload: Mapping[str, Any]) -> None:
        if not isinstance(payload, Mapping):
            raise ValueError("runtime telemetry payload must be an object")
        row = {
            "runtime_telemetry_schema_version": RUNTIME_TELEMETRY_SCHEMA_VERSION,
            "sequence": self._sequence,
            **dict(payload),
        }
        encoded = json.dumps(
            row,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        with self._lock:
            with self.path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(encoded + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._sequence += 1


class _ObservedEpisodeMixin:
    """Mixin that mirrors the accepted episode loop and emits copied telemetry."""

    runtime_telemetry_sink: RuntimeTelemetrySink | None

    def _emit_runtime(self, payload: Mapping[str, Any]) -> None:
        sink = self.runtime_telemetry_sink
        if sink is not None:
            sink.emit(payload)

    def _run_episode(
        self,
        *,
        bundle: Any,
        agent: Any,
        scenario: ScenarioSpec,
        root_seed: int,
        scope: str,
        phase: str,
        branch: str,
        agent_id: str,
        episode_index: int,
        agent_seeds: Mapping[str, int],
    ) -> tuple[float, int, str]:
        streams = RandomStreams(derive_scoped_seed(root_seed, scope)).derived_seeds()
        environment = GridWorldEnvironment(scenario)
        observation = environment.reset(
            seeds=EnvironmentSeeds(
                scenario=streams["scenario"],
                environment=streams["environment"],
                action_disturbance=streams["action_disturbance"],
                observation_disturbance=streams["observation_disturbance"],
            )
        )
        debug = dict(environment.debug_state())
        self._emit_runtime(
            {
                "event": "episode_started",
                "run_id": self.request.run_id,
                "root_seed": root_seed,
                "agent_id": agent_id,
                "branch": branch,
                "phase": phase,
                "episode_index": episode_index,
                "scenario_id": scenario.scenario_id,
                "grid": {
                    "width": int(scenario.initial_state_spec["grid"]["width"]),
                    "height": int(scenario.initial_state_spec["grid"]["height"]),
                    "start": list(debug["position"]),
                    "goal": list(debug["goal"]),
                    "obstacles": [list(item) for item in debug["obstacles"]],
                },
                "delivered_observation": list(observation),
            }
        )
        total_reward = 0.0
        length = 0
        outcome = "invalid"
        try:
            while True:
                self._check_deadline()
                action_name = agent.act(observation)
                if action_name not in ACTION_NAMES:
                    raise ValueError("agent returned an unknown action")
                transition = environment.step(int(GridAction[action_name.upper()]))
                # The agent receives only the policy-projected transition first.
                agent.observe(project_for_agent(transition, environment.information_policy))
                total_reward += float(transition.reward)
                length += 1

                # Live telemetry is an evaluator/read-only copy.  Nothing from
                # this callback is ever fed back into agent/environment state.
                self._emit_runtime(
                    {
                        "event": "gridworld_step",
                        "run_id": self.request.run_id,
                        "root_seed": root_seed,
                        "agent_id": agent_id,
                        "branch": branch,
                        "phase": phase,
                        "episode_index": episode_index,
                        "scenario_id": scenario.scenario_id,
                        "step": int(transition.step),
                        "true_state": list(transition.true_state),
                        "delivered_observation": list(transition.delivered_observation),
                        "intended_action": transition.intended_action,
                        "executed_action": transition.executed_action,
                        "reward": float(transition.reward),
                        "terminated": bool(transition.terminated),
                        "truncated": bool(transition.truncated),
                        "regime_id": transition.regime_id,
                        "disturbance_flags": dict(transition.disturbance_flags),
                        "change_event_ids": list(transition.change_event_ids),
                        "cumulative_episode_return": total_reward,
                    }
                )

                if self.request.retention_policy is RetentionPolicy.FULL_TRACE:
                    bundle.append_trace(
                        {
                            "root_seed": root_seed,
                            "agent_id": agent_id,
                            "branch": branch,
                            "phase": phase,
                            "episode_index": episode_index,
                            "transition": asdict(transition),
                        }
                    )
                observation = transition.delivered_observation
                if transition.terminated or transition.truncated:
                    outcome = "terminated" if transition.terminated else "truncated"
                    break
            agent.end_episode(
                {
                    "episode_index": episode_index,
                    "return": total_reward,
                    "length": length,
                    "outcome": outcome,
                }
            )
        finally:
            environment.close()

        bundle.append_event(
            {
                "event": "episode_completed",
                "root_seed": root_seed,
                "agent_id": agent_id,
                "branch": branch,
                "phase": phase,
                "episode_index": episode_index,
                "return": total_reward,
                "length": length,
                "outcome": outcome,
                "scenario_id": scenario.scenario_id,
                "agent_initialization_seed": agent_seeds["agent_initialization"],
                "agent_exploration_seed": agent_seeds["agent_exploration"],
                "environment_seeds": {
                    "scenario": streams["scenario"],
                    "environment": streams["environment"],
                    "action_disturbance": streams["action_disturbance"],
                    "observation_disturbance": streams["observation_disturbance"],
                },
            }
        )
        self._emit_runtime(
            {
                "event": "episode_completed",
                "run_id": self.request.run_id,
                "root_seed": root_seed,
                "agent_id": agent_id,
                "branch": branch,
                "phase": phase,
                "episode_index": episode_index,
                "scenario_id": scenario.scenario_id,
                "return": total_reward,
                "length": length,
                "outcome": outcome,
            }
        )
        return total_reward, length, outcome


class ObservedV11DevelopmentRunner(_ObservedEpisodeMixin, V11ExperimentRunner):
    """Small development runner used to prove observer non-interference."""

    def __init__(self, *args: Any, runtime_telemetry_sink: RuntimeTelemetrySink, **kwargs: Any) -> None:
        self.runtime_telemetry_sink = runtime_telemetry_sink
        super().__init__(*args, **kwargs)


class ObservedV11CandidateRunner(_ObservedEpisodeMixin, V11CandidateExperimentRunner):
    """Application execution runner for protocol-approved v1.1 candidates."""

    def __init__(self, *args: Any, runtime_telemetry_sink: RuntimeTelemetrySink, **kwargs: Any) -> None:
        self.runtime_telemetry_sink = runtime_telemetry_sink
        super().__init__(*args, **kwargs)


__all__ = [
    "ObservedV11CandidateRunner",
    "ObservedV11DevelopmentRunner",
    "RUNTIME_TELEMETRY_SCHEMA_VERSION",
    "RuntimeTelemetrySink",
]
