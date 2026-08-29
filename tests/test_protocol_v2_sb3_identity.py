from __future__ import annotations

import base64
import copy
import io
import json
import unittest
from pathlib import Path

try:
    import gymnasium as gym
    import numpy as np
    import torch
    from gymnasium import spaces
    from stable_baselines3 import DQN, PPO

    from resilient_agents.protocol_v2_sb3 import (
        SB3ScientificStateAdapter,
        dqn_state_adapter,
        ppo_state_adapter,
    )
    from resilient_agents.protocol_v2_sb3_identity import (
        diff_canonical_sb3_archives,
        require_scientific_continuation_invariants,
        scientific_continuation_sha256,
    )

    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False


if _SB3_AVAILABLE:

    class _IdentityEnv(gym.Env):
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
            reward = 1.0 if int(action) == self._state % 2 else -0.25
            self._state = (self._state + 1) % 4
            self._steps += 1
            return (
                np.array([float(self._state)], dtype=np.float32),
                reward,
                self._steps >= 4,
                False,
                {},
            )


    def _environment_factory():
        environment = _IdentityEnv()
        environment.reset(seed=7001)
        return environment


@unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
class ProtocolV2SB3IdentityTests(unittest.TestCase):
    DQN_CONFIGURATION = {
        "learning_rate": 1e-3,
        "buffer_size": 64,
        "learning_starts": 0,
        "batch_size": 4,
        "discount_factor": 0.9,
        "train_freq": 1,
        "gradient_steps": 1,
        "target_update_interval": 2,
        "exploration_fraction": 1.0,
        "exploration_initial_eps": 0.5,
        "exploration_final_eps": 0.1,
        "net_arch": [8],
    }
    PPO_CONFIGURATION = {
        "learning_rate": 1e-3,
        "n_steps": 8,
        "batch_size": 4,
        "n_epochs": 1,
        "discount_factor": 0.9,
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "ent_coef": 0.0,
        "vf_coef": 0.5,
        "max_grad_norm": 0.5,
        "net_arch": {"pi": [8], "vf": [8]},
    }

    def _dqn_adapter(self):
        model = DQN(
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
        model.learn(total_timesteps=8, progress_bar=False)
        return dqn_state_adapter(
            model,
            configuration=self.DQN_CONFIGURATION,
            environment_factory=_environment_factory,
        )

    def _ppo_adapter(self):
        model = PPO(
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
        model.learn(total_timesteps=8, progress_bar=False)
        return ppo_state_adapter(
            model,
            configuration=self.PPO_CONFIGURATION,
            environment_factory=_environment_factory,
        )

    def _restored_dqn(self, state):
        target = self._dqn_adapter()
        target.restore_state(state)
        return target

    def test_runtime_metadata_changes_raw_archive_but_not_scientific_identity(self):
        adapter = self._dqn_adapter()
        first = adapter.export_state()
        historical_sha = adapter.state_sha256()
        continuation_sha = scientific_continuation_sha256(adapter)

        adapter.model.start_time = int(adapter.model.start_time) + 1
        second = adapter.export_state()

        self.assertEqual(adapter.state_sha256(), historical_sha)
        self.assertEqual(scientific_continuation_sha256(adapter), continuation_sha)
        self.assertNotEqual(first["model_zip_b64"], second["model_zip_b64"])
        self.assertNotEqual(
            json.dumps(first, sort_keys=True, separators=(",", ":")).encode(),
            json.dumps(second, sort_keys=True, separators=(",", ":")).encode(),
        )
        archive_diff = diff_canonical_sb3_archives(
            base64.b64decode(first["model_zip_b64"]),
            base64.b64decode(second["model_zip_b64"]),
        )
        self.assertEqual(
            [item["path"] for item in archive_diff["member_differences"]],
            ["data"],
        )
        self.assertEqual(
            archive_diff["data_field_differences"],
            [
                {
                    "path": "start_time",
                    "first": {
                        "kind": "int",
                        "value": int(adapter.model.start_time) - 1,
                    },
                    "second": {"kind": "int", "value": int(adapter.model.start_time)},
                    "classification": "serialization-runtime-metadata-only",
                }
            ],
        )

        for state in (first, second):
            restored = self._restored_dqn(state)
            self.assertEqual(restored.state_sha256(), historical_sha)
            self.assertEqual(
                scientific_continuation_sha256(restored), continuation_sha
            )

    def test_retained_dec052_dqn_restores_exact_historical_identity_and_invariants(self):
        checkpoint_path = (
            Path(__file__).resolve().parents[1]
            / "results"
            / "pilots"
            / "protocol-v2-feasibility-v0.1-recovery"
            / "checkpoints"
            / "dqn"
            / "t526-r01"
            / "gw-l1-a.json"
        )
        state = json.loads(checkpoint_path.read_text(encoding="utf-8"))["state"]
        loaded = DQN.load(
            io.BytesIO(base64.b64decode(state["model_zip_b64"])),
            env=None,
            device="cpu",
            force_reset=False,
        )
        loaded.load_replay_buffer(
            io.BytesIO(base64.b64decode(state["replay_buffer_b64"]))
        )
        adapter = SB3ScientificStateAdapter(
            method_id="dqn",
            model=loaded,
            configuration=state["configuration"],
            rng_state=state["rng_state"],
        )
        adapter.restore_state(state)
        self.assertEqual(
            adapter.state_sha256(),
            "bee1cce1b96fcffbcb9675c2e8175e3c1e1461add75e112ce23369cb87e03897",
        )
        components = require_scientific_continuation_invariants(adapter)
        self.assertEqual(components["counters"]["num_timesteps"], 2048)
        self.assertEqual(
            components["target_and_schedule_state"]["n_calls"], 2048
        )
        self.assertTrue(all(components["invariants"].values()))

    def test_dqn_continuation_relevant_perturbations_fail_the_barrier(self):
        source = self._dqn_adapter()
        state = source.export_state()
        historical_sha = source.state_sha256()
        continuation_sha = scientific_continuation_sha256(source)

        def assert_historical_change(mutator):
            candidate = self._restored_dqn(copy.deepcopy(state))
            mutator(candidate)
            self.assertNotEqual(candidate.state_sha256(), historical_sha)
            try:
                derived_sha = scientific_continuation_sha256(candidate)
            except ValueError:
                return
            self.assertNotEqual(derived_sha, continuation_sha)

        assert_historical_change(
            lambda adapter: next(adapter.model.q_net.parameters()).data.add_(1.0)
        )
        assert_historical_change(
            lambda adapter: next(adapter.model.q_net_target.parameters()).data.add_(1.0)
        )

        def perturb_optimizer(adapter):
            optimizer_state = next(iter(adapter.model.policy.optimizer.state.values()))
            tensor = next(value for value in optimizer_state.values() if torch.is_tensor(value))
            tensor.add_(1.0)

        assert_historical_change(perturb_optimizer)
        assert_historical_change(
            lambda adapter: adapter.model.replay_buffer.observations.__setitem__(
                (0, 0, 0),
                adapter.model.replay_buffer.observations[0, 0, 0] + 1.0,
            )
        )
        assert_historical_change(
            lambda adapter: setattr(
                adapter.model.replay_buffer,
                "pos",
                (int(adapter.model.replay_buffer.pos) + 1)
                % int(adapter.model.replay_buffer.buffer_size),
            )
        )
        assert_historical_change(
            lambda adapter: setattr(
                adapter.model.replay_buffer,
                "full",
                not bool(adapter.model.replay_buffer.full),
            )
        )
        assert_historical_change(
            lambda adapter: setattr(adapter.model, "_n_updates", adapter.model._n_updates + 1)
        )
        assert_historical_change(
            lambda adapter: setattr(
                adapter.model, "exploration_rate", adapter.model.exploration_rate + 0.01
            )
        )

        rng_candidate = self._restored_dqn(copy.deepcopy(state))
        rng_candidate._rng_state["python"][1][0] += 1
        self.assertNotEqual(rng_candidate.state_sha256(), historical_sha)

        action_rng_candidate = self._restored_dqn(copy.deepcopy(state))
        action_rng_candidate._action_space_rng_state["state"]["state"] += 1
        self.assertNotEqual(action_rng_candidate.state_sha256(), historical_sha)

    def test_omitted_dqn_counter_and_schedule_are_independently_guarded(self):
        source = self._dqn_adapter()
        historical_sha = source.state_sha256()
        continuation_sha = scientific_continuation_sha256(source)

        source.model._n_calls += 1
        self.assertEqual(source.state_sha256(), historical_sha)
        with self.assertRaisesRegex(ValueError, "n_calls"):
            require_scientific_continuation_invariants(source)
        source.model._n_calls -= 1

        source.model.exploration_schedule.end += 0.01
        self.assertEqual(source.state_sha256(), historical_sha)
        with self.assertRaisesRegex(ValueError, "exploration"):
            scientific_continuation_sha256(source)

    def test_ppo_identity_covers_policy_optimizer_counters_rng_and_schedules(self):
        source = self._ppo_adapter()
        components = require_scientific_continuation_invariants(source)
        self.assertEqual(components["ppo_boundary_state"]["boundary"], "completed-update")
        state = source.export_state()
        historical_sha = source.state_sha256()

        for mutator in (
            lambda adapter: next(adapter.model.policy.parameters()).data.add_(1.0),
            lambda adapter: setattr(
                adapter.model, "_n_updates", int(adapter.model._n_updates) + 1
            ),
            lambda adapter: adapter._rng_state["python"][1].__setitem__(
                0, adapter._rng_state["python"][1][0] + 1
            ),
        ):
            candidate = self._ppo_adapter()
            candidate.restore_state(copy.deepcopy(state))
            mutator(candidate)
            self.assertNotEqual(candidate.state_sha256(), historical_sha)

        optimizer_candidate = self._ppo_adapter()
        optimizer_candidate.restore_state(copy.deepcopy(state))
        optimizer_state = next(
            iter(optimizer_candidate.model.policy.optimizer.state.values())
        )
        optimizer_tensor = next(
            value for value in optimizer_state.values() if torch.is_tensor(value)
        )
        optimizer_tensor.add_(1.0)
        self.assertNotEqual(optimizer_candidate.state_sha256(), historical_sha)

        schedule_candidate = self._ppo_adapter()
        schedule_candidate.restore_state(copy.deepcopy(state))
        continuation_sha = scientific_continuation_sha256(schedule_candidate)
        schedule_candidate.model.clip_range.value_schedule.val = 0.3
        self.assertEqual(schedule_candidate.state_sha256(), historical_sha)
        self.assertIsInstance(continuation_sha, str)
        with self.assertRaisesRegex(ValueError, "ppo_model_matches"):
            scientific_continuation_sha256(schedule_candidate)


if __name__ == "__main__":
    unittest.main()
