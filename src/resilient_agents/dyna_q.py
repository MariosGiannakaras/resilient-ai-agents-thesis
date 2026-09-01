"""Plain tabular Dyna-Q built on the validated Dyna-Q+ machinery.

The intended scientific contrast is deliberately narrow: Dyna-Q plans only
from state/action pairs that have been experienced for real and applies no
recency bonus.  Dyna-Q+ additionally creates default models for untried actions
in visited states and adds the recency-directed planning bonus.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .dyna_q_plus import DynaQPlusAgent, DynaQPlusConfig

DYNA_Q_STATE_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class DynaQConfig:
    """Explicit configuration for plain Dyna-Q."""

    agent_id: str
    actions: Sequence[Any]
    learning_rate: float
    discount_factor: float
    exploration_epsilon: float
    planning_steps: int
    bootstrap_on_truncation: bool
    initial_q_value: float

    def to_plus_config(self) -> DynaQPlusConfig:
        return DynaQPlusConfig(
            agent_id=self.agent_id,
            actions=self.actions,
            learning_rate=self.learning_rate,
            discount_factor=self.discount_factor,
            exploration_epsilon=self.exploration_epsilon,
            planning_steps=self.planning_steps,
            kappa=0.0,
            bootstrap_on_truncation=self.bootstrap_on_truncation,
            initial_q_value=self.initial_q_value,
        )

    def __post_init__(self) -> None:
        # Reuse all validated numeric/action checks from the shared Dyna config.
        self.to_plus_config()


class DynaQAgent(DynaQPlusAgent):
    """Dyna-Q: empirical-model planning without Dyna-Q+ re-exploration."""

    def __init__(
        self,
        config: DynaQConfig,
        *,
        checkpoint: Mapping[str, Any] | None,
    ) -> None:
        if not isinstance(config, DynaQConfig):
            raise ValueError("config must be DynaQConfig")
        self.strategy_config = config
        super().__init__(config.to_plus_config(), checkpoint=checkpoint)

    def _ensure_state_model(self, state_key: str) -> None:
        """Plain Dyna-Q has no synthetic model for untried actions.

        Real state/action pairs are inserted by the inherited
        ``_record_real_model`` method after an actual transition is observed.
        Planning therefore samples only experienced pairs.
        """
        del state_key

    def get_state(self) -> Mapping[str, Any]:
        state = dict(super().get_state())
        state["schema_version"] = DYNA_Q_STATE_SCHEMA_VERSION
        state["method"] = "dyna_q_v1"
        return state

    def restore_state(self, state: Mapping[str, Any]) -> None:
        if not isinstance(state, Mapping):
            raise ValueError("state must be an object")
        if state.get("schema_version") != DYNA_Q_STATE_SCHEMA_VERSION:
            raise ValueError("unsupported Dyna-Q state schema_version")
        if state.get("agent_id") != self.agent_id or state.get("method") != "dyna_q_v1":
            raise ValueError("state identity does not match Dyna-Q configuration")
        translated = dict(state)
        translated["method"] = "dyna_q_plus_v1"
        super().restore_state(translated)
