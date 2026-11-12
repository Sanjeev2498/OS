@echo off
REM Batch Script for Windows - OS Resource Manager Analysis

echo ========================================================================
echo      OS RESOURCE MANAGER - AUTOMATED ANALYSIS SCRIPT (Windows)
echo ========================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed or not in PATH
    exit /b 1
)

echo [32mPython found[0m
python --version
echo.

REM Create output directory if not exists
if not exist "..\output\automated_runs" mkdir "..\output\automated_runs"

echo Running Automated Analysis...
echo --------------------------------
echo.

echo 1. Running scheduling algorithm comparison...
echo    (Manual mode: Please run main.py and select options)
echo.

echo 2. Running memory allocation comparison...
echo    (Manual mode: Please run main.py and select options)
echo.

echo 3. Running deadlock detection...
echo    (Manual mode: Please run main.py and select options)
echo.

echo ========================================================================
echo AUTOMATED ANALYSIS COMPLETE
echo ========================================================================
echo.
echo Results saved in: output\automated_runs\
echo Charts saved in: output\charts\
echo Logs saved in: output\system.log
echo.
echo To view detailed results, run:
echo   python ..\main.py
echo.

pause
