import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_commit_reachable(commit: str, repo_root: Path) -> bool:
    try:
        subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                commit,
                "origin/archive/final-campaign-execution",
            ],
            cwd=str(repo_root),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def freeze_historical_v1(repo_root: Path) -> int:
    runs_dir = repo_root / "results" / "runs"
    thesis_final_dir = repo_root / "results" / "thesis-final"
    thesis_final_dir.mkdir(parents=True, exist_ok=True)

    final_runs = [
        d for d in runs_dir.iterdir() if d.is_dir() and d.name.startswith("FINAL-")
    ]

    evidence_set = []
    for d in sorted(final_runs):
        manifest_path = d / "manifest.json"
        if not manifest_path.exists():
            print(f"ERROR: Missing manifest for {d.name}")
            return 1

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        status = manifest.get("status", "unknown")
        commit = manifest.get("source", {}).get("git_commit", "unknown")
        protocol = manifest.get("protocol_version", "unknown")

        # 1. FINALIZED marker
        if not (d / "FINALIZED").exists():
            print(f"ERROR: {d.name} lacks FINALIZED marker.")
            return 1

        # 2. Status match
        if status != "completed":
            print(f"ERROR: {d.name} is not completed (status={status}).")
            return 1

        # 3. Checksum verification
        files_dict = manifest.get("files", {})
        payload_files = [
            p
            for p in d.iterdir()
            if p.is_file()
            and p.name not in {"manifest.json", "checksums.sha256", "FINALIZED"}
        ]

        if len(files_dict) != len(payload_files):
            print(f"ERROR: File count mismatch in {d.name}")
            return 1

        file_hashes = {}
        for p in payload_files:
            actual_hash = sha256_file(p)
            expected_hash = files_dict.get(p.name, {}).get("sha256")
            if actual_hash != expected_hash:
                print(
                    f"ERROR: Checksum mismatch for {d.name}/{p.name}. "
                    f"Expected {expected_hash}, got {actual_hash}"
                )
                return 1
            file_hashes[p.name] = actual_hash

        # 4. Source commit reachability
        if not check_commit_reachable(commit, repo_root):
            print(f"ERROR: Source commit {commit} is not reachable for {d.name}.")
            return 1

        evidence_set.append(
            {
                "run_id": d.name,
                "status": status,
                "git_commit": commit,
                "protocol_version": protocol,
                "file_hashes": file_hashes,
                "inclusion": "included",
                "exclusion_reason": None,
            }
        )

    if len(evidence_set) != 14:
        print(f"ERROR: Expected 14 final runs, found {len(evidence_set)}.")
        return 1

    freeze_manifest = {
        "freeze_time_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_version": "protocol-v1.0",
        "provenance_archive_ref": "origin/archive/final-campaign-execution",
        "total_final_runs_found": len(evidence_set),
        "included_runs": len(evidence_set),
        "runs": evidence_set,
    }

    freeze_path = thesis_final_dir / "freeze-manifest.json"
    freeze_path.write_text(
        json.dumps(freeze_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("Forensic Evidence freeze complete. Verified 14/14 runs strictly.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and freeze accepted evidence."
    )
    parser.add_argument(
        "--protocol-v2.1-final",
        dest="protocol_v2_1_final",
        action="store_true",
        help="freeze the accepted DEC-062 protocol-v2.1 replacement Study",
    )
    parser.add_argument("--validator-git-commit")
    parser.add_argument("--freeze-time-utc")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if not args.protocol_v2_1_final:
        if args.validator_git_commit or args.freeze_time_utc:
            parser.error("validator/freeze-time options require --protocol-v2.1-final")
        return freeze_historical_v1(repo_root)
    if not args.validator_git_commit or not args.freeze_time_utc:
        parser.error(
            "--protocol-v2.1-final requires --validator-git-commit "
            "and --freeze-time-utc"
        )

    if str(repo_root / "src") not in sys.path:
        sys.path.insert(0, str(repo_root / "src"))
    from resilient_agents.evidence_v2.freeze import (
        validate_and_freeze_protocol_v21_final,
    )

    result = validate_and_freeze_protocol_v21_final(
        repo_root,
        validator_git_commit=args.validator_git_commit,
        freeze_time_utc=args.freeze_time_utc,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
