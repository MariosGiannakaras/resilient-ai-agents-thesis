from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resilient_agents.evidence_v2.denominators import build_scientific_denominators
from resilient_agents.study import (
    EvidenceClass,
    StudyJobSpec,
    StudyPlan,
    StudyRecipe,
    StudyStage,
    StudyStore,
)


class EvidenceV2DenominatorTests(unittest.TestCase):
    def test_counts_failed_and_skipped_scientific_units_without_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = StudyRecipe(
                recipe_id="denominator-study",
                protocol_version="protocol-v2.0-candidate",
                evidence_class=EvidenceClass.DEVELOPMENT,
                scientific_status="denominator-test",
                frozen=False,
                study={"purpose": "denominator-test"},
            )
            digest = recipe.sha256()
            plan = StudyPlan(
                study_id=recipe.recipe_id,
                jobs=(
                    StudyJobSpec(
                        job_id="pa-1",
                        stage=StudyStage.PHASE_A,
                        evidence_class=EvidenceClass.DEVELOPMENT,
                        payload={
                            "job_type": "phase-a-training",
                            "recipe_sha256": digest,
                            "method": {"method_id": "q_learning"},
                        },
                    ),
                    StudyJobSpec(
                        job_id="pa-2",
                        stage=StudyStage.PHASE_A,
                        evidence_class=EvidenceClass.DEVELOPMENT,
                        payload={
                            "job_type": "phase-a-training",
                            "recipe_sha256": digest,
                            "method": {"method_id": "q_learning"},
                        },
                    ),
                    StudyJobSpec(
                        job_id="pb-1",
                        stage=StudyStage.PHASE_B,
                        evidence_class=EvidenceClass.DEVELOPMENT,
                        dependencies=("pa-1",),
                        payload={
                            "job_type": "phase-b-matched-set",
                            "recipe_sha256": digest,
                            "method": {"method_id": "q_learning"},
                            "condition": {"condition_id": "remap"},
                        },
                    ),
                    StudyJobSpec(
                        job_id="pb-2",
                        stage=StudyStage.PHASE_B,
                        evidence_class=EvidenceClass.DEVELOPMENT,
                        dependencies=("pa-2",),
                        payload={
                            "job_type": "phase-b-matched-set",
                            "recipe_sha256": digest,
                            "method": {"method_id": "q_learning"},
                            "condition": {"condition_id": "remap"},
                        },
                    ),
                ),
            )
            store = StudyStore.create(
                repo_root=root,
                writable_root=root,
                recipe=recipe,
                plan=plan,
            )
            store.start_job("pa-1")
            store.complete_job("pa-1")
            store.start_job("pa-2")
            store.fail_job_scientifically("pa-2", reason="retained scientific failure")
            store.start_job("pb-1")
            store.complete_job("pb-1")

            result = build_scientific_denominators(store)
            phase_a = result["phase_a_methods"][0]
            self.assertEqual(phase_a["planned"], 2)
            self.assertEqual(phase_a["completed"], 1)
            self.assertEqual(phase_a["scientific_failed"], 1)

            phase_b = result["phase_b_method_conditions"][0]
            self.assertEqual(phase_b["planned"], 2)
            self.assertEqual(phase_b["completed"], 1)
            self.assertEqual(phase_b["skipped"], 1)
            self.assertEqual(phase_b["scientific_failed"], 0)


if __name__ == "__main__":
    unittest.main()
