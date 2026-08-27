@echo off
REM One-click launcher for the local thesis application (REQ-APP-014).

setlocal
set REPO_ROOT=%~dp0
cd /d "%REPO_ROOT%"

if not exist "frontend\dist\index.html" (
    echo ERROR: frontend\dist\index.html is missing.
    echo This checkout does not contain the prebuilt thesis application frontend.
    echo Restore or build the validated frontend artifact before normal application use.
    exit /b 1
)

where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH.
    exit /b 1
)

uv run uvicorn app.main:app --app-dir src --host 127.0.0.1 --port 8501
if %ERRORLEVEL% neq 0 (
    echo ERROR: the thesis application failed to start.
    exit /b 1
)
