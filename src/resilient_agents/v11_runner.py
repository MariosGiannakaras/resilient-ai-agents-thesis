"""Protocol-v1.1 headless runner extension with explicit D0 parameters.

The historical v1.0/pilot protocol loader remains unchanged so historical
validation and evidence semantics cannot drift. T-520 provides a deliberately
non-final development adapter solely to prove D0 runner integration. T-521 owns
the authoritative candidate-v1.1 schema, tuning plan and freeze lifecycle.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contracts import ProtocolStage, RetentionPolicy
from .dyna_deployment import DynaQPlusDeploymentAgent
from .dyna_q_plus import DynaQPlusConfig
from .experiment_runner import HeadlessExperimentRequest, HeadlessExperimentRunner
from .gridworld import ACTION_NAMES
from .pilot_protocol import PilotProtocol
from .protocol import assert_stage_access
from .randomness import RandomStreams, derive_scoped_seed

V11_RUNNER_SCHEMA_VERSION = 1
V11_DEVELOPMENT_PROTOCOL_PREFIX = "v1.1-development-fixture"


class V11DevelopmentProtocol(PilotProtocol):
    """Non-final D0-capable adapter over an already validated historical protocol.

    The historical :class:`PilotProtocol` intentionally accepts only the
    historical F0/C0/R0 regimes. Relaxing that loader would alter old validation
    semantics. Instead this adapter starts from a fully validated protocol,
    replaces only its agent-regime declaration for a development-only D0
    integration check, and marks the resulting payload as non-final.

    `V11ExperimentRunner` independently blocks every stage except DEVELOPMENT
    while this adapter is in use. T-521 must replace this fixture with the
    authoritative candidate-v1.1 protocol representation before tuning/pilot or
    final execution is possible.
    """

    @classmethod
    def from_validated_base(cls, base: PilotProtocol) -> "V11DevelopmentProtocol":
        if not isinstance(base, PilotProtocol):
            raise ValueError("base must be an already validated PilotProtocol")
        payload = base.to_dict()
        base_version = str(payload["protocol_version"])
        payload["protocol_version"] = f"{V11_DEVELOPMENT_PROTOCOL_PREFIX}-{base_version}"
        payload["status"] = "pilot-unfrozen"
        scope = dict(payload["scientific_scope"])
        scope["final_evidence_use"] = False
        payload["scientific_scope"] = scope

        historical = {
            str(item["agent_id"]): dict(item)
            for item in payload.get("agent_regimes", [])
            if isinstance(item, Mapping) and "agent_id" in item
        }
        if "f0" not in historical or "c0" not in historical:
            raise ValueError("validated base must declare historical f0 and c0 regimes")
        payload["agent_regimes"] = [
            historical["f0"],
            historical["c0"],
            {
                "agent_id": "d0",
                "method": "dyna_q_plus_v1",
                "checkpoint_source": "same-selected-common-q-checkpoint-as-f0-c0",
                "post_change_learning": True,
                "deployment_exploration": "selected-common-epsilon",
                "method_configuration": {
                    "learning_rate_policy": "selected-tuning-value",
                    "discount_policy": "selected-common-discount",
                    "bootstrap_on_truncation": False,
                    "initial_q_value": 0.0,
                    "planning_steps_policy": "explicit-development-request-only",
                    "kappa_policy": "explicit-development-request-only",
                },
            },
        ]
        canonical = json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        return cls(canonical)


def _probability(value: Any, *, field: str, allow_one: bool = False) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    upper_valid = result <= 1.0 if allow_one else result < 1.0
    if not math.isfinite(result) or result < 0.0 or not upper_valid:
        boundary = "[0, 1]" if allow_one else "[0, 1)"
        raise ValueError(f"{field} must be finite and in {boundary}")
    return result


def _positive_integer(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{field} must be a positive integer")
    return value


def _seed_sequence(value: Sequence[int], *, field: str) -> tuple[int, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{field} must be an explicit sequence")
    result = tuple(value)
    if not result:
        raise ValueError(f"{field} must be non-empty")
    if any(
        not isinstance(seed, int)
        or isinstance(seed, bool)
        or not 0 <= seed < 2**64
        for seed in result
    ):
        raise ValueError(f"{field} values must be integers in [0, 2**64)")
    if len(set(result)) != len(result):
        raise ValueError(f"{field} values must be unique")
    return result


@dataclass(frozen=True)
class V11ExperimentRequest(HeadlessExperimentRequest):
    """v1.1 request: legacy fields plus explicit D0-only parameters."""

    dyna_planning_steps: int | None = None
    dyna_kappa: float | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "V11ExperimentRequest":
        if not isinstance(payload, Mapping):
            raise ValueError("v1.1 experiment request must be an object")
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
                "v1.1 request keys mismatch; "
                f"missing={sorted(expected - set(payload))}, "
                f"unknown={sorted(set(payload) - expected)}"
            )
        try:
            values = dict(payload)
            values["stage"] = ProtocolStage(values["stage"])
            values["retention_policy"] = RetentionPolicy(values["retention_policy"])
            return cls(**values)
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid v1.1 experiment request") from exc

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
        allowed = {"f0", "c0", "d0"}
        if not agents or len(set(agents)) != len(agents) or any(agent not in allowed for agent in agents):
            raise ValueError("agent_ids must be a unique non-empty subset of f0/c0/d0")

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

        if "d0" in agents:
            _positive_integer(self.dyna_planning_steps, field="dyna_planning_steps")
            if (
                not isinstance(self.dyna_kappa, (int, float))
                or isinstance(self.dyna_kappa, bool)
                or not math.isfinite(float(self.dyna_kappa))
                or float(self.dyna_kappa) <= 0.0
            ):
                raise ValueError("dyna_kappa must be finite and > 0 for D0")
        elif self.dyna_planning_steps is not None or self.dyna_kappa is not None:
            raise ValueError("Dyna parameters are only valid when d0 is requested")

        object.__setattr__(self, "root_seeds", seeds)
        object.__setattr__(self, "agent_ids", agents)

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()
        payload["dyna_planning_steps"] = self.dyna_planning_steps
        payload["dyna_kappa"] = None if self.dyna_kappa is None else float(self.dyna_kappa)
        return payload


class V11ExperimentRunner(HeadlessExperimentRunner):
    """Versioned development runner that adds D0 without changing v1.0 code."""

    request: V11ExperimentRequest

    def __init__(
        self,
        *,
        repo_root: Path,
        protocol: V11DevelopmentProtocol,
        request: V11ExperimentRequest,
    ) -> None:
        if not isinstance(protocol, V11DevelopmentProtocol):
            raise ValueError(
                "T-520 runner requires V11DevelopmentProtocol; T-521 will supply "
                "the authoritative candidate-v1.1 protocol type"
            )
        if not isinstance(request, V11ExperimentRequest):
            raise ValueError("request must be V11ExperimentRequest")
        super().__init__(repo_root=repo_root, protocol=protocol, request=request)

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
        if "d0" in self.request.agent_ids and declared["d0"].get("method") != "dyna_q_plus_v1":
            raise ValueError("protocol d0 must declare method dyna_q_plus_v1")

        if self.request.stage is not ProtocolStage.DEVELOPMENT:
            raise ValueError(
                "v1.1 non-development execution is blocked until T-521 "
                "candidate protocol validation is implemented"
            )

    def _resolved_config(self) -> dict[str, Any]:
        resolved = super()._resolved_config()
        resolved["headless_runner_schema_version"] = V11_RUNNER_SCHEMA_VERSION
        resolved["entrypoint"] = "resilient_agents.v11_runner.v1"
        resolved["protocol_lifecycle"] = "development-fixture-only"
        return resolved

    def _dyna_agent(self, *, checkpoint: Mapping[str, Any]) -> DynaQPlusDeploymentAgent:
        if self.request.dyna_planning_steps is None or self.request.dyna_kappa is None:
            raise RuntimeError("D0 parameters were not resolved")
        return DynaQPlusDeploymentAgent(
            DynaQPlusConfig(
                agent_id="d0",
                actions=ACTION_NAMES,
                learning_rate=float(self.request.q_learning_rate),
                discount_factor=float(self.request.discount_factor),
                exploration_epsilon=float(self.request.exploration_epsilon),
                planning_steps=int(self.request.dyna_planning_steps),
                kappa=float(self.request.dyna_kappa),
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=dict(checkpoint),
        )

    def _run_branch(
        self,
        *,
        bundle: Any,
        root_seed: int,
        agent_id: str,
        q_checkpoint: Mapping[str, Any],
        branch: str,
    ) -> tuple[list[float], str]:
        if agent_id != "d0":
            return super()._run_branch(
                bundle=bundle,
                root_seed=root_seed,
                agent_id=agent_id,
                q_checkpoint=q_checkpoint,
                branch=branch,
            )
        if branch not in {"reference", "disrupted"}:
            raise ValueError("branch must be reference or disrupted")

        total = self.request.pre_change_episodes + self.request.post_change_episodes
        curve: list[float] = []
        agent = self._dyna_agent(checkpoint=q_checkpoint)
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
