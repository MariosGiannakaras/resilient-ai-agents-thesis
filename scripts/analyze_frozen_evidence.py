import json
import sys
from pathlib import Path

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    
    if str(repo_root / "src") not in sys.path:
        sys.path.insert(0, str(repo_root / "src"))
        
    from resilient_agents.analysis import write_analysis
    
    freeze_path = repo_root / "results" / "thesis-final" / "freeze-manifest.json"
    if not freeze_path.exists():
        print("Error: freeze-manifest.json not found.", file=sys.stderr)
        return 1
        
    manifest = json.loads(freeze_path.read_text(encoding="utf-8"))
    run_ids = [r["run_id"] for r in manifest.get("runs", []) if r["inclusion"] == "included"]
    
    if not run_ids:
        print("No included runs found in freeze manifest.", file=sys.stderr)
        return 1
        
    print(f"Running analysis on {len(run_ids)} frozen runs...")
    
    result = write_analysis(
        repo_root=repo_root,
        analysis_id="thesis-final-analysis",
        run_ids=run_ids,
    )
    
    print(f"Analysis written to: {result.analysis_dir.relative_to(repo_root)}")
    print(f"Valid units: {result.unit_count}")
    print(f"Sensitivity records: {result.sensitivity_record_count}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
