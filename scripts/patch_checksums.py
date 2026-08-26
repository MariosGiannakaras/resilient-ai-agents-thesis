import json
import sys
from pathlib import Path
import hashlib

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    runs_dir = repo_root / "results" / "runs"
    
    for d in runs_dir.iterdir():
        if d.is_dir() and d.name.startswith("FINAL-"):
            # Update manifest.json
            manifest_path = d / "manifest.json"
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                payload_files = [
                    p for p in d.iterdir()
                    if p.is_file() and p.name not in {"manifest.json", "checksums.sha256", "FINALIZED"}
                ]
                
                manifest["files"] = {
                    p.name: {"sha256": sha256_file(p), "size_bytes": p.stat().st_size}
                    for p in sorted(payload_files)
                }
                
                # Write back manifest.json with LF
                manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
                
            # Update checksums.sha256
            checksum_lines = []
            for p in sorted(d.iterdir()):
                if p.is_file() and p.name not in {"checksums.sha256", "FINALIZED"}:
                    checksum_lines.append(f"{sha256_file(p)}  {p.name}")
            
            checksums_path = d / "checksums.sha256"
            checksums_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8", newline="\n")
            print(f"Patched checksums for {d.name}")
            
    return 0

if __name__ == "__main__":
    sys.exit(main())
