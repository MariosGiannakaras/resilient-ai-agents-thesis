"""Safe one-commit/one-push publication for finalized experiment bundles."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

FINAL_STATUSES = {"complete", "failed", "cancelled", "invalid", "excluded"}


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
    """Commit and push exactly one finalized whole-experiment run bundle.

    A run may contain many seeds/episodes. Publication happens only after the
    bundle is finalized, so there is never one commit per seed. Unrelated tracked
    changes, changed source code, non-fast-forward remotes, and missing Git LFS
    are treated as safe publication failures; the run files remain on disk.
    """

    repo_root = repo_root.resolve()
    run_dir = repo_root / "results" / "runs" / run_id
    manifest_path = run_dir / "manifest.json"
    index_path = repo_root / "results" / "run-index.jsonl"
    if not manifest_path.is_file():
        raise PublishError(f"run manifest not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    status = str(manifest.get("status", ""))
    if status not in FINAL_STATUSES:
        raise PublishError("run bundle must be finalized before publication")

    source_commit = manifest.get("source", {}).get("git_commit")
    if not source_commit:
        raise PublishError("run manifest has no source Git commit")
    current_commit = _run(repo_root, ["rev-parse", "HEAD"])
    if current_commit != source_commit:
        raise PublishError("repository HEAD changed after the run started; refusing mixed provenance")
    if manifest.get("source", {}).get("tracked_changes_present"):
        raise PublishError("run started from a repository with tracked changes")

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
