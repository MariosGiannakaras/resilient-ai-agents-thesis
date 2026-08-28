"""Deterministic recipe-to-job materialization for complete protocol-v2 studies."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

from ..protocol_v2 import ProtocolV2Branch
from .model import EvidenceClass, StudyJobSpec, StudyPlan, StudyStage
from .recipe import StudyRecipe

STUDY_MATRIX_SCHEMA_VERSION = 2
_COMPONENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_EXPECTED_BRANCHES = tuple(branch.value for branch in ProtocolV2Branch)


def _component(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not _COMPONENT_RE.fullmatch(value):
        raise ValueError(
            f"{field} must start with an alphanumeric character and contain only "
            "letters, digits, dot, underscore or hyphen"
        )
    if "__" in value:
        raise ValueError(f"{field} must not contain the reserved '__' delimiter")
    return value


def _records(
    value: Any,
    *,
    field: str,
    id_key: str,
    allow_empty: bool = False,
) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, list) or (not value and not allow_empty):
        suffix = "a list" if allow_empty else "a non-empty list"
        raise ValueError(f"{field} must be {suffix}")
    records: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise ValueError(f"{field}[{index}] must be an object")
        record = dict(item)
        identifier = _component(record.get(id_key), field=f"{field}[{index}].{id_key}")
        if identifier in identifiers:
            raise ValueError(f"duplicate {field} identifier: {identifier}")
        identifiers.add(identifier)
        records.append(record)
    return tuple(records)


def _exact_keys(value: Mapping[str, Any], expected: set[str], *, field: str) -> None:
    if set(value) != expected:
        missing = sorted(expected - set(value))
        unknown = sorted(set(value) - expected)
        raise ValueError(f"{field} keys mismatch; missing={missing}, unknown={unknown}")


def _object(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise ValueError(f"{field} must be a non-empty object")
    return dict(value)


@dataclass(frozen=True)
class StudyPlanPreview:
    phase_a_jobs: int
    phase_b_jobs: int
    validation_jobs: int
    analysis_jobs: int
    export_jobs: int
    total_jobs: int
    method_count: int
    reference_count: int
    root_count: int
    layout_count: int
    condition_count: int

    def to_dict(self) -> dict[str, int]:
        return {
            "phase_a_jobs": self.phase_a_jobs,
            "phase_b_jobs": self.phase_b_jobs,
            "validation_jobs": self.validation_jobs,
            "analysis_jobs": self.analysis_jobs,
            "export_jobs": self.export_jobs,
            "total_jobs": self.total_jobs,
            "method_count": self.method_count,
            "reference_count": self.reference_count,
            "root_count": self.root_count,
            "layout_count": self.layout_count,
            "condition_count": self.condition_count,
        }


@dataclass(frozen=True)
class StudyMatrixDefinition:
    phase_a_execution: Mapping[str, Any]
    methods: tuple[Mapping[str, Any], ...]
    references: tuple[Mapping[str, Any], ...]
    roots: tuple[Mapping[str, Any], ...]
    layouts: tuple[Mapping[str, Any], ...]
    phase_b_execution: Mapping[str, Any]
    conditions: tuple[Mapping[str, Any], ...]
    branches: tuple[str, ...]
    validation: Mapping[str, Any]
    analysis: Mapping[str, Any]
    exports: Mapping[str, Any]

    @classmethod
    def from_recipe(cls, recipe: StudyRecipe) -> "StudyMatrixDefinition":
        study = recipe.study
        _exact_keys(
            study,
            {"matrix_schema_version", "phase_a", "phase_b", "postprocessing"},
            field="study",
        )
        if study["matrix_schema_version"] != STUDY_MATRIX_SCHEMA_VERSION:
            raise ValueError("unsupported study matrix schema_version")

        phase_a = study["phase_a"]
        phase_b = study["phase_b"]
        postprocessing = study["postprocessing"]
        if not isinstance(phase_a, Mapping):
            raise ValueError("study.phase_a must be an object")
        if not isinstance(phase_b, Mapping):
            raise ValueError("study.phase_b must be an object")
        if not isinstance(postprocessing, Mapping):
            raise ValueError("study.postprocessing must be an object")
        _exact_keys(
            phase_a,
            {"execution", "methods", "references", "roots", "layouts"},
            field="study.phase_a",
        )
        _exact_keys(
            phase_b,
            {"execution", "conditions", "branches"},
            field="study.phase_b",
        )
        _exact_keys(
            postprocessing,
            {"validation", "analysis", "exports"},
            field="study.postprocessing",
        )

        phase_a_execution = _object(
            phase_a["execution"], field="study.phase_a.execution"
        )
        phase_b_execution = _object(
            phase_b["execution"], field="study.phase_b.execution"
        )
        methods = _records(
            phase_a["methods"], field="study.phase_a.methods", id_key="method_id"
        )
        references = _records(
            phase_a["references"],
            field="study.phase_a.references",
            id_key="reference_id",
            allow_empty=True,
        )
        roots = _records(phase_a["roots"], field="study.phase_a.roots", id_key="root_id")
        layouts = _records(
            phase_a["layouts"], field="study.phase_a.layouts", id_key="layout_id"
        )
        conditions = _records(
            phase_b["conditions"],
            field="study.phase_b.conditions",
            id_key="condition_id",
        )
        condition_ids = {str(item["condition_id"]) for item in conditions}

        branches_payload = phase_b["branches"]
        if not isinstance(branches_payload, list) or not all(
            isinstance(item, str) for item in branches_payload
        ):
            raise ValueError("study.phase_b.branches must be a list of strings")
        branches = tuple(branches_payload)
        if branches != _EXPECTED_BRANCHES:
            raise ValueError(
                "study.phase_b.branches must exactly match protocol-v2 FN/FD/AN/AD order"
            )

        normalized_methods: list[dict[str, Any]] = []
        for index, method in enumerate(methods):
            allowed = method.get("phase_b_condition_ids")
            if not isinstance(allowed, list) or not allowed or not all(
                isinstance(item, str) for item in allowed
            ):
                raise ValueError(
                    f"study.phase_a.methods[{index}].phase_b_condition_ids must be a non-empty list"
                )
            if len(set(allowed)) != len(allowed):
                raise ValueError("method phase_b_condition_ids must be unique")
            unknown = [item for item in allowed if item not in condition_ids]
            if unknown:
                raise ValueError(
                    f"method {method['method_id']} references unknown Phase-B conditions: {unknown}"
                )
            normalized_methods.append({**method, "phase_b_condition_ids": list(allowed)})

        for name in ("validation", "analysis", "exports"):
            if not isinstance(postprocessing[name], Mapping):
                raise ValueError(f"study.postprocessing.{name} must be an object")

        return cls(
            phase_a_execution=phase_a_execution,
            methods=tuple(normalized_methods),
            references=references,
            roots=roots,
            layouts=layouts,
            phase_b_execution=phase_b_execution,
            conditions=conditions,
            branches=branches,
            validation=dict(postprocessing["validation"]),
            analysis=dict(postprocessing["analysis"]),
            exports=dict(postprocessing["exports"]),
        )


class StudyPlanner:
    """Materialize one immutable study recipe into stable scientific job IDs.

    Phase B is intentionally materialized as one matched-set job per
    method/root/layout/condition.  The validated protocol-v2 executor creates
    FN/FD/AN/AD from one exact branch point atomically; splitting those branches
    into independent scheduler jobs would weaken the matched-design invariant.
    """

    def __init__(self, recipe: StudyRecipe) -> None:
        if not isinstance(recipe, StudyRecipe):
            raise ValueError("recipe must be StudyRecipe")
        self.recipe = recipe
        self.matrix = StudyMatrixDefinition.from_recipe(recipe)
        self._condition_by_id = {
            str(item["condition_id"]): item for item in self.matrix.conditions
        }

    def materialize(self) -> StudyPlan:
        jobs: list[StudyJobSpec] = []
        phase_a_ids: dict[tuple[str, str, str], str] = {}

        for method in self.matrix.methods:
            method_id = str(method["method_id"])
            for root in self.matrix.roots:
                root_id = str(root["root_id"])
                for layout in self.matrix.layouts:
                    layout_id = str(layout["layout_id"])
                    job_id = self.phase_a_job_id(method_id, root_id, layout_id)
                    phase_a_ids[(method_id, root_id, layout_id)] = job_id
                    jobs.append(
                        StudyJobSpec(
                            job_id=job_id,
                            stage=StudyStage.PHASE_A,
                            evidence_class=self.recipe.evidence_class,
                            payload={
                                "job_type": "phase-a-training",
                                "recipe_sha256": self.recipe.sha256(),
                                "execution": dict(self.matrix.phase_a_execution),
                                "method": dict(method),
                                "root": dict(root),
                                "layout": dict(layout),
                            },
                        )
                    )

        for reference in self.matrix.references:
            reference_id = str(reference["reference_id"])
            for root in self.matrix.roots:
                root_id = str(root["root_id"])
                for layout in self.matrix.layouts:
                    layout_id = str(layout["layout_id"])
                    jobs.append(
                        StudyJobSpec(
                            job_id=self.reference_job_id(reference_id, root_id, layout_id),
                            stage=StudyStage.PHASE_A,
                            evidence_class=self.recipe.evidence_class,
                            payload={
                                "job_type": "phase-a-reference",
                                "recipe_sha256": self.recipe.sha256(),
                                "execution": dict(self.matrix.phase_a_execution),
                                "reference": dict(reference),
                                "root": dict(root),
                                "layout": dict(layout),
                            },
                        )
                    )

        for method in self.matrix.methods:
            method_id = str(method["method_id"])
            allowed_conditions = tuple(method["phase_b_condition_ids"])
            for root in self.matrix.roots:
                root_id = str(root["root_id"])
                for layout in self.matrix.layouts:
                    layout_id = str(layout["layout_id"])
                    phase_a_job_id = phase_a_ids[(method_id, root_id, layout_id)]
                    for condition_id in allowed_conditions:
                        condition = self._condition_by_id[condition_id]
                        jobs.append(
                            StudyJobSpec(
                                job_id=self.phase_b_job_id(
                                    method_id,
                                    root_id,
                                    layout_id,
                                    condition_id,
                                ),
                                stage=StudyStage.PHASE_B,
                                evidence_class=self.recipe.evidence_class,
                                dependencies=(phase_a_job_id,),
                                payload={
                                    "job_type": "phase-b-matched-set",
                                    "recipe_sha256": self.recipe.sha256(),
                                    "execution": dict(self.matrix.phase_b_execution),
                                    "phase_a_job_id": phase_a_job_id,
                                    "method": dict(method),
                                    "root": dict(root),
                                    "layout": dict(layout),
                                    "condition": dict(condition),
                                    "branches": list(self.matrix.branches),
                                },
                            )
                        )

        jobs.append(
            StudyJobSpec(
                job_id="validate-study",
                stage=StudyStage.VALIDATION,
                evidence_class=EvidenceClass.DERIVED,
                payload={
                    "job_type": "study-validation",
                    "recipe_sha256": self.recipe.sha256(),
                    "specification": dict(self.matrix.validation),
                },
            )
        )
        jobs.append(
            StudyJobSpec(
                job_id="analyze-study",
                stage=StudyStage.ANALYSIS,
                evidence_class=EvidenceClass.DERIVED,
                dependencies=("validate-study",),
                payload={
                    "job_type": "study-analysis",
                    "recipe_sha256": self.recipe.sha256(),
                    "specification": dict(self.matrix.analysis),
                },
            )
        )
        jobs.append(
            StudyJobSpec(
                job_id="export-study",
                stage=StudyStage.EXPORT,
                evidence_class=EvidenceClass.DERIVED,
                dependencies=("analyze-study",),
                payload={
                    "job_type": "study-export",
                    "recipe_sha256": self.recipe.sha256(),
                    "specification": dict(self.matrix.exports),
                },
            )
        )
        return StudyPlan(study_id=self.recipe.recipe_id, jobs=tuple(jobs))

    def preview(self) -> StudyPlanPreview:
        plan = self.materialize()
        by_stage = {
            stage: len(plan.jobs_for_stage(stage))
            for stage in (
                StudyStage.PHASE_A,
                StudyStage.PHASE_B,
                StudyStage.VALIDATION,
                StudyStage.ANALYSIS,
                StudyStage.EXPORT,
            )
        }
        return StudyPlanPreview(
            phase_a_jobs=by_stage[StudyStage.PHASE_A],
            phase_b_jobs=by_stage[StudyStage.PHASE_B],
            validation_jobs=by_stage[StudyStage.VALIDATION],
            analysis_jobs=by_stage[StudyStage.ANALYSIS],
            export_jobs=by_stage[StudyStage.EXPORT],
            total_jobs=len(plan.jobs),
            method_count=len(self.matrix.methods),
            reference_count=len(self.matrix.references),
            root_count=len(self.matrix.roots),
            layout_count=len(self.matrix.layouts),
            condition_count=len(self.matrix.conditions),
        )

    @staticmethod
    def phase_a_job_id(method_id: str, root_id: str, layout_id: str) -> str:
        components = (
            _component(method_id, field="method_id"),
            _component(root_id, field="root_id"),
            _component(layout_id, field="layout_id"),
        )
        return "pa__" + "__".join(components)

    @staticmethod
    def reference_job_id(reference_id: str, root_id: str, layout_id: str) -> str:
        components = (
            _component(reference_id, field="reference_id"),
            _component(root_id, field="root_id"),
            _component(layout_id, field="layout_id"),
        )
        return "ref__" + "__".join(components)

    @staticmethod
    def phase_b_job_id(
        method_id: str,
        root_id: str,
        layout_id: str,
        condition_id: str,
    ) -> str:
        components = (
            _component(method_id, field="method_id"),
            _component(root_id, field="root_id"),
            _component(layout_id, field="layout_id"),
            _component(condition_id, field="condition_id"),
        )
        return "pb__" + "__".join(components)
