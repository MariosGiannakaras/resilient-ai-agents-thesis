import sys
import shutil
from pathlib import Path

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    
    thesis_final_dir = repo_root / "results" / "thesis-final"
    summaries_dir = repo_root / "results" / "summaries" / "thesis-final-analysis"
    
    if not thesis_final_dir.exists() or not summaries_dir.exists():
        print("Missing required frozen directories.", file=sys.stderr)
        return 1
        
    staging_dir = repo_root / "results" / "evidence-package-staging"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True)
    
    # Copy thesis-final artifacts and manifest
    shutil.copytree(thesis_final_dir, staging_dir / "thesis-final")
    
    # Copy statistical analysis
    shutil.copytree(summaries_dir, staging_dir / "analysis")
    
    # We do not copy the raw runs here due to size/LFS, we just package the summaries and artifacts.
    # The raw runs are version controlled in results/runs/FINAL-*
    
    archive_path = repo_root / "results" / "thesis_evidence_package"
    shutil.make_archive(str(archive_path), 'zip', str(staging_dir))
    
    shutil.rmtree(staging_dir)
    print(f"Evidence package created: {archive_path.name}.zip")
    return 0

if __name__ == "__main__":
    sys.exit(main())
