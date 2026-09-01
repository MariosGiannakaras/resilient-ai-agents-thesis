"""Protocol-v2.1 passive temporal evidence for SB3 Phase B.

The historical SB3 branch driver remains untouched.  This adapter replaces only
its environment facade with a reward-recording subclass.  Adaptive DQN/PPO
still execute through the inherited single method-native learning call, so the
32-interaction evidence windows never become learner update boundaries.
"""
from __future__ import annotations

from collections.abc import Sequence

from .environment import EnvironmentSeeds
from .protocol_v2 import ProtocolV2Branch
from .protocol_v2_gridworld import GridWorldScientificStateAdapter
from .protocol_v2_multi_episode import PersistentMultiEpisodeBranchGridWorldEnv
from .protocol_v2_sb3 import SB3ScientificStateAdapter
from .protocol_v2_sb3_phase_b import SB3PhaseBBranchDriver
from .protocol_v2_temporal import FixedRewardWindowRecorder, RewardWindow


class TemporalPersistentMultiEpisodeBranchGridWorldEnv(
    PersistentMultiEpisodeBranchGridWorldEnv
):
    """Observe fixed reward windows without changing continuation control flow."""

    def __init__(
        self,
        branch: GridWorldScientificStateAdapter,
        *,
        subsequent_episode_seeds: Sequence[EnvironmentSeeds],
        window_size: int = 32,
    ) -> None:
        super().__init__(
            branch,
            subsequent_episode_seeds=subsequent_episode_seeds,
        )
        self._reward_recorder = FixedRewardWindowRecorder(window_size=window_size)

    @property
    def reward_windows(self) -> tuple[RewardWindow, ...]:
        return self._reward_recorder.completed_windows

    def require_complete_reward_windows(self, *, total_interactions: int) -> None:
        self._reward_recorder.require_complete(total_interactions=total_interactions)

    def step(self, action):
        result = super().step(action)
        self._reward_recorder.record(float(result[1]))
        return result


class SB3PhaseBBranchDriverV21(SB3PhaseBBranchDriver):
    """SB3 v2.1 branch driver with observational 32-interaction reward windows."""

    def __init__(
        self,
        *,
        branch: ProtocolV2Branch,
        adaptive: bool,
        learner: SB3ScientificStateAdapter,
        environment: GridWorldScientificStateAdapter,
        deterministic_inference: bool,
        subsequent_episode_seeds: Sequence[EnvironmentSeeds] = (),
    ) -> None:
        super().__init__(
            branch=branch,
            adaptive=adaptive,
            learner=learner,
            environment=environment,
            deterministic_inference=deterministic_inference,
            subsequent_episode_seeds=subsequent_episode_seeds,
        )
        # The inherited constructor has not executed any environment interaction.
        # Replacing only the continuation facade therefore cannot affect the
        # branch point, learner state, action sequence, or method-native cadence.
        self._continuation = TemporalPersistentMultiEpisodeBranchGridWorldEnv(
            environment,
            subsequent_episode_seeds=subsequent_episode_seeds,
            window_size=32,
        )
        if adaptive:
            # The inherited adaptive path calls learn_to_total_interactions once.
            self.learner.environment_factory = lambda: self._continuation

    @property
    def reward_windows(self) -> tuple[RewardWindow, ...]:
        return self._continuation.reward_windows

    def require_complete_reward_windows(self, *, total_interactions: int) -> None:
        self._continuation.require_complete_reward_windows(
            total_interactions=total_interactions
        )
