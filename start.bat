@echo off
REM OpenBB Mobile API - Windows Start Script

echo Starting OpenBB Mobile API...
echo.

REM Check if conda environment exists
conda env list | findstr "openbb" >nul
if errorlevel 1 (
    echo Error: 'openbb' conda environment not found!
    echo Please create it first: conda create -n openbb python=3.11
    pause
    exit /b 1
)

REM Activate conda environment
call conda activate openbb

REM Change to script directory
cd /d "%~dp0"

REM Check if port 8007 is in use
netstat -ano | findstr ":8007" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo Warning: Port 8007 is already in use!
    echo Please close the application using that port.
    pause
    exit /b 1
)

REM Start the API
echo Starting API on http://localhost:8007
echo Docs: http://localhost:8007/docs
echo.
echo Press Ctrl+C to stop
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8007 --reload

pause
