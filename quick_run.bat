@echo off
setlocal
cd /d "%~dp0"

set "VENV_DIR=.venv"
set "HOST=127.0.0.1:8000"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run start_python.bat first.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

echo [INFO] Starting Django development server at http://%HOST%/
echo [INFO] Press CTRL-BREAK to stop the server

python manage.py runserver %HOST%
goto :eof