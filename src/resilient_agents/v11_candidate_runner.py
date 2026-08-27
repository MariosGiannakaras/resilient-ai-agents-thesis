"""Authoritative non-final runner for the protocol-v1.1 candidate.

The T-523 runner proved the five mechanisms with common development parameters.
This module binds every selected strategy to a protocol-approved configuration
ID/hash while keeping common nominal checkpoint training explicit.  Candidate
execution is limited to DEVELOPMENT/TUNING; FINAL remains fail-closed until the
protocol is frozen by T-522 and the later application/human gates are passed.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contracts import ProtocolStage, RetentionPolicy
from .dyna_deployment import DynaQPlusDeploymentAgent
from .dyna_q import DynaQConfig
from .dyna_q_deployment import DynaQDeploymentAgent
from .dyna_q_plus import DynaQPlusConfig
from .experiment_runner import HeadlessExperimentRequest, HeadlessExperimentRunner
from .gridworld import ACTION_NAMES
from .protocol import assert_stage_access
from .randomness import RandomStreams, derive_scoped_seed
from .sarsa import SarsaConfig
from .sarsa_deployment import SarsaDeploymentAgent
from .v11_protocol import V11CandidateProtocol, V11_STRATEGY_IDS
from .v11_runner import _positive_integer, _probability, _seed_sequence

V11_CANDIDATE_RUNNER_SCHEMA_VERSION = 1


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
        raise ValueError("candidate runner values must be finite JSON") from exc


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _configuration_map(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ValueError("agent_configuration_ids must be an object")
    result: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("agent_configuration_ids keys must be non-empty strings")
        if not isinstance(item, str) or not item.strip():
            raise ValueError("configuration IDs must be non-empty strings")
        result[key] = item
    return result


@dataclass(frozen=True)
class V11CandidateExperimentRequest(HeadlessExperimentRequest):
    """One protocol-approved v1.1 development/tuning experiment."""

    agent_configuration_ids: Mapping[str, str] | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "V11CandidateExperimentRequest":
        if not isinstance(payload, Mapping):
            raise ValueError("candidate v1.1 experiment request must be an object")
        expected = {
            "run_id", "stage", "layout_id", "condition_id", "root_seeds",
            "agent_ids", "q_learning_rate", "discount_factor",
            "exploration_epsilon", "training_episodes_per_layout",
            "pre_change_episodes", "post_change_episodes", "immediate_window",
            "worst_window", "terminal_window", "recovery_tolerance",
            "recovery_stability_episodes", "retention_policy", "auto_publish",
            "execution_timeout_seconds", "agent_configuration_ids",
        }
        if set(payload) != expected:
            raise ValueError(
                "candidate v1.1 request keys mismatch; "
                f"missing={sorted(expected-set(payload))}, "
                f"unknown={sorted(set(payload)-expected)}"
            )
        values = dict(payload)
        try:
            values["stage"] = ProtocolStage(values["stage"])
            values["retention_policy"] = RetentionPolicy(values["retention_policy"])
            return cls(**values)
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid candidate v1.1 experiment request") from exc

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
        if (
            not agents
            or len(set(agents)) != len(agents)
            or any(agent not in V11_STRATEGY_IDS for agent in agents)
        ):
            raise ValueError("agent_ids must be a unique non-empty subset of f0/c0/s0/dq0/d0")
        configurations = _configuration_map(self.agent_configuration_ids)
        if set(configurations) != set(agents):
            raise ValueError("agent_configuration_ids must exactly cover selected agent_ids")

        _probability(self.q_learning_rate, field="q_learning_rate", allow_one=True)
        _probability(self.discount_factor, field="discount_factor")
        _probability(self.exploration_epsilon, field="exploration_epsilon", allow_one=True)
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
        object.__setattr__(self, "root_seeds", seeds)
        object.__setattr__(self, "agent_ids", agents)
        object.__setattr__(self, "agent_configuration_ids", configurations)

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()
        payload["agent_configuration_ids"] = dict(self.agent_configuration_ids or {})
        return payload


class V11CandidateExperimentRunner(HeadlessExperimentRunner):
    """Execute protocol-approved candidate configurations without final access."""

    protocol: V11CandidateProtocol
    request: V11CandidateExperimentRequest

    def __init__(
        self,
        *,
        repo_root: Path,
        protocol: V11CandidateProtocol,
        request: V11CandidateExperimentRequest,
    ) -> None:
        if not isinstance(protocol, V11CandidateProtocol):
            raise ValueError("protocol must be V11CandidateProtocol")
        if not isinstance(request, V11CandidateExperimentRequest):
            raise ValueError("request must be V11CandidateExperimentRequest")
        super().__init__(repo_root=repo_root, protocol=protocol, request=request)

    def _validate_request(self) -> None:
        self.protocol.assert_execution_allowed(self.request.stage)
        assert_stage_access(
            stage=self.request.stage,
            scenario_ids=[self.request.layout_id],
            partition=self.protocol.partition(),
        )
        if self.request.condition_id not in self.protocol.condition_ids():
            raise ValueError("condition_id is not defined by protocol-v1.1")
        for field in (
            "immediate_window", "worst_window", "terminal_window",
            "recovery_stability_episodes",
        ):
            if getattr(self.request, field) > self.request.post_change_episodes:
                raise ValueError(f"{field} exceeds the post-change episode count")

        payload = self.protocol.to_dict()
        checkpoint = payload["checkpoint_training"]
        expected_checkpoint = {
            "q_learning_rate": checkpoint["learning_rate"],
            "discount_factor": checkpoint["discount_factor"],
            "exploration_epsilon": checkpoint["exploration_epsilon"],
            "training_episodes_per_layout": checkpoint["training_episodes_per_layout"],
        }
        for field, expected in expected_checkpoint.items():
            if getattr(self.request, field) != expected:
                raise ValueError(f"{field} must match the protocol-v1.1 common checkpoint budget")
        if self.request.pre_change_episodes != 16 or self.request.post_change_episodes != 32:
            raise ValueError("candidate v1.1 experiments use the predeclared 16/32 evaluation blocks")

        expected_roots = self.protocol.root_seeds_for(self.request.stage)
        if tuple(self.request.root_seeds) != expected_roots:
            raise ValueError("approved candidate experiments must use the complete predeclared stage root bank")
        if self.request.stage is ProtocolStage.TUNING:
            if self.request.condition_id not in payload["tuning"]["condition_ids"]:
                raise ValueError("tuning condition is outside the bounded predeclared tuning design")

        for agent_id in self.request.agent_ids:
            configuration_id = (self.request.agent_configuration_ids or {})[agent_id]
            configuration = self.protocol.configuration(configuration_id)
            if configuration["agent_id"] != agent_id:
                raise ValueError("configuration ID does not belong to its selected agent")
            if self.request.stage is ProtocolStage.TUNING and configuration_id not in self.protocol.candidate_configuration_ids(agent_id):
                raise ValueError("configuration ID is outside the protocol-approved tuning surface")
            if self.request.stage is ProtocolStage.DEVELOPMENT and configuration_id not in payload["development"]["allowed_configuration_ids"]:
                raise ValueError("configuration ID is outside the approved development surface")

        if self.request.retention_policy is not RetentionPolicy.EVENTS:
            raise ValueError("candidate v1.1 requires events plus persisted episode curves")

    def _configuration(self, agent_id: str) -> tuple[str, dict[str, Any]]:
        configuration_id = (self.request.agent_configuration_ids or {})[agent_id]
        return configuration_id, self.protocol.configuration(configuration_id)

    def _resolved_config(self) -> dict[str, Any]:
        resolved = super()._resolved_config()
        identities: dict[str, Any] = {}
        for agent_id in self.request.agent_ids:
            configuration_id, configuration = self._configuration(agent_id)
            identities[agent_id] = {
                "configuration_id": configuration_id,
                "configuration_sha256": self.protocol.configuration_sha256(configuration_id),
                "configuration": configuration,
            }
        resolved["v11_candidate_runner_schema_version"] = V11_CANDIDATE_RUNNER_SCHEMA_VERSION
        resolved["entrypoint"] = "resilient_agents.v11_candidate_runner.v1"
        resolved["protocol_sha256"] = self.protocol.protocol_sha256()
        resolved["protocol_lifecycle"] = "candidate-non-final"
        resolved["agent_configuration_identities"] = identities
        resolved["configuration_set_sha256"] = _sha256(identities)
        return resolved

    @staticmethod
    def _settings(configuration: Mapping[str, Any]) -> Mapping[str, Any]:
        settings = configuration.get("settings")
        if not isinstance(settings, Mapping):
            raise RuntimeError("validated configuration settings are missing")
        return settings

    def _sarsa_agent(self, *, checkpoint: Mapping[str, Any]) -> SarsaDeploymentAgent:
        _, configuration = self._configuration("s0")
        settings = self._settings(configuration)
        return SarsaDeploymentAgent(
            SarsaConfig(
                agent_id="s0",
                actions=ACTION_NAMES,
                learning_rate=float(settings["learning_rate"]),
                discount_factor=float(settings["discount_factor"]),
                exploration_epsilon=float(settings["exploration_epsilon"]),
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=dict(checkpoint),
        )

    def _dyna_q_agent(self, *, checkpoint: Mapping[str, Any]) -> DynaQDeploymentAgent:
        _, configuration = self._configuration("dq0")
        settings = self._settings(configuration)
        return DynaQDeploymentAgent(
            DynaQConfig(
                agent_id="dq0",
                actions=ACTION_NAMES,
                learning_rate=float(settings["learning_rate"]),
                discount_factor=float(settings["discount_factor"]),
                exploration_epsilon=float(settings["exploration_epsilon"]),
                planning_steps=int(settings["planning_steps"]),
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=dict(checkpoint),
        )

    def _dyna_q_plus_agent(self, *, checkpoint: Mapping[str, Any]) -> DynaQPlusDeploymentAgent:
        _, configuration = self._configuration("d0")
        settings = self._settings(configuration)
        return DynaQPlusDeploymentAgent(
            DynaQPlusConfig(
                agent_id="d0",
                actions=ACTION_NAMES,
                learning_rate=float(settings["learning_rate"]),
                discount_factor=float(settings["discount_factor"]),
                exploration_epsilon=float(settings["exploration_epsilon"]),
                planning_steps=int(settings["planning_steps"]),
                kappa=float(settings["kappa"]),
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
            scenario = self._scenario(layout_id=self.request.layout_id, condition_id=condition_id)
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
                bundle=bundle, root_seed=root_seed, agent_id=agent_id,
                agent=self._sarsa_agent(checkpoint=q_checkpoint), branch=branch,
            )
        if agent_id == "dq0":
            return self._run_continual_branch(
                bundle=bundle, root_seed=root_seed, agent_id=agent_id,
                agent=self._dyna_q_agent(checkpoint=q_checkpoint), branch=branch,
            )
        if agent_id == "d0":
            return self._run_continual_branch(
                bundle=bundle, root_seed=root_seed, agent_id=agent_id,
                agent=self._dyna_q_plus_agent(checkpoint=q_checkpoint), branch=branch,
            )
        return super()._run_branch(
            bundle=bundle,
            root_seed=root_seed,
            agent_id=agent_id,
            q_checkpoint=q_checkpoint,
            branch=branch,
        )


__all__ = [
    "V11_CANDIDATE_RUNNER_SCHEMA_VERSION",
    "V11CandidateExperimentRequest",
    "V11CandidateExperimentRunner",
]
