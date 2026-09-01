"""Fail-closed DEVELOPMENT execution firewall for the T-534 desktop UI."""
from __future__ import annotations

import json
from pathlib import Path

from ..study.model import EvidenceClass, JobState
from ..study.recipe import StudyRecipe
from ..study.store import StudyStore

_CURRENT_PROTOCOL = Path("configs/protocols/protocol-v2.1-final.json")
_ALLOWED_DEVELOPMENT_PROTOCOLS = {
    "protocol-v2.1-development",
    # Historical DEVELOPMENT studies remain resumable; this is compatibility,
    # not active presentation authority.
    "protocol-v2.0-development",
}


def assert_final_reserve_locked(repo_root: Path) -> None:
    path = Path(repo_root).resolve() / _CURRENT_PROTOCOL
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot verify final-reserve authority: {path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("current protocol authority must be a JSON object")
    if payload.get("protocol_id") != "protocol-v2.1":
        raise RuntimeError("desktop execution requires current protocol-v2.1 authority")
    if payload.get("final_reserve_access") is not False:
        raise RuntimeError("desktop DEVELOPMENT execution requires final_reserve_access=false")
    if payload.get("execution_authorization") != "requires-explicit-t610-gate":
        raise RuntimeError("unexpected final execution authorization contract")


def assert_development_recipe_execution_allowed(recipe: StudyRecipe) -> None:
    if not isinstance(recipe, StudyRecipe):
        raise ValueError("recipe must be StudyRecipe")
    if recipe.evidence_class is not EvidenceClass.DEVELOPMENT:
        raise RuntimeError("desktop worker may execute DEVELOPMENT studies only")
    if recipe.frozen:
        raise RuntimeError("desktop worker refuses frozen recipes")
    if recipe.protocol_version not in _ALLOWED_DEVELOPMENT_PROTOCOLS:
        raise RuntimeError("desktop worker refuses non-DEVELOPMENT protocol identities")
    if "final" in recipe.recipe_id.lower() or "confirmatory" in recipe.scientific_status.lower():
        raise RuntimeError("desktop worker refuses final/confirmatory recipe identity")


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
