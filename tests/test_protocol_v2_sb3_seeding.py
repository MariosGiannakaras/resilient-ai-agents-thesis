from __future__ import annotations

import copy
import unittest
from collections.abc import Mapping

try:
    import gymnasium as gym
    import numpy as np
    import torch
    from gymnasium import spaces
    from stable_baselines3 import DQN

    from resilient_agents.protocol_v2_sb3 import dqn_state_adapter
    from resilient_agents.protocol_v2_sb3_seeding import reseed_sb3_behavior_rng

    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False


if _SB3_AVAILABLE:

    class _SeedEnv(gym.Env):
        metadata = {"render_modes": []}

        def __init__(self):
            super().__init__()
            self.action_space = spaces.Discrete(2)
            self.observation_space = spaces.Box(
                low=np.array([0.0], dtype=np.float32),
                high=np.array([1.0], dtype=np.float32),
                dtype=np.float32,
            )

        def reset(self, *, seed=None, options=None):
            super().reset(seed=seed)
            return np.array([0.0], dtype=np.float32), {}

        def step(self, action):
            return np.array([0.0], dtype=np.float32), 0.0, False, True, {}


    def _model(initialization_seed: int):
        return DQN(
            "MlpPolicy",
            _SeedEnv(),
            learning_rate=1e-3,
            buffer_size=16,
            learning_starts=0,
            batch_size=2,
            gamma=0.9,
            train_freq=1,
            gradient_steps=1,
            target_update_interval=2,
            policy_kwargs={"net_arch": [8]},
            seed=initialization_seed,
            device="cpu",
            verbose=0,
        )


@unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
class ProtocolV2SB3SeedingTests(unittest.TestCase):
    def assert_nested_parameter_equal(self, first, second):
        if isinstance(first, Mapping):
            self.assertIsInstance(second, Mapping)
            self.assertEqual(set(first), set(second))
            for key in first:
                self.assert_nested_parameter_equal(first[key], second[key])
            return
        if torch.is_tensor(first):
            self.assertTrue(torch.equal(first, second))
            return
        self.assertEqual(first, second)

    def test_behavior_reseed_preserves_initialized_parameters_and_changes_rng_state(self):
        model = _model(101)
        adapter = dqn_state_adapter(
            model,
            configuration={"initialization_seed": 101},
            environment_factory=_SeedEnv,
        )
        before_parameters = copy.deepcopy(model.get_parameters())
        before_rng = copy.deepcopy(adapter.export_state()["rng_state"])

        reseed_sb3_behavior_rng(adapter, exploration_seed=202)

        self.assert_nested_parameter_equal(before_parameters, model.get_parameters())
        self.assertNotEqual(adapter.export_state()["rng_state"], before_rng)

    def test_same_initialization_seed_same_parameters_but_distinct_behavior_streams(self):
        first_model = _model(303)
        second_model = _model(303)
        first = dqn_state_adapter(
            first_model,
            configuration={"initialization_seed": 303},
            environment_factory=_SeedEnv,
        )
        second = dqn_state_adapter(
            second_model,
            configuration={"initialization_seed": 303},
            environment_factory=_SeedEnv,
        )
        reseed_sb3_behavior_rng(first, exploration_seed=401)
        reseed_sb3_behavior_rng(second, exploration_seed=402)

        self.assert_nested_parameter_equal(
            first_model.get_parameters(),
            second_model.get_parameters(),
        )
        self.assertNotEqual(
            first.export_state()["rng_state"],
            second.export_state()["rng_state"],
        )
        self.assertNotEqual(first.state_sha256(), second.state_sha256())

    def test_invalid_behavior_seed_fails_closed(self):
        adapter = dqn_state_adapter(
            _model(505),
            configuration={"initialization_seed": 505},
            environment_factory=_SeedEnv,
        )
        with self.assertRaises(ValueError):
            reseed_sb3_behavior_rng(adapter, exploration_seed=-1)


if __name__ == "__main__":
    unittest.main()
