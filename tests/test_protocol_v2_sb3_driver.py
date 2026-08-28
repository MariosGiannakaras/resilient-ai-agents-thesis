from __future__ import annotations

import unittest

try:
    import gymnasium as gym
    import numpy as np
    from gymnasium import spaces
    from stable_baselines3 import DQN, PPO

    from resilient_agents.protocol_v2 import ProtocolV2TaskSemantics
    from resilient_agents.protocol_v2_executor import execute_phase_a
    from resilient_agents.protocol_v2_runtime import (
        NoLearningProbePlan,
        PhaseARequest,
        ProtocolV2MethodConfig,
        ProtocolV2RootIdentity,
    )
    from resilient_agents.protocol_v2_sb3 import dqn_state_adapter, ppo_state_adapter
    from resilient_agents.protocol_v2_sb3_driver import (
        SB3_IMPLEMENTATION_ID,
        SB3NoLearningProbeEvaluator,
        SB3PhaseADriver,
    )

    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False


if _SB3_AVAILABLE:

    class _ProbeEnv(gym.Env):
        metadata = {"render_modes": []}

        def __init__(self):
            super().__init__()
            self.action_space = spaces.Discrete(2)
            self.observation_space = spaces.Box(
                low=np.array([0.0], dtype=np.float32),
                high=np.array([2.0], dtype=np.float32),
                dtype=np.float32,
            )
            self._step = 0

        def reset(self, *, seed=None, options=None):
            super().reset(seed=seed)
            self._step = 0
            return np.array([0.0], dtype=np.float32), {}

        def step(self, action):
            self._step += 1
            terminated = self._step >= 2
            return (
                np.array([float(self._step)], dtype=np.float32),
                1.0 if int(action) == 0 else 0.0,
                terminated,
                False,
                {},
            )


    def _env_factory():
        return _ProbeEnv()


@unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
class ProtocolV2SB3DriverTests(unittest.TestCase):
    def _root(self):
        return ProtocolV2RootIdentity(
            root_id="root-sb3-driver",
            initialization_seed=101,
            exploration_seed=102,
            scenario_seed=103,
            environment_seed=104,
            action_disturbance_seed=105,
            observation_disturbance_seed=106,
        )

    def test_dqn_runs_through_generic_phase_a_executor_with_isolated_probes(self):
        model = DQN(
            "MlpPolicy",
            _env_factory(),
            learning_rate=1e-3,
            buffer_size=32,
            learning_starts=0,
            batch_size=2,
            gamma=0.9,
            train_freq=1,
            gradient_steps=1,
            target_update_interval=2,
            exploration_fraction=1.0,
            exploration_initial_eps=0.5,
            exploration_final_eps=0.1,
            policy_kwargs={"net_arch": [8]},
            seed=101,
            device="cpu",
            verbose=0,
        )
        parameters = {
            "discount_factor": 0.9,
            "bootstrap_on_truncation": True,
            "learning_rate": 1e-3,
            "buffer_size": 32,
            "learning_starts": 0,
            "batch_size": 2,
            "train_freq": 1,
            "gradient_steps": 1,
            "target_update_interval": 2,
            "exploration_fraction": 1.0,
            "exploration_initial_eps": 0.5,
            "exploration_final_eps": 0.1,
            "net_arch": [8],
            "seed": 101,
        }
        adapter = dqn_state_adapter(
            model,
            configuration=parameters,
            environment_factory=_env_factory,
        )
        driver = SB3PhaseADriver(adapter)
        request = PhaseARequest(
            protocol_version="protocol-v2.0-candidate",
            experiment_id="dqn-phase-a-driver",
            layout_id="tiny",
            root=self._root(),
            task=ProtocolV2TaskSemantics(
                gamma=0.9,
                reward_contract={"step": 0.0, "goal": 1.0},
            ),
            method=ProtocolV2MethodConfig(
                method_id="dqn",
                implementation_id=SB3_IMPLEMENTATION_ID,
                parameters=parameters,
            ),
            training_interaction_budget=4,
            probe_plan=NoLearningProbePlan(
                interaction_indices=(0, 2, 4),
                episodes_per_probe=2,
            ),
        )
        evaluator = SB3NoLearningProbeEvaluator(
            environment_factory=_env_factory,
            episode_seeds=(201, 202),
            deterministic=True,
        )
        execution = execute_phase_a(
            request,
            driver=driver,
            probe_evaluator=evaluator,
            checkpoint_provenance={"test": "sb3-driver"},
        )
        self.assertEqual(execution.result.ledger.training_interactions, 4)
        self.assertEqual(execution.result.ledger.probe_interactions, 12)
        self.assertEqual(model.num_timesteps, 4)
        self.assertEqual(len(execution.result.probes), 3)
        self.assertEqual(
            execution.result.final_checkpoint.provenance["implementation_id"],
            SB3_IMPLEMENTATION_ID,
        )

    def test_ppo_driver_preserves_rollout_boundary_requirement(self):
        model = PPO(
            "MlpPolicy",
            _env_factory(),
            learning_rate=1e-3,
            n_steps=4,
            batch_size=2,
            n_epochs=1,
            gamma=0.9,
            policy_kwargs={"net_arch": {"pi": [8], "vf": [8]}},
            seed=301,
            device="cpu",
            verbose=0,
        )
        adapter = ppo_state_adapter(
            model,
            configuration={"discount_factor": 0.9, "n_steps": 4, "seed": 301},
            environment_factory=_env_factory,
        )
        driver = SB3PhaseADriver(adapter)
        with self.assertRaisesRegex(ValueError, "rollout/update boundaries"):
            driver.train_to_interaction(2)
        driver.train_to_interaction(4)
        self.assertEqual(driver.training_interactions, 4)

    def test_probe_requires_explicit_sufficient_unique_seeds(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            SB3NoLearningProbeEvaluator(
                environment_factory=_env_factory,
                episode_seeds=(1, 1),
                deterministic=True,
            )


if __name__ == "__main__":
    unittest.main()
