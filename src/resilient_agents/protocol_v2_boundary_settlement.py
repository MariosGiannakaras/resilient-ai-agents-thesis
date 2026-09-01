"""DEC-054 Phase-A interaction-budget boundary settlement.

Settlement completes method-specific algorithmic bookkeeping attributable to
an already-consumed Phase-A interaction.  It never steps an environment and it
never treats a fresh Phase-B observation as continuation of the Phase-A
episode.  The historical checkpoint remains immutable input; the result is a
derived, quiescent deployment-start learner state.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Collection, Mapping

from .protocol_v2 import ScientificStateAdapter
from .protocol_v2_sb3 import SB3ScientificStateAdapter
from .protocol_v2_sb3_identity import require_scientific_continuation_invariants
from .protocol_v2_tabular_phase_b import _agent


SETTLEMENT_POLICY_ID = "dec-054-phase-a-budget-boundary-settlement-v1"
CORE_METHOD_IDS = ("q_learning", "sarsa", "dqn", "ppo", "dyna_q_plus")


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _counter_snapshot(
    learner: ScientificStateAdapter, *, expected_interactions: int
) -> Mapping[str, int | float]:
    state = learner.export_state()
    if learner.method_id in {"q_learning", "sarsa", "dyna_q_plus"}:
        count = state["observed_transition_count"]
        last_step = state["last_step"]
        if count != expected_interactions or last_step != expected_interactions - 1:
            raise ValueError(
                f"{learner.method_id} Phase-A boundary counters do not identify "
                "the final consumed interaction"
            )
        result: dict[str, int | float] = {
            "observed_transition_count": int(count),
            "last_step": int(last_step),
        }
        if learner.method_id == "dyna_q_plus":
            if state["time"] != expected_interactions:
                raise ValueError("Dyna-Q+ time does not match consumed interactions")
            result.update(
                {
                    "time": int(state["time"]),
                    "planning_update_count": int(state["planning_update_count"]),
                }
            )
        return result
    if learner.method_id in {"dqn", "ppo"}:
        if not isinstance(learner, SB3ScientificStateAdapter):
            raise ValueError("SB3 method requires SB3ScientificStateAdapter")
        require_scientific_continuation_invariants(learner)
        counters = state["counters"]
        if counters["num_timesteps"] != expected_interactions:
            raise ValueError("SB3 Phase-A interaction counter mismatch")
        return {
            "num_timesteps": int(counters["num_timesteps"]),
            "n_updates": int(counters["n_updates"]),
            "current_progress_remaining": float(
                counters["current_progress_remaining"]
            ),
        }
    raise ValueError(f"unsupported boundary-settlement method: {learner.method_id!r}")


def require_quiescent_deployment_state(
    learner: ScientificStateAdapter, *, expected_interactions: int
) -> Mapping[str, int | float]:
    """Require a method-correct deployment-start state at the Phase-A budget."""

    if learner.method_id not in CORE_METHOD_IDS:
        raise ValueError("learner method is outside the DEC-054 core set")
    counters = _counter_snapshot(
        learner, expected_interactions=expected_interactions
    )
    state = learner.export_state()
    if learner.method_id == "q_learning" and state["pending_action"] is not None:
        raise ValueError("Q-Learning boundary has an unconsumed pending action")
    if learner.method_id == "sarsa" and (
        state["pending_action"] is not None or state["deferred_update"] is not None
    ):
        raise ValueError("SARSA boundary is not quiescent")
    if learner.method_id == "dyna_q_plus" and state["pending"] is not None:
        raise ValueError("Dyna-Q+ boundary has an unconsumed pending action")
    return counters


@dataclass(frozen=True)
class BoundarySettlementResult:
    method_id: str
    policy_id: str
    no_op: bool
    deferred_state_present: bool
    pre_learner_state_sha256: str
    post_learner_state_sha256: str
    pre_counters: Mapping[str, int | float]
    post_counters: Mapping[str, int | float]
    environment_interactions_consumed: int
    details: Mapping[str, Any] | None

    def __post_init__(self) -> None:
        if self.policy_id != SETTLEMENT_POLICY_ID:
            raise ValueError("boundary settlement policy mismatch")
        if self.environment_interactions_consumed != 0:
            raise ValueError("boundary settlement must consume zero interactions")
        if self.no_op and self.pre_learner_state_sha256 != self.post_learner_state_sha256:
            raise ValueError("no-op settlement changed learner state")
        if not self.no_op and self.method_id != "sarsa":
            raise ValueError("only SARSA may require non-no-op DEC-054 settlement")

    def to_mapping(self) -> Mapping[str, Any]:
        return {
            "method_id": self.method_id,
            "policy_id": self.policy_id,
            "no_op": self.no_op,
            "deferred_state_present": self.deferred_state_present,
            "pre_learner_state_sha256": self.pre_learner_state_sha256,
            "post_learner_state_sha256": self.post_learner_state_sha256,
            "pre_counters": dict(self.pre_counters),
            "post_counters": dict(self.post_counters),
            "environment_interactions_consumed": 0,
            "details": None if self.details is None else dict(self.details),
        }


def settle_phase_a_interaction_boundary(
    learner: ScientificStateAdapter,
    *,
    expected_source_learner_sha256: str,
    expected_interactions: int,
    valid_observations: Collection[tuple[int, int]] | None = None,
) -> BoundarySettlementResult:
    """Settle one exact accepted Phase-A state without environment execution.

    The operation is explicitly idempotent for already-quiescent states.  The
    physical runner nevertheless always applies it to an exact DEC-053 source
    whose pre-settlement digest is independently pinned by recovery evidence.
    """

    if learner.method_id not in CORE_METHOD_IDS:
        raise ValueError("learner method is outside the DEC-054 core set")
    if expected_interactions <= 0:
        raise ValueError("expected_interactions must be > 0")
    pre_sha = learner.state_sha256()
    if pre_sha != expected_source_learner_sha256:
        raise ValueError("boundary-settlement source learner SHA mismatch")
    pre_counters = _counter_snapshot(
        learner, expected_interactions=expected_interactions
    )

    if learner.method_id != "sarsa":
        post_counters = require_quiescent_deployment_state(
            learner, expected_interactions=expected_interactions
        )
        return BoundarySettlementResult(
            method_id=learner.method_id,
            policy_id=SETTLEMENT_POLICY_ID,
            no_op=True,
            deferred_state_present=False,
            pre_learner_state_sha256=pre_sha,
            post_learner_state_sha256=learner.state_sha256(),
            pre_counters=pre_counters,
            post_counters=post_counters,
            environment_interactions_consumed=0,
            details=None,
        )

    state = learner.export_state()
    if state["pending_action"] is not None:
        raise ValueError("SARSA settlement requires pending_action is None")
    deferred = state["deferred_update"]
    if deferred is None:
        post_counters = require_quiescent_deployment_state(
            learner, expected_interactions=expected_interactions
        )
        return BoundarySettlementResult(
            method_id="sarsa",
            policy_id=SETTLEMENT_POLICY_ID,
            no_op=True,
            deferred_state_present=False,
            pre_learner_state_sha256=pre_sha,
            post_learner_state_sha256=learner.state_sha256(),
            pre_counters=pre_counters,
            post_counters=post_counters,
            environment_interactions_consumed=0,
            details=None,
        )
    if set(deferred) != {"state", "action", "reward", "next_state"}:
        raise ValueError("SARSA deferred update schema mismatch")
    if valid_observations is None:
        raise ValueError("SARSA deferred settlement requires valid observations")
    next_observation = deferred["next_state"]
    if (
        not isinstance(next_observation, list)
        or len(next_observation) != 2
        or any(not isinstance(item, int) or isinstance(item, bool) for item in next_observation)
        or tuple(next_observation) not in valid_observations
    ):
        raise ValueError("SARSA deferred next_state is not a valid layout observation")

    agent = _agent(learner)
    if agent.config.bootstrap_on_truncation is not True:
        raise ValueError("DEC-054 SARSA settlement requires bootstrap_on_truncation")
    if agent._deferred_update is None or agent._pending_action is not None:
        raise ValueError("SARSA restored private boundary state is inconsistent")
    prior_state_key, prior_action_key, reward, next_state_key = agent._deferred_update
    if (
        json.loads(prior_state_key) != deferred["state"]
        or json.loads(prior_action_key) != deferred["action"]
        or reward != float(deferred["reward"])
        or json.loads(next_state_key) != deferred["next_state"]
    ):
        raise ValueError("SARSA deferred public/private state mismatch")

    rng_before = state["exploration_rng_state"]
    q_before = float(agent._q_value(prior_state_key, prior_action_key))
    bootstrap_action_key = agent._select_action_key(next_state_key)
    bootstrap_q_value = float(agent._q_value(next_state_key, bootstrap_action_key))
    target = float(reward) + float(agent.config.discount_factor) * bootstrap_q_value
    expected_after = q_before + float(agent.config.learning_rate) * (target - q_before)
    if not math.isfinite(expected_after):
        raise ValueError("SARSA boundary settlement produced non-finite Q value")
    agent._update(
        state_key=prior_state_key,
        action_key=prior_action_key,
        reward=float(reward),
        bootstrap=bootstrap_q_value,
    )
    agent._deferred_update = None
    q_after = float(agent._q_value(prior_state_key, prior_action_key))
    if q_after != expected_after:
        raise RuntimeError("SARSA settlement did not apply the exact one-step update")
    if agent._pending_action is not None:
        raise RuntimeError("bootstrap-only SARSA action leaked into deployment pending state")

    post_counters = require_quiescent_deployment_state(
        learner, expected_interactions=expected_interactions
    )
    if post_counters != pre_counters:
        raise RuntimeError("SARSA settlement changed interaction accounting")
    post_state = learner.export_state()
    details = {
        "deferred_transition": dict(deferred),
        "selected_bootstrap_action": agent._action_by_key[bootstrap_action_key],
        "behavior_policy": "restored-phase-a-epsilon-greedy",
        "behavior_policy_exploration_epsilon": float(
            agent.config.exploration_epsilon
        ),
        "behavior_policy_action_order": list(agent.config.actions),
        "exploration_rng_source": "exact-restored-phase-a-exploration-rng",
        "exploration_rng_state_sha256_before": _sha256(rng_before),
        "exploration_rng_state_sha256_after": _sha256(
            post_state["exploration_rng_state"]
        ),
        "q_value_before": q_before,
        "bootstrap_q_value": bootstrap_q_value,
        "target": target,
        "q_value_after": q_after,
        "bootstrap_action_executed_in_environment": False,
    }
    return BoundarySettlementResult(
        method_id="sarsa",
        policy_id=SETTLEMENT_POLICY_ID,
        no_op=False,
        deferred_state_present=True,
        pre_learner_state_sha256=pre_sha,
        post_learner_state_sha256=learner.state_sha256(),
        pre_counters=pre_counters,
        post_counters=post_counters,
        environment_interactions_consumed=0,
        details=details,
    )
