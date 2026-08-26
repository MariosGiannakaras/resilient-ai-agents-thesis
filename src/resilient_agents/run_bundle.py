"""Self-contained experiment run bundles and provenance capture."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA_VERSION = 1
FINALIZATION_MARKER = "FINALIZED"
GENERATED_OUTPUT_PREFIXES = ("results/", "artifacts/")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "value") and isinstance(getattr(value, "value"), str):
        return value.value
    return value


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _write_json(path: Path, payload: Any) -> None:
    _write_text_atomic(
        path,
        json.dumps(_jsonable(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def _git(repo_root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _untracked_nonoutput_present(repo_root: Path) -> bool | None:
    output = _git(repo_root, "ls-files", "-z", "--others", "--exclude-standard")
    if output is None:
        return None
    paths = [path for path in output.split("\0") if path]
    return any(not path.startswith(GENERATED_OUTPUT_PREFIXES) for path in paths)


def _tracked_diff_sha256(repo_root: Path) -> str | None:
    output = _git(repo_root, "diff", "--binary", "HEAD")
    if output is None:
        return None
    return hashlib.sha256(output.encode("utf-8")).hexdigest()


def _untracked_nonoutput_sha256(repo_root: Path) -> str | None:
    output = _git(repo_root, "ls-files", "-z", "--others", "--exclude-standard")
    if output is None:
        return None
    paths = sorted(
        path
        for path in output.split("\0")
        if path and not path.startswith(GENERATED_OUTPUT_PREFIXES)
    )
    digest = hashlib.sha256()
    try:
        for relative in paths:
            path = repo_root / relative
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(bytes.fromhex(sha256_file(path)))
    except OSError:
        return None
    return digest.hexdigest()


def source_provenance(repo_root: Path) -> dict[str, Any]:
    commit = _git(repo_root, "rev-parse", "HEAD")
    tracked_status = _git(repo_root, "status", "--porcelain", "--untracked-files=no")
    return {
        "git_commit": commit,
        "tracked_changes_present": bool(tracked_status) if tracked_status is not None else None,
        "untracked_nonoutput_present": _untracked_nonoutput_present(repo_root),
        "tracked_diff_sha256": _tracked_diff_sha256(repo_root),
        "untracked_nonoutput_sha256": _untracked_nonoutput_sha256(repo_root),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }


def capture_system_inventory(repo_root: Path) -> dict[str, Any]:
    script = repo_root / "scripts" / "system_inventory.py"
    if not script.is_file():
        return {"status": "unavailable", "reason": "collector-not-found"}
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        return {"status": "unavailable", "reason": "collector-execution-failed"}
    if result.returncode != 0:
        return {"status": "unavailable", "reason": "collector-returned-nonzero"}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"status": "unavailable", "reason": "collector-output-invalid"}
    return {"status": "captured", "inventory": payload}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class RunBundle:
    """Writes one whole-experiment bundle for later audit and publication."""

    def __init__(
        self,
        *,
        repo_root: Path,
        run_id: str,
        resolved_config: Mapping[str, Any],
        protocol_version: str,
        stage: str,
        retention_policy: str,
    ) -> None:
        if not run_id.strip():
            raise ValueError("run_id must be non-empty")
        self.repo_root = repo_root.resolve()
        self.run_id = run_id
        self.run_dir = self.repo_root / "results" / "runs" / run_id
        if self.run_dir.exists():
            raise FileExistsError(f"run bundle already exists: {self.run_dir}")
        self.run_dir.mkdir(parents=True)
        self.started_at = _utc_now()
        self.provenance = source_provenance(self.repo_root)
        self.manifest: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "status": "running",
            "protocol_version": protocol_version,
            "stage": stage,
            "retention_policy": retention_policy,
            "started_at_utc": self.started_at,
            "finished_at_utc": None,
            "source": self.provenance,
            "files": {},
        }
        _write_json(self.run_dir / "resolved-config.json", resolved_config)
        _write_json(self.run_dir / "system-capability.json", capture_system_inventory(self.repo_root))
        _write_json(self.run_dir / "manifest.json", self.manifest)

    @classmethod
    def resume(
        cls,
        *,
        repo_root: Path,
        run_id: str,
        resolved_config: Mapping[str, Any],
        protocol_version: str,
        stage: str,
        retention_policy: str,
    ) -> "RunBundle":
        """Reopen an unfinished bundle only when identity/provenance still agree."""

        root = repo_root.resolve()
        run_dir = root / "results" / "runs" / run_id
        if not run_dir.is_dir():
            raise FileNotFoundError(f"run bundle does not exist: {run_dir}")
        if (run_dir / FINALIZATION_MARKER).exists():
            raise RuntimeError("finalized run bundles cannot be resumed")
        try:
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
            stored_config = json.loads(
                (run_dir / "resolved-config.json").read_text(encoding="utf-8")
            )
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RuntimeError("unfinished run bundle metadata is unreadable") from exc
        if not isinstance(manifest, dict) or manifest.get("status") != "running":
            raise RuntimeError("only an explicitly running bundle can be resumed")
        expected_identity = {
            "run_id": run_id,
            "protocol_version": protocol_version,
            "stage": stage,
            "retention_policy": retention_policy,
        }
        if any(manifest.get(key) != value for key, value in expected_identity.items()):
            raise RuntimeError("resume identity does not match the stored manifest")
        if _jsonable(resolved_config) != stored_config:
            raise RuntimeError("resume resolved configuration does not match")
        stored_source = manifest.get("source")
        if not isinstance(stored_source, dict):
            raise RuntimeError("resume source provenance is unavailable")
        current_source = source_provenance(root)
        if current_source.get("git_commit") != stored_source.get("git_commit"):
            raise RuntimeError("source Git commit changed since the run started")
        if current_source.get("tracked_changes_present") != stored_source.get(
            "tracked_changes_present"
        ):
            raise RuntimeError("tracked source state changed since the run started")
        if current_source.get("untracked_nonoutput_present") != stored_source.get(
            "untracked_nonoutput_present"
        ):
            raise RuntimeError("untracked non-output source state changed since run start")
        if current_source.get("tracked_diff_sha256") != stored_source.get(
            "tracked_diff_sha256"
        ):
            raise RuntimeError("tracked source content changed since the run started")
        if current_source.get("untracked_nonoutput_sha256") != stored_source.get(
            "untracked_nonoutput_sha256"
        ):
            raise RuntimeError("untracked non-output inputs changed since run start")
        cls._validate_resumable_jsonl(run_dir / "events.jsonl")
        cls._validate_resumable_jsonl(run_dir / "trace.jsonl")

        bundle = cls.__new__(cls)
        bundle.repo_root = root
        bundle.run_id = run_id
        bundle.run_dir = run_dir
        bundle.started_at = str(manifest.get("started_at_utc"))
        bundle.provenance = stored_source
        bundle.manifest = manifest
        return bundle

    @staticmethod
    def _validate_resumable_jsonl(path: Path) -> None:
        if not path.exists():
            return
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise RuntimeError(f"resume log is unreadable: {path.name}") from exc
        if content and not content.endswith("\n"):
            raise RuntimeError(f"resume log has an incomplete final line: {path.name}")
        for number, line in enumerate(content.splitlines(), start=1):
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"resume log contains invalid JSON at {path.name}:{number}"
                ) from exc
            if not isinstance(value, dict):
                raise RuntimeError(
                    f"resume log entry must be an object at {path.name}:{number}"
                )

    def _require_running(self) -> None:
        if self.manifest.get("status") != "running":
            raise RuntimeError("run bundle is already finalized and cannot be mutated")

    def append_event(self, event: Mapping[str, Any]) -> None:
        self._require_running()
        self._append_jsonl("events.jsonl", event)

    def append_trace(self, record: Mapping[str, Any]) -> None:
        self._require_running()
        self._append_jsonl("trace.jsonl", record)

    def write_json_artifact(self, filename: str, payload: Mapping[str, Any]) -> Path:
        """Atomically replace one top-level JSON checkpoint while running."""

        self._require_running()
        if (
            not isinstance(filename, str)
            or not filename.endswith(".json")
            or Path(filename).name != filename
            or filename in {"manifest.json", "resolved-config.json", "system-capability.json"}
        ):
            raise ValueError("artifact filename must be a safe non-reserved .json name")
        if not isinstance(payload, Mapping):
            raise ValueError("JSON artifact payload must be an object")
        path = self.run_dir / filename
        _write_json(path, payload)
        return path

    def _append_jsonl(self, filename: str, payload: Mapping[str, Any]) -> None:
        path = self.run_dir / filename
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(_jsonable(payload), ensure_ascii=False, sort_keys=True))
            handle.write("\n")

    def finalize(self, *, status: str, summary: Mapping[str, Any]) -> Path:
        self._require_running()
        if status not in {"completed", "failed", "cancelled", "invalid"}:
            raise ValueError("unsupported final run status")

        _write_json(self.run_dir / "summary.json", summary)
        self.manifest["status"] = status
        self.manifest["finished_at_utc"] = _utc_now()

        payload_files = [
            path
            for path in self.run_dir.iterdir()
            if path.is_file()
            and path.name not in {"manifest.json", "checksums.sha256", FINALIZATION_MARKER}
        ]
        self.manifest["files"] = {
            path.name: {"sha256": sha256_file(path), "size_bytes": path.stat().st_size}
            for path in sorted(payload_files)
        }
        _write_json(self.run_dir / "manifest.json", self.manifest)

        checksum_lines = []
        for path in sorted(self.run_dir.iterdir()):
            if path.is_file() and path.name not in {"checksums.sha256", FINALIZATION_MARKER}:
                checksum_lines.append(f"{sha256_file(path)}  {path.name}")
        _write_text_atomic(
            self.run_dir / "checksums.sha256",
            "\n".join(checksum_lines) + "\n",
        )

        # The index is a rebuildable cache, but a failed update is still explicit:
        # do not advertise the bundle as finalized until every planned finalization
        # side effect has succeeded.
        self._update_run_index()

        # This marker is deliberately written last. Consumers/publishers require
        # it, so a partially failed finalization cannot masquerade as finalized.
        _write_text_atomic(
            self.run_dir / FINALIZATION_MARKER,
            f"schema_version={SCHEMA_VERSION}\nstatus={status}\n",
        )
        return self.run_dir

    def _update_run_index(self) -> None:
        index_path = self.repo_root / "results" / "run-index.jsonl"
        existing: list[str] = []
        if index_path.exists():
            existing = [line for line in index_path.read_text(encoding="utf-8").splitlines() if line]
        record = {
            "run_id": self.run_id,
            "status": self.manifest["status"],
            "protocol_version": self.manifest["protocol_version"],
            "stage": self.manifest["stage"],
            "started_at_utc": self.manifest["started_at_utc"],
            "finished_at_utc": self.manifest["finished_at_utc"],
            "source_git_commit": self.provenance.get("git_commit"),
        }
        encoded = json.dumps(record, ensure_ascii=False, sort_keys=True)
        without_same_run = [
            line for line in existing if json.loads(line).get("run_id") != self.run_id
        ]
        _write_text_atomic(index_path, "\n".join([*without_same_run, encoded]) + "\n")
