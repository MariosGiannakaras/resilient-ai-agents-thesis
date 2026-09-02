"""Fail-closed protocol-v2.1 final-evidence validation and freeze package."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from collections import Counter
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

from ..git_publish import validate_finalized_run
from ..run_bundle import sha256_file
from ..study import ArtifactRole, EvidenceClass, StudyPlanner, StudyStore
from ..study.protocol_v2_1_recipe import load_protocol_v21_final_recipe
from .validation import StudyEvidenceValidator

FREEZE_PACKAGE_SCHEMA_VERSION = 1
FINAL_STUDY_ID = "protocol-v2.1-final"
ACCEPTED_EXECUTION_ID = "protocol-v2.1-final--t610-recovery-01"
FREEZE_RELATIVE_DIR = Path("results/final-evidence/protocol-v2.1-final")
EXPECTED_RECIPE_SHA256 = (
    "8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154"
)
EXPECTED_PLAN_SHA256 = (
    "073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4"
)
EXPECTED_EXECUTION_SOURCE_COMMIT = "86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730"
EXPECTED_PROGRESS = {
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
EXPECTED_ROLE_COUNTS = {
    "analysis-data": 2521,
    "analysis-table": 5,
    "evidence-package": 1,
    "provenance": 1,
    "run-bundle": 600,
    "scientific-checkpoint": 120,
    "thesis-table": 6,
    "validation-report": 1,
}
EXPECTED_EVIDENCE_CLASS_COUNTS = {"confirmatory": 3240, "derived": 15}
VALIDATOR_SOURCE_FILES = (
    "scripts/freeze_evidence.py",
    "src/resilient_agents/evidence_v2/freeze.py",
    "src/resilient_agents/evidence_v2/validation.py",
    "src/resilient_agents/git_publish.py",
    "src/resilient_agents/study/pre_t610.py",
    "src/resilient_agents/study/store.py",
)


def _canonical_json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_line(payload: Any) -> bytes:
    return (
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _git(repo_root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.rstrip("\r\n")


def _validate_freeze_time(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("freeze_time_utc must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("freeze_time_utc must include a UTC offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("freeze_time_utc must be UTC")
    return parsed.isoformat().replace("+00:00", "Z")


def _artifact_by_id(store: StudyStore, artifact_id: str):
    matches = [item for item in store.artifacts() if item.artifact_id == artifact_id]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one registered artifact: {artifact_id}")
    return matches[0]


def _validate_registered_report(
    store: StudyStore, report_payload: Mapping[str, Any]
) -> dict[str, Any]:
    artifact = _artifact_by_id(store, "validation-report")
    expected = _canonical_json_bytes(report_payload)
    path = store.writable_root / artifact.relative_path
    actual = path.read_bytes()
    if actual != expected or artifact.sha256 != _sha256_bytes(expected):
        raise RuntimeError(
            "registered validation report disagrees with fresh validation"
        )
    return {
        "artifact_id": artifact.artifact_id,
        "relative_path": artifact.relative_path,
        "sha256": artifact.sha256,
    }


def _validate_handoff_package(store: StudyStore) -> dict[str, Any]:
    artifact = _artifact_by_id(store, "evidence-handoff-package")
    path = store.writable_root / artifact.relative_path
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise TypeError("evidence handoff manifest must be an object")
    if (
        payload.get("schema_version") != 2
        or payload.get("package") != "protocol-v2-evidence-handoff-v2"
        or payload.get("study_id") != ACCEPTED_EXECUTION_ID
        or payload.get("recipe_sha256") != EXPECTED_RECIPE_SHA256
    ):
        raise RuntimeError("evidence handoff manifest identity is invalid")
    files = payload.get("files")
    if not isinstance(files, list) or len(files) != 12:
        raise RuntimeError("evidence handoff manifest file inventory is invalid")
    registered = {item.artifact_id: item for item in store.artifacts()}
    for row in files:
        if not isinstance(row, Mapping):
            raise TypeError("evidence handoff file entry must be an object")
        registered_artifact = registered.get(str(row.get("artifact_id")))
        if registered_artifact is None or registered_artifact.sha256 != row.get(
            "sha256"
        ):
            raise RuntimeError(
                "evidence handoff file is not registered with the declared hash"
            )
    return {
        "artifact_id": artifact.artifact_id,
        "relative_path": artifact.relative_path,
        "sha256": artifact.sha256,
        "file_count": len(files),
    }


def _run_inventory(store: StudyStore) -> tuple[bytes, str]:
    entries: list[dict[str, Any]] = []
    for artifact in sorted(
        (item for item in store.artifacts() if item.role is ArtifactRole.RUN_BUNDLE),
        key=lambda item: item.artifact_id,
    ):
        run_id = artifact.metadata.get("run_id")
        if not isinstance(run_id, str) or not run_id.startswith(
            ACCEPTED_EXECUTION_ID + "--"
        ):
            raise RuntimeError(
                "accepted evidence contains a mixed or invalid run identity"
            )
        manifest = validate_finalized_run(repo_root=store.repo_root, run_id=run_id)
        source = manifest.get("source")
        if (
            not isinstance(source, Mapping)
            or source.get("git_commit") != EXPECTED_EXECUTION_SOURCE_COMMIT
        ):
            raise RuntimeError(f"accepted run has mixed source provenance: {run_id}")
        if (
            manifest.get("protocol_version") != "protocol-v2.1"
            or manifest.get("status") != "completed"
        ):
            raise RuntimeError(f"accepted run has invalid protocol/status: {run_id}")
        entries.append(
            {
                "artifact_id": artifact.artifact_id,
                "manifest_sha256": artifact.sha256,
                "run_id": run_id,
                "source_git_commit": source["git_commit"],
            }
        )
    if len(entries) != 600:
        raise RuntimeError("accepted evidence must contain exactly 600 run bundles")
    data = b"".join(_canonical_json_line(entry) for entry in entries)
    return data, _sha256_bytes(data)


def _write_package_atomic(
    output_dir: Path, *, manifest_bytes: bytes, inventory_bytes: bytes
) -> str:
    if output_dir.exists():
        raise RuntimeError(
            "final-evidence freeze package already exists; refusing overwrite"
        )
    staging = output_dir.with_name(output_dir.name + ".staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    (staging / "freeze-manifest.json").write_bytes(manifest_bytes)
    (staging / "run-manifest-inventory.jsonl").write_bytes(inventory_bytes)
    manifest_sha256 = _sha256_bytes(manifest_bytes)
    marker = (
        f"schema_version={FREEZE_PACKAGE_SCHEMA_VERSION}\n"
        "status=frozen\n"
        f"manifest_sha256={manifest_sha256}\n"
    ).encode()
    (staging / "FINALIZED").write_bytes(marker)
    staging.replace(output_dir)
    return manifest_sha256


def validate_protocol_v21_final_freeze(repo_root: Path) -> dict[str, Any]:
    """Verify the durable freeze envelope without recomputing scientific outcomes."""

    repo_root = Path(repo_root).resolve()
    output_dir = repo_root / FREEZE_RELATIVE_DIR
    manifest_path = output_dir / "freeze-manifest.json"
    inventory_path = output_dir / "run-manifest-inventory.jsonl"
    marker_path = output_dir / "FINALIZED"
    if not all(path.is_file() for path in (manifest_path, inventory_path, marker_path)):
        raise RuntimeError("final-evidence freeze package is incomplete")

    manifest_sha256 = sha256_file(manifest_path)
    marker_fields: dict[str, str] = {}
    for line in marker_path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if not separator or not key or key in marker_fields:
            raise RuntimeError("final-evidence freeze marker is malformed")
        marker_fields[key] = value
    if marker_fields != {
        "schema_version": str(FREEZE_PACKAGE_SCHEMA_VERSION),
        "status": "frozen",
        "manifest_sha256": manifest_sha256,
    }:
        raise RuntimeError("final-evidence freeze marker does not match manifest")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, Mapping):
        raise TypeError("final-evidence freeze manifest must be an object")
    expected_identity = {
        "schema_version": FREEZE_PACKAGE_SCHEMA_VERSION,
        "status": "frozen",
        "scientific_recipe_id": FINAL_STUDY_ID,
        "accepted_execution_instance_id": ACCEPTED_EXECUTION_ID,
        "execution_source_git_commit": EXPECTED_EXECUTION_SOURCE_COMMIT,
        "recipe_sha256": EXPECTED_RECIPE_SHA256,
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "artifact_count": 3255,
        "run_bundle_count": 600,
        "scientific_outcomes_interpreted": False,
    }
    if any(manifest.get(key) != value for key, value in expected_identity.items()):
        raise RuntimeError("final-evidence freeze manifest identity is invalid")
    if (
        manifest.get("progress") != EXPECTED_PROGRESS
        or manifest.get("artifact_role_counts") != EXPECTED_ROLE_COUNTS
        or manifest.get("artifact_evidence_class_counts")
        != EXPECTED_EVIDENCE_CLASS_COUNTS
    ):
        raise RuntimeError("final-evidence freeze manifest counts are invalid")

    inventory_metadata = manifest.get("run_manifest_inventory")
    if not isinstance(inventory_metadata, Mapping):
        raise TypeError("run manifest inventory metadata must be an object")
    if (
        inventory_metadata.get("relative_path")
        != (FREEZE_RELATIVE_DIR / inventory_path.name).as_posix()
        or inventory_metadata.get("record_count") != 600
        or inventory_metadata.get("sha256") != sha256_file(inventory_path)
    ):
        raise RuntimeError("run manifest inventory integrity is invalid")
    run_ids: set[str] = set()
    for number, line in enumerate(
        inventory_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"run manifest inventory line {number} is invalid JSON"
            ) from exc
        if not isinstance(entry, Mapping) or set(entry) != {
            "artifact_id",
            "manifest_sha256",
            "run_id",
            "source_git_commit",
        }:
            raise RuntimeError(f"run manifest inventory line {number} is invalid")
        run_id = entry["run_id"]
        if (
            not isinstance(run_id, str)
            or not run_id.startswith(ACCEPTED_EXECUTION_ID + "--")
            or run_id in run_ids
            or entry["source_git_commit"] != EXPECTED_EXECUTION_SOURCE_COMMIT
        ):
            raise RuntimeError(
                f"run manifest inventory line {number} is mixed/duplicate"
            )
        run_ids.add(run_id)
    if len(run_ids) != 600:
        raise RuntimeError(
            "run manifest inventory must contain exactly 600 unique runs"
        )

    study_dir = repo_root / "results" / "studies" / ACCEPTED_EXECUTION_ID
    if manifest.get("study_manifest_sha256") != sha256_file(
        study_dir / "manifest.json"
    ) or manifest.get("study_finalization_marker_sha256") != sha256_file(
        study_dir / "FINALIZED"
    ):
        raise RuntimeError("frozen Study envelope integrity is invalid")
    for key in ("validation_report", "evidence_handoff_package"):
        reference = manifest.get(key)
        if not isinstance(reference, Mapping):
            raise TypeError(f"{key} reference must be an object")
        path = repo_root / str(reference.get("relative_path"))
        if reference.get("sha256") != sha256_file(path):
            raise RuntimeError(f"frozen {key} integrity is invalid")

    validator = manifest.get("validator")
    if not isinstance(validator, Mapping) or not isinstance(
        validator.get("source_files"), list
    ):
        raise TypeError("freeze validator provenance is invalid")
    for record in validator["source_files"]:
        if not isinstance(record, Mapping):
            raise TypeError("freeze validator source record must be an object")
        path = repo_root / str(record.get("relative_path"))
        if record.get("sha256") != sha256_file(path):
            raise RuntimeError("freeze validator source file hash mismatch")
    return {
        "valid": True,
        "freeze_manifest_sha256": manifest_sha256,
        "run_manifest_inventory_sha256": inventory_metadata["sha256"],
        "run_bundle_count": len(run_ids),
    }


def validate_and_freeze_protocol_v21_final(
    repo_root: Path,
    *,
    validator_git_commit: str,
    freeze_time_utc: str,
) -> dict[str, Any]:
    """Validate the accepted replacement and atomically freeze references to it."""

    repo_root = Path(repo_root).resolve()
    freeze_time = _validate_freeze_time(freeze_time_utc)
    if _git(repo_root, "rev-parse", "HEAD") != validator_git_commit:
        raise RuntimeError("validator_git_commit must equal the checked-out HEAD")
    if _git(repo_root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError(
            "tracked working tree must be clean before final-evidence freeze"
        )

    # Import lazily because pre_t610 imports evidence_v2 executors through this
    # package; eager import here would create a package-initialization cycle.
    from ..study.pre_t610 import validate_protocol_v21_t610_completion

    completion = validate_protocol_v21_t610_completion(repo_root)
    if (
        completion["study_id"] != ACCEPTED_EXECUTION_ID
        or completion["source_git_commit"] != EXPECTED_EXECUTION_SOURCE_COMMIT
        or completion["recipe_sha256"] != EXPECTED_RECIPE_SHA256
        or completion["plan_sha256"] != EXPECTED_PLAN_SHA256
        or completion["progress"] != EXPECTED_PROGRESS
        or completion["run_bundle_count"] != 600
    ):
        raise RuntimeError(
            "T-610 completion handoff does not match the accepted T-611 identity"
        )

    store = StudyStore.load(
        repo_root=repo_root,
        writable_root=repo_root,
        study_id=ACCEPTED_EXECUTION_ID,
    )
    recipe = load_protocol_v21_final_recipe(repo_root)
    if (
        recipe.sha256() != EXPECTED_RECIPE_SHA256
        or store.plan != StudyPlanner(recipe).materialize()
    ):
        raise RuntimeError(
            "stored Study recipe/plan differs from canonical materialization"
        )

    report = StudyEvidenceValidator().validate(store)
    if (
        not report.valid
        or report.findings
        or report.to_dict()
        != {
            "study_id": ACCEPTED_EXECUTION_ID,
            "recipe_sha256": EXPECTED_RECIPE_SHA256,
            "valid": True,
            "ready_for_analysis": True,
            "planned_scientific_jobs": 600,
            "completed_scientific_jobs": 600,
            "scientific_failures": 0,
            "skipped_scientific_jobs": 0,
            "checkpoint_count": 120,
            "run_bundle_count": 600,
            "failure_record_count": 0,
            "findings": [],
        }
    ):
        raise RuntimeError(
            "fresh final-evidence validation did not pass the exact contract"
        )

    artifacts = store.artifacts()
    role_counts = dict(sorted(Counter(item.role.value for item in artifacts).items()))
    evidence_class_counts = dict(
        sorted(Counter(item.evidence_class.value for item in artifacts).items())
    )
    if (
        role_counts != EXPECTED_ROLE_COUNTS
        or evidence_class_counts != EXPECTED_EVIDENCE_CLASS_COUNTS
    ):
        raise RuntimeError(
            "accepted Study artifact inventory differs from the frozen contract"
        )
    for artifact in artifacts:
        scientific_job = any(
            store.plan.by_id()[job_id].payload.get("job_type")
            in {"phase-a-training", "phase-a-reference", "phase-b-matched-set"}
            for job_id in artifact.source_job_ids
        )
        if scientific_job and artifact.evidence_class is not EvidenceClass.CONFIRMATORY:
            raise RuntimeError(
                "scientific artifact has a non-confirmatory evidence class"
            )

    registered_report = _validate_registered_report(store, report.to_dict())
    handoff_package = _validate_handoff_package(store)
    inventory_bytes, inventory_sha256 = _run_inventory(store)

    manifest = {
        "schema_version": FREEZE_PACKAGE_SCHEMA_VERSION,
        "status": "frozen",
        "freeze_time_utc": freeze_time,
        "scientific_recipe_id": FINAL_STUDY_ID,
        "accepted_execution_instance_id": ACCEPTED_EXECUTION_ID,
        "execution_source_git_commit": EXPECTED_EXECUTION_SOURCE_COMMIT,
        "recipe_sha256": EXPECTED_RECIPE_SHA256,
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "study_manifest_sha256": sha256_file(store.study_dir / "manifest.json"),
        "study_finalization_marker_sha256": sha256_file(store.study_dir / "FINALIZED"),
        "study_file_integrity": store.manifest["files"],
        "progress": EXPECTED_PROGRESS,
        "artifact_count": len(artifacts),
        "artifact_role_counts": role_counts,
        "artifact_evidence_class_counts": evidence_class_counts,
        "run_bundle_count": 600,
        "run_manifest_inventory": {
            "relative_path": (
                FREEZE_RELATIVE_DIR / "run-manifest-inventory.jsonl"
            ).as_posix(),
            "record_count": 600,
            "sha256": inventory_sha256,
        },
        "validation_report": registered_report,
        "evidence_handoff_package": handoff_package,
        "validator": {
            "git_commit": validator_git_commit,
            "source_files": [
                {"relative_path": name, "sha256": sha256_file(repo_root / name)}
                for name in VALIDATOR_SOURCE_FILES
            ],
        },
        "excluded_execution": {
            **completion["failed_attempt"],
            "exclusion_reason": (
                "DEC-062 immutable failed/incomplete predecessor; permanently "
                "ineligible for T-611 and downstream evidence"
            ),
        },
        "scientific_outcomes_interpreted": False,
    }
    manifest_bytes = _canonical_json_bytes(manifest)
    output_dir = repo_root / FREEZE_RELATIVE_DIR
    manifest_sha256 = _write_package_atomic(
        output_dir,
        manifest_bytes=manifest_bytes,
        inventory_bytes=inventory_bytes,
    )
    return {
        "freeze_directory": FREEZE_RELATIVE_DIR.as_posix(),
        "freeze_manifest_sha256": manifest_sha256,
        "run_manifest_inventory_sha256": inventory_sha256,
        "artifact_count": len(artifacts),
        "run_bundle_count": 600,
        "valid": True,
    }
