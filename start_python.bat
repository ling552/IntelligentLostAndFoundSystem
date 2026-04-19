@echo off
setlocal
cd /d "%~dp0"

set "VENV_DIR=.venv"
set "HOST=127.0.0.1:8000"
set "PYTHON_CMD=python"
set "PYTHON_LABEL=python"

where py >nul 2>nul
if not errorlevel 1 (
    py -3.10 --version >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=py -3.10"
        set "PYTHON_LABEL=py -3.10"
    )
)

call %PYTHON_CMD% --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] No usable Python interpreter was found.
    echo [ERROR] Please install Python 3.10, 3.11, or 3.12 and try again.
    pause
    exit /b 1
)

for /f %%i in ('call %PYTHON_CMD% -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set "PYTHON_VERSION=%%i"
if not "%PYTHON_VERSION%"=="3.10" if not "%PYTHON_VERSION%"=="3.11" if not "%PYTHON_VERSION%"=="3.12" (
    echo [ERROR] Detected %PYTHON_LABEL% ^(%PYTHON_VERSION%^) which is not recommended for this project.
    echo [ERROR] Please use Python 3.10, 3.11, or 3.12 and run this script again.
    pause
    exit /b 1
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [INFO] Local virtual environment %VENV_DIR% was not found. Creating it now...
    call %PYTHON_CMD% -m venv "%VENV_DIR%"
    if errorlevel 1 goto :failed
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 goto :failed

echo [INFO] Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
if errorlevel 1 goto :failed
python -m pip install -r requirements.txt
if errorlevel 1 goto :failed

echo [INFO] Running database migrations...
python manage.py migrate
if errorlevel 1 goto :failed

echo [INFO] Starting Django development server at http://%HOST%/
python manage.py runserver %HOST%
goto :eof

:failed
echo [ERROR] Startup failed. Please review the output above.
pause
exit /b 1
