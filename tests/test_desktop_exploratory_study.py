from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.exploratory_study import DesktopExploratoryStudyModel
from resilient_agents.study.planner import StudyPlanner
from resilient_agents.study.protocol_v2_executors import _root_identity, _scenario_from_layout

REPO_ROOT = Path(__file__).resolve().parents[1]


class DesktopExploratoryStudyTests(unittest.TestCase):
    def _model(self, writable_root: Path) -> DesktopExploratoryStudyModel:
        return DesktopExploratoryStudyModel(repo_root=REPO_ROOT, writable_root=writable_root)

    def test_executable_recipe_uses_only_development_identities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            model = self._model(Path(directory))
            recipe = model.build_recipe(
                selected_method_ids=("q_learning", "ppo"),
                root_count=2,
                layout_count=2,
                study_id="t528-dev-test",
            )
            payload = recipe.to_dict()
            encoded = json.dumps(payload, sort_keys=True)
            self.assertEqual(payload["evidence_class"], "development")
            self.assertNotIn("gw-l1-final", encoded)
            self.assertNotIn("t527-final-r", encoded)
            self.assertIn("gw-l1-a", encoded)
            self.assertIn("gw-l1-b", encoded)

            planner = StudyPlanner(recipe)
            preview = planner.preview()
            self.assertEqual(preview.phase_a_jobs, 8)
            self.assertEqual(preview.phase_b_jobs, 16)
            self.assertEqual(preview.total_jobs, 27)

            for root in recipe.study["phase_a"]["roots"]:
                identity = _root_identity(root)
                self.assertTrue(identity.root_id.startswith("t528-dev-r"))
                self.assertGreaterEqual(identity.initialization_seed, 900_000_000)
            for layout in recipe.study["phase_a"]["layouts"]:
                scenario = _scenario_from_layout(layout)
                self.assertEqual(tuple(scenario.change_events), ())
                self.assertEqual(scenario.action_disturbance_spec["failure_probability"], 0.0)
                self.assertEqual(
                    scenario.observation_disturbance_spec["mislocalization_probability"],
                    0.0,
                )

    def test_create_is_durable_but_does_not_execute_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            writable = Path(directory)
            model = self._model(writable)
            created = model.create(
                selected_method_ids=("q_learning",),
                root_count=1,
                layout_count=1,
                study_label="smoke",
                study_id="t528-dev-create-smoke",
            )
            self.assertEqual(created.study_id, "t528-dev-create-smoke")
            self.assertEqual(created.total_jobs, 6)
            study_dir = writable / "results" / "studies" / created.study_id
            self.assertTrue((study_dir / "recipe.json").is_file())
            self.assertTrue((study_dir / "plan.json").is_file())
            runs = writable / "results" / "runs"
            self.assertFalse(runs.exists())

    def test_rejects_final_sounding_study_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            model = self._model(Path(directory))
            with self.assertRaisesRegex(ValueError, "must not imply final evidence"):
                model.build_recipe(
                    selected_method_ids=("q_learning",),
                    root_count=1,
                    layout_count=1,
                    study_id="final-thesis-run",
                )


if __name__ == "__main__":
    unittest.main()
