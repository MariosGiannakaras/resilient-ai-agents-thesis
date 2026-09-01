from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.desktop.execution_policy import (
    assert_development_recipe_execution_allowed,
    assert_final_reserve_locked,
)
from resilient_agents.desktop.exploratory_study import DesktopExploratoryStudyModel
from resilient_agents.study import EvidenceClass, StudyRecipe

REPO_ROOT = Path(__file__).resolve().parents[1]


class DesktopExecutionPolicyTests(unittest.TestCase):
    def test_application_development_recipe_is_execution_eligible_without_final_identities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            model = DesktopExploratoryStudyModel(
                repo_root=REPO_ROOT,
                writable_root=Path(directory),
            )
            recipe = model.build_recipe(
                selected_method_ids=("q_learning", "ppo"),
                root_count=2,
                layout_count=2,
                study_id="t528-dev-policy-test",
            )
            assert_final_reserve_locked(REPO_ROOT)
            assert_development_recipe_execution_allowed(recipe)
            encoded = str(recipe.to_dict())
            self.assertNotIn("gw-l1-final-a", encoded)
            self.assertNotIn("t527-final-r01", encoded)

    def test_execution_policy_rejects_final_identity_even_when_mislabeled_development(self) -> None:
        recipe = StudyRecipe(
            recipe_id="t528-dev-invalid",
            protocol_version="protocol-v2.0-development",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="non-final-development-ui",
            frozen=False,
            study={"layout_id": "gw-l1-final-a"},
        )
        with self.assertRaisesRegex(RuntimeError, "final-reserve identities"):
            assert_development_recipe_execution_allowed(recipe)

    def test_execution_policy_rejects_confirmatory_recipe(self) -> None:
        recipe = StudyRecipe(
            recipe_id="confirmatory-test",
            protocol_version="protocol-v2.0",
            evidence_class=EvidenceClass.CONFIRMATORY,
            scientific_status="frozen-final",
            frozen=True,
            study={"purpose": "guard-test"},
        )
        with self.assertRaisesRegex(RuntimeError, "DEVELOPMENT studies only"):
            assert_development_recipe_execution_allowed(recipe)


if __name__ == "__main__":
    unittest.main()
