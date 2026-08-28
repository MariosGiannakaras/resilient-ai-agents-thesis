"""Explicit planned/observed outcome denominators for protocol-v2 Study analysis."""
from __future__ import annotations

from collections import Counter
from typing import Any

from ..study.model import JobState, StudyStage
from ..study.store import StudyStore


def _counts(states: list[JobState]) -> dict[str, int]:
    counter = Counter(state.value for state in states)
    return {
        "planned": len(states),
        "completed": counter[JobState.COMPLETED.value],
        "scientific_failed": counter[JobState.SCIENTIFIC_FAILED.value],
        "skipped": counter[JobState.SKIPPED.value],
        "infrastructure_failed": counter[JobState.INFRASTRUCTURE_FAILED.value],
        "cancelled": counter[JobState.CANCELLED.value],
        "pending": counter[JobState.PENDING.value],
        "running": counter[JobState.RUNNING.value],
    }


def build_scientific_denominators(store: StudyStore) -> dict[str, Any]:
    """Return outcome counts without replacing or imputing scientific units."""

    if not isinstance(store, StudyStore):
        raise ValueError("store must be StudyStore")

    phase_a: dict[str, list[JobState]] = {}
    references: dict[str, list[JobState]] = {}
    phase_b: dict[tuple[str, str], list[JobState]] = {}

    for job in store.plan.jobs_for_stage(StudyStage.PHASE_A):
        job_type = job.payload.get("job_type")
        state = store.lifecycle.state_for(job.job_id)
        if job_type == "phase-a-training":
            method = job.payload.get("method", {})
            method_id = str(method.get("method_id"))
            phase_a.setdefault(method_id, []).append(state)
        elif job_type == "phase-a-reference":
            reference = job.payload.get("reference", {})
            reference_id = str(reference.get("reference_id"))
            references.setdefault(reference_id, []).append(state)

    for job in store.plan.jobs_for_stage(StudyStage.PHASE_B):
        if job.payload.get("job_type") != "phase-b-matched-set":
            continue
        method = job.payload.get("method", {})
        condition = job.payload.get("condition", {})
        key = (str(method.get("method_id")), str(condition.get("condition_id")))
        phase_b.setdefault(key, []).append(store.lifecycle.state_for(job.job_id))

    return {
        "phase_a_methods": [
            {"method_id": method_id, **_counts(states)}
            for method_id, states in sorted(phase_a.items())
        ],
        "phase_a_references": [
            {"reference_id": reference_id, **_counts(states)}
            for reference_id, states in sorted(references.items())
        ],
        "phase_b_method_conditions": [
            {
                "method_id": method_id,
                "condition_id": condition_id,
                **_counts(states),
            }
            for (method_id, condition_id), states in sorted(phase_b.items())
        ],
    }
