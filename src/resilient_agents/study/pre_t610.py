"""Read-only pre-final readiness checks and a synthetic protocol-v2.1 pipeline smoke.

Nothing in this module authorizes or executes the final reserve. The preflight
materializes the frozen recipe, proves that the framework-neutral StudyService
still refuses final execution without the separate authorization token, and
runs the downstream scientific evidence pipeline only on explicitly synthetic
DEVELOPMENT identities.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Mapping

from ..evidence_v2.analysis_executor_v21 import StudyAnalysisExecutorRouter
from ..evidence_v2.analysis_v21 import V21_STUDENT_T_95_CRITICAL_BY_N
from ..evidence_v2.executors import StudyValidationExecutor
from ..evidence_v2.export_executor_v21 import StudyExportExecutorRouter
from ..evidence_v2.records import (
    PHASE_B_TEMPORAL_SCHEMA_VERSION,
    PhaseAAnalysisRecord,
    PhaseBAnalysisRecord,
    ProbeMeasurement,
)
from ..protocol_v2 import ProtocolV2Branch
from ..protocol_v2_temporal import RewardWindow
from ..git_publish import validate_finalized_run
from ..run_bundle import sha256_file, source_provenance
from .model import (
    ArtifactRole,
    EvidenceClass,
    JobState,
    StudyArtifact,
    StudyExecutionIdentity,
    StudyJobSpec,
    StudyPlan,
    StudyStage,
)
from .planner import StudyPlanner
from .protocol_v2_1_recipe import load_protocol_v21_final_recipe
from .recipe import StudyRecipe
from .scheduler import StudyExecutorRegistry, StudyScheduler
from .service import StudyService
from .store import StudyStore

_FINAL_AUTHORITY = Path("configs/protocols/protocol-v2.1-final.json")
_FINAL_STUDY_ID = "protocol-v2.1-final"
_REPLACEMENT_EXECUTION_ID = "protocol-v2.1-final--t610-recovery-01"
_RECOVERY_DECISION_ID = "DEC-062"
_REPLACEMENT_SOURCE_COMMIT = "86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730"
_FAILED_SOURCE_COMMIT = "7442dcb65674dcb3bc9ce0c71996418289d79061"
_FAILED_MANIFEST_SHA256 = "0c6c18ae9892ed48766543c5747d0cf7f1d78c700246ace28e2f26825d7d5865"
_FAILED_LIFECYCLE_SHA256 = "10cae9facbe34fdd9a0447fb9e1acfb12689584c7fb0ae3beefb85b767e366dc"
_FAILED_EVENTS_SHA256 = "49cf34aef054611e3cdaa2fabeb53ceb488e899c90865020f0f090b1ebe9ae6e"
_FAILED_ARTIFACTS_SHA256 = "c6f5c4f6dba69ef690d39274bcc7c6bd55c22bfa611f61ece8260510c730bb4d"
_FAILED_PLAN_SHA256 = "073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4"
_EXPECTED_GATE = "requires-explicit-t610-gate"
_SYNTHETIC_STUDY_ID = "protocol-v2.1-synthetic-smoke"
_METHODS = ("q_learning", "sarsa")
_ROOTS = ("synthetic-r01", "synthetic-r02")
_LAYOUT = "synthetic-layout-a"
_CONDITION = "synthetic-action-remap"


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return payload


def _write_bytes(root: Path, relative: str, data: bytes) -> tuple[str, str]:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return relative, hashlib.sha256(data).hexdigest()


def _write_json(root: Path, relative: str, payload: Mapping[str, Any]) -> tuple[str, str]:
    data = (
        json.dumps(payload, allow_nan=False, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    return _write_bytes(root, relative, data)


def _validate_preserved_failed_attempt(
    repo_root: Path,
    *,
    recipe: StudyRecipe,
) -> dict[str, Any]:
    study_dir = repo_root / "results" / "studies" / _FINAL_STUDY_ID
    expected_files = {
        "manifest.json": _FAILED_MANIFEST_SHA256,
        "lifecycle.json": _FAILED_LIFECYCLE_SHA256,
        "events.jsonl": _FAILED_EVENTS_SHA256,
        "artifacts.jsonl": _FAILED_ARTIFACTS_SHA256,
    }
    if not study_dir.is_dir():
        raise RuntimeError("preserved T-610 failed Study bundle is missing")
    for filename, expected_sha256 in expected_files.items():
        if sha256_file(study_dir / filename) != expected_sha256:
            raise RuntimeError(
                f"preserved T-610 failed Study changed: {filename} SHA-256 mismatch"
            )

    store = StudyStore.load(
        repo_root=repo_root,
        writable_root=repo_root,
        study_id=_FINAL_STUDY_ID,
    )
    expected_progress = {
        "cancelled": 0,
        "completed": 216,
        "infrastructure_failed": 1,
        "pending": 386,
        "resolved": 216,
        "running": 0,
        "scientific_failed": 0,
        "skipped": 0,
        "total": 603,
    }
    if store.recipe.sha256() != recipe.sha256():
        raise RuntimeError("preserved T-610 failed Study recipe identity changed")
    if store.manifest.get("plan_sha256") != _FAILED_PLAN_SHA256:
        raise RuntimeError("preserved T-610 failed Study plan identity changed")
    if store.manifest.get("source", {}).get("git_commit") != _FAILED_SOURCE_COMMIT:
        raise RuntimeError("preserved T-610 failed Study source commit changed")
    if store.manifest.get("status") != "active" or store.manifest.get(
        "finalized_at_utc"
    ) is not None:
        raise RuntimeError("preserved T-610 failed Study no longer has failed/incomplete state")
    if store.lifecycle.progress() != expected_progress:
        raise RuntimeError("preserved T-610 failed Study progress changed")
    failed_job_id = (
        "pb__sarsa__t527-final-r01__gw-l1-final-a__"
        "action-remap-swap-right-down"
    )
    if store.lifecycle.state_for(failed_job_id) is not JobState.INFRASTRUCTURE_FAILED:
        raise RuntimeError("preserved T-610 failed Study failure identity changed")

    artifacts = store.artifacts()
    run_artifacts = tuple(
        item for item in artifacts if item.role is ArtifactRole.RUN_BUNDLE
    )
    if len(artifacts) != 936 or len(run_artifacts) != 216:
        raise RuntimeError("preserved T-610 failed Study artifact inventory changed")
    for artifact in run_artifacts:
        run_id = artifact.metadata.get("run_id")
        if not isinstance(run_id, str) or not run_id.startswith(
            _FINAL_STUDY_ID + "--"
        ):
            raise RuntimeError("preserved T-610 failed Study run identity is invalid")
        validate_finalized_run(repo_root=repo_root, run_id=run_id)

    return {
        "study_id": _FINAL_STUDY_ID,
        "source_git_commit": _FAILED_SOURCE_COMMIT,
        "recipe_sha256": recipe.sha256(),
        "plan_sha256": _FAILED_PLAN_SHA256,
        "progress": expected_progress,
        "artifact_count": len(artifacts),
        "run_bundle_count": len(run_artifacts),
        "eligible_for_replacement_evidence": False,
        "eligible_for_t611_or_later": False,
    }


def _window_series(values: tuple[float, ...]) -> tuple[RewardWindow, ...]:
    if len(values) != 8:
        raise ValueError("synthetic recovery smoke requires exactly eight windows")
    return tuple(
        RewardWindow(
            start_interaction=index * 32 + 1,
            end_interaction=(index + 1) * 32,
            interaction_count=32,
            mean_reward=value,
        )
        for index, value in enumerate(values)
    )


def _analysis_spec() -> dict[str, Any]:
    return {
        "analysis_recipe": "protocol-v2-root-level-v2.1",
        "phase_a_metric": "return_mean",
        "phase_a_direction": "higher-is-better",
        "phase_b_metric": "return_sum",
        "phase_b_direction": "higher-is-better",
        "layout_aggregation": "equal-weight",
        "require_complete_layout_blocks": True,
        "interval": {
            "kind": "student-t",
            "confidence": 0.95,
            "critical_value_by_n": {
                str(n): value for n, value in V21_STUDENT_T_95_CRITICAL_BY_N.items()
            },
        },
        "recovery": {
            "window_size": 32,
            "observation_horizon": 256,
            "tolerance": 0.10,
            "sensitivity_tolerances": [0.05, 0.20],
            "stability_windows": 2,
            "primary_condition_family": "action-remap",
        },
    }


def _synthetic_recipe_and_plan() -> tuple[StudyRecipe, StudyPlan]:
    recipe = StudyRecipe(
        recipe_id=_SYNTHETIC_STUDY_ID,
        protocol_version="protocol-v2.1",
        evidence_class=EvidenceClass.DEVELOPMENT,
        scientific_status="synthetic-pre-final-pipeline-smoke",
        frozen=False,
        study={"purpose": "synthetic protocol-v2.1 downstream scientific pipeline smoke"},
    )
    phase_a_jobs: list[StudyJobSpec] = []
    phase_b_jobs: list[StudyJobSpec] = []
    phase_b_ids: list[str] = []
    for method in _METHODS:
        for root in _ROOTS:
            pa_id = f"pa__{method}__{root}__{_LAYOUT}"
            pb_id = f"pb__{method}__{root}__{_LAYOUT}__{_CONDITION}"
            phase_a_jobs.append(
                StudyJobSpec(
                    job_id=pa_id,
                    stage=StudyStage.PHASE_A,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    payload={
                        "job_type": "phase-a-training",
                        "method": {"method_id": method},
                        "root": {"root_id": root},
                        "layout": {"layout_id": _LAYOUT},
                    },
                )
            )
            phase_b_jobs.append(
                StudyJobSpec(
                    job_id=pb_id,
                    stage=StudyStage.PHASE_B,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    dependencies=(pa_id,),
                    payload={
                        "job_type": "phase-b-matched-set",
                        "method": {"method_id": method},
                        "root": {"root_id": root},
                        "layout": {"layout_id": _LAYOUT},
                        "condition": {
                            "condition_id": _CONDITION,
                            "family": "action-remap",
                        },
                        "execution": {
                            "prefix_interactions": 1,
                            "interaction_budget_per_branch": 256,
                            "episode_reset_policy_id": "synthetic-persistent-deployment",
                            "subsequent_episode_seed_count": 256,
                            "temporal_evidence_id": "synthetic-fixed-window-v1",
                            "temporal_window_size": 32,
                        },
                        "branches": ["FN", "FD", "AN", "AD"],
                    },
                )
            )
            phase_b_ids.append(pb_id)
    derived = (
        StudyJobSpec(
            job_id="validate-study",
            stage=StudyStage.VALIDATION,
            evidence_class=EvidenceClass.DERIVED,
            dependencies=tuple(phase_b_ids),
            payload={
                "job_type": "study-validation",
                "specification": {"validator": "protocol-v2.1-study-temporal"},
            },
        ),
        StudyJobSpec(
            job_id="analyze-study",
            stage=StudyStage.ANALYSIS,
            evidence_class=EvidenceClass.DERIVED,
            dependencies=("validate-study",),
            payload={"job_type": "study-analysis", "specification": _analysis_spec()},
        ),
        StudyJobSpec(
            job_id="export-study",
            stage=StudyStage.EXPORT,
            evidence_class=EvidenceClass.DERIVED,
            dependencies=("analyze-study",),
            payload={
                "job_type": "study-export",
                "specification": {
                    "package": "protocol-v2-evidence-handoff-v2",
                    "emit_csv": True,
                },
            },
        ),
    )
    return recipe, StudyPlan(
        study_id=recipe.recipe_id,
        jobs=tuple((*phase_a_jobs, *phase_b_jobs, *derived)),
    )


def _phase_a_value(method: str, root: str) -> float:
    return {
        ("q_learning", "synthetic-r01"): 0.80,
        ("q_learning", "synthetic-r02"): 0.90,
        ("sarsa", "synthetic-r01"): 0.70,
        ("sarsa", "synthetic-r02"): 0.75,
    }[(method, root)]


def _branch_metric(method: str, root: str, branch: ProtocolV2Branch) -> float:
    values = {
        ("q_learning", "synthetic-r01"): {"FN": 100, "FD": 70, "AN": 90, "AD": 80},
        ("q_learning", "synthetic-r02"): {"FN": 110, "FD": 80, "AN": 100, "AD": 95},
        ("sarsa", "synthetic-r01"): {"FN": 90, "FD": 60, "AN": 85, "AD": 70},
        ("sarsa", "synthetic-r02"): {"FN": 95, "FD": 70, "AN": 90, "AD": 75},
    }
    return float(values[(method, root)][branch.value])


def _branch_windows(
    method: str,
    root: str,
    branch: ProtocolV2Branch,
) -> tuple[RewardWindow, ...]:
    if branch in {ProtocolV2Branch.FROZEN_NOMINAL, ProtocolV2Branch.ADAPTIVE_NOMINAL}:
        return _window_series((1.0,) * 8)
    if branch is ProtocolV2Branch.FROZEN_DISTURBED:
        return _window_series((0.70,) * 8)
    adaptive_disturbed = {
        ("q_learning", "synthetic-r01"): (0.60, 0.75, 0.88, 0.92, 0.95, 0.96, 0.97, 0.98),
        ("q_learning", "synthetic-r02"): (0.70, 0.89, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98),
        ("sarsa", "synthetic-r01"): (0.50, 0.60, 0.75, 0.85, 0.91, 0.93, 0.94, 0.95),
        ("sarsa", "synthetic-r02"): (0.50, 0.70, 0.80, 0.85, 0.88, 0.89, 0.89, 0.89),
    }
    return _window_series(adaptive_disturbed[(method, root)])


def _record_phase_a_synthetic_evidence(store: StudyStore) -> dict[tuple[str, str], str]:
    root = store.writable_root
    checkpoints: dict[tuple[str, str], str] = {}
    for method in _METHODS:
        for root_id in _ROOTS:
            pa_id = f"pa__{method}__{root_id}__{_LAYOUT}"
            store.start_job(pa_id)
            run_rel, run_sha = _write_json(root, f"results/runs/{pa_id}/run.json", {"synthetic": True})
            run_artifact_id = f"{pa_id}-run"
            store.record_artifact(
                StudyArtifact(
                    artifact_id=run_artifact_id,
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=run_rel,
                    sha256=run_sha,
                    source_job_ids=(pa_id,),
                    metadata={"synthetic": True},
                )
            )
            cp_rel, cp_sha = _write_bytes(root, f"results/runs/{pa_id}/checkpoint.bin", b"synthetic-checkpoint")
            checkpoint_id = f"{pa_id}-checkpoint"
            checkpoints[(method, root_id)] = checkpoint_id
            store.record_artifact(
                StudyArtifact(
                    artifact_id=checkpoint_id,
                    role=ArtifactRole.SCIENTIFIC_CHECKPOINT,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=cp_rel,
                    sha256=cp_sha,
                    source_job_ids=(pa_id,),
                    source_artifact_ids=(run_artifact_id,),
                    metadata={"synthetic": True},
                )
            )
            final = _phase_a_value(method, root_id)
            pa_record = PhaseAAnalysisRecord(
                study_id=store.plan.study_id,
                job_id=pa_id,
                method_id=method,
                root_id=root_id,
                layout_id=_LAYOUT,
                probes=(
                    ProbeMeasurement(interaction_index=0, metrics={"return_mean": final - 0.20}),
                    ProbeMeasurement(interaction_index=8192, metrics={"return_mean": final}),
                ),
                resource_metrics={"environment_interactions": 8192.0},
            )
            pa_rel, pa_sha = _write_json(root, f"results/runs/{pa_id}/analysis.json", pa_record.to_dict())
            store.record_artifact(
                StudyArtifact(
                    artifact_id=f"{pa_id}-analysis",
                    role=ArtifactRole.ANALYSIS_DATA,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=pa_rel,
                    sha256=pa_sha,
                    source_job_ids=(pa_id,),
                    source_artifact_ids=(run_artifact_id, checkpoint_id),
                    metadata={"record_type": "phase-a", "synthetic": True},
                )
            )
            store.complete_job(pa_id)
    return checkpoints


def _record_phase_b_synthetic_evidence(
    store: StudyStore,
    checkpoints: Mapping[tuple[str, str], str],
) -> None:
    root = store.writable_root
    for method in _METHODS:
        for root_id in _ROOTS:
            pb_id = f"pb__{method}__{root_id}__{_LAYOUT}__{_CONDITION}"
            checkpoint_id = checkpoints[(method, root_id)]
            store.start_job(pb_id)
            pb_run_rel, pb_run_sha = _write_json(root, f"results/runs/{pb_id}/run.json", {"synthetic": True})
            pb_run_id = f"{pb_id}-run"
            store.record_artifact(
                StudyArtifact(
                    artifact_id=pb_run_id,
                    role=ArtifactRole.RUN_BUNDLE,
                    evidence_class=EvidenceClass.DEVELOPMENT,
                    relative_path=pb_run_rel,
                    sha256=pb_run_sha,
                    source_job_ids=(pb_id,),
                    source_artifact_ids=(checkpoint_id,),
                    metadata={"synthetic": True},
                )
            )
            for branch in ProtocolV2Branch:
                record = PhaseBAnalysisRecord(
                    schema_version=PHASE_B_TEMPORAL_SCHEMA_VERSION,
                    study_id=store.plan.study_id,
                    job_id=pb_id,
                    method_id=method,
                    root_id=root_id,
                    layout_id=_LAYOUT,
                    condition_id=_CONDITION,
                    branch=branch,
                    checkpoint_artifact_id=checkpoint_id,
                    metrics={"return_sum": _branch_metric(method, root_id, branch)},
                    resource_metrics={"environment_interactions": 256.0},
                    reward_windows=_branch_windows(method, root_id, branch),
                )
                branch_rel, branch_sha = _write_json(
                    root,
                    f"results/runs/{pb_id}/{branch.value.lower()}-analysis.json",
                    record.to_dict(),
                )
                store.record_artifact(
                    StudyArtifact(
                        artifact_id=f"{pb_id}-{branch.value.lower()}-analysis",
                        role=ArtifactRole.ANALYSIS_DATA,
                        evidence_class=EvidenceClass.DEVELOPMENT,
                        relative_path=branch_rel,
                        sha256=branch_sha,
                        source_job_ids=(pb_id,),
                        source_artifact_ids=(checkpoint_id, pb_run_id),
                        metadata={"record_type": "phase-b", "branch": branch.value, "synthetic": True},
                    )
                )
            store.complete_job(pb_id)


def _record_synthetic_scientific_evidence(store: StudyStore) -> None:
    checkpoints = _record_phase_a_synthetic_evidence(store)
    _record_phase_b_synthetic_evidence(store, checkpoints)


def run_synthetic_protocol_v21_pipeline_smoke(repo_root: Path) -> dict[str, Any]:
    """Exercise validation -> v2.1 analysis -> export -> finalization on synthetic evidence."""

    repo_root = Path(repo_root).resolve()
    with tempfile.TemporaryDirectory(prefix="protocol-v21-synthetic-smoke-") as directory:
        writable_root = Path(directory).resolve()
        recipe, plan = _synthetic_recipe_and_plan()
        store = StudyStore.create(
            repo_root=repo_root,
            writable_root=writable_root,
            recipe=recipe,
            plan=plan,
        )
        _record_synthetic_scientific_evidence(store)
        scheduler = StudyScheduler(
            store=store,
            executors=StudyExecutorRegistry(
                [
                    StudyValidationExecutor(),
                    StudyAnalysisExecutorRouter(),
                    StudyExportExecutorRouter(),
                ]
            ),
        )
        results = scheduler.run_ready()
        if tuple(item.job_id for item in results) != (
            "validate-study",
            "analyze-study",
            "export-study",
        ):
            raise RuntimeError("synthetic pipeline derived-stage execution order mismatch")
        store.finalize()
        reloaded = StudyStore.load(
            repo_root=repo_root,
            writable_root=writable_root,
            study_id=_SYNTHETIC_STUDY_ID,
        )
        artifacts = {item.artifact_id: item for item in reloaded.artifacts()}
        required = {
            "validation-report",
            "analysis-package",
            "evidence-handoff-package",
            "thesis-table-phase-a-method-contrasts",
            "thesis-table-phase-b-method-contrasts",
            "thesis-table-recovery-method-contrasts",
            "analysis-table-recovery-trajectories",
        }
        missing = sorted(required - set(artifacts))
        if missing:
            raise RuntimeError(f"synthetic pipeline is missing derived artifacts: {missing}")
        analysis = _read_json(writable_root / artifacts["analysis-package"].relative_path)
        recovery = analysis["phase_b"]["recovery"]
        statuses = {row["status"] for row in recovery["root_records"]}
        if not {"recovered", "right-censored"}.issubset(statuses):
            raise RuntimeError("synthetic recovery smoke did not exercise both recovery outcomes")
        if analysis.get("analysis_recipe") != "protocol-v2-root-level-v2.1":
            raise RuntimeError("synthetic analysis did not use the protocol-v2.1 analysis identity")
        if analysis.get("interval_policy", {}).get("critical_value_selected_by") != "actual-independent-root-count":
            raise RuntimeError("synthetic analysis did not retain actual-root interval provenance")
        return {
            "schema_version": 1,
            "study_id": _SYNTHETIC_STUDY_ID,
            "evidence_class": "development",
            "final_identities_used": False,
            "scientific_jobs": len(_METHODS) * len(_ROOTS) * 2,
            "derived_jobs": len(results),
            "analysis_recipe": analysis["analysis_recipe"],
            "recovery_statuses_exercised": sorted(statuses),
            "evidence_package": artifacts["evidence-handoff-package"].metadata.get("package"),
            "finalized": True,
        }


def run_protocol_v21_preflight(repo_root: Path) -> dict[str, Any]:
    """Return a fail-closed readiness report without authorizing final execution."""

    repo_root = Path(repo_root).resolve()
    source = source_provenance(repo_root)
    if (
        source.get("git_commit") is None
        or source.get("tracked_changes_present") is not False
        or source.get("untracked_nonoutput_present") is not False
    ):
        raise RuntimeError("protocol-v2.1 recovery preflight requires clean Git source")
    authority_path = repo_root / _FINAL_AUTHORITY
    authority = _read_json(authority_path)
    if authority.get("final_reserve_access") is not False:
        raise RuntimeError("protocol-v2.1 final reserve is not sealed")
    if authority.get("execution_authorization") != _EXPECTED_GATE:
        raise RuntimeError("protocol-v2.1 explicit final-execution gate changed")

    recipe = load_protocol_v21_final_recipe(repo_root)
    preview = StudyPlanner(recipe).preview()
    expected_preview = {
        "method_count": 5,
        "reference_count": 0,
        "root_count": 12,
        "layout_count": 2,
        "condition_count": 4,
        "phase_a_jobs": 120,
        "phase_b_jobs": 480,
        "validation_jobs": 1,
        "analysis_jobs": 1,
        "export_jobs": 1,
        "total_jobs": 603,
    }
    actual_preview = preview.to_dict()
    for key, expected in expected_preview.items():
        if actual_preview.get(key) != expected:
            raise RuntimeError(f"protocol-v2.1 plan preview mismatch for {key}")

    failed_attempt = _validate_preserved_failed_attempt(repo_root, recipe=recipe)
    replacement_bundle = (
        repo_root / "results" / "studies" / _REPLACEMENT_EXECUTION_ID
    )
    if replacement_bundle.exists():
        raise RuntimeError(
            "the T-610 replacement Study already exists; inspect it before execution"
        )
    replacement_run_prefix = _REPLACEMENT_EXECUTION_ID + "--"
    runs_root = repo_root / "results" / "runs"
    if runs_root.is_dir() and any(
        path.name.startswith(replacement_run_prefix) for path in runs_root.iterdir()
    ):
        raise RuntimeError("a T-610 replacement run directory already exists")
    run_index = repo_root / "results" / "run-index.jsonl"
    if run_index.is_file():
        for line in run_index.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if str(record.get("run_id", "")).startswith(replacement_run_prefix):
                raise RuntimeError("a T-610 replacement run-index record already exists")

    # Plan creation is non-executing. The call below proves the generic backend
    # refuses even the first final job without the separate explicit authority.
    with tempfile.TemporaryDirectory(prefix="protocol-v21-gate-check-") as directory:
        writable_root = Path(directory).resolve()
        service = StudyService(
            repo_root=repo_root,
            writable_root=writable_root,
            executors=StudyExecutorRegistry(),
        )
        identity = StudyExecutionIdentity.replacement(
            execution_instance_id=_REPLACEMENT_EXECUTION_ID,
            scientific_recipe_id=recipe.recipe_id,
            predecessor_execution_instance_id=_FINAL_STUDY_ID,
            recovery_decision_id=_RECOVERY_DECISION_ID,
        )
        service.create(recipe, execution_identity=identity)
        try:
            service.run_ready(_REPLACEMENT_EXECUTION_ID, max_jobs=1)
        except RuntimeError as exc:
            if "separate explicit scientific execution authorization" not in str(exc):
                raise
        else:
            raise RuntimeError("generic StudyService did not enforce the final execution gate")
        final_store = StudyStore.load(
            repo_root=repo_root,
            writable_root=writable_root,
            study_id=_REPLACEMENT_EXECUTION_ID,
        )
        if any(final_store.lifecycle.attempts_for(job.job_id) for job in final_store.plan.jobs):
            raise RuntimeError("final gate preflight unexpectedly started a scientific job")
        if final_store.artifacts():
            raise RuntimeError("final gate preflight unexpectedly produced evidence")

    return {
        "schema_version": 1,
        "protocol_id": "protocol-v2.1",
        "study_id": _FINAL_STUDY_ID,
        "replacement_execution_instance_id": _REPLACEMENT_EXECUTION_ID,
        "recovery_decision_id": _RECOVERY_DECISION_ID,
        "recipe_sha256": recipe.sha256(),
        "plan_preview": expected_preview,
        "final_reserve_access": False,
        "execution_authorization": _EXPECTED_GATE,
        "backend_default_execution_blocked": True,
        "preserved_failed_attempt": failed_attempt,
        "replacement_bundle_present": False,
        "final_execution_authorized": False,
        "ready_for_recovery_execution_authorization": True,
    }


def validate_protocol_v21_t610_completion(repo_root: Path) -> dict[str, Any]:
    """Validate operational T-610 completion without interpreting outcomes."""

    repo_root = Path(repo_root).resolve()
    recipe = load_protocol_v21_final_recipe(repo_root)
    failed_attempt = _validate_preserved_failed_attempt(repo_root, recipe=recipe)
    store = StudyStore.load(
        repo_root=repo_root,
        writable_root=repo_root,
        study_id=_REPLACEMENT_EXECUTION_ID,
    )
    expected_progress = {
        "cancelled": 0,
        "completed": 603,
        "infrastructure_failed": 0,
        "pending": 0,
        "resolved": 603,
        "running": 0,
        "scientific_failed": 0,
        "skipped": 0,
        "total": 603,
    }
    if store.recipe.sha256() != recipe.sha256():
        raise RuntimeError("T-610 replacement recipe identity changed")
    if store.manifest.get("plan_sha256") != _FAILED_PLAN_SHA256:
        raise RuntimeError("T-610 replacement plan identity changed")
    if store.lifecycle.progress() != expected_progress:
        raise RuntimeError("T-610 replacement lifecycle is not complete")
    if store.manifest.get("status") != "completed" or not (
        store.study_dir / "FINALIZED"
    ).is_file():
        raise RuntimeError("T-610 replacement is not durably finalized")
    source = store.manifest.get("source")
    if not isinstance(source, Mapping) or (
        source.get("git_commit") != _REPLACEMENT_SOURCE_COMMIT
        or source.get("tracked_changes_present") is not False
        or source.get("untracked_nonoutput_present") is not False
    ):
        raise RuntimeError("T-610 replacement source provenance changed")
    identity = store.manifest.get("execution_identity")
    if not isinstance(identity, Mapping) or (
        identity.get("execution_instance_id") != _REPLACEMENT_EXECUTION_ID
        or identity.get("scientific_recipe_id") != _FINAL_STUDY_ID
        or identity.get("predecessor_execution_instance_id") != _FINAL_STUDY_ID
        or identity.get("recovery_decision_id") != _RECOVERY_DECISION_ID
        or identity.get("source_git_commit") != _REPLACEMENT_SOURCE_COMMIT
    ):
        raise RuntimeError("T-610 replacement execution lineage changed")

    artifacts = store.artifacts()
    run_artifacts = tuple(
        artifact for artifact in artifacts if artifact.role is ArtifactRole.RUN_BUNDLE
    )
    if len(artifacts) != 3255 or len(run_artifacts) != 600:
        raise RuntimeError("T-610 replacement artifact inventory changed")
    for artifact in run_artifacts:
        run_id = artifact.metadata.get("run_id")
        if not isinstance(run_id, str) or not run_id.startswith(
            _REPLACEMENT_EXECUTION_ID + "--"
        ):
            raise RuntimeError("T-610 replacement run identity is invalid")
        validate_finalized_run(repo_root=repo_root, run_id=run_id)

    return {
        "study_id": _REPLACEMENT_EXECUTION_ID,
        "scientific_recipe_id": _FINAL_STUDY_ID,
        "source_git_commit": _REPLACEMENT_SOURCE_COMMIT,
        "recipe_sha256": recipe.sha256(),
        "plan_sha256": _FAILED_PLAN_SHA256,
        "progress": expected_progress,
        "artifact_count": len(artifacts),
        "run_bundle_count": len(run_artifacts),
        "finalized": True,
        "failed_attempt": failed_attempt,
        "outcomes_interpreted": False,
    }


def run_pre_t610_readiness_package(repo_root: Path) -> dict[str, Any]:
    """Run both read-only final preflight and synthetic downstream smoke."""

    return {
        "preflight": run_protocol_v21_preflight(repo_root),
        "synthetic_pipeline_smoke": run_synthetic_protocol_v21_pipeline_smoke(repo_root),
    }
