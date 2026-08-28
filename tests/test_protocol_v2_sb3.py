from __future__ import annotations

import unittest

try:
    import gymnasium as gym
    import numpy as np
    from gymnasium import spaces
    from stable_baselines3 import DQN, PPO

    from resilient_agents.protocol_v2_sb3 import (
        SUPPORTED_SB3_VERSION,
        dqn_state_adapter,
        ppo_state_adapter,
    )

    _SB3_AVAILABLE = True
except ImportError:  # optional dependency is intentionally absent from default CI
    _SB3_AVAILABLE = False


if _SB3_AVAILABLE:

    class _TinyDeterministicEnv(gym.Env):
        metadata = {"render_modes": []}

        def __init__(self) -> None:
            super().__init__()
            self.action_space = spaces.Discrete(2)
            self.observation_space = spaces.Box(
                low=np.array([0.0], dtype=np.float32),
                high=np.array([3.0], dtype=np.float32),
                dtype=np.float32,
            )
            self._state = 0
            self._steps = 0

        def reset(self, *, seed=None, options=None):
            super().reset(seed=seed)
            self._state = 0
            self._steps = 0
            return np.array([0.0], dtype=np.float32), {}

        def step(self, action):
            action_value = int(action)
            expected = self._state % 2
            reward = 1.0 if action_value == expected else -0.25
            self._state = (self._state + 1) % 4
            self._steps += 1
            terminated = self._steps >= 4
            observation = np.array([float(self._state)], dtype=np.float32)
            return observation, reward, terminated, False, {}


    def _environment_factory():
        # Scientific branch tests checkpoint only after complete four-step episodes.
        env = _TinyDeterministicEnv()
        env.reset(seed=7001)
        return env


@unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
class ProtocolV2SB3AdapterTests(unittest.TestCase):
    def test_supported_version_is_pinned(self):
        import stable_baselines3 as sb3

        self.assertEqual(sb3.__version__, SUPPORTED_SB3_VERSION)
        self.assertEqual(SUPPORTED_SB3_VERSION, "2.9.0")

    def _dqn(self):
        return DQN(
            "MlpPolicy",
            _environment_factory(),
            learning_rate=1e-3,
            buffer_size=64,
            learning_starts=0,
            batch_size=4,
            tau=1.0,
            gamma=0.9,
            train_freq=1,
            gradient_steps=1,
            target_update_interval=2,
            exploration_fraction=1.0,
            exploration_initial_eps=0.5,
            exploration_final_eps=0.1,
            policy_kwargs={"net_arch": [8]},
            seed=12345,
            device="cpu",
            verbose=0,
        )

    def _ppo(self):
        return PPO(
            "MlpPolicy",
            _environment_factory(),
            learning_rate=1e-3,
            n_steps=8,
            batch_size=4,
            n_epochs=1,
            gamma=0.9,
            gae_lambda=0.95,
            clip_range=0.2,
            ent_coef=0.0,
            vf_coef=0.5,
            max_grad_norm=0.5,
            policy_kwargs={"net_arch": {"pi": [8], "vf": [8]}},
            seed=54321,
            device="cpu",
            verbose=0,
        )

    def test_dqn_bundle_persists_replay_rng_optimizer_and_exact_continuation(self):
        config = {
            "learning_rate": 1e-3,
            "buffer_size": 64,
            "learning_starts": 0,
            "batch_size": 4,
            "gamma": 0.9,
            "train_freq": 1,
            "gradient_steps": 1,
            "target_update_interval": 2,
            "exploration_fraction": 1.0,
            "exploration_initial_eps": 0.5,
            "exploration_final_eps": 0.1,
            "net_arch": [8],
            "seed": 12345,
        }
        model = self._dqn()
        model.learn(total_timesteps=8, progress_bar=False)
        adapter = dqn_state_adapter(
            model,
            configuration=config,
            environment_factory=_environment_factory,
        )

        saved = adapter.export_state()
        self.assertEqual(saved["method_id"], "dqn")
        self.assertTrue(saved["model_zip_b64"])
        self.assertTrue(saved["replay_buffer_b64"])
        self.assertEqual(saved["counters"]["num_timesteps"], 8)
        self.assertGreater(saved["counters"]["replay_pos"], 0)

        clone = adapter.clone()
        self.assertEqual(adapter.state_sha256(), clone.state_sha256())

        adapter.learn_to_total_interactions(12)
        clone.learn_to_total_interactions(12)
        self.assertEqual(adapter.state_sha256(), clone.state_sha256())
        self.assertEqual(adapter.model.num_timesteps, 12)
        self.assertEqual(clone.model.num_timesteps, 12)

    def test_ppo_checkpoint_requires_completed_rollout_and_exact_continuation(self):
        config = {
            "learning_rate": 1e-3,
            "n_steps": 8,
            "batch_size": 4,
            "n_epochs": 1,
            "gamma": 0.9,
            "gae_lambda": 0.95,
            "clip_range": 0.2,
            "ent_coef": 0.0,
            "vf_coef": 0.5,
            "max_grad_norm": 0.5,
            "net_arch": {"pi": [8], "vf": [8]},
            "seed": 54321,
        }
        model = self._ppo()
        model.learn(total_timesteps=8, progress_bar=False)
        adapter = ppo_state_adapter(
            model,
            configuration=config,
            environment_factory=_environment_factory,
        )
        saved = adapter.export_state()
        self.assertEqual(saved["method_id"], "ppo")
        self.assertIsNone(saved["replay_buffer_b64"])
        self.assertEqual(saved["counters"]["rollout_boundary"], "completed-update")
        self.assertEqual(saved["counters"]["rollout_buffer_size"], 8)

        clone = adapter.clone()
        self.assertEqual(adapter.state_sha256(), clone.state_sha256())
        with self.assertRaises(ValueError):
            adapter.learn_to_total_interactions(12)

        adapter.learn_to_total_interactions(16)
        clone.learn_to_total_interactions(16)
        self.assertEqual(adapter.state_sha256(), clone.state_sha256())
        self.assertEqual(adapter.model.num_timesteps, 16)

    def test_configuration_mismatch_is_rejected_on_restore(self):
        model = self._dqn()
        model.learn(total_timesteps=4, progress_bar=False)
        source = dqn_state_adapter(
            model,
            configuration={"contract": "source"},
            environment_factory=_environment_factory,
        )
        state = source.export_state()
        target = dqn_state_adapter(
            self._dqn(),
            configuration={"contract": "different"},
            environment_factory=_environment_factory,
        )
        with self.assertRaises(ValueError):
            target.restore_state(state)


if __name__ == "__main__":
    unittest.main()
