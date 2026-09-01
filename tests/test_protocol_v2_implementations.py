from __future__ import annotations

import unittest

from resilient_agents.protocol_v2_implementations import (
    PROJECT_STATE_ADAPTER_VERSION,
    resolved_core_method_registry,
    resolved_implementation_provenance,
)


class ProtocolV2ImplementationRegistryTests(unittest.TestCase):
    def test_all_core_candidates_have_concrete_non_pending_implementations(self):
        registry = resolved_core_method_registry()
        self.assertEqual(
            registry.method_ids(),
            ("dqn", "dyna_q_plus", "ppo", "q_learning", "sarsa"),
        )
        for method_id in registry.method_ids():
            registration = registry.get(method_id)
            self.assertNotIn("pending", registration.implementation_id)
            self.assertTrue(registration.implementation_version)

    def test_deep_methods_are_pinned_to_sb3_2_9_0_adapter(self):
        registry = resolved_core_method_registry()
        for method_id in ("dqn", "ppo"):
            registration = registry.get(method_id)
            self.assertEqual(
                registration.implementation_id,
                "stable-baselines3-scientific-state-adapter",
            )
            self.assertEqual(registration.implementation_version, "2.9.0")

    def test_project_methods_use_exact_state_adapter_version(self):
        registry = resolved_core_method_registry()
        for method_id in ("q_learning", "sarsa", "dyna_q_plus"):
            registration = registry.get(method_id)
            self.assertEqual(
                registration.implementation_id,
                "project-protocol-v2-state-adapter",
            )
            self.assertEqual(
                registration.implementation_version,
                PROJECT_STATE_ADAPTER_VERSION,
            )

    def test_provenance_helper_is_complete(self):
        provenance = resolved_implementation_provenance("dqn")
        self.assertEqual(provenance["method_id"], "dqn")
        self.assertEqual(provenance["implementation_version"], "2.9.0")
        self.assertIn("implementation_id", provenance)


if __name__ == "__main__":
    unittest.main()
