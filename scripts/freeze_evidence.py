import json
import sys
from pathlib import Path
from datetime import datetime, timezone

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    
    runs_dir = repo_root / "results" / "runs"
    thesis_final_dir = repo_root / "results" / "thesis-final"
    thesis_final_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Identify all FINAL runs
    final_runs = []
    for d in runs_dir.iterdir():
        if d.is_dir() and d.name.startswith("FINAL-"):
            final_runs.append(d)
            
    # 2. Gather their statuses, manifests, and commit links
    evidence_set = []
    for d in sorted(final_runs):
        manifest_path = d / "manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            status = manifest.get("status", "unknown")
            commit = manifest.get("source", {}).get("git_commit", "unknown")
            reason = None
            if status != "completed":
                reason = "Failed or interrupted during execution"
            
            # verify checksums exist
            checksums_path = d / "checksums.sha256"
            has_checksums = checksums_path.exists()
            
            evidence_set.append({
                "run_id": d.name,
                "status": status,
                "git_commit": commit,
                "has_checksums": has_checksums,
                "inclusion": "included" if status == "completed" else "excluded",
                "exclusion_reason": reason,
            })
            
    # 3. Create freeze manifest
    freeze_manifest = {
        "freeze_time_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_version": "protocol-v1.0",
        "total_final_runs_found": len(evidence_set),
        "included_runs": len([r for r in evidence_set if r["inclusion"] == "included"]),
        "runs": evidence_set
    }
    
    freeze_path = thesis_final_dir / "freeze-manifest.json"
    freeze_path.write_text(json.dumps(freeze_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    
    print(f"Evidence freeze complete. Found {len(evidence_set)} runs.")
    print(f"Manifest written to {freeze_path.relative_to(repo_root)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
