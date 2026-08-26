import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest

def main():
    repo_root = Path(__file__).resolve().parents[1]
    
    if str(repo_root / "src") not in sys.path:
        sys.path.insert(0, str(repo_root / "src"))
        
    print("Starting T-511 Comprehensive UI Validation...")
    
    log_path = repo_root / "results" / "t511_ui_validation_log.txt"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    app_dir = repo_root / "src" / "app"
    pages_dir = app_dir / "pages"
    
    files_to_test = [app_dir / "main.py"]
    if pages_dir.exists():
        files_to_test.extend(sorted(pages_dir.glob("*.py")))
        
    with log_path.open("w", encoding="utf-8") as f:
        f.write("T-511 COMPREHENSIVE UI VALIDATION LOG\n")
        f.write("=======================================\n\n")
        
        for file_path in files_to_test:
            f.write(f"TESTING {file_path.name}:\n")
            print(f"Testing {file_path.name}...")
            
            at = AppTest.from_file(str(file_path))
            try:
                at.run(timeout=10)
            except Exception as e:
                f.write(f"EXCEPTION DURING EXECUTION: {e}\n\n")
                print(f"Failed executing {file_path.name}: {e}")
                return 1
                
            if at.exception:
                f.write(f"APP CRASHED ON STARTUP: {at.exception}\n\n")
                print(f"App crashed on {file_path.name}: {at.exception}")
                return 1
                
            f.write("SUCCESS: Rendered cleanly.\n")
            for markdown in at.markdown:
                f.write(f"  - Markdown: {repr(markdown.value)[:100]}\n")
            for warning in at.warning:
                f.write(f"  - Warning: {warning.value}\n")
            for error in at.error:
                f.write(f"  - Error: {error.value}\n")
            for info in at.info:
                f.write(f"  - Info: {info.value}\n")
                
            f.write("\n")
            
        f.write("\nSUCCESS: All pages validated successfully without exceptions.\n")
        f.write("\nNOTE: Human smoke test remains inherently required for subjective UX factors.\n")
        
    print(f"UI validation log written to {log_path.relative_to(repo_root)}")
    print("T-511 objective validation successfully simulated.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
