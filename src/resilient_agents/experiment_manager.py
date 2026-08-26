"""Experiment management API for dashboard backend and batch execution."""
from __future__ import annotations

import json
import logging
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .run_bundle import FINALIZATION_MARKER, sha256_file

logger = logging.getLogger(__name__)

# Canonical run-index record keys (matches RunBundle._update_run_index).
_INDEX_RECORD_KEYS = {
    "run_id",
    "status",
    "protocol_version",
    "stage",
    "started_at_utc",
    "finished_at_utc",
    "source_git_commit",
}

_FINAL_STATUSES = {"completed", "failed", "cancelled", "invalid"}


@contextmanager
def acquire_single_writer_lock(
    repo_root: Path, timeout: float = 300.0
) -> Iterator[None]:
    """Provides a safe single-writer boundary using a directory lock."""
    lock_path = repo_root / "results" / ".publish.lock"
    start = time.monotonic()
    while True:
        try:
            lock_path.mkdir(parents=True, exist_ok=False)
            break
        except FileExistsError:
            if time.monotonic() - start > timeout:
                raise TimeoutError(
                    "Could not acquire publication single-writer lock"
                )
            time.sleep(1.0)
    try:
        yield
    finally:
        try:
            lock_path.rmdir()
        except OSError:
            pass


def _read_finalization_marker(marker_path: Path) -> dict[str, str]:
    """Parse the canonical FINALIZED marker file into key-value pairs."""
    result: dict[str, str] = {}
    for line in marker_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip()
    return result


def _validate_bundle_integrity(run_dir: Path, run_id: str) -> dict[str, Any]:
    """Validate a finalized run bundle matches the canonical contract.

    Checks:
    - FINALIZATION_MARKER exists
    - manifest.json exists, is valid JSON, has matching run_id
    - manifest status is a final status
    - marker status matches manifest status
    - checksums.sha256 exists and all checksums verify
    - manifest file metadata matches actual file hashes and sizes

    Raises ValueError for any malformed/inconsistent finalized bundle.
    Returns the validated manifest dict.
    """
    marker_path = run_dir / FINALIZATION_MARKER
    manifest_path = run_dir / "manifest.json"
    checksum_path = run_dir / "checksums.sha256"

    if not marker_path.is_file():
        raise ValueError(
            f"Bundle {run_id} has no finalization marker; "
            "it is unfinished or interrupted"
        )
    if not manifest_path.is_file():
        raise ValueError(f"Finalized bundle {run_id} is missing manifest.json")
    if not checksum_path.is_file():
        raise ValueError(
            f"Finalized bundle {run_id} is missing checksums.sha256"
        )

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"Cannot read manifest for finalized bundle {run_id}"
        ) from exc

    if not isinstance(manifest, dict):
        raise ValueError(f"Manifest in {run_id} is not a JSON object")
    if manifest.get("run_id") != run_id:
        raise ValueError(
            f"Manifest run_id mismatch in {run_id}: "
            f"expected {run_id!r}, got {manifest.get('run_id')!r}"
        )

    status = str(manifest.get("status", ""))
    if status not in _FINAL_STATUSES:
        raise ValueError(
            f"Bundle {run_id} manifest status {status!r} is not a final status"
        )

    # Validate finalization marker matches manifest
    marker = _read_finalization_marker(marker_path)
    expected_marker = {
        "schema_version": str(manifest.get("schema_version")),
        "status": status,
    }
    if marker != expected_marker:
        raise ValueError(
            f"Finalization marker in {run_id} does not match manifest"
        )

    # Validate manifest file metadata
    files_metadata = manifest.get("files")
    if not isinstance(files_metadata, dict):
        raise ValueError(f"Manifest files metadata in {run_id} is not a dict")
    for name, metadata in files_metadata.items():
        if not isinstance(metadata, dict):
            raise ValueError(
                f"Invalid file metadata for {name} in {run_id}"
            )
        path = run_dir / name
        if not path.is_file():
            raise ValueError(
                f"Manifest references missing file {name} in {run_id}"
            )
        expected_hash = metadata.get("sha256")
        expected_size = metadata.get("size_bytes")
        actual_hash = sha256_file(path)
        actual_size = path.stat().st_size
        if expected_hash != actual_hash or expected_size != actual_size:
            raise ValueError(
                f"Integrity mismatch for {name} in {run_id}"
            )

    # Validate checksums.sha256
    try:
        lines = checksum_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValueError(
            f"Cannot read checksums for {run_id}"
        ) from exc
    recorded: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        parts = line.split("  ", 1)
        if len(parts) != 2:
            raise ValueError(
                f"Malformed checksum line {number} in {run_id}"
            )
        digest, name = parts
        if name in recorded:
            raise ValueError(f"Duplicate checksum entry {name} in {run_id}")
        recorded[name] = digest

    actual_files = {
        path.name: path
        for path in run_dir.iterdir()
        if path.is_file()
        and path.name not in {"checksums.sha256", FINALIZATION_MARKER}
    }
    if set(recorded) != set(actual_files):
        raise ValueError(
            f"Checksum scope does not match bundle files in {run_id}"
        )
    for name, path in actual_files.items():
        if sha256_file(path) != recorded[name]:
            raise ValueError(f"Checksum mismatch for {name} in {run_id}")

    return manifest


class ExperimentRegistry:
    """Provides access to historical runs and rebuilds the index safely.

    Uses the canonical FINALIZATION_MARKER from run_bundle.py.
    Unfinished bundles (no marker) are silently skipped during rebuild.
    Finalized bundles with integrity failures raise ValueError (fail closed).
    """

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.runs_dir = self.repo_root / "results" / "runs"
        self.index_path = self.repo_root / "results" / "run-index.jsonl"

    def rebuild_index(self) -> None:
        """Rebuild the index from individual finalized run bundles.

        Unfinished bundles are silently skipped (they are resumable).
        Finalized bundles that fail integrity checks raise ValueError.
        """
        records: list[str] = []
        if self.runs_dir.exists():
            for run_dir in sorted(self.runs_dir.iterdir()):
                if not run_dir.is_dir():
                    continue
                marker = run_dir / FINALIZATION_MARKER
                if not marker.exists():
                    # Unfinished/interrupted — skip silently; it's resumable
                    continue

                # Finalized: must pass full integrity check or fail closed
                manifest = _validate_bundle_integrity(run_dir, run_dir.name)

                record = {
                    "run_id": manifest["run_id"],
                    "status": manifest["status"],
                    "protocol_version": manifest["protocol_version"],
                    "stage": manifest["stage"],
                    "started_at_utc": manifest["started_at_utc"],
                    "finished_at_utc": manifest["finished_at_utc"],
                    "source_git_commit": manifest.get("source", {}).get(
                        "git_commit"
                    ),
                }
                records.append(
                    json.dumps(record, ensure_ascii=False, sort_keys=True)
                )

        with acquire_single_writer_lock(self.repo_root):
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            self.index_path.write_text(
                "\n".join(records) + ("\n" if records else ""),
                encoding="utf-8",
            )

    def list_runs(self) -> list[dict[str, Any]]:
        """Return all finalized run records from the index."""
        if not self.index_path.exists():
            self.rebuild_index()
        runs: list[dict[str, Any]] = []
        for line in self.index_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                runs.append(json.loads(line))
        return runs

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        """Load a specific run's manifest and resolved config."""
        run_dir = self.runs_dir / run_id
        manifest_path = run_dir / "manifest.json"
        config_path = run_dir / "resolved-config.json"
        if not manifest_path.exists():
            return None
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        config: dict[str, Any] = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        return {"manifest": manifest, "config": config}


def get_resource_snapshot(repo_root: Path) -> dict[str, Any]:
    """Return a current system resource snapshot using the canonical collector.

    Returns the full system_inventory schema-v2 payload. Callers should access
    top-level keys: cpu, memory, storage, accelerators, system, etc.
    """
    script_path = repo_root / "scripts" / "system_inventory.py"
    try:
        result = subprocess.check_output(
            [sys.executable, str(script_path)],
            encoding="utf-8",
            timeout=20,
        )
        return json.loads(result)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        logger.warning("System inventory unavailable: %s", exc)
        return {"status": "unavailable"}


class CampaignManager:
    """Batch executes experiments using a single-writer boundary."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.registry = ExperimentRegistry(repo_root)

    def launch_batch(
        self, protocol_path: Path, requests: list[dict[str, Any]]
    ) -> None:
        """Execute a batch of headless run requests sequentially.

        Each request is written to a temp file and passed to
        scripts/run_headless_experiment.py via --request.
        Already-finalized runs are skipped.
        """
        runner_script = self.repo_root / "scripts" / "run_headless_experiment.py"

        for req in requests:
            run_id = req["run_id"]
            run_dir = self.repo_root / "results" / "runs" / run_id
            finalized_marker = run_dir / FINALIZATION_MARKER
            if finalized_marker.exists():
                logger.info("Run %s is already finalized, skipping.", run_id)
                continue

            with acquire_single_writer_lock(self.repo_root):
                with tempfile.NamedTemporaryFile(
                    "w", suffix=".json", delete=False
                ) as f:
                    json.dump(req, f)
                    req_path = f.name

                cmd = [
                    sys.executable,
                    str(runner_script),
                    "--repo-root",
                    str(self.repo_root),
                    "--protocol",
                    str(protocol_path),
                    "--request",
                    req_path,
                ]

                logger.info("Launching run %s", run_id)
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    logger.error(
                        "Run %s failed with code %d", run_id, e.returncode
                    )
                    raise
                finally:
                    import os

                    if os.path.exists(req_path):
                        os.unlink(req_path)
