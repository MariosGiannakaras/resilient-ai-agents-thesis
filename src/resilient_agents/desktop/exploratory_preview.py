"""Backend-owned preview-only DEVELOPMENT experiment projection for T-534.

This adapter materializes only a DEVELOPMENT StudyRecipe for StudyService.preview().
It cannot create or execute work and it never uses final-reserve roots/layouts/outcomes.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from ..study.model import EvidenceClass
from ..study.recipe import StudyRecipe
from ..study.scheduler import StudyExecutorRegistry
from ..study.service import StudyService


@dataclass(frozen=True)
class ExploratoryPlanPreview:
    recipe_sha256: str
    method_count: int
    root_count: int
    layout_count: int
    condition_count: int
    phase_a_jobs: int
    phase_b_jobs: int
    validation_jobs: int
    analysis_jobs: int
    export_jobs: int
    total_jobs: int
    development_layout_ids: tuple[str, ...]
    condition_ids: tuple[str, ...]


class DesktopExploratoryPreviewModel:
    """Resolve non-final UI intent through the real framework-neutral planner."""

    _PROFILE_PATH = Path("configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json")
    _CURRENT_PROTOCOL_PATH = Path("configs/protocols/protocol-v2.1-final.json")
    _MAX_PREVIEW_ROOTS = 2
    _MAX_PREVIEW_LAYOUTS = 2

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = Path(repo_root).resolve()
        self._profile = self._load_json(self._PROFILE_PATH)
        self._current = self._load_json(self._CURRENT_PROTOCOL_PATH)
        if self._profile.get("final_reserve_access") is not False:
            raise RuntimeError("development preview profile must keep final reserve closed")
        if self._current.get("final_reserve_access") is not False:
            raise RuntimeError("T-534 refuses current protocol with final reserve enabled")
        if self._current.get("protocol_id") != "protocol-v2.1":
            raise RuntimeError("DEVELOPMENT preview requires current protocol-v2.1 authority")

        layouts = self._profile.get("development_layouts")
        if not isinstance(layouts, list) or len(layouts) < self._MAX_PREVIEW_LAYOUTS:
            raise RuntimeError("development preview requires two non-final layouts")
        self._development_layouts = tuple(dict(item) for item in layouts[:2])

        sizing = self._mapping(self._profile.get("sizing"), "sizing")
        conditions = sizing.get("conditions")
        if not isinstance(conditions, list) or not conditions:
            raise RuntimeError("development preview conditions are unavailable")
        self._conditions = tuple(dict(item) for item in conditions)

        selected_configs = self._mapping(
            self._current.get("selected_configs"), "current.selected_configs"
        )
        retained = self._current.get("retained_methods")
        if not isinstance(retained, list) or not retained:
            raise RuntimeError("current retained method list is unavailable")
        self._retained_methods = tuple(str(item) for item in retained)
        self._selected_configs = {
            method_id: dict(
                self._mapping(
                    selected_configs.get(method_id),
                    f"current.selected_configs.{method_id}",
                )
            )
            for method_id in self._retained_methods
        }

    @property
    def max_root_count(self) -> int:
        return self._MAX_PREVIEW_ROOTS

    @property
    def max_layout_count(self) -> int:
        return self._MAX_PREVIEW_LAYOUTS

    @property
    def development_layout_ids(self) -> tuple[str, ...]:
        return tuple(str(item["layout_id"]) for item in self._development_layouts)

    @property
    def condition_ids(self) -> tuple[str, ...]:
        return tuple(str(item["condition_id"]) for item in self._conditions)

    def preview(
        self,
        *,
        selected_method_ids: Sequence[str],
        root_count: int,
        layout_count: int,
    ) -> ExploratoryPlanPreview:
        methods = tuple(str(item) for item in selected_method_ids)
        if not methods:
            raise ValueError("at least one DEVELOPMENT method is required")
        if len(set(methods)) != len(methods):
            raise ValueError("DEVELOPMENT method identities must be unique")
        unknown = tuple(item for item in methods if item not in self._retained_methods)
        if unknown:
            raise ValueError(f"unsupported DEVELOPMENT methods: {unknown}")
        if not 1 <= root_count <= self._MAX_PREVIEW_ROOTS:
            raise ValueError("root_count must be within the non-final development pool")
        if not 1 <= layout_count <= self._MAX_PREVIEW_LAYOUTS:
            raise ValueError("layout_count must be within the non-final development pool")

        recipe = self._recipe(methods=methods, root_count=root_count, layout_count=layout_count)
        service = StudyService(
            repo_root=self.repo_root,
            writable_root=self.repo_root,
            executors=StudyExecutorRegistry(),
        )
        summary = service.preview(recipe)
        preview = summary.preview
        return ExploratoryPlanPreview(
            recipe_sha256=summary.recipe_sha256,
            method_count=preview.method_count,
            root_count=preview.root_count,
            layout_count=preview.layout_count,
            condition_count=preview.condition_count,
            phase_a_jobs=preview.phase_a_jobs,
            phase_b_jobs=preview.phase_b_jobs,
            validation_jobs=preview.validation_jobs,
            analysis_jobs=preview.analysis_jobs,
            export_jobs=preview.export_jobs,
            total_jobs=preview.total_jobs,
            development_layout_ids=tuple(
                str(item["layout_id"]) for item in self._development_layouts[:layout_count]
            ),
            condition_ids=self.condition_ids,
        )

    def _recipe(
        self,
        *,
        methods: tuple[str, ...],
        root_count: int,
        layout_count: int,
    ) -> StudyRecipe:
        phase_a = self._mapping(self._current.get("phase_a"), "current.phase_a")
        phase_b = self._mapping(self._current.get("phase_b"), "current.phase_b")
        task = self._mapping(self._profile.get("task"), "development.task")
        condition_ids = list(self.condition_ids)
        method_records: list[dict[str, Any]] = []
        for method_id in methods:
            config = self._selected_configs[method_id]
            method_records.append(
                {
                    "method_id": method_id,
                    "configuration_id": str(config["config_id"]),
                    "configuration": dict(config),
                    "role": "core-development-preview",
                    "phase_b_condition_ids": condition_ids,
                }
            )

        roots = [
            {
                "root_id": f"t534-preview-r{index:02d}",
                "preview_only": True,
                "seed_family": 88000 + index,
            }
            for index in range(1, root_count + 1)
        ]
        reward = self._mapping(task.get("reward_spec"), "development.task.reward_spec")
        return StudyRecipe(
            recipe_id="t534-development-preview",
            protocol_version="protocol-v2.1-development-preview",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="non-final-preview-only",
            frozen=False,
            study={
                "matrix_schema_version": 2,
                "phase_a": {
                    "execution": {
                        "training_interaction_budget": int(phase_a["training_interaction_budget"]),
                        "probe_interaction_indices": list(phase_a["probe_interaction_indices"]),
                        "episodes_per_probe": int(phase_a["episodes_per_probe"]),
                        "task": {
                            "gamma": float(task["gamma"]),
                            "reward_contract": dict(reward),
                            "administrative_truncation": bool(task["administrative_truncation"]),
                            "bootstrap_on_truncation": bool(task["bootstrap_on_truncation"]),
                        },
                        "preview_only": True,
                    },
                    "methods": method_records,
                    "references": [],
                    "roots": roots,
                    "layouts": [dict(item) for item in self._development_layouts[:layout_count]],
                },
                "phase_b": {
                    "execution": {
                        "interaction_budget_per_branch": int(phase_b["horizon"]),
                        "prefix_interactions": int(phase_b["common_nominal_no_learning_prefix_interactions"]),
                        "preview_only": True,
                    },
                    "conditions": [dict(item) for item in self._conditions],
                    "branches": ["FN", "FD", "AN", "AD"],
                },
                "postprocessing": {
                    "validation": {"mode": "development-preview-only"},
                    "analysis": {"mode": "development-preview-only"},
                    "exports": {"mode": "development-preview-only"},
                },
            },
        )

    def _load_json(self, relative: Path) -> Mapping[str, Any]:
        path = self.repo_root / relative
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"cannot read DEVELOPMENT preview authority: {path}") from exc
        return self._mapping(value, str(relative))

    @staticmethod
    def _mapping(value: Any, field: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise RuntimeError(f"{field} must be an object")
        return value
