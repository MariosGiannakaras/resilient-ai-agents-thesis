@echo off
REM One-click launcher for the local native thesis application (REQ-APP-014).

setlocal
set REPO_ROOT=%~dp0
cd /d "%REPO_ROOT%"

where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH.
    echo Install the validated thesis Python environment tooling before running the repository launcher.
    exit /b 1
)

set THESIS_APP_BROWSER_MODE=
uv run --locked resilient-agents-app
if %ERRORLEVEL% neq 0 (
    echo ERROR: the thesis application failed to start.
    exit /b 1
)
