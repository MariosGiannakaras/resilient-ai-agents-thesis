from __future__ import annotations

import unittest
from dataclasses import replace

try:
    from stable_baselines3 import DQN, PPO

    from resilient_agents.environment import EnvironmentSeeds
    from resilient_agents.gridworld import GridAction, GridWorldEnvironment
    from resilient_agents.protocol_v2 import ProtocolV2Branch
    from resilient_agents.protocol_v2_executor import execute_phase_b
    from resilient_agents.protocol_v2_gridworld import GridWorldScientificStateAdapter
    from resilient_agents.protocol_v2_sb3 import dqn_state_adapter, ppo_state_adapter
    from resilient_agents.protocol_v2_sb3_gridworld import (
        BranchContinuationGridWorldEnv,
        ExplicitSeededGridWorldEnv,
    )
    from resilient_agents.protocol_v2_sb3_phase_b import (
        SB3PhaseBBranchDriver,
        _frozen_learning_state,
    )
    from tests.test_gridworld import fixture_spec

    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False


@unittest.skipUnless(_SB3_AVAILABLE, "protocol-v2-pilot dependency group not installed")
class ProtocolV2SB3GridWorldPhaseBTests(unittest.TestCase):
    def _nominal_and_disturbed(self):
        base_nominal = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=20,
            include_change=False,
        )
        grid = {
            "grid": {
                "width": 10,
                "height": 10,
                "start": [0, 0],
                "goal": [9, 9],
                "obstacles": [],
            }
        }
        nominal = replace(
            base_nominal,
            scenario_id="sb3-long-nominal",
            initial_state_spec=grid,
        )
        base_disturbed = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=20,
            include_change=True,
        )
        disturbed = replace(
            base_disturbed,
            scenario_id="sb3-long-disturbed",
            initial_state_spec=grid,
        )
        return nominal, disturbed

    def _episode_seeds(self, count=8):
        return tuple(
            EnvironmentSeeds(
                scenario=1000 + index,
                environment=2000 + index,
                action_disturbance=3000 + index,
                observation_disturbance=4000 + index,
            )
            for index in range(count)
        )

    def _branch_point(self):
        nominal, disturbed = self._nominal_and_disturbed()
        source = GridWorldEnvironment(nominal)
        source.reset(seeds=self._episode_seeds(1)[0])
        source.step(GridAction.RIGHT)
        source.step(GridAction.RIGHT)
        return source, GridWorldScientificStateAdapter(source), nominal, disturbed

    def _dqn_adapter(self):
        nominal, _ = self._nominal_and_disturbed()
        env = ExplicitSeededGridWorldEnv(
            scenario=nominal,
            episode_seeds=self._episode_seeds(),
        )
        model = DQN(
            "MlpPolicy",
            env,
            learning_rate=1e-3,
            buffer_size=64,
            learning_starts=0,
            batch_size=2,
            gamma=0.9,
            train_freq=1,
            gradient_steps=1,
            target_update_interval=2,
            exploration_fraction=1.0,
            exploration_initial_eps=0.2,
            exploration_final_eps=0.1,
            policy_kwargs={"net_arch": [8]},
            seed=101,
            device="cpu",
            verbose=0,
        )
        configuration = {
            "discount_factor": 0.9,
            "learning_rate": 1e-3,
            "buffer_size": 64,
            "learning_starts": 0,
            "batch_size": 2,
            "train_freq": 1,
            "gradient_steps": 1,
            "target_update_interval": 2,
            "exploration_fraction": 1.0,
            "exploration_initial_eps": 0.2,
            "exploration_final_eps": 0.1,
            "net_arch": [8],
            "seed": 101,
        }
        adapter = dqn_state_adapter(
            model,
            configuration=configuration,
            environment_factory=lambda: ExplicitSeededGridWorldEnv(
                scenario=nominal,
                episode_seeds=self._episode_seeds(),
            ),
        )
        adapter.learn_to_total_interactions(4)
        return adapter

    def _ppo_adapter(self):
        nominal, _ = self._nominal_and_disturbed()
        env = ExplicitSeededGridWorldEnv(
            scenario=nominal,
            episode_seeds=self._episode_seeds(),
        )
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=1e-3,
            n_steps=4,
            batch_size=2,
            n_epochs=1,
            gamma=0.9,
            policy_kwargs={"net_arch": {"pi": [8], "vf": [8]}},
            seed=201,
            device="cpu",
            verbose=0,
        )
        configuration = {
            "discount_factor": 0.9,
            "learning_rate": 1e-3,
            "n_steps": 4,
            "batch_size": 2,
            "n_epochs": 1,
            "net_arch": {"pi": [8], "vf": [8]},
            "seed": 201,
        }
        adapter = ppo_state_adapter(
            model,
            configuration=configuration,
            environment_factory=lambda: ExplicitSeededGridWorldEnv(
                scenario=nominal,
                episode_seeds=self._episode_seeds(),
            ),
        )
        adapter.learn_to_total_interactions(4)
        return adapter

    def test_explicit_gridworld_env_keeps_algorithm_and_environment_seeds_independent(self):
        nominal, _ = self._nominal_and_disturbed()
        declared = EnvironmentSeeds(11, 22, 33, 44)
        env = ExplicitSeededGridWorldEnv(
            scenario=nominal,
            episode_seeds=(declared,),
        )
        env.reset(seed=999)
        self.assertEqual(env.environment.gym_env._seeds, declared)
        env.close()

    def test_branch_continuation_reset_is_attachment_only_and_second_reset_fails(self):
        source, branch_point, nominal, _ = self._branch_point()
        branch = branch_point.fork_into(nominal)
        before = branch.state_sha256()
        wrapper = BranchContinuationGridWorldEnv(branch)
        observation, info = wrapper.reset(seed=123)
        self.assertEqual(info, {})
        self.assertEqual(
            observation,
            branch.environment.gym_env.last_transition.delivered_observation,
        )
        self.assertEqual(branch.state_sha256(), before)
        with self.assertRaisesRegex(RuntimeError, "environment reset"):
            wrapper.reset()
        source.close()
        branch.environment.close()

    def test_frozen_dqn_preserves_model_optimizer_replay_and_counters(self):
        source, branch_point, nominal, _ = self._branch_point()
        learner = self._dqn_adapter().clone()
        before = _frozen_learning_state(learner)
        branch = branch_point.fork_into(nominal)
        driver = SB3PhaseBBranchDriver(
            branch=ProtocolV2Branch.FROZEN_NOMINAL,
            adaptive=False,
            learner=learner,
            environment=branch,
            deterministic_inference=True,
        )
        driver.run_to_interaction(1)
        self.assertEqual(_frozen_learning_state(learner), before)
        self.assertEqual(driver.interactions, 1)
        source.close()
        branch.environment.close()

    def test_ppo_four_branch_executor_resumes_learning_from_exact_prefix(self):
        source, branch_point, nominal, disturbed = self._branch_point()
        execution = execute_phase_b(
            learner=self._ppo_adapter(),
            shared_environment=branch_point,
            nominal_spec=nominal,
            disturbed_spec=disturbed,
            interaction_budget_per_branch=4,
            driver_factory=lambda branch, adaptive, learner, environment: (
                SB3PhaseBBranchDriver(
                    branch=branch,
                    adaptive=adaptive,
                    learner=learner,
                    environment=environment,
                    deterministic_inference=True,
                )
            ),
        )
        results = {item.branch: item for item in execution.results}
        self.assertEqual(set(results), set(ProtocolV2Branch))
        for branch in ProtocolV2Branch:
            self.assertEqual(results[branch].interactions, 4)
        self.assertEqual(results[ProtocolV2Branch.FROZEN_NOMINAL].metrics["adaptive"], 0.0)
        self.assertEqual(results[ProtocolV2Branch.ADAPTIVE_NOMINAL].metrics["adaptive"], 1.0)
        self.assertEqual(results[ProtocolV2Branch.FROZEN_DISTURBED].metrics["adaptive"], 0.0)
        self.assertEqual(results[ProtocolV2Branch.ADAPTIVE_DISTURBED].metrics["adaptive"], 1.0)
        source.close()

    def test_ppo_adaptive_multi_episode_uses_declared_resets_without_clock_reset(self):
        source, branch_point, nominal, _ = self._branch_point()
        learner = self._ppo_adapter().clone()
        branch = branch_point.fork_into(nominal)
        driver = SB3PhaseBBranchDriver(
            branch=ProtocolV2Branch.ADAPTIVE_NOMINAL,
            adaptive=True,
            learner=learner,
            environment=branch,
            deterministic_inference=True,
            subsequent_episode_seeds=self._episode_seeds(8),
        )
        base = int(learner.model.num_timesteps)
        metrics = driver.run_to_interaction(24)
        self.assertEqual(driver.interactions, 24)
        self.assertEqual(int(learner.model.num_timesteps), base + 24)
        self.assertGreaterEqual(metrics["episodes_started"], 2.0)
        self.assertGreaterEqual(metrics["episodes_completed"], 1.0)
        source.close()
        branch.environment.close()


if __name__ == "__main__":
    unittest.main()
