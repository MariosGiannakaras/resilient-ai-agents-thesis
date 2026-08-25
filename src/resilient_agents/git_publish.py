"""Safe one-commit/one-push publication for finalized experiment bundles."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

FINAL_STATUSES = {"completed", "failed", "cancelled", "invalid"}
FINALIZATION_MARKER = "FINALIZED"
CHECKSUM_RE = re.compile(r"^([0-9a-f]{64})  ([^/\\]+)$")


class PublishError(RuntimeError):
    pass


@dataclass(frozen=True)
class PublishResult:
    commit: str
    branch: str
    remote: str


def _run(repo_root: Path, args: Sequence[str], *, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise PublishError(message)
    return result.stdout.strip()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PublishError(f"invalid run manifest: {path}") from exc
    if not isinstance(value, dict):
        raise PublishError("run manifest must be a JSON object")
    return value


def _read_finalization_marker(path: Path) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise PublishError("cannot read run finalization marker") from exc

    fields: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        if not line or "=" not in line:
            raise PublishError(f"malformed run finalization marker line {number}")
        key, value = line.split("=", 1)
        if key not in {"schema_version", "status"} or key in fields:
            raise PublishError("run finalization marker contains invalid or duplicate fields")
        fields[key] = value
    return fields


def _verify_run_index(index_path: Path, manifest: dict[str, Any]) -> None:
    if not index_path.is_file():
        raise PublishError("finalized run bundle has no run-index entry")
    try:
        lines = index_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise PublishError("cannot read run index") from exc

    matches: list[dict[str, Any]] = []
    for number, line in enumerate(lines, start=1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PublishError(f"invalid run-index JSON on line {number}") from exc
        if not isinstance(record, dict):
            raise PublishError(f"run-index line {number} must be a JSON object")
        if record.get("run_id") == manifest.get("run_id"):
            matches.append(record)

    if len(matches) != 1:
        raise PublishError("finalized run must have exactly one matching run-index entry")

    source = manifest.get("source")
    if not isinstance(source, dict):
        raise PublishError("run manifest source provenance must be an object")
    expected = {
        "run_id": manifest.get("run_id"),
        "status": manifest.get("status"),
        "protocol_version": manifest.get("protocol_version"),
        "stage": manifest.get("stage"),
        "started_at_utc": manifest.get("started_at_utc"),
        "finished_at_utc": manifest.get("finished_at_utc"),
        "source_git_commit": source.get("git_commit"),
    }
    record = matches[0]
    mismatched = [key for key, value in expected.items() if record.get(key) != value]
    if mismatched:
        raise PublishError(
            "run-index entry does not match finalized manifest: " + ", ".join(mismatched)
        )


def _verify_finalized_bundle(run_dir: Path, run_id: str) -> dict[str, Any]:
    marker_path = run_dir / FINALIZATION_MARKER
    manifest_path = run_dir / "manifest.json"
    checksum_path = run_dir / "checksums.sha256"

    if not marker_path.is_file():
        raise PublishError("run bundle has no finalization marker; refusing partial publication")
    if not manifest_path.is_file():
        raise PublishError(f"run manifest not found: {manifest_path}")
    if not checksum_path.is_file():
        raise PublishError("finalized run bundle has no checksum manifest")

    manifest = _read_manifest(manifest_path)
    if manifest.get("run_id") != run_id:
        raise PublishError("run directory and manifest run_id do not match")
    status = str(manifest.get("status", ""))
    if status not in FINAL_STATUSES:
        raise PublishError("run bundle must be finalized before publication")

    marker = _read_finalization_marker(marker_path)
    expected_marker = {
        "schema_version": str(manifest.get("schema_version")),
        "status": status,
    }
    if marker != expected_marker:
        raise PublishError("run finalization marker does not match finalized manifest")

    files_metadata = manifest.get("files")
    if not isinstance(files_metadata, dict):
        raise PublishError("run manifest files metadata must be an object")
    for name, metadata in files_metadata.items():
        if not isinstance(name, str) or Path(name).name != name or not isinstance(metadata, dict):
            raise PublishError("run manifest contains invalid file metadata")
        path = run_dir / name
        if not path.is_file():
            raise PublishError(f"run manifest references missing payload file: {name}")
        expected_hash = metadata.get("sha256")
        expected_size = metadata.get("size_bytes")
        if expected_hash != _sha256_file(path) or expected_size != path.stat().st_size:
            raise PublishError(f"run payload integrity mismatch: {name}")

    try:
        lines = checksum_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise PublishError("cannot read finalized run checksum manifest") from exc
    recorded: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        match = CHECKSUM_RE.fullmatch(line)
        if not match:
            raise PublishError(f"malformed run checksum line {number}")
        digest, name = match.groups()
        if name in recorded:
            raise PublishError(f"duplicate run checksum path: {name}")
        recorded[name] = digest

    actual_files = {
        path.name: path
        for path in run_dir.iterdir()
        if path.is_file() and path.name not in {"checksums.sha256", FINALIZATION_MARKER}
    }
    if set(recorded) != set(actual_files):
        raise PublishError("run checksum scope does not match finalized bundle files")
    for name, path in actual_files.items():
        if _sha256_file(path) != recorded[name]:
            raise PublishError(f"run checksum mismatch: {name}")

    return manifest


def _tracked_changes(repo_root: Path) -> list[str]:
    output = _run(repo_root, ["status", "--porcelain", "--untracked-files=no"])
    paths: list[str] = []
    for line in output.splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return paths


def _requires_lfs(repo_root: Path, paths: Sequence[str]) -> bool:
    for path in paths:
        attributes = _run(repo_root, ["check-attr", "filter", "--", path], check=False)
        if attributes.rstrip().endswith(": lfs"):
            return True
    return False


def publish_finalized_run(
    *, repo_root: Path, run_id: str, remote: str = "origin"
) -> PublishResult:
    """Commit and push exactly one verified finalized whole-experiment bundle.

    A run may contain many seeds/episodes. Publication happens only after the
    completion marker, manifest, checksums, and run-index entry agree, so partial
    or corrupted evidence fails before Git staging. Unrelated tracked changes,
    changed source code, non-fast-forward remotes, and missing Git LFS are also
    safe publication failures; the run files remain on disk.
    """

    repo_root = repo_root.resolve()
    run_dir = repo_root / "results" / "runs" / run_id
    index_path = repo_root / "results" / "run-index.jsonl"
    manifest = _verify_finalized_bundle(run_dir, run_id)
    status = str(manifest["status"])

    source = manifest.get("source")
    if not isinstance(source, dict):
        raise PublishError("run manifest source provenance must be an object")
    source_commit = source.get("git_commit")
    if not source_commit:
        raise PublishError("run manifest has no source Git commit")
    _verify_run_index(index_path, manifest)

    current_commit = _run(repo_root, ["rev-parse", "HEAD"])
    if current_commit != source_commit:
        raise PublishError("repository HEAD changed after the run started; refusing mixed provenance")
    if source.get("tracked_changes_present") is not False:
        raise PublishError("run did not start from a verified clean tracked repository state")

    allowed_prefix = f"results/runs/{run_id}/"
    allowed_exact = {"results/run-index.jsonl"}
    unrelated = [
        path
        for path in _tracked_changes(repo_root)
        if path not in allowed_exact and not path.startswith(allowed_prefix)
    ]
    if unrelated:
        raise PublishError(
            "unrelated tracked changes present; refusing automatic commit: " + ", ".join(unrelated)
        )

    relative_paths = [
        path.relative_to(repo_root).as_posix() for path in run_dir.rglob("*") if path.is_file()
    ]
    if index_path.exists():
        relative_paths.append(index_path.relative_to(repo_root).as_posix())
    if _requires_lfs(repo_root, relative_paths):
        lfs = subprocess.run(
            ["git", "lfs", "version"], capture_output=True, text=True, check=False, timeout=10
        )
        if lfs.returncode != 0:
            raise PublishError("Git LFS is required for this run but is not installed/configured")

    _run(repo_root, ["add", "--", *relative_paths])
    staged = _run(repo_root, ["diff", "--cached", "--name-only"])
    if not staged:
        raise PublishError("run produced no staged repository changes")

    branch = _run(repo_root, ["branch", "--show-current"])
    if not branch:
        raise PublishError("automatic publication requires a named Git branch")

    protocol = str(manifest.get("protocol_version", "unknown"))
    stage = str(manifest.get("stage", "unknown"))
    title = f"experiment: {status} {run_id}"
    body = "\n".join(
        [
            f"Run-ID: {run_id}",
            f"Protocol: {protocol}",
            f"Stage: {stage}",
            f"Source-Commit: {source_commit}",
            f"Status: {status}",
        ]
    )
    _run(repo_root, ["commit", "-m", title, "-m", body])
    commit = _run(repo_root, ["rev-parse", "HEAD"])

    _run(repo_root, ["fetch", remote, branch])
    remote_ref = f"{remote}/{branch}"
    relation = subprocess.run(
        ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", remote_ref, commit],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    if relation.returncode != 0:
        raise PublishError(
            "remote branch advanced independently; run commit is preserved locally but was not pushed"
        )
    _run(repo_root, ["push", remote, f"HEAD:{branch}"])
    return PublishResult(commit=commit, branch=branch, remote=remote)
