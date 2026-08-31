"""T-528 execution firewall for the desktop application."""
from __future__ import annotations

import json
from pathlib import Path

from ..study.model import EvidenceClass, JobState
from ..study.recipe import StudyRecipe
from ..study.store import StudyStore

_FINAL_PROTOCOL = Path("configs/protocols/protocol-v2.0-final.json")
_FORBIDDEN_FINAL_IDENTITIES = (
    "gw-l1-final-a",
    "gw-l1-final-b",
    *(f"t527-final-r{index:02d}" for index in range(1, 13)),
)


def assert_final_reserve_locked(repo_root: Path) -> None:
    path = Path(repo_root).resolve() / _FINAL_PROTOCOL
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot verify final-reserve authority: {path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("final protocol authority must be a JSON object")
    if payload.get("final_reserve_access") is not False:
        raise RuntimeError(
            "T-528 execution is disabled unless protocol-v2.0 final_reserve_access=false"
        )


def assert_development_recipe_execution_allowed(recipe: StudyRecipe) -> None:
    if not isinstance(recipe, StudyRecipe):
        raise ValueError("recipe must be StudyRecipe")
    if recipe.evidence_class is not EvidenceClass.DEVELOPMENT:
        raise RuntimeError("desktop worker may execute DEVELOPMENT studies only")
    if recipe.frozen:
        raise RuntimeError("desktop worker refuses frozen recipes during T-528")
    if recipe.protocol_version == "protocol-v2.0":
        raise RuntimeError("desktop worker refuses the final protocol identity during T-528")
    encoded = json.dumps(recipe.to_dict(), sort_keys=True)
    leaked = [identity for identity in _FORBIDDEN_FINAL_IDENTITIES if identity in encoded]
    if leaked:
        raise RuntimeError(
            "desktop DEVELOPMENT recipe contains final-reserve identities: "
            + ", ".join(leaked)
        )


def assert_development_store_execution_allowed(
    store: StudyStore,
    *,
    repo_root: Path,
) -> None:
    if not isinstance(store, StudyStore):
        raise ValueError("store must be StudyStore")
    assert_final_reserve_locked(repo_root)
    assert_development_recipe_execution_allowed(store.recipe)


def job_ids_in_state(store: StudyStore, state: JobState) -> tuple[str, ...]:
    if not isinstance(store, StudyStore):
        raise ValueError("store must be StudyStore")
    if not isinstance(state, JobState):
        raise ValueError("state must be JobState")
    return tuple(
        job.job_id
        for job in store.plan.jobs
        if store.lifecycle.state_for(job.job_id) is state
    )


def infrastructure_failure_job_ids(store: StudyStore) -> tuple[str, ...]:
    return job_ids_in_state(store, JobState.INFRASTRUCTURE_FAILED)


def running_job_ids(store: StudyStore) -> tuple[str, ...]:
    return job_ids_in_state(store, JobState.RUNNING)
