from __future__ import annotations

import unittest
from dataclasses import replace

from resilient_agents.gridworld import GridAction, GridWorldEnvironment
from resilient_agents.protocol_v2_gridworld import GridWorldScientificStateAdapter
from tests.test_gridworld import fixture_seeds, fixture_spec


class ProtocolV2GridWorldStateTests(unittest.TestCase):
    def test_exact_mid_episode_restore_preserves_future_stochastic_trace(self):
        spec = fixture_spec(
            action_failure=0.5,
            observation_corruption=0.5,
            max_steps=8,
            include_change=False,
        )
        source = GridWorldEnvironment(spec)
        source.reset(seeds=fixture_seeds(action=7, observation=11))
        source.step(GridAction.RIGHT)
        source.step(GridAction.DOWN)
        adapter = GridWorldScientificStateAdapter(source)
        snapshot = adapter.export_state()

        restored_environment = GridWorldEnvironment(spec)
        restored = GridWorldScientificStateAdapter(restored_environment)
        restored.restore_state(snapshot)
        self.assertEqual(adapter.state_sha256(), restored.state_sha256())

        future_actions = [GridAction.RIGHT, GridAction.DOWN, GridAction.LEFT]
        source_trace = []
        restored_trace = []
        for action in future_actions:
            source_transition = source.step(action)
            restored_transition = restored_environment.step(action)
            source_trace.append(source_transition)
            restored_trace.append(restored_transition)
            if source_transition.terminated or source_transition.truncated:
                break
        self.assertEqual(source_trace, restored_trace)
        self.assertEqual(adapter.state_sha256(), restored.state_sha256())
        source.close()
        restored_environment.close()

    def test_shared_prefix_forks_to_nominal_and_action_remap_at_exact_boundary(self):
        nominal_spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=False,
        )
        disturbed_spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=True,
        )
        source = GridWorldEnvironment(nominal_spec)
        source.reset(seeds=fixture_seeds())
        source.step(GridAction.RIGHT)
        prefix_last = source.step(GridAction.RIGHT)
        self.assertEqual(source.debug_state()["step"], 2)

        branch_point = GridWorldScientificStateAdapter(source)
        nominal = branch_point.fork_into(nominal_spec)
        disturbed = branch_point.fork_into(disturbed_spec)
        self.assertEqual(
            nominal.environment.gym_env.last_transition,
            disturbed.environment.gym_env.last_transition,
        )
        self.assertEqual(nominal.environment.gym_env.last_transition, prefix_last)
        self.assertEqual(
            nominal.environment.debug_state()["position"],
            disturbed.environment.debug_state()["position"],
        )

        nominal_next = nominal.environment.step(GridAction.RIGHT)
        disturbed_next = disturbed.environment.step(GridAction.RIGHT)
        self.assertEqual(nominal_next.executed_action, "right")
        self.assertEqual(disturbed_next.executed_action, "down")
        self.assertEqual(
            disturbed_next.change_event_ids,
            ("persistent-right-to-down",),
        )
        self.assertNotEqual(nominal_next.true_state, disturbed_next.true_state)
        source.close()
        nominal.environment.close()
        disturbed.environment.close()

    def test_fork_can_activate_action_failure_only_after_shared_prefix(self):
        nominal_spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=False,
        )
        failed_spec = replace(
            nominal_spec,
            scenario_id="phase-b-action-failure",
            action_disturbance_spec={
                "type": "no-op-failure",
                "failure_probability": 1.0,
            },
        )
        source = GridWorldEnvironment(nominal_spec)
        source.reset(seeds=fixture_seeds())
        prefix = source.step(GridAction.RIGHT)
        self.assertFalse(prefix.disturbance_flags["action_failure"])

        branch_point = GridWorldScientificStateAdapter(source)
        nominal = branch_point.fork_into(nominal_spec)
        failed = branch_point.fork_into(failed_spec)
        nominal_next = nominal.environment.step(GridAction.RIGHT)
        failed_next = failed.environment.step(GridAction.RIGHT)
        self.assertFalse(nominal_next.disturbance_flags["action_failure"])
        self.assertTrue(failed_next.disturbance_flags["action_failure"])
        self.assertEqual(failed_next.executed_action, "noop")
        source.close()
        nominal.environment.close()
        failed.environment.close()

    def test_fork_rejects_task_change_or_misaligned_action_remap(self):
        source_spec = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=False,
        )
        source = GridWorldEnvironment(source_spec)
        source.reset(seeds=fixture_seeds())
        source.step(GridAction.RIGHT)
        source.step(GridAction.RIGHT)
        branch_point = GridWorldScientificStateAdapter(source)

        changed_reward = replace(
            source_spec,
            scenario_id="changed-reward",
            reward_spec={"step": -0.2, "collision": -0.25, "goal": 1.0},
        )
        with self.assertRaises(ValueError):
            branch_point.fork_into(changed_reward)

        remap = fixture_spec(
            action_failure=0.0,
            observation_corruption=0.0,
            max_steps=8,
            include_change=True,
        )
        late_event = replace(remap.change_events[0], onset_step=3)
        late_remap = replace(
            remap,
            scenario_id="late-remap",
            change_events=(late_event,),
        )
        with self.assertRaises(ValueError):
            branch_point.fork_into(late_remap)
        source.close()


if __name__ == "__main__":
    unittest.main()
