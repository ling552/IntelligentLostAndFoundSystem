@echo off
setlocal
cd /d "%~dp0"

set "ENV_NAME=intelligent-lostfound"
set "HOST=127.0.0.1:8000"

for /f "delims=" %%i in ('conda info --base 2^>nul') do set "CONDA_BASE=%%i"
if not defined CONDA_BASE (
    echo [ERROR] Conda was not found. Please install Miniconda or Anaconda first.
    pause
    exit /b 1
)

set "CONDA_BAT=%CONDA_BASE%\condabin\conda.bat"
if not exist "%CONDA_BAT%" (
    echo [ERROR] conda.bat was not found: %CONDA_BAT%
    pause
    exit /b 1
)

call "%CONDA_BAT%" run -n %ENV_NAME% python --version >nul 2>nul
if errorlevel 1 (
    echo [INFO] Conda environment %ENV_NAME% does not exist. Creating it now...
    if exist "environment.yml" (
        call "%CONDA_BAT%" env create -f environment.yml
    ) else (
        call "%CONDA_BAT%" create -n %ENV_NAME% python=3.10 -y
        if errorlevel 1 goto :failed
        call "%CONDA_BAT%" run -n %ENV_NAME% python -m pip install -r requirements.txt
    )
    if errorlevel 1 goto :failed
) else (
    echo [INFO] Conda environment %ENV_NAME% already exists. Updating dependencies...
    if exist "environment.yml" (
        call "%CONDA_BAT%" env update -n %ENV_NAME% -f environment.yml --prune
        if errorlevel 1 goto :failed
    ) else (
        call "%CONDA_BAT%" run -n %ENV_NAME% python -m pip install -r requirements.txt
        if errorlevel 1 goto :failed
    )
)

echo [INFO] Running database migrations...
call "%CONDA_BAT%" run -n %ENV_NAME% python manage.py migrate
if errorlevel 1 goto :failed

echo [INFO] Starting Django development server at http://%HOST%/
call "%CONDA_BAT%" run -n %ENV_NAME% python manage.py runserver %HOST%
goto :eof

:failed
echo [ERROR] Startup failed. Please review the output above.
pause
exit /b 1
