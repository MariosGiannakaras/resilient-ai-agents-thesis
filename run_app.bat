@echo off
setlocal

REM Repository-checkout launcher for the T-534 PySide6 desktop application.
REM Scientific execution remains owned by the validated Python backend.

set "REPO_ROOT=%~dp0"
cd /d "%REPO_ROOT%" || (
    echo ERROR: Could not open repository root: "%REPO_ROOT%"
    exit /b 1
)

where uv >nul 2>&1
if errorlevel 1 (
    echo ERROR: uv is not installed or not available on PATH.
    echo Install uv, then double-click run_app.bat again.
    exit /b 1
)

if not exist "pyproject.toml" (
    echo ERROR: pyproject.toml was not found in "%REPO_ROOT%".
    echo Run this launcher from a normal resilient-ai-agents-thesis repository checkout.
    exit /b 1
)

if not exist "requirements\application-ui.txt" (
    echo ERROR: requirements\application-ui.txt is missing.
    exit /b 1
)

echo Preparing locked thesis environment...
uv sync --locked --group gridworld-prototype --no-progress
if errorlevel 1 (
    echo ERROR: Failed to restore the locked Python environment.
    exit /b 1
)

echo Preparing pinned PySide6 application overlay...
uv pip install --python ".venv\Scripts\python.exe" --requirement "requirements\application-ui.txt"
if errorlevel 1 (
    echo ERROR: Failed to install the pinned application UI overlay.
    exit /b 1
)

set "PYTHONPATH=%REPO_ROOT%src"
echo Starting Resilient AI Agents...
uv run --no-sync python -m resilient_agents.desktop
set "APP_EXIT=%ERRORLEVEL%"
if not "%APP_EXIT%"=="0" (
    echo ERROR: The desktop application exited with code %APP_EXIT%.
)

endlocal & exit /b %APP_EXIT%
