"""UI-independent runtime registry/service for truthful live experiments.

The service owns operational process state and read-only live telemetry only.
Scientific execution remains in validated runners/run bundles. Runtime metadata
is separate under ``results/runtime`` so application interruptions never
masquerade as finalized scientific evidence.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence

from .experiment_manager import get_resource_snapshot
from .run_bundle import FINALIZATION_MARKER
from .runtime_observer import RUNTIME_TELEMETRY_SCHEMA_VERSION
from .v11_candidate_runner import (
    V11CandidateExperimentRequest,
    V11CandidateExperimentRunner,
)
from .v11_protocol import load_v11_candidate_protocol

RUNTIME_SERVICE_SCHEMA_VERSION = 1
_RUNTIME_METADATA = "runtime.json"
_RUNTIME_REQUEST = "request.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write_json_atomic(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"runtime JSON is unreadable: {path}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"runtime JSON must be an object: {path}")
    return value


def _safe_run_id(value: Any) -> str:
    if not isinstance(value, str) or not value.strip() or Path(value).name != value:
        raise ValueError("run_id must be a non-empty path-safe string")
    return value


def _telemetry_rows(path: Path) -> tuple[dict[str, Any], ...]:
    """Read only complete NDJSON rows; tolerate one concurrently-written tail."""
    if not path.is_file():
        return ()
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise RuntimeError("runtime telemetry is unreadable") from exc
    if not content:
        return ()
    lines = content.splitlines(keepends=True)
    if lines and not lines[-1].endswith(("\n", "\r")):
        lines = lines[:-1]
    rows: list[dict[str, Any]] = []
    previous = -1
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError("runtime telemetry contains invalid JSON") from exc
        if not isinstance(row, dict):
            raise RuntimeError("runtime telemetry row must be an object")
        if row.get("runtime_telemetry_schema_version") != RUNTIME_TELEMETRY_SCHEMA_VERSION:
            raise RuntimeError("runtime telemetry schema mismatch")
        sequence = row.get("sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence <= previous:
            raise RuntimeError("runtime telemetry sequence must be strictly increasing")
        previous = sequence
        rows.append(row)
    return tuple(rows)


class RuntimeStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INTERRUPTED = "interrupted"


@dataclass(frozen=True)
class RuntimeCapabilities:
    can_cancel: bool
    can_restart: bool
    can_pause: bool = False
    can_resume: bool = False


@dataclass(frozen=True)
class RuntimeProgress:
    completed_roots: int
    total_roots: int
    fraction_complete: float
    latest_phase: str | None = None
    latest_episode_index: int | None = None
    latest_step: int | None = None

    def __post_init__(self) -> None:
        if self.completed_roots < 0 or self.total_roots < 0:
            raise ValueError("root progress counts must be non-negative")
        if self.completed_roots > self.total_roots:
            raise ValueError("completed_roots cannot exceed total_roots")
        if not math.isfinite(self.fraction_complete) or not 0.0 <= self.fraction_complete <= 1.0:
            raise ValueError("fraction_complete must be finite and in [0, 1]")


@dataclass(frozen=True)
class RuntimeRunSnapshot:
    schema_version: int
    run_id: str
    status: RuntimeStatus
    created_at_utc: str
    updated_at_utc: str
    heartbeat_at_utc: str | None
    protocol_path: str | None
    attempt: int
    process_id: int | None
    return_code: int | None
    progress: RuntimeProgress
    capabilities: RuntimeCapabilities
    latest_telemetry_sequence: int | None
    telemetry_path: str | None
    run_dir: str | None
    message: str | None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


@dataclass
class _ManagedProcess:
    process: subprocess.Popen[Any]
    run_id: str


class RuntimeService:
    """Single-application runtime registry over scientific child processes.

    Arbitrary commands are intentionally unsupported. The current launcher is
    only the repository-owned protocol-v1.1 candidate entrypoint. A frozen-v1.1
    entrypoint is added explicitly only after T-522 freezes one.
    """

    def __init__(self, repo_root: Path, *, python_executable: str | None = None) -> None:
        if not isinstance(repo_root, Path):
            repo_root = Path(repo_root)
        self.repo_root = repo_root.resolve()
        self.runtime_root = self.repo_root / "results" / "runtime"
        self.runs_root = self.repo_root / "results" / "runs"
        self.python_executable = python_executable or sys.executable
        self.runner_script = self.repo_root / "scripts" / "run_v11_candidate_runtime.py"
        self._managed: dict[str, _ManagedProcess] = {}
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        self._reconcile_orphaned_records()

    def _runtime_dir(self, run_id: str) -> Path:
        return self.runtime_root / _safe_run_id(run_id)

    def _metadata_path(self, run_id: str) -> Path:
        return self._runtime_dir(run_id) / _RUNTIME_METADATA

    def _request_path(self, run_id: str) -> Path:
        return self._runtime_dir(run_id) / _RUNTIME_REQUEST

    def _load_metadata(self, run_id: str) -> dict[str, Any]:
        path = self._metadata_path(run_id)
        if not path.is_file():
            raise KeyError(run_id)
        payload = _read_json_object(path)
        if payload.get("schema_version") != RUNTIME_SERVICE_SCHEMA_VERSION:
            raise RuntimeError("unsupported runtime metadata schema")
        if payload.get("run_id") != run_id:
            raise RuntimeError("runtime metadata run_id mismatch")
        return payload

    def _save_metadata(self, payload: Mapping[str, Any]) -> None:
        run_id = _safe_run_id(payload.get("run_id"))
        _write_json_atomic(self._metadata_path(run_id), dict(payload))

    def _final_bundle_status(self, run_id: str) -> tuple[RuntimeStatus, str | None] | None:
        run_dir = self.runs_root / run_id
        if not (run_dir / FINALIZATION_MARKER).is_file():
            return None
        manifest = _read_json_object(run_dir / "manifest.json")
        status = str(manifest.get("status", ""))
        if status == "completed":
            return RuntimeStatus.COMPLETED, None
        if status == "cancelled":
            return RuntimeStatus.CANCELLED, None
        if status in {"failed", "invalid"}:
            return RuntimeStatus.FAILED, f"Scientific bundle finalized with status {status}."
        raise RuntimeError(f"unknown finalized scientific status: {status}")

    def _reconcile_orphaned_records(self) -> None:
        """Reconcile persisted active records when a new app session starts."""
        for directory in self.runtime_root.iterdir():
            if not directory.is_dir():
                continue
            path = directory / _RUNTIME_METADATA
            if not path.is_file():
                continue
            payload = _read_json_object(path)
            if payload.get("status") not in {
                RuntimeStatus.RUNNING.value,
                RuntimeStatus.QUEUED.value,
            }:
                continue
            finalized = self._final_bundle_status(directory.name)
            if finalized is not None:
                payload["status"] = finalized[0].value
                payload["message"] = finalized[1]
            else:
                payload["status"] = RuntimeStatus.INTERRUPTED.value
                payload["message"] = (
                    "Application/runtime session ended before this run finalized."
                )
            payload["updated_at_utc"] = _utc_now()
            payload["process_id"] = None
            self._save_metadata(payload)

    def enqueue_v11_candidate(
        self,
        *,
        protocol_path: Path,
        request: Mapping[str, Any],
    ) -> RuntimeRunSnapshot:
        """Validate and queue one approved non-final candidate request."""
        if not isinstance(request, Mapping):
            raise ValueError("request must be an object")
        protocol_path = Path(protocol_path).resolve()
        if not protocol_path.is_file():
            raise FileNotFoundError(protocol_path)
        protocol = load_v11_candidate_protocol(protocol_path)
        validated = V11CandidateExperimentRequest.from_dict(request)
        # Constructor validation is side-effect free and catches protocol/config
        # mismatches before the application creates a queued runtime record.
        V11CandidateExperimentRunner(
            repo_root=self.repo_root,
            protocol=protocol,
            request=validated,
        )
        run_id = _safe_run_id(validated.run_id)
        directory = self._runtime_dir(run_id)
        if directory.exists():
            raise FileExistsError(f"runtime record already exists: {run_id}")
        if (self.runs_root / run_id / FINALIZATION_MARKER).is_file():
            raise FileExistsError(f"scientific run is already finalized: {run_id}")

        directory.mkdir(parents=True)
        _write_json_atomic(self._request_path(run_id), validated.to_dict())
        now = _utc_now()
        metadata = {
            "schema_version": RUNTIME_SERVICE_SCHEMA_VERSION,
            "run_id": run_id,
            "status": RuntimeStatus.QUEUED.value,
            "created_at_utc": now,
            "updated_at_utc": now,
            "heartbeat_at_utc": None,
            "protocol_path": str(protocol_path),
            "attempt": 1,
            "process_id": None,
            "return_code": None,
            "latest_telemetry_sequence": None,
            "telemetry_path": str(directory / "telemetry-attempt-1.ndjson"),
            "message": None,
        }
        self._save_metadata(metadata)
        return self.get_run(run_id)

    def _queued_ids(self) -> list[str]:
        queued: list[tuple[str, str]] = []
        for directory in self.runtime_root.iterdir():
            path = directory / _RUNTIME_METADATA
            if not directory.is_dir() or not path.is_file():
                continue
            payload = _read_json_object(path)
            if payload.get("status") == RuntimeStatus.QUEUED.value:
                queued.append((str(payload.get("created_at_utc", "")), directory.name))
        return [run_id for _, run_id in sorted(queued)]

    def _active_managed(self) -> _ManagedProcess | None:
        for item in self._managed.values():
            if item.process.poll() is None:
                return item
        return None

    def start_next(self) -> RuntimeRunSnapshot | None:
        """Launch at most one queued run; runtime execution is single-process."""
        self.refresh()
        if self._active_managed() is not None:
            return None
        queued = self._queued_ids()
        if not queued:
            return None
        run_id = queued[0]
        metadata = self._load_metadata(run_id)
        if not self.runner_script.is_file():
            raise RuntimeError(f"runtime runner script is missing: {self.runner_script}")
        cmd = [
            self.python_executable,
            str(self.runner_script),
            "--repo-root",
            str(self.repo_root),
            "--protocol",
            str(metadata["protocol_path"]),
            "--request",
            str(self._request_path(run_id)),
            "--telemetry",
            str(metadata["telemetry_path"]),
        ]
        process = subprocess.Popen(
            cmd,
            cwd=self.repo_root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
        now = _utc_now()
        metadata.update(
            {
                "status": RuntimeStatus.RUNNING.value,
                "updated_at_utc": now,
                "heartbeat_at_utc": now,
                "process_id": process.pid,
                "return_code": None,
                "message": None,
            }
        )
        self._save_metadata(metadata)
        self._managed[run_id] = _ManagedProcess(process=process, run_id=run_id)
        return self.get_run(run_id)

    def refresh(self) -> None:
        """Refresh child state and activity-derived heartbeat metadata."""
        for run_id, managed in list(self._managed.items()):
            metadata = self._load_metadata(run_id)
            previous_sequence = metadata.get("latest_telemetry_sequence")
            latest = self._latest_telemetry(run_id, metadata)
            if latest is not None:
                sequence = int(latest["sequence"])
                metadata["latest_telemetry_sequence"] = sequence
                if sequence != previous_sequence:
                    metadata["heartbeat_at_utc"] = _utc_now()
            return_code = managed.process.poll()
            if return_code is None:
                metadata["updated_at_utc"] = _utc_now()
                self._save_metadata(metadata)
                continue

            metadata["return_code"] = int(return_code)
            metadata["process_id"] = None
            finalized = self._final_bundle_status(run_id)
            if metadata.get("status") == RuntimeStatus.CANCELLED.value:
                pass
            elif finalized is not None:
                metadata["status"] = finalized[0].value
                metadata["message"] = finalized[1]
            else:
                metadata["status"] = RuntimeStatus.INTERRUPTED.value
                metadata["message"] = (
                    "Child process ended without a finalized scientific bundle."
                )
            metadata["updated_at_utc"] = _utc_now()
            self._save_metadata(metadata)
            del self._managed[run_id]

    def _latest_telemetry(
        self, run_id: str, metadata: Mapping[str, Any] | None = None
    ) -> dict[str, Any] | None:
        if metadata is None:
            metadata = self._load_metadata(run_id)
        value = metadata.get("telemetry_path")
        if not isinstance(value, str):
            return None
        rows = _telemetry_rows(Path(value))
        return None if not rows else rows[-1]

    def tail_telemetry(
        self, run_id: str, *, after_sequence: int = -1, limit: int = 500
    ) -> tuple[dict[str, Any], ...]:
        if not isinstance(after_sequence, int) or isinstance(after_sequence, bool):
            raise ValueError("after_sequence must be an integer")
        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            raise ValueError("limit must be a positive integer")
        metadata = self._load_metadata(run_id)
        value = metadata.get("telemetry_path")
        if not isinstance(value, str):
            return ()
        selected = [
            row
            for row in _telemetry_rows(Path(value))
            if int(row["sequence"]) > after_sequence
        ]
        return tuple(selected[:limit])

    def _progress(
        self,
        run_id: str,
        request: Mapping[str, Any],
        latest: Mapping[str, Any] | None,
    ) -> RuntimeProgress:
        roots = request.get("root_seeds")
        total = (
            len(roots)
            if isinstance(roots, Sequence) and not isinstance(roots, (str, bytes))
            else 0
        )
        completed = 0
        state_path = self.runs_root / run_id / "runner-state.json"
        if state_path.is_file():
            state = _read_json_object(state_path)
            values = state.get("completed_root_seeds")
            if isinstance(values, list):
                completed = len(values)
        completed = min(completed, total)
        fraction = 0.0 if total == 0 else completed / total
        phase = (
            latest.get("phase")
            if latest is not None and isinstance(latest.get("phase"), str)
            else None
        )
        episode = (
            latest.get("episode_index")
            if latest is not None and isinstance(latest.get("episode_index"), int)
            else None
        )
        step = (
            latest.get("step")
            if latest is not None and isinstance(latest.get("step"), int)
            else None
        )
        return RuntimeProgress(
            completed_roots=completed,
            total_roots=total,
            fraction_complete=fraction,
            latest_phase=phase,
            latest_episode_index=episode,
            latest_step=step,
        )

    @staticmethod
    def _capabilities(status: RuntimeStatus, *, managed: bool) -> RuntimeCapabilities:
        return RuntimeCapabilities(
            can_cancel=(
                status is RuntimeStatus.QUEUED
                or (status is RuntimeStatus.RUNNING and managed)
            ),
            can_restart=status in {RuntimeStatus.CANCELLED, RuntimeStatus.INTERRUPTED},
            can_pause=False,
            can_resume=False,
        )

    def get_run(self, run_id: str) -> RuntimeRunSnapshot:
        self.refresh()
        metadata = self._load_metadata(run_id)
        status = RuntimeStatus(str(metadata["status"]))
        latest = self._latest_telemetry(run_id, metadata)
        request = _read_json_object(self._request_path(run_id))
        managed = run_id in self._managed and self._managed[run_id].process.poll() is None
        run_dir = self.runs_root / run_id
        return RuntimeRunSnapshot(
            schema_version=RUNTIME_SERVICE_SCHEMA_VERSION,
            run_id=run_id,
            status=status,
            created_at_utc=str(metadata["created_at_utc"]),
            updated_at_utc=str(metadata["updated_at_utc"]),
            heartbeat_at_utc=metadata.get("heartbeat_at_utc"),
            protocol_path=metadata.get("protocol_path"),
            attempt=int(metadata.get("attempt", 1)),
            process_id=metadata.get("process_id"),
            return_code=metadata.get("return_code"),
            progress=self._progress(run_id, request, latest),
            capabilities=self._capabilities(status, managed=managed),
            latest_telemetry_sequence=(
                None if latest is None else int(latest["sequence"])
            ),
            telemetry_path=metadata.get("telemetry_path"),
            run_dir=str(run_dir) if run_dir.is_dir() else None,
            message=metadata.get("message"),
        )

    def cancel(self, run_id: str) -> RuntimeRunSnapshot:
        metadata = self._load_metadata(run_id)
        status = RuntimeStatus(str(metadata["status"]))
        if status is RuntimeStatus.QUEUED:
            metadata["status"] = RuntimeStatus.CANCELLED.value
            metadata["updated_at_utc"] = _utc_now()
            metadata["message"] = "Queued run cancelled before scientific execution started."
            self._save_metadata(metadata)
            return self.get_run(run_id)
        managed = self._managed.get(run_id)
        if (
            status is not RuntimeStatus.RUNNING
            or managed is None
            or managed.process.poll() is not None
        ):
            raise RuntimeError("run cannot be cancelled by this runtime session")
        managed.process.terminate()
        try:
            managed.process.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            managed.process.kill()
            managed.process.wait(timeout=5.0)
        metadata["status"] = RuntimeStatus.CANCELLED.value
        metadata["updated_at_utc"] = _utc_now()
        metadata["process_id"] = None
        metadata["return_code"] = managed.process.returncode
        metadata["message"] = (
            "Runtime process cancelled; unfinished scientific bundle is retained "
            "for audit/restart."
        )
        self._save_metadata(metadata)
        del self._managed[run_id]
        return self.get_run(run_id)

    def restart(self, run_id: str) -> RuntimeRunSnapshot:
        metadata = self._load_metadata(run_id)
        status = RuntimeStatus(str(metadata["status"]))
        if status not in {RuntimeStatus.CANCELLED, RuntimeStatus.INTERRUPTED}:
            raise RuntimeError("only cancelled/interrupted unfinished runs can be restarted")
        if (self.runs_root / run_id / FINALIZATION_MARKER).is_file():
            raise RuntimeError("finalized scientific bundles cannot be restarted in place")
        attempt = int(metadata.get("attempt", 1)) + 1
        metadata.update(
            {
                "status": RuntimeStatus.QUEUED.value,
                "updated_at_utc": _utc_now(),
                "heartbeat_at_utc": None,
                "attempt": attempt,
                "process_id": None,
                "return_code": None,
                "latest_telemetry_sequence": None,
                "telemetry_path": str(
                    self._runtime_dir(run_id) / f"telemetry-attempt-{attempt}.ndjson"
                ),
                "message": None,
            }
        )
        self._save_metadata(metadata)
        return self.get_run(run_id)

    def pause(self, run_id: str) -> None:
        _safe_run_id(run_id)
        raise NotImplementedError(
            "pause is intentionally unsupported by the scientific runtime"
        )

    def resume(self, run_id: str) -> None:
        _safe_run_id(run_id)
        raise NotImplementedError(
            "resume is intentionally unsupported; use restart for unfinished runs"
        )

    def resource_snapshot(self) -> dict[str, Any]:
        """Return the existing canonical system inventory snapshot for the UI."""
        return get_resource_snapshot(self.repo_root)

    def list_runs(self) -> tuple[RuntimeRunSnapshot, ...]:
        self.refresh()
        snapshots: list[RuntimeRunSnapshot] = []
        known: set[str] = set()
        for directory in sorted(self.runtime_root.iterdir()):
            if directory.is_dir() and (directory / _RUNTIME_METADATA).is_file():
                snapshots.append(self.get_run(directory.name))
                known.add(directory.name)

        # Preserve scientific bundles that predate runtime metadata. Finalized
        # status stays authoritative; an unfinished running manifest is visible
        # as interrupted, but no restart button is advertised without a stored
        # request/protocol identity.
        if self.runs_root.exists():
            for directory in sorted(self.runs_root.iterdir()):
                if not directory.is_dir() or directory.name in known:
                    continue
                manifest_path = directory / "manifest.json"
                if not manifest_path.is_file():
                    continue
                manifest = _read_json_object(manifest_path)
                started = str(manifest.get("started_at_utc") or "")
                finished = manifest.get("finished_at_utc")
                finalized = (directory / FINALIZATION_MARKER).is_file()
                raw_status = str(manifest.get("status", "running"))
                if finalized and raw_status == "completed":
                    status = RuntimeStatus.COMPLETED
                elif finalized and raw_status == "cancelled":
                    status = RuntimeStatus.CANCELLED
                elif finalized:
                    status = RuntimeStatus.FAILED
                else:
                    status = RuntimeStatus.INTERRUPTED
                snapshots.append(
                    RuntimeRunSnapshot(
                        schema_version=RUNTIME_SERVICE_SCHEMA_VERSION,
                        run_id=directory.name,
                        status=status,
                        created_at_utc=started,
                        updated_at_utc=str(finished or started),
                        heartbeat_at_utc=None,
                        protocol_path=None,
                        attempt=0,
                        process_id=None,
                        return_code=None,
                        progress=RuntimeProgress(0, 0, 0.0),
                        capabilities=RuntimeCapabilities(
                            can_cancel=False,
                            can_restart=False,
                            can_pause=False,
                            can_resume=False,
                        ),
                        latest_telemetry_sequence=None,
                        telemetry_path=None,
                        run_dir=str(directory),
                        message=(
                            "Historical/externally-created unfinished run; no "
                            "runtime request is available for restart."
                            if not finalized
                            else None
                        ),
                    )
                )
        snapshots.sort(
            key=lambda item: (item.created_at_utc, item.run_id), reverse=True
        )
        return tuple(snapshots)


__all__ = [
    "RUNTIME_SERVICE_SCHEMA_VERSION",
    "RuntimeCapabilities",
    "RuntimeProgress",
    "RuntimeRunSnapshot",
    "RuntimeService",
    "RuntimeStatus",
]
