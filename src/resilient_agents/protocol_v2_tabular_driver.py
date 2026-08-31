"""Protocol-v2 Phase-A drivers for project tabular/model-based learners.

Unlike the historical v1.x trainer, protocol-v2 keeps one persistent learner
state across episodes within a root. Environment episodes reset independently,
while the learner's Q/model/recency/RNG state is never reduced to a Q-only
checkpoint between episodes. Agent transition step indices are global actual
interaction indices so the strict project agents can continue across local
episode-step resets without resetting learner state.
"""
from __future__ import annotations

import math
from dataclasses import replace
from statistics import fmean
from typing import Any, Mapping, Sequence

from .contracts import ScenarioSpec, project_for_agent
from .environment import EnvironmentSeeds
from .gridworld import ACTION_NAMES, GridAction, GridWorldEnvironment
from .protocol_v2 import (
    NativeStateAdapter,
    ScientificStateAdapter,
    TabularQScientificStateAdapter,
)
from .protocol_v2_implementations import PROJECT_STATE_ADAPTER_VERSION
from .protocol_v2_runtime import ProbeResult, ProtocolV2RootIdentity
from .randomness import derive_scoped_seed

PROJECT_IMPLEMENTATION_ID = "project-protocol-v2-state-adapter"


def _episode_environment_seeds(
    root: ProtocolV2RootIdentity,
    *,
    scope: str,
    episode_index: int,
) -> EnvironmentSeeds:
    if episode_index < 0:
        raise ValueError("episode_index must be >= 0")
    child = f"{scope}:episode:{episode_index}"
    return EnvironmentSeeds(
        scenario=derive_scoped_seed(root.scenario_seed, child),
        environment=derive_scoped_seed(root.environment_seed, child),
        action_disturbance=derive_scoped_seed(root.action_disturbance_seed, child),
        observation_disturbance=derive_scoped_seed(
            root.observation_disturbance_seed, child
        ),
    )


def _agent_from_adapter(adapter: ScientificStateAdapter) -> Any:
    if isinstance(adapter, TabularQScientificStateAdapter):
        return adapter.agent
    if isinstance(adapter, NativeStateAdapter):
        return adapter.agent
    raise ValueError("unsupported project scientific-state adapter")


class ProjectTabularPhaseADriver:
    """Persistent Q/SARSA/Dyna-Q+ nominal-training driver."""

    implementation_id = PROJECT_IMPLEMENTATION_ID
    implementation_version = PROJECT_STATE_ADAPTER_VERSION

    def __init__(
        self,
        *,
        adapter: ScientificStateAdapter,
        scenario: ScenarioSpec,
        root: ProtocolV2RootIdentity,
    ) -> None:
        if adapter.method_id not in {"q_learning", "sarsa", "dyna_q_plus"}:
            raise ValueError("project Phase-A driver supports Q, SARSA or Dyna-Q+")
        if not isinstance(scenario, ScenarioSpec):
            raise ValueError("scenario must be ScenarioSpec")
        if not isinstance(root, ProtocolV2RootIdentity):
            raise ValueError("root must be ProtocolV2RootIdentity")
        self.state_adapter = adapter
        self.method_id = adapter.method_id
        self.scenario = scenario
        self.root = root
        self._agent = _agent_from_adapter(adapter)
        initial_state = adapter.export_state()
        if initial_state.get("initialized") is True:
            raise ValueError("Phase-A project driver requires a fresh uninitialized learner")
        self._agent.reset(
            initialization_seed=root.initialization_seed,
            exploration_seed=root.exploration_seed,
        )
        self._interactions = 0
        self._episode_index = 0
        self._environment: GridWorldEnvironment | None = None
        self._observation: Any = None
        self._episode_return = 0.0
        self._episode_length = 0

    @property
    def training_interactions(self) -> int:
        return self._interactions

    def _start_episode(self) -> None:
        if self._environment is not None:
            raise RuntimeError("cannot start a new episode while one is active")
        environment = GridWorldEnvironment(self.scenario)
        observation = environment.reset(
            seeds=_episode_environment_seeds(
                self.root,
                scope="protocol-v2-phase-a",
                episode_index=self._episode_index,
            )
        )
        self._environment = environment
        self._observation = observation
        self._episode_return = 0.0
        self._episode_length = 0

    def _finish_episode(self, *, outcome: str) -> None:
        if self._environment is None:
            raise RuntimeError("no active episode")
        self._agent.end_episode(
            {
                "episode_index": self._episode_index,
                "return": self._episode_return,
                "length": self._episode_length,
                "outcome": outcome,
                "global_training_interactions": self._interactions,
            }
        )
        self._environment.close()
        self._environment = None
        self._observation = None
        self._episode_index += 1

    def train_to_interaction(self, target_interaction: int) -> None:
        if (
            not isinstance(target_interaction, int)
            or isinstance(target_interaction, bool)
            or target_interaction < self._interactions
        ):
            raise ValueError("target_interaction must be an integer >= current interactions")
        while self._interactions < target_interaction:
            if self._environment is None:
                self._start_episode()
            if self._environment is None:
                raise RuntimeError("training environment was not initialized")
            action_name = self._agent.act(self._observation)
            if action_name not in ACTION_NAMES:
                raise ValueError("project learner returned an unknown action")
            truth = self._environment.step(int(GridAction[action_name.upper()]))
            visible = project_for_agent(truth, self._environment.information_policy)
            # Environment step numbers are episode-local; project learner
            # lifecycle state is root-global in protocol-v2.
            visible = replace(visible, step=self._interactions)
            self._agent.observe(visible)
            self._interactions += 1
            self._episode_return += float(truth.reward)
            self._episode_length += 1
            self._observation = truth.delivered_observation
            if truth.terminated or truth.truncated:
                self._finish_episode(
                    outcome="terminated" if truth.terminated else "truncated"
                )

        if self.training_interactions != target_interaction:
            raise RuntimeError("project Phase-A driver failed exact interaction target")

    def close(self) -> None:
        if self._environment is not None:
            self._environment.close()
            self._environment = None


class ProjectTabularNoLearningProbeEvaluator:
    """Greedy no-learning probes over the project agents' Q-valued policy state.

    The evaluator reads a cloned checkpoint and never calls the learner's
    ``observe`` method. Ties use the declared action order, giving a deterministic
    standardized inference rule independent of training exploration RNG.
    """

    def __init__(
        self,
        *,
        scenario: ScenarioSpec,
        environment_seeds: Sequence[EnvironmentSeeds],
    ) -> None:
        if not isinstance(scenario, ScenarioSpec):
            raise ValueError("scenario must be ScenarioSpec")
        seeds = tuple(environment_seeds)
        if not seeds or not all(isinstance(item, EnvironmentSeeds) for item in seeds):
            raise ValueError("environment_seeds must be explicit EnvironmentSeeds")
        self.scenario = scenario
        self.environment_seeds = seeds

    @staticmethod
    def _q_policy(adapter: ScientificStateAdapter) -> tuple[tuple[str, ...], float, dict[tuple[str, str], float]]:
        agent = _agent_from_adapter(adapter)
        checkpoint = agent.checkpoint()
        actions = tuple(str(item) for item in checkpoint["actions"])
        if actions != ACTION_NAMES:
            raise ValueError("probe requires canonical GridWorld action order")
        initial = float(checkpoint["initial_q_value"])
        q_values: dict[tuple[str, str], float] = {}
        for item in checkpoint["q_values"]:
            state_key = json_key(item["state"])
            action_key = str(item["action"])
            q_values[(state_key, action_key)] = float(item["value"])
        return actions, initial, q_values

    def __call__(
        self,
        adapter: ScientificStateAdapter,
        *,
        training_interaction_index: int,
        episodes: int,
    ) -> ProbeResult:
        if not isinstance(episodes, int) or isinstance(episodes, bool) or episodes <= 0:
            raise ValueError("episodes must be an integer > 0")
        if episodes > len(self.environment_seeds):
            raise ValueError("not enough predeclared probe environment seeds")
        actions, initial, q_values = self._q_policy(adapter)
        returns: list[float] = []
        lengths: list[int] = []
        terminated_count = 0
        truncated_count = 0
        interactions = 0

        for seeds in self.environment_seeds[:episodes]:
            env = GridWorldEnvironment(self.scenario)
            try:
                observation = env.reset(seeds=seeds)
                total = 0.0
                length = 0
                while True:
                    state_key = json_key(observation)
                    values = [q_values.get((state_key, action), initial) for action in actions]
                    best = max(values)
                    # Stable declared action-order tie rule for standardized probes.
                    action_name = next(
                        action
                        for action, value in zip(actions, values, strict=True)
                        if value == best
                    )
                    truth = env.step(int(GridAction[action_name.upper()]))
                    reward = float(truth.reward)
                    if not math.isfinite(reward):
                        raise ValueError("probe reward must be finite")
                    total += reward
                    length += 1
                    interactions += 1
                    observation = truth.delivered_observation
                    if truth.terminated or truth.truncated:
                        terminated_count += int(truth.terminated)
                        truncated_count += int(truth.truncated)
                        break
                returns.append(total)
                lengths.append(length)
            finally:
                env.close()

        return ProbeResult(
            training_interaction_index=training_interaction_index,
            probe_environment_interactions=interactions,
            episodes=episodes,
            metrics={
                "return_mean": float(fmean(returns)),
                "episode_length_mean": float(fmean(lengths)),
                "terminated_rate": terminated_count / episodes,
                "truncated_rate": truncated_count / episodes,
            },
        )


def json_key(value: Any) -> str:
    import json

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
