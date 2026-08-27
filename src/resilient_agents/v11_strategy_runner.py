"""Development-only runner proving the DEC-047 five-strategy surface.

This module intentionally does not freeze protocol-v1.1.  It extends the
validated T-520 development adapter so SARSA and plain Dyna-Q can be exercised
through the same headless runner/information/seed contracts before T-521 owns
the authoritative candidate protocol schema.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contracts import ProtocolStage, RetentionPolicy
from .dyna_q import DynaQConfig
from .dyna_q_deployment import DynaQDeploymentAgent
from .experiment_runner import HeadlessExperimentRequest
from .gridworld import ACTION_NAMES
from .pilot_protocol import PilotProtocol
from .protocol import assert_stage_access
from .randomness import RandomStreams, derive_scoped_seed
from .sarsa import SarsaConfig
from .sarsa_deployment import SarsaDeploymentAgent
from .v11_runner import (
    V11DevelopmentProtocol,
    V11ExperimentRequest,
    V11ExperimentRunner,
    _positive_integer,
    _probability,
    _seed_sequence,
)

BROADENED_V11_RUNNER_SCHEMA_VERSION = 2
MAIN_STRATEGY_IDS = ("f0", "c0", "s0", "dq0", "d0")


class BroadenedV11DevelopmentProtocol(V11DevelopmentProtocol):
    """Development-only declaration for the five DEC-047 strategies."""

    @classmethod
    def from_validated_base(cls, base: PilotProtocol) -> "BroadenedV11DevelopmentProtocol":
        initial = super().from_validated_base(base)
        payload = initial.to_dict()
        historical = {
            str(item["agent_id"]): dict(item)
            for item in payload.get("agent_regimes", [])
            if isinstance(item, Mapping) and "agent_id" in item
        }
        if not {"f0", "c0", "d0"}.issubset(historical):
            raise ValueError("development base is missing f0/c0/d0 declarations")
        payload["agent_regimes"] = [
            historical["f0"],
            historical["c0"],
            {
                "agent_id": "s0",
                "method": "sarsa_v1",
                "user_facing_name": "SARSA",
                "checkpoint_source": "development-common-nominal-q-checkpoint",
                "post_change_learning": True,
                "deployment_exploration": "explicit-request-epsilon",
                "method_configuration": {
                    "learning_rate_policy": "explicit-development-request",
                    "discount_policy": "explicit-development-request",
                    "bootstrap_on_truncation": False,
                    "initial_q_value": 0.0,
                },
            },
            {
                "agent_id": "dq0",
                "method": "dyna_q_v1",
                "user_facing_name": "Dyna-Q",
                "checkpoint_source": "development-common-nominal-q-checkpoint",
                "post_change_learning": True,
                "deployment_exploration": "explicit-request-epsilon",
                "method_configuration": {
                    "learning_rate_policy": "explicit-development-request",
                    "discount_policy": "explicit-development-request",
                    "bootstrap_on_truncation": False,
                    "initial_q_value": 0.0,
                    "planning_steps_policy": "explicit-development-request",
                    "recency_bonus": "disabled",
                },
            },
            historical["d0"],
        ]
        canonical = json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        return cls(canonical)


@dataclass(frozen=True)
class BroadenedV11ExperimentRequest(V11ExperimentRequest):
    """Development request allowing the five DEC-047 strategy IDs."""

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "BroadenedV11ExperimentRequest":
        if not isinstance(payload, Mapping):
            raise ValueError("broadened v1.1 experiment request must be an object")
        expected = {
            "run_id", "stage", "layout_id", "condition_id", "root_seeds",
            "agent_ids", "q_learning_rate", "discount_factor",
            "exploration_epsilon", "training_episodes_per_layout",
            "pre_change_episodes", "post_change_episodes", "immediate_window",
            "worst_window", "terminal_window", "recovery_tolerance",
            "recovery_stability_episodes", "retention_policy", "auto_publish",
            "execution_timeout_seconds", "dyna_planning_steps", "dyna_kappa",
        }
        if set(payload) != expected:
            raise ValueError(
                "broadened v1.1 request keys mismatch; "
                f"missing={sorted(expected - set(payload))}, "
                f"unknown={sorted(set(payload) - expected)}"
            )
        try:
            values = dict(payload)
            values["stage"] = ProtocolStage(values["stage"])
            values["retention_policy"] = RetentionPolicy(values["retention_policy"])
            return cls(**values)
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid broadened v1.1 experiment request") from exc

    def __post_init__(self) -> None:
        if not isinstance(self.run_id, str) or not self.run_id.strip():
            raise ValueError("run_id must be non-empty")
        if Path(self.run_id).name != self.run_id:
            raise ValueError("run_id must not contain path components")
        if not isinstance(self.stage, ProtocolStage):
            raise ValueError("stage must be ProtocolStage")
        if not isinstance(self.layout_id, str) or not self.layout_id.strip():
            raise ValueError("layout_id must be non-empty")
        if not isinstance(self.condition_id, str) or not self.condition_id.strip():
            raise ValueError("condition_id must be non-empty")

        seeds = _seed_sequence(self.root_seeds, field="root_seeds")
        agents = tuple(self.agent_ids)
        allowed = set(MAIN_STRATEGY_IDS)
        if (
            not agents
            or len(set(agents)) != len(agents)
            or any(agent not in allowed for agent in agents)
        ):
            raise ValueError(
                "agent_ids must be a unique non-empty subset of "
                "f0/c0/s0/dq0/d0"
            )

        _probability(self.q_learning_rate, field="q_learning_rate", allow_one=True)
        _probability(self.discount_factor, field="discount_factor")
        _probability(
            self.exploration_epsilon, field="exploration_epsilon", allow_one=True
        )
        for field in (
            "training_episodes_per_layout", "pre_change_episodes",
            "post_change_episodes", "immediate_window", "worst_window",
            "terminal_window", "recovery_stability_episodes",
        ):
            _positive_integer(getattr(self, field), field=field)
        if (
            not isinstance(self.recovery_tolerance, (int, float))
            or isinstance(self.recovery_tolerance, bool)
            or not math.isfinite(float(self.recovery_tolerance))
            or float(self.recovery_tolerance) < 0.0
        ):
            raise ValueError("recovery_tolerance must be finite and non-negative")
        if not isinstance(self.retention_policy, RetentionPolicy):
            raise ValueError("retention_policy must be RetentionPolicy")
        if not isinstance(self.auto_publish, bool):
            raise ValueError("auto_publish must be boolean")
        if self.execution_timeout_seconds is not None and (
            not isinstance(self.execution_timeout_seconds, (int, float))
            or isinstance(self.execution_timeout_seconds, bool)
            or not math.isfinite(float(self.execution_timeout_seconds))
            or float(self.execution_timeout_seconds) <= 0.0
        ):
            raise ValueError("execution_timeout_seconds must be finite and positive")

        needs_planning = "dq0" in agents or "d0" in agents
        if needs_planning:
            _positive_integer(self.dyna_planning_steps, field="dyna_planning_steps")
        elif self.dyna_planning_steps is not None:
            raise ValueError("dyna_planning_steps requires dq0 or d0")

        if "d0" in agents:
            if (
                not isinstance(self.dyna_kappa, (int, float))
                or isinstance(self.dyna_kappa, bool)
                or not math.isfinite(float(self.dyna_kappa))
                or float(self.dyna_kappa) <= 0.0
            ):
                raise ValueError("dyna_kappa must be finite and > 0 when Dyna-Q+ is requested")
        elif self.dyna_kappa is not None:
            raise ValueError("dyna_kappa is only valid when Dyna-Q+ is requested")

        object.__setattr__(self, "root_seeds", seeds)
        object.__setattr__(self, "agent_ids", agents)


class BroadenedV11ExperimentRunner(V11ExperimentRunner):
    """Development runner for Fixed/Adaptive Q, SARSA, Dyna-Q and Dyna-Q+."""

    request: BroadenedV11ExperimentRequest

    def __init__(
        self,
        *,
        repo_root: Path,
        protocol: BroadenedV11DevelopmentProtocol,
        request: BroadenedV11ExperimentRequest,
        writable_root: Path | None = None,
    ) -> None:
        if not isinstance(protocol, BroadenedV11DevelopmentProtocol):
            raise ValueError("protocol must be BroadenedV11DevelopmentProtocol")
        if not isinstance(request, BroadenedV11ExperimentRequest):
            raise ValueError("request must be BroadenedV11ExperimentRequest")
        super().__init__(repo_root=repo_root, protocol=protocol, request=request, writable_root=writable_root)

    def _validate_request(self) -> None:
        assert_stage_access(
            stage=self.request.stage,
            scenario_ids=[self.request.layout_id],
            partition=self.protocol.partition(),
        )
        if self.request.condition_id not in self.protocol.condition_ids():
            raise ValueError("condition_id is not defined by the protocol")
        for field in (
            "immediate_window", "worst_window", "terminal_window",
            "recovery_stability_episodes",
        ):
            if getattr(self.request, field) > self.request.post_change_episodes:
                raise ValueError(f"{field} exceeds the post-change episode count")

        declared = {
            str(item["agent_id"]): item
            for item in self._payload.get("agent_regimes", [])
            if isinstance(item, Mapping) and "agent_id" in item
        }
        missing = set(self.request.agent_ids) - set(declared)
        if missing:
            raise ValueError(
                "requested agents are not declared by the protocol: "
                + ", ".join(sorted(missing))
            )
        expected_methods = {
            "s0": "sarsa_v1",
            "dq0": "dyna_q_v1",
            "d0": "dyna_q_plus_v1",
        }
        for agent_id, method in expected_methods.items():
            if agent_id in self.request.agent_ids and declared[agent_id].get("method") != method:
                raise ValueError(f"protocol {agent_id} must declare method {method}")
        if self.request.stage is not ProtocolStage.DEVELOPMENT:
            raise ValueError(
                "broadened v1.1 non-development execution is blocked until T-521"
            )

    def _resolved_config(self) -> dict[str, Any]:
        resolved = super()._resolved_config()
        resolved["headless_runner_schema_version"] = BROADENED_V11_RUNNER_SCHEMA_VERSION
        resolved["entrypoint"] = "resilient_agents.v11_strategy_runner.development-v1"
        resolved["agent_strategy_names"] = {
            "f0": "Fixed Q-Learning",
            "c0": "Adaptive Q-Learning",
            "s0": "SARSA",
            "dq0": "Dyna-Q",
            "d0": "Dyna-Q+",
        }
        return resolved

    def _sarsa_agent(self, *, checkpoint: Mapping[str, Any]) -> SarsaDeploymentAgent:
        return SarsaDeploymentAgent(
            SarsaConfig(
                agent_id="s0",
                actions=ACTION_NAMES,
                learning_rate=float(self.request.q_learning_rate),
                discount_factor=float(self.request.discount_factor),
                exploration_epsilon=float(self.request.exploration_epsilon),
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=dict(checkpoint),
        )

    def _plain_dyna_agent(self, *, checkpoint: Mapping[str, Any]) -> DynaQDeploymentAgent:
        if self.request.dyna_planning_steps is None:
            raise RuntimeError("Dyna-Q planning_steps were not resolved")
        return DynaQDeploymentAgent(
            DynaQConfig(
                agent_id="dq0",
                actions=ACTION_NAMES,
                learning_rate=float(self.request.q_learning_rate),
                discount_factor=float(self.request.discount_factor),
                exploration_epsilon=float(self.request.exploration_epsilon),
                planning_steps=int(self.request.dyna_planning_steps),
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=dict(checkpoint),
        )

    def _run_continual_branch(
        self,
        *,
        bundle: Any,
        root_seed: int,
        agent_id: str,
        agent: Any,
        branch: str,
    ) -> tuple[list[float], str]:
        if branch not in {"reference", "disrupted"}:
            raise ValueError("branch must be reference or disrupted")
        total = self.request.pre_change_episodes + self.request.post_change_episodes
        curve: list[float] = []
        for episode in range(total):
            self._check_deadline()
            after_change = episode >= self.request.pre_change_episodes
            condition_id = (
                self.request.condition_id
                if branch == "disrupted" and after_change
                else "nominal"
            )
            scenario = self._scenario(
                layout_id=self.request.layout_id,
                condition_id=condition_id,
            )
            seeds = RandomStreams(
                derive_scoped_seed(root_seed, f"evaluation-agent:{episode}")
            ).derived_seeds()
            if episode == 0:
                agent.start_branch(
                    initialization_seed=seeds["agent_initialization"],
                    exploration_seed=seeds["agent_exploration"],
                )
            else:
                agent.start_next_episode(
                    initialization_seed=seeds["agent_initialization"],
                    exploration_seed=seeds["agent_exploration"],
                )
            episode_return, _, _ = self._run_episode(
                bundle=bundle,
                agent=agent,
                scenario=scenario,
                root_seed=root_seed,
                scope=f"evaluation-environment:{episode}",
                phase="post-change" if after_change else "pre-change",
                branch=branch,
                agent_id=agent_id,
                episode_index=episode,
                agent_seeds=seeds,
            )
            curve.append(episode_return)
        return curve, agent.state_sha256()

    def _run_branch(
        self,
        *,
        bundle: Any,
        root_seed: int,
        agent_id: str,
        q_checkpoint: Mapping[str, Any],
        branch: str,
    ) -> tuple[list[float], str]:
        if agent_id == "s0":
            return self._run_continual_branch(
                bundle=bundle,
                root_seed=root_seed,
                agent_id=agent_id,
                agent=self._sarsa_agent(checkpoint=q_checkpoint),
                branch=branch,
            )
        if agent_id == "dq0":
            return self._run_continual_branch(
                bundle=bundle,
                root_seed=root_seed,
                agent_id=agent_id,
                agent=self._plain_dyna_agent(checkpoint=q_checkpoint),
                branch=branch,
            )
        return super()._run_branch(
            bundle=bundle,
            root_seed=root_seed,
            agent_id=agent_id,
            q_checkpoint=q_checkpoint,
            branch=branch,
        )


__all__ = [
    "BROADENED_V11_RUNNER_SCHEMA_VERSION",
    "MAIN_STRATEGY_IDS",
    "BroadenedV11DevelopmentProtocol",
    "BroadenedV11ExperimentRequest",
    "BroadenedV11ExperimentRunner",
]
