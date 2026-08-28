"""Filesystem study bundle above individual scientific run bundles."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from ..run_bundle import sha256_file, source_provenance
from .lifecycle import StudyLifecycle
from .model import (
    ArtifactRole,
    EvidenceClass,
    StudyArtifact,
    StudyJobSpec,
    StudyPlan,
    StudyStage,
)
from .recipe import StudyRecipe

STUDY_BUNDLE_SCHEMA_VERSION = 1
STUDY_FINALIZATION_MARKER = "FINALIZED"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _canonical_json(payload: Any) -> str:
    return json.dumps(
        payload,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _sha256_json(payload: Any) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"study JSON is unreadable: {path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"study JSON must be an object: {path}")
    return payload


def _plan_to_dict(plan: StudyPlan) -> dict[str, Any]:
    return {
        "study_id": plan.study_id,
        "jobs": [
            {
                "job_id": job.job_id,
                "stage": job.stage.value,
                "evidence_class": job.evidence_class.value,
                "dependencies": list(job.dependencies),
                "payload": dict(job.payload),
            }
            for job in plan.jobs
        ],
    }


def _plan_from_dict(payload: Mapping[str, Any]) -> StudyPlan:
    if set(payload) != {"study_id", "jobs"}:
        raise ValueError("persisted study plan keys mismatch")
    jobs_payload = payload["jobs"]
    if not isinstance(jobs_payload, list):
        raise ValueError("persisted study plan jobs must be a list")
    jobs: list[StudyJobSpec] = []
    for item in jobs_payload:
        if not isinstance(item, Mapping) or set(item) != {
            "job_id",
            "stage",
            "evidence_class",
            "dependencies",
            "payload",
        }:
            raise ValueError("persisted study job keys mismatch")
        dependencies = item["dependencies"]
        if not isinstance(dependencies, list) or not all(
            isinstance(value, str) for value in dependencies
        ):
            raise ValueError("persisted study job dependencies must be strings")
        try:
            stage = StudyStage(str(item["stage"]))
            evidence_class = EvidenceClass(str(item["evidence_class"]))
        except ValueError as exc:
            raise ValueError("persisted study job enum value is unsupported") from exc
        jobs.append(
            StudyJobSpec(
                job_id=item["job_id"],
                stage=stage,
                evidence_class=evidence_class,
                dependencies=tuple(dependencies),
                payload=item["payload"],
            )
        )
    return StudyPlan(study_id=payload["study_id"], jobs=tuple(jobs))


def _artifact_to_dict(artifact: StudyArtifact) -> dict[str, Any]:
    return {
        "artifact_id": artifact.artifact_id,
        "role": artifact.role.value,
        "evidence_class": artifact.evidence_class.value,
        "relative_path": artifact.relative_path,
        "sha256": artifact.sha256,
        "source_job_ids": list(artifact.source_job_ids),
        "source_artifact_ids": list(artifact.source_artifact_ids),
        "metadata": dict(artifact.metadata),
    }


def _artifact_from_dict(payload: Mapping[str, Any]) -> StudyArtifact:
    expected = {
        "artifact_id",
        "role",
        "evidence_class",
        "relative_path",
        "sha256",
        "source_job_ids",
        "source_artifact_ids",
        "metadata",
    }
    if set(payload) != expected:
        raise ValueError("persisted artifact keys mismatch")
    try:
        role = ArtifactRole(str(payload["role"]))
        evidence_class = EvidenceClass(str(payload["evidence_class"]))
    except ValueError as exc:
        raise ValueError("persisted artifact enum value is unsupported") from exc
    source_job_ids = payload["source_job_ids"]
    source_artifact_ids = payload["source_artifact_ids"]
    if not isinstance(source_job_ids, list) or not all(
        isinstance(value, str) for value in source_job_ids
    ):
        raise ValueError("persisted source_job_ids must be a list of strings")
    if not isinstance(source_artifact_ids, list) or not all(
        isinstance(value, str) for value in source_artifact_ids
    ):
        raise ValueError("persisted source_artifact_ids must be a list of strings")
    return StudyArtifact(
        artifact_id=payload["artifact_id"],
        role=role,
        evidence_class=evidence_class,
        relative_path=payload["relative_path"],
        sha256=payload["sha256"],
        source_job_ids=tuple(source_job_ids),
        source_artifact_ids=tuple(source_artifact_ids),
        metadata=payload["metadata"],
    )


class StudyStore:
    """Durable parent bundle for one materialized study.

    Individual scientific execution continues to use validated run bundles. This
    parent bundle records the immutable recipe/plan, job lifecycle and explicit
    lineage from run/checkpoint artifacts through validation, analysis and
    thesis/presentation exports.
    """

    def __init__(
        self,
        *,
        repo_root: Path,
        writable_root: Path,
        study_dir: Path,
        recipe: StudyRecipe,
        plan: StudyPlan,
        lifecycle: StudyLifecycle,
        manifest: dict[str, Any],
    ) -> None:
        self.repo_root = repo_root
        self.writable_root = writable_root
        self.study_dir = study_dir
        self.recipe = recipe
        self.plan = plan
        self.lifecycle = lifecycle
        self.manifest = manifest

    @classmethod
    def create(
        cls,
        *,
        repo_root: Path,
        recipe: StudyRecipe,
        plan: StudyPlan,
        writable_root: Path | None = None,
    ) -> "StudyStore":
        repo_root = Path(repo_root).resolve()
        writable_root = Path(writable_root).resolve() if writable_root else repo_root
        if plan.study_id != recipe.recipe_id:
            raise ValueError("study plan study_id must equal recipe_id")
        study_dir = writable_root / "results" / "studies" / plan.study_id
        if study_dir.exists():
            raise FileExistsError(f"study bundle already exists: {study_dir}")
        study_dir.mkdir(parents=True)
        lifecycle = StudyLifecycle(plan)
        now = _utc_now()
        plan_payload = _plan_to_dict(plan)
        recipe_payload = recipe.to_dict()
        manifest = {
            "schema_version": STUDY_BUNDLE_SCHEMA_VERSION,
            "study_id": plan.study_id,
            "status": "active",
            "created_at_utc": now,
            "updated_at_utc": now,
            "protocol_version": recipe.protocol_version,
            "evidence_class": recipe.evidence_class.value,
            "recipe_id": recipe.recipe_id,
            "recipe_sha256": recipe.sha256(),
            "plan_sha256": _sha256_json(plan_payload),
            "source": source_provenance(repo_root),
            "current_stage": lifecycle.current_stage.value
            if lifecycle.current_stage is not None
            else None,
            "progress": lifecycle.progress(),
            "finalized_at_utc": None,
        }
        _write_json_atomic(study_dir / "recipe.json", recipe_payload)
        _write_json_atomic(study_dir / "plan.json", plan_payload)
        _write_json_atomic(study_dir / "lifecycle.json", lifecycle.snapshot())
        _write_json_atomic(study_dir / "manifest.json", manifest)
        store = cls(
            repo_root=repo_root,
            writable_root=writable_root,
            study_dir=study_dir,
            recipe=recipe,
            plan=plan,
            lifecycle=lifecycle,
            manifest=manifest,
        )
        store._append_event("study-created", {"recipe_sha256": recipe.sha256()})
        return store

    @classmethod
    def load(
        cls,
        *,
        repo_root: Path,
        study_id: str,
        writable_root: Path | None = None,
    ) -> "StudyStore":
        repo_root = Path(repo_root).resolve()
        writable_root = Path(writable_root).resolve() if writable_root else repo_root
        study_dir = writable_root / "results" / "studies" / study_id
        if not study_dir.is_dir():
            raise FileNotFoundError(f"study bundle not found: {study_dir}")
        manifest = _read_json_object(study_dir / "manifest.json")
        if manifest.get("schema_version") != STUDY_BUNDLE_SCHEMA_VERSION:
            raise RuntimeError("unsupported study bundle schema")
        if manifest.get("study_id") != study_id:
            raise RuntimeError("study manifest identity mismatch")
        recipe = StudyRecipe.from_dict(_read_json_object(study_dir / "recipe.json"))
        if recipe.recipe_id != study_id or recipe.sha256() != manifest.get("recipe_sha256"):
            raise RuntimeError("study recipe identity/hash mismatch")
        plan_payload = _read_json_object(study_dir / "plan.json")
        plan = _plan_from_dict(plan_payload)
        if plan.study_id != study_id or _sha256_json(plan_payload) != manifest.get(
            "plan_sha256"
        ):
            raise RuntimeError("study plan identity/hash mismatch")
        lifecycle_payload = _read_json_object(study_dir / "lifecycle.json")
        if set(lifecycle_payload) != {"states", "attempts"}:
            raise RuntimeError("study lifecycle keys mismatch")
        states = lifecycle_payload["states"]
        attempts = lifecycle_payload["attempts"]
        if not isinstance(states, Mapping) or not isinstance(attempts, Mapping):
            raise RuntimeError("study lifecycle states/attempts must be objects")
        lifecycle = StudyLifecycle.restore(plan, states=states, attempts=attempts)
        store = cls(
            repo_root=repo_root,
            writable_root=writable_root,
            study_dir=study_dir,
            recipe=recipe,
            plan=plan,
            lifecycle=lifecycle,
            manifest=manifest,
        )
        store._validate_manifest_against_lifecycle()
        store._validate_artifacts()
        return store

    def _require_mutable(self) -> None:
        if (self.study_dir / STUDY_FINALIZATION_MARKER).exists():
            raise RuntimeError("finalized study bundles are immutable")
        if self.manifest.get("status") != "active":
            raise RuntimeError("study bundle is not active")

    def _append_event(self, event_type: str, payload: Mapping[str, Any]) -> None:
        record = {
            "at_utc": _utc_now(),
            "event": event_type,
            "payload": dict(payload),
        }
        with (self.study_dir / "events.jsonl").open(
            "a", encoding="utf-8", newline="\n"
        ) as handle:
            handle.write(_canonical_json(record) + "\n")

    def _persist_lifecycle(self) -> None:
        self._require_mutable()
        self.manifest["updated_at_utc"] = _utc_now()
        self.manifest["current_stage"] = (
            self.lifecycle.current_stage.value
            if self.lifecycle.current_stage is not None
            else None
        )
        self.manifest["progress"] = self.lifecycle.progress()
        _write_json_atomic(self.study_dir / "lifecycle.json", self.lifecycle.snapshot())
        _write_json_atomic(self.study_dir / "manifest.json", self.manifest)

    def start_job(self, job_id: str) -> None:
        self._require_mutable()
        self.lifecycle.start(job_id)
        self._persist_lifecycle()
        self._append_event(
            "job-started",
            {"job_id": job_id, "attempt": self.lifecycle.attempts_for(job_id)},
        )

    def complete_job(self, job_id: str) -> None:
        self._require_mutable()
        self.lifecycle.complete_job(job_id)
        self._persist_lifecycle()
        self._append_event("job-completed", {"job_id": job_id})

    def fail_job_scientifically(self, job_id: str, *, reason: str) -> None:
        self._require_mutable()
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("scientific failure reason must be non-empty")
        self.lifecycle.fail_scientifically(job_id)
        self._persist_lifecycle()
        self._append_event(
            "job-scientific-failure", {"job_id": job_id, "reason": reason}
        )

    def fail_job_infrastructure(self, job_id: str, *, reason: str) -> None:
        self._require_mutable()
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("infrastructure failure reason must be non-empty")
        self.lifecycle.fail_infrastructure(job_id)
        self._persist_lifecycle()
        self._append_event(
            "job-infrastructure-failure", {"job_id": job_id, "reason": reason}
        )

    def retry_job(self, job_id: str) -> None:
        self._require_mutable()
        self.lifecycle.retry_infrastructure_failure(job_id)
        self._persist_lifecycle()
        self._append_event("job-retry-authorized", {"job_id": job_id})

    def artifacts(self) -> tuple[StudyArtifact, ...]:
        path = self.study_dir / "artifacts.jsonl"
        if not path.is_file():
            return ()
        artifacts: list[StudyArtifact] = []
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"invalid artifact JSON at line {number}") from exc
            if not isinstance(payload, Mapping):
                raise RuntimeError(f"artifact line {number} must be an object")
            artifacts.append(_artifact_from_dict(payload))
        return tuple(artifacts)

    def record_artifact(self, artifact: StudyArtifact) -> None:
        self._require_mutable()
        if not isinstance(artifact, StudyArtifact):
            raise ValueError("artifact must be StudyArtifact")
        existing = {item.artifact_id: item for item in self.artifacts()}
        if artifact.artifact_id in existing:
            raise ValueError(f"duplicate study artifact_id: {artifact.artifact_id}")
        known_jobs = set(self.plan.by_id())
        if any(job_id not in known_jobs for job_id in artifact.source_job_ids):
            raise ValueError("artifact references unknown source job")
        if any(
            artifact_id not in existing for artifact_id in artifact.source_artifact_ids
        ):
            raise ValueError("artifact references unknown source artifact")
        path = (self.writable_root / artifact.relative_path).resolve()
        try:
            path.relative_to(self.writable_root)
        except ValueError as exc:
            raise ValueError("artifact path escapes writable evidence root") from exc
        if not path.is_file():
            raise FileNotFoundError(path)
        if sha256_file(path) != artifact.sha256:
            raise ValueError("artifact SHA-256 does not match file contents")
        with (self.study_dir / "artifacts.jsonl").open(
            "a", encoding="utf-8", newline="\n"
        ) as handle:
            handle.write(_canonical_json(_artifact_to_dict(artifact)) + "\n")
        self._append_event(
            "artifact-recorded",
            {"artifact_id": artifact.artifact_id, "role": artifact.role.value},
        )

    def finalize(self) -> None:
        self._require_mutable()
        if not self.lifecycle.complete:
            raise RuntimeError("study cannot finalize while lifecycle is unresolved")
        progress = self.lifecycle.progress()
        status = (
            "completed-with-scientific-failures"
            if progress["scientific_failed"] or progress["skipped"]
            else "completed"
        )
        self.manifest["status"] = status
        self.manifest["updated_at_utc"] = _utc_now()
        self.manifest["finalized_at_utc"] = self.manifest["updated_at_utc"]
        self.manifest["current_stage"] = None
        self.manifest["progress"] = progress
        tracked_files = [
            "recipe.json",
            "plan.json",
            "lifecycle.json",
            "events.jsonl",
        ]
        if (self.study_dir / "artifacts.jsonl").is_file():
            tracked_files.append("artifacts.jsonl")
        self.manifest["files"] = {
            name: {
                "sha256": sha256_file(self.study_dir / name),
                "size_bytes": (self.study_dir / name).stat().st_size,
            }
            for name in tracked_files
        }
        _write_json_atomic(self.study_dir / "manifest.json", self.manifest)
        marker = (
            f"schema_version={STUDY_BUNDLE_SCHEMA_VERSION}\n"
            f"status={status}\n"
            f"recipe_sha256={self.recipe.sha256()}\n"
        )
        temporary = self.study_dir / (STUDY_FINALIZATION_MARKER + ".tmp")
        temporary.write_text(marker, encoding="utf-8", newline="\n")
        temporary.replace(self.study_dir / STUDY_FINALIZATION_MARKER)

    def _validate_manifest_against_lifecycle(self) -> None:
        if self.manifest.get("progress") != self.lifecycle.progress():
            raise RuntimeError("study manifest progress does not match lifecycle")
        expected_stage = (
            self.lifecycle.current_stage.value
            if self.lifecycle.current_stage is not None
            else None
        )
        if self.manifest.get("current_stage") != expected_stage:
            raise RuntimeError("study manifest current_stage does not match lifecycle")
        marker_exists = (self.study_dir / STUDY_FINALIZATION_MARKER).is_file()
        if marker_exists and self.manifest.get("status") not in {
            "completed",
            "completed-with-scientific-failures",
        }:
            raise RuntimeError("study finalization marker/status mismatch")
        if not marker_exists and self.manifest.get("status") != "active":
            raise RuntimeError("unfinalized study must remain active")

    def _validate_artifacts(self) -> None:
        known_jobs = set(self.plan.by_id())
        known_artifacts: set[str] = set()
        for artifact in self.artifacts():
            if artifact.artifact_id in known_artifacts:
                raise RuntimeError("duplicate persisted artifact_id")
            if any(job_id not in known_jobs for job_id in artifact.source_job_ids):
                raise RuntimeError("persisted artifact references unknown job")
            if any(
                artifact_id not in known_artifacts
                for artifact_id in artifact.source_artifact_ids
            ):
                raise RuntimeError("persisted artifact lineage points forward/unknown")
            path = (self.writable_root / artifact.relative_path).resolve()
            try:
                path.relative_to(self.writable_root)
            except ValueError as exc:
                raise RuntimeError("persisted artifact path escapes evidence root") from exc
            if not path.is_file() or sha256_file(path) != artifact.sha256:
                raise RuntimeError("persisted artifact file/hash is invalid")
            known_artifacts.add(artifact.artifact_id)
