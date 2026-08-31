"""Authorized non-final Study creation for the T-528 desktop application.

This application adapter creates DEVELOPMENT Study recipes only.  It reuses the
validated protocol-v2 executors and retained method implementations while
keeping final held-out roots/layouts and final-reserve execution inaccessible.
Creation is durable but has no execution side effect; starting jobs is a
separate application action.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from ..study.model import EvidenceClass
from ..study.recipe import StudyRecipe
from ..study.service import StudyService, StudyStatus

_DEVELOPMENT_PROFILE = Path("configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json")
_FINAL_PROTOCOL = Path("configs/protocols/protocol-v2.0-final.json")
_RESET_POLICY = "dec-055-persistent-multi-episode-deployment-v1"
_ACTION_VECTORS = {
    "up": [0, -1],
    "right": [1, 0],
    "down": [0, 1],
    "left": [-1, 0],
}
_INFORMATION_POLICY = {
    "expose_executed_action": False,
    "expose_disturbance_flags": False,
    "expose_change_indicator": False,
    "expose_regime_id": False,
    "expose_true_state": False,
}


@dataclass(frozen=True)
class CreatedExploratoryStudy:
    study_id: str
    recipe_sha256: str
    status: str
    total_jobs: int


class DesktopExploratoryStudyModel:
    """Create executable DEVELOPMENT studies without opening the final reserve."""

    MAX_ROOTS = 2
    MAX_LAYOUTS = 2

    def __init__(self, *, repo_root: Path, writable_root: Path | None = None) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.writable_root = (
            Path(writable_root).resolve() if writable_root is not None else self.repo_root
        )
        self._development = self._read_json(_DEVELOPMENT_PROFILE)
        self._final = self._read_json(_FINAL_PROTOCOL)
        if self._development.get("final_reserve_access") is not False:
            raise RuntimeError("development profile must keep final reserve closed")
        if self._final.get("final_reserve_access") is not False:
            raise RuntimeError("T-528 refuses final protocol with reserve access enabled")

        layouts = self._development.get("development_layouts")
        if not isinstance(layouts, list) or len(layouts) < self.MAX_LAYOUTS:
            raise RuntimeError("development layout bank is incomplete")
        self._development_layouts = tuple(dict(item) for item in layouts[: self.MAX_LAYOUTS])

        sizing = self._mapping(self._development.get("sizing"), "development.sizing")
        conditions = sizing.get("conditions")
        if not isinstance(conditions, list) or not conditions:
            raise RuntimeError("development conditions are unavailable")
        self._development_conditions = tuple(dict(item) for item in conditions)

        retained = self._final.get("retained_methods")
        configs = self._mapping(self._final.get("selected_configs"), "final.selected_configs")
        if not isinstance(retained, list) or not retained:
            raise RuntimeError("retained method list is unavailable")
        self._retained_methods = tuple(str(item) for item in retained)
        self._configs = {
            method_id: dict(self._mapping(configs.get(method_id), f"config.{method_id}"))
            for method_id in self._retained_methods
        }

    def create(
        self,
        *,
        selected_method_ids: Sequence[str],
        root_count: int,
        layout_count: int,
        study_label: str = "",
        study_id: str | None = None,
    ) -> CreatedExploratoryStudy:
        recipe = self.build_recipe(
            selected_method_ids=selected_method_ids,
            root_count=root_count,
            layout_count=layout_count,
            study_label=study_label,
            study_id=study_id,
        )
        service = StudyService(
            repo_root=self.repo_root,
            writable_root=self.writable_root,
        )
        status = service.create(recipe)
        return self._created(status)

    def build_recipe(
        self,
        *,
        selected_method_ids: Sequence[str],
        root_count: int,
        layout_count: int,
        study_label: str = "",
        study_id: str | None = None,
    ) -> StudyRecipe:
        methods = self._validated_methods(selected_method_ids)
        if not 1 <= root_count <= self.MAX_ROOTS:
            raise ValueError("root_count must be within the T-528 development pool")
        if not 1 <= layout_count <= self.MAX_LAYOUTS:
            raise ValueError("layout_count must be within the T-528 development pool")

        resolved_id = study_id or self.suggest_study_id(study_label)
        if "final" in resolved_id.lower():
            raise ValueError("exploratory study_id must not imply final evidence")

        final_phase_a = self._mapping(self._final.get("phase_a"), "final.phase_a")
        final_phase_b = self._mapping(self._final.get("phase_b"), "final.phase_b")
        task = self._mapping(self._development.get("task"), "development.task")
        condition_ids = [str(item["condition_id"]) for item in self._development_conditions]

        method_records = [self._method_record(method_id, condition_ids) for method_id in methods]
        roots = [self._root_record(resolved_id, index) for index in range(1, root_count + 1)]
        layouts = [
            self._layout_record(item, task=task)
            for item in self._development_layouts[:layout_count]
        ]

        branch_horizon = int(final_phase_b["horizon"])
        recipe = StudyRecipe(
            recipe_id=resolved_id,
            protocol_version="protocol-v2.0-development",
            evidence_class=EvidenceClass.DEVELOPMENT,
            scientific_status="non-final-development-ui",
            frozen=False,
            study={
                "matrix_schema_version": 2,
                "phase_a": {
                    "execution": {
                        "training_interaction_budget": int(
                            final_phase_a["training_interaction_budget"]
                        ),
                        "probe_interaction_indices": list(
                            final_phase_a["probe_interaction_indices"]
                        ),
                        "episodes_per_probe": int(final_phase_a["episodes_per_probe"]),
                        "task": {
                            "gamma": float(task["gamma"]),
                            "reward_contract": dict(
                                self._mapping(task.get("reward_spec"), "task.reward_spec")
                            ),
                            "administrative_truncation": bool(
                                task["administrative_truncation"]
                            ),
                            "bootstrap_on_truncation": bool(
                                task["bootstrap_on_truncation"]
                            ),
                        },
                    },
                    "methods": method_records,
                    "references": [],
                    "roots": roots,
                    "layouts": layouts,
                },
                "phase_b": {
                    "execution": {
                        "prefix_interactions": int(
                            final_phase_b[
                                "common_nominal_no_learning_prefix_interactions"
                            ]
                        ),
                        "interaction_budget_per_branch": branch_horizon,
                        "episode_reset_policy_id": _RESET_POLICY,
                        "subsequent_episode_seed_count": branch_horizon,
                    },
                    "conditions": [dict(item) for item in self._development_conditions],
                    "branches": ["FN", "FD", "AN", "AD"],
                },
                "postprocessing": {
                    "validation": {"validator": "protocol-v2-study-v1"},
                    "analysis": {
                        "analysis_recipe": "protocol-v2-root-level-v1",
                        "phase_a_metric": "terminated_rate",
                        "phase_a_direction": "higher-is-better",
                        "phase_b_metric": "return_sum",
                        "phase_b_direction": "higher-is-better",
                        "layout_aggregation": "equal-weight",
                        "require_complete_layout_blocks": True,
                        "interval": {"kind": "none"},
                    },
                    "exports": {
                        "package": "protocol-v2-evidence-handoff-v1",
                        "emit_csv": True,
                    },
                },
            },
        )
        self._assert_no_final_identity(recipe)
        return recipe

    @staticmethod
    def suggest_study_id(label: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "-", label.strip().lower()).strip("-")
        slug = (normalized or "exploratory")[:32].rstrip("-")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        return f"t528-dev-{stamp}-{slug}"

    def _method_record(self, method_id: str, condition_ids: list[str]) -> dict[str, Any]:
        raw = dict(self._configs[method_id])
        config_id = str(raw.pop("config_id"))
        implementation_id = str(raw.pop("implementation_id"))
        return {
            "method_id": method_id,
            "configuration_id": config_id,
            "implementation_id": implementation_id,
            "role": "core-development",
            "phase_b_condition_ids": list(condition_ids),
            "parameters": raw,
        }

    @staticmethod
    def _root_record(study_id: str, index: int) -> dict[str, Any]:
        # A high, development-only deterministic namespace prevents accidental
        # reuse of the low-valued frozen final root streams (71k-76k).
        def seed(stream: str) -> int:
            digest = hashlib.sha256(
                f"t528-development:{study_id}:root:{index}:{stream}".encode("utf-8")
            ).digest()
            return 900_000_000 + int.from_bytes(digest[:4], "big") % 90_000_000

        return {
            "root_id": f"t528-dev-r{index:02d}",
            "initialization_seed": seed("initialization"),
            "exploration_seed": seed("exploration"),
            "scenario_seed": seed("scenario"),
            "environment_seed": seed("environment"),
            "action_disturbance_seed": seed("action-disturbance"),
            "observation_disturbance_seed": seed("observation-disturbance"),
        }

    @staticmethod
    def _layout_record(layout: Mapping[str, Any], *, task: Mapping[str, Any]) -> dict[str, Any]:
        layout_id = str(layout["layout_id"])
        reward = dict(DesktopExploratoryStudyModel._mapping(task.get("reward_spec"), "task.reward_spec"))
        scenario = {
            "scenario_id": layout_id,
            "environment_id": str(task["environment_id"]),
            "max_steps": int(layout["max_steps"]),
            "reward_spec": reward,
            "initial_state_spec": {
                "grid": {
                    "width": int(layout["width"]),
                    "height": int(layout["height"]),
                    "start": list(layout["start"]),
                    "goal": list(layout["goal"]),
                    "obstacles": [list(item) for item in layout["obstacles"]],
                }
            },
            "dynamics_spec": {"action_vectors": dict(_ACTION_VECTORS)},
            "observation_spec": {
                "type": "position",
                "coordinate_order": "x-y",
                "reset_observation": "true-state",
            },
            "action_disturbance_spec": {
                "type": "no-op-failure",
                "failure_probability": 0.0,
            },
            "observation_disturbance_spec": {
                "type": "position-mislocalization",
                "mislocalization_probability": 0.0,
            },
            "change_events": [],
            "information_policy": dict(_INFORMATION_POLICY),
        }
        return {"layout_id": layout_id, "scenario": scenario}

    def _validated_methods(self, values: Sequence[str]) -> tuple[str, ...]:
        methods = tuple(str(item) for item in values)
        if not methods:
            raise ValueError("at least one exploratory method is required")
        if len(set(methods)) != len(methods):
            raise ValueError("exploratory method identities must be unique")
        unknown = tuple(item for item in methods if item not in self._retained_methods)
        if unknown:
            raise ValueError(f"unsupported exploratory methods: {unknown}")
        return methods

    def _assert_no_final_identity(self, recipe: StudyRecipe) -> None:
        encoded = json.dumps(recipe.to_dict(), sort_keys=True)
        forbidden = [
            "gw-l1-final-a",
            "gw-l1-final-b",
            *(f"t527-final-r{index:02d}" for index in range(1, 13)),
        ]
        used = [item for item in forbidden if item in encoded]
        if used:
            raise RuntimeError(f"development recipe leaked final-reserve identities: {used}")

    def _read_json(self, relative: Path) -> Mapping[str, Any]:
        path = self.repo_root / relative
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"cannot read application authority: {path}") from exc
        return self._mapping(value, str(relative))

    @staticmethod
    def _mapping(value: Any, field: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise RuntimeError(f"{field} must be an object")
        return value

    @staticmethod
    def _created(status: StudyStatus) -> CreatedExploratoryStudy:
        return CreatedExploratoryStudy(
            study_id=status.study_id,
            recipe_sha256=status.recipe_sha256,
            status=status.status,
            total_jobs=int(status.progress.get("total", 0)),
        )
