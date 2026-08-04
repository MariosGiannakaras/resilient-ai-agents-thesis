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


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(_jsonable(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


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


def source_provenance(repo_root: Path) -> dict[str, Any]:
    commit = _git(repo_root, "rev-parse", "HEAD")
    tracked_status = _git(repo_root, "status", "--porcelain", "--untracked-files=no")
    return {
        "git_commit": commit,
        "tracked_changes_present": bool(tracked_status) if tracked_status is not None else None,
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

    def append_event(self, event: Mapping[str, Any]) -> None:
        self._append_jsonl("events.jsonl", event)

    def append_trace(self, record: Mapping[str, Any]) -> None:
        self._append_jsonl("trace.jsonl", record)

    def _append_jsonl(self, filename: str, payload: Mapping[str, Any]) -> None:
        path = self.run_dir / filename
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(_jsonable(payload), ensure_ascii=False, sort_keys=True))
            handle.write("\n")

    def finalize(self, *, status: str, summary: Mapping[str, Any]) -> Path:
        if status not in {"complete", "failed", "cancelled", "invalid", "excluded"}:
            raise ValueError("unsupported final run status")
        _write_json(self.run_dir / "summary.json", summary)
        self.manifest["status"] = status
        self.manifest["finished_at_utc"] = _utc_now()

        payload_files = [
            path
            for path in self.run_dir.iterdir()
            if path.is_file() and path.name not in {"manifest.json", "checksums.sha256"}
        ]
        self.manifest["files"] = {
            path.name: {"sha256": sha256_file(path), "size_bytes": path.stat().st_size}
            for path in sorted(payload_files)
        }
        _write_json(self.run_dir / "manifest.json", self.manifest)

        checksum_lines = []
        for path in sorted(self.run_dir.iterdir()):
            if path.is_file() and path.name != "checksums.sha256":
                checksum_lines.append(f"{sha256_file(path)}  {path.name}")
        (self.run_dir / "checksums.sha256").write_text(
            "\n".join(checksum_lines) + "\n", encoding="utf-8"
        )
        self._update_run_index()
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
        temporary = index_path.with_suffix(".jsonl.tmp")
        temporary.write_text("\n".join([*without_same_run, encoded]) + "\n", encoding="utf-8")
        temporary.replace(index_path)
