import sys
import json
from pathlib import Path
from streamlit.testing.v1 import AppTest

def main():
    repo_root = Path(__file__).resolve().parents[1]
    
    if str(repo_root / "src") not in sys.path:
        sys.path.insert(0, str(repo_root / "src"))
        
    print("Starting T-511 Post-Execution UI Validation...")
    
    # We will test the main app
    app_path = repo_root / "src" / "app" / "main.py"
    if not app_path.exists():
        print(f"App not found at {app_path}")
        return 1
        
    at = AppTest.from_file(str(app_path))
    at.run(timeout=10)
    
    assert not at.exception, f"App crashed on startup: {at.exception}"
    
    # Save a representation of the UI to a durable log
    log_path = repo_root / "results" / "t511_ui_validation_log.txt"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with log_path.open("w", encoding="utf-8") as f:
        f.write("T-511 POST-EXECUTION UI VALIDATION LOG\n")
        f.write("========================================\n\n")
        f.write("MAIN PAGE RENDER:\n")
        for markdown in at.markdown:
            f.write(f"- Markdown: {markdown.value}\n")
            
        f.write("\nSUCCESS: The application started cleanly without exceptions.\n")
        
    print("UI validation log written to results/t511_ui_validation_log.txt")
    print("T-511 objective validation successfully simulated.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
