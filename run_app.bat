@echo off
REM Execute the Streamlit UI dashboard
REM Required by REQ-APP-014

set REPO_ROOT=%~dp0
cd /d "%REPO_ROOT%"

REM Check if uv is available
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo uv is not installed or not in PATH. Please install uv.
    exit /b 1
)

REM Run the Streamlit app
uv run streamlit run src/app/main.py
