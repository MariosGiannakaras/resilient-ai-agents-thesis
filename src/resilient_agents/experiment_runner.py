"""Headless multi-seed execution over the validated pilot protocol."""
from __future__ import annotations

import json
import math
import time
import traceback
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .agents import (
    RectangularRobustValueIterationAgent,
    RobustStateAction,
    RobustTransitionOutcome,
    RobustTransitionRow,
    RobustValueIterationConfig,
    TabularQLearningAgent,
    TabularQLearningConfig,
)
from .contracts import (
    ChangeEvent,
    InformationPolicy,
    ProtocolStage,
    RetentionPolicy,
    ScenarioSpec,
    project_for_agent,
)
from .environment import EnvironmentSeeds
from .gridworld import ACTION_NAMES, GridAction, GridWorldEnvironment
from .metrics import compute_resilience_metrics
from .pilot_protocol import PilotProtocol
from .protocol import assert_stage_access
from .randomness import RandomStreams, derive_scoped_seed
from .run_bundle import RunBundle
from .session import ExperimentSession

HEADLESS_RUNNER_SCHEMA_VERSION = 1
RUNNER_STATE_FILENAME = "runner-state.json"


class ExperimentTimeoutError(RuntimeError):
    """Raised when a predeclared child wall-clock deadline is exceeded."""


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
class HeadlessExperimentRequest:
    """Fully explicit inputs for one multi-root, multi-agent experiment."""

    run_id: str
    stage: ProtocolStage
    layout_id: str
    condition_id: str
    root_seeds: Sequence[int]
    agent_ids: Sequence[str]
    q_learning_rate: float
    discount_factor: float
    exploration_epsilon: float
    training_episodes_per_layout: int
    pre_change_episodes: int
    post_change_episodes: int
    immediate_window: int
    worst_window: int
    terminal_window: int
    recovery_tolerance: float
    recovery_stability_episodes: int
    retention_policy: RetentionPolicy
    auto_publish: bool
    execution_timeout_seconds: float | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "HeadlessExperimentRequest":
        if not isinstance(payload, Mapping):
            raise ValueError("headless experiment request must be an object")
        expected = {
            "run_id",
            "stage",
            "layout_id",
            "condition_id",
            "root_seeds",
            "agent_ids",
            "q_learning_rate",
            "discount_factor",
            "exploration_epsilon",
            "training_episodes_per_layout",
            "pre_change_episodes",
            "post_change_episodes",
            "immediate_window",
            "worst_window",
            "terminal_window",
            "recovery_tolerance",
            "recovery_stability_episodes",
            "retention_policy",
            "auto_publish",
            "execution_timeout_seconds",
        }
        if set(payload) != expected:
            raise ValueError(
                "headless request keys mismatch; "
                f"missing={sorted(expected - set(payload))}, "
                f"unknown={sorted(set(payload) - expected)}"
            )
        try:
            values = dict(payload)
            values["stage"] = ProtocolStage(values["stage"])
            values["retention_policy"] = RetentionPolicy(values["retention_policy"])
            return cls(**values)
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid headless experiment request") from exc

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
            or any(agent not in {"f0", "c0", "r0"} for agent in agents)
        ):
            raise ValueError("agent_ids must be a unique non-empty subset of f0/c0/r0")
        _probability(self.q_learning_rate, field="q_learning_rate", allow_one=True)
        _probability(self.discount_factor, field="discount_factor")
        _probability(self.exploration_epsilon, field="exploration_epsilon", allow_one=True)
        for field in (
            "training_episodes_per_layout",
            "pre_change_episodes",
            "post_change_episodes",
            "immediate_window",
            "worst_window",
            "terminal_window",
            "recovery_stability_episodes",
        ):
            _positive_integer(getattr(self, field), field=field)
        if (
            not isinstance(self.recovery_tolerance, (int, float))
            or isinstance(self.recovery_tolerance, bool)
            or not math.isfinite(float(self.recovery_tolerance))
            or self.recovery_tolerance < 0.0
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
            or self.execution_timeout_seconds <= 0.0
        ):
            raise ValueError("execution_timeout_seconds must be finite and positive")
        object.__setattr__(self, "root_seeds", seeds)
        object.__setattr__(self, "agent_ids", agents)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "stage": self.stage.value,
            "layout_id": self.layout_id,
            "condition_id": self.condition_id,
            "root_seeds": list(self.root_seeds),
            "agent_ids": list(self.agent_ids),
            "q_learning_rate": float(self.q_learning_rate),
            "discount_factor": float(self.discount_factor),
            "exploration_epsilon": float(self.exploration_epsilon),
            "training_episodes_per_layout": self.training_episodes_per_layout,
            "pre_change_episodes": self.pre_change_episodes,
            "post_change_episodes": self.post_change_episodes,
            "immediate_window": self.immediate_window,
            "worst_window": self.worst_window,
            "terminal_window": self.terminal_window,
            "recovery_tolerance": float(self.recovery_tolerance),
            "recovery_stability_episodes": self.recovery_stability_episodes,
            "retention_policy": self.retention_policy.value,
            "auto_publish": self.auto_publish,
            "execution_timeout_seconds": self.execution_timeout_seconds,
        }


@dataclass(frozen=True)
class HeadlessRunResult:
    run_dir: Path
    publication_commit: str | None


class HeadlessExperimentRunner:
    """Execute and safely resume one experiment at root-seed boundaries."""

    def __init__(
        self,
        *,
        repo_root: Path,
        protocol: PilotProtocol,
        request: HeadlessExperimentRequest,
        writable_root: Path | None = None,
    ) -> None:
        if not isinstance(repo_root, Path):
            raise ValueError("repo_root must be pathlib.Path")
        if not isinstance(protocol, PilotProtocol):
            raise ValueError("protocol must be PilotProtocol")
        if not isinstance(request, HeadlessExperimentRequest):
            raise ValueError("request must be HeadlessExperimentRequest")
        self.repo_root = repo_root.resolve()
        self.writable_root = Path(writable_root).resolve() if writable_root else self.repo_root
        self.protocol = protocol
        self.request = request
        self._payload = protocol.to_dict()
        self._deadline_monotonic: float | None = None
        self._validate_request()

    def _validate_request(self) -> None:
        assert_stage_access(
            stage=self.request.stage,
            scenario_ids=[self.request.layout_id],
            partition=self.protocol.partition(),
        )
        if self.request.condition_id not in self.protocol.condition_ids():
            raise ValueError("condition_id is not defined by the pilot protocol")
        post_length = self.request.post_change_episodes
        for field in (
            "immediate_window",
            "worst_window",
            "terminal_window",
            "recovery_stability_episodes",
        ):
            if getattr(self.request, field) > post_length:
                raise ValueError(f"{field} exceeds the post-change episode count")
        tuning = self._payload["tuning"]
        evaluation = self._payload["evaluation"]
        metrics = self._payload["metric_sensitivity"]
        if self.request.stage is ProtocolStage.PILOT:
            if tuple(self.request.root_seeds) != tuple(evaluation["root_seeds"]):
                raise ValueError("pilot execution must use the complete precommitted seed bank")
            expected = (
                ("training_episodes_per_layout", tuning["training_episodes_per_layout"]),
                ("pre_change_episodes", evaluation["pre_change_episodes"]),
                ("post_change_episodes", evaluation["post_change_episodes"]),
            )
            for field, value in expected:
                if getattr(self.request, field) != value:
                    raise ValueError(f"pilot {field} differs from pilot-v0.1")
            search = tuning["q_learning_search"]
            for request_field, protocol_field in (
                ("q_learning_rate", "learning_rates"),
                ("discount_factor", "discount_factors"),
                ("exploration_epsilon", "exploration_epsilons"),
            ):
                if getattr(self.request, request_field) not in search[protocol_field]:
                    raise ValueError(f"pilot {request_field} is outside the search")
            for request_field, protocol_field in (
                ("immediate_window", "immediate_windows"),
                ("worst_window", "worst_windows"),
                ("terminal_window", "terminal_windows"),
                ("recovery_tolerance", "recovery_tolerances_step_reward_units"),
                ("recovery_stability_episodes", "recovery_stability_episodes"),
            ):
                if getattr(self.request, request_field) not in metrics[protocol_field]:
                    raise ValueError(f"pilot {request_field} is outside metric sensitivity")
        elif self.request.stage is ProtocolStage.TUNING:
            if tuple(self.request.root_seeds) != tuple(tuning["root_seeds"]):
                raise ValueError("tuning execution must use the complete tuning seed bank")
            if self.request.training_episodes_per_layout != tuning[
                "training_episodes_per_layout"
            ]:
                raise ValueError("tuning training budget differs from pilot-v0.1")
            if (
                self.request.pre_change_episodes + self.request.post_change_episodes
                != tuning["nominal_evaluation_episodes_per_layout"]
            ):
                raise ValueError("tuning nominal evaluation budget differs from pilot-v0.1")
            if self.request.condition_id != "nominal" or self.request.agent_ids != ("f0",):
                raise ValueError("Q tuning must evaluate the frozen checkpoint nominally")
            search = tuning["q_learning_search"]
            if (
                self.request.q_learning_rate not in search["learning_rates"]
                or self.request.discount_factor not in search["discount_factors"]
                or self.request.exploration_epsilon
                not in search["exploration_epsilons"]
            ):
                raise ValueError("tuning hyperparameters are outside the predeclared search")
        if self.request.stage is ProtocolStage.PILOT:
            if self.request.agent_ids != ("f0", "c0", "r0"):
                raise ValueError("pilot experiments must execute the complete agent set")
            if self.request.retention_policy is not RetentionPolicy.EVENTS:
                raise ValueError("pilot-v0.1 requires events plus persisted episode curves")
        if self.request.stage in {ProtocolStage.TUNING, ProtocolStage.PILOT}:
            timeout = self.request.execution_timeout_seconds
            timeout_rule = self._payload["resource_policy"]["child_timeout_rule"]
            if timeout is None or not (
                timeout_rule["minimum_seconds"]
                <= timeout
                <= timeout_rule["maximum_seconds"]
            ):
                raise ValueError("tuning/pilot child timeout is outside pilot-v0.1")

    def _resolved_config(self) -> dict[str, Any]:
        return {
            "headless_runner_schema_version": HEADLESS_RUNNER_SCHEMA_VERSION,
            "entrypoint": "resilient_agents.experiment_runner.v1",
            "seed_derivation": {
                "scoped_root": "resilient-agents-scoped-v1",
                "independent_streams": "resilient-agents-v1",
            },
            "protocol": self._payload,
            "request": self.request.to_dict(),
        }

    def _new_or_resumed_bundle(self) -> tuple[RunBundle, bool]:
        resolved = self._resolved_config()
        run_dir = self.writable_root / "results" / "runs" / self.request.run_id
        common = dict(
            repo_root=self.repo_root,
            writable_root=self.writable_root,
            run_id=self.request.run_id,
            resolved_config=resolved,
            protocol_version=self.protocol.protocol_version,
            stage=self.request.stage.value,
            retention_policy=self.request.retention_policy.value,
        )
        if run_dir.exists():
            return RunBundle.resume(**common), True
        return RunBundle(**common), False

    def _load_state(self, bundle: RunBundle, *, resumed: bool) -> dict[str, Any]:
        path = bundle.run_dir / RUNNER_STATE_FILENAME
        if path.exists():
            try:
                state = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                raise RuntimeError("runner checkpoint is unreadable") from exc
            if not isinstance(state, dict) or set(state) != {
                "schema_version",
                "resume_generation",
                "completed_root_seeds",
                "root_results",
            }:
                raise RuntimeError("runner checkpoint schema is invalid")
            completed = state["completed_root_seeds"]
            results = state["root_results"]
            if (
                state["schema_version"] != HEADLESS_RUNNER_SCHEMA_VERSION
                or not isinstance(state["resume_generation"], int)
                or not isinstance(completed, list)
                or not isinstance(results, list)
                or len(completed) != len(results)
                or completed != [item.get("root_seed") for item in results]
                or len(set(completed)) != len(completed)
                or any(seed not in self.request.root_seeds for seed in completed)
            ):
                raise RuntimeError("runner checkpoint content is inconsistent")
            if resumed:
                state["resume_generation"] += 1
        elif resumed:
            raise RuntimeError("unfinished bundle has no runner checkpoint")
        else:
            state = {
                "schema_version": HEADLESS_RUNNER_SCHEMA_VERSION,
                "resume_generation": 0,
                "completed_root_seeds": [],
                "root_results": [],
            }
        bundle.write_json_artifact(RUNNER_STATE_FILENAME, state)
        return state

    def run(self) -> HeadlessRunResult:
        self._deadline_monotonic = (
            None
            if self.request.execution_timeout_seconds is None
            else time.monotonic() + self.request.execution_timeout_seconds
        )
        bundle, resumed = self._new_or_resumed_bundle()
        session = ExperimentSession(bundle)
        state = self._load_state(bundle, resumed=resumed)
        bundle.append_event(
            {
                "event": "experiment_resumed" if resumed else "experiment_started",
                "resume_generation": state["resume_generation"],
                "completed_root_count": len(state["completed_root_seeds"]),
                "total_root_count": len(self.request.root_seeds),
            }
        )
        if self.request.stage in {ProtocolStage.TUNING, ProtocolStage.PILOT}:
            source = bundle.provenance
            clean = (
                source.get("git_commit") is not None
                and source.get("tracked_changes_present") is False
                and source.get("untracked_nonoutput_present") is False
            )
            if not clean:
                message = "tuning/pilot execution requires a clean committed source tree"
                session.finalize(
                    status="invalid",
                    summary={
                        "failure": {"type": "SourceProvenanceError", "message": message},
                        "runner_state": state,
                    },
                    auto_publish=False,
                )
                raise RuntimeError(message)
        try:
            for root_seed in self.request.root_seeds:
                self._check_deadline()
                if root_seed in state["completed_root_seeds"]:
                    continue
                bundle.append_event(
                    {
                        "event": "root_started",
                        "root_seed": root_seed,
                        "resume_generation": state["resume_generation"],
                    }
                )
                result = self._run_root(bundle=bundle, root_seed=root_seed)
                state["completed_root_seeds"].append(root_seed)
                state["root_results"].append(result)
                bundle.write_json_artifact(RUNNER_STATE_FILENAME, state)
                bundle.append_event(
                    {
                        "event": "root_completed",
                        "root_seed": root_seed,
                        "completed_root_count": len(state["completed_root_seeds"]),
                        "total_root_count": len(self.request.root_seeds),
                    }
                )
        except Exception as exc:
            failure = {
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc(),
            }
            try:
                bundle.append_event({"event": "experiment_failed", "failure": failure})
            finally:
                session.finalize(
                    status="failed",
                    summary={"failure": failure, "runner_state": state},
                    auto_publish=self.request.auto_publish,
                )
            raise
        summary = {
            "status": "completed",
            "protocol_version": self.protocol.protocol_version,
            "stage": self.request.stage.value,
            "layout_id": self.request.layout_id,
            "condition_id": self.request.condition_id,
            "completed_root_count": len(state["completed_root_seeds"]),
            "requested_root_count": len(self.request.root_seeds),
            "root_results": state["root_results"],
        }
        run_dir, publication = session.finalize(
            status="completed", summary=summary, auto_publish=self.request.auto_publish
        )
        return HeadlessRunResult(
            run_dir=run_dir,
            publication_commit=None if publication is None else publication.commit,
        )

    def _check_deadline(self) -> None:
        if (
            self._deadline_monotonic is not None
            and time.monotonic() >= self._deadline_monotonic
        ):
            raise ExperimentTimeoutError(
                f"experiment exceeded {self.request.execution_timeout_seconds} seconds"
            )

    def _run_root(self, *, bundle: RunBundle, root_seed: int) -> dict[str, Any]:
        checkpoint, training_curves = self._train_checkpoint(bundle=bundle, root_seed=root_seed)
        audit = self._q_agent(
            agent_id="checkpoint-audit", learning_enabled=False, checkpoint=checkpoint
        )
        results = [
            self._evaluate_agent(
                bundle=bundle,
                root_seed=root_seed,
                agent_id=agent_id,
                q_checkpoint=checkpoint,
            )
            for agent_id in self.request.agent_ids
        ]
        return {
            "root_seed": root_seed,
            "training_episode_returns": training_curves,
            "common_q_checkpoint": checkpoint,
            "common_q_checkpoint_sha256": audit.checkpoint_sha256(),
            "agent_results": results,
        }

    def _training_layout_ids(self) -> tuple[str, ...]:
        if self.request.stage in {ProtocolStage.TUNING, ProtocolStage.PILOT}:
            return tuple(self._payload["partitions"]["tuning"])
        return (self.request.layout_id,)

    def _train_checkpoint(
        self, *, bundle: RunBundle, root_seed: int
    ) -> tuple[dict[str, Any], dict[str, list[float]]]:
        checkpoint: dict[str, Any] | None = None
        curves: dict[str, list[float]] = {}
        for layout_id in self._training_layout_ids():
            scenario = self._scenario(layout_id=layout_id, condition_id="nominal")
            returns: list[float] = []
            for episode in range(self.request.training_episodes_per_layout):
                self._check_deadline()
                agent = self._q_agent(
                    agent_id="nominal-trainer",
                    learning_enabled=True,
                    checkpoint=checkpoint,
                )
                seeds = RandomStreams(
                    derive_scoped_seed(root_seed, f"training-agent:{layout_id}:{episode}")
                ).derived_seeds()
                agent.reset(
                    initialization_seed=seeds["agent_initialization"],
                    exploration_seed=seeds["agent_exploration"],
                )
                episode_return, _, _ = self._run_episode(
                    bundle=bundle,
                    agent=agent,
                    scenario=scenario,
                    root_seed=root_seed,
                    scope=f"training-environment:{layout_id}:{episode}",
                    phase="training",
                    branch="nominal",
                    agent_id="nominal-trainer",
                    episode_index=episode,
                    agent_seeds=seeds,
                )
                checkpoint = agent.checkpoint()
                returns.append(episode_return)
            curves[layout_id] = returns
        if checkpoint is None:
            raise RuntimeError("nominal training produced no checkpoint")
        return checkpoint, curves

    def _evaluate_agent(
        self,
        *,
        bundle: RunBundle,
        root_seed: int,
        agent_id: str,
        q_checkpoint: Mapping[str, Any],
    ) -> dict[str, Any]:
        reference, reference_state = self._run_branch(
            bundle=bundle,
            root_seed=root_seed,
            agent_id=agent_id,
            q_checkpoint=q_checkpoint,
            branch="reference",
        )
        observed, observed_state = self._run_branch(
            bundle=bundle,
            root_seed=root_seed,
            agent_id=agent_id,
            q_checkpoint=q_checkpoint,
            branch="disrupted",
        )
        pre = self.request.pre_change_episodes
        if observed[:pre] != reference[:pre]:
            raise RuntimeError("matched branches diverged before the change boundary")
        metrics = compute_resilience_metrics(
            observed,
            reference_values=reference,
            change_index=pre,
            immediate_window=self.request.immediate_window,
            worst_window=self.request.worst_window,
            terminal_window=self.request.terminal_window,
            recovery_tolerance=float(self.request.recovery_tolerance),
            recovery_stability_steps=self.request.recovery_stability_episodes,
        )
        return {
            "agent_id": agent_id,
            "reference_episode_returns": reference,
            "observed_episode_returns": observed,
            "metrics": asdict(metrics),
            "reference_final_state_sha256": reference_state,
            "observed_final_state_sha256": observed_state,
        }

    def _run_branch(
        self,
        *,
        bundle: RunBundle,
        root_seed: int,
        agent_id: str,
        q_checkpoint: Mapping[str, Any],
        branch: str,
    ) -> tuple[list[float], str]:
        if branch not in {"reference", "disrupted"}:
            raise ValueError("branch must be reference or disrupted")
        total = self.request.pre_change_episodes + self.request.post_change_episodes
        curve: list[float] = []
        current_checkpoint = dict(q_checkpoint)
        robust_agent = self._robust_agent() if agent_id == "r0" else None
        for episode in range(total):
            self._check_deadline()
            after_change = episode >= self.request.pre_change_episodes
            condition_id = (
                self.request.condition_id
                if branch == "disrupted" and after_change
                else "nominal"
            )
            scenario = self._scenario(
                layout_id=self.request.layout_id, condition_id=condition_id
            )
            seeds = RandomStreams(
                derive_scoped_seed(root_seed, f"evaluation-agent:{episode}")
            ).derived_seeds()
            if agent_id in {"f0", "c0"}:
                agent: Any = self._q_agent(
                    agent_id=agent_id,
                    learning_enabled=agent_id == "c0",
                    checkpoint=current_checkpoint,
                )
            elif robust_agent is not None:
                agent = robust_agent
            else:
                raise ValueError(f"unsupported agent_id: {agent_id}")
            agent.reset(
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
            if agent_id in {"f0", "c0"}:
                current_checkpoint = agent.checkpoint()
        if agent_id in {"f0", "c0"}:
            audit = self._q_agent(
                agent_id=agent_id,
                learning_enabled=agent_id == "c0",
                checkpoint=current_checkpoint,
            )
            return curve, audit.checkpoint_sha256()
        if robust_agent is None:
            raise RuntimeError("robust agent state is unavailable")
        return curve, robust_agent.plan_sha256()

    def _run_episode(
        self,
        *,
        bundle: RunBundle,
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
                agent.observe(project_for_agent(transition, environment.information_policy))
                total_reward += float(transition.reward)
                length += 1
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
                    "observation_disturbance": streams[
                        "observation_disturbance"
                    ],
                },
            }
        )
        return total_reward, length, outcome

    def _q_agent(
        self,
        *,
        agent_id: str,
        learning_enabled: bool,
        checkpoint: Mapping[str, Any] | None,
    ) -> TabularQLearningAgent:
        return TabularQLearningAgent(
            TabularQLearningConfig(
                agent_id=agent_id,
                actions=ACTION_NAMES,
                learning_rate=float(self.request.q_learning_rate),
                discount_factor=float(self.request.discount_factor),
                exploration_epsilon=float(self.request.exploration_epsilon),
                learning_enabled=learning_enabled,
                bootstrap_on_truncation=False,
                initial_q_value=0.0,
            ),
            checkpoint=checkpoint,
        )

    def _robust_agent(self) -> RectangularRobustValueIterationAgent:
        layout = self._layout(self.request.layout_id)
        grid = layout["grid"]
        width, height = int(grid["width"]), int(grid["height"])
        obstacles = {tuple(item) for item in grid["obstacles"]}
        goal = tuple(grid["goal"])
        states = tuple(
            (x, y)
            for x in range(width)
            for y in range(height)
            if (x, y) not in obstacles
        )
        vectors = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0),
        }
        rewards = self._payload["reward_spec"]
        mappings = self._payload["robust_prior"]["candidate_action_mappings"]
        entries: list[RobustStateAction] = []
        for state in states:
            if state == goal:
                continue
            for action in ACTION_NAMES:
                rows = []
                for mapping in mappings:
                    dx, dy = vectors[mapping[action]]
                    candidate = state[0] + dx, state[1] + dy
                    collided = (
                        not 0 <= candidate[0] < width
                        or not 0 <= candidate[1] < height
                        or candidate in obstacles
                    )
                    next_state = state if collided else candidate
                    terminal = next_state == goal
                    reward = (
                        rewards["goal"]
                        if terminal
                        else rewards["collision"]
                        if collided
                        else rewards["step"]
                    )
                    rows.append(
                        RobustTransitionRow(
                            outcomes=(
                                RobustTransitionOutcome(
                                    next_state, 1.0, float(reward), terminal
                                ),
                            )
                        )
                    )
                entries.append(RobustStateAction(state, action, tuple(rows)))
        r0 = next(
            item for item in self._payload["agent_regimes"] if item["agent_id"] == "r0"
        )
        method = r0["method_configuration"]
        return RectangularRobustValueIterationAgent(
            RobustValueIterationConfig(
                agent_id="r0",
                states=states,
                terminal_states=(goal,),
                actions=ACTION_NAMES,
                state_actions=tuple(entries),
                discount_factor=float(self.request.discount_factor),
                convergence_tolerance=float(method["convergence_tolerance"]),
                max_iterations=int(method["max_iterations"]),
                initial_value=float(method["initial_value"]),
                exploration_epsilon=float(self.request.exploration_epsilon),
            )
        )

    def _layout(self, layout_id: str) -> Mapping[str, Any]:
        try:
            return next(
                item
                for item in self._payload["layouts"]
                if item["layout_id"] == layout_id
            )
        except StopIteration as exc:
            raise ValueError(f"unknown layout_id: {layout_id}") from exc

    def _condition(self, condition_id: str) -> Mapping[str, Any]:
        try:
            return next(
                item
                for item in self._payload["conditions"]
                if item["condition_id"] == condition_id
            )
        except StopIteration as exc:
            raise ValueError(f"unknown condition_id: {condition_id}") from exc

    def _scenario(self, *, layout_id: str, condition_id: str) -> ScenarioSpec:
        layout = self._layout(layout_id)
        condition = self._condition(condition_id)
        horizon = self._payload["episode_horizon"]
        max_steps = int(
            horizon["required_shortest_path_length"]
            * horizon["shortest_path_multiplier"]
        )
        events: tuple[ChangeEvent, ...] = ()
        if condition["mechanism"] == "action-remap":
            identity = {name: name for name in ACTION_NAMES}
            events = (
                ChangeEvent(
                    event_id=condition_id,
                    change_type="action-remap",
                    onset_step=0,
                    persistent=True,
                    affected_mechanism="transition",
                    severity={"remapped_actions": condition["remapped_actions"]},
                    pre_change={"action_remap": identity},
                    post_change={"action_remap": dict(condition["action_mapping"])},
                ),
            )
        return ScenarioSpec(
            scenario_id=f"{layout_id}--{condition_id}",
            environment_id="project-gridworld-v1",
            max_steps=max_steps,
            reward_spec=dict(self._payload["reward_spec"]),
            initial_state_spec={"grid": dict(layout["grid"])},
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
                "failure_probability": condition["action_failure_probability"],
            },
            observation_disturbance_spec={
                "type": "position-mislocalization",
                "mislocalization_probability": condition[
                    "observation_corruption_probability"
                ],
            },
            change_events=events,
            information_policy=InformationPolicy(**dict(self._payload["information_policy"])),
        )
