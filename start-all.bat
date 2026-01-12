@echo off
REM AI Disease Detection Platform - Windows Startup Script
REM This script starts both frontend and backend services

echo ========================================
echo AI Disease Detection Platform
echo Starting Frontend and Backend Services
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/5] Checking backend dependencies...
cd ai-backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and check dependencies
call venv\Scripts\activate.bat
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing backend dependencies... (this may take 5-10 minutes)
    pip install -r requirements.txt
)

echo.
echo [2/5] Checking frontend dependencies...
cd ..\ai-disease-ui

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies... (this may take 3-5 minutes)
    call npm install
)

echo.
echo [3/5] Starting Backend Server...
cd ..\ai-backend

REM Start backend in a new window
start "AI Backend Server" cmd /k "venv\Scripts\activate.bat && python -m app.main"

REM Wait for backend to start
echo Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

echo.
echo [4/5] Starting Frontend Server...
cd ..\ai-disease-ui

REM Start frontend in a new window
start "AI Frontend Server" cmd /k "npm run dev"

echo.
echo [5/5] Opening application in browser...
timeout /t 8 /nobreak >nul

REM Open browser
start http://localhost:3000

echo.
echo ========================================
echo Successfully Started!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Two terminal windows have opened:
echo   1. Backend Server (Python)
echo   2. Frontend Server (Node.js)
echo.
echo To stop the servers:
echo   - Close both terminal windows
echo   - Or press Ctrl+C in each window
echo.
echo Press any key to exit this window...
pause >nul
