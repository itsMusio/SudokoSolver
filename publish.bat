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

set "REQ_REPORT=%TEMP%\sudoku_solver_build_requirements_%RANDOM%.json"

echo %INFO%Checking build requirements...%RESET%
"venv\Scripts\python.exe" -m pip install --dry-run --report "%REQ_REPORT%" -r build-requirements.txt >nul 2>nul
if errorlevel 1 (
    echo %WARN%Build requirements check failed. Installing all build requirements...%RESET%
    goto install_build_requirements
)

"venv\Scripts\python.exe" -c "import json, sys; data=json.load(open(r'%REQ_REPORT%', encoding='utf-8')); sys.exit(1 if data.get('install') else 0)"
if errorlevel 1 (
    echo %WARN%At least one build requirement is missing. Installing all build requirements...%RESET%
    goto install_build_requirements
)

echo %SUCCESS%Build requirements are already installed.%RESET%
goto publish_app

:install_build_requirements
echo %WARN%Installing build requirements...%RESET%
"venv\Scripts\python.exe" -m pip install -r build-requirements.txt
if errorlevel 1 (
    echo %ERROR%Failed to install build requirements.%RESET%
    if exist "%REQ_REPORT%" del "%REQ_REPORT%"
    pause
    exit /b 1
)
echo %SUCCESS%Build requirements installed successfully.%RESET%

:publish_app
if exist "%REQ_REPORT%" del "%REQ_REPORT%"

echo %LAUNCH%Publishing Sudoku Solver executable...%RESET%
"venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onefile --windowed --name SudokuSolver main.py
if errorlevel 1 (
    echo %ERROR%Publishing failed.%RESET%
    pause
    exit /b 1
)

echo %SUCCESS%Published successfully: dist\SudokuSolver.exe%RESET%
pause

endlocal
