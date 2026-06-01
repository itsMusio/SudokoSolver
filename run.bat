@echo off
setlocal

cd /d "%~dp0"

for /f "delims=" %%A in ('powershell -NoProfile -Command "[char]27"') do set "ESC=%%A"
set "RESET=%ESC%[0m"
set "INFO=%ESC%[36m"
set "WARN=%ESC%[33m"
set "SUCCESS=%ESC%[32m"
set "ERROR=%ESC%[31m"
set "LAUNCH=%ESC%[35m"

if not exist "venv\Scripts\python.exe" (
    echo %WARN%Creating virtual environment...%RESET%
    py -m venv venv
    if errorlevel 1 (
        echo %ERROR%Failed to create virtual environment.%RESET%
        pause
        exit /b 1
    )
)

set "REQ_REPORT=%TEMP%\sudoku_solver_requirements_%RANDOM%.json"

echo %INFO%Checking requirements...%RESET%
"venv\Scripts\python.exe" -m pip install --dry-run --report "%REQ_REPORT%" -r requirements.txt >nul 2>nul
if errorlevel 1 (
    echo %WARN%Requirements check failed. Installing all requirements...%RESET%
    goto install_requirements
)

"venv\Scripts\python.exe" -c "import json, sys; data=json.load(open(r'%REQ_REPORT%', encoding='utf-8')); sys.exit(1 if data.get('install') else 0)"
if errorlevel 1 (
    echo %WARN%At least one requirement is missing. Installing all requirements...%RESET%
    goto install_requirements
)

echo %SUCCESS%Requirements are already installed.%RESET%
goto start_app

:install_requirements
echo %WARN%Installing requirements...%RESET%
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo %ERROR%Failed to install requirements.%RESET%
    if exist "%REQ_REPORT%" del "%REQ_REPORT%"
    pause
    exit /b 1
)
echo %SUCCESS%Requirements installed successfully.%RESET%

:start_app
if exist "%REQ_REPORT%" del "%REQ_REPORT%"

echo %LAUNCH%Starting Sudoku Solver...%RESET%
"venv\Scripts\python.exe" main.py

endlocal
