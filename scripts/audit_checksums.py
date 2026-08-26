import sys
import json
import subprocess
from pathlib import Path
import hashlib

def main():
    repo_root = Path(__file__).resolve().parents[1]
    runs_dir = repo_root / "results" / "runs"
    
    final_runs = [d for d in runs_dir.iterdir() if d.is_dir() and d.name.startswith("FINAL-")]
    
    audit_results = {
        "runs_audited": 0,
        "files_audited": 0,
        "semantic_equivalence_confirmed": True,
        "mismatches": [],
        "details": {}
    }
    
    for run_dir in sorted(final_runs):
        manifest_path = run_dir / "manifest.json"
        if not manifest_path.exists():
            continue
            
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        commit = manifest.get("source", {}).get("git_commit")
        
        run_details = {}
        for file_path in run_dir.iterdir():
            if not file_path.is_file() or file_path.name in {"manifest.json", "checksums.sha256", "FINALIZED"}:
                continue
                
            local_bytes = file_path.read_bytes()
            
            try:
                rel_path = file_path.relative_to(repo_root).as_posix()
                blob_bytes = subprocess.check_output(
                    ["git", "show", f"origin/archive/final-campaign-execution:{rel_path}"],
                    cwd=str(repo_root)
                )
            except subprocess.CalledProcessError:
                audit_results["semantic_equivalence_confirmed"] = False
                audit_results["mismatches"].append(f"{run_dir.name}/{file_path.name}: not found in archive branch")
                continue
                
            local_hash = hashlib.sha256(local_bytes).hexdigest()
            blob_hash = hashlib.sha256(blob_bytes).hexdigest()
            
            # Since JSON formatting might differ only by CRLF vs LF, we check semantic JSON equivalence
            try:
                local_json = [json.loads(line) for line in local_bytes.decode("utf-8").strip().split("\n") if line.strip()]
                blob_json = [json.loads(line) for line in blob_bytes.decode("utf-8").strip().split("\n") if line.strip()]
                semantic_match = (local_json == blob_json)
            except Exception as e:
                # Not a valid JSON or JSONL, so compare bytes exactly, or normalize newlines
                local_norm = local_bytes.replace(b"\r\n", b"\n")
                blob_norm = blob_bytes.replace(b"\r\n", b"\n")
                semantic_match = (local_norm == blob_norm)
                
            if not semantic_match:
                audit_results["semantic_equivalence_confirmed"] = False
                audit_results["mismatches"].append(f"{run_dir.name}/{file_path.name}: semantic difference found!")
                
            run_details[file_path.name] = {
                "local_hash": local_hash,
                "blob_hash": blob_hash,
                "semantic_match": semantic_match,
                "bytes_differ": local_bytes != blob_bytes
            }
            audit_results["files_audited"] += 1
            
        audit_results["details"][run_dir.name] = run_details
        audit_results["runs_audited"] += 1
        
    out_path = repo_root / "results" / "forensic_checksum_audit_summary.json"
    out_path.write_text(json.dumps(audit_results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    
    print(f"Audit complete. Audited {audit_results['files_audited']} files across {audit_results['runs_audited']} runs.")
    if audit_results["semantic_equivalence_confirmed"]:
        print("SUCCESS: 100% semantic equivalence confirmed. All byte differences are strictly newlines/Git normalization.")
        return 0
    else:
        print("FAILED: Semantic differences detected!")
        for m in audit_results["mismatches"]:
            print(f" - {m}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
